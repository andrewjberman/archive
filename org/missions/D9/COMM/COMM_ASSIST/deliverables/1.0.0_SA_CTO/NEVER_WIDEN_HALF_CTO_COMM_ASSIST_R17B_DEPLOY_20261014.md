# CTO never-widen half -- COMM_ASSIST round 17, cell CA-i-12: the replay-fix deploy (code only, one file)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~01:1xZ** | **Against:**
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17B_DEPLOY_20261014.md` |
**Pin:** `8a480805e5` | **Order:** `COMM_ASSIST.TO-CA-i-12.round17b-replay-fix-deploy.md` | **Closes:** the CVO's carried row
`COMM_ASSIST-C-S5` (a replayed signed answer).

## Blast radius, signed

Two keys: the code of `module.ldo_001.aws_lambda_function.handler` and of `.ingress[0]`. Expected plan `0/2/0`, with no
environment key and no `-var`. Rollback: the CA-i-4 package (pin `b19849b51c`, now live) through the same targeted apply.

**Read by this seat at the pin:** the diff from `b19849b51c` to `8a480805e5`, over the packaged set and the `transcripts` root, is
`teams_chat/tenant.py` +32 -6 and nothing else.

The change only NARROWS what a muse answer can do:
- the same signed bytes act at most once (a sha256 of payload and signature is recorded when the answer moves a draft; the last
  200 are kept);
- a chat draft's answer must carry that draft's `seq`;
- `version` is now required as a whole number on every action.

No answer that was refused before is accepted now. muse answers cannot arrive until CA-i-5 (the forwarder), so nothing in today's
text path changes.

## Conditions

1. The live pre-state equals the CA-i-4 package recorded at its close (ledger @4df21cf33f). Any other hash is Branch B.
2. After the act: one new package on both functions, the served `tenant.py` equal to the pin's, a targeted re-plan with no change,
   and within 10 minutes `ingress_poll` and the mail step `polled` in the logs. Otherwise roll back to the CA-i-4 package and file
   a BLOCKING row.
3. Not 20:00Z-21:45Z, and no End of Day event in flight. The NEVER-2 ledger entry is opened before the act and closed only on
   condition 2.
