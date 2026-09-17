# LT-s-1 round 1 result -- `0.9.0_WK_LGIC_LGCTFM~1` on `LGIC_LGCTFM.TO-LT-s-1-r1`

**Cell:** `LT-s-1`. **Artifacts:** `org/standards/LGCTFM_CONTRACT.schema.json` (new) and
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/CONTRACT_SCHEMA_RULE24.md` (new),
committed at `e2daf62f07` on branch `wk-lgic-lgctfm-1-1`.

## What the schema does

One draft 2020-12 JSON Schema for a run's contract, authored from
`infra/logic/11_LGCTFM_CONTRACT_SCHEMA_RECORD.md` sections 1-4 (the record itself, whole file, is the
governing four-postulate record + token census; this schema is authored FROM it, not a restatement of
it). Top level: `schema_version`, `subject` {`kind`, `key`, `vintage` {`repo_head`, `graph_built`,
`registry_hash`} -- plain strings, the run's own coordinate, never cells}, `trigger_denominator`
{`list_rules`, `list_schedules`, each a cell}, `ranking_rule` (string), `rows[]` (RESOURCE/PLANE rows with
a `current` and `desired` half, every field a cell, plus `mark`; or FORK rows with `members[]`, `one_job`
and `canonical_member`), `edges[]`, `tensions[]` (`axis`, `deciding_rules[]`, `kind`, `object_count`,
`factors` -- four cells), `plan[]`.

`$defs.cell` requires `{value, status, evidence}`, `evidence` requiring at least `instrument` and
`blind_spot` (order's own words; adopted structurally from
`projects/ATOM_DECOMP/skill/atomic-decomposition/references/ssot_establishment.schema.json` `$defs.cell`,
narrowed to this contract's own minimum-viable evidence form, record s.3).

`$defs.node_type.enum` is the 33-member union of `org/standards/NAMING_SCHEMA.json` `kind.by_type` keys
(18) and `types_not_graded_by_kind` keys (15), re-derived at authoring time (not copied from the record's
printed numbers) -- see `CONTRACT_SCHEMA_RULE24.md` for the re-derivation and its result (0 uncovered,
matching the record).

`$defs.row_kind`, `$defs.cell_status`, `$defs.axis`, `$defs.tension_kind` are typed exactly to the
record's own enums (s.1.2, s.3, s.4); `FORK` appears only in `row_kind`, never in `tension_kind`.

## Criterion-by-criterion

All six mechanical criteria run against `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py`
(read-only fixed input, not edited).

- **S1R1-AC1** `s1-valid`: the planted contract validates with 0 errors. PASS.
- **S1R1-AC2** `s1-bare-value`: the planted contract with `rows[0].current.name` replaced by its bare
  `value` string fails validation (the cell schema's `type: object` / `required` rejects a bare string).
  PASS.
- **S1R1-AC3** `s1-one-api`: the planted contract with `trigger_denominator.list_schedules` removed fails
  validation (`list_schedules` is `required`). PASS.
- **S1R1-AC4** `s1-no-instrument`: the planted contract with `rows[0].current.name.evidence.instrument`
  removed fails validation (`instrument` is `required` inside `evidence`). PASS.
- **S1R1-AC5** `s1-node-types`: the schema's `$defs.node_type.enum` (33 values) matches the
  `NAMING_SCHEMA.json` union exactly, both directions empty (`in the vocabulary, absent from the schema: []`;
  `in the schema, absent from the vocabulary: []`). PASS.
- **S1R1-AC6** `s1-enums`: `$defs.row_kind`, `$defs.cell_status`, `$defs.axis`, `$defs.tension_kind` each
  match the record's sets exactly (four `OK` rows). PASS.
- **S1R1-AC7**: JUDGMENT, no verdict from this worker. `CONTRACT_SCHEMA_RULE24.md` names the uncovered-member
  hunt (re-derivation against `NAMING_SCHEMA.json` at this commit, 0 uncovered) and, per record s.5, which
  cells each of the seven remedies does not move, mapped onto the schema's own field boundaries (`current`/
  `desired` kept as two separately-scoped cell objects; `mark` typed as a plain field never a cell; FORK
  rows carrying no `current`/`desired` split at all). Every enum value traces to the carrier named in that
  note or in this record.

## Controls

**Negative control (mutant, on the schema's own absence, not a doctored pass):** all six subcommands were
re-run with `org/standards/LGCTFM_CONTRACT.schema.json` temporarily moved aside (restored immediately
after, `git status --porcelain` clean on the path both before and after). Every one FAILed, each printing
`absent: org/standards/LGCTFM_CONTRACT.schema.json` -- the state at the cut, before this cell existed.
Every criterion's own DOCTORED-input arm (bare/one_api/no_instrument) is already exercised by the checker
itself inside each PASS run (`core_schema_refuses` derives the invalid variant from the planted valid one
in memory and asserts it is refused): S1R1-AC2/AC3/AC4 are themselves the fired-mutant evidence for the
accept arm S1R1-AC1.

**Determinism:** `s1-valid` and `s1-enums` each run twice against the committed schema; outputs
byte-identical both times (`diff` empty).

## Commits

- `e2daf62f07` `build(LGIC_LGCTFM.TO-LT-s-1-r1, 0.9.0_WK_LGIC_LGCTFM~1): the contract JSON schema, authored
  from the Rule 24 record` -- `org/standards/LGCTFM_CONTRACT.schema.json`,
  `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~1/CONTRACT_SCHEMA_RULE24.md`.

No surprise row filed: nothing in this cell diverged from its order, the record, or the fixed-input
checker.
