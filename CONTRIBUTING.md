# Contributing

Thanks for your interest. A few rules to keep the repository clean.

## Before opening an issue

- State the kit version (see [`CHANGELOG.md`](CHANGELOG.md)), which Garmin connector you use, whether Open-meteo is connected, and what you did just before the problem.
- **Remove all personal data**: first name, heart rate, place, race dates, your dashboard link. A screenshot of the demo (`exemples/demo.html`) is often enough.

## Proposing a change

1. Make your change in `kit/coach-dashboard-template.html` and, if the `COACH` schema changes, in `kit/GUIDE-CLAUDE.md` (schema, guidance and examples).
2. Regenerate the demo: `python3 -I exemples/build-demo.py`.
3. Open `exemples/demo.html` in your browser and go through the tabs: no errors in the console.
4. Add a line to [`CHANGELOG.md`](CHANGELOG.md).

## Principles

- **No personal data in the template.** Everything specific to the athlete goes through `COACH`. Optional tabs (Strength, Race day, Season) disappear when their data is missing.
- **The template must survive missing data**: a watch without HRV must not bring the page down.
- No new external dependency in the published page: only the script hosts allowed by Claude's artifacts work.
- `exemples/exemple-coach.json` stays fictional.
