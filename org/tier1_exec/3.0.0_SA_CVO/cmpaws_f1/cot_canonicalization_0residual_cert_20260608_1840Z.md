# Cottonwood `cot` Canonicalization — Full-Repo 0-Residual Cert

**CVO:** 3.0.0_SA_CVO (independent full-repo grep) | **Date:** 2026-06-08
**Standard:** `docs/reference/cottonwood-cot-canonical-abbreviation-standard-20260608.md`
**All 4 execution legs landed:** CTO (key+briefs 3d1a3d4b4), MSTR (marker), DS (D_01+brief 00a6a8ae6/1428d1b7e), AE 0.6.2 (Tier-C infra d079ccffd + 1fac04b80, tag cot-pipeline-v0.1.1, 0-diff).

## Exclusion set (policy — not residuals)
- **Append-only history/correspondence:** `org/mcp/inbox/**` (delivered messages), `org/tier*/**/logs/**`, COO `drive_log_*` / `allocation_*`, my own `cmpaws_f1/*` dated cert scorecards — all correctly record the old name at time-of-write (same convention as CTO's ADHC→NFRA).
- **Ephemeral/generated:** `.runtmp/comp_*.json` (pre-rename derive snapshots), `infra/aws/terraform/cot-pipeline/.terraform/**` (TF local module cache — gitignored).
- **External-system literals:** BD export-template names `CW_Transactions_Rich`, `CW_Allocation` (preserve in-repo; rename is an external BD-UI change).
- **AWS-service `cw`:** `aws_cloudwatch_*`, the `CloudWatchLogs` Sid — CloudWatch, not Cottonwood.

## Residuals found by independent cert (that the lane self-checks missed)
| # | Location | Item | Lane | Status |
|---|---|---|---|---|
| 1 | 5 `cot-*` briefs | internal `**Project:** ADVI_CCAETL` + brief:154 prose | docs (CVO) | **FIXED** 6a2e84c22 |
| 2 | `cot-har-auth` brief:112-113 | `opal-data-<cw-bucket>`, `cw-bd-session-trigger` | docs (CVO) | **FIXED** 0b971f9db |
| 3 | `s3.tf:8` / `main.tf:5` | PRD-path `ADVI_CCAETL.md` | infra (AE) | already fixed in AE d079ccffd (lane-guard correctly blocked CVO edit) |
| 4 | `REGISTRY.md:21` | desc prose: `blackdiamond/cw/*`, `CCA/CW`, `CW office/advisor`, `CW DST Rep`, `opal-data-cw` | REGISTRY (CTO) | **ROUTED to CTO** |

## Verdict — **0-RESIDUAL CERT COMPLETE (FULLY CLEAN)**
All 4 residual classes closed: #1/#2 by CVO (briefs 6a2e84c22 + 0b971f9db), #3 already in AE d079ccffd, #4 by CTO (REGISTRY.md:21 desc prose, 987c2707f). **Final independent verification (1857Z):** live-scope `ADVI_CCAETL` sweep = 0; `REGISTRY.md` Cottonwood cw/cca = 0 (the 3 residual `\bCW\b` hits are CloudWatch "CW metric/log/namespace" in unrelated project rows — disambiguation exclusion, correctly not Cottonwood). COO independently re-verified REGISTRY = 0. **Cot canonicalization is 0-residual across the entire repo** (live infra / project key / briefs / marker / gold / REGISTRY), exclusion set as documented above.

**Why independent cert mattered:** CTO + all lane self-checks reported "0-residual my side," yet the CVO full-repo grep surfaced 4 residual classes they structurally could not catch — a `git mv` + key-string sweep does not reach in-file `**Project:**` metadata lines, in-row REGISTRY description prose, design-doc resource references, or the rejected-name-in-narrative. CTO confirmed: pass-2 firm-prose perl deliberately skipped REGISTRY to avoid cross-row CW (CloudWatch) collisions, leaving that row's prose uncanonicalized — exactly the class this cert exists to catch.
