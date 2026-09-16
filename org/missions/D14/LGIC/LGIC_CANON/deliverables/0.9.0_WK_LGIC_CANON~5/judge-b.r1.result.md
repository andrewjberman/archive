# LGIC_CANON.TO-CN-j-2 -- result (judge B, cell CN-j-2, round 1)

**Worker:** 0.9.0_WK_LGIC_CANON~5 · **Worktree:** `.worktrees/wk-lgic-canon-1-5`, branch `wk-lgic-canon-1-5`, base
`671925aecc77f15dfb33a1b15cfb966b0ae2c3ae` (CLOUD @671925aecc; canon v1.0 at that base).
**Answer file:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/judge-b.tsv` @98ed3177ff. It was
committed alone, before this worker read anything outside the order's reads (the surprise channel, the row
schema), so the answer is fixed by that hash.

## 1. The verdicts (copied from the answer file @98ed3177ff)

| id | verdict | deciding rule(s) | why, in short |
|---|---|---|---|
| A1 INGESTION | UNDETERMINED | R9, R20 | the arrival mechanism and P1's bronze format are not measured, so R9 cannot be decided; the one measured departure (the Orion JWT read from opal-data-inf) is X1, GRANTED, so DECLARED-EXCEPTION under R20; UNDETERMINED ranks above it |
| A2 BUCKET STRUCTURE | VIOLATES | R4, R5, R6, R7 | P1 bronze in opal-data-mdpf (R4); P4/P5 gold in opal-data-assets (R5); P6's cottonwood and inflection firm slices in opal-data-portal-v2 (R6/R7, MANDATORY), with X7 covering only 49financial category-views.json; P7 global is X2; P2 code conforms (R16) |
| A3 NAMING | VIOLATES | R1 | source-first in every bucket: P1 `mdpf/bronze/` has no scope segment; P4 `gold/mdpf/`, P6/P7 `platinum/mdpf/...` are tier-first; P5 `portal/gold/` has no scope; P2's root `code/` falls under R1's legacy non-application; X1/X2/X7 are A1/A2 entries only |
| A4 COMPUTE | UNDETERMINED | R13 | a LAMBDA and an EC2_INSTANCE are live, but the tree does not measure which tier transition each runs, and R13's heavy threshold is deferred |
| A5 FORMAT | VIOLATES | R11 | P4 (502) and P5 (409) JSON gold objects; platinum JSON conforms (R12); bronze format unmeasured (R9) |
| J-N1 `blackdiamond/49f/credentials` SECRET | CONFORMANT | R1; section 3 N2 and N3 (secret grammar) | {system}/{scope}/{purpose}: vendor system of its own integration credential; 49f is the SHORT form the secret slot takes; `credentials` is a named purpose kind |
| J-N2 `opal-data-bd` S3_BUCKET | ALIAS | R1; section 3 N5 with N4 and the bucket grammar | the bucket grammar holds, the scope slot carries bd, which N5 names as a registry alias spelling; canonical_form `opal-data-49financial` (LONG) |
| J-N3 `bd-49f-runner-role` IAM_ROLE | OUT-OF-PATTERN | R1; section 3 N3 (never a system: a firm) and N5 | the canon's only resolution of bd is as the firm's alias, and a firm in the system slot fails the grammar (N5) |

Severity rule applied as the order states it: VIOLATES, UNDETERMINED, DECLARED-EXCEPTION, DEPARTS-RECOMMENDED, CONFORMS.

## 2. The criteria (each run as `cd <WS> && timeout 120 python .../check_canon_r1.py <sub>`)

| criterion | baseline, file absent | at the answer file (98ed3177ff bytes) | doctored copy | restored |
|---|---|---|---|---|
| J2-AC1 `j2-axes` | `VERDICT: FAIL-JB-AXES-ABSENT` | `AXES: 5  JUDGED WITH A CANON RULE: 5  (rule ids in the canon: 21)` / `VERDICT: PASS-JB-AXES-JUDGED` rc=0 | A3 citing R99: `FAIL-JB-AXES-UNJUDGED` (4 of 5) | PASS |
| J2-AC2 `j2-naming` | `VERDICT: FAIL-JB-CASES-ABSENT` | `NAMING CASES: 3  GRADED WITH A CANON CITATION: 3` / `VERDICT: PASS-JB-CASES-GRADED` rc=0 | J-N2 citing `N5 ALIAS` only: `FAIL-JB-CASES-UNGRADED` (2 of 3) | PASS |
| J2-AC3 `j2-base` | `VERDICT: FAIL-JB-BASE-MISSING` | `BASE: 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae  resolves to a commit: True` / `VERDICT: PASS-JB-BASE-STATED` rc=0 | base `deadbeef00deadbeef00`: `FAIL-JB-BASE-MISSING` | PASS |

The doctored copy was written in place and restored from `.scratch/judge-b.orig.tsv`; `cmp` read the two files
identical before the restored run. The checker's exit code is 0 on every run, FAIL included, so the VERDICT line
decides, never the rc.

## 3. Blindness, and what this worker read

- **Read for the judgment:** `infra/logic/02_DOCTRINE.md`, `CN_TREE_MDPF.md`, `CN_JUDGE_CASES.json`, the task order.
- **Read for the mechanics, never for a key:** `check_canon_r1.py` lines 21-46 (path constants and the two verdict
  vocabularies), 97-143 (`tsv`, `canon_rules`, `rule_ids`, which the j2 subcommands call), 355-410 (`judge_rows`,
  `cases`, `j_axes`, `j_naming`, `j_base`), and a listing of its function names; `org/standards/PROOF_OF_SPEC.schema.json`;
  `org/surprise_channel/schemas/investigation_item.schema.json`.
- **Read outside the order's list, disclosed:** the sibling proof instance
  `deliverables/0.9.0_WK_LGIC_CANON~1/LGIC_CANON.TO-CN-k-1.canon.proof_of_spec.json`, for its shape only. It is the
  canon writer's instance and carries no verdict on this tree or these names.
- **Read after the answer was committed (@98ed3177ff):** the project channel `INVESTIGATION_v1.md`. Its row
  LGIC_CANON-S2 cites ledger lines for MDPF (MIGRATE rows, X1 GRANTED). It could not shape the answer, which was
  already fixed.
- **Not read:** `06_CONFORMANCE_LEDGER.md`, `CN_JUDGE_NAMING_KEY.json`, `judge-a.tsv` (absent at the base: the
  `exercises/` folder held `naming-a.tsv` and `naming-b.tsv` only), any other `infra/logic/` document,
  `GRADING_RULE.md`, the PRD, and no `git log`/`git show` of any of them.
- **The preloaded context.** No preloaded text carried a verdict on this tree or on these three names. Two items
  are disclosed as possible influences:
  - The workspace CLAUDE.md Rule 13 writes *"cot is a separate firm from bd"*, using `bd` as a firm's name. That
    points the same way as this worker's J-N3 reading (bd as the firm's alias). The cited basis is the canon's N5
    example and N4, not that line.
  - The worktree CLAUDE.md's Rule 30 summarises the tier homes (bronze and silver in `opal-data-assets`,
    firm-attributable gold and platinum in the firm bucket). That agrees with the canon's R4-R7, which are the
    rules cited.

## 4. For the comparison (CN-j-3) and L9: where a second reader could fairly differ

- **A1.** DECLARED-EXCEPTION (X1, R20) is the other reading if a judge treats "mechanism not measured" as no
  finding rather than as an UNDETERMINED one. The order ranks UNDETERMINED above DECLARED-EXCEPTION, and R9 cannot
  be decided for P1, so this worker wrote UNDETERMINED.
- **A2.** R14 is not in the rule ids. It is what makes the firm-attributable cells MANDATORY rather than
  RECOMMENDED; R7 states the same MANDATORY directly for the firm slices.
- **A3.** R1's census tag reads the monolith's non-SmartX planes CONFORMANT, while R1's text (source-first) read
  against R5's census says P4/P5 are not. This worker graded by the rule text. That is row LGIC_CANON-W5-S1.
- **J-N2.** RAISE would follow only if no registry row resolved bd. The canon's N5 names bd as a registry alias
  spelling, so ALIAS.
- **J-N3.** If bd in the system slot is read as the vendor's alias (N4: *"The vendor is blackdiamond"*), the grammar
  holds and the verdict is ALIAS, canonical `blackdiamond-49f-runner-role`. This worker read bd as the firm, on N5's
  own example, which places bd in a scope slot as a firm spelling.

## 5. Rows filed

- `LGIC_CANON-W5-S1` -- OBSERVATION, INERT: R1's census tag and R1's text give two answers on A3 for the monolith's
  tier-first gold planes.
