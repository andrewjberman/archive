# FE-s-28 -- the `<placeholders>` declaration is MANDATORY at L6

`0.9.0_WK_IRPT_FNTEND~4` on `IRPT_FNTEND.TO-FE-s-28` | worktree `/c/tmp/wk-irpt_fntend-4-4-fe-s-28`
(branch `wk-irpt_fntend-4-4-fe-s-28`, cut at `f3b42b1e0b`) | build commit `d0c28a59be` | **LOCAL, not pushed**

**STATUS: COMPLETE -- flipped after the issuer's re-cut.** At `946fa17409` seven of eight mechanical
criteria passed by output and `F28-AC6` did not, because its bar (`0 fail`) was a string its instrument never
prints (section 4). The issuer (`2.0.0_SA_COO~F`) re-cut that one bar at `9ab6043728` to `BATTERY PASS`. The
criterion was re-run exactly as now written -- EXIT=0, `proof-of-spec alignment battery: 35/35 arms as
expected`, `BATTERY PASS ...` -- and every mechanical criterion now passes by output.

---

## 1. THE BOUNDARY, AND WHY IT IS THE RIGHT ONE

**The rule as shipped:** `.tools/to-pipeline-gate.py` GATE (viii) refuses a task order **STAGED AS ADDED**
(git status `A` or `R`) under `org/missions/D<n>/<MACRO>/<CODE>/task-orders/` when it carries no
`<placeholders>` element, carries an EMPTY one, or declares a set that does not cover a `<TOKEN>` its own
`<invocation>` strings use. It does **not** bind a MODIFICATION of an existing order, and it does **not**
bind the flat-root `org/**/task_orders/` population.

**Measured before it was chosen** (the cell's instruction), at `f3b42b1e0b` over 33,337 tracked paths using
the gate's own `TO_PATH_RE`:

| population | count |
|---|---|
| task-order files tracked | **2559** |
| tree orders (`org/missions/D*/*/*/task-orders/`) | 305 |
| flat-root legacy (`org/**/task_orders/`) | 2254 |
| carrying `<placeholders>` | **2** (`TO-FE-s-23`, which invented the element; `TO-FE-s-28`, which mandates it) |
| tree orders lacking it, never graded under this boundary | 303 |

The cell says 0 of 2554. That is 2 of 2559 today; the drift is filed as `IRPT_FNTEND-W4-S6` and **every
number in the refusal text, in the gate's block comment and in the battery's census line is the re-measured
one**, never the inherited one.

**Why this boundary and not another.** Three candidates existed and two were rejected on their mechanics,
not on their results:

1. **Grade the corpus.** Refuses 2557 files nobody can now edit. The gate's own header records what happens
   next -- a gate that refuses wholesale is routed around wholesale.
2. **Grandfather by DATE, or by an allow-list of projects.** This is the opt-in again wearing a new name: it
   drifts silently the moment the date passes or a project is added, and it needs a SECOND vintage carrier
   that can disagree with the first.
3. **Bind what an issuance ADDS** -- chosen. It is the cell's own words ("The refusal must bind what an
   issuance ADDS"), and it **adds no new mechanism**: `main()` already sends only newly-added (`A`/`R`) paths
   through `check_file`, and `_newly_added`'s docstring already states the contract ("A modification (M) does
   not: this gate never refuses an existing TO"). One vintage carrier, already tested, nothing new to drift.

**It is stated where a seat will meet it.** The refusal text carries the boundary and the fix, because the
cell requires it and because a fail-closed gate that cannot teach its own rule turns into a `--no-verify`.

**It was not chosen to make the tests pass, and there is a discriminator for that claim:** the boundary is
proved end-to-end with **IDENTICAL BYTES in two git states inside ONE gate run** -- refused as an ADD,
admitted as a MODIFY. A boundary reverse-engineered from a test would not have needed the positive control
sitting in the same run as the negative one.

**The circularity the BOUNDS name is resolved, not special-cased.** This order's own face is part of the
corpus; it declares `<placeholders>WS</placeholders>`; its invocations carry only `<WS>`; the limb ADMITS it
and the battery asserts that on the real bytes. There is no self-exemption anywhere in the limb.

**What the boundary does NOT reach, stated so the L9 grade is not owed a discovery:** 303 tree orders and
2254 flat-root orders carry no declaration and never will, so `proof-of-spec-check`'s invocation-alignment
limb stays in ANNOUNCE for every instance governed by them. This makes the declaration unavoidable
**prospectively**. It does not retro-arm the estate and nothing here claims it does.

## 2. WHICH ORACLE IS THE STRONGER ONE -- AND THE CONFLICT OF INTEREST, STATED

⚠ **This instance is graded by `.tools/proof-of-spec-check.py`, whose sibling gate this order changed.** The
two files are different tools, but they now read the SAME element with byte-identical regexes, by design --
so a reader is entitled to ask whether the proof and the subject are independent.

**They are not fully independent, and the ranking of the evidence says so:**

- **STRONGEST: `F28-AC4`'s real-corpus, end-to-end arm.** Real committed task-order bytes, a real git index,
  the gate's own CLI, and the boundary decided by two git STATES of identical content. Nothing in that arm
  is a fixture, and nothing in it is graded by the tool under discussion.
- **NEXT: `F28-AC2`/`F28-AC3`.** Also real bytes and the real CLI, with the delta attributed by a
  byte-identical comparison of every OTHER refusal line across the two runs.
- **WEAKEST: `F28-AC1`/`F28-AC7`, the self-test.** It is the subject grading itself, in-process, on strings
  the limb's own author chose. It is worth running -- it is how a regression is caught cheaply -- but it is
  the arm that would survive a limb that was subtly wrong, which is exactly why the mutant control below
  exists and why the corpus arm is the one to lean on.

**The anti-brick control, run and recorded** (a passing assertion never mutated has never been tested): with
the limb's refusal branch disabled, the battery reports `UNDECLARED NEW TO REFUSED: 0 of 3`, withholds the
boundary line entirely and prints `REFUSAL TEXT INCOMPLETE` (12/18 arms, rc=1); the gate's self-test reports
`10 arm(s) failed of 51` against a clean-copy control's 7, i.e. **exactly 3 placeholders arms flipped**. The
first cut of that control did NOT behave -- the battery died with a traceback instead of scoring -- and the
limb call is now wrapped so a raise becomes a scoreable FAIL. A fixture that cannot represent the failure
cannot score it.

## 3. WHICH BATTERY `F28-AC6` NAMED, AND WHICH WERE RUN

The criterion allows for the battery being named differently ("run the battery that exists and say which in
the result file"). **The named file exists**, so the fallback does not apply -- but both of FE-s-23's
batteries were run and both are recorded:

| battery | rc | summary | contains `0 fail`? |
|---|---|---|---|
| `.tools/tests/test_proof_of_spec_alignment.py` (named by the criterion) | 0 | `proof-of-spec alignment battery: 35/35 arms as expected` / `BATTERY PASS ...` | **no** |
| `.tools/tests/test_invocation_limb.py` (FE-s-23's own, by TO name) | 0 | `invocation-limb battery: 17/17 arms as expected` / `BATTERY PASS ...` | **no** |

Denominator: **2 of 2 candidate batteries PASS; 0 of 2 emit the bar string.** Nothing this order built broke
FE-s-23's limb.

## 4. WHY `F28-AC6` WAS FIRST RECORDED `FAIL` -- RESOLVED BY THE RE-CUT AT `9ab6043728`

> **Resolution:** the issuer re-cut the bar to `<expect>BATTERY PASS</expect>` at `9ab6043728` (a one-line diff
> of the order file; no other criterion changed). Re-run as written: EXIT=0, `35/35 arms as expected`,
> `BATTERY PASS ...` -> **PASS by output**. The text below is the record of the refusal as it stood at
> `946fa17409`, kept because the row (`IRPT_FNTEND-W4-S5`) cites it.

`F28-AC6`'s `<expect>` is the pattern `0 fail`. The battery's only summary writer
(`.tools/tests/test_proof_of_spec_alignment.py@f3b42b1e0b:455-462`) prints `{n}/{N} arms as expected` and
then either `BATTERY PASS ...` (rc 0) or `BATTERY FAILED -- the gate does not behave as specified.` (rc 1).
**Neither branch, and no per-arm line, contains the substring.** So no run of the invocation the criterion
names -- clean or dirty -- can match the bar the criterion names. The criterion's SUBSTANCE is met and its
BAR is unsatisfiable, and those are different things.

This is the same defect the issuer caught and corrected on `F28-AC1` *before issuing* ("this tool does NOT
print the same shape as `proof-of-spec-check` ... Never assume two tools in `.tools/` report alike"), one
criterion later. Filed as `IRPT_FNTEND-W4-S5`.

⛔ **What was NOT done, and it is the tempting repair:** `test_proof_of_spec_alignment.py` sits inside this
order's `<paths>` grant. A one-line edit to its summary would have made the bar match and the order close.
Editing an instrument so that a bar fits it grades the tool instead of the world, and the BOUNDS say a real
trip of a boundary is a FINDING, never an edit. The battery is unchanged. **The repair is the issuer's:**
re-cut the bar to something the instrument emits (`arms as expected`, or `BATTERY PASS`).

## 5. ROWS FILED

| id | class / standing | one line |
|---|---|---|
| `IRPT_FNTEND-W4-S5` | BLOCKING / INERT | `F28-AC6`'s bar matches no output its instrument can emit; the battery passes (35/35, rc=0) and the criterion still cannot PASS by output. |
| `IRPT_FNTEND-W4-S6` | OBSERVATION / INERT | The cell's `0 of 2554` is **2 of 2559** at `f3b42b1e0b`; conclusion unchanged, every shipped number re-measured. |
| `IRPT_FNTEND-W4-S7` | OBSERVATION / **ARMED** (`disarm_owner 2.0.0_SA_COO~F`) | A PROSE mention of `<placeholders>` before the real element swallows everything between: on this order's own face the checker reads **367 names instead of 1**, and all 367 become wildcards under ENFORCE. Measured INERT here (the invocations carry only `<WS>`; the minimal set `{WS}` gives the same 7/7 match, 0 diverge) and left ARMED for the next order. |

`W4-S7` is the one to read twice: it is the same class the sibling `<paths>` limb already fixed with a
line-anchored regex (`PATHS_BLOCK_RE`, "94157 gap (a)"), rediscovered on the element that arms the alignment
check itself. **GATE (viii) mirrors the defect deliberately** -- byte-identical readers are what stop the
gate admitting an element the checker cannot see -- so the gate neither worsens it nor fixes it, and the
checker is outside this order's write surface. The obvious repair (require the block form) would refuse the
INLINE one-line element that both declaring orders use today, so the bounded fix is a cut, not a worker act.

## 6. THE RECORD

- Build commit `d0c28a59be` -- `.tools/to-pipeline-gate.py` (+119), `.tools/tests/test_mandatory_placeholders.py`
  (+353, new), `INVESTIGATION_v2.md` (+44). 3 files, 516 insertions, 0 deletions, read from `git show --stat`.
- `--self-test`: `RESULT: 0 arm(s) failed of 51` (42 before this order; 9 added, 5 RED and 4 GREEN/scope).
- Battery: 18/18 arms, `BATTERY PASS`.
- `commit-gate.sh` on both `.py` files: rc=0, `OK: pre-commit gate clean for 2 of 2 file(s)`; the 4 non-ASCII
  WARN lines on the gate file are pre-existing (identical 4 in the pre-edit baseline).
- `proof-of-spec-check.py <instance> F28-AC1..F28-AC8`: **`VALID (rc=0)`**, `violations=0`, `3 surprises
  resolve to a channel row`, `invocation-alignment 7/7 comparable rows match, 0 diverge`.
  At `946fa17409` the `FAIL` row on `F28-AC6` kept TO-FE-s-28 open, because a VALID instance is not a met
  order. After the re-cut at `9ab6043728` that row reads PASS by output. The instance was re-validated and
  `<status>` flipped to `complete` in the same commit.
- Push state: **LOCAL** on `wk-irpt_fntend-4-4-fe-s-28`. Nothing pushed, nothing merged.
