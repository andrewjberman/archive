# TO D12_PHONE_OTP_ALL_AWS.SF-SITEZ — SMS enable + phone capture/ownership-verify UI

<task_order id="D12_PHONE_OTP_ALL_AWS.SF-SITEZ" project="D12_PHONE_OTP_ALL_AWS">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T14:xxZ</issued>
<status>IN PROGRESS - NOT COMPLETE. SF-3 (stale-docstring fix) DONE @portal 17c9a829. SF-2 (phone capture + ownership-verify UI) BUILDING on surface (c) = a POST-LOGIN authenticated enrolment step (ruled by 1.0.0_SA_CTO~Z 19024; trigger = dismissible card on /market); the SB-7/8 endpoint contract is reconciled so SF-2 is unblocked. SF-1 (enable sms) NOT flipped - gated on a DELIVERED test SMS per CVO~Z's amended rubric 6530ac26e0, which needs SP-1 go-live. This TO stays OPEN until SF-2 lands and SF-1's gate is met.</status>
<priority>P1 — parallel with SB-SITEZ. SF-2 is the real added UI and does not depend on provisioning.</priority>
<authority>
Andrew-direct 2026-09-01 (CTO~Z terminal): "lets push for all AWS" -> "Authorized, go ahead."
BUILD LEG AUTHORIZED. Decomp:
`org/tier1_exec/2.0.0_SA_COO/deliverables/laneZ_DECOMP_20260901_D12_PHONE_OTP_ALL_AWS.md` @`71c743405a`.
PRD: `1.0.0_SA_CTO~Z` @`65f7a59396`.
</authority>
<proof_of_spec>
  <expected_criteria>SF-1,SF-2,SF-3</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/D12_PHONE_OTP_ALL_AWS.SF_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## SCOPE — you hold this project and this project only (Rule 27)
Your `PLATFORM_OPS_USERMGMT` faces (DE1/DE2/DE3) are CLOSED as of this seating. This is a SIBLING project.

## THE ATOMS (full detail in the decomp; source anchors RELAYED from the PRD — CONFIRM at source)
| id | must observe |
|---|---|
| **SF-1** | flip `sms` to `available:true` in `MfaOptInPrompt` CHANNELS — ⛔ **only AFTER Lane A (SB) is live in the target env.** Until then the picker stays "Unavailable." |
| **SF-2** | **NEW: phone capture + ownership-verify UI** — collect E.164, send a test code, confirm, store via `/auth/mfa/preference`. Channel is chosen at ENROLMENT (stored pref); the login-time picker reflects the stored channel. Acceptance: a user can enrol a number they demonstrably control (test-code round-trip) and CANNOT store an unverified number; E.164 validated client-side to match `auth.ts:245`. |
| **SF-3** | fix the STALE docstrings (`MfaOptInPrompt.tsx` header + `AuthContext.tsx:429`) still describing the pre-Act-B backend as current — they must describe issue-not-send (Act B) reality. |

## GATES + NOTES
⛔ **SF-2 stores a number against the account, but NO real SMS is sent to an unverified number** until Lane A is live and provisioning (SP-1/SP-2) clears — the sandbox enforces verified-destinations-only; exercise SF-2 against a VERIFIED test number.
⚠ **F-10 sibling:** SF-2 associates the phone with the account; the identity-continuity gap (email-keyed refresh) is `0.7.0_AE_CloudOps~Z`'s plane, tracked as F-10 in `PLATFORM_OPS_USERMGMT` — do not re-file here.
⛔ No monitor/alarm on this surface (moratorium).

## ⛔ AMENDMENT 1 — CTO~Z 18859 (per-channel copy signal)
The `login()` response now carries `channel` = `user.mfaChannel` (`email|sms`), server-authoritative and
bound at enrolment (NOT a per-login caller pick). ⭐ **That is your per-channel "we texted/emailed you"
copy signal — render the confirmation copy from the response's `channel`, never infer it.** Consistent with
SF-2's enrolment-preference model.

## ⛔ AMENDMENT 2 — proof-of-spec scoping + SF-2 unblock path (DE~Z 18934, adopted)
- **SF proof-of-spec scores the CLIENT contract ONLY:** SF-2's UI round-trip (F2), the client correctly
  gating store-behind-verify, E.164 matching `auth.ts:245`. ⛔ The SERVER invariants (F1, F3a, F4, F5) are
  scored against the SB backend atom's acceptance, NOT this SF face — else SF is graded on properties its
  lane cannot deliver (D12's original-defect shape, one level up).
- **F3b: DE-CALLS / AE-WRITES.** SF-2 DRIVES the verify (calls SB-8); the verified-state field is written
  server-side (AE~Z's plane). SF-2 never writes the user record (Rule 13).
- **SF-2 build UNBLOCKS once SB-7/SB-8's endpoint contract is named** (AE~Z↔DE~Z handshake, per SB Amendment
  3). Holding SF-2 until then is correct — build the client against real endpoints, not presumed ones.
- ⛔ **SF-1 (`available:true`) GATED on F3a binding + SF-2's verify path existing — as a VALIDITY CONDITION
  ON THE SF-1 ROW** (MSTR~Z's deadline), not held in your head. The one-line flip is the "smaller,
  safer-looking edit that lands ahead of its validation" shape.

## ⛔ AMENDMENT 3 — surface (c) RULED + SF-1 REFRAMED (CTO~Z 19024; BINDING)
✅ **Enrolment surface RULED: (c) POST-LOGIN authenticated step** (CTO~Z, concurring with the COO scope
verdict; (b) OUT on the assurance-level principle, (a) is future scope). SF-2 is a component in the
authenticated shell (post-login landing `/market`) — **NO new route, stays in scope.** The TRIGGER widget
(one-time nudge / dismissible card / menu-item modal) is `0.4.0_DE_ClientPlatform~Z`'s UX proposal to bring;
CTO~Z rules the surface, not the widget.
⛔ **SF-1 REFRAMED — it is NOT "add a selectable sms radio."** `mfaChannel` is a SINGLE stored value bound
at issue, so the login-time `MfaOptInPrompt` must **RENDER the user's stored channel** ("we'll text a code
to the number on file" / "we'll email you") with "Send me a code" as the consent. The current email-vs-sms
picker is VESTIGIAL: `requestMfaCode` sends only `{challengeId}` and the backend dispatches on the
challenge's bound channel, ignoring any client channel — **a UI offering a choice the backend ignores would
LIE.** So SF-1 = "the login prompt correctly REFLECTS + the send HONORS the stored sms channel for enrolled
users," NOT a per-login channel choice (which would require multi-channel enrolment — not the model).
`3.0.0_SA_CVO~Z`: score SF-1 to this framing.

## ⛔ AMENDMENT 4 — SF-1 GATE CORRECTED to a DELIVERED test SMS (DE~Z 19119 / CVO~Z `6530ac26e0`; BINDING)
⛔ **My SF-1 gate ("F3a bound + SF-2 verify path exists") was INCOMPLETE — it fails toward ACTIVATION.**
DE~Z found the false-pass: after the SB apply (15:23:40Z), "Lane A live" split into (a) SB CODE DEPLOYED
(TRUE now) vs (b) SMS ACTUALLY SENDABLE (FALSE — 0 origination identities, `sms.ts` fails closed, SP-1 held).
Flipping `available:true` on (a) — or on "F3a + verify path" — while (b) is false lets a user select sms and
wait on a code that never sends: the cheerful-lockout the whole leg exists to prevent.
- **CORRECTED SF-1 GATE: `available:true` (and SF-2's card visibility) gate on A TEST SMS ACTUALLY DELIVERED**
  — on the S5 downstream oracle (End User Messaging config set → CloudWatch Logs event destination,
  per-message by MessageId). ⛔ NOT "code deployed," NOT "SP-1 provisioned," NOT "F3a + verify path" alone —
  a configured-but-broken identity FAILS it. **The gate is a CAPABILITY (CAN SEND), not a code property**
  (a deployed sha establishes NOT-ACT-C, never CAN-SEND). `0.4.0_DE_ClientPlatform~Z` encodes it client-side;
  `3.0.0_SA_CVO~Z` scores it. This supersedes Amendment 3's SF-1 gate wording.

## REPORTING
Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; certification `3.0.0_SA_CVO~Z`. Surprise items
→ `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`), one line, keep working. Push state MEASURED — is-ancestor
predicate for ON-ORIGIN, vintage-stamped for LOCAL-ahead (CVO~Z 18806). The client double-submit-guards
question (put to `1.0.0_SA_CTO~Z`) is SEPARATE from this TO and not a dependency.
