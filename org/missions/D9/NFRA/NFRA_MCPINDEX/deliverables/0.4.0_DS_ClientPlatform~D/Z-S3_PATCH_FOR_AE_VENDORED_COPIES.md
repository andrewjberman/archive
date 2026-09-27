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

---

## 7. SECOND EDIT, ADDED 2026-09-27T07:4xZ -- the vendoring payload is now TWO changes

`1.0.0_SA_CTO~O` ruled at msg `20260927T072615Z` on row `NFRA_MCPINDEX-Z-S25`, and its step (2) says the
four vendored copies **ride this same Z-S3 worker cell**. So the payload for each of the four files is now
two edits to `mirror_conversion.py`, not one. **Vendoring only section 1 would leave the second defect
live.**

Landed at source: see the commit that carries `test_empty_numeric_cell_is_NULL_not_a_raise_on_the_real_20260829_bytes`.

### The edit

In `_numeric_or_raise`, the string arm. Find:

```python
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
```

and insert the empty case ahead of the `try`:

```python
    if isinstance(v, str):
        if v == "":
            return None
        try:
            return float(v)
        except ValueError:
```

The landed source carries a comment block above `return None` explaining why; copy it or not, but
**`== ""` is the contract and a `.strip()` would be wrong.**

### Why, in one line each

- An EXACTLY-empty CSV field IS the source's null, so mapping it substitutes nothing -- it is not `fillna`,
  and the `None`/NaN arm two lines above already returns `None` for the same reason.
- **Whitespace and every other non-parsing token still raise.** `" "`, `"\t"`, `"n/a"`, `"--"` are a
  rendering the vendor chose, and those stay a reviewed edit.
- Measured case: filepoint `DailyNAV.csv` for 2026-08-29 and 2026-08-30 delivered
  `Median 30 Day Spread Percentage` empty for both funds; the raise failed the whole unit for both funds on
  both dates, which is the 4 missing `fact_dailynav` partitions. Full evidence:
  `PATHFINDER_DAILYNAV_GAP_CAUSE.md`.

### Both edits are in the same function region

Section 1's edit is in `to_arrow`'s column loop; this one is in `_numeric_or_raise`. They are independent
and can be applied in either order, but **both** belong in the same vendoring so the four bundles do not
end up split across two states.

### After the deploy -- step (3), and it is NOT this lane's

The CTO's step (3): once the vendored copies are live, **re-convert 2026-08-29 and 2026-08-30**, which
writes the 4 named `fact_dailynav` partitions. That is a literal-key write of four keys the actor controls,
so NEVER-1's never-widen sign-off does not reach it (its own non-application clause). It is not started and
is not mine: nothing is backfilled until that deploy is live.

---

## 8. THE UNMEASURED PANDAS QUESTION, NARROWED -- added 2026-09-27T08:2xZ

Section 6 said "which pandas the four Lambdas actually run is NOT measured here". It is still not measured,
but the read is now one step from done and the next reader should not restart it. Measured on
`opal-assets-silver-etf`:

```
Runtime      : python3.11
Layers       : arn:aws:lambda:us-east-1:313476888478:layer:pandas-pyarrow-layer:1
CodeSha256   : ZyhzyrjuHLi9TfRC9CFSpvPHY6Rcyq/aPgseJafmuTg=     (at 2026-09-27T08:1xZ, pre-MX-s-8)
layer created: 2026-01-15T10:33:11Z   size 67,631,690   Description: EMPTY
```

**Two things that separates, which are easy to conflate:**

- **The FUTURE-IMPORT question is moot on this plane.** The runtime is python3.11, where PEP-604 `X | Y`
  evaluates natively. So Z-S18's `from __future__ import annotations` concern -- and ADHC_DSFLOW.004's
  "Python 3.9 runners" premise -- does not bite these four functions. It bites whatever actually runs 3.9.
- **The DTYPE question turns on PANDAS, not on python**, and that is the one that decides whether sections 1
  and 7 repair a live defect or pre-empt a latent one. The version is not in the layer's description, so the
  remaining read is inside `pandas-pyarrow-layer:1` itself.

**Why I stopped here rather than pulling the layer.** Reading it means fetching 67 MB, and the answer would
not change any act of mine or of the vendoring: both hunks land either way, and `s8.AC1` grades their
presence, not their necessity. Under CLAUDE.md section 2 that makes the next check unowed at this seat. It
IS owed wherever the framing matters -- a release note that says "fixed a live defect" versus "closed a
latent one" is a different claim, and only the pandas version settles it.

**The cheap read, for whoever wants it:** the layer zip's `pandas-*.dist-info/METADATA`, or a one-off
`python -c "import pandas; print(pandas.__version__)"` in a throwaway function on the same layer. Do NOT try
to get it out of `opal-assets-silver-etf` by invoking it: `lambda_entry` accepts only an S3-event shape or
`{"mode": "sweep"}`-style sweep mode and refuses anything else by design, so there is no version echo to
call, and an S3-shaped payload would DO CONVERSION WORK rather than answer a question.

---

## 9. PRE-DEPLOY BASELINE for `s8.AC1` -- captured 2026-09-27T09:1xZ, BEFORE MX-s-8 lands

A baseline is only takeable before the act, so it is taken here. `s8.AC1` requires both fixes in **4 of 4**,
and the cheapest way to catch a partial deploy is that **every one of these four values must MOVE**:

| function | CodeSha256 (pre-MX-s-8) | LastModified |
|---|---|---|
| `opal-assets-silver-etf` | `ZyhzyrjuHLi9TfRC9CFSpvPHY6Rcyq/aPgseJafmuTg=` | 2026-09-26T09:26:39Z |
| `opal-assets-silver-orion` | `rwI6QN5qzT30lWZrf87RlSOEl5XmSGkCTUTdlljqDPo=` | 2026-07-15T22:32:26Z |
| `opal-assets-silver-eclipse` | `5hRkhhxIMZ2hiAqZWtfVtUnwXZt3xeKPnLryWOo5OJU=` | 2026-07-22T14:50:08Z |
| `opal-assets-silver-blackdiamond` | `XiJ6ZADpVAwtJcRR4U0l/IhO4+eFfzost0Mz9fnTIJA=` | 2026-08-25T17:14:42Z |

**Read at the same moment: the MX-s-8 deploy is NOT live.** All four still carry their pre-MX-s-8 bytes, so
nothing in sections 1, 7 or 8 has been served yet and the 4-partition backfill stays gated. This table is
the negative control for that statement, not a prediction.

### The thing this table exists to catch

**The four bundles are NOT in lockstep -- they are months apart** (2026-07-15, 07-22, 08-25, 09-26). Four
different shas, four different vintages. Two consequences for the vendoring:

1. **A partial deploy is the realistic failure, not a total one.** If one or two functions move and the
   others do not, every symptom stays exactly as it is today for the unmoved ones, and the only tell is a
   sha that did not change. Grade all four by this table, and print 4 of 4.
2. **Section 5's "diff each copy against the source" will show pre-existing differences beyond the two
   hunks**, because these copies were trimmed and vendored at different times (hence the guard sitting at
   `:277`, `:275`, `:330`, `:330`). That is expected. The check is "the only NEW difference is the two
   hunks", not "the copies become identical to the source".

### Note on which functions the dailynav path actually needs

The pathfinder / filepoint conversion runs in `opal-assets-silver-etf`. So the **backfill** in
`PATHFINDER_DAILYNAV_GAP_CAUSE.md` section 8 is unblocked by that ONE function moving and serving both
hunks -- but `s8.AC1` is the COO's criterion across all four, and the other three carry the same latent
defect for their own sources. **Do not read "etf moved" as "MX-s-8 is complete."**
