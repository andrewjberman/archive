# NEVER-WIDEN PACKET -- rewrite the ONE served method-row-3 object so it states income ABSENT (IRPT_DASHBD.TO-DB-b-122)

Author: 0.9.0_WK_IRPT_DASHBD~97 (worker), for the pair 2.0.0_SA_COO~D2 / 1.0.0_SA_CTO~DELL2. Ordered by CTO ruling msg 4634
("It rewrites one served object, so it comes with a pair"). **This cell wrote nothing to S3** (`s3_writes: 0`): the only AWS call
was the one read in section 2. The act this packet is for is LATER, is not authorised by this file, and is not done.

## 1. The object (builder output, never typed)

`object_address`: `s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3`

It is the `address` the producer's own dry run returns for the `_commonwealth_delivery` entry
(`emit_method_row(None, firm_scope(entry), thresholds, upload=False, src=entry)`, which calls `lib/opal_naming.py address()`),
printed by the round-66 check for criterion DB66-1-AC3. The partition holds **2 keys** (`emit_method_row` writes both,
`account_return_daily.py:2053-2054`): `data.parquet` (the row) and `manifest.json` (the row plus `thresholds`).

## 2. The live object as it is now (ONE `list-objects-v2`, 2026-10-11T10:16:35Z, through the `.tools/aws` shim)

Command: `.tools/aws s3api list-objects-v2 --bucket opal-data-cottonwood --prefix irpt/cottonwood/gold/dim_return_method/method_version=3`
rc=0. The read was NOT denied. Verbatim `Contents`:

| Key | Size | LastModified | ETag | Checksum |
|---|---|---|---|---|
| `irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet` | 10421 | 2026-10-11T07:17:07+00:00 | `"7b70c246337d26fbba60eac594c21f0f"` | CRC32 FULL_OBJECT |
| `irpt/cottonwood/gold/dim_return_method/method_version=3/manifest.json` | 1831 | 2026-10-11T07:17:07+00:00 | `"5951829e6839cf07e4ef3ce1afdca914"` | CRC32 FULL_OBJECT |

`list-objects-v2` returns no version id. **Whether `opal-data-cottonwood` is versioned was NOT read** (that is a second AWS call this
order does not allow). No object body was read; what the object states is therefore the round-59 mint's statement (written
07:17Z by `emit_method_row`, five thresholds null each claimed `absent`, `income_basis` the old literal `cash_when_received`),
not a read of this cell.

## 3. WRITERS of that object (N = 2 rules read; the count stands on the denominators below)

Denominator: `comp-find -i --files "\bdim_return_method\b"` = 283 hit(s) across 69542 file(s) scanned (corpus=all), 133 files
listed; each first-party code file was opened for the call it makes.

1. **`emit_method_row`, the function that puts the two keys** -- `data/assets/scripts/gold/irpt_reporting/account_return_daily.py:1981`
   (`stream_to_parquet` at 2053, `put_object` of `manifest.json` at 2054). Rule read: it overwrites without a guard of its own.
2. **`apply_days`, the only caller that can reach THIS address** -- `data/assets/scripts/silver/commonwealth_account_return_daily.py:835`
   (`ard.emit_method_row(s3, SCOPE, extra["thresholds"], upload=True, src=entry)`). Rule read: it reads every target key first and
   REFUSES the whole run if any exists (its own docstring, line 776: "any existing key refuses the whole run"). **So the existing
   mint cannot perform the rewrite**; the rewrite needs an overwrite act that the round-59 pair did not cover ("No key is
   overwritten", NEVER_WIDEN_R59 section 4).

Callers that are NOT writers of this address (read, counted, excluded): `account_return_daily.py:2159` and `:2213` (`main()`) reach
only `declared_sources(doc)`, which excludes the underscore-prefixed `_commonwealth_delivery` entry (`:319-331`; `source_entry`
refuses it); the reporting-gold Lambda `handler.py` does not call `emit_method_row` (its docstring, lines 12-16) and emits for
declared sources only. `commonwealth_account_return_daily.py:671` is the dry run (`upload=False`).

## 4. READERS of that object (N = 1 code reader, 0 consumers of the income members)

Same denominator as section 3.

1. **The mint's own verify**, `commonwealth_account_return_daily.py:981-989`: reads `data.parquet`, requires 1 row, `method_version`
   equal to 3 and the five `*_claim` columns equal to `absent`. It reads no income member; the rewritten row keeps all of those, so it
   still reads `method_row=match`.

No other code reads the served object: `reporting-publish` is IAM-granted the reporting gold `dim_return_method` prefix (`infra/aws/terraform/investor-reporting/reporting-publish/iam.tf:40`) but its source
(`infra/aws/lambda/investor-reporting/reporting-publish/publisher.py`) reads `method_version` from the return rows and no method row;
the Cottonwood hop3 leg (FWD-12) is a planned reader, not built (NEVER_WIDEN_R59 section 5). Zero is a value: **zero readers bind
`income_basis`.**

## 5. The exact before row and after row (the producer's dry run, `upload=False`, five null thresholds each `absent`, no tie-out)

Before = the dry run at the base `94acc5a925` (identical to what the round-59 mint wrote, bar `measured_at`); after = this branch.
31 columns after; 29 before.

| column | before (served now) | after |
|---|---|---|
| `income_basis` | `cash_when_received` | `null` (typed string) |
| `income_basis_claim` | (no such column) | `absent` |
| `income_basis_reason` | (no such column) | `FWD-3 does not separate income: it sits inside the value through the cash leg, so this method states no income basis (its income columns are null on every row)` |

**The columns that change: 3** (one changed value, two new columns). **The 28 other pre-existing columns keep their values for the
same input** (`method_version` 3, `method`, `flow_convention` END, `value_basis`, `value_basis_ruling`, `fee_basis`
PER_ENTRY_FEE_TREATMENT, the five thresholds null, the five `*_claim` `absent`, `threshold_claims_source` stated, `guard_substitution`,
`day_count`, `tieout_tolerance_proposed` null, `tieout_tolerance_proposed_claim` absent, `tieout_tolerance` 0.0035, its ruling,
`gips_alignment`, `schema_version`, `source_pipeline`, `firm`); `measured_at` is re-stamped by every emit and is the emission
instant. The new schema hash is the contract's 0.6.0 `schema_hash` (`fd468e209e53f14514380089c9281b0ca90f947ab8eaf53c841bdee666bdfba1`).
The test `tests/test_method_row3_income.py` pins row 2 on its 28 columns bar `measured_at` and row 3's three income members.

## 6. Blast radius and rollback, per key

- **Blast radius: exactly 2 keys** -- `.../method_version=3/data.parquet` and `.../method_version=3/manifest.json`. NOT touched: the 6,650
  day keys under `account_return_daily/`, the sidecar `account_return_daily_blank_reasons/`, any 49F object, any other partition of
  `dim_return_method`, any Lambda, role or schedule. The one reader (section 4) reads no changed member.
- **Rollback, per key.** No prior version is established: the round-59 mint wrote these keys first-time ("no prior version exists to
  restore"), and this cell did not read whether the bucket is versioned. Therefore **the rewrite act's FIRST step is the capture, not
  an option**: for each of the 2 keys, `get-object` the body to a path outside the repo, record its `sha256`, size and ETag (the
  ETag above is the md5 of a single-part put, so it must read back as listed, or the object was changed since 07:17:07Z and the act
  stops), and `get-bucket-versioning`. Restoration = `put-object` of the saved bytes to the same key, then a `head-object` whose
  size and the saved sha256 match. If the bucket is versioned, the prior version id read at capture is the restore point instead
  (copy-object from it). A re-run of the old producer cannot restore the bytes: `measured_at` would differ.
- **Deleting a key is Andrew's act** (CTO msg 3486 precedent); the rollback above is an overwrite with the captured bytes, never a delete.

## 7. Which act lands it, and who verifies

- **The act**: one overwrite of the two keys through `emit_method_row(s3, SCOPE, thresholds, upload=True, src=entry)` with the stamped
  manifest's thresholds and claims (`method_row` in `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json`), run from a tree that carries this branch merged
  (the producer's METHOD_ROWS change is what states row 3 absent). It is NOT `--apply` (that refuses an existing key). It needs its own
  pair: the COO half names this blast radius, the CTO half reads both branches (all four of the keys' states below).
- **Both branches the pair must cover**: (a) the keys are as section 2 states (ETag, size unchanged) -> capture, write, read back;
  (b) either key changed since 07:17:07Z, or the capture fails, or versioning/permission is not as assumed -> the act stops before
  the write and writes nothing.
- **Verifier**: `2.0.0_SA_COO~C2`'s read-back, per the CTO: `head-object` on both keys (size and LastModified moved), a body read of
  `data.parquet` stating `income_basis` null, `income_basis_claim` `absent`, `income_basis_reason` non-empty, the 28 others as before,
  and the mint's verify line reading `method_row=match`.
- **Not established by this packet**: the bucket's versioning; IAM for `s3:PutObject` on these two keys (the R59 half simulated the
  identity policy only; the bucket policy was not simulated and a real put on the method-row key had not been made when it was
  written, though the objects now exist, so a put succeeded at 07:17Z); whether anything outside this repo reads
  the object (the denominator is the repo's).
