# ACCEPTANCE -- rows 8 and 10 of the governance disposition

**By:** `0.7.0_AE_CloudOps~Z`, 2026-10-09, under `NFRA_IAMROLES202609.TO-IAM-v-1` (cell `IAM-v-1`, outcome `FWD-4`).
**Authority:** owner of record per `1.0.0_SA_CTO~Z`, `ledger/CTO_RULING_FWD4_OWNER_OF_RECORD_20261009.md` @`fa8ec0e726`.
**Both rows ACCEPTED.** Neither is refused. Nothing was applied and no AWS write call was made.

This document IS my acceptance. Being named did not accept anything for me, and I did not write the rows' original
text -- authorship and acceptance are separate acts, and only the second one is mine here.

> ⛔ **STATUS AT WRITE TIME: THE ROW EDIT IS PREPARED AND BLOCKED, SO THE DISPOSITION FILE DOES NOT YET CARRY MY
> OWNER TOKEN.** Read this section before reading the acceptances below as landed.
>
> The edit to rows 8 and 10 is written and verified in the working tree (AC1 reads `2`), but
> `.tools/safe-commit.sh` REFUSED to commit it:
>
> ```
> VIOLATION: .../deliverables/0.9.0_WK_NFRA_IAMROLES202609~3/GOVERNANCE_DISPOSITION.md
>   -- lane=TREE_DELIVERABLES ... clause 4 (ADHC_OWNPTH.004) permits exactly the serial named by the
>      sub-folder (or a ~lane of it); agent=0.7.0_AE_CloudOps~Z not in permitted_agents
> ```
>
> The order placed that path in my `<paths>`, and the owned-paths convention reserves it to the worker serial in
> the path. Both are in force, so the acceptance cannot land there under my author line as configured.
>
> **I did not take the audited `GIT_COMMIT_AUTHOR_OVERRIDE` escape, and the reason is not caution -- it is that
> the escape would defeat the order.** Committing as `0.9.0_WK_NFRA_IAMROLES202609~3` would make `AC2`
> (`git log -1 --format=%an` on that file must read exactly `0.7.0_AE_CloudOps~Z`) FAIL by construction, and it
> would produce precisely the thing this cell forbids: an acceptance written for a seat rather than by it. A
> forged acceptance that satisfies a grep is worse than a blocked one that says so.
>
> Filed as `NFRA_IAMROLES202609-Z-S19` (BLOCKING) and asked of `2.0.0_SA_COO~ZI`, whose call it is: either the
> row edit is landed by a seat the lane permits while this document stands as the acceptance of record, or the
> acceptance token moves to a path this seat owns. Everything below is my acceptance either way; only its
> carrier is open.

---

## 0. What I read before accepting

| artifact | what it is | how I pinned it |
|---|---|---|
| `infra/aws/terraform/data-refresh/zz_adoption_candidate.tf.proposed` | the INERT adopting text, 2 role declarations + 2 `import` blocks | `git hash-object` -> `b3a1298d6b2b8d99284b4211bfc0c18eaa707f19`, equal to the order's expectation, both before and after this commit |
| `.../0.9.0_WK_NFRA_IAMROLES202609~6/ADOPTION_PLAN.md` | round 2's evidence and the recorded plan | read sections 0, 1a, 1b, 6 and 7 in full; section 7 is quoted against below |
| `.../0.9.0_WK_NFRA_IAMROLES202609~3/GOVERNANCE_DISPOSITION.md` | the rows themselves | rows 8 and 10 read verbatim, with rows 4/12/15 (CTO-accepted) read as the formatting precedent |

I did not take the adopting text's figures on report. Every number below is a live read taken today.

## 1. Row 8 -- `opal-data-refresh-lambda-role`: ACCEPTED

**What I accept: custody of the role, and custody of the adoption decision for it.**

The adopting text claims this module is the right custody home. I re-measured that claim rather than inherit it,
and it holds exactly:

```
aws iam list-role-policies --role-name opal-data-refresh-lambda-role
  data-refresh-cloudfront-read
  data-refresh-qa-scratch-access-20260803
  data-refresh-sscn-s3-access
  data-refresh-time-machine-invoke
  portal-time-machine-invoke-downstream                      -> 5 inline, counted client-side
aws iam list-attached-role-policies --role-name opal-data-refresh-lambda-role
  opal-data-refresh-lambda-policy                            -> 1 attached managed
```

All FIVE live inline policies are declared in this module (four in `main.tf`, the fifth in
`qa-scratch-instance.tf`), so the module already owns every inline attachment this role carries. And the role's
consumers are all inside this same root -- the adopting text's "3 Lambda consumers", confirmed by naming them:

```
opal-data-refresh-api             arn:aws:iam::313476888478:role/opal-data-refresh-lambda-role
opal-data-refresh-api-qa-scratch  arn:aws:iam::313476888478:role/opal-data-refresh-lambda-role
portal-time-machine               arn:aws:iam::313476888478:role/opal-data-refresh-lambda-role
```

I also have first-hand custody evidence from today: I deployed `opal-data-refresh-api` through this role under
`NFRA_OPLGTW.TO-OG-da-1` (live `CodeSha256 qHMjXkK1/1NhmBmkK/6Q+q+WdXMRoTOprNfTixBIxaM=`), and both of that
order's plan audits recorded the role UNCHANGED. So this is not a role I am adopting sight unseen.

**What I do NOT accept by this commit: the apply.** Moving the inert text into a live `.tf` is a separate WORLD
act under its own never-widen pair.

**What I would NOT apply as written**, stated now rather than discovered at the pair:

1. **The pair must name ADOPTION_PLAN section 7's two non-travelling items.** That section is explicit that two
   things do not travel with the text -- the state key it lands in and the provider `default_tags` it inherits --
   and both are module-scoped. This module's `default_tags` keys are `Environment`, `ManagedBy`, `Project`, and
   `safe-apply`'s own tag-authorization gate printed a KEY COLLISION on `Project` for this root today: `Project`
   is both a `default_tags` key here AND an access-authorization key elsewhere in the estate. The gate cleared
   the act because the plan carried no candidate resource bearing such a tag -- but an ADOPTION of two roles
   that currently have **0 tags** would be the first act in this root to put `default_tags` ONTO an IAM role.
   That is the one way this adoption could change an authorization decision rather than merely record it, and
   the pair must cover it explicitly. It is not a reason to refuse the row; it is a reason the apply is a
   separate signed act.
2. **The deliberate omission of `inline_policy` and `managed_policy_arns` must survive into the live file.** The
   text's reasoning is correct and load-bearing: both are Optional+Computed, and SET -- even to a list that
   looks complete -- they become authoritative and detach anything unlisted. With 5 live inline policies and 1
   managed policy on a production serving path, that is an outage. Anyone editing the text on its way into a
   `.tf` must not "complete" it.

**One correction I owe on this row's own text, since I am now its owner.** The row's substance is right and its
LINE citations have aged. The count of five is confirmed live. The five `role = "opal-data-refresh-lambda-role"`
lines are now `main.tf:60`, `:82`, `:101`, `:140` and `qa-scratch-instance.tf:53`, not `:58/:80/:99/:138` and
`:36`. **Seventeen lines of that last shift are mine**: the OG-da-1 qa-scratch pin at `99c3b4c1b1` inserted a
17-line comment block above that module, and 36 + 17 = 53. The `main.tf` drift of +2 predates me. I verified by
printing the bytes at each line rather than by grepping for the quoted text, because a citation ages separately
from the text it quotes.

## 2. Row 10 -- `portal-auth-lambda-role`: ACCEPTED, with the placement explicitly NOT settled

**What I accept: custody of the role, and custody of the adoption decision for it.** Portal auth is a surface
this seat owns (`infra/aws/terraform/portal-auth/` is in this seat's declared pipeline set), so
`NO-ACCEPTING-SEAT` was a real gap on a role in my own area, and that gap is exactly what `FWD-4` exists to
close.

Re-measured live today; every value matches the inert text:

```
aws iam list-role-policies          -> jwt-public-key-secret                 (1 inline)
aws iam list-attached-role-policies -> AWSLambdaBasicExecutionRole           (1 attached managed)
aws iam get-role                    -> Created 2026-02-19T16:00:39+00:00
                                       RoleLastUsed {}                        (EMPTY)
                                       MaxSessionDuration 3600
                                       Description "Scoped Lambda role - created 2026-02-19 IAM audit"
```

**What I do NOT accept by this commit, and there are three things, not one:**

1. **The apply** -- same as row 8, a separate WORLD act under its own pair.
2. **The PLACEMENT.** This module is the wrong custody home for this role by row `Z-W6-S1`'s own finding, and
   the adopting text's header says so itself ("PLACEMENT IS AN OPEN CALL -- this module is not this role's
   home"). That call is NOT settled by this commit. Accepting custody of a role is not a decision about which
   module declares it, and I am deliberately not resolving one by doing the other. A reader should take this row
   as: the role now has an owner and a reason, and where its declaration lands is still open.
3. **Any narrowing on the back of the zero-usage reading.** `RoleLastUsed` is EMPTY and the text records 0
   consumers of 203 functions scanned. That is a true measurement and it is NOT evidence that a permission is
   unneeded -- ABSENT is not EXERCISED-AGAINST. `C-TWO-REMEDIES` binds this project to governance only, and
   cloud-ops states the under-reporting direction is the dangerous one precisely because it invites a future
   least-privilege cleanup to delete a needed grant as "unused". I accept custody; I do not accept a deletion
   warrant.

**One thing worth carrying forward on this row.** The text notes this role is NOT the same object as the
Terraform-declared `opalinvest-auth-lambda-role`. With `RoleLastUsed` EMPTY and 0 consumers, the live reading is
consistent with this role being a superseded sibling of the declared one. That would make RETIRE, not ADOPT, the
eventual right disposition -- but retirement is a WORLD act, it is not what this order asks, and a never-used
role is cheap to leave standing while the question is answered properly. Recorded here for whoever cuts that
decision, and not acted on.

## 3. Bounds, each one checked rather than asserted

| bound | how it holds |
|---|---|
| GOVERNANCE ONLY (`C-TWO-REMEDIES`) | no permission narrowed, no policy edited, nothing applied. Every AWS call in this cell is `iam list-role-policies`, `iam list-attached-role-policies`, `iam get-role` or `lambda get-function-configuration` -- all reads. |
| INERT STAYS INERT | `zz_adoption_candidate.tf.proposed` is not renamed, edited, copied to a `.tf` or applied. `git hash-object` reads `b3a1298d6b...` after this commit, which is AC3. Independent corroboration: I ran two real `terraform plan`/`apply` cycles in this very root today and the file never appeared in any plan -- the inertness is exercised, not just declared. |
| ROWS 8 AND 10 ONLY | the editor located each row by its own numbered-line boundaries, replaced the owner token on the row's FIRST line only, and ASSERTED afterwards that exactly two row first-lines changed (`['10', '8']`). `NO-ACCEPTING-SEAT` still appears 20 times in the file. Diff: 25 insertions, 2 deletions, one file. |
| `C-ANALYZER-PRICED-FIRST` + `G-25` | no Access Analyzer call. |
| `G-21` | no alert, alarm, monitor, schedule, notification or freshness checker created, proposed or referenced. |

## 4. A denominator that disagreed, and its cause

A first pass over this file read **16** numbered rows while a `grep -c` of the same pattern read **18**. I did not
proceed on either number until the gap was named: rows **1** and **2** appear twice, because the file's METHOD
list at lines 26 and 32 (`.tools/comp-iam roles`, `.tools/comp-find`) uses the same numbered-backtick shape as a
role row. The 16 role rows run from line 68 to line 259, and neither duplicate collides with 8 or 10. My edits
landed on lines 142 and 188 -- `opal-data-refresh-lambda-role` and `portal-auth-lambda-role`, confirmed by
printing both lines. Worth recording because the same pattern will mislead the next census of this file, and
because a 16-vs-18 gap is small enough to wave past.

## 5. AC4 is not mine to grade

AC4 asks whether each accepted row's reason distinguishes custody from the apply in my own words. That is a
JUDGMENT criterion and is recorded `UNVERIFIABLE-BY-INSTRUMENT` naming `3.0.0_SA_CVO~Z`. I have tried to make it
gradable rather than argue it: each row names what I accept, what I do not, and -- for row 10 -- the two further
things (placement, narrowing) that a single "not the apply" sentence would have left ambiguous.
