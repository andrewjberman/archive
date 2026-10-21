# FWD-10 enrichment (1): does a typed ETF reach `_compare_stage`? -- measurement, 2026-10-21

**From:** `2.0.0_SA_COO~G2`. **Asked by:** CTO msg 11977. **Read-only, offline.** Instrument: `checks/etf_typed_measure.py` (runs the tree's real `maintained_sources.resolve_comparison_fields` with a classification table naming VNQ, then the exact mapping of `resident_worker._opal_comparables`). Vintage: tree HEAD 1cc43f2edab, whose modules equal the r34s tarball for these files (r34s changed only the five files named in the r34s packet; `maintained_sources.py` and `resident_worker.py` `_opal_comparables` are r34r/r34s-era code). Claim class: MEASURED on the tree; the live resident was not run.

## Result: NO. A typed ETF is admitted but arrives at `_compare_stage` as an empty "other" comparable.

| hop | measured |
|---|---|
| door (`resolve_comparison_fields`) | VNQ not in the Opal catalogue -> `_classified_etf` admits it from `etf-classifications`: entry `{vendor_id: VNQ, name: Vanguard Real Estate ETF, security_type: etf, namespace: YCHARTS, source_id: VNQ, mapping_evidence}` |
| `has_key_field` | **False.** The door drops `key` from every catalog entry (`maintained_sources.py:614`, `:627`); the key is the dict key |
| `_opal_comparables` (`resident_worker.py:547`) | `ticker = c.get("key") if security_type == "etf"` -> **None**. Output `{key: VNQ, label: ..., ticker: null}` |
| `_compare_stage` (`opal_producer.py:449`) | `elif entry.get("ticker")` false -> the `else` branch: kind "other", no series, no allocation, no reason. No price is read, so no vendor call is made either |

Cause: AR-g-182 zipped the browser's `comparison_keys` with the entries to recover the key for a model, but kept `c.get("key")` for the ETF ticker. The offline ETF tests passed because they handed the producer a comparable that already carried `ticker`.

## Fix (one wiring cell, failing-first, r34t)
`ticker = key if c.get("security_type") == "etf" else None` in `_opal_comparables` (the zipped key; the ticker is the key, as the door states: vendor_id VNQ). Test: the real door output through `_opal_comparables` yields `ticker == "VNQ"`; then the existing ETF arm prices it through the holdings' tiers (estate, yfinance, ycharts) and classifies it through `stores["classifier"]`.

Not measured: whether the estate or yfinance tier holds the typed ticker's history (the ycharts tier, a vendor call, is last in the chain and runs only if both miss). That is run 7M's read, with an ETF the estate holds.

## Item (2): page 60 as-of per model
`model_source.read_allocation` returns one `as_of` (`data_as_of`); `comparables.py:178` prints it for every model row. The per-model dates (ST 2026-10-08, LT 2026-08-18) are each portfolio entry's `data_as_of` in the same file (7J read, observation 4; the field is to be confirmed on the live object by the cell's first test). The cell reads each model's own date and prints it in the row's basis. Same release.
