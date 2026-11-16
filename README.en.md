# allure-coach-garmin

*A running coach for **Garmin**, inside Claude. Fork of [allure-coach](https://github.com/Sekiro-kost/allure-coach) (built for COROS).*

Claude reads your Garmin data, sets your heart-rate zones, builds a plan for your race and publishes a dashboard: plan, readiness of the day, session reviews, aerobic progress, weather, race-day sheet.

**Difference from the original: everything is read-only.** Nothing is sent to your watch or your Garmin account. The plan lives in the dashboard.

> Independent project, not affiliated with Garmin, COROS or Anthropic. Not medical advice.

- Try it: open [`exemples/demo.html`](exemples/demo.html) in a browser (fictional athlete).
- Needs: Claude with Artifact + ArtifactData (Claude Code or Cowork), a Garmin MCP connector (read access), optionally Open-Meteo.
- Setup: add the three files of [`kit/`](kit) to a Claude project and write **"Lance le kit coach course"** (the guide is in French, Claude answers in your language). Refresh with **"update my coach"**.
- The page has no Garmin access at all: Claude reads Garmin and writes the data into the artifact's database. No GPS track is stored (weather uses your city), all displayed text is escaped, no external fonts. Don't share the dashboard link. See [`SECURITY.md`](SECURITY.md).

License: [MIT](LICENSE).
