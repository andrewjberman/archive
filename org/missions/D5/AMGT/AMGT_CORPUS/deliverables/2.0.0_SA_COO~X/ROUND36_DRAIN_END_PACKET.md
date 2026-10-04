# AMGT_CORPUS round 36 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`, 2026-10-04 ~23:5xZ. **Decomposition:** v36.0 @`80717c897c`.

**Source:** `1.0.0_SA_CTO~Z` round-35 analysis @`02bbbc0208` s.4 (msg 29236). Closed tonight with al-4 CARRIED, per the CTO's ruling
(msg 29322): "close round 36 tonight with al-1/2/3/5 terminal and al-4 CARRIED as a named read on that fire". An ad-hoc fire is not
covered: it would be a second Bloomberg pull beyond Andrew's one-daily word.

Serves FWD-20 (the V3 lines on the Model tab).

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-al-1` the Model slice serves fiscal reasons | LOCAL | DONE, worker `~1`, drained @`98a93db70b` | AC1 `al1 build 1/1 control 1/1` (1299 HK 97/97, BA 0/0), re-run by the issuer at HEAD; AC2 3 passed; plus 22 tests, py_compile and ruff clean; proof VALID |
| `CRPS-al-2` the Model sheet renders the 49 V3 lines | LOCAL (portal) | DONE, worker `~1` (re-seated), outer drain @`66edd940a7`. Portal `fb1f3cbb` was reworked by the issuer to `75efe9d6` (merge of DEV `1b9f553d`, CTO review REWORK @`934205909b` then APPROVED @`60d69ec86e`). Now ON portal DEV: Andrew "rec approved" @`40cd6d2680`, pushed by MSTR~Z, CI run 37241631766 success | AC1 `al2 build 3/3 control 1/1`; AC2 `CHECKS-OK 12 of 12`; typecheck clean; DSGN battery29 ALL PASS; DSGN r34 x3 and r35 changed/cloud/payload PASS; instrument35 0/4 = DSGN's recorded base (ROUND35_CLOSE.md:51). **AC3 JUDGMENT is yours** (section 3) |
| `CRPS-al-3` the units judgment read | LOCAL (read) | DONE, worker `~2`, drained @`288de3d95d` | AC1 `al3 build 2/2`; **AC2 JUDGMENT is yours**: `deliverables/0.9.0_WK_AMGT_CORPUS~2/R36_UNITS_JUDGMENT_READ.md` |
| `CRPS-al-4` the 2026-10-05 13:00Z fire on pin `74e00624b0` | LOCAL (read) | **CARRIED** (CTO msg 29322): a named read on that fire, owed by the issuer after it runs | expect 96 pulled, rc 0, 0 pointer-unit figures (`checks/round35/v35.py`); and `al5_served.py --where deployed` still 1/1 + 1/1 |
| `CRPS-al-5` code redeploy of `opal-amgt-scoped-api` | WORLD | DONE, ledger `amgt-corpus-r36-al5` CLOSED @`e2790c8b2b` (Branch A); pair COO @`cbf0800776` / CTO @`95d297d418` | section 2 |

`fanout: 2 of 2 worker chains, cap 8`. All build checks FAILed at the base, as expected.

**Issuer acts and rulings inside the decomposition:**
- The worker on al-1 could not be resumed, so slot ~1 was re-seated for al-2, naming al-1's commits as inherited state.
- An order for al-5 to `0.7.0_AE_CloudOps~A` was REFUSED by `to-pipeline-gate` as a second issuance in round 36. It was not
  committed. al-5 stayed the issuer's act, as v36.0 s.1 allows.
- The al-2 rework merge (`75efe9d6`) was the issuer's drain act. The only conflict was the import lines of `ModelTab.tsx`. DSGN's
  AV-zg-5/AV-zi-1 body is unchanged. COO~D agreed to hold ModelTab/modelSheet candidates until it landed (msg 29294).

## 2. The WORLD act al-5 -- ledger `amgt-corpus-r36-al5`

| leg | result |
|---|---|
| L0 | Started after RESAPP aq-5 CLOSED (22:27:41Z, no rollback). Base re-read unchanged (`aoQ+WrefJ`, 1769, `auoGQqF5`). Real build from a clean detached checkout at `288de3d95d`: CONTENT-DIFF 356 files, CHANGED 1 (`scoped_amgt.py`), ADDED 0, REMOVED 0; FATAL []; isolated 3/3; 96.8% of the ceiling |
| L1 | Upload VersionId `O1WGPxfTK9vszvvZqzzuOfjQAGMOIZiM` (41,158,959 B, content-sha `2rFeF57l`), re-read by head-object |
| L2 | FULL plan from show -json: 49 = 48 no-op + 1 update (the function: `s3_object_version`, `source_code_hash`); memory 1769 -> 1769; 0 IAM/route/gateway/destroy/create. HALT-GATE: 28 items, 0 touching this act, so HALT_ACK. Apply 0/1/0. Live CodeSha256 `2rFeF57l` |
| L3 | `al5 deployed build 1/1 control 1/1` (1299 HK 97/97, BA 0/0). RESAPP regressions: r67 c23/c25/c26 YES; c24 NO = aq-5's own closing state (74 mismatches on days 30/90/365, its missing grant), unchanged; r66 c18/c19/c22 YES; r65 c17 YES; r64 c9-c14 YES; r64 c15 first read NO on WARM containers only (~250 ms, 200, 6 headlines), then YES cold after 15 min idle (1935/2369/2327 ms) |

Evidence: `evidence/r36_al5_build_only.txt`, `evidence/r36_al5_leg_v_served.txt`, `evidence/r36_al5_leg_v_regressions.txt`.

## 3. The real run (both outcomes on the page) -- `evidence/r36_al2_real_page.md` @`adebac9c47`

Candidate `75efe9d6` (now DEV), against the redeployed API. Walks: BA `tmp/ui-walk/20261004T224710Z` and 1299 HK
`20261004T225046Z`, 0 API issues, disarms REFUSED.
- 1299 HK's Model tab shows the group "VALUATION, RETURN AND BALANCE-SHEET LINES" after "EBITDA AND MARGIN HISTORY", with the
  45 lines in words and typed.
- It shows the facts line: "Company short name: AIA; Country: HONG KONG; Average daily value traded (three months): 2,079,092,000;
  Market capitalisation: 715,988 million".
- It shows one reason line: "Lines with no figure: Bloomberg returned no value for this line for this company".
- The fully-absent lines are named in the footnote.

**For your AC3 judgment, two limits the issuer read on the page:**
1. **A gap inside a showing row has no reason.** The price-dated range rows read `--` in 2016, 2017 and 2022 on 1299 HK. Those are
   the years the API now serves "not dated at the fiscal period end (non-December FYE, fye_join)" for, 97 entries. al-2 words a
   reason only for a FULLY absent row.
2. **Money lines name no currency.** The V3 money rows carry the page's "currency not stated by the source" mark, and the facts
   line prints market cap and average daily value with no currency. This is row Z-W2-S20, and the CTO's round-37 candidate.

## 4. Rows, and what the round-36 analysis receives

| row | standing | what |
|---|---|---|
| `Z-W2-S20` (al-3) | OBSERVATION, INERT | On TSM, 92 of the 52's 167 figures are monetary and carry currency null / basis invariant on a USD-quote, TWD-filing block. The block's `currencies` entry is right; the 52 are not wired to it. BA and SAP carry the same null on single-currency blocks |
| none new | -- | al-1, al-2 and al-5 filed no rows |

al-3's read: 24 family rows, RIGHT 19 / WRONG 0 / CANNOT-TELL 5 (YEAR x3 unserved; TSM diluted shares and EPS unserved). TSM
currency labels: right 75, wrong 92, cannot-tell 0.

**Candidates for round 37, mine to name and the CTO's to rule** (the CTO names the first, Z-W4-S4 and al-4):
1. Currency labels for the 52's monetary figures (producer/classifier, then one re-derive of the 96 blocks), so the page names
   them. This is row Z-W2-S20.
2. A reason for a gap inside a showing row (FWD-20 section 3, limit 1). The page has the served per-year reasons now.
3. Row Z-W4-S4 (the CTO's pick).
4. al-4: the 2026-10-05 13:00Z fire's read, carried.

Push state: LOCAL (ls-remote read at commit time).
