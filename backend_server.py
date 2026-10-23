from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="IoT Smart Irrigation Backend",
    description=(
        "Backend server handling IoT telemetry and database storage for smart"
        " irrigation."
    ),
)


# Initialize SQLite Database
def init_db():
  conn = sqlite3.connect("irrigation_backend.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone TEXT,
            crop TEXT,
            soil_moisture REAL,
            temperature REAL,
            humidity REAL,
            fault TEXT,
            timestamp TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()


class SensorData(BaseModel):
  zone: str
  crop: str
  soil_moisture: float
  temperature: float
  humidity: float
  fault: str


# API Endpoint 1: Receive data from IoT devices/simulators (POST)
@app.post("/telemetry")
def receive_telemetry(data: SensorData):
  conn = sqlite3.connect("irrigation_backend.db")
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO sensor_logs (zone, crop, soil_moisture, temperature,"
      " humidity, fault, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
      (
          data.zone,
          data.crop,
          data.soil_moisture,
          data.temperature,
          data.humidity,
          data.fault,
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      ),
  )
  conn.commit()
  conn.close()
  return {
      "status": "success",
      "message": f"Data for {data.zone} saved to database securely!",
  }


# API Endpoint 2: Fetch stored data for the dashboard (GET)
@app.get("/readings")
def get_readings():
  conn = sqlite3.connect("irrigation_backend.db")
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM sensor_logs ORDER BY id DESC LIMIT 15")
  rows = cursor.fetchall()
  conn.close()
  return [dict(row) for row in rows]