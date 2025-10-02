#!/usr/bin/env python3
"""WebSocket server for real-time sensor data updates."""

import asyncio
import json
import logging
from datetime import datetime
from typing import Set

import websockets
from websockets.server import WebSocketServerProtocol

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensorWebSocketServer:
    """WebSocket server for real-time sensor data."""
    
    def __init__(self):
        self.clients: Set[WebSocketServerProtocol] = set()
        self.sensor_data = {}
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Register a new client connection."""
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send current sensor data to new client
        if self.sensor_data:
            await websocket.send(json.dumps({
                'type': 'sensor_data',
                'data': self.sensor_data
            }))
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Unregister a client connection."""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_sensor_data(self, sensor_data: dict):
        """Broadcast sensor data to all connected clients."""
        if not self.clients:
            return
        
        message = json.dumps({
            'type': 'sensor_data',
            'data': sensor_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Send to all clients, remove disconnected ones
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Remove disconnected clients
        for client in disconnected:
            self.clients.discard(client)
    
    async def broadcast_alert(self, alert_data: dict):
        """Broadcast alert to all connected clients."""
        if not self.clients:
            return
        
        message = json.dumps({
            'type': 'alert',
            'data': alert_data,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Send to all clients
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
        
        # Remove disconnected clients
        for client in disconnected:
            self.clients.discard(client)
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        """Handle client connection."""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received: {message}")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
    
    async def handle_message(self, websocket: WebSocketServerProtocol, data: dict):
        """Handle incoming message from client."""
        message_type = data.get('type')
        
        if message_type == 'subscribe':
            # Client wants to subscribe to specific farm data
            farm_id = data.get('farm_id')
            logger.info(f"Client subscribed to farm {farm_id}")
            
        elif message_type == 'ping':
            # Respond to ping with pong
            await websocket.send(json.dumps({'type': 'pong'}))
        
        else:
            logger.warning(f"Unknown message type: {message_type}")


# Global server instance
server = SensorWebSocketServer()


async def simulate_sensor_data():
    """Simulate real-time sensor data for demo purposes."""
    import random
    
    while True:
        # Generate mock sensor data
        sensor_data = {
            'farm_1': {
                'temperature': round(22 + random.gauss(0, 1), 1),
                'humidity': round(65 + random.gauss(0, 5), 1),
                'ph': round(6.2 + random.gauss(0, 0.1), 2),
                'nutrients': round(950 + random.gauss(0, 25), 0)
            },
            'farm_2': {
                'temperature': round(24 + random.gauss(0, 1), 1),
                'humidity': round(70 + random.gauss(0, 5), 1),
                'ph': round(6.0 + random.gauss(0, 0.1), 2),
                'nutrients': round(900 + random.gauss(0, 30), 0)
            },
            'farm_3': {
                'temperature': round(23 + random.gauss(0, 1), 1),
                'humidity': round(60 + random.gauss(0, 5), 1),
                'ph': round(6.3 + random.gauss(0, 0.1), 2),
                'nutrients': round(980 + random.gauss(0, 20), 0)
            }
        }
        
        # Broadcast to all clients
        await server.broadcast_sensor_data(sensor_data)
        
        # Wait 5 seconds before next update
        await asyncio.sleep(5)


async def main():
    """Start the WebSocket server."""
    logger.info("Starting WebSocket server on ws://localhost:8765")
    
    # Start the WebSocket server
    start_server = websockets.serve(server.handle_client, "localhost", 8765)
    
    # Start sensor data simulation
    sensor_task = asyncio.create_task(simulate_sensor_data())
    
    # Run both tasks concurrently
    await asyncio.gather(start_server, sensor_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("WebSocket server stopped")
