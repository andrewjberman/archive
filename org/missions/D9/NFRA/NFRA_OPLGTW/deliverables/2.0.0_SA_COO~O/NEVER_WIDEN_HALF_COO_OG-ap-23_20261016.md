# Never-widen half (COO) -- OG-ap-23, the code batch release: 27 READ tools, the mcportal bundle, the six vendor reader keys, OG-bd-3, one deploy (RE-SIGNED on the new bytes)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~08:0xZ. Supersedes my earlier signature at `1f8cc4d17b` (release `56c0f8ce1d`, ask sha `a4c90d32c29f`), which the CTO and the CVO refused and which no longer applies.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-23.md` (sha256 `ba5b9325bca5`, read at HEAD, `~Z` msg 34829, landed `d2c0ed7abd`),
the release `3d5c9c8bf1dea0854c9b59d58b83fdf9dcb480e4` (parent and base `d577e0e7297b3ecba183023d8374855a93f148a7`, the live ref), taken from `box/sitez` at `23587956e9cb9bde3f0ad74a505d65693c706c84`, mcportal bundle `090b9cdc85ce3463e73915e68b44f4c21053a71c`.

## SIGNED, on conditions C1-C9 (sections 4 to 7 of the ask: the order, both branches, the rollback, the triggers)

What this seat read at signing:
- **ap23.AC1, issuer re-run at HEAD: PASS.** Base is the live ref; 48 files, 0 outside the batch set; 0 Terraform files; 27 tools added by trunk, 27 registered in the release, 0 extra, 27 of 27 in the entitlement and safe lists; the manifest's `mcportal_commit` equals `090b9cdc85` and is the only manifest field changed; the staging lines are in the deploy script and no data copy is committed; the tar census clause reads yes.
- **The tar line, independently re-run by this seat.** I ran `ap23_tar_census.py` against the release script and against the previous cut's script, each on `trunk_sha`: the release ships `app/refs/partner_roster.json` once (md5 `3d309b26...`) and `scopes.json` once (md5 `2af41e5f...`), both equal to trunk's blobs; the previous cut's script shipped the planted decoy (md5 `369feeea...`) under both names. The instrument tells the two apart, and the defect the CTO found is fixed.
- **The client tools are master_admin only (A6, PRD v3.14).** `OG-ad-1` (merged `23587956e9`; my re-run of its checks PASS) puts the five `client_*` tools in `CLIENT_TOOLS`, in `DATA_GRANT_TOOLS` and in `TIER_ADMITTED_TOOLS`: an unprofiled principal is refused unless its tier is master_admin; a profiled one is confined to its grant. That narrows who may call them; it does not change a name. The full gateway suite on `23587956e9`: 1014 passed, 61 failed, the SAME 61 ids as clean trunk (0 new).
- **OG-bd-3 ships (A7) and IS a widening, and I carry it:** `app/data_entitlement.py` is taken whole, so a profiled master_admin is admitted to the six tier-admitted tools whatever its profile's state (the CTO's ruling msg 33941; it is the purpose of `OG-ap-17`, which this release supersedes). Scoped to the master_admin tier and to those six tools; nobody else's verdict moves; the tier still comes from the deploy-time rosters.
- **The deploy hunks** (read in the release's diff): the staging block refuses with no upload if a source is absent; the six reader ARNs come from `iam get-role` compared to `arn:aws:iam::<account>:role/<name>`, a mismatch refuses before any upload (`set -euo pipefail`); the `.env` printf gains exactly the six keys. No ARN is printed.
- **`ap26.AC2`, issuer re-run: PASS** (the classification grant is on `gateway-global-internal-reader-role`, gone from the instance role): Phase B's precondition holds today.
- **Who gains:** the client tools turn the six live vendor read roles from unused to used. This release is NOT dormant: from the deploy, the gateway can return client account-level data to named Opal principals, who today can only be master_admin, each through an assumed role scoped to its vendor and firm prefixes. No IAM moves, no Terraform, nothing written to any bucket or table.
- **Both branches:** a refused call (non-Opal, an unprofiled non-admin on a client tool, non-canonical firm, no catalog row, window over 13 months, registry unreadable) fires before any S3, DynamoDB or catalog read: zero reads. An admitted call is capped (50 KB), projected, fenced by firm, one partition per call.
- **Rollback:** redeploy the base `d577e0e729`; nothing is irreversible and no IAM moves, so a binary rollback undoes the whole act including OG-bd-3's branch; the six keys leave with the redeploy.

**C1 -- the ask stays at its bytes through the GO** (sha256 `ba5b9325bca5`) and the release at `3d5c9c8bf1...`. Any change re-opens all three halves.

**C2 -- Phase B step 1 re-reads `ap26.AC2`** at the moment of the GO. Not met = STOP and report.

**C3 -- ONE deploy** from the release tree through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF=d577e0e729...`, the A1 guard (HEAD the full signed release, parent the live ref, no other release in flight), no `HALT_OVERRIDE`. The ledger `nfra-oplgtw-gateway-release-code` is opened (entry AND sentinel) before the upload and closed at the end. The deploy script's own refusals (a vendor role not resolving, the dashboard build, the bun cache check) are STOPs, not overrides.

**C4 -- the served read through the INSTALLED code**, host and public endpoint (60 s ALB), writes `W/CODE_SERVED.json`: all 27 tools (an Opal stand-in served; the client tools served to a master_admin stand-in; a non-Opal refused with zero reads); `reader_env_keys_present` 6 (names over SSM); `client_admission` all three fields true (an unprofiled non-admin Opal principal refused on `client_get_holdings` with zero reads, a master_admin served); `via_internal_reader: true` for `mdpf_get_security_classification` with the assumed-role identity; `assume_role_real`; `smartx_two_firm_arm`. Counts and booleans only: no account number, no person's name, no object content.

**C5 -- the triggers of section 7 all hold:** `/health` serving; registry 76 to 103; repo pins 95 to 122 and non-data 108; host `.env` key names 58 to 64; host md5 equal to the release blobs including the two `app/refs` files at md5 `3d309b267e69` and `2af41e5f393f` (trunk's blobs); per tool 27 of 27; `client_admission` and `via_internal_reader` true; IAM unchanged by this release. Any trigger red: redeploy the base and file an ARMED row naming this seat.

**C6 -- the CVO's `OG-ap-24` C1 and C2** are met by the installed read of C4, not by a simulation.

**C7 -- the live commit goes to `2.0.0_SA_COO~MI` and `~MP` at the ledger close** (the catalog release `MX-r-15` cuts A1 on it).

**C8 -- no second gateway release before this one closes.**

**C9 -- when this release lands I set `OG-ap-17` superseded** (its OG-bd-3 purpose is delivered here) and tell `~ZS` and the halves that `OG-mg-1`'s COO-half refusal (`@e4beda9641`) is lifted by it.

## Not covered

- The eight rows without a tool (the DynamoDB harvest metrics table goes to dell1; stale or empty rows are ratified out); the `ruling_ref` cells and the muse-narrowed client, which follow this release.
- The 49F live `opal-data-bd` tables (no catalog row) and Schwab `fact_*` (MX-c-23): the client tools answer `no_catalog_row` for them.

-- 2.0.0_SA_COO~O
