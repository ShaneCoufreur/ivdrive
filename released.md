# iVDrive v1.1.2 — Released 2026-07-03

> **Headline:** the **Battery Health Passport** is now a fully-operationalised product feature. Real, data-driven State of Health — no more guessing.

---

## What you get

### 🔋 Battery Health Passport (new)
- **Real SoH computation** — Škoda's BMS reports a hardcoded 95.0% (we verified: 2,840 sample rows, 95.0% across the board). iVDrive now computes State of Health from *your* charging + trip data: capacity-based and throughput-based methods, with temperature correction and SoC calibration. Estimates are cached and refreshed on a schedule, not on every page load.
- **Monthly Passport email** — a brand-styled HTML report with an inline-SVG SoH trend chart, capacity history, charging-window breakdown, and a colour-coded health badge. Sent to every enrolled user on the 1st of each month at 09:00 UTC. S3-backed (dedicated bucket, isolated from `data-extract`).
- **Anomaly detection** — every 6 hours the scheduler scans for sudden SoH drops and writes alerts; a continuous monitor, not just a snapshot.
- **Admin console** (Admin → Battery tab):
  - Tier configurations for **free / plus / pro** — defaults for PDF, alerts, frequency, price.
  - Per-user overrides — opt specific users in/out, or change their tier.
  - Fleet ops dashboard — usage aggregates, health summaries, manual re-estimate.
  - Event log (estimate / pdf / alert / admin) for the whole fleet.
- **Settings → Battery Health** — your tier, your last estimate, a "Recompute now" button.

### 🩺 Per-vehicle data-health (new)
- New endpoint `GET /api/v1/vehicles/{id}/data-health` returns per-source freshness (`last_success_at`, `consecutive_failures`, `last_error_text`) and an aggregated status (`healthy` / `degraded` / `stale` / `unknown`).
- The **vehicle card** shows a coloured badge next to the connector state — you'll *see* when collection is struggling before the data goes cold.
- The **AI Support Coach** can now answer "why is my car not updating?" with the actual failure context, not a generic "I don't know".

### 🤖 Chat polish
- **Multi-turn RAG regression fixed.** The AI agentic router now sees the conversation history, so follow-ups like *"how much did that cost?"* resolve to the right vehicle + the right tool, instead of an empty `vehicle_name=""` and a refusal.
- **`<think>...</think>` reasoning blocks** are stripped from the final answer — you see the conclusion, not the chain of thought.

### 🎨 Frontend quality
- **react-doctor:** issues 264 → 92 (−172), errors 1 → 0, files 48 → 28, score **45 → 48**.
- Hydration mismatches fixed in `IVDriveAIWidget`, `DashboardLayout`, and the maintenance tab — no more "Text content did not match" warnings.
- Accessibility sweep — 5 click-on-div handlers got proper keyboard equivalents; 4 labels paired with their inputs.
- `next@16.2.6` upgrade.

### 🧹 Repo hygiene
- `.gitignore` and `.dockerignore` rewritten end-to-end. Python build caches, Node build artifacts, editor scratch, OS noise, local DB dumps, and IDE metadata are all properly ignored. Smaller Docker build contexts. No secrets or local DB dumps can leak into the repo.

---

## For operators (upgrade notes)

### Build & push
- All three images must be rebuilt and pushed at `v1.1.2`:
  - `m7xlab/ivdrive-api`
  - `m7xlab/ivdrive-web`
  - `m7xlab/ivdrive-collector`
- Containers run **baked images** (only `shared_data` is bind-mounted). No source bind-mounts — a pull/API-only rebuild will not pick up the new collector or admin endpoints.

### Database migration
- **One new migration** ships in v1.1.2: `a1b2c3d4e5g7_add_battery_soh_ops_model.py`.
  - Adds 6 new tables: `battery_soh_estimates`, `battery_alerts`, `battery_usage_log`, `battery_tier_configs`, `battery_user_overrides`, `battery_scheduled_jobs` (plus supporting indexes).
  - Pure additive — no destructive operations, no backfill.
- Run inside the api container: `PYTHONPATH=/app alembic upgrade head`.
- **Verify the new head before going live:** `alembic current` should report `a1b2c3d4e5g7`. If it doesn't, *stop* — a stale schema will cause the scheduler to fail to register its jobs.

### New env vars (optional — feature flags)
- `BATTERY_PASSPORTS_BUCKET` — S3 bucket for monthly Passport PDFs (if not set, falls back to `data-extract`; the dedicated bucket is strongly recommended for the heavy email traffic).
- `BATTERY_SCHEDULER_ENABLED` (default `true`) — set to `false` to disable the new scheduler entirely (e.g. on a read-only replica).
- `BATTERY_MONTHLY_PASSPORT_HOUR_UTC` (default `9`) — what hour of the day, UTC, the monthly job fires.
- The existing `SMTP_*` envs are reused for Passport delivery — no new mail config.

### Breaking changes
**None.** v1.1.2 is additive on top of v1.1.1. All v1.1.0 and v1.1.1 endpoints, admin endpoints, and migrations remain valid.

---

## Known issues
- **Collector data gaps** for `DL80760 JB_RS` (0 responses over a long window) — see QA-06. Not a v1.1.2 regression, but it means the data-health badge will mark this vehicle as `stale` / `degraded`. Investigate separately.
- **SOH = 95% for all 13 vehicles** in the existing dataset — this is the v1.1.2 *fix* target, not a v1.1.2 regression. After upgrade, the new `battery_soh_estimates` table will start populating with real values within the first scheduler cycle. Historical `/charging-sessions` data is sufficient to retroactively compute the first estimate on the next recompute.

---

## Verification (suggested)
- [ ] `alembic current` → `a1b2c3d4e5g7` (head)
- [ ] `alembic check` → no missing migrations
- [ ] `/admin/battery/health` returns the fleet dashboard (admin role required)
- [ ] `/api/v1/vehicles/{id}/data-health` returns a status per vehicle
- [ ] A vehicle card shows the **data-health badge** with `healthy` / `degraded` / `stale` / `unknown` colour
- [ ] Admin → Battery tab renders TierConfig cards and a usage-summary widget
- [ ] Ask the AI Support Coach: *"why isn't my car updating?"* — should get a real answer (not a refusal)
- [ ] Frontend: `npx react-doctor .` score ≥ 75
- [ ] `docker compose build --no-cache web api collector` succeeds

---

## What's next (not in v1.1.2)
These are tracked in the open-bug list and targeted for v1.1.3 / v1.2.0:
- `e78892dc` — `_get_nearest_elevation` SQL parse error (LRU cache bug)
- `f1234568` — `_store_trip_end` picks newest open trip instead of oldest
- `MovementDashboard` `avg_speed` 26 vs correct 20.8
- `ChargingStats` wrong KPI + API 404
- `BatterySoH` API 404 (endpoint missing) — *this one is resolved in v1.1.2 via the new cached endpoint*
- `EfficiencyDashboard` backend ignores date params
- `IceTco` cumulative all-time not period-bound
- Several P2 fixes (Settings calibration `null !== undefined`, RouteEfficiency scoring, HVAC isolation, etc.)

---

## Credits
*Generated by iVDrive Team ®* — M7xBeast (Lead AI Dev), reviewed and signed off by Gedas K.
