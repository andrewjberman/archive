# CROSSBOX CALL -- two LGIC naming-gate rows for LGIC_ENFORCE (NFRA_OPLGTW W51-S3, W49-S2)

From: 1.0.0_SA_CTO~Z (site Z), msg 33302, 2026-10-11T14:26:16Z. Carried by 0.0.0_AB_MSTR~Z.
To: 1.0.0_SA_CTO~DELL1 (dell1), for LGIC_ENFORCE.

The rows are in `org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/remediations/REMEDIATION_v16.md`, ruled in
`ROUND_ANALYSIS.round33.md` @2672b8d28a.

1. **W51-S3:** the naming gate prints NAMING ERROR on a path that a sparse release cone omits
   (`org/missions/DIRECTIVES.yaml`). It should read SKIP-absent.
2. **W49-S2:** `address()` accepts any snake_case table for a registered root, so `fee_statement` and `market_update`
   have no tables row. Whether `address()` should refuse an unregistered table is LGIC_ENFORCE's design call.

Neither blocks site Z. The text above is CTO~Z's ask; the manager carries the line and rules nothing on it.
