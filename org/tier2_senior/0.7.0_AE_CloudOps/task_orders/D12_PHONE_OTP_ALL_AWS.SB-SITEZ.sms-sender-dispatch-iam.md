# TO D12_PHONE_OTP_ALL_AWS.SB-SITEZ — SMS sender + dispatch + IAM (all-AWS)

<task_order id="D12_PHONE_OTP_ALL_AWS.SB-SITEZ" project="D12_PHONE_OTP_ALL_AWS">
<issued_to>0.7.0_AE_CloudOps~Z</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-09-01T14:xxZ</issued>
<status>ISSUED — the BUILD limbs (SB-1..SB-4, SB-5 authored) launch NOW against the pending identity. SB-5 APPLY and any real send are GATED — see §GATES.</status>
<priority>P1 — parallel with SF-SITEZ; the long-pole provisioning (SP-1, Andrew-gated) starts separately and blocks only the outward send.</priority>
<authority>
Andrew-direct 2026-09-01 (CTO~Z terminal): "lets push for all AWS" -> "Authorized, go ahead",
preceded by "I'd prefer to operate this entirely out of AWS." BUILD LEG AUTHORIZED. Decomp:
`org/tier1_exec/2.0.0_SA_COO/deliverables/laneZ_DECOMP_20260901_D12_PHONE_OTP_ALL_AWS.md` @`71c743405a`.
PRD: `1.0.0_SA_CTO~Z` @`65f7a59396`.
</authority>
<proof_of_spec>
  <expected_criteria>SB-1,SB-2,SB-3,SB-4,SB-5,SB-6,SB-7,SB-8</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D12_PHONE_OTP_ALL_AWS.SB_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>
</task_order>

## SCOPE — you hold this project and this project only (Rule 27)
Your `PLATFORM_OPS_USERMGMT` faces (W1/W2/W3) are CLOSED as of this seating. This is a SIBLING project.

## THE ATOMS (full detail in the decomp; source anchors are RELAYED from the PRD — CONFIRM at source)
| id | must observe |
|---|---|
| **SB-1** | `sendMfaCodeSms(phoneE164, code, ttlMin)` via `@aws-sdk/client-pinpoint-sms-voice-v2` `SendTextMessageCommand` (`OriginationIdentity`=TFN ARN, `MessageType:'TRANSACTIONAL'`), mirroring `email.ts sendMfaCodeEmail`. Unit-exercised against the SANDBOX on a VERIFIED destination only; returns a message id; the code ASSERTS verified-only so a future sandbox exit does not silently open sends. |
| **SB-2** | `resendMfaCode` (`auth.ts:223`): after `sendChallengeCode` (already charges the channel-agnostic budget), branch on `user.mfaChannel` — email→`sendMfaCodeEmail`, sms→`sendMfaCodeSms(user.phoneNumber, issued.code, TTL)`. ⛔ **Act C parity: ONE sealed code per challenge across N resends, never rotated** — on SMS as on email. |
| **SB-3** | `login()` sms-branch: replace the current `503` — if `user.phoneNumber` present, `issueChallenge(channel:'sms')`, return `{mfaRequired, challengeId, channel:'sms'}`, **send NOTHING** (Act B parity). Keep `503` only for sms-selected-but-no-number. Evidence: a CloudWatch check shows challenge issued and NO send at credential time. |
| **SB-4** | parameterize the hardcoded `channel:'email'` in the `issueChallenge` log (cosmetic); the field reflects the real channel, no other behavior change. |
| **SB-5** | IAM: add `sms-voice:SendTextMessage` to the auth-handler role, ⛔ **RESOURCE-SCOPED to the origination-identity ARN — NOT a blanket Allow. Do NOT repeat F-1** (the unconditioned `ses:SendEmail`). Terraform + `safe-apply` (never bare). Terraform AUTHORED now; **APPLY gated on the TFN ARN existing (SP-1).** |

## GATES
⛔ **NO SMS to a real (unverified) user until: SP-1 TFN verified · SP-2 sandbox exited or the number verified · Andrew's go.** The sandbox enforces verified-destinations-only; SB-1 asserts it in code too.
⛔ **SB-5 APPLY waits on the TFN ARN.** Author the Terraform now; do not apply an IAM grant scoped to an ARN that does not exist. No monitor/alarm on this surface (moratorium).

## ⛔ AMENDMENT 1 — CTO~Z acceptance contract (18859, adopting CVO~Z 18845). These REFINE the atoms above and are BINDING.
⛔ **CHANNEL IS SERVER-AUTHORITATIVE AND BOUND AT ISSUE — measured gap: the challenge row does NOT persist
a channel today (`mfa.ts:245` hardcodes `'email'`; the challenge Item has no channel field).** So:
- **SB-4 (widened):** (a) PERSIST `channel` on the challenge row at `issueChallenge`, set from
  `user.mfaChannel` (passed by `login()`) — exactly as the RECIPIENT is bound today ("the challenge names
  its own recipient; the caller does not"). (b) The existing events (`mfa_code_sent`, `mfa_send_refused`,
  `mfa_challenge_issued`) carry a **`channel` PARAMETER** — ⛔ **NEVER a new event name (`mfa_sms_sent`).
  HARD-FAIL criterion (Rule 24: channel is a dimension, not a new type)** — a new name silently under-counts
  every `mfa_code_sent` census and voids CVO~Z's certified Act-C rubrics.
- **SB-2 (corrected):** `resendMfaCode` dispatches on the **CHALLENGE's** stored channel, NOT re-derived
  from the caller or re-read from `user` at resend time. ⛔ Deriving the channel from the caller is F-1's
  unconditioned-choice lesson on the APPLICATION plane (an SMS demanded for a phone-less account; per-channel
  budget bypassed by channel-switching). A mid-flight `email→sms` preference change must NOT switch an
  in-flight challenge's channel — it is bound at issue.
- **SB-3:** the `login()` response's `channel` = `user.mfaChannel` (`email|sms`) so `0.4.0_DE_ClientPlatform~Z`'s
  per-channel "we texted/emailed you" copy is correct. Act B parity unchanged (issue, send NOTHING).
- **BUDGET:** per-challenge `MAX_SENDS` is UNCHANGED (the accepted bound: N logins = N challenges = N×budget).
  SMS makes the worst case partly billable → the dollar backstop is the AWS **spend cap (SP-2, a SECURITY
  parameter, held at CTO~Z)**, not app logic. Named edge (backstopped, not hidden): a mid-flight `email→sms`
  change can leave one email + one sms live challenge = 2×MAX_SENDS, half billable.
⭐ **CVO~Z's Act B/C rubrics (`ef3ec6f019`, `57dd460e6c`) TRANSFER unchanged; only the oracle binding moves,
and SB-4(b) keeps it stable. CVO~Z pre-registers the SMS criteria to CTO~Z for review BEFORE your code exists.**

## ⛔ AMENDMENT 2 — SB-6 SERVER GUARD (CVO~Z 18909, CORRECTED by AE~Z 18919 + MSTR~Z 18914; BINDING)
⛔ **THE LOOSE GUARD (CVO~Z, confirmed verbatim by AE~Z at source): `updateMfaPreference(email,'sms')` with
no `phoneNumber` passes both guards today — enum + format-IF-supplied. Nothing checks a number EXISTS, let
alone that it is VERIFIED.**
⛔ **CHAIN CORRECTED: CVO~Z's silent-lockout chain measured the tree BEFORE SB-3 committed. SB-3 as committed
(`8fd0ae2810`) requires `user.mfaChannel==='sms' && user.phoneNumber` before issuing — so a no-number sms
user gets a LOUD 503 at login (naming support), NOT a silent 200-no-text.** ✅ CVO~Z's core conclusion
stands: Amendment 1 makes the loose guard LOAD-BEARING; the committed consequence is a hard 503, not a
silent lockout.
⚠ **RESIDUAL that DOES survive (AE~Z §3, narrower): sms+number user logs in (channel frozen 'sms') → the
number is REMOVED while the challenge is live → resend reads the row 'sms', finds no number → SILENT refuse
(the route must not be an account probe) → 200, no text, until the challenge TTLs (≤10 min, self-healing;
fresh login then 503s).** Real, bounded, worth closing.
✅ **REACHABILITY (MSTR~Z 18914): NOT reachable today — the UI ships sms `available:false` and NO sender
exists in the deployed handler. A BUILD-TIME finding, not a live exposure; Andrew + aj@ cannot reach it.
NOT a reason to soften it.**
- **SB-6 — COMMISSIONED (AE~Z's requested "say the word"): `updateMfaPreference` MUST REJECT
  `mfaChannel='sms'` unless a phone number is SUPPLIED in the same call OR ALREADY STORED on the record.**
  ~3 lines, AE~Z's lane. ⛔ A UI cannot satisfy this — **F3 is a SERVER refusal; routing it to SF-2 UI is
  D12's original defect shape (a client enforcing what the server did not).** Acceptance exhibits a DIRECT
  API call requesting sms with no number and the SERVER REFUSING it (a guard with no exhibited refusing
  input is untested).
- ⚠ **SB-6 is only the "a number EXISTS" half. The "a number is VERIFIED" half is JOINT** — verification
  state has no home in the user record today; SF-2 adds the field and the server checks it. **F1** (unverified
  number never stored): oracle = the USER RECORD read directly, BRACKETED before/after (never a client/handler
  self-report).
- ⛔ **DEADLINE (MSTR~Z): SB-6 MUST BIND BEFORE SF-1 flips sms `available:true` — not before ship, before
  that ONE LINE.** `0.4.0_DE_ClientPlatform~Z`: treat `available:true` as gated on SB-6 + SF-2's verify path,
  and SAY SO on the SF row rather than holding it in your head.
- `1.0.0_SA_CTO~Z` rules the exact error shape / enforcement points; the INVARIANT (refuse it) is not in dispute.

## ⛔ AMENDMENT 3 — SB-7/SB-8 ENROLMENT-VERIFICATION BACKEND (DE~Z 18934 finding; UNBLOCKS SF-2; BINDING)
⛔ **DECOMP GAP (DE~Z, correct — my miss): SB-1..SB-6 build the LOGIN-challenge SMS path + the preference
guard. NONE builds the ENROLMENT-VERIFICATION round-trip SF-2 depends on** ("collect E.164, SEND A TEST
CODE, CONFIRM, store"). SF-2 has nothing to CALL until these exist, so it is BLOCKED, not merely un-enabled.
- **SB-7 (enrolment send-code-to-candidate):** an endpoint that sends an SMS OTP to a CANDIDATE number that
  is NOT yet the account's stored preference. ⛔ Cannot reuse SB-2 resend (it dispatches on the STORED
  challenge, and storing the number first to trigger it would violate F1). Reuses `sendMfaCodeSms` (SB-1)
  for delivery. Acceptance: sends a code to a candidate number WITHOUT mutating the account's stored
  channel/number.
- **SB-8 (enrolment verify-and-mark + the F3b field):** verifies the entered code against the enrolment
  challenge and, on success, stores the number + MARKS IT VERIFIED (writes the F3b verified-state field on
  the `opal-users-v2` record). ⛔ Distinct from `verifyAndConsumeChallenge` (that consumes a LOGIN
  challenge; marking a NUMBER verified at enrolment is a different act). Acceptance: only a correctly-verified
  number is stored+marked; F1 holds (an unverified number is never stored), oracle = the user record bracketed.
- ⛔ **NO SHADOW SYSTEM (Andrew veto): EXTEND the existing challenge mechanism with a PURPOSE parameter
  (`login|enrolment`), not a parallel challenge store.** `1.0.0_SA_CTO~Z` rules the design; `0.7.0_AE_CloudOps~Z`
  builds; ⛔ **AE~Z + DE~Z AGREE THE ENDPOINT CONTRACT (paths, request/response) BEFORE DE~Z builds SF-2's
  client** — DE~Z is blocked until the contract is named, and rightly holds SF-2 rather than build against
  presumed endpoints.
- **F3b lane precision (DE~Z, adopted): DE-CALLS / AE-WRITES** — SF-2 DRIVES the verify (calls SB-8); the
  field and the record write are AE~Z's plane. SF-2 (UI) never writes `opal-users-v2` (Rule 13).

## REPORTING
Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; certification `3.0.0_SA_CVO~Z`. Surprise items
→ `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`), one line, keep working. Push state MEASURED — is-ancestor
predicate for ON-ORIGIN, vintage-stamped for LOCAL-ahead (CVO~Z 18806). Commit via `safe-commit -F`,
non-shell writer; `.py`/`.ts` through the gates.
