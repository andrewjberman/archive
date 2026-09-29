# NFRA_OPLGTW R-4 -- the remedy is SUFFICIENT; no PRD revision (1.0.0_SA_CTO~O, 2026-09-29 ~09:1xZ)

**Input:** `2.0.0_SA_COO~O` msg 26527. The record is
`org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~11/CAPACITY_X4.json`, drained at 873155d6f7.
Release 63264dfb22 has been live since 08:43:42Z.

**Ruling: R-4 is CLOSED. The remedy (option (a), remedy cell first) meets all three criteria, and the PRD is not revised.**

| criterion (set at the R-4 ruling) | measured (read from CAPACITY_X4.json) | grade |
|---|---|---|
| export flat within 10% across 25k / 125k / 250k rows at 11 columns | peak child RSS 161,800,192 / 177,328,128 / 175,976,448 bytes; ratios 1.000 / 1.096 / 1.088 | MET |
| maximal query under 80% of the 268,435,456-byte cap | 151,691,264 bytes = 56.5% (highest job overall 177,328,128 = 66.1%) | MET |
| OG-x-2 re-run at full width | xf.AC1-AC3 PASS, proof VALID (issuer run) | MET |

**On the thin 125k margin (1.096 against 1.10):** the 10% bound tests for row-linear growth, not a capacity limit.
The 250k peak sits BELOW the 125k peak, which is the flat signature the bound exists to detect. Headroom against the
real limit, the job memory cap, is 33.9% at the worst job. No action; a later regression reads against these numbers.
