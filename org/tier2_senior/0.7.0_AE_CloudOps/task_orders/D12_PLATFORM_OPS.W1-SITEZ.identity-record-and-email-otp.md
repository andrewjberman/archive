# TO D12_PLATFORM_OPS.W1-SITEZ — identity record extension + email OTP (the MFA critical path)

<task_order id="D12_PLATFORM_OPS.W1-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-31T23:3xZ</issued>
<status>pending — GO rides this commit. Cells 1.1/1.2/2.1 are READY; 2.5 is READY but CONDITIONAL (see §5).</status>
<priority>P1 — the entire MFA spine depends on WS-1, and D12 is Andrew's stated first priority.</priority>
<authority>
ANDREW-DIRECT 2026-08-31 ~23:15Z, record @efcfa8cc5b, VERBATIM: "All recs approved. Make sure that on
the email otp we should be properly set up with SES now that its no longer sandboxed. The only thing
we will want to clarify is the DNS/DKIM/DMARC and health of that service so these things don't go to
spam. Furthermore, we will want to do the testing for 2FA on my account so we know it works before
pushing anything to clients" — which PLACED D12 ON SITE Z and made this TO cuttable.
Rule 27 chain: PRD `docs/architecture/D12_PLATFORM_OPS_PRD.md` @2da36986f6 (1.0.0_SA_CTO~Z) ->
COO atom-decomp `org/tier1_exec/2.0.0_SA_COO/deliverables/laneZ_DECOMP_20260831_D12_PLATFORM_OPS_USERMGMT.md`
@0a8a66af57 (this TO's cells are that decomp's, unchanged).
ARCH-GATE DECIDED — 1.0.0_SA_CTO~Z under the PRD's own CTO gate: **BUILD IN `auth-handler`.** NOT
Cognito (the bespoke token is read by ~8 surfaces incl. 2 at the CDN edge; Cognito changes issuer and
shape for all of them to add a challenge in front of a working session flow). NOT Entra (eliminated on
POPULATION — portal users are partner-firm clients outside Opal's tenant). That seat owes a decision
record; do not re-litigate the gate.
</authority>
<proof_of_spec>
  <expected_criteria>W1-1,W1-2,W1-3,W1-4,W1-5,W1-6,W1-7,W1-8,W1-9</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D12_PLATFORM_OPS.W1_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 0. PROOF-OF-SPEC CRITERIA — what each id must OBSERVE

⛔ **Every row below is an OBSERVATION, not a description.** A criterion whose evidence is "the code
does X" has not run. Cite the call, the input and the result.

| id | must observe |
|---|---|
| **W1-1** | A **pre-migration** user logs in successfully AND reads a **DEFINED** MFA preference. Evidence: the user's pre-migration state, then the post-migration read-back showing a non-null value. ⛔ A schema dump is not this. |
| **W1-2** | A new user round-trips a phone number: write, then **read back the stored value**. |
| **W1-3** | An MFA-enabled account **cannot reach the dashboard** without a live code — exercised end to end against the deployed handler, not a unit test. |
| **W1-4** | A **WRONG** code is rejected. Name the code submitted. |
| **W1-5** | A **REPLAYED** (previously-valid, already-consumed) code is rejected. ⭐ This is the one most often skipped and the one that matters — a replayable OTP is not a second factor. |
| **W1-6** | The OTP secret is **never returned by any endpoint**. Name the endpoints checked and the denominator (how many endpoints exist on the handler). |
| **W1-7** | The channel preference accepts `sms` as an **expressible value** while **no SMS sender is wired**. Both halves: the value stores and reads back, AND a search for an SMS send path returns zero **with a positive control**. |
| **W1-8** | **NEGATIVE — nothing alarm-shaped was created.** Enumerate every AWS resource this work created and show the set contains no alarm, SNS subscriber, monitor or freshness checker. A bare "I did not build one" is not evidence; print the created-resource list. |
| **W1-9** | **NEGATIVE — no remembered-device work and no invented TTL constant.** WS-3 is not in this TO. Show no TTL constant other than the ruled 30 days appears in what you wrote, with a positive control proving the search works. |

⚠ **W1-8 and W1-9 are NEGATIVE criteria and they are the two most likely to be scored from memory.**
A negative criterion needs a **positive control** or it cannot tell a true absence from a broken
search — that failure mode has bitten three seats on this fabric tonight alone.

## 1. OBJECTIVE

`opal-users-v2` carries the identity fields MFA needs, and an **email** OTP challenge sits between the
credential check and dashboard access in `auth-handler`.

## 2. CELLS

| Cell | Deliverable |
|---|---|
| **1.1** | `opal-users-v2` carries phone number, MFA channel preference (`email\|sms\|none`), and whatever the WS-3 remembered-device design requires. |
| **1.2** | Migration leaving existing users in a **DEFINED** state, never a null one. |
| **2.1** | OTP challenge between credential check and dashboard. **EMAIL LEG ONLY.** |
| **2.5** | Per-account MFA enablement — **CONDITIONAL, read §5 before building it.** |

## 3. ACCEPTANCE — every row is an EXERCISE, and a description is never one

**1.1 / 1.2:** a **pre-migration** user logs in successfully and reads a *defined* MFA preference; a
new user round-trips a phone number through write and read.
⛔ **A SCHEMA DUMP IS NOT ACCEPTANCE.** The PRD says so explicitly. Show the read-back.

**2.1, and all four halves are required:**
1. an MFA-enabled account **cannot reach the dashboard** without a live code — exercised end to end;
2. a **wrong** code fails;
3. a **replayed** code fails (this is the one most often skipped, and it is the one that matters);
4. the OTP secret is **never returned by any endpoint** — name the endpoint you checked.

## 4. HARD CONSTRAINTS

- ⛔ **NO ALARM, MONITOR, SNS SUBSCRIBER OR FRESHNESS CHECKER.** Andrew lifted the hold on ONE named
  thing tonight (D7's ticket reminder) and **a hold lifted by name is lifted for that name.**
  GLOBALALARM stands for everything else, including anything that would watch email deliverability.
- ⛔ **EMAIL LEG ONLY. THE SMS LEG IS DEFERRED, NOT RETIRED**, and needs Andrew's explicit **per-use**
  word before any vendor egress. Availability is not authorization. Build the channel-preference field
  (1.1) so `sms` is expressible; do not wire an SMS sender.
- ⛔ **REMEMBERED-DEVICE TTL IS SETTLED: 30 DAYS, revocable by sign-out-everywhere.** Do not invent a
  different constant, and do not build WS-3 under this TO — it is a separate cell behind 2.1.
- ⛔ **MFA IS ENTIRELY GREENFIELD. IF YOU RE-DERIVE THAT, USE A WORD BOUNDARY AND EXCLUDE LOCKFILES.**
  A loose census returned 5 apparent `mfa`/`totp`/`otp` hits in `auth-handler` and **every one was a
  base64 substring inside a lockfile integrity hash** (`sha512-...AmfAaJ...` matches `mfa`).
  Word-boundary re-run over source: **ZERO**; positive control `password`: **157**. There is nothing to
  extend — 2.1 builds it. `PORTAL_AUTHHARD`'s WS-3 was specified and never built.
- ⛔ **PRIOR ART: IMPORT, DO NOT REOPEN.** `PORTAL_AUTHHARD` carries the MFA/account-lifecycle design.
  Read its PRD at its path; **do not reopen the project** — that is Andrew's call, not this lane's.
- **Deploy lane:** `auth-handler` is infra/AE. Terraform only for Lambda code; never
  `aws lambda update-function-code`. `safe-apply`, never bare `terraform apply`.

## 5. ⚠ CELL 2.5 IS CONDITIONAL, AND THE CONDITION IS THAT IT RESTS ON AN INFERENCE

Andrew said: *"we will want to do the testing for 2FA on my account so we know it works before pushing
anything to clients."* That is a **STAGED-ROLLOUT GATE naming an ORDERING**, and it binds this
workstream's acceptance: **no client account is exposed to MFA before his own account has been
exercised end to end.**

`1.0.0_SA_CTO~Z` inferred from it that MFA must be **enable-able PER ACCOUNT** rather than globally,
because the gate is otherwise unsatisfiable. ⛔ **THAT INFERENCE IS EXPLICITLY NOT ANDREW'S WORDS AND
IS FLAGGED AS SUCH BY ITS AUTHOR.** Build 2.5 only if per-account enablement is genuinely required to
satisfy the ordering. **If you find another way to satisfy it, say so and DO NOT BUILD 2.5** — it is
not a requirement he stated, and a cell built on an unstated requirement is scope you invented.

## 6. NOT YOURS UNDER THIS TO

- **2.3 SES readiness** and **2.4 DNS/DKIM/DMARC + service health** are `1.0.0_SA_CTO~Z`'s and it has
  taken them. ⭐ **2.4 IS AN ACCEPTANCE CONDITION OF WS-2, NOT A FOLLOW-UP — a one-time code that lands
  in spam is a BROKEN login, not a degraded one.** Your 2.1 is not accepted until that lands; coordinate,
  do not duplicate.
  ⚠ Andrew states SES sandbox exit as FACT. **A stated premise is still measured before it is built on.**
  If 2.3 comes back saying the account is NOT out of sandbox, that is a **finding to report**, not
  something to quietly fix — and your email leg's acceptance depends on the answer.
- **4.1 admin UI** is DE-class. **6.1 onboarding review** is unassigned. **WS-5 partner-admin
  delegated add** is a later TO and depends on 4.1.

## 7. CERTIFICATION

⚠ **`3.0.0_SA_CVO~Z` IS DEAD — no CVO reader exists on this device right now.** Re-seating it is
routed to `0.0.0_AB_MSTR~Z` as a reboot respawn. **Cells whose entire value is independent
certification must not be self-scored** — a build seat scoring its own security exercise is the
author-verifies-author shape. Nothing in THIS TO is a cross-firm refusal cell, so proceed; but if you
reach one, stop and route it.

## 8. REPORTING

Report to `2.0.0_SA_COO~Z` (validation) and `1.0.0_SA_CTO~Z` (acceptance). State push state as a
MEASURED value. **Surprise items** (class {OBSERVATION, BLOCKING}) route to `0.0.0_AB_MSTR~Z` while
there is no CVO reader — surface and keep working; do not halt-and-investigate.
