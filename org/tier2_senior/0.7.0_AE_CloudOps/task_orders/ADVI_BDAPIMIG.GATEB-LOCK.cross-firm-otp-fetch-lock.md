# TASK ORDER — ADVI_BDAPIMIG.GATEB-LOCK

<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_BDAPIMIG, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: on-hold</status>
<!-- ON-HOLD 2026-06-29 (CTO briefing 142313Z, Andrew Schwab-SSOT-migration GO): the thin-BD-tether direction makes BD's surviving role low-frequency, so 49f stays ATTENDED/periodic through the migration -- which sidesteps the cot/49f unattended concurrency entirely, so the unattended OTP-lock is not currently needed. LEG2 already proved the mechanism (49f cookie re-mints, durable port works). Design 09d0883cd + this TO stand READY if the migration PRD ever wants unattended 49f. Do NOT build until CTO/PRD calls for it. -->
<priority>ON-HOLD — superseded by the Schwab-SSOT thin-tether right-sizing (49f attended-only); ready if PRD wants unattended</priority>
<date>2026-06-29</date>

## Objective

Build the gateway-side cross-firm OTP-fetch LOCK that makes a cot/49f cross-firm OTP collision
CANNOT-HAPPEN (the bar for a NEVER#1 control), enabling 49f durable auto-login to run UNATTENDED
(GATE B). Design contract: `org/tier2_senior/0.6.2_AE_PartnerETL/designs/bd-otp-cross-firm-lock-contract.md`
(09d0883cd, 0.6.2-authored, COO-accepted).

## Why a lock, not a time-blackout (ruled — COO 2026-06-29)

cot + 49f read OTP from ONE shared mailbox (andrew@opalinvest.com); the gateway bearer does NOT route
per-firm. `window_seconds` bounds STALENESS but not CONCURRENCY. A time-blackout was rejected — it
fails both of CTO's tests (0.6.2-grounded): (i) SIZING — cot's worst-case OTP span is ~15-20min (tries
30 x delay 10s x 3 attempts + backoff), so a blackout would have to be huge and eat 49f's own re-mint
windows; (ii) OFF-CYCLE — cot has 3 trigger paths (daily cron + 15m keepalive + freshness-probe), so a
fixed-time window cannot guarantee single-window. The lock is concurrency-correct by construction.

## Load-bearing design point (DO NOT scope this as a fetch-only lock)

A gateway-ONLY lock inside `/otp/fetch` is INSUFFICIENT — the collision forms BOX-side at
CREDENTIAL-SUBMIT (when BD emails the OTP into the shared mailbox), BEFORE any fetch. So the lock MUST
be HELD ACROSS cred-submit via 3 gateway endpoints:
- `/otp/acquire` — called BEFORE the box submits credentials; takes the lock.
- `/otp/fetch` — returns the code ONLY if the caller holds the live lock.
- `/otp/release` — called in a `finally` after the login resolves.

Lock state: gateway-side, a single global DDB item keyed to the shared mailbox, conditional-write,
TTL auto-expiry (~20min ceiling, fail-closed if the lock service is down). `window_seconds` retained
as belt-and-suspenders.

## Build lanes

- **Gateway code + DDB table + IAM** = 0.7.0_AE_CloudOps (base, the m365-mcp-gateway owner lane) — the
  3 endpoints in `otp.py`/`server.py`, the DDB lock table + conditional-write, the gateway-role IAM.
- **Box-side acquire/release wrap** = 0.6.2_AE_PartnerETL — thin wrapper change around the login
  critical section (the box already loud-fails+retries on OTP_GATEWAY_NO_CODE, so a lock-induced
  wait/retry is already handled). Coordinate with base on the endpoint contract.
- **Arch-gate** = 1.0.0_SA_CTO ratifies the lock contract (the cannot-happen firm-sep guarantee) before
  it goes live + before GATE B (unattended 49f) is enabled.

<compiler_tools_mandate>
- `comp-iam service` on the gateway role after the DDB + endpoint IAM changes (conditional-write grant).
- `comp-routes behaviors` if the 3 new endpoints touch CloudFront/ALB routing.
- Ground the firm-sep guarantee against a concurrent-login test (two firms acquire simultaneously — one
  must block), not config-only.
</compiler_tools_mandate>

<cross_domain_coordination>
Touches the SHARED m365-mcp-gateway (cot ALSO uses /otp/fetch — this is the whole point). The acquire/fetch/release contract change must be backward-compatible with cot's existing gateway-OTP path OR cot's box-side wrap updates in the same change (cot is the other firm on the lock). Coordinate base (gateway) + 0.6.2 (49f box) + the cot-pipeline owner (cot box) so no firm is left calling the old fetch-only contract. CTO arch-gates the cross-firm correctness.
</cross_domain_coordination>

<acceptance_criteria>
1. The 3 endpoints (acquire/fetch/release) live on the gateway; /otp/fetch returns a code ONLY to the live lock-holder.
2. CONCURRENT-LOGIN TEST: two simulated firm logins acquire simultaneously — exactly one proceeds, the other blocks until release/TTL. Proven, not asserted (the cannot-happen guarantee).
3. TTL fail-closed: a never-released lock auto-expires at the ceiling; a down lock-service fails closed (no code returned), not open.
4. cot's existing gateway-OTP path still works (backward-compat or co-updated).
5. CTO arch-gate PASS on the firm-sep contract. RAVC to 2.0.0_SA_COO with the concurrent-test evidence; only THEN is GATE B (unattended 49f enablement) eligible.
</acceptance_criteria>

## Sequencing

STAGED — do NOT pull this onto the LEG2 critical path. 49f LEG2 (the attended unfreeze) proves the
mechanism (GATE A) and is firm-safe via window_seconds + attended off-cot-window timing. This lock is
the prerequisite for flipping 49f to UNATTENDED steady-state (GATE B), which stays HELD until this is
built + the concurrent-test passes + CTO ratifies. Pick it up after LEG2 lands.
