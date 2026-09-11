# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-rt-4` (second execution)

Worktree `/c/tmp/wk-irpt-2-3`, branch `wk-irpt_bckend-2-3`, cut from `77b2acc7a9` -- the merged
tip, after the issuer drained this order's first report and amended the face.

**Outcome: RT4-AC1 PASSES at `5 of 5`.** The first execution reported `4 of 5`, blocked on row
`W3-S17`. The issuer routed it, the premise proved wrong in a way that changed nothing about the
withheld apply being correct, and the work completes here.

## Order of acts

1. **The bar**, then the gitignored session-serial line at
   `org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial` -- required before any apply, absent in a
   fresh worktree, confirmed gitignored at `.gitignore:423`.
2. **Read the amended face from disk**, the ISSUER AMENDMENT under arm (e) first.
3. **Re-grounded what survived the drain.** My `_keys`, `_authz/errors.py`,
   `_authz/error_path_census.py`, `directory/`, `intake/` and `export/bundle.py` edits are in the
   tree; my `export/handler.py`, `export/render.py` and source-map edits are not, exactly as the
   amendment said.
4. **Re-ran the census over the MERGED module set** rather than re-applying a remembered diff --
   see below, it is the decision that mattered most.
5. **Re-applied the envelope on IB-rt-8's controller structure**, ten edits, `0 of 57` after.
6. **Measured the layer before touching it**, read the published zip member by member, and
   concluded a rebuild would be a 0-diff.
7. **Deployed one function**: ledger open, sentinel committed, upload, plan, apply, verify,
   close, commit -- in that order.
8. **Graded, filed four rows, and reported.**

## The decision that mattered: census, not diff

The amendment said to re-run arm (c)'s census over the merged module set. It would have been
quicker to re-apply the ten edits I had made before the merge. The numbers say why that would
have been wrong:

| | before the merge | at the merged tip |
|---|---|---|
| modules | 25 | 30 |
| except handlers | 49 | 57 |
| rendering the exception | 10 | 9 |

Of the nine at the tip, **two** were paths I had fixed before and seven were in code that did not
exist at my first cut -- including `dispatch.py`, a whole module the census had never read. A
remembered diff closes what you remember.

## The judgement call: an unconvergeable shared root

After my apply the export root read `No changes`. Half an hour later it planned
`0 to add, 2 to change, 1 to destroy`. I did not apply it, and the reasoning is the substance of
row `W3-S20`:

- `aws_iam_role_policy.render_host_export_evidence` is in the shared **state** and in no `.tf` of
  this branch -- applying **destroys** a live `s3:GetObject`/`PutObject` grant on the ycharts
  runner role.
- `aws_ssm_document.export_render_run` is declared here, but the live document is a sibling's
  version 3 -- applying **deletes** 21 command lines including the whole host preflight and the
  `RENDERER_MODULE_ABSENT` refusal branch.
- `module.irpt_export_render.aws_lambda_function.this` -- applying **reverts**
  `IRPT_PORTAL_ORIGIN` from `portal.opalcapital.co` to `opalinvest.dev`.

**The discriminator is one verifiable fact: this order changed no Terraform configuration at
all.** `git status --porcelain -- infra/aws/terraform/` is empty, so no diff in that plan can be
mine. The battery now prints every residual with its address and the reason it cannot be
converged from here, rather than reporting a bare non-clean plan or quietly passing.

## What went wrong, and what each cost

- **My ownership classifier called my own Lambda FOREIGN.** A module-nested address has the
  inner name `this`, which appears in no root `.tf`. That is the self-serving label the
  classifier exists to prevent, produced by the classifier itself. Fixed to attribute a
  `module.X.*` address by the **module** name.
- **It also called the SSM document "OURS"**, because this branch declares that resource -- when
  the diff was that the live content is newer. Reading the actual removed lines is what showed
  it. *Declared here* and *ours* are different claims.
- **Four roots reported `rc 1`** in the first graded run: a missing `terraform init` in a new
  worktree. An rc is not a reading, and I recorded it as a defect rather than as a plan result.
- **I nearly minted a row id in another slot's namespace** (`W4-S16`, where `W4` is a sibling's).
  Caught before the rows were written; a worker mints only `<CODE>-W<its own slot>-S<k>`.
- **The whole-tree export tests read `4 failed`.** Established as pre-existing by running the
  pristine tip via `git archive` into a temp directory -- `5 failed, 61 passed, 2 skipped` there
  against `4 failed, 64 passed` here. No regression, one better, and the cause is row `W3-S22`.
  (`git stash` was refused by the shared-worktree gate, correctly.)

## Bounds honoured

- **No live vendor call.** Reads are AWS control-plane, S3 and one Lambda invoke, all
  Opal-owned.
- **No monitor, alarm, SNS or SES.**
- **Nothing outside the grant.** The layer builder, `lambda-layer-map.json` and the
  `performance`/`narrative` roots are **not** in this order's `<paths>`. Arm (e) step (3) is
  satisfied by MEASURING that the published layer already carries the union rather than by
  republishing it from a root I do not hold -- and the measurement is recorded so a grader can
  check it.
- **No `.tf` touched at all** -- which is also what makes the attribution in arm (e) checkable.
- **Four findings surfaced and deliberately not fixed:** the split two-part change's general
  shape, the sibling on the shared root, the layer's stale manifest, the `dispatch` collision.

## Rows filed

`W3-S19` (a two-part change split by the drain) · `W3-S20` (a sibling writing the shared export
state) · `W3-S21` (the layer's manifest disagrees with the published layer) · `W3-S22` (two
`dispatch.py` modules collide on the flat path).

## Commits (all LOCAL on `wk-irpt_bckend-2-3`)

| hash | subject |
|---|---|
| `862b0e4a6e` | the envelope re-applied on IB-rt-8's controller, the import closure closed, and the OPEN sentinel before the act |
| `1577717530` | close the change-management entry -- all five legs proven |

Plus the closing commit carrying this log, the result document, the battery, its output, the four
channel rows, the proof instance and the `<status>` flip to `complete`.
