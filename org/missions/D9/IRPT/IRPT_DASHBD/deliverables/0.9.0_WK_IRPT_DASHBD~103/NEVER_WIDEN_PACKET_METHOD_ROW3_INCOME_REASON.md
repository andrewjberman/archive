# NEVER-WIDEN PACKET -- reword the served income reason on method row 3 for the METHOD (IRPT_DASHBD.TO-DB-b-128)

Author: 0.9.0_WK_IRPT_DASHBD~103 (worker), for the pair 2.0.0_SA_COO~D2 / 1.0.0_SA_CTO~DELL2. Ordered by the ROUND-68 ANALYSIS
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_ROUND_68_20261011.md`, section 2 item 4), answering row
IRPT_DASHBD-D2-S13. Follows `deliverables/0.9.0_WK_IRPT_DASHBD~97/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME.md` section by section.
**This cell wrote nothing to S3** (`s3_writes: 0`): the only AWS call was the one read in section 2. The act this packet is for is
LATER, is not authorised by this file, and is not done. No client name, account id or figure appears here.

## 1. The object (builder output, never typed)

`object_address`: `s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3`

It is the `address` the producer's own dry run returns for the `_commonwealth_delivery` entry
(`emit_method_row(None, firm_scope(entry), thresholds, upload=False, src=entry)`, which calls `lib/opal_naming.py address()`),
re-run by this cell on this branch. The partition holds **2 keys**, both put by `emit_method_row`
(`account_return_daily.py:2054` `stream_to_parquet` of `data.parquet`; `:2055-2057` `put_object` of `manifest.json`, whose body is the
row plus `thresholds`).

## 2. The live object as it is now (ONE `list-objects-v2`, 2026-10-11T15:31:42Z, through the `.tools/aws` shim)

Command: `.tools/aws s3api list-objects-v2 --bucket opal-data-cottonwood --prefix irpt/cottonwood/gold/dim_return_method/method_version=3`
rc=0. NOT denied. These are the keys AFTER today's 10:38Z rewrite (TO-DB-b-123), not the 07:17Z ones the earlier packet listed:

| Key | Size | LastModified | ETag | Checksum |
|---|---|---|---|---|
| `irpt/cottonwood/gold/dim_return_method/method_version=3/data.parquet` | 11641 | 2026-10-11T10:38:24+00:00 | `"9c774f3770e82ed5e7e6b2a4ebe3e7d3"` | CRC32 FULL_OBJECT |
| `irpt/cottonwood/gold/dim_return_method/method_version=3/manifest.json` | 2037 | 2026-10-11T10:38:25+00:00 | `"6d5aabdd1e0f3cc9ff2a6c544bd327fd"` | CRC32 FULL_OBJECT |

`list-objects-v2` returns no version id, and no second AWS call was made. The version ids below are NOT this cell's read: they are the
ones the TO-DB-b-123 apply recorded in `deliverables/0.9.0_WK_IRPT_DASHBD~98/METHOD_ROW3_APPLY.json` (`head_after`, `capture`), and the
same record states `bucket_versioning: Enabled`. The sizes, LastModified and ETags above equal that record's `head_after` exactly, so
the keys have not moved since 10:38Z as of 15:31:42Z.

| Key | Version id NOW (per ~98 `head_after`) | Version id PRIOR (per ~98 `capture`, retained) |
|---|---|---|
| `data.parquet` | `hcqKO1hmuZIFPMKZrRF6gw7jS0mY4xnU` | `.MnBtIEprWTsvzhZSqkuRkJCU1n4SehQ` (07:17:07Z) |
| `manifest.json` | `9mFo70MiWTNgg3u8xC24yvm3pmOsxQw6` | `In.WljkGD7o_t6CsgY8O7clIHMh3K1IH` (07:17:07Z) |

No object body was read by this cell. What the object states is therefore the TO-DB-b-123 apply's record (`served_after`:
`income_basis` null, `income_basis_claim` `absent`, `income_basis_reason` the OLD sentence below), not a read of this cell.

## 3. WRITERS of that object (N = 2 rules read)

Denominator: `comp-find -i --files "emit_method_row"` = 148 hit(s) across 70505 file(s) scanned (corpus=all), 58 files listed; each
first-party code file in the SURFACED and DEF bands was opened for the call it makes.

1. **`emit_method_row`, the function that puts the two keys** -- `data/assets/scripts/gold/irpt_reporting/account_return_daily.py:2054-2057`.
   Rule read: it overwrites without a guard of its own (a put to the same key; the bucket keeps the prior version).
2. **`apply_days`, the only caller that can reach THIS address** -- `data/assets/scripts/silver/commonwealth_account_return_daily.py:884`
   (`ard.emit_method_row(s3, SCOPE, extra["thresholds"], upload=True, src=entry)`). Rule read: it reads every target key first and REFUSES
   the whole run if any exists, so `--apply` cannot perform this rewrite; the rewrite is an explicit overwrite act of its own.

Callers read, counted and excluded: `account_return_daily.py main()` reaches only `declared_sources(doc)`, which excludes the
underscore-prefixed `_commonwealth_delivery` entry (`:319-325`); the reporting-gold handler (`infra/aws/lambda/investor-reporting/reporting-gold/handler.py`)
has no `emit_method_row` call (lines 16, 221, 557, 601, 654 read: `declared_sources` and `source_entry` only); `commonwealth_account_return_daily.py:719` is the
dry run (`upload=False`).

## 4. READERS of that object (N = 1 code reader, 0 readers of any income member)

1. **The mint's own verify**, `data/assets/scripts/silver/commonwealth_account_return_daily.py:1030-1038` (the read itself at `:1031`, the
   table read at `:1035`): it reads `data.parquet`, requires 1 row, `method_version` equal to the manifest's, and the five
   `*_claim` threshold columns equal to `absent`. It names no income member, so the reworded reason cannot change its state;
   after the rewrite it still reads `method_row=match`.

No other code reads the served object: the `reporting-publish` Lambda reads `method_version` from the return rows and no method row
(carried from the ~97 packet section 4, not re-read by this cell); the Cottonwood hop3 leg (FWD-12) is a planned reader, not built.
Zero is a value: **zero readers bind `income_basis_reason`.** The repo-wide name census, `comp-find -i --files "income_basis_reason"` =
62 hit(s) across 70496 file(s) scanned, lists the producer (DEF), two issuer checks (p66, p67) that require the member to be non-empty
only, tests, the contract, records and prose; none compares it to a sentence.

## 5. The exact before row and after row (the producer's dry run, `upload=False`, five null thresholds each `absent`, no tie-out)

Before = the sentence the object states now (TO-DB-b-123 `served_after`; byte-equal to the producer at the base `53ce87e407`);
after = this branch. 31 columns before and after; none added or removed; the contract's `schema_hash` is unchanged
(`fd468e209e53f14514380089c9281b0ca90f947ab8eaf53c841bdee666bdfba1`, recomputed from this branch's `table_schema`: equal).

| column | before (served now) | after |
|---|---|---|
| `income_basis_reason` | `FWD-3 does not separate income: it sits inside the value through the cash leg, so this method states no income basis (its income columns are null on every row)` | `A positions-based method values the account from its positions and cash, so income is inside that value and is not separated from it: the method states no income basis.` |
| `measured_at` | the 10:38:24Z emission instant | the new emission instant (re-stamped by every emit) |

**The columns that change: 2** (one wording, plus the emission instant). The 29 other columns keep their values for the same input:
`income_basis` null, `income_basis_claim` `absent`, `method_version` 3, `method`, `flow_convention` END, `value_basis`,
`value_basis_ruling`, `fee_basis` PER_ENTRY_FEE_TREATMENT, the five thresholds null, the five `*_claim` `absent`,
`threshold_claims_source`, `guard_substitution`, `day_count`, `tieout_tolerance_proposed` null, `tieout_tolerance_proposed_claim` `absent`,
`tieout_tolerance`, its ruling, `gips_alignment`, `schema_version`, `source_pipeline`, `firm`. `manifest.json` carries the same row, so the
same two members differ there; its `thresholds` object is unchanged. Row 2 is not in this object and does not move. The new
sentence is pinned by `tests/test_method_row3_income.py` (exact text; no outcome id, firm, custodian or channel token).

## 6. Blast radius and rollback, per key

- **Blast radius: exactly 2 keys** -- `.../method_version=3/data.parquet` and `.../method_version=3/manifest.json`. NOT touched: the day
  keys under `account_return_daily/`, the sidecar `account_return_daily_blank_reasons/`, any 49F object, any other partition of
  `dim_return_method`, any Lambda, role or schedule. The one reader (section 4) reads no changed member.
- **Rollback, per key, by the prior version id (the bucket is versioned).** The apply's FIRST step is the capture, not an option: for
  each of the 2 keys, `head-object` and `get-object` (body to a path outside the repo, with its sha256), recording the version id, ETag and
  size; they must read back as section 2 lists (ETag `9c774f37...` / `6d5aabdd...`, sizes 11641 / 2037), or the object was changed since
  10:38Z and the act stops (branch b). After the write, the version ids captured in that step ARE the restore points: `copy-object`
  (or `get-object --version-id` then `put-object`) of that exact version id to the same key, then a `head-object` whose size and
  ETag equal the captured ones. The 07:17Z versions (`.MnBtIEpr...`, `In.WljkGD7o...`) are older restore points and stay retained. A re-run of
  the old producer cannot restore the bytes: `measured_at` would differ.
- **Deleting a key, or a version, is Andrew's act** (CTO msg 3486 precedent); the rollback is a restore of a retained version, never a delete.

## 7. Which act lands it, and who verifies

- **The act**: one overwrite of the two keys through `emit_method_row(s3, SCOPE, thresholds, upload=True, src=entry)` with the stamped
  manifest's thresholds and claims (`method_row` in `org/missions/D8/ADVI/ADVI_COTBKF/deliverables/0.9.0_WK_ADVI_COTBKF~79/ard_cottonwood_manifest.json`),
  run from a tree that carries this branch merged (the producer's METHOD_ROWS change is what states the new sentence). It is NOT
  `--apply` (that refuses an existing key). **The applier is an AE seat (a cloud-ops seat), under a newly signed COO/CTO pair for
  this blast radius, and NEVER a worker**: row IRPT_DASHBD-D2-W87-S1 records that the apply gate (`safe-apply`, APPLY-WHO) graded a worker's
  apply REFUSED, and the CTO's ruling on it is that the gates admit an AE seat, not a worker. The AE seat opens the change-management
  ledger entry before the first write, **captures both keys first** (section 6), writes, reads back and closes it. Nothing in this
  cell authorises that act.
- **Both branches the pair must cover**: (a) the keys are as section 2 states (ETag, size, version id unchanged) -> capture, write, read
  back; (b) either key changed since 10:38Z, or the capture fails, or versioning is not `Enabled`, or `s3:PutObject` is denied -> the
  act stops before the write and writes nothing (a partial write of one key is rolled back by section 6 the same turn).
- **Verifier**: the read-back by the seat that signs the pair's other half: `head-object` on both keys (size and LastModified moved), a
  body read of `data.parquet` stating `income_basis` null, `income_basis_claim` `absent`, `income_basis_reason` equal to the section 5
  after sentence, the 29 others as before, and the mint's method-row check reading `method_row=match`.
- **Not established by this packet**: the version ids' CURRENT truth (they are the ~98 record's, re-read by the capture step); IAM for
  `s3:PutObject` for the AE seat on these two keys (simulated by the pair, not here); whether anything outside this repo reads the
  object (the denominators are the repo's).
