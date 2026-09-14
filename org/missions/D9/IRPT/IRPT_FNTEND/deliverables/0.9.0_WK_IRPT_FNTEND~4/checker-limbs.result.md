# IRPT_FNTEND.TO-FE-s-29 -- the checker limbs: result

**Worker:** `0.9.0_WK_IRPT_FNTEND~4` | **Branch:** `wk-irpt_fntend-5-4-fe-s-29` (from CLOUD @8666e6701e) |
**Code commit:** `9e6ed6c236` (8 files, 1871 insertions, 27 deletions) | **Push state:** LOCAL |
**Instance:** `IRPT_FNTEND.TO-FE-s-29.checker-limbs.proof_of_spec.json` (beside this file)

All four limbs landed on the fabric's two grading instruments in one commit. Every mechanical criterion,
F29-AC1 to F29-AC14, passed on its bar when run exactly as written on the committed bytes. F29-AC15 is a
judgment criterion; it is recorded here without a verdict and is 3.0.0_SA_CVO's to grade at L9.

## What landed

| Limb | Ruling | Where | Behaviour |
|---|---|---|---|
| 1. Line-anchored `<placeholders>` reader | 1.0.0_SA_CTO RULING M(i) @23af9479ab; rows S53, W4-S7 | `PLACEHOLDERS_TAG_RE` in BOTH `.tools/to-pipeline-gate.py` and `.tools/proof-of-spec-check.py` | `^[ \t]*<placeholders>(.*?)</placeholders>[ \t]*$` with `re.M`. The element must stand on its own line. The two patterns are byte-identical, and both batteries compare them. |
| 2. Count-bar limb | RULING M(ii) @23af9479ab; row S56 | `count_bar_check()` in the checker | A PASS whose zero-count bar matches its evidence is refused if the evidence also carries a NONZERO count of that noun. ANSI escapes are stripped before counting, counts are left-anchored with `(?<![0-9.])`, never `\b`, and a count after `of ` is treated as a denominator. |
| 3. Drives (seeded-criterion) limb | RULING Q + the CTO's condition @4f6c7abc7b; rows S42, C-S67 | `drives_check()` in the checker | Every criterion of a new IRPT_FNTEND order must declare `drives="network"` or `drives="none"`. A `drives="network"` PASS is refused if its invoked `bun test` file, or a `__tests__` helper it imports, names a seeding `initial*` prop in code. It is also refused if that file cannot be read at all. |
| 4. Gate (viii) on a modify | Andrew-direct card 6, record @e2210bf34c | `_staged_modified()`, `_head_blob()` and `_placeholder_modify_violations()` in the gate; `main()` wired | A tree order staged as MODIFIED is graded only if it already declares `<placeholders>` at HEAD. The staged bytes are read from the index. The module docstring's PROSPECTIVE ONLY paragraph and `_newly_added`'s docstring state the exception and its authority. |

## The boundary chosen for limbs 2 and 3, and its NON-APPLICATION

**NEW vs LEGACY is derived from repository state.** An instance is NEW when its governing order was first
added in a commit that descends from the commit that recorded the ruling:
- limb 2 uses `23af9479ab`, the round-4 analysis carrying RULING M;
- limb 3 uses `4f6c7abc7b`, the commit that introduced the MANDATORY drives condition (its parent does not carry it).

Two git calls read this. `git log --full-history --diff-filter=A` finds the order's earliest add commit, and
`git merge-base --is-ancestor <pin> <add>` tests it against the pin. No clock, no list of instances, and no
declaration the graded party writes. Once an order lands its add commit is fixed, so:
- an issuer cannot reach the legacy side by omitting the drives declaration (F29-AC10: FE-s-29 with every `drives=` removed is still ENFORCE and still refused);
- a worker cannot reach it through anything written in the instance.

The batteries check both pins against the ruling's text.

Measured sides at the cut:
- **NEW:** round 5, FE-s-29 through FE-s-36, all added at b4d1b8bfef, which descends from both pins.
- **LEGACY:** round 4 (b6062ad2a2) and every earlier round, none of which descends from either pin.

Limb 3's mandatory declaration is scoped to IRPT_FNTEND, the project the condition names
(`DRIVES_RULING = {"IRPT_FNTEND": "4f6c7abc7b"}`). Other projects' drives declarations are read but never
required.

**NON-APPLICATION.** The boundary is UNREAD, and the limb only ANNOUNCES and names why in its frame, in three cases:
- the governing order does not resolve;
- git cannot name the order's add commit;
- the ruling pin is not in this object store (a cross-fabric reader before a fetch).

## Per criterion (deciding line; full evidence in the instance)

| Criterion | Deciding line | Verdict by output |
|---|---|---|
| F29-AC1 | `[to-pipeline-gate --self-test] RESULT: 0 arm(s) failed of 59` (51 at the cut) | PASS |
| F29-AC2 | `RESULT: 32 of 32 arm(s) behaved` (18 at the cut; +7 count-bar, +7 drives) | PASS |
| F29-AC3 | `LINE-ANCHORED READER, BOTH READERS: 5 of 5 cases behave as S53 measured ...` | PASS |
| F29-AC4 | `READERS BYTE-IDENTICAL: yes (...)` | PASS |
| F29-AC5 | `CONTRADICTING COUNT, NEW INSTANCE: REFUSED 2 of 2` | PASS |
| F29-AC6 | `GENUINE ZERO ADMITTED: 3 of 3` | PASS |
| F29-AC7 | `CONTRADICTING COUNT, LEGACY INSTANCE: ANNOUNCED, 0 violations (F17-AC8, ...)` | PASS |
| F29-AC8 | `SEEDED CRITERIA REFUSED: 6 of 6 (F10-AC5, F10-AC10, F26-AC7, F5-AC2, F5-AC3, F5-AC4)` | PASS |
| F29-AC9 | `BROWSER CRITERIA ADMITTED: 2 of 2 (F19-AC4, F19-AC5; ...)` | PASS |
| F29-AC10 | `NEW INSTANCE, CRITERION DECLARING NEITHER: REFUSED (...)` and `LEGACY ROUND-4 INSTANCES: 5 of 5 ANNOUNCED with 0 violations` | PASS |
| F29-AC11 | `MODIFIED DECLARING ORDER, BROKEN DECLARATION: REFUSED 4 of 4 (...)` | PASS |
| F29-AC12 | `MODIFIED ORDER WITHOUT THE ELEMENT: NOT GRADED (...)` | PASS |
| F29-AC13 | `EXISTING CORPUS STILL COMMITTABLE: 2613 task-order files tracked ...` / `26/26` | PASS |
| F29-AC14 | `BATTERY PASS -- conformant reads VALID, ...` / `35/35` | PASS |
| F29-AC15 | judgment | RECORDED, no verdict (3.0.0_SA_CVO at L9) |

How the controls were built. Every input is a real shape.
- **Limb 1** uses S53's five cases from `git show HEAD:` bytes. Case C splices in the first committed `<PORT>`
  criterion whose real row matches it exactly under full expansion (F11-AC4). Case D quotes the gate's own
  emitted refusal text for FE-s-27.
- **Limb 2** runs bun itself on a scratch suite of ten failing tests.
- **Limb 3** reads the suites the criteria actually invoke.
- **Limb 4** runs in real git indexes through the gate's own CLI.

A refusal counts only when the case could have gone the other way:
- Limb 1's cases count only where the OLD reader gave S53's verdict in the same run.
- Limb 2's refusals count only where the bar's own `re.search` matches and `conditional_checks()` raises nothing.

## Controls

**Mutants.** Each limb was disabled in-process (`.scratch/mutant.py`; no committed file touched), and its battery went red:
- limb 2: `REFUSED 0 of 2`, 6 of 9 arms, rc=1;
- limb 3: `SEEDED CRITERIA REFUSED: 0 of 6`, 12 of 18, rc=1;
- limb 4: `RESULT: 1 arm(s) failed of 59`.

Limb 1's mutant is built into its battery. The old reader ADMITS cases C and D and reads 367 names from
FE-s-28's face, which reproduces S53 and W4-S7.

**Determinism.** Every battery ran at least twice on unchanged bytes and gave identical deciding lines.

## Rows filed (INVESTIGATION_v2.md, 68 insertions, 0 deletions)

- **IRPT_FNTEND-W4-S8** (OBSERVATION, INERT). The line-anchored reader turned FE-s-28's battery red, at
  `DECLARED NEW TO ADMITTED: 1 of 3`. The cause was the battery's `_declare` fixture: it put the element
  mid-line, after a prose mention of `<paths>`, in 2 of its 3 specimens. No real order was the cause: all 10
  declaring orders write the element on its own line and are admitted. The fixture was corrected; the
  pattern was not changed. So this is NOT the BLOCKING case the bounds name.
- **IRPT_FNTEND-W4-S9** (OBSERVATION, INERT). CLAUDE.md Rule 27's L4-R clause quotes the `_newly_added`
  sentence that limb 4 amended. CLAUDE.md is outside this order's grant. What the clause says about limb 6
  remains true.
- **IRPT_FNTEND-W4-S10** (OBSERVATION, INERT). The drives limb reads ten seeding props, not the three named:
  15 declared `initial*` props minus 5 UI-state ones. Under the ten, one more committed criterion would be
  refused if it were declared network: F15-AC7, via `job-states.test.ts:78 initialJob`. All six AC8 criteria
  are refused on a ruled prop alone, so AC8 does not depend on this choice.

## Named weaknesses (for L9 and for the issuer)

1. **Limb 2 reads only count-before-noun bars** (`0 fail`, `0 arm(s) failed`, `0 errors`). Key=value bars such
   as `rc=0` and `LEAKS: 0` are out of scope: 123 distinct such bars exist estate-wide, and the ruling names
   count nouns. Widening this is the CTO's call.
2. **Limb 3 refuses a `drives="network"` PASS whose invoked test cannot be read here** (fail-closed). The
   worker's own run reads its portal worktree. A re-run from a tree where neither the recorded directory nor
   this tree's portal nor the main worktree's portal carries the file would refuse. The refusal says to run
   the checker where the portal worktree exists.
3. **Limb 3 follows relative imports only into `__tests__` directories**, and it does not read an invocation
   that runs no `bun test`. Both cases are counted in the frame.
4. **Limbs 2 and 3 rely on the governing order resolving.** An instance whose `to_id` / `to_ref` names no
   committed order has an UNREAD boundary and only ANNOUNCES. Every older limb in this checker has the same
   dependency.
5. **The seeded battery is the slowest criterion.** It took 137 s of its 300 s bound when run beside seven other
   criterion runs. Most of that is its unscoped census over 159 file-naming bun-test criteria.

## What the issuer may want to amend

Nothing in the order had to be refused. Three items are carried forward:
- **W4-S9:** CLAUDE.md's quoted docstring sentence, for whoever owns that text.
- **W4-S10:** the seed-prop set, which is L9's to confirm or narrow.
- **Weakness 1:** limb 2's NON-APPLICATION for key=value bars.
