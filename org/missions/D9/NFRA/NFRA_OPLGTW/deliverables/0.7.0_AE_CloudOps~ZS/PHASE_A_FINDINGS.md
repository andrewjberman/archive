# NFRA_OPLGTW.TO-OG-ap-24 Phase A -- findings that stop the .tf (0.7.0_AE_CloudOps~ZS, 2026-10-15)

Live read: `GR_BEFORE.json` (3 `gateway-*-read-role` present; BD policy sha256_16 4893211d4408180a; copy in `bd_policy_before.json`).

1. BD extension cannot be additive. The live `gateway-blackdiamond-read-policy` carries explicit Deny statements
   (`DenyReadsOutsideTheFeesPrefix` NotResource = `opal-data-bd/silver/fees/*`; `DenyListingOtherBuckets`;
   `DenyListingOutsideTheFeesPrefix`). An explicit Deny beats any Allow, so a second policy on that role granting
   `opal-data-assets/blackdiamond/49f/silver/` is denied. The extension is an EDIT of `bd_read_policy` in
   `infra/aws/terraform/opal-gateway/blackdiamond_reader_iam.tf`, which is not in the order's `<paths>`.
2. AC1 counts `resource "aws_iam_role"` in `client_vendor_roles_iam.tf` and wants 6. The BD role is declared in
   `blackdiamond_reader_iam.tf` (`aws_iam_role.bd_read`); a second declaration is a duplicate address. The file can
   hold 5 role resources, not 6.
3. Schwab: `gateway-schwab-read-role-policy` allows 12 prefixes, all `dim_position|dim_balance|dim_asset|dim_transaction`
   for masters 08242234, 08335338, 08403355. It does NOT cover any `fact_*` prefix: that is a gap to name, not coverage.
4. The code has ONE role per vendor KEY, and `blackdiamond` is one key for both firms. `client_core.Ctx._scope` sets
   `vendor = prefix.split("/",1)[0]` and calls `client_role.client_for(vendor)`; `client_role.role_env_name` returns
   `<VENDOR>_READER_ROLE_ARN`. `client_adapter_bd49f.py` and `client_adapter_bdcottonwood.py` both set `VENDOR = "blackdiamond"`,
   so the 49F and Cottonwood reads both use `BLACKDIAMOND_READER_ROLE_ARN`. A `gateway-cot-blackdiamond-read-role`
   has no environment variable that selects it, so it is unreachable as the code stands. The vendor keys the code
   can select are: blackdiamond, orion, eclipse, smartx, commonwealth (new or extended) and schwab (exists).
   That is 5 roles to build or extend, not 6, and one role (blackdiamond) would read two firms' prefixes.
