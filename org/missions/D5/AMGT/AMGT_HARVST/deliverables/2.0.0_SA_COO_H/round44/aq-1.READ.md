# HVST-aq-1 -- FWD-2 field census (round 44, READ ONLY) -- `2.0.0_SA_COO~H`

**FWD-2 DONE WHEN:** "every field present in the received article (including language, paywall flags, the publisher's own ticker
tags, sentiment, themes and summary where sent) appears typed in the queryable table, rebuilt from the stored original, and a
query by company and date returns it".

**Overall: FWD-2 is NOT MET. 1 of 5 publishers PASS (sa); barrons, bbg, ft and wsj FAIL.** A FAIL is a repair cell (the silver
builders type the lost fields, rebuilt from the stored originals); nothing was repaired here.

## Instrument

`aq-1.field_census.py` (ruff clean, py39), run to completion at 2026-10-04 18:14Z (`aq-1.field_census.out`, `.json`). It
performed S3 list and get only, with no write, no vendor call and no publisher request. The run began before the pause and
finished; this READ was written on resume and nothing was re-run.

- **Sample:** <= 50 stored originals per publisher, deterministic and stratified by extension, with the denominator printed.
- **Population:** sa 11,205 originals, bbg 1,277, wsj 444, ft 184, barrons 164.
- **Leaves:** each original is parsed into leaves. A JSON document is parsed whole. An HTML page yields its `__NEXT_DATA__`, its
  JSON-LD, its `<meta>` tags and `<html lang>`.
- **Classes:** a leaf is class A (inside the subtree the silver builder treats as the article) or class B (the rest of the page).
- **Compared row:** each leaf is checked against the silver row whose `bronze_key` is that original, i.e. the row rebuilt from it.
- **States:** a leaf is
  - TYPED: same field name and value in a typed column;
  - TEXT: found only inside `page_config_json`;
  - ELSEWHERE: the same value is in a typed column under another name, so the value is kept;
  - MISSING: none of the above, so the value is lost.
- **Notation:** `[A|B mN eN tN/C]` reads class, missing, elsewhere, text-only, and objects carrying the path.
- **Grading rule:** "LOST" below means MISSING in at least one sampled object.
- **Site chrome not counted:** navigation menus, ad config and translation strings are not article fields. Examples are bbg's
  `menuItems...subscriber-events` and `menuItems...market_data_tickers`.

## Per publisher

| publisher | compared | article paths (lost) | named kinds LOST (count of paths, e.g.) | query by company + date | verdict |
|---|---|---|---|---|---|
| **sa** | 50 of 50 | 24 (0) | none. All named kinds sent are typed: paywall 2, ticker tags 5, sentiment 1, themes 1. | AMD_US_Equity 2022-01-31: returned (see the note below) | **PASS** |
| **barrons** | 50 of 50 | 1,331 (935) | ticker tags 40 (`articleMeta.properties[].symbol`, `.properties.ticker`, `.internalSymbol`); paywall 7 (`isFreeArticle`, `isBICPaywall`, `isServerUnlockedArticle`); themes 10 (`djmlKeyword`, `articleMeta...topicId`); summary 6 (`articleToolsProps.summary`) | BAC_US_Equity 2026-09-24: returned | **FAIL** |
| **bbg** | 50 of 50 | 2,158 (0) | language 2 (`html_lang`, `__NEXT_DATA__.query.lang`, 49/49); themes 14 (`html_meta.keywords` 49/49, `parsely-section`, `lotame-bbg-category`, `lotame-bbg-topic`) | BP/_LN_Equity 2026-07-07: returned | **FAIL** (page-level descriptors only; the article subtree is fully kept) |
| **ft** | 50 of 50 | 62 (8) | language 1 (`html_lang`, 46/46). Article subtree: the JSON-LD `publisher` block (`publisher.legalName`, `.url`, `.logo.*`, `.sameAs[]`) lost in 14 of 46 | AAPL_US_Equity 2026-06-25: returned | **FAIL** |
| **wsj** | 47 of 50 | 486 (0) | language 3 (`html_lang`, `__NEXT_DATA__.locale`, `ld[other].inLanguage`, 45/45); paywall 2 (`ld[other].isAccessibleForFree`, `.hasPart.isAccessibleForFree`); themes 12 (`html_meta.keywords`, `news_keywords`, `page.section`, `page_editorial_keywords`); summary 2 (`ld[other].description`) | MA_US_Equity 2026-05-04: returned | **FAIL** |

**Also FAILS the "rebuilt from the stored original" limb:** 3 of 50 sampled wsj originals have NO silver row at all. All 3 were
fetched 2026-10-02 (`wsj/harvest/bronze/article/article_hash=b27bbdc2.../20261002T064907Z.html`, `cc8d1d4d.../20261002T062437Z.html`,
`f721b35d.../20261002T064733Z.html`).

**Kept, not lost (not counted against a publisher):** wsj paywall 41, themes 159 and summary 6 paths; bbg summary 5 (`og:description`,
`twitter:description`, `meta description`); ft summary 1 (`og:description`). In each case the value is in a typed column under another
name (ELSEWHERE) or in `page_config_json` (TEXT).

## The repair the FAILs call for (not done here)

The repair is one producer cell over `lib/opal_data_harvest/silver_from_bronze.py` and the publisher field maps:
- type the lost article fields, barrons first: ticker tags, paywall flags, topics and summary;
- type the page-level article descriptors: `<html lang>` / `inLanguage` / `locale`, meta `keywords` / `news_keywords` / section,
  JSON-LD `isAccessibleForFree` and `description`;
- rebuild silver from the stored originals;
- find why 3 wsj originals produced no silver row.

A silver rebuild is a served write, so it goes under a never-widen pair.

## Limits and notes

- **Sample, not population.** These are 50-object samples per publisher. A path absent from the sample is not proven absent from
  the population, and sa's PASS covers 50 of 11,205 originals.
- **Observation for aq-4 (FWD-12), out of this cell's scope:** the sa query example returned, under `AMD_US_Equity`, the article
  `sa:3793704` titled "Why did Regeneron Pharmaceuticals stock drop today? ..." with a 2022-01-31 UTC date. A pre-2026 article about
  another company, attached to AMD, is the wrong-article class FWD-12 names.

Evidence: `round44/aq-1.field_census.py`, `aq-1.field_census.out`, `aq-1.field_census.json`, this file.
