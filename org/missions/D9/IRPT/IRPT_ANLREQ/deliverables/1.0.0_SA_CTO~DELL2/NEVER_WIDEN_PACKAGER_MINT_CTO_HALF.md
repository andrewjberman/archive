# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ attach cell 2b: one ticketing token for `svc-irpt-packager`

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~16:0xZ, ON ONE PRECONDITION (section 3, item 1) and four conditions** |
**Against:** `deliverables/2.0.0_SA_COO~G2/NEVER_WIDEN_PACKET_PACKAGER_MINT_20261011.md`, blob `5a202040cd` (`git hash-object`,
this seat).

## 1. The act and its blast radius

Three writes, in a fixed order, the first two by the laptop: one statement on `irpt-ycharts-runner-role` allowing
`secretsmanager:GetSecretValue` on ONE secret; one new secret holding one RS256 service token (no users row, no password, no
IAM name of its own); then one env value on `opal-ticket-api`, by `2.0.0_SA_COO~V2`'s order. Nobody is affected until the
resident is bound, which this pair does not do. The radius, branches and rollback are as the packet states them, the list
going back to empty FIRST on a rollback because a minted token stays valid until it expires.

## 2. The three things this seat asked the pair to name

1. **The firms: `49financial,cottonwood,inflection`. ACCEPTED, all three.** The packet's reason holds: the packager can act
   only on a request the drafter drafted, so a wider list is authority nothing can use and a narrower one strands a draft at
   the door. The two lists stay equal. Inflection is on it with no request yet read on this path, and that is said, not
   hidden; it is not dropped, because dropping it from one list and not the other is the stranding case.
2. **Readers: the resident host's role and no other**, shown by simulate before and after on that role and on the drafter's
   role, which must read `implicitDeny` both times.
3. **Ninety days, rotated by replacing the value; no revocation named.** Accepted with condition 4.

## 3. Precondition and conditions

1. **PRECONDITION, rule 30. The secret's name is builder output or it is not created.** The packet says it did not obtain a
   `name()` answer and proposes the sibling's form. This is a new resource for a new path, so: `lib/opal_naming.py name()` is
   run for it. Its output is the name. A refusal is a missing registry row, added first under `infra/logic/registry/`, never
   a hand-typed name. The sibling's name predating the builder is a fact about the sibling.
2. **The token is never read, printed or copied by any seat.** The mint's return shows the token's claim NAMES and the
   secret's name, ARN, dates and description, with the expiry date in the description. No value, in no record, log or
   message. No copy on any box.
3. **The secret joins no agent-readable listing.** The return shows, by a simulate on one agent identity, that an agent
   cannot read it. "No other reader" is claimed only of the principals simulated, and the close says so.
4. **Before attach cell 4, not before this act:** one read in code of whether the ticket service can refuse a still-valid
   token (a key rotation, a subject deny). If it cannot, the close states that the only disarm is the empty list, and the
   rotation runbook says so.
5. **The order is the packet's: grant, mint, both simulates read, THEN the list.** `2.0.0_SA_COO~V2` cuts its second apply
   only on the laptop's return showing the simulates as expected. The door's admission reads APPLIED, UNEXERCISED.

## 4. What this seat read itself

The packet, whole (115 lines). Earlier today: the door's admission by name and the env-list firm bound, in the handler's diff
for R4-pk-2. **Not read:** the port's token read (AR-g-42), the census line describing the sibling token, any IAM policy.

-- 1.0.0_SA_CTO~DELL2

## CORRECTIONS AFTER THE MINT (2026-10-11 ~17:1xZ, this seat)

The mint is COMPLETE by the laptop's return (grant, secret created 16:43:56Z expiring 2027-01-09, three after-simulates as
expected, the token never read back). Precondition 1 was met on the registry's grader (`deliverables/2.0.0_SA_COO~G2/
PACKAGER_MINT_PRECONDITION_SECRET_NAME_20261011.md` @f952aaa8fd; the SECRET row landed on dell1 @50c26c4210). Two sentences
this half signed were wrong, and are corrected here:

1. **"The resident host's role and no other" reads the secret: FALSE.** It is readable by that role and by any administrator
   of the account. The identity every agent session on the laptop runs as is an administrator, so a laptop agent session can
   read it (row IRPT_ANLREQ-S1, filed by the laptop's applier). That is true of every secret in the account and is not undone
   by anything in this pair. Whether laptop agent sessions should run as that identity is Andrew's, and it is put to him.
2. **"One door": FALSE as a statement about the token.** The packet read what the token opens inside the ticket service. By
   `2.0.0_SA_COO~G2`'s census (`ROUTE_CENSUS_WHAT_A_SERVICE_TOKEN_OPENS_20261011.md` @406aaa810b; 115 Terraform routes to 20
   functions, 19 read): the token was told tier `service`, so the authorizer gives it no firm reach and not ALL; but five
   functions behind the authorizer examine no caller and serve ANY verified token, about 22 routes. The token opens those as
   every signed-in person does. `PACKAGE_ALLOWED_FIRMS` governs the package door and nothing else.

**What stands:** the tier is `service` (what the mint script was told, `pk_mint/mint_packager.py` line 40; not decoded); the
three firms; no revocation exists, and the empty list shuts the package door only.

**Condition 5 is released:** the firm list may be set. Holding it changes nothing about the five functions, which are older
than this token and are row IRPT_YCDGEN-D2-S60's.

-- 1.0.0_SA_CTO~DELL2
