# S13-AC3 -- JUDGMENT OUTPUT, RECORDED AND NOT SELF-GRADED

TO `IRPT_BCKEND.TO-IB-s-13` | cell `IB-s-13` | worker `0.9.0_WK_IRPT_BCKEND~4`
Oracle: `3.0.0_SA_CVO` at L9. This file carries the OUTPUT and NO verdict.

---

## 1. HOW MUCH USABLE HISTORY THERE ACTUALLY IS

Measured, not estimated: a full projection scan of `opal-news-trending-daily` and a full
`list-objects-v2` of `s3://opal-data-news-v2/trending_reports/`, both re-run inside the
S13-AC1 battery so the numbers below are the ones the arm printed.

| carrier | first | last | calendar span | days present | days absent | rows/objects |
|---|---|---|---|---|---|---|
| DynamoDB `opal-news-trending-daily` (the dated evidence of record) | 2025-11-21 | 2026-09-10 | 294 | **289** | **5** | 5,156 items; 2 to 26 per day |
| S3 `trending_reports/YYYY/MM/DD/` (the prefilter archive) | 2025-12-01 | 2026-09-10 | 284 | 277 | 7 | 695 dated objects + 1 `latest.json` |

**THE GAPS, NAMED RATHER THAN AVERAGED AWAY** -- 5 missing days in the table, in 3 runs:
`2025-11-23` (1 day), `2025-12-08..09` (2 days), `2025-12-31..2026-01-01` (2 days). Two of
the three straddle a holiday. Recent density is high: **599 items across 30 of the last 30
days**.

**AGAINST WHAT THE BRIEF ASKED FOR.** The brief wanted "almost a full year". 294 calendar
days is **9.7 months**, 80% of a year, and 289 of those days carry topics -- so the request
is **substantially met and is NOT met in full**, and the shortfall is at the OLD end: there
is nothing before 2025-11-21 anywhere. A report whose window opens earlier than that does
not get a thin answer, it gets `MISSING HISTORY` with these bounds printed, which is what
arm (c) exercises.

**A SECOND, SMALLER ASYMMETRY WORTH THE CVO'S ATTENTION:** the table reaches back 10 days
FURTHER than the S3 archive (2025-11-21 vs 2025-12-01). The two carriers are not
interchangeable at the boundary, and a cell that reached for the archive because it is
easier to list would silently lose those 10 days.

---

## 2. IS THE PREFILTER ARCHIVE THE FINAL TOPIC CLOUD? **NO -- AND THE FINAL ONE HAS NO HISTORY AT ALL.**

The order allows the prefilter archive to be used as the final historical Topic Cloud
"only after proof that it is". That proof does not exist, and the read below is what
decided it. Three facts, each with its citation:

1. **The archive carries the PRE-FILTER set.** `save_report_to_s3` writes
   `report['trending_topics']` -- and `trending_topics` is the top `TOP_N_TOPICS = 100`
   detected keywords
   (`news_trending_analysis/lambda_function.py:75`, `:594`, `:1186`).
2. **The final Topic Cloud is a DIFFERENT, SMALLER, FURTHER-FILTERED set.** In the same
   function, `balanced_topics = select_balanced_keywords(report['trending_topics'],
   total_keywords=50)` runs AFTER the archive write, and is then put through a
   sports-keyword filter, before being written as the portal's canonical file
   (`:1405`, the `_TOPICCLOUD_SPORTS_KEYWORDS` block, and `:1522-1527`
   `Bucket=S3_BUCKET_PORTAL, Key='json/sentiment/keyword-sentiments.json'`). The consumer
   confirms the direction of the arrow: `keyword_drilldown_generator/lambda_function.py:9`
   and `:108` read `s3://opal-data-portal-v2/json/sentiment/keyword-sentiments.json` as
   "the TopicCloud source file".
3. **AND THAT FINAL FILE HAS NO DATED ARCHIVE.** `list-objects-v2` over
   `s3://opal-data-portal-v2/json/sentiment/` returns **722 keys, of which exactly 2 are
   top-level files**: `keyword-sentiments.json` and `fear-greed-index.json`. The other 720
   are `keyword-history-articles/` (360) and `keyword-history-summary/` (360), keyed by
   KEYWORD, not by date. There is **one** Topic Cloud object and it is overwritten in
   place.

**SO THE QUESTION THE ORDER ASKS HAS A HARDER ANSWER THAN "NOT PROVEN": a historical
Topic Cloud does not exist in the estate.** The archive is not it, and nothing else is
either -- the only dated, per-day carrier of curated topics is
`opal-news-trending-daily`, which is what this cell reads. The archive is used here as a
CORROBORATOR only, and even then with a caveat the battery prints: its object PATH date is
the writer's naive local clock (`news_trending_analysis:1366`), so the archive's own day
counts bound the ARCHIVE and are never read as publication dates.

---

## 3. WHERE A READER WOULD STILL READ CAUSATION, DESPITE THE WORDING

The validator refuses 18 causal patterns and requires a contemporaneity marker, and the
shipped prose passes both. That is a control on the SENTENCES. None of the four things
below is a sentence, and every one of them is a place a careful reader still draws a
causal arrow. They are stated here because the cell cannot fix them alone -- three are
FNTEND's surface and one is a policy question.

1. **ADJACENCY IS AN ARGUMENT.** "On 2026-07-29 the portfolio sat at its lowest point
   below that high at a cumulative 0.25%. Over the same window the dated topic record
   carried 'Lululemon Cuts Annual Outlook'." Nothing in that asserts a cause and almost
   every reader will infer one. The mechanism is SELECTION, not wording: putting a market
   moment and a headline in the same sentence is the claim, whatever the verb is.
   **The disclaimer does not undo it** -- the final line ("no causal relation ... is
   asserted, tested or implied") is a sentence competing with a layout.

2. **THE EVIDENCE IS SELECTED BY THE EVENT, SO THE SET IS NOT NEUTRAL.** Evidence is
   gathered in a 7-day lookback anchored on the event date. Topics that trended when
   NOTHING happened are never shown. A reader sees "topic and drawdown together" every
   single time, and never sees the negative case -- which is precisely the shape that
   would falsify a causal reading. A control panel of topics from a QUIET window would be
   the cheapest honest counterweight; this cell does not build one and it is not in the
   order.

3. **RANK IS READ AS RELEVANCE.** The topics carry `topic_rank` values like `bearish-1`
   and the store returns them in rank order, so the first-listed topic beside a drawdown
   reads as the most-related one. It is the most TRENDING one. Nothing in the packet
   distinguishes those two, and the field name invites the wrong reading.

4. **THE PROSE VALIDATOR'S DOMAIN IS DECLARED, NOT EXHAUSTIVE.** `CAUSAL_PATTERNS` is 18
   regexes and `prose.py` says in its own comment that this is a declared domain and a
   floor under the wording, never a proof of innocence. A model-written paragraph would
   find the uncovered member -- "amid", "as X slid", "against a backdrop of", a
   semicolon -- and the validator would pass it. The validator binds today because the
   generator is a deterministic template with no causal slot; on the day a model writes
   the prose, the validator alone is NOT sufficient and that is a decision to take
   deliberately rather than discover.

**WHAT THIS OUTPUT DOES NOT CLAIM.** It does not claim a reader will not infer causation.
It claims no sentence asserts one, every citation resolves to a dated item that predates
its cutoff, and the four places the inference survives are named rather than left for the
first advisor who asks "so what caused it?".
