# FRESHGUARD leg-5 v2: PARITY-DRIFT signal (repo_head_sha vs live origin HEAD) -- design for CTO arch-gate

**Author:** 0.7.0_AE_CloudOps~B · **Date:** 2026-07-08 · **Status:** DESIGN (staged for CTO arch-gate; NOT applied) · BUILD blocked on cross-region secret (tracked separately, see "Blocker" below)
**TO:** NFRA_GLOBGRPH.FRESHGUARD leg-5 (extension) · **Incident this closes:** code_heat's 9-day stale-checkout live-read (the class leg-5 v1 cannot catch)

## Problem (recap, why v1 is insufficient for this specific class)

leg-5 v1 (`freshness_alarm.tf`, commit 94c4739a0) alarms on served-object AGE. It catches "producer stopped" (no object age advances) but NOT "producer re-emits STALE" -- the exact code_heat incident, where the served parquet's `last_modified` advanced daily (fresh object) while its CONTENT (`repo_head_sha`, a parity column 0.8.0~B built for exactly this) stayed frozen at a 9-day-old commit because the emitter's local git checkout was never synced. Object-age reads GREEN through the entire incident. This is a structural blind spot of the age-only signal, not a tuning issue -- v2 needs a CONTENT-based signal.

## Design

**Signal:** the served artifact's own `repo_head_sha` column vs the LIVE origin default-branch HEAD, per repo. Mirrors `code_heat_parity.py`'s VINTAGE-PRIMARY philosophy (source-read this session) with one adaptation: `code_heat_parity.py` needs a local git checkout (`git -C root rev-parse HEAD`), which a Lambda doesn't have -- v2 substitutes a GitHub API call for the live-HEAD read.

**Why "stuck-duration", not bare HEAD-mismatch (the same lesson `code_heat_parity.py` already learned):** `ajb_workspace` HEAD advances constantly (multi-agent, seconds-to-minutes cadence this session alone). A bare `repo_head_sha != live_HEAD` check would ALARM almost continuously (false-positive storm) the instant any commit lands after an emit -- that's expected/healthy for a periodic live-read, not staleness. The robust signal is **how long `repo_head_sha` has been STUCK at the same value while live HEAD keeps moving** -- exactly the incident shape (frozen for 9 days while `ajb_workspace` accumulated 150+ commits).

**Mechanism (per repo, e.g. `ajb_workspace` / `portal`):**
1. Read the served parquet's current `repo_head_sha` (already a column; requires a Lambda with `pyarrow` -- leg-5 v1's Lambda is deliberately dependency-free/tiny, so v2 needs either a `pyarrow` layer added to the existing `freshness_alarm` Lambda or a small sibling Lambda reusing the derive-image's already-`pyarrow`-equipped runtime pattern. Recommend the layer -- keeps one Lambda, one registry, consistent with leg-5's "generalize, don't fork" design principle).
2. Fetch the live branch-HEAD SHA via GitHub REST API: `GET https://api.github.com/repos/Opal-Capital/{repo}/commits/{branch}` -- `Authorization: token <PAT>` header, `PAT` from the `github-token` secret. **Grounded this session (live `git branch`/`git remote show origin`): the branch to diff is the AGENT WORKING branch, NOT the GitHub repo's default branch** -- `ajb_workspace`'s remote default is `main`, but every agent commits to `CLOUD` (CLAUDE.md "Working branch: CLOUD"); `portal`'s remote default is also `main`, but agents work `DEV` (CLAUDE.md "Portal main worktree stays on DEV, always"). So the API call MUST explicitly target `ref=CLOUD` / `ref=DEV`, never the bare default-branch endpoint -- calling `.../commits/main` would silently diff against the wrong branch and could show false-current or false-stale depending on how far `main` has drifted from the working branch.
3. Maintain a tiny per-repo state object (`s3://opal-313476888478-globgrph/warehouse/freshness_parity_state/<repo>.json` = `{last_seen_sha, first_seen_at}`) -- NOT DynamoDB, to stay consistent with leg-5's S3-object-centric design (no new AWS service surface for a 2-field state blob):
   - If the parquet's current `repo_head_sha` == `last_seen_sha` (unchanged since last check): `stuck_hours = now - first_seen_at`.
   - If it changed: reset `first_seen_at = now`, `last_seen_sha = <new sha>`, `stuck_hours = 0`.
4. **Alarm condition:** `repo_head_sha != live_HEAD_sha` AND `stuck_hours > threshold` (proposed 48h -- 2x code_heat's historical ~26h cadence, mirrors leg-5 v1's own threshold reasoning + tool_activity's precedent). If `repo_head_sha == live_HEAD_sha`, never alarm regardless of `stuck_hours` (a quiet repo with no new commits is NOT stale -- the checkout correctly reflects reality).
5. Publish a metric (`Opal/FreshnessAlarm`, new metric name `ProducerParityStuckHours`, dimensioned `Producer=<repo>`) -- reuses leg-5's existing alarm/SNS/`missing-data=breaching` pattern exactly; a NEW `aws_cloudwatch_metric_alarm` per repo (2 more registry-style entries, same `critical_surface_alerts` topic).

## Blocker (tracked, not blocking the design)

Cross-region secret: `github-token` lives in `us-east-2`; the `freshness_alarm` Lambda is `us-east-1`. Base `0.7.0_AE_CloudOps` offered a multi-region Secrets Manager replica (~5min TF) after their leg-4/collision-fix work. **This design is build-ready the moment that lands** -- no other blocker.

## Blast radius / rollback

Additive: 1 pyarrow Lambda layer, 1 new IAM grant (`secretsmanager:GetSecretValue` on the replicated `github-token` ARN, read-only), 2 new S3 state objects (tiny, self-managed), 2 new CloudWatch alarms (reusing the existing topic). No change to any existing v1 registry entry or alarm. Rollback = destroy the new alarm resources + layer attachment; v1 keeps functioning independently (v1 and v2 are additive siblings, not a replacement).

## I3 exercise (exists != fires) -- CVO exercise-verifies on build

- **RED fixture:** the REAL code_heat incident is directly replayable -- seed the state object with `{last_seen_sha: "15e3a25b9c9a", first_seen_at: <9 days ago>}` (the actual frozen SHA + actual incident duration this session's grounding already captured) against a parquet/live-HEAD pair where they genuinely differ -- `stuck_hours` computes to ~216h > 48h threshold -> ALARM. Demonstrable without needing to reproduce the incident live.
- **GREEN:** current state (repo_head_sha == live HEAD after this session's manual emit-fix) -> no alarm regardless of threshold.
- Post-build: confirm live alarm state = OK (current), supply the red-fixture computation as the I3 evidence; CVO exercise-verifies.

## Ask

Arch-gate GO on: (a) the pyarrow-layer-vs-sibling-Lambda choice (recommend layer), (b) the S3-state-object-vs-DynamoDB choice (recommend S3, consistency with leg-5's design), (c) the 48h stuck-duration threshold, (d) branch targets CLOUD (ajb_workspace) / DEV (portal) -- grounded live this session, not the repos' GitHub-default `main`. On GO + the cross-region token landing: I implement (Lambda layer + state objects + 2 alarms + registry-consistent IAM), exercise the RED/GREEN fixtures, RAVC CTO + CVO.
