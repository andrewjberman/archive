# AMGT-rd-6 -- THE PRICE AXIS ENGINE: host record

`0.9.0_WK_AMGT_RESAPP~6`, round 5/v5, cell AMGT-rd-6 (row S16, FWD-15).

## The host this engine runs on

**The BLOOMBERG TERMINAL box** -- the machine whose loopback-only DAPI at `127.0.0.1:8194`
is the only place Bloomberg data can be pulled from. Measured directly, this session:

```
$ hostname
Opal_Bloomberg

$ python integrations/bloomberg/auth/dapi_check.py
DAPI: UP (session + SPX Index/PX_LAST returned -- entitled session live)

$ where python
C:\Users\Opal Bloomberg\AppData\Local\Programs\Python\Python311\python.exe
```

`python` on PATH resolves to Python311 (blpapi + boto3 + pyarrow importable, measured by
`price_axis_pull.py` running end to end against the live DAPI and landing rows to DynamoDB
in this same session) -- the PY_AWS interpreter `integrations/bloomberg/READ_HERE.md` section
3 names as the landing-legs interpreter, and the one `integrations/bloomberg/pipeline/
etf_daily_pull.py` and AMGT-s-1's `model_block_pull.py` already run under.

**NOT the harvester EC2 box `AMGT-rd-3` stands up.** That box hosts the four ARTICLE
harvesters and carries no Bloomberg terminal; this engine was never deployed there and does
not depend on it (the task order's own DEPENDENCIES section: "It does NOT depend on
`AMGT-rd-3`"). **NOT a Lambda.** The DAPI is loopback-only (`127.0.0.1:8194`); a Lambda has
no network route to a loopback address on this box, so no Lambda-calling-Bloomberg path
exists anywhere in this engine (AC3's denominator: 103 hits across 107 files under
`lib/research` + `integrations/bloomberg` reach Bloomberg exclusively through `8194` /
`blpapi` / `127.0.0.1` -- zero hits name an HTTP invoke of a Lambda from this code).

## The existing box-side pull this engine follows

`price_axis_pull.py` (`integrations/bloomberg/research/price_axis_pull.py`) is the SAME
shape as two already-landed precedents, not a second path to the same data:

1. **`integrations/bloomberg/pipeline/etf_daily_pull.py`** (ETFS_POSITIONING L1, LIVE in
   production) -- the cell text's own name for the shape, "the ETF-daily-pull shape": a job
   ON THIS BOX calls the estate's raw client (`blp_client.reference_data` /
   `blp_client.historical_data`), computes, and lands the result. Nothing crosses inbound
   from AWS.
2. **`integrations/bloomberg/research/model_block_pull.py`** (AMGT-s-1, LANDED round 1,
   this project's own round-1 precedent) -- the same raw client, the same box, a
   `HistoricalDataRequest` for a fiscal-year series, and a persisted, re-readable output.

`price_axis_pull.py` reuses `integrations/bloomberg/mcp/blp_client.py` unmodified (imported,
never re-implemented) for both the health-adjacent probe (`dapi_check.py`, run before this
record) and the historical pull (`blp.historical_data`, batched in chunks of 20 securities --
the same chunking shape `etf_daily_pull.py` uses), and writes through `boto3.resource(
"dynamodb").Table("opal-amgt-security-metrics")` the way `etf_daily_pull.py` writes through
`boto3.client("s3")` -- a box-side job landing to an AWS store it has credentials for, never
the reverse.

## What it computed and wrote, this run

```
as-of 2026-09-10 (lib.trading_calendar.prev_trading_day of 2026-09-11)
window 2026-08-11 .. 2026-09-10 (30 days, lib.research.price.axis.WINDOW_DAYS)
universe: 34 covered names (AMGT-s-12's universe.json, bloomberg_ticker status MEASURED)
scored: 32 of 34 (2 insufficient history in window: Enel IM, ROG SW)
written: 32 of 32 PRICE-axis rows to opal-amgt-security-metrics
  axis_date = "PRICE#2026-09-10" (HASH), ticker (RANGE), rank_sort zero-padded (GSI
  axis-rank-index), rank 1 = PBR US (+19.24%), rank 32 = BABA US (-15.09%)
```

Verified live, this session, via two independent reads (a `Query` on the real KeySchema and
a `describe-table`-adjacent `scan --select COUNT`), not from this script's own log:

```
$ aws dynamodb query --table-name opal-amgt-security-metrics \
    --key-condition-expression "axis_date = :ad" \
    --expression-attribute-values '{":ad":{"S":"PRICE#2026-09-10"}}' --select COUNT
{"Count": 32, "ScannedCount": 32}

$ aws dynamodb scan --table-name opal-amgt-security-metrics --select COUNT
{"Count": 42, "ScannedCount": 42}   # 32 PRICE + 10 CHATTER -- both axes coexist, no overwrite
```

## Instrument trap found and corrected in-session

`aws dynamodb scan --output text` renders every attribute NAME upper-cased
(`AXIS_DATE`, `TICKER`, ...) for display; the table's actual, declared `KeySchema` and every
stored attribute name are lowercase (`axis_date`, `ticker`, ...), confirmed by re-reading the
same table with `--output json`. A first cut of `price_axis_pull.py` copied the `text`
rendering literally into its `PutItem` calls and every write failed with `ValidationException:
Missing the key axis_date in the item` -- caught by exercising the write live (AC2's own
"LIVE plane" reasoning) rather than trusting the script's own success claim, and fixed before
this record was written. `price_axis_pull.py`'s docstring carries the correction inline.
