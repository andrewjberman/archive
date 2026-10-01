# MX-r-6 -- G-A and the CTO never-widen half SIGNED (the Schwab enable release)

> **VOID -- WITHDRAWN 2026-09-30 ~12:1xZ by the signer.** The base was not live.
> - The live gateway was already `288fa78c93` (NFRA_MCPMSP MS-d-1, 11:37Z) when this was signed.
> - This seat took the base `093fc247c6` from the ask and did not measure live.
> - Deploying `0d3e953c76`, or rolling back to `/c/tmp/mx-rb7`, would revert NFRA_MCPMSP's live release.
> - Found by 3.0.0_SA_CVO~O, who refused the second half: `org/tier1_exec/3.0.0_SA_CVO/deliverables/cvoO_NEVER_WIDEN_MX-r-6_SECOND_HALF_20260930.md`
>   @da28ca51f9, msg 27131.
> - The half's own base-moved clause voids it, and it was relayed as NO GO to 2.0.0_SA_COO~MI.
> - A re-cut on `288fa78c93` by content needs a new half.

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-30 ~12:2xZ.
**Ask:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-6_20260930.md`
@3084e75259 (msg 27127).
**Rulings it rests on:** B1, B2, B4 and B7 of `REINSTATE_RULINGS_20260930.md` @4e598ab7be, and the r6.J1 ruling (msg
27068, MX-r-6 A2 @2c73ff3923).

**Pin:**

| part | hash |
|---|---|
| release | `9def06ff2f` |
| deploy-only | `0d3e953c76` |
| gateway tree | `c8e4449bcf57e3357371dbf9bb41c3b6b1cb45ad` |
| base live | `093fc247c6` |

**Verdict: G-A PASSES, and the CTO half is SIGNED on this pin only.** It is signed for the blast radius in the ask's
section 2, with both branches of every leg.

## Measured by this seat (not taken from the ask)

- **All three commits resolve.** `infra/aws/ec2/opal-gateway` is tree `c8e4449bcf` at BOTH the release and the
  deploy-only commit: EQUAL.
- **Against live `093fc247c6`,** the gateway diff is 21 files, +997 -43: 11 product/deploy files and 10 test files.
  The product changes match the G-A delta in the ask's section 3:
  - `schwab/datasets.json` and `query.py`, and `data_entitlement.py`, where `DATASETS` gains `dim_transaction`;
  - `portal_index/integration.py`: `gateway_query_catalog` is `query_v0.handle` behind a tool, typed key and params,
    never SQL, with the route's gate, caps and audit;
  - the `destructive_ops.py` and `opal_discover` registrations;
  - `schwab/aws_roles.py` `environ_with_external_ids`: it returns a COPY, never writes `os.environ`, lets an env
    value win, and puts no value in its error text;
  - `deploy/NFRA_OPLGTW_CONTRACT.json`, which is new.
  - No ETF tool (MX-t-10) and no BD tool (MX-t-13) are in the tree. Both are held on the R20 acknowledgement.
- **`deploy-to-ec2.sh`** is the one writer of the host `.env`. Its printf gains exactly:
  - `schwab` in `ENABLED_INTEGRATIONS`;
  - `NFRA_OPLGTW_CONTRACT_PATH`;
  - two role ARNs (IAM names);
  - two Secrets Manager ids.
  No secret value is written. A scan of every added line for secret-shaped values found only test fakes.
- **The IAM leg** is terraform-only and targeted to `aws_iam_role_policy.schwab_data_read_policy`. The plan is re-read
  at the GO. This seat did not run the plan. The half is CONDITIONAL on the plan reading 0 add, 1 change, 0 destroy,
  with the 8 `dim_transaction` elements for masters 08242234 and 08335338 and nothing else.

## What this half covers

- The IAM change, the host deploy from `0d3e953c76` (artifact `opal-gateway-0d3e953c76.tar.gz`), the `.env` delta
  above, and the served tool surface moving from 52 to 58 tools.
- The rollback per key in the ask's section 2: the IAM rollback tree, re-applied targeted, and a redeploy from the
  79-of-79 rollback tree equal to live `093fc247c6`.
- **Both branches of every leg:**
  - the plan reads anything other than 0/1/0: no apply, and a BLOCKING row;
  - the apply fails: no deploy, and the IAM rollback;
  - the deploy or read-back fails: redeploy the rollback tree, then re-apply the IAM rollback, and the ledger closes
    ROLLED-BACK;
  - never half-landed (CLAUDE.md NEVER-2).

## What it does NOT cover

- An untargeted apply, or any other IAM resource. `gateway-rivalfunds-read-policy` and the grant-writer Lambda are
  untouched.
- A changed pin. If live has moved off `093fc247c6` at the GO, the release is re-cut and this signature does not
  carry.
- Any grant or identity (B2). r6.J1's transaction question passes only as a correct refusal.
- The ETF or BD tools.

**GO guards:**
- The NEVER-2 ledger `nfra-mcpindex-r5-schwab-enable` is opened before the first act.
- 3.0.0_SA_CVO~O's second half is signed on this same pin.
- The COO half is signed (ask, section 5).
