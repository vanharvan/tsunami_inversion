import pandas as pd
import matplotlib.pyplot as plt

station_code = "21413"
input_file = f"./sealevel/{station_code}.txt"

df = pd.read_csv(input_file, sep=";")
df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
df["sealevel_m"] = pd.to_numeric(df["sealevel_m"], errors="coerce")

df = df[df["sealevel_m"] != 9999.0] 
df.dropna(subset=["sealevel_m"], inplace=True)

eq_origin = pd.to_datetime("2025-07-29 23:24:52", utc=True)
start_time = pd.to_datetime("2025-07-29 00:00:00", utc=True)
end_time = eq_origin + pd.Timedelta(hours=72)


df_plot = df[(df["time_utc"] >= start_time) & (df["time_utc"] <= end_time)].copy()


# --- PLOTTING ---
plt.figure(figsize=(12, 5))
plt.plot(df_plot["time_utc"], df_plot["sealevel_m"], color='black', linewidth=1, label="Tsunami Waveform")
plt.axvline(x=eq_origin, color='red', linestyle='-', linewidth=2, label="EQ Origin")
plt.title(f"DART - {station_code}")
plt.xlabel("Time (UTC)")
plt.ylabel("Sea Level (m)")
plt.legend(loc='upper right')
plt.grid(True, alpha=0.5)
plt.tight_layout()

plt.show()