# Hosted Garmin connector (use Claude with Garmin from a phone)

Lets people **without a PC** use Claude with their Garmin data from the Claude mobile app. You host one small
server; each person signs in with your identity provider and pastes **their own** Garmin personal API key.

It is **read-only**: it uses Garmin's official Personal API (a key the person creates and can revoke), never a
Garmin password. The coaching dashboard in [`kit/`](../kit) works with or without it.

> This is a homelab-grade setup, written down so it can be reproduced. Read [Limitations](#limitations) first.

## How it works

```
phone / web ──▶ claude.ai ──▶ your reverse proxy ──▶ mcp-front ──▶ one garmin-personal-mcp process per person ──▶ Garmin API
 (Claude app)  (custom         (TLS, IP filter)        │              (own key, empty environment)
                connector)                             └─▶ your identity provider (OIDC): who may sign in
```

- **claude.ai connects from Anthropic's servers**, not from the phone, so the server must be reachable over
  public HTTPS. A local (stdio) MCP server cannot be used.
- [`mcp-front`](https://github.com/stainless-api/mcp-front) is the OAuth front door for claude.ai. It lets people
  sign in through any OIDC provider, stores each person's key, and starts a **separate**
  [`garmin-personal-mcp`](https://github.com/Mason-Levyy/garmin-personal-mcp) process per person.
- Nothing here talks to Garmin except that per-person process, with that person's key.

## Security model

| Concern | How it is handled |
|---|---|
| Who may use it | Only members of a group bound to the OIDC application. **The identity provider is the only filter.** A patch makes mcp-front's email-domain list optional (it only does exact matching and refuses to start without one): [`patches/allow-any-domain.patch`](patches/allow-any-domain.patch). Without `MCP_FRONT_ALLOW_ANY_DOMAIN=true` it still refuses to start. |
| Garmin keys | Pasted by each person on `/my/tokens`. Stored **in RAM only** (`storage: memory`); no volume, read-only filesystem. They are **lost whenever the container is recreated or restarted**. |
| Key isolation | mcp-front's stdio processes inherit its whole environment. [`garmin-run.sh`](garmin-run.sh) starts each Garmin process with `env -i`, so it sees only its own key, never the JWT/encryption/OIDC secrets. |
| Deleting a key | Button on `/my/tokens`: the next call fails immediately. Also **revoke the key on Garmin's site** — that is the only real guarantee. |
| Network exposure | The container publishes no port. Machine endpoints only accept Anthropic's published outbound ranges; browser endpoints sit behind your usual filter. See [`deploy/reverse-proxy.example.conf`](deploy/reverse-proxy.example.conf). |
| Dependencies | `garmin-personal-mcp==0.3.0` with all 35 dependencies pinned **by hash** ([`requirements.lock`](requirements.lock)); mcp-front pinned to a commit. Update by hand, after reading the changelog. |
| Tools | `garmin_download_activity` is blocked (it writes files on the server). Everything else exposed by the Personal API is read-only. |

## Setup

### 1. Identity provider (example: authentik)

1. Create an **OAuth2/OpenID provider**: confidential client, redirect URI (strict)
   `https://garminmcp.example.com/oauth/callback`, scopes `openid email profile`, implicit consent flow.
2. Create an **application** (slug `mcp-garmin`) using it, and **bind a group** (for example `garmin-users`)
   to the application. Make sure users outside that group are denied.
3. Note the client ID and secret. Put them in `.env` yourself; do not paste secrets into chats or tickets.
4. The discovery URL is `https://auth.example.com/application/o/mcp-garmin/.well-known/openid-configuration`.

### 2. Build the image

```sh
podman build -t garmin-mcp:0.1 connector/      # or: docker build ...
```

The build clones mcp-front at the pinned commit, applies the patch, and installs the hash-locked Python
dependencies. mcp-front is **not** vendored in this repository (Elastic License 2.0).

### 3. Run it

Copy [`deploy/compose.example.yaml`](deploy/compose.example.yaml) and [`deploy/.env.example`](deploy/.env.example),
adapt the hostnames and the Docker network name, fill in `.env` (`chmod 600`), then `docker compose up -d`.
Generate the two keys with `openssl rand -base64 36` (`JWT_SECRET`) and `openssl rand -base64 24`
(`ENCRYPTION_KEY`, exactly 32 characters).

> Changing `.env` needs a **recreate** (`docker compose up -d --force-recreate`), not a restart: a restart keeps the
> old environment.

### 4. Reverse proxy

Use [`deploy/reverse-proxy.example.conf`](deploy/reverse-proxy.example.conf). Do **not** put forward-auth in front of
this host and do not apply a country filter at server scope: claude.ai's servers could not pass either.

### 5. Add the connector in claude.ai (each person, once)

1. claude.ai (web) → Settings → Connectors → **Add custom connector**.
2. URL: `https://garminmcp.example.com/garmin/sse` — **`/garmin/sse`, not `/garmin/mcp`**. mcp-front serves stdio
   servers over SSE only; `/garmin/mcp` returns 404 ("no MCP server found").
3. Keep "Sign in now" and "Register automatically". Ignore the SSE deprecation notice and keep SSE.
4. Sign in through your identity provider.
5. Open `https://garminmcp.example.com/my/tokens` in a browser and paste the Garmin key
   (create it at <https://connect.garmin.com/app/settings/personalApiToken>; it is shown only once).
6. Start a **new** conversation, enable the connector, and ask for last night's sleep.

mcp-front does not ask for the key during the sign-in flow (it only does that for OAuth-type services), so step 5
is a separate visit. The connector then also appears in the mobile app.

## Operating it

- **Add a friend:** create their account, add them to the group, they follow step 5 above.
- **Remove a friend:** remove them from the group, and ask them to delete their key on `/my/tokens` and revoke it on Garmin.
  Removing them from the group does not delete a key already held in memory; recreating the container does.
- **Restarts erase everyone's key.** Do not restart or update the container casually; tell people first.
- **Logs:** mcp-front never prints the key (it prints the `{{token}}` template). If the connector fails, the
  reverse proxy log shows `403` for any IP not in the allowed ranges.

## Limitations

- **SSE is deprecated in claude.ai.** It works today; the connector UI warns that it is being phased out. The planned
  replacement is a small purpose-built server speaking streamable HTTP.
- **Keys are in RAM only.** Safe against disk theft, but everyone must paste their key again after any recreation.
  mcp-front's only other store is Firestore (Google Cloud), which this setup avoids. A custom server could keep
  keys encrypted on disk instead.
- **Garmin's Personal API does not expose everything.** Training Readiness, VO2max, race predictions and lactate
  threshold returned 404 in testing. Sleep, Body Battery, stress, HRV, activities and laps work.
- **mcp-front is alpha**, single-maintainer, and its docs partly disagree with its code. Verify before upgrading.
- You become responsible for other people's health data and their keys. Tell them, and keep it small.

## Layout

| Path | What |
|---|---|
| `Dockerfile` | Builds mcp-front (pinned + patched) and the Garmin server into one image |
| `patches/allow-any-domain.patch` | Makes the email-domain list optional (identity provider is the filter) |
| `config.json` | mcp-front configuration (OIDC, per-user key, blocked tool) |
| `garmin-run.sh` | Starts one person's Garmin process with an empty environment |
| `requirements.in` / `.lock` | Garmin server and hash-locked dependencies |
| `deploy/` | Example compose, reverse proxy config, `.env.example` |
