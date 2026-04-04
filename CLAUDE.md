# CLAUDE.md — Zwift Climb Log

## Project Overview

A single-file web app (`index.html`) for browsing Zwift climb portal completions. Data is maintained in Stata and synced into the HTML via a Python script. No build tools, no frameworks, no server — just open the file in a browser.

## Architecture

- **`index.html`** — Self-contained app. All HTML, CSS, and JS in one file. Climb data lives in a `const CLIMBS = [...]` JSON array near the top of the `<script>` block.
- **`climbs.dta`** — Stata data file. This is the source of truth. All data edits happen here first.
- **`update_climbs.py`** — Reads `climbs.dta` with pandas and overwrites the `CLIMBS` array in `index.html` using regex replacement. Run after any data change.

## Key Design Decisions

- **No framework.** Vanilla HTML/CSS/JS. The app is small enough that a framework adds complexity without benefit.
- **Data embedded in HTML.** Avoids needing a server or fetch calls. The tradeoff is the sync script, but the workflow is simple.
- **Multi-select dropdown.** Users can view one or many climbs at once. Dropdown stays open on selection, chips show selected climbs above results.
- **Split rider weight.** W/kg calculation uses `riderKg(seq)` function — seq 1–43 at 81.6 kg, seq 44+ at 80.3 kg. Constants are `RIDER_KG_OLD`, `RIDER_KG_NEW`, and `WEIGHT_CHANGE_SEQ`.

## Data Schema

Each climb record has: `climb` (string), `date` (string, M/D/YY), `portal` (F=France, W=Watopia), `time` (string, MM:SS or H:MM:SS), `watts` (int), `seq` (int, chronological order), `elev` (int, feet), `dist` (float, km).

## Strava Links

Each attempt links to `https://www.strava.com/athlete/calendar#MM/DD/YYYY` — this opens the Strava training calendar at the climb date so the user can find the full activity.

## Styling

Dark theme. Fonts: DM Serif Display (headings), IBM Plex Mono (data/labels), IBM Plex Sans (body). Accent color: `#f97316` (orange). Color-coded metrics: orange for time, blue for watts, purple for W/kg, green for elevation.

## Common Tasks

### Add new climbs
1. Edit `climbs.dta` in Stata (add rows, increment `seq`)
2. Run `python update_climbs.py`
3. Commit and push

### Change rider weight
Edit the constants at the top of the `<script>` block in `index.html`:
- `RIDER_KG_NEW` for the new weight in kg
- `WEIGHT_CHANGE_SEQ` for the first seq number that uses the new weight
- Add a new split if needed by extending the `riderKg()` function

### Verify data integrity
Run this to compare the Stata file against the HTML array:
```bash
python -c "
import pandas as pd, json, re
df = pd.read_stata('climbs.dta')
html = open('index.html').read()
js = json.loads(re.search(r'const CLIMBS = (\[.*?\]);', html, re.DOTALL).group(1))
for i, (_, r) in enumerate(df.iterrows()):
    j = js[i]
    for f in ['climb','date','portal','time']:
        assert str(r[f]).strip() == j[f], f'Row {i} {f}: {r[f]} vs {j[f]}'
    assert int(r['watts']) == j['watts'], f'Row {i} watts'
    assert int(r['seq']) == j['seq'], f'Row {i} seq'
    assert int(r['elev']) == j['elev'], f'Row {i} elev'
    assert round(float(r['dist']),1) == j['dist'], f'Row {i} dist'
print(f'All {len(df)} entries match.')
"
```

## GitHub Pages

If enabled, the app is live at `https://clwesterl.github.io/climbs/`. Point Pages to root (`/`) of `main` branch.
