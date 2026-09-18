# judge-g.r3.result -- LGIC_CANON.TO-CN-j-9-r3 (cell CN-j-9, judge G), 0.9.0_WK_LGIC_CANON~4

## Blindness (A-22)

Before reading `CN_TREE_R3.md` or `infra/logic/02_DOCTRINE.md`, this worker wrote and committed
`org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r3/judge-g.base` with exactly one line,
`base_commit: 1e2a9c931b2e46adc0518ac2c16a2f487619b614` -- the worktree's HEAD as spawned, before
`org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r3/` even existed as a directory. `j9-blind`
confirms: the base is an ancestor of HEAD, the canon is visible at base (positive control), and 0 of 3
sibling artifacts (judge-f.tsv, judge-h.tsv, judge-compare-r3.md) are present at base. No other judge's
order, output or worktree was opened at any point in this session.

## The tree judged

`CN_TREE_R3.md` -- the 49FINANCIAL family (two Schwab masters, blackdiamond monolith + legacy long/short
scope forms, the legacy `opal-data-bd` bucket, the ruled firm bucket `opal-data-49financial`, the
`opal-data-etfs` general-data product bucket, and one shared-serving-bucket plane), 23 planes, judged from
`infra/logic/02_DOCTRINE.md` v1.1 alone, as the tree names it.

## Method, stated once

Each plane is judged on all five axes (A1 INGESTION, A2 BUCKET STRUCTURE, A3 NAMING, A4 COMPUTE, A5 FORMAT)
per `02_DOCTRINE.md` s.2's axis table, citing the DECIDING rule per THE CITATION RULE. Recurring reads
applied uniformly, disclosed here rather than repeated per row:

- **A1 (ingestion mechanism)**: the tree carries no ingestion-mechanism fact for any plane, so A1 reads
  UNDETERMINED citing R18, except the one plane the canon's own R18 census names explicitly as a dual-write
  twin (`opal-data-assets/schwab/08335338/gold/`, 2,108 json / 2,108 parquet), which reads VIOLATES.
- **A4 (compute)**: R13's own census line states compute is UNMEASURED by the plane census; no row carries
  a Lambda/EC2 fact, so A4 reads UNDETERMINED, citing R13, on all 23 rows.
- **R21 placement**: the axis table (s.2) does not list R21 under any of A1-A5. It is placed under A3
  NAMING here by analogy to R17 (the canon's own adjacent HYGIENE rule, also A3, for the identical
  "wrong content sitting inside a tier plane" shape) -- disclosed rather than silently assumed.
- **Legacy-bucket rows (`opal-data-bd/*`)**: per R-9(iii) coordinate C3 (in the R6 block, extended here to
  R5 the same way the canon's own text extends it: "opal-data-inf/gold/ (R5)... sit on the RETIRING legacy
  plane"), the legacy short-form bucket is NOT the ruled firm bucket. Per R19's coordinate C4, an in-flight
  migration with no evidenced never-widen sign-off reads VIOLATES under R20's default, never
  DECLARED-EXCEPTION and never UNDETERMINED. Applied to every `opal-data-bd/*` row.
- **Direct census matches**: where the canon's own per-rule census line names the exact plane or an exact
  object count matching the tree's stated facts (R4's 174/7,989 bd bronze/silver; R9's 242-parquet bd/smartx
  bronze; R10's 29-of-58 blackdiamond/49financial silver; R5's 56d blackdiamond/49f gold; R6's 19-object
  advi/49financial platinum; R18's 2,108/2,108 schwab gold twin), that citation is treated as the strongest
  available evidence and is named in the row's `why`.

## Verdicts

See `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r3/judge-g.tsv` (23 rows, committed
2304cd40f894b213817afcab3b47a21633dcc3a4) for the full table: five axis verdicts, every axis's citing
rule(s), the single most-severe finding (`worst_verdict`), its one rule (`worst_rule`), the six-rule reach,
and a one-sentence `why` per row.

Overall reading per plane (most severe axis verdict):

| plane | overall | worst rule |
|---|---|---|
| schwab/08242234/bronze/ | UNDETERMINED | R18 |
| schwab/08242234/silver/ | UNDETERMINED | R18 |
| schwab/08335338/bronze/ | UNDETERMINED | R18 |
| schwab/08335338/silver/ | UNDETERMINED | R18 |
| schwab/08335338/gold/ | VIOLATES | R18 (dual-write twin) |
| blackdiamond/49f/bronze/ | VIOLATES | R1 (short-form scope) |
| blackdiamond/49f/silver/ | VIOLATES | R1 (short-form scope) |
| blackdiamond/49f/gold/ | VIOLATES | R5 (gold in monolith, VIOLATED-DEAD) |
| blackdiamond/49financial/bronze/ | UNDETERMINED | R18 |
| blackdiamond/49financial/silver/ | VIOLATES | R10 (29 of 58 json) |
| blackdiamond/49financial/bronze_legacy/ | VIOLATES | R1 (invalid tier segment) |
| blackdiamond/49financial/silver_legacy/ | VIOLATES | R1 (invalid tier segment) |
| opal-data-bd/platinum/ | VIOLATES | R6 (legacy bucket, in-flight) |
| opal-data-bd/gold/ | VIOLATES | R5 (legacy bucket, in-flight) |
| opal-data-bd/silver/ | VIOLATES | R4 (silver outside assets) |
| opal-data-bd/bronze/ | VIOLATES | R4 (bronze outside assets) |
| opal-data-bd/smartx/bronze/ | VIOLATES | R9 (100% parquet under bronze) |
| opal-data-bd/code/ | VIOLATES | R1 ('bd' alias) |
| opal-data-49financial/gold/ | VIOLATES | R1 (source-first supersession) |
| opal-data-etfs/silver/ | UNDETERMINED | R18 |
| opal-data-etfs/gold/ | VIOLATES | R11 (32 of 60 json) |
| opal-data-etfs/platinum/ | UNDETERMINED | R12 (canon's own open ledger question) |
| opal-data-portal-v2/platinum/advi/49financial/ | VIOLATES | R6 (VIOLATED-DEAD, wrong bucket) |

## The three mechanical criteria

- **J9R3-AC1** (`j9-rows`): `ROWS 23 over a tree of 23 plane(s); same set, no duplicates: True` /
  `row defects, denominator 23: 0 []` / `VERDICT: PASS-J9-ROWS-WELLFORMED`
- **J9R3-AC2** (`j9-reach`): `REACHED 5 of 6: ['R3', 'R8', 'R14', 'R19', 'R21']` /
  `NOT REACHED 1 of 6: ['R15']` / `VERDICT: PASS-J9-REACH-OVER-SIX`
- **J9R3-AC3** (`j9-blind`): base ancestor True, positive control True, 0 of 3 siblings present, canon at
  base carries v1.1 True / `VERDICT: PASS-J9-BLIND-AT-BASE`

A mutant control was additionally run on `j9-rows` (doctoring row 1's A2 cell to an off-vocabulary token,
in place, then restoring byte-identically): the checker FAILED as expected, naming the exact row and
defect, then the restored file re-passed cleanly. See the proof-of-spec instance's `controls.mutant`.

## Where the canon left room for a second reader to differ (for J9R3-AC4, 3.0.0_SA_CVO at L9)

1. **R21's axis placement (A3 vs A2).** The axis table does not list R21 under any of A1-A5; this worker
   placed it under A3 by analogy to R17. A2 (bucket/tier structure) is an equally defensible placement.
2. **Tie-breaking among co-severe VIOLATES axes.** Several rows carry two or three VIOLATES axes at once
   (e.g. `opal-data-bd/gold/`: A2, A3, A5 all VIOLATES). `worst_rule` was chosen by which axis's departure
   affects the largest share of the plane's objects, stated in each row's `why`; CN_SEVERITY.md does not
   order ties, so this choice is this worker's own, not the canon's.
3. **`opal-data-etfs/platinum/`'s A2 read as DECLARED-EXCEPTION.** This rests on X3 (named in
   `CN_SEVEN_RULES.json`'s R8 note) covering all three etfs tiers including platinum; the register entry's
   own text was not independently re-read in this worktree, only its citation in the fixed inputs.
4. **The legacy-bucket VIOLATES read (R-9(iii) C3 extended from platinum/R6 to gold/R5).** The canon's own
   coordinate note names this extension for `opal-data-inf`; this worker applied the identical reasoning to
   `opal-data-bd` by analogy. A reader could instead treat R5's plain census text ("Firm/product bucket
   golds CONFORMANT on home") as controlling for `opal-data-bd/gold/` specifically, absent an explicit
   `opal-data-bd` citation in R5's own coordinate note.
