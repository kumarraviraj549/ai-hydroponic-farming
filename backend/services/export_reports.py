#!/usr/bin/env python3
"""Export utilities for generating CSV and PDF reports for farms and sensors."""
from __future__ import annotations

import csv
import io
from datetime import datetime, timedelta, timezone
from typing import List

from flask import Response
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from models import db, Farm, Sensor, SensorReading


def export_farm_readings_csv(farm_id: int, hours: int = 24) -> Response:
    """Export sensor readings for a farm as CSV for the last N hours."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "sensor_id", "sensor_name", "type", "unit", "value"])

    readings = (
        db.session.query(SensorReading, Sensor)
        .join(Sensor, Sensor.id == SensorReading.sensor_id)
        .filter(SensorReading.farm_id == farm_id, SensorReading.timestamp >= start)
        .order_by(SensorReading.timestamp.asc())
        .all()
    )

    for reading, sensor in readings:
        writer.writerow([
            reading.timestamp.isoformat(),
            sensor.id,
            sensor.name,
            sensor.sensor_type,
            sensor.unit,
            reading.value,
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=farm_{farm_id}_readings_{hours}h.csv"
        },
    )


def export_farm_summary_pdf(farm_id: int, hours: int = 24) -> Response:
    """Export a simple PDF summary report for a farm for the last N hours."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)

    farm: Farm | None = Farm.query.get(farm_id)
    if not farm:
        return Response("Farm not found", status=404)

    # Aggregate metrics
    sensors: List[Sensor] = Sensor.query.filter_by(farm_id=farm_id).all()
    readings_count = (
        SensorReading.query.filter(
            SensorReading.farm_id == farm_id, SensorReading.timestamp >= start
        ).count()
    )

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2 * cm, f"HydroAI Farm Summary: {farm.name}")

    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, height - 3 * cm, f"Location: {farm.location}")
    c.drawString(2 * cm, height - 3.6 * cm, f"Period: {start.isoformat()} to {end.isoformat()}")
    c.drawString(2 * cm, height - 4.2 * cm, f"Sensors: {len(sensors)}  |  Readings: {readings_count}")

    y = height - 5.5 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, y, "Sensors")
    y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    for s in sensors[:20]:
        c.drawString(2 * cm, y, f"- {s.name} ({s.sensor_type}, {s.unit}) thresholds: {s.min_threshold}-{s.max_threshold}")
        y -= 0.5 * cm
        if y < 3 * cm:
            c.showPage()
            y = height - 3 * cm

    c.showPage()
    c.save()

    buf.seek(0)
    return Response(
        buf.getvalue(),
        mimetype="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=farm_{farm_id}_summary_{hours}h.pdf"
        },
    )
