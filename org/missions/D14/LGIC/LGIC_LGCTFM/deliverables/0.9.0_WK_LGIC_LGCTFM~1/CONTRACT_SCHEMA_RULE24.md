# CONTRACT_SCHEMA_RULE24 -- LT-s-1, worker note on `org/standards/LGCTFM_CONTRACT.schema.json`

**Author:** `0.9.0_WK_LGIC_LGCTFM~1`. **Cell:** `LT-s-1` (`LGIC_LGCTFM.TO-LT-s-1-r1`). **Governing record:**
`infra/logic/11_LGCTFM_CONTRACT_SCHEMA_RECORD.md` (whole file; the four-postulate record and its
word-boundary token census are LANDED there, not restated here -- Rule 24: *"A value-enum proposal
arrives WITH its four-postulate record + word-boundary token census, or it is not a proposal"*; this note
does not re-run the census, it cites where the record already ran it, section 6).

## The uncovered-member hunt this cell ran

The record's own domain subtraction (s.1.1) is already printed: `node_type_vocabulary.denominator` = 33
in `org/standards/NAMING_SCHEMA.json`, partitioned `kind.by_type` (18, disjoint) + `types_not_graded_by_kind`
(15, disjoint) = 33, 0 uncovered. This cell's job was narrower and mechanical: **re-derive that same
subtraction from the live file at this commit** rather than copy the record's printed numbers forward, so
a schema `$defs.node_type.enum` written from a stale recollection cannot drift from the carrier it claims
to cite. Measured directly against `org/standards/NAMING_SCHEMA.json` at this commit:

```
by_kind = set(NAMING_SCHEMA.json["kind"]["by_type"].keys())          -> 18
other   = set(NAMING_SCHEMA.json["types_not_graded_by_kind"].keys()) -> 15
want    = by_kind | other                                            -> 33, disjoint (by_kind & other == {})
```

`$defs.node_type.enum` in the schema is exactly `sorted(want)`, 33 values, none typed from memory --
`check_lt_r1.py s1-node-types` (`core_node_types`) re-derives the identical union at grading time and
diffs it against the schema's enum both ways (`in the vocabulary, absent from the schema` /
`in the schema, absent from the vocabulary`), so a hand-typed enum that silently dropped or added a
member would show as a non-empty diff, not a green. No member was found uncovered: the record's printed
"0 uncovered" (s.1.1) held under re-derivation.

## The four enums this schema adopts or mints, and their carriers

- `row_kind` {RESOURCE, PLANE, FORK} -- record s.1.2. `FORK` is the ONE token the record mints (s.6, token
  census row `fork`: 30 hits, disambiguated against `org/standards/isck/ledger/lineage.py`'s different
  "fork" -- a supersedes chain on RECORDS, never on RESOURCES); `RESOURCE` and `PLANE` are the record's own
  vocabulary, minted there, not adopted from elsewhere.
- `cell_status` {MEASURED, UNMEASURED, INFERRED, NOT_MEASURABLE} -- adopted whole from
  `projects/ATOM_DECOMP/skill/atomic-decomposition/references/ssot_establishment.schema.json`
  `$defs.cell.status` (record s.3, s.6).
- `axis` {A1, A2, A3, A4, A5, PROCESS, IDENTITY} -- adopted from `infra/logic/02_DOCTRINE.md` sect. 2
  (A1-A5 with their rules; PROCESS = R18-R20; IDENTITY = the spine, `infra/logic/05_IDENTITY_SPINE.md`'s
  cross-cutting family) (record s.4).
- `tension_kind` {HOME, FORMAT, GRAMMAR, COMPUTE, DECLARATION, PROCESS, IDENTITY} -- HOME/FORMAT/GRAMMAR
  adopted from `06_CONFORMANCE_LEDGER.md` sect. 7's MIGRATE kinds; COMPUTE/DECLARATION/PROCESS/IDENTITY
  name the remaining move classes the canon's rules imply (record s.4). `FORK` is a `row_kind` value and
  never appears in `tension_kind` -- the schema enumerates the two separately by construction (Rule 24(iii),
  intent coherence: a tension's `kind` answers "what moves", a row's `kind` answers "what grain of object
  this row is"; conflating them would let one token do two jobs).

`edge_type` (11 values: CALLS, READS, WRITES, TRIGGERS, INVOKES, STARTS, PUBLISHES, SERVES, AUTHORIZES,
MONITORS, REPLACES) is adopted whole from `evidence-model.md`'s edge vocabulary (record s.6); no acceptance
criterion in this round exercises it, it is included because the schema's `edges[]` field needs a closed
type and the record already names its carrier.

## Which cells a rename does NOT move (record s.5), carried into the schema's shape

The schema does not encode remedies (state coherence is a fact about the RUN, not the schema's grammar),
but its field boundaries are drawn so the record's s.5 table stays checkable against a contract instance
without a schema change:

- RENAME moves `desired.verdict` and may clear `mark`; it does NOT move `current.arn_or_path`, any PLANE
  row's disposition, or any trigger's `target`. The schema keeps `current.*` and `desired.*` as two
  separate cell-valued objects (never one flat field list) precisely so a remedy that moves only one half
  cannot silently touch the other's keys -- `additionalProperties` on `current` and `desired` are each
  scoped to their own object, not shared.
- HOME MOVE moves `current.arn_or_path` and a PLANE row's `members`; it does NOT move `desired.form`
  (name/format unaffected by home) -- the schema does not couple `current.arn_or_path` and `desired.form`
  validation to each other, so one can change under a remedy while the other's cell is untouched and still
  schema-valid.
- MARK moves nothing live and nothing in either half; the schema's `mark` field on a RESOURCE/PLANE row is
  typed `["string", "null"]`, never a cell -- it names WHICH of the three existing carriers marks the row,
  not a measured fact about the resource, so a MARK remedy's write (to `remediations.json` /
  `LEGACY_SERVED_PATHS.json` / a `scopes.json` alias row) is legible as a change to a plain field, not to a
  cell's `status`/`evidence`.
- FORK rows carry no `current`/`desired` split at all (record s.1.2: a FORK is a relation over rows, not a
  row with its own measured/desired pair) -- the schema's `fork_row` definition has no `current` or
  `desired` property, so a remedy that resolves a FORK (clearing `canonical_member`'s `RULING-OWED`) cannot
  be mistaken for a remedy on the member rows themselves; those stay separate `resource_or_plane_row`
  entries the FORK row only references by `row_id`.

## Traceability

Every enum value in `org/standards/LGCTFM_CONTRACT.schema.json` traces to a carrier this note or the
record names above; none is typed from this cell's own judgment. Schema file:
`org/standards/LGCTFM_CONTRACT.schema.json` (this commit). Record:
`infra/logic/11_LGCTFM_CONTRACT_SCHEMA_RECORD.md` (whole file, v0.1). Checker:
`org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py`
(`s1_node_types`, `s1_enums`, `s1_valid`, `s1_bare_value`, `s1_one_api`, `s1_no_instrument`), read-only,
never edited by this cell.
