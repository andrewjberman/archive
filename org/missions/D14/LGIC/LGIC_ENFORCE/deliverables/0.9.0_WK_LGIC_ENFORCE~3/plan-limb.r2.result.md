# Result -- LGIC_ENFORCE.TO-EN-t-2-r2 (the apply limb reads the plan)

Assignee: `0.9.0_WK_LGIC_ENFORCE~3` | Worktree: `wk-lgic-enforce-2c-3` | Artifact commit: `0af3c52597`

## What changed

`.tools/naming-apply-gate.py` grows a plan mode (`--plan-json FILE [--enforce]`) alongside its existing
pre-plan DIR mode:

- `_get_path(d, path)` reads a dotted own-name attribute out of a plan JSON object (the schema's map,
  via `naming-gate.py`'s `TF_NODE` -- item 4, never a map of this file's own).
- `_is_addition(change, attr)` -- `actions` includes `create`, or `update` whose own-name attribute's
  value changed between `before` and `after` -- is an ADDITION; everything else (no-op, a name-keeping
  update, a delete) is not.
- `judge_capped()` wraps `judge()` and downgrades any REFUSE-worthy grade to WARN (`refuses=False`) for a
  name this limb cannot confirm is new: every non-ADDITION plan resource, and every DIR-mode literal
  (pre-plan can't tell an addition from an existing resource either).
- `run_plan(path)` grades every managed `resource_changes` entry whose Terraform type the schema's map
  covers: `judge()` (may REFUSE) for an ADDITION, `judge_capped()` (WARN only) for everything else.
- `_main_dir()` (the old `main()` body) now grades every literal with `judge_capped()`, so `refused` is
  structurally always 0 -- DIR mode can never refuse -- and its denominator line prints
  `<n> expression(s) deferred to plan` in the exact phrasing the checker's `\b2 expressions? deferred to
  plan\b` regex requires.
- `_main_plan()` prints `NAMING <verdict> <address> <name> -> <canonical>` per graded name, then
  `NAMING-PLAN: <PASS|WARN|REFUSE> <n> graded`; a REFUSE exits 1 enforcing, 0 otherwise.

`.tools/safe-apply.sh` gets one new stage, right after the existing pre-plan naming stage and before the
tag-authorization gate: it renders the plan it is about to run (`terraform plan -out=...` then
`terraform show -json ...`, reusing the already-computed `NAPPLY_TREE`/`NAPPLY_ENFORCE`), grades it with
`naming-apply-gate.py --plan-json`, and on a REFUSE while enforcing prints `safe-apply: BLOCKED by the
naming plan limb ...` and exits 7 -- before tag-authz, tombstone, or the real `terraform apply` ever run.
WARN mode never changes the exit code, matching the existing pre-plan stage's own contract.

## Acceptance

| id | invocation (subcommand) | expect | result |
|---|---|---|---|
| T2R-AC1 | `t2r-create-literal` | `VERDICT: PASS-CREATE-REFUSED-WITH-CANONICAL` | PASS |
| T2R-AC2 | `t2r-create-expression` | `VERDICT: PASS-EXPRESSION-REFUSED-AT-PLAN` | PASS |
| T2R-AC3 | `t2r-rename` | `VERDICT: PASS-RENAME-REFUSED` | PASS |
| T2R-AC4 | `t2r-existing` | `VERDICT: PASS-EXISTING-ONLY-WARNS` | PASS |
| T2R-AC5 | `t2r-correct` | `VERDICT: PASS-CORRECT-CREATE-PASSES` | PASS |
| T2R-AC6 | `t2r-deferred` | `VERDICT: PASS-DEFERRED-COUNT-PRINTED` | PASS |
| T2R-AC7 | `t2r-wired-blocks` | `VERDICT: PASS-WIRED-PLAN-LIMB-BLOCKS` | PASS |
| T2R-AC8 | `t2r-wired-passes` | `VERDICT: PASS-WIRED-PLAN-LIMB-PASSES` | PASS |

8 of 8 mechanical criteria PASS by output, both on the pre-commit working tree and re-run at the committed
artifact `0af3c52597`, identical VERDICT lines both times.

## Controls

Two hand-built scratch-copy mutants (`.scratch/mutant/`, never touching the read-only fixtures) flip only
the field `_is_addition()` reads: a bad-name CREATE turned into a no-op flips REFUSE -> WARN (rc 1 -> 0
enforcing); a bad-name no-op turned into a CREATE flips WARN -> REFUSE (rc 0 -> 1 enforcing). Both fired
exactly as predicted, confirming the ADDITION/non-ADDITION branch genuinely discriminates rather than
being a decoration. Determinism: two back-to-back runs of the same `--plan-json` invocation produced
byte-identical stdout+stderr and rc.

## Proof of spec

`python .tools/proof-of-spec-check.py
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/LGIC_ENFORCE.TO-EN-t-2-r2.plan-limb.proof_of_spec.json
T2R-AC1,T2R-AC2,T2R-AC3,T2R-AC4,T2R-AC5,T2R-AC6,T2R-AC7,T2R-AC8` -> `VALID (rc=0)`, `violations=0`,
2/2 artifacts CONTENT-resolved at `0af3c52597`, 0 surprises declared (none filed -- nothing in this cell
required an override or hit a missing path).

## Surprises

None filed. Every fixed input matched the cell's own description, no path outside the granted `<paths>`
was needed, and no criterion asked this worker to plan or apply anything real.

## Status

Every mechanical criterion (T2R-AC1..AC8) PASSES by output. `<status>` flips to `complete` in the same
commit as this result file and the proof instance.
