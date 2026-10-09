# NFRA_TRNSPT round 18 -- close record: coverage graded; the second reader built; two served applies carried (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `ffa3c6987d` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R18.md`, CTO ADDENDUM 6). `round-close-check --round 18` MAY-CLOSE (2 orders).

- **TR-g-18 (coverage):** merged `ed84ea7977`, `R18-G18-OK 8 rows` (`R18_COVERAGE.md`). Graded by the CTO, ADDENDUM 8 @c592051597: FWD-7 REALIZED;
  FWD-1, 2, 3, 4, 5, 6, 8, 9 NOT REALIZED, each with its hop. Rows filed: W1-S7 (Teams silver unwiped vs PRD C-TIERS), W1-S8 (`read_meeting.py`
  prints held-out Research rows) -- W1-S8 ruled ARMED, disarm owner this seat: `read_meeting.py` is NOT run against Research silver until the
  round-19 fix lands.
- **TR-p-18 (FWD-8 second reader):** merged `f8c4859407`, `R18-P18-OK 3 passed`: role `teams-global-transcripts-second-reader-role` (name() output),
  GetObject/ListBucket only, added to `NamedReadersUseTheKey`; nothing else widened.
- **TR-a-18 (its apply): CARRIED.** Pair GIVEN (COO @056809859f, CTO @f2ec32dea4, trust `user/Opal_Terminal`, measured tag
  purpose=bloomberg-terminal-device). Order `NFRA_TRNSPT.TO-APPLY-a18` @04313a7e39 relayed to the laptop via MSTR.
- **TR-s-18 (FWD-2 scheduled read):** read @3f7583537b -- NOT READABLE: the Teams meeting pull was never applied (pull.tf DESIRED only).
  CTO ADDENDUM 7 cut its apply: order `NFRA_TRNSPT.TO-APPLY-p18` @7dcb3cc48f, pair GIVEN (COO @7dcb3cc48f, CTO @b972f130c9). **CARRIED and HELD at
  step 2:** the COO half's line that new silver lands "through the same wipe" was FALSE (`parse_silver.py:5-6`: no PII wipe on transcripts); the
  half is SUSPENDED (ADDENDUM 1 @507be5a916) pending the CTO's (a)/(b) re-rule. The error is this seat's: the line was written without reading the code.

Round 19 rectangle: the CTO's ADDENDUM 8 enrichment list (W1-S8 first, as ARMED).
