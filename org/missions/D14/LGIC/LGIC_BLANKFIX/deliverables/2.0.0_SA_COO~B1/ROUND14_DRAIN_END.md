# LGIC_BLANKFIX -- round 14 drain end: FWD-4 row by row (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @032773b458, `decompositions/LGIC_BLANKFIX_DECOMP.round14.md`, cut on `ledger/ROUND_ANALYSIS.round13.md` @9abfddbcff.
That analysis found 8 of 9 REALIZED, and FWD-4 not yet REALIZED (rows S8 and S7).
**Orders:** 3 of 3 complete and merged. The issuer re-proved each before its merge, and the slots are removed.

| cell | ruling | merge | proof |
|---|---|---|---|
| `BF-ac-1`, cadence words from fires | R1 (S8) | @1f63f8ca4a, closed @a5ed95d0dd | `FWD4-CADENCE-R14 ok=True schedules=180 agree=148 partial=32 mismatch=0 carried_over=0` (BAC1-AC1, re-run on the trunk per AMENDMENT 1); `FWD4-RENAME-12H ok=True name=news-keyword-intelligence-generator-12h grade=CONFORMANT` |
| `BF-ac-2`, firm schedule names from `name()` | R2 (S7) | @48ca3c6a7b | `FIRM-SCHEDULES ok=True lines=31 builder_names=31 gate_pass=31 owed_rows=0 hand_composed=0`; the typed-literal control is refused 31 of 31 |
| `BF-ac-3`, owner and scope as columns; per-firm rows as patterns; the no-word partial form (AMENDMENT 1) | R4, R5 | @48ca3c6a7b | `FWD4-STORED-R14 ok=True files=254 owner_and_scope=207 per_firm_patterns=14 undecided=10 owner_unnamed=23` |

**Amendment:**
- AMENDMENT 1 (@2c56f0390a) moved the `decide()` partial form from BF-ac-1 to BF-ac-3. The file belongs to slot ~2, and both slots
  were writing it at once. BAC1-AC1 was then re-run on the trunk after slot ~2's merge.
- When the issuer tried to update BF-ac-1's proof instance, the TREE_DELIVERABLES lane refused it, because the folder is the worker
  serial's. The worker closed it on its own instance @baf738ea62.

**Hygiene:** every `lib/tests/test_opal_naming_*.py` passes (ROOTCHECK 355); `.tools/naming-gate.py --self-test` passes; and `pytest lib/tests`
reads 193 passed, 1 skipped.

## The real run at the close (FWD-4 row by row)

`ALL_ROOTS_round14.txt` beside this file, base a5ed95d0dd:

`ALL-ROOTS ok=True roots_total=86 mapped=86 unmapped=0 ... right=669 fix=1618 not_asked=268 pattern=39 ... hole=7 ...
unknown_word_holes=1 other_holes=6 stale_hints=0 uncounted=1 counted_at_caller=17`

- **Schedules:** of 180, 148 carry a word their expression agrees with and 32 print their partial form with a reason. 0 disagree and
  0 carry over an old word. This is the CTO's close test: no row where the word and the expression disagree.
- **The 6 partial-form rows** are the AMENDMENT 1 rows, each a HOLE that prints the reader's reason:
  - `fear-greed-daily-update` and `trending-topics-portal-publisher-daily`: fires at 14 and 21, gaps of 7 and 17 hours, uneven;
  - `keyword-drilldown-generator-daily`: 12 and 21, uneven;
  - `finbert-scoring-post-ingestion-45min`: 0, 13 and 20, uneven;
  - `teams-global-transcripts-pull-hourly`: 13-22, not a fixed interval;
  - `fred-ingestion-monthly-early`: first Friday, no cadence word.
- **Firm-bearing schedules:** all 31 are builder output and pass the live gate.
- **Stored files:** 207 print owner and scope as two columns. The 14 per-firm rows show as patterns. The 10 open-place rows and the 23
  owner-unnamed rows print UNDECIDED with their reason.
- **FWD-8 still holds:** `FWD8-PATTERNS ok=True ... patterns=25 shown_as_pattern=25 shown_as_name=0`. The census `pattern=39` adds the 14
  per-firm stored-file rows.
- **The 7th hole is not this round's:** `HOLE S3Key _status/lots_not_computed.json -> K1: segment 1 '_status' is neither a source nor a
  tier [infra/aws/lambda/investor-reporting/reporting-gold/handler.py:448]`. It is a key newly in another project's code (items 2599 ->
  2601 since round 12), owed to the registry writer.

## Rows for the round-14 analysis

- **D1-W2-S9:** a firm schedule passes the gate only in the `opal_name` module form. The gate grades 0 strings there; the typed literal is
  refused. Owner: `1.0.0_SA_CTO`, for FWD-4's grade.
- **D1-W2-S10:** 23 FIX stored-file lines have no key ruling row naming a mover, so their owner prints UNDECIDED with a reason.
- **D1-W2-S12:** `place()` now returns PATTERN for the 14 per-firm names. The gate self-test passes; the commit-gate behaviour on such a
  name is otherwise unmeasured.
- **D1-W2-S8:** `name()` refused the interval word `15min` through an `_is_cadence` gap, which is fixed in `lib/opal_naming.py`.
- **D1-W2-S11:** the round-13 stored-file checker was re-parsed for the `scope=` field.
- **D1-W1-S9 and S10:** S9 is resolved by S10.
