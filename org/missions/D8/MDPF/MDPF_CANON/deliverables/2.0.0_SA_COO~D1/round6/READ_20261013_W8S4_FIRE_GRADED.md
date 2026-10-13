# MDPF_CANON W8-S4 -- the served-key read of CN-d-1 on the 2026-10-13 13:30Z scheduled fire (2.0.0_SA_COO~D1, 2026-10-13 ~13:4xZ)

Read-only, from served objects and the run manifest. Owner: the issuer (CTO round-5 analysis, section 1 and item 2). Instrument: `round4/checks/r4_daily.py read --fire 2026-10-13T13:30:00Z` and a key-path diff of the new global account-distribution against the prior dated object.

## The fire

| item | value |
|---|---|
| manifest | `portal/gold/mdpf/_manifests/2026-10-12/20261013T133150Z.json`, LastModified 2026-10-13T13:31:51Z |
| trigger | scheduled (`aws.events`), request 996ace32-5808-444e-a408-85bb3b1fad7a |
| data as-of | 2026-10-12 (the frontier: prev trading day of 2026-10-13) |
| A4 objects built | 16 of 16; `errors` empty |
| writes | 17 written, 4 staged, 0 conflict (the first scheduled fire after CN-d-1 minted a new dated key) |
| `run.code.commit` | `88e974ca10` (the stale environment stamp, row D1-S18; the deployed package is `0d39789fdf`; fixed in the fold deploy's plan) |

## The served-key clause (W8-S4)

`portal/gold/mdpf/global/account-distribution/2026-10-13.json` against `.../2026-10-12.json` (the prior dated object, written before CN-d-1's change reached a scheduled fire):
- `meta.cottonwood_fold` keys: `accounts_folded`, `age_trading_days`, `by_model_folded`, `note`, `source`, `value_date`. New: `value_date` = 2026-10-12, `age_trading_days` = 1.
- Key paths: new 304, prior 302; added exactly `/meta/cottonwood_fold/age_trading_days` and `/meta/cottonwood_fold/value_date`; removed 0.
- 215 leaf values differ, all under `by_model/*`, `total` and the period/provenance stamps: they are a new date's roster (total.account_count 8417 -> 8422), not a structural change.

W8-S4 reads MET: the new-date global account-distribution carries the two keys and no other key moved.

## The daily-fire arms (r4_daily.py)

ARM 1 CURRENT 12 of 12 series at the frontier 2026-10-12; ARM 2 UNCHANGED 547 of 547 snapshot keys kept their ETag; ARM 3 PARITY 12 of 12; ARM 4 UNITS 3 of 3.

## What this read does not show

One fire; the fold is not deployed (the pair and `ADHOC.canon-r6-fold-deploy` wait on this read). The `run.code.commit` stamp is wrong by the D1-S18 row, so code vintage here is carried by the served keys themselves (the two keys exist only in 0d39789fdf's output), not by the stamp.
