# FE-s-23 -- the checker's invocation-comparison limb

`0.9.0_WK_IRPT_FNTEND~3` on `IRPT_FNTEND.TO-FE-s-23`, worktree `/c/tmp/wk-irpt_fntend-3-3-fe-s-23`
(branch `wk-irpt_fntend-3-3-fe-s-23` from CLOUD `9762d5b8a3`, WORKSPACE ONLY -- no portal pair, none
created). Work commit `d2c4c6fafb`. Push state: **LOCAL** (nothing pushed; `git push` never run).

---

## 1. WHAT WAS BUILT

`invocation_alignment_check()` in `.tools/proof-of-spec-check.py`, wired into `main()` beside the
surprises limb so it runs on **every** instance and prints its denominator whether or not anything
diverged.

Per acceptance row it compares the instance's recorded `invocation` against the same-id criterion's
`<invocation>` in the **governing task order**. Normalisation is exactly the two operations the cell
names -- declared placeholder expansion, and whitespace at the ends of the string. A difference in a
flag, a path, a query parameter or a quoted argument is a divergence, reported with **both strings and
the criterion id**. Two properties worth stating because they are what make the rule safe rather than
merely strict:

- a placeholder expands to `\S+`, which **cannot cross whitespace or a newline**, so an expansion can
  never swallow an added flag, an added argument or an appended query parameter -- the literal tail
  would then have nothing to match;
- a **repeated** placeholder is a **backreference**: `<WS>` twice in one command must expand to one
  value, so two different workspaces in one invocation cannot pass as one substitution.

`--self-test` grows from 12 arms to 18 (M-R), and every new arm description names the limb, which is
what makes it discoverable without reading the source.

## 2. THE ONE DESIGN DECISION THE CELL DID NOT SPECIFY, AND THE MEASUREMENT THAT FORCED IT

The cell says two things: *"A mismatch is a VIOLATION"* and *"THIS LIMB MUST NOT BREAK THE EXISTING
CORPUS."* **Measured before the limb was written, over the whole repo, unscoped:**

| quantity | value |
|---|---|
| committed proof-of-spec instances | 294 |
| with a governing TO under the tree root | 275 (18 flat, 1 unresolved) |
| acceptance rows | 1481 |
| comparable rows (criterion carries an `<invocation>`; row names a real criterion) | 874 |
| **rows that DIVERGE under the cell's own normalisation** | **318** |

The dominant shapes are **honest**: a worker adding the `timeout 120` bound the order's BOUNDS section
demanded while the criterion's `<invocation>` omitted it; a record eliding a long path to `.../x.txt`.
Refusing by default would retro-invalidate work across every project in the estate and refuse
**in-flight completion flips in projects this cell does not own** -- widening far past one cell.

So the two clauses are **jointly unsatisfiable at the default**, and the axis the cell left unspecified
-- enforcement **scope** -- is where the conflict was resolved. **The normalisation was not touched.**

    ENFORCE  iff the governing TO declares  <placeholders>WS, PORT</placeholders>   -> VIOLATIONS
    ANNOUNCE otherwise                                                              -> the IDENTICAL
                                                                                       diagnostic, both
                                                                                       strings, refuses
                                                                                       nothing

This is the shape of the existing `<owned_cells>` opt-in (CTO 66893): a declaration that turns an
announce into an assertion, because the undeclared form is a *guess* and a guess must not refuse.
Census before choosing the token: **0 of 2554** task-order files carry `<placeholders>`, so nothing in
the estate is retro-enforced by construction.

**NAMED WEAKNESS, not hidden:** the opt-in is written by the **issuer**, and the issuer is the party
whose prompt-only correction this limb exists to catch. **Detection is unconditional; refusal is
conditional.** Making the declaration mandatory at the L6 gate is the only thing that makes refusal
unconditional, it is outside this order's `<paths>`, and it is filed as **`IRPT_FNTEND-W3-S14`**,
`ARMED`, `disarm_owner 2.0.0_SA_COO~F`.

## 3. THE CELL'S PREMISE IS FALSE, AND THE GREEN SAYS SO ON ITS OWN LINE

The cell asserts *"Round 2's instances are honestly aligned and must stay VALID."* They are not all
aligned. **5 of 7** are clean; two are not, and both are printed by name with both strings by the
battery's census arm, immediately beneath the 7-of-7 line:

| cell | criterion | task order says | record says |
|---|---|---|---|
| FE-s-18 | `F18-AC17` | `... timeout 120 ... bun test src/pages/InvestorReporting` | `... timeout 180 ...` |
| FE-s-12 | `F12-AC5` | `... \| wc -l)"` | `... \| wc -l)` (closing quote dropped) |

`F18-AC17` is **S31's own class, in the very instance S31 was raised about, surviving the record fix**.
`F12-AC5` leaves the field the schema calls *"re-runnable by a verifier"* holding an unbalanced shell
command. Under a TO declaring `<placeholders>` **both would be REFUSED**; they read VALID today only
because the announce branch applies to them.

**Neither instance was edited and the normalisation was not widened by one character** -- the order
forbids both in terms. Filed as **`IRPT_FNTEND-W3-S13`**.

So read `ROUND-2 CORPUS STILL VALID: 7 of 7` narrowly: it is a statement about the **verdict**, never
about alignment. The battery prints `ROUND-2 STRICT DIVERGENCE CENSUS: 2 row(s) across 2 of 7
instance(s)` directly under it so the number cannot be lifted out and quoted wider.

## 4. CRITERIA

Every invocation below was **extracted from the committed task order and run with only `<WS>`
substituted**, so the string recorded in each acceptance row *is* the string that ran -- this cell's
own discipline, applied to itself.

| id | verdict | deciding line | denominator |
|---|---|---|---|
| F23-AC1 | PASS-by-output | `RESULT: 18 of 18 arm(s) behaved` | 18 arms: 12 pre-existing + 6 added (M-R) |
| F23-AC2 | PASS-by-output | `DIVERGENCE CAUGHT: 4 of 4` | 4 mutants x 3 assertions (refuses once, names the id, carries both strings) |
| F23-AC3 | PASS-by-output | `PLACEHOLDER EXPANSION TOLERATED: 3 of 3` | 3 substitution-only pairs, plus ANTI-BRICK 3 of 3 |
| F23-AC4 | PASS-by-output | `ROUND-2 CORPUS STILL VALID: 7 of 7` | 7 committed instances via the CLI; census beside it: 2 of 7 carry a printed divergence |
| F23-AC5 | PASS-by-output | `VALID (rc=0)` | 1 instance, 14 rows, 14 ids, 0 violations; limb reads 13/13 comparable aligned |
| F23-AC6 | PASS-by-output | 6 arm lines + the battery header name the limb | 7 of 18 self-test lines name it |
| F23-AC7 | **RECORDED (judgment)** | no verdict -- graded by `3.0.0_SA_CVO` at L9 | see the instance row |

## 5. THE TWO VALIDATIONS THE ORDER ASKED FOR, AND WHY THEY ARE NOT THE SAME STRENGTH

**(a) With the limb active.**
`python .tools/proof-of-spec-check.py <this instance> F23-AC1,...,F23-AC7` -> `VALID (rc=0)`,
`violations=0`, and the frame reads
`invocation-frame: ... placeholders DECLARED ['WS'] -> ENFORCE` /
`invocation-alignment: 6/6 comparable row(s) match modulo placeholder expansion; 0 diverge`.
This instance is the **first in the estate graded on the ENFORCE branch**, which is the whole reason
the single `<placeholders>WS</placeholders>` line was added to this order (disclosed,
**`IRPT_FNTEND-W3-S16`**, reversible in one line).

**(b) And that oracle is WEAKER than F23-AC4's, stated plainly.** This instance is graded **by the tool
this order changes**, so the two are not independent: a limb that silently did nothing would still
return `VALID` here, and (a) could not tell the difference. What discriminates is elsewhere and is
cited, not assumed:

- `F23-AC4` reads **real committed bytes** of seven instances nobody here wrote, through the checker's
  **own CLI** -- a different instrument from the in-process function calls every fixture arm uses;
- the limb **separates** those seven into 5 clean and 2 divergent rather than passing or refusing all
  seven, which no inert limb and no refuse-everything limb can do;
- the **ANTI-BRICK** arm shows the three tolerated pairs *diverge* when the declaration is removed, so
  the tolerance is the declaration and not an accepting limb;
- the five sibling `test_proof_of_spec_*` batteries re-run green at this commit (alignment 35/35,
  artifact_resolution, cell_id_re, content_rung 9/9, decomp_ref_content 24/24), so the new limb did not
  buy its own green by loosening someone else's.

## 6. ROWS FILED (none edited after landing)

| id | class / hazard | what |
|---|---|---|
| `IRPT_FNTEND-W3-S13` | OBSERVATION / INERT | the cell's "honestly aligned" premise is false -- 2 of 7, both strings each |
| `IRPT_FNTEND-W3-S14` | OBSERVATION / **ARMED**, `disarm_owner 2.0.0_SA_COO~F` | 318 of 874 estate-wide; why ENFORCE is opt-in; the opt-in's named weakness |
| `IRPT_FNTEND-W3-S15` | OBSERVATION / INERT | correction to this order's own preflight: `--help` returns **rc=2**, not rc=0 |
| `IRPT_FNTEND-W3-S16` | OBSERVATION / INERT | disclosed: the one `<placeholders>WS</placeholders>` line added to this order's own file |

## 7. NOT DONE, DELIBERATELY

- **No `--help`** -- the order says it is a different cell's business. The docstring now states no
  `--help` exists and that an unrecognised single argument is read as an instance path.
- **No `<placeholders>` mandate at the L6 gate** -- outside `<paths>`; `W3-S14` carries it.
- **No edit to any existing proof instance**, and **no widening of the normalisation** -- the order
  forbids both, and the two divergent rows are reported rather than smoothed.
- **No portal worktree, no portal path, nothing staged under `portal/`.**
