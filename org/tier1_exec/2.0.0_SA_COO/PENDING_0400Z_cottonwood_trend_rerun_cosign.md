# PENDING TIME-TRIGGER — ~04:00Z 2026-07-23 — Cottonwood trend re-run + COO counter-sign

**Owner of the RUN:** `0.4.0_DS_ClientPlatform` (inside his already-scheduled post-B5 pass).
**Owner of the COUNTER-SIGN:** COO (`2.0.0_SA_COO` if live; else the live COO/CTO — this record is the carrier).
**Authority:** CTO order 013852Z (pre-signed conditioned) + the standing Andrew build-override that ran
tonight's Cottonwood builds. CTO co-sign half PRE-SIGNED; COO counter-sign is AT THE ARTIFACT.

## Why it exists
Tonight's served Cottonwood trend (`aggregate_aua_timeseries.json`) is **0/427 all-null** — verified by
COO direct-read — because its axis ends 07-20 and Cottonwood data starts 07-21 (zero overlap). A value
enters ONLY when the producer RUNS against an axis that carries the date. So real morning trend points
require a producer re-run AFTER tonight's 02:04Z nightly advances the global axis.

## The sequence (fires ~04:00Z, ONLY if conditions met)
1. ⛔ **HARD PRE-FLIGHT:** verify `axis_last >= 2026-07-21` (the 02:04Z nightly advanced the axis). If
   still 07-20 → DO NOT run; report axis-stale; the conservative line (empty tonight, fills when 6d lands
   in daylight) stands.
2. ⛔ **IF THE 02:04Z NIGHTLY FAILED** (ADVI-fix closure risk is live) → run does NOT fire; conservative
   line stands unmodified.
3. Re-run `build_cottonwood_mdpf_slice.py --upload` (one run; same build vs the advanced axis; NOT an
   ad-hoc validation run — sovereign-override authorized).
4. **PRINT: identities (model+non_model==total; count-axis distinct-not-sum) + the NON-NULL COUNT**
   (expected `covered_dates >= 1`, `model_aua` non-null on 07-21 at minimum). Zero non-null = FAILED
   render, not a pass.
5. Republish the ONE key `aggregate-aua-timeseries.json` on refreshed pins.

## COO counter-sign conditions (verify AT THE RE-PUBLISHED ARTIFACT, per tonight's verify-not-transcribe)
- (i) axis advanced (`axis_last >= 07-21`) — verified BEFORE the run,
- (ii) identities green on the re-published artifact,
- (iii) **non-null count > 0 PRINTED and confirmed on the actual file** (read it, do not transcribe).
Only then does the served republish of the trend key complete. **No blank-check pre-sign of an artifact
that does not exist yet.**

## Andrew-facing horizon (accurate at both)
- Trend EMPTY tonight (verified).
- REAL first points at dawn IF nightly lands AND the ~04:00Z re-run passes its printed checks.
- SELF-SUSTAINING from tomorrow night once the 6d dispatcher leg lands (G3w, daylight, CTO-gated).

**Delete this file once the counter-sign fires (or the conservative line is confirmed on a stale/failed
nightly).**

-- `2.0.0_SA_COO`, recorded 2026-07-23 ~01:40Z
