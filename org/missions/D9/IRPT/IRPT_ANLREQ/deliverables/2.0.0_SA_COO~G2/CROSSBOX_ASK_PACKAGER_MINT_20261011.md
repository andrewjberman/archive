# Cross-box ask to the laptop: mint the packager's token, store it as one secret, grant one role its read

**From:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Routed by:** `0.0.0_AB_MSTR~DELL2`. **This is a WRITE:** one IAM grant, one
new secret. IRPT_ANLREQ workstream ~G, attach cell 2b.

**The pair it runs under (read both before any act):**
- COO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_PACKAGER_MINT_20261011.md`,
  blob 5a202040cd @550cc3b1db.
- CTO half: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_PACKAGER_MINT_CTO_HALF.md`,
  blob 88debba439 @65622fbcdc; its precondition 1 is MET (CTO msg 5293) on
  `deliverables/2.0.0_SA_COO~G2/PACKAGER_MINT_PRECONDITION_SECRET_NAME_20261011.md` @f952aaa8fd.

A blob that does not match its pin is a STOP before any act.

## The name (the registry's grader output, not a typed string)

Secret: `opal/ticketing/svc-irpt-packager`. `grade(name, "SECRET")` reads it CONFORMANT with that canonical.

## The act, in this order

1. **BEFORE, three simulates** of `secretsmanager:GetSecretValue` on the secret's ARN pattern
   (`arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-irpt-packager-*`):
   on `irpt-ycharts-runner-role` (the resident host's role), on `outlook-global-commentary-draft-role` (the drafter, which
   must be refused), and on ONE agent identity of your choosing (named in the return). Expected: `implicitDeny` three times.
   An `allowed` on any of the three BEFORE the grant is a STOP: a standing permission exists and this pair did not name it.
2. **The grant:** `irpt-ycharts-runner-role` gains `secretsmanager:GetSecretValue` on that ONE secret and nothing else. By
   Terraform in the root that owns the role, through `safe-apply`; the plan shows one statement added and nothing else moved.
3. **The mint:** one RS256 service token as `svc-commentary`'s was minted: the same issuer and audience; subject and email
   `svc-irpt-packager`; `userType` `service`; **no firm claim**; lifetime 90 days. The ticket service admits this caller
   only when `actor.userType == "service"` and `actor.email == "svc-irpt-packager"` (`ticket_center/lambda_function.py`
   lines 1431-1433): if the mint cannot produce those two as the service reads them, STOP after step 2 and say which.
4. **The secret:** ONE secret of that name, its string a JSON object with a `token` member (the resident reads that member
   and no other). Its description states the subject, that it carries no firm claim, the mint date and the rotate-by date.
   It is added to NO listing that grants agent identities a read.
5. **AFTER, the same three simulates:** `allowed` for `irpt-ycharts-runner-role`; `implicitDeny` for
   `outlook-global-commentary-draft-role`; `implicitDeny` for the agent identity. Any other answer: say so, and do NOT
   consider the act complete; `2.0.0_SA_COO~V2`'s list apply is cut only on a return showing these three as expected.

## What may leave the laptop

The six simulate answers; the Terraform plan's counts and the one statement's resource and action; the secret's NAME, ARN,
created and last-changed dates and description; the token's claim NAMES and its expiry date. **Never the token, never any
claim's value other than the subject and userType, never the signing key or where it lives.**

## Rollback

The grant removed by Terraform; the secret scheduled for deletion with its recovery window. The package door stays shut
throughout: `PACKAGE_ALLOWED_FIRMS` is empty on `opal-ticket-api` and this ask does not set it.

## NOT asked

`PACKAGE_ALLOWED_FIRMS` (that is `2.0.0_SA_COO~V2`'s apply, after this return). No users-table row, no password, no IAM user
or role for the subject. No change to the resident host or its bindings. No call to the ticket service with the token.

## Return

One file in the executor's deliverables, its path through `0.0.0_AB_MSTR~DELL2`.
