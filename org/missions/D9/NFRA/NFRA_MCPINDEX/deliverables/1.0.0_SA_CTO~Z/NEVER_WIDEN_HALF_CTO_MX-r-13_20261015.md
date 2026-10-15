# Never-widen half (CTO) -- NFRA_MCPINDEX MX-r-13: the round 13, 14 and 16 catalog release (two files)

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~06:2xZ. **SIGNED, on the same pins as the COO half.**

**Against:** `deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-13_20261015.md` @10fb65f08c, sha256 `c72254d68b8cd255...`.
**Pinned to:** deploy-only commit `d020bee315` (single parent = live `ee23dd004c`); blobs `11620b3c52` (DATA_CATALOG.yaml)
and `f3cf344cc3` (opal_discover/integration.py); rollback artifact `opal-gateway-ee23dd004c.tar.gz` (ETag `159fa4ea...`).
VOID on any of the COO half's conditions: a moved base, a changed pin, another deploy script, a new tool, key or
integration id, a third file, or any census difference except the link counts at 33 / 112.

## What I read
- `git diff --stat ee23dd004c d020bee315`: 2 files, +19951 -648, the two named. No IAM, grant, key or tool change: the
  tools stay 93, `.env` 57, integrations 7.
- **A content screen the ask did not carry, because the catalog is SERVED to every Opal user through `opal_discover`:** every
  8+-digit number in the shipped catalog (436 lines) was classed. They are byte and row counts, the AWS account id, and
  the three Schwab MASTER ids (firm-level, already in served prefixes and the registry). **No client account number.**
  Firm names appear as fork-key values, joined from the registry, which is the firm fork Andrew asked for and not client
  data.

## The link-count difference
EXPECTED, as the issuer ruled: 11 tools / 14 links -> 33 / 112. These are catalog rows now naming tools the gateway
already serves (the ten harvest, the news and the portal tools live since OG-ap-18/19). The reader blob is unchanged and
no access widens. MP-z-6 is staged, not started.

## Rollback
Redeploy the versioned `opal-gateway-ee23dd004c.tar.gz`; `-latest` re-points. Never roll back past `ee23dd004c`.
