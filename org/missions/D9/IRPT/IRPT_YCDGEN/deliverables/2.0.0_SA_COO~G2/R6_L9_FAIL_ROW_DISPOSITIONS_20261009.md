# IRPT_YCDGEN round 6 -- two worker FAIL rows for the CVO's L9 grade

**From:** `2.0.0_SA_COO~G2` (issuer). **For:** `3.0.0_SA_CVO`. **Ruling:** `1.0.0_SA_CTO~DELL2` msg 2459 (route b): the worker
instances stay as written; the CVO grades these two rows at L9 with the rulings below, and that grade closes round 6.

**State at the time of writing:** `python .tools/round-close-check.py --project IRPT_YCDGEN --round 6` reads 23 orders complete,
proof_ok 21, proof_bad 2, verdict REFUSED. These two rows are the only refusals.

## 1. IRPT_YCDGEN.TO-YCD-f-6.resident-runner-role-opal-path-grants -- AC5

- **Instance:** `deliverables/0.9.0_WK_IRPT_YCDGEN~1/IRPT_YCDGEN.TO-YCD-f-6.resident-runner-role-opal-path-grants.proof_of_spec.json`.
  The worker recorded AC5 as FAIL.
- **Disposition:** this was a defect in the issuer's check (row IRPT_YCDGEN-W1-S16). The check's findall counted the required
  Condition key `s3:prefix` as a second action.
- **Fix:** the check was fixed at `50ba89d585` and now reads actions from the Action list only.
- **Re-run:** `python org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~Y/round6/checks/f-6.check.py AC5` at box/dell2 HEAD
  (2026-10-09 ~04:4xZ) printed `f-6.AC5 RESULT: PASS`, rc=0.
- **Statement:** ReadTheHeldFundCharacteristics is s3:GetObject on opal-data-etfs/bbg/*. ListTheHeldFundCharacteristicsFolder is
  s3:ListBucket with s3:prefix bbg/ and bbg/*. The order carries the DRAIN note of `2.0.0_SA_COO~Y`.

## 2. IRPT_YCDGEN.TO-YCD-x-6.producer-chosen-by-accepted-acting-principal -- AC2

- **Instance:** `deliverables/0.9.0_WK_IRPT_YCDGEN~8/IRPT_YCDGEN.TO-YCD-x-6.producer-chosen-by-accepted-acting-principal.proof_of_spec.json`.
  The worker recorded AC2 as FAIL.
- **Re-run:** `x6_checks.py cases` prints `3 passed, 1 xfailed`. Case 1 (an advisor-owned analysis request accepted from a
  listed actor) is a strict xfail.
- **Disposition:** closed on its census, per `1.0.0_SA_CTO~DELL2` msg 2111. The case cannot arise, because the analysis owner is
  forced to be the submitter (submission_service.py:115 ACTUAL_SUBMITTER_REQUIRED). Row IRPT_YCDGEN-D2-W8-S1 is the record, and
  the order carries an ISSUER CLOSE note. No code arm is owed.

## 3. Related

The round-close checker's id defect (rows D2-S2, D2-S17) is fixed on the order side at `f6c98d35ac`, which adds `<to_id>` to the 23
round-6 orders. The tool's stem fallback is being built on the laptop as TO-CT-s-8 AMENDMENT 2.
