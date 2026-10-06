# AMGT_CORPUS round 38 CRPS-an-7 -- the census half of the FWD sweep (FWD-14, FWD-19), read 2026-10-05 ~20:5xZ

Read-only. Raw outputs:
- `r38_an7_coverage.txt` -- `python -m lib.research.corpus.backlog --coverage-dry-run`, rc 0, `written NONE put_performed False`;
- `r38_an7_folder_reads.txt` -- `--folder` on 3 names.

These are measurements laid against each DONE WHEN. Grading them is the CVO's job.

## FWD-14

DONE WHEN (PRD ENDPOINT): "for a named folder the read returns a dossier or a reason; and the three counts (resolved / ambiguous
/ empty-or-workbook-only) SUM TO THE FOLDER COUNT every time".

**Limb 1, a named folder returns a dossier or a reason:** 3 of 3 named reads did, one per disposition class:

| folder | disposition | what the read returned |
|---|---|---|
| Brookfield Corporation BN CA | unresolved-with-reason | the reason: `security-6de6b403b5858428` matches no identifier form in crosswalk/v1, "NOT guessed" |
| Air Liquide AI FP | served-as-empty-shell | a dossier URI, with reason "empty" |
| Costco COST | served-as-empty-shell | a dossier URI, with reason "workbook-only" |

**Limb 2, the three counts sum to the folder count:**
- The read is `fence14 resolved 84 ambiguous 0 empty-or-workbook-only 12 sum 96 outside-fence 1 folders_read 97`.
- **The three counts sum to 96, against a folder count of 97.** The one folder outside them is Brookfield, unresolved, which none
  of FWD-14's three categories holds.
- The tool prints the miss as `outside-fence 1` and names the folder (`fence14_outside ...`).

## FWD-19

DONE WHEN: "a census prints, for all 93, dossier-served / resolved-but-no-prose / unresolved-with-reason, and THE THREE SUM TO 93;
the 60 today-unresolved folders are inducted by a SCRIPTED producer and re-ingested; and the 11 that can never carry prose
(10 workbook-only, 1 empty) are NAMED".

**Population:** the library now holds **97** folders, not 93. The sweep reads the clause on the live population.

**Limb 1, the three sum to the folder count:**
- The read is `fence dossier-served 83 resolved-but-no-prose 13 unresolved-with-reason 1 sum 97 folders_read 97`.
- So it sums.

**Limb 2, scripted induction:**
- The scheduled induction (`amgt-induction-daily`) is FWD-22's producer, REALIZED at round 35.
- 1 folder (Brookfield) stays unresolved, and its reason is printed.

**Limb 3, the never-prose folders are named:**
- The read is `never_prose_named 12`: 11 workbook-only and 1 empty (Air Liquide).
- All 12 are listed by name in `r38_an7_coverage.txt` :4-15.
- The PRD counted 11 (10 workbook-only + 1 empty), so the live population added one workbook-only name.
