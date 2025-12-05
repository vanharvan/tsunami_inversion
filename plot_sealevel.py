import pandas as pd
import matplotlib.pyplot as plt

station_code = "nksk"
input_file = f"{station_code}.txt"

df = pd.read_csv(input_file, sep=";")
df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
df["sealevel_m"] = pd.to_numeric(df["sealevel_m"], errors="coerce")

plt.figure(figsize=(12, 5))
plt.plot(df["time_utc"], df["sealevel_m"], linewidth=1)
plt.title(f"Sea Level Time Series - {station_code}")
plt.xlabel("Time (UTC)")
plt.ylabel("Sea Level (m)")
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)

plt.show()