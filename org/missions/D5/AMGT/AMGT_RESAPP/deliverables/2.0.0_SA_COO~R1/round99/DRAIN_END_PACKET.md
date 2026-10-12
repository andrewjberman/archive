# AMGT_RESAPP round 99 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-12 ~00:5xZ. Three orders, all complete: `AMGT-bf-1` (the SECOND redeploy from a MERGED pin carrying AMGT_CORPUS's /14 files, bd-1's serve kept;
`opal-amgt-scoped-api` `mbGRmy1H..` -> `oEDHTRPqvrjYubJNqogLVKubI2UyQ8wZco0oa2Z6GVc=`, APPLIED and HELD), `AMGT-bf-2` (a read-only reading: the function's invocations over 20 s in the
last day) and `AMGT-bf-3` (the portal repoint of the top-level `fiscal_year_figures` readers: a DEV candidate, LANDED on portal DEV by the box manager); `bf-4` (pp-4) STAGED, no order.**
Round 99 implements the CTO~DELL1 round-98 analysis `ledger/ROUND_ANALYSIS.round98.md` (msg 4161); decomposition s.107; issuance @a5ca1e13ff. One amendment (the issuer's own order,
no gate limb graded it: it is a modification): `bf-3` AMENDMENT 1 @735f0e7b08. `round-close-check.py --round 99` is expected REFUSED until the CVO grades `bf-2` AC2 (one JUDGMENT criterion).

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-bf-1` | 1: the /14 redeploy from merged pin `b3d4856531`; bd-1's `scoped_amgt.py` `9b13bf0371d4` and `monthly_chatter.py` `38e9511ccc9c` unchanged; /15 not carried | complete, SERVED: applied 2026-10-12T00:23:02Z (LastModified 00:23:30Z) by `0.7.0_AE_CloudOps~RA1`, commit 311ebc45d1, ledger `amgt-resapp-r99-bf1-corpus14-redeploy-dell1` CLOSED, proof VALID | pair `ledger/NEVER_WIDEN_ROUND99_CORPUS14_REDEPLOY_{COO,CTO}_HALF.md` (COO @13e041156f, CTO msg 4184) |
| `AMGT-bf-2` | 2: the invocations over 20 s of the last day, per name and why | complete, merged @4040230b7f, proof VALID; AC2 UNGRADED (the CVO's) | worker ~395 @038df2c8d3; reading `deliverables/0.9.0_WK_AMGT_RESAPP~395/BF2_OVERLAY_TAIL_READING_20261011.md` |
| `AMGT-bf-3` | 3: every reader of the top-level `fiscal_year_figures` reads `model.fiscal_year_figures` (step 1 of the payload de-duplication) | complete, merged @f3d3a97852, proof VALID; CTO review APPROVED (`ledger/CTO_REVIEW_R99_BF_3_PORTAL_REPOINT.md`, msg 4179); LANDED on portal DEV `0a06280a40` by `0.0.0_AB_MSTR~DELL1` (msg 4182) | worker ~396 @de92a5cf7b, portal candidate `cd229995b3` (patch-id `3a8eefec6a32`, equal to the landed commit's) |
| `AMGT-bf-4` | 4: the DEMQUE answer's reader (pp-4) | STAGED, no order | no quote, no answer; row `MDPF_DEMQUE-D1-S10` stands |

## 2. The issuer's ONE REAL RUN at close

- **bf-1 (SERVED, WORLD): re-run by the issuer on the live function after the apply and after C1's read, one reader at a time.** `r98_thesis_fullbody_compare.py --after local` (the live /14
  function against the pin's own handler, 95 names, all 200): **0 paths under `model.team_sheet`**, 11 generation clocks, 18 `float_repr` (the measuring checkout's python 3.14 printing a request-time
  sum, the same 18 paths as in round 98 and in the pre-act measurement), 0 other: `R98 THESIS FULLBODY: YES`. Deployed censuses `r97_sector_serve_census.py`, `r95_classification_census.py`,
  `r94_name_census.py` all YES (bd-1's serve KEPT); `r89_peers_deployed.sh`, `r89_deployed_close.sh --want amgt-corpus-dossier/14`, `r92_minor_unit_census.py`, `r95_casing_deployed.py` all YES.
- **C1's post-act read (msg 4195, an independent seat, against RA1's immediate pre-act capture):** `ax7 names 95 team_sheet_equals_stored14 95/95 others_equal 95/95 max_response_bytes 1289958
  (AZN_LN_Equity) margin_to_6MB 5001498 over_6MB 0 growth_exceeds_delta 0`; `ax7 compare build 1/1`.
- **RA1's compare** (`BF1_POST_APPLY_COMPARE_20261012.json`): single reader, 528 requests, status moved 0, 88 `team_sheet` paths on 7 subjects, 37 clocks, 0 `float_repr`, 0 outside the table.
  **The slow-request clause fired once and passed:** `ASML_NA_Equity` overlay 24.87 s (200), three re-invokes 200 with identical bytes; the first request of its sequence (29.27 s before the apply),
  which RA1 reads as first-after-idle.
- **bf-2 (LOCAL): re-run by the issuer.** `r99_overlay_tail_reading_check.py` 9 of 9 YES on the merged file; the issuer's own Logs Insights queries over the same log group read the same counts
  (32,528 REPORT lines, 53 over 20 s, 12 cold, 49 with a pool-full warning, 0 naming a route or key).
- **bf-3 (LOCAL, then landed): re-run by the issuer.** `r99_repoint_readers.py` 5 of 5 on the candidate (0 top-level reads over 703 files); the nine stock harnesses and `join` green; typecheck rc 0;
  on portal DEV `0a06280a40` a `git grep` of `fiscal_year_figures` finds no top-level reader (`ModelTab.tsx:607,616`, `postureCites.ts:369`, `CardFooter.tsx:188,192` read the model copy; the only
  top-level mention left is the type declaration `types.ts:1299`), and `git patch-id` of the landed commit equals the candidate's.

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **`bf-3` AC2's invocation was never run as written.** The dry-run at the cut ran `grep -E "CHECKS-OK|FAIL|rror" | tail -1`; the order carried `tail -1` of each harness, and
   `modelPattern.harness.cjs` prints its `CHECKS-OK` line and then a fixture JSON line, so the worker's honest run read FAIL on a green candidate. **Cost: one re-seat (the worker re-ran AC2
   and updated its instance) and AMENDMENT 1.** The control I now keep: the invocation string a dry-run executes is copied FROM the order file, never retyped.
2. **My round-98 account of the overlay timeout was a candidate cause stated too firmly.** I wrote that my own 4-thread sweep overlapping RA1's first replay was a candidate cause, and the CTO
   named KEEP on that reading. The round-99 reading (`bf-2`) shows the tail pre-dates the apply (47 of the 53 slow invocations precede it), several slow runs sit in minutes with one to three
   invocations, and 49 of 53 carry a pool-full warning: **the slow tail is not load-induced by my sweep.** The KEEP stands on better evidence; the packet corrects the cause.
3. **A stale capture produced three false growth excesses (21, 21, 11 bytes).** `ax7_compare.py` against a live capture taken before the measurement read AZN and BATS 21 bytes over their
   delta; the live body of each had moved by 21 bytes with no code change (RA1's pre-act capture carried the same +21). Resolved by reading the live body again, then by RA1's capture
   immediately before the apply; named in the COO half. SNPS's 11 bytes were its `float_repr`.

## 4. JUDGMENT for L9

`bf-2` AC2 (the CVO's): the counts follow from the queries (the issuer's re-run reproduces them), the splits sum to OVER 20 s, **no route or name is inferred** (the function logs no request path; the
reading says `ROUTE none attributable` with the reason), and the not-read surfaces are named (the gateway's or function URL's own log, the S3 request log, the client side). Offered for your own re-run:
`r99_logq.py` queries over `/aws/lambda/opal-amgt-scoped-api` (24 h), and `r98_thesis_fullbody_compare.py --after local` against the pin (announce it to the applier first: it is a live reader).

## 5. Rows filed this round

Worker: `AMGT_RESAPP-D1-W396-S1` (OBSERVATION, INERT: the AC2 `tail -1` defect, resolved by AMENDMENT 1), `S2` (OBSERVATION, INERT: no committer identity in the portal worktree; the retry set
`GIT_COMMITTER_*` per call, nothing written to git config). `~395`: none. RA1: none. Issuer: none. **Disarmed by this round:** none open.

## 6. For the next round (the ENRICHMENT LIST's inputs; the CTO's rulings at msgs 4177, 4184, 4191)

1. **The /15 third redeploy (AMGT_CORPUS ay-4, CTO half signed msg 4191):** a merged pin with `dossier.py` `7b67bf62afdd` (METHOD /15), bd-1's two blobs unchanged; baseline the function
   `oEDHTRPq..`; effect block rows only; post-act read live vs live within the /15 delta; it never folds /14 with /15; then FWD-20's DEV census (0 values under a foreign header).
2. **The connection-pool cell (CTO msg 4184):** 49 of 53 slow invocations log "Connection pool is full". Read at HEAD: the harvest store builds `boto3.client("s3", region_name="us-east-1")`
   with no `Config` (the library default pool is 10), while request-path thread pools run 8 wide (`CLASSIFICATION_JOIN_WORKERS`, `MODEL_BLOCK_NAME_WORKERS`, `CLASSIFICATION_WORKERS`), 16 wide
   (`LEDGER_READ_WIDTH`, `collector_read.READ_WIDTH`) and `names_read` sizes its pool by chunk count; `publication_gold._TIMELINE_READ_WORKERS` carries the comment "boto3's default
   connection pool is 10". This is the cell's READ, not a proof of cause; the cell sets the pool and the widths consistent under its own pair and closes on the next day's counts against 53 and 49.
3. **The payload de-duplication, steps 2 and 3:** step 1 is on DEV. Step 2 is Andrew's portal PROD promote (`e7f2`); step 3 (the API drops the top-level key) is a later redeploy pair, after
   step 2, closing on the response bytes falling by about the measured share per name with both builds rendering unchanged.
4. **CSL AU's sector reads as of 2026-09-30** (served with its date; withholding by age is the CTO's call). **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6`, the portal PROD promote
   (`dell1-20261011T033643Z-e7f2`), FWD-16 and the model API key stay Andrew's.

checked 3 of 3 orders terminal, 3 of 3 proofs VALID, 1 judgment criterion ungraded (bf-2 AC2)
