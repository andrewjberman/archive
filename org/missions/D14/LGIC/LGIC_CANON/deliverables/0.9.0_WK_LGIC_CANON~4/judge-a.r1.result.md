# judge-a.r1.result -- LGIC_CANON.TO-CN-j-1 (cell CN-j-1, judge A), 0.9.0_WK_LGIC_CANON~4

**Worktree:** `.worktrees/wk-lgic-canon-1-4`, branch `wk-lgic-canon-1-4`, base `671925aecc77f15dfb33a1b15cfb966b0ae2c3ae`
(cut from CLOUD; `git rev-parse HEAD` read at start = the base; no commit of mine preceded the answer).
**Answer file:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-a.tsv`.
**The one document:** `infra/logic/02_DOCTRINE.md` v1.0 at the base (canon rule ids counted by the checker: 21).

## Verdicts (as filed in the answer file)

| row | verdict | decided by |
|---|---|---|
| A1 INGESTION | UNDETERMINED | R9, R18 (mechanism and bronze formats not measured; X1 is a DECLARED-EXCEPTION finding, less severe) |
| A2 BUCKET STRUCTURE | VIOLATES | R4, R5, R6, R7 (bronze in the product bucket; gold in opal-data-assets; cot/inf firm platinum in portal-v2) |
| A3 NAMING | VIOLATES | R1 (tier-first and scope-less keys against the N1 source-first grammar) |
| A4 COMPUTE | UNDETERMINED | R13 (the tier transition each compute runs is not stated; threshold deferred) |
| A5 FORMAT | VIOLATES | R11 (JSON under gold) |
| J-N1 `blackdiamond/49f/credentials` SECRET | CONFORMANT | R1; §3 N2, N3 secret grammar |
| J-N2 `opal-data-bd` S3_BUCKET | ALIAS | R1; §3 N5, N4, N3 bucket grammar |
| J-N3 `bd-49f-runner-role` IAM_ROLE | OUT-OF-PATTERN | R1; §3 N5, N3 (never a system: a firm), N4 |

## Criteria, output verbatim (each run from the worktree under `timeout 120`)

`J1-AC1` -- `python .../fixed_inputs/r1/check_canon_r1.py j1-axes` -- rc=0, denominator 5 of 5 axes
```
AXES: 5  JUDGED WITH A CANON RULE: 5  (rule ids in the canon: 21)
VERDICT: PASS-JA-AXES-JUDGED
```
`J1-AC2` -- `... check_canon_r1.py j1-naming` -- rc=0, denominator 3 of 3 cases
```
NAMING CASES: 3  GRADED WITH A CANON CITATION: 3
VERDICT: PASS-JA-CASES-GRADED
```
`J1-AC3` -- `... check_canon_r1.py j1-base` -- rc=0, denominator 1 of 1 base line
```
BASE: 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae  resolves to a commit: True
VERDICT: PASS-JA-BASE-STATED
```
These checks grade the answer's SHAPE (a verdict from the vocabulary and a canon citation per row). Whether the
verdicts are right is graded at CN-j-3 and L9, not here.

## Blindness statement

Read for the judgment: the canon, `CN_TREE_MDPF.md`, `CN_JUDGE_CASES.json` and this order only. From
`check_canon_r1.py` I read only its path constants (lines 21-46), `tsv()`, `canon_rules()`/`rule_ids()` (the
helpers the j1 subcommands call) and `judge_rows`/`cases`/`j_axes`/`j_naming`/`j_base` (lines 355-410). I read
neither `06_CONFORMANCE_LEDGER.md`, `CN_JUDGE_NAMING_KEY.json`, `judge-b.tsv`, any other `infra/logic/` document,
`GRADING_RULE.md` nor the PRD, and ran no `git log`/`git show` on them. Process files (the proof schema, the
surprise channel) were opened only after this answer was committed.

**The preloaded context, stated as the order asks.** Two lines in the preloaded context speak to `bd`: the
workspace CLAUDE.md (*"cot is a separate firm from bd"*) and the auto-memory (*"Legacy bd/inf/cot buckets are the
ACTIVE..."*). Both treat `bd` as a FIRM token, which leans toward the J-N2 and J-N3 answers. Neither states a
naming verdict, and both verdicts rest on the canon's own text: N5's ALIAS clause names `bd` as a registry alias
spelling (its example is the scope slot), N4 says *"the firm is 49financial"*, and N3/N5 say a firm in the system
slot is OUT-OF-PATTERN. CLAUDE.md rule 30 restates the canon's homes and adds nothing this tree turned on.
Nothing preloaded carried a verdict for this tree's axes.

## Where the canon left room for a second reader to differ (form only, not significance)

1. **J-N3 turns on what `bd` resolves to in the SYSTEM slot.** N4 names both readings (*"The vendor is
   blackdiamond; the firm is 49financial"*). N5 ties `bd` as an alias to the firm (scope-slot example). Read as
   the firm, the system slot holds a firm: OUT-OF-PATTERN (my verdict). Read as a vendor alias, the grammar holds:
   ALIAS with `blackdiamond-49f-runner-role`. Read as a token that resolves two ways: RAISE (N5 unplaceable). The
   canon has no sentence that picks between these.
2. **A3 against R1's census tag.** R1's census reads *"53 of 53 non-SmartX monolith planes CONFORMANT"*, but R5's
   census lists `opal-data-assets/gold/` and `portal/gold/` as monolith planes, and neither reads
   `{source}/{scope}/{tier}` under N1. The census vintage (`01_CENSUS.md`, 2026-09-12) comes before the
   source-first ruling (2026-09-13 ~03:2xZ), so I graded against the rule text, which §0 says governs, and not
   against the tag.
3. **A1 citation.** The deciding finding is UNDETERMINED; I cite the axis's two rules (R9, R18), not R20. X1's
   DECLARED-EXCEPTION rests on R20 and is named in the reason.
4. **P2's legacy root `code/` home.** R1's non-application excludes it, while N1 says such a key *"grades
   OUT-OF-PATTERN"*. That did not change A3, which P1/P4/P5/P6/P7 decide anyway.
