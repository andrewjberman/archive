# AMGT_RESAPP round 95 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-11 ~18:3xZ. Five orders, all terminal: `aa-1`, `aa-2`, `aa-4` built and merged; `aa-3` a read-only reading (filed, proof VALID); `aa-5` (the ONE redeploy,
`opal-amgt-scoped-api` `VNcX9ntm..` -> `TmeKvn83..`) APPLIED and HELD.** Round 95 implements the CTO~DELL1 round-94 analysis `ledger/ROUND_ANALYSIS.round94.md` section 3 (items 1-5;
msg 3969, ADDENDUM 1 msg 3986); decomposition s.103; issuance @1e92ba6e74. Amendments (all the issuer's own check or face errors, each with its gate limb: none grades an
amendment to the issuer's own order): aa-2 AMENDMENTS 1, 2 (@db3d3a7787, @f4748adede). **`round-close-check.py --round 95`: orders 5, proof_ok 5 of 5, judgment 1, graded 0,
verdict REFUSED on exactly that one ungraded judgment (`aa-3` AC2, the CVO's). `dep_stage` is left at EXECUTING until the CVO grades it; every mechanical criterion is YES.**

## 1. Orders, cells and the issuer acts

| cell | item | state | evidence |
|---|---|---|---|
| `AMGT-aa-1` | 1: the verifier locates a stored point by its `stated_value` (D1-S24) | complete, merged @84c2876f3c; producer-side, no served write | worker ~390 @d53c2af66a, proof VALID; SAP's object may be re-verified again |
| `AMGT-aa-2` | 2: no field of a table row whose name disagrees with the registered name is served (D1-S26) | complete, merged @b12a5c865b and @fe7175efde (two amendments); SERVED by aa-5 | worker ~391 @5fd5f992f3, proof VALID, re-seated twice |
| `AMGT-aa-3` | 3: READ the two `/compare` 500s to their cause (C-S82) | complete (reading filed @dc5c1e60b2, proof @b2bc4ad98a VALID); **AC2 is the CVO's judgment** | RA1: CAUSE DEV-PROXY, by elimination; nothing written anywhere |
| `AMGT-aa-4` | 4: a short initialism keeps its capitals ('CSL Ltd') | complete, merged @ecb3e3689b; SERVED by aa-5 | worker ~391 @f2532b1f0e, proof VALID |
| `AMGT-aa-5` | 2, 4: the ONE redeploy carrying aa-2 and aa-4 | complete, SERVED: `VNcX9ntm83qe07/eOOD16AYsDmoEp20eCzj9ljfGvGE=` -> `TmeKvn83XnePF4RrJUQKIpbzYdH4VnCmvyXePbs3KB8=` (apply 18:03:15Z), built at the scratch pin `b3512d18fb` | RA1 ledger CLOSED @6af831a822, proof VALID; pair `ledger/NEVER_WIDEN_ROUND95_CLASSIFICATION_REDEPLOY_{COO,CTO}_HALF.md` (COO @b38de315e7, CTO msg 4042) |
| `AMGT-aa-6` (ss-7 / pp-4) | 5: the DEMQUE answer's reader | STAGED, no order | no quote, no answer; row `MDPF_DEMQUE-D1-S10` stands |

## 2. The issuer's ONE REAL RUN at close

- **aa-5 (SERVED, WORLD): re-run by the issuer on the live function, not RA1's report.** `r95_classification_census.py --where deployed`: 243 subjects, two disagreeing table rows listed whole
  (CSL 'Carlisle Cos Inc' / US Large Cap, scheduled; SAN 'Banco Santander S.A. ADR' / Health Care, legacy); K1 2 ranked rows, K2 2 rank series and K3 3 collected-chatter rows withheld
  with 'classification not available for this listing'; K4 no per-security route carries a classification; K5 186 ranked rows and 186 series equal their table row's own; K6 each
  disagreeing ticker asked for by ticker serves no table-row name or classification; **6 of 6, `R95 CLASSIFICATION CENSUS: YES`** (the base read K1, K2, K3, K6 FAIL).
  `r95_casing_deployed.py`: CSL_AU_Equity serves 'CSL Ltd' (the base 'Csl Ltd'), JD_US_Equity 'JD.com Inc', SAN_FP_Equity 'Sanofi', ASML 'ASML Holding NV'; `YES`.
  No-regression: `r94_name_census.py --where deployed` C1/C3/C4 0 different, `YES`; `r92_minor_unit_census.py` M1-M4 `YES`; `r89_peers_deployed.sh` and `r89_deployed_close.sh --want
  amgt-corpus-dossier/12` `YES`.
- **RA1's compare** (`AA5_POST_APPLY_COMPARE_20261011.json`, a 527-request baseline recorded 17:56-18:01Z against the live function after): **39 name and classification paths** (3 overlay/peers,
  6 ranked, 24 rank series asked for every measured ticker x 4 combinations, 6 collected chatter) on `SAN_FP_Equity` and `CSL_AU_Equity`, 28 generation clocks, **0 corpus, 0 outside the
  pair's table**; status moved 0; the other 186 ranked rows and 186 series and all 2,230 peer members unmoved. Admission at the pin: exactly two members at the half's blobs; the builder
  replay YES (88 calls, 18 distinct, 0 differ).
- **aa-1 (LOCAL):** `r95_reverify_idempotent.py` 6 of 6 (the base 2 of 6); `r94_rescale_table.py` over the 12 stored analysis objects SAP stored 3 | expected 3, changed 0 (the base 3 | 1);
  341 filings tests. **aa-2, aa-4 (LOCAL):** the census `--where local` 6 of 6 and `r95_casing.py` 5 of 5; `lib/research/api/tests` 956 passed.
- **aa-3:** the reading names its sources with denominators; its own limits are stated in it (the proxy's console line unreadable; no request id; Lambda@Edge regional logs not read).

## 3. What the issuer got wrong, and what it cost (the CVO's L9 read)

1. **My round-94 check D10 asserted the opposite of this round's rule.** `r94_display_name.py` D10 said a series whose name is replaced keeps its classification, and the test
   worker 387 wrote to mirror it said the same; aa-2 reverses exactly that. I reused the check without re-reading the arms a new rule reverses. Two worker rows (`D1-W391-S1`, `S2`, BLOCKING),
   one re-seat; ruled by AMENDMENT 1 (the check changed by me, one test assertion by the worker).
2. **aa-2's series lookup was the covered universe, and CSL_AU_Equity is not in it.** The three places I named each read the table by ticker; the rank series finds the security key through
   `_covered_bloomberg_index()` (95 names) and CSL is a measured subject outside it, so CSL AU asked for by ticker still served 'Carlisle Cos Inc' and 'US Large Cap'. **My census arm K2
   judged only tickers a ranked list holds, so it passed without seeing CSL AU: its denominator was narrower than the sentence beside it** (the round-94 packet had stated the same
   gap as a limit; it was the same lookup). I found it by my own post-merge read of the merged tree, not by the check; a second reopen, a second re-seat; K6 and
   `r95_series_by_ticker_table.py` (every measured ticker x four combinations) now read it. Cost: about 40 minutes and one worker re-seat.
3. **The orders for the three code cells carry no "when you are done" section in the committed file** (my generator template lacked it; I put the text in each worker's spawn prompt). The
   committed order files are therefore less self-contained than round 94's. The workers' instructions were complete; the files are not.
4. **What the measurement caught (not an error, recorded as cost avoided):** the admission table at `box/dell1` HEAD named AMGT_CORPUS's round-47 files (`dossier.py`, `team_sheet.py`,
   `template.py`, `factset_descriptions.json`), which no pair of this act admits and which move the served dossier pick; the build pin is therefore a scratch commit (the live package's tree
   plus the two api files, every hunk read as aa-2 or aa-4). `scratch/r95-aa5-pin` is kept until a merged-pin redeploy supersedes it (the CTO's condition 3).

## 4. JUDGMENT for L9

**One judgment criterion: `AMGT_RESAPP.TO-AMGT-aa-3` AC2 -- the reading's cause follows from its evidence and its denominators.** The reading is
`deliverables/0.7.0_AE_CloudOps~RA1/C-S82_COMPARE_500_READING_20261011.md`: CAUSE DEV-PROXY by elimination (CloudFront 5xxErrorRate 0 over 405 requests; HTTP API 5xx 0 over 266; function and
authorizer Errors and Throttles 0 over 291 and 218 invocations; reserved concurrency none against 978 unreserved, peak 10; the installed Vite answers a proxy error 500 with an empty body),
with what it does not prove stated. Offered for the CVO's own re-run: `r95_classification_census.py --where deployed`, `r95_casing_deployed.py`, `r94_name_census.py --where deployed`,
`r95_reverify_idempotent.py`, `r94_rescale_table.py`, `r92_minor_unit_census.py`, and the browser walk of the Security Analysis header and lists for SAN FP ('Sanofi', no classification) and CSL AU.

## 5. Rows filed this round

Workers: `D1-W391-S1`, `S2` (BLOCKING, ARMED: the two assertions of the round-94 reading) ruled by aa-2 AMENDMENT 1; `D1-W391-S3`, `S4` (INERT: a re-seated worktree's empty portal
submodule skips two tests; the order's literal worktree path). RA1: none. Issuer: **`D1-S25`** (the rank timeseries series name; closed by aa-5), **`D1-S26`** (CSL AU serves Carlisle's classification;
**closed by aa-5, K1-K6**), `D1-S24` (the verifier; **disarmed by aa-1**). **Disarmed by this round:** `D1-S24`, `D1-S25`, `D1-S26`. `C-S82` read to its cause (INERT, dev server only).

## 6. For the next round (the ENRICHMENT LIST's inputs)

1. **SAN FP's classification is withheld on the list routes** (the CTO's ruling, msg 3986): an exchange-qualified classification row (a key that is not the bare ticker) is the later cell
   that serves a true sector for SAN FP and CSL AU; until it exists both say why.
2. **AMGT_CORPUS's round-47 files (`CRPS-aw-1` and its /13 write) wait for their own pair and redeploy**, which re-measures at its GO against `TmeKvn83..`; `scratch/r95-aa5-pin` is
   superseded by that merged-pin redeploy.
3. **The function ran up to 28.5 s in the walk window** (timeout 29 s, 15:30Z to 15:41Z maxima 18-28 s) with no error: which route, and whether a long answer is the trigger of the dev
   proxy's socket-level 500, was not in the reading's remit; a read of the duration by route is the cell if the CTO wants it.
4. **C-S82 has no fix to cut:** the cause is the portal dev server's proxy (no timeout configured, no error handler); PROD users do not traverse it. Not served, not scheduled.
5. **Cosmetic:** `JD.COM INC-ADR` cleans to 'JD.Com Inc' where the table's own name is 'JD.com Inc' (only the registered-name path); the `.COM` word is not declared.
6. **ss-7 / pp-4** when the DEMQUE answer lands. `AMGT-nn-6`, the portal PROD promote (`dell1-20261011T033643Z-e7f2`: Andrew's word is NO for now, until he visually smokes DEV and has
   the DEV-not-on-PROD breakdown), FWD-16 and the model API key stay Andrew's.

checked 5 of 5 orders terminal, 5 of 5 proofs VALID, 1 judgment criterion ungraded (the CVO's)
