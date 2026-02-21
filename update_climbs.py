#!/usr/bin/env python3
"""
update_climbs.py

Reads climbs.dta and updates the CLIMBS JSON array in index.html.
Run this after adding new climbs to the Stata file.

Usage:
    python update_climbs.py

Requires: pandas (pip install pandas)
"""

import pandas as pd
import json
import re
import sys
from pathlib import Path

# Paths relative to script location
script_dir = Path(__file__).parent
dta_path = script_dir / "climbs.dta"
html_path = script_dir / "index.html"

def main():
    # Check files exist
    if not dta_path.exists():
        print(f"Error: {dta_path} not found")
        sys.exit(1)
    if not html_path.exists():
        print(f"Error: {html_path} not found")
        sys.exit(1)

    # Read Stata file
    df = pd.read_stata(dta_path)
    print(f"Read {len(df)} climbs from {dta_path.name}")

    # Build JSON records
    records = []
    for _, row in df.iterrows():
        records.append({
            "climb": str(row["climb"]),
            "date": str(row["date"]),
            "portal": str(row["portal"]),
            "time": str(row["time"]),
            "watts": int(row["watts"]),
            "seq": int(row["seq"]),
            "elev": int(row["elev"]),
            "dist": round(float(row["dist"]), 1)
        })

    # Format as indented JS array
    lines = ["const CLIMBS = ["]
    for i, rec in enumerate(records):
        comma = "," if i < len(records) - 1 else ""
        lines.append(f"  {json.dumps(rec)}{comma}")
    lines.append("];")
    new_array = "\n".join(lines)

    # Read HTML and replace the CLIMBS array
    html = html_path.read_text(encoding="utf-8")

    # Match from "const CLIMBS = [" to the closing "];"
    pattern = r"const CLIMBS = \[.*?\];"
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        print("Error: Could not find CLIMBS array in index.html")
        sys.exit(1)

    # Replace
    new_html = html[:match.start()] + new_array + html[match.end():]
    html_path.write_text(new_html, encoding="utf-8")

    print(f"Updated {html_path.name} with {len(records)} climbs")

    # Show latest entries
    print("\nLatest 3 climbs:")
    for rec in records[-3:]:
        print(f"  #{rec['seq']} {rec['climb']} ({rec['date']}) — {rec['time']}, {rec['watts']}w")

if __name__ == "__main__":
    main()
