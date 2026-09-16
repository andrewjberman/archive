# LGIC_ENFORCE.TO-EN-g-1-r2 -- commit-limb, round 2 -- result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, slot ~3, queue position 1. **Worktree:** `.worktrees/wk-lgic-enforce-2b-3`,
branch `wk-lgic-enforce-2b-3`, cut from `CLOUD` @`3ee4bb55ec`. **Commit:** `d49f538774194592cb77e89c71731c533bca1ce6`
(LOCAL on the worktree branch; the COO drains it).

## The bar

`EN-g-1`, round 2 (decomp v2.1 @8e0d09e418, section 0b): the commit limb refuses only what a change ADDS to
an AUTHORED file. Edit `.tools/naming-gate.py` for three items: (1) skip a machine-written Terraform plan
JSON at commit, never grading it; (2) validate the registry BEFORE reading it, printing `NAMING ERROR`
naming the refusal and grading nothing when it is invalid; (3) read the Terraform-type-to-node-type map from
`org/standards/NAMING_SCHEMA.json` v1.9 rather than a hand-typed literal, keeping the name `TF_NODE` so
`naming-apply-gate.py`'s import still resolves. Round 1's 14 commit-limb criteria must still pass.

## Premises re-grounded

- Gate G-V19b (the one-carrier group with the schema's Terraform-type map, on CLOUD) was MET, measured, not
  assumed: `git merge-base --is-ancestor 4730cec6ca <base>` read true at spawn.
- `org/` and `.tools/` both present at the worktree root (first-act check).
- `org/standards/NAMING_SCHEMA.json` carries `tf_type_map` (34 entries, `version: v1.9`) at my base; its 28
  entries matching the pre-edit `TF_NODE` are byte-identical in value; the 6 extra keys
  (`aws_apigatewayv2_route`, `aws_cloudfront_distribution`, `aws_iam_user`, `aws_kms_key`,
  `aws_route53_record`, `aws_vpc_endpoint`) occur 0 times across round 1's 32 fixed-input files (measured
  with `comp-find`, denominator printed), so widening `TF_NODE` to the full schema map cannot move round 1's
  suite.
- `lib/opal_naming.py` carries `validate(reg_dir=None, systems_file=None) -> (refusals, warnings)`, each a
  list of `(where, field, reason)` tuples -- the same call the CLI `validate` subcommand and the round-2
  checker's `_plant_broken_registry()` use, over the same default registry path `Naming.__init__`'s
  `mod._registry()` reads.

## What was built

`.tools/naming-gate.py`:

1. `is_plan_artifact(post_text)` -- `json.loads`s the JSON post-image; true iff the top level is a dict
   carrying `format_version` AND `terraform_version`, with `resource_changes` OR `planned_values`. In
   `grade_file()`'s `.json` branch, a plan artifact returns one row, verdict `SKIP`, counts-as `PASS`
   (never REFUSE/WARN), printed through the existing `NAMING <verdict> ...` / `why:` format -- no change to
   `main()`'s printing loop. An authored `.json` file that does not match falls through to `json_literals()`
   exactly as before.
2. `run()` now calls `mod.validate()` right after `load_opal()` and BEFORE constructing `Naming(mod)` (which
   is what reads the registry into `firm_whole`/`product_whole`/etc.). A non-empty `refusals` list raises
   `GateError("the registry is refused by validate (%d refusal(s)): %s.%s: %s" % ...)`, caught by `main()`'s
   existing handler exactly like any other internal error: `NAMING ERROR <msg>` printed, exit 1 enforcing / 0
   WARN. The message always contains the substring "registry".
3. `TF_NODE` is no longer a literal dict. `_load_tf_node()` reads `org/standards/NAMING_SCHEMA.json`,
   converts its `tf_type_map` (`{tf_type: {"node_type":..., "name_attribute":...}}`) into the
   `{tf_type: (node_type, name_attribute)}` shape `_tf_hint()` already consumed, and is bound to `TF_NODE` at
   import time (a `naming-apply-gate.py` plain `import`/`exec_module` never calls `main()`/`run()`, so the
   map must exist as soon as the module loads). A schema read/parse failure returns `{}` rather than raising
   at import -- the same degrade an unlisted Terraform type already produced before this change (no hint,
   `classify()`'s generic reading takes over). No dict literal with >=10 `aws_`-prefixed string keys remains
   anywhere in the file (`aws_dict_literals(GATE)` via AST walk reads 0).

## The four verdicts

| id | invocation (subcommand) | result |
|---|---|---|
| G1R-AC1 | `g1r-plan-not-graded` | **FAIL-PLAN-FILE-GRADED** (rc=1) -- BLOCKED by a corrupt fixture, not the limb; see below |
| G1R-AC2 | `g1r-registry-first` | **PASS-REGISTRY-VALIDATED-FIRST** (rc=0) |
| G1R-AC3 | `g1r-map-from-schema` | **PASS-COMMIT-LIMB-READS-SCHEMA-MAP** (rc=0) |
| G1R-AC4 | `g1r-regression` | **PASS-G1-SUITE-HOLDS** (rc=0), 14 of 14 round-1 commit-limb criteria |

### G1R-AC1: blocked by the fixture, not the code

The named invocation reads `VERDICT: FAIL-PLAN-FILE-GRADED`. Cause: its own fixed input,
`fixed_inputs/r2/tests/g1r/01_plan_json_added.patch`, is a corrupt unified diff -- the hunk header declares
`@@ -0,0 +1,13 @@` (13 added lines) while the body between the header and EOF carries exactly 12
`+`-prefixed lines (enumerated directly, index 5-16 of 18 total lines). `naming-gate.py`'s own
`parse_diff()` refuses it as "not a unified diff: ... ends early (0/0 old, 12/13 new)" -- **on BOTH the
pre-edit gate (`git show HEAD:.tools/naming-gate.py`, saved unmodified to a scratch copy) and the edited
one**, and independently, `git apply --check` on the same bytes returns `error: corrupt patch at ...:18`,
rc=128. This is a defect that predates and is independent of this cell's change.

To confirm the SKIP logic itself is correct, a byte-identical copy of the fixture with only the hunk header
corrected (`@@ -0,0 +1,12 @@`) was built in `.scratch/` (never committed, never in `fixed_inputs/`, which
stays untouched per BOUNDS) and run directly against the edited gate:

```
NAMING SKIP .../fixture_plan.r2.json:1 <machine-written plan file> -> -
  why: top level carries format_version, terraform_version and resource_changes or planned_values (a
  terraform show -json artifact): not graded
NAMING-GATE: PASS 1 graded
```
rc=0 -- and the untouched control fixture, `02_authored_json_added.patch` (an authored JSON file carrying
the identical string `mdpf-cottonwood-publisher-queue`), still reads `NAMING REFUSE ... -> mdpf-cot-publisher-queue`,
rc=1, exactly as item 1 of the cell specifies.

Filed `LGIC_ENFORCE-W3-S10` (class BLOCKING, hazard ARMED, disarm owner `2.0.0_SA_COO~G`, the fixed inputs'
issuer) per BOUNDS: the fixture is outside this order's `<paths>` and read-only, so this is a row, never an
override. Per the proof-of-spec contract, G1R-AC1's acceptance row below is graded `FAIL` by the invocation's
actual output, honestly, and the row is not marked complete.

### G1R-AC2: registry-first, three arms

Enforcing, over a registry that LOADS but `validate` refuses (a planted `systems.json` row owned by
`D999`, which `_DCODE_RE` accepts but which resolves nowhere in `DIRECTIVES.yaml`): `rc=1`,
`NAMING ERROR the registry is refused by validate (1 refusal(s)): systems.json[17].owner_directive: 'D999'
does not resolve in org/missions/DIRECTIVES.yaml`. WARN mode, same broken registry: `rc=0`, the same
`NAMING ERROR` line printed (an error is never silent, only non-blocking). Control, the same patch over the
restored, valid registry: `rc=0`, no `NAMING ERROR` anywhere.

**Negative control** (discriminating the fix): the same three arms run against the pre-edit gate (temporary
swap, restored byte-for-byte afterward -- `git status --porcelain -- .tools/naming-gate.py` clean before and
after) read `VERDICT: FAIL-REGISTRY-NOT-VALIDATED`: enforcing over the broken registry the pre-edit limb
grades normally (`NAMING CONFORMANT ... -> opal-platform-events-queue`, `NAMING-GATE: PASS 1 graded`,
`rc=0`), never noticing the registry is invalid, because it reads the registry through `Naming.__init__` and
never calls `validate()` at all.

### G1R-AC3: schema-sourced map, no hand-kept literal

`tf_map_in(NAMING_SCHEMA.json)` finds the schema's own `tf_type_map` at `$.tf_type_map` (34 entries);
`aws_dict_literals(.tools/naming-gate.py)` (an AST walk for a `Dict` node with >=10 string keys starting
`aws_`) reads 0.

**Mutant** (discriminating the fix): a scratch copy of the edited gate with one 10-key `aws_*` dict literal
reinserted (`_MUTANT_MAP = {"aws_a": 1, ..., "aws_j": 1}`) read `DICT LITERALS ...: 1` and
`VERDICT: FAIL-COMMIT-LIMB-OWN-MAP`, rc=1 -- fired as expected. Swapped back afterward; `git status
--porcelain -- .tools/naming-gate.py` clean.

### G1R-AC4: round-1 regression

`check_en.py --list` names 14 `g1-*` subcommands; each re-run individually against the edited gate:
`ROUND-1 COMMIT-LIMB CRITERIA RE-RUN: 14  NOT PASSING: []`, `VERDICT: PASS-G1-SUITE-HOLDS`, rc=0.

## Determinism

Two same-input runs of `python .tools/naming-gate.py --diff .scratch/01_plan_json_added.fixed.patch
--enforce` (the corrected scratch copy of G1R-AC1's fixture) compared with `cmp`: byte-identical, 314 bytes
each, `cmp` rc=0.

## Rows filed

`LGIC_ENFORCE-W3-S10` (BLOCKING, ARMED, disarm `2.0.0_SA_COO~G`) -- the corrupt `01_plan_json_added.patch`
fixture, detailed above.

## Limits

- G1R-AC1 cannot be proven PASS through its named invocation while the fixture stands; the row above is the
  honest record, and the commit-limb logic it targets is independently confirmed correct against a
  header-corrected copy of the same bytes, run outside `fixed_inputs/` (never committed).
- The schema read for `TF_NODE` degrades to an empty map on a read/parse failure rather than raising at
  import (required so `naming-apply-gate.py`'s plain `import` of this module, which never calls
  `main()`/`run()`, cannot crash on a broken schema); this mirrors the pre-existing degrade for any
  Terraform type absent from the map (no hint, `classify()`'s generic reading). No criterion here exercises
  a missing/corrupt schema.
- `.scratch/` files used for the negative control, the mutant and the corrected-fixture check are not
  committed (worktree scratch only, per CLAUDE.md); their content and the exact commands run are quoted
  above and in the proof-of-spec instance's `output_evidence`/`controls` for re-derivation.
