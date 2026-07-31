# WS-C7 -- THE SHELL-REACHABILITY GATE: REACHABILITY IS PER (TOOL, INVOCATION SHAPE)

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**Scope grant:** CTO~Z `20260731T151744Z` -- last C7 cut.
**Canonical specimen:** `SPEC-1` (`2c5e1c60e`) -- written for exactly this gate.
**Binds:** the completeness family (`manifest_check_cli.py:87-100`) and schema v3 (`153f16f2c`).
**Substrate read, not modified.**

---

## 1. WHAT MEMBER 4 ALREADY COVERS, AND WHAT IT CANNOT

Member 4 exists because members 1+3 bind a **proxy**: they prove the router *names* the tool, not
that the named command exists. Its own origin (`manifest_check_cli.py:96-100`): `comp-system` passed
member 1 AND member 3 -- `comp-which` returned it RANK-1 for its own use_case -- while
`.tools/comp-system` had **never existed**. ***"Routable" and "runnable" are different facts.***

**Member 4 asserts the file EXISTS on disk and is tracked. THAT IS ALSO A PROXY, ONE LAYER DOWN.**

> **A FILE THAT EXISTS IS NOT A COMMAND THAT RUNS.** `SPEC-1`: `.tools/aws.cmd` existed, was
> tracked, and resolved to a real absolute path -- and executing that exact path returned
> `rc=1, "The system cannot find the path specified."` because its own delegation target did not
> exist on this device. **Every existence check passed. The command could not run.**

**Three proxies, each caught by the next:** named -> exists -> **runs**. Shell-reachability is the
third, and nothing currently asserts it.

---

## 2. THE CORE FINDING: REACHABILITY IS NOT A SCALAR

**The same tool, on the same box, at the same instant, is reachable from one caller and not from
another.** Measured (`SPEC-1`, this device, 2026-07-31):

| caller | resolves to | result |
|---|---|---|
| bash | `.tools/aws` (MSYS guard shim) | **WORKS** |
| native Python via `shutil.which` | `~/bin/aws.CMD` -> `.tools/aws.cmd` -> dead target | **rc=1** |
| bare-argv `subprocess.run(['aws',...])` | Windows `CreateProcess` + PATHEXT | **rc=0** |

**Three shapes, three different files, two different verdicts.** Every hand-run `aws` call on this
box worked for the entire window in which the estate's `default_tags` applies were broken.

> **THEREFORE: `reachable` IS A PROPERTY OF THE PAIR (TOOL, INVOCATION SHAPE), NEVER OF THE TOOL.**

**This is the same shape as `failure_direction` being a PAIR across a consumer edge rather than a
scalar per tool** (schema v3 section 4). A gate holding one reachability value per tool records the
shape its author happened to test and **grades every other shape by proxy.**

---

## 3. THE THREE REQUIREMENTS

### 3.1 EXERCISE, NEVER RESOLVE
> **The check that resolves is the check everybody writes, and it is the one that cannot fail in the
> state it exists to detect.** (`SPEC-1` thesis.)

`command -v`, `shutil.which`, `test -x`, and a registration lookup **all pass** on `SPEC-1`'s
specimen. **Score the OUTPUT, not the exit code and not the path** -- the tool must produce
something only a working tool produces.

### 3.2 THE EXERCISE MUST USE THE CALLER'S INVOCATION SHAPE
**Bash-exercising a tool that native Python will call proves nothing -- they reach different files.**
This is not a caveat; it is the requirement. **A reachability result is valid ONLY for the shape it
was measured with**, and a gate that measures one shape and reports "reachable" is making a claim
about shapes it never touched.

### 3.3 THE PROBE MUST BE ABLE TO FAIL -- AND ITS SUBJECT MUST NOT BE HAND-CHOSEN

Two distinct requirements that are easy to conflate:

**(a) A KNOWN-NEGATIVE (L-16).** Exercising proves a tool RUNS; only a known-negative proves the
PROBE DISCRIMINATES. My own CRLF counter was exercised -- on real files, returning real numbers --
and was a line counter.

**(b) THE SUBJECT MUST NOT BE THE PRIVILEGED MEMBER.** `org/XXX.md` Step 1b A.3 already mandates
exercising rather than resolving, after the 2026-07-29 *"93 of 93 resolve bare / ZERO of them ran"*
incident. **And it exercises `comp-which`** -- which is in the provisioner's named subset and is
therefore **the member most likely to be healthy.** `SPEC-1` is the proof: `comp-which` was never
the broken member; the broken chain was `.tools/aws.cmd` reached by native Python.

> **THE 2026-07-25 LESSON WAS LEARNED ONE LEVEL TOO SHALLOW: resolve-vs-exercise was fixed and the
> HAND-CHOSEN SAMPLE was kept.** Same shape as CLAUDE.md's *"a hand-chosen negative control measures
> the AUTHOR, a generated one measures the INSTRUMENT."*

*(A.3 is a law surface. CTO~Z routed this to MSTR~Z with `SPEC-1` attached on `20260731T133026Z`. I
reference the defect; I do not propose the edit.)*

---

## 4. THE DENOMINATOR

A.3 reports **"93 of 95 comp-tools resolve bare."** That is a **RESOLUTION** denominator, and
section 3.1 says resolution is not the question.

**A reachability denominator is over PAIRS**, not tools: `(tools) x (invocation shapes in use)`.
**Any pair not exercised is `structurally_invisible` or `run_conditional` per schema v3 -- declared,
never silently counted as reachable.**

> **A tool count where a pair count is meant is a DENOMINATOR AT THE WRONG GRAIN** -- schema v3's G2,
> and mechanically flaggable there. Here it would mean reporting `93/95` while the actual
> denominator is `95 x N` shapes.

---

## 5. WHAT THIS GATE CANNOT DO

- It **cannot** prove a tool is reachable from a shape nobody exercised. **Unexercised is
  undeclared, not passing.**
- It **cannot** detect a tool that runs and returns a wrong answer (**M2**, out of contract).
- It **cannot** survive its own success: a gate that goes green **must not** be read as "this tool
  is reachable," only as **"this tool was exercised from these shapes and produced working output."**

**That last one is the fourth appearance of one shape in this workstream** -- `comp-iam`'s operation
list as a deletion warrant, a green member 5 as "the declaration is correct", a boundary report that
does not travel, and now a green reachability gate as unconditional reachability. **In every one the
artifact is honest and the CONSUMER's inference is wrong.**

---

## 6. ROUTED TO THE GATE, NOT DECIDED HERE

1. **Which invocation shapes are IN SCOPE.** This device exhibits at least three (bash, native
   Python via explicit resolution, bare-argv). **Enumerating the fleet's shapes is not something I
   can do from one box** -- and per section 4 an unenumerated shape must be declared, not assumed.
2. **Whether shell-reachability is member 6 or an extension of member 4.** It asserts a strictly
   stronger fact than member 4 on the same subject. **Family structure is the gate's.**
3. **Cost.** Exercising every (tool, shape) pair at commit time is not free; substrate-scoping
   (the family's b2 pattern) presumably applies, but the introducing substrate for a *shape* is not
   obvious and I did not invent one.
4. **A.3's hand-chosen subject** -- already routed by CTO~Z to MSTR~Z with `SPEC-1` attached.

**CONTROL 2 CHECK:** nothing here types where an assertion sits. Not rail vocabulary.
