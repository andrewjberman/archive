# NEVER-WIDEN -- COO half -- ADVI_COTBKF round 38, CB-al-2: mint Cottonwood `account_return_daily`

**Signer:** `2.0.0_SA_COO~C2` (dell2) | **State: GIVEN 2026-10-09 ~16:0xZ**
**Act:** `0.7.0_AE_CloudOps~CB2` runs `data/assets/scripts/silver/commonwealth_account_return_daily.py --apply` (round 49, drained
@26cf9c42db). It lands every locally built day through IRPT_DASHBD's producer `emit_day(upload=True)`, the table's one writer
function.

## 1. Blast radius -- 3,325 day prefixes MINTED (6,650 keys); nothing overwritten, nothing deleted

- **Prefix:** `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_return_daily/` (from `address("irpt", "cottonwood", "gold",
  "account_return_daily", "date=<D>")`).
  - It read 0 keys at ~15:5xZ, against a positive control: `irpt/` gave 3 keys on its first page.
- **Per day:** `<prefix>date=<D>/data.parquet` and `<prefix>date=<D>/manifest.json`. The days run 2013-04-03 .. 2026-06-22, 3,325
  in all.
- **The exact day list and per-day hashes** (`sha256`, `content_sha256`, `manifest_sha256`) are
  `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~74/ard_cottonwood_manifest.json`, file sha256
  `56eafe04bf550c148461ec68bb45ce4f2de9441515bfb27c76cb72faec8bdc19`.
- **Local files to land:** `.scratch/advi_cotbkf/ard_cottonwood_r47/date=<D>/data.parquet`, built at round 47 (~74, drained
  @9c6b230812).
  - The issuer's re-run of that build is byte-identical: 3,325 of 3,325 day files.
  - The apply's rebuilt `first_data_date` map equals the build's: 1,533 accounts, 0 differ (issuer check ~16:0xZ). So the served
    manifests carry the same map the build used.
- **Content:**
  - 1,691,729 rows. 107,316 measured rows read `return_basis=TWR`; the rest read `NOT_MEASURABLE`.
  - Every manifest and row reads `method_version` 3 (`positions_based`).
  - Every manifest carries `valuation_source=positions_x_as_traded_close`, `fee_treatment=net_of_fees` and `price_basis=as_traded`
    (IRPT_DASHBD ADDENDUM 13.1 / 13.2).
- **The two named exceptions are blanks with reasons, never zeros:**
  - the 5 ABSENT account-months (110 account-days, `REGRESSED_UNDER_AS_TRADED`, rows D2-S53..S57);
  - the 988 held bond account-days (`HELD_SOURCE_UNDER_REVIEW`).

## 2. Rollback

- No key is overwritten, so no prior version exists to restore.
- Deleting minted keys is Andrew's act (CTO msg 3486 precedent), so the seat's rollback is NOT a delete. On a failed or partial run,
  the minted keys stay UNREAD behind the reader gate (ADDENDUM 11.1: no reader without its own pair). Their exact list (the
  `LANDED` lines) goes into the ledger for Andrew's delete.
- The apply prints one `LANDED` line per day, so a partial run is visible.

## 3. Writers and readers of the named property

- **Writers (1):** this act, through the producer's `emit_day`.
  - IRPT_DASHBD's scheduled reporting-gold Lambda writes `account_return_daily` only for its declared sources (`declared_sources()` =
    `['schwab_08335338']`).
  - The Cottonwood entry is underscore-prefixed (never a source), and the deployed Lambda packages its own pinned `sources.json`.
- **Readers: 0.** The reader gate stands: each reader, role, route or export is its own pair, naming both exceptions above. The first
  planned reader is IRPT_DASHBD's hop3 leg (FWD-12), under its own pair.

## 4. Guards the apply enforces (round 49, tested on faked S3)

1. Both pair files must be git-tracked.
2. Every local file is re-hashed against the manifest's `sha256`.
3. ANY existing key under the prefix refuses the whole run.
4. The only writer is the producer's `emit_day(upload=True)`; there is no other key and no delete path.

**Proof:** `--verify-served --manifest <the manifest>` reads `ARD-COTTONWOOD-VERIFY days=3325 match=3325/3325` on content hashes.
