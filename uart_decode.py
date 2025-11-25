import pandas as pd

CSV_FILE = "afe_sim.csv"
STOP_TIME = 2_110_000_000     # safe upper bound slightly above max


print("Loading CSV...")
df = pd.read_csv(CSV_FILE)

print("Columns in CSV:", df.columns)

# Trim to requested time window
df = df[df["time_ns"] <= STOP_TIME]
print(f"Processing rows up to {STOP_TIME} ns → {len(df)} rows")

time = df["time_ns"].values
tx   = df["uart_tx"].values

BIT_PERIOD = 8680  # ns for 115200 baud (approx)
HALF_BIT   = BIT_PERIOD // 2

decoded_bytes = []
i = 0
n = len(df)

print("\n=== UART DECODE START ===\n")

while i < n - 12:
    # Detect start bit: falling edge 1→0
    if tx[i] == 1 and tx[i+1] == 0:
        t0 = time[i+1]  # start of start bit

        # Sample 8 data bits + 1 stop bit
        bits = []
        for b in range(1, 10):
            sample_time = t0 + b * BIT_PERIOD - HALF_BIT
            # find nearest sample index
            idx = (abs(time - sample_time)).argmin()
            bits.append(tx[idx])

        stop_bit = bits[-1]
        data_bits = bits[:-1]

        if stop_bit != 1:
            print("Frame error.")
        else:
            val = 0
            for k, bit in enumerate(data_bits):
                val |= (bit << k)
            decoded_bytes.append(val)
            print(f"Byte decoded: 0x{val:02X}")

        # advance search window
        i += int((10 * BIT_PERIOD) / (time[1] - time[0])) // 2
    else:
        i += 1

print("\n=== UART DECODE COMPLETE ===")
print("Decoded bytes:", decoded_bytes)
