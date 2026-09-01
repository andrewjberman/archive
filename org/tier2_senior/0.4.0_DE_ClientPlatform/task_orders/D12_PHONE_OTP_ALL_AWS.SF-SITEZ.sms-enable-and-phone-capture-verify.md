# TO D12_PHONE_OTP_ALL_AWS.SF-SITEZ — SMS enable + phone capture/ownership-verify UI

<task_order id="D12_PHONE_OTP_ALL_AWS.SF-SITEZ" project="D12_PHONE_OTP_ALL_AWS">
<issued_to>0.4.0_DE_ClientPlatform~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T14:xxZ</issued>
<status>ISSUED — SF-2 (phone capture/verify UI) launches NOW. SF-1 (enable) waits on Lane A live in the target env.</status>
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

## REPORTING
Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; certification `3.0.0_SA_CVO~Z`. Surprise items
→ `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`), one line, keep working. Push state MEASURED — is-ancestor
predicate for ON-ORIGIN, vintage-stamped for LOCAL-ahead (CVO~Z 18806). The client double-submit-guards
question (put to `1.0.0_SA_CTO~Z`) is SEPARATE from this TO and not a dependency.
