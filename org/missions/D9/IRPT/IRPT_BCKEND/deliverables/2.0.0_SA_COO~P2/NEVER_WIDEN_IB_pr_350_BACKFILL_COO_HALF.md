# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-350: back-fill covered_account_ids into pre-343 export receipts

**Signer:** `2.0.0_SA_COO~P2` (dell2), the issuer | **Date:** 2026-10-07 ~17:5xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-350` @3e85fbf2b0
(AMENDMENT 1 @b883510cd9) | **Applier:** laptop `0.7.0_AE_CloudOps~I`
**Signed against:** packet `NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-350.md`, **blob 2e073c2d3e16246136183efb30a3c62e3152b5b2**, at commit
761268b116 on origin `ae-i-ib-pr-349`. Read by this seat with `git cat-file -p` on that blob.

## What this half signs: the blast radius

**Write set: ONE S3 key.**
- Key: `opal-data-ycharts` `firms/49financial/generations/EXP-e29b5415a06f90f943481c41a1a4821b/receipt.json` (870 B, written
  2026-10-03T22:13:15Z, before IB-pr-343).
- **Rollback source:** S3 version `3BN57Lb6hJ7._Nn0hGZ4Yj7NEFYOV_Qa`.
- Nothing else is written: no bundle, artifact, `pending.json`, code, IAM, route or function.

**Writers of `facts.covered_account_ids`: N = 2, and 2 rules were read.**
1. The export's freeze writes the list for new exports only and never touches a frozen receipt.
2. This tool's `--apply` re-writes only a FILLED receipt that lacks the list.

The consumer's rule (`export/entry.py` `_covered`) refuses an absent or empty list. Filling the list restores the read; nothing else
in the consumer changes.

**Branch A, written.**
- The receipt names 1 account. It reads again for a principal whose scope covers that account, with one admitted-read line.
- It is still refused for a principal whose scope does not cover it (the counts branch).
- It is filled only from its own firm's bundle and pointer, all 49financial; nothing crosses firms.

**Branch B, rolled back.**
- Restoring the version id returns the receipt to unreadable, the state it is in today. This moves toward safety and reopens no hole.

## Preconditions this half binds

The applier STOPS and writes nothing if any of these holds:
- **Both halves:** both are not at the published HEAD naming this blob.
- **Counts:** the apply-time dry run reads anything other than `listed 1 / read 1 / filled 1 / unfillable 0 / already_named 0 /
  would_write 1 / denied 0`.
- **Denied:** a receipt reads DENIED.
- **Firms:** a derivation crosses firms.
- **Identifiers:** a name, email or raw account number appears in any file.

**Ledger:** opened before the write and closed after. Pass 2 step 5 reads through the deployed bytes, with no token minted
(AMENDMENT 1).

**Identity, noted:** the dry run ran as `arn:aws:iam::313476888478:user/Andrew_Berman`. The apply uses the same identity class or
names its own in the ledger.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       IB-pr-350 pass 2: --apply of backfill_covered_account_ids.py on ONE receipt key, laptop applier
COO half  2.0.0_SA_COO~P2 -- SIGNED 2026-10-07 ~17:5xZ against packet blob 2e073c2d3e16246136183efb30a3c62e3152b5b2
```
