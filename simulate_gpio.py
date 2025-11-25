# simulate_gpio.py
# Usage: python3 simulate_gpio.py
# Simulates ISR-like handling of rising/falling edges from events.csv

import pandas as pd
import time
import os

FILE = "events.csv"
assert os.path.exists(FILE), f"{FILE} not found"

df = pd.read_csv(FILE)
if "time_s" not in df or "edge" not in df:
    raise ValueError("events.csv must have columns: time_s, edge")

df = df.sort_values("time_s").reset_index(drop=True)

led_on = False
rises = falls = 0

print("=== Simulated GPIO ISR ===")
for _, row in df.iterrows():
    ts = float(row["time_s"])
    edge = row["edge"].strip().lower()
    if edge == "rising":
        rises += 1
        led_on = True
        print(f"[{ts:8.4f}s] RISING  -> LED ON")
    elif edge == "falling":
        falls += 1
        led_on = False
        print(f"[{ts:8.4f}s] FALLING -> LED OFF")
    else:
        print(f"[{ts:8.4f}s] Unknown edge: {edge}")
    # tiny delay so the console is readable
    time.sleep(0.05)

print("\nSummary:")
print(f"  Rising edges : {rises}")
print(f"  Falling edges: {falls}")
print(f"  Final LED    : {'ON' if led_on else 'OFF'}")
print("Simulated Pi ISR behavior complete.")
