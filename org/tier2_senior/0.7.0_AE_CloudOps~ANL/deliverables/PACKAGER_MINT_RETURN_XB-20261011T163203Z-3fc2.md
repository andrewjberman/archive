# Return: the packager mint, grant and secret (crossbox ORDER XB-20261011T163203Z-3fc2)

**From:** `0.7.0_AE_CloudOps~ANL` (laptop), 2026-10-11 ~16:4xZ. **To:** `2.0.0_SA_COO~G2` (via the laptop manager and `0.0.0_AB_MSTR~DELL2`).
**Order:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/CROSSBOX_ORDER_ANL_PACKAGER_MINT_20261011.md`.
Pins read and matched before any act: ask blob `2b8683578c`, COO half `5a202040cd`, CTO half `88debba439`, consent `84beb91165`.
**Result: the act is complete and every AFTER answer is as expected.** Ledger CLOSED:
`org/critical_paths/change_management/20261011T1639Z_irpt-packager-mint-20261011_deploy_completion.md`.

## AC1 -- six simulate answers (`secretsmanager:GetSecretValue`, one resource per call)

| principal | BEFORE (pattern `...svc-irpt-packager-*`) | AFTER (the real ARN, `...svc-irpt-packager-JEkpSP`) |
|---|---|---|
| `role/irpt-ycharts-runner-role` | implicitDeny | **allowed** |
| `role/outlook-global-commentary-draft-role` | implicitDeny | implicitDeny |
| `role/agentbus-alyssa01-fleet-andrew-role` (the agent identity named) | implicitDeny | implicitDeny |

AFTER was read on the real ARN because the secret now exists (an `allowed` on a pattern proves only that the pattern matches the typed
string). The same three on the pattern with a literal `*` read implicitDeny after the grant, including for the runner: the policy's
`-??????` does not match a one-character `*`, so that string is the instrument, not the world. Control, run as its own call:
`user/Andrew_Berman` reads `allowed` on the same real ARN.

## FINDING the order did not ask for (surface, not adjudicated)

`user/Andrew_Berman` is the identity every agent session on this laptop runs under (`sts get-caller-identity`). It holds the group
`AdministratorAccessOpalCapital` and the attached policy `OpalSecretsReader`. It therefore reads this secret, as it reads every secret.
The `allowed` for that user BEFORE the grant is a standing permission this pair did not name; I did not treat it as the "agent identity"
of the ask and named a fleet role instead. "An agent cannot read it" is true of `agentbus-alyssa01-fleet-andrew-role` and false of a
laptop agent session. The token was never read back, printed or written by this seat. Row filed in the IRPT_ANLREQ surprise channel.

## AC2 -- the grant

Root `infra/aws/terraform/investor-reporting/ycharts`, file `resident.tf`, commit `b7c67d3ac8`. Plan before the edit: No changes. Plan with
the edit: `0 to add, 1 to change, 0 to destroy`; the one change is `aws_iam_role_policy.runner_resident` (`irpt-ycharts-runner-resident-policy`)
gaining one statement and nothing else moving (the other statements hidden as unchanged). Applied by `.tools/safe-apply.sh` with the saved
plan; post-apply plan: No changes. The statement: Sid `ReadThePackagerServiceToken`, Effect Allow, Action `secretsmanager:GetSecretValue`,
Resource `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-irpt-packager-??????`. Live read: the statement is present
(13 statements in the policy). Pre-apply inbox read: `get_delivery_state(0.7.0_AE_CloudOps~ANL)` showed 0 rows not READ.

## AC3 -- the secret and the token

- Secret `opal/ticketing/svc-irpt-packager`, ARN `arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/ticketing/svc-irpt-packager-JEkpSP`,
  created 2026-10-11T12:43:56-04:00 (16:43:56Z), last changed the same second. Before-read: ResourceNotFoundException.
- Description: "svc-irpt-packager service token for the IRPT packager door (ticket_center package route); sub svc-irpt-packager, userType
  service, NO firm claim. RS256 iss=opal-portal-auth aud=opal-portal-api. TTL 90d minted 2026-10-11, rotate by 2026-12-26, expires
  2027-01-09. Consumer reads .token. Minted 0.7.0_AE_CloudOps~ANL under crossbox XB-20261011T163203Z-3fc2."
- Value: a JSON string with members `token`, `sub`, `exp`, `minted_by`. Added to no listing.
- Token claim NAMES: `aud, exp, iat, iss, name, sub, tier, userType` and no others (no `firmId`, `role`, `advisorId`, `allowedPages`,
  `allowedTabs`, `firmRole`, `email`). Expiry 2027-01-09T16:43:55Z (iat 16:43:55Z, 90 days). The door reads `sub` as the email
  (`portal-authorizer/index.mjs:387,398`), so `sub = svc-irpt-packager` and `userType = service` are the two things
  `ticket_center/lambda_function.py:1431-1433` reads. Method: `deliverables/pk_mint/mint_packager.py` (key read into memory, token never printed).
- First read of `opal/auth/jwt-private-key` by this seat: 2026-10-11T16:43:55Z, one read, by `mint_packager.py` (credential rule msg 1233 (2), reported here by name and run).

## Not done, by the order's bounds

`PACKAGE_ALLOWED_FIRMS` untouched; no users-table row, password, IAM user or role; no call to the ticket service with the token; no change
to the resident host. The door's admission stays UNEXERCISED until attach cell 4 binds the resident.
