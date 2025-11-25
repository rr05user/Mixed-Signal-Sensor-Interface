# simulate_gpio_realtime.py
# Usage: python3 simulate_gpio_realtime.py [speed]
# Example: python3 simulate_gpio_realtime.py 2.0   (2x faster than real time)

import sys, time, os
import pandas as pd

FILE = "events.csv"
assert os.path.exists(FILE), f"{FILE} not found"

speed = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
assert speed > 0, "speed must be > 0"

df = pd.read_csv(FILE).sort_values("time_s").reset_index(drop=True)
if "time_s" not in df or "edge" not in df:
    raise ValueError("events.csv must have columns: time_s, edge")

t0 = float(df.iloc[0]["time_s"])
now_sim = t0
led_on = False
rises = falls = 0

print(f"=== Real-time GPIO playback (speed {speed}x) ===")
start_wall = time.time()

for _, row in df.iterrows():
    target = float(row["time_s"])
    # sleep for the delta / speed
    dt = (target - now_sim) / speed
    if dt > 0:
        time.sleep(dt)
    now_sim = target

    edge = row["edge"].strip().lower()
    if edge == "rising":
        led_on = True; rises += 1
        print(f"[{target:8.4f}s] RISING  -> LED ON")
    elif edge == "falling":
        led_on = False; falls += 1
        print(f"[{target:8.4f}s] FALLING -> LED OFF")
    else:
        print(f"[{target:8.4f}s] Unknown edge: {edge}")

elapsed = time.time() - start_wall
print("\nSummary:")
print(f"  Rising edges : {rises}")
print(f"  Falling edges: {falls}")
print(f"  Final LED    : {'ON' if led_on else 'OFF'}")
print(f"  Wall time    : {elapsed:.2f}s  (speed {speed}x)")
