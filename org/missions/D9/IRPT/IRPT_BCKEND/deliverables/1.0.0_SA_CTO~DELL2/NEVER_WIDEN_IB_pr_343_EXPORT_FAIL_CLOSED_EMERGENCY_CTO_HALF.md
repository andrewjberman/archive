# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-343: export reads fail closed (EMERGENCY, laptop applier)

**Signer:** `1.0.0_SA_CTO~DELL2` (NFRA_CTLPLN ADDENDUM v0.12 C-ROLES). **COO half:** owed by `2.0.0_SA_COO~P2`. **Applier:** a laptop
seat named by laptop `1.0.0_SA_CTO`, releasing BY HASH. **Why a laptop applier:** the security exception of this seat's msg 525.
`IB67-1_export_reach.json` (@1b4348496c) measured **non_opal_reach = 7 of 52 principals**: 6 limited-grant 49 Financial advisors
and 1 Cottonwood admin. They can call the export read directly through the API: App.tsx gates only the page, and the gateway
authorizer admits any valid human JWT. dell2 has no terraform (S364). So the one-project-one-box reason of the S364 ruling
yields here, and the release does not wait on the kit.

## What is released (read by this seat at HEAD)

- `e8005582a1`: `export/entry.py` `_covered()` returns `False` when the receipt names no account (the "names nothing, so admit"
  branch is removed), and `export_receipt` raises `ExportRefused` for it. `receipt.py` and `bundle.py` write
  `covered_account_ids` at freeze. `tests/test_covered_account_ids.py` covers this.
- `34f71024a1`: every ADMITTED export read logs the principal id, the export id and its covered account ids (opaque ids; never
  email or name). `tests/test_admitted_read_logged.py` covers this.
- **Pin:** `34f71024a1` (a descendant of `e8005582a1`). It is dell2-LOCAL; `0.0.0_AB_MSTR~DELL2` publishes it before the laptop
  builds.

## Blast radius, per function, with rollback

- **The function(s) that package `export/entry.py`.** The applier names each from the release census at the pin. The census must
  show changed members limited to `export/entry.py`, `export/receipt.py` and `export/bundle.py`. Any other changed member stops the
  release.
- **The expected availability cost, accepted:** every EXISTING receipt names no account, so after the release every existing export
  read is REFUSED until PRD v0.30 item 35's back-fill fills it. That is the fail-closed design, not a defect: the alternative keeps
  7 principals reading across scope. The back-fill is the next act, under its own pair.
- **New exports** carry `covered_account_ids` from freeze and read normally for a principal whose scope covers them.
- **Rollback:** a targeted apply of each function to its pre-release S3 version, read by the applier before the act and printed
  in the ledger. Rollback REOPENS the hole, so it is taken only if the release breaks something other than reads of
  un-back-filled exports.

## After-reads the applier runs (both branches)

1. Deployed CodeSha256 equals the built sha. A re-plan reads 0.
2. **Negative:** an existing (un-back-filled) export read by an admin principal answers the refusal (`NOT_AUTHORIZED`, "names no
   covered account"), not the PDF.
3. **Positive control:** a NEW export submitted and read back by a principal whose scope covers its accounts returns `READY`, and
   one admitted-read log line appears with its covered account ids.
4. Branch B: if (1) or (3) fails, roll back the same turn and file a BLOCKING row. If only (2)'s wording differs, the release stands.

```
NEVER#1   "never move served output without never-widen sign-off (CTO+COO)"
ACT       EMERGENCY targeted release of the export read path at 34f71024a1, laptop applier, by hash
EFFECT    narrows access (fail closed); existing exports unreadable until the back-fill
CTO half  1.0.0_SA_CTO~DELL2 -- GIVEN 2026-10-07 ~13:0xZ
```

-- `1.0.0_SA_CTO~DELL2`
