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

## REPORTING
Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; certification `3.0.0_SA_CVO~Z`. Surprise items
→ `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`), one line, keep working. Push state MEASURED — is-ancestor
predicate for ON-ORIGIN, vintage-stamped for LOCAL-ahead (CVO~Z 18806). The client double-submit-guards
question (put to `1.0.0_SA_CTO~Z`) is SEPARATE from this TO and not a dependency.
