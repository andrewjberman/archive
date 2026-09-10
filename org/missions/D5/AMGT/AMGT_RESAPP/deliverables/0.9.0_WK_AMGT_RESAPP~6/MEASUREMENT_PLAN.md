# MEASUREMENT_PLAN.md -- AMGT_RESAPP.TO-AMGT-s-13, the social feed's first act

**This is a PLAN, not a RUN.** No dataset has been triggered by this order and none is
triggered by reading this file. `lib/research/social/measure.py` composes exactly this
plan as data and REFUSES to send anything (`REQUIRES Andrew's per-use word (G-24); not
run by AMGT-s-13`, exit 3) unless invoked with an explicit `--word-record <path@hash>`
naming the record that carries Andrew's per-use word for this vendor call
(G-24 / C-VENDOR-EGRESS). This order supplies no such record.

## 1. The dataset ids (CITED from F12) and the one chosen for the first run

F12 (CITED, task order body): the datasets-list surface returned HTTP 200 and 1,763
datasets on the live account, including these five post-level/company-level ids:

| dataset id | name |
|---|---|
| `gd_lwxkxvnf1cynvib9co` | X (formerly Twitter) - Posts |
| `gd_lvz8ah06191smkebj4` | Reddit - Posts |
| `gd_lvzdpsdlw09j6t702` | Reddit - Comments |
| `gd_l1vikfnt1wgvvqz95w` | LinkedIn company information |
| `gd_lmrpz3vxmz972ghd7` | Yahoo Finance business information |

**Chosen for the first run: `gd_lwxkxvnf1cynvib9co` (X / Twitter - Posts).** It is the
only one of the five that is both post-level (a discussion body a cashtag query runs
against) and on a platform F13 already measured this account holds datasets for (X: 5
datasets vs. Reddit's 4). LinkedIn company information and Yahoo Finance business
information are company-profile datasets, not post-level discussion -- neither can
answer the cashtag-queryability observable at all, so they are not candidates for the
first run.

## 2. The one company and the query shapes, in order, with the stop rule

**Company: Home Depot HD**, read from AMGT-s-12's `universe.json`
(`deliverables/0.9.0_WK_AMGT_RESAPP~3/universe.json`, folder `"Home Depot HD"`):
`bloomberg_ticker` MEASURED `"HD US"`, `sa_symbol` INFERRED `"HD"` via the stated
US-suffix rule. Chosen because it is a clean, unambiguous row -- many `universe.json`
rows at this cut carry AMGT-s-12's own data-quality defect of a repeated `"AAPL US"`
`bloomberg_ticker`; Home Depot is not one of them.

Query shapes, attempted in this order:

1. **cashtag** -- `$HD`. The cashtag-native shape, the one the feed needs.
2. **company_name** -- `Home Depot`. Fallback if the cashtag query returns 0 records.
3. **handle** -- `from:<OFFICIAL_HANDLE>`. Fallback if neither (1) nor (2) returns a
   record the item rule admits as ABOUT the security. This shape requires
   `social_account` to be MEASURED or INFERRED; for Home Depot that key is
   `UNRESOLVED` in `universe.json` at this cut (AMGT-s-12: no vendor word for a social
   lookup), so shape 3 is not reachable until AMGT-s-15's social map resolves it.

**Stop rule:** stop at the first query shape (in the order above) that returns at
least one record the item rule (`lib.research.rules.item.qualify`) does not REFUSE
outright, or after all reachable shapes are exhausted -- whichever comes first. No
shape already attempted in this run is re-triggered a second time.

## 3. The observables, and how each is read

| observable | how it is read |
|---|---|
| **cost** | the account's usage/billing delta -- read before the trigger and again after; the difference is this record's cost |
| **field schema** | the first returned record's own keys, read directly (`json.loads(response_body)[0].keys()`) -- no schema is assumed ahead of the measurement |
| **latency** | wall-clock delta between the request being sent and the response being fully received (`time.monotonic()` immediately before/after the call) |
| **freshness** | the newest returned record's own timestamp field, compared to `datetime.utcnow()` at read time -- the gap IS the freshness |
| **cashtag-queryability** | whether the order-1 (`$HD`) query returns >=1 record the item rule admits as ABOUT the security -- not merely whether the API call itself returns HTTP 200 |

These five are implemented as data in `lib/research/social/measure.py`'s
`OBSERVABLES` dict, in this same wording, so the plan and the script cannot drift
apart.

## 4. The cost cap and the refusal signal

**Cost cap: $5.00 USD per run**, stated here and enforced by
`lib.research.social.measure.cost_cap_exceeded()`. This run's own per-record cost is
itself one of the observables above (unmeasured until triggered) -- the cap is a guard
against an unknown price, not a budget drawn from a known one. $5.00 is small enough
that a single-company, single-query-shape exploratory pull cannot exceed it under any
plausible per-record price Bright Data has published for comparable listed datasets,
and large enough that a genuine first page of results is not truncated by the guard
itself. A trigger whose estimated cost would exceed the cap REFUSES before it is sent
-- it never spends to find out.

**The refusal signal** -- what output means "this dataset cannot serve the feed":
all reachable query shapes exhausted with zero records the item rule admits as PASS or
PROVISIONAL (every returned record REFUSEd by the item rule, or the API itself
returned zero records for every reachable shape), OR the estimated cost for the next
attempt would exceed the cost cap before that attempt is sent. Either condition
refuses the run; neither is silently treated as success.

## 5. The fourth-surface fact (not a fourth zone)

F12 (CITED): the datasets API is the SAME credential (`brightdata-api-key`) presented
against a DIFFERENT API surface than the proxy/zone surface `lib/research/identity`
and other estate consumers use for SERP/unlocker work. This is a fourth **surface** on
the one existing credential, **not a fourth zone** -- C-ZONE-IN-CALLER. The next
order's client should read this surface directly against the credential already held;
it does not need to hunt for or provision a new zone.

## 6. What runs when the word arrives

```
python -m lib.research.social.measure \
  --dataset gd_lwxkxvnf1cynvib9co \
  --company "Home Depot HD" \
  --word-record <path-to-the-record-carrying-Andrews-word>@<commit>
```

is the one command. Every dataset id, the company, the query order, the stop rule,
the cost cap and the refusal signal above are already data inside `measure.py` --
the next worker supplies the word record and, per AC6, the HTTP client this module
does not yet carry (AC4: no `requests`/`urllib.request`/`httpx`, no vendor host
named as a literal string, anywhere under `lib/research/social/` at this cut).
