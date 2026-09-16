# The ~32 KB ARGV CLIFF has a THIRD half, and it is the one that re-creates the defect

- recorded by: `0.0.0_AB_MSTR~Z`, 2026-09-16 ~02:2xZ
- authority: Andrew-direct at the site-Z terminal, VERBATIM AND ENTIRE: **"GOWITH YOUR REC"**,
  answering a recommendation to fix the hook rather than bypass it with `--no-verify`.
- prior art, and it predicted this event eleven days early: `38a37be871`, `1.0.0_SA_CTO`,
  2026-09-04T22:56:38-04:00 -- *"the ~32 KB ARGV CLIFF -- the two gates carrying every merge
  exemption were the exact two the hook could not start on a large merge, and a cross-fabric
  reconcile is the largest commit this estate makes."*

## What happened here

`/integrate parity` leg 1 resolved cleanly and EVERY gate PASSED on the merged index
(surprise-row-gate OK across 22 files; missions-tree-check 0 violations over 642 tree/register
paths). The commit then died downstream:

```
.git/hooks/pre-commit: line 124: .../python: Argument list too long
```

`pre-commit` built `STAGED="$(git diff --cached --name-only)"` and stage 9 ran
`python "$ROOT/.tools/to-pipeline-gate.py" $STAGED` -- **UNQUOTED**, so 2537 paths / **230,037
bytes** became argv against an MSYS limit near 32,767.

⛔ **THE GATE DID NOT REFUSE THE MERGE. IT NEVER RAN.** Those are different states and only one is
evidence about the branch. Discriminating pair, same gate, same content, only SIZE differs:
`2 paths -> rc 0, prints a verdict` vs `2537 paths -> rc 126, E2BIG`.

⚠ **`safe-merge.sh`'s own refusal text says "a hook saw something the merged-index grade above did
not."** In this instance that is WRONG and worth correcting in its source: the hook saw NOTHING, it
died before reading a single path. **A CRASH AND A REFUSAL ARE NOT THE SAME OBJECT, and this one
reports in the vocabulary of the other** -- which sends the reader hunting the branch for a defect
that is not there. Not fixed here; surfaced to that script's owner.

## THE THREE HALVES, and why two devices ended up in different states

`0.0.0_AB_MSTR` (laptop) named two halves that travel differently. There is a THIRD.

| half | tracked? | travels by | state before tonight |
|---|---|---|---|
| the GATES (`.tools/*.py`) | YES | git | FIXED everywhere, incl. site Z |
| the live HOOK (`.git/hooks/pre-commit`) | **NO** -- inside `.git/` | nothing | fixed on the laptop BY HAND; still broken on site Z |
| the **INSTALLERS** (`.tools/git-hooks/install-*.sh`) | **YES** | git | **STILL CARRIED THE DEFECT ON BOTH BOXES** |

**So `38a37be871` repaired the laptop's hook by hand and left the thing that RE-CREATES it
unrepaired.** Two consequences, and the second is the one nobody had:

1. Any fresh clone, or any re-run of those installers, re-mints the cliff.
2. ⛔ **THE LAPTOP'S OWN HOOK WAS NEVER DURABLY FIXED -- it is fixed until someone re-installs it.**
   A hand-patched untracked file has no defence against its own generator.

⭐ **THE GENERAL FORM: WHEN A FIX TOUCHES A GENERATED ARTIFACT, THE FIX IS NOT LANDED UNTIL THE
GENERATOR CARRIES IT.** Patching the output leaves a defect that reads as fixed and regenerates
silently on the next install. **Ask what MINTS the file you just corrected.**

## What was changed here (under Andrew's word)

```
.git/hooks/pre-commit                          :124  to-pipeline-gate   argv -> env   (device-local)
.git/hooks/pre-commit                          :138  surprise-row-gate  argv -> env   (device-local)
.tools/git-hooks/install-to-pipeline-gate.sh   :44                      argv -> env   (TRACKED)
.tools/git-hooks/install-surprise-row-gate.sh  :41                      argv -> env   (TRACKED)
```
Form: `ROOT="$ROOT" STAGED="$STAGED" python "$ROOT/.tools/<gate>.py"` -- no argv.

⛔ **NOT TOUCHED:** `.tools/to-pipeline-gate.py` and `.tools/surprise-row-gate.py`. Both were already
correct and are not this seat's.

**DENOMINATOR:** exactly 2 unquoted argv sites existed in the hook. The other `$STAGED` uses --
`:79`/`:80` export it as env, `:97` passes it as env, `:110` pipes it into `grep` -- were already
safe. Fixing only `:124` would have crashed at `:138`: Rule 22's shared-dependency shape.

## THE PRECONDITION, and why order mattered

⛔ **THE ARGV CLIFF FAILS CLOSED (rc 126). A HALF-APPLIED FIX FAILS OPEN (rc 0, "denominator: 0"),
WHICH READS EXACTLY LIKE A HEALTHY PASS.** So dropping argv on a device whose GATES could not read
env would have been strictly worse than the blocker. Named by `0.0.0_AB_MSTR`; verified here at this
seat's OWN ref rather than accepted, because a peer's confirmation on a fail-open hazard is the one
place repetition is least acceptable:

```
git merge-base --is-ancestor 38a37be871 HEAD          -> YES
.tools/to-pipeline-gate.py  :2611  env = os.environ.get("STAGED", "")   (bytes printed, not grepped)
.tools/surprise-row-gate.py :966   same
```

Both gates additionally **PRINT their input source** when it is not argv -- which is what makes the
fix verifiable rather than merely applied.

## VERIFICATION -- a discriminating pair, not a smoke test

| arm | input | result |
|---|---|---|
| the fix | 2537 paths via `STAGED` env | **rc 0**, `[to-pipeline-gate] input: 2537 path(s) from the STAGED environment variable` |
| the FAIL-OPEN shape | no argv, no env | rc 0, `denominator: 0 dispatched path(s)`, **and no `input:` line** |
| surprise-row-gate | 2537 paths via env | reads 2537 and returns a **verdict** rather than crashing |

**The two rc-0 outcomes are distinguishable at the console**, which is the property that matters: a
real read announces its count and its source; a vacuous pass prints a zero denominator and no source
line. Before the change the same input produced `rc 126` and no output at all.

## Scope

This unblocks a commit; it authorizes nothing else. No gate's VERDICT changed, no exemption widened,
no `--no-verify` used. The LD-0522 Amendment 4 precedent (run the gates by hand, commit
`--no-verify`, state it) was available and was NOT taken -- it discards every other gate, and the
point here was to make a gate RUN, not to route around one.
