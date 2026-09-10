# CONDITION AXIS -- what a policy REQUIRES of the caller, not only what it scopes

Cell IAM-s-4, task order `NFRA_IAMROLES202609.TO-IAM-s-4`, serving outcome FWD-3:

> For any policy, a reviewer can see what it REQUIRES of the caller, not only what it lets
> them touch. DONE WHEN EXERCISED -- at least one real policy has been surfaced as perfectly
> scoped and yet requiring nothing of whoever calls it.

The reader that produces this axis: `condition-axis-reader.py` (this directory).
Invocation: `python condition-axis-reader.py --policy <path-to-a-terraform-iam-file>`.

## BOUND -- C-DESIRED-UNTIL-EXERCISED (task order BOUNDS, G-15 + acceptance property 3)

Every finding in this document is read from POLICY TEXT. That is **DESIRED**, never an
APPLIED state and never an EXERCISED one -- a document read is not a live state. Only a real
`aws iam simulate-principal-policy` battery (cell IAM-s-8, downstream, NOT this cell) can move
any of these claims past DESIRED. Nothing below reports as APPLIED or EXERCISED, and nothing
in this cell ran a simulate battery -- that instrument, and that verb, belong to IAM-s-8.

## THE EXHIBIT -- a perfectly scoped statement that requires nothing of its caller

Real policy, unmodified, read at `infra/aws/terraform/estate-report/iam.tf` (this cell reads
only -- narrowing is IAM-s-8's question and this cell does not touch the file):

```hcl
resource "aws_iam_role_policy" "runner_selfstop" {
  name = "estate-report-runner-selfstop"
  role = aws_iam_role.runner.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "SelfStopThisInstanceOnly"
        Effect   = "Allow"
        Action   = ["ec2:StopInstances"]
        Resource = ["arn:aws:ec2:us-east-1:${local.account_id}:instance/${aws_instance.estate_report_runner.id}"]
      },
    ]
  })
}
```

The reader's verdict on this exact statement, produced by the invocation above against this
exact file:

```
[aws_iam_role_policy.runner_selfstop (policy)] statement 1/1 -- Sid=SelfStopThisInstanceOnly Effect=Allow
    REQUIRES-NOTHING
```

This is the (action, resource) axis at its tightest: one action (`ec2:StopInstances`), one
ARN-pinned resource -- not a wildcard, not a tag-scoped `*`, the literal instance ID of the
one instance this role is even attached to. The file's own comment block explains why this
ARN-pinning was chosen over an earlier tag-conditioned form ("a tag condition is one
tag-write away from a wider grant"). Being that careful about WHAT the caller can touch does
not, on its own, ask anything about WHO the caller is or HOW they authenticated: no MFA
condition, no source-address condition, no principal-tag condition, no session-age condition
-- no Condition block at all. `REQUIRES-NOTHING` is the token that makes that absence VISIBLE
instead of leaving it silent inside a policy that otherwise reads as exemplary.

The same file carries more instances of the identical shape (also real, also read by the same
invocation, unmodified):

```
[aws_iam_role_policy.scheduler (policy)] statement 1/1 -- Sid=<unnamed> Effect=Allow
    REQUIRES-NOTHING

[aws_iam_role_policy.orchestrator (policy)] statement 1/3 -- Sid=StartRunnerInstanceOnly Effect=Allow
    REQUIRES-NOTHING

[aws_iam_role_policy.capture_writer (policy)] statement 1/1 -- Sid=PutTextInputAnyDayNeverDelete Effect=Allow
    REQUIRES-NOTHING
```

`StartRunnerInstanceOnly` is ARN-pinned to the same single instance from the caller side
(the orchestrator role); `PutTextInputAnyDayNeverDelete` is scoped to exactly one bucket
prefix pattern. Both are careful about scope. Neither asks anything of the caller.

## CONTRAST -- statements in the SAME file that DO require something

So the reader is not simply printing `REQUIRES-NOTHING` for everything it reads, the same
run surfaces two statements in this file that DO carry a Condition block:

```
[aws_iam_role_policy.runner (policy)] statement 3/5 -- Sid=ListOwnPrefixes Effect=Allow
    REQUIRES (DESIRED, read from policy text -- NOT yet EXERCISED):
      - StringLike  s3:prefix = ["daily/*", "manifest/*", "code/*"]   [call parameter -- scopes the LIST call, not the caller]

[aws_iam_role.outset_drift_publisher_laptop (assume_role_policy / trust)] statement 1/1 -- Sid=<unnamed> Effect=Allow
    REQUIRES (DESIRED, read from policy text -- NOT yet EXERCISED):
      - StringEquals  sts:RoleSessionName = "outset-drift-laptop"   [caller session identity]
```

These two are usefully different from each other, and the reader's advisory hint says so:
`ListOwnPrefixes`'s `s3:prefix` condition narrows WHICH KEYS a `ListBucket` call may
enumerate -- a call-parameter restriction, not a fact about the caller. The trust policy on
`outset_drift_publisher_laptop`, by contrast, pins `sts:RoleSessionName` to an exact string --
that IS a requirement of the caller (the assumed session must present that exact name), the
closest thing to the FWD-3 axis this file's population happens to contain. Neither of these
two is an MFA condition, a source-address condition, or a principal-tag condition -- this
file's population simply does not happen to carry one of those three; see the population
bound below for what that observation does and does not license.

Across the estate's other seven `iam.tf` files this cell may read (`mdpf-pipeline`,
`inf-pipeline`, `cot-pipeline`, `news-pipeline`, `etfs-reports`, `bd-pipeline`,
`fred-pipeline`), the same reader surfaces two more Condition shapes present in this estate's
text, offered as further real (not synthetic) contrast, each one DESIRED / unexercised same as
above:

```
$ python condition-axis-reader.py --policy infra/aws/terraform/bd-pipeline/iam.tf
[aws_iam_role_policy.step_functions_lambda_invoke (policy)] statement 3/3 -- Sid=<unnamed> Effect=Allow
    REQUIRES (DESIRED, read from policy text -- NOT yet EXERCISED):
      - StringEquals  ec2:ResourceTag/System = "BDGoldLayer"   [resource tag -- scopes the TARGET, not the caller]
```

That is a tag condition on the *resource*, not the caller (the reader's hint says so
explicitly) -- another way a Condition block can be present without ever answering "who is
this caller and how did they prove it".

## DENOMINATORS -- what was actually read, printed, never aggregated into a population claim

Each run below is one invocation against one file, `DENOMINATOR:` line quoted verbatim from
the reader's own output (this cell's write surface names these eight `iam.tf` files as READ
surfaces; all eight were read, none modified):

| file | statements examined | REQUIRES-NOTHING | REQUIRES | UNKNOWN |
|---|---|---|---|---|
| `estate-report/iam.tf` | 17 | 15 | 2 | 0 |
| `mdpf-pipeline/iam.tf` | 39 | 29 | 10 | 0 |
| `inf-pipeline/iam.tf` | 68 | 60 | 8 | 0 |
| `cot-pipeline/iam.tf` | 25 | 22 | 3 | 0 |
| `news-pipeline/iam.tf` | 27 | 27 | 0 | 0 |
| `etfs-reports/iam.tf` | 7 | 6 | 1 | 0 |
| `bd-pipeline/iam.tf` | 67 | 56 | 11 | 0 |
| `fred-pipeline/iam.tf` | 5 | 5 | 0 | 0 |

255 statements examined across these eight files; 220 carry `REQUIRES-NOTHING`, 35 carry a
Condition block this reader could resolve (`REQUIRES`), 0 fell to `UNKNOWN` (a Condition
block present but unparseable -- reserved and distinct from `REQUIRES-NOTHING` per the
comp-iam Rule-22a discipline this reader inherits: "a Condition block you cannot PARSE is
UNKNOWN, never REQUIRES-NOTHING").

## POPULATION BOUND (task order BOUNDS, PRD section 8 row S4 / brief Part VII item 5)

A pattern noticed across one policy, or across the eight files read for this exhibit, is an
inference from that read alone, and it is never a measured population claim. The table above
is a **denominator for eight files, read one at a time**, not a census, and not licensed to
become one. This document deliberately avoids the specific sentence shapes the task order
names as off-limits for exactly that reason -- a claim of the form "[the whole estate] +
[lacks/never uses] + [this axis]" is not supported by reading eight files one at a time, and
this cell is not commissioned to run the census that WOULD support it. What this document
licenses is narrower and sufficient for FWD-3's DONE WHEN: **at least one real, unmodified,
perfectly scoped policy statement has been surfaced, by the reader built for this cell, as
requiring nothing of its caller** -- `SelfStopThisInstanceOnly` above, plus two further real
instances in the same file, plus more again across the other seven files this cell was
permitted to read. A census of the whole estate's condition-key usage is explicitly NOT this
cell's commission (BOUNDS: "this cell is not commissioned to do that. Report what you read,
with its denominator, and stop there.").

## SCOPE HELD

This cell READS. No policy file was modified to produce this document or the reader above.
Narrowing any of the statements shown here (e.g. adding an MFA condition) is cell IAM-s-8's
question, not this one's, and applying any change is nobody's question in this round. No
alert, alarm, monitor, schedule or notification was created to produce this exhibit.
