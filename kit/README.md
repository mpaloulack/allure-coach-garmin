# Running coach kit with Claude and Garmin

This kit gives you a coach: it analyses your Garmin data, sets your heart-rate zones, builds a plan for your race and publishes a dashboard. You can move or swap a session there (long-press the tile), lighten it or strengthen it. It tells you whether you are fit for today's session, compares planned and actual after every session and shows the weather. Optional: strength work, race-day sheet, season timeline, Sunday review.

**Read-only**: nothing is sent to your watch or to your Garmin account.

## What you need

- Claude with the Artifact tool (Claude Code, or Cowork on claude.ai).
- A Garmin connector (MCP server) that reads Garmin Connect.
- Optional: the **Open-meteo** connector for the weather.

## Setup (5 minutes)

1. In Claude, create a project, for example "Running".
2. Add the three kit files: `GUIDE-CLAUDE.md`, `coach-dashboard-template.html`, `inject-coach.py`.
3. Write: **"Start the running coach kit"**.
4. Answer the questions. Claude shows you your zones, its diagnosis and the plan before publishing the dashboard.

## Good to know

- Data is refreshed when you ask Claude to "update my coach" (or every day with a scheduled task). The page itself never connects to Garmin.
- For the session review to compare each step properly, press "lap" at every step change, or create the workout in Garmin Connect.
- Open the dashboard from Claude (sidebar or gallery): that is where it reads its database.
- Don't share the dashboard link: it contains your heart rate, HRV, sleep and notes.
