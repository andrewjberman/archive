# RULING -- OA-t-6: the gateway release carries NFRA_OPALAI's change ONLY

**By:** `1.0.0_SA_CTO~O` (PRD owner). **On:** `2.0.0_SA_COO~O` msg 25815 and row NFRA_OPALAI-Z-W2-S3.
**Written:** 2026-09-25 ~00:3xZ.

## The situation, measured

Deployed commit `1764e54a16`. `git log 1764e54a16..HEAD -- infra/aws/ec2/opal-gateway` reads 7 commits:

| commit | project | what |
|---|---|---|
| cc22fdfb9d | NFRA_OPALAI | OA-t-5, the asker-scoped query tool |
| 650c9a99cb | NFRA_MCPINDEX | MX-c-2, silver dataset catalog entries |
| 6abf60e5d5, 8dce9aeb0b, e8f800e6a9 | MDPF_TAXSMA | TX-g-1, the `/ms/taxsma-workbook` route |
| 9e4074c33a, 6c37cc6b00 | NFRA_OPLGTW | OG-r-2 benchmark harness; OG-r-1 rollback-census amend |

## Ruling: option (b), narrow, never the coordinated release

1. **OA-t-6 deploys `1764e54a16` plus NFRA_OPALAI's own changes, and nothing else.** That is cc22fdfb9d plus OA-t-6's
   own `app/audit.py` `_ARGS_ALLOWLIST` hookup (amend e0137c7ece). It is built on a release branch cut at `1764e54a16`
   in the issuer's own worktree, with those changes applied by content. It is deployed with that worktree's copy of
   the deploy scripts, so their clean-tree check and commit read see the release tree, not the shared tree.
2. **The manifest records the release commit.** The deploy record also states in words that CLOUD HEAD holds the 5
   foreign commits above as unreleased.
3. **Why not the coordinated release:**
   - OG-r-2's cell closed with two FAILs standing (OGR2-AC2, OGR2-AC4).
   - NFRA_OPLGTW is under Andrew's 2026-09-22 stop ("do not go further with it"), so shipping its code is his word,
     not mine.
   - TX-g-1 is MDPF_TAXSMA's to release under its own gates and its own issuer (`2.0.0_SA_COO~T`).
   - MX-c-2 releases with NFRA_MCPINDEX's re-cut, beside MX-c-4, under that project's own order.
   - One release carrying four projects' unrelated changes would make every rollback reach all four.

## The CTO half of the release sign-off (CLAUDE.md NEVER-1: the blast radius, not the decision)

- **May touch:** the gateway process on its EC2 host. The new module `app/asker_scope.py`, one tool registration in
  `app/tools.py`, one `NATIVE_TOOLS` line in `app/data_entitlement.py`, and one `_ARGS_ALLOWLIST` row in
  `app/audit.py`. No other file changes against `1764e54a16`. No IAM, Terraform, ALB, secret or data write.
- **Served behaviour change:** one new tool, `opal_asker_query`, listed and callable. It is DARK for the concierge
  identity, which is not in its allowlist (row Z-S6). For any other caller it refuses an unprofiled asker before any
  read.
- **Both branches, per NEVER-1:** a caller with an active grant carrying `query` gets a catalog-gated read; every other
  caller gets a structured refusal. The existing 44 enabled tools are unchanged at the bytes.
- **Rollback, per key:** redeploy `1764e54a16`'s bytes through the same script. Whether that commit's artifact is
  rebuildable is OA-t-6's census to prove before the act, because NFRA_MCPINDEX recorded "the live Gateway has no
  valid rollback". If it cannot be proven, the deploy does not happen.
- **The standing hazard this does not remove:** any later deploy from CLOUD HEAD by any seat ships the 5 foreign
  commits. Row Z-W2-S3 carries it. Its owners are MDPF_TAXSMA's issuer (TX-g-1), Andrew (OPLGTW, his stop) and this
  program (MX-c-2).
