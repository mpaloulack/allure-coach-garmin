#!/bin/sh
# Starts ONE user's Garmin server with an empty environment:
# it only gets its own key, never mcp-front's secrets (JWT, encryption, OIDC).
H=$(mktemp -d /tmp/garmin.XXXXXX) || exit 1
exec env -i PATH=/usr/local/bin:/usr/bin:/bin HOME="$H" \
  GARMIN_PERSONAL_API_KEY="$GARMIN_PERSONAL_API_KEY" \
  garmin-personal-mcp
