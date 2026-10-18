# L10 SLUG -- NFRA_OPLGTW round 43 -- DRAFT (2.0.0_SA_COO~O, 2026-10-18 ~15:0xZ), NOT SENT

Status (2026-10-18 ~23:2xZ): all 12 round-43 orders are complete with proofs VALID. The round-close check reads REFUSED on ONE limb only: REVIEWER-ON-BOX ABSENT (the CVO~Z session died in the 20:48Z crash; 0 judgment criteria, so nothing else is owed). Nothing is sent until a CVO-kind seat is live and the check reads MAY-CLOSE (`python .tools/round-close-check.py --project NFRA_OPLGTW --round 43`). This file is the skeleton the slug is finished from.

## 1. The round, by order (state at the writing)

| order | what | state |
|---|---|---|
| `OG-pr-4` | the probe lease pins the firm; the listener refuses a mismatched firm (403 `probe_firm_refused`) before the tool runs, and a lease without a valid firm as malformed; drained `01c182170a`; my runs AC1 12 of 12, AC3 30 both orders, proof VALID | complete |
| `OG-en-31` | `test_ogpr1_ac13`: every refusal pulls the whole body before `http.response.start`; the mutant check FAILED/PASSED/restored byte-equal; drained `30e0cfc889` | complete |
| `OG-sec-2` | `graph.call` refuses a non-https, non-`graph.microsoft.com`, user-info or odd-port absolute URL before any client; my AC3 file set was the issuer's error (row `Z-W152-S1`, ruled `Z-S390`), amended; drained `ff2c1969f8` | complete |
| `OG-sec-3` | SSRF audit over six modules, 21 sites, 0 controllable, CLEAN; drained `c26cd96d5f` | complete |
| `OG-ev-8` | inline audit-write table: 81 sites, 68 on the loop, 1 off, 12 unknown; every timeout botocore's default; frequency ABSENT (the lake key names no tool); drained `273fd63f3d` | complete |
| `OG-ev-9` | limiter trace: 120 per 60 s, keyed on the validated principal key, Retry-After set, fail-open; 1 refusal row in 24 hours; recommendation no change; drained `fb6d78084b` | complete |
| `OG-ap-42` | ninth release (the four take-list files) on dell1's `ck-3` base `922ee425fe`: LIVE `a0c83303ee`, ledger `batch10` CLOSED 2026-10-18T16:32:05Z, UNARMED only (lease absent before, after and at the close, no SSM write); `ap42.AC1` and `AC2` PASS on my runs, `CODE10_SERVED.json` read by me, proof VALID (`3aff518318`); the firm pin is first exercised in the service by `OG-ev-7` | complete |
| `OG-ev-7` | the peers call measured in the service under one firm-pinned lease (15 minutes, placeholder account, one arming, deleted 21:08:37Z): walls 3.59 / 1.07 / 1.09 s against 4.2 s in a fresh process, VmRSS 248 MB, one PID, NRestarts 0; verdict COLD (the first call is 3.4x the second; the 17.9 s of `Z-S389` did not recur); journal `POST /probe/` 5, lake `probe:OG-ev-7` 3, `probe:unarmed` 2; three halves signed; `ev7.AC1` PASS on my run, proof VALID; flipped `96115e3368` | complete |
| `OG-pr-5` | the repair of the access-log regression `Z-S395`: `make_server` snapshots and restores the four process-wide `uvicorn` loggers around the listener's `Config` (worker `~156`; AC1 3/3, AC3 31 both orders; drained `b527ac88db`) | complete |
| `OG-ap-44` | the tenth release `eff517546e` on `a0c83303ee`, UNARMED: the service's access log is BACK, 164 `POST /mcp` journal lines against 286 audit-lake records in the same 30-minute window (baseline 168); listener `/probe/` lines 3 of 3 requests made (AC2 amended, `Z-S398`); ledger `batch11` CLOSED 20:01:40Z; three halves signed; `ap44.AC1` and `AC2` PASS on my runs; flipped `4abc086d96` | complete |
| `OG-ap-45` | the landing of `eff517546e` (carrying `a0c83303ee`) on `box/sitez` (the CTO's ask, msg 35792): merge `a9f066d680` on the applier's branch, drained `4ae39a3ab1`; 0 conflicted paths; `ap45.AC1` to `AC3` PASS on my runs (AC3: 125 files, 122 equal, 3 listed SITE-Z-OWN: `admin_people_access.py`, `destructive_ops.py`, `family_depth.py`); `AC4` 71 of 71 in both orders on 6 of 6 later runs, but my first run after the drain read forward 0 (`Z-S399`); proof VALID; flipped `ba9f196b64` | complete |
| `OG-ap-43` | the landing of `922ee425fe` (carrying `6575999df5` and `3b94a83e05`) on `box/sitez`: merge `eb9a60c0ac`, drained `b1e92a9635`; `ap43.AC1` to `AC3` PASS on my runs with the repaired check (the applier's first AC1 'no' was my check's defect, `Z-S393`, ruled `Z-S394`); proof VALID (`b5b84eeb9d`) | complete |

## 2. What the round delivered against the endpoint

(To write at the close from the CLOSED ledger and the served record.)

## 3. Rows

Rulings: `Z-S388` (earlier), `Z-S390`, `Z-S392`, `Z-S394`, `Z-S396`, `Z-S398`. CVO: `Z-S375` and `Z-S338` DISARMED. Carried ARMED: `Z-W94-S2`, `Z-S177` (traced), `Z-W155-S1`. Observations carried to round 44: `Z-S391`, `Z-W153-S2`, `Z-S399` (the both-orders check reads forward 0 on the first run after a change to the tree); items for the CTO and MSTR: the audit-lake registry row, the device's missing hashed account-id list.

## 4. The enrichment list this seat proposes for round 44

Full text and source rows: `deliverables/2.0.0_SA_COO~O/ROUND44_CANDIDATES_DRAFT_20261018.md`.
