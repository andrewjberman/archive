# CTO never-widen half -- COMM_ASSIST round 17, cell CA-i-4: deploy the round-17 package (targeted apply of `module.ldo_001`)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~00:0xZ, on the conditions below** |
**Against:** `org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17_DEPLOY_20261014.md`
(read whole) | **Pin:** `b19849b51c` | **Order:** `COMM_ASSIST.TO-CA-i-4.round17-package-deploy.md`, `0.7.0_AE_CloudOps~CA`.

## 1. Blast radius, signed as written

There are two keys: `module.ldo_001.aws_lambda_function.handler` and `.ingress[0]`. Each gets new code, plus ONE added environment
key, `MUSE_ANSWER_PUBKEY`, a public key. Every existing key is unchanged (`MAIL_BEARER_SECRET`, `SMS_ORIGINATION` and the nine
`LDO_*`). No policy, secret, reader or other address moves.

Rollback per key: the saved live zip (`nIQW...`, 269,206 B) through the same targeted apply, with the pubkey variable at `""`.
Both branches are covered. **Signed.**

**Read by this seat at the pin, not taken from the packet:**
- The packaged-path diff `2fd32e12c2..b19849b51c` over the build's set reads **13 files, +1373 -48**, as stated.
- The round-17 files are four: `assist.py` +3/-1 (the `ldo-001` stamp), `mail_requests.py`, the new `muse_verify.py` (+182), and
  `tenant.py`.
- `build.sh` at the pin copies `handlers.py`, `ldo.py`, `teams_chat/`, the end-of-day pair, `lib/opal_naming.py`, the schema and the
  registry. That is the named set.

**The foreign files** (`lib/opal_naming.py` +724, eight registry files) are other projects' committed work riding the package. They
are admitted on the COO half's measured-effect check: 17 of 17 probes are equal between the built package and the zip the live
function serves (the bucket, the state, silver and bronze keys for five chat shapes, and the mail parties). Condition 2 below
re-runs it at the act.

**A wrong pubkey fails closed:** the receiver refuses every muse answer and acts on none. So the one new key cannot widen what can
answer in Andrew's place. muse answers stay impossible until the dell2 forwarder (CA-i-5) exists.

## 2. Conditions (in addition to the COO half's 1 to 4)

1. **The live pre-state must still read `nIQW...` on both functions at the act.** Another writer moving it is Branch B.
2. **`check_i4_equiv.py ok=True` is re-run by the applier, at the act, on the package it is about to upload.** Any probe unequal is
   Branch B. The foreign files are admitted only because they change nothing the assistant reads.
3. **After the act:** `check_i4_live.py` PASS, and within 10 minutes the ingress logs show `ingress_poll` and the mail step `polled`.
   Either missing means roll back at once and file a BLOCKING row.
4. The window rule stands: not 20:00Z-21:45Z, and no End of Day event in flight.
