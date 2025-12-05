import os
import requests
import pandas as pd
import sys
import re

station_code = "nksk"
period_days = "3"
endtime = "2025-08-01"

base = "https://www.ioc-sealevelmonitoring.org/bgraph.php"
params = {
    "code": station_code,
    "period": str(period_days),
    "output": "tab",
    "endtime": endtime
    }

full_url = requests.Request("GET", base, params=params).prepare()
print("Accessing URL:", full_url.url)
print("station code:", station_code, "|", " period (days):", period_days, "|", " endtime:", endtime)
print("Downloading data...\n")
      
response = requests.get(full_url.url, timeout=5)
raw_text = response.text

if re.search(r'Tide gauge.*?NO\s*DATA', raw_text, re.I) or re.search(r'Is\s+NO\s+DATA', raw_text, re.I):
    print(f"No data at the sea level for station {station_code}")
    sys.exit(0)

tmp_file = "raw_sealevel.txt"
with open(tmp_file, "w", encoding="utf-8") as f:
    f.write(raw_text)

tables = pd.read_html(tmp_file, header=None)
df = tables[0]
df = df.iloc[1:].reset_index(drop=True)
#df.columns = ["time", "prt", "prte"] ### adjust this ###
df.columns = ["time", "rad"]
df = df.fillna("NaN")
df.to_csv(tmp_file, sep=";", index=False)

df2 = pd.read_csv(tmp_file, sep=";")
df2 = df2.replace("NaN", pd.NA)
final_df = pd.DataFrame()
final_df["time_utc"] = df2["time"]
#final_df["sealevel_m"] = df2["prte"].fillna(df2["prt"]) ### adjust this ###
final_df["sealevel_m"] = df2["rad"]


os.remove(tmp_file)

final_df.to_csv(f"{station_code}.txt", sep=";", index=False)
print("\nData saved to :", f"{station_code}.txt")

