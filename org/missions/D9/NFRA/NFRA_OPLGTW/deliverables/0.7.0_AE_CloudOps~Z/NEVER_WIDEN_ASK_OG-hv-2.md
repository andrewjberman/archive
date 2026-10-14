# NEVER-WIDEN ASK -- OG-hv-2: the harvest read grant and the gateway release of `harvest_list` / `harvest_read`

To: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O` and `3.0.0_SA_CVO~Z` -- THREE halves, each signed on its own.
From: `0.7.0_AE_CloudOps~Z`. Phase A of `NFRA_OPLGTW.TO-OG-hv-2`, at amendments A1-A5 (`@ff91700f3b`).
**NOTHING IS APPLIED AND NOTHING IS DEPLOYED.** The grant file is written and planned; the release is
cut and tested. Both acts wait on this ask.

Records: `hv2_release.json`, `hv2_grant_gen.py` (the generator), `infra/aws/terraform/opal-gateway/harvest_read_iam.tf`.

## 0. The two acts, in the order they must run

| act | ledger | what it does | reversible by |
|---|---|---|---|
| **ACT 1 -- the grant** | `nfra-oplgtw-harvest-read-grant` | CREATE one inline policy `gateway-global-harvest-read-policy` on `gateway-global-internal-reader-role` | `delete-role-policy` of that one name |
| **ACT 2 -- the deploy** | `nfra-oplgtw-gateway-release-hv` | install release `7c558b4e2176a632d13e6301af3e06d434aa1540` on `i-07dccb1615503ac99` | redeploy base `90967e39ba4bdca17c6f84d9806c29cc67f8482e` |

**The order is load-bearing, not a preference.** Grant first: the grant alone creates no reachable new
state, because no installed byte calls the harvest path -- `s3:GetObject` on a bucket nothing reads is
inert. Deploy first would open a live window in which every served harvest read is `AccessDenied`.

## 1. The release, by file -- `90967e39ba` -> `7c558b4e21`

| file | +/- | taken |
|---|---|---|
| `app/harvest_read.py` | +181 -0 | whole; byte-equal to `box/sitez` HEAD and to OG-hv-1's own blob |
| `tests/test_og_hv1.py` | +240 -0 | whole |
| `app/tools.py` | +21 -0 | by hunk -- the two `@mcp.tool()` registrations and one import |
| `app/destructive_ops.py` | +2 -0 | by hunk -- both names into `SAFE_TOOLS` |
| `app/data_entitlement.py` | +1 -0 | by hunk -- both names into `NATIVE_TOOLS` |
| `tests/test_entitlement_admin.py` | +2 -1 | by hunk -- the registry count 63 -> 65 |
| `tests/test_data_entitlement_family.py` | +3 -3 | by hunk -- the non-data count 54 -> 56 |

**7 files, 0 outside OG-hv-1's seven, and the add/delete counts are IDENTICAL per file to OG-hv-1's own
gateway diff at `4e26a29872`** -- so nothing from trunk rode along on a file that moved for other
reasons. Tests in the release tree: `test_og_hv1.py` 5 passed, `test_entitlement_admin.py` 9 passed,
`test_data_entitlement_family.py` 4 passed.

The base is the live ref, measured and not assumed: one SSM md5 read over `app/`, `deploy/` and
`dashboard/` read **105 of 105 files EQUAL** against `90967e39ba`, 0 differing, 0 repo-only.

## 2. The two widenings, each named as one (PRD v2.8)

**W1 -- the gateway's reach: an Opal principal can now read `s3://opal-data-harvest` under 24 top-level
prefixes, `raw/` included.** Before this release no gateway tool reaches that bucket at all. The 24 are
not a choice made here: they are `app/harvest_read.py`'s own `SERVED_PREFIXES`, from Andrew's call 8
(2026-10-13 ~20:0xZ) that all 24 serve to Opal principals. `raw/` means unprocessed harvest input is
readable by any Opal principal, which is the widest single consequence in this ask and is intended.

**W2 -- `gateway-global-internal-reader-role` gains its own S3 read on `opal-data-harvest`** (A5: this
is the role `harvest_read` actually assumes; `opal-gateway-role` is NOT widened by this ask and keeps
only the `sts:AssumeRole` it already holds).

**W2's blast radius, read from the live trust policy rather than inferred:** that role's
`AssumeRolePolicyDocument` carries **exactly one statement** -- `Allow sts:AssumeRole`, `Principal =
arn:aws:iam::313476888478:role/opal-gateway-role`, **no condition**. So the only identity in the account
that can pick up this read is the gateway instance role. Nothing else gains anything.

Its width today, so the addition is read beside it: **1 inline policy, 0 attached managed** --
`gateway-global-internal-reader-policy`, `s3:GetObject` on `opal-data-portal-v2/json/*` and
`/platinum/*` only. This ask makes `opal-data-harvest` the **second** bucket that role may read.

**Who loses: nobody.** No statement is removed, no policy is replaced, no object is written anywhere,
and no grant-store record is touched.

## 3. Both branches of the expected outcome, from IAM's own answers

The five reads below are each a separate `simulate-principal-policy` invocation with ONE
`--resource-arns` (the instrument flips held resources to `implicitDeny` when several ride one call).
`head-bucket opal-data-harvest` = **yes**, so no `allowed` here is the documented false-ALLOW mode
against a resource that does not exist.

| # | principal | action / resource | now | after ACT 1 |
|---|---|---|---|---|
| 1 | the internal reader | `s3:GetObject` `opal-data-harvest/packs/x.json` | `implicitDeny` | **allowed** |
| 2 | the internal reader | `s3:GetObject` `opal-data-portal-v2/json/x.json` | **allowed** | allowed (untouched) |
| 3 | the internal reader | `s3:GetObject` `opal-data-harvest/zzz-not-served/x.json` | `implicitDeny` | **`implicitDeny` -- STAYS** |
| 4 | the internal reader | `s3:ListBucket` `opal-data-harvest` | `implicitDeny` | **allowed** (prefix-conditioned) |
| 5 | `user/Andrew_Berman` | `s3:GetObject` `opal-data-harvest/packs/x.json` | **allowed** | allowed |

Row 2 is the same-principal positive control: it rules out the simulator's four false-DENY modes
(multi-ARN, unsupplied `Condition` context, an unvalidated action name, a wrong-grain ARN) on the exact
principal and action the denies are read from. Row 5 is the broad control. **Row 3 is the branch that
matters: the act is bounded only if an off-list prefix is still refused afterwards**, and the half
covers that branch as much as the allowed one.

## 4. The grant, exactly as it will apply

`infra/aws/terraform/opal-gateway/harvest_read_iam.tf` -- ONE `aws_iam_role_policy`, generated by
`hv2_grant_gen.py`, never hand typed:

- **name** `gateway-global-harvest-read-policy` = `lib/opal_naming.py name("gateway", "global",
  "harvest-read", "policy")`, run, not quoted from the order (Rule 30). A literal, because the
  commit-time naming limb grades the resource name's own bytes.
- **role** `aws_iam_role.int_reader` (`mcpmsp_internal_reader.tf:32`). The gateway instance role is
  not referenced in the file at all.
- **`s3:GetObject`** on 24 object ARNs `arn:aws:s3:::opal-data-harvest/<prefix>*`, where the 24
  prefixes are read **by AST** from `app/harvest_read.py` `SERVED_PREFIXES` -- 24 of 24 equal, 0 extra,
  **0 bucket-wide (`/\*`) ARNs**.
- **`s3:ListBucket`** on `arn:aws:s3:::opal-data-harvest` under `Condition StringLike s3:prefix` = the
  same 24, each bare and starred: **48 values**. Bare admits a list AT the prefix, starred admits
  below it.
- **Actions present in the whole file: exactly `s3:GetObject`, `s3:ListBucket`, `s3:prefix`.** No Put,
  no Delete, no bucket-wide object read: **non-read actions 0**.

**The plan, targeted:** `terraform plan -input=false -target=aws_iam_role_policy.int_reader_harvest_read
-var market_update_s3_root=<builder address()>` ->

```
Plan: 1 to add, 0 to change, 0 to destroy.
```

**One thing the halves should know about the directory, not the act:** this configuration also carries
`aws_iam_role_policy.market_update_gateway_put` (OG-mu-1), written and deliberately **never applied**.
An untargeted apply here would land it too. ACT 1 is `-target`ed at the one resource, which is why the
plan reads 1 and not 2, and the targeting is part of what is being signed.

## 5. Writers of the named property: N printed, each read

**ACT 1's property -- the internal reader role's inline policies. N = 2, both read.**

1. `aws_iam_role_policy.int_reader` (`mcpmsp_internal_reader.tf:44`) -- the portal-v2 read above.
2. `aws_iam_role_policy.int_reader_harvest_read` -- this act.

No third writer: a census of `aws_iam_role.int_reader` across the 39 files of
`infra/aws/terraform/opal-gateway/` returns those two `role =` assignments and nothing else, and the
live role shows **1 inline policy and 0 managed**, so terraform is the only writer in evidence. The
name this act writes is **absent today** (`contains(PolicyNames, 'gateway-global-harvest-read-policy')`
= `False`), so it is a CREATE, which is what the plan says, and the existing policy is not read for
writing or touched.

**ACT 2's property -- `services.opal-gateway.deployed_commit` in `EC2_MANIFEST.json`. N = 2, both
read, and one of them misbehaves:** `deploy-to-ec2.sh` writes its own manifest record on the branch it
runs from, and it **does not recompute `file_checksums`** (measured in OG-ap-14: 8 of 10 mismatched,
and its `previous_deployed_commit` read a stale `2c0f84966d`). So this seat writes the trunk record
itself -- `previous_deployed_commit` from trunk's own current value, checksums recomputed from the
release blobs. That is a known defect being worked around deliberately, not a surprise, and it is
named here because the manifest is how a later reader learns what is live.

## 6. The two tools, and what refuses before anything is read

`harvest_list(prefix, start_after)` -- one page (1000 keys max) under a served prefix.
`harvest_read(key)` -- one object, JSON parsed, Parquet as rows, else UTF-8 text, capped at 4 MB.

The admission runs **before any S3 call**: a principal, then `tools._is_opal_user(principal.email)`,
then the served-prefix test with a `..` check. Refusals, each `{error, code, guard_denied: True}`:
`principal_required`, `harvest_opal_only`, `harvest_prefix_not_served`, `harvest_over_cap` (and
`harvest_not_json` on a malformed object). AC2's `s3_calls_on_refusal: 0` is the field that proves the
ordering rather than asserting it.

**The honest risk in this ask: the Opal-only boundary is a CODE gate, not an IAM gate.** After ACT 1,
IAM admits the whole served surface to the role the gateway assumes; the only thing between a non-Opal
principal and that data is `_is_opal_user` (`app/tools.py:1037`). IAM will not catch a regression in
it. What holds it is `tests/test_og_hv1.py::test_oghv1_ac02` and `::test_oghv1_ac04` (every tool
refused `harvest_opal_only` for a non-Opal principal, and `principal_required` with no principal at
all) plus AC2's live negative arms on `packs/` and `wsj/harvest/`. A half that wants that boundary in
IAM instead should refuse this ask and say so -- it cannot be expressed as a prefix condition, because
the principal is a gateway-level identity, not an AWS one.

## 7. The research-only boundary, from the producer's rule

The two names go into `NATIVE_TOOLS` (`app/data_entitlement.py:117`) and `SAFE_TOOLS`
(`app/destructive_ops.py`) -- the **read class, deliberately NOT `DATA_GRANT_TOOLS`**. So an Opal
principal with no data grant reaches the harvest tools and **stays refused every `schwab_*` tool and
`blackdiamond_list_fees`** by `data_entitlement.decide()` with `entitlement_denied`, unless Andrew
admits that principal to PRD v2.2's connected set. That is asserted at the release by
`tests/test_data_entitlement_family.py::test_ogpf1_ac01` (non-data tools 54 -> 56, disjoint from
`SCHWAB`) and `tests/test_og_hv1.py::test_oghv1_ac05` (the same unprofiled principal that reads
`packs/` gets `entitlement_denied` on the Schwab and Black Diamond tools), both passing.

## 8. What ACT 2 must read back, and what each trigger would mean

| trigger | instrument | pass |
|---|---|---|
| service up | `GET /health` on `127.0.0.1:8080` (the live listener; 8000 is not bound) | `{"ok":true}` |
| **tools +2 and only +2** | the app's OWN registry -- `tests/test_entitlement_admin.py::test_ogz2_ac08`, `len(registered_tool_names)` | **63 -> 65** |
| `.env` untouched | no release file sits under `deploy/`; key NAMES compared, never values | unchanged |
| `ENABLED_INTEGRATIONS` untouched | the same -- the key is present on the host and not written by this release | unchanged |
| the running bytes ARE the release | SSM md5 over `app/`, `deploy/`, `dashboard/` vs `7c558b4e21` | 105 of 105 |

**Do not grade the tool trigger with `grep -c '@mcp.tool'`.** That census reads **65 on the installed
bytes today** (44 in `app/tools.py`, across 11 files) because it counts decorators, not the registry
the app builds -- a different denominator that would read the pre-release host as already at 65. The
registry count is 63 now and 65 at the release, and it is the number in the sentence above.

Any trigger failing: redeploy the base and file an ARMED row naming `2.0.0_SA_COO~O`.

## 9. Rollback per act, per key

**ACT 1:** `aws iam delete-role-policy --role-name gateway-global-internal-reader-role --policy-name
gateway-global-harvest-read-policy`. One key, and it is exactly the key this act creates; the
pre-existing `gateway-global-internal-reader-policy` has a different name and is never read or
rewritten, so the rollback cannot damage the portal read. Nothing has to be re-PUT, so the
envelope-vs-document hazard of a `get-role-policy` capture does not arise here.

**ACT 2:** redeploy `90967e39ba` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF`. It is a complete
rollback and not a hope, because that ref's parity with the host is already measured at 105 of 105.

## 10. What is NOT asked

No catalog edit. No grant-store record. No object written to any bucket. No `.env` key added. No
`opal-gateway-role` change. No second policy, and no bucket-wide ARN. No change to the Opal-only
predicate or to any Schwab or Black Diamond entitlement. AC3 (a real Opal asset manager's live read)
is a judgment criterion owed by `3.0.0_SA_CVO~Z` and is not part of this ask.
