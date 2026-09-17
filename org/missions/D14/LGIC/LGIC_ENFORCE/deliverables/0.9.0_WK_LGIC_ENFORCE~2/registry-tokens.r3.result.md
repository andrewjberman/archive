# EN-r-5-r3 result -- registry tokens (R-6's six)

**Assignee:** `0.9.0_WK_LGIC_ENFORCE~2`. **Cell:** `EN-r-5` (`LGIC_ENFORCE_DECOMP.md` v3.2, round-3
cell 5, s.0c). **Commit:** `23980d3fbe` (the edits), this deliverables directory's commits carry
the proof and status flip.

## What landed

`infra/logic/registry/systems.json`:
1. `refused_keys.retired = ["imo"]` + `retired_basis` (Andrew's card 9, RETIRE) + Rule 24 record
   (`RETIRED_CLASS_RULE24.r3.md`, same directory).
2. `refused_keys.workstream_code` gains `"find"` + `find_basis` (a project code is never a system,
   V3; FIND_INSURE orders + `data/find/`).
3. `systems` gains a `harvest` PRODUCT row: `owner_directive: D5`, `owner_claim: inferred` (per
   R-6's own instruction, not `measured`, though the citation is direct), `owner_basis` citing
   `infra/aws/terraform/harvest/main.tf`'s consolidation comment, the `scoped-amgt-api.tf` note
   naming the Andrew-direct, the AMGT_RESAPP harvester task orders and `DIRECTIVES.yaml` D5's
   `projects: [AMGT_RESAPP]` line.
4. `unresolved` drops to three entries -- `astn`, `news`, `trade` -- each with a NEW `why` (not the
   pre-cell sentence) stating the measured fact: none traces to a `DIRECTIVES.yaml` line or a
   mission-tree `D<n>` project; each traces only to a LEGACY FLAT `org/projects/*.json` record
   naming a SEAT as owner. `trade`'s `why` additionally records that R-6's own "plausibly the
   TRADEOPS second fabric's product" hypothesis is MEASURED FALSE (the resources are S3-backed
   from this repo's own artifacts bucket or EXTERNAL, not from the separate `docs_abcdeg` repo).
5. Regenerated `infra/aws/terraform/modules/opal_name/tests/vectors.json` and
   `opal_name.tftest.hcl` via `python lib/opal_naming.py generate --out . --target <those two>`,
   at the new registry hash `registry@4a7c7676da225e7b`. Test fixtures only (R-26); nothing live
   moved, no Terraform ran.

**Owner cards for Andrew** (per R-6 s.3's "the cell returns ONE card ... per such token"):
`OWNER_CARDS.r3.md`, one card each for `astn`, `news`, `trade`.

## Criteria, all four run at commit `23980d3fbe`

- **R5R3-AC1** (`r5-imo-retired`): `PASS-R5-IMO-RETIRED`, rc 0. "retired class present: True; imo
  a member: True; imo still unresolved: False".
- **R5R3-AC2** (`r5-find-refused`): `PASS-R5-FIND-REFUSED`, rc 0. "workstream_code members: 11;
  find a member: True; find still unresolved: False".
- **R5R3-AC3** (`r5-product-owners`): `PASS-R5-OWNERS-MEASURED`, rc 0. "harvest ROW ... -> ok;
  astn/news/trade OPEN why changed from the cut: True ... DENOMINATOR: 4 product token(s) ruled by
  R-6; 0 defective".
- **R5R3-AC4** (`python lib/opal_naming.py validate`): `VALIDATE: OK 25 system row(s), 9 scope
  row(s), 17 warning(s) at registry@4a7c7676da225e7b`, rc 0. 17 WARNs, all pre-existing `inferred`
  claims plus the new `harvest` row's own WARN (an `inferred` claim is EXPECTED to WARN by design,
  per `_about.row_fields`; WARN is not a refusal).
- **R5R3-AC5**: judgment, for `3.0.0_SA_CVO` at L9. Not self-graded.

## Controls

**Mutant, two arms**, each on a saved copy of the committed `systems.json`, graded by the fixed
checker, then restored and verified byte-identical to the save (`cmp`):
- ARM A: `refused_keys.pop("retired")`. Expected FAIL naming `imo` not retired. Observed:
  `retired class present: False; imo a member: False; imo still unresolved: False` /
  `FAIL-R5-IMO-NOT-RETIRED`, rc 1. Restored, `cmp` identical.
- ARM B: `harvest` row's `owner_basis` set to `""`. Expected FAIL naming `harvest` defective.
  Observed: `harvest ROW ... basis_len=0 -> DEFECT` / `... 1 defective` /
  `FAIL-R5-OWNERS-UNMEASURED`, rc 1. Restored, `cmp` identical.

Both FIRED-AS-EXPECTED.

**Determinism:** AC1, AC2, AC3 and AC4 each run twice in immediate succession on the same
committed tree (`23980d3fbe`). All four IDENTICAL byte-for-byte output both runs, rc 0 both times.
STABLE.

## Declared exclusions

- `imo`'s live bucket state (`opal-data-imo`, still LIVE at R-6's measurement) is NOT touched --
  retirement here is a naming-registry act (`systems.json`), never a bucket delete; its resources
  grade as class (d) rule gaps by design (R-6 :225) until the R19 retirement project removes them.
- The 21 `find`-carrying live resource names, the 14 `astn`, 34 `news` and 22 `trade` live resource
  names are NOT renamed or touched -- this cell is the naming-REGISTRY act only (BOUNDS: nothing
  live moves).
- No AWS read of `opal-data-harvest`'s live object listing was re-run by this cell; R-6's own
  measurement (132 objects, newest 2026-09-15T16:56Z) is cited, not re-derived, since re-deriving
  the same live-bucket read with the same instrument would be repetition, not corroboration, and
  the harvest disposition does not turn on the exact object count, only on LIVE-vs-row-18's-dead
  object, which R-6 already established.
- `scopes`, `tiers`, `resources`, `exemptions` untouched (BOUNDS).

## Surprises

None filed. Every branch this cell measured (harvest resolvable, astn/news/trade unresolvable,
trade's tradeops hypothesis false) is a branch the order's own text explicitly anticipated and
instructed the disposition for ("Where the tree links to ... mint a PRODUCT row ... Where it links
to NONE, the token STAYS unresolved ... A trade whose resources deploy from the tradeops root is
recorded as that fabric's, not minted here" -- measured NOT the case, and the order's own
conditional framing already covers that outcome).
