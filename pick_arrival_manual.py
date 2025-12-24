import pandas as pd
import matplotlib.pyplot as plt

station_code = "32413"
input_file = f"./sealevel/{station_code}.txt"

# 1. Load Data
df = pd.read_csv(input_file, sep=";")
df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
df["sealevel_m"] = pd.to_numeric(df["sealevel_m"], errors="coerce")

# 2. Clean Data
df = df[df["sealevel_m"] != 9999.0] 
df.dropna(subset=["sealevel_m"], inplace=True)

# A. Calculate Sampling Rate automatically
# (This ensures the filter works whether data is 1-min or 15-sec interval)
if len(df) > 1:
    dt_seconds = (df["time_utc"].iloc[1] - df["time_utc"].iloc[0]).total_seconds()
else:
    dt_seconds = 60 # Default fallback

# B. Define Filter Window (2 Hours)
# Tides are slow (>12h), Tsunamis are fast (<1h). A 2h window separates them.
window_hours = 2
window_int = int((window_hours * 3600) / dt_seconds)

# C. Apply Filter
# This creates a smooth curve of the tide
df["tide_background"] = df["sealevel_m"].rolling(window=window_int, center=True, min_periods=1).mean()

# D. Calculate Residual (The Tsunami)
df["tsunami_waveform"] = df["sealevel_m"] - df["tide_background"]

eq_origin = pd.to_datetime("2025-07-29 23:24:52", utc=True)
start_time = pd.to_datetime("2025-07-29 00:00:00", utc=True)
end_time = eq_origin + pd.Timedelta(hours=72)

# ---- ARRIVAL PICKING ------
#arrival_time = pd.to_datetime("2025-07-29 23:32:00", utc=True)

df_plot = df[(df["time_utc"] >= start_time) & (df["time_utc"] <= end_time)].copy()

# --- PLOTTING ---
plt.figure(figsize=(12, 8))
plt.plot(df_plot["time_utc"], df_plot["tsunami_waveform"], color='black', linewidth=1, label="Tsunami Waveform")
plt.axvline(x=eq_origin, color='red', linestyle='-', linewidth=2, label="EQ Origin")
#plt.axvline(x=arrival_time, color='blue', linestyle='-', linewidth=2, label="Tsunami Arrival")
y_pos = df_plot["tsunami_waveform"].max() * 0.8
#plt.text(x=arrival_time, 
#         y=y_pos, 
#         s=f" Arrival\n {arrival_time.strftime('%H:%M:%S')}", 
#         color='blue', 
#         fontsize=10, 
#         fontweight='bold',
#         ha='left',   # horizontal alignment: left of the anchor point
#         va='bottom') # vertical alignment: bottom of the anchor point
plt.title(f"DART - {station_code}")
plt.xlabel("Time (UTC)")
plt.ylabel("Amplitude (m)")
plt.legend(loc='upper right')
plt.grid(True, alpha=0.5)

plt.tight_layout()
plt.show()
#output_filename = f"./sealevel/{station_code}_waveform.png"
#plt.savefig(output_filename, dpi=300, bbox_inches='tight')
#print(f"Plot saved successfully to: {output_filename}")