# NEVER-WIDEN ASK -- NFRA_OPLGTW.TO-OG-nw-1 (round 37, FWD22-W6, FWD-22 G6, Phase A)

For the three halves: `1.0.0_SA_CTO~Z`, `2.0.0_SA_COO~O`, `3.0.0_SA_CVO~Z`.
Author: `0.9.0_WK_NFRA_OPLGTW~82`. Phase A: build, grant file, ask. NOTHING is applied and NOTHING is deployed by this ask.
Surprise rows that bear on this ask: `NFRA_OPLGTW-Z-W82-S1` (preflight versus body on IAM), `-S2` (sparse source GSI),
`-S3` (security_key shape), `-S4` (no DynamoDB admission scope), `-S5` (fallback trigger), `-S6` (window counting).

## 1. diff

Files this cell adds or changes, by path (the commit hash is in the worker report):

- `infra/aws/ec2/opal-gateway/app/news_typed.py` (new): the five G6 tools. No table-name literal. No `Scan` call.
  No principal getter import. No boto3 client at module scope (`_ddb()` and `_portal_client()` create theirs lazily).
- `infra/aws/ec2/opal-gateway/tests/test_og_nw1.py` (new): five offline tests `test_ognw1_ac01` .. `ac05`, a recording
  DynamoDB fake that serves Query alone, and recording S3 fakes. The table names in the test are synthetic.
- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` (changed): the `.env` printf gains three keys on the existing
  `AMGT_SCOPED_API_FUNCTION` line: `NEWS_ARTICLES_TABLE`, `NEWS_TRENDING_TABLE`, `NEWS_KEYWORD_TABLE`.
- `infra/aws/terraform/opal-gateway/news_read_iam.tf` (new): ONE `aws_iam_role_policy`, the grant in section 4.
- This file and `TARGETED_PLAN_OG-nw-1.txt` in the same folder (the targeted plan record).

Not touched by this cell, by design: `app/tools.py`, `app/data_entitlement.py`, `app/destructive_ops.py` and the pinned-count
tests. The issuer registers the five tools and re-pins the counts at the merge.

## 2. tools

Five read-only tools. Admission runs first on every tool, before any DynamoDB or S3 call.

- `news_search_articles(date_from, date_to, text, source, sentiment_label, limit)`: a window of 15 or more calendar days
  is refused `harvest_bad_argument` with zero reads (the window is counted inclusively: 2026-10-01..2026-10-14 is accepted,
  2026-10-01..2026-10-15 is refused). One Query per day on the articles table for the day's items, and one COUNT Query per
  day for `per_day_counts`. A per-day read cap of 2,000 items; `cap_bit_days` names any day the cap cut. `limit` default 25,
  max 100 (`limit_applied`). `source` and the FinBERT label filter in Python (the source index is sparse; see surprise row S2).
- `news_trending_topics(date, side, days, match)`: `side` in bullish, bearish, all (else refused). `days` 1 to 30
  (`days_applied`). With no `date`, the newest populated day is found by a COUNT walk back from today (10 days at most).
- `news_keyword_intelligence(keyword, date)`: with keyword, that keyword's newest brief (or the brief on `date` when both are
  given); with date only, the briefs of that date through the `date-index` GSI. Neither given is refused `harvest_bad_argument`.
- `news_market_mood()`: reads exactly the two singleton keys. The fear/greed current block is slimmed (its component series
  reduced to counts, since the series alone exceed the 50 KB answer); the keyword set is projected to fit and flagged
  `truncated` when it does not fit.
- `news_for_security(security_key, ticker, window_days)`: the mention index, newest partition, newest part only, through the
  HARVEST scope's admission. A ticker matches as the prefix of the exchange-qualified key. The text fallback runs when a
  ticker is given and every fallback row carries `match: "text"`.

Refusals and their codes: `typed_opal_only` or `harvest_opal_only` (non-Opal), `principal_required` (no principal),
`harvest_bad_argument` (bad or missing argument, or a window over 14 days), `news_unavailable` (a table name unset in the
environment; no read made), `harvest_over_cap` (a singleton over the read cap).

Freshness: every answer states its store's newest date and its lag in TRADING days behind T-1, measured with
`lib/trading_calendar.py` (`trading_days_behind_t1`).

## 3. widening

- The gateway instance role `aws_iam_role.gw` gains `dynamodb:Query` and `dynamodb:GetItem` only, on the three tables and the
  two indexes (read only; no Scan, no write, no wildcard).
- The S3 singleton reads need NO grant change: the internal reader role already carries `s3:GetObject` on `json/*` of the
  portal bucket (`infra/aws/terraform/opal-gateway/mcpmsp_internal_reader.tf`, served bucket from `modules/opal_name`).
- Three `.env` keys are written by the deploy printf: `NEWS_ARTICLES_TABLE`, `NEWS_TRENDING_TABLE`, `NEWS_KEYWORD_TABLE`
  (values are the live table names; the deploy writes them, the code reads them from the environment at call time).
- The grant names `source_date_index` because the order lists it. No tool reads it (surprise row S2). Narrowing the grant
  to `date-index` is a safe option the CTO may choose; this ask does not narrow it on its own.

## 4. grant

- Policy: ONE `aws_iam_role_policy` `gw_news_read`, name `gateway-global-news-read-policy`, the builder's output for
  `lib/opal_naming.py name("gateway", "global", "news-read", "policy")`, on role `aws_iam_role.gw`.
- Actions: `dynamodb:Query`, `dynamodb:GetItem` (no others).
- Resources (five): `arn:aws:dynamodb:us-east-1:313476888478:table/opal-news-articles` and its index
  `.../index/source_date_index`; `.../table/opal-news-trending-daily`; `.../table/opal-keyword-intelligence` and its index
  `.../index/date-index`. No `*` resource.
- Plan: `terraform plan -target=aws_iam_role_policy.gw_news_read -lock=false` (no `-out`, no apply). Result:
  1 to add, 0 to change, 0 to destroy. The only resource in the targeted plan is the one policy. The full plan record is
  `TARGETED_PLAN_OG-nw-1.txt` in this folder. The `market_update_s3_root` input was fed from the builder's `address()` output
  (`s3://opal-data-transcripts/sharepoint/transcripts/bronze/market_update/`), not typed.

## 5. both branches

- REFUSED (zero reads): a non-Opal principal or no principal is refused by every tool before any read (`typed_opal_only`,
  `harvest_opal_only`, `principal_required`); a window of 15 or more days is refused `harvest_bad_argument`; neither
  keyword nor date given is refused `harvest_bad_argument`; a table name unset in the environment returns `news_unavailable`
  before any DynamoDB call.
- ADMITTED (bounded): each article day is one paginated Query capped at 2,000 items read; trending reads at most 30 calendar
  days of rows; the keyword and date reads are key-conditioned; the mention read is the newest part only; every answer
  is projected to 50 KB with `truncated` set when projection cut it. Each served call writes one SERVE audit row
  (tool, reference, bytes; never item content).

## 6. rollback

- Release level: redeploy the prior release artifact with `deploy-to-ec2.sh`. The prior `.env` has no `NEWS_*` keys; the tools
  are not registered in `app/tools.py` until the issuer's merge, so they are unreachable before that registration.
- Grant level: destroy the one policy, `terraform destroy -target=aws_iam_role_policy.gw_news_read` through `safe-apply`,
  on the issuer's word. This ask performs neither step.
- No data is written by this cell, so no data rollback exists to run.

## 7. triggers

- Tools +5 on the live census: the five tools are registered at the merge; the registered count moves by five, and the
  pinned-count tests are re-pinned by the issuer in the same commit.
- The three `.env` names present: `ENV_KEYS_AFTER` in the deploy output names them after the release; the probe's live AC2
  sets the same three names itself.
- A served read of each tool under an Opal stand-in principal: the live probe `nw1.AC2.sh` runs each tool against the live
  tables and singletons with the box's credentials (INTERNAL_READER_ROLE_ARN unset) and re-derives the day count from an
  independent COUNT. Its result is recorded in the proof instance.
