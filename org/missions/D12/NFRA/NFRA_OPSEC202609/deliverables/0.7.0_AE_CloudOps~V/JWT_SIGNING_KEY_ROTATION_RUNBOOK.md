# RUNBOOK -- rotating the portal JWT signing key with NO sign-out

**Owner:** AE cloud-ops lane - **First executed:** 2026-09-10 (`NFRA_OPSEC202609.TO-OP-S-10`,
`0.7.0_AE_CloudOps~V`) - **Ledger:** `org/critical_paths/change_management/20260910T0012Z_opsec-s10-signing-key-rotation_deploy_completion.md`

The estate rotates ONE keypair here: `opal/auth/jwt-private-key` signs, `opal/auth/jwt-public-key`
verifies. The whole difficulty is that **verification is distributed and signing is not**. Widen what
is accepted first, confirm every acceptor, then move the single thing that signs.

> ⛔ **DO NOT configure Secrets Manager automatic rotation.** A rotation firing unattended on a live
> login path is a larger change than this outcome asks for. `RotationEnabled` stays unset; if you
> think otherwise, that is a row and a recommendation, not an act.
> ⛔ **Never schedule deletion of an old secret version inside the rotation.** The old material is
> the rollback.

---

## THE CONSUMER SET IS FOUR, NOT TWO

TO-OP-S-10 was cut naming **two** consumers. That number was wrong and finding it was most of the
work. **Enumerate before you write anything** -- do not inherit this list, re-measure it:

| # | consumer | role | how it reads |
|---|---|---|---|
| 1 | `auth-validator-edge` | verifier (Lambda@Edge, replicated) | two-slot + TTL |
| 2 | `opal-portal-authorizer` | verifier | two-slot + TTL |
| 3 | `opal-session-analytics` | verifier | two-slot + TTL |
| 4 | `opalinvest-auth-handler` | **signer AND verifier** | private: single CURRENT + TTL; public: two-slot |

Rows `Z-S157` (consumer 3 was missed entirely and was live at 52,540 inv/7d) and `Z-S160` (consumer 4
is *also* a verifier) are why. **A COMPONENT'S NAME IS NOT ITS ROLE SET** -- ask, per *read*, what the
value is used FOR. `opalinvest-auth-handler` reads two secrets and plays two roles, and a rule written
for one of them was applied to both.

The same trap sits on the authorizer census: **two of three live HTTP-API authorizers carry `jwt` in
their NAME while being `REQUEST` type** (Lambda authorizers). Read the TYPE field, never the name.

**Non-Lambda verifiers -- re-measure, do not assume:** at the 2026-09-10 vintage there were none.
5 HTTP APIs / 3 authorizers all `REQUEST`, native JWT = 0; 1 REST API / 1 `REQUEST` authorizer,
`COGNITO_USER_POOLS` = 0; **0 Cognito user pools in us-east-1**; 1 ALB `authenticate-oidc` action
pointing at a Microsoft tenant (a different token family); `trade-authorizer` on an HS256 env secret
(also a different family).

---

## THE STEPS, WITH THE WAIT AT EACH

**TTL is 300 s** (`JWT_KEY_TTL_MS`, shared module `lib/authkeys/jwtPublicKeys.mjs`). Every "wait" below
is one TTL plus margin. The origin-verify cache is deliberately the same 300 s so one number governs;
that is also why the number alone can never tell the two windows apart.

### 0. Before anything
- Open the deploy ledger with **the rollback named in the entry itself**.
- **Drain the broker inbox** -- the signing switch is the irreversible step on a live login path.
- Confirm both secrets: one version each, `RotationEnabled` unset, no `DeletedDate`.

### 1. Mint the keypair and build the discriminating fixtures
RSA-2048, matching what it replaces (confirm the outgoing pair actually IS a matched pair first).

**Mint the probe tokens BEFORE any write** -- old-key, and a control key that will be in *neither*
slot. Then **establish the baseline on the live endpoint**: what does an old-key token return *now*,
and what does a neither-slot token return? On `POST /auth/refresh` these were `{"error":"User not
found"}` (crypto ACCEPTED, failing later at the user lookup) versus `{"error":"Internal server
error"}` (crypto REJECTED). **Without that baseline the after-test is vacuous** -- "the old token
still verifies" means nothing unless you know it verified before.

### 2. Publish the verification envelope -- WIDENS ONLY
Write `opal/auth/jwt-public-key` as `{"current": NEW_PUB, "previous": OLD_PUB}`.

This is safe in isolation and deliberately first: a converged consumer accepts both keys, an
unconverged one still holds the old bare PEM and accepts the old key -- which is still the only key
anything signs with. **There is no instant at which a live token is unacceptable to any reader.**

**Verify by reading the secret BACK from AWS** and fingerprinting both halves against your local PEMs
**on SPKI DER** (see traps). Confirm the prior version sits at `AWSPREVIOUS`.

### 3. WAIT ONE TTL, then confirm every consumer is SERVING it
> **"Deployed" is not "serving", and CloudTrail is not an instrument here** -- its delivery latency
> means 0 `GetSecretValue` events proves nothing.

The discriminator is a token signed by the NEW key, which exists only in `current`. An unconverged
consumer refuses it. **Read each consumer separately, with its own timestamp** -- four observations,
never one generalised:

| consumer | probe | ACCEPTED looks like |
|---|---|---|
| 1 + 2 | `GET /v1/market/rsi` with bearer | `200` (traverses edge THEN origin authorizer, so 200 needs both) |
| 3 | direct `lambda invoke`, `/sessions` | `400 user or date parameter required` -- i.e. *past* `requireAdmin` |
| 4 | `POST /auth/refresh`, cookie | `User not found` (crypto accepted) vs `Internal server error` (rejected) |

**Run all four arms on every consumer:** `NEW`, `OLD`, `CTL` (neither slot), `EXP` (correct key,
deliberately expired). Also confirm **no consumer was redeployed during the window** -- every
`LastModified` must predate the envelope write, measured not assumed. A redeploy mid-window masks
whether convergence works at all.

### 4. Switch signing
Write `opal/auth/jwt-private-key` = `NEW_PRIV`, **a bare PEM, single CURRENT**. Two slots would be a
defect here: a signer must know which key is current, or it may sign under a retired one.

**Pre-write gate:** confirm `NEW_PRIV`'s public half equals the *served* `current` slot **on SPKI
DER**. If they differ, the switch mints tokens no consumer can verify -- a total outage.

**Then read the secret back and parse it.** See trap 1; this is not optional.

### 5. WAIT ONE TTL, then OBSERVE THE SIGNER -- never infer it from the verifiers
`POST /auth/refresh` returns an `accessToken` minted by `generateAccessToken -> getJwtPrivateKey`, so
it is signer output by construction. **Verify that token's signature locally** against the old and new
public halves. No verifier enters the reading.

Ride the OLD-SHAPE refresh path (`{sub: <email>, type: "refresh"}`, accepted for one 7-day window per
OP-s-11 / F-10): it needs only an active address -- no password, no MFA leg -- and writes nothing.

Expect the flip: `signed by OLD key` before, `signed by NEW key` after, with the CTL arm refused at
both ends. **Take the BEFORE reading or the AFTER reading means nothing.**

### 6. The outcome bar
Present **the literal pre-act token from step 1**, unchanged, and confirm it still verifies. Its 7-day
refresh lifetime is why it survives as evidence where a 15-minute access token cannot. Then confirm a
neither-slot token is still REFUSED, and that both secrets still show no `DeletedDate` with
`RotationEnabled` unset. Close the ledger.

### 7. Retiring the old slot -- NOT part of this rotation
The old key stays in `previous` for at least one `REFRESH_TOKEN_EXPIRY` (**7 days**), because a refresh
token minted before the switch stays valid that long. Retiring it earlier signs those users out, which
is the exact failure this procedure exists to prevent. **That retirement is a separate cut.**

---

## TRAPS -- each of these cost real time or real production impact

### 1. `.tools/aws.cmd` SILENTLY TRUNCATES a multi-line argv value, and the API says OK
Row `Z-S161`. Passing a PEM as one argv element to the shim stored **27 bytes** -- the
`-----BEGIN PRIVATE KEY-----` line alone -- while `put-secret-value` returned `rc=0` with a `VersionId`
and `['AWSCURRENT']`. **The signing key was invalid in production for 3m52s.**

The shim is a Windows **CMD batch** file; CMD re-parses argv and cannot carry an embedded newline.
`shell=False` protects against *the shell* -- the shim is not the shell, it is a CMD process
downstream of it. **The precaution aimed at the wrong layer is worse than none, because it retires the
worry.**

> **Use `boto3` in-process for any multi-line secret material.** No CMD layer exists to re-parse it.
> **And read the object back and parse it** -- a write receipt certifies that a version was CREATED,
> never what it CONTAINS.

### 2. Repairing the key POISONS the documented rollback
Re-writing the correct key moved `AWSPREVIOUS` onto the truncated version, so the standard
stage-move rollback would have **restored a broken key**. Nothing announces this. After any corrective
re-write, **read `AWSPREVIOUS` back and check it parses**; re-point it with
`update-secret-version-stage` if not (move the label, delete nothing).

### 3. An EXPIRED fixture is byte-identical to a WRONG-KEY one
A stale probe token read as `NEW accepted / OLD REJECTED` -- the exact signature of a single-slot
verifier -- and would have halted a correct rotation on a defect that did not exist. Both return
`401 {"error":"Unauthorized","details":"Invalid token"}`.

> **Carry an `EXP` arm on purpose** -- the correct key, deliberately expired -- in the before *and*
> after tests. `EXP` matching `CTL` is what makes `NEW` and `OLD` mean anything.
> **An experiment whose fixture has a TTL shorter than the experiment is measuring its own clock.**

### 4. Compare keys on DER, never on PEM text
PEM **text** hashes read as three key mismatches when they were three *encodings of one key* (line
endings, header variants, trailing newline). Had that been believed, a correct act would have been
aborted. `openssl pkey -pubin -outform DER | sha256` is the canonical comparison.

### 5. Terraform artifact patterns differ inside one root
`session-analytics.tf` hardcodes `source_code_hash` (an S3 upload alone plans **No changes** -- the
hash line *is* the deploy); `auth_handler` and `portal_authorizer` resolve it through a
`data aws_s3_object` lookup (the upload alone moves the plan). Read the plan; never infer from the
resource shape.

### 6. Lambda@Edge `qualified_arn` lifecycle pin
Publishing a version without dropping the pin leaves CloudFront serving the old one.

---

## ROLLBACK

`update-secret-version-stage` moving `AWSCURRENT` back to the prior version id -- **verify first that
`AWSPREVIOUS` parses as a key** (trap 2). Because the public envelope only ever *widens* what is
accepted, rolling back **signing** alone is sufficient and safe: every consumer still accepts both
keys. The old material is retained by AWS as a version, so rollback is a stage move, not a restore.

At the 2026-09-10 rotation the rollback was `1acd44f3-d07e-486b-9ad8-66993a0b6716` (private) and
`fabe94f0-019d-455d-8c72-47b3d709bd8b` (public).
