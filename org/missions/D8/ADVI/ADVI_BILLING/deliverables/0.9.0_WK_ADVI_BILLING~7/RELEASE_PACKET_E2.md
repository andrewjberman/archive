# RELEASE_PACKET_E2 -- copy_site_file_to_s3 on the Opal gateway

For: the gateway's owners (NFRA_OPLGTW, site Z). From: 0.9.0_WK_ADVI_BILLING~7, ADVI_BILLING.TO-AB-r-3.
State: PREPARED. Nothing is deployed, nothing is applied, no S3 object was written. Push state: LOCAL on branch wk-ADVI_BILLING-7 until the drain.

## 1. What ships (one new write tool, one grant, one env line)

| Piece | Where | Status |
|---|---|---|
| Module `copy_site_file_to_s3(user_token, site_id, item_id, quarter)` | `infra/aws/ec2/opal-gateway/app/integrations/advi_billing/site_to_s3.py` | built round 2, not registered |
| Tool registration, refusals as `{"error", "refused": true}` | `infra/aws/ec2/opal-gateway/app/tools.py` (`copy_site_file_to_s3`, after `upload_text_to_site`) | done this cell |
| IAM grant | `infra/aws/terraform/opal-gateway/advi_billing_gateway_iam.tf` (`aws_iam_role_policy.advi_billing_gateway_put`, policy name `gateway-49f-advi-billing-put-policy`) | written, planned, not applied |
| Env line | see section 3 | owners' edit |
| Classification of the tool | see section 2, REQUIRED CARRY | NOT done, outside this cell's grant |

## 2. Commits to carry, and the one REQUIRED CARRY that is missing

Cut the release on the host's running ref plus these commits (cherry-pick or merge in this order):

1. `931774fb11` -- round 2: `site_to_s3.py` and `tests/test_advi_site_to_s3.py`.
2. `e8290dd5fe` -- this cell: tool registration, `tests/test_advi_site_to_s3_registration.py`, `advi_billing_gateway_iam.tf`, `AB_R3_PLAN.txt`.

**REQUIRED CARRY (row ADVI_BILLING-D2-W7-S1, BLOCKING, hazard INERT).** The gateway fail-closes any tool that `app/destructive_ops.py` does not classify. As released with only the two commits above, a call to `copy_site_file_to_s3` returns `confirm_required` (blast_cap) and `write_class` is `UNCLASSIFIED`, which no tier is entitled to. It is listed and it is NOT safe (that is what AB3-3-AC1 measures) but it cannot complete. Before the cut, a cell whose grant names these two files must add:

- `app/destructive_ops.py`: a `DESTRUCTIVE_OPS["copy_site_file_to_s3"]` entry (class `WRITE_REVERSIBLE`; native undo = delete the written key; conditional put so it never overwrites; `blast_dimensions: ["files:1"]`) and `TOOL_WRITE_CLASS["copy_site_file_to_s3"] = "write_files"` (the same class `upload_text_to_site` and `save_email_attachment_to_site` carry).
- `app/data_entitlement.py`: the name in `NATIVE_TOOLS`.

Do not ship the two commits without it and expect the post-deploy proof in section 6 to pass.

## 3. Config: where the gateway reads env, and the line

- The gateway READS env from `/opt/opal-gateway/.env` (`infra/aws/ec2/opal-gateway/deploy/opal-gateway.service` line 10, `EnvironmentFile=`).
- That file is WRITTEN, whole, on every deploy by the single `printf ... | sudo -u ec2-user tee ${REMOTE_DIR}/.env` at `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` line 417. A line added by hand on the host is erased by the next deploy. Nothing under `deploy/` carries env values, and `deploy-to-ec2.sh` is outside this cell's grant, so it was not edited (row ADVI_BILLING-D2-W7-S2).
- The line to add (the value is the builder's address for the table with no partition; it is not a secret):

```
ADVI_FEE_STATEMENT_S3_ROOT=s3://opal-data-assets/smartx/49financial/bronze/fee_statement/
```

Diff for `deploy-to-ec2.sh` line 417: add `ADVI_FEE_STATEMENT_S3_ROOT=%s\n` to the printf format string and one trailing argument `"${ADVI_FEE_STATEMENT_S3_ROOT}"`. Compute the value on the deploying workstation from the builder, never typed:

```
ADVI_FEE_STATEMENT_S3_ROOT="$(python -c 'from lib.opal_naming import address; a=address("smartx","49financial","bronze","fee_statement","quarter=X"); print(a[:-len("quarter=X")])')"
```

The module refuses (fail closed, before any Graph read) when this variable is unset or is not shaped like a `.../bronze/fee_statement/` root.

## 4. IAM grant and the plan

`advi_billing_gateway_iam.tf` adds ONE inline policy on the gateway instance role: `s3:PutObject` on `arn:aws:s3:::<bronze home>/smartx/49financial/bronze/fee_statement/*`. No Get, List, Delete, other prefix or other bucket. The bucket is read at plan time from the registry tier-home rule (`infra/logic/registry/tiers.json`, FIRM bronze) and the scope from the `opal_name` module, because HCL cannot call `address()` (row ADVI_BILLING-D2-W7-S4); `test_tf_prefix_equals_builder_address` pins that join to `address()` output.

Cross-firm deny check (`mcpmsp_gateway_firm_deny.tf`): its `DenyFirmSegments` statement denies `s3:GetObject` only, on `platinum/mdpf/<firm>/*` in the served bucket. This grant is `s3:PutObject` on a bronze key in a different bucket, so the deny's action and resource both miss it: no block, and no weakening.

Plan: `AB_R3_PLAN.txt` in this folder -- `Plan: 1 to add, 0 to change, 0 to destroy`, only `aws_iam_role_policy.advi_billing_gateway_put`. CAVEAT (row ADVI_BILLING-D2-W7-S3): that is a `-target` plan. A whole-root plan fails at refresh on the preparing device (AccessDenied reads, one missing secret, an external build that needs the deployed commit), so drift elsewhere in the root is UNMEASURED. Before apply, run the whole-root plan with the owners' credentials and the deployed commit and confirm it adds exactly this one resource.

## 5. Blast radius and rollback

- Blast radius: ONE new write tool (one conditional put of one `.xlsx` of at most 50 MiB per call, to `quarter=<q>/` under the one prefix, never an overwrite); ONE `s3:PutObject` grant on that prefix; ONE env line. The caller's own delegated Graph token reads the SharePoint item; the gateway role writes only the prefix.
- Rollback, in order: (a) redeploy the prior ref (the host's running ref recorded at the cut; `DEPLOY_BASE_REF` is that ref), which removes the tool and, with the env line gone from the printf, the variable; (b) destroy the one policy: `terraform destroy -target=aws_iam_role_policy.advi_billing_gateway_put` (or remove the `.tf` and apply). The tool without the grant fails closed at S3 with AccessDenied and writes nothing. Objects already written are removable by key (`aws s3 rm` of that one key); none is overwritten, so no prior object is lost.

## 6. DEPLOY_BASE_REF rule

`deploy-to-ec2.sh` (STALE-BASE GUARD, lines 99-165) refuses an upload unless `DEPLOY_BASE_REF` equals the live ref it reads from the artifact plane at the moment of upload. Cut this release on the host's RUNNING ref plus the commits in section 2, and export `DEPLOY_BASE_REF=<that running ref>` to `infra/aws/ec2/safe-ec2-deploy.sh`. Read the running ref at the cut; if another seat ships in between, re-cut on the new ref -- do not declare a ref the release does not carry. The running ref is not recorded here: it moves, and this cell did not read the artifact plane.

## 7. Post-deploy proof (all three)

1. Tool listed: the gateway's MCP tool list includes `copy_site_file_to_s3`, and it is absent from the read-only set.
2. One refused call on a bad quarter: `copy_site_file_to_s3(site_id=<any>, item_id=<any>, quarter="2026Q9")` returns `{"error": ..., "refused": true}` and writes nothing (needs the section 2 classification, or the call stops at the guard first).
3. The env line equals `address()`: the `.env` key `ADVI_FEE_STATEMENT_S3_ROOT` (key NAMES are announced by the deploy's `ENV_KEYS_AFTER`; read the value on the host) equals `address("smartx","49financial","bronze","fee_statement","quarter=X")` with `quarter=X` removed.
