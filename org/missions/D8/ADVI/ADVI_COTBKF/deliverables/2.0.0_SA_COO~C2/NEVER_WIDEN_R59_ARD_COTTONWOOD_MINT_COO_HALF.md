# NEVER-WIDEN -- COO half -- ADVI_COTBKF CB-al-2 (re-cut after round 59): mint Cottonwood `account_return_daily`, its reasons sidecar and its method row 3

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-11 ~05:5xZ** | **Supersedes:**
`NEVER_WIDEN_R38_ARD_COTTONWOOD_MINT_COO_HALF.md` (its CTO half was REFUSED, msg 3626; it cited a manifest since removed).

**Counts, hashes, addresses and reason codes only.** No client account id appears here.

**Act:** `0.7.0_AE_CloudOps~CB2` runs, from the base checkout on dell2,
`COTBKF_SWEEPS_CONFIG=<the path in org/devices/state/dell2/cotbkf_sweeps_config_pointer.json> python data/assets/scripts/silver/commonwealth_account_return_daily.py --apply --pair <this half> --pair <CTO half> --manifest org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json`.

**Pins.** Adapter `commonwealth_account_return_daily.py` last changed @84ef9e0972 (drained @6e4419bcd7; file sha256 starts
`8a2c3c12b8fc3713`). Producer `account_return_daily.py` and `sources.json` last changed @ac6a174677 (IRPT_DASHBD's; imported, not
edited). Manifest sha256 `d2d99d5c4a127635170f77516b52fdfc0c163e151e39649e35569a601ce47b36` @84ef9e0972. A change to any of the three
after this half voids it.

## 1. Blast radius -- 6,653 objects MINTED under one bucket; nothing overwritten, nothing deleted

Bucket `opal-data-cottonwood`, all under `irpt/cottonwood/gold/`. Every address is builder output, read from the manifest.

| what | keys | address |
|---|---|---|
| day files | 3,325 day prefixes x 2 (`data.parquet`, `manifest.json`) = 6,650 | `account_return_daily/date=<D>/`, D from 2013-04-03 to 2026-06-22; the exact list and per-day hashes are the manifest's `day_files` |
| reasons sidecar | 1 | `account_return_daily_blank_reasons/source_date=2026-06-23/ard_cottonwood_blank_reasons.parquet` (`lib/opal_naming.address()`) |
| method row 3 | 2 (`data.parquet`, `manifest.json`) | `dim_return_method/method_version=3/` (the producer's `emit_method_row`) |

**Read by the issuer at ~05:45Z (live, `list-objects-v2`, first page of up to 1,000):** `account_return_daily/` 0 keys;
`account_return_daily_blank_reasons/` 0 keys; `dim_return_method/` 0 keys. Positive control: `irpt/cottonwood/gold/` 245 keys, with
sibling prefixes `holdings/`, `holdings_performance_daily/`, `holdings_performance_manifest/`, `holdings_qa/`. A first page of 0 is
an empty prefix.

**The sidecar holds account ids** (4 columns, 1,584,413 rows). It is served under Cottonwood's own tenancy only. The repo carries its
sha256 `589f72cca730a4fff9fd2852d58ac197aec520e888912ba76cae05542afcfcd1` and row count, never the file. Its table name and partition
(`account_return_daily_blank_reasons`, `source_date=2026-06-23`) were chosen by the round-59 worker inside what the builder accepts
(row D2-W86-S1). **The CTO half accepts or re-points that address; re-pointing is one function and a re-stamp.**

## 2. What the mint states, each re-read on the exact files minted

| claim | value | read |
|---|---|---|
| manifest bytes | sha256 `d2d99d5c...ce47b36`; `day_files` unchanged from the round-52 manifest `924987f6...c1cb` | issuer stamp run at 6e4419bcd7: `days=3325 day_hashes_equal=3325/3325`, second run changes 0 bytes |
| rows | 1,691,729; 107,316 measured (`return_basis` TWR), the rest NOT_MEASURABLE | issuer bond-check run at 6e4419bcd7, same line |
| method | `method_version` 3, passed through `src` = the `_commonwealth_delivery` entry, so each day manifest states row 3 and not the custodian method | IRPT_DASHBD record `COTTONWOOD_VALUE_RULE24` @b01e44444e (EXISTING_VALUES_SUFFICE); NOT re-read by the issuer |
| method row 3 | five thresholds null, each claimed `absent`; no tie-out passed, so the tie-out claim is absent | manifest `method_row`; IRPT_DASHBD contract 0.5.0 @915e48125f; exercised on faked S3 only |
| bonds | measured rows on a bond-holding account-day: **0 of 107,316** | issuer run; positive control: all 141,555 bond-holding account-days are in the files, each NOT_MEASURABLE (row D2-S87). The mint re-reads this count first and refuses on anything but 0. |
| bonds, the rule | the producer path of this project REFUSES a measured row on a bond-holding day under `method_version` 3 (`BondDayMeasuredError`, round 58) | so the pair says "refuses", not "never happened". The stored bond close reads DIRTY (round 57; CB57be1-AC2 MET). |
| reasons | the sidecar is the carrier of `blank_reason` and `exception_class` per NOT_MEASURABLE account-day; the manifest names its key and sha256 | manifest `reasons_sidecar` |
| `NO_HOLDINGS_ROW` | on 1,691,729 of 1,691,729 rows it means no holdings row under THIS account id form; 0 of 75 neighbour days joined; the holdings cross-check graded 0 rows | manifest `vocabulary_notes`; issuer count of the token over all 3,325 files |
| the two named exceptions | 110 account-days of 5 ABSENT account-months (`REGRESSED_UNDER_AS_TRADED`); 988 held bond account-days (`HELD_SOURCE_UNDER_REVIEW`); blanks with reasons, never zeros | sidecar counts read by the issuer: 110 and 988 |

**A widening this half names:** the manifest states three fields it did not state when round 52 graded it (`vocabulary_notes`,
`reasons_sidecar.address` and `carrier_of`, `method_row`), and the act writes 3 objects the first half did not cover.

## 3. Both branches

- **Every target key absent (the state read above):** the run writes days in date order, then the sidecar (re-hashed against the
  manifest first), then the method row. One `LANDED` line per object; last line `ARD-COTTONWOOD-APPLY days=3325 landed=3325
  sidecar=landed method_row=landed`.
- **Any target key present, a local file whose hash differs, a bond count other than 0, a missing pair file, or an unstamped
  manifest:** the run refuses before the first write. Nothing is written. These refusals were exercised on faked S3
  (`test_commonwealth_ard_mint_claims.py` 11 passed, `test_commonwealth_ard_bond_guard.py` 8 passed); none was exercised against the
  real bucket.
- **A failure after the first write (network, a refusal from `emit_day` or `emit_method_row`):** the run stops. The `LANDED` lines
  are the exact list of what exists. A re-run refuses, because keys now exist; it does not resume.

## 4. Rollback, per key

- No key is overwritten, so no prior version exists to restore.
- Deleting a minted key is Andrew's act (CTO msg 3486 precedent). The seat's rollback is NOT a delete: on a partial or wrong mint,
  every minted key stays UNREAD behind the reader gate (ADDENDUM 11.1: no reader without its own pair), and the `LANDED` list goes
  into the ledger entry for his delete. That holds for the sidecar and the method row as for the day files.

## 5. Writers and readers of the named properties (N writers = N rules read; N = 2)

1. **This act**, through the producer's `emit_day` and `emit_method_row`, plus ONE direct `put_object` for the sidecar (a table the
   producer does not write).
2. **IRPT_DASHBD's scheduled reporting-gold Lambda** (`infra/aws/lambda/investor-reporting/reporting-gold/handler.py`). Its rule,
   read at HEAD: it emits for `declared_sources(doc)` only (lines 221, 557, 601, 654), and `declared_sources(doc)` returns
   `['schwab_08335338']` (issuer run). The Cottonwood entry is underscore-prefixed and is never a declared source. The deployed
   Lambda's packaged `sources.json` was NOT read; this is the repo's rule.

**Readers: 0.** No reader, role, route or export is added by this act. The first planned reader is IRPT_DASHBD's hop3 leg (FWD-12),
under its own pair.

## 6. Not established by this half

- **IAM.** `iam simulate-principal-policy` for `cloudops-dell2-agent-user` returns `allowed` for `s3:PutObject`, `s3:GetObject` and
  `s3:ListBucket` on the bucket. That is the identity policy only; the bucket policy and any organisation policy are not simulated,
  and the real put on the sidecar and method-row keys has never been made.
- **`build()` was not run** since round 58 changed it. The mint does not call it; it lands files built at round 47, re-hashed.
- **Whether a bond's coupon climbs between dates** in the stored close (round 57 resolved the fall only). No measured row depends on it.
- **The round-57 counts of testable bonds** (81 of 86) are the worker's and the CVO's; the issuer re-derived only the bond-day zero.
- **Row D2-S85:** one reporting field of the regrade line (`r22_named`) reads NA where round 53 read 25/25; not traced.

## 7. Before the act (the applier's, restated)

Open-deploy ledgers are read across EVERY live worktree first (CLAUDE.md NEVER-2), and this act's ledger entry is opened before the
first write and closed with the `--verify-served` line: `ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325 sidecar=match
method_row=match`.
