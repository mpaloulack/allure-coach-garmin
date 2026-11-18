# Security and privacy

This fork handles health and activity data (heart rate, HRV, sleep, reported pain). Here is what it does to protect them, and what remains your responsibility.

## Design choices

| Risk | In the original (COROS) | In this fork |
|---|---|---|
| The page modifies the watch | the page can call `updateTrainingPlan` | the page has no access to Garmin; Claude only uses read tools |
| HTML injection (XSS) through an activity name, a note, a plan request or text copied from a race website | text inserted without escaping (`innerHTML`) | all text is escaped on the way in (`clean()`), including data read back from the database |
| A COACH text closing the `<script>` tag | not handled | `inject-coach.py` escapes `</` and U+2028/2029 and checks the syntax |
| Locating your home | start coordinates of every run, rounded to ~1 km, stored in the database | no run coordinates; a fixed city position (`wxGeo`, rounded to 0.1°) for the weather |
| IP leak at load time | Google Fonts | system fonts, no external resource at load |
| Instruction injection into Claude (an activity name or a note that "gives orders") with a write tool set to "Always allow" | recommended in the README | the guide treats these texts as data, and there is no Garmin write tool any more |

## What remains your responsibility

- **The dashboard link**: the artifact is private, but anyone who has the link sees your data. Don't share it, don't paste it into an issue.
- **The Garmin connector**: it has access to your whole Garmin Connect account. Pick one you trust, **pin its version** (no automatically launched `@latest`) and keep its tokens in a file readable only by you (`chmod 600`). Turn on two-factor authentication on your Garmin account.
- **Permissions**: only allow the connector's read tools; never set a tool to "Always allow" if it can write.
- **Kit updates**: read the changes to the HTML template before replacing it.

## Reporting a problem

Open an issue without personal data (no name, heart rate, location or dashboard link).
