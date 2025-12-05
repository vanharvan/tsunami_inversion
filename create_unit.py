import pandas as pd
import os

path = "./all_unit_sources.csv"

df = pd.read_csv(path, dtype=str)
out_dir = "./unit_sources"
os.makedirs(out_dir, exist_ok=True)

# columns to write (exclude unit_source), keep original order, then add slip
cols = [c for c in df.columns if c != "unit_source"]

# write one text file per row, named <unit_source>.txt, no header, space-delimited,
# values = all columns except unit_source, plus slip=1 at end
for _, row in df.iterrows():
    unit = str(row["unit_source"]).strip()
    filename = os.path.join(out_dir, f"{unit}.txt")

    values = [(row[col] if pd.notna(row[col]) else "") for col in cols]
    values.append("1")  # slip value

    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(" ".join(values) + "\n")

print(f"Wrote {len(df)} files to {out_dir}")