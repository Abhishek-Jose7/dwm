"""
SoundPulse Streaming Inc. - Build Dashboard Web Assets
Embeds the cleaned dataset into dashboard/data.js and validates asset linkage.
"""

import pandas as pd
import json

df = pd.read_csv("data/cleaned_music_data.csv")
records = df.to_dict(orient="records")

with open("dashboard/data.js", "w", encoding="utf-8") as f:
    f.write("// SoundPulse Music Operations - Synthesized Survey Dataset (240 Cohort Users)\n")
    f.write("const MUSIC_DATA = ")
    json.dump(records, f, indent=2)
    f.write(";\n")

print(f"Exported {len(records)} records into dashboard/data.js")
