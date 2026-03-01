# Self-hosting iVDrive

This guide is for running the full iVDrive stack (API, collector, frontend, database, cache) on your own machine or NAS with Docker Compose. Most users can simply use [ivdrive.eu](https://ivdrive.eu) with no setup.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

## Quick start

1. **Clone the repository**
   ```bash
   git clone https://github.com/m7xlab/iVDrive.git
   cd iVDrive
   ```

2. **Configure environment**
   - Copy `.env.example` to `.env`.
   - Set the required variables:
     - `POSTGRES_PASSWORD` — Database password.
     - `VALKEY_PASSWORD` — Cache password.
     - `JWT_SECRET_KEY` — A long random string (e.g. 64 characters) for signing tokens.
     - `ENCRYPTION_KEY` — Base64-encoded 32-byte key for encrypting stored credentials (e.g. Škoda Connect passwords).
   - See [.env.example](../.env.example) for all options and notes.

3. **Start the stack**
   ```bash
   docker compose up -d
   ```

4. **Open the app**
   - Web UI: http://localhost:3035 (or the host/port you use).
   - API: http://localhost:8000.
   - Register and add your vehicle with your Škoda Connect credentials.

## Services

| Service | Purpose |
|---------|---------|
| **ivdrive-web** | Next.js frontend (port 3000 inside container; map to 3035 or your choice). |
| **ivdrive-api** | FastAPI backend (port 8000). |
| **ivdrive-collector** | Background worker that polls the Škoda API and stores telemetry. |
| **postgres** | PostgreSQL database. |
| **valkey** | Valkey (Redis-compatible) cache. |

## Optional settings

- **CORS_ORIGINS** — If you access the UI from another origin (e.g. a different domain), add it here (JSON array of allowed origins).
- **NEXT_PUBLIC_API_URL** — Leave empty if the browser talks to the same host (recommended). Set only if the API is on a different host than the frontend; then rebuild the web image after changing.
- **LOG_LEVEL** — `info` (default) or `debug`.
- **COLLECTOR_DEBUG** — Set to `true` to log parsed API response summaries in the collector (for troubleshooting).

## Backups

- Back up the PostgreSQL data volume (`pgdata`) and your `.env` (especially `JWT_SECRET_KEY` and `ENCRYPTION_KEY`). Restore with the same keys so existing tokens and encrypted credentials remain valid.

For architecture and code layout, see [Project overview](project_overview.md).
