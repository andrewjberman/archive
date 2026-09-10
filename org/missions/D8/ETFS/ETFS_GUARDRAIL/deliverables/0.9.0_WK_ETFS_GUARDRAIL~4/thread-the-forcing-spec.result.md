# ETFS_GUARDRAIL.TO-EG-s-24 -- THE FORCING SEAM: BUILT AND GREEN, UNCOMMITTABLE BY ME

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` (L7 worker subagent of `2.0.0_SA_COO`, round 3, cell `EG-s-24`)
**Worktree:** `/c/tmp/wk-etfs-3-4` on `wk-etfs_guardrail-3-4`, HEAD `11c0810142` (unchanged by this order)
**Face:** read at `d30e3ca107` -- it is NOT in this branch's ancestry, and that is the whole problem.
**Outcome:** `S24-AC1` **FAIL**, blocked at the commit. `<status>` NOT flipped (it cannot be).
**Rows:** `ETFS_GUARDRAIL-W4-S3` (BLOCKING / ARMED), `ETFS_GUARDRAIL-W4-S4` (OBSERVATION / INERT, a correction to my own `W4-S1`).

> **NO DEPLOY, NO INVOKE, NO SEND.** The plan was never run and `safe-apply` was never called,
> because L1 (code committed before the apply) could not be satisfied. The served function is
> untouched at `CodeSha256 ag4La0jgP8JEr55FCvXx+gnR5pDqw1CpvbEHZBrBTPc=`. `EG-s-21`'s single
> permitted driven run remains **unspent**.

---

## 1. THE WORK IS DONE, AND IT IS GREEN

`python -m pytest infra/aws/lambda/etfs-reports-orchestrator/ -q` -> **26 passed** (was 20; +6 new
arms in `test_forcing_seam.py`). `.tools/commit-gate.sh` -> `pre-commit gate clean for 2 of 2
file(s)`. ASCII-clean and LF, checked explicitly.

**The seam**, in `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`:

```
FORCING_KEY     = "force_fixture_remove"
FORCING_SPEC_RE = ^[a-z0-9][a-z0-9_-]{0,31}:\d{4}-\d{2}-\d{2}(,\d{4}-\d{2}-\d{2})*$
_forcing_spec(event) -> the validated spec, or "" for OFF
_render_command(month, forcing="")      <- DEFAULTED, so every existing caller is unchanged
_render_command(month, _forcing_spec(event))    <- the one call site
```

**The safety property, which is what the cell is for.** CLAUDE.md: an override letting a scheduled
producer run off its own inputs **creates a new reachable state on the manual path**. This one is
worse-shaped than EG-s-15's `--month` override -- that changed *which* month was rendered; this
changes *what data* the month is rendered over. Four mechanical fences:

1. **The default is OFF, and OFF is bit-for-bit.** `""` appends nothing, so the marker-free command
   is byte-identical to the pre-change one -- asserted against the **actual pre-change blob**, read
   from git at a pinned commit and verified *by content* against the sha256 measured on the deployed
   zip member, with a positive control on `git show` and an explicit wrong-pin assert (Rule 22a).
2. **Two independent conditions, neither in the scheduled payload.** The event must carry BOTH
   `test_run` AND `force_fixture_remove`; the schedule's own input is `jsonencode({mode = "run"})`.
3. **The coupling is the safety composition.** Forcing requires the TEST marker -- exactly the marker
   EG-s-20's forbidden-filter keys on -- so **a run that drops its own input data can never be a run
   whose recipients include aj@**. An arm asserts both directions.
4. **The spec is shell-bound, so it is validated.** It interpolates into a single-quoted
   `su - ec2-user -c '...'` handed to SSM. 13 injection attempts (quote-break, `;`, `&&`, backticks,
   `$( )`, newline, a second `--s3-out`, path traversal, malformed dates) each resolve to OFF and
   leave the command **equal to the clean one**.

**Three of my own test assertions were wrong and the tests caught them, not the code.** An injection
arm asserted "no `'` in the command" and failed on the *wrapper's* own closing quote; a later
version asserted "no `$(`" and failed on the orchestrator's own `CHROME=$(ls -d ...)`; and the
recipient arm asserted both recipients while never setting `EMAIL_RECIPIENT`, so its converse limb
would have passed **vacuously** against a set that never contained aj@. All three are now delta-based
or explicitly pinned, each carrying the reason inline.

---

## 2. WHY IT CANNOT BE COMMITTED -- two correct gates, jointly blocking

| attempt | pathspec | result |
|---|---|---|
| 1 | code + tests + **the face** + ledger | **L6 gate REFUSED**: *"a NEW tree task order committed under `0.9.0_WK_ETFS_GUARDRAIL~4`. COO is the only agent that does task orders (LD-0521 A3)"* -- plus 3 more, because my branch's decomposition is the v0.3 index (**22 cell ids, `EG-s-24` absent**) while the cell was minted in v0.6 at `d30e3ca107` |
| 2 | code + tests + ledger (face removed from worktree) | **lane gate REFUSED**: *"agent=`0.9.0_WK_ETFS_GUARDRAIL~4` not in permitted_agents -- WORKER: no NON-TERMINAL task order at HEAD issued_to this serial names this path in its `<paths>` block (ADHC_OWNPTH.005: the order is the grant; a missing path is a cut defect, never an override)"* |
| 3 | same, with the face materialised **untracked** in the worktree | **refused identically** -- so the grant resolves from **HEAD**, not the worktree. This is the discriminating read. |

`git log -1` -> `11c0810142~0.9.0_WK_ETFS_GUARDRAIL~4~L7(...EG-s-21...)`; negative control
`git log -1 --format=%h deadbeefdeadbeef` -> `fatal: ambiguous argument`. **HEAD is unchanged and
nothing landed** -- asked of the repository, not of the tool's stdout, per the refusal's own warning.

**The bind is exact:** gate 2 resolves my grant from a task order *at HEAD*; gate 1 forbids me
putting that task order at HEAD.

**This is the banked hazard running backwards.** The estate has recorded that a worker's own
`<status>` flip *withdraws* its grant on its own branch. Here the same coupling bites at the start:
my `EG-s-20` face at HEAD names `infra/aws/lambda/etfs-reports-orchestrator/` but I flipped it to
`complete`, so it is **terminal and grants nothing**; my `EG-s-21` face at HEAD is non-terminal but
its `<paths>` deliberately excludes that directory; and the `EG-s-24` face that *does* grant it lives
only at `d30e3ca107`, which I may not merge.

**I took neither printed override.** The L6 refusal offers `# pipeline-override: <reason>` and the
lane refusal has `GIT_COMMIT_AUTHOR_OVERRIDE=<LANE>`. Using the first would be a worker acting as
the issuer on the one artefact the workflow reserves to the issuer; using the second would be a
worker writing its own lane grant. My standing instruction is that a path my order lacks is a
**BLOCKING row, never an override**, and both refusals are correct.

---

## 3. NOTHING IS LOST -- what is preserved, and the one-line fix

Committed to this deliverables folder (which *is* reachable, by tree convention):

| artefact | size | sha256 |
|---|---|---|
| `EG-s-24_UNCOMMITTED_lambda_function.patch` | 7,751 B | `7d67b7ec9fd6909d0ae1c615b04ffc87315f73542505c94cc656106257e7c223` |
| `EG-s-24_UNCOMMITTED_test_forcing_seam.py` | 13,365 B | `d3878289eecb1a45e8ea6153e7c9bf78d08b12ee805863d2e7f1396695267c05` |

The worktree files they were taken from: `lambda_function.py` 45,641 B sha256
`fe46e12c51b77747a4779536297ad19cd0d47a3a6e4b703e114565a7ca4ba95f`; `test_forcing_seam.py` 13,365 B
sha256 `d3878289eecb1a45…`.

**The cheapest fix is the issuer's and the code needs no change:** put `d30e3ca107` (or just the
`EG-s-24` face plus the v0.6 decomposition) into this worker branch's ancestry, and the same commit
lands unmodified.

---

## 4. THE CRITERIA

### `S24-AC1` -- FAIL

The battery `test_egs24_forcing_seam.py` was **not written**, deliberately. Arms (a)-(d) are
measurable only against **deployed** bytes, and arm (e) is a deploy that could not begin: its own L1
is "committed BEFORE the apply", and the commit is what is blocked. Writing a battery that reads the
*worktree* would be precisely the Rule 22a error this project has been correcting all night --
proving a property of bytes nobody serves. The hermetic evidence that the seam is correct is the
6 new pytest arms (26 of 26 green); the evidence that it is not *deployed* is that the served
`CodeSha256` is unchanged.

### `S24-AC2` -- RECORDED, judgment, NO VERDICT

- **The forcing key's shape, and why it cannot be confused with a scheduled field.** Two keys must
  co-occur (`test_run` + `force_fixture_remove`); the schedule's entire input is
  `jsonencode({mode = "run"})`. `force_fixture_remove` is a verb-phrase in the imperative, not a
  noun a scheduler would emit, and it is matched **exactly** -- `FORCE_FIXTURE_REMOVE`,
  `Force_Fixture_Remove`, `fixture_remove`, `--fixture-remove` and a nested `detail.*` copy are all
  tested and all resolve to OFF.
- **What a caller could still do wrong.** Three things, none of which reach the world. (i) Pass a
  well-formed spec naming a partner that does not exist -- the renderer's `_apply_fixture_remove`
  uses `daily.get(p, {}).pop(d, None)`, so it is a silent no-op and the run would PUBLISH while the
  operator believed it forced; that is a *disclosure* problem and it is `EG-s-25`'s field, which is
  exactly why the two cells are paired. (ii) Pass dates that are already absent -- same shape.
  (iii) Force on a month whose holes are class D, which does not refuse; the class table, not the
  forcing, decides.
- **Other callers of `_render_command`, censused not recalled:** an AST walk finds **1** call site
  (`:643`), and a pytest arm asserts that count and that `forcing` is **defaulted**, so an unknown
  future caller keeps the old behaviour.
- **What this seam does NOT make reachable.** It cannot write or delete an S3 key; it cannot change
  which month is published; it cannot reach a recipient (the recipient path is EG-s-20's and is
  keyed on the same marker); it cannot survive into a scheduled fire; and it cannot put a shell
  metacharacter into the SSM command. It makes exactly one thing reachable: `--fixture-remove` on a
  test invocation.

**Evidence vintage:** code as measured in the worktree 2026-09-10 ~05:0xZ (uncommitted, sha256s
above); deployed orchestrator unchanged at `LastModified 2026-09-10T03:54:09Z`; gate refusals quoted
verbatim from this session.

---

## 5. WHAT I DID NOT DO

- **No deploy.** No `terraform plan`, no `safe-apply`, no `update-function-code`.
- **No invoke, no send.** `EG-s-21`'s one run is unspent.
- **No override**, of either gate.
- **No edit to the renderer** (`EG-s-25`, `0.9.0_WK_ETFS_GUARDRAIL~5`) or to
  `data/etfs/scripts/coverage/` (`EG-s-23`, `0.9.0_WK_ETFS_GUARDRAIL~1`). I read
  `render_month_end.py` only to import `_parse_fixture_remove` in a test and to cite line numbers.
- **No `<status>` flip**, on any face.
- **The NEVER-2 entry `20260910T0508Z_etfs-guardrail-eg-s-24-forcing-seam` is left OPEN** with 5
  legs and is *uncommitted* -- its sentinel could not ride the blocked commit either. It is named
  here so it is not later mistaken for an abandoned deploy: **no deploy ever started.**
