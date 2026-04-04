# Zwift Climb Log

A self-contained web app for tracking completed Zwift climb portal rides. Select one or multiple climbs from a searchable dropdown to view attempt history, power data, and link out to Strava.

## Features

- **Multi-select searchable dropdown** — type to filter, check multiple climbs, keyboard navigable
- **Per-climb stats** — time, watts, W/kg, elevation, distance for every attempt
- **PR tracking** — fastest attempt per climb flagged with ⚡ PR badge
- **Strava integration** — each attempt links to your Strava training calendar for that date
- **Elevation comparison** — visual bar comparing each climb against the highest logged (Mt. Fuji)
- **Summary dashboard** — total climbs, unique climbs, cumulative elevation and distance

## Usage

Open `index.html` in any browser. No build step, no dependencies, no server required.

To host via GitHub Pages, enable Pages in repo settings pointing to the root (`/`) of the `main` branch, then visit `https://clwesterl.github.io/climbs/`.

## Adding New Climbs

1. Add the new climb to `climbs.dta` in Stata
2. Run the sync script:

```bash
python update_climbs.py
```

3. Commit and push:

```bash
git add .
git commit -m "Add Climb Name"
git push
```

The script reads `climbs.dta` and updates the `CLIMBS` array in `index.html` automatically. Requires `pandas` (`pip install pandas`).

## Data

Source of truth is `climbs.dta` (Stata format). The climb records are embedded in `index.html` as a JSON array for zero-dependency operation. Always edit the `.dta` file first, then run `update_climbs.py` to sync.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `climb` | string | Name of the climb |
| `date` | string | Date completed (M/D/YY) |
| `portal` | string | Portal: F (France) or W (Watopia) |
| `time` | string | Climb duration (MM:SS or H:MM:SS) |
| `watts` | number | Average watts |
| `seq` | number | Chronological order of completion |
| `elev` | number | Elevation gain (ft) |
| `dist` | number | Distance (km) |

## Configuration

Rider weight for W/kg uses a split based on when the weight changed:

```javascript
const RIDER_KG_OLD = 81.6;       // seq 1–43
const RIDER_KG_NEW = 80.3;       // seq 44+
const WEIGHT_CHANGE_SEQ = 44;
```

To update the cutoff or weights, edit these constants in `index.html`.

## File Structure

```
climbs/
├── index.html          # The app (self-contained HTML/CSS/JS)
├── climbs.dta          # Source data (Stata format)
├── update_climbs.py    # Sync script: .dta → index.html
├── CLAUDE.md           # Project context for Claude Code
├── .gitignore
└── README.md
```

## License

Personal project — not licensed for redistribution.
