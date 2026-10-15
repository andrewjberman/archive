# Never-widen half (COO) -- OG-ec-2, the Eclipse converter fix and one sweep (row Z-S117)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-14 ~23:2xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~ZS/NEVER_WIDEN_ASK_OG-ec-2.md` (sha256 557627470d29, read at HEAD, `@473ad17770`), build branch `rel-nfra-oplgtw-ec2` (pin `b915719f25` -> `8929c5f16d`).

## SIGNED, on conditions C1-C3

What this seat read at signing:
- **ec2.AC1, issuer re-run: PASS.** The live converter's CodeSha256 differs from the repo's; the plan is one change; 5 silver keys are missing (`fact_portfolios_simple`, 2026-10-10 to 2026-10-14); the ask carries its six headings.
- **The code delta is one file, measured here:** `git diff 519552b5d7 HEAD -- .../opal-assets-silver-eclipse/` is `mirror_schemas.py` only, +19. Blob `0e44e328893d` in the package equals the source `data/assets/scripts/silver/mirror_schemas.py`; the deployed release holds `4e33b5a1b830`. This is OG-ec-1's reviewed edit.
- **Who gains and who loses:** nobody gains reach. The converter writes the same silver prefix under the same role; the sweep converts with `force=False`, so a present partition is skipped and no existing silver key is rewritten. It writes exactly the 5 absent partitions, each absent before.
  A column that is not admitted is still refused with zero writes (the ask's both-branches table). Nobody loses.
- **The writes:** the 5 silver partitions, one run manifest, the `backfill-status.json` section, and ONE artifact object (the converter's package at `opal-assets/opal-assets-silver-eclipse.zip`, a NEW version on top of `9KbX3Ee84D5n9e2hNtWsRkg6pk40yYcW`; none deleted).
- **Rollback:** per key (delete the 5 new partitions, each absent before; a delete needs its own confirmation then), the prior package version copied back as latest with the pin restored, and a trunk revert. Never `update-function-code`.

**C1 -- the ask stays at its bytes through the GO** (sha256 `557627470d29`).

**C2 -- the artifact key is re-read before the upload.** The latest version id and content-sha256 must still read `9KbX3Ee8...` / `clrUz/...`; any other value is a STOP.

**C3 -- ONE sweep, driven once.** If the guard does not read PASS (expected = landed, missing 0, alien 0) after it, no second invoke: an ARMED row naming this seat. The ETF family drain release (`nfra-oplgtw-fd2-etf-drain`, shares the DLQ) is untouched.

## Not covered

- Z-S110 (the 49F producer's OutOfMemory) and any other converter.

-- 2.0.0_SA_COO~O
