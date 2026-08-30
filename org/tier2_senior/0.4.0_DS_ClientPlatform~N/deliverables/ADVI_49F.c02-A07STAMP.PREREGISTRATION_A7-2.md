# A7-2 PRE-REGISTRATION -- ADVI_49F.c02-A07STAMP (cell C02-g-10)

**Written 2026-08-30T13:26:28Z, BEFORE either run.** Seat `0.4.0_DS_ClientPlatform~N`.
Criterion A7-2: *"one ad-hoc run at date D to a SCRATCH root; `_ingested_at == D` and
`source_pipeline == "49f-gold-runners"` on both outputs; every other column byte-identical to the
served partition at D (denominator = each table's column count, both printed); a third moving
column FAILS."*

## D, and the baseline as MEASURED (not assumed)

`D = 2026-08-28` -- the latest served date on both tables (540 served dates each, read from
`s3://opal-data-49financial/gold/advi/dimensions/`).

| table | rows served @ D | COLUMN DENOMINATOR | `source_pipeline` served | `_ingested_at` served |
|---|---|---|---|---|
| `dim_asset_classification` | 3,864 | **10** | `canonical-dims/a07_dim_asset_classification` | `2026-08-30T12:47:05Z` |
| `alias_key_expansion` | 4,165 | **8** | `canonical-dims/a07_dim_asset_classification` | `2026-08-30T12:47:05Z` |

The served `_ingested_at` on the `date=2026-08-28` partition is **2026-08-30T12:47:05Z** -- a clock
read two days after the content date. That is the defect, measured on the served object, not
inferred from source.

## THE TRAP THIS PRE-REGISTRATION EXISTS TO CLOSE

**a07's output for a fixed D is NOT a function of D.** It classifies against the LIVE DynamoDB
`bd-securities` substrate, so the same partition re-run at a different time yields different
content. This is measured, not suspected -- `_manifests/2026-08-28/` holds **two** builds of the
same date:

```
20260829T124649Z__alias_key_expansion.json   rows=4164  content_hash=a86546af...
20260830T124705Z__alias_key_expansion.json   rows=4165  content_hash=efd49051...
```

**4,164 -> 4,165 rows and a different content hash, same D, one fire apart.** So a straight
comparison of my run against the served partition CANNOT distinguish "my change moved a column"
from "DynamoDB moved between 12:47Z and now". A criterion scored that way would be scored by the
substrate's drift rate, not by my edit.

**THE CLOSURE: a PAIRED run.** The pre-fix bytes (`git show HEAD:...`, the 2 pre-fix stamp lines
confirmed present) and the post-fix bytes are run **back to back into two scratch roots, minutes
apart, against the same DDB state**. Pre-vs-post is then attributable to the edit alone. The
served partition at D is still compared as the criterion's literal ask -- but any difference there
is reported with the DDB-drift caveat NAMED, never silently scored as a pass or a fail.

## THE PREDICTION -- registered before the runs

**PRE-fix run vs POST-fix run, same D, same window:**

1. `dim_asset_classification`: **exactly 2 of 10** columns differ.
   - `source_pipeline`: `canonical-dims/a07_dim_asset_classification` -> `49f-gold-runners`
   - `_ingested_at`: a `%Y-%m-%dT%H:%M:%SZ` clock -> the literal `2026-08-28`
2. `alias_key_expansion`: **exactly 2 of 8** columns differ, the same two, the same way.
3. The remaining **8 of 10** and **6 of 8** columns are byte-identical pre-vs-post.
4. Row counts identical pre-vs-post on both tables.
5. The `A5-A07-DETERMINISM key: content hash` line printed by both runs is **IDENTICAL** -- the
   hash is computed at `:348-349`, BEFORE the stamp, so the remedy cannot move it. A moved hash
   means DDB drifted between the two runs and the paired comparison is void; it does NOT mean the
   stamp changed the content, and it will not be reported as either.
6. `process_ts` (manifest only, `:394`) still differs between runs -- it is a build-event field and
   is NOT a served column. It is excluded from the column comparison BY NAME, declared here in
   advance, not discovered afterwards.

## THE FALSIFIER

**A third moving column FAILS this criterion.** If any column outside
{`source_pipeline`, `_ingested_at`} differs pre-vs-post on either table, A7-2 is NOT MET and is
reported NOT MET. Both column denominators (10 and 8) are printed beside the result.

Equally: if `_ingested_at` is anything other than the literal string `2026-08-28` on either output,
or `source_pipeline` is anything other than `49f-gold-runners`, A7-2 is NOT MET.
