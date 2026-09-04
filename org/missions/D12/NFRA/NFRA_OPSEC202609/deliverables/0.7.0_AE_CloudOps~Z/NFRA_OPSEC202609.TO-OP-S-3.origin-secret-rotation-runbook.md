# ORIGIN-SECRET ROTATION RUNBOOK

**TO:** `NFRA_OPSEC202609.TO-OP-S-3` (deliverable 4) - **Cell:** `OP-s-3` - **Seat:** `0.7.0_AE_CloudOps~Z`
**Secret:** `opal/auth/origin-verify` (`arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/auth/origin-verify-Pe97BM`)
**Header:** `X-Opal-Origin-Verify` on the CloudFront origins `APIGateway-portal` (`7k3ed8px20`) and `APIGateway-portfolio` (`f61h681z9g`), distribution `EVTSA9VEHNZVH`
**Written:** 2026-09-03

---

## THE TWO-SLOT MECHANISM

The secret is a JSON document with exactly two slots:

```json
{ "current": "<the value CloudFront is sending>", "previous": "<the value it was sending before>" }
```

The **distribution sends `current` only.** `previous` exists solely so the CONSUMERS can keep
accepting the outgoing value while a change propagates. The overlap is therefore a property of the
consumers, never of what the edge sends.

## WHY A ROTATION CANNOT 401/403 THE PORTAL

Both consumers accept **`current` OR `previous`**, on these lines:

| consumer | the OR |
|---|---|
| `opalinvest-auth-handler` | `infra/aws/opalinvest_dev/lambda/auth-handler/src/originVerify.ts:138` - `if (slots.previous && safeEqual(presented, slots.previous)) return true;` |
| `opal-portal-authorizer` | `infra/aws/users/lambda/portal-authorizer/index.mjs:134` - `if (slots.previous && safeEqual(presented, slots.previous)) {` |

During the window in which some edges still send the old value and others send the new one, **both
values are live and both are accepted**, so no request is refused for carrying the "wrong" one.

### The half that is easy to get wrong, and the reason step 2 exists

Both consumers cache the secret **with a TTL** (`originVerify.ts:66` `SLOTS_TTL_MS = 300_000`;
`index.mjs:33` `ORIGIN_VERIFY_TTL_MS = 300000` - **300 seconds**).

**The TTL is a correctness control, not a performance one.** With an UNBOUNDED cache the two-slot
design silently fails:

```
container started BEFORE the rotation caches {current: A, previous: ""}
  -> secret rotated to {current: B, previous: A}   that container: still fine on A
  -> the distribution starts sending B             that container: B matches NOTHING it holds
                                                   -> 403 on every request it serves
```

Lambda does not bound execution-environment lifetime, so "the container will recycle eventually" is
not a control. **Step 2 below - waiting longer than the TTL before touching the header - is what
converts the two-slot design from a hope into a guarantee.**

---

## THE ROTATION, IN ORDER

**Never reorder these. The header must never move to a value some live container has not yet seen.**

### 1. Mint the next value and promote (no traffic impact)

Read the current document, move `current` into `previous`, put a fresh high-entropy value in
`current`, and write it back. Mint the value out of band and never echo it:

```bash
# writes {current: <new>, previous: <the old current>} to a 0600 temp file, then uploads it
python - <<'PY'
import json, secrets, subprocess, tempfile, os
cur = json.loads(subprocess.check_output([
    "aws","secretsmanager","get-secret-value",
    "--secret-id","opal/auth/origin-verify",
    "--query","SecretString","--output","text"]).decode())
doc = {"current": secrets.token_urlsafe(48), "previous": cur["current"]}
fd, p = tempfile.mkstemp(suffix=".json"); os.close(fd)
open(p,"w").write(json.dumps(doc))
subprocess.check_call(["aws","secretsmanager","put-secret-value",
    "--secret-id","opal/auth/origin-verify","--secret-string","file://"+p])
os.remove(p)
print("rotated; value not printed by design")
PY
```

At this moment the distribution is still sending the OLD value, which is now `previous`. **Every
consumer still accepts it.** Traffic is unaffected.

### 2. WAIT 600 SECONDS

**`OVERLAP_WAIT_SECONDS = 600`** - twice the 300 s cache TTL.

This is the step that makes the rotation safe. After 600 s **every live execution environment has
re-read the secret** and holds `{current: NEW, previous: OLD}`, so every container accepts both
values. Do not shorten it below the TTL; if the TTL is ever changed, this number must change with it.

### 3. Move the header on the distribution

`local.origin_verify_current` in `infra/aws/terraform/portal-auth/secrets.tf` reads `current` from the
secret at plan time, so the header value follows the secret automatically:

```bash
cd infra/aws/terraform/portal-auth
terraform plan -detailed-exitcode -out=rot.tfplan     # expect exit 2, and ONLY aws_cloudfront_distribution.portal in the diff
HALT_ACK=1 ../../../../.tools/safe-apply.sh -chdir=infra/aws/terraform/portal-auth apply rot.tfplan
```

**Confirm propagation before going on** - a `Deployed` status means every edge is now sending the new
value:

```bash
aws cloudfront get-distribution --id EVTSA9VEHNZVH --query 'Distribution.Status' --output text   # wait for: Deployed
```

Between the apply and `Deployed`, edges send a MIX of old and new. That is exactly the window
`previous` exists for, and both are accepted throughout.

### 4. WAIT THE OVERLAP WINDOW, then retire `previous`

**`OVERLAP_WINDOW_SECONDS = 3600`** (1 hour) measured from the `Deployed` reading in step 3.

3600 s is not derived from a measured propagation figure - it is a deliberate over-estimate of
CloudFront propagation (typically minutes) chosen so the retirement is never the thing that races a
slow edge. **It is a floor, not a measurement, and it is safe to exceed.**

Then clear the slot (same out-of-band shape as step 1, with `previous` set to `""`). After this,
only the new value is accepted - which is the point: a leaked old value stops working.

---

## RESIDUAL, STATED RATHER THAN OMITTED

**A rotation retires the value from the LIVE header, but NOT from Terraform state history.**

A CloudFront custom origin header value is a readable attribute of the distribution, so it is written
into `s3://opal-313476888478-terraform-state/portal-auth/tfstate` by construction - no write path
avoids it. That bucket is SSE-S3 encrypted with all four public-access blocks set, **but versioning is
Enabled with no lifecycle configuration**, so every superseded state object is retained indefinitely
and each carries the origin-verify value that was current when it was written.

Accepted by the issuer 2026-09-03 (msg 19500, design call (a)) on surprise row
`NFRA_OPSEC202609-Z-S2`. **The controls that bound it are the ones in this runbook:** step 4's
retirement of `previous` is what makes a value read out of state history stop working, so rotating on
a schedule - rather than only after a suspected exposure - is what keeps that window short. A
noncurrent-version expiry on the state bucket would close it properly; that is the estate backend
bucket's lane (routed to `1.0.0_SA_CTO~Z` / `0.0.0_AB_MSTR~Z`), deliberately not part of this TO.

**What the secret does and does not buy:** it proves PATH OF ENTRY only. Every authenticated route
still requires the JWT, so a leaked origin value alone does not grant data access - it only removes
the front-door requirement for the caller that holds it.

## IF SOMETHING GOES WRONG

Symptoms are unambiguous: `403 {"error":"Forbidden"}` from `/auth/*`, or `isAuthorized:false` on every
authorized route. Both consumers log `Origin verification FAILED` (`index.ts:180`, `index.mjs:280`),
and a secret that cannot be read logs `Origin verification unavailable` - which distinguishes a
BROKEN SECRET from a WRONG HEADER without exposing either to the caller.

**Fastest recovery:** put the previous value back into `current` (step 1 in reverse) and wait one TTL
(300 s). The consumers converge on their own; no deploy is required, because nothing about the value
lives in the code.
