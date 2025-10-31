
import pandas as pd
from pathlib import Path

IN_CSV = Path("sample_results/scalability_input.csv")
OUT_CSV = Path("results/scalability_output.csv")
OUT_CSV.parent.mkdir(exist_ok=True)

df = pd.read_csv(IN_CSV)
df["eficiencia_percent"] = (df["throughput_real"] / df["throughput_ideal"] * 100).round(2)
df.to_csv(OUT_CSV, index=False)
print(df)
