# LGIC_LGCTFM.TO-LT-x-5-r4 -- RESULT (`0.9.0_WK_LGIC_LGCTFM~1`)

**Branch:** `wk-lgic-lgctfm-4-3` (linked worktree). **Commit, LOCAL:** `9160215d2b` (the run, HASHES.json, FWD10.json,
the record and one surprise row).
**Order status: stays `pending`** -- X5R4-AC3 reads FAIL and a FAIL row leaves the order open.

## Verdicts

| criterion | verdict | deciding line |
|---|---|---|
| X5R4-AC1 | **PASS-by-output** | `VERDICT: PASS-X4-RUN` |
| X5R4-AC2 | **PASS-by-output** | `VERDICT: PASS-X4-FLOOR` |
| X5R4-AC3 | **FAIL** | `VERDICT: FAIL-X4-NO-REGISTRY-MOVE` -- 2 path(s) changed, both an unrelated project's |
| X5R4-AC4 | RECORDED (judgment) | graded at L9 by `3.0.0_SA_CVO`; no verdict here |

`selftest-arms` was run FIRST as required: `PASS-ARMS-DISCRIMINATE`, 34 arms (13 POSITIVE-SATISFIABILITY, 21
mutant/other), both before this worker's commit and again after it.

## The run

```
python lib/opal_lgctfm.py run --subject 49financial --run-home-subject blackdiamond-49financial \
  --seed opal-data-bd --seed opal-data-49financial --root workflows/legacy_transform
```

**No token/leg flag was added.** The order's template names `<the token/leg flags LT-e-6 built>`; reading
`lib/opal_lgctfm.py`'s `p_run` argparse block (`--subject`, `--run-home-subject`, `--seed`, `--seed-loc`, `--root`,
`--plant-untypeable`) shows LT-e-6 added none -- its repoint (`live_iam_plane()`) and hand-surface guard
(`source_map_guard()`) run unconditionally inside `cmd_walk`/`cmd_run`, not behind a flag. So the invocation is
exactly round 3's, unchanged.

Run id `20260919T034609Z-c28c728`, rc=0. 404 rows (402 involved + 2 standing plants), 356 tensions, 19 node_types,
token floor **90 hits of 2595 nodes scanned** at vintage `Built from the estate as of 2026-09-19 03:32:23 UTC`.

## HASHES.json and FWD10.json -- neither is emitted by the `run` verb

Confirmed directly: the fresh run directory carried `COVERAGE_EVIDENCE.json`, `HAND_SURFACES.json`, `PLANT.json`,
`PLANT_UNTYPEABLE.json`, `VINTAGE.json`, `contract.json`, `flow.current.md`, `flow.desired.md`, `live-iam-census.json`,
`plan.json`, `plan.md` -- no `HASHES.json`. `check_lt_r4.py`'s `_newest_run()` requires
`os.path.isfile(os.path.join(d, "HASHES.json"))` before a post-cut run is found AT ALL, so without it X5R4-AC1 would
read `FAIL-X4-RUN ("no post-cut run with HASHES.json ...")` regardless of the run's own content. This worker wrote
both files, following the R-40 pattern LT-x-1 (round 1) established (the order's own text: "the run lands ... with its
own `HASHES.json` (R-40)"):

- **`HASHES.json`**: `git hash-object` over all 12 files the run directory carries, hashed AFTER `FWD10.json` was
  finished, per R-40 ("`HASHES.json` does not hash itself"). This round's file set differs from round 1's fixed
  8-key list (no MARK this round; LT-e-6 adds `COVERAGE_EVIDENCE.json`/`HAND_SURFACES.json`/`live-iam-census.json`
  to every walk), so every file present is hashed rather than a copied key list.
- **`FWD10.json`**: AWS plane before = the walk's own token-leg read embedded in `contract.json`
  (`coverage.token_floor` + `coverage.vintage`: 90/2595 at `2026-09-19 03:32:23 UTC`); after = a fresh
  `comp-find --corpus aws '\b(49f|49financial)\b' -i --all` read at `2026-09-19T03:56:43Z`. Both resolve to the
  SAME stitched snapshot (identical vintage line and manifest id `d6bf6e104ca5`, since `comp-find --corpus aws`
  reads a periodically-rebuilt stitch, not a fresh per-call AWS sweep) -- hits and scanned byte-identical, so
  `delta_outside_run: []`. `served` is marked not-applicable this round (no MARK, no live-serve read this walk's
  design takes).

**Driven mutant, proving the dependency rather than asserting it:** `HASHES.json` was removed from the run
directory; `x4-run` re-read `FAIL-X4-RUN ("no post-cut run with HASHES.json under the run home (0 found)")`;
`HASHES.json` was restored from a backup and diff-verified byte-identical; `x4-run` re-read `PASS-X4-RUN`.

## Coverage: 0 dropped vs round 3

| node_type | r3 | r4 | | node_type | r3 | r4 |
|---|---|---|---|---|---|---|
| EC2_INSTANCE | 19 | **20** | | S3Key | 154 | 154 |
| EVENT_RULE | 37 | **38** | | SECRET | 5 | 5 |
| IAM_POLICY | 22 | **23** | | S3_BUCKET_POLICY | 3 | 3 |
| IAM_ROLE | 46 | **56** | | S3_BUCKET, CW_ALARM, SNS_TOPIC, SQS_QUEUE, SSM_DOCUMENT | 2 | 2 |
| INSTANCE_PROFILE | 6 | **7** | | CLOUDFRONT_DISTRIBUTION, DYNAMODB_TABLE, SECURITY_GROUP | 1 | 1 |
| LAMBDA | 67 | **73** | | LOG_GROUP | 0 | 0 |
| SCHEDULE | 9 | **10** | | | | |

7 grew, 12 held, 0 dropped, matching LT-e-6's own e6-no-loss measurement exactly (this is the same repaired engine,
run for real instead of the `walk`-only sidecar).

## X5R4-AC3 FAIL: an unrelated project's commit, already in this worktree before spawn

`x4-no-registry-move` diffs `cut_pin` (`87607a2a30`) against `HEAD` over the two registry paths, actor-blind. It
names `infra/logic/registry/exemptions.json` and `infra/logic/registry/scopes.json`. `git merge-base --is-ancestor
845343f925 HEAD` (rc=0) confirms that commit -- `registry(IRPT_BCKEND steps 2-3, 4.0.0_SA_CRO): the
inflection/cottonwood provisioned flip ...` -- is already an ancestor of this worktree's own HEAD (`c28c728a30`),
landed before this worker was spawned. `git diff 87607a2a30 HEAD -- ` the two paths shows only that commit's
IRPT_BCKEND content (`bucket_provisioned`, `bucket_managed_by`, six operator exemption rows for
`opal-data-inflection`/`opal-data-cottonwood`) -- zero LGIC_LGCTFM content, and this worker's own commit
(`9160215d2b`) touches neither path. No act inside this order's grant can satisfy this arm: filed
`LGIC_LGCTFM-W1-S39`, BLOCKING, ARMED, `disarm_owner: 2.0.0_SA_COO~G`.

## Step 3 -- what the 49F pipeline is made of, from the contract alone

Read from `20260919T034609Z-c28c728/contract.json` and `flow.current.md`'s own COMPUTE column, nothing else,
except where named:

- **SCHEDULES (10):** `advi-49f-gold-floor`, `advi-49f-publisher`, `irpt-directory-refresh`, `irpt-intake-poll`,
  `mdpf-feeder-backstop-daily`, `opal-assets-bd49f-dim-convert-daily`, `smartx-jwt-refresher-daily`,
  `smartx-rest-pull-daily`, `wsb-49f-model-aua-pull-daily`, `wsd-49f-partner-held-etf-pull-daily`.
- **RULES (EVENT_RULE):** 38 rows.
- **LAMBDAS:** 73 rows.
- **EC2 RUNNER:** 20 rows -- `bd-49f-auto-login` plus 19 shared monolith runners (`bd-allocations`, `bd-assets`,
  `bd-fees`, `bd-gold-detail-generator`, `bd-gold-layer-runner`, `bd-gold-qa-runner`, `bd-transactions`,
  `consolidation-gold-runner`, `etfs-reports-reporter`, `historical-prices-fetcher` x8, `mdpf-daily-runner`,
  `opal-gateway`).
- **ROLES:** 56 real IAM_ROLE rows (57 counted rows include 1 fictional standing plant, excluded from "involved").
- **TABLE:** 1 DYNAMODB_TABLE, `opal-partner-49financial`.
- **BUCKETS:** 2 S3_BUCKET rows, `opal-data-49financial` and `opal-data-bd`.

**COMPUTE column as rendered** (`flow.current.md`): `coverage: 95 row(s) of 95 involved node(s)` /
`coverage by node_type (rows/involved): EC2_INSTANCE 20/20; LAMBDA 73/73; SSM_DOCUMENT 2/2`.

**What I still had to look up by hand, named rather than hidden:** (a) the invocation's own CLI flags -- the
contract does not say what flags produced it, so this came from `infra/logic/10_LEGACY_TRANSFORM.md` and
`lib/opal_lgctfm.py`'s argparse block, per the order's own instruction; (b) confirming LT-e-6 added no new flag
required reading `p_run.add_argument(...)` directly.

**The one relation that read zero, recorded UNVERIFIED per the pre-spawn amendment:**
`COVERAGE_EVIDENCE.json` `legs.token.live_pattern_triggers: 0` -- no live trigger's own EventPattern text literally
names a `49f`/`49financial` token; every subject-relevant trigger this run rowed was reached via `trigger_target`
(its target already involved through `iam_grant`/`source_text`), not by pattern-text match. No positive control was
run to distinguish a genuine absence from an instrument limit, so this is recorded UNVERIFIED, never as "the
subject has no pattern-named triggers." `trigger_denominator` discloses a partial census (38 of 144 EVENT_RULEs,
10 of 23 SCHEDULEs census'd), consistent with the method note's own disclosed blind spot.

## Controls

**Mutant:** (1) this worker's own artifact -- `HASHES.json` removed/restored around `x4-run`, FAIL then PASS,
restoration diff-verified byte-identical (above). (2) `selftest-arms` PASS-ARMS-DISCRIMINATE both before and after
this worker's commit, 34 arms.

**Determinism:** `x4-run`/`x4-floor` each run 2+ times against the unchanged committed run directory (pre-commit,
post-commit, and the restore-run) -- run id, node_type count, floor figures and the 7 named classes identical every
time. Not claimed stable across vintages: the live estate can move between separate invocations, as it did between
round 3's walk-time read (88/2590) and this run's (90/2595); within this session's repeated reads it did not.

## Proof

`LGIC_LGCTFM.TO-LT-x-5-r4.coverage-run-on-the-repaired-engine.proof_of_spec.json` --
`python .tools/proof-of-spec-check.py <instance> X5R4-AC1,X5R4-AC2,X5R4-AC3,X5R4-AC4 --governing-order <order>`.
**A FAIL row leaves the order open**, so `<status>` stays `pending`.
