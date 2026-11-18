# Changelog

## garmin-1.1.0 · 2026-11-18

- Hosted Garmin connector for people without a PC (`connector/`).
- Documentation translated to English (README, security, contributing, changelog, kit guide, examples); the French README is kept as `README.fr.md`. `kit/LISEZ-MOI.md` is now `kit/README.md`. The dashboard interface itself is still in French.
- Demo regenerated (picks up the session-review refresh fix).

## garmin-1.0.0 · 2026-11-15

Fork for Garmin, read-only.

- Garmin data is read by Claude and written to the artifact's database (`sync/latest`, `laps/<date>`); the page no longer has any access to the watch.
- No more sending the plan to the watch: the plan lives in the dashboard.
- Session review computed from the laps written by Claude, perceived effort taken from Garmin's RPE.
- Security: all displayed text is escaped, COACH injection is made safe (`kit/inject-coach.py`), no more GPS coordinates of runs (weather uses the city), no more Google Fonts.
- Demo regenerated (`exemples/build-demo.py`).

## 1.0.0 · 2026-10-13

First public version.

- Tailored plan sent to the COROS watch, with zones from threshold heart rate and Daniels paces.
- Vertical calendar: session sheet in a modal, long-press to move or swap, consistency advice.
- Readiness of the day (green, orange, red), lighten or strengthen a session, planned vs actual review.
- Aerobic progress at fixed heart rate, HRV, resting heart rate, sleep, load.
- Optional: weather for runs and race day (Open-Meteo), strength work, race-day sheet, season timeline, Sunday review.
- Self-contained demo with a fictional athlete (`exemples/demo.html`).
