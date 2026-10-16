# Never-widen half (COO) -- OG-ap-24, the six vendor read roles of the G2 client adapters (one batch)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~01:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ap-24.md` (sha256 692cce61ddf8, read at HEAD, `~ZS` msg 34628, landed `d177d1d5ec`),
the grant `infra/aws/terraform/opal-gateway/client_vendor_roles_iam.tf` at sha256-16 `21a54e8f197eeea2` (22740 bytes, read here: it equals the hash the ask binds to).

## SIGNED, on conditions C1-C6

What this seat read at signing:
- **ap24.AC1, issuer re-run: PASS.** Generator `--check` exit 0 (the `.tf` equals what the generator derives from the merged adapters and the catalog rows); 6 `aws_iam_role` and 6 `aws_iam_role_policy` resources; wildcard resource 0; Put or Delete in actions 0; trust principals other than the gateway role 0; plan 12 to add, 0 to change, 0 to destroy.
- **Structure of every policy, read in the `.tf`:** six `AssumeRole` trusts, each `Principal = aws_iam_role.gw.arn` only (`OnlyOpalGatewayRole`); each role carries an explicit Deny of every non-read S3 action (`NotAction` the read actions plus `ListBucket`), an explicit Deny of reads outside its approved object ARNs (`NotResource`), a Deny of listing any other bucket, a Deny of listing outside its prefix forms, then the Allows: `GetObject`/`GetObjectVersion` on the approved prefixes and `ListBucket` confined by `s3:prefix`. Explicit Denies beat any other grant.
- **Who gains:** the gateway instance role can assume six NEW roles, each reading only its vendor's catalog prefixes in `opal-data-assets` (the ask's section 2 table: 49F two tables, Cottonwood seven, Orion two, Eclipse two, Commonwealth four, SmartX five). Six tools reach client data only through these roles (`client_*`, Opal principals only). Nobody loses a grant; no existing Terraform file changes.
- **The live Black Diamond and Schwab roles are not touched** (policy hashes `4893211d4408180a` and `a3e8ca81172af8cc`), per my A3: the two Black Diamond firms get separate roles, so IAM fences 49F from Cottonwood. The generator tested reuse of the live BD role against the Cottonwood prefixes (0 of 7 covered) and the ask asks no delta, so my one-delta clause of A3 is not used.
- **SmartX is the widest in firm terms** (four firms in each object): IAM cannot fence them; the fence is code (row filter by `advisor_id` through the roster name join, cl-5 A2, two-firm negative arm in its proof). Accepted on that account.
- **No ExternalId on the six trusts** (the Schwab and Black Diamond readers carry one): the trust is the one gateway role ARN in the same account. That decision is the CTO half's; this half accepts either ruling and, if the CTO rules the other way, the ask is re-issued and this half re-read.
- **Both branches:** a read outside a role's prefixes is denied by the explicit Deny; an admitted call reads one capped `date=` partition. The applier cannot assume these roles, so Phase B reads the IAM branch by `simulate-principal-policy`, one resource per call, with a separate `*`-principal positive control.
- **Rollback:** per role, delete the inline policy then the role (or targeted destroy); the prior state of each is absence. Nothing served changes.
- **Gaps accepted as named (ask section 8), not coverage:** the 49F live `opal-data-bd` tables (allocations, fees, transactions, unrealized) have no catalog row, so the 49F holdings, transactions and fees answer `no_catalog_row` until the catalog row and a later grant exist (CTO ruling msg 34134 reads `opal-data-assets` silver only); Schwab `fact_*` is uncovered (MX-c-23, MX-r-15).

**C1 -- the ask stays at its bytes through the GO** (sha256 `692cce61ddf8`), and the `.tf` at `21a54e8f197eeea2`. If the catalog gains rows before the apply, the generator re-runs, the `.tf` changes, and this half does not carry: re-issue and re-sign.

**C2 -- one role at a time, in the ask's order** (`inf-orion`, `inf-eclipse`, `49f-blackdiamond`, `cot-commonwealth`, `cot-blackdiamond`, `smartx`), each through `safe-apply` targeted at that role and its policy (2 adds), then `get-role` and `get-role-policy` read back and compared with the plan. After the last, a re-plan of the six targets reads `No changes`.

**C3 -- the live Black Diamond and Schwab policy hashes are re-read after the last role and equal their before values.** Any change stops the act.

**C4 -- the ledger `nfra-oplgtw-grants-ap24`** is opened (entry AND sentinel) before the first apply and closed at the end; `W/GR_APPLIED.json` written. On any trigger failing, a failed role is destroyed and an ARMED row names this seat.

**C5 -- the IAM branch read:** `simulate-principal-policy` for at least one allowed prefix and one outside prefix per role (ONE resource per call), with the `*`-principal positive control in its own invocation, and an existence read of the exact prefix after each role exists.

**C6 -- no gateway deploy in this act, and the roles stay UNUSED until `OG-ap-23`** (the code with `OG-ch-1` keying the Black Diamond role by firm). No apply in any form before the three halves are signed and the GO names them.

## Not covered

- The code release (`OG-ap-23`), `OG-ch-1`, and the env values the host needs (`<KEY>_READER_ROLE_ARN`): the code batch carries them.
- The 49F live tables and Schwab `fact_*` (named gaps), and any change to the live Black Diamond or Schwab roles.

-- 2.0.0_SA_COO~O
