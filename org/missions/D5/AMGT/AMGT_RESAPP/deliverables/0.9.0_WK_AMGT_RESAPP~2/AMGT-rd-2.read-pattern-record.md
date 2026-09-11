# AMGT-rd-2 -- THE METRICS STORE: read-pattern record

`0.9.0_WK_AMGT_RESAPP~2`, round 5/v5, cell AMGT-rd-2 (row S16, FWD-15). Table:
`infra/aws/terraform/amgt-resapp/security-metrics-table.tf`.

## Key schema, as declared and as-deployed (matches -- verified via live `describe-table`
below, not asserted from the `.tf` file alone)

Base table `opal-amgt-security-metrics`:
- `axis_date` (S) -- HASH. Format `"<AXIS>#<as_of_date>"`, e.g. `"CHATTER#2026-09-11"`.
  `AXIS` is one of the four ranking axes (writer-defined name; AMGT-rd-5 writes the
  chatter axis, AMGT-rd-6 the price axis); `as_of_date` is the ISO date the row was
  computed for.
- `ticker` (S) -- RANGE.
- billing_mode = `PAY_PER_REQUEST`.

GSI `axis-rank-index`:
- `axis_date` (S) -- HASH (same partition value as the base table).
- `rank_sort` (S) -- RANGE. Zero-padded rank string (e.g. `"00001"`), written by the
  producer cell at compute time. Projection `ALL`.

## The exact read the Lead Panel (AMGT-rd-8) will issue

The Lead Panel's page load is "give me the ranked set for this axis [on this date]" --
never a scan, never a client-side sort (`C-SERVER-SIDE-RANKING`, PRD s.3b). That read is
a single DynamoDB `Query`:

```
Query(
  TableName = "opal-amgt-security-metrics",
  IndexName = "axis-rank-index",
  KeyConditionExpression = "axis_date = :ad",
  ExpressionAttributeValues = { ":ad": "<AXIS>#<as_of_date>" },
  ScanIndexForward = true,     -- ascending rank_sort = ascending rank
)
```

This returns the day's ranked rows for that axis PRE-SORTED, in one round trip -- the
producer (AMGT-rd-5 / AMGT-rd-6) does the ranking once, server-side, at write time; the
Lead Panel never re-derives it. Optionally bounded with `Limit` for a TOP_N view (e.g.
chatter's TOP_N=10 per PRD s.3b) since the GSI is already rank-ordered -- `Limit` then
trims a pre-sorted page instead of sorting a larger read client-side.

A second, narrower read -- a single ticker's row for one axis + date (e.g. a detail panel
or a watchlist join) -- is a point read against the base table, not the GSI:

```
GetItem(
  TableName = "opal-amgt-security-metrics",
  Key = { "axis_date": "<AXIS>#<as_of_date>", "ticker": "<TICKER>" },
)
```

Both reads are structurally the ONLY reasonable way to get data out of this table for
those two questions -- there is no unindexed scan that is cheaper or more natural, which
is what makes the pre-computed read the one a consumer reaches for (bound (a): the schema
"should not make [it] impossible" to read any other way, and does not; it simply makes
the scan-and-sort path strictly worse than the indexed one for both stated access
patterns).

## The `opal-news-trending-daily` shape mirrored, measured from the LIVE table (not asserted)

`opal-news-trending-daily` has NO declarative Terraform source in this repo
(`comp-find --corpus aws` at the round-5 cut: drift=LIVE-no-DECLARED). Read directly,
2026-09-11, via `.tools/aws dynamodb describe-table --table-name opal-news-trending-daily`:

```
KeySchema:
  date        (S) -- HASH
  topic_rank  (S) -- RANGE
TableStatus:  ACTIVE
BillingMode:  PAY_PER_REQUEST
ItemCount:    5175
```

`opal-news-trending-daily`'s shape is "partition on the grouping key (`date`), sort-range
on the rank (`topic_rank`)" -- a `Query(date = X)` returns that day's topics already
ranked, no scan. `opal-amgt-security-metrics`'s GSI applies the exact same shape
(`axis_date` as the grouping partition, `rank_sort` as the sort-range), generalized to
group by axis-AND-date in one partition key (since this table serves four axes, not one
implicit "trending" axis) and adds the base-table point-read path on `ticker` that
`opal-news-trending-daily` does not need (a topic, unlike a ticker, is not looked up
individually by the Lead Panel).

`opal-news-articles`' shape was also read directly (also drift=LIVE-no-DECLARED), for
contrast with AMGT-rd-1's `opal-amgt-articles` (the content-table analogue to this
rankings table):

```
KeySchema:
  article_date (S) -- HASH
  url_hash     (N) -- RANGE
GSI source_date_index:
  source        (S) -- HASH
  published_at  (S) -- RANGE
TableStatus:  ACTIVE
BillingMode:  PAY_PER_REQUEST
ItemCount:    344211
```

## Live verification (this cell's own table, post-apply)

```
$ .tools/aws dynamodb describe-table --table-name opal-amgt-security-metrics \
    --query "Table.[TableName,TableStatus,BillingModeSummary.BillingMode]" --output text
opal-amgt-security-metrics    ACTIVE    PAY_PER_REQUEST
```

Pre-build re-measure (2026-09-11, before this cell's apply):
`.tools/aws dynamodb describe-table --table-name opal-amgt-security-metrics` ->
`ResourceNotFoundException: Requested resource not found` -- confirms the cell's stated
GENUINE CREATE (surprise row `AMGT_RESAPP-Z-S5`: 0 hits across 2445 aws nodes at the cut)
was still true at build time; not merely trusted from the battery finding.

## Not built here (bound (b)/(d))

No writers (AMGT-rd-5 chatter, AMGT-rd-6 price) and no watchlist (AMGT-rd-7). The schema
above does not make either impossible: a writer only needs to know `axis_date` / `ticker`
/ `rank_sort` plus whatever score/box-side attributes it wants to add (DynamoDB does not
require non-key attributes to be pre-declared); a PER-FIRM starred watchlist can live in
this table under a firm-scoped `axis_date` value (e.g. `"WATCHLIST#<firm>"`) or in a
sibling table/keyspace -- this cell does not foreclose either.
