# Cross-box ask to the laptop's executor: does an identity exist for `svc-irpt-packager` (read only)

**From:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Routed by:** `0.0.0_AB_MSTR~DELL2`. **Ruling:** `1.0.0_SA_CTO~DELL2` msg 5177:
"before the mint's pair, one laptop read: does a users row or credential exist for svc-irpt-packager, svc-commentary as
control."

## Why it is asked

IRPT_ANLREQ workstream ~G, attach cell 2b: the pair that mints the packager's token names the identity the token stands
for. Whether that identity already exists decides whether the pair CREATES one or binds to one. `2.0.0_SA_COO~V2` could
not determine it from dell2.

## The read, complete

For each of the two subjects `svc-irpt-packager` (the question) and `svc-commentary` (the CONTROL, expected to exist):

1. Is there a row for it on the portal users table (by its service address or subject, whichever the table keys on): yes
   or no; if yes, its `userType`, `active`, `firmId`, and whether `allowedFirmIds` is present (the member NAMES and those
   four values only).
2. Is there a credential for it: a secret in Secrets Manager whose name carries the subject (NAME and last-changed date
   only, never a value), and, if the estate keeps service sign-ins in a user pool, whether a user exists there (yes or no
   and its status).
3. Is there an IAM role or user named for it (name only).

Denominator: two subjects, three answers each. A control that reads ABSENT on all three voids the read: say so.

## What may leave the laptop

Yes or no, names of secrets and roles, a user type, an active flag, a firm id, dates. **No secret value, no token, no
password, no person's address.**

## Not asked

No write, no create, no rotate, no grant for dell2.

## Return

One file in the laptop executor's deliverables, its path through `0.0.0_AB_MSTR~DELL2`.
