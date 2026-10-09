# AMGT_RESAPP round 87 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-09 ~20:1xZ. Four of four orders terminal, all complete; round-close-check MAY-CLOSE (4 of 4, proofs 4 ok).**
Nothing below is a verdict. Round 87 implements the CTO~DELL1 round-86 analysis `ledger/ROUND_ANALYSIS.round86.md` @2eba7c172b (R1-R3);
decomposition s.95; issuance @433e2b510d. Item 4 (kk-1 republish, W338-S1 yield) was done in round 86 and not cut.

## 1. Orders (each line is the order's own last status, written at its drain)

- **`AMGT-ll-1`** (a FAILED description is never served): complete -- merged @fa79702892. `read_drafted_sections` serves a
  company_description whose own verdict reads FAILED with `sentences: []`, keeps the state and reason, adds `withheld_failed`, and carries
  `description_verdict_test` so the /overlay header keeps its failed_on / rule detail. 3 tests (the base code fails the FAILED arm); local
  check YES while NU still read FAILED.
- **`AMGT-ll-2`** (NU's description empty): complete -- merged @5939733791, under kk-3's pair (COO ADDENDUM 1). One key
  `drafting/v1/NU_US_Equity.json`: prior ms8LxPe8... kept, new WniVHKcc...; the local diff is one path (`/sections/0/sentences`, 1 -> []).
  NEVER-2 entry CLOSED. NU serves 0 description sentences; outside the section 0 of 98 restated or glued, every name at its base.
- **`AMGT-ll-3`** (the redeploy): complete -- `0.7.0_AE_CloudOps~RA1` @7f0ecf440c, proof VALID (12 of 12 controls). Pair COO + CTO
  (@b6f9ac164e, conditions 1-3). Live `HZoC2x` -> **`b7Lj1J/KKhDtg+mvN/vmu4VAoaExU055uB78roHiHfM=`** (19:51:25Z), pin 9c32fb942d; content
  diff 7 non-identical, 0 off-list. Condition 1: AMGT_CORPUS leg v graded /9 before the pin (95 of 95, ellipsis 0, prefix 0; C1 msg
  3057). Condition 2 printed an EMPTY FAILED list at the pin (ll-2 had emptied NU), so AC1 is a bound (ruled, msg 3091): the deploy is
  discriminated by the issuer's byte read -- the deployed `scoped_amgt.py` is byte-equal to the pin (sha256 5b987a17...) and carries the
  withhold. RA1 notes two /thesis bodies moved (BABA -20 B, NU +74 B), attributed to dossier_sections; the sentence and store checks below
  read every drafted section unchanged.
- **`AMGT-ll-4`** (the open remediation rows): complete -- merged @4c3f3fcb2e. `deliverables/0.9.0_WK_AMGT_RESAPP~348/DISPOSITION_LEDGER.json`:
  125 of 125 open rows (of 505) disposed once -- CLOSED 66, CARRIED 29, DISMISSED 30, carried without an owner 0. Issuer rulings on two
  carried to this seat: D1-W339-S2 and D1-W338-S1 -> CLOSED by round 86 (kk-3 @23a50926ad, kk-5 @2cb7806aa1). **The ledger is the CVO's
  to apply to REMEDIATION; no channel file was edited.**

## 2. The issuer's ONE REAL RUN at close

`round87/ONE_REAL_RUN_20261009.txt` (script `round87_prep/checks/r87_real_run.sh`), live `b7Lj1J` (hash read before and after, equal):
- `r87_withheld` AC1: **YES** (no FAILED description served; 5 of 5 answer); NU: **YES** (0 sentences).
- `r87_dossier`: **YES** (deployed /9, not /8).
- `r87_rows` on the ll-4 ledger: **YES** (125 of 125).
- Round-86 set, no regression: `r86_description` YES; `r85_sentences` outside the description YES (0 of 98); `r85_crosswalk` YES (folders
  102); `r84_listing` YES 3/3; `r86_yield` YES; writers 8 passed; kk-1 guard 10 passed; `r84_store` AC1 + AC2 YES 5 of 5; r82, r81, r80
  deployed YES.

## 3. JUDGMENT for L9

1. The CVO's read of NU's served page: the description card shows its empty state (CTO condition 4, R2).
2. Apply the ll-4 ledger to the REMEDIATION rows (the analysis's R3: the count after the pass is printed above).

## 4. Rows filed this round

RA1's ll-3 report filed none (the bound was predicted by the COO half). Carried rows are in the ll-4 ledger.

## 5. For the next round

1. D1-S18: the scoped watchlist route refuses an off-list selected_tenant like the other scoped routes.
2. AMGT_RESAPP-S3: `library.py` refuses a SET but nonexistent `OPAL_RESEARCH_LIBRARY_ROOT`.
3. The rows the ll-4 ledger carried to `2.0.0_SA_COO~R1` (D1-W332-S2, D1-S14, D1-S16, D1-W345-S2, Z-W212-S2, Z-W266-S3, and the live ones).
4. FWD-16 waits on Andrew's 2026-09-15 hold; the model key rotation is Andrew's act.
