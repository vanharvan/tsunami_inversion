import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# USER SETTINGS
# -------------------------
station_code = "21415"
input_file = f"./sealevel/{station_code}.txt"

# Earthquake origin time
eq_origin = pd.to_datetime("2025-07-29 23:24:52", utc=True)

# Plot window
start_time = eq_origin - pd.Timedelta(hours=24)
end_time = eq_origin + pd.Timedelta(hours=24)

poly_order = 4

# -------------------------
# READ & CLEAN DATA
# -------------------------
df = pd.read_csv(input_file, sep=";")

df["time_utc"] = pd.to_datetime(df["time_utc"], utc=True)
df["sealevel_m"] = pd.to_numeric(df["sealevel_m"], errors="coerce")

# Remove missing / bad values
df = df[df["sealevel_m"] != 9999.0]
df.dropna(subset=["sealevel_m"], inplace=True)

# Select time window
df_plot = df[
    (df["time_utc"] >= start_time) &
    (df["time_utc"] <= end_time)
].copy()

df_plot["time_min_from_eq"] = (
    df_plot["time_utc"] - eq_origin
).dt.total_seconds() / 60.0

# -------------------------
# POLYNOMIAL DETIDING
# -------------------------

# Convert time to numeric (hours since start)
t0 = df_plot["time_utc"].iloc[0]
time_hours = (df_plot["time_utc"] - t0).dt.total_seconds() / 3600.0

# Polynomial fit (order 2)
coeffs = np.polyfit(time_hours, df_plot["sealevel_m"], poly_order)
tide_fit = np.polyval(coeffs, time_hours)

# Detided signal
df_plot["tide_poly"] = tide_fit
df_plot["sealevel_detided"] = df_plot["sealevel_m"] - tide_fit

# -------------------------
# PLOTTING
# -------------------------
plt.figure(figsize=(12, 7))

# Raw sea level
plt.subplot(2, 1, 1)
plt.plot(df_plot["time_utc"], df_plot["sealevel_m"], linewidth=1, label="Raw Sea Level")
plt.plot(df_plot["time_utc"], df_plot["tide_poly"], linewidth=2, label="Polynomial Tide")
plt.axvline(eq_origin, linewidth=2, color='red', label="EQ Origin")
plt.title(f"DART {station_code}")
plt.xlabel("Time (UTC)")
plt.ylabel("amplitude (m)")
plt.legend()
plt.grid(alpha=0.5)

# Detided signal
plt.subplot(2, 1, 2)
plt.plot(
    df_plot["time_min_from_eq"],
    df_plot["sealevel_detided"],
    linewidth=1,
    label="Sea Level"
)

plt.axvline(0, linewidth=2, color='red', label="EQ Origin")
plt.title("Detided Sea Level")
plt.xlabel("Time (minutes)")
plt.ylabel("amplitude (m)")
plt.legend()
plt.grid(alpha=0.5)

plt.tight_layout()
plt.show()
