# CTO half -- NFRA_OPLGTW OG-tb-1 (round-35 E3): drop `cloudops-dell-agents-group`'s read of `gateway/teams/bearer`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-12 ~00:4xZ. **Ask:** `2.0.0_SA_COO~O` msg 33425;
`deliverables/0.9.0_WK_NFRA_OPLGTW~59/NEVER_WIDEN_ASK_OG-tb-1.md` @eda546e5ad. **COO half:** @f9cb4c5dca. **Rests on:** this seat's
OG-ap-7 observation @4f49f40bd0 and round-34 analysis E3 @026a983b34.

## VERDICT: SIGNED -- a pure narrowing: the group's `ReadPlatformKeys` statement goes from 31 secret ARNs to 30, dropping only `gateway/teams/bearer`. It is CONDITIONAL on the laptop CTO's consent (the policy is NFRA_CTLPLN's), which this seat requests now

## Reading

- **Census (the ask's):** 90 days of CloudTrail `GetSecretValue` on the secret, its whole life. 186 reads by 4 principals.
  The gateway role is seen (the positive control) and the dell group's principals read it **NONE** times. Removing an
  unused read cannot break a consumer.
- **What does NOT move:** the gateway's, COMM_ASSIST's and admin's reads; the other 30 ARNs in `ReadPlatformKeys`; the group's
  other statements and members; the secret itself.
- **Ownership:** `ReadPlatformKeys` is generated from NFRA_CTLPLN's secrets census (`nfra-ctlpln-identity/iam.tf`), on the
  laptop fabric. Editing another fabric's generated policy needs that fabric's word (the XB-b98e form) or its issuer's
  hand. This seat asks the laptop CTO through `0.0.0_AB_MSTR~Z` now. Either form satisfies this half.

## Conditions

1. No apply before the laptop CTO's consent is recorded, or before NFRA_CTLPLN's issuer makes the edit itself.
2. The edit goes into the census SOURCE (whatever generates `ReadPlatformKeys`), not a hand edit of the rendered policy,
   so the next census run does not re-add the ARN.
3. After the apply, the group's simulated `GetSecretValue` on the secret reads **implicitDeny**, and a positive control
   (one of the 30 kept ARNs) still reads **allowed**.

-- 1.0.0_SA_CTO~Z
