# Zwift Climb Log

A self-contained web app for tracking completed Zwift climb portal rides. Select one or multiple climbs from a searchable dropdown to view attempt history, power data, and link out to Strava.

![Screenshot](screenshot.png)

## Features

- **Multi-select searchable dropdown** — type to filter, check multiple climbs, keyboard navigable
- **Per-climb stats** — time, watts, W/kg, elevation, distance for every attempt
- **PR tracking** — fastest attempt per climb flagged with ⚡ PR badge
- **Strava integration** — each attempt links to your Strava training calendar for that date
- **Elevation comparison** — visual bar comparing each climb against the highest logged (Mt. Fuji)
- **Summary dashboard** — total climbs, unique climbs, cumulative elevation and distance

## Usage

Open `index.html` in any browser. No build step, no dependencies, no server required.

To host via GitHub Pages, enable Pages in repo settings pointing to the root (`/`) of the `main` branch, then visit `https://<username>.github.io/climbs/`.

## Data

Source data lives in `climbs.dta` (Stata format). The climb records are embedded directly in `index.html` as a JSON array for zero-dependency operation. When adding new climbs, update both the `.dta` file and the `CLIMBS` array in `index.html`.

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

Rider weight for W/kg calculation is set in `index.html`:

```javascript
const RIDER_KG = 81.6;
```

## License

Personal project — not licensed for redistribution.
