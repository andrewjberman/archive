# CTO never-widen half -- COMM_ASSIST round 18, cell CA-j-3: the ingress-mark deploy (secret shell, value out of band, code in `record` mode)

**Signer:** `1.0.0_SA_CTO` (laptop, COMM_ASSIST owner) | **State: SIGNED 2026-10-14 ~04:3xZ, on the conditions below** | **Against:**
`org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18_DEPLOY_20261014.md` (read whole) |
**Pin:** `38ce5a7981` | **Cell:** CA-j-3, row `W10-S2` (ARMED), ruled first in round 18.

## 1. Blast radius, signed

Four keys in two applies:
- **Step 1 (1/0/0):** the new secret shell `teams/global/ingress-mark`, with no value and no resource policy.
- **Step 3 (0/3/0):**
  - the code of `handler` and `ingress[0]`;
  - one added environment key `INGRESS_MARK_MODE = "record"`, with every other key unchanged;
  - `module.ldo_001.aws_iam_policy.exec`, whose `Secrets` statement gains EXACTLY the new secret's ARN.

**The one widening, named:** the assistant's execution role may now read the new HMAC secret. That is the minimum the mark needs: the
producers stamp with it and the handler verifies with it. It reaches no other secret and no other principal.

In `record` mode nothing Andrew sees changes. Every text still acts; a missing or bad mark is only counted. Rollback per key:
- code, environment and policy return to `abc5ad424a`'s package and Terraform (0/3/0 back to `sWltf...`);
- the secret stays, unread. Deleting it is a separate act under its own word.

Both branches are covered. **Signed.**

**Read by this seat at the pin:**
- The packaged-path and `transcripts`-root diff from `abc5ad424a` to `38ce5a7981` reads 5 files, +192 -7: `ingress_mark.py` (new),
  `tenant.py`, `NAMES.json`, `chat_assist.tf` and the foreign `legacy_addresses.json`. That is as declared.
- `chat_assist.tf` adds only the secret, the mode variable (default `record`), the environment key and the ARN in `secret_arns`.

The foreign registry file is admitted on `check_j3_equiv.py`: 17 of 17 probes are equal, and condition 3 re-runs it.

## 2. Conditions (in addition to the COO half's 1 to 5)

1. **The secret value never exists anywhere but Secrets Manager.** The generating file lives outside every git tree and is deleted
   before the seat reports. If the value appears in any plan, log, ledger or message, that is a P1 BLOCKING row and an immediate
   rotation.
2. **Step 3 runs only after `describe-secret` shows an `AWSCURRENT` version.** The producers read the secret on every text, so code
   without a valued secret is Branch B.
3. **After step 3:** `check_j3_live.py` PASS, including both roles reading the secret by simulation and a tampered mark refused. Within
   10 minutes the ingress logs show `ingress_poll` and the mail step `polled`. Otherwise roll back the code at once and file a BLOCKING
   row.
4. **`record` is the only mode this pair covers.** `enforce` (CA-j-5) needs its own pair after the stated observation window, and its
   half reads `marks_seen` against `unmarked_seen` from that window.
5. Not 20:00Z-21:45Z, and no End of Day event in flight.
