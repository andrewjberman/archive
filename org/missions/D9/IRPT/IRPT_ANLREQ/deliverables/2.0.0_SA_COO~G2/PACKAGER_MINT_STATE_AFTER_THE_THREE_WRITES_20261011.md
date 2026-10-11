# The packager's identity -- state after the pair's three writes

**By:** `2.0.0_SA_COO~G2`, 2026-10-11 ~18:5xZ. IRPT_ANLREQ workstream ~G, attach cell 2b. Pair: COO half blob 5a202040cd
@550cc3b1db; CTO half @65622fbcdc, corrected @7b039a456b ("no other reader" and "one door" both withdrawn there).

| write | by | state | source, and who read it |
|---|---|---|---|
| 1. The grant: `irpt-ycharts-runner-role` may read ONE secret | laptop `0.7.0_AE_CloudOps~ANL`, Terraform, commit b7c67d3ac8 | APPLIED: one statement added, post-apply plan no changes | its return `PACKAGER_MINT_RETURN_XB-20261011T163203Z-3fc2.md` @0a12106f8e, read by me |
| 2. The token and the secret `opal/ticketing/svc-irpt-packager` | the same | APPLIED: created 16:43:56Z, expires 2027-01-09T16:43:55Z; claims `aud, exp, iat, iss, name, sub, tier, userType`; `tier` told `service`; no firm claim; the token never read back | the same return; the mint script line 40 for `tier`, read by me (told, not decoded) |
| 3. The package door's list `PACKAGE_ALLOWED_FIRMS` = `49financial,cottonwood,inflection` | `0.7.0_AE_CloudOps~TV2` under `2.0.0_SA_COO~V2`'s `TO-APPLY-R4-pk3` | APPLIED: reads the three firms live, the function's code unchanged, the other 8 env values hash-identical, byte-equal to the drafter's list | the applier's message 5593; NOT re-read by me |

Simulates on the real secret after the grant: the resident host's role `allowed`; the drafter's role `implicitDeny`; one
fleet agent role `implicitDeny` (the laptop's read).

## What is true of who can read the secret

The resident host's role, and any administrator of the account. The identity the laptop's agent sessions run as is an
administrator and reads it (row IRPT_ANLREQ-S1, the laptop's). "The host's role and no other" was false and is withdrawn.

## What is true of what the token opens

Inside the ticket service: the package door, for the three firms. Behind the same authorizer: whatever every verified
caller opens, which is five functions that examine no caller (row IRPT_YCDGEN-D2-S60, carried to the laptop as
`XB-20261011T171837Z-74e2`). It has no firm reach from the authorizer: `tier` `service`, no firm claim.

## UNEXERCISED

The door's admission. The resident is unbound, so nothing presents the token. No seat has called the door with it. It stays
unexercised until attach cell 4.

## Rollback

One change closes the door: the list back to empty. Then the grant removed and the secret scheduled for deletion. There is
no revocation of the token before its expiry.

## What cell 4 (the binding) still waits on

- The one test message on the commentary-ready queue (row IRPT_ANLREQ-D2-S26) accounted for at the binding's own pre-read:
  bound as things are, the resident would refuse it `TICKET_ID_ABSENT`, keep it, and dead-letter it on its third receive.
- The CTO's word. Release 6 (the drafter's READY gate) is live, per `2.0.0_SA_COO~Y2` msg 5412.
