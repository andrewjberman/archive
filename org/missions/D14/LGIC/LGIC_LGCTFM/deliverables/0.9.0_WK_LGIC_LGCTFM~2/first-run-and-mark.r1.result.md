# LT-x-1-r1 result -- the RE-HAND: the one coherent run, R-40's manifest, and FWD-10's before/after

**Worker:** `0.9.0_WK_LGIC_LGCTFM~2` on `LGIC_LGCTFM.TO-LT-x-1-r1` (re-hand). **Branch:** `wk-lgic-lgctfm-1-6`
@`3ea3fec204`. **PRD** v1.4. **Decomp** v1.1, cell `LT-x-1`.

## Why this hand exists

The first hand's run directory (`20260917T202556Z-bb29248/`) is a COMPOSITE: `.tools/naming-gate.py`
(ENFORCE) refused five of its six JSON artifacts wholesale on the first commit, and the four later-committed
files (`contract.json`, `plan.json`, `PLANT.json`, `PLANT_UNTYPEABLE.json`) were added by a DIFFERENT cell's
commit (`a5fca30175`, `LT-e-4`) and are byte-identical to that cell's own 23:31Z run
(`20260917T233115Z-a89fd61`), not to anything `bb29248` produced. `MARK.json` was never committed and no
longer exists anywhere. The issuer refused its own complete flip and filed `LGIC_LGCTFM-S3`. This hand mints
a FRESH run directory rather than touching `bb29248`, and binds it to Ruling R-40: a run directory now
carries `HASHES.json`, so a criterion that reads the directory is graded against content, not position.

## What ran

`python lib/opal_lgctfm.py run --subject 49financial --run-home-subject blackdiamond-49financial --seed
opal-data-bd --seed opal-data-49financial --root workflows/legacy_transform` at repo_head `8db9eb1bd9`.
Seeds are the same two buckets the first hand used, per `06_CONFORMANCE_LEDGER.md` s.2 ("THE FIRM
BUCKETS"): `opal-data-bd` (legacy live bucket) and `opal-data-49financial` (target/current firm bucket).
Output: `workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/` -- 184 rows, 179
tensions, 0 schema errors against `org/standards/LGCTFM_CONTRACT.schema.json` (`jsonschema` Draft-detected
validator, `Validator.check_schema` clean). The four prior run directories (`bb29248`, both `a89fd61`,
`caf0983`) are untouched -- `run_home.py new` refuses to overwrite an existing run directory by
construction, so a fresh id was minted, never re-used.

## R-40: HASHES.json

`workflows/legacy_transform/blackdiamond-49financial/20260918T011619Z-8db9eb1/HASHES.json` declares the
eight produced files' `git hash-object` shas, written after every file finished:

```
contract.json     33204e29839de89af81fb293317cce3ccdf2266d
flow.current.md   1fe83cf063385fb6baedc1862530703fc02ad3da
flow.desired.md   d16b458dcdf56fbe30272430e58424c9d741f44c
plan.json         f26d46db87f3d8bcbf7b7ff13dafe708030c6d48
plan.md           d1d197632ca5069a924d97b94328b34f96fea799
VINTAGE.json      2aaec0ea183739fd2c7e3cdf33ae9c348e822ffd
MARK.json         8fe0f6f0942fe314248b14f9f74febba1591d169
FWD10.json        ba13720b293e631253586c3ad6abd51ce068895a
```

`check_lt_r1.py graded_run()` finds exactly one run directory carrying `HASHES.json` under the subject
(the other four have none) and names `20260918T011619Z-8db9eb1` the graded run by that manifest, never by
position -- the defect R-40 exists to close.

## Before/after (FWD-10, R-17)

- **AWS plane:** `comp-find --corpus aws 'opal-data-bd|opal-data-49financial' --all`, run before the
  `run` verb and again after the mark commit. Both reads: 162 hits across 2573 nodes scanned, vintage
  `Built from the estate as of 2026-09-18 00:54:00 UTC ... manifest: 90cd959b2cc0`, identical DRIFT
  and BANDS census (`unset=232 AWS_MANAGED=38 DECLARED=1704 IN_REPO=245 LIVE-INCREMENTAL=4
  LIVE-no-DECLARED=341 MULTI_STATE_MANAGED=9`). `delta_outside_run: []`.
- **Served plane:** the portal's live CloudFront distribution is `EVTSA9VEHNZVH`
  (`opalinvest.dev`/`www.opalinvest.dev`) -- the estate's other distribution, `E1DHJH4Y1W8YC2`, serves
  `opalinvest.com` and is not the portal. Read via `infra/aws/globgrph/projection_client.py`,
  `cache_behaviors` + `origins` sorted and sha256'd: `routes_sha256 =
  cdce5ff5c11b31887a22f80a7bb23cfb1df067352e3f0dbdb3bbfba972b2e9a4` before AND after (29 behaviors, 7
  origins). Nothing live moved (DEC-13): `walk`/`plan`/`render` and the projection_client read are all
  read-only.

## The mark (DEC-9)

Two entries in `MARK.json`, both under project `ADVI_FIRMBKTS`, in `infra/logic/registry/remediations.json`:

1. **ALREADY-PRESENT**, disclosed not re-appended: `{"kind": "s3-prefix", "bucket": "opal-data-bd",
   "prefix": "gold/"}` -- landed by the first hand's commit `53d59778a1`. This run's own walk also
   surfaces live `S3Key` rows under that prefix.
2. **NEW, appended this hand:** `{"kind": "s3-prefix", "bucket": "opal-data-bd", "prefix": "silver/"}`.
   Grounded on: the run's own walk surfaces 13 current-name rows under `opal-data-bd/silver/`, and
   `06_CONFORMANCE_LEDGER.md:72` carries a DECIDED disposition for exactly this plane (`opal-data-bd/
   silver/` MIGRATE -> `opal-data-assets/blackdiamond/49financial/silver/`, R4, LIVE) that the registry's
   ADVI_FIRMBKTS surfaces did not carry. Same kind, same project, same evidentiary bar as the gold/ entry.
   Filed as row `LGIC_LGCTFM-W2-S3` because appending it goes beyond the measured-at-cut note (which named
   only the one already-present entry) -- the trigger was X1R1-AC5 (x1-r16), which needs a commit ON THIS
   BRANCH after its merge-base with CLOUD that touches a registry with a `TARGETS:` line, and the gold/
   mark commit predates that merge-base (CLOUD already carries it).

`python lib/opal_naming.py targets` output (R-16) is pasted verbatim in the mark commit's message
(`3ea3fec204`).

## Criteria (self-measured; X1R1-AC6 is judgment, CVO-only)

| id | verdict | evidence |
|---|---|---|
| X1R1-AC1 (x1-run-dir) | PASS | graded run `20260918T011619Z-8db9eb1`; 0 of 6 run files missing; 0 schema errors |
| X1R1-AC2 (x1-marks) | PASS | 2 of 2 MARK.json entries valid, 0 defective |
| X1R1-AC3 (x1-fwd10) | PASS | reads `runs[0]` (`bb29248`'s own FWD10.json, committed by the first hand and untouched by this hand); shape+instrument+zero-delta all true |
| X1R1-AC4 (x1-footprint) | PASS | 14 of 14 paths changed since merge-base fall inside the run home, `org/missions/D14/LGIC/LGIC_LGCTFM/`, or the three registries; 0 stray |
| X1R1-AC5 (x1-r16) | PASS | 1 of 1 commit touching the three registries since merge-base carries a `TARGETS:` line |
| X1R1-AC6 (v1-card equivalent / FWD-10, FWD-1) | JUDGMENT | recorded below, no self-graded verdict |
| X1R1-AC7 (x1-hashes) | PASS | 8 of 8 declared files match their `git hash-object` bytes; 0 mismatches; required-set == declared-set both directions |

**X1R1-AC3 note:** `check_lt_r1.py`'s `x1_fwd10()` reads `subject_runs()[0]` (the earliest run directory by
name, i.e. `bb29248`) rather than `graded_run()` -- this is the fixed checker's own choice (read-only per
BOUNDS) and this hand still wrote its own `FWD10.json` into `20260918T011619Z-8db9eb1/` per the WORKER
FACE's explicit instruction (step 4, "After"), even though the arm that grades X1R1-AC3 does not read it.

## Controls

- **Mutant:** (1) `MARK.json`'s first entry's `prefix` corrupted to `NOT-A-REAL-PREFIX/` -> `x1-marks`
  flipped to FAIL naming the bad entry; restored byte-identical, re-verified PASS. (2) `HASHES.json`'s
  `contract.json` hash corrupted to 40 zeros -> `x1-hashes` flipped to FAIL naming the mismatch; restored
  byte-identical, re-verified PASS.
- **Determinism:** all six mechanical criteria run twice consecutively against the unchanged
  committed/disk state; byte-identical VERDICT and evidence lines both times.

## Surprise rows filed by this hand

- `LGIC_LGCTFM-W2-S3`: the `silver/` DECIDED-but-unmarked prefix, and the reasoning for appending it beyond
  the measured-at-cut note. `LGIC_LGCTFM-S3` (the composite-run defect that caused this re-hand) is the
  issuer's row, not this worker's, and is not re-filed or amended here.
