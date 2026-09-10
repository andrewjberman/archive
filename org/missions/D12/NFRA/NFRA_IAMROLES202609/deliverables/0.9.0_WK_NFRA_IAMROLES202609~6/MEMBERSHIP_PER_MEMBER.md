# NFRA_IAMROLES202609 — IAM-r-3: TRUE membership of the undeclared set, per member, on a plane that did not build the set

**Cell:** `IAM-r-3` (FWD-4, acceptance property 1). **Worker:** `0.9.0_WK_NFRA_IAMROLES202609~6`.
**Worktree HEAD:** `5fa4a00cbccd4b84917f3d930972ddc39d2683b7`, branch `wk-NFRA_IAMROLES202609-6`.
**Terraform tree state at measurement:** `git status --short -- infra/aws/terraform/` = 0 lines
(clean, no untracked/modified files in this worktree); 415 tracked `.tf` files
(`git ls-files infra/aws/terraform/`). **Measured 2026-09-10.**

## THE SET UNDER TEST

The 16-member `LIVE-no-DECLARED` set, re-measured by this cell on its own vintage before checking any
member (the set has already been shown stable in name AND count by `IAM-s-5` and re-confirmed by
`IAM-r-2`; this is a fourth independent read, not a re-use of theirs):

```
comp-find '.' --corpus aws IAM_ROLE --all   (this cell, 2026-09-10)
VINTAGE: Built from the estate as of 2026-09-10 12:24:50 UTC. Stitch source: stitch-codebuild
         built 2026-09-10T03:01:17Z.  manifest: aebbd9cef8c4
DENOMINATOR: 219 hit(s) across 219 aws node(s) scanned [corpus=aws types=IAM_ROLE]
DRIFT (scanned): DECLARED=203 LIVE-no-DECLARED=16
```

⛔ **This comp-find read establishes WHO IS IN THE SET (the live-plane roster), not WHETHER the set's
classification is correct.** It is the same instrument family the cell's own bound calls out as
same-instrument agreement. Every verdict below is decided on a **different plane** — a read of the
committed Terraform source in this worktree — never on this roster repeating itself.

## METHOD

For each of the 16 names, this cell ran a literal-string content search over the whole committed
`infra/aws/terraform/` tree (native `Grep` tool, not the live graph, not `comp-iam`'s parser). A hit
is classed **DECLARED-IN-TF** only if it sits inside a `resource "aws_iam_role" "<label>" { name =
"<this exact string>" ... }` block — the block that would actually mint or adopt the role in
Terraform. Any other hit (a `role_arn` string, an `aws_iam_role_policy.role = "..."` attachment, a
comment, a mention) is a **reference**, not a declaration, and the member is classed **NOT-IN-TF**
with the hit count stated so a reader can see it is a nonzero-but-reference case rather than silence.

⚠ **Scope caveat carried forward from `IAM-r-2` and from this order's own preamble:** this worktree is
clean and does not contain the five untracked `.tf` files (four `aws_iam_role` blocks) present in the
shared main checkout that produced the battery's disputed "195". If any of the 16 names below is
declared ONLY in one of those untracked files, this cell's search cannot see it and will correctly —
but only for THIS committed tree — read it NOT-IN-TF. No such case was found among the 16 (the four
untracked blocks were not identified by name by any upstream cell), but the caveat is stated because a
reader diffing against the main checkout could see a different NOT-IN-TF/DECLARED-IN-TF split for a
member this cell did not test against that checkout.

## PER-MEMBER VERDICTS (16 of 16)

1. bd-merge-daily-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/` (recursive, all 415 tracked
   `.tf` files), hits: 0 (zero hits, no reference of any kind found)
2. bd-pipeline-task-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
3. codebuild-semantic-clustering-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
4. ecsTaskExecutionRole — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 for the literal role name
   (a case-insensitive widen to `ecsTaskExecution` alone found only four unrelated hits — managed
   policy ARN strings `arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy` in
   `globgrph/item2a.tf:251`, `globgrph/iam.tf:106`, `globgrph/projection.tf:194`,
   `globgrph/trino.tf:148` — a policy attachment reference, not a role declaration, and not this
   member's name even as a substring of a declared block)
5. finbert-ec2-backfill-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
6. lambda-ec2-runtime-monitor-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
7. lambda-test-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
8. opal-data-refresh-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 9, ALL references,
   ZERO are inside a `resource "aws_iam_role"` block — **NEGATIVE CONTROL**. Citations: `role_arn`
   strings at `infra/aws/terraform/data-refresh/qa-scratch-instance.tf:19`, `data-refresh/main.tf:38`,
   `data-refresh/main.tf:124`; `aws_iam_role_policy.role = "opal-data-refresh-lambda-role"`
   attachments at `data-refresh/qa-scratch-instance.tf:38`, `data-refresh/main.tf:60`,
   `data-refresh/main.tf:82`, `data-refresh/main.tf:101`, `data-refresh/main.tf:140`; one comment
   mention at `data-refresh/main.tf:53`. The module has zero `aws_iam_role` blocks for this name — the
   role is attached to and referenced by, never minted by, this Terraform tree.
9. opal-smartx-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
10. portal-auth-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits). Context
    (not a hit on this name, offered because it explains the near-miss risk): the `portal-auth` module
    (`infra/aws/terraform/portal-auth/iam.tf:15-16`) declares a role named
    `opalinvest-auth-lambda-role`, a DIFFERENT literal string, so it does not satisfy this member.
11. portfolio-management-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits).
    Context: the `portfolio-management` module (`infra/aws/terraform/portfolio-management/main.tf:226-227`)
    declares `portfolio-export-lambda-role`, a DIFFERENT literal string, so it does not satisfy this
    member either.
12. rds-monitoring-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0, including a
    case-insensitive widen on `rds.monitoring|monitoring.role` (0 hits)
13. **seeking-alpha-scraper-role — DECLARED-IN-TF** — **POSITIVE CONTROL** — citation:
    `infra/aws/terraform/seeking-alpha/main.tf:240-241`:
    ```
    resource "aws_iam_role" "seeking_alpha_role" {
      name = "seeking-alpha-scraper-role"
    ```
    The one confirmed false positive named in this cell's own preamble: it is inside the LIVE-no-DECLARED
    set (comp-find, above) yet a `resource "aws_iam_role"` block for this exact name exists in the
    committed tree.
14. sentiment_query_api-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)
15. vpc-flow-logs-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0, including a
    case-insensitive widen on `vpc.flow.log` (0 hits)
16. workspace-sync-lambda-role — NOT-IN-TF — scope: `infra/aws/terraform/`, hits: 0 (zero hits)

## SUMMARY

| # | member | verdict | hits | citation |
|---|---|---|---|---|
| 1 | bd-merge-daily-lambda-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 2 | bd-pipeline-task-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 3 | codebuild-semantic-clustering-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 4 | ecsTaskExecutionRole | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit (policy-ARN near-misses noted above) |
| 5 | finbert-ec2-backfill-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 6 | lambda-ec2-runtime-monitor-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 7 | lambda-test-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 8 | opal-data-refresh-lambda-role | NOT-IN-TF | 9 (all references) | `data-refresh/main.tf:38,60,82,101,124,140`, `data-refresh/qa-scratch-instance.tf:19,38`, `data-refresh/main.tf:53` (comment) |
| 9 | opal-smartx-lambda-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 10 | portal-auth-lambda-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 11 | portfolio-management-lambda-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 12 | rds-monitoring-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 13 | seeking-alpha-scraper-role | DECLARED-IN-TF | 1 declaration | `infra/aws/terraform/seeking-alpha/main.tf:240-241` |
| 14 | sentiment_query_api-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 15 | vpc-flow-logs-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |
| 16 | workspace-sync-lambda-role | NOT-IN-TF | 0 | `infra/aws/terraform/` — no hit |

**Total: 16 of 16 members carry a verdict. 1 DECLARED-IN-TF (the known false positive,
`seeking-alpha-scraper-role`), 15 NOT-IN-TF.**

## THE FINDING

This is the boring, real answer, stated as the bound requires rather than hunted past: of the 16
members of the `LIVE-no-DECLARED` set, exactly **one** — `seeking-alpha-scraper-role` — is a confirmed
false positive (declared, mis-classed). The remaining **fifteen** are genuinely undeclared on this
plane: a literal-string search of the entire committed `infra/aws/terraform/` tree (415 tracked files,
clean worktree) finds either zero hits at all, or (in `opal-data-refresh-lambda-role`'s case) hits that
are exclusively references to a role Terraform attaches policies to but never declares with an
`aws_iam_role` block. No second false positive was found, and none was manufactured to look for one.

This converts the round's "at most 15 genuinely undeclared" framing into a **measured 15**, each with
its own citation, on a plane (Terraform source) that did not build the live-graph set being checked.

## CONTROLS CARRIED

- **POSITIVE CONTROL** (`seeking-alpha-scraper-role`): DECLARED-IN-TF, `resource "aws_iam_role"
  "seeking_alpha_role" { name = "seeking-alpha-scraper-role" }` at
  `infra/aws/terraform/seeking-alpha/main.tf:240-241`. The probe fires on the known false positive.
- **NEGATIVE CONTROL** (`opal-data-refresh-lambda-role`): NOT-IN-TF despite 9 hits, all references
  (`role_arn` values and `aws_iam_role_policy.role =` attachments), zero `aws_iam_role` declaration
  blocks. The probe does not mistake a reference-heavy role for a declared one.

Both controls match the exact citations named in this task order's own preamble, independently
reproduced by this cell's own search rather than copied.

## SCOPE HELD

This deliverable establishes membership only — which of the 16 is genuinely undeclared and which is a
misclassification. It does not recommend adoption, exemption, removal or any other disposition for any
member; that is `C-TWO-REMEDIES` territory reserved for the three downstream disposition cells.
