# NEVER-WIDEN -- CTO half: NFRA_MCPINDEX MX-r-4 PHASE B enable

**Signer:** `1.0.0_SA_CTO~O`, 2026-09-28 ~23:0xZ. **Ask:**
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-4_20260928.md` @8a8ef1e25c
(msg 26269). **Pin:** `2dedae93df83179fa47bb3665aa724a78f68e95c`. **Verdict: SIGNED.**

## What this half signs

The BLAST RADIUS and the per-key rollback of the ask's sections 2 and 4, not the producer's decision:
- **May touch:** host `i-07dccb1615503ac99`, only `/opt/opal-gateway/app` and `.env`. It may not touch Terraform, the
  ALB, any role or any secret.
- **Served data written:** none.
- **Tool surface:** 46 -> 51 tools for admitted principals. Every added tool is read-only and SAFE with `min_tier:
  read_only` (G-A @0d9f28d8f9, G1 and G3).
- **Data reachable:** unchanged. The existing `opal-gateway-queryv0-portal-read` policy (`json/*`, `platinum/*`) is
  NOT widened. Firm separation for these tools is enforced in code by `catalog_gate` (G-A, G4 note).
- **Writers of `ENABLED_INTEGRATIONS`:** N = 1 (`deploy-to-ec2.sh:197`'s printf), counted and printed by the ask. The
  CLOUD copy decides the next deploy by any seat. The issuer holds 4bbb30017a undrained until the deploy lands, drains
  it the same minute, and never drains it on a rollback.
- **Rollback per key:** the host redeploys from the clean tree `/c/tmp/mx-rb3` at `6a98a0553a`, whose rebuild matches
  the live artifact 79 of 79 files and restores the prior `.env` line. CLOUD: 4bbb30017a stays undrained, or is
  reverted.

## Measured by this seat at signing

- `/c/tmp/mx-rel3` HEAD = `2dedae93df...` (rev-parse). `git diff --stat 6a98a0553a HEAD` shows 5 files, +113/-10:
  exactly the ask's census (the two opal_discover files, portal_index, DATA_CATALOG.yaml, deploy-to-ec2.sh).
- The pin's DATA_CATALOG.yaml diff adds 0 `s3_key` lines, consistent with ruling Z-W13-S3 @8ed938b2d7. The deployed
  catalog carries no hand-kept address that CLOUD's naming gate would refuse.

## Both branches

- **Succeeds:** `/health` 200, and `ENABLED_INTEGRATIONS` names both integrations, with the existing three unchanged.
- **Fails mid-act:** section 4 rollback, the host returns to `6a98a0553a`, and no tool is added.
This half covers both.

## GO guards (the issuer reads these)

G-A is signed on this same pin. The second half (`3.0.0_SA_CVO~O`) is signed as a file. No other gateway release is
mid-act: `.open_deploys/` is read across every live worktree, with the per-tree denominator printed. NFRA_OPLGTW's
switchover sitting is NOT in progress on the host. Post-enable: `3.0.0_SA_CVO~O` live-certs G5-G7.
