# LGIC_BLANKFIX -- round 13 drain end: FWD-4 and FWD-8 served (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @fbbe63a3ad, `decompositions/LGIC_BLANKFIX_DECOMP.round13.md`, cut on `ledger/ROUND_ANALYSIS.round12.md` @b45108c324.
That analysis found 7 of 9 outcomes REALIZED, and FWD-4 and FWD-8 never served.

**Orders:** 3 of 3 complete. The issuer re-proved each in its slot's worktree before the chain-end merge, and removed the slots.

| cell | serves | merge | proof re-run by the issuer |
|---|---|---|---|
| `BF-ab-1`, schedules (group C) | FWD-4 | @c0664b9e80 | `FWD4-CADENCE ok=True schedules=180 agree=144 undecided=36 mismatch=0`; `FWD4-RENAME ok=True name=estate-report-0900et-daily grade=CONFORMANT`; **BAB1-AC3 judgment, ungraded** |
| `BF-ab-2`, stored files (group D) | FWD-4 | @910a465426 | `ROOTCHECK-TEST ok=True cases=334`; `FWD4-STORED ok=True files=254 with_source_owner=230 undecided=24` |
| `BF-ab-3`, the whole list | FWD-8 | @910a465426 | `FWD8-PATTERNS ok=True roots=75 items=2599 patterns=25 shown_as_pattern=25 shown_as_name=0` (its own detector, plus a negative arm) |

**Hygiene:** every `lib/tests/test_opal_naming_*.py` passes, and `pytest lib/tests` reads 193 passed, 1 skipped. No `infra/` or
`org/mcp/` file changed. The scope test reads 826 assertions on the trunk, down from 831, because the two retired roots shrank the data.

## The exercises (FWD-4 DONE WHEN, "renamed from the list alone")

- **Schedule:** `estate-report-0900et` was renamed to `estate-report-0900et-daily` from its list line alone. The rename was made in a
  temporary copy of `infra/aws/terraform/estate-report/orchestrator.tf:56`. The real `.tools/naming-gate.py` read it `NAMING-GATE: PASS
  1 graded`, with no placement refusal. Negative control: the wrong cadence word (`-hourly`) was refused, with `NAMING-PLACE: REFUSE 1`.
- **Stored file:** `code/bronze/cot_bronze_ingest.py` -> `blackdiamond/49financial/code/bronze/bronze_ingest.py`, source `blackdiamond`,
  owner `49financial`, read from the list line alone. Nothing was moved.
- No live rename or S3 move was made. Each would be a deploy or data act with its own pair.

## The real run at the close

`ALL_ROOTS_round13.txt`, base 910a465426:

`ALL-ROOTS ok=True roots_total=86 mapped=86 unmapped=0 ... items=2601 right=672 ... pattern=25 ... hole=0 ... stale_hints=0 uncounted=1`

The item count rose by 2 against round 12, from other projects' new names (both read RIGHT). Holes stay 0.

## Rows that bear on the FWD-4 grade

- **`D1-W1-S7`:** for the 21 of 120 FIX schedule lines that carry `49f`, the gate refuses the list's new name as a hand-kept
  firm-token carrier. Those list lines cannot be landed as printed. The 10 lines carrying `cot` were not run.
- **`D1-W1-S8`:** 10 of the 36 undecided rows state an expression, but the list keeps the word the current name already carries.
  Seven fire twice a day under `daily`, and `finbert-scoring-post-ingestion-45min` fires three times a day.
- **`D1-W2-S6`, ruled by the issuer:** 20 stored-file lines take source and owner from the grader's canonical address (key grammar
  and vocabulary), not from a ruling row. This counts: it is the canon, not the folder name.
- **`D1-W2-S7`:** a ruling row's own `owner` field names who moves the store. `owner=` prints the address's scope, which says whose
  file it is.
- **The 24 UNDECIDED stored files:** 14 are per-firm rulings whose owner is filled per firm at run time; 10 carry an open
  `{source}`/`{scope}` place.

## Open for the round-13 analysis

- **BAB1-AC3 (judgment, `3.0.0_SA_CVO`):** does a person reading the schedule agree with the word the list chose? The three
  schedules are:
  - `bd-pipeline/bd-49f-interim.tf:148`, `rate(15 minutes)`, read as `-15min`;
  - `estate-report/orchestrator.tf:56`, `cron(0 9 * * ? *)`, read as `-daily`;
  - `etfs-reports/orchestrator.tf:178`, `cron(0 10 1 * ? *)`, read as `-monthly`.
  `round-close-check` reads REFUSED on this judgment alone.
- **FWD-4's and FWD-8's grades are `1.0.0_SA_CTO~DELL1`'s,** weighing S7 and S8 against FWD-4's ACCEPT ("a person who reads the
  schedule itself agrees with the word the list chose").
