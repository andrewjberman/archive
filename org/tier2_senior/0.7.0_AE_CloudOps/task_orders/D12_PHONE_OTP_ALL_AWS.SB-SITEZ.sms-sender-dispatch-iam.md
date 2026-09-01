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
  <expected_criteria>SB-1,SB-2,SB-3,SB-4,SB-5</expected_criteria>
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

## REPORTING
Validation `2.0.0_SA_COO~Z`; acceptance `1.0.0_SA_CTO~Z`; certification `3.0.0_SA_CVO~Z`. Surprise items
→ `3.0.0_SA_CVO~Z` (cc `0.0.0_AB_MSTR~Z`), one line, keep working. Push state MEASURED — is-ancestor
predicate for ON-ORIGIN, vintage-stamped for LOCAL-ahead (CVO~Z 18806). Commit via `safe-commit -F`,
non-shell writer; `.py`/`.ts` through the gates.
