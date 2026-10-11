# Never-widen ask -- OG-mu-1, the gateway's market_update writer (rows W49-S3, W49-S4 route (a))

By: `0.9.0_WK_NFRA_OPLGTW~55`, Phase A. Halves owed: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`.
Nothing here is applied, planned against AWS, deployed or released. Code and tests are on branch `wk-NFRA_OPLGTW-55`
(the commit is named in the worker report). Blast radius of the whole ask: ONE new S3 key per accepted `.pptx` call,
under ONE prefix, in ONE bucket, by ONE role.

## 1. The diff by file

| file | change |
|---|---|
| `infra/aws/ec2/opal-gateway/app/integrations/advi_billing/site_to_s3.py` | `.pptx` pair only: key = `<root>date=<UTC date of the put>/deck_<sha256[:16]>.pptx` (intake's form); sanitized original name in `Metadata["original-name"]`; new optional `now` argument (test injection). The `.xlsx` pair is untouched. The conditional put (`IfNoneMatch="*"`) stays. |
| `infra/aws/ec2/opal-gateway/tests/test_og_mu1.py` | new; `test_ogmu1_ac01..03`, offline. |
| `infra/aws/terraform/opal-gateway/variables.tf` | new; REQUIRED `variable "market_update_s3_root"` (no default), validated to be `s3://...` ending `/bronze/market_update/`, no `..`. |
| `infra/aws/terraform/opal-gateway/advi_billing_gateway_iam.tf` | appended: `module.market_update_policy_name` (name only) and `aws_iam_role_policy.market_update_gateway_put` on `aws_iam_role.gw`. |

## 2. The one statement

```
Sid      = "OplgtwPutMarketUpdateBronzeOnly"
Effect   = "Allow"
Action   = ["s3:PutObject"]
Resource = ["arn:aws:s3:::${substr(var.market_update_s3_root, 5, -1)}*"]
```

Fed `-var market_update_s3_root=<address() output>` (the same call the deploy uses for `ADVI_MARKET_UPDATE_S3_ROOT`), it
resolves to `arn:aws:s3:::opal-data-transcripts/sharepoint/transcripts/bronze/market_update/*` (measured offline from
`lib/opal_naming.address`). No Get, List or Delete; no other prefix or bucket. No bucket or prefix literal is typed in HCL.
The new inline policy is separate from `advi_billing_gateway_put`, so it is removable alone.

## 3. Both branches of a call

| | refused | admitted |
|---|---|---|
| what runs | extension outside the two pairs, bad partition grammar, item not `.pptx`, bytes not a zip, empty/oversize, unset or mis-shaped root, or the key already exists (S3 412 on `IfNoneMatch`) | a `.pptx` zip within the size bound, root set, key absent |
| what is written | nothing | exactly ONE new object: `.../bronze/market_update/date=<UTC>/deck_<sha16>.pptx` (+ Metadata `original-name`) |
| overwrite | never (conditional put) | never |

The same bytes put again on the same UTC date are REFUSED as existing, the same outcome whether the first writer was this
tool or intake (both build one key).

## 4. Writers N

N = 2 writers to this prefix: (1) `data/transcripts/scripts/updates/intake.py` `place()` (offline operator path; already
writes `deck_<sha16>.pptx`; its own role, unchanged); (2) the gateway's `copy_site_file_to_s3` (this ask, the new one).
Counted by `Grep market_update` over `data/transcripts` (3 files: `intake.py`, `NAMES.json`, `test_market_update_intake.py`;
only `intake.py` writes) plus the gateway module. Not counted: other roles' grants on the bucket, which this ask does not
read or change.

## 5. Order of acts

1. Apply the grant: plan with `-var market_update_s3_root=<address() output>`, review that the only add is
   `aws_iam_role_policy.market_update_gateway_put` (+ the pure-name module), apply through `safe-apply` (applier order, signed
   pair). The grant alone changes nothing observable: no code calls it yet (the live gateway has no `.pptx` pair).
2. Then a gateway release that carries this code and sets `ADVI_MARKET_UPDATE_S3_ROOT` from the same `address()` call
   (`deploy-to-ec2.sh`, test_ogab2_ac03). Reverse order (release first) would make an admitted call fail with a 403 on the
   put and write nothing.

## 6. Rollback per act

- Grant: `terraform destroy -target=aws_iam_role_policy.market_update_gateway_put` (or remove the resource and apply);
  nothing else depends on it; takes effect for new calls at once.
- Release: the gateway's standard rollback to the prior live release; the prior release has no `.pptx` pair, so the call is
  refused as an extension outside the pairs.
- Objects already written: each is a new key that nothing overwrote; remove by key (a deliberate delete act, outside this ask).

## 7. Residual

One deck placed on two different dates lands under two keys (the date partition is the UTC date of the put, the name is the
content hash). The same-day duplicate is refused; the cross-day duplicate is not. Also: the registered tool's `quarter`
argument is still required and grammar-checked for a `.pptx` but no longer names the key (row `NFRA_OPLGTW-Z-W55-S2`).

## 8. Open item the halves should know

None open. Row `NFRA_OPLGTW-Z-W55-S1` (AC1 FAIL on `test_ogab2_ac02`, which pinned the superseded name-in-key form) was the
issuer's cut defect; Amendment 1 (@1ceb994ad3) added the file to the order's paths and `test_ogab2_ac02` is re-pinned to the
content-addressed key. AC1 and AC2 both read PASS (citing row `NFRA_OPLGTW-Z-W55-S3`). The diff by file in section 1 gains
`infra/aws/ec2/opal-gateway/tests/test_og_ab2_pairs.py`: `test_ogab2_ac02` only (9 insertions, 3 deletions).
