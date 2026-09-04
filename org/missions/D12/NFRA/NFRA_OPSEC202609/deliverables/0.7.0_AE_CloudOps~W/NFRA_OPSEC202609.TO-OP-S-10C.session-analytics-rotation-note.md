# session-analytics and the signing-key rotation -- what TO-OP-S-10 must carry

**Seat:** `0.7.0_AE_CloudOps~W` - **Face:** `NFRA_OPSEC202609.TO-OP-S-10C` (S10C-AC4)
**Written:** 2026-09-04 ~05:0xZ - **Consumer:** `TO-OP-S-10`, whose rotation runbook does not exist yet

---

## WHY THIS IS A NOTE AND NOT A RUNBOOK AMENDMENT

`S10C-AC4` requires "an explicit statement that redeploy-per-rotation is required, **with the rotation
runbook amended to say so**". **There is no rotation runbook to amend.** `TO-OP-S-10` reads `staged`,
and the dual-key overlap runbook is that face's own deliverable (PRD S10). The project's deliverables
carry a `TO-OP-S-3` ORIGIN-secret rotation runbook and a blocked-addresses runbook; neither governs the
signing key.

So this note is the carrier, and it is delivered to `TO-OP-S-10`'s lane in writing with a message id
rather than left to be discovered. **Writing it into a runbook that does not exist would satisfy the
criterion's words and none of its purpose.**

---

## THE ANSWER: REDEPLOY-PER-ROTATION IS REQUIRED TODAY

`opal-session-analytics` verifies portal JWTs (`src/auth.ts`, `verifyAuth`) using
`opal/auth/jwt-public-key`, fetched through this:

```js
async function getJwtPublicKey() {
    if (cachedPublicKey) return cachedPublicKey;          // auth.js:24-25
    const response = await secretsClient.send(new GetSecretValueCommand({
        SecretId: 'opal/auth/jwt-public-key' }));          // auth.js:26
    cachedPublicKey = response.SecretString || '';
    ...
}
```

Module-level variable, **no TTL, no invalidation, one slot**. A container fetches the key once at cold
start and holds it for its entire life. So on rotation a warm container keeps verifying against the
OLD public key and **rejects every token signed with the new private key**, for as long as it lives.

---

## BUT "IT BREAKS PERMANENTLY" IS AN OVERSTATEMENT, AND THE CORRECTION MATTERS

`TO-OP-S-10C` states the function "breaks PERMANENTLY, with no mechanism left to repair it", and row
`Z-S123` that it "cannot expire itself into a retry". **The cache is bounded by CONTAINER LIFETIME, not
unbounded.** Containers recycle, and each new one fetches the current key.

Measured on this function, from CloudWatch log streams (one stream per execution environment),
creation to last event:

```
  median        5.6 minutes
  p90          52.3
  p99         138.0
  MAX observed 143.0  (2.4 hours)
```

**BOUND ON THAT MEASUREMENT, STATED BECAUSE IT CHANGES HOW IT SHOULD BE USED:** 107 streams with a
measurable span out of 200 sampled, and `NextToken` was present -- so this is a **FLOOR, not a census**,
and the sample is ordered by last-event time so it is biased toward recently-active containers. **The
observed maximum is not the possible maximum.** `jwtPublicKeys.mjs:17-23` states the structural half in
its own words: a stale container "rejects every request it serves until it happens to be recycled --
and **Lambda does not bound execution-environment lifetime**."

So the honest shape of a rotation without a redeploy is **not permanent breakage** and **not a clean
cutover**. It is:

> **A PARTIAL, SILENT, SELF-CLEARING OUTAGE OF UNBOUNDED TAIL DURATION.** A shrinking fraction of
> requests fail as containers recycle. Most clear within minutes. The tail is measured to 2.4 hours
> here and is not bounded in principle. Nothing reports which containers hold which key, so nobody can
> tell when it is over except by waiting and watching failures stop.

That is worse than permanent breakage in one specific respect worth naming: **permanent breakage is
noticed.** A partial outage that clears on its own gets absorbed as "some 401s during the rotation",
attributed to the rotation generally, and never traced to this consumer.

---

## THE REFRESH PATH EXISTS ALREADY, AND THIS FUNCTION IS THE ONE THAT CAN USE IT MOST EASILY

`infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs` (`TO-OP-S-10B`, `0.7.0_AE_CloudOps~V`) is exactly the
remedy: two-slot current/previous, `JWT_KEY_TTL_MS = 300000` (300s), and it accepts **both** a bare PEM
(the secret's shape today) and a `{current, previous}` envelope (its shape after rotation) -- so it is
deployable BEFORE the rotation rather than as part of it.

NOTE: **AND THE PACKAGING NOTE IN THAT MODULE POINTS DIRECTLY AT THIS FUNCTION.** It records that the
build-time mirror of `infra/aws/lambda/lib/` into `<source_dir>/src/lib/`
(`build-nodejs-lambda.sh:137-158`) is **gated on the consumer having a `src/` directory**, and that
"neither `portal-authorizer` nor `auth-validator-edge` has one". **`session-analytics` HAS a `src/`.**
It is the one consumer of the three for which the canonical lib mirror applies directly.

**So the refresh path is not hypothetical and does not need designing. It needs deploying.**

---

## WHY IT IS NOT DEPLOYED HERE, WHICH IS A SCOPE FACT AND NOT A DIFFICULTY

Adopting the shared module is a CODE change, and code deployment for this function is **act two** of
the adoption (`portal-auth/session-analytics.tf`). Act one -- landed at `ea544ac7e2` -- brought the
function under Terraform inertly with the code attributes ignored. Act two removes that `ignore_changes`
as its first step, builds via `build-nodejs-lambda.sh`, and swaps to an S3 artifact; it also forces the
handler from `index.handler` to `dist/index.handler`.

`TO-OP-S-10C` is scoped to establishing the deploy path, not to shipping a code change through it.

---

## WHAT TO-OP-S-10 SHOULD CARRY INTO ITS RUNBOOK

1. **TODAY, WITHOUT A CODE CHANGE: `opal-session-analytics` MUST BE REDEPLOYED AS PART OF EVERY
   ROTATION.** A redeploy replaces every execution environment at once, converting an unbounded silent
   tail into one controlled event. That is the whole reason to prefer it over waiting.
2. **DO NOT "WAIT FOR CONVERGENCE" ON THIS CONSUMER.** There is no convergence window to wait for --
   only a distribution with an unbounded tail and no observable completion. Any runbook step of the
   form "wait N minutes for all consumers to pick up the new key" is unsatisfiable here at any N, which
   is the same finding `Z-S100` made about `opal-portal-authorizer` before `TO-OP-S-10B` gave it a TTL.
3. **THE BETTER FIX IS SMALL AND ALREADY BUILT:** switch this function to `jwtPublicKeys.mjs`. Then it
   converges within `JWT_KEY_TTL_MS` (300s) like the other two, the redeploy step drops out of the
   runbook, and all three consumers share one convergence window -- which that module's own comment
   names as the point ("a rotation runbook that must reason about three different convergence windows
   is a runbook nobody executes correctly").
4. **ORDERING, IF THE REDEPLOY ROUTE IS TAKEN:** rotate the secret, then redeploy this function. A
   redeploy BEFORE the secret changes just re-caches the old key and buys nothing.

---

## ONE THING THIS NOTE DOES NOT ESTABLISH

Whether any OTHER consumer of `opal/auth/jwt-public-key` has the same unbounded-cache shape. `Z-S100`
covered `opal-portal-authorizer` and `auth-validator-edge`; `Z-S105` bounded the reachable set at 25
live functions via two shared roles and explicitly called that an upper bound rather than a count.
**This note speaks only for `opal-session-analytics`.** A consumer census is `TO-OP-S-10`'s to close,
and a CloudTrail `GetSecretValue` census will systematically UNDER-count exactly the consumers that
matter most -- the no-TTL ones -- for the reason recorded in `Z-S134`: an unbounded cache fetches once
per container lifetime, so the more dangerous the consumer, the quieter it looks.
