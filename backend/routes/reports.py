from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.export_reports import export_farm_readings_csv, export_farm_summary_pdf

reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/reports")


@reports_bp.get("/farms/<int:farm_id>/readings.csv")
@jwt_required(optional=True)
def download_farm_readings_csv(farm_id: int):
    hours = int(request.args.get("hours", 24))
    return export_farm_readings_csv(farm_id, hours)


@reports_bp.get("/farms/<int:farm_id>/summary.pdf")
@jwt_required(optional=True)
def download_farm_summary_pdf(farm_id: int):
    hours = int(request.args.get("hours", 24))
    return export_farm_summary_pdf(farm_id, hours)
