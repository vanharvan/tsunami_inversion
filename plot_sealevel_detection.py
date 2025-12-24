import pandas as pd
import matplotlib.pyplot as plt

station_code = "21413"
input_file = f"./sealevel/{station_code}.txt"

# 1. Load & Clean Data
df = pd.read_csv(input_file, sep=";")
df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
df["sealevel_m"] = pd.to_numeric(df["sealevel_m"], errors="coerce")
df = df[df["sealevel_m"] != 9999.0] 
df.dropna(subset=["sealevel_m"], inplace=True)

# 2. Filter Tide (Rolling Mean)
if len(df) > 1:
    dt_seconds = (df["time_utc"].iloc[1] - df["time_utc"].iloc[0]).total_seconds()
else:
    dt_seconds = 60
window_int = int((2 * 3600) / dt_seconds) # 2 hour window

df["tide_background"] = df["sealevel_m"].rolling(window=window_int, center=True, min_periods=1).mean()
df["tsunami_waveform"] = df["sealevel_m"] - df["tide_background"]

# 3. Define Window & Slice
eq_origin = pd.to_datetime("2025-07-29 23:24:52", utc=True)
end_time = eq_origin + pd.Timedelta(hours=2) # Looking at first 2 hours
df_plot = df[(df["time_utc"] >= eq_origin) & (df["time_utc"] <= end_time)].copy()

# --- NEW: AUTOMATIC DETECTION ---

# A. Determine Max Height
max_height_val = df_plot["tsunami_waveform"].max()
max_height_time = df_plot["tsunami_waveform"].idxmax()
# Note: idxmax returns the index, so we need to fetch the time from that index if not indexed by time
# Since our index is likely integers 0..N, we do this:
max_row = df_plot.loc[df_plot["tsunami_waveform"] == max_height_val].iloc[0]
max_time = max_row["time_utc"]

# B. Determine Arrival Time (Threshold Method)
# We assume the wave arrives when the amplitude exceeds 2cm (0.02m)
# You can adjust this threshold based on how noisy your station is.
detection_threshold = 0.02 

# Get all rows where wave > threshold
arrival_candidates = df_plot[df_plot["tsunami_waveform"].abs() > detection_threshold]

if not arrival_candidates.empty:
    first_arrival_row = arrival_candidates.iloc[0]
    arrival_time = first_arrival_row["time_utc"]
    arrival_amp = first_arrival_row["tsunami_waveform"]
    arrival_str = arrival_time.strftime('%H:%M:%S')
    print(f"Computed Arrival: {arrival_str}")
else:
    arrival_time = None
    print("No arrival detected above threshold.")

# --- PLOTTING ---
plt.figure(figsize=(12, 6))

# Plot Waveform
plt.plot(df_plot["time_utc"], df_plot["tsunami_waveform"], color='black', linewidth=1, label="Waveform")

# 1. Mark Max Height
plt.scatter(max_time, max_height_val, color='red', s=50, zorder=5)
plt.text(max_time, max_height_val + 0.01, f" Max Height: {max_height_val:.3f}m", 
         color='red', fontweight='bold', ha='left')

# 2. Mark Arrival Time (if detected)
if arrival_time:
    plt.axvline(x=arrival_time, color='blue', linestyle='--', linewidth=1.5, label="Arrival Detected")
    plt.scatter(arrival_time, arrival_amp, color='blue', s=50, zorder=5)
    plt.text(arrival_time, arrival_amp - 0.03, f" Arrival\n {arrival_str}", 
             color='blue', fontweight='bold', ha='right', va='top')

# 3. Mark Threshold Lines (Visual Aid)
plt.axhline(y=detection_threshold, color='green', linestyle=':', alpha=0.5, label=f"Threshold (+/- {detection_threshold}m)")
plt.axhline(y=-detection_threshold, color='green', linestyle=':', alpha=0.5)

plt.axvline(x=eq_origin, color='gray', linestyle='-', linewidth=1, label="EQ Origin")
plt.title(f"Stations - {station_code}\nMax Height: {max_height_val:.2f}m | Arrival: {arrival_str if arrival_time else 'N/A'}")
plt.xlabel("Time (UTC)")
plt.ylabel("Amplitude (m)")
plt.legend(loc='upper right')
plt.grid(True, alpha=0.5)

output_filename = f"./sealevel/{station_code}_analysis.png"
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()