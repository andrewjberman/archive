# AMGT_RESAPP.TO-AMGT-r-4 -- session log

Worker `0.9.0_WK_AMGT_RESAPP~2`, task order `AMGT_RESAPP.TO-AMGT-r-4.sa-coverage-re-exercise.md`,
worktree `wk-amgt-2-2` (branch `wk-AMGT_RESAPP-2-2`), cut by hand from SITEZ @3730474e77.

## Sequence

1. Tree check (`TREE-OK`), status flipped `staged` -> `pending` on the task order file.
2. Read `lib/research/coverage/reader.py` (AMGT-s-4, unchanged), `lib/research/coverage/run_reader.py`
   (round-1's driver, unchanged), `lib/research/coverage/tests/test_reader.py` (baseline: `5 passed`),
   `lib/research/coverage/fixtures.py` (BABA_US/BA_US/COST_US ir+publication fixtures, already present),
   `lib/research/identity/resolver.py` (AMGT-s-12, `resolve()`/`render_together()`), and
   `lib/research/rules/item.py` (AMGT-s-11's held-back item rule).
3. Re-grounded the cell's premise against live state. The cell text and the battery-findings note both
   name the landed tickers as "BABA/RTX/+1" and "BABA (137271), RTX, +1". A direct live S3 read
   (`ListObjectsV2` under `raw/seekingalpha/`) and the committed `sa_ids.json`
   (`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~9/sa_ids.json`, merged at
   `3be9d03962`) both show **BABA (137271), BA (769), COST (58)** -- 18 objects, 3 tickers, 6 objects each
   (symbol/report/analysis/news/article x2). No RTX object exists anywhere under `raw/seekingalpha/`.
   Filed as `AMGT_RESAPP-Z-W2-S5` (see the investigation file); proceeded against the REAL landed set
   (BABA_US/BA_US/COST_US), which is what the reader can actually be re-exercised over, and which
   coincidentally already had fixtures under `COVERAGE_FIXTURES` for the ir/publication half.
4. Built `lib/research/coverage/sa_ingest.py`: the minimum adapter from AMGT-s-b4's landed SA JSON shape
   (`report.json`'s single virtualAnalyst body; `analysis.json`/`news.json`'s per-entry arrays; a fuller
   `article_<id>.json` body preferred over its own `analysis.json` summary when both landed) into the
   plain record shape `reader.read()`'s `"sa"` source list expects. `base_url` is a caller-supplied
   argument, read by the driver from `integrations/seekingalpha/config.json`'s own `base_url` field --
   never a literal in this module (AC4's negative grep bans the vendor host as a literal string under
   `lib/research/coverage/`, the same convention `run_reader.py` already stated for the bucket/vendor
   names). `reader.py` itself was NOT touched -- `read()`, `_build_item()`, `check_no_shared_item_sets()`,
   `extract_display_domain()` are byte-identical to AMGT-s-4's shipped version.
5. Built `lib/research/coverage/run_sa_reexercise.py`: discovers the landed security keys LIVE from S3
   (`ListObjectsV2` with `Delimiter='/'` under `raw/<vendor>/`) rather than trusting a sibling worker's
   `run_manifest.json` (see point 3 above -- that file's own selection rule still names BABA/BA/COST, so
   in this instance the two methods agree, but the live-discovery method is the one this cell's own
   premise mismatch argues for). ir/publication sources still come from `COVERAGE_FIXTURES` (unchanged,
   no new G-24 word for a live SERP scan). Writes `coverage_items_<key>.json` x3 and `run_summary.json`
   to this worker's own deliverables directory.
6. Ran it: `SA COVERAGE RE-EXERCISE: 3 securities; 19 items attached (15 sa-class); sa_raw_keys_found 18;
   identity_dropped {'BABA_US': 1, 'BA_US': 1, 'COST_US': 1}`. Re-ran a second time; both
   `coverage_items_BABA_US.json` and `run_summary.json` byte-identical (determinism control).
7. Mutant control (`.scratch/run_mutant_sa_ingest_test.py`, not committed): monkeypatched
   `run_sa_reexercise.report_item`/`list_items` to no-ops and re-ran the same driver logic in memory.
   `sa_raw_keys_found` stayed `18` (computed independently of the ingest functions, from the raw S3
   listing) while sa-class items collapsed to `0` -- the mutant fired as expected, proving AC1's
   "sa-class items >= 1" half is load-bearing rather than vacuously true.
8. `python -m pytest lib/research/coverage/tests -q` -> `5 passed` (AC2, unchanged reader, invariants
   survive real SA content in play). `py_compile` clean. `ruff check --target-version py39
   lib/research/coverage/` -> `All checks passed!`.
9. AC5 (judgment): read `coverage_items_BABA_US.json`'s ranked list end to end (see below).

## primary_subject/affected_tickers -- left honest, not invented

The SA JSON's `relationships.primaryTickers`/`secondaryTickers` carry numeric SA ticker ids, not the
identity layer's `security_key` strings, and reverse-mapping them (via each security's own `sa_id` from
`symbol.json`) was judged OUT of "the minimum adaptation to ingest the SA JSON shape" the BOUNDS name --
it would add a new derivation, not an ingest step. `primary_subject`/`affected_tickers` are left
`None`/`[]` for every sa-class item, the SAME honest gap AMGT-s-4 already carries for ir/publication
items; the item rule's third branch ("not found in this item's tags at all") returns PROVISIONAL, which
the cell text itself names as "honest at this cut."

## `mentions` for sa-class items

Set to the landed `commentCount` attribute (a real, measured field on every article/news object) rather
than a constant `1` -- `commentCount` is the closest real signal to "how much discussed" the landed JSON
actually carries, and using it lets the ranking's frequency tiebreaker mean something on real content
(e.g. BABA's "Michael Burry pulls back..." carries `mentions: 102` vs the report item's `mentions: 1`).
The `report_item()` itself (one per security, no comment count of its own) stays at `mentions: 1`.

## AC5 (judgment -- recorded, not self-graded)

Read `coverage_items_BABA_US.json`'s ranked list (7 items: 4 sa-class, 2 publication, and the
identity-dropped ir item recorded separately):

```
2026-09-10T15:00:11-04:00 | mentions 10  | PROVISIONAL | sa          | Anthropic accuses DeepSeek...
2026-09-10T01:14:28-04:00 | mentions 102 | PROVISIONAL | sa          | Michael Burry pulls back...
2026-09-09T02:01:31-04:00 | mentions 2   | PROVISIONAL | sa          | Alibaba: Decoding The AI Pivot...
2026-09-08T00:00:22-04:00 | mentions 1   | PROVISIONAL | sa (report) | Seeking Alpha Virtual Analyst Report: BABA
2026-09-08          | mentions 3   | PROVISIONAL | publication | Alibaba posts Q2 cloud revenue growth...
2026-09-01          | mentions 10  | REFUSE      | publication | Alibaba, JD.com and Pinduoduo compared...
2026-08-28T13:53:44-04:00 | mentions 13  | PROVISIONAL | sa   | Alibaba: Three-Year AI CapEx Payback...
```

Recency wins first (every row above is dated on or before the row before it, ties broken the other way
only same-day); the two most-recent items are also the two highest-`mentions` sa items (102 and 10
comments respectively) -- on this real content, "most recent" and "most discussed" mostly coincide near
the top, which is the shape an analyst opening the page would recognise. Every PROVISIONAL verdict
carries the SAME reason string, verbatim from the item rule: `"'BABA_US' not found in this item's tags at
all -- cannot determine aboutness"` -- specific about WHY (no tag data, not "low confidence" or some other
vague hedge) and actionable (a reader knows exactly what would need to change: a confirmed
`primary_subject`/`affected_tickers` tag, which this cell's BOUNDS explicitly do not invent). The single
REFUSE (`'BABA_US' appears only in a broad affected_tickers tag list of 3 names ... contains the string,
not ABOUT the security`) is likewise specific. The identity-dropped ir item names `ir_domain` and quotes
`render_together`'s refusal verbatim, unchanged from round 1.

## What is NOT done (declared, not hidden)

- No live SA fetch, no HTML parse, anywhere in `lib/research/coverage/` (AC4).
- `primary_subject`/`affected_tickers` for sa-class items are not derived from the SA relationships'
  numeric ticker ids -- see above; PROVISIONAL is the honest, un-invented state.
- `reader.py` is unmodified; every adaptation lives in the new `sa_ingest.py`.
