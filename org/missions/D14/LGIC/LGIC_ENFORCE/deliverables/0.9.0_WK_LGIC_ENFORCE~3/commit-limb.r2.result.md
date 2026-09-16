# LGIC_ENFORCE.TO-EN-g-1-r2 -- commit-limb, round 2 -- result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, slot ~3, queue position 1. **Worktree:** `.worktrees/wk-lgic-enforce-2b-3`,
branch `wk-lgic-enforce-2b-3`, cut from `CLOUD` @`3ee4bb55ec`. **Build commit:**
`d49f538774194592cb77e89c71731c533bca1ce6` (LOCAL; the COO drained it into CLOUD at `4f7f050f2c` per the
resume message, independently confirmed below).

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
  entries matching the pre-edit `TF_NODE` are byte-identical in value; the 6 extra keys occur 0 times across
  round 1's 32 fixed-input files (measured with `comp-find`, denominator printed), so widening `TF_NODE`
  cannot move round 1's suite.
- `lib/opal_naming.py` carries `validate(reg_dir=None, systems_file=None) -> (refusals, warnings)`, the same
  call the CLI `validate` subcommand and the round-2 checker's `_plant_broken_registry()` use, over the same
  default registry path `Naming.__init__`'s `mod._registry()` reads.

## What was built

`.tools/naming-gate.py` (unchanged since the build commit; nothing below required a further code edit):

1. `is_plan_artifact(post_text)` -- true iff the JSON post-image's top level carries `format_version` AND
   `terraform_version`, with `resource_changes` OR `planned_values`. `grade_file()`'s `.json` branch returns
   one `SKIP`/`PASS` row for a match, printed through the existing format; an authored `.json` file that does
   not match is graded exactly as before.
2. `run()` calls `mod.validate()` right after `load_opal()` and BEFORE constructing `Naming(mod)`. A
   non-empty `refusals` list raises `GateError("the registry is refused by validate (%d refusal(s)): ...")`,
   caught by `main()`'s existing handler: `NAMING ERROR <msg>` printed, exit 1 enforcing / 0 WARN.
3. `TF_NODE` is built at import time by `_load_tf_node()` from `org/standards/NAMING_SCHEMA.json`'s
   `tf_type_map`, converted into the `{tf_type: (node_type, name_attribute)}` shape `_tf_hint()` already
   consumed. No dict literal with >=10 `aws_`-prefixed string keys remains in the file.

## Round-1 fixture defect, found and remedied mid-order

G1R-AC1's own fixed input, `fixed_inputs/r2/tests/g1r/01_plan_json_added.patch`, was a corrupt unified diff:
its hunk header declared `@@ -0,0 +1,13 @@` (13 added lines) while the body carried exactly 12. This worker
found it, verified it on two independent instruments (the pre-edit gate's own `parse_diff()`, and real
`git apply --check`, rc=128), confirmed the edited gate's SKIP logic was correct on a header-corrected
scratch copy of the same bytes, filed `LGIC_ENFORCE-W3-S10` (BLOCKING, ARMED, disarm `2.0.0_SA_COO~G`), left
the order's `<status>` `pending`, and delivered a proof-of-spec instance recording G1R-AC1 as an honest FAIL
by the named invocation's actual output -- **without touching working code to paper over a broken input**.

The issuer, `2.0.0_SA_COO~G`, verified the finding independently (a parser reading the hunk header against
its own body, and `git apply --check` -- both agreed) and corrected the ONE wrong line
(`@@ -0,0 +1,13 @@` -> `@@ -0,0 +1,12 @@`, zero other bytes changed, all 17 CRLF endings intact), committed
as `6f640ead30`, and drained this worker's branch into CLOUD at `4f7f050f2c`. The other two `g1r` fixtures
(`02_authored_json_added.patch`, `03_conformant_name.patch`) were checked too and are sound; the blast
radius was exactly one file.

**Independently re-verified in this worktree, on a different instrument than the coordinator's message
alone** (never taken on the message's word):

- `git show 6f640ead30:<path>` vs the worktree's post-fix copy of the fixture: differ only by CRLF rendering
  (0 CRLF in the stored blob, 17 in the checked-out copy); byte content identical once normalized to LF.
- `git diff HEAD -- <path>` in this worktree: the only hunk changed is the header, `+1,13` -> `+1,12`; no
  other line differs.
- `git merge-base --is-ancestor 7bdcbfb325 4f7f050f2c` -> true (this worker's proof-delivery commit is an
  ancestor of the drain tip). `git merge-base --is-ancestor 6f640ead30 4f7f050f2c` -> true (the fixture fix
  is included in the drain tip).
- All four criteria re-run in this worktree with the corrected fixture (below).

## The four verdicts, final

| id | invocation (subcommand) | result |
|---|---|---|
| G1R-AC1 | `g1r-plan-not-graded` | **PASS-PLAN-FILE-NOT-GRADED** (rc=0) |
| G1R-AC2 | `g1r-registry-first` | **PASS-REGISTRY-VALIDATED-FIRST** (rc=0) |
| G1R-AC3 | `g1r-map-from-schema` | **PASS-COMMIT-LIMB-READS-SCHEMA-MAP** (rc=0) |
| G1R-AC4 | `g1r-regression` | **PASS-G1-SUITE-HOLDS** (rc=0), 14 of 14 round-1 commit-limb criteria |

### G1R-AC1, re-run with the corrected fixture

```
MACHINE-WRITTEN PLAN FILE ADDED: rc=0  GIC_ENFORCE~9/fixture_plan.r2.json:1 <machine-written plan file> -> -
  why: top level carries format_version, terraform_version and resource_changes or planned_values (a
  terraform show -json artifact): not graded
NAMING-GATE: PASS 1 graded
CONTROL, THE SAME NAME IN AN AUTHORED JSON FILE: rc=1  on:2 mdpf-cottonwood-publisher-queue -> mdpf-cot-publisher-queue
  why: NEW and ALIAS as SQS_QUEUE: REFUSE; hand-kept carrier of 'cottonwood' outside every permitted context: read it through lookup('cottonwood')
NAMING-GATE: REFUSE 1 graded
VERDICT: PASS-PLAN-FILE-NOT-GRADED
```
rc=0. Confirms item 1 of the cell exactly: the plan file is SKIPped, and the authored JSON file carrying the
identical string is still REFUSEd with the canonical form.

### G1R-AC2, G1R-AC3, G1R-AC4 -- unaffected, re-run for completeness

Unchanged from the build: `VERDICT: PASS-REGISTRY-VALIDATED-FIRST` (rc=0, three arms: enforcing over a
`validate`-refused registry `NAMING ERROR ... regist...`, WARN mode the same error non-blocking, control over
the restored registry no error); `VERDICT: PASS-COMMIT-LIMB-READS-SCHEMA-MAP` (rc=0, schema's `tf_type_map`
found, 0 `aws_`-prefixed dict literals of >=10 keys in the gate); `VERDICT: PASS-G1-SUITE-HOLDS` (rc=0, 14 of
14 round-1 criteria).

## Controls (from the build; still valid, none touched the fixture)

- **Negative control, G1R-AC2:** the same three arms against the pre-edit gate (temporary swap, restored
  byte-for-byte) read `VERDICT: FAIL-REGISTRY-NOT-VALIDATED` -- the pre-edit limb never calls `validate()`
  and grades the broken registry normally.
- **Mutant, G1R-AC3:** a scratch copy with one 10-key `aws_*` dict literal reinserted reads
  `VERDICT: FAIL-COMMIT-LIMB-OWN-MAP`.
- **Determinism:** two same-input runs of `python .tools/naming-gate.py --diff <corrected-fixture-copy>
  --enforce`, byte-identical (cmp rc=0, 314 bytes each).

## Rows filed

- `LGIC_ENFORCE-W3-S10` (BLOCKING, ARMED, disarm `2.0.0_SA_COO~G`) -- the corrupt fixture, found this order.
- `LGIC_ENFORCE-W3-S11` (OBSERVATION, INERT, `disposition: GRADUATED`, `adjudicates: [LGIC_ENFORCE-W3-S10]`)
  -- disposes S10: the issuer's remedy landed at `6f640ead30`, independently re-verified above, G1R-AC1 now
  passes by output.

## Limits

- The schema read for `TF_NODE` degrades to an empty map on a read/parse failure rather than raising at
  import (required so `naming-apply-gate.py`'s plain `import` of this module, which never calls
  `main()`/`run()`, cannot crash on a broken schema); no criterion here exercises a missing/corrupt schema.
- `.scratch/` files used during the investigation (the negative control, the mutant, the header-corrected
  scratch copy of the fixture) were never committed, per CLAUDE.md; their exact commands are quoted in the
  proof-of-spec instance's `output_evidence`/`controls`.
