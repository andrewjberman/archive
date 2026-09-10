# NFRA_IAMROLES202609.TO-IAM-s-2 -- The POSTURE NUMBER

FWD-1, acceptance property 1: someone can state the least-privilege posture with a number, what it
is out of, and when it was taken -- with that evidence attached, rather than an opinion.

## The number

```
POSTURE: 8 of 22 granted permissions on opal-data-refresh-lambda-role carried an observed usage
verdict (used or never-used) under a 90-day lookback, vintage 2026-09-10.
```

`claim: measured` -- both integers are read live off IAM Access Advisor at render time (below),
never copied from a prior write-up or scaled from any other cell's figure.

## What the two integers are, and are NOT

This is a ROLLUP OF `IAM-s-1` AND NOTHING ELSE, per the cell's own bound. `IAM-s-1`'s instrument
(`comp-iam-usage permission-cold`) measured exactly ONE role's granted-permission set at PERMISSION
grain. The rollup therefore inherits that scope exactly -- it is a posture number for the one role
IAM-s-1 exercised, not for the estate's role population, and this file says so rather than letting
the outcome text's "the estate's" read as a broader claim than the underlying measurement supports
(A VALUE MUST CARRY ITS CLAIM).

- **Denominator (22):** the DESIRED-plane count of granted permissions on the role -- the union of
  Allow-actions across its attached-managed and inline policies, read live. This is IAM-s-1's own
  printed `DENOMINATOR` line, not an estimate.
- **Numerator (8):** `used` (6) + `never-used` (2) -- the two bands of `IAM-s-3`'s coverage
  vocabulary that mean "Access Advisor produced a usage verdict for this permission," i.e. the
  count of things actually CHECKED. This is exactly the rollup COVERAGE_VOCABULARY.md section 7
  names for this cell: *"IAM-s-2 ... can build `used + never-used` as its numerator/rollup input
  and must carry `unobservable`'s count and reason-set alongside any headline figure."*
- **What is excluded from the numerator, on purpose:** `unobservable` (14 of 22, 64% -- the
  LARGEST band on this role) is never folded into the numerator and never silently dropped from
  the denominator. A permission this instrument could not observe is not "checked," and counting
  it as checked would be exactly the forbidden reading PRD section 8's S3 bound names ("a grant
  nobody looked at must never render as a grant shown clean"), one level up from `never-used` --
  here it would be a grant nobody looked at rendering as CHECKED, which is the same failure shape
  applied to the coverage figure instead of the usage verdict.

**C-COVERAGE-OVER-COUNT, applied:** the honest headline is `8 of 22`, not `22 of 22` and not a
disguised `24 of 22` from double-counting. A number that quietly credited the 14 unobservable
permissions as "checked" would be larger and more flattering, and false. Stating `8 of 22` plus the
14-permission unobservable band beside it is the smaller, honest number this bound requires.

## The unobservable band, carried alongside the headline (not hidden)

14 of 22 granted permissions on this role are `unobservable` -- Access Advisor produced NO usage
verdict for them, for reasons split as follows (reason-set, per COVERAGE_VOCABULARY.md's own
per-row `reason` field, re-read live):

| cause | permissions | count |
|---|---|---|
| service has no action-level tracking in Access Advisor | `dynamodb:DeleteItem`, `dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:Query`, `dynamodb:Scan`, `dynamodb:UpdateItem`, `lambda:InvokeFunction`, `s3:CopyObject`, `s3:DeleteObject`, `s3:GetObject`, `s3:GetObjectVersion`, `s3:ListBucket`, `s3:PutObject` | 13 |
| action not in Access Advisor's tracked-action list for a tracked service | `logs:PutLogEvents` | 1 |

None of these 14 renders `used` or `never-used`; none is silently omitted from the 22. A reviewer
reading only the headline `8 of 22` and stopping there would still be told, on the same page, that
the majority of this role's grants (14 of 22) were never inspected at all -- "nobody has measured
it" stops being the honest answer for the 8, and stays the honest answer, stated as such, for the
14.

## The plane this number is NOT about (named, so it is not conflated)

This is a PERMISSION-grain figure on ONE role. It is not, and must not be read as:

- **The role-population plane** (`comp-find --corpus aws IAM_ROLE`, currently 219 live nodes,
  DECLARED=203 / LIVE-no-DECLARED=16 at vintage `2026-09-10 03:31:02 UTC` per the decomposition's
  own re-grounding). That denominator moved across three prior vintages while this project's
  decomposition was being written and is a DIFFERENT plane's number entirely -- roles that exist,
  not permissions checked on one role. It is not folded in here, per the cell's explicit bound, and
  no digit of that stale brief-era population figure appears anywhere in this file.
- **`comp-iam`'s Terraform-parse gap count (304)** or **the 16 undeclared roles** (`IAM-s-5`/`S6`'s
  planes) -- different instruments, different denominators, explicitly excluded by the cell text.
- **The condition axis** (`IAM-s-4`) -- a different axis on the same permissions, not this figure.

## Live re-derivation (this cell's own read, not inherited)

Re-run fresh for this cell, from this worktree, against the same role `IAM-s-1` exercised (its
determinism control already showed two back-to-back live reads diff byte-identical; this is a
third read, taken independently for this cell's own vintage rather than copied from that record):

```
$ .tools/comp-iam-usage permission-cold --role opal-data-refresh-lambda-role --lookback 90
comp-iam-usage permission-cold -- PERMISSION-grain usage for role 'opal-data-refresh-lambda-role' (ADVISORY; NEVER deletes)
  lookback 90 days | granted permissions examined (DENOMINATOR)=22
  counts: used=6 never-used=2 unobservable=14

    never-used     cloudfront:GetInvalidation
    never-used     logs:CreateLogGroup                       last-used=2026-01-19 (234d ago, outside 90d lookback)
    used           cloudfront:CreateInvalidation             last-used=2026-08-01 (39d ago)
    used           cloudfront:GetDistributionConfig          last-used=2026-08-01 (39d ago)
    used           logs:CreateLogStream                      last-used=2026-09-04 (5d ago)
    used           states:DescribeExecution                  last-used=2026-09-04 (5d ago)
    used           states:GetExecutionHistory                last-used=2026-09-04 (5d ago)
    used           states:ListExecutions                     last-used=2026-09-04 (5d ago)
    (14 unobservable rows: see the reason-set table above)
```

`used=6 never-used=2 unobservable=14`, `6+2+14=22`, matching the tool's own printed denominator
line exactly -- and matching `IAM-s-1`'s originally-landed run digit for digit, which is the
determinism this rollup leans on rather than re-asserting. Numerator = `6+2=8`. Vintage stamped at
this re-derivation: `2026-09-10` (`date -u` at render time, same UTC day as this cell's own
worktree session).

## Read as an answer, not an artefact (FWD-1's ACCEPT, in plain terms)

Asked "are we following least privilege?" for `opal-data-refresh-lambda-role`, the honest answer
this file supports is: *"8 of its 22 granted permissions have been checked for use over the last
90 days as of 2026-09-10 -- 6 are in active use, 2 have not been used in that window (candidates
for tightening, human-gated, never auto-revoked by this instrument) -- and 14 of the 22 (the
majority) could not be checked at all, because this AWS account's Access Advisor does not track
those services or actions at action grain. Nobody has measured whether those 14 follow least
privilege; that is stated, not hidden."* That is a number, a denominator, a vintage, and an
explicit account of what it could not see, on ONE role -- exactly the scope `IAM-s-1` produced and
nothing wider. Whether this is the kind of answer FWD-1's ACCEPT sentence asks for is judged at L9
(AC5 of this cell's task order), not by this builder.
