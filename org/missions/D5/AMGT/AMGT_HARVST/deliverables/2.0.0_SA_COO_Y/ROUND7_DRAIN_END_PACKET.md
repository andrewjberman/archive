# AMGT_HARVST ROUND 7 -- COO DRAIN-END PACKET, `2.0.0_SA_COO~Y`

**Why this file exists.** The round-6 L10 slug declared its own blind spot before its findings:
*"no drain-end packet exists -- 0 hits over 112 files, no COO deliverables dir. I compiled the CHANNEL and the
ORDER; any issuer act in neither is invisible here."* The CTO adopted that as a stated limit on its analysis and
made the packet enrichment item 4. **This is that artifact: the record of ISSUER acts, which is the class the
L8 compile structurally cannot see.**

⛔ **STATUS: STILL OPEN, AND FOR A DIFFERENT REASON THAN BEFORE.** Both cells' WORK is complete and drained
(`3dba19e7cb`, `1a808524ba`) and section 6 is now filled with measured results. What keeps this packet open
is that **`HVST-v-2` reads `<status>pending</status>` at HEAD** and cannot be flipped: its instance is
INVALID on one annotated field, only the worker's serial may edit that file, and the worker cannot be
resumed (row `Z-S29`). **A packet that called itself complete over an order the record still shows as
pending would assert a terminal state that does not exist** -- the same defect this round was cut to clean
up, which is why it stays open rather than being tidied.

---

## 1. WHAT THE ROUND IS

Two cells, one serial chain, cut off the round-6 analysis (`ledger/ROUND_ANALYSIS.round6.md` @`37217d8053`)
enrichment items 1 and 2.

| cell | what | risk | state |
|---|---|---|---|
| `HVST-v-1` | disarm `Z-S28`: an EMPTY MAPPING reaches silver, publisher-neutral | LOCAL | **complete**, drained @`3dba19e7cb` |
| `HVST-v-2` | drain the 20 HELD sa rows, then capture, then measure | WORLD | **executing** |

## 2. ISSUER ACTS, in order, with their pins -- the invisible class

| # | act | pin |
|---|---|---|
| 1 | L5 decomposition v1.6 section 18 | `97af12ec2b` |
| 2 | 18e: round scoped from FOUR cells to TWO, `v-3`/`v-4` deferred | in `de200db5ff` |
| 3 | L6 ONE ISSUANCE, two orders | `de200db5ff` |
| 4 | **cell-id collision fixed** -- cut as `r-1`/`r-2`, renamed to `v-1`/`v-2` | `ba8d60d62a` |
| 5 | `v-2` AMENDMENT 1: AC2 widened to `--all-securities`, ceiling stated | `f4abae8b29` |
| 6 | `v-1` drain | `3dba19e7cb` |
| 7 | `v-1` AMENDMENT 1: AC3 ruled PASS, its clause rewritten, `Z-W21-S1` disarmed | `76ba64b079` |
| 8 | AC scripts relocated out of `.scratch/` into this lane's deliverables | `97e6a98178` |
| 9 | vendor ledger opened for the 02:17Z sa call | `52240c6676` |

## 3. THE ISSUER'S OWN DEFECTS THIS ROUND -- THREE, ALL THE SAME FAMILY

**Stated here because a packet that records only the round's successes is not a record of the issuer.**

1. **`v-2`'s `<MAIN_TREE>` token was used and not declared**, and AC4 carried `grader=` without
   `judgment="true"`. Both caught by `to-pipeline-gate` at the issuance, both fixed before landing.
2. ⛔ **THE CELL IDS COLLIDED WITH A PREVIOUS ROUND'S.** `HVST-r-1` is the timeline-spec cell whose BUILD gate
   the CTO had vacated two messages earlier. **The gate PASSED it**: *"1 owned cell and 3 criterion references
   RESOLVE against the decomposition (20 cell ids)"* -- true, and about the wrong object. A reference check
   answers *does this id exist*, never *is this id YOURS*. Found by accident when a fresh worktree listed two
   files matching `TO-HVST-r-1*`.
3. ⛔ **AC3's "named in the output" clause was UNSATISFIABLE WHEN WRITTEN.** `pytest -q` prints a nodeid only
   for a FAILING test, so a passing new test can never appear. The worker measured it (0 grep hits, tailed and
   untailed), refused to self-grade it, and routed the call to the issuer -- which is exactly right.

⭐ **ALL THREE ARE ONE FAMILY: a criterion or an id written against a surface the issuer had not exercised.**
Round 6's two defects (17g) were the same family. **The remedy that keeps working is not more review -- it is
printing the denominator before naming anything:** `ls task-orders/ | cut -d. -f1 | sort -u` for an id,
one dry invocation for a flag, one `--collect-only` for a suite.

## 4. A STRUCTURAL LIMIT MEASURED, NOT INFERRED -- AN ISSUER CANNOT REPAIR A WORKER'S EVIDENCE

`v-1`'s order sent the AC check scripts to `.scratch/r1/`, which the drain destroys. The attempt to relocate
them into `deliverables/0.9.0_WK_AMGT_HARVST~21/scripts/` was **REFUSED by owned-paths** on all four files:
lane `TREE_DELIVERABLES` permits exactly the serial named by the sub-folder (`ADHC_OWNPTH.004`), and
`2.0.0_SA_COO~Y` is not that serial.

**The refusal is CORRECT and it is structural: the owner is in the path.** `GIT_COMMIT_AUTHOR_OVERRIDE` would
have worked and was NOT used -- writing into another serial's folder is the precise sweep that rule prevents.
The artifact moved to a folder this lane owns, with provenance and 9 of 9 sha256 digests compared.

**CONSEQUENCE FOR EVERY FUTURE ORDER:** a criterion's script is part of its EVIDENCE, not its workspace, and
only the WORKER can put it in the worker's folder. `v-2`'s order was written with that correction in it.

## 5. `HVST-v-1` -- WHAT IT PROVED AND WHAT IT LEFT OPEN

**The fix** (`silver_from_bronze.py:292`, `_null_empty_mappings`): an empty dict becomes null at any depth; a
populated one is untouched. **Its only predicate is emptiness, so it is publisher-neutral by construction** --
not by a list of publishers, which is what would have rotted.

- **AC1** -- write RAISED before (`ArrowNotImplementedError`), wrote **20 of 20** rows after, `themes` now
  `null`. The BEFORE arm ran the pre-change bytes via `git show HEAD:<file>`, with an arm-provenance control
  printing `carries '_null_empty_mappings': False` / `True`.
- **AC2, the criterion that could have failed the cell** -- wsj's row set **BYTE-IDENTICAL** (same sha256 both
  arms), schema **IDENTICAL** across 25 of 25 fields, and a populated mapping still `struct<berkshire: string>`.
- **AC3** -- `+1` test, **zero regressions**, 162 collected (re-measured by the worker with `--collect-only`
  after catching its own arithmetic).

**LEFT OPEN, and carried to the round-7 analysis rather than closed:**
- `Z-W21-S2` **ARMED**: the graded suite is **already RED at HEAD** (3 failures), so "zero regressions" is
  measured against a red baseline; and one failure **changed its CAUSE between two runs at the same nodeid**
  (`KeyError 'bundle'` -> `FileExistsError [WinError 183]`) -- flapping, not stable. Outside this round's grant.
  **Not disarmed: an exposure closed on "nothing went wrong in my cell" is the ABSENT-vs-EXERCISED-AGAINST
  conflation.**
- `Z-W21-S3` INERT: the second held wsj page yields **ZERO** rows (its captured `searchResults` is an empty
  list), so the wsj control is 20 rows from ONE page, not 40 from two.
- **DECLARED EXCLUSION:** `article_rows` was NOT changed. An empty mapping in an ARTICLE payload still fails at
  the same parquet writer. **An open exposure on a second table, declared by the worker rather than silently
  widened.**

## 6. `HVST-v-2` -- COMPLETE AND DRAINED (`1a808524ba`). THE WORK SUCCEEDED; THE INSTANCE IS INVALID

- **AC1 PASS** -- the 20 HELD rows reached silver, **+20 (0 -> 20)**, uploader rc 0, `written_rows 20`,
  `remaining_pending 0`, **no vendor call**. `v-1`'s fix exercised on the same sa bytes that raised at 02:1xZ.
- **AC2 PASS** -- ONE capture. **4 vendor requests, all HTTP 200, `auth_refreshes: 0`**, no browser, clause 4
  never reached. sa listing_hit **20 -> 40**, bronze `news_listing` +1, silver article parts +2. Ledger row
  landed in the same commit. Attempted **8 of 89**, skipped-for-missing-symbol **0 of 8**, queried **1 of 8**,
  **cooldown-suppressed 7 of 8** -- job 1's `Timeout` cooled the publisher and cost the other seven.
- **AC3 PASS** (pure, `GOLD WRITE PERFORMED: none`, two runs byte-identical) -- population A, the **6**
  securities `build_daily` is invoked with: **0 of 6** sa spans, **0 of 1614** rows moved. Population B, the
  89-name universe: **1 of 89** spans (2026-07-15 to 2026-09-26), **74 of 23941** DENIED -> PARTIAL,
  `publishers_covered 1 of 5`, `COMPLETE` **0 times** in any moved row.
- **AC4 RECORDED, NOT GRADED** -- 40 of 40 sa rows censused; population A files **0 of 40**, population B
  **20 of 40**; the queried symbol corroborated by the row's own content links in **36 of 40**. The CVO
  grades it at L9. It is the round's ONLY judgment criterion, and it exists because round 6's L9 was VACUOUS
  at 0 of 8 against a control reading 1.

⛔ **THE INSTANCE IS INVALID (rc=1) AND THE ORDER STILL READS `pending` AT HEAD.** Two
`invocation-alignment` violations, neither of them the work: AC1's recorded `invocation` field is 342
characters where the command is 132, the remainder being the worker's own annotation, and the limb compares
the whole string; AC2 diverges on **one space**, because the limb builds `(\S+)` per placeholder and this
device's workspace path contains one. **I fixed AC2** (literal path, `<placeholders>NONE</placeholders>`)
and **AC3** (reverted a re-path I should not have made). AC1 needs one annotation moved to a field the limb
does not compare -- **authorized under five conditions (`7d5f8279a8`) and NOT YET DONE, because
`PROOF_OF_SPEC.schema.json` sets `additionalProperties: false` and permits no note field.** Row `Z-S29`.

⚠ **AND THE CVO's ROUND-7 COMPILE IS PARKED ON EXACTLY THAT FLIP.** `3.0.0_SA_CVO~Z` wound down and its
checkpoint parks three L8/L9s, one of them *AMGT_HARVST 7 on TO-HVST-v-2 reaching a terminal `<status>`*.
So the one unlanded field gates the round's compile, and whoever next holds that serial inherits it.

⭐ **WHAT CHANGED AFTER THE DRAIN, and it is why AC3's zero is no longer the end of the story:** `Z-W22-S3`
was the finding that the rows landed and the grade did not move -- `_listing_hit_security_match` matched a
security's ALIASES against a query written as a VENDOR SYMBOL, so `'Lenovo'` could never match `'LNVGY'`.
**That join is now fixed (`4cc54df506`)**, in the reader AND in the securities builder, because the
securities file carried `sa_symbol` on 0 of 191 rows and a listing row carries no `security_key` at all.
**The measured ceiling is 21 of 191 securities, and it is the JOIN KEY that caps it, not the symbol count:**
only 32 of 89 research folders carry a `bloomberg_ticker`, the sole key on both planes. Re-running AC3 over
the fixed reader is round 8's, not a retro-edit of this instance's recorded outputs.

## 7. WHAT IS CARDED AT ANDREW OUT OF THIS ROUND

1. **The bbg verification troubleshooting** he offered -- an OFFER OF AN ACT, untaken. The last movable
   publisher of the four, and `COMPLETE` needs all five.
2. **serp** -- CTO-ruled to a card, not a cell: `bright_data_serp` is imported by nothing but its own test
   across 75,455 files (a BUILD, not a run), and Bright Data is metered, making 92 names **SPEND**, which the
   egress term excludes BY NAME.
3. **The authenticated symbol-resolution pass** -- and this one carries a clock. The resolver's symbol source
   (`IDENTITY_SA_SYMBOL_DENSITY_PASS_20260913_Z.json`) reads 89 names, **18 resolved, 71
   `NOT_ASKED_vendor_refusal`**, having died on HTTP 403 against an endpoint its own provider line calls
   *"DIRECT, unauthenticated, NO VENDOR"*. Tonight supplies both things that pass lacked: the egress word and a
   **proven-valid** sa session. ⚠ **This corrects a claim this seat made to the CTO** -- that the identity gap
   was "untouched by" the word. It is not; it is the thing the word most plausibly moves.
4. **The 5 best-effort identities**, parked by his own instruction.
