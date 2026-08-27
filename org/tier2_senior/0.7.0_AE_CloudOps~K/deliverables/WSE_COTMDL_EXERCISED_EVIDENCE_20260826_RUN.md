# WSE_COTMDL TO-R1-AE / TO-R2-AE -- EXERCISED EVIDENCE, 2026-08-26 06:00Z SCHEDULED RUN

**author:** `0.7.0_AE_CloudOps~K` -- scored 2026-08-26 ~13:5xZ
**scores:** `0.7.0_AE_CloudOps~H`'s pre-registered predictions, written 2026-08-25 BEFORE the run
(`org/tier2_senior/0.7.0_AE_CloudOps~H/deliverables/WSE_COTMDL_PREREGISTERED_EXPECTATIONS_20260826_RUN.md`).
**VERDICT: P0 grounded; P1-P6 ALL PASS. Nothing falsified.**

⛔ **THIS SEAT DID NOT BUILD WHAT IT SCORED.** `~H` authored the predictions and landed both deploys;
`~K` scored them against the run. **That separation is the point** -- a prediction registered before the
exercise, scored by a seat that could not rationalise it after, is the strongest form this evidence takes.

---

## 1. STATE AXIS -- WHAT WAS ALREADY TRUE WHEN THIS SEAT WAS SEATED

⛔ **BOTH TOs WERE ALREADY LANDED AND APPLIED BEFORE THIS SEAT EXISTED.** The dispatch that seated me
(`2.0.0_SA_COO` 72169, 2026-08-26T13:46:26Z) reads *"R1 AND R2 ARE COUPLED AND ORDERED. R1 landed ALONE
ships the WRONG SEMANTICS into production... Land them together."* **That premise was already discharged
2026-08-25.** Measured, not recalled:

| layer | claim | evidence | STATE |
|---|---|---|---|
| DESIRED | `cot_rebalancer_runner.tf:154 = "all"` | @`27a3a98cdc` 2026-08-25T05:36:58-04:00, `0.7.0_AE_CloudOps~H` | committed |
| DESIRED | `:316` guard removed -- `all` UNIONs roster with descent | @`b56ec0e8ce` 2026-08-25T06:30:50-04:00, `0.7.0_AE_CloudOps~H` | committed |
| **APPLIED** | live `MODEL_DETAIL_SCOPE` | `aws lambda get-function-configuration cot-rebalancer-runner` -> `"all"` | **APPLIED** |
| **APPLIED** | live `CodeSha256` | `gdW/oQJlKLIaREk8DhEBOv7/kPxIcHuguJhk4KmGE8Y=`, LastModified `2026-08-25T10:38:32.000+0000` | **APPLIED** |

The live `CodeSha256` is **byte-identical to the value `~H` recorded in the pre-registered doc before the
run**, so the artifact scored here is the artifact whose behaviour was predicted -- not a later one.

**NEVER#6 -- both deploy-completion ledgers verified CLOSED, per-leg, by reading them (not by trusting the
claim that they were closed):**
- `org/critical_paths/change_management/20260825T0939Z_cotmdl-model-detail-scope-all_deploy_completion.md`
  -- 3 legs, `CLOSED 20260825T095533Z`.
- `org/critical_paths/change_management/20260825T1032Z_cotmdl-scope-all-union-descent_deploy_completion.md`
  -- 4 legs, `CLOSED 20260825T104029Z`, incl. the Rule-22a read on **deployed package bytes** resolved
  through the source map's `source_dir` (BUILD INPUT), never by filename.

**Therefore `~K` opened NO new deploy ledger: this seat deployed nothing.** Scoring a past run is a READ.
An entry opened for a read would be an entry that never closes.

---

## 2. P0 -- RETRIEVAL GROUNDING (run FIRST; P1-P6 not scored without it)

`~H` added P0 because `0.4.0_DS_ClientPlatform~F` produced a **clean, internally consistent, completely
false** table from a broken parse (`roster 0 | landed 30 | gap 0`, both reconciliations `True`). The
reconciliations in P5 are **not** evidence the retrieval worked -- they reconcile in the broken shape too.

| # | assertion | result |
|---|---|---|
| P0a | roster parsed from the **literal** key `pagedResults`, never guessed | **PASS** n=64 |
| P0b | `len(parsed_roster) == payload["totalResultCount"]` | **PASS** 64 == 64 |
| P0b+ | manifest `types.rebalancer_models.total_result_count` agrees | **PASS** 64 |
| P0c | detail ids = **full filename stem** (UUID), never a digit-run regex | **PASS** 81 ids from 81 keys |
| P0d | positive control (`01c4c8f2...`) resolves; negative control (bogus UUID) does not | **PASS** `True` / `False` |
| P0e | every count printed with the denominator it came from | **PASS** -- below |

**Sources, all `s3api`/UTC:** manifest `blackdiamond/cottonwood/meta/2026-08-26-complete.json`
(LastModified `Wed, 26 Aug 2026 06:00:56 GMT`, ContentLength 10378 -- matched on fetch); roster
`.../bronze/rebalancer_models/2026-08-26/page_000.json` (named by the manifest's own `bronze_keys`, not
guessed); detail keys enumerated by `list-objects-v2` with the CLI **paginating** and the set counted
client-side.

⚠ **ONE READING NOTE THAT COST A CYCLE, RECORDED SO THE NEXT SEAT DOES NOT REPEAT IT.** The pre-registered
doc writes the field as `manifest rebalancer_model_detail`. It is **not** a top-level key -- it lives at
`types.rebalancer_model_detail`. A top-level read returns `None`, which is a clean, well-formed **absence**
that reads as "the producer stopped emitting it." Both days carry the identical shape; only the notation
was shorthand.

---

## 3. P1-P6 -- SCORED

Run: `completed_at 2026-08-26T06:00:41Z`, manifest stamped `06:00:56 GMT`.

| # | prediction | observed | verdict |
|---|---|---|---|
| **P1** | `scope == "all"` | `"all"` | **PASS** |
| **P2** | every roster id present, denominator **re-read** from today's own file | **64 of 64**, 0 missed | **PASS** |
| **P3** | `>= 8` non-roster children, and the 8 known by id | **17 children**, 8 of 8 known present | **PASS** |
| **P4** | both Anna models present (matched on **id**) | both PRESENT | **PASS** |
| **P5** | `count == P2 + P3` and `count > 30` | `64 + 17 = 81` == manifest `81` == S3 `81` | **PASS** |
| **P6** | runtime well inside a 300000 ms timeout | **13362.81 ms** = 4.45% of budget, 22x headroom; 107 MB of 512 MB | **PASS** |

### THE RESULT, AS TWO POPULATIONS -- NEVER A FUSED DELTA

```
roster coverage ........  22 of 64   ->   64 of 64      (+42 roster models recovered)
non-roster children ....         8   ->         17      (+9 never previously landed)
detail files (fused) ...        30   ->         81
```

⛔ **THE FUSED NUMBER IS REPORTED LAST AND ONLY FOR RECONCILIATION.** *"30 -> 81"* is arithmetically true
and describes something that did not happen: 30 was 22 roster + 8 children, and the two populations moved
for different reasons. Reporting the fused delta is exactly what hid the original defect.

### P2 -- the roster gap is CLOSED

42 roster models that had never been landed under `opal_closure` are present. **Denominator re-read from
today's own file (64), not carried forward from yesterday** -- the roster is vendor-side and can change
overnight; a stale denominator is the defect this TO chain exists to correct. It did not change today.

### P3 -- 9 children nobody had ever seen, and this is the PREDICTED case

`~H` wrote: *"P3 IS A LOWER BOUND, NOT AN EQUALITY... A count above 8 is the expected case, not an
anomaly."* Today descended from all 64 seeds instead of 22, so the 42 newly-pulled roster models exposed
children that were undiscoverable by construction. **All 17 itemised by id (never "the rest"); the 9 new
ones are the ones absent from `~H`'s known-8 list:**

```
02572bfc-660f-45a5-b753-5385772d00a9    41a70e42-0a05-45e7-b8cd-d2e13605714e
09bfd1d1-ff67-45f8-9f4c-8b2ccb6e1f25    5fc639ab-4dda-4708-90dd-ec29ad613068
13dfa1c3-2259-4440-a272-eb237c592405    a40cf6b6-9077-48f4-bc49-6d39f03b945d
31f17857-3456-4f9b-8a47-a4a8e383d56c    c2496734-f490-405e-9f08-7e9d7b60d4e4
                                        fe580676-53ae-42fa-9825-87b8bbe89cfb
```

**The known 8, all present:** `0e632e04`, `267376fd`, `58ea3200`, `623b1942`, `67010675`, `ac3b8211`,
`ae9ef8d2`, `b25ed964` (full UUIDs in the scorer output).

**This is the union working.** Under the old `all` these 17 would be 0; under `opal_closure` the roster
would be 22. Only the union produces 64 **and** 17.

### P4 -- the falsifying case holds

`1ae61190-70fb-4d6c-a259-cee9019ed125` (`'Anna *9237'`) and `6ae9e540-9b27-474c-8ad9-3dfc5131c530`
(`' Anna *9238'`, **leading space preserved, matched on id, never normalised**) are both present. These
two accounts ($46,436,739.80) are why the defect was found; their absence would have falsified the fix
whatever the count said.

### P6 -- runtime

Prior 5 scheduled runs 6751-7322 ms; today **13362.81 ms** (RequestId `62303f80-a76b-4c50-87f9-b63a92d65a6c`),
~1.9x for 2.7x the detail GETs. Init 488.38 ms. **Exactly one REPORT line in the window -- one invocation,
no ad-hoc contamination of the production evidence.**

---

## 4. WHAT WOULD HAVE FALSIFIED THIS, AND DID NOT

All three of `~H`'s named falsifiers were live and none fired:
- **P4 fails** -> the fix did not fix what it was authorized for. *Both Anna models present.*
- **P3 returns 0 children** -> the `:316` union is not operative in the deployed path. *17 children.*
- **count unchanged at 30** -> `MODEL_DETAIL_SCOPE` is not the operative control. *81.*

**The build-level mutants were fired by `~H` at deploy time and are recorded in the ledgers** (R2 L1: guard
restored on an isolated scratch copy -> union test failed precisely on the children, `opal_closure` test
still passed, proving the mutation surgical). **This seat did not re-run them: a scheduled production run
cannot be mutated, and forcing an ad-hoc mutant run would be a QA instrument masquerading as production
evidence.** The mutant evidence is cited at its ledger, not re-derived.

---

## 5. RESIDUALS -- NAMED, NOT MINE, NOT ACTED ON

1. **The 08-21 backfill (`COT-e-1`)** -- excluded by determination, **an open call at Andrew.** Forward-only
   means **every partition through 2026-08-25 inclusive permanently carries 22-of-64 roster coverage.**
   2026-08-26 is the first correct partition. Not remediated by anything here.
2. **3 foreign committed-but-unapplied changes in the `opal-assets` workspace** -- `aws_iam_role_policy.bd49f_reporting_io`,
   `aws_iam_role_policy.emitter`, `module.emitter.aws_lambda_function.this`. **STILL ARMED.** Both `~H`
   applies were `-target`ed, which disarmed *those two acts only, not the workspace*. **CTO owns naming
   disarm owners.** A blanket 0-diff remains UNAVAILABLE in this workspace and is not the passing form.
3. **TO `<status>` fields read `pending` on both R1 and R2** while the work is landed, applied and now
   exercised -- declarative drift, corrected by this delivery.

## 6. INVARIANTS HELD

No alert / alarm / SNS / SES / notification / freshness-checker / monitor created (standing moratorium).
No shadow path, parallel emitter, or standing comparator. No served output moved -- this is a producer,
NEVER#3 does not attach. No ad-hoc invoke of the runner. **MDPF path untouched** -- COO's 72169 freeze on
`mdpf-gold-lambda` and the portal publisher was live at seating; nothing here invokes, dry-runs or nudges
either, and `cot-rebalancer-runner` is a different producer in a different firm tree.
