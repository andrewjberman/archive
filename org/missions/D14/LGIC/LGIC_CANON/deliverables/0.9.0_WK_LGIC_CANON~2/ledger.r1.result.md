# LGIC_CANON.TO-CN-l-1 -- the conformance ledger at v1.0 -- round 1 result

**Worker:** 0.9.0_WK_LGIC_CANON~2 (slot ~2, queue position 1), issued by 2.0.0_SA_COO~G.
**Branch:** wk-lgic-canon-1-2, cut from CLOUD @f95470f384. **Worktree:**
/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-2.
**This file is committed together with the artifacts it describes.** The proof instance beside it pins that commit.

## Bar and premises

- The branch is `wk-lgic-canon-1-2`, and the tree check printed `TREE-OK`: `org/`, `.tools/`, `infra/logic/06_CONFORMANCE_LEDGER.md`
  and the fixed inputs `deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/` are all present.
- **Premise 1: the ledger is v0.3, last touched @c9048873d1.** HELD.
  - `git log -- infra/logic/06_CONFORMANCE_LEDGER.md` lists five commits, newest first: c9048873d1 (4.0.0_SA_CRO),
    9cf4a274db (1.0.0_SA_CTO), 6dab0d76a7, a4cc0cb681 and 4faf061126.
  - The title line reads v0.3 at 6dab0d76a7, 9cf4a274db and c9048873d1.
- **Premise 2: section 7 says its counts were computed by hand.** HELD, at `:158-159` @c9048873d1.
- **Premise 3: X2 was GRANTED @9cf4a274db.** HELD. The commit's own message records Andrew-direct 2026-09-15 ~14:4xZ
  *"RECS APPROVED"* (card E2).
- **Premise 4: X3 and X5 name no decider.** HELD: the `acknowledged` cell of both reads `—`.
- **The negative control, on the unedited ledger at f95470f384, with the same four invocations:**

  | criterion | output |
  |---|---|
  | L1-AC1 | `FAIL-L1-RECOUNT-DISAGREES`, with 8 of 8 count rows differing and 'RE-DERIVED BY HAND' STILL PRINTED: True |
  | L1-AC2 | `FAIL-L1-DECIDER-UNNAMED`, with 1 of 3 naming a decider |
  | L1-AC3 | `FAIL-L1-CONDITION-UNOWNED`, with 0 of 3 |
  | L1-AC4 | `FAIL-L1-COLUMN-MISSING`, with 6 of 6 plane tables lacking the column |

## What was done

1. **`ledger_recount.py`** is in this folder, and its instrument is stated in its docstring and in the ledger's section 7.
   - It reads the ledger's markdown tables row by row and splits cells on `|` outside backticks. It checks every row's
     cell count against the row's header and compares its split with a plain `|` split. On v1.0 there were 0
     mismatches of either kind.
   - It classifies each plane row once, by a stated precedence: AWAITING > MIGRATE > RETIRE > DECLARED EXCEPTION >
     CONFORMANT > OUT OF SCOPE.
   - It derives WAITING from the register: a row is WAITING when it carries an AWAITING token or names an entry not
     GRANTED, and its decider is that entry's `decider:`.
   - It prints the required SECTION, TOTAL, DECIDED and WAITING lines, plus ROW, REGISTER and CHECK evidence lines.
     It exits 1 on any disagreement.
2. **The ledger is now v1.0** (`infra/logic/06_CONFORMANCE_LEDGER.md`).
   - (a) Section 7 carries the script's counts, and its instrument and denominator are stated. The denominator is 68
     plane rows (section 1 28, section 2 25, section 3 7, section 4 6, section 5 2) and 7 register entries. The by-hand
     sentence is gone.
     - Corrected: CONFORMANT 25 -> 21, MIGRATE (home) 21 -> 23, MIGRATE (format only) 3 -> 1, and AWAITING a word
       0 -> 3. The three `opal-data-etfs` rows already read "until then AWAITING", "as X3" and "AWAITING X5".
     - DECLARED EXCEPTION is split into its plane row (1) and the register's states (5 GRANTED, 2 OWED).
     - OUT OF SCOPE goes from "2 classes" to 2 rows.
     - The SmartX total goes from 12,432 to 12,443 (11 + 7,066 + 5,366). v0.3's figure is the account and allocation
       trees alone.
     - Reproduced unchanged: MIGRATE (grammar) 4 and RETIRE 13.
   - (b) **Deciders:**
     - X2 names its acknowledgement, plus `decider: Andrew — decided, recorded @9cf4a274db`.
     - X3 and X5 each carry `decider: Andrew`. The ground is R20, `02_DOCTRINE.md` :313-317: *"Every exception is
       sovereign-acknowledged"*, with its authority, Andrew-direct 2026-08-25, *"I will acknowledge what those are"*.
   - (c) **Every CONDITIONAL entry** (X3, X5, X7: 3 of 7 register rows) carries a `condition:` and an `owner:`.
     - X3 and X5: owner Andrew.
     - X7: owner 1.0.0_SA_CTO, MDPF_CANON's lead per `org/missions/D8/MDPF/MDPF_CANON/project.json` `leads.cto`, where
       `leads.coo` is null.
   - (d) Each of the five plane tables gains a `decided` column: 65 DECIDED and 3 `WAITING (Andrew)`, the etfs silver,
     gold and platinum rows.
     - Those cells were written by a one-shot edit that names the three etfs rows literally
       (`.scratch/add_decided_column.py`, not committed). They were NOT produced by the recount's derivation, so the
       recount re-derives the column instead of repeating it.
   - (e) The header reads v1.0, and the new section 9 CHANGE LOG carries the v1.0 entry.
   - **No plane's disposition text changed.** Every edit to sections 1-5 is the added column. The section 6 edits are the
     decider, condition and owner clauses. Sections 7, 8 and 9 are counts, qualifiers and the log.

## Acceptance (run after the edits, in the worktree, verbatim as the order names them)

`cd /c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-canon-1-2 && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py <sub>`

| id | sub | deciding output (verbatim) | rc | denominator |
|---|---|---|---|---|
| L1-AC1 | l1-recount | `script rc: 0  SECTION LINES: 10  COUNT ROWS COMPARED: 14  DIFFERING: 0  'RE-DERIVED BY HAND' STILL PRINTED: False` / `VERDICT: PASS-L1-RECOUNT-AGREES` | 0 | 14 of 14 section-7 count rows agree; 10 of 10 sections print a SECTION line |
| L1-AC2 | l1-deciders | `ENTRIES X2, X3, X5: 3 found  NAMING A DECIDER: 3` / `VERDICT: PASS-L1-DECIDERS-NAMED` | 0 | 3 of 3 named entries |
| L1-AC3 | l1-conditional | `CONDITIONAL ENTRIES: 3  WITH CONDITION AND OWNER: 3` / `VERDICT: PASS-L1-CONDITIONS-OWNED` | 0 | 3 of 3 CONDITIONAL entries (of 7 register rows) |
| L1-AC4 | l1-column | `PLANE TABLES: 5  WITHOUT A 'decided' COLUMN: 0  BAD CELLS: 0  LEDGER DECIDED/WAITING: 65/3  SCRIPT: 65/3` / `VERDICT: PASS-L1-COLUMN-REDERIVED` | 0 | 5 of 5 plane tables; 68 of 68 cells valid |
| L1-J1 | (judgment) | RECORDED, NO VERDICT. The 3 rows that wait read `WAITING (Andrew)` in their `decided` cell and AWAITING in section 7; the register names each OWED entry's decider, condition and owner; section 8 states that DECIDED does not mean moved. Graded at L9 by 3.0.0_SA_CVO. | -- | 68 plane rows, 3 WAITING |

The recount script's own run: `python org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~2/ledger_recount.py`
rc=0. Its closing lines:

```
TOTAL CONFORMANT: 21
TOTAL MIGRATE (home): 23
TOTAL MIGRATE (format only): 1
TOTAL MIGRATE (grammar): 4
TOTAL RETIRE: 13
TOTAL DECLARED EXCEPTION: 1
TOTAL AWAITING a word: 3
TOTAL OUT OF SCOPE: 2
TOTAL PLANE ROWS (the denominator): 68
TOTAL GRANTED: 5
TOTAL OWED: 2
TOTAL REGISTER ENTRIES (the denominator): 7
TOTAL DECIDED: 65
TOTAL WAITING: 3
SMARTX ENTITY-TREE PLANES: 12443 (3 rows: 11 + 7066 + 5366)
DECIDED: 65
WAITING: 3
DENOMINATOR: 68 plane rows in 5 plane tables; 7 register entries; decided cells disagreeing: 0; plane tables without a 'decided' column: 0
RECOUNT: OK
```

## Controls

- **Mutant.** The recount was run with `--ledger` on a copy with two planted defects: `opal-data-etfs/platinum/`'s
  decided cell changed to DECIDED, and section 7's RETIRE changed to 12. It exited rc=1 with
  `PROBLEM: line 105: decided cell 'DECIDED', derived 'WAITING (Andrew)'`,
  `PROBLEM: section 7 'RETIRE': ledger 12, script 13` and `RECOUNT: MISMATCH 2`. Both planted defects were caught.
- **Determinism.** Two runs of the recount on the same bytes gave byte-identical output (`cmp`: 119 lines,
  12,238 bytes).
- **Commit gate** on the script: `OK: pre-commit gate clean for 1 of 1 file(s)`, rc=0.

## Surprise rows (INVESTIGATION_v1.md, both OBSERVATION and INERT)

- **LGIC_CANON-W2-S1.** The checker's l1-column selects plane tables by a header cell of exactly `disposition`, and
  section 7's count table had one. Section 7's first column now reads `disposition class`.
- **LGIC_CANON-W2-S2.** The ledger had no change log for clause 2e to update. Section 9 is added.

## Not done, and why

- **Choosing a branch where a disposition offers two** (`code/bronze/` "or RETIRE if orphaned", `opal-runner-shared`
  "RETIRE or move", `opal-data-inf` backups "or `_backup/` root"). Both branches of each take the plane out of its
  non-conforming state, so the row is DECIDED on conformance. The choice between branches is the migration's MAP step
  (R19), and the new section 8 qualifier states this.
- **Moving anything.** DEC-9 forbids it: no data, trigger, policy, AWS or Terraform act was taken.
- **Push, merge, rebase.** Forbidden by the order. The COO drains the branch.
