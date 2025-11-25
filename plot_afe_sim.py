# plot_afe_sim.py
# Works in WSL (no GUI). Saves afe_plot.png next to this script.

import os
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless backend for WSL/non-GUI
import matplotlib.pyplot as plt

# ---------- CONFIG: set one of these paths ----------
# If you saved the CSV into Downloads/ecenproj on Windows:
PATH_WINDOWS = r"C:\Users\rahul\Downloads\ecenproj\afe_sim.csv"
# The same file as seen from WSL:
PATH_WSL = "/mnt/c/Users/rahul/Downloads/ecenproj/afe_sim.csv"

# Pick the one that exists so you don't have to edit every time
csv_path = PATH_WSL if os.path.exists(PATH_WSL) else PATH_WINDOWS

if not os.path.exists(csv_path):
    print(f"[ERROR] CSV not found.\n  Tried:\n    {PATH_WSL}\n    {PATH_WINDOWS}")
    sys.exit(1)

print(f"[INFO] Reading: {csv_path}")
df = pd.read_csv(csv_path)

# ---------- Clean & validate ----------
df.columns = [c.strip().lower() for c in df.columns]
required = {"time_ns", "vin_code", "cmp_out", "logic_out"}
missing = required - set(df.columns)
if missing:
    print(f"[ERROR] CSV missing columns: {missing}\nColumns found: {df.columns.tolist()}")
    sys.exit(1)

# Coerce numerics, drop bad rows
for c in ["time_ns", "vin_code", "cmp_out", "logic_out"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna()

if df.empty:
    print("[ERROR] CSV parsed but has no valid rows after numeric coercion.")
    sys.exit(1)

# ---------- Prepare data ----------
time_ms = df["time_ns"].to_numpy() / 1e6
vin     = df["vin_code"].to_numpy()
cmp_o   = df["cmp_out"].to_numpy()
q       = df["logic_out"].to_numpy()

# Thresholds used in HDL (12-bit @ 3.3 V): HIGH=1510 (~1.22V), LOW=1460 (~1.18V)
TH_HIGH = 1510
TH_LOW  = 1460

print("[INFO] Head of data:")
print(df.head())

# ---------- Plot ----------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True)

# Top: Vin (ADC codes) with thresholds
ax1.plot(time_ms, vin, label="Vin (ADC code)", linewidth=1.5)
ax1.axhline(TH_HIGH, linestyle="--", linewidth=1.0, label="High Th ≈ 1510 (~1.22 V)")
ax1.axhline(TH_LOW,  linestyle="--", linewidth=1.0, label="Low Th  ≈ 1460 (~1.18 V)")
ax1.set_ylabel("ADC Code (0–4095)")
ax1.set_title("AFE Digital Comparator & Latch (Vivado Simulation)")
ax1.grid(True, alpha=0.3)
ax1.legend(loc="best")

# Bottom: logic signals (step plot, scaled for visibility)
ax2.step(time_ms, cmp_o, where="post", label="cmp_out", linewidth=1.5)
ax2.step(time_ms, q,     where="post", label="logic_out (latched)", linewidth=1.5)
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("Logic Level")
ax2.set_yticks([0, 1])
ax2.grid(True, alpha=0.3)
ax2.legend(loc="best")

plt.tight_layout()

# ---------- Save ----------
out_png = os.path.join(os.path.dirname(csv_path), "afe_plot.png")
plt.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
print(f"[OK] Plot saved to: {out_png}")


