# TP1AE-AC4 / D1-inv-3 -- PRE-FIRE BASELINE (captured before the 2026-08-28 13:30Z run)

**Seat:** `0.7.0_AE_CloudOps~Z` · **TO:** `D1_CATVIEWS.TO-P1-AE` · **Captured:** 2026-08-28 ~02:4xZ

---

## WHY THIS EXISTS AND WHY IT COULD NOT WAIT

> `TP1AE-AC4` -- **`D1-inv-3` byte-unchanged** -- legacy `non_model` fields identical **before/after**,
> **by hash or ETag**, not by inspection.

⛔ **THE "BEFORE" IS PERISHABLE AND THE "AFTER" IS NOT.** Every other criterion on this TO is gated on
the 13:30Z scheduled fire. This one has a half that is only capturable **while the fire has not yet
run**. Captured after the fact it is not a measurement, it is a reconstruction from S3 version history
-- a strictly weaker evidence class for the one criterion the TO calls *"the regression direction that
announces nothing if it breaks."*

⚠ **AND THE OBVIOUS INSTRUMENT IS THE WRONG ONE.** The fire writes a **NEW dated key**; it does not
rewrite `2026-08-26.json`. So a whole-file ETag comparison across the fire compares two different
days and **always differs** -- it would report a violation on a perfectly correct run. What must be
unchanged is the **`non_model` FIELD CONTENT**, so the baseline hashes the fields, canonically encoded,
independently of the file that carries them.

## WHAT WAS CAPTURED

| artifact | file | | |
|---|---|---|---|
| per-field hashes | `D1_CATVIEWS.TP1AE-AC4_PREFIRE_BASELINE.json` | **15 field captures** across **5 artifacts** | canonical `json.dumps(sort_keys, separators)` -> sha256 |
| full key manifest | `D1_CATVIEWS.TP1AE-AC4_PREFIRE_KEY_MANIFEST.json` | **292 keys**, `portal/gold/mdpf/` | Key + Size + ETag + LastModified (s3api, **UTC**) |

Fields tracked: `non_model_aua` · `non_model_assets_detail` · `inflection_non_model_aua`, at every
depth (including `meta/latest_cross_section/...` and inside `time_series[]`).

Artifacts (newest per scope/type carrying those fields), all `2026-08-26.json`:
`49financial` · `cottonwood` · `global` · `inflection` aggregate-aua-timeseries, plus `global`
non-model-assets.

## TWO CONSISTENCY CHECKS THAT FELL OUT OF THE CAPTURE

These were not sought; they are worth recording because they show the extractor read the right thing.

1. `non_model_assets_detail` hashes **identically** (`74234e98...`, canonical `null`, 4 B) in
   **exactly** the three NON-global scopes. That is what the deployed consolidator says it should be:
   `:486` / `:493` -- `... if scope == "global" else None`. **Code and served artifact agree.**
2. `inflection_non_model_aua` inside `time_series[]` hashes **identically** (`dd7889d6...`) in BOTH
   `global/aggregate-aua-timeseries` and `global/non-model-assets` -- the same value carried in two
   artifacts, agreeing.

⛔ **NEITHER IS A PASS FOR ANYTHING.** They evidence that the extraction is pointed at real fields, not
that `D1-inv-3` holds -- which is unmeasurable until an "after" exists.

## HOW TO SCORE AC4 AFTER THE FIRE

```
1  re-read the SAME five 2026-08-26 keys      -> whole_file_sha256 + ETag MUST be unchanged
                                                 (the fire must not rewrite a settled day)
2  re-run the field extractor on the NEW dated artifacts, and compare the non_model field hashes
   for every as-of date present in BOTH                 -> MUST match the baseline entry for that date
3  diff the 292-key manifest                   -> EXISTING key with a changed ETag/Size = REWRITE,
                                                 which D1-inv-3 forbids. NEW dated keys are EXPECTED
                                                 and are NOT a violation.
```

⚠ **BOUND -- WHAT THIS BASELINE CANNOT DO:** it fixes the *before* only for the artifacts and dates
listed. A `non_model` regression confined to a scope or date **not** in this capture would not be
caught by it. The 292-key manifest is the wider net and it detects **rewrites**, not value drift inside
a newly written key.

⚠ **AND IT IS A BASELINE, NOT A VERDICT.** `AC4` is UNMEASURED and stays UNMEASURED until the fire
produces an "after." Nothing here should be read as AC4 passing, or as predicting that it will.
