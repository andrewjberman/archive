# News Scanner Deep Dive: Trending Topics + Daily Cloud, top to bottom

**Author:** 0.1.0_DS_MarketIntelligence (site Z)
**Vintage:** repo SITEZ @ `ed1a036b2b`; served artifacts and DynamoDB read 2026-09-16 02:0x-03:0xZ;
AWS graph vintage 2026-09-16T02:09:31Z. Every count below prints its denominator.
**Ask (Andrew-direct 2026-09-15 local):** trace the trending-topics and keyword-intelligence /
daily-cloud processes end to end, name the dubious logic, and find the high-leverage inflection
points for better semantics and fidelity.

---

## 0. The one-paragraph verdict

The pipeline's *plumbing* is sound and heavily defended (nine ban/filter layers, deterministic
post-GPT gates, idempotency, chain-invocation). Its *semantics* rest on three primitives that
are each wrong in a way that compounds: (1) a third of the corpus carries a date format the
recency function cannot parse, so those articles get a fixed "half-fresh" score forever;
(2) FinBERT's neutral class is encoded as exactly `0.0` and then *excluded* from every mean, so
the colour of a word is the average of a minority of its articles while its size counts all of
them; (3) a topic's bullish/bearish direction is the *sign of an unweighted mean* over a cluster
whose label describes fewer than half its members in 88 of 100 cases, and the curation prompt then
forbids GPT from questioning that sign. The energy/yields inversion, the "meta ai agent" flip, and
"Brent Crude Reaches $100" filed as bullish-2 are all the third defect wearing different clothes.
Four targeted changes (Section 4) address all three primitives; the first is one line.

---

## 1. The pipeline as built (measured, not as documented)

```
BUILD PLANE  (all times UTC; ET = UTC-4)
=================================================================================================
 43 RSS feeds x 30 items          NewsAPI: 12 publisher ids x 20  +  6 keyword queries x 20
        |  7 runs/day                     |  14 runs/day
        v                                 v
 news-ingestion-scheduler  --dedup url_hash-->  DynamoDB opal-news-articles  (PK article_date)
        stores RAW published_date string (35.6% RFC-822, 63.0% ISO-Z, 1.4% ISO+offset)
        |
        |  +10 min, 14x/day
        v
 finbert-batch-processor -> opal-news-ai-sentiment (image)      text = "title. summary[:500]"
        writes sentiment_finbert = +conf | -conf | 0.0(neutral), _label, _confidence
        |
        |  11:15 + 21:15  (news-trending-analysis, "Layer 2")
        v
 load 7 days -> filter blocked sources/clickbait -> per-article {decay, quality, sentiment}
   -> OpenAI text-embedding-3-small(256d) -> HDBSCAN(min 5, leaf) -> ~100 clusters
   -> label = most-common bigram -> gpt-4o-mini relabel (3 titles)  -> dedup sim>0.65
   -> trending_score = sum(decay) x1.5 [x1.5 if >50% "recent"]
   -> avg_sentiment = mean(non-zero FinBERT)   sample_articles = top 50 by SOURCE quality
        |                                       |
        | writes                                | writes (balanced 10/5/10 + fill, sports,
        v                                       v  dynamic stopwords, gpt-4o-mini junk pass)
 s3 opal-data-news-v2/                    s3 opal-data-portal-v2/json/sentiment/
   trending_reports/latest.json             keyword-sentiments.json  (45 kw, articles[:10])
        |                                       |               |
        | chain-invoke (async)                  | chain (morning-only in code; see F18)
        v                                       v               v
 opal-news-layer3-curation ("Layer 3")   keyword-intelligence-  opal-keyword-drilldown-
   prefilter -> pools by SIGN of          generator (KIG)          generator  12:25+21:25
   avg_sentiment -> composite score       gpt-5.4 + 2 web          14-day EXACT-PHRASE match
   -> gpt-5.6-sol selects 10+10           searches per kw          -> 0 files since 2026-04-07
   -> gates -> gpt-5.6-sol per-topic      -> DynamoDB opal-        (43 of 45 keywords match
   write-up -> dedup -> backfill ->       keyword-intelligence       nothing)   [DEAD]
   rerank caps -> DynamoDB                (PK keyword, SK date;
   opal-news-trending-daily (20 rows)     idempotent per day)
        |
        | chain-invoke
        v
 opal-trending-topics-portal-publisher -> s3 .../json/trending/latest.json
   sentiment_bull_bear HARDCODED +/-0.6; top_articles passed through (all)

CONSUME PLANE (portal)
=================================================================================================
 SentimentGauge.tsx  -> keyword-sentiments.json -> TopicCloud (top 20 of 45; colour by
                        sentiment, size by log count)  -> click -> KeywordSentimentModal
                        -> POST /v1/sentiment/keyword-intelligence -> proxy: DynamoDB today,
                           else prior day (up to 7), else static "evolving card" (no GPT)
 ExecutiveSummary.tsx -> json/trending/latest.json -> bullish/bearish cards; card sentiment
                        recomputed CLIENT-SIDE = mean of non-zero top_articles; articles
                        date-sorted, 10 visible
 DORMANT: news-semantic-clustering, semantic-news-layer3-curation, semantic-...-publisher
          (EventBridge rules deleted; Lambdas + a CloudWatch alarm still live)
 DEAD CODE: trending.ts getLayer3KeywordSentiments (no consumer; keyword = first word of topic)
```

Deployed-vs-repo vintages (lambda-source-map + live code_sha): news-trending-analysis and
keyword-intelligence-generator are AT repo HEAD (`903fbe9a8d`, `09f361593c`). Layer 3 live
code_sha `bWvoG+WeKBa/...` matches my 2026-09-11 deploy record (`d6913f1e9b`); the source map
still says May (`efe2819146`) -- stale map entry (F17). My 2026-09-15 L3 edit `ed1a036b2b` is
LOCAL and NOT deployed.

---

## 2. Findings, graded by leverage

Leverage = how many served surfaces the defect corrupts x how cheap the fix is. Every finding
names its instrument and denominator. MEASURED = read from a served artifact or table;
CODE = read from source at the stated vintage; INFERRED = stated as such.

### TIER 1 -- primitives every downstream number inherits

**F1. Recency is broken for 35.6% of the corpus, and it is the *premium* third.** (MEASURED +
CODE)
`news_trending_analysis.calculate_time_decay` parses with `datetime.fromisoformat`; an RFC-822
string (`'Thu, 10 Sep 2026 15:23:00 GMT'`) raises and the function returns the literal default
`0.5`. Ingestion stores the feed's raw `published` string, so every article from a feed that
emits RFC-822 gets `time_decay = 0.5` regardless of age.
- 2381 of 6691 articles over 7 days (35.6%) are RFC-822; 0 of 2537 NewsAPI, 2381 of 4154 RSS.
- Publishers at **100% RFC-822** (n>=20): Seeking Alpha 1278, Zerohedge 267, MarketWatch 161,
  Financial Times 136, Investors Business Daily 116, Oil Price 105, TechCrunch 91, Housing Wire
  68, Ars Technica 52, Naked Capitalism 30, InvestorPlace 22. CNBC 71%.
- With `DECAY_LAMBDA = 1.386` (12h half-life) a genuine article is 1.0 today, 0.25 at 1d,
  0.06 at 2d, 0.016 at 3d. So a **6-day-old FT article outweighs a 2-day-old Bloomberg
  article 8:1**, and an RFC-822 article can **never** count as "recent" (the bonus needs
  decay > 0.5, and 0.5 is not > 0.5).
- Effect on today's report (100 clusters): 18 clusters are 100% RFC-822 and every one sits at
  `avg_time_decay = 0.500` exactly; >=50% RFC clusters median 0.375; <50% median 0.134; 0% RFC
  median 0.085. Five of the top 15 by trending_score are all-RFC clusters, including #1
  "earnings calls" (35 members, 0 voters).
- Five consumers read this one wrong value: L2 `trending_score`, L2 recency bonus, L3
  `PREFILTER_RECENCY_FLOOR = 0.10` (an all-RFC cluster can never be floor-dropped), L3 composite
  score (recency is the **0.45** weight), L3 `STALE_RECENCY_THRESHOLD = 0.5` (an all-RFC cluster
  is never "stale", so the top-3 stale guard cannot fire on it).
- Same root cause makes `keyword_intelligence_generator` sort articles by the raw string
  (`sort(key=published, reverse=True)`): `'Wed, 09 Sep'` sorts above `'2026-09-15T...'`, which
  is why the two OLDEST Muse articles head the "meta ai agent" list.
- `news_ingestion_scheduler` already imports `dateutil.parser` and parses `pub_dt` for the
  partition key -- it just stores the raw string beside it. **Fix is one line at ingest**
  (store `pub_dt.isoformat()`), plus a one-time backfill or a `dateutil` fallback in
  `calculate_time_decay` for the existing 7-day window.

**F2. FinBERT's neutral class is `0.0`, and `0.0` is excluded from every mean -- so a word's
colour is the average of a minority of its articles while its size counts all of them.**
(MEASURED + CODE)
- `finbert_batch_processor`: `finbert_score = +confidence` (positive), `-confidence`
  (negative), else `0.0`. Verified on 6691 of 6691 scored articles: `|score| == confidence` on
  every one, and all 3787 zeros carry `label = neutral` -- zero is not "no signal", it is the
  neutral class, **56.6%** of the corpus. The trending report header itself says
  `meaningful_coverage_pct: 43.5`.
- `get_article_sentiment` returns `None` on `0.0` ("no meaningful sentiment ... adds noise").
  The same exclusion is repeated in Layer 3 (`_carrying_articles` abstains below 0.25), KIG,
  the drilldown, the publisher and the portal card (`filter(s !== 0)`). Six places, one belief.
- Over today's 100 clusters: voters/members median **0.40**, p25 0.17; **53 of 100** clusters
  have fewer than half their members voting. "meta ai agent": count 15 (size), 6 voters
  (colour), 10 displayed -- three denominators in one served record; the served `sentiment
  0.1134` equals the mean of the 6 exactly.
- Neutral-heavy sources are systematically silenced: Seeking Alpha 74% neutral, The Verge 71%,
  Business Insider 69%, USA Today 64%, TechCrunch 62%, BBC 54%.
- The 7-day window plus 12-hour decay means the *set of voters* changes daily, so a cluster's
  colour can swing on 2-3 articles entering or leaving. That is the "meta ai agent" flip:
  two 09-15 subscription-pricing articles (+0.92, +0.52) joined; nothing about AI agents did.
- Fix: keep neutral in the denominator (mean over all scored, neutral = 0 -- the score then
  shrinks toward 0 in proportion to how uncertain the cluster is, which is the honest
  reading), and carry `voters/members` into the served record and the tooltip as a confidence.

**F3. Direction is the sign of an unweighted mean over a cluster whose label does not describe
it -- and the prompt then forbids the model from disagreeing.** (MEASURED + CODE)
- L2 `avg_sentiment` is the plain mean over the cluster's voters; L3 `prefilter_topics_by_finbert`
  pools strictly on its sign (`> 0` bullish, `< 0` bearish); the curation prompt says *"THE SORT
  IS GIVEN ... Do not re-file, re-rank or argue with the direction."*
- Label fidelity today (100 clusters, label vs its own sample titles): the exact label phrase
  appears in **0 of its own headlines for 80 of 100**; all label tokens appear in fewer than
  half the headlines for **88 of 100**. The L3 gate's own docstring measured 44.1% earlier;
  it is worse now. Labels in today's cloud: "financial options", "politics markets", "stock
  lists", "daily links", "tech startup event", "financial education", "restaurant tribute".
- So a PM reads a *word* and a *colour*, and the colour was computed over articles the word
  does not describe, by a model that scores verbs (F10), with neutrals removed (F2).
- Served instances right now: cloud `oil prices surge +0.523` (bullish), `rising gas prices
  +0.065`; stored cards 2026-09-15 `bullish-2 "Brent Crude Reaches $100 as War Intensifies"
  finbert +0.523`, `bullish-7 "U.S. Diesel Prices Cross $6 a Gallon" +0.065`. Meanwhile
  `bearish-10 "Dow Falls as Oil and Yields Rise"` is correct -- the same fact filed both ways
  in one day's output.
- My 2026-09-15 fix (`ed1a036b2b`, local) forces rising-energy / rising-yield clusters bearish
  at L3. It is a patch on this defect for two subject classes; it does not touch L2 or the
  cloud, and it cannot generalise ("China investment slumps" +, "Xi and Modi rebuild ties" is
  bullish-6 on what?). **F3 is the inflection point that subsumes it** (Section 4.2).

**F4. Cluster labelling is a bigram-frequency count relabelled from three titles.** (CODE +
MEASURED)
`extract_cluster_label` = most common keyword/bigram with a 1.5x phrase bonus;
`_gpt_label_clusters` sends gpt-4o-mini the **first 3 sample titles** (which are
quality-sorted, so 3 Seeking Alpha transcripts for any cluster SA touches). The relabel is
never checked against the cluster. The #1 cluster today is "earnings calls": 35 members, 0
voters, `avg_sentiment None` -- it can never reach the cloud or the cards, yet it holds the top
slot of the 100 and its 35 articles were embedded, clustered, labelled and scored for nothing.
Clusters with 0 voters are not dropped before ranking; 6 of the top 45 today have `None`.

### TIER 2 -- what a user actually sees disagreeing with itself

**F5. The cloud regenerates twice a day; the modal behind it is frozen at the first
computation of the day per keyword.** (MEASURED)
KIG is idempotent on `(keyword, generated_date)` via `get_item`. "meta ai agent": KIG record
`generated_at 2026-09-15T11:21:16Z`, `sentiment_score -0.1917 Bearish`, 10 articles none
newer than 09-12; the cloud served at `21:16:33Z` says `+0.1134` with four 09-15 articles.
Fabric-wide today: 1 of the 20 visible keywords disagrees on label (the one Andrew clicked);
the other 19 agree only because 15 were first computed at 21:16-21:19Z. Structural, not rare:
any keyword that survives from morning to evening is served with the morning's articles and
verdict under the evening's colour. Fix: key the cache on the cloud artifact's `generated_at`
(or a hash of the keyword's article list), so a recolour invalidates the card.

**F6. The article list under a keyword is quality-sorted, then string-sorted, never
date-sorted, and carries three date formats.** (MEASURED) See F1 for the sort; the served
"meta ai agent" record carries `'Thu, 10 Sep 2026 15:23:00 GMT'`, `'2026-09-15T11:00:00-04:00'`,
`'2026-09-15T15:23:23Z'`. The portal modal re-sorts by `new Date()` (which parses all three),
but the GPT write-up was generated from the string-sorted top 15, and `summary` is blanked
(`''`) in the cloud record, so KIG's gpt-5.4 sees titles only.

**F7. The drilldown generator has produced nothing since 2026-04-07.** (MEASURED) It matches
multi-word keywords by exact substring (`keyword in text`); 43 of 45 cloud keywords have no
history file; the newest object under `keyword-history-summary/` is dated 2026-04-07 (360
stale files); the two that exist are from March. It still runs 2x/day and loads 14 days of
DynamoDB to do it. The modal stopped reading it when KIG landed. **Retire it.**

**F8. The bullish/bearish cards' `sentiment_bull_bear` is a hardcoded constant.** (CODE +
MEASURED) `trending-topics-portal-publisher`: `sentiment_bull_bear = 0.6 if is_bullish else
-0.6`; all 20 served cards read exactly +/-0.6. The portal then recomputes a per-card score
client-side from `top_articles` non-zero mean (F2 again) and falls back to the constant.

**F9. GPT is told the wrong ranking formula, then its ranking is overridden anyway.** (CODE)
Prompt: "Article coverage (30%), Sentiment strength (45%), Recency (25%)". Code
(`calculate_composite_score`, rebalanced 2026-05-12): 0.30 / 0.25 / **0.45**. The prompt also
says "OUTPUT ORDER IS THE FINAL RANK (NON-NEGOTIABLE)"; the handler then runs
`detect_and_merge_duplicates`, a second overlap pass, backfill, and `rerank_with_caps`, each of
which reorders. Neither statement is true.

**F10. Sentiment is scored on the verb, per article, with no notion of market consequence.**
(CODE) FinBERT (ProsusAI) is a tone classifier over `"title. summary"`. "Oil surges" is
positive tone; "Meta expands subscription push" +0.92. This is the correct model for
"is this sentence upbeat" and the wrong model for "is this good for a portfolio". Layer 3
already knows this for one class (transcript clusters get a neutral headline because
"management-speak is always constructive"). F3's remedy generalises that carve-out.

### TIER 3 -- dead, vestigial, drifted

**F11.** L3's idempotency guard `check_existing_topics` is `table.scan(FilterExpression=...,
Limit=1)`. DynamoDB applies `Limit` before the filter, so it evaluates one arbitrary item of
~5,256 and returns "no existing topics" ~99.6% of the time. Consequently every invoke
clears and rewrites; both the 11:15 and 21:15 chains rewrite the day's cards (`created_at`
21:20-21:22Z on all four days checked, i.e. the evening rewrite is what persists). The 21:55
EventBridge fallback is DISABLED, so no third write. Harmless today; the guard is a no-op.
**F12.** The stored L3 row is ~60% vestigial: `sentiment.{bullish_bearish, confidence_fear,
positive_negative, risk_appetite, legal_risk, emotional_intensity}` always 0.0 (read from a
`sentiment_all_articles` key that no producer writes); `velocity`, `momentum`,
`avg_escalation_score`, `layer2_trending_rank` are placeholders/TODO; `confidence_level`,
`market_implication`, `affected_sectors`, `affected_tickers`, `citations`,
`initial_analysis`, `enhancement_metadata` are never asked of GPT and always empty; a
`keywords_raw` DynamoDB scan fallback targets a field that does not exist.
**F13.** `TOP_20_KEYWORDS` (`ai, war, tech, ... euro, retail, nasdaq`) and
`KEYWORD_NORMALIZATION` are from the pre-cloud era; `original_keyword` is still normalised to
that list and used as the anti-concentration bucket, so "brent crude" and "diesel prices"
both bucket as `oil` and "natural gas" as `energy`.
**F14.** Yahoo Finance is ingested (1,047 of 6,691 articles, 15.6%) and FinBERT-scored, then
blocked wholesale at L2 (`BLOCKED_SOURCES`) -- the largest single source in the corpus is
paid for and discarded. `quality_map` still scores it 85. Same for the semantic pipeline: three
Lambdas and an alarm live with their rules deleted. `getLayer3KeywordSentiments` in the portal
has no consumer and derives a keyword as `topic.split(' ')[0]`.
**F15.** `detect_and_merge_duplicates` merges on >=50% word overlap measured against the
*shorter* of two <=45-char headlines ("Fed Holds Rates Steady" / "Fed Rate Cut Hopes Fade" =
2 of 4 shared -> merged); `merge_topics` averages `sentiment_score` and unions `articles`,
neither of which exists on a GPT topic, so a merge yields 0 and [].
**F16.** Doc drift: L2 header says "lambda=0.05, ~14 day half-life"; code is 1.386 / 12 h
(`97e2a2e1c8`, 2026-04-08). `dynamic_stopwords.json` = 427 entries, untouched since
2026-04-22, applied every run ("a bull", "as jobs", "avalanche").
**F17.** `lambda-source-map.json` says L3 was last deployed `efe2819146` (May); live sha
matches the 2026-09-11 deploy. A fix to a generated artifact that its generator never carried.
**F18.** Repo (and deployed, `903fbe9a8d`) gates KIG to the morning run (`hour < 17`); yet
15 of 20 visible keywords have KIG records stamped 21:16-21:19Z today, and two at 04:27Z. The
proxy does not write back (cache miss -> static card). Either `KIG_MORNING_CUTOFF_UTC` is
overridden on the live function or something else invokes it. UNRESOLVED; one
`get-function-configuration` read settles it. It matters only for GPT spend (the 06-11 cost
directive), not for correctness.
**F19.** Seven different sentiment cut-points across one chain: L2 balance +/-0.05; L2 report
+/-0.1; L3 pools strict sign; L3 `DIRECTION_MIN_MAGNITUDE` 0.25; KIG conflict +/-0.4; KIG label
+/-0.05/0.15; cloud colour 0.05/0.20/-0.30. No two surfaces agree on what "bullish" means.
**F20.** `select_balanced_keywords` guarantees 10 bullish / 5 neutral / 10 bearish in the
cloud's 50 regardless of what the week looked like -- a flat week and a crash render the
same mix. Reasonable as a UI floor; worth knowing it is a floor, not a reading.

---

## 3. How the two reported symptoms decompose

| Symptom (Andrew) | F1 | F2 | F3 | F5 | F6 | F10 |
|---|---|---|---|---|---|---|
| Energy up / yields up painted bullish | | | x | | | x |
| "meta ai agent" bearish Mon -> bullish Tue with no visible recent news | x (old RSS at top) | x (6 of 15 vote) | x (label != cluster) | x (modal frozen at 11:21Z) | x (quality/string sort) | |

Both are the same three primitives. Neither is a prompt problem.

---

## 4. The inflection points, in the order I would take them

Ranked by (surfaces fixed) / (cost). Each is one bounded change with its own acceptance read.

### 4.1 Normalise the publish date at ingest -- one line, fixes five readers (F1, F6)
`news_ingestion_scheduler` already computes `pub_dt` with `dateutil`; store
`pub_dt.astimezone(utc).isoformat()` in `published_date` instead of the raw string. Add a
`dateutil` fallback inside `calculate_time_decay` so the existing window heals without a
backfill. Zero model cost. **Acceptance:** rerun L2 ad hoc; `topics with avg_time_decay ==
0.500` goes from 18/100 to ~0; "earnings calls" leaves the top slot; FT/MarketWatch/SA stop
carrying a permanent recency subsidy. **Blast radius:** every consumer parses ISO already
(RFC-822 is the one they cannot); KIG's string sort becomes a correct date sort for free.

### 4.2 Assign direction by judgment at the cluster, not by the sign of a mean (F3, F10, F4;
subsumes the energy/yields patch)
At L2, after labelling, one cheap call per cluster (~100/run, gpt-4o-mini or gpt-5.x-mini):
input = the label + top-K titles with their FinBERT scores + the voter/member ratio; output =
`{direction: bullish|bearish|mixed|not_market, market_reason: <=20 words, label_ok: bool,
better_label?: str}`. Rules in that prompt are the ones Andrew stated (supply-push energy,
bond selloff, cost shocks, demand destruction) plus "a rise in a cost is not a rise in
prosperity". Store the verdict and reason on the topic; L3 pools on the verdict, and the
curation prompt's "THE SORT IS GIVEN" becomes true for the right reason. FinBERT stays as a
feature (voter split shown to the judge) rather than the verdict. `mixed` clusters go to
neither pool -- today they are forced into one by whichever side has one more voter.
`label_ok = false` with a better label fixes F4 in the same call. **Cost:** ~100 mini calls
twice a day, cents. **Acceptance:** "Brent $100 as War Intensifies" files bearish with the
reason "supply shock"; "Dow Falls as Oil and Yields Rise" and it stop disagreeing; label
fidelity (all tokens in >=50% of titles) rises from 12/100 toward the majority. This retires
my `ed1a036b2b` regex patch, which should not ship if 4.2 does.

### 4.3 Put neutral back in the denominator and carry confidence (F2, F19, F8)
`avg_sentiment = sum(all scored) / count(all scored)` with neutral = 0 -- the cluster mean
then shrinks toward zero in proportion to how much of it is neutral, which is what a PM
would want to know. Publish `voters`, `members` and a `confidence = voters/members` on every
topic; show it in the cloud tooltip and the card. Define the cut-points once
(`sentiment_thresholds.py`) and import them in L2, L3, KIG, publisher and portal. Stop
hardcoding +/-0.6 in the publisher; pass the cluster score through. **Acceptance:** the
served record's three numbers (size, colour, displayed) share one denominator; "meta ai
agent" reads ~+0.05 (6 votes of 15) instead of +0.11, coloured neutral-lean with 40%
confidence.

### 4.4 Tie the modal to the cloud's vintage; retire the drilldown (F5, F7)
Key KIG rows on `(keyword, cloud_generated_at)` or on a hash of the keyword's article URLs;
the proxy looks up today's vintage first, then the prior. Delete the drilldown generator and
its 2x/day schedule (no consumer, no output since April). **Acceptance:** after an evening
recolour, clicking any recoloured word returns a card whose `generated_at` >= the cloud's.

### 4.5 Hygiene, in one sweep, after the above
Stop ingesting what L2 blocks (Yahoo Finance: 15.6% of ingest + FinBERT spend), or unblock it
with a per-article quality gate instead of a source ban. Drop clusters with 0 voters before
ranking. Fix the prompt's weight text (F9) or delete the RELEVANCE paragraph. Replace the
`scan(Limit=1)` guard with a `query` on the date partition (F11). Prune the vestigial row
fields (F12) and the stale keyword maps (F13). Decommission the three semantic Lambdas and
their alarm (F14). Curate or delete `dynamic_stopwords.json` (F16). Resolve F18 with one
config read.

---

## 5. What was NOT changed by this deep dive

Nothing was deployed. The only code change this session is the earlier local commit
`ed1a036b2b` (Layer 3 energy/yields inversion), which Section 4.2 supersedes; my
recommendation is to land 4.1 and 4.2 instead of deploying it.

---

## Appendix A -- Measurements (instrument, denominator)

| # | Measurement | Value | Denominator | Instrument |
|---|---|---|---|---|
| A1 | Articles scored by FinBERT | 6691 | 6691 (7d) | DynamoDB opal-news-articles |
| A2 | Score exactly 0.0 | 3787 (56.6%) | 6691 | same |
| A3 | Zeros carrying label=neutral | 3787 | 3787 | same |
| A4 | abs(score) == confidence | 6691 | 6691 | same |
| A5 | RFC-822 published_date | 2381 (35.6%) | 6691 | same |
| A6 | Publishers at 100% RFC-822 (n>=20) | 11 | 29 with n>=20 | same |
| A7 | Clusters at avg_time_decay == 0.500 | 18 | 100 | trending_reports/latest.json 21:16Z |
| A8 | Clusters with <50% members voting | 53 | 100 | same |
| A9 | Voters/members median | 0.40 | 100 | same |
| A10 | Label phrase absent from all own titles | 80 | 100 | same |
| A11 | All label tokens in <50% of own titles | 88 | 100 | same |
| A12 | Top-45 clusters with avg_sentiment None | 6 | 45 | same |
| A13 | Cloud keywords served | 45 (20 visible) | -- | keyword-sentiments.json 21:16Z |
| A14 | Visible keywords whose KIG label disagrees with cloud | 1 | 20 | opal-keyword-intelligence |
| A15 | KIG records stamped 21:1xZ despite morning-only gate | 15 | 20 | same |
| A16 | Cloud keywords with any drilldown file | 2 | 45 | s3 keyword-history-summary/ |
| A17 | Newest drilldown file | 2026-04-07 | 360 files | same |
| A18 | L3 rows created_at (4 days) | 21:20-21:22Z each day | 80 rows | opal-news-trending-daily |
| A19 | Cards with sentiment_bull_bear == +/-0.6 | 20 | 20 | json/trending/latest.json 21:23Z |
| A20 | Yahoo Finance ingested then blocked | 1047 | 6691 | DynamoDB + stopwords.py |
| A21 | dynamic_stopwords entries / last update | 427 / 2026-04-22 | -- | s3 config/ |

## Appendix B -- Files read (repo @ ed1a036b2b unless noted)
`infra/aws/lambda/news_ingestion_scheduler/lambda_function.py` (379 l);
`infra/aws/lambda/finbert_batch_processor/lambda_function.py`;
`infra/aws/lambda/news_trending_analysis/{lambda_function,phrase_filters,stopwords,stopwords_config,text_cleaner}.py` (1667+510+838+179+404 l);
`infra/aws/lambda/news_layer3_curation/lambda_function.py` (3410 l);
`infra/aws/lambda/keyword_intelligence_generator/lambda_function.py` (715 l);
`infra/aws/lambda/keyword_drilldown_generator/lambda_function.py` (425 l);
`infra/aws/lambda/v2_portal/01_market_overview/lambdas/trending-topics-portal-publisher/lambda_function.py` (299 l);
`infra/aws/lambda/portal_data_proxy/lambda_function.py` (get_keyword_intelligence);
`infra/aws/lambda/semantic-trending-topics-portal-publisher/lambda_function.py` (dormant);
`infra/aws/terraform/news-pipeline/{lambdas,eventbridge,finbert-batch}.tf`;
`infra/aws/lambda/ci/lambda-source-map.json`;
`portal/src/components/market-performance/{TopicCloud,SentimentGauge,KeywordSentimentModal,ExecutiveSummary}.tsx`;
`portal/src/api/endpoints/{sentiment,trending,market}.ts`, `portal/src/api/portal-proxy.ts`.
