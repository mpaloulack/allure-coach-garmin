# allure-coach-garmin

**English** · [Français](README.fr.md)

*A running coach for **Garmin**, inside Claude. Fork of [allure-coach](https://github.com/Sekiro-kost/allure-coach) (built for COROS).*

A coach that reads your Garmin data, sets your heart-rate zones, builds a plan for your race and publishes a dashboard: plan, readiness of the day, a review of each session, aerobic progress, weather, race-day sheet.

**Difference from the original: everything is read-only.** Nothing is sent to your watch or to your Garmin account. The plan lives in the dashboard; if you want wrist guidance for a workout, create it yourself in Garmin Connect.

> **Independent project.** Not affiliated with Garmin, COROS or Anthropic. This is **not medical advice**: the plans are suggestions to adapt to how you feel. If something hurts, stop and see a health professional.

## Try it without installing anything

Open [`exemples/demo.html`](exemples/demo.html) in your browser (download the file, then double-click it). Fictional athlete, nothing is read or written, dates are shifted to the current week.

## What it does

- **Tailored plan**: zones from your threshold heart rate (Friel), Daniels paces, varied sessions, 80/20 polarisation, taper.
- **Calendar**: tap a session for its sheet, long-press to move or swap it, with advice when the sequence gets risky.
- **Readiness of the day**: green, orange or red from HRV (against your normal Garmin range), sleep, load, Training Readiness and how you feel.
- **Session review**: planned versus actual, from your watch's laps, with your rating and any pain.
- **Aerobic progress**: your pace at a fixed heart rate, with the effect of heat.
- **Optional**: weather (Open-Meteo), strength work, race-day sheet with a start forecast, season timeline, Sunday review.

## What you need

- Claude with the Artifact tool and its database (ArtifactData): Claude Code, or Cowork on claude.ai.
- A **Garmin connector** (MCP server) that reads Garmin Connect. Tools differ between connectors: the guide tells Claude what to look for, not which names to use.
- Optional: the **Open-meteo** connector.

## Setup

1. Create a project in Claude, for example "Running".
2. Add the files from [`kit/`](kit): `GUIDE-CLAUDE.md`, `coach-dashboard-template.html` and `inject-coach.py`.
3. Write: **"Start the running coach kit"**. Claude answers in your language. The dashboard interface itself is currently in French.
4. Answer the questions (race, date, goal, days available, training city). Claude shows your zones, its diagnosis and the plan, then publishes the dashboard.
5. To refresh the data: **"update my coach"** (or a daily scheduled task).

## How it works

```
Garmin connector ──(read)──> Claude ──(ArtifactData)──> artifact database <──(read)── dashboard
                                                                                  Open-Meteo (weather, city only)
```

The page has **no** access to Garmin: Claude reads Garmin and writes the data (`sync/latest`, `laps/<date>`) into the artifact's database. The page only calls the Open-Meteo connector, with your city's position. Everything specific to the athlete lives in the `COACH` object, injected into the HTML template by `inject-coach.py`. Full schema: [`kit/GUIDE-CLAUDE.md`](kit/GUIDE-CLAUDE.md), example: [`exemples/exemple-coach.json`](exemples/exemple-coach.json).

## Privacy and security

See [`SECURITY.md`](SECURITY.md). In short:
- read-only on Garmin, the page itself has no access to it;
- no GPS coordinates of your activities are stored: weather uses the city (rounded to about 10 km);
- all text coming from the data is escaped before display (a booby-trapped activity name cannot run code);
- no Google font or other external resource at load time;
- the dashboard is private: **do not share its link**, it contains your health data.

## Using it from a phone (no PC)

Friends without a computer can use Claude with their Garmin data through a small hosted connector: OAuth sign-in through your own identity provider, one Garmin personal API key per person, read-only. See [`connector/README.md`](connector/README.md). It is a homelab-grade setup, so read its limitations first.

## Differences from allure-coach

| | allure-coach (COROS) | allure-coach-garmin |
|---|---|---|
| Sending the plan to the watch | yes | no (read-only) |
| Page access to the watch | COROS read + write | none |
| Data refresh | the page, when opened | Claude, on request or scheduled |
| Weather position | start of each run (~1 km) | fixed city (~10 km) |
| Escaping of displayed text | no | yes |
| Fonts | Google Fonts | system fonts |

## License

[MIT](LICENSE), like the original project (© its authors). Trademarks belong to their owners.
