# FRESHNESS-CHECKER POINTER HARVEST — POINTERS ENUMERATED (routes NOT joined)

**Author:** `0.7.0_AE_CloudOps~B` · **Date:** 2026-08-04 ~2340-0000Z · **HEAD at harvest:** `920a7c017`
**Authority chain:** Andrew-direct ~0355Z (the homing-signal bet, recorded @2937949e2) → CTO 054440Z
(kill-lane rider: checker-class EXCLUDED from dead-consumer kills until this lands) → CTO 055416Z
(predicate widened to killed-but-git-preserved) → CTO 064222Z (the split: POINTERS ENUMERATED now,
ROUTES JOINED waits on the artifact-identity primitive; NO string hand-join — the 4-way bell
collision is the standing proof lookalike keys lie).

## DECLARED LIMITATION (binding, per CTO 064222Z)
This deliverable ENUMERATES pointers with per-class denominators. It does NOT read them as a
deprecated-route map: the join structurally waits on the identity primitive (a PRD premise,
@655e3f551 population proof: zero cross-plane edges, json/ tier unmodeled). Every claim below is
exactly as strong as its instrument; residues are named, not silently absent.

---

## CLASS A — DECLARED CONFIG ROWS (live surface) — 99 rows / 99 pointer-bearing / 0 without

Sidecar with every row: `FRESHNESS_HARVEST_classA_rows_20260804.json` (regenerable from the five
configs at HEAD; fields: artifact_id, pointer, pipeline, severity, cadence, freshness_basis, scripts).

| config | rows | pointer grain |
|---|---|---|
| `data/served_freshness_config.yaml` | 13 | s3_key_prefix (key/prefix grain) |
| `data/ddb_freshness_config.yaml` | 2 | ddb:table (opal-users-v2, opal-routing-config) |
| `data/black_diamond/scripts/gold/gold_freshness_config.yaml` | 37 | s3_key_prefix |
| `data/cot/scripts/gold/gold_freshness_config.yaml` | 9 | s3_key_prefix |
| `data/inf/scripts/gold/gold_freshness_config.yaml` | 38 | s3_key_prefix |

Prior-window context stands: served config (authored 06-17, newest surface) tracked 10/13 LIVE
routes — recent authorship tracks live routes by construction. **The archaeology weight is in the
OLDER surfaces below.**

## CLASS B — EMBEDDED IN-CODE CHECKS (live surface, file grain) — 138 files at HEAD

Pattern: `grep -rlE "freshness|staleness|stale_|max_age|is_stale" --include="*.py"`, pycache
excluded. Per-tree denominators (re-derivable):

| tree | files |
|---|---|
| infra/aws/lambda | 79 |
| data/inf | 33 |
| data/cot | 9 |
| data/mdpf | 5 |
| data/etfs | 3 |
| data/black_diamond | 8 |
| data/assets | 1 |

**RESIDUE (named):** key-grain pointer extraction from these 138 files is NOT done — bucket-grain
only where harvested (B′ below). This is the long tail; it does not gate the rider lift if CTO
accepts file-grain + the config/killed classes as "pointers banked" — CTO's call, flagged.

## CLASS B′ — CHECKER-SHAPED REPO DIRS, LIVE FLEET = ZERO (the name-class was
positive-controlled against the live Lambda list in the 0105-0600Z window: 0 of 50 live functions
match fresh/stale/monitor/checker/alert; control query returns mdpf-daily-trigger)

| repo dir | bucket-grain pointers | note |
|---|---|---|
| `infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker` | opal-data-bd, opal-data-portal-v2, opal-data-schwab | the terminated-gate family |
| `infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe` | opal-data-bd, opal-data-cot | |
| `infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe` | opal-data-bd, opal-data-cot | cross-firm pointer pair — note only, not adjudicated here |
| `infra/aws/lambda/inf-pipeline/inf-gold-freshness-guard` | opal-data-inf | TF deleted 07-17 (@dd7d2da955) |
| `infra/aws/lambda/schwab-bronze-freshness` | (source DELETED @1d920662fe 08-04; only .pyc remains at HEAD) | source recoverable at `1d920662fe^` |
| `infra/aws/globgrph/freshness_alarm` | no S3 literals — CloudWatch-metric pointer class | TF deleted 07-17 (@858554332d) |
| `infra/aws/globgrph/tool_activity_freshness` | no S3 literals — metric pointer class | TF deleted 07-17 (@858554332d) |

(`data_refresh` and `smartx_jwt_refresher` matched the name glob but are refresh/JWT tools, not
freshness checkers — excluded, stated so the denominator is honest.)

## CLASS C — KILLED-BUT-GIT-PRESERVED (mined; each recoverable at the cited vintage)

| definition | killed | vintage for recovery | pointers named |
|---|---|---|---|
| **K1 dead role** (mdpf checker scope) | pre-08-03 | `infra/aws/terraform/mdpf-pipeline/iam.tf@440d16e018:759-842` (VERBATIM re-grounded this harvest — the CTO relay's bare "iam.tf" cite resolves to the MDPF root, not globgrph) | `platinum/mdpf/aggregate_aua_timeseries.json` (underscore root artifact) · `platinum/mdpf/aggregate_aua/*` · `platinum/mdpf/_g6_fixture/*` |
| `freshness_alarm.tf` + `tool_activity_freshness.tf` + `freshguard_derive_watchdog.tf` (globgrph) | 07-17 @858554332d | `858554332d^` | metric-class |
| `inf-gold-freshness-guard.tf` | 07-17 @dd7d2da955 | `dd7d2da955^` | opal-data-inf gold |
| `bd-gold-detail-checker` (lambda) | 06-29 @712c9888c0 | `712c9888c0^` | opal-data-bd |
| `schwab-bronze-freshness` (lambda source) | 08-04 @1d920662fe | `1d920662fe^` | opal-data-schwab bronze |
| `INF_D_00e.fresh_header_supplement.py` | 06-30 @a406ed891e | `a406ed891e^` | inf gold header |
| Kill records | — | `org/critical_paths/.open_deploys/`: freshguard-leg4-writer-wiring-finish.json, freshguard-leg5-v2-parity-drift.json; + freshness-alarm-teardown-20260717.json (deleted @b0918e876c, recoverable `b0918e876c^`) | — |

**Method note:** the deletion mine's first pass ran a `git show` cite with `2>/dev/null` and
mis-resolved the K1 file — caught by the CLAUDE.md rule (positive control beside every ABSENT
verdict), re-grounded loud: the cited iam.tf is the **mdpf-pipeline** root (842 lines at vintage),
not globgrph (235). The wrong-root cite came IN with the relay; recorded so the next reader does
not chase globgrph.

## RIDER LIFT CONDITION (CTO 054440Z: "harvest complete = both halves")
- LIVE half: Class A complete (99/99), Class B file-grain complete (138, key-grain residue named),
  B′ complete (7/7 dirs).
- KILLED half: Class C mined from deletion log + kill records + the K1 role; the mine's pattern +
  denominators printed for re-derivation.
**CTO adjudicates whether the named residue (Class B key-grain) blocks the lift.**
