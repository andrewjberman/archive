# HVST-aq-4 -- FWD-12 graded from storage and code (round 44, READ ONLY)

**Reader:** fork of `2.0.0_SA_COO~H`, 2026-10-04. Code read at HEAD a2a5cb3a6a, then re-verified at HEAD 29e44bd234 after
Andrew's resume (CTO~Z msg 29178): config.json:26 `"sa": 25`, worker.py:531, publishers.py:185 and :643 are unchanged.
**Instrument:** `aq-4.sa_integrity.py` (ruff clean, py39). Its output is in `aq-4.sa_integrity.out` and `.json`. The
instrument was re-run to completion after the resume. Its output is identical, line for line, to the run stopped by the pause.
It sent no publisher request, wrote nothing to S3, and invoked no Lambda.

FWD-12 DONE WHEN: (a) every wrong sa row is quarantined and counted against the rows checked; (b) no `/api/v3/articles/{news_id}`
request, and the body comes from the listing; (c) the listing page cap is raised past 25; (d) a re-check over every stored sa row
reads 0 mismatches.

| limb | verdict | evidence |
|---|---|---|
| (a) | **PASS** | `round32/ae1_wrong_object_cut.json`: 38 wrong-object rows of 85 checked, 33 distinct keys. The newest S3 sa quarantine object (`publication_gold.sa_quarantined_keys`) holds 33 keys, equal to the round-32 set. |
| (b) | **PASS** | `lib/opal_data_harvest/publishers.py` `seeking_alpha()` at HEAD: 0 code lines request `/api/v3/articles/`. The only mention is the HVST-ae-1 comment (:643, "the body comes from the LISTING item ... no article request is made"). The yielded row is built from the listing item (`raw_bytes = {"data": item}`, `raw_url=listing_url`). |
| (c) | **FAIL on the run path** | The code default is raised: `DEFAULT_MAX_LISTING_PAGES["sa"] = 200` (publishers.py:185), and `test_ae1_sa_listing_body.py::test_iii` checks only that default. But `lib/opal_data_harvest/config.json` still sets `"max_listing_pages": {"sa": 25, ...}`. `worker.py:531` sets `client.max_listing_pages` from that config on every backfill job, and the site-Z backfill driver spawns that worker with that config.json. **Stored evidence agrees:** 23,364 sa listing hits read, max `search_page` = 25, 0 hits on any page past 25. Of 1,194 query-runs, 25 stopped exactly at page 25 and 0 went beyond. The cap that governed the backfill was 25. |
| (d) | **PASS** | The round-32 classifier (`round32/checks/ae1_common.classify`, independent of the collector) was run over EVERY stored sa silver article row: 11,210 rows (1,242 parts; 11,163 listing-discovered with an article id). It finds 38 wrong-object rows, all 38 in the quarantine. **MISMATCHES outside the quarantine: 0** (0 among rows published since 2026-01-01). Every input was in storage; no publisher request was needed. |

**Overall: FWD-12 NOT YET REALIZED.** (a), (b) and (d) are met. (c) is met in the code default but not on the path that runs: the
config value 25 overrides the default 200.

- **The repair is code and config only (LOCAL):** raise `config.json` `max_listing_pages.sa` past 25, or stop the worker from
  overriding the publisher default with a config value. Add a plant that the worker path's effective sa cap is > 25.
- **Proving the raised cap reaches deeper than page 25** needs a new sa backfill run. That is collection, gated on Andrew's word:
  "We will discuss internally on how to proceed with further data collection after review."

**Observation, outside FWD-12:** 8,843 of the 11,210 stored sa rows were published before 2026-01-01, back to 2013. 2,367 are from
2026.
