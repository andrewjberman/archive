# PARKED -- stranded uncommitted edit to seed-etf-constituents.py (2026-09-29)

**Parked by:** `0.0.0_AB_MSTR~Z`, 2026-09-29 ~12:3xZ, on `2.0.0_SA_COO~Z` msg 26592 (row `AMGT_RESAPP-Z-S301`).
**Owner (lands it or discards it):** `1.0.0_SA_CTO~Z` -- author of the file (b3d830094c, ETFS_POSITIONING) and the
seat whose 2026-08-25 ruling the edit implements. Its original editor is unrecorded; the 2026-09-16 relaunch record
calls it "a DS edit" stranded at that reboot.

## What it is

`infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py`, 13 insertions / 6 deletions against HEAD:
1. `NAME_CORRECTIONS`: `CASH` -> "Cash & Cash Equivalents" (Andrew-direct 2026-08-25 canonical cash line, quoted in
   the edit's own comment); the `CASH&OTHER` row removed.
2. `batch.put_item`: drop empty-string values as well as `None` -- `sub_asset_class` backs a GSI and DynamoDB refuses
   an empty string for an indexed key ("measured: ValidationException on the first real write", per the edit).

## Why it was parked, not committed or discarded

Worker branch `wk-AMGT_RESAPP-172` @8757ce95eb (AMGT-ww-3, VALID 3 of 3) edits the same file, and git refused the drain
while this edit stood in the shared tree. The branch does NOT carry this change (it adds `--universe amgt-library`),
so the edit is unique content: it is preserved here, not superseded.

## Files and proof

- `PARKED_seed-etf-constituents_stranded_edit_20260929.patch` -- `git diff` against HEAD, 2396 bytes, sha256 prefix
  `00472a38a27a`. Proven before the restore: applied to HEAD's file it reproduces the edited file exactly (EOL-normalised).
- `PARKED_seed-etf-constituents_stranded_edit_20260929.full.py.txt` -- the edited file as it stood, sha256 prefix
  `ec46042e35ae`.
- The shared-tree file was then restored to HEAD (`git checkout -- <file>`); `git status` for it reads clean.

## To land it (owner)

After `wk-AMGT_RESAPP-172` drains, re-apply on the new HEAD (`git apply` this patch; the `put_item` hunk may need a
3-way apply if the drain touched `main()`), review, and commit under your serial.
