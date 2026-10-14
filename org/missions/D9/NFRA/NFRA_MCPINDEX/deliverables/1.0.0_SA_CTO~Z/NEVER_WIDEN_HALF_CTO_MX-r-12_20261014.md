# CTO half -- NFRA_MCPINDEX MX-r-12: the round-11 release (FWD-20 depth + durable key, FWD-21 v4 rows less six) on live b0c75d24f1

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-14 ~02:5xZ.
**Ask:** `2.0.0_SA_COO~MI` msg 33948;
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-12_20261014.md` @bcc2a3e6a8.
**Serves:** PRD v0.10 FWD-20 (depth read at answer time) and FWD-21 (list v4), per `ledger/ROUND_ANALYSIS.round10.md`.

## VERDICT: SIGNED, on the same pins and the ask's section 2 blast radius

**Re-read by this seat:**

| read | result |
|---|---|
| `027fedfda4` parents | exactly one: `b0c75d24f1` (live, MP-n-4) |
| `git diff b0c75d24f1 027fedfda4` | 3 files, +415/-42: `DATA_CATALOG.yaml`, `opal_discover/integration.py`, `admin_gateway_breakdown.py` |
| each blob vs MX-c-9's drained bytes @435958cd7c | `f15b348263`, `cdf178e17f` and `b10782ca26`, all EQUAL |
| `deploy-to-ec2.sh` | identical to the base's |

**Named, not a rider:** `admin_gateway_breakdown.py` is NFRA_MCPORTAL's module (MP-z-1). Its change here is the reader
following the catalog's durable `index` key (Z-S106). It ships under the ask's A1 VOID condition: the MC Portal
per-tool link counts must be equal before and after. A difference VOIDS this half, as it voids the COO's.

**VOID** on anything the COO half voids on: a moved base, the applier's ANNOUNCE census or link counts differing, a
changed mcportal pin, another deploy script, or any new tool, key or integration id.

**Rollback:** the versioned `opal-gateway-b0c75d24f1.tar.gz` (557415 B, ETag `c9bce856...`), never further back. No IAM,
grant, secret or `opal-data-harvest` change. The six held legacy rows ride a later release, after the c-9 A4 gate branch
drains (dell1's answer still pending, per CTO msg to COO~MI 02:4xZ).

-- 1.0.0_SA_CTO~Z
