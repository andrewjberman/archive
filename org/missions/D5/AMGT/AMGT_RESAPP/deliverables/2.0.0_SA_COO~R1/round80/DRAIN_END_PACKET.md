# AMGT_RESAPP round 80 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: DRAFT, 2026-10-09 ~03:4xZ. dd-4 APPLIED (live `OUOsYXa`, 03:37:34Z) and the one real run reads YES (section 2); the order's
close and its ledger are the applier's report, pending.** Nothing below is a verdict.

Round 80 is the first round on dell1. It implements the CTO~Z round-79 analysis (`ledger/ROUND_ANALYSIS.round79.md` @c249be336b,
R1-R5). Decomposition s.88; issuance @5681442761 (4 orders, fanout 3 of 3 chains, cap 8). Every commit named here is on box/dell1.

## 1. Orders (each line is the order's own last status, written by the issuer at its drain)

- **`AMGT-dd-1`** (R1, code half): complete -- merged @6e44bfec4a as a SITE-Z DEPLOY under the pair COO @afd9b76ee1 (census corrected
  @6fd5166a9a) + `1.0.0_SA_CTO~Z` @f1a7df146f; NEVER-2 entry `20261009T0255Z_amgt-resapp-r80-dd1-sitez-cutter-merge` CLOSED, 2 of 2
  legs. Re-run on the merged tree: filings suite 217 passed (fitz stubbed: PyMuPDF does not import on dell1); R80 R1 AC1-AC3 SERVED:
  YES. Two amendments (section_coverage.py, then its test) on the issuer's drain read. Census: 0 of 5 stored 20-F names carry a
  business section; 4 of 5 risk items came from the removed fallback heading.
- **`AMGT-dd-2`** (R2): complete -- drained @a06f7f9c20; AC1-AC3 SERVED: YES on the shared tree (AC1 after the issuer repaired its own
  check's P6). Locally: 0 of 272 served citations letterless (4 before); stored records untouched (41 of 1122 still carry one).
- **`AMGT-dd-3`** (R3, a read): complete -- drained @a68418f40a; R80 DD3 WALK RECORD: YES (17 captures, portal `8d2a08a92b5e`, one
  commit on `84e13d0f`); walker disarmed. AC3 is yours (section 4).
- **`AMGT-dd-4`** (redeploy of dd-2 + R5's source-map record): IN FLIGHT. First GO @3be917d400 STOPPED correctly at step 3 (row D1-S4:
  three packaged registry data members off the COO half's list); both halves' ADDENDUM 1 admit them (COO @c79b9318b8/@5d24268e09,
  CTO @b7f8b30f32) with CTO condition 5. Second STOP (row D1-S5): harvest/ never initialized on dell1; AMENDMENT 1 @3c9385489c admits one
  terraform init provider fetch under law edit 4d77a9c3ea (egress open except Bloomberg).

## 2. The issuer's ONE REAL RUN at close

`round80/ONE_REAL_RUN_20261009.txt`, run by this seat 2026-10-09 ~03:45Z on the live function `OUOsYXaJSklKJ65vpIe2jWfcXm9jvP0bCyia15F8Bxs=`
(LastModified 03:37:34Z); the hash read before and after the run, equal.
- `r80_dd4_served.py --where deployed`: **R80 DD4 SERVED: YES**, exit 0 -- 12 of 12 names answered 200; served citation locations
  with a letterless heading **0 of 271** (4 of 271 on the prior function `ltXvElw`: ASML NA "5.09%", "0.01%"; SAP GY two zero-width spaces).
- `r79_deployed.py`: **R79 DEPLOYED: YES 1 of 1**; `r78_deployed.py`: **R78 DEPLOYED: YES 3 of 3** (no regression).

## 3. Not cut, and why (decomposition s.88b)

- **R1's store half** (re-fetch ASML NA's 20-F, its silver row, re-analysis, draft rebuild): held at the cut for Andrew's per-use
  egress word. That hold LIFTED mid-round (law edit 4d77a9c3ea, egress open except Bloomberg; MSTR~DELL1 msg 1498); not cut
  because the decomposition is frozen. Row AMGT_RESAPP-D1-S3. It needs no Bloomberg call.
- **The ABNB model-block pull and the ICT identity read:** filed as MDPF_DEMQUE requests @3a9a64971e (tier 4); site Z draws them;
  `2.0.0_SA_COO~Q1` holds them and records the measured cells.
- **FWD-16:** Andrew's 2026-09-15 hold, unchanged.

## 4. JUDGMENT for L9 (yours)

**dd-3 AC3, the walk on DEV.** Record `deliverables/0.9.0_WK_AMGT_RESAPP~317/WALK_ROUND80.md`, 17 captures. The worker's
observations, no verdict:
- **FWD-1, AMD US:** the page draws a "REVENUE BY SEGMENT" table, six rows, first column Fiscal year 2025 (Data Center 16,635); the
  API's `segment_table` is served, 6 rows, first value 16635, USD millions. Lower on the same page the "Business segments -- from the
  filing" panel still reads "No filing analysis is stored for this name yet, so no segment breakdown is shown." (capture 014).
- **FWD-7:** the page draws the served Seeking Alpha sentence on 10 of 10 rows (BA, BABA, COST read; AIA, NOW, ZURN no record; Hon
  Hai, MNST, KDDI checked; Lenovo read and stale). 1 of 95 rows flagged stale. First paint 3,702 ms, second 1,792 ms.

## 5. Rows filed this round

AMGT_RESAPP-D1-S2 (issuer cut defects: dd-2 P6 and the R1 id form), D1-S3 (R1 store half unblocked), D1-W315-S1/S2 (dd-1's
test-file grant, resolved), D1-W317-S1 (walker DeleteParameter denied on disarm), D1-W317-S2 (walk script's bare python lacks
bcrypt), D1-W317-S3 (R1 id form refused), D1-S4 (dd-4 step-3 STOP, filed by the applier), D1-S5 (dd-4: harvest/ uninitialized on dell1; ruled by AMENDMENT 1).

## 6. For the next round (carried; cited, not cut here)

1. R1's store half (row D1-S3), then a FWD-18 walk on ASML NA.
2. The "Business segments -- from the filing" panel's sentence beside a served segment table (FWD-1, dd-3 capture 014): the page's
   owner is DSGN_AMGTV1.
3. The walker's disarm on dell1 (row D1-W317-S1): DeleteParameter is denied by design (CTO~DELL1 msg 1386); the skill's disarm
   step should not need it.

-- 2.0.0_SA_COO~R1
