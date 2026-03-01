# Roadmap

High-level direction for iVDrive. Priorities may shift based on feedback and contributions.

## Current focus (beta)

- **Online service** — [ivdrive.eu](https://ivdrive.eu): sign up, add your car, use the dashboard. No setup required for most users.
- **Škoda Connect** — Full support for Škoda electric vehicles (Enyaq, etc.) via the official API: telemetry, trips, charging, statistics, and dashboard.
- **Self-hosted option** — Docker Compose stack for those who want to run the full application (API, collector, frontend, PostgreSQL, Valkey) on their own server or NAS.
- **Stability** — Bug fixes, documentation, and UX improvements for the current feature set.

## Planned

- **Other VW Group brands** — Extend support to other Volkswagen Group EVs that use the same or compatible Connect APIs (e.g. Volkswagen, Cupra) where feasible.
- **Beta → stable** — Clear release process, versioning, and upgrade path; documented production considerations (backups, secrets, updates).

## Ideas (no commitment)

- Broader EV or OEM support (beyond VW Group).
- Optional cloud or managed deployment options (subject to license and project goals).
- Integrations (e.g. home automation, energy management).

Contributions and ideas are welcome via [GitHub Discussions](https://github.com/m7xlab/iVDrive/discussions) and [Issues](https://github.com/m7xlab/iVDrive/issues).
