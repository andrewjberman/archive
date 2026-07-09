# SCTY_PREMCP F1 (/otp) — LIVE verification record + three stale-record corrections

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-09T18:55Z · **Archetype:** VALIDATE
**Trigger:** Andrew NFRA-first drive brief + COO 183905Z DRIVE, both of which read
*"SCTY_PREMCP: /otp auth-model arch-GO RULED — 0.7.0 un-blocked to build /otp/fetch. Ungated and unstaffed. Build it."*

**Verdict: /otp/fetch was ALREADY BUILT, DEPLOYED, and is LIVE-HEALTHY.** Nothing to build.
This record supplies the evidence, closes PREMCP §4's one explicitly-deferred verify
(*"confirm the OAuth guard on /mcp+/teams does not fall through to it — it won't, but verify"*),
and corrects three stale records that each would have caused wrong work.

---

## 1. Delivery state — grounded, applied + exercised (Rule 22a)

| Layer | Claim | Grounding | Verdict |
|---|---|---|---|
| Code | `/otp/fetch` + `/otp/health` + `app/otp.py` | `server.py:431,573-574`; commit `c654461f9` | PRESENT |
| Code (cross-firm guard) | per-request `window_seconds` | commit `0ccee9134` — merge-base confirms it IS an ancestor of HEAD | MERGED |
| **Deployed code** | running box == repo HEAD | SSM `sha256sum /opt/m365-mcp-gateway/app/otp.py` = `e3ce8bac…c87a01` **==** local HEAD sha256 | **MATCH** |
| ALB | `/otp/fetch`,`/otp/health` forward, no OIDC | live `describe-rules` prio=30, actions=`['forward']` | APPLIED |
| Secrets | both firm bearers exist | live: `blackdiamond/49f/otp-gateway-token`, `blackdiamond/cot/otp-gateway-token` | APPLIED |
| Gateway env | 2 bearers injected, mailbox set | SSM: `OTP_BEARER` word-count = **2**; `OTP_MAILBOX_set=1` | APPLIED |
| IAM + liveness | 6h probe → SNS | `m365-otp-liveness` State=Active; rule `m365-otp-liveness-6h` `rate(6 hours)` ENABLED | APPLIED |
| **Behavior** | the path actually works | **EXERCISED:** `lambda invoke m365-otp-liveness` → `{"ok": true, "detail": "status=200"}` | **GREEN** |

`OTP_WINDOW_SECONDS` is *unset* in the gateway `.env` — correct and by design: `otp.py:105`
defaults it to `0` (disabled), and the window is passed **per-request** by each firm-box
(cot ~120s), never as a shared env. Back-compat for the 49F path is preserved as designed.

> **Stale-record correction A.** Commit `0ccee9134`'s message says *"Staged, NOT yet deployed."*
> That note is now false — the sha256 of the deployed file equals HEAD. The message was
> accurate when written; nothing re-stamped it after the deploy landed.

---

## 2. PREMCP §4 hardening requirement — bearer-isolation, now EXERCISED (was INFERRED)

PREMCP §4 asserts the `/otp` static bearer is accepted **only** by `/otp/fetch`, and explicitly
flags the assertion as unproven: *"it won't, it's not a valid RS256 JWT, but **verify**."*
Under Rule 22a an unexercised security assertion is `INFERRED` and non-actionable. Exercised now.

**Method — zero credential handling.** The real capability bearer was never read. A random 32-byte
opaque token of the same shape was used as a negative control.

> ### CORRECTION (CVO 190631Z) — my original reasoning here was WRONG. Do not reuse it.
>
> I originally wrote: *"if the guard rejects **any** opaque bearer, it rejects the real one —
> strictly stronger than testing with the live secret."* **That inference does not hold, and CVO
> refuted it.** A random token and the real bearer differ in exactly the one property a guard could
> key on: **membership in a static allowlist.** Had `/mcp` contained a branch like
> `if hmac.compare_digest(token, cfg.OTP_BEARER): accept`, my random token would still 401 while the
> real bearer returned 200. The probe **cannot distinguish** *"no static-bearer path exists on /mcp"*
> from *"a static-bearer path exists that a random token can never trigger."* On the precise failure
> mode the PRD flagged — accidental static-bearer acceptance on `/mcp` — the random-token control has
> **zero power**. It is strictly *weaker*, not stronger.
>
> The tell was in the PRD text I was verifying: *"it's not a valid RS256 JWT, so it could never pass."*
> That is a **mechanism claim about the guard's logic**, and Rule 22 says a mechanism claim closes at
> **SOURCE**, never by a behavioral probe against a different input. I ran a behavioral probe at a
> mechanism claim and then called it dominant. That is the error.

**What actually closes it — SOURCE, independently re-derived (not taken from CVO's word):**

- `server.py:91-106` `_bearer_email()` — `Bearer ` prefix → `oauth_as.validate_access_token()` (RS256
  sig / iss / aud / exp) → non-empty `sub` → required scope. **No static branch, no allowlist, no
  `compare_digest` anywhere on this path.**
- `otp.check_bearer` has exactly **two** call sites — `server.py:446` and `:486`, both `/otp/*` routes.
  `ms_ingest.check_bearer` has exactly **one** — `:507`, on `/ms/*`. Neither is reachable from `/mcp`.
  *(CVO cited `:439`/`:479`/`:500`; the 7-line offset is my own comment edit in `bfbf89ba7`, not drift.)*
- The only other `compare_digest` in the app is `oauth_as.py:224` — the **PKCE** challenge check, not a
  bearer path.

That **call-site enumeration** is what makes *"the OTP bearer is accepted ONLY by /otp/*"* SOURCE-CONFIRMED.

**Both artifacts are required, and neither dominates** (CVO's synthesis, adopted):
the probe proves the **deployed binary behaves as the source says** (mechanical axis — source alone
cannot prove that: the deployed sha could differ, a route could shadow, the ALB could rewrite);
the source read proves the **guard has no allowlist** (the probe alone cannot prove that). Together
they close it. The error was not running the probe — keep the probe. The error was the "strictly
stronger" framing.

| Probe | Result | Want | |
|---|---|---|---|
| `POST /mcp` w/ opaque non-JWT bearer | **401** | 401/403 | PASS — no fall-through |
| `POST /otp/fetch` w/ **wrong** opaque bearer | **401** | 401 | PASS — constant-time compare gates |
| `GET /otp/health` w/ no auth | **401** | 401 | PASS |
| `POST /otp/fetch` w/ no auth | **401** | 401 | PASS |
| `GET /otp/health` w/ real bearer (via liveness λ) | **200** | 200 | PASS — positive control |
| `GET /teams/poll` w/ opaque non-JWT bearer | **302** | 401/403 | see §3 |

**F1 bearer-isolation: CERTIFIED** (CVO 190631Z, on the source enumeration above — *not* on the probe).
Positive and negative controls both fire, so the `/otp` leg is airtight behaviorally; the `/mcp` leg
needed source, and got it. The zero-credential *instinct* is endorsed; the *"strictly stronger"*
reasoning is retracted.

**Transferable lesson (the one worth keeping):** *a behavioral probe cannot close a mechanism claim.*
Ask what property distinguishes your control input from the real one — if a guard could key on exactly
that property, your control has zero power against the failure mode you care about. Reach for source
(here: a call-site enumeration), then use the probe to prove the deployed artifact matches it.

---

## 3. Finding — `/teams/poll` is OIDC-gated at the perimeter, not bearer-gated (DECLARATIVE drift)

**Symptom (grounded, live):** `/teams/poll` + opaque bearer → **302**, not 401. It never reaches
the app's bearer guard.

**Mechanism (grounded — live ALB config, not inferred):** the listener has exactly five rules —
prio 10 `/mcp*,/authorize,/register,/token`; prio 20 well-knowns/`/callback`; prio 30 `/otp/*`;
prio 31 `/ms/*`; **default**. All four non-default rules are bare `forward`. Only the **default**
rule carries `authenticate-oidc`. **No non-default rule matches `/teams/poll`**, so it falls to
the default rule and ALB redirects an unauthenticated caller to the IdP.

**Why it matters (map-vs-territory, not a hole).** The drift runs in the *fail-safe* direction —
the route is **more** restricted than believed — so this is not a vulnerability. But the belief
is load-bearing in a security decision:

- `server.py:401` docstring: *"Bearer-gated REST poll for the teams-watch.sh monitor… so a shell watcher can curl it."* A shell watcher **cannot** curl it; it gets a 302.
- `audit.py:75` comments `/teams/poll` as *"the read-only /teams/poll REST bypass"* and SCTY_MCPGUARD built a G6 audit-fold to close its supposed audit-coverage hole.
- CTO gated a live-path GO on `NO-BYPASS` = 0.8.0's **independent corroboration** of 0.7.0's *"3 REST bypasses"* enumeration. **Both enumerations were performed at the APP layer (`server.py` routes). Neither checked the ALB.** The enum is app-layer-true and perimeter-layer-wrong.

**The actual bearer-gated-not-OIDC perimeter set** (live): `/mcp*` + `/authorize,/register,/token`
+ the well-knowns + `/otp/*` + `/ms/*`. `/teams/poll` is **not** in it. This matches the PREMCP
`inbound_to_fold` note (*"/ms/… joins /otp/* + the MCP-OAuth bypass paths… must be VISIBLE in the
perimeter model, not silent"*) — which never claimed `/teams/poll` either.

**Live-consumer check:** `teams-watch.sh` **does not exist anywhere in the repo.** So no in-repo
machine consumer is currently broken. *Bounded claim:* absence-in-repo is weaker evidence than an
access-log read — if a consumer lives off-repo (e.g. on moltbot), it is currently 302ing and its
owner would see that. The app-layer bearer guard **is** correctly built, so if a `/teams/poll`
ALB rule is ever added, the route lands already-hardened.

**Disposition: FILED, not driven.** No code change. The correction belongs in the SCTY perimeter
model + the two comments above. Routed to CTO (owner of the NO-BYPASS gate) + CVO. The
transferable lesson is the Rule-22a one: *an app-route enumeration is not a perimeter enumeration.*

---

## 4. Stale-record corrections (three, all of which would have caused wrong work)

**B. `github-token-6FYoJ6` is not a secret name — it is the Secrets Manager ARN's random suffix.**
The secret's real name is `github-token`; it already exists (created 2025-12-23, holds an
`AWSCURRENT` version). `create-secret --name github-token-6FYoJ6` would mint a decoy nothing reads.
This is a **rotate** (`put-secret-value`), and the body must be JSON `{"token":"…"}` — the consumer
does `json.loads(SecretString)["token"]` (`freshness_alarm/lambda_function.py:218-219`), so a
bare-string secret raises `JSONDecodeError` rather than merely 401ing. Full steps sent to COO 184845Z.

**C. `NFRA_COMPAWS`'s `blocking:` field is stale and contradicts its own `phase:`.** `blocking:`
still reads *"ACTIVE capacity-gated build-ramp… ramps as AE 0.7 capacity frees"* (2026-06-18 text)
while `phase:` records *"DEPRIORITIZED (Andrew-direct 2026-07-01)… PARKED (not cancelled, not
re-certed)"* and `status: inactive`. Both remaining TOs (`SFN-FIX`, `IAM-CONDITIONS`) are
`<status>complete</status>`, consistent with the 07-01 ruling that they are by-design-DONE.
The stale `blocking:` line is what propagated into the drive brief as *"its blocker is capacity,
your respawn IS the unblock."* **Not ramped** — ramping would re-litigate a completion the 07-01
ruling exists to protect. Registry fix is COO/CTO-authorable, not mine; routed.

**A.** (see §1) — `0ccee9134`'s "NOT yet deployed" note, superseded by the live sha256 match.

**Pattern.** Three independent records drifted, and each drifted in the direction of *inviting work
that is already done*. A `blocking:` field, a commit-message deploy-note, and an ARN-suffix-as-name.
None was caught by a gate, because none of these fields has one. Gate candidate routed to CTO:
`blocking:`/`phase:`/`status:` mutual-consistency lint on `org/projects/*.json` (a `status:inactive`
+ `blocking:` beginning "ACTIVE" is mechanically detectable).

---

## 5. What is genuinely open on PREMCP (unchanged by this record)

- **E1 — secrets-rotation SOP + JWT/Fernet/Graph-secret break-glass: NOT WRITTEN.** Ungated,
  unstaffed, in-lane. PREMCP §4 also parks the `/otp` static-bearer rotation entry here. **Next build.**
- **A1** token revocation (JTI deny-list) — the highest standalone gap per §6.
- **B2** read-only grant coded, not live (needs Andrew admin action).
- **H1** network isolation; **G1** broker review; **E2** Fernet in-memory.
- CVO live-testing of the deployed WAF still pending.

## Compiler Tools

| tool | use | result |
|---|---|---|
| `comp-which` | routed "where is the gateway source / teams/poll" | near-tie (comp-routes/comp-cluster) — **neither fits** (gateway is EC2+ALB, not CloudFront); fell through to on-rails `comp-glob`/`comp-grep` as designed |
| `comp-glob` / `comp-grep` | located `app/*.py`, `/otp` call-sites, `github-token-6FYoJ6` consumers | PASS — 13 matches / 9 files; found the `freshness_alarm.tf` ARN that decoded the suffix-vs-name confusion |

**Gap found:** `comp-which` has no route for *"what is the live ALB/perimeter shape of this
host?"* — the question that produced §3. `comp-routes` covers CloudFront→origin→Lambda, not
ALB-listener-rule → OIDC-vs-forward. An `comp-routes perimeter` (or `comp-aws alb`) surface would
have surfaced the `/teams/poll` drift mechanically instead of by a curl that happened to return
302. Filed as a comp-tool coverage gap (Rule 21: a repeat manual override for one intent = build the tool).
