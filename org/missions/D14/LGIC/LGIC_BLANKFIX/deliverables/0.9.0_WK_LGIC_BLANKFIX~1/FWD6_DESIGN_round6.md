# FWD-6 design -- the creator hears at creation (LGIC_BLANKFIX round 6, cell BF-u-6)

**Author:** 0.9.0_WK_LGIC_BLANKFIX~1 for 2.0.0_SA_COO~G. **Date:** 2026-10-08. **Kind:** design only; nothing in `lib/`,
`.tools/` or `infra/logic/` is changed. **Claim marks:** MEASURED = I ran it in this worktree at trunk `41361dfefe`;
READ = read in the file cited; UNMEASURED = not run, and the build cell must measure it before relying on it.

## Outcome

FWD-6 as the PRD prints it, `org/missions/D14/LGIC/LGIC_BLANKFIX/prd/LGIC_BLANKFIX_PRD.md` lines 67-73 (the order gave 66-71; the
ACCEPT's last clause is at line 72, so the quote runs to 73 -- row `LGIC_BLANKFIX-W1-S16`):

```
67:  FWD-6  Whoever creates a name the check cannot place hears about it when they create it
68:         DONE WHEN  EXERCISED -- a deliberately unplaceable name has been tried and stopped, and a
69:                    placeable one let through
70:         ACCEPT     the person who adds something with a name nobody could place is told at that moment,
71:                    and told what they owe to make it placeable; the list of unplaceable names is no
72:                    longer than it was the last time anyone ran the check
73:         SOURCE     brief O5; Part III O5
```

The CTO's cut of it (`org/missions/D14/LGIC/LGIC_BLANKFIX/ledger/ROUND_ANALYSIS.round5.md`, E5): the check, run before any name is
written, refuses a new stored name the canon would print as FIX. The ACCEPT has two halves, and the design answers both:
(1) at the moment of creation the person is refused AND told what they owe; (2) a ratchet: the count of unplaceable names
after the act is no larger than the count before it.

**The gap, MEASURED.** The commit-time naming gate already refuses a wrong new name, but it tells the person only what the
grader knows. A schedule named `irpt-directory-newjob` added to `infra/aws/terraform/investor-reporting/directory/schedule.tf`
(a weekday cron, as the sibling schedule there has) is graded by `.tools/naming-gate.py` like this:

```
NAMING REFUSE infra/aws/terraform/investor-reporting/directory/schedule.tf:559 irpt-directory-newjob -> irpt-directory-newjob-{cadence}
  why: NEW and OUT-OF-PATTERN as SCHEDULE: REFUSE
NAMING-GATE: REFUSE 1 graded            (rc=1)
```

The form it prints still carries a blank, `{cadence}`. The root check fills that blank from the schedule's own expression and
prints `FIX SCHEDULE irpt-directory-refresh -> irpt-directory-refresh-daily` for the sibling resource. The creator is refused but
is not told the name to type, nor what is owed when the blank cannot be filled. That is the distance this design closes.

## Past patterns

Source: `org/tier1_exec/4.0.0_SA_CRO/deliverables/PRE_WRITE_REFUSAL_PATTERNS_20261008.md` (29 rows). I use or reject each.

**The naming gate's row, answered by name (row 16, the LGIC naming limb at commit).** It is the host, not a rival. The file says the
live mode is ENFORCE (the switch file `org/mcp/naming-gate.enforce` is present); CLAUDE.md rule 30 still says "WARN today" and the
order repeats it -- that is stale (row `LGIC_BLANKFIX-W1-S15`). It lives only inside `.tools/safe-commit.sh`, so a bare
`git commit` and `--no-verify` (row 23) never reach it: this design inherits that reach and says so under "What it does not cover".
It grades with `grade()` alone, which is why its refusal prints a blank. USED: its NEW-versus-pre-image rule (DEC-6), its
switch-file mode, its verdict lines. CHANGED: after it decides REFUSE it asks the root check what the canon would print.

USED (and how):

- **Row 17, builders `address()` / `name()`** in `lib/opal_naming.py`: a creator who calls the builder never types a bad name;
  the refusal text points there ("build it with `name()`") when the FIX form is a plain name. The builder cannot be the check
  itself, because a hand-typed literal never calls it (the CRO's own note).
- **Row 18, the Terraform `opal_name` module** (`infra/aws/terraform/modules/opal_name/variables.tf`, `main.tf`): its fences are output
  `precondition` and not a `check` block, because a `check` block only warns. The same lesson binds here: the refusal is a
  non-zero exit, never a printed warning.
- **Row 19, safe-apply's naming limb** (`.tools/naming-apply-gate.py`, called from `.tools/safe-apply.sh`): the second door, for a
  name that reaches Terraform without going through a diff the commit gate graded. In plan mode it already refuses an ADDED
  resource; the same placement step is the one reused there.
- **Row 13, safe-commit's refusals before staging** (`.tools/safe-commit.sh`) and **row 14, the universal commit gate**
  (`.tools/commit-gate.sh`): the host wrapper, and the model of a gate that fails closed when ZERO checks ran on a declared
  file. The placement step does the same: if it cannot run it refuses with the reason, it does not pass.
- **Row 15, cross-firm lists GENERATED from the registry** (`.tools/ds-precommit-check.py`): a guard is only as wide as its
  enumeration, and the fix that held was to generate the list. The roots this check runs for come from the root map and the
  scope's own enumeration (`infra/logic/registry/root_map.json`, `lib/opal_naming_scope.py`), never from a list kept in the gate.
- **Rows 5 and 6, prospective grading** (`.tools/to-pipeline-gate.py`, `.tools/surprise-row-gate.py`): they grade only what is
  NEW, so history is never re-litigated. The naming gate's NEW test is the same shape; the ratchet adds the one thing a
  prospective test cannot see (an old name turning unplaceable, see "The decision rule").
- **Pattern 4 (the mode lives in a switch file, docs drift)** and **row 10 (a WARN-ramp end date in the past made a gate go
  live BLOCKING while its message said WARN)**: the new step has its own switch file and NO date-based ramp.
- **Pattern 6 (an override whose value a consumer can reject)**: the only way past the step is an R20 register row id, which the
  gate can look up (`.tools/naming-gate.py` already does this for its waivers).
- **The E2 precedent at the end of the CRO's patterns section** (rows 3, 9, 15 key on path strings and break on a move): the
  placement step decides by what the name IS (name and type, bucket and key), never by the file's path; the path only
  finds which root's map entry applies. A moved root turns its names into HOLE lines with a stated cause, which the ratchet
  counts; it is loud, not silent.

REJECTED (and why):

- **Row 25 (a harness PreToolUse hook on Write/Edit)** as the primary door: it fires before the file is written, which is the
  literal reading of "before any name is written", but it is fail-open on a parse failure (`.tools/hooks/memory-write-guard.sh`),
  does not see a write made through Bash, and grades text that is not yet a diff, so it cannot tell a NEW name from an
  existing one. Kept as a possible second door for a later round; not the design.
- **Row 22 (`.tools/hooks/never-rules-gate.sh`)**: it enumerates command shapes and has twice missed a shape; a name can be
  created by any command.
- **Row 3 (owned-paths, `.tools/git-hooks/owned-paths-check.sh`)**: its `OWNED_PATHS_MODE=warn` env and unvalidated
  `GIT_COMMIT_AUTHOR_OVERRIDE` let a caller lower the mode with no record that a consumer can reject (848 override rows).
  The shape is rejected; the override form above replaces it.
- **Rows 1, 2, 4, 7, 8, 9, 10, 11, 12, 20, 21, 24, 26-29**: they guard branches, lanes, task-order shape, the law files,
  append-only logs, mass deletion, messages, pushes, deploys, search and seats. None sees a stored name. Row 21 (the drain,
  `.tools/safe-merge.sh`) matters only as a door that is NOT covered.
- **Row 23 (`--no-verify`)**: a gap, not a pattern; named under "What it does not cover".

## Where it runs

One placement step, called from the two doors that already exist; no new hook.

1. **Home of the step:** a function in `lib/opal_naming_rootcheck.py`, `place(name, type, root, map_path)`, that runs the
   root check's own per-item decision (`decide`) for ONE name against ONE root's answers. It is the code `check_root` already
   runs for every item (the answer assembly at `check_root`, the decision at `decide`); the build extracts it, it does not
   write a second decision. A second decision is the shadow the CLAUDE.md forbids.
2. **Door 1, commit:** `.tools/naming-gate.py`, in `judge()`, at the branch where a NEW ALIAS / OUT-OF-PATTERN literal is
   refused: before printing, call `place()` and put its answer in the `->` form and the `why:` line. It also gets one new
   branch: a NEW name `grade()` calls CONFORMANT or NO-SYSTEM-ASKED that `place()` prints as FIX or HOLE (a well-formed
   name the canon would still place elsewhere, or cannot place) is refused. The gate runs from `.tools/safe-commit.sh` on the
   ADDED lines of the staged diff, so it runs before the name lands in history.
3. **Door 2, apply:** `.tools/naming-apply-gate.py`, plan mode, the same call for an ADDED resource.
4. **Mode:** a sibling switch file, to be created as naming-place.enforce beside `org/mcp/naming-gate.enforce`, so the new refusal can be proved on a branch before it is
   live without lowering the gate that is live today. Present = refuse; absent = print the same text and pass. No date, no ramp.
5. **Which roots run:** only the roots a staged name belongs to. The scope's enumeration decides, not a path prefix: the
   lines of `infra/aws/terraform/investor-reporting/directory` include `where` files outside the root's folder
   (`infra/aws/lambda/investor-reporting/directory/handler.py:53`, MEASURED). Cost, MEASURED: one root check takes about
   8 s of wall time (`bd-pipeline`, 142 items, 8.4 s); a commit touching several roots costs several of these (UNMEASURED
   for a many-root commit; the build cell measures it and states the bound it adds to a commit).

## The decision rule

For every NEW stored name in the diff (new = absent from its file's pre-image, exactly the test `.tools/naming-gate.py` uses):

1. Find the name's type (the gate already classifies it) and its root (step 5 above). If the name belongs to no root, or to an
   UNMAPPED root, the rule uses `grade()` alone: the existing REFUSE for a wrong NEW name stands, and a well-formed name
   passes. A well-formed name is never refused for lacking a registry row; that refusal was withdrawn
   (`org/missions/D14/LGIC/LGIC_BLANKFIX/prd/LGIC_BLANKFIX_PRD.md` CONTRACTS, row C-CREATE, line 119; and line 174).
2. Otherwise call `place()` and act on the kind it returns:

| Kind `place()` returns | Action | What the person is told |
|---|---|---|
| FIX | REFUSE | the exact name to use (the FIX detail) and where each blank in it was filled from |
| HOLE | REFUSE | the blank that cannot be filled, whose it is to fill (table below), and that the name is placeable the moment it is filled |
| RIGHT, NOT-ASKED, PATTERN, CARDED | pass | nothing (NOT-ASKED prints its existing reason) |
| REFUSED (a key tied to another firm) | pass here; the cross-firm guard (`.tools/ds-precommit-check.py`) owns it | the REFUSED line, printed |

3. **The ratchet (the ACCEPT's second half).** For each root the diff touches, run the root check on the post-image and on
   HEAD, and count its HOLE lines. If the post-image count is larger than HEAD's, REFUSE the commit and print the HOLE
   lines that are new. The comparison is HEAD against post-image, run now, never against a saved file: the BS9-AC1 failure
   (`LGIC_BLANKFIX` row S8) was a check compared with a saved copy of its own output. The ratchet is what catches an OLD name
   that a diff turns unplaceable -- a root moved (its map key no longer resolves), a map entry removed, a schedule's expression
   changed so the name's cadence word no longer agrees, or two names given one target (the root check already turns that
   into HOLE). A diff that removes a HOLE passes; a diff that leaves the count equal passes.
4. **Unmapped roots** have no lines, so no HOLE count to ratchet. The number of names the scope finds in them is printed as a
   delta (`UNMAPPED <root> names=N`, before and after) as a notice and never refuses; refusing on it would be the withdrawn rule.
   That is a real limit on half (2) of the ACCEPT, stated again under "What it does not cover".

What each HOLE tells the person they owe (the texts are the root check's own `why` strings, READ in `decide`):

| HOLE cause printed by `decide` | What is owed | Owner |
|---|---|---|
| `{system}: no map entry for this root` | a root-map entry for the root | `4.0.0_SA_CRO` (writer of `infra/logic/registry/root_map.json`) |
| `{system}: this root serves more than one firm; its map entry does not give the system` | the entry's `fills` for the system | `4.0.0_SA_CRO` |
| `{cadence}: no cadence row for this name` / `the schedule says X and ... no such ending to rebuild` | a schedule expression the cadence reader can decide, or a name that already ends in the word | the creator (their own schedule) |
| `{source}/{scope}: ...` (key class UNDECIDED) | a key ruling row for the key | `4.0.0_SA_CRO` (`infra/logic/registry/key_rulings.json`) |
| `this target is also given to ...` | one of the two names; nothing here says which keeps it | the creator, with the owner of the older name |
| `the grader gave verdict ... and no canonical form` | a rule or registry defect, not the creator's | `1.0.0_SA_CTO` (reported as a rule or registry defect, as the gate reports RAISE) |

The refusal text names the owner and the file; the creator does not write the registry (only `4.0.0_SA_CRO` does), so for a
registry-owed HOLE the text tells the creator to hand the owner the one line it prints, which is the content of the row.

## What it refuses and what it lets through

Both examples are lines of the live run (`lib/opal_naming_rootcheck.py` on `infra/aws/terraform/investor-reporting/directory`,
MEASURED this session; the whole-estate record is
`org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/2.0.0_SA_COO~G/ALL_ROOTS_round5_second_seat.txt`).

**Deliberately wrong.** The live line `FIX SCHEDULE irpt-directory-refresh -> irpt-directory-refresh-daily
[infra/aws/terraform/investor-reporting/directory/schedule.tf:389]` is what the canon prints for the sibling name. A creator who
adds the NEW schedule `irpt-directory-newjob` (cron `50 9 ? * MON-FRI *`) in that file is refused. Today (MEASURED above) the
gate prints `irpt-directory-newjob-{cadence}`. The build prints, in this form (proposed wording, the facts in it are the root check's):

```
NAMING REFUSE schedule.tf:559 irpt-directory-newjob -> irpt-directory-newjob-daily
  why: NEW name the canon places as FIX. Owed: rename it to irpt-directory-newjob-daily (the cadence word "daily" is read
       from schedule_expression cron(50 9 ? * MON-FRI *); the system from the root map entry for the root).
       Build it with name() or edit the literal; nothing else is owed.
```

A second wrong example from the same run, with a key: `FIX LAMBDA irpt-directory-search -> irpt-directory-search-lambda`
(the Lambda kind word is missing); the person is told to add the `-lambda` ending.

**Deliberately right.** The live line `RIGHT SCHEDULE irpt-directory-refresh-retry-daily -> irpt-directory-refresh-retry-daily
[.../schedule.tf:423]`. A creator who adds `irpt-directory-newjob-daily` with the same cron is let through (MEASURED: the
present gate prints `NAMING CONFORMANT ... PASS 1 graded`, rc=0; the step must keep that result, and `place()` prints RIGHT).

**Unplaceable (HOLE).** The live whole-estate run has `hole=0` over the 13 mapped roots, so there is no live HOLE line to quote.
The arm is built in the exercise by removing the root-map entry from a COPY of the map (never from the registry) so the same
creator act reads `{system}: no map entry for this root`; the text then tells the creator the owner is `4.0.0_SA_CRO` and the
row to hand over is the root's map entry.

**Let through, by design:** an EXISTING wrong name the diff only touches (the gate WARNs, as DEC-6 says); a PATTERN line (a
code pattern, not a name); a NOT-ASKED name; a name in an unmapped root that `grade()` calls well-formed.

## The exercise that would prove it

Every arm is driven on demand, on a throwaway worktree, with nothing committed to the trunk and no AWS or network call. The gate
is run on a unified diff with `python .tools/naming-gate.py --diff FILE`, and a staged commit is run through
`.tools/safe-commit.sh` on a scratch branch. Denominators are printed with each arm.

| Arm | Act | Expected |
|---|---|---|
| A. refuse FIX | add the schedule `irpt-directory-newjob` to a copy of `infra/aws/terraform/investor-reporting/directory/schedule.tf` | rc=1; the line names `irpt-directory-newjob-daily` and what is owed; no `{` in the printed form |
| B. let through (NEGATIVE ARM) | the same resource named `irpt-directory-newjob-daily` | rc=0; `NAMING-GATE: PASS` |
| C. refuse HOLE | arm A's act against a COPY of the root map with the `investor-reporting/directory` entry removed | rc=1; the line says no map entry, names `4.0.0_SA_CRO` as the owner |
| D. ratchet grows | a diff that edits a schedule's cron so an EXISTING name's cadence word no longer agrees | rc=1; the new HOLE line printed; count after greater than count at HEAD |
| E. organic case (NEGATIVE ARM) | a diff that touches an existing wrong name without renaming it (the existing `irpt-directory-refresh`) | rc=0 with a WARN, not a refusal |
| F. ratchet shrinks (NEGATIVE ARM) | a diff that fixes a HOLE | rc=0 |
| G. switch absent | arm A with the naming-place.enforce switch file absent | the same text, rc=0 (shows the refusal is this step's and not the older gate's) |
| H. override | arm A carrying an R20 register row id the registry holds | passes with the row id printed; a made-up id still refuses |

Two controls, run first: the arm A diff through the CURRENT gate must print `{cadence}` (the baseline already MEASURED above, so the
exercise can see the difference), and the live root check must print `hole=0` over the mapped roots at the start (the ratchet's
denominator). A test of the build asserts relations and rows by name, never a typed total of repository names, roots or
registry rows (those move daily); the existing bar (`python -m pytest lib/tests -q -p no:cacheprovider`, and every
`lib/tests/test_opal_naming_*.py` printing `ok=True` except the red keyfill test, row `LGIC_BLANKFIX-S7`) is unchanged by it.
`lib/tests/test_opal_naming_rootcheck.py` is where `place()`'s tests go.

## What it does not cover

- **A commit that does not go through `.tools/safe-commit.sh`:** a bare `git commit`, `--no-verify` (row 23), and a merge
  or drain that carries a name in (row 21; every pre-commit exemption applies under MERGE_HEAD). The step has the same reach
  as the gate it sits in. Row 23 is a gap in the estate, not in this design; closing it is not proposed here.
- **A name created outside any diff:** typed into the AWS console, made by a script's boto3 call at run time, or built from
  a variable at run time. Only literals the gate already sees are graded; the PATTERN kind is by definition not a name.
- **Names in the 74 unmapped roots** (`ROOTS total=87 mapped=13 unmapped=74` at round 5): they have no lines, so the ratchet
  has no count there. A wrong NEW name in one is refused by `grade()` as today (with a blank still unfilled); a well-formed one
  passes. FWD-2 and FWD-7 are what shrinks this; this design does not.
- **Stored-name carriers the scope enumeration misses** (row `LGIC_BLANKFIX-W1-S14`: names declared through locals, modules
  or a `.json` file): the root check does not list them, so `place()` has no line for them either.
- **Which of two names keeps a shared target:** the check reports the collision as HOLE and says nothing decides it.
- **The registry rows owed to a HOLE:** the creator is told what is owed; the row is written only by `4.0.0_SA_CRO`. The
  step shortens the wait by printing the row's content, it does not remove the hand-off.
- **Pre-write in the literal sense:** the step runs at commit and at apply plan, the first places a name is a diff. A name
  can exist in a working file between its typing and the commit; only a Write/Edit hook (rejected above) would reach that.
- **UNMEASURED:** the added commit time with many roots; whether every `where` file maps to exactly one root by the scope's
  enumeration; the behaviour when a staged file belongs to two roots. The build cell measures these first and files a row for
  any it cannot bound.
