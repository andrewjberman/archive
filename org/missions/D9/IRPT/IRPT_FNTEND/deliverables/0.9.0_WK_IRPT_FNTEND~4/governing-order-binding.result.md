# FE-s-37 -- the governing order is the order being flipped

Order `IRPT_FNTEND.TO-FE-s-37` (decomp cell `FE-s-37`; 1.0.0_SA_CTO RULING S @942e4ff992 s.2; row IRPT_FNTEND-S61).
Worker `0.9.0_WK_IRPT_FNTEND~4`, branch `wk-irpt_fntend-6-4-fe-s-37` from CLOUD @62f3adb8ca. The code is at
**da3e61889d**, and every criterion ran on those committed bytes. Rows W4-S13 are at da3e61889d, and W4-S14 and
W4-S15 are in their own commit. This file, the instance and the status flip ride the flip commit.

## 1. What changed

**`.tools/to-pipeline-gate.py` -- `check_complete_flip`.**
- It runs `python .tools/proof-of-spec-check.py <instance> --governing-order <the flipped order>`. Before, it ran the
  checker on the instance alone.
- A refused flip now returns the verdict line plus each of the checker's `VIOLATION:` lines, up to 12 and then a
  count. Before, every refusal read `INVALID (rc=1)`, whatever refused it.
- Two self-test arms (72 arms, 0 failed).

**`.tools/proof-of-spec-check.py`.**
- `--governing-order <order.md>` (or `=<order.md>`) is lifted out of argv first, so the positional contract (one
  instance, then optional ids) is unchanged. An empty value, or a path outside the checker's tree, is
  `USAGE-ERROR (rc=2)`.
- `governing_binding_check` runs **first in `main()`**, before coverage, schema and every limb. When bound:
  - A `decomp_ref.to_ref` that normalises to a different file than the bound order raises one violation naming
    **both paths**.
  - A `to_id` the bound order does not answer to raises one violation naming the bound order, the id forms it
    answers to, and the tracked order(s) whose filename carries that id.
- `_resolve_governing_to` answers with the bound order **before it reads to_ref**, with the same missing and
  untracked handling to_ref had. Every limb resolves through it: alignment; surprises, via `_governing_is_tree`;
  invocation (limb 1, the placeholders reader); count-bar (limb 2) and drives (limb 3), via `_governing_rel`. So
  every limb reads the order being closed, and neither to_ref nor to_id is a source any more.
- Ten self-test arms, B1-B10 (42 of 42 behave).

**`.tools/tests/test_governing_binding.py`** (new). Its arms are in s.4 to s.6.

**How I read "REFUSED, before any limb runs".** The binding's violation is appended before any limb is called, and no
limb can remove it, so a refused instance reads INVALID whatever the limbs say. The limbs still **run** afterwards,
against the bound order, so their frames print. F37-AC6 and F37-AC7 read those frames on the doctored arm. None of
them can read to_ref.

## 2. The checker run from its CLI without a flipped order (UNBOUND)

**Behaviour.** Resolution is exactly today's: to_ref wins, else the to_id scan. The run prints, as its first frame:

    governing-binding: UNBOUND -- no --governing-order was given, so the governing order below is resolved from the
    instance's OWN decomp_ref.to_ref (else its to_id), fields the graded party writes. ...

**Not looser than today's.** No verdict changes unbound. Over all 36 committed IRPT_FNTEND instances the unbound and
bound runs read the same rc and the same violation set (s.3). An unbound run is simply **not protected** from its own
to_ref, and it says so. The battery shows it: the doctored instance, run unbound, still reads the to_ref order
(TO-FE-s-28) LEGACY for limbs 2 and 3, rc=0. That is S61 reproduced, with the UNBOUND frame printed. This order's own
validation step (`python .tools/proof-of-spec-check.py <instance> <ids>`) is an unbound run. The flip that closes the
order is bound.

## 3. Proof that the binding refuses no instance whose to_ref names its own order

**The committed IRPT_FNTEND corpus** (in the battery, every run):
- Scope: every `git ls-files` `*.proof_of_spec.json` under `org/missions/D9/IRPT/IRPT_FNTEND/deliverables/`, which is
  **36**. For each, its own order is `task-orders/<stem>.md`, the order `check_complete_flip` would bind.
- Each instance runs through the checker CLI **unbound** and **bound** (`--governing-order <own order>`).
- Results: 36 of 36 name their own order in to_ref; bound == unbound (rc and violation set) 36 of 36; refused by the
  binding **0 of 36**; each run prints its binding frame, 36 of 36. All 36 read rc=0 both ways.

**The estate, cross-check alone** (in-process `governing_binding_check`):
- Scope: every tracked order (`TO_PATH_RE`, **2619**) with an instance where `check_complete_flip` looks for one, on
  both roots. That is **335** orders.
- Result: refused **0 of 335**; 0 instances unreadable.

**Before the rule was written** (instance side, at 62f3adb8ca):
- 576 tracked instances, 337 with a sibling order.
- to_ref == that order in 336, absent in 1, naming another order in 0.
- An **exact** to_id match would refuse **119**: a slug on one side, or an order with no `<to_id>` tag.
- So to_ref is matched exactly and to_id slug-tolerantly. An id matches the bound order when:
  - it equals the order's `<to_id>`, its filename stem, or an `id="..."` declaration; or
  - one of the two is the other plus a `.`-delimited suffix, and the shorter carries `.TO`.
- Under that rule `...FE-s-2` never matches `...FE-s-29`, and a bare project code matches nothing (arms B5-B8). Row
  **IRPT_FNTEND-W4-S13**.

## 4. The flip path, on real bytes in a real git index (F37-AC3..AC7)

**The fixture.**
- A scratch repo under `<WS>/.scratch/fe-s-37-binding/` borrows this repository's object store
  (`objects/info/alternates`) and sits at the worktree's HEAD.
- It sparse-checks-out `.tools`, `org/standards`, `org/projects` and the project folder. So the ruling pins and every
  order's add commit resolve exactly as they do here.
- The worktree's current gate and checker bytes are copied in.
- One scratch commit returns FE-s-29 to just before its close: order `<status>pending</status>`, with the instance
  and its PENDING-THIS-COMMIT result file removed.
- Each arm then stages FE-s-29's **real** close, the shape of 6ad371c88e: order M, instance A, `checker-limbs.result.md`
  A. The FE-s-29 order is read by `git show HEAD:`, the FE-s-28 order by `git ls-files` + `git show`.
- Staging the result file is what keeps the replay from raising the PENDING-sentinel violation that S61 names for a
  copy.

**The arms** (identical in all three runs):

| arm | through | result |
|---|---|---|
| POSITIVE CONTROL, as committed | gate CLI, `check_complete_flip()`, bound checker | VALID: rc=0, `[]`, `VALID (rc=0)` |
| DOCTORED to_ref -> `IRPT_FNTEND.TO-FE-s-28.mandatory-placeholders.md` | gate CLI and `check_complete_flip()` | REFUSED, rc=1; the refusal names both paths; the binding is the checker's **only** violation |
| DOCTORED to_id -> `IRPT_FNTEND.TO-FE-s-28` (to_ref as committed) | gate CLI | REFUSED, rc=1 |
| BEFORE: the same doctored close under the tools S61 measured (checker @9e6ed6c236, gate @8aa00e60fb) | gate CLI | **ADMITTED (rc=0)**, so the refusal above is the binding's, and S61's "inferred" flip is now exercised |

**Frames.**
- Limb 1 on the doctored arm: `invocation-frame: governing TO=...TO-FE-s-29.checker-limbs.md; placeholders DECLARED
  ['WS'] -> ENFORCE`; 14/14 comparable rows match.
- Limbs 2 and 3, bound (as committed and doctored): 4 of 4 read `mode ENFORCE -- ...TO-FE-s-29... -> NEW`.
- Unbound doctored run: 2 of 2 read `...TO-FE-s-28... -> LEGACY` (the contrast).

## 5. The whole-suite census of record (F37-AC8)

- **Domain:** 63 `.py` files under `.tools/tests/`; 13 name `proof-of-spec-check` or `to-pipeline-gate`. The census
  runner itself is excluded **by name**, because running it inside itself would recurse. That leaves **12 run**.
- **Result: 12 of 12 green**: test_seeded_limb, test_count_bar_limb, test_gate_viii_modify, test_invocation_limb,
  test_mandatory_placeholders, test_output_vocabulary, test_placeholders_reader, test_proof_of_spec_alignment,
  test_proof_of_spec_artifact_resolution, test_proof_of_spec_cell_id_re, test_proof_of_spec_content_rung and
  test_proof_of_spec_decomp_ref_content.
- **Timing:** everything runs through one 8-worker pool, longest first. Wall time was 290 s (the F37-AC3..AC7 run)
  and 393 s (the F37-AC8 run), and test_seeded_limb alone took 312-391 s under contention.
- **Margin:** F37-AC3..AC7 carry `timeout 600`, so the margin is roughly 200 s, and it is set by test_seeded_limb
  (359 s alone at the cut). If that battery grows, the AC3..AC7 invocation times out before the AC8 one does.

**The limbs kept.** Neither tool's limb code was edited. The diff touches only `check_complete_flip`, the two self-test
lists, `main()`, the head of `_resolve_governing_to`, and the new binding block. Their batteries are in the 12:
- FE-s-29 limb 1, the line-anchored placeholders reader: test_placeholders_reader.
- Limb 2, count-bar: test_count_bar_limb.
- Limb 3, drives: test_seeded_limb.
- Limb 4, gate (viii) on a modify: test_gate_viii_modify.
- FE-s-36's gate (ix), output vocabulary: test_output_vocabulary.

**Outside the domain.** `org/standards/test_artifact_coverage_both_grammars.py` also runs the checker. It reads 3/6
PASS, rc=1, **both at 62f3adb8ca and with this change**, and the same arms fail (A, B, E). So it was red before this
change and is not counted in the 12. Row **IRPT_FNTEND-W4-S15**.

## 6. Every caller of the checker -- which are bound

Method: Grep for `proof-of-spec-check.py` over `*.py, *.sh, *.ps1, *.js, *.mjs, *.ts, *.cmd, *.bat` in the worktree.
That returns 64 files: 17 are this worker's own scratch, and 47 are in the corpus (15 in `.tools/`, 22 in `workflows/`,
10 in `org/`). Each hit was read at the call site.

| caller | runs the checker | bound |
|---|---|---|
| `.tools/to-pipeline-gate.py` `check_complete_flip` | on every staged terminal flip of a pipeline-registered order | **yes** (this change) |
| `.tools/receiving-check.py` (the L7->L8 route) | `[sys.executable, tp] + [p]` | no |
| 3.0.0_SA_CVO intake/audit scripts: `amgt_round5_cvo_audit.py:54,:84`, `amgt_round6_cvo_audit.py:41`, `amgt_round7_cvo_intake.py:80`, `amgt_round8_cvo_intake.py:107`, `posn_round3_cvo_intake.py:47` | `[sys.executable, '.tools/proof-of-spec-check.py', <instance>, <ids>]` | no |
| `org/standards/test_artifact_coverage_both_grammars.py:67` | a battery | no |
| the 12 `.tools/tests/` batteries | fixtures and the corpus | by design, as each needs |

The other 22 `workflows/` files and 4 `org/` files name the checker in comments, docstrings or emitted face text.

An unbound caller prints `governing-binding: UNBOUND` and is not protected from to_ref. That includes an instance
edited **after** its flip, because `check_complete_flip` grades only a commit that stages the order. Row
**IRPT_FNTEND-W4-S14**. A `.tools`-scoped census had found receiving-check.py alone. The unscoped read found the CVO's
scripts, and the row was corrected before it was minted.

## 7. Residuals, stated

- The L8 receiving side is unbound (W4-S14). The remedy is one argv-builder per caller: derive the sibling order from
  the instance path (the inverse of `check_complete_flip`'s search) and pass `--governing-order`. Those files are
  outside this grant, or are another seat's deliverables.
- to_id is a weaker cross-check than to_ref (slug-tolerant, W4-S13). The governing order no longer comes from either
  field, so neither can steer a limb.
- A pre-FE-s-37 checker paired with this gate reads `USAGE-ERROR (rc=2)`, which refuses the flip (fail-closed). The
  two ship in one commit.
- The gate's `REFUSED -- N violation(s)` count now includes the surfaced instance violations.
