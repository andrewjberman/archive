# VERIFY #23 -- target: unknown

- is_real: **False**
- confidence: **refuted**
- corrected_severity: low

## Reasoning
The flag has a nugget of truth (the `x or 0.0` idiom does not default a present-but-NaN value, since `NaN or 0.0 == NaN`), but both of its concrete failure scenarios are refuted or unreachable at the real code/data.

CRASH VARIANT (Float64 pd.NA -> TypeError -> leg dark): REFUTED by grounded dtype. In convert_eclipse_portfolios_to_silver.py, `model_aum` (API `modelAUM`) is in NO typed bucket for model_composition (`_COMP_INT_FIELDS` line 80; no float_fields arg at the line-307 `_coerce_frame` call; not bool/date/json). It only hits the fallback (lines 177-181: object->pandas `string`, else keep inferred dtype); `coerce_silver_ids` (line 310) touches only ID cols. The API returns `modelAUM` as a JSON number, so pandas infers plain numpy float64 — never nullable Float64. Live `silver/eclipse/2026-07-06/model_composition.parquet` confirms `model_aum dtype: float64`. The flag itself conditions the TypeError on "If silver typed model_aum as nullable Float64," which is false; the fallback never produces Float64.

WRONG-OUTPUT VARIANT (float64 NaN -> silent NaN firm headline): mechanism is logically correct but the TRIGGER is not reachable. It requires a model row to EXIST with a null/absent model_aum (dict-miss -> None -> `None or 0.0` = 0.0 is handled fine; only present-NaN propagates). Live data: `model_aum null count: 0`; all 9 models populated; the two empty SMA models (id 9,10) return exactly 0.00, not null — so the Eclipse API's demonstrated convention for a zero-AUM model is 0.0, not null. `0.0 or 0.0 == 0.0` is also correct, so even legit zeros are harmless. No observed path yields a null modelAUM.

NOT CURRENTLY FIRING / no accidental NaN: served gold summary (INF_E_00 lines 260/279/290) firm row `model_aum_eclipse = 128449850.64` (= sum of the 9 model AUMs), `model_aum_eclipse null count: 0`; `gold_complete.json` firm_headline `model_aum_eclipse: 128449850.64` with NO `NaN` token (checked live). All nine `aum_map.get(mid)` lookups resolve (Int64 index key vs Python-int mid are hash/compare-equal — confirmed by matching per-model values), so there is no key-mismatch NaN either.

Per the "default to refuted when no concrete triggering path can be constructed" bar: the crash is dtype-refuted, and the wrong-output requires an external-API null that contradicts observed behavior and live data. Residual truth = a cheap latent robustness gap: `aum_map.get(mid) or 0.0` should be an explicit null guard (e.g. `v = aum_map.get(mid); 0.0 if v is None or pd.isna(v) else float(v)`) or the silver converter should pin `model_aum` to a typed float with an explicit fillna. That hardening is warranted but is low-severity (latent, not firing, crash-variant impossible at the real dtype), not the flagged high-severity crash/mis-served-headline.
