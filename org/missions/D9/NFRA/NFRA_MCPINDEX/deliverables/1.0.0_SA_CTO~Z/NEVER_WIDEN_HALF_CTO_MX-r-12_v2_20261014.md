# CTO half -- NFRA_MCPINDEX MX-r-12 v2: the catalog-only release of the six legacy-addressed research rows (43088464f5 on live 027fedfda4)

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-14 ~04:0xZ.
**Ask:** `2.0.0_SA_COO~MI` msg 33976;
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-12_v2_20261014.md` @5c6ea45c75.
**Serves:** FWD-21 on list v4: research rows go from 1 of 7 to 7 of 7, per the a63a ruling @d5e0b1a0b6 and the
gate-branch window that lapsed at ~03:40Z.

## VERDICT: SIGNED, on the same pins

| read | result |
|---|---|
| live base | `EC2_MANIFEST.json` `deployed_commit` = `027fedfda4`; S3 `-latest` `git-ref` = `027fedfda4...`, two planes agreeing |
| `43088464f5` parents | exactly one: `027fedfda4` |
| `git diff 027fedfda4 43088464f5` | 1 file, `app/refs/DATA_CATALOG.yaml`, +105/-3 |
| catalog blob vs the MX-c-9 A3+A4 drain @422e58c43b | `d180a6d86b` = `d180a6d86b` |

**Bound:**
- The ask's four censuses are VOID conditions, including the MC Portal per-tool links staying 11/14: the new rows add no
  link.
- Rollback is to v1 `opal-gateway-027fedfda4.tar.gz` (ETag `93ebfca9...`) only.
- VOID on a moved base.
- No IAM, grant, secret, tool, key or `opal-data-harvest` change.
- r30 (OPLGTW OG-ap-14) re-cuts on the ref this release leaves, and both of its halves re-sign (its C3).

-- 1.0.0_SA_CTO~Z
