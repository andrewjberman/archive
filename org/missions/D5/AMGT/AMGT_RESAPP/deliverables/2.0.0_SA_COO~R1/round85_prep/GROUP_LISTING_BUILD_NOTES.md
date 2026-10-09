# AMGT_RESAPP round-85 PREP -- the ASML listing collapse: write path, read path, CIK source, cells and pairs

Grounding fork of `2.0.0_SA_COO~R1`, 2026-10-09 ~12:1xZ. READ-ONLY (no store write, no deploy, no model call). Builds on
`round84_prep/GROUP_LISTING_NOTES.md`; rulings: DSGN `CTO_RULING_ROUND57_R1A_R6_20261009.md` ADDENDUM 2, CTO~DELL1 msg 2302, round-84
analysis item 3 (`ledger/ROUND_ANALYSIS.round84.md`).

## 1. The name list: where it lives, who writes it, who reads it

- **Store:** `s3://opal-data-harvest/crosswalk/v1/<YYYY-MM-DD>.json` (`lib/research/identity/crosswalk.py:70-72`, `POOL_BUCKET`,
  `CROSSWALK_PREFIX`). Latest today: `crosswalk/v1/2026-10-07.json` (800,952 bytes, 243 records); 5 dated objects under the prefix.
- **Writers (3 entry points, ONE choke point):** every put passes `crosswalk.write_pool` (`:1413`), which unions the latest served
  document first (a served record leaves only by `--retire`) and validates against `crosswalk.schema.json`. Callers:
  `python -m lib.research.identity.crosswalk --as-of <date> --write-pool` (`main`, `:1516`), `add_security.py`
  (`_persist_registration_and_pool`), `build_universe.py` (`union_main`). All are HAND-RUN: no schedule, rule or Lambda in `infra/`
  invokes them (census over `infra/`: 0 hits for the three entry points).
- **Serve-time read:** the live function `opal-amgt-scoped-api` reads the list from S3 at request time:
  `name_search.resolve_query` (`lib/research/api/name_search.py:77-85`) -> `crosswalk.resolve` / `crosswalk.load_crosswalk()` ->
  `_read_pool_latest` (`crosswalk.py:1236`) = the LATEST key under `crosswalk/v1/`. The function sets no `AMGT_CROSSWALK_PATH`
  (env holds only `HARVEST_ARTICLES_TABLE`, `HARVEST_METRICS_TABLE`), so nothing is packaged: **a new crosswalk object is served
  the moment it is the latest key**.

So: publishing the new list IS a served-store write (one new versioned key, put-if-absent by date; rollback = the prior key stays and a
newer dated object re-carrying the prior document, never a delete) and needs a never-widen pair with this writer census. The resolver
change (`name_search.py`, and the `identity.other_listings` line in `scoped_amgt.py`) is code inside the function's closure: it needs a
redeploy of `opal-amgt-scoped-api` (a CODE leg, pair + `0.7.0_AE_CloudOps~RA1`).

## 2. The CIK: measured sources and coverage (243 records)

| source | what it is | coverage | measured or inferred |
|---|---|---|---|
| `identity.cik` (crosswalk field today) | registered identity block | 65 of 243 | measured |
| SEC ticker-to-CIK table `s3://opal-data-harvest/sec/harvest/bronze/company_tickers/date=2026-09-22/company_tickers.json` (10,459 tickers; the source ASML_US's provenance text names) | a US ticker -> CIK | 171 of 188 `_US_Equity` records by root ticker | measured for a US listing |
| same table, matched on a NON-US listing's root ticker | e.g. `ASML_NA` root `ASML` -> 937966 | 16 of 55 non-US records | **inferred** (a name/ticker match on another listing) -- not a served identity |
| the record's own stored 20-F/10-K (`sec/harvest/silver/filing_source` row `url` .../edgar/data/<CIK>/...) | the filer that filed this name's stored filing | 13 names with a stored filing | measured (the filing the name serves) |
| CIK only inside free text (`provenance`, `source_row` evidence) | 127 records | -- | not a served identity until measured (CTO msg 2302) |

The two ASML rows: `ASML_US_Equity` -> 937966 from the ticker table on its own US ticker (measured); `ASML_NA_Equity` -> 937966 from
the EDGAR path of its OWN stored 20-F (`000162828026011378`, measured). Both measured, same CIK, so the collapse arm applies. (BABA
1577552, NU 1691493, PBR 1119639, SAP 1000184 come from their stored filings the same way.)

**Precedence for `issuer.cik`, each value carrying its claim (`measured` + source):** `identity.cik` where registered; else the record's
own stored filing's EDGAR CIK; else the ticker table on a `_US_Equity` record's own ticker. Never the ticker table on a non-US root, and
never a CIK read from text.

## 3. Names that must still list

At HEAD, `round84_prep/checks/r84_listing.py --crit AC1`, both arms identical:
- `--where local` and `--where deployed`: R1 FAIL ("ASML" 404 with two candidates), R2 PASS ("Micro" lists AMD, MSFT, MU -- three
  issuers, three CIKs), R3 PASS (resolve "Nu", "zzqx" and thesis "zzqx" byte-equal to the base, 3 of 3) -> `R84 LISTING AC1: NO`.
The check already has a `--where deployed` arm, so the same check grades the redeploy. R2 stays the negative arm: the collapse requires
every candidate to carry the SAME measured CIK, and "Micro"'s three do not.

## 4. The cells and the pairs owed

The CTO's item 3 says one cell when the route serves no issuer id: "the cell makes the route serve one, and the collapse follows in the
same cell". The store and the function are two separate world objects, so the honest cut is ONE build cell plus TWO world acts:

1. **Build (LOCAL, worker):** `crosswalk.py` `build_crosswalk` carries `issuer.cik` by the precedence above (+ schema field, +
   tests); `name_search.resolve_query` collapses only when every candidate shares one non-null measured `issuer.cik` and exactly one is
   covered; `scoped_amgt.py` serves `identity.other_listings`. Proven `--where local` with `AMGT_CROSSWALK_PATH` pointed at a dry-run
   document (`crosswalk --dry-run` output): r84_listing R1 YES, R2/R3 PASS; plus `crosswalk --disclosure` denominators unchanged.
   Not a site-Z producer path (crosswalk and name_search are not the 20-F producers).
2. **Store (WORLD):** `crosswalk --as-of <date> --write-pool` publishes the new dated key. Pair COO + 1.0.0_SA_CTO~DELL1: blast radius
   one new key (union-first, no record dropped), writer census N = 3 entry points, both branches (old code ignores `issuer`; new code
   collapses). Ordering: publish the list BEFORE the redeploy -- the live function then serves byte-equal answers until the code lands
   (old resolver ignores the new field), so no window serves a half state.
3. **Redeploy (WORLD, `0.7.0_AE_CloudOps~RA1`):** one code leg of `opal-amgt-scoped-api`. Pair COO + CTO; closure diff names
   `name_search.py`, `scoped_amgt.py`, `crosswalk.py`. The order also carries row D1-S7 (the recorder's `_last_deploy_recorded`).
   Proof: `r84_listing --where deployed` R1 YES, R2/R3 PASS.

If the CTO holds to one cell, cells 2 and 3 become that cell's two legs, each still under its own pair.

-- grounding fork of 2.0.0_SA_COO~R1
