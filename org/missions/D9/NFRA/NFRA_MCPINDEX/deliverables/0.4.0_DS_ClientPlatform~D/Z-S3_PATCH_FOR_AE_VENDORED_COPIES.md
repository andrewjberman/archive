# Z-S3 patch handoff to `0.7.0_AE_CloudOps~I` -- the 4 vendored `mirror_conversion.py` copies

**From:** `0.4.0_DS_ClientPlatform~D` · **Source fix landed:** `8ba0d6645b` (source copy + tests only)
**Routed by:** `1.0.0_SA_CTO~O` msg `20260927T051535Z` -- "Source copy only ... Hand the patch to
`0.7.0_AE_CloudOps~I`." · **Written:** 2026-09-27T06:0xZ

A unified diff is NOT given, and deliberately: the four copies carry this block at four different line
numbers, so one patch file cannot apply cleanly to all of them. The exact before/after text plus the four
targets is what applies by hand or by script.

## 1. THE EDIT -- one condition, plus the comment that explains it

Find, in each file, the ONLY occurrence of this line:

```python
        elif t == "float64" and df[c].dtype == object:
```

Replace the condition (keeping the body untouched) with:

```python
        elif t == "float64" and (df[c].dtype == object
                                 or pd.api.types.is_string_dtype(df[c].dtype)):
```

`pd` is already imported in every copy, so no import changes. The landed source adds an explanatory
comment above `df[c] = df[c].map(...)`; copy it or not, but the condition is the contract.

## 2. THE FOUR TARGETS, enumerated by PATTERN not by a list I was handed

```
infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py        :277
infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py      :275
infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py          :330
infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py :330
```

**It is FOUR, not five.** Row Z-S3 says the file is vendored into "blackdiamond, eclipse, etf, orion and
schwab". `opal-assets-silver-schwab` carries **no** `mirror_conversion.py` -- it has its own
`schwab_conversion.py`, which does not contain this guard. A repo-wide search for
`float64" and df[c].dtype == object` returns exactly these 4 plus the now-fixed source. Re-run that search
before you sign, so the enumeration is yours and not mine.

## 3. WHY THIS EDIT, in one line each

- pandas 3 can hold a text column as the `str` dtype; `== object` is False for it.
- So `_numeric_or_raise` was never called, and the module's documented promise -- "a string that does NOT
  parse RAISES naming column and value" -- was not kept on a pandas-3 runtime.
- **Not data corruption.** The physical arrow/parquet type is `double` in every arm. Two harms only:
  a bad cell raises pyarrow's `ArrowInvalid` (naming neither column nor vendor) instead of
  `VendorDriftError`, and a good cell's pandas metadata carries `numpy_type=str`, so a pandas reader gets
  strings back out of a physically-double column.

Measured on pandas 3.0.3, `orion`/`assets`.`currentShares`, all four arms:

| dtype | value | before the fix | after |
|---|---|---|---|
| object | `'1.5'` | OK, 1.5 | unchanged |
| object | `'n/a'` | `VendorDriftError` (the design) | unchanged |
| `str` | `'1.5'` | OK but round-trips **str** | round-trips float64 |
| `str` | `'n/a'` | **`ArrowInvalid`** | `VendorDriftError` naming column + value |

## 4. THE PRECEDENT -- this is not a new pattern in this estate

`data/assets/scripts/silver/etf_conversion.py:209` **already** carries exactly this condition, with the
comment "NOT `dtype == object`: pandas 3 infers a column of strings as the `str`", and its own belt at
`data/assets/scripts/silver/tests/test_etf_conversion.py:445`. The etf bundle's vendored
`etf_conversion.py:209` also already has it. So the same class was found and fixed once before; this is the
mirror framework catching up to its sibling, and your vendoring step has done it before.

## 5. HOW TO PROVE IT IN A BUNDLE

The bundles carry no tests, so the source belts cannot run there. Two checks that do work:

1. **Byte check** -- after the edit, every vendored `mirror_conversion.py` should differ from the landed
   source copy only where it already differed (the copies are not line-identical: 277/275 vs 330 says they
   are trimmed differently). So diff each copy against the source and confirm the ONLY new difference is
   this condition.
2. **Behaviour check, per bundle, no deploy needed** -- import the bundle's own `mirror_conversion` with
   its directory on `sys.path` and assert both arms directly:

```python
import pandas as pd, mirror_conversion as mc, mirror_schemas as ms
src, feed = "orion", "assets"          # or the bundle's own source/feed
fcol = next(c for c, t in ms.DECLARED[(src, feed)].items() if t == "float64")
rec = {c: {"string": "x", "int64": 7, "float64": 1.5, "bool": True, "json": "{}"}[t]
       for c, t in ms.DECLARED[(src, feed)].items()}
df = pd.DataFrame([rec])
for c, t in ms.PROVENANCE_COLS.items():
    df[c] = "p" if t in ("string", "json") else 1
df[fcol] = pd.Series(["n/a"], dtype="str")
try:
    mc.to_arrow(df, src, feed)
    print("NOT-OK: no raise")
except mc.VendorDriftError as e:
    print("OK:", fcol in str(e) and "n/a" in str(e))
```

This needs a **pandas 3** interpreter to be meaningful. On pandas 2 the `str` dtype does not arise and the
test passes vacuously -- which is worth knowing before you read a green as evidence.

## 6. WHAT IS NOT MINE, AND NOT DONE

- **No deploy, no vendoring, no sign-off from this lane.** The CTO put the four copies on the AE lane under
  a never-widen sign-off; this file is the patch, not the act.
- **Which pandas the four Lambdas actually run is NOT measured here.** It decides whether the fix is
  repairing a live defect or closing a latent one in each bundle, and it is the one number that would turn
  this from hygiene into a live repair. Your lane can read it from the bundle's runtime; I did not.
- A sibling of this defect with a SHARPER consequence is filed separately as row
  `NFRA_MCPINDEX-Z-S24` against `data/black_diamond/scripts/silver/convert_assets_to_silver.py` -- there the
  same `== object` guard wraps a `pd.to_numeric` call, so on pandas 3 the column would land as a STRING in
  silver rather than merely carrying bad metadata. It is INERT today on production evidence.
