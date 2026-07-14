# OPAL_ASSETS V2 — Silver Converter Lambda Contract (V2-7 container <-> V2-8 converters)

**Status:** DRAFT — AE (TF-side) half committed; DS (converter-side) half lands after V2-6.
**Co-cited by:** `OPAL_ASSETS.V2-7.silver-container.md` (0.7.0_AE_CloudOps) + `OPAL_ASSETS.V2-8.silver-converters.md` (0.4.0_DS_ClientPlatform).
**PRD:** `docs/architecture/OPAL_ASSETS_V2_PRD.md` §3 rulings 22–26 (@ 53ba45c5f).
**Purpose:** one committed seam definition so V2-7's TF and V2-8's converter code land against the SAME
names, prefixes, and exclusions. Cells marked `TBD-DS` are DS's to fill; cells marked `PROPOSED` are
AE defaults DS may veto before the TF lands. Nothing here is applied until the V2-5 cert gate opens
(V2-7 `<go>`); this note is the pre-gate coordination COO authorized 072322Z.

---

## 1. Naming convention (AE half — fixed unless DS vetoes)

| Thing | Pattern | Precedent |
|---|---|---|
| Converter lambda | `opal-assets-silver-{family}` | `opal-assets-ingest-mirror`, `opal-assets-daily-emitter` |
| Execution role | `opal-assets-silver-{family}-role` | `opal-assets-ingest-router-role` |
| Silver-write policy | `opal-assets-silver-write-{source}` (NEW — see §4) | `opal-assets-write-{source}` |
| Source dir | `infra/aws/lambda/opal-assets/opal-assets-silver-{family}/` | mirror/emitter layout |
| Handler | `lambda_function.lambda_handler` | repo standard |
| Runtime | `python3.12` | mirror |
| DLQ | `opal-assets-silver-dlq` (one queue, all event paths) | — |
| Sweep rule | `opal-assets-silver-{family}-sweep-daily` | `opal-assets-ingest-mirror-{inf,cot}-daily` |

Every lambda registers in `infra/aws/lambda/ci/lambda-source-map.json` at its own build (Rule 4);
artifacts via `ci/build-and-upload.sh` to `opal-assets/{function}.zip` (Rule 1/2 cycle).

## 2. Channel families (PROPOSED — granularity is DS's call, ruling 23 "typed vendor-shape boundary")

AE default: family == vendor shape, so a drift-raise boundary is one vendor's shape, never a union.

| family | covers `{source}/{scope}` | vendor shape | V2-8 order |
|---|---|---|---|
| `schwab` | `schwab/08242234`, `schwab/08335338` | CRS fixed-width/csv + ruling-11a T1 trailer recon; masters NEVER commingled — one lambda, two scope lanes, separate writes | 1 |
| `orion` | `orion/inflection` | flat `.jsonl.gz` API dumps | 2 |
| `eclipse` | `eclipse/inflection` | `TBD-DS` (624 mirrored keys — DS grounds shape) | 2 |
| `blackdiamond` | `blackdiamond/cottonwood` | `.xlsx` forwardfill + `_complete` sidecars (sidecars are signal, not data) | 2 |
| `etf` | `trueshares/{DIVZ,IDVZ}`, `pathfinder/{filepoint→PFOE,PFDE}`, `msn/*` | per-vendor parse branches behind one fact-table target; legacy CSV silver keeps serving until ruled cutover | 3 |
| `smartx` | `smartx/*` (C5 narrows) | `TBD-DS` (0.5.0 co-owns) | 4 |

`etf` as ONE family vs three is the weakest cell — DS decides at V2-8 pickup; TF cost of splitting later
is one module block + one role each, no restructure (the §4 policy shape is per-source already).

## 3. Event-prefix map (ruling 22) + meta-key exclusion (rulings 21/25)

The monolith bucket's notification config is EMPTY (measured); V2-7 is its FIRST writer and it stays
monolith-only, ONE `aws_s3_bucket_notification` resource (the singleton hazard — no pipeline adds its
own). Two independent exclusion belts:

- **Belt 1 (structural, TF):** every rule is `prefix = {source}/{scope}/bronze/` AND
  `suffix = <data extension>`. Meta lives at `{source}/{scope}/meta/` — a DISJOINT prefix (ruling 21),
  so no meta key can match any rule. In-bronze sidecars (`*_complete`, `_BRONZE_COMPLETE.json`) fail
  the suffix. S3 notification filters cannot negative-match; suffix-scoping is the only structural form.
- **Belt 2 (code, DS):** converter no-ops loud (`SKIP: non-data key`) on anything that is not its
  vendor shape — the belt that survives a new sidecar spelling.

| rule | prefix | suffix | target |
|---|---|---|---|
| 1 | `schwab/08242234/bronze/` | `TBD-DS` (CRS ext) | `opal-assets-silver-schwab` |
| 2 | `schwab/08335338/bronze/` | `TBD-DS` | `opal-assets-silver-schwab` |
| 3 | `orion/inflection/bronze/` | `.jsonl.gz` | `opal-assets-silver-orion` |
| 4 | `eclipse/inflection/bronze/` | `TBD-DS` | `opal-assets-silver-eclipse` |
| 5 | `blackdiamond/cottonwood/bronze/` | `.xlsx` | `opal-assets-silver-blackdiamond` |
| 6–8 | `trueshares/DIVZ/bronze/`, `trueshares/IDVZ/bronze/`, `pathfinder/filepoint/bronze/` | `TBD-DS` | `opal-assets-silver-etf` |
| 9 | `msn/` (fallback tier — scope open-ended) | `TBD-DS` | `opal-assets-silver-etf` |
| 10 | `smartx/` | `TBD-DS` | `opal-assets-silver-smartx` (C5) |

Silver output grammar (ruling 23, fixed): `{source}/{scope}/silver/{fact_table}/` hive `date=`
partitions. Conversion manifests → `{source}/{scope}/meta/` (disjoint from every guarded prefix).

## 4. Execution roles (never-widen, per-channel, monolith-scoped)

Per family: `opal-assets-silver-{family}-role` attaches EXACTLY —
1. `AWSLambdaBasicExecutionRole` (logs);
2. **the one-way fan-in fence** (`opal-assets-one-way-fan-in-fence`) — provably incapable of writing any
   source bucket or Door 6, same as the router;
3. **NEW `opal-assets-silver-write-{source}`** — `s3:PutObject` + `s3:GetObject` (read-back verify law)
   on `{source}/{scope}/silver/*` + `{source}/{scope}/meta/*` ONLY, per owned scope;
4. **bronze READ-ONLY** — `s3:GetObject` on `{source}/{scope}/bronze/*` + conditioned `ListBucket`.

Deliberately NOT the existing `opal-assets-write-{source}` (it grants Put on the whole source tree incl.
`bronze/` — a converter that can mutate raw bronze is Rule 17a one layer up). A converter role can READ
its bronze and WRITE its silver+meta, and nothing else in the estate. DLQ: `sqs:SendMessage` on
`opal-assets-silver-dlq` only. 22a at apply: per role, live simulate, one `--resource-arns` per call,
REAL keys, isolated positive control, fence negatives (firm bucket, Door-6 key, out-of-scope monolith
prefix, own-bronze `PutObject` → expect Deny).

## 5. DLQ + sweep (ruling 22 — the sweep is load-bearing, not belt)

- `opal-assets-silver-dlq`: SQS, 14-day retention, wired as every converter's async on-failure
  destination. NOT an alarm (no-alarms constraint): the sweep reads it.
- Per-family sweep `opal-assets-silver-{family}-sweep-daily` invokes the SAME converter lambda in sweep
  mode (ruling 24 — one code path): computes bronze<->silver per-folder set-identity, converts misses,
  drains+reports DLQ entries, emits denominator + verdict to `{source}/{scope}/meta/`.

| family | bronze landing window (grounded) | sweep slot (PROPOSED) |
|---|---|---|
| `blackdiamond` | mirror cot walk 03:30Z | 05:00Z |
| `orion` / `eclipse` | mirror inf walk 14:15Z | 16:00Z |
| `schwab` | C3 daily REST (0.6.2) `TBD` | landing+2h |
| `etf` | 22:00Z native landing | 23:30Z |
| `smartx` | C5 cadence `TBD` | landing+2h |

Reserved concurrency PROPOSED = 2 per converter (event bursts tolerable, skip-if-landed idempotent;
the mirror's =1 was pass-serialization, a different problem). DS may veto per family.

## 6. Open cells (the whole point of committing this early)

1. `etf` family granularity (one vs three) — DS at V2-8 pickup.
2. Data-extension suffixes per family (rules 1,2,4,6–10) — DS grounds on LIVE mirrored bytes
   (ruling 26: never on recollection).
3. `msn`/`smartx` open-ended scopes: rules 9/10 use the source root as prefix (scope segment is `*` in
   the grammar) — converter code carries the scope parse; confirm no meta collision (`meta/` is per
   scope, `{source}/{scope}/meta/`, so root-prefix rules MUST still suffix-scope to data extensions).
4. Schwab conversion manifest shape for the two-master lanes (NEVER summed — two manifests, never one).
5. Sweep slots vs C3/C5 cadences once those land.

— AE half: 0.7.0_AE_CloudOps, 2026-07-14 ~07:3xZ. DS half: pending V2-6.
