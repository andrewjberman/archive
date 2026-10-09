# RESTATEMENT_RULE -- IRPT_DASHBD.TO-DB-b-111 (cell DB-b-111, FWD-8, E3)

Pre-registered by 0.9.0_WK_IRPT_DASHBD~86 BEFORE any run. This file is committed alone; the script and both records are committed
later. Nothing below carries an account number or a client figure. Claim on every restated figure: INFERRED (a restatement is a
computation, not a Black Diamond field).

## 1. The common convention

Opal's declared design (account_return_daily.py, C-METHOD and amendment 5 (d)): the return is GROSS of ADVISORY fees
(FEE-MANAGEMENT is added back as a flow); an administrative or service fee (FEE-ADMIN) STAYS INSIDE the return; income counts on CASH
RECEIPT. Black Diamond books a service-fee row as a net addition (outside its return) and accrues income at a boundary before it is paid.
The CTO's ruling on W75-S1 (ADDENDUM 19 item 2): compare on ONE convention, never two; restate Black Diamond's return to Opal's.

## 2. The restatement (both sides' own figures only)

Tolerance: 0.35 pp, never widened. Grade = absolute difference in percentage points, "within" when `<= 0.35`.

Inputs per segment, keyed (account, start, end), all read from the private evidence the face names (no S3, no vendor call):
- `opal_return`, `bd_gross_return` (Black Diamond's compounded return with its advisory fee added back, the tie-out's comparator), from
  `~35/TIEOUT_COMPOUND_V2.json`;
- `restated_return`, from `~75/W73_S1_EVIDENCE.json` `return_read`: Opal's own daily series re-run with the two Black Diamond conventions
  (service fee as a flow on its day; income accrued, money-market accrual spread linearly between payments).

Define the CONVENTION SHIFT of a segment: `shift = restated_return - opal_return`. It is the return effect of exactly the two
conventions in section 1, measured on Opal's own series and the custodian rows that tie.

Black Diamond restated to Opal's conventions: `bd_restated = bd_gross_return - shift`.
Restated grade: `restated_diff_pp = abs(bd_restated - opal_return) * 100`, which is identically `abs(bd_gross_return - restated_return) * 100`.
The shift is applied additively (first order), as the tie-out's own add-back is; that is a stated approximation.

SCOPE OF THE RESTATEMENT: `shift` exists only where a per-segment two-sided convention measure exists, which is the 74 segments of
`~75/W73_S1_EVIDENCE.json`. Every other outside segment has no measured convention shift in any record the face names; its shift is NOT
imputed as zero and NOT estimated: it is "not restated", and it keeps its reason (section 3). A restatement is never invented to reach 0.35.

## 3. Classification, applied in this order to each of the 990 outside segments (reason source = DB-b-99's final)

Current reason of a segment: the `~73/UNEXPLAINED_CLASSIFIED.json` reason for the 510 re-derived (a `ZERO_GAIN_VENDOR_TWR` is UNEXPLAINED, per
DB-b-99's `regraded_to_unexplained`), else the `~35` reason (FLOW_TIMING, INCOME_DATE, MISSING_PRICE, COVERAGE_DAYS).

Rulings applied (1.0.0_SA_CTO~DELL2 ADDENDUM 21, relayed by 2.0.0_SA_COO~D2). They are classification rules over the restated grades, not
part of the restatement in section 2:
1. **Matching dates refute FLOW_TIMING / INCOME_DATE.** A FLOW_TIMING or INCOME_DATE segment that DB-b-106 graded `confirmed` (dates agree)
   becomes UNEXPLAINED unless step 3 below gives it CONVENTION; one DB-b-106 graded UNEXPLAINED stays UNEXPLAINED. No FLOW_TIMING or
   INCOME_DATE label survives into the output.
2. **NOT_COMPARABLE.** A segment whose END date is after 2026-08-20 (Black Diamond's transaction record ends 2026-08-20) is
   `NOT_COMPARABLE`, reason `BD_RECORD_ENDS_2026-08-20`. This test comes FIRST and is by date alone, over all 990. The count is printed. The
   ruling names "the 319 DB-b-106 flagged"; the date test is the mechanical form of "segments falling after 2026-08-20", and where the
   319 and the date test differ that difference is reported in a row, not resolved here.
3. **CONVENTION.** Among segments not NOT_COMPARABLE: a segment with a section-2 restatement whose `restated_diff_pp <= 0.35` is
   `CONVENTION` (confirmed). A segment still outside 0.35 after restatement is NOT explained by convention.
4. **Everything else** keeps its current reason, except that FLOW_TIMING and INCOME_DATE become UNEXPLAINED by ruling 1. A segment whose
   current reason is DEFECT keeps DEFECT (a cause was found in DB-b-100 / DB-b-101).

`comparison_window_end` is stated in the repo record as 2026-08-20.

## 4. The records

- Private, per segment, outside the repo: `C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~86/RESTATED_TIEOUT.json`.
- Repo (counts and sha256 only): `RESTATED_TIEOUT.json` beside this file: `n_outside_before` 990; `by_reason` summing to 990 (keys include
  `CONVENTION` and `NOT_COMPARABLE`); `within_after_restatement` (segments within 0.35 after section 2, counted over all 990 before the
  section 3 window test, with the count inside the window beside it); `comparison_window_end`; `rulings_applied`; `private_record` {path,
  sha256}; `preregistration` {restatement_rule_file, rule_commit, output_commit}.
- Account tokens in the repo, if any, are `acct#<sha256("49financial:<account>")[:8]>`. None is needed.
