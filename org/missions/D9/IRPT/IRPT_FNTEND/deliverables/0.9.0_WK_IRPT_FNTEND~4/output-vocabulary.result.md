# FE-s-36 -- the output-vocabulary limb (GATE (ix) of `.tools/to-pipeline-gate.py`)

Worker `0.9.0_WK_IRPT_FNTEND~4`, order `IRPT_FNTEND.TO-FE-s-36`, branch `wk-irpt_fntend-5-4-fe-s-36` from CLOUD
`0a74710f33`. Code commit `8aa00e60fb`. Push state: LOCAL (this worker never pushes).

## What it does

When a tree task order is committed **staged as ADDED**, the L6 gate reads each of its mechanical criteria.
It refuses a criterion whose `<expect>` bar the named tool can never print. Where it cannot tell, it
announces that it cannot and refuses nothing. Everything else is the scope the gate already owns: it never
grades a modification, never grades an existing order, and never grades a `judgment="true"` criterion.

## What it reads -- and nothing else

1. **The `<invocation>`**. It is evaluated only when it is ONE program: an optional `cd <WS>` or
   `cd <WS>/<sub>`, optional `timeout N` and `VAR=value` prefixes, then `python|python3|py <path>.py [args]`.
2. **The named `.py` file from the INDEX** (`git show :<path>`), i.e. what exists at the cut. It never runs
   the file and never runs a test.
3. **The file's authored text**, parsed with `ast`: every string literal, every f-string, %-format and
   `.format()` template, and every `print()` argument list joined by its separator.
   - A field is resolved when the file binds it only to authored strings: a constant, a conditional of
     constants, or a name assigned only such values. Otherwise it is a field that may carry any text.
   - Digits, and any field, are number slots.
4. **The `<expect>` bar, parsed as the regex the checker uses** (`re._parser`).
   - Its literal runs are kept.
   - Digit runs, `\d` classes and digit back-references become number slots.
   - Lookarounds and anchors are dropped, which only ever loosens.
   - A run is judged only if it carries a word of two or more letters.

**The decision, per literal run of the bar:**

| Verdict | When |
|---|---|
| ADMITTED | One template authors the run: every letter is authored text, and counts land on number slots. |
| ANNOUNCED (UNDECIDED) | A template authors a word of the run in place, but a field filled at run time would carry the rest. |
| REFUSED | No template authors even one word of the run in place. |

F28-AC6 as issued is exactly this case. The alignment battery authors `fail` (an arm is named
`fail-closed: ...`), but never directly after a number. Its result lines are `  {verdict:4s} {name}`,
where both fields hold text. So `0 fail` is refused.

## What it declines to judge (ANNOUNCED or not evaluated -- never refused)

- **A runner** (bun, pytest, node, npm, a comp-tool, a shell script). The limb does not model a runner's
  vocabulary, so `bun test <file>` with `0 fail` is counted and never read.
- **A compound line** (a pipe, `;`, `||`, a second command, a redirect, a substitution). Its output is not
  one program's.
- **A target absent at the cut.** This is the ordinary case: the worker writes the test.
- **A tool whose output is not only its own:**
  - it prints a bare value (`print(out)`);
  - it runs a program other than `git` (for example `sys.executable`);
  - it hands off to `unittest.main`, `pytest.main`, `runpy`, `exec` or `X.main()`;
  - or it prints nothing itself.
- **An irreducible bar:** an alternation, or no two-letter word.
- **What it cannot see at all:** interpreter tracebacks, argparse usage text, and `timeout`'s own output.

## Its two stated assumptions

**A: vocabulary is authored text.** Text a tool relays *inside* an authored line (a diagnostic after `<-`)
is not credited with a bar's words. A module the tool imports as a library is not read; the limb builds no
call graph. So a bar that could only ever match relayed text is refused. It would pass on a diagnostic,
which is its own defect.

**B: one line comes from one template, with one modelled exception.** A call that leaves its line open
(`print(..., end="")` or a `write()`) is read as continuing into any later call. In such a file, any line
may begin mid-way. A word spliced from fragments at run time is still not credited.

## What was measured

### Real-shape battery

`.tools/tests/test_output_vocabulary.py`: 17 of 17 arms, rc=0. Each fixture is a real repository that
borrows the workspace's objects through git alternates, so nothing is written to the workspace. HEAD and
the index are `0a74710f33`. Orders are placed as ZZZ_TWIN files and `git add`-ed, so they read as ADDED.
Every arm is graded by the gate's own CLI.

| Arm | Result |
|---|---|
| F28-AC6 as issued (`b6062ad2a2`) | REFUSED, rc=1. The only OUTPUT-VOCABULARY refusal among FE-s-28's 7 mechanical criteria. |
| F28-AC6 as re-cut (`9ab6043728`) | ADMITTED: evaluated, 0 refused, and every other refusal line byte-identical between the two runs. The vintages also differ in the `<status>` line; the limb never reads it. |
| Runners | F1-AC2 (`bun test .../fe-s-1/keys.test.ts`, bar `0 fail`; the file is present in the pinned portal commit `e85f6eb84f`) and F30-AC8 (`(?<![0-9])0 fail` over three directories, 2 present at the pin) are both not refused. |
| Absent target | FE-s-36's 5 criteria naming this battery are announced, not refused. Control: with the battery staged, the absence note is gone. |
| Round 5 | 8 orders, 73 criteria (65 mechanical): 0 refused. 3 evaluated and admitted, 18 announced, 38 runner, 6 not one python program. |

### Self-test

70 of 70 arms, 0 failed: the 59 at the cut plus 11 GATE (ix) arms. Mutant control: with `_ov_judge`
forced to ADMITTED in-process, the RED arm (`0 fail` against the alignment shape) fails.

### Census over every tracked tree order

Dev census, not a criterion. It called the committed function per order, reading tools from this
worktree's index.

- 359 orders, 1235 mechanical criteria: 17 evaluated and admitted, 6 refused, 160 announced, 438 runner,
  614 not one python program.
- **The 6 refusals are all AMGT_RESAPP.** Each has an English sentence as its `<expect>`, which no output
  can match (row `IRPT_FNTEND-W4-S12`).
- **One honest bar was refused before landing:** NFRA_CLDGRPH F5-AC1. Its tool prints
  `UNREACHABLE_REFUSAL_NAMES=` with `end=""` and the value on the next print. That is why Assumption B now
  models an open line. F5-AC1 now reads UNDECIDED (announced).

### Evaluability, stated plainly

The limb evaluates few criteria: 17 plus 6 of 1235. Most python tools in the estate relay subprocess
output or run `sys.executable`, and the limb will not guess about those. That is the price of refusing
nothing it cannot evaluate.

## Deviation from the face, recorded

F36-AC4 names `(?<![0-9])0 fail` on `bun test <an existing file>`. No committed criterion has that exact
shape: 0 of the 53 single-file bun criteria across the 30 orders carrying a `0 fail` bar. The arm grades
the two nearest real shapes instead of joining them into an invented string (row `IRPT_FNTEND-W4-S11`).

## How to satisfy a refusal

- Expect a line the tool itself prints.
- Or name the tool that prints the bar. A runner's `N fail` is bun's, not a python battery's.
- Or, if the order genuinely stands outside the pipeline, use `# pipeline-override: <reason>`, which is
  audited.

The refusal text names the criterion, the bar, the tool, the number of templates read, and the nearest
authored lines carrying the bar's longest word.

## Not touched

`.tools/proof-of-spec-check.py` (excluded by BOUNDS), CLAUDE.md, and any portal path. FE-s-29's four limbs
and all 59 of their self-test arms still pass.
