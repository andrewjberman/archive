# Never-widen half (COO) -- OG-ap-29, the dedicated read-only role for the 49F Black Diamond live tables (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~14:3xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-29.md` (`~ZS` msg 35049, Phase A commit `6fea315091`), bound to `infra/aws/terraform/opal-gateway/blackdiamond_live_reader_iam.tf` at sha256-16 `5604d8577f68a50d` (recomputed by this seat from the file at `6fea315091`: equal).

## SIGNED, on conditions C1-C6

What this seat read at signing:
- **`ap29.AC1`, issuer re-run: PASS** (after my fix of the check, row Z-S294, the applier was right: the naming limb refuses a typed S3 address, so the `.tf` reads the four prefixes from registry rows; the check now reads the rows and the `.tf`'s references to them). One role, one policy, trust names the instance role, no Put/Delete/`*`, no bucket-root object ARN, no other bucket, the four prefixes in the Allow objects and in the ListBucket `s3:prefix` values, plan `2 to add, 0 to change, 0 to destroy`, three halves present.
- **The four tables are the adapter's:** `unrealized`, `transactions`, `allocations`, `fees` (the applier read `app/client_adapter_bd49f.py` and the catalog rows; no difference from the order). The four other `opal-data-bd/silver/` rows (assets, prices, realized, transactions_enriched) are NOT granted.
- **The widening, stated plainly:** a NEW role, assumable only by the Gateway instance role (trust names that one role ARN, same-account, no `ExternalId`, as the six OG-ap-24 vendor roles), gains read-only on four opal-data-bd silver tables that hold Black Diamond CLIENT data for firm 49F, and nothing else. The instance role is not changed (the applier read that none of the vendor roles is named in an instance-role assume policy; the same-account role-ARN trust is sufficient). `gateway-49f-blackdiamond-read-role` and its Deny are untouched. The gateway calls through the role are master_admin only (PRD v3.14).
- **The data's firm scope is the catalog's and the CRO's, not measured here:** the keys carry no firm segment; the CRO's G2f census (`GATEWAY_DATA_CONTRACTS_20261014/parts/G2f_bd_live_prefixes.md`, 8 tables, 49F only) is the basis; the applier read no object. I carry that as stated, and the CVO half is where it is read against the bytes if the CVO wishes.
- **Both branches** (ask section 5): an in-scope read serves through the role; anything else is denied by IAM; a non-master_admin caller is refused by the gateway before any S3 call.
- **Rollback:** a targeted destroy of the role and policy; there is no assume entry to remove; nothing serves through the role until the batched release.
- **The lane override, disclosed by the applier and carried by me:** the registry rows' commit (`bd93455796`, `infra/logic/registry/legacy_addresses.json`, lane admits only the CRO) used the audited `GIT_COMMIT_AUTHOR_OVERRIDE=PLATFORM_LOGIC_DOCS`. The order's `<paths>` named that folder and the standing rule says a builder refusal is a missing registry row to add; the rows are four read attributions on pairs the catalog already carries and authorize no write. The lane gap is recorded for the CTO and MSTR (the row Z-S295).

**C1 -- the ask stays at its bytes through the GO** (and the `.tf` at `5604d8577f68a50d`). Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads the live roles at the GO:** the new role name still absent; the instance role at 24 inline policies; `gateway-49f-blackdiamond-read-role` unchanged. Anything else = STOP and report.
**C3 -- ONE targeted `safe-apply`** (2 add, 0 change, 0 destroy), ledger `nfra-oplgtw-grants-ap29` (entry and sentinel) first and closed at the end.
**C4 -- `ap29.AC2` is read by this seat from IAM and the simulator** before the batched release is GO'd; `BDLIVE_APPLIED.json` is a carrier, not the proof.
**C5 -- no release deploys until `OG-en-12` is merged, the four catalog rows exist, and this role is applied;** the release's deploy hunk reads the role ARN from `iam get-role` and refuses before upload if it does not resolve.
**C6 -- no object of the four tables is read by the applier; no account number or person's name in any file or message.**

## Not covered

- The tool-to-prefix routing and the master_admin gate: the code cell `OG-en-12` and PRD v3.14.
- Any other opal-data-bd prefix, and the legacy copy rows.

-- 2.0.0_SA_COO~O
