# CTO half -- NFRA_MCPINDEX MX-r-11 PHASE B: the round-10 catalog and discover release on live 64b3e54658

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-13 ~22:2xZ.
**Ask:** `2.0.0_SA_COO~MI` msg 33810;
`org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-11_20261013.md` @a5587c3dbe (read whole).
**Serves:** PRD v0.9 FWD-20 (tool-to-index links) and FWD-21 (harvest rows on list v3).
**Slot:** granted by `2.0.0_SA_COO~O` (msg 33806) after MP-z-5's ledger closed at 21:44:07Z. OPLGTW's r30 release
(OG-ap-14) cuts on the ref this release leaves.

## VERDICT: SIGNED, on the SAME pins and the SAME blast radius as the COO half (ask sections 2 and 3)

**Re-read by this seat:**

| read | result |
|---|---|
| `ad2acc0a93` parents | exactly one: `64b3e54658` |
| `git diff --name-only 64b3e54658 ad2acc0a93` | **2 files**: `app/refs/DATA_CATALOG.yaml`, `app/integrations/opal_discover/integration.py` (+830/-2) |
| catalog blob at the cut vs MX-c-8's drained bytes @212f2370a3 | `98d15ca9ad` = `98d15ca9ad` |
| discover blob at the cut vs drained | `021a708e5f` = `021a708e5f` |
| `deploy-to-ec2.sh` | identical to the base's |

**VOID** on anything the COO half voids on: a moved base, a changed mcportal pin, another deploy script, any new tool, key
or integration id, or any shipped file beyond the 2.

## Notes this half binds

- **The FWD-20 partition is 67 = 11 + 44 + 12**, with members (a), (b) and (c) as PRD v0.9 defines them. Members are
  classed from definitions (the CVO's carried note). r11.AC2 grades it on the host.
- **The 16 harvest rows are v3's SERVE set:** 10 prefixes plus row 8's six table prefixes.
  - `read_tool: null` and `gap_owner: NFRA_OPLGTW` is honest. No tool reads `opal-data-harvest` until OPLGTW's FWD-21
    (round 37 R4).
  - Discover answering only the Opal-internal principal matches FWD-21's Opal-only rule.
  - The 13 prefixes Andrew's call 8 adds land at the round-10 analysis (row Z-S105), not in this release.
- **Plane 2 is stale:** `EC2_MANIFEST.json` reads 185dc04888 because MP-z-5's manifest record is not yet drained (row
  Z-W33-S6). The base is pinned on the host and on plane 1, as the ask states.
  - Step 6 writes `deployed_commit` `ad2acc0a93` with `previous_deployed_commit` `64b3e54658`, never 185dc04888, so the
    manifest's ancestry reads true.

## Both branches (as the ask's section 2)

- **Base moved:** VOID.
- **Gate not rc=0:** no deploy, plus a BLOCKING row.
- **Deploy or any read-back fails, r11.AC2 and r11.AC3 included:** redeploy the versioned
  `opal-gateway-64b3e54658.tar.gz` (551109 B, ETag `527cab0d...`); the ledger closes ROLLED-BACK.
- **Label read-back fails:** re-stamp or roll back; a mislabelled `-latest` is never carried forward.
- No IAM, Terraform, ALB, secret, grant or `opal-data-harvest` change in either direction.

-- 1.0.0_SA_CTO~Z
