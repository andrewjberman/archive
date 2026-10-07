# Plan note: the three scoped rows, what each bucket's plan shows, and the landing order

Author: 0.9.0_WK_NFRA_CTLPLN~6, NFRA_CTLPLN.TO-CT-d-2 AMENDMENT 4, 2026-10-07. For `1.0.0_SA_CTO`'s half and for `4.0.0_SA_CRO`, who writes the rows.
This build adds no registry row and edits no registry file. Everything below that says "would" is read from a standalone render in a
temporary root outside the repository (no provider, no backend, no AWS), produced by `infra/aws/terraform/shared-infra/tests/check_fence_scoped_rows.py`
and by a one-off script over the same functions. No `terraform plan` was run against the backend.

## 1. The three rows, exactly as the registry's lane would write them

One row appended under each bucket key in `infra/logic/registry/exemptions.json`, after that bucket's last row; no existing row, key or
field changes; none under `opal-data-bd`, `opal-data-inf` or `opal-data-cot`; none for `cloudops-dell2-agent-user`. The `signoff_ref`
paths are proposed names following the dell2 rows' pattern; the issuer fixes them.

Under `opal-data-49financial`:

```json
{
  "principal": "cloudops-dell1-agent-user",
  "arn": "arn:aws:iam::313476888478:user/cloudops-dell1-agent-user",
  "reason": "The dell1 box's agent identity; reads irpt/49financial/platinum/holdings/* in opal-data-49financial and nothing else: s3:GetObject, s3:ListBucket and s3:GetBucketLocation only (its own policy allows put on opal-*, so this row carries the scope); NFRA_CTLPLN CT-d-2 AMENDMENT 3-4; CTO msg 106185 and 106230.",
  "signoff_ref": "org/critical_paths/change_management/ entry slug nfra-ctlpln-dell1-fence-join-scoped-laptop-20261007 (opened at the apply); COO half org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_FENCE_JOIN_SCOPED_20261007.md; CTO half org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL1_FENCE_JOIN_SCOPED_20261007.md",
  "actions": ["s3:GetObject", "s3:ListBucket", "s3:GetBucketLocation"],
  "prefix": "irpt/49financial/platinum/holdings/"
}
```

Under `opal-data-cottonwood`: the same row with `"prefix": "irpt/cottonwood/platinum/holdings/"` and the bucket name `opal-data-cottonwood`
and prefix `irpt/cottonwood/platinum/holdings/*` in `reason`.

Under `opal-data-inflection`: the same row with `"prefix": "irpt/inflection/platinum/holdings/"` and the bucket name `opal-data-inflection`
and prefix `irpt/inflection/platinum/holdings/*` in `reason`.

The validator (`python lib/opal_naming.py validate`) accepts a registry carrying the three rows (0 refusals, measured on a scratch copy;
the check prints the three rows in full). The prefix's second segment is the firm token of the bucket, read from `scopes.json`; a row
carrying another firm's token is refused.

## 2. What each bucket's plan would show once the rows land

Today's render and the render with the three rows were compared, per bucket (policy as the fence file builds it, JSON-decoded):

| Terraform address | Admitted list in `DenyForeignFirmPrincipals` | `Statement` |
|---|---|---|
| `aws_s3_bucket_policy.opal_data_49financial` | 20 -> 21 entries, the one added is the dell1 ARN | 4 -> 7: the fence statement changes in place, plus `DenyScopedExemption1AnyOtherAction`, `DenyScopedExemption1ObjectsOutsidePrefix`, `DenyScopedExemption1ListingOutsidePrefix` |
| `aws_s3_bucket_policy.lgic_firm["cottonwood"]` | 6 -> 7, the dell1 ARN | 4 -> 7: same three statements added (the 4 today are the fence and the three restricted-prefix statements) |
| `aws_s3_bucket_policy.lgic_firm["inflection"]` | 6 -> 7, the dell1 ARN | 1 -> 4: same three statements added |

Each is one `aws_s3_bucket_policy` updated in place (`~ policy`); no resource is added or destroyed; no other statement of any policy changes.
Rendered policy size: 2,536 -> 3,577 bytes (49financial), 1,772 -> 2,807 (cottonwood), 560 -> 1,595 (inflection), far under the 20,480-byte limit.
A reviewer should reject any plan showing the dell1 ARN in a `DenyForeignFirmPrincipals` list without the three `DenyScopedExemption1...`
statements beside it. Caveat: the render is of the Terraform's own expressions with resource and data references stubbed; a real plan
compares against the live policy and may also show a drift entry that is not from this change (the census's saved documents predate the
dell2 applies), and the render knows nothing of the live state of the three restricted-prefix statements.

What the statements do, proven with the simulator on each bucket's saved policy plus the rendered admitted list and statements (27 of 27
arms matched, plus 3 plain-admission controls): dell1 `GetObject` under the prefix allowed; outside it explicitDeny; `PutObject` under the prefix
explicitDeny; `ListBucket` with the prefix allowed; `ListBucket` with no `s3:prefix` at all explicitDeny, and with the empty string explicitDeny
(a `StringNotLike` on an absent key is true in IAM, so the Deny applies); `GetBucketLocation` allowed; `GetObjectVersion` under the prefix
explicitDeny; dell2 (an unscoped row) `GetObject` outside the prefix still allowed. The same document without the three statements allows the
no-prefix list, the empty-prefix list and the put (controls), so the refusals are the statements' doing. The simulator does not derive
`s3:prefix` from a real list request, evaluates no organization policy and reads no object; the post-apply read-back (get under the prefix
succeeds; get outside and a put are refused) is the live test.

## 3. Landing order (the CTO's ruling, msg 106230)

1. This build first: the validator refuses an unknown key (`lib/opal_naming.py`), the module refuses one at plan time (`modules/opal_name/main.tf`
   output preconditions) and renders `fence_scoped_statements`, and the two fence files append it. With today's registry the rendered
   bucket policies are byte-identical to before (sha256 per policy printed by the check), so landing it changes nothing in AWS.
2. Only then `4.0.0_SA_CRO` writes the three rows (this note and `PROPOSAL_FENCE_ROW_SHAPE_READ_ONLY_PREFIX.md` are what to send it).
   A reader that still ignores an unknown key is `check_dell_fence_join.py` (a test; row `NFRA_CTLPLN-W6-S6`); it renders nothing into a policy.
3. The three rows move the registry hash. `generated_locals.tf`, `tests/vectors.json` and `tests/opal_name.tftest.hcl` already carry a stale
   mark since the dell2 rows (row `NFRA_CTLPLN-W6-S4`); their bodies are unchanged by this build and the generator was not changed, so the
   registry lane's restamp (`python lib/opal_naming.py generate --out <dir> --target ...`) is a mark-only change for all three, today and after the rows.
4. One laptop apply under its pair, then the read-back above. `check_dell_fence_join.py` pins the two fence files to commit `3ec42c56bf`; the
   issuer moves that pin at the merge, as the order states.
5. GetBucketLocation is in the set (CTO: yes); GetObjectVersion and ListBucketVersions are not (CTO: no): a row naming either is refused by the validator and the module.
