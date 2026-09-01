# AUTH_SELFHEAL — Rule 27 STAGE-2 PURPOSE-LEVEL PRD

**Project:** `AUTH_SELFHEAL` (D8, `macro_code: AUTH`) · **Version:** v0.1 · **Date:** 2026-08-31
**Author:** `0.6.2_AE_PartnerETL`, named stage-2 author by `1.0.0_SA_CTO` ruling 2026-08-31T22:51Z
**Gate:** `1.0.0_SA_CTO` · **Stage 3 (atom-decomp):** `2.0.0_SA_COO`, unblocked the moment this lands
**Supersedes as scope source:** `BRIEF_SELF_HEALING_RETRY_AUTH_PATTERN_D8_20260831.md` (register `prds[0]`)

> **PURPOSE-LEVEL.** This states WHAT the project is for and WHAT done means. It does not design a
> solution, and it cuts no TO.

---

## 0. THE BINDING CONSTRAINT ON THIS DOCUMENT

`1.0.0_SA_CTO` bound this PRD, on the grounds that its author made three subject/ordering inferences
on 2026-08-31 (wrong function; a comment read in place of `lambdas.tf`; `:410`/`:412` ordering inferred
while the correct line numbers sat in my own quoted traceback):

> **Every mechanism claim carries its status in a field a reader can reject on —
> `measured` / `inferred` / `held` / `absent`. A claim about EXECUTION ORDER or WHICH COMPONENT FAILED
> is `inferred` unless a file:line at a stated vintage or a CloudWatch frame is cited beside it.**

**Applied throughout. A row without a status field is a defect in this document, not a fact.**

---

## 1. PURPOSE

**Auth is a shared dependency across every cookie-riding BD consumer, and when it fails transiently the
estate loses data permanently — because the auth chain repairs itself and nothing re-runs.**

`AUTH_SELFHEAL` exists to make that class safe: a consumer whose auth was briefly unavailable should
end the day with its data, without a human noticing. It owns the **PATTERN** across every consumer and
both firms. It does not own any single pipeline's incident.

⭐ **The property that makes this worth a project rather than a fix: THE SELF-REPAIR REMOVES THE
EVIDENCE.** After the chain heals, every downstream instrument reads a genuinely healthy chain. The
only wrong thing left in the estate is a date that does not exist.

## 2. WHAT IS ESTABLISHED — every row carries its status

| # | Claim | Status | Evidence |
|---|---|---|---|
| E1 | `cot-rebalancer-runner` raised on all 3 invocations 2026-08-31 06:00:41 / 06:01:35 / 06:03:26Z, `RuntimeError: rebalancer /auth/token 200 but no access_token` | **measured** | CloudWatch frame, `/aws/lambda/cot-rebalancer-runner`, stream `2026/08/31/[$LATEST]72a525f1...`; raise at `lambda_function.py:151 mint_rebalancer_bearer` <- `:163` <- `:361` |
| E2 | 0 of 3 Cottonwood bronze feeds landed for 2026-08-31; 3 of 3 (1/5/83 objects) for 08-30 | **measured** | `s3api list-objects-v2`, per-feed, with the 08-30 positive control |
| E3 | 41 of 41 calendar days 2026-07-21..08-30 complete; 0 fully-missing, 0 partial. 08-31 is the first hole in that feed's life. ⛔ **DO NOT EXTRACT THIS ROW WITHOUT THIS CLAUSE: the ordering defect (E8/E9) was present on ALL 41 of those days. The clean days measure MARGIN, NOT HEALTH** — absolute session lifetime happening to outlast the exposure window, 41 times running. **The DEFECT is standing and daily; only its EXPRESSION is new.** This is a per-MEMBER census (members = 41 dates) that cannot see a defect in what the members SHARE (one runner, one auth chain, one schedule) — CLAUDE.md rule 22 COVERAGE, added 2026-09-01 `a590f40325`, of which this row is the fifth instance | **measured**, with the qualifier binding | 1,659 keys enumerated, denominator printed |
| E4 | `opal-assets-bd49f-reporting-pull` failed at auth 2026-08-30 ~18:0xZ, `RuntimeError: BD GET /session/token -> HTTP 401` | **measured** | CloudWatch frame, raise at `lambda_function.py:147 get_clientview_token` |
| E5 | **n=2 for AUTH-STEP FAILURE** — two firms, two functions, two different BD apps (ClientView, Rebalancer), both cookie-riders, both dead at the auth step, with *different* error signatures | **measured** | E1 + E4. ⛔ **This is n=2 for auth-step failure ONLY. It is NOT n=2 for absolute-lifetime expiry.** |
| E6 | `bd-cot-keepalive` ran 4/hr with 0 errors in 19 of 19 hourly buckets across 2026-08-30T18:00Z–08-31T12:00Z, spanning the outage | **measured** | CloudWatch Invocations + Errors; gap-sensitivity bounded by a negative control (a known 18h gap renders as ABSENT buckets) |
| E7 | The keepalive holds READ-only on the session secret and therefore **cannot re-mint** — it extends, it cannot renew | **measured** | ⚠ **PROVENANCE CORRECTED 2026-09-01 (self-filed, 90175): as first written this row was tagged `measured` on an INHERITED peer claim, not my own read.** Now measured at this seat: `simulate-principal-policy` on `bd-cot-keepalive-role` vs `...secret:blackdiamond/cot/session-jnzOyC` → `PutSecretValue` implicitDeny, `UpdateSecret` implicitDeny, **`GetSecretValue` allowed (positive control)**. Conclusion unchanged; provenance was not earned when written |
| E8 | `cot-rebalancer-runner` fires `cron(0 6 * * ? *)`; its session mints `cron(30 7 * * ? *)` America/New_York | **measured** | `cot_rebalancer_runner.tf:171`, `schedule-et.tf:78-97`, both read at source and re-derived by `3.0.0_SA_CVO` |
| E9 | `cot_rebalancer_runner.tf:171` still declares `PLACEHOLDER 06:00Z -- exact time = CTO/WS-4 chain-timing confirm`; that confirm never happened | **measured** | file:line at source |
| E10 | `cot-bd-session-trigger` fired 2026-08-30T11:30:15Z in `mode=session-refresh`, probe returned `HTTP Error 503`, and it took **Lever A — full OIDC-login mint (fail-safe)** | **measured** | CloudWatch frame, stream `2026/08/30/[$LATEST]f4a9989c...` |
| E11 | `cot-rebalancer-runner`'s idempotency guard `_already_landed()` is structurally dead on the deployed role (no `s3:GetObject`; bare `except` renders AccessDenied as "absent"), so `--force` is inert | **measured** | `simulate-principal-policy`: `s3:GetObject` -> implicitDeny; `s3:PutObject` same key -> allowed (control). Fix written and reverted at `725685f85a`; evidence survives at its parent |
| E12 | `aws secretsmanager list-secret-version-ids --include-deprecated` **truncates**, and the truncation renders as a plausible session age rather than an error | **measured** | Two seats, two secrets, two different absurd values (`1,415 h`; `1,979.52 h`); newest version returned for the cot secret `2026-06-09T18:29:20Z` vs `describe-secret` LastChanged `2026-08-31T11:33:37Z` — an ~83-day disagreement |
| E13 | The 49F session served a token successfully at **21.59 h** of age (minted 00:03:47Z, pre-flight succeeded 21:39:14Z) | **measured by `0.4.0_DS_ClientPlatform~Y`, cited not re-derived** | CloudWatch; relayed via `1.0.0_SA_CTO` ruling §3 |
| E14 | The "~18 h session window" as an **absolute lifetime** | **FALSIFIED** | E13 exceeds it. `2.0.0_SA_COO` withdrew the hypothesis. ⛔ **This PRD may not carry a ceiling.** |
| E15 | Cottonwood session age at the 06:00:41Z failure | **inferred** | E10 gives the mint FIRE time (measured); the secret WRITE time for 08-30 is not readable (E12). Deriving ~18.5 h requires assuming the 08-31 fire→write lag (~3.4 min) also held on 08-30. **Stated as inferred; not to be promoted.** |
| E16 | 49F session age at the 2026-08-30 401 (E4) | **absent** | Not measured by any seat. ⛔ **Must never be derived from E12.** |

⚠ **A NOTE ON E10, WHICH IS NEW TO THIS DOCUMENT AND CHANGES AN INPUT OTHERS ARE USING.** `1.0.0_SA_CTO`
and `0.0.0_AB_MSTR` both recorded my nomination of the session-trigger CloudWatch record as *untested*.
**I have now tested it and it works** — it yields the mint FIRE time, the mode, and which lever was
taken, per day. **It does NOT yield the secret WRITE time**, which is the quantity E15/E16 actually
need. So it is a partial replacement for E12, not a full one, and I am not claiming more.

## 3. SCOPE

**In scope — the pattern, estate-wide:**
1. **Ordering as a first-class constraint.** For every cookie-riding consumer, derive and validate the
   fire time against its own mint time; retire every `PLACEHOLDER` schedule declaration in the class.
2. **Post-heal recovery.** When auth heals mid-day, what re-runs? Today: nothing (E1+E2 with E10).
3. **Re-mint capability, or an explicit decision not to have one.** E7 means nothing between daily
   mints can renew a dead session. Whether that should change is this project's to decide.
4. **The consumer inventory** — every consumer, its secret, its mint, its schedule, its exposure
   window — so the next instance is found by a table rather than by an incident.
5. **The session-age instrument.** E12 is broken and E10 is partial. The project's central quantity is
   currently unmeasurable for historical dates; establishing a sound instrument is in scope.

**Out of scope:**
- ⛔ **Alarms, monitors, notifications, freshness-checkers.** **This project FIXES; it does not NOTIFY.**
  All alarms are **held** pending `GLOBALALARM` (D10). A retry is not an alarm; a detector is.
  **A deliverable that drifts from retrying/reordering into detecting-and-reporting has changed
  category and is HELD.**
- ⛔ Vendor-credential handling, rotation policy, login-mechanism changes.
- ⛔ Shadow or build-alongside auth paths (standing Andrew veto).
- ⛔ **The Cottonwood instance.** `MDPF_HEALGAP` owns the missing 2026-08-31 date, that runner's
  schedule ordering, and its recovery gap. **Boundary confirmed by `1.0.0_SA_CTO` as written on the
  register row.** The tell: moving one `schedule_expression` fixes the instance and makes **no other
  pipeline safer**.

## 4. DEFINITION OF DONE

`AUTH_SELFHEAL` terminates when all four hold:
1. **An inventory exists** covering every cookie-riding consumer across both firms, each row carrying
   secret, mint schedule, fire schedule and exposure window.
2. **A validated ordering rule exists** and every consumer conforms or carries a stated exception —
   no `PLACEHOLDER` schedule survives in the class.
3. **A stated position on re-mint** — either the capability exists, or the decision not to have one is
   recorded with its consequence.
4. **A consumer whose auth was transiently unavailable ends the day with its data**, demonstrated on a
   real seam rather than argued.

⚠ **Not sufficient for done:** a schedule move. It is a **mitigation** — it shrinks the exposure window
and makes no mid-window outage recoverable. Item 4 is the one that closes the class.

## 5. OPEN QUANTITIES — carried as open, not as unknowns to be filled by inference

- **Session-age-at-failure** for both instances (E15 `inferred`, E16 `absent`). Carried as an **OPEN
  QUANTITY**. ⛔ **No ceiling may be asserted** (E14).
- **Whether the class has silently holed other dates** on other consumers. Only the cot rebalancer has
  been swept (E3). **Absent for every other consumer.**
- **What actually killed the cot session** on 08-31. E7 removes the keepalive; E14 removes the simple
  lifetime story. **Currently `absent`, and the PRD does not nominate a mechanism.**

## 6. CONSTRAINTS AND LIVE HOLDS

- The `--date 2026-08-31` one-shot recovery is **HELD** by Andrew (*"I will discuss with CTO, hold for
  further advisory"*). **HELD is not DECLINED.** Belongs to `MDPF_HEALGAP`, not here.
- **Vendor egress requires Andrew's own explicit per-use word.** Per `2.0.0_SA_COO`'s adopted split: a
  CTO advisory settles design/disposition, but **a hold can be tightened by a relay and never released
  by one.**
- Placement is deferred behind the comb; the whole-register device-ownership decision settles it.
- The alarm moratorium binds this project (§3).
- E11 is a **precondition** for any second-attempt design: with the guard dead, a second fire re-pulls
  instead of skipping.

## 7. WHAT STAGE 3 NEEDS FROM THIS DOCUMENT

The decomp domain is §3 in / §3 out, with §4 as the termination test. ⚠ **§5 items are OPEN QUANTITIES,
not cells to be closed by reasoning** — a cell that "resolves" an open quantity without a new
measurement is the failure mode this PRD's §0 constraint exists to prevent.
