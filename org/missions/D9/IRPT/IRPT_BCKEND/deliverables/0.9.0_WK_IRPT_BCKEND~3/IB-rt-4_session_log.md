# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-rt-4`

Worktree `/c/tmp/wk-irpt-2-3`, branch `wk-irpt_bckend-2-3`, cut from `7478fdf144` (the round-2
issuance). First order of slot ~3 in round 2; the same subagent that built intake, generation
and extraction in round 1, executing a ruling on two rows it found itself.

**Outcome: RT4-AC1 FAILS at `4 of 5` arms. The order stays open.** Arms (a)-(d) -- the whole
substance of CTO ruling 4 -- pass. Arm (e) fails on one of five Terraform roots, for a reason
that is not this cell's code and cannot be cleared by this cell's authority (row `W3-S17`).

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-2-3`; `TREE-OK`; then every
   path the face names, checked one by one. Then the **gitignored session-serial line** --
   `org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial`, which the face requires before any apply
   and which did not exist in this worktree; written, and confirmed gitignored at `.gitignore:423`.

2. **Censused before building anything.** Three censuses, each of which changed what I built:
   - **The public surface of `_keys`, by AST**: 11 public callables, 4 of them readers, so **7
     constructors**. Driving all 7 x 4 negatives against round-1 HEAD found **6 accepted pairs**,
     not the 2 the ruling implies.
   - **The error paths, by AST** over the six families: 25 modules, 49 except handlers, 18
     binding the exception, **10 rendering it**.
   - **The `%r` sites in `_keys`, by AST**: **18 placeholders across 16 refusal sites**, where
     the ruling says twelve.

3. **Built the refusal layer**: a closed 16-member reason vocabulary, a structured
   `KeyComponentRefused` carrying a component NAME and a reason CLASS with the value in a
   developer-only method, and a positive allowlist of segment shapes for the two leaky
   constructors.

4. **Built the ONE envelope** (`_authz/errors.py`): a closed 14-member public reason enum, a
   correlation id, and no third field. Then closed all ten leaking error paths.

5. **Verified the grammar did not move** against the module at round-1 HEAD loaded from git --
   12 of 12 keys byte-identical, including the IB-s-9 and IB-s-10 artifact keys verbatim.

6. **Deployed what could be deployed cleanly**: `init` (caches purged estate-wide), pre-apply
   plans read BEFORE each apply, four roots applied, five functions verified, four ledgers
   closed. **The fifth root was refused** -- see below.

7. **Graded, filed six rows, and reported the FAIL** rather than narrowing the arm to fit what
   worked.

## The blocker, and why I did not route around it

`terraform plan` on the export root, **before any change of mine**:

```
# aws_iam_role_policy.export_render_dispatch   will be destroyed (not in configuration)
# aws_iam_role_policy.export_render_evidence   will be destroyed (not in configuration)
# aws_ssm_document.export_render_run           will be destroyed (not in configuration)
Plan: 0 to add, 1 to change, 3 to destroy.
```

IB-s-14 removed these from the `.tf` at `1beda4bf49` and never applied. Two are IAM role
policies on a live function.

I considered three routes and rejected each for a stated reason:

- **Apply it.** Destroys two live IAM role policies. Bound 7 forbids touching served output, and
  the face's own deploy condition is *"plans show only the code changes"*. Refused.
- **`-target` the Lambda only.** Leaves the root non-converged, so the post-apply plan cannot
  read `No changes` -- arm (e) fails anyway, and now with a half-applied root behind it.
- **`terraform state rm` the three.** Leaves them live and unmanaged, which is worse than either.

So the code is committed and the apply is withheld. **Arm (e) grades the FULL requirement** --
`IMPACTED` and `ROOTS` are every changed function and every root that holds one -- because
narrowing those tuples to the four that applied cleanly would have turned a blocked deploy into
a green.

## What went wrong, and what each cost

- **My first wiring of the error helper used a module-level import in two handlers whose zips are
  closed over their own directory.** `export/handler.py`'s header says so explicitly and gives
  the reason. The commit gate caught the undefined name; the design lesson was to import lazily
  and package `errors.py` flat, which is what the estate already does for `enforce.py` and
  `keys.py`.
- **The error-path census over-fired 2 of 12.** It flagged any expression mentioning the bound
  exception, including `type(exc).__name__` -- so `directory/refresh.py` and
  `ycharts/extract/extract.py` were reported as leaking when they had *already applied this
  lesson deliberately*, one of them citing row W2-S10 in a comment. **A census that over-fires
  sends a careful reader to "fix" correct code AND inflates the denominator its own fix is graded
  against**: "10 of 10 closed" would have read as "12 of 12".
- **My battery reported a cleaner import closure than the truth** -- `6 of 6` in-process against
  the standalone script's `5 of 6`. The battery imports modules of its own first, so a packaged
  module's `import enforce` resolved from a leftover `sys.modules` entry instead of failing. The
  check whose entire purpose is to prove a zip stands alone was leaning on the process it ran in.
  **A saved-and-restored `sys.modules` is not isolation; only a new interpreter is.** It now runs
  in a clean subprocess. Caught only because two instruments disagreed.
- **A firm token classified as the generic shape reason.** `49financial` opens with a digit, so
  it matches no segment shape and was refused as `NOT_A_DECLARED_SHAPE` before the firm-token
  check ever ran. Both refuse; only one tells the caller it tried to put a firm in a key body.
  The classifier now takes the token set where it is known.
- **A directory test asserted the old prose contract** and failed against my change. Fixing it
  surfaced `repr(op)` on an ordinary return path -- a leak no AST census of except handlers could
  ever see (row `W3-S15`). Both tests were updated to the new contract and **strengthened**: each
  now also asserts the caller's own input appears nowhere in the response.
- **The whole-tree `pytest` run shows 25 failures** from flat-module-name collisions. Established
  as pre-existing by extracting round-1 HEAD read-only with `git archive` and running the same
  command there: **26 failed at round-1 HEAD vs 25 now** -- no regression, and one better.
  (`git stash` was refused by the shared-worktree gate, correctly; it would have parked every
  other seat's dirty file to answer a local question.)

## Bounds honoured

- **No live vendor call.** The only live reads are AWS control-plane and S3 against Opal's own
  account.
- **No monitor, alarm, SNS or SES.** Named explicitly in the RT4-AC2 record as the reason the
  reason-enum's health is *unobserved*: a standing count of reason codes by frequency is the only
  thing that would catch `UNEXPECTED` quietly becoming the common case, and it is a monitor.
- **No key already written is renamed.** The RT4-AC2 census is a LISTING: 38 live keys, 251
  segments, **0 name-shaped**.
- **`safe-apply` only**, from roots `init`-ed with the worktree-provisioned binary; sentinels
  committed OPEN before the act and removed before the grading reads.
- **No neighbouring defect fixed.** Four of the six rows are things this cell found and
  deliberately did not repair: the dead export download route, the stale source-map registration,
  IB-s-14's half-landed change, and the width of arm (c)'s own census.

## Rows filed

`W3-S13` (constructor census found a second leak) · `W3-S14` (export download route dead on
import) · `W3-S15` (arm (c)'s denominator is narrower than its name) · `W3-S16` (the ruling's
count is stale) · **`W3-S17` BLOCKING** (export root would destroy three live resources) ·
`W3-S18` (source-map registration disagrees with S3 and Lambda).

## Commits (all LOCAL on `wk-irpt_bckend-2-3`)

| hash | subject |
|---|---|
| `48313e9c0e` | the code, the source map and four OPEN sentinels, before the act |
| `a36c28a079` | close the four change-management entries -- all five legs proven on each |
| `5a8b6f2961` | six channel rows -- one BLOCKING, five observations, all measured |

Plus the closing commit carrying this log, the result document, the battery, its output and the
proof instance. **The `<status>` is NOT flipped: RT4-AC1 is a FAIL and the order stays open.**
