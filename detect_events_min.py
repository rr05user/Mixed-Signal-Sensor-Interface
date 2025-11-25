# detect_events_min.py
# Usage: python3 detect_events_min.py
# Requires: pip install pandas numpy matplotlib

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # save plots to files (headless-friendly)
import matplotlib.pyplot as plt

fname = "AFE_transient.csv"
if not os.path.exists(fname):
    raise FileNotFoundError(f"Couldn't find {fname} in {os.getcwd()}")

# Load LTspice export: it's TAB-delimited per your head output
df = pd.read_csv(fname, sep="\t", comment="I", skip_blank_lines=True)

# Ensure exact column names exist
expected = ["time", "V(cmp_out)", "V(filt_out)", "V(vin_sensor)"]
missing = [c for c in expected if c not in df.columns]
if missing:
    raise ValueError(f"Missing columns {missing}. Found: {list(df.columns)}")

# Coerce to numeric
for c in expected:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=expected)

# Extract arrays
t    = df["time"].to_numpy()
vcmp = df["V(cmp_out)"].to_numpy()
vin  = df["V(vin_sensor)"].to_numpy()
vout = df["V(filt_out)"].to_numpy()

# Digitalize comparator around mid-rail (3.3V logic)
th = 1.65
logic = (vcmp > th).astype(int)

# Edge detection
rising_idx  = np.where((logic[1:] == 1) & (logic[:-1] == 0))[0] + 1
falling_idx = np.where((logic[1:] == 0) & (logic[:-1] == 1))[0] + 1

# Frequency & duty (if enough edges)
freq = np.nan
duty = np.nan
if len(rising_idx) >= 2:
    periods = np.diff(t[rising_idx])
    periods = periods[periods > 0]
    if periods.size:
        period = np.median(periods)
        freq = 1.0 / period
        # duty via median high time / period
        highs = []
        for r in rising_idx:
            f_after = falling_idx[falling_idx > r]
            if f_after.size == 0:
                break
            highs.append(t[f_after[0]] - t[r])
        if highs:
            duty = np.median(highs) * freq * 100.0

# Print summary
print("\n=== Event Detection Summary ===")
print(f"Samples:        {len(t)}")
print(f"Rising edges:   {len(rising_idx)}")
print(f"Falling edges:  {len(falling_idx)}")
if np.isfinite(freq):
    print(f"Approx freq:    {freq:.3f} Hz")
if np.isfinite(duty):
    print(f"Duty (median):  {duty:.1f}%")

# Save events
events = [{"time_s": float(t[i]), "edge": "rising"} for i in rising_idx] + \
         [{"time_s": float(t[i]), "edge": "falling"} for i in falling_idx]
events_df = pd.DataFrame(events).sort_values("time_s")
events_df.to_csv("events.csv", index=False)
print("Saved events.csv")

# Save plots
plt.figure(figsize=(9,4))
plt.plot(t, vin,  label="VIN_SENSOR")
plt.plot(t, vout, label="FILT_OUT")
plt.plot(t, vcmp, label="CMP_OUT")
plt.xlabel("Time (s)"); plt.ylabel("Voltage (V)")
plt.title("AFE Transient – Sensor → Filter → Comparator")
plt.legend(); plt.tight_layout()
plt.savefig("afe_waveforms.png", dpi=150)
print("Saved afe_waveforms.png")
