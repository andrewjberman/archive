# NFRA_OPLGTW.TO-OG-c-1 -- result: the Schwab producer's qualified closure

**Worker:** `0.9.0_WK_NFRA_OPLGTW~4` | **Branch:** `wk-nfra_oplgtw-1-4` (worktree `/c/tmp/wk-oplgtw-1-4`, cut from
`CLOUD` @1bcc827bda) | **Code commit:** `c0c7b4d2f2` (LOCAL, not pushed) | **Spec:** PRD v0.2 C3 @f0aa50dbc0 |
**Decomposition:** v1 @8768f46770, cell `OG-c-1` | **Deployed:** nothing (deploy and replay are `OG-c-2`'s, held on G-B).

## 1. Premise, re-grounded

The order quotes the certified rectangle @c9a44aa896: the v1 marker carries master/date/run_id/emitted_at/declared_source,
declared vs written tables with both disagreement directions, no VersionId or digest, and each run can replace the
date-keyed marker. Read at the cut (`data/assets/scripts/silver/conversion_manifest.py:158-272` @1bcc827bda): exactly that.
`build_complete_markers` emits nine keys (`schema, master, date, declared_tables, declared_source, written_tables,
disagreement, run_id, emitted_at`), `write_complete_marker_verified` puts then HEADs, and both runtime paths emit under a
per-lane "no failed result" gate (`schwab_runtime.py:92`, `:188`). The premise holds.

## 2. What changed (composition only)

* `conversion_manifest.py` -- `build_closure` (pure: the day's inventory plus this run's results -> one closure),
  `validate_closure` (one argument; decides from the closure alone), `closure_id` (a sha256 over the day's facts,
  independent of which run composed them), and a conditional write path inside `write_complete_marker_verified` that is
  taken ONLY when a composer is passed. Without one, the v1 write is byte for byte what it was.
* `schwab_runtime.py` -- `day_inventory` (READ-ONLY: ListObjectsV2 of the lane's bronze and silver for the date, then one
  ranged GetObject per silver object for its VersionId, size, ETag and parquet-footer row count) and the composer. Both
  are wired at the two existing emit sites, inside the unchanged per-lane gate.
* `tests/test_conversion_manifest.py` -- `test_ogc1_ac01` .. `test_ogc1_ac11` appended; no existing test edited.

The published object stays at `schwab/{master}/meta/complete/date={date}.json` and gains ONE key, `closure`.

## 3. The record's new schema -- `closure` (`schema_version: "opal.silver.closure/v1"`)

| field | what it carries | claim |
|---|---|---|
| `schema_version` | `opal.silver.closure/v1` | constant |
| `master`, `date` | the one master (never both) and the Schwab business date | from the v1 marker |
| `run` | `run_id`, `trigger` (event/sweep), `force`, `composed_at` | run facts, NOT in the identity |
| `expected_source_basis` | the expected set's claim: OBSERVED bronze at composition, `required_types` enforced | text, on the record |
| `required_types` | `["rld"]` -- a pipe delivery without it is refused whole (`schwab_conversion.NON_OPTIONAL`) | producer law |
| `source_partitions[]` | per bronze type landed for the date: `type`, `kind` (pipe/identity/hole/unknown), `disposition` (`EXPECTED` / `NON_APPLICABLE_NAMED_HOLE` / `UNKNOWN_TYPE`), `bronze_keys`, `expected_tables` | measured (listing) |
| `non_applicable[]` | explicit: each named hole (`NAMED_HOLE`) and each SPECS-declared table with no source partition that day (`DECLARED_NO_SOURCE_PARTITION`) | derived |
| `expected_tables` | union of the expected partitions' tables -- facts through `set_identity_guard.expected_tables`, dims through its projection map | derived |
| `tables{}` | per table: `expected`, `source_type`, `projection_of`, `disposition`, `object` (`key`, `version_id`, `size`, `etag`), `rows`, `objects_seen`, `keys_seen` when ambiguous, `run_outcome` (`written` / `overwritten` / `idempotent-existing` / `prior-run` / `failed`) | measured (footer) + run facts |
| `objects[]` | every qualifying silver object: `table`, `key`, `version_id`, `size`, `etag`, `rows` | derived from `tables` |
| `empty` / `day_disposition` | tables with `EMPTY_TYPED`; `EMPTY_TYPED` when every expected table is, `DATA` otherwise, `NO_EXPECTED_SOURCE` when nothing is expected | derived |
| `outputs` | `successful` (qualifying expected tables) and `failed` (`source_type`, `bronze_key`, `outcome`, `reason_class` -- the exception CLASS only, sanitized) | derived + run facts |
| `counts` | source_partitions, expected_source_partitions, non_applicable, expected_tables, tables_seen, objects, successful, failed, empty, missing, rows, written_this_run, overwritten_this_run, idempotent_existing, prior_run | derived |
| `inventory_errors[]` | any listing or object that could not be read (`class`, `subject`) | measured |
| `write_guard` | `conditional`, or `unconditional` when the client could not send the conditions | write fact |
| `closure_id` | `sha256:` over schema, master, date, required_types, source_partitions, expected_tables, non_applicable, tables minus `run_outcome`, and failed outputs | derived |
| `status` / `findings[]` | `qualified` iff `validate_closure` finds nothing; each finding is `class` / `subject` / `detail` | stamped by the validator |

**Table dispositions:** only `PRESENT` (rows > 0) and `EMPTY_TYPED` (0 rows from a pipe type, which lands nothing
that does not tie to its T1 trailer) qualify. The rest are `EMPTY_UNEXPLAINED` (0 rows from an identity file, which has
no trailer), `MISSING`, `FAILED`, `AMBIGUOUS` (more than one object in the partition, or rows unread), `UNVERSIONED`
(VersionId absent or `null`) and `UNEXPLAINED_OUTPUT` (an output no delivered source explains).

**Finding classes:** `MISSING_OUTPUT`, `FAILED_CONVERSION`, `UNEXPLAINED_EMPTY_DAY`, `UNEXPLAINED_EMPTY_OUTPUT`,
`INCONSISTENT_GRAIN` (a non-canonical key, projection row parity broken, or a bronze object outside its partition),
`AMBIGUOUS_INVENTORY`, `UNVERSIONED_OBJECT`, `REQUIRED_SOURCE_ABSENT`, `INCONSISTENT_RECORD` (the record disagrees with
itself: summaries, closure_id, or a stored `qualified` over findings) and `UNGUARDED_WRITE`.

**Self-sufficiency:** `validate_closure(closure)` takes one parameter, re-derives every summary from the facts, and
reaches no storage. Its transitive callees contain none of `get_object`, `head_object`, `list_objects`, `put_object`,
`open(`, `boto3`, `urlopen`, `socket`, `import ` or `meta/conversions`, and `test_ogc1_ac11` runs it with sockets, file
opens and boto3 all shut. The producer stamps `status` by calling the same function, so producer and reader hold one rule.

**Write protocol (exactly one qualified closure):**
1. The first PUT asserts absence (`If-None-Match: *`).
2. On a conflict the writer reads the object and its ETag, composes AGAIN from a fresh inventory, and writes only with
   `If-Match` on that ETag.
3. If the object already holds a qualified closure with the same `closure_id`, the run writes nothing.
4. After 8 lost races it raises.
5. If the client rejects the conditions client-side (botocore `ParamValidationError`), the v1 marker still lands
   unchanged, and its closure says `write_guard: unconditional`, `status: incomplete`.

## 4. Criteria -- run exactly as the order writes them, `<WS>` = `/c/tmp/wk-oplgtw-1-4`

| id | invocation (test / probe) | deciding output | rc | denominator |
|---|---|---|---|---|
| OGC1-AC1 | `...::test_ogc1_ac01` | `1 passed in 0.46s` | 0 | 1 of 1 selected |
| OGC1-AC2 | `...::test_ogc1_ac02` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC3 | `...::test_ogc1_ac03` | `1 passed in 0.46s` | 0 | 1 of 1 |
| OGC1-AC4 | `...::test_ogc1_ac04` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC5 | `...::test_ogc1_ac05` | `1 passed in 0.55s` | 0 | 1 of 1 |
| OGC1-AC6 | `...::test_ogc1_ac06` | `1 passed in 0.48s` | 0 | 1 of 1 |
| OGC1-AC7 | `...::test_ogc1_ac07` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC8 | `...::test_ogc1_ac08` | `1 passed in 0.53s` | 0 | 1 of 1 |
| OGC1-AC9 | `...::test_ogc1_ac09` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC10 | `...::test_ogc1_ac10` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC11 | `...::test_ogc1_ac11` | `1 passed in 0.47s` | 0 | 1 of 1 |
| OGC1-AC12 | `pytest data/assets/scripts/silver/tests` | `300 passed, 11 skipped in 5.43s` | 0 | 311 collected (cut baseline 289 passed / 11 skipped; +11 = the new tests) |
| OGC1-AC13 | `probes/og_c1.py AC13` | `VERDICT: PASS-OGC1-AC13` | 0 | 146 hits across 33,034 files scanned; 59 of 59 listed files classified (6 executed + 53 record) + 1 hop |
| OGC1-J1 | judgment | recorded below, NO verdict | -- | 708 changed lines in the two source files |

AC13 detail: the probe prints `FIELDS: v1 at 1bcc827bda = 9` and `DELTA: removed 0 [] | renamed 0 | value-changed 0 [] |
added 1 ['closure'] | marker key unchanged: True`. The executed readers, and what each reads:

| reader | what it reads |
|---|---|
| `silver.tf` | S3 ObjectCreated on key prefix `schwab/08335338/meta/complete/`, suffix `.json`: the object KEY, no body field |
| `advi_49f_floor.tf` | names the marker in comments only; body fields read: none |
| accelerator target `advi-49f-gold-dispatch/lambda_function.py` (hop) | `Records[0].s3.object.key` only; no body field, no `get_object` |
| the producer and its vendored copy | writers |
| the test | asserts the v1 face |
| the probe | reads nothing of the marker |

## 5. Controls (each fired)

* **Mutant M1**, the conditions dropped from the closure PUT: `FAILED test_ogc1_ac08`, `1 failed, 10 passed`.
* **Mutant M2**, `_verdict` always qualified: 7 red (`ac03`, `ac04`, `ac05`, `ac08`, `ac09`, `ac10`, `ac11`),
  `7 failed, 4 passed`. The 4 greens (`ac01`, `ac02`, `ac06`, `ac07`) carry no incomplete arm.
* **Probe control A**, the census without `advi_49f_floor.tf`: `VERDICT: FAIL-OGC1-AC13 census lacks the named consumer(s)
  infra/aws/terraform/opal-assets/advi_49f_floor.tf`, rc 1.
* **Probe control B**, a write path that drops `written_tables`: `DELTA: removed 1 ['written_tables']` then
  `VERDICT: FAIL-OGC1-AC13 the cell removes/renames/changes v1 field(s) ['written_tables']`, rc 1.
* **Tests carry their own controls:**
  * the AC8 race against a bucket that ignores the conditions lands TWO qualified closures;
  * the AC10 untouched complete bucket qualifies;
  * the AC9 identity-file zero rows are not a typed empty;
  * the AC2 golden fails on a renamed field.

Mutants ran in a scratch copy of the silver tree (`.scratch/mut/`), never in the tracked files.

## 6. OGC1-J1 record (for 3.0.0_SA_CVO at L9 -- no verdict here)

`git diff 1bcc827bda c0c7b4d2f2 -- conversion_manifest.py schwab_runtime.py`: 708 added or removed lines. Every one that
names an S3 write verb (`put_object`, `delete_object`, `copy_object`, `upload_`, `_put_table_verified`,
`_write_parquet_verified`, `ChunkedParquetWriter`) is a marker PUT at `key = complete_marker_key(...)`:
* the removed v1 line, `client.put_object(Bucket=bucket, Key=key, Body=body)`, moved under `if compose is None`;
* the re-added v1 line;
* the two closure PUTs in `_write_closure_marker`.

The only S3 calls the inventory adds are `list_objects_v2` and a ranged `get_object`. No silver writer, `force` path or
bronze call is added or changed, and `schwab_conversion.py` is untouched.

## 7. Surprise rows filed (channel `INVESTIGATION_v1.md`, committed at c0c7b4d2f2)

* `NFRA_OPLGTW-W4-S1` OBSERVATION/INERT: the cut's census (361 / 172,084) does not reproduce in a fresh worktree, which
  holds tracked files only. The AC13 census carries its own denominator.
* `NFRA_OPLGTW-W4-S2` OBSERVATION/INERT: exactly-one rests on conditional PUT, and the Lambda (python3.11) uses the
  runtime's unpinned boto3. The code fails closed for the closure and safe for v1.
* `NFRA_OPLGTW-W4-S3` OBSERVATION/INERT: no declared per-day expected source set exists. The expected set is the observed
  bronze plus the RLD law, stated on the record, and a later landing supersedes.
* `NFRA_OPLGTW-W4-S4` OBSERVATION/INERT: an identical qualified completion writes no object, so the accelerator fires
  once per distinct closure, not once per clean run. The field set is unchanged.

## 8. Declared limits

* **No live read.** This cell read no object in `opal-data-assets`. How many historical dates would qualify (surplus
  tables, collisions, `null` VersionIds from before versioning) is what `OG-c-2`'s controlled replay measures.
* **Deploy premises for `OG-c-2`:**
  * the deployed runtime's botocore must accept `IfNoneMatch` / `IfMatch` (W4-S2);
  * the existing grants suffice: PutObject+GetObject on `schwab/{m}/meta/*` and silver, ListBucket on the lane's
    `bronze/*`, `silver/*` and `meta/*` (`silver.tf:320-356`, `:511-540` @1bcc827bda);
  * the vendored copy under `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/` is untouched here.
* **The gateway side (`OG-k-1`)** re-implements or imports `validate_closure` and independently HEADs every named object.
  This cell only makes that possible from the one object.
