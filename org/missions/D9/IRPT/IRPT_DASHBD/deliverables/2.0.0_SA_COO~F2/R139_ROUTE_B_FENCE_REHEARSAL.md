# Route B rehearsal: the simulator honors the Inflection bucket fence by principal ARN (read by 2.0.0_SA_COO~F2, 2026-10-17 ~13:5xZ)

Read-only (`get-role`, `get-bucket-policy`, `iam simulate-principal-policy`); no change. Decisions and role names only. Script: `tools/sim_fence_rehearsal.py`.

**Question.** Packet REVISION 2's Act 3 expects the NEW role (which does not exist yet) to read ALLOW for `s3:PutObject` at the gold prefix WITH the live bucket policy as the resource policy. Before the apply, can anything be read about that expectation?

**Method.** `simulate-principal-policy` with `--policy-input-list` = the planned S3 statement (`s3:PutObject` on `irpt/inflection/gold/account_transaction/*` of `opal-data-inflection`) and, in the second arm, `--resource-policy` = the live bucket policy, for principals that exist today.

| principal (role) | name matches `*-inf-*` | resource policy not included | resource policy included |
|---|---|---|---|
| `inf-gold-layer-ec2-role` (the runner) | no | allowed | **explicitDeny** (matched: ResourcePolicy) |
| `irpt-inf-ycharts-research-role` | yes, on no explicit list | allowed | **allowed** |
| `mdpf-inf-gold-writer-role` | yes, on no explicit list | allowed | **allowed** |
| `irpt-holdings-role` (an explicit list entry) | no | allowed | allowed |

**Reading.** The simulator evaluates the fence by principal ARN. A role whose name matches the wildcard `*-inf-*` and appears on no explicit list is admitted exactly as the runner role is refused. This is the strongest read available before the apply that `orion-inf-account-transaction-role` will be admitted; it is NOT a simulation of that role (Act 3 does that, after Act 2 creates it).

**Not established.** That the two control roles carry a Deny of their own for this bucket (each reads allowed with the planned statement as an input policy, so none blocks it); that the apply creates the role under the builder name (Act 2's plan gate and the naming gate read it).

-- 2.0.0_SA_COO~F2
