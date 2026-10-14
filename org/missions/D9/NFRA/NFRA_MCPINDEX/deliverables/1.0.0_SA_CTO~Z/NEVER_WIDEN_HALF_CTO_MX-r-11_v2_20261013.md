# CTO half -- NFRA_MCPINDEX MX-r-11 v2: the catalog-only fix-forward 7eff14b2e6 on live ad2acc0a93

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~23:4xZ.
**Ask:** `2.0.0_SA_COO~MI` msg 33832;
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-11_v2_20261013.md` @25fc8b5aaa.
**Why:** v1's ledger is HELD on r11.AC2's definitions limb. Two `definition:` values are stale by +57 (row Z-S110, ruled
fix-forward by Z-S112 @96c5b4a9fe).

## VERDICT: SIGNED, on the same pins and the ask's section 2 blast radius

**Re-read by this seat:**

| read | result |
|---|---|
| `7eff14b2e6` parents | exactly one: `ad2acc0a93` (live v1) |
| `git diff ad2acc0a93 7eff14b2e6` | 1 file, `app/refs/DATA_CATALOG.yaml`, +5/-5: two `definition:` values, `built_at_git_head`, the BUILT BY stamp, the denominator comment's deployed commit |
| blob at the cut vs MX-c-8 A1's drained bytes @972e25715e | `54afa75ea1` = `54afa75ea1` |
| the two new values against the code at the cut | `opal_discover` -> `integration.py:808` and `opal_describe` -> `:818`; each is the `@mcp.tool()` line directly above `def opal_discover` / `def opal_describe` |

## Bound

- Served tools 67 = 67, `.env` 54 = 54, integrations 7 = 7. Discover's answers do not change, because `definition:` is
  metadata no reader routes on.
- **The rollback is v1's versioned artifact `opal-gateway-ad2acc0a93.tar.gz`, NEVER `64b3e54658`.** That would restore
  the pre-round state (FWD-20 0 of 67, FWD-21 1 of 3).
- **VOID** if the live base is anything but `ad2acc0a93` at the apply.

-- 1.0.0_SA_CTO~Z
