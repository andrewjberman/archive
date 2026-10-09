# X2 GLOBAL BASIS -- why the combined all-firms `global` figure reveals nothing about any single firm's clients

Cell CN-b-2 (PRD DEC-7, FWD-3). Producer read: `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` (the fold's call site) and
`data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py` (`build_global_artifact`, the fold itself). No client figure or
account id is quoted here; all evidence is code position.

## Aggregation level

One `global` figure is a per-date sum over FIRMS, never over accounts. The consolidator runs the fold once, after the three firm legs
have built (`mdpf_gold_consolidator.py:2524-2535`, `_fold()` then `arts["global"] = _isolated("global", _fold)`), and hands it the three
already-aggregated firm artifacts: `spine.build_global_artifact(arts["49financial"], arts["inflection"], arts["cottonwood"])`
(`mdpf_gold_consolidator.py:2532`). The fold is `dim_mdpf_aggregate_aua_timeseries.py:2245` (`build_global_artifact`), joined by date
over the union of the three firms' date axes (`:2309`). Per date it adds one firm-level number per leg: `model_aua` is
49financial + inflection (+ cottonwood where in coverage) (`:2420-2429`); `non_model_aua` is the 49financial value alone (`:2435`);
`custody` is a two-firm sum (`:2439`). The inputs are firm-level series, so the sum is over firms. The `by_model` map is a cross-firm
fold keyed by model name (`:2504-2522`, `:2631`): each entry is a model's total across the firms, not a list of the model's accounts.

## Minimum firm count

Minimum firm count: 2.

Evidence: a figure exists on a date only if every contributing leg is present, because the sums are None-poisoning. `_sum2`
(`dim_mdpf_aggregate_aua_timeseries.py:2399-2400`) returns None if either operand is None. For `model_aua` and `opal_aggregate_aua`,
the branch with no cottonwood leg (`:2427-2429`) needs both 49financial and inflection, and the branch with cottonwood
(`:2422-2425`) needs all three, otherwise the cell is None. The two-firm `custody` series is the same `_sum2` over 49financial and
inflection (`:2439`). So no non-null figure combines fewer than 2 firms; 2 is the floor (49financial + inflection), 3 the full
fold, with cottonwood structurally absent before its first coverage date (`:2284-2289`, the cottonwood fold discriminator comment). At the run level the fold needs all three
firm artifacts and refuses otherwise (`mdpf_gold_consolidator.py:2525-2531`, "global fold SKIPPED"), so no single-firm `global`
artifact is ever emitted. The one-firm case is a null cell, not a figure; no figure combines fewer than 2 firms, so no row is filed.

## Why no per-firm or per-account row survives

The fold's output is the dict returned at `dim_mdpf_aggregate_aua_timeseries.py:2798-2905` (Lambda key
`portal/gold/mdpf/global/...`). Field by field:

- `firm_id` ("global"), `as_of_first`, `as_of_last`, `n_dates`, `dates`: scope label and the date axis.
- `opal_aggregate_aua`, `model_aua`, `non_model_aua`, `inflection_non_model_aua`: arrays of one number per date. These are the
  cross-firm sums above, except `non_model_aua` (49financial's alone, `:2435`) and `inflection_non_model_aua` (inflection's alone,
  carried as an audit array). Each is one value per date, with no firm key and no account key. These two single-firm series are the
  documented basis-B exceptions (they are firm-level aggregates, not client rows, and carry no account identifier).
- `by_model`: one entry per model name in the fixed `GLOBAL_MODEL_KEYS` tuple; its arrays are per-date model totals and per-date
  `account_count` integers. Keys are model names, never account ids.
- `cohort_provenance`, `point_class`, `count_provenance`, `count_basis`, `count_as_of`, `source_vintage_last`: per-date labels and
  vintage dates (categorical or dates, no dollars per client).
- `account_count_total`, `account_count_total_raw`: one integer per date, the total number of accounts. A count, not a list.
- `meta`: build stamps, the per-firm basis and fee-scope maps (text), channel participation (which firm entered each date, as a
  label), carry policy, `latest_cross_section` (the latest date's global totals) and axis reconciliation (counts and date lists). One
  residual to name: `meta` basis text at `:2911` names the Opal-owned Model Portfolios master account in a descriptive string. That is
  the firm's own model master, a source-description string and not a per-client row; it is the only account identifier in the shape
  and it identifies no client.

No field in the output is a list of accounts, a per-account value, or a client-keyed map; the finest grain is a model name with
aggregate arrays, and the finest account-level fact is an integer count. This matches the ledger's wording for X2: aggregate counts,
status and dates only, no account identifiers (`MDPF_TAXSMA_DATA_CONTRACT.json` `categories.wire_privacy`). Moving X2 to GRANTED
is Andrew's later acknowledgement and is not made here.
