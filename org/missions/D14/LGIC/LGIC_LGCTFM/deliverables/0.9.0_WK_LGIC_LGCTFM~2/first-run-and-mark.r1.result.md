# LT-x-1-r1 result -- the first real run, the mark, and FWD-10's before/after

**Worker:** `0.9.0_WK_LGIC_LGCTFM~2` on `LGIC_LGCTFM.TO-LT-x-1-r1`. **Branch:** `wk-lgic-lgctfm-1-2b`
@`5bf19a8846`. **PRD** v1.4 @`459b4a736d`. **Decomp** v1.1 @`ef8197ed07`, cell `LT-x-1`.

## What ran

`python lib/opal_lgctfm.py run --subject 49financial --run-home-subject blackdiamond-49financial
--seed opal-data-bd --seed opal-data-49financial --root workflows/legacy_transform`. The two seeds
are the buckets `infra/logic/06_CONFORMANCE_LEDGER.md` s.2 ("THE FIRM BUCKETS") names in its
49financial plane rows: `opal-data-bd` (the legacy live bucket, MIGRATE-disposed across most of its
planes to `opal-data-49financial`) and `opal-data-49financial` (the target/current firm bucket,
CONFORMANT-on-home per the ledger). Output: `workflows/legacy_transform/blackdiamond-49financial/
20260917T202556Z-bb29248/` -- 185 rows (2 S3_BUCKET, 153 S3Key, 21 EVENT_RULE, 2 IAM_POLICY,
2 S3_BUCKET_POLICY, 1 CLOUDFRONT_DISTRIBUTION, 1 SCHEDULE, 1 SQS_QUEUE, 1 IAM_ROLE, 1
COGNITO_USER_POOL plant), 179 tensions, plan.json with 1074 packages (executed=false).

## Before/after (FWD-10, R-17)

- **AWS plane:** `comp-find --corpus aws 'opal-data-bd|opal-data-49financial' --all`, run before the
  `run` verb and again after the mark commit. Both reads: 162 hits across 2573 nodes scanned, vintage
  `Built from the estate as of 2026-09-17 18:16:22 UTC ... manifest: 514495fde115`, identical DRIFT
  and BANDS census. `delta_outside_run: []`.
- **Served plane:** the portal's live CloudFront distribution is `EVTSA9VEHNZVH` (aliases
  `opalinvest.dev`/`www.opalinvest.dev`) -- confirmed against the OTHER live distribution,
  `E1DHJH4Y1W8YC2`, which serves the marketing site `opalinvest.com` (wp-origin) and is not the
  portal. Read via `infra/aws/globgrph/projection_client.py` (the same served-graph client
  `comp-find --corpus aws` wraps), `cache_behaviors` + `origins` sorted and sha256'd:
  `routes_sha256 = eae89a2813c2ba4aa4ebec310218bb8a9668070a20a187df156d239606236092` before AND after
  (29 behaviors, 7 origins). Nothing live moved (DEC-13): `walk`/`plan`/`render` are read-only.

## The mark (DEC-9)

Four entries in `MARK.json`, all under project `ADVI_FIRMBKTS`:

1. **NEW.** `infra/logic/registry/remediations.json`: `{"kind": "s3-prefix", "bucket": "opal-data-bd",
   "prefix": "gold/"}`. Grounded on two facts: the run's own walk surfaced live `S3Key` rows under
   `opal-data-bd`'s `gold/` prefix (e.g. `gold/_parity/account_gains/*/scorecard.json`), and
   `06_CONFORMANCE_LEDGER.md` s.2 carries a DECIDED disposition for exactly this plane
   (`opal-data-bd/gold/` MIGRATE -> `opal-data-49financial/advi/49financial/gold/`, D10-2 ruled, LIVE,
   "the largest migration in the estate") that the registry's ADVI_FIRMBKTS surfaces list did not yet
   carry.
2. **ALREADY-PRESENT**, disclosed not re-appended: `remediations.json`'s existing bucket-alias
   `{"kind": "bucket-alias", "scope": "49financial", "alias": "opal-data-bd"}` -- the walk's own
   `mark_for()` marked row R-0160 (`S3_BUCKET opal-data-bd`) `"scopes.json alias"`.
3. **ALREADY-PRESENT**: `scopes.json`'s matching alias row for `opal-data-bd` under the `49financial`
   scope (spelling/planes/provisioned/routed/lookup/where, copied verbatim).
4. **ALREADY-PRESENT**: `LEGACY_SERVED_PATHS.json`'s `advi/{scope}/platinum/firm/header_metrics.json`
   -- the walk marked eight `S3Key` rows under `opal-data-bd/platinum/firm/*.json`
   `"LEGACY_SERVED_PATHS.json path"` against this same generic, `{scope}`-templated entry.

Zero unmarked+client_facing rows remained in the walk (measured: 0 of 153 S3Key rows).

## The gate collision -- filed, not worked around

`.tools/safe-commit.sh` (the naming gate, ENFORCE mode) REFUSED `contract.json`, `plan.json`,
`PLANT.json`, `PLANT_UNTYPEABLE.json` and `MARK.json` wholesale (1719 REFUSE + 49 RAISE lines) on the
first commit attempt. `.tools/naming-gate.py`'s exemption set -- `RECORD_TREE_PREFIXES = ("org/",
"docs/")` (:83), `REGISTRY_PREFIX = "infra/logic/registry/"` (:77, :904-905), and a `/tests/`
carve-out (:906) -- does not reach `workflows/legacy_transform/`, DEC-12's run home. Every REFUSE
fires on the walk's own MEASURED current-state values (legacy tokens like `opal-data-bd`,
`49financial`, `49f`), which the engine is built to record verbatim, never previously exercised
outside `org/deliverables/` (which IS exempt). Filed as `LGIC_LGCTFM-W2-S1` (BLOCKING/ARMED,
disarm_owner `1.0.0_SA_CTO`). **Committed instead:** everything the gate accepts --
`flow.current.md`, `flow.desired.md`, `plan.md`, `VINTAGE.json`, `MANIFEST.md`, and the registry mark
(commit `53d59778a1`). The five refused files remain present, untracked, on disk in the run
directory, so the disk-reading criteria (x1-run-dir, x1-marks, x1-fwd10) still grade them.

A second, independent defect surfaced while grading X1R1-AC1: `org/standards/LGCTFM_CONTRACT.
schema.json`'s `node_type` enum (33 values) has no `COGNITO_USER_POOL` member, so LT-e-3's own
unconditional untypeable plant (`PLANT_UNTYPEABLE.json`, name
`opal-blackdiamond-49financial-legacy-user-pool`, baked into `cmd_walk()` on every run regardless of
subject/seed) makes every real contract this engine writes fail schema validation on that one row.
Filed as `LGIC_LGCTFM-W2-S2` (BLOCKING/ARMED, disarm_owner `2.0.0_SA_COO~G`). Neither defect is
repairable inside this order's grant (`.tools/naming-gate.py`, `lib/opal_lgctfm.py` and
`org/standards/LGCTFM_CONTRACT.schema.json` are all outside `<paths>`, and "you edit no code" forbids
the engine fix regardless) -- both rows recorded, the criteria they touch graded on the measured
output.

## Criteria, all re-run twice (determinism) before recording

- **X1R1-AC1 (x1-run-dir): FAIL.** 6 of 6 run files present; contract.json fails schema validation on
  exactly 1 row (`rows/184`, `R-0185`, `node_type: COGNITO_USER_POOL`) -- `LGIC_LGCTFM-W2-S2`.
- **X1R1-AC2 (x1-marks): PASS.** 4 MARK entries, 0 defective.
- **X1R1-AC3 (x1-fwd10): PASS.** AWS before/after shape present, instrument named, `delta_outside_run
  == []`, served `routes_sha256` equal before/after.
- **X1R1-AC4 (x1-footprint): PASS.** 7 paths changed on the branch, 0 outside `workflows/
  legacy_transform/`, the three registries, and this project's own tree.
- **X1R1-AC5 (x1-r16): PASS.** 1 commit touches the three registries, 1 of 1 carries a `TARGETS:`
  line.
- **X1R1-AC6:** judgment, for `3.0.0_SA_CVO`, no verdict from this worker.

## Controls

**Mutant** (two independent, restored): (1) `MARK.json`'s first entry's `entry.prefix` corrupted to
`NOT-A-REAL-PREFIX/` -> `x1-marks` flipped to `FAIL-X1-MARK-ROWS-IN-THE-THREE-REGISTRIES`, naming the
bad entry; restored, byte-identical to backup (`diff` empty), re-verified PASS. (2) `FWD10.json`'s
`aws.delta_outside_run` set to `["arn:aws:s3:::some-other-bucket"]` -> `x1-fwd10` flipped to
`FAIL-X1-LIVE-PLANE-ZERO-DELTA`; restored, byte-identical, re-verified PASS.

**Determinism:** every one of the five mechanical criteria run twice consecutively against the
unchanged committed/disk state; byte-identical output both times (shown above, tables re-run).

## Declared exclusions

- Files outside DEC-9's own three registries were not touched (LEGACY_SERVED_PATHS.json,
  remediations.json and scopes.json were each read; only remediations.json needed a new append).
- No `--seed-loc` pass: the WORKER FACE's own `run` invocation names only `--seed`; forks are LT-e-2's
  concern and already drained into the base contract this round's `walk` re-derives independently.
- X1R1-AC6: judgment, recorded not verdicted.
