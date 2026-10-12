# AMGT_RESAPP round 100 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-12 ~05:1xZ. Three orders, all complete: `AMGT-bg-1` (the THIRD redeploy from a MERGED pin carrying AMGT_CORPUS's /15 files, bd-1's serve kept; `opal-amgt-scoped-api`
`oEDHTRPq..` -> `7DUlZxhl8C19Avw3LslWy4lF5psB7a0iU/ERSGqOKCs=`, APPLIED and HELD under the CTO's KEEP), `AMGT-bg-2` (a build: `_s3_client()` is ONE client per container with a pool of 32; merged,
not served by itself) and `AMGT-bg-3` (its apply: `7DUlZxhl..` -> `42z0tn68TZjuk8awBclnMii0k+FX2Pw2bw7iN9Xitz0=`, no served byte moved); `bg-4` (pp-4) STAGED, no order.** Round 100 implements the
CTO~DELL1 round-99 analysis `ledger/ROUND_ANALYSIS.round99.md` (msg 4198); decomposition s.108; issuance @aa58e5e113. One amendment (the issuer's own order, no gate limb graded it: it is a
modification): `bg-2` AMENDMENT 1 @e2693c1630. `round-close-check.py --round 100`: orders 3, proof_ok 3 of 3, judgment 0, **verdict MAY-CLOSE** (no JUDGMENT criterion in any order).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-bg-1` | 1: the /15 redeploy from merged pin `6e8dcaf414`; bd-1's `scoped_amgt.py` `9b13bf0371d4` and `monthly_chatter.py` `38e9511ccc9c` unchanged; bg-2's blob NOT in it | complete, SERVED: applied 2026-10-12T02:54:49Z (LastModified 02:55:18Z) by `0.7.0_AE_CloudOps~RA1`, commit ba22af15f5, ledger CLOSED, proof VALID; CTO KEEP (msg 4244, ADDENDUM 1) for the first-after-idle overlay timeout | pair `ledger/NEVER_WIDEN_ROUND100_CORPUS15_REDEPLOY_{COO,CTO}_HALF.md` (COO @c9fe8212d6, CTO msg 4225) |
| `AMGT-bg-2` | 2: `_s3_client()` builds ONE client per container, pool 32 (mirrors `_dynamodb()`) | complete, merged @703845dc6e, proof VALID; a candidate, served only by bg-3 | worker ~397 @302b0d397f; CTO confirmed the design (msg 4200, ADDENDUM 1 of the round-99 analysis) |
| `AMGT-bg-3` | 2: the SECOND apply carrying bg-2's build from merged pin `ba22af15f5`; no served byte moves | complete, SERVED: applied 2026-10-12T04:17:52Z (LastModified 04:18:21Z) by RA1, commit 15b3cba618, ledger CLOSED, proof VALID | pair `ledger/NEVER_WIDEN_ROUND100_S3CLIENT_REDEPLOY_{COO,CTO}_HALF.md` (COO @7d8d398673, CTO msg 4262, ADDENDUM 1 msg 4271) |
| `AMGT-bg-4` | 3: the DEMQUE answer's reader (pp-4) | STAGED, no order | no quote, no answer; row `MDPF_DEMQUE-D1-S10` stands |

## 2. The issuer's ONE REAL RUN at close

- **bg-1 (SERVED, WORLD): re-run by the issuer on the live function, after RA1's apply and C1's read, alone.** `r98_thesis_fullbody_compare.py --after local` (the live /15 function against the pin's
  own handler, 95 names, all 200): **0 paths under `model.team_sheet`**, 4 generation clocks, 18 `float_repr` (the measuring checkout's python 3.14; the same 18 as rounds 98 to 100), 0 other:
  `R98 THESIS FULLBODY: YES`. Deployed censuses `r97_sector_serve_census.py`, `r95_classification_census.py`, `r94_name_census.py` and `r89_peers_deployed.sh`, `r89_deployed_close.sh --want
  amgt-corpus-dossier/15`, `r92_minor_unit_census.py`, `r95_casing_deployed.py` all YES. C1's independent read (msg 4250): `ay4 names 95 team_sheet_equals_stored15 95/95 others_equal 95/95 max
  1303205 growth_exceeds_delta 0`, build 1/1; its DEV census 0 values under a foreign header, unmapped 0, unclassed 0.
- **bg-3 (SERVED, WORLD): the same run after its apply** (my run at ~05:0xZ): 0 paths under `team_sheet`, 18 `float_repr`, 4 clocks, 0 other; every census YES. RA1's compare: replay 528 requests,
  status moved 0, 37 clock paths, 0 over 20 s (median 0.39 against 0.55 s), `ay4_compare` growth 0 for all 95 names, build 1/1. C1's control (msg 4273): the served field did not move.
- **bg-2 (LOCAL): re-run by the issuer on the merged tree.** `r100_pool_peak.py`: overall per-client maximum 20 over 35 reads, **0 reads with a client above its own pool** (the base reads 1);
  `r100_cold_check.py` YES 4 of 4 (7 clients against 146); the route table `thesis corpus 663 path(s)` only; pytest 39 passed.

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **`bg-2` AC3's expectation named a fixed count of a clock-dependent class.** I wrote `thesis noise 2 path(s)` from ONE dry-run; the class is the generation clocks (2 at the cut, 0 in the worker's
   run, 3 in my re-run). The worker's honest run read FAIL on a candidate whose routes did not move. **Cost: one re-seat and AMENDMENT 1.** The control I now keep: a count that depends on a clock
   is written as "absent or any count", and the dry-run is repeated before a number is fixed. (Round 99's `bf-3` AC2 was the same class of defect: an invocation never run as written.)
2. **A local timing did not transfer to Lambda, and I stated it as a measured effect before the act.** Locally one S3 client per container cut the cold first overlay from 11.1 s to 7.8 s; on
   Lambda the cold handler time is still 22-26 s (24.02 and 23.77 s after the apply, 27.81 s for `ASML_NA` after a 17-minute quiet, against 28.04 s before). The orders said "the Lambda network is
   not the box's" and gated the effect on the day-after logs, so nothing was claimed served; **the cost is an apply (a WORLD act and about 40 minutes of RA1's window) whose main effect is the pool-full
   warnings 78 -> 0 and the warm median 0.55 -> 0.39 s, not the cold tail.** The attribution I ran after the apply (`r100_cold_requests_by_key.py`: 253 S3 requests, 97 `input_ledger.json` GETs and
   ~45 per-peer refdata LISTs) is what I should have run BEFORE choosing the cell: the CTO's own wording, and my first reading, treated client construction as the cost. It was one of three costs.
3. **The slow-request clause did not cover a TIMEOUT of the first request.** `bg-1`'s first replay met an `ASML_NA` overlay at 29 s (a timeout, 1 function error): the clause I carried said a request
   over 20 s with three identical re-invokes is recorded, which a timeout is not, so RA1 stopped and the CTO named KEEP (msg 4244). **Cost: a STOP-class round-trip and about 15 minutes of RA1's
   window** (the same signature as round 98). The clause now reads against the pre-apply baseline of the first request of each sequence (25.95 to 29.3 s on three packages).

## 4. JUDGMENT for L9

No JUDGMENT criterion in any order. Offered for your own re-run: `r100_pool_peak.py` and `r100_cold_check.py` (read-only, the checkout's own handler on the live pool),
`r98_thesis_fullbody_compare.py --after local` against the pin (a live reader: announce it to the applier first), and the log-group queries of round 99 for the day-after count.

## 5. Rows filed this round

Worker ~397: `AMGT_RESAPP-D1-W397-S1` (OBSERVATION, INERT: the AC3 noise line, resolved by AMENDMENT 1). RA1: none. Issuer: none. **Disarmed by this round:** none open. The AMGT_CORPUS C-S64 row
(`'660.45'` in ROG's period grid) is carried on its own carrier; its served close is `bg-1` and C1's DEV census.

## 6. For the next round (the ENRICHMENT LIST's inputs; the CTO's rulings at msgs 4244, 4262, 4271)

1. **Round 101's first cell (CTO msg 4271): read-then-fix of the cold first overlay.** One refdata read per container instead of ~45 per-peer `ListObjectsV2` of
   `bloomberg/harvest/bronze/refdata/security_key=*` (~330 ms each locally), and the 97 `packs/*/input_ledger.json` GETs read once per container with a STATED freshness rule, under its own
   pair, served bytes byte-equal. Close: the cold first overlay for `ASML_NA_Equity` and `ADBE_US_Equity` after 15 quiet minutes **under 20 s**, request counts printed before and after.
2. **`bg-3`'s close, a read the day after the apply** (the 24-hour window starting after 2026-10-12T04:18Z, the round-99 method): invocations over 20 s and "Connection pool is full" warnings
   against 53 and 49 and the 0.16 percent rate. The CTO: pool warnings that persist come back to him.
3. **Payload de-duplication steps 2 and 3:** step 1 is on DEV; step 2 is Andrew's portal PROD promote (`e7f2`); step 3 (the API drops the top-level key) a later pair, after step 2.
4. **CSL AU's sector reads as of 2026-09-30** (served with its date; withholding by age is the CTO's call). **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6`, the portal PROD promote
   (`dell1-20261011T033643Z-e7f2`), FWD-16 and the model API key stay Andrew's.

checked 3 of 3 orders terminal, 3 of 3 proofs VALID, 0 judgment criteria
