# NEVER-WIDEN SIGN-OFF -- CTO HALF -- irpt-ycharts-generate RELEASE 6 (the custody factory: a Performance client statement is accepted)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~03:2xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 2265 (READ-acked)
**Signed against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release6_custody/NEVER_WIDEN_PAIR_RELEASE6_CUSTODY.md`,
**blob a3c54ba263** (@4bd8f7bc3c). Pin `bea2a2ceb3`.

## Measured by this seat

| Read | Result |
|---|---|
| `release-census.py irpt-ycharts-generate --pin bea2a2ceb3` | 104 built, 100 live, `changed_members=11`: 7 changed (composition, ExportBundle.schema.json, custody_submission, generate_installed, reporting_policies.json, repository, retention) and 4 added (custody_interpreter, custody_ports, holdings_publication, holdings_publication_port). Equals the packet |
| pin on origin | `bea2a2ceb3` is an ancestor of fetched origin box/dell2 |
| live `get-function-configuration` | `Un0wVZqj...` (release 3, 01:52:26Z). **Release 5b has NOT landed.** This half's precondition 1 holds the apply |

## Blast radius signed

- **ONE function, 11 members, plus one layer** (`AWSSDKPandas-Python312:16`).
- **ONE new inline role policy:** `irpt-ycharts-generate-custody-factory-policy`, named from `name()`. It has 3 statements over 11 ARNs, exactly as the
  packet's table renders them:
  - GetObjectVersion on cottonwood's BD silver `fact_holdings` and `fact_allocations` only;
  - Get and GetVersion on the three firms' pinned holdings publication only, with no List and no Put;
  - Put, Get and GetVersion on the three firms' `custody_reports/*` only.
  - No KMS grant (SSE-S3).
  - No new principal class and no new route.
- **This IAM write is dell2's own under step F.** It is reported after the fact through MSTR~DELL2: the name plus the 11 ARNs.
- **Branch B** is as the packet states: roll back to 5b's build, remove the policy and the layer by a targeted revert apply, then clean up and file a
  BLOCKING row. Read the failing call's CloudWatch line before halting.

## Preconditions and conditions

1. **Release 5b is live (`5FRkux2o...`) before this pair starts.** Its rollback target is 5b's build, not release 3.
2. **The symbol closure is re-run on the UPLOADED zip**, with `missing=0`, and the 2 optional fallbacks are named. The import census gates every
   later read.
3. **The policy reads back with exactly the 11 ARNs.** One more is a STOP.
4. **Cleanup:** read 3's objects under `custody_reports/` are listed by version and named. Their S3 deletes are Andrew's act per object (CLAUDE.md
   Agent Autonomy).

## Section 5's principal (msg 2124), NAMED

IRPT_CUSTDY E2a's scoped POST uses a **new service principal `svc-custody-statement`, with `allowedFirmIds = [cottonwood]` only** (E2a's firm).
- It follows the svc-analyst-intake and svc-commentary pattern: a token in Secrets Manager, CREATE-scoped to the statement route.
- It is minted under its own never-widen pair, drafted by IRPT_CUSTDY's issuer `2.0.0_SA_COO~K2`.
- **Release 6 grants it nothing.** E2a runs only after both release 6 and that mint have landed.

**Verdict: GIVEN**, for exactly these 11 members, the one policy and the one layer at `bea2a2ceb3`, after release 5b.

-- 1.0.0_SA_CTO~DELL2
