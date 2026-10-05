# ETFS_RIVALS -- the IDVZ/PFOE Bloomberg backfill to 2026-01-01 (D12): how it runs without widening served output

Authority: Andrew-direct @a36e70f335 ("We definitely can get the data on IDVZ and PFOE back to January 1 via BBG through the
original backfill ... go pick up ad hoc"); 3-year cap @357e681ddf. Traced read-only 2026-10-05 ~05:4xZ (code + live AWS reads).

## What a bare backfill would do (DO NOT RUN)

`python -m rivalfunds.collector_bloomberg --mode backfill --start 2026-01-02 --end 2026-10-02`:
- has no fund-list argument (`collector_bloomberg.py:553-566`); it queries the bloomberg_primary funds (TXUE, BIDD, CGIC, INEQ,
  SCHY) plus issuer_first funds lacking issuer bronze (`:313-316`) -- NOT IDVZ/PFOE (home_producer) unless the leg gate is set;
- writes 189 captures + sidecars to `bloomberg/etfs/bronze/holdings/date=<capture UTC day>/` and ONE `fetch-bloomberg` marker at
  `rivalfunds/etfs/state/fetch_bloomberg/date=<event.date or the last day>/` (`:486`, `:451`, `:533`);
- **that marker is consumed within seconds by the S3 event rule `rivalfunds-build-silver-bloomberg-on-marker-created`**, which
  matches the WHOLE `fetch_bloomberg/` prefix (generated.auto.tfvars.json:55-58; ENABLED live): silver_bloomberg in daily mode
  for that batch -> canonical-shape, coverage, gated trade schedule (`sweep.py:389-411`). Live: the 10-03 marker 07:06:49 ->
  silver 07:06:57 -> canonical 07:07:36. So a bare backfill rebuilds ~189 report dates of served G1. A `date` override does not
  help: the rule matches every partition. The 09:00 sweep itself reads only its own day (`sweep.py:219`, `:453`).
- For home_producer funds, Bloomberg silver changes nothing while the policy holds (`silver_bloomberg.py:194-201`,
  `gold_canonical_shape.py:380-384`). No live Lambda has the leg gate set (all three environments read).

## The plan

- **Step A (inert, any time the Terminal is up and outside the 07:00 ET vehicle):** pull IDVZ and PFOE to a LOCAL sink through
  `handler_entry` (it takes `funds`), writing nothing to S3:
  `handler_entry({'mode':'backfill','start':'2026-01-02','end':'2026-10-02','funds':['IDVZ','PFOE'],'sink':'local:C:/bbg_backfill/idvz_pfoe','batch_id':'backfill-d12-idvz-pfoe'})`
  with `PYTHONPATH=<repo>;<repo>\data\etfs\scripts`. Measured cost basis (row Z-S20): IDVZ ~45 + PFOE ~24 rows a day, under any cap.
- **Step B (served; after the round-8 merge, after the D12 gate flip incl. the Lambda environment, under its CTO+COO never-widen
  pair):** `mode:'import'` of the local capture `.json` files (not sidecars) with a recent `date`, so any G1 cursor stays inside
  the sweep's 10-day lookback; import skips a capture already in the partition with the same sha256 (`:164-196`).
  Blast radius: bronze `date=<capture UTC day>/` (189 + 189), `state/fetch_bloomberg/date=<D>/`, silver
  `bloomberg/etfs/silver/holdings/date=<each report date>/` IDVZ-*/PFOE-*, `state/build_bloomberg_silver/date=<D>/`, gold
  `canonical_shape/date=<each report date>/` + cursor + marker, coverage, then the gated trade schedule and the page.
- The ACWI/IWM (D13) backfill follows the same two steps after the D13 flip, inside CTO~Z's budget ruling (msg 29445: 1M rows,
  per date, stop on first failure, cost measured first).

Not measured: the local sink's on-disk layout; whether any day returns no rows for IDVZ or PFOE (a no-rows day withholds the
batch marker, `:534-535`).
