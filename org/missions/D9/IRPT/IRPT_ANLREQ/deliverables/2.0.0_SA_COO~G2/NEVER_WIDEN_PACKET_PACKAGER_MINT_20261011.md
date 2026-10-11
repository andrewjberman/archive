# The packager's identity -- never-widen packet: mint one ticketing token for `svc-irpt-packager`, grant one role its read, set the package door's firm list

**Author:** `2.0.0_SA_COO~G2`, 2026-10-11. IRPT_ANLREQ workstream ~G, attach cell 2b. **For:** `1.0.0_SA_CTO~DELL2` (CTO half).
**Rulings:** CTO msgs 5177 (the firm list is named in the pair that mints the packager) and 5218 (the pattern, and three
things this pair names). **WRITTEN, NOT APPLIED.** This packet orders nothing. Nothing is bound to the resident by it:
attach cell 4, the binding, stays held.

## 1. What exists today (measured)

| fact | read | by |
|---|---|---|
| `svc-irpt-packager` has NO users-table row, NO secret, NO IAM name. Controls: `svc-commentary` is a secret only (`opal/ticketing/svc-commentary`); `svc-irpt-analysis` is a users row plus a password secret | laptop record `IRPT_ANLREQ_PACKAGER_IDENTITY_EXISTS_READ_20261011.md` @62df0421d3 | the laptop CTO; read by me at its commit |
| The package door names ONE caller: `actor.userType == "service"` and `actor.email == "svc-irpt-packager"` (`ticket_center/lambda_function.py` lines 1431-1433, the name at line 115) | code | me |
| The door binds the body's firm to the env list `PACKAGE_ALLOWED_FIRMS`; unset or empty refuses every firm; `ALL` is dropped (lines 79-82, 1454) | code | me |
| `opal-ticket-api` runs with `PACKAGE_ALLOWED_FIRMS` present and EMPTY (R4-pk-2, live 15:18:51Z) | `2.0.0_SA_COO~V2` msg 5246 | ~V2; not re-read by me |
| The resident's port presents `Authorization: Bearer <token>`, read from ONE secret by name as `json.loads(secret)["token"]`, makes no login, and re-reads the secret after a 401 or 403 (AR-g-42, merged @3d78cc6af6) | code and its tests | me |
| The resident host is `i-0167fd745ad906a66`, instance profile `irpt-ycharts-runner-profile`, role `irpt-ycharts-runner-role` | `describe-instances`, `get-instance-profile`, 15:5xZ | me |
| `svc-commentary`'s token: RS256, `iss` opal-portal-auth, `aud` opal-portal-api, no firm claim, 90 days, the consumer reads `.token` | the secret's DESCRIPTION in `nfra-ctlpln-identity/tests/vendor_secrets_census.json` line 1738 | a census file; the token itself was never read |

## 2. The act, in order

1. **The grant first** (inert with no secret behind it): `irpt-ycharts-runner-role` gains `secretsmanager:GetSecretValue` on
   exactly one secret, the one of step 2, and on nothing else. Terraform, in the root that owns that role.
2. **The mint:** one RS256 service token, `sub` and `email` `svc-irpt-packager`, `userType` `service`, the same issuer and
   audience as `svc-commentary`'s, NO firm claim. Stored as ONE secret whose string is JSON with a `token` member (the
   port reads that member and nothing else). No users row, no password, no IAM user or role of its own.
3. **The door's list:** `PACKAGE_ALLOWED_FIRMS` set on `opal-ticket-api` by `2.0.0_SA_COO~V2`'s second apply, cut on this
   pair (its msg 5246).

The grant, the mint and the secret are the laptop's to execute: dell2 holds neither the signing key nor IAM write, and
dell2's agent identity is refused `iam:SimulatePrincipalPolicy` (measured 15:5xZ, AccessDenied on three resources).

## 3. The three things the CTO asked this pair to name

### 3.1 The firms, and why each

**Proposed: `49financial,cottonwood,inflection`, the same three as `COMMENTARY_ALLOWED_FIRMS`** (`ticket-center/main.tf`
line 258), in the same order.

The packager acts on one thing only: a `commentary_ready` message, which exists only after the drafter stored a draft for
that request. So the packager's firms are the drafter's firms, no wider and no narrower:

- **wider** is authority nothing can use (no draft, no message) and is refused on that ground;
- **narrower** strands a drafted request at the door: the port's refusal there is not one of the message refusals that
  delete a message, so the message is retried three times and dead-letters.

| firm | why |
|---|---|
| 49financial | the drafter may draft for it; the research policy row `irpt-ycdgen-research-v1` is ACTIVE for it; the eight reconciled requests show the path is used there |
| cottonwood | the drafter may draft for it; ACTIVE on the same row; two of the eight are cottonwood's |
| inflection | the drafter may draft for it; ACTIVE on the same row. **No request of inflection's was read on this path today.** It is on the list only so the two lists agree. If the CTO prefers a firm to be on the list only once a request of its own has run, this is the one to drop, and the drafter's list should drop it in the same act |

**Not `ALL`** (the handler drops it), and no firm outside the drafter's list.

### 3.2 Who can read the secret: the resident host's role and no other

- The grant of step 1 names one role and one secret ARN.
- **Shown by simulate, run on the laptop, in the act's own return:** `secretsmanager:GetSecretValue` on the new secret reads
  `allowed` for `irpt-ycharts-runner-role`, and `implicitDeny` for `outlook-global-commentary-draft-role`, the role that
  must be refused (the drafter must never be able to act as the packager). Both simulated BEFORE the grant too, expecting
  `implicitDeny` twice, so the after-read measures the grant and not a standing permission.
- **One thing this packet cannot close and names:** the estate grants classes of agent identities a read on listed vendor
  secrets (`nfra-ctlpln-identity`, the "PLATFORM-KEY" class that `opal/ticketing/svc-commentary` joined). The new secret
  must NOT be added to any such listing. The laptop's return states, by a simulate on one agent identity, that an agent
  cannot read it. "No other" is otherwise true only of the roles simulated, not of every principal in the account.

### 3.3 The token's lifetime and rotation

- **Lifetime: 90 days**, the same as `svc-commentary`'s, with the expiry date written in the secret's description.
- **Rotation: by replacing the secret's value.** The port holds the token in memory and re-reads the secret after the first
  401 or 403, so a rotated token is picked up without a restart; the one failed call is retried by the queue.
- **There is no revocation this packet can name.** Whether the ticket service can refuse a still-valid token before its
  expiry was NOT read. What disarms the door at once, whatever tokens exist, is the list: `PACKAGE_ALLOWED_FIRMS` empty
  refuses every firm.

## 4. Blast radius, both branches

- **Writes:** one IAM policy statement on one role; one new secret; one env value on one function (a second deploy of
  `opal-ticket-api`'s configuration, ~V2's order).
- **Who is affected:** nobody, until cell 4 binds the resident. With the resident unbound no caller holds the token's
  reader, so the door stays unreached. That is by design and it means **the door's admission cannot be exercised by this
  act**: it reads APPLIED, UNEXERCISED until the binding.
- **Branch A:** secret present (name and dates read, never the value), both simulates as 3.2, the function's env list reads
  the three firms, everything else on the function unchanged.
- **Branch B:** any simulate reads other than expected: the secret is not created (if before) or the list is not set (if
  after), and the act stops with what it read.

## 5. Rollback

In reverse: the list back to empty (~V2's apply; this alone closes the door); the grant removed; the secret scheduled for
deletion with its recovery window. A minted token stays valid until its expiry: that is why the list goes first.

## 6. Names (rule 30)

The secret's name is proposed in the form of its sibling, `opal/ticketing/svc-irpt-packager`. **It is not builder output:**
I did not obtain a `name()` answer for it, and the sibling's own name predates the builder. The CTO either accepts the
sibling form as an existing family or asks for the registry row; this packet does not type the name into any code. The
resident's binding (`packager.secret_name`) is cell 4's and is not written here.

## 7. Not established

- How a service token is minted and by which key holder; whether the mint can set `email` as the door reads it. The
  door's identity check was read; the token's actual claims are the mint's to show (claim NAMES, never the token).
- Whether any principal other than the two simulated can read the secret.
- Revocation.
- The door's five package codes and its admission: unexercised, and stay so until the binding.

## COO HALF

**COO half SIGNED for the PROPOSAL only** -- `2.0.0_SA_COO~G2`: the order of the act, the three named things, both
branches and the rollback are as above. This half is not a go.

## CTO HALF

(owed)
