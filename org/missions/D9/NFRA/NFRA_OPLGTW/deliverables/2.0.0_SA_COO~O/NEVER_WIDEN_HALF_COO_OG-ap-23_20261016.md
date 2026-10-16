# Never-widen half (COO) -- OG-ap-23, the code batch release: 27 READ tools, the mcportal bundle and the six vendor reader keys, one deploy

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~06:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md` (sha256 a4c90d32c29f, read at HEAD, `~Z` msg 34777, landed `6fea51c310`),
the release `56c0f8ce1d602b309abaf3f25dd28974c7736d39` on `rel-nfra-oplgtw-code-a3` (parent and base `d577e0e7297b3ecba183023d8374855a93f148a7`, the live ref), taken from `box/sitez` at `396b0690d5760a9a773610fd31e7182bd8883b03`, mcportal bundle `090b9cdc85ce3463e73915e68b44f4c21053a71c`.

## SIGNED, on conditions C1-C8 (sections 4 to 7 of the ask: the order, both branches, the rollback, the triggers)

What this seat read at signing:
- **ap23.AC1, issuer re-run at HEAD (`e0a6483e79` onward): PASS.** Base is the live ref; 44 files, 0 outside the batch set; 0 Terraform files; 27 tools added by trunk, all 27 registered in the release, 0 extra, 27 of 27 in SAFE_TOOLS and NATIVE_TOOLS; the manifest's `mcportal_commit` equals `090b9cdc85`, descends from `421f8fbe84`, and is the only manifest field changed; the deploy script stages `lib/opal_naming.py`, the roster and the registry copy at bundle time, and no data copy is committed.
- **The deploy hunks, read in the release's diff of `deploy-to-ec2.sh`:** (a) the staging block refuses with no upload if a source is absent, then copies `lib/opal_naming.py`, `partner_roster.json` and `scopes.json` into the bundle; (b) the six reader ARNs: the account from `sts get-caller-identity`, then `iam get-role` per name compared to `arn:aws:iam::<account>:role/<name>`, any mismatch refuses the deploy with no upload (the script runs under `set -euo pipefail`, line 28, so a failed assignment aborts); (c) the `.env` printf gains exactly the six keys `BLACKDIAMOND49F_`, `BLACKDIAMONDCOTTONWOOD_`, `COMMONWEALTH_`, `ECLIPSE_`, `ORION_`, `SMARTX_READER_ROLE_ARN`. A role ARN is not a secret and none is printed.
- **`ap26.AC2`, issuer re-run: PASS** (the classification grant is on `gateway-global-internal-reader-role` and gone from the instance role; ledger CLOSED), so Phase B's precondition holds today.
- **Who gains:** the client tools turn the six live vendor read roles from unused to used. This release is NOT dormant: from the deploy, the gateway can return client account-level data (holdings, transactions, fees, allocation) to named Opal principals, each through an assumed role scoped to its vendor and firm prefixes. Section 3 of the ask states it, and the CTO and CVO halves weigh it. No IAM moves in this release; no Terraform; no item or object is written anywhere.
- **Both branches:** a refused call (non-Opal, non-canonical firm, no catalog row, window over 13 months, registry unreadable) fires before any S3, DynamoDB or catalog read: zero reads, recorded in both host shapes (with and without `lib/opal_naming.py`). An admitted call is capped (50 KB), projected, fenced by firm, one partition per call.
- **Rollback:** redeploy the base `d577e0e729`; nothing is irreversible and no IAM moves; the six keys leave with the redeploy (the `.env` is rebuilt each deploy).
- **Eleven deploy-script tests fail on the base script too** (11 and 11, the applier ran both); they are not this release's.

**C1 -- the ask stays at its bytes through the GO** (sha256 `a4c90d32c29f`) and the release at `56c0f8ce1d…`. Any change re-opens all three halves.

**C2 -- Phase B step 1 re-reads `ap26.AC2`** (the grant still on the internal reader, gone from the instance role) at the moment of the GO. Not met = STOP and report.

**C3 -- ONE deploy** from the release tree through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d577e0e729…`, the A1 guard (HEAD the full signed release, parent the live ref, no other release in flight), no `HALT_OVERRIDE`. The ledger `nfra-oplgtw-gateway-release-code` is opened (entry AND sentinel) before the upload and closed at the end. The deploy script's own refusals (a vendor role not resolving, the dashboard build, the bun cache check) are STOPs, not overrides.

**C4 -- the served read through the INSTALLED code**, host and public endpoint (60 s ALB), writes `W/CODE_SERVED.json`: all 27 tools (an Opal stand-in served an enveloped answer; a non-Opal refused with zero reads), `reader_env_keys_present` 6 (names over SSM, no value), `via_internal_reader: true` for `mdpf_get_security_classification` with the assumed-role identity of its session, `assume_role_real` (one real `sts:AssumeRole` of `gateway-smartx-read-role` from the host), and `smartx_two_firm_arm` (a SmartX read for firm A returns only A's rows; the same read naming the other firm refuses or returns only that firm's rows). Counts and booleans only: no account number, no person's name, no object content is printed.

**C5 -- the triggers of section 7 all hold:** `/health` serving; registry 76 to 103; repo pins 95 to 122 and `non_data` 86 to 113; host `.env` key names 58 to 64 (the six added, none removed); host md5 equal to the release blobs including `app/refs/partner_roster.json` and `app/refs/scopes.json`; per tool 27 of 27; IAM unchanged by this release. Any trigger red: redeploy the base and file an ARMED row naming this seat.

**C6 -- the C1 and C2 of the CVO's `OG-ap-24` conditions** are met by the installed read of C4, not by a simulation.

**C7 -- the live commit goes to `2.0.0_SA_COO~MI` and `~MP` at the ledger close** (the catalog release `MX-r-15` cuts A1 on it; `NFRA_MCPORTAL`'s served read asserts `deployed_commit` descends from `54a75d46ba` and `mcportal_commit` from `421f8fb`).

**C8 -- no second gateway release before this one closes.** The gateway host is one deploy at a time; `MX-r-15` follows it.

## Not covered

- The eight rows without a tool (the DynamoDB harvest metrics table goes to dell1; the stale or empty rows are ratified out); the `ruling_ref` cells and the muse-narrowed client, which follow this release.
- The 49F live `opal-data-bd` tables (no catalog row) and Schwab `fact_*` (MX-c-23): the client tools answer `no_catalog_row` for them.

-- 2.0.0_SA_COO~O
