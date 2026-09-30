# MX-r-6 v2 -- G-A and the CTO never-widen half SIGNED (the Schwab enable release, on live 288fa78c93)

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-30 ~13:3xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-6_v2_20260930.md`
@17259505a2 (msg 27178).
**Supersedes** this seat's VOID v1 half, `G-A_AND_NEVER_WIDEN_CTO_HALF_MX-r-6_20260930.md` (@37b1a21c71, voided
@9e7a0e72f0).
**Grounds:**
- rulings B1, B2, B4 and B7 of `REINSTATE_RULINGS_20260930.md` @4e598ab7be;
- Andrew-direct `ANDREW_DIRECT_20260930_13xxZ_R20_ETFS_BDFEES_YES_SCHWAB_GRANT_YES_ADVI_LIFTED.md` @1eba868308 for the
  one grant widening (A5).

**Pin:**

| part | hash |
|---|---|
| release | `63d6094823` |
| deploy-only | `2e2254156e` |
| gateway tree | `bf741bd45a6fd86ba1f0ee2509c8bf861d761bb2` |
| base live | `288fa78c93` |

**Verdict: G-A PASSES, and the CTO half is SIGNED on this pin only.**

## The live base, measured by THIS seat (the v1 miss, not repeated)

- **S3 at ~13:3xZ,** `opal-313476888478-lambda-artifacts/ec2/opal-gateway/`, sorted by LastModified:
  - `opal-gateway-288fa78c93.tar.gz` (11:37:11Z) and `opal-gateway-latest.tar.gz` (11:37:13Z) share ETag
    `be161c825e92471afe31c9f6ba4f3758`;
  - no key is newer;
  - `093fc247c6` (09-29 10:11Z) is the prior release.
- The live artifact is therefore `288fa78c93`.

## Measured by this seat against that base

- **Tree equality:** `infra/aws/ec2/opal-gateway` is tree `bf741bd45a` at BOTH `63d6094823` and `2e2254156e`. The
  live base's tree is `e298beb2ac`.
- **The diff against live `288fa78c93`** is 21 files, +998 -43:
  - the same Schwab/MX-q-3 product set as the signed-then-voided v1 delta;
  - `deploy/NFRA_OPLGTW_CONTRACT.json`, which is new;
  - 10 test files.
  - No MCPMSP file appears in the diff.
- **MCPMSP preserved:**
  - `app/tenant_registry.py` (blob `6876b359`) and `app/firm_role.py` (blob `0ff54e33`) are byte-identical in live and
    in the release.
  - The release's `deploy-to-ec2.sh` keeps `FIRM_ROLE_ARNS={"inflection": ".../gateway-inf-firm-reader-role"}` and adds
    `schwab` to `ENABLED_INTEGRATIONS`.
- **The IAM leg** is terraform-only and targeted to `aws_iam_role_policy.schwab_data_read_policy`. It is re-planned at
  the GO. The half is CONDITIONAL on 0 add, 1 change, 0 destroy: the 8 `dim_transaction` elements for masters
  08242234 and 08335338, and nothing removed.

## What this half covers

- The IAM change, the host deploy from `2e2254156e` (artifact `opal-gateway-2e2254156e.tar.gz`), the `.env` going from
  28 to 33 keys with MCPMSP's line kept, and the served tools moving from 52 to 58.
- **The ONE grant widening (A5)** on Andrew's word: one existing principal's Schwab grant gains `dim_transaction`
  through the grant admin tool, recorded before and after, with the prior grant as the rollback.
- The rollback per key in the ask's section 2: the IAM rollback file re-applied targeted, and a redeploy from
  `/c/tmp/mx-rb8`, 82 of 82 equal to live `288fa78c93`.
- **Both branches of every leg:**
  - the base differs at the GO: VOID, no act;
  - the plan is not 0/1/0: no apply, and a BLOCKING row;
  - the apply fails: no deploy, and the IAM rollback;
  - the deploy or read-back fails: redeploy `/c/tmp/mx-rb8` and the IAM rollback, with the ledger closed ROLLED-BACK;
  - the grant tool refuses: no grant change, and the A2 refusal stands;
  - never half-landed (CLAUDE.md NEVER-2).

## What it does NOT cover

- An untargeted apply, or any other IAM resource.
- A changed pin, or a live base other than `288fa78c93` at the GO.
- Any second grant, a new identity, or a new principal.
- The ETF and BD tools (MX-t-10, MX-t-13, MX-r-7), which are held on the naming-gate edit.

**GO guards:**
- The GO re-reads the live artifact.
- The NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable` is opened before the first act.
- 3.0.0_SA_CVO~O's second half is signed on this same pin.
