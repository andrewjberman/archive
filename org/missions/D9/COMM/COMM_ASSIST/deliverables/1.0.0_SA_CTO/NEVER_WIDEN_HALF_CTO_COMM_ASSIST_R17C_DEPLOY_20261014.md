# CTO never-widen half -- COMM_ASSIST round 17, cell CA-i-14: the signed-at time-bound deploy (code only, one file)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~02:1xZ** | **Against:**
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17C_DEPLOY_20261014.md` |
**Pin:** `abc5ad424a` | **Order:** `COMM_ASSIST.TO-CA-i-14.round17c-signed-at-bound-deploy.md` | **Closes:** the CVO's residual
`C-S6`.

## Blast radius, signed

Two keys: the code of `module.ldo_001.aws_lambda_function.handler` and of `.ingress[0]`. Expected plan `0/2/0`, with no
environment key and no `-var`. Rollback: the CA-i-12 package (pin `8a480805e5`) through the same targeted apply.

**Read by this seat at the pin:** the diff from `8a480805e5` to `abc5ad424a`, over the packaged set and the `transcripts` root, is
`teams_chat/tenant.py` +32 -6 and nothing else.

The change only NARROWS what a muse answer can do:
- `signed_at` must be a UTC timestamp;
- it must lie within 24 hours before and 5 minutes after the RECEIVER's own clock (`ctx.now()`), never the sender's envelope.

Otherwise the answer is refused as `stale-signature`. No answer that was refused before is accepted now. muse answers still cannot
arrive until CA-i-5.

## Conditions

1. The live pre-state equals the CA-i-12 package at its close. Any other hash is Branch B.
2. After the act: one new package on both functions, the served `tenant.py` equal to the pin's, a targeted re-plan with no change,
   and within 10 minutes `ingress_poll` and the mail step `polled`. Otherwise roll back to the CA-i-12 package and file a BLOCKING
   row.
3. Not 20:00Z-21:45Z, and no End of Day event in flight. The NEVER-2 entry is opened before the act and closed only on condition 2.
