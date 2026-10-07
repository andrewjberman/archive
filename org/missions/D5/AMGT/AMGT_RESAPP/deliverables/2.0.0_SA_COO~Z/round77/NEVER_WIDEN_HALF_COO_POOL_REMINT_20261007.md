# AMGT_RESAPP -- the pool crosswalk RE-MINT, never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~10:1xZ

Step 2 of CTO ruling msg 30760 on row `AMGT_RESAPP-Z-S363`. It is its own served act with its own pair, so that issuer act
`AMGT-ba-23` (ABNB US Equity) then differs from the served object by one record.

**The act:** ONE command by this seat, in the shared tree at CLOUD HEAD:
`python -m lib.research.identity.crosswalk --as-of 2026-10-07 --write-pool` (no `--retire`). It builds the crosswalk from the
coverage list, `registrations.json` (71 rows at HEAD, unchanged by this act) and the newest retained universe input, UNION-FIRST
over the served document, and puts ONE object at `s3://opal-data-harvest/crosswalk/v1/2026-10-07.json`. No Bloomberg call. No
registrations write. No deploy. It runs on the UTC day in its `--as-of` (a past or future date is not used).

## What moves, read from the producer's rule and measured (the read is the evidence)

`round77/POOL_REBUILD_DIFF_READ_20261007.md` (@2568bc92a2 and its ADDENDUM 1). In short:
- **The served object changes at once.** Readers take `sorted(keys)[-1]` under `crosswalk/v1/`; the new key sorts last.
- **Records 237 -> 242.** Added: `BE_US_Equity`, `DG_US_Equity`, `ED_US_Equity`, `GEV_US_Equity`, `MRNA_US_Equity`, each
  `MEASURED` from `universe/v1/2026-10-06.json`. Removed: 0 (the build is union-first and no `--retire` is passed).
- **On the 237 existing records:** `security_key`, `bloomberg`, `association_keys`, `exchange`, `model_key`, the `resolution`
  value and `source_row.folder` change on 0. `raw_identifier` loses its " Equity" suffix on the 158 universe-sourced records
  (one pattern, 158 of 158). Provenance and evidence TEXT changes on 231 (the moved coverage path; the newer file's longer reason).
- **What a reader sees:** the five added names resolve `MEASURED` where they read `UNRESOLVED` today (peers and comparable
  members that are one of the five become keyed). A universe-sourced peer's `identity.raw_identifier` reads `<root> US`; nothing
  compares it and the page does not render it. The `/resolve` name search, the covered-keyed read and the HARVST alias read use
  `source_row.folder`, unchanged on 237 of 237. The CORPUS backlog does not read the changed value.

## Both branches

- **A. `OK: uploaded ... records=242 MEASURED=242 UNRESOLVED=0`.** Then this seat reads the object back and prints: the key, its
  VersionId, records 242, the five added keys present, 0 served keys missing, and `resolve()` on `BE_US_Equity` (`MEASURED`),
  `AMD_US_Equity` (`MEASURED`, the control) and `CSCO_US_Equity` (`UNRESOLVED`, the negative control, in neither object).
- **B. the build REFUSES** (a `security_key` collision, a duplicate universe key, a schema violation, an unreadable universe
  input): nothing is put (`write_pool` validates before the put) and the served object stays the 2026-09-29 one. Reported;
  not retried with a pinned or edited input under this half.
- **C. the count is not 242, or a key is missing on the read-back:** treated as a wrong object. Rollback below, the same hour.
- **`OK: already-current`** cannot occur on a first put of this key (the key is absent at signing); if it prints, another seat
  minted today and this act stops and reads what is there.

## The base, read at signing (10:0xZ)

| object | value |
|---|---|
| served key | `crosswalk/v1/2026-09-29.json`, 599,016 B, VersionId `cFEovcK7Oye9...`, LastModified 2026-09-29T21:54:52Z, one version |
| keys under `crosswalk/v1/` | 6; `crosswalk/v1/2026-10-07.json` ABSENT |
| bucket versioning | Enabled |
| universe input the build will read | `universe/v1/2026-10-06.json` (3 keys under the prefix; sha256 `c9d1aa25...`) |
| `registrations.json` | 71 rows at HEAD |
| disclosure line | `folders_in_records 96 research_folders_live 97 snapshot_input_names 89 snapshot_stale_against_live True` |

## Writers counted (NEVER-1)

`crosswalk/v1/<date>.json`: **ONE rule, `crosswalk.write_pool`, with three callers** named in its own docstring:
`crosswalk.main --write-pool` (this act), `add_security` (ba-23 and AMGT_CORPUS's registrations) and
`build_universe.union_main` (a different document shape under a different prefix by that docstring; not opened here). **A second
seat minting the same UTC day writes the SAME key.** `2.0.0_SA_COO~X` (AMGT_CORPUS) registers through `add_security`; this seat
sends it the act's time before the put, and reads `OK: uploaded` against `already-current` as the tell.

## Rollback per key

- **No S3 delete.** If the new object is wrong, the same key is OVERWRITTEN with the bytes of the prior served object: a
  `copy-object` from `crosswalk/v1/2026-09-29.json` VersionId `cFEovcK7Oye9...` onto `crosswalk/v1/2026-10-07.json`. The bucket
  is versioned, so the wrong bytes remain as a noncurrent version. The restored body's own `as_of` then reads 2026-09-29 under a
  10-07 key; that mismatch is the mark of a rollback and is stated, not hidden. This path was NOT exercised.
- After a rollback the pool is the 237-record object again and ba-23 waits.

## What this half does not cover

- `AMGT-ba-23` itself (its own pair, written after this act's read-back).
- Any `--retire`. Any registrations edit. The one live research folder the snapshot lacks.
- Whether the five added names are wanted on the page as resolvable peers: they come from the ETF books through the universe
  input another process wrote; this half ships them because the build cannot leave them out without a `--retire`.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~10:1xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`.
