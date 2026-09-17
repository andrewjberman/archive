# LT-e-3 round 1 result -- `0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-e-3-r1`

**Cell:** `LT-e-3`. **Artifacts:** `lib/opal_lgctfm.py` (edited -- `_type_uncovered()`, the NOT_COVERED branch
of `desired_cells()`, the third plant and `build_tensions()`/`_factor_live()`/`_factor_client_facing()`/
`_factor_irreversible()`/`_factor_rules_colliding()`/`_tension_rank_key()`), plus the GRADED RUN's own
re-generated output `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk/{contract.json,
PLANT_UNTYPEABLE.json}` (`PLANT.json` unchanged from LT-e-1/LT-e-2).

## What this cell adds

`walk`'s own `cmd_walk()` now also types TENSION rows onto the same contract, per DEC-6 /
`11_LGCTFM_CONTRACT_SCHEMA_RECORD.md` s.4:

- **`build_tensions(rows)`** emits one tension per `RESOURCE`/`PLANE` row whose `desired.verdict` is
  `ALIAS`, `OUT-OF-PATTERN` or `RAISE` (DEC-6's own definition: "one row's halves disagreeing" --
  `CONFORMANT` is no disagreement, `NOT-GRADED` is outside `grade()`'s domain, `NOT_COVERED` is this cell's own
  "no type fits" verdict; a `FORK` row carries no halves of its own and is never a tension's `row_id`, DEC-6:
  "never a tension kind"). This round's WALK carries no `FORK` rows (those are the `forks` verb's, a separate
  contract file `E3R1` does not read).
- **Typing.** This round's only builder is `grade()` (DEC-4) -- the naming grammar alone (N1-N5, both the key
  and resource grammars, all under R1's own generated section, `02_DOCTRINE.md`). Every tension this walk can
  type therefore sits on **axis A3**, **deciding rule R1**, **kind GRAMMAR** (the ledger's MIGRATE kind a RENAME
  remedy closes, s.5's state-coherence table). This is a real, cited constraint of what this round's ONE
  builder measures, not a shortcut: a future cell adding a second builder (e.g. `address()` for a HOME-axis
  check) would widen the set of `(axis, kind, deciding_rules)` combinations this pass can emit.
- **The four factor cells**, each MEASURED with the instrument DEC-6 names: `live` and `client_facing` carry
  the row's own `current.live`/`current.client_facing` value and status, re-wrapped so the FACTOR's own
  instrument text always names `lib/trading_calendar.py` (for `live`) or `07_ROUTING_REDERIVATION.md`/
  `LEGACY_SERVED_PATHS.json` (for `client_facing`) regardless of which of `current`'s several code paths
  produced the underlying value -- the original instrument is kept as the cell's `locator`, for provenance.
  `rules_colliding` = `len(deciding_rules)` = 1 for every tension this round emits (no second, independently-
  measured ruling collision is counted). `irreversible` = `false` for every tension this round emits, cited to
  `02_DOCTRINE.md` R1/N5 ("renames authorized: NONE ... moves no live name") and s.5's state-coherence table
  (RENAME moves only `desired.verdict`) -- a naming-grammar disagreement is closed by a rename, which touches
  no bytes, no triggers and no plane rows, so it is never irreversible under this round's own rule set (R9's
  parquet-under-bronze is the canon's cited IRREVERSIBLE example, and it is not R1).
- **The rank.** `ranking_rule` (unchanged since LT-e-1: `"order by irreversible, then client_facing, then
  live, then rules_colliding; object_count as tiebreak (08_TENSION_MAP.md s.0)"`) is printed at the top level,
  and `tensions[]` is emitted PRE-SORTED by exactly that key (`_tension_rank_key()`, the same tuple
  `check_lt_r1.py`'s own `rank_key()` re-derives from the emitted cells) -- `tension_id` is assigned `T-0001..`
  in the sorted position, never re-sorted by a reader.
- **The untypeable plant (E3R1-AC5).** A third planted row, `COGNITO_USER_POOL` (a real AWS resource class with
  no row in `NAMING_SCHEMA.json`'s `node_type_vocabulary` -- measured: `'COGNITO_USER_POOL' not in
  opal_naming._vocab().types`, 33 of 33 types enumerated, none matching), name
  `opal-blackdiamond-49financial-legacy-user-pool`. `desired_cells()` calls `grade(name, "COGNITO_USER_POOL")`,
  which raises `RaiseDefect("G1.1: 'COGNITO_USER_POOL' is not a node type of NAMING_SCHEMA.json")`; the new
  `_type_uncovered()` helper recognizes the G1.1 prefix and returns `desired.verdict = NOT_COVERED` (the sixth
  verdict `11_LGCTFM_CONTRACT_SCHEMA_RECORD.md` s.3.1 adopts, distinct from `RAISE` -- a RAISE is a real,
  schema-covered type whose registry row is missing; NOT_COVERED is a type the schema itself does not cover at
  all). The row's name is also written to `walk/PLANT_UNTYPEABLE.json` as `{"name": ...}`. `build_tensions()`
  excludes any row whose verdict is not in `{ALIAS, OUT-OF-PATTERN, RAISE}`, so this row is never graded into a
  tension by construction -- "a resource no type fits is returned, never silently graded" (WORKER FACE).

## The graded run

Re-run identically to LT-e-1/LT-e-2's own invocation (never fed `SUBJECT_CONTROL.json`): `--subject 49financial
--seed opal-data-bd --seed opal-data-inf --seed opal-data-cot --out .../deliverables/0.9.0_WK_LGIC_LGCTFM~1/walk`.
278 rows (incl. 3 planted: LT-e-1's UNMEASURED-current notify-target plant, LT-e-2's RAISE plant, and this
round's NOT_COVERED plant), verdict distribution `OUT-OF-PATTERN 244, ALIAS 14, RAISE 13, CONFORMANT 5,
NOT-GRADED 1, NOT_COVERED 1` (278 total). **271 tension rows** (244 + 14 + 13 = 271, the three excluded classes
sum to 7: 278 - 7 = 271, checked). AWS-plane pull: 249 hits, denominator 2573 nodes scanned; both trigger APIs
census'd (`list_rules=58` of 144, `list_schedules=2` of 23). Re-run into a fresh scratch directory and diffed:
byte-identical (determinism, below).

## Criterion-by-criterion

All five mechanical criteria run against the committed `walk/contract.json`:

- **E3R1-AC1** `e3-rule`: `ranking_rule` printed with `irreversible`/`client_facing`/`live`/`rules_colliding`/
  `object` at strictly increasing string positions `[9, 28, 48, 59, 76]`. PASS.
- **E3R1-AC2** `e3-factors`: 271 tensions x 4 factor cells = 1084 checked, 0 defective (every cell a valid
  status, every instrument matching its named pattern). PASS.
- **E3R1-AC3** `e3-order`: the contract's own `tensions[]` order re-derives byte-for-byte from
  `sorted(tensions, key=rank_key)` -- first divergence `None`. PASS.
- **E3R1-AC4** `e3-types`: every tension's `axis` in the closed set, `kind` in the closed set (never `FORK`),
  `deciding_rules` non-empty and each entry matching `^R\d+$` -- 0 off the closed set. PASS.
- **E3R1-AC5** `e3-untypeable`: the planted name has 1 row, 1 `NOT_COVERED`, 0 tensions naming it. PASS.
- **E3R1-AC6**: judgment, for `3.0.0_SA_CVO` at L9 -- recorded `UNVERIFIABLE-BY-INSTRUMENT` below, no
  self-graded verdict.

## Controls

**Mutant (E3R1-AC3/AC2/AC4 combined, one mutation run each, then restored):**
1. Swapped `tensions[0]` and `tensions[-1]` (rank keys `(True, False, False, -1, -1)` vs
   `(True, True, True, -1, -1)`, genuinely different) -> `e3-order` flipped to
   `FAIL-E3-ORDER-REPRODUCED-FROM-CELLS`, first divergence at index 0. (A first attempt swapping
   `tensions[0]`/`tensions[1]`, which TIE on rank key, did NOT flip the verdict -- a stable re-sort cannot
   distinguish two orderings of tied keys, so that pair was not a discriminating mutant; recorded as a finding
   about the control, not a defect.)
2. Set `tensions[0].factors.live.evidence.instrument = "a calendar day"` -> `e3-factors` flipped to
   `FAIL-E3-FOUR-FACTORS-MEASURED`, naming `T-0001 factor live`.
3. Set `tensions[1].kind = "FORK"` -> `e3-types` flipped to `FAIL-E3-TENSION-TYPES-CLOSED`, naming `T-0002`.
4. Restored from a pre-mutation copy (`diff` byte-identical to the pre-mutation file); all five criteria
   re-verified PASS.

**Determinism:** the ENGINE itself (not just the checker) re-run with the identical `walk` invocation into a
fresh scratch directory; `diff` against the committed `walk/contract.json` -- byte-identical (including row
order, tension order, `tension_id` assignment and every factor cell).

## Surprise filed

`LGIC_LGCTFM-W1-S1` (OBSERVATION, ARMED, `disarm_owner: 2.0.0_SA_COO~G`): `check_lt_r1.py`'s `e2-reproduce`
(LT-e-2's own E2R1-AC1 arm, `core_reproduce()`) treats any raising builder call as correctly reported only when
`desired.verdict == "RAISE"`; it has no branch for `NOT_COVERED`, a verdict this round's own WORKER FACE mints.
Re-running `e2-reproduce` against this round's regenerated `walk/contract.json` now reads `277 of 278
reproduced`, `FAIL-E2-DESIRED-EQUALS-BUILDER`, though LT-e-2's own cell did not change and its order is already
`complete`. Filed because a later re-run of that criterion (by the issuer, the CVO at L9, or a future regression
sweep) would read a FAIL that is not a defect in LT-e-2's own code. Not routed BLOCKING: it blocks none of
E3R1-AC1..AC6, all of which read PASS against the same regenerated contract.

## Declared exclusions

- **A second, independently-measured "prior rulings met" term inside `rules_colliding`.** DEC-6: "COLLIDING
  from the R-id count" -- this round counts only `len(deciding_rules)` (always 1, since every tension cites
  `["R1"]` alone); no cross-referenced Andrew-ruling collision count is added. Named as a coverage choice, not
  hidden inside the "R-id count" language.
- **Tensions of any axis/kind other than A3/GRAMMAR/R1.** This round's `walk` calls exactly one builder
  (`grade()`, DEC-4); a row whose disagreement would type on A1/A2/A4/A5/PROCESS/IDENTITY needs a second
  builder call this cell does not make (e.g. `address()` for a HOME-axis check, or a plan-step read for
  PROCESS). `TENSION_AXIS`/`TENSION_KIND`/`TENSION_DECIDING_RULES` are named as module-level constants in
  `lib/opal_lgctfm.py` specifically so a later cell adding a second builder can extend `build_tensions()`
  without re-deriving this round's reasoning.
- **The plan.** `plan: []`, unchanged -- LT-p-1's cell (worker slot ~2, decomposition v1.1 s.10).

## Commit

Artifact committed on branch `wk-lgic-lgctfm-1-1` before grading (see the commit hash in this deliverable's
proof-of-spec `artifacts_produced[].commit_or_etag`).
