import argparse
import csv
import os
import random
import time


def generate_readings(ticks=500, interval=0.0, output_file="irrigation_data.csv"):
  crops = {
      "Zone 1: Wheat": {"moisture": 55.0, "temp": 22.0, "humidity": 60.0},
      "Zone 2: Sugarcane": {"moisture": 70.0, "temp": 28.0, "humidity": 75.0},
      "Zone 3: Cotton": {"moisture": 45.0, "temp": 32.0, "humidity": 50.0},
  }

  fieldnames = [
      "tick",
      "zone",
      "crop",
      "soil_moisture",
      "temperature",
      "humidity",
      "fault",
  ]

  print(
      f"[*] Starting IoT Sensor Simulator for {ticks} ticks. Saving to"
      f" {output_file}..."
  )

  with open(output_file, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for tick in range(1, ticks + 1):
      for zone_name, state in crops.items():
        crop_type = zone_name.split(":")[1].strip()

        # Normal small movements
        state["moisture"] += random.uniform(-0.5, 0.5)
        state["temp"] += random.uniform(-0.2, 0.2)
        state["humidity"] += random.uniform(-0.5, 0.5)

        fault = "none"
        if random.random() < 0.05:
          fault = random.choice([
              "pump_failure",
              "pipe_leakage",
              "dry_spell",
          ])

        if fault == "pump_failure":
          state["moisture"] -= 1.2
        elif fault == "pipe_leakage":
          state["moisture"] += 1.5
        elif fault == "dry_spell":
          state["moisture"] -= 2.0

        # Keep values inside safe limits
        state["moisture"] = max(10.0, min(100.0, state["moisture"]))
        state["temp"] = max(10.0, min(50.0, state["temp"]))
        state["humidity"] = max(20.0, min(99.0, state["humidity"]))

        writer.writerow({
            "tick": tick,
            "zone": zone_name,
            "crop": crop_type,
            "soil_moisture": round(state["moisture"], 2),
            "temperature": round(state["temp"], 2),
            "humidity": round(state["humidity"], 2),
            "fault": fault,
        })


if __name__ == "__main__":
  generate_readings()