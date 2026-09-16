# judge-c.r2.result -- LGIC_CANON.CN-j-4-r2 (cell CN-j-4, judge C), 0.9.0_WK_LGIC_CANON~4

**Worktree:** `.worktrees/wk-lgic-canon-2-4`, branch `wk-lgic-canon-2-4`, cut from CLOUD at `49b4a5b74a`.
**Answer file:** `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/r2/judge-c.tsv`, committed `95d6a4513e`.
**The one document:** `infra/logic/02_DOCTRINE.md` v1.1 (CN-k-2 landed, `31392ef996`), read in full (627 lines).
**Fixed inputs read in full:** `CN_TREE_INFLECTION.md` (81 lines), `CN_SEVERITY.md` (51 lines),
`CN_SEVEN_RULES.json` (55 lines).

## Verdicts (as filed in the answer file; full per-axis citations and `why` are in the TSV)

Overall reading = the most severe verdict across a plane's five axes (CN_SEVERITY.md's severity order:
`CONFORMS < DECLARED-EXCEPTION < DEPARTS-RECOMMENDED < UNDETERMINED < VIOLATES`).

| plane | A1 | A2 | A3 | A4 | A5 | overall | reach |
|---|---|---|---|---|---|---|---|
| `orion/inflection/bronze/` | CONFORMS | CONFORMS | CONFORMS | UNDETERMINED | CONFORMS | UNDETERMINED | R14 |
| `orion/inflection/silver/` | UNDETERMINED | CONFORMS | CONFORMS | UNDETERMINED | UNDETERMINED | UNDETERMINED | R14 |
| `eclipse/inflection/bronze/` | CONFORMS | CONFORMS | VIOLATES | UNDETERMINED | CONFORMS | VIOLATES | R14 |
| `eclipse/inflection/silver/` | UNDETERMINED | CONFORMS | CONFORMS | UNDETERMINED | UNDETERMINED | UNDETERMINED | R14 |
| `opal-data-inf/platinum/` | CONFORMS | VIOLATES | UNDETERMINED | UNDETERMINED | CONFORMS | VIOLATES | R14, R19 |
| `opal-data-inf/gold/` | CONFORMS | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | VIOLATES | R14, R19 |
| `opal-data-inf/silver/` | VIOLATES | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | VIOLATES | R14, R19 |
| `opal-data-inf/bronze/` | VIOLATES | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | VIOLATES | R14, R19 |
| `opal-data-inf/backup/gold_canonical_PRE_REDERIVE_.../` | UNDETERMINED | UNDETERMINED | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | R17 |
| `opal-data-inf/_pre_rebuild_backup/.../silver/` | UNDETERMINED | UNDETERMINED | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | R17 |
| `opal-data-inf/_toolprobe_scratch/` | UNDETERMINED | UNDETERMINED | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | R17 |
| `opal-data-inf/backup/pre_pullheal_.../code/gold/` | UNDETERMINED | UNDETERMINED | VIOLATES | UNDETERMINED | UNDETERMINED | VIOLATES | R17 |
| `opal-data-inf/code/{bronze,silver,gold}` | UNDETERMINED | CONFORMS | CONFORMS | UNDETERMINED | UNDETERMINED | UNDETERMINED | (none) |

Seven-rule reach, union across all 13 rows: **REACHED (3 of 7)** -- R14, R17, R19. **NOT REACHED (4 of 7)**
-- R3, R8, R15, R21 (matches the checker's own `j4-reach` output below).

## Criteria, output verbatim (each run from the worktree under `timeout 120`, HEAD `95d6a4513e`)

`J4-AC1` -- `python .../fixed_inputs/r2/check_canon_r2.py j4-axes` -- rc=0, denominator 13 of 13 rows
```
judge C rows, denominator 13; rows not carrying all 5 axis verdicts: 0
VERDICT: PASS-J4-EVERY-AXIS-JUDGED
```
`J4-AC2` -- `... check_canon_r2.py j4-cites` -- rc=0, denominator 13 of 13 rows
```
judge C rows, denominator 13; rows citing no canon rule: 0
VERDICT: PASS-J4-EVERY-VERDICT-CITES
```
`J4-AC3` -- `... check_canon_r2.py j4-reach` -- rc=0, denominator 7 of 7 rules
```
A-13's seven rules, denominator 7
  REACHED     (3): ['R14', 'R17', 'R19']
  NOT REACHED (4): ['R3', 'R8', 'R15', 'R21']
the reach is PRINTED, which is what A-13 asks for; a non-empty NOT REACHED is not a failure
VERDICT: PASS-J4-REACH-PRINTED
```
These checks grade the answer's SHAPE (all five axes carry a verdict, every row cites at least one canon
rule, the seven-rule reach is printed). Whether the verdicts are right, and whether each rests on the rule
it cites, is `J4-J1` at L9 (`3.0.0_SA_CVO`), not here.

## Method, stated once (applied consistently across all 13 rows)

- **The canon's own CENSUS TAGS are part of the rule text, not a second document.** Where a rule's
  `census:` bullet names the exact object/path in the tree I am judging (R4's and R9's and R10's and
  R17's census enumerate `opal-data-inf/bronze|silver|platinum`, the exact `_backup`/`_pre_rebuild_backup`/
  `_toolprobe_scratch` paths), I read that as the canon's own finding on this plane and cited it directly
  -- four of the thirteen rows match a rule's own census enumeration verbatim (rows `opal-data-inf/silver/`,
  `opal-data-inf/bronze/`, and the three census-named backup paths). Where a rule's census offers a BLANKET
  clearance not tied to a specific path (R9's "Monolith bronze CONFORMANT... the bucket-policy deny is LIVE
  on assets only"), I extended it to the monolith bronze planes in this tree (rows 1, 3) because the
  clearance's own stated mechanism (a bucket-policy deny) covers the whole monolith bronze plane, not a named
  subset. R10 (silver format) carries NO equivalent blanket clearance -- only named violators plus "Completeness
  and trigger UNMEASURED by the census" -- so I did NOT extend a silver blanket clearance to rows 2 and 4;
  their A5 verdicts are UNDETERMINED for want of plane-specific evidence, not CONFORMS by analogy to R9.
- **UNDETERMINED is used only where the facts, not my effort, run out.** Nine of thirteen rows carry at
  least one UNDETERMINED, and A4 (compute) is UNDETERMINED on all thirteen except `opal-data-inf/gold/`,
  where R13's own non-application clause names the existing Inflection EC2 gold runner UNCLASSIFIED pending
  Andrew's deferred heavy-threshold ruling (`ANDREW_DIRECT_20260826_1810Z` call 4) -- a stronger, still-
  UNDETERMINED-shaped citation, not a CONFORMS I have no basis for. Two UNDETERMINED axes are, on their own
  terms, a hole in the canon rather than a parked hard case: A4 for `opal-data-inf/platinum/` (neither R13,
  which is silver-to-gold only, nor R22, a definitional rule with no plane census, names a compute rule for
  gold-to-platinum production), and A1/A4/A5 for the four backup/scratch/probe rows and for the code-home row
  (rows 9-13), where the ingestion, compute and data-format axes have no test that reaches non-tier material
  in the first place.
- **A stated-but-not-re-measured tree fact is still a fact I judge against.** `CN_TREE_INFLECTION.md` names
  the 108 date-named table-level prefixes inside `eclipse/inflection/bronze/` as "a naming sub-finding [the
  ledger] did not re-measure" and states plainly "They are part of the tree you are judging." I read that as
  an instruction to grade the finding, not to discount it for lack of a fresh sweep: a bare date occupying
  R1's `{table}` grammar slot (where N1 reserves dates for the `{partition}` slot only, as `date=YYYY-MM-DD`)
  is OUT-OF-PATTERN, undeclared, so A3 reads VIOLATES.
- **A live dual-write reads on the DUPLICATED plane, not on the correct twin.** `opal-data-inf/silver/`
  carries the same newest date (09-12) as its canonical destination
  `opal-data-assets/{orion,eclipse}/inflection/silver/`, which the tree states "already exist[s]; LIVE" --
  two homes serving the same logical silver concurrently, with no register entry or never-widen sign-off
  named anywhere in the tree or the canon for this pair. I read this as R18's shadow-path/dual-write test
  failing and cited it on the LEGACY plane (A1 VIOLATES, `opal-data-inf/silver/`), not on the canonical
  monolith silver planes (rows `orion/inflection/silver/`, `eclipse/inflection/silver/`), which are doing
  what R4/R19 ask of the correct target; their own A1 stays UNDETERMINED for lack of plane-specific
  ingestion-mechanism evidence, not VIOLATES by association with the plane duplicating them. I extended the
  same reasoning to `opal-data-inf/bronze/` (A1 VIOLATES via R9's own "coerces schema at ingest" finding,
  which is itself an ingestion-mechanism failure, not only a format one), since its canonical bronze twins
  carry the identical 09-12 date.
- **Ledger dispositions (MIGRATE/RETIRE/CONFORMANT) are excluded by the order's own instruction** ("not
  the ledger's dispositions, which are another seat's verdicts on the same planes"). An active, ruled R19
  migration does not itself excuse a source plane from an axis verdict under R4-R11 -- R19 classifies a
  migration as its own PROJECT ("the canon classifies... it never moves"), it does not retroactively convert
  an undeclared bucket/format departure into something other than VIOLATES absent an actual register entry.
  Every VIOLATES verdict on a legacy `opal-data-inf` row stands on its own axis rule, with R19 named
  separately in `reach` as the process context, never as the deciding citation for A2 or A5.

## Blindness statement

I did not open `judge-d.tsv`, `judge-e.tsv`, `judge-compare-r2.md`, `06_CONFORMANCE_LEDGER.md`, or any
other judge's task order or deliverable folder; `git ls-tree` over `exercises/r2/` at CLOUD was empty before
this order started and no other judge's output exists in this worktree. I read `check_canon_r2.py` only for
its `j_axes`/`j_cites`/`j_reach` bodies (lines 274-313) and its path constants, to confirm the exact column
positions and matching rules (word-boundary `\bR\d+\b`, and that `j4-reach`'s denominator is the union across
all rows, not a per-row count) -- not to shape a verdict toward a PASS string.

**Preloaded context.** The workspace CLAUDE.md names LGIC generally (Rule 30: tier homes and tenancy come
from `infra/logic/02_DOCTRINE.md`) and the auto-memory notes "Legacy bd/inf/cot buckets are the ACTIVE
channels until the D14 full-name migration" -- which is exactly the R19-migration context this tree presents
(the legacy `opal-data-inf` bucket, active, mid-migration to `opal-data-inflection`). Neither source states an
axis verdict for any of these 13 planes; both are consistent with, and add nothing beyond, the canon's own R5/
R19 text and the tree's "the legacy three RETIRE after migration" ruling already carried in the canon's own
change log (v0.3).

## Where the canon left room for a second reader to differ (form only, not significance)

1. **Whether R9's blanket "Monolith bronze CONFORMANT" census extends to a specific plane not named in it.**
   I read it as extending to `orion/inflection/bronze/` and `eclipse/inflection/bronze/` because the stated
   mechanism (a bucket-policy deny) is scoped to the whole monolith bucket, not to named paths; a stricter
   reader could hold that only the specifically-named comparison set (`opal-data-inf`, `opal-data-bd/smartx`)
   is measured and grade the rest UNDETERMINED for want of a per-plane sweep.
2. **Whether the legacy plane or the canonical destination (or both) carries an R18 dual-write finding.**
   I put the VIOLATES on the legacy `opal-data-inf/silver/` and `opal-data-inf/bronze/` rows alone, on the
   view that the destination is doing what is asked of it and the departure is the source's continued
   existence; a reader who treats a dual-write as a joint property of the pair would grade the canonical
   twins VIOLATES too.
3. **Whether the 108 date-named table-level prefixes are a genuine, presently-true finding or an unverified
   claim I should discount to UNDETERMINED.** `CN_TREE_INFLECTION.md` states the count as fact and says
   explicitly it is part of the tree being judged; I graded it as true. A reader who weighs "the ledger did
   not re-measure it" as doubt about CURRENT state, rather than as a disclosure of the finding's provenance,
   would grade A3 UNDETERMINED instead of VIOLATES for `eclipse/inflection/bronze/`.
4. **Whether R17, filed under A3 in the axis table, should also inform A2 for the four backup/scratch/probe
   rows**, since its own text names "(or a separate bucket)" as a valid backup home -- a bucket-structure
   fact. I kept A2 UNDETERMINED (citing R4, which does not test backup placement) rather than importing R17
   into A2; a reader could argue R17 settles A2 too, in which case those four rows would read A2 CONFORMS
   (a separate/adjacent root, exactly what R17 permits) rather than UNDETERMINED.
