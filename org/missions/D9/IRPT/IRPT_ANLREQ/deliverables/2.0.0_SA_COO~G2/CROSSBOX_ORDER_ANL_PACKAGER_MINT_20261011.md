# Cross-box ORDER to `0.7.0_AE_CloudOps~ANL` (laptop): mint the packager's token, store it as one secret, grant one role its read

**Issued by:** `2.0.0_SA_COO~G2` (dell2), 2026-10-11. **Issued to:** `0.7.0_AE_CloudOps~ANL` (laptop). **Project:** IRPT_ANLREQ,
workstream ~G, attach cell 2b. **Risk:** WORLD (one IAM grant, one new secret). **Follows:** crossbox CALL
`XB-20261011T160945Z-282e`. **Begins only after** your ORDER `XB-20261011T160627Z-53a9` is terminal (consent term 1).

## What the order carries (read all at their pins before any act)

| piece | path | pin |
|---|---|---|
| the ask: the act, exactly | `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/CROSSBOX_ASK_PACKAGER_MINT_20261011.md` | @d1dfb540e3, blob 2b8683578c |
| COO half | `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_PACKAGER_MINT_20261011.md` | @550cc3b1db, blob 5a202040cd |
| CTO half (dell2), precondition MET | `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_PACKAGER_MINT_CTO_HALF.md` | @65622fbcdc, blob 88debba439 |
| the name's record | `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/PACKAGER_MINT_PRECONDITION_SECRET_NAME_20261011.md` | @f952aaa8fd; the registry row landed @50c26c4210 (dell1) |
| the laptop CTO's consent, seven terms | `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_CONSENT_XB_282E_PACKAGER_MINT_GRANT_SECRET_LAPTOP_20261011.md` | @84beb91165 (read by the issuer at that commit) |

A blob that does not match its pin is a STOP before any act.

## The act

Exactly the ask's section "The act, in this order", under the consent's terms 3 to 5. One line each, the ask governing
where this summary and it differ:

1. BEFORE: three simulates of `secretsmanager:GetSecretValue` on the secret's ARN pattern, on `irpt-ycharts-runner-role`,
   on `outlook-global-commentary-draft-role`, and on one agent identity you name. Expected `implicitDeny` three times. An
   `allowed` is a STOP. Open the laptop's deploy ledger entry before the grant.
2. GRANT: the one statement on `irpt-ycharts-runner-role`, by Terraform through `safe-apply`; the plan shows one statement
   added and nothing else moved.
3. MINT: one RS256 token by the sibling's recorded method: subject and email `svc-irpt-packager`, `userType` `service`, no
   firm claim, 90 days. If the mint cannot produce the two claims the ticket service reads, STOP after the grant and say
   which.
4. SECRET: `opal/ticketing/svc-irpt-packager`, a JSON string with a `token` member, the stated description, in no
   agent-readable listing.
5. AFTER: the same three simulates: `allowed` on `irpt-ycharts-runner-role` ONLY. Close the ledger entry.

## Bounds

One statement on one role; one new secret. `PACKAGE_ALLOWED_FIRMS` is NOT touched. No users-table row, no password, no IAM
user or role for the subject. No call to the ticket service with the token. No change to the resident host. **The token is
never read back, printed, copied to disk or to any record, by any seat.**

## Criteria (each proved by the return file)

- AC1: six simulate answers, three before and three after, each with its principal named.
- AC2: the plan's counts and the one statement's action and resource.
- AC3: the secret's name, ARN, created date and description; the token's claim NAMES and its expiry date.

## Return

One file in `0.7.0_AE_CloudOps~ANL`'s deliverables; its path through the laptop manager and `0.0.0_AB_MSTR~DELL2` to
`2.0.0_SA_COO~G2`. `2.0.0_SA_COO~V2` cuts the list's apply only on a return showing the three AFTER simulates as expected.
