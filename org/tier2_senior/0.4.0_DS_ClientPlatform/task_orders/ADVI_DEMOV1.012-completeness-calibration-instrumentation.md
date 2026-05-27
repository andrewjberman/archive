# Task Order: ADVI_DEMOV1.012 — Completeness + calibration + instrumentation

**TO ID:** ADVI_DEMOV1.012
**Status:** DISPATCHED 2026-05-27T~13:55Z
**Project:** ADVI_DEMOV1 (status remains `complete` per cycle 145 LANDMARK + cycle 158 .011 RAVC2-ACCEPT-CLOSE; this is FIX-class post-close TO under "Phase 6+ reopen for completeness" framing per Andrew `feedback_prd_addendum_phase_n_reopen_over_new_project`)
**Classification:** FIX-class FOLD per ws CTO /ws-charter cycle 0072-sub RATIFY (same-page-extension within §3.6 mandate; symmetric-substrate test passes; no NOVEL framing)
**Owner:** Phase 1 DS-lane source-edit → 0.4.0_DS_ClientPlatform~D primary (~D session continuity from .011) | Phase 2-3 AE-lane → 0.7.0_AE_CloudOps
**Dispatching exec:** 2.0.0_SA_COO
**Authority chain:** Andrew sovereign `feedback_prd_addendum_phase_n_reopen_over_new_project` (PRD-addendum/reopen over new project) → ws CTO `bcc4cb142` PRD v0.1.4 §3.6 amendment + cycle 0072-sub FOLD ratify → ws COO cycle 161 autonomous FIX-class authoring
**RAVC2 ETA:** ~3-5h wall (Phase 1 DS edit + Phase 2 AE re-transform with extended executionTimeout 6h budget + Phase 3 joint RAVC2)
**Time-pressure:** None. Andrew "tomorrow morning colleague" framing already satisfied via .011 strict R5 PASS (cycle 158).

## Provenance

**Why this TO exists:** ADVI_DEMOV1.011 Fire 7 strict R5 PASS (cycle 158 `8498fae7`) empirically validated PRD v0.1.4 §3.6 durable structural-fix spec (leak=0 + anomaly=0). But validation occurred against partial-PASS-2 bucket state from Fire 6 TimedOut at 3h cap — clients/+firm/ empty + advisors/ ~10/169 + accounts/ 5000+ FULL. AC3 was spec-correctness validation, NOT completeness validation. 3 dichotomy-derived scope items emerged + 1 sister IAM hardening + 1 F1 retire fold-candidate:

1. **Completeness gap** — partial bucket state means downstream demo consumers may hit missing-subpath surfaces; needs full transform re-run with extended executionTimeout
2. **Calibration** — Fire 6 demonstrated first-Fire-post-schema-rev Phase B ~2h+ vs steady-state ~30-60min; future SSM executionTimeout sizing needs empirical formula
3. **Instrumentation** — PASS-2 completion-gate (source-account-count vs accounts-written-count) would have made Fire 6 truncation exit-distinct from TimedOut, simplifying RAVC2 analysis
4. **IAM logs/ skip-on-TimedOut propagation** — bash `set -euo pipefail` propagated logs/ AccessDenied → SSM Status=Failed despite scan PASS; cycle 145 IAM amendment `ccbc93a51` partially addressed; remaining hardening: dispatch script should tolerate logs/ upload failure when result.json upload succeeded
5. **F1 retire FOLD-CANDIDATE** — DS~D 1247Z observation: snapshot-clean coverage extension already structurally executed F1-retire at .011 Fire 6 start (clients/+firm/ EMPTY post-sweep = F1 z-shaped residue purged + advisors/ swept); separate F1-retire write-up may be redundant

## Acceptance Criteria

### AC1 — PASS-2 completion-gate instrumentation (DS-lane source-edit)

- Extend `data/demo/scripts/transform/demo_transform.py` with completion-gate at end of PASS 2
- Record `source_account_count` (from BD input) vs `accounts_written_count` (OPAL###### writes that succeeded) — both derived from `prefixes` iteration
- If `accounts_written_count < source_account_count` AND wall-clock not at executionTimeout → emit explicit incomplete-pass error (distinct exit code, e.g., exit 4) BEFORE TimedOut wraps
- If `accounts_written_count < source_account_count` AND wall-clock approaching executionTimeout → emit forward-leaning warning + checkpoint-state-write for resumability (defer impl to AC1.2 if scope permits)
- Per-subpath completion summary emitted to stdout + result.json

### AC2 — Full-completeness re-transform (AE-lane SSM dispatch)

- Dispatch `demo_transform.py` (post-AC1 source) against demo bucket via SSM with executionTimeout=21600s (6h budget; 2x first-post-schema-rev calibration headroom)
- Empirical record of Phase B + PASS 2 wall + completion-gate result
- Validates AC1 instrumentation fires correctly at scale

### AC3 — Strict scan against post-AC2 bucket validates clean R5 + complete coverage

- Run `pii_leak_scan.py` against post-AC2 bucket state (strict default, no `--f1-residue-tolerance`)
- Expected R5: `leak_count=0` + `format_anomaly_count=0` + scan exit 0 (strict PASS reproduces cycle 158 .011 close)
- Additional completeness verification: scan corpus reflects ~6745 OPAL accounts/ + ~169 advisors/ + clients/+firm/ full corpus (specific count anchors per PRD §3.6 spec or post-AC2 measurement)

### AC4 — Calibration empirical anchors recorded

- TO close-out body documents:
  - Fire 6 Phase B + PASS 2 wall (~2h+ first-post-schema-rev)
  - Post-AC2 transform wall (steady-state schema-current with full clean-then-write)
  - Calibration formula: future SSM executionTimeout = max(steady-state × 1.5, first-Fire-post-schema-rev × 1.5)
- Banking observation: `feedback_first_fire_post_schema_rev_executiontimeout_calibration_formula` anchors the structural-fix-empirically-anchored cycle pattern

### AC5 — IAM logs/ skip-on-TimedOut hardening (AE-lane infra/dispatch)

- Update SSM dispatch wrapper script: handle `aws s3 cp .../logs/*.log` failure gracefully (don't propagate exit 1 to SSM)
- Use `aws s3 cp ... || true` or explicit conditional success-check
- Preserve scan body exit code as SSM final exit code, NOT logs upload exit code
- Empirical anchor from Fire 7 (already-clean) + Fire 6 (TimedOut + logs/ skip-on-cap) close-out hardening

### AC6 — F1 retire FOLD absorption decision

- Confirm DS~D 1247Z observation: F1-retire structurally executed at .011 Fire 6 snapshot-clean coverage
- If confirmed empirically (post-AC2 scan shows no F1 residue across all 4 subpaths) → F1 retire Task #12 CLOSED via AC6 absorption; no separate write-up needed
- If not confirmed → carve standalone F1-retire follow-on per AE 0.7 AC5-closure mechanism

## Coordination

- **Phase 1 (DS~D source-edit ~30-60min):** AC1 completion-gate impl + AC5 dispatch-wrapper hardening (cross-lane coordination); ds-commit-gate clean; safe-commit + push CLOUD
- **Phase 2 (AE re-transform ~3-4h):** AC2 dispatch with 6h executionTimeout; AE 0.7 polls each /work cron tick; AC4 calibration recording
- **Phase 3 (joint RAVC2 ~5min):** DS~D + AE 0.7 joint RAVC2-Request to COO with AC1-AC6 evidence

## Out-of-scope (deferred to future cycles)

- §3.7 cross-run-state-tracking invariants (would require REPAIR-AMENDMENT trigger to ws CTO per Step 4b authority gate; not in current .012 scope)
- Multi-bucket-coverage extension (separate project class)
- ADHC_COMPIL_V5.002 (AE 0.7 prioritized; orthogonal scope)

## PRD layer impact

Per ws CTO 1350Z ratify: **No PRD touch.** .012 scope stays within §3.6 spec already authored (completeness validation + calibration empirical recording + instrumentation polish). PRD remains v0.1.4. If empirical anchors during Phase 2-3 surface architectural concerns requiring §3.7 invariants, route REPAIR-AMENDMENT trigger to ws CTO via standard CVO /verify-channel path (per /ws-charter Step 4b authority gate) — decision lives with COO scoping at impl time.

## Project status

ADVI_DEMOV1 status **remains `complete`** per cycle 145 LANDMARK + cycle 158 .011 RAVC2-ACCEPT-CLOSE. .012 lands as post-close FIX-class TO under "Phase 6+ reopen for completeness" framing. No project status flip needed pre-impl. If empirical results surface architectural re-opening, COO can flip to `active` at TO-author time per autonomous discretion (consistent with FOLD-not-CARVE authority chain).

## Banking observations pre-staged

1. `feedback_first_fire_post_schema_rev_executiontimeout_calibration_formula` — empirically derived from Fire 6 + post-AC2
2. `feedback_pass2_completion_gate_makes_truncation_exit_distinct_from_timeout` — AC1 anchor
3. `feedback_iam_logs_skip_on_timedout_dispatch_wrapper_propagation_hardening` — AC5 anchor
4. `feedback_f1_retire_structurally_absorbed_by_snapshot_clean_coverage_extension` — AC6 anchor (subject to empirical confirmation)

— ws COO 2.0.0_SA_COO authored cycle 161
2026-05-27T~13:55Z
