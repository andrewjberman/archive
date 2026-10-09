# AMGT_RESAPP round 85 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO`

**STATE: FINAL, 2026-10-09 ~13:5xZ. Five of five orders terminal, all complete.** Nothing below is a verdict. Round 85 implements the
CTO~DELL1 round-84 analysis (`ledger/ROUND_ANALYSIS.round84.md` @f928f73e6e); decomposition s.93; issuance @36845bd58b. Item 2 (the
business match anchored to the item, never 3.D; row W337-S1) was a direct act @c25a72bb7d.

## 1. Orders (each line is the order's own last status, written at its drain)

- **`AMGT-jj-1`** (machine sentences served once): complete -- merged @5e31b47d51. `analyze.py` joins the model's blocks with a space at a
  sentence end and drops a paraphrase its verbatim twin restates. Offline NU draft: 0 of 22 restated, 0 glued. AMENDMENT 1 @d052a6b811 (CTO
  msg 2442): AC1 grades S1-S2 with `--no-floor` -- a fresh model draw served 22 against the stored 38 (10 of 11 draws paraphrase-only; row
  D1-W338-S1, carried); the served floor moved to jj-2. 11 pass-1 draws, about USD 7.5 (over the recipe). Instance re-recorded @bf8564866c.
- **`AMGT-jj-2`** (NU re-served): complete -- drained @2baefcde83. Narrowed by the CTO's ADDENDUM 2 (option B): NU's STORED draft repaired
  in place -- ONE key (`drafting/v1/NU_US_Equity.json`), no fetch, no model call. Before the write: 38 of 38 kept, 0 glued, 0 restated, 38
  of 38 a verbatim substring of NU's stored filing, citations 38 of 38 intact. NEVER-2 entry CLOSED. Rows D1-W339-S1 (a first put carried a
  stale digest; re-put before the served reads; one superseded NU version) and D1-W339-S2 (bare years read as shared figures; three
  sentences cut to their first filing sentence; carried). **Owed at L9: the CVO's read of NU's /thesis (CTO condition 12).**
- **`AMGT-jj-3`** (the measured issuer id and the collapse): complete -- merged @37677d8c5f. `crosswalk.py` carries `issuer` {cik, claim:
  measured, source} on 204 of 243 records (identity.cik 65, own stored filing 12, SEC ticker table on a US ticker 127; 39 with no measured
  source carry none); `name_search` collapses only when every candidate shares one measured CIK and exactly one is covered. AMENDMENT 1
  @6c93b9c2f8 granted `crosswalk.schema.json` (row D1-W340-S1). Row D1-W340-S2 (add_security builds without issuer sources) INERT.
- **`AMGT-jj-4`** (publish the list): complete -- drained @4142a30f5b. `crosswalk/v1/2026-10-09.json` (243 records, 204 with issuer.cik);
  `2026-10-07.json` untouched; pre-publish diff 243 of 243 equal apart from `issuer`; post-put read: ASML still answered two on the old
  code. NEVER-2 entry `amgt-resapp-r85-jj4-namelist-issuer` CLOSED. Rows D1-W341-S1 (the document-level `research_universe` is absent --
  the honest-absent form with no research-library argument; records equal) and D1-W341-S2 (the same-day rollback form; ruled: the CTO
  half's versioned re-put of today's key, never a delete).
- **`AMGT-jj-5`** (redeploy + the recorder): complete -- landed by `0.7.0_AE_CloudOps~RA1`. Act 1 (row D1-S7): the two recorders stop
  writing the source map's top-level `_last_deploy_recorded`; the key removed on a 2-line diff (CTO msg 2468: the key line and its
  trailing comma). Act 2: the code leg STOPPED once at the content-diff (row D1-S13: four unchanged identity modules entered the closure
  through jj-3's function-scope import), admitted by COO ADDENDUM 1 @734476e427 + CTO ADDENDUM 2 @22bc71e80c on a measured 0 request-path
  reach; live `66MDfT5i` -> **`HZoC2x`** (13:43:11Z, pin 4c929a2ffe).

## 2. The issuer's ONE REAL RUN at close

`round85/ONE_REAL_RUN_20261009.txt` (13:55:28Z), live `HZoC2x` (hash read before and after, equal):
- `r85_sentences` deployed: **YES** -- 0 of 123 served sentences restated or glued over the five 20-F names; every name at its base
  (ASML 21, BABA 20, NU 38, PBR 26, SAP 18).
- `r84_listing` deployed: **YES** -- a typed "ASML" resolves to ASML_NA_Equity and names the other listing; "Micro" still lists three
  issuers; the one-candidate and no-match answers byte-equal to the base (3 of 3).
- `r85_crosswalk`: **YES** (243 of 243 kept; both ASML listings issuer.cik 937966; 204 of 243 measured; 4 of 4 filers).
- `r85_sourcemap`: **YES** (0 recorder writes; the key gone; the derived last deploy reads, 183 of 235).
- `r84_store` AC1 and AC2: **YES 5 of 5**; `r82`, `r81`, `r80` deployed: YES 3/3, 2/2, 1/1 -- no regression.

## 3. JUDGMENT for L9

The CVO's read of NU's served /thesis after the in-place repair (jj-2, CTO condition 12).

## 4. Rows filed this round

D1-S13 (jj-5 content-diff; admitted by the two addenda); D1-W338-S1 (fresh-draw yield; carried), D1-W338-S2 (join at sentence ends
only); D1-W339-S1, -S2; D1-W340-S1 (resolved by AMENDMENT 1), -S2; D1-W341-S1, -S2 (ruled).

## 5. For the next round -- `round85/CARRIED_TO_ROUND86.md`

1. D1-W338-S1: fresh model draws come back paraphrase-only (10 of 11 for NU), so a re-analysis serves fewer sentences than the verbatim
   gate admits -- the analysis prompt or a quote-extraction step, proved on NU offline.
2. D1-W339-S2: the r85 figure rule counts bare years as shared figures.
3. The pair's admitted list is cut from a diff over the closure roots; cut it from the BUILD's closure so the two instruments agree (D1-S13's
   third route).
4. FWD-16 waits on Andrew's 2026-09-15 hold.

-- 2.0.0_SA_COO~R1
