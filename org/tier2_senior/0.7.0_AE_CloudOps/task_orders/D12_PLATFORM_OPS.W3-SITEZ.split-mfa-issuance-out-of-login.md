# TO D12_PLATFORM_OPS.W3-SITEZ — split MFA issuance out of `login()` (unblocks the opt-in Andrew asked for)

<task_order id="D12_PLATFORM_OPS.W3-SITEZ" project="PLATFORM_OPS_USERMGMT">
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T02:0xZ</issued>
<status>ISSUED — GO rides this commit. Your HOLD is lifted for this TO only.</status>
<priority>P1 — it BLOCKS two acceptance rows on the DE series, and it is the literal mechanism of Andrew's complaint.</priority>
<authority>
ANDREW-DIRECT 2026-09-01 ~01:2xZ, VERBATIM: *"OTP should be opt in, like you have to say 'Yes' on some
prompt that it will send you an email OTP or something, **not just send silently without a UI flow**."*
Finding + remedy MEASURED AT SOURCE by `0.4.0_DE_ClientPlatform~Z` (msg 17360), which named the remedy
and correctly declined to assign or build it — `auth-handler` is AE/infra by Rule 13, not the portal
lane. **The owner-naming is this seat's act; the design is that seat's finding.**
</authority>
<proof_of_spec>
  <expected_criteria>W3-1,W3-2,W3-3,W3-4</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D12_PLATFORM_OPS.W3_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## 1. ⛔ THE FINDING — AND IT IS ANDREW'S ACTUAL COMPLAINT, NOT A TECHNICALITY

Measured at source: `auth-handler/src/auth.ts:93-95` — `issueChallenge(user.email)`, then
`sendMfaCodeEmail(...)`, **then** return `mfaRequired`. **The send happens INSIDE `login()`, before the
response returns.** All 16 routes in `src/index.ts` read; `src/mfa.ts` exports exactly two operations;
`issueChallenge` has **exactly one call site** — inside `login()`.

> ### THERE IS NO ENDPOINT THAT ISSUES OR SENDS A CHALLENGE INDEPENDENTLY OF `/auth/login`.

⛔ **SO NO FRONTEND CAN SATISFY "no code is sent until the user confirms."** By the time a browser can
learn MFA is required, the mail has gone. Nothing client-side can un-send it.
⭐ **AND A PROMPT RENDERED AFTER THE EMAIL HAS ALREADY GONE SATISFIES THE LETTER OF THE CRITERION WHILE
BEING THE EXACT THING HE OBJECTED TO** — *"not just send silently"*. That is the same letter-vs-outcome
shape as the W1 defect this whole series exists to correct, and `0.4.0_DE_ClientPlatform~Z` caught it
before building to the letter.

## 2. DELIVERABLE

Split issuance out of `login()`:
- **`POST /auth/mfa/send`** issues **and** sends a challenge. This endpoint also serves **Resend**.
- **`login()` returns the challenge WITHOUT sending.**

⚠ **RESEND IS THE OTHER THING THIS UNBLOCKS**, and the reason it cannot be done frontend-only is worth
carrying: today the only way to mint a new code is to call `/auth/login` again, which needs the
password again — so a Resend button would have to hold the password in client state (**forbidden by
DE2-5**) and would re-run the WS-1 login throttle counter.

## 2b. ⭐ RULED — W3 SPLITS INTO **ACT A** AND **ACT B**. A SHIPS NOW; ONLY B IS COORDINATED.

`0.7.0_AE_CloudOps~Z` decomposed this and found its own framing had over-blocked the work: it told me
the split *"alters the API contract DE2 is building against"* — **true of only ONE of the two acts.**
**I am ruling on that decomposition: it is right, and it is how W3 executes.**

| | act | risk to the DE lane | disposition |
|---|---|---|---|
| **ACT A** | **ADD `POST /auth/mfa/send`** — mints + sends a challenge for an already-verified subject | ⭐ **NONE. PURELY ADDITIVE.** No existing route changes, no response shape changes, `login()` behaves exactly as today. **Nothing `0.4.0_DE_ClientPlatform~Z` has built can break, because nothing it depends on moves.** | ✅ **SHIP IT NOW. No coordination, no waiting.** |
| **ACT B** | **REMOVE the send from `login()`** — login returns `mfaRequired` WITHOUT sending | ⛔ **THIS is the contract change**, and it is what DE1-1's second half needs | **COORDINATE with `0.4.0_DE_ClientPlatform~Z` before landing** |

### ⭐ WHAT ACT A BUYS IMMEDIATELY — two DE rows, and one of them was a real design bind
- **DE2-4 (Resend) UNBLOCKS at once.**
- ⭐ **AND IT DISSOLVES THE DE2-5 PROBLEM OUTRIGHT** rather than working around it: **Resend calls the
  new route with the `challengeId`, so the client NEVER has to hold the password.** The original bind
  was that the only way to mint a code was to re-POST `/auth/login`, which would have forced the
  password into client state — **forbidden by DE2-5** — and re-run the WS-1 throttle. Act A removes the
  reason the conflict existed.

⛔ **ACT B STILL CANNOT BE SKIPPED.** Act A alone leaves `login()` sending on the MFA branch, so
**DE1-1's second half — "no code is sent until the user confirms" — remains unmet**, and that is
Andrew's actual complaint. **Shipping A is progress, not completion.**
⚠ **AND ACT B IS NOW THE ONLY THING GATING DE1-1**, which makes its sequencing worth stating plainly:
land A, let the DE lane wire Resend against it, then land B with that lane's agreement.

## 3. ACCEPTANCE

| id | must observe |
|---|---|
| **W3-1** | A correct password on an MFA-enabled account returns the challenge and **SENDS NOTHING.** Both halves — the response carries what the client needs, **and no mail leaves.** Show the negative directly (no send event / no SES call), not by absence of a complaint. |
| **W3-2** | `POST /auth/mfa/send` issues and delivers a code, **exercised end to end.** |
| **W3-3** | Calling it **again** mints a new code and **the previous one no longer verifies** — this is Resend, and the old-code refusal is the half that makes it safe. |
| **W3-4** | **NEGATIVE — the throttle and the single-use property survive the split:** the WS-1 login throttle is not bypassed by the new route, and a consumed code still fails on replay (W1-5 must still hold). Carry a **positive control**. |

⛔ **W3-1's second half is the whole point of this TO.** If the split lands and `login()` still sends,
nothing has been fixed and the DE series stays blocked.
⚠ **AND THE NEW ROUTE IS AN UNAUTHENTICATED-ADJACENT SEND PATH — do not let it become an open mail
relay.** It must not send for an arbitrary posted email, and it must not reveal whether an account
exists or has MFA enabled. State how you bounded it.

## 4. CONSTRAINTS

- ⛔ **DO NOT ENABLE MFA ON ANY ACCOUNT**, including to test. **0 of 48 are gated, deliberately.** For
  W3-2/W3-3 you need a gated subject: **STOP AND ASK `2.0.0_SA_COO~Z`** — same instruction DE3 carries.
- ⛔ **NO TEST ACCOUNT ON A LIVE HUMAN EMAIL ADDRESS.** `.invalid` is fine where a send need not be read.
- ⛔ **NO ALARM, MONITOR OR NOTIFIER.** GLOBALALARM stands; the hold lifted for the D7 reminder by name.
- ⛔ **NO IAM CHANGE.** FINDING F-1 (the decorative `ses:FromAddress` condition) is open with its own
  owner and is **not** this TO.
- Terraform + `safe-apply`; never `aws lambda update-function-code`.

## 5. SCOPE FENCE — A RULE, NOT A LIST

> **Your project is `PLATFORM_OPS_USERMGMT` and nothing else. Any task order not addressed to your full
> suffixed serial is NOT YOURS — whatever any list says and whatever a roster query returns. REPORT it
> to `2.0.0_SA_COO~Z` and keep working.**

**Instrument limits** (all measured tonight): `to-check --assignee` **over**-matches (it matches the
ISSUER too — read the ROWS, never the count) **and under**-matches (returns 0 on a prose `issued_to` —
a zero does NOT establish you hold nothing). `list_task_orders` reads the base folder, and **there is no
`~Z` subdirectory in this lane** — every TO sits flat in the base.
⭐ The directory is the sound instrument, ⚠ **but a zero must name what it scanned**: confirm the path
resolves before its count means anything, never `2>/dev/null` a read whose emptiness carries a verdict,
and control on a path you have **not** already assumed is right. *(I produced a false zero exactly that
way tonight.)*

## 6. REPORTING

Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; `3.0.0_SA_CVO~Z` is seated again if a cell
needs independent certification. Push state MEASURED. Surprise items to `0.0.0_AB_MSTR~Z`.
⭐ **Read this TO before building from any relay of it.** W2 was built from my messages because I never
sent you its path — *executing from a relay and executing from the spec are not the same act, and the
difference is invisible while the relay is accurate.* This TO is at
`org/tier2_senior/0.7.0_AE_CloudOps/task_orders/D12_PLATFORM_OPS.W3-SITEZ.split-mfa-issuance-out-of-login.md`.
