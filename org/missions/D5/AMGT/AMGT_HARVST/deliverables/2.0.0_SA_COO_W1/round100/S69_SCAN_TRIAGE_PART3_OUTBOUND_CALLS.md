# Row AMGT_HARVST-D1-S69 -- triage part 3: does the driver's own code reach a host beyond AWS? (2.0.0_SA_COO~W1, 2026-10-21 ~02:0xZ)

Continues parts 1 and 2 (`2dc420645c`, `68c78e014d`). Image `amgt-gold-refresh-repo@sha256:4da76365...fdd74`.

## What I searched, with its denominator

Native Grep over `lib/`, glob `**/{gold_refresh,publication_gold,store,universe_securities,finbert_sentiment,pool_reader,crosswalk,chatter_axis,chatter_gate,generation_writer,movement_gate,trading_calendar,opal_naming,harvest_grammar}.py`. **Positive control first:** the same glob with the pattern `boto3|^import |^from ` matched 16 files (143 hits). Fourteen are the closure's modules from `co5_closure.out` (its 20 `lib_modules` are these 14 files plus 6 package `__init__` files, which I did not search); two (`research/watchlist/store.py`, `research/aifill/store.py`) share a basename and are NOT in the closure. My first attempt used directory-qualified globs and returned zero files: a zero out of corpus, discarded.

## Results

| Pattern | Hits in the 14 closure files |
|---|---|
| `urllib`, `http.client`, `urlopen`, `socket`, `requests` (the library), `ftplib`, `smtplib`, `websocket`, `curl` | **none.** The `requests` hits in `gold_refresh.py` (lines 63, 83, 99, 111, 123) are an S3 request COUNTER, not the library. |
| `subprocess`, `os.system` | `lib/opal_naming.py` lines 2921-2930, 3109-3110, 3487-3491: `git grep`, `git ls-files` and a command run inside naming-gate functions that work on the repository. The image carries no `.git`; these functions are not on the driver's call path as I read it (the driver builds names through `name()`), but I did not trace every caller. |
| `boto3.client(...)` / `resource(...)` | `s3` in `store.py:184`, `pool_reader.py:138`, `chatter_axis.py:254`, `crosswalk.py` (five sites); **`lambda`** in `finbert_sentiment.py:84` and `:199` (scoring: `_lambda_invoke` and `score_missing` with `workers>1`); **`dynamodb`** in `generation_writer.py:416`. |

## What the driver actually calls (read)

`gold_refresh.py` imports `finbert_sentiment` and calls ONLY `finbert_sentiment.latest_scores(client)` (line 230), with the S3 client it built; it does not call `score_missing` or `_lambda_invoke`. The canary's own log shows `NOTE sentiment scored_keys=13224 bytes_read=2096262` (an S3 read) and `gets=14204 s3_puts=0` over the whole run. I did not trace `generation_writer` (DynamoDB): the driver does not import it directly, and the task role holds no DynamoDB or Lambda action (live policy read at 00:2xZ: `s3:ListBucket`, `s3:GetObject`, `s3:PutObject` under three prefixes), so a call to either would be denied.

## Reading, and what stays open

- **Measured:** no standard-library or third-party HTTP client call in the 14 modules; the driver's sentiment path is an S3 read; the one non-S3 AWS client in its import chain (Lambda scoring) sits on a path the driver does not call; the IAM role cannot reach it anyway.
- **Not measured:** the 812 modules of the loaded closure beyond these 14 (pandas, pyarrow, numpy and the calendar libraries could in principle open a network connection; I did not read them); the six package `__init__` files; the callers of the `opal_naming` subprocess functions; a rebuild on the current base image (part 2 (c)).
- **For the enabling addendum:** the evidence is that this task's outbound traffic is S3 reads and puts by `boto3`, bounded by a role that can do nothing else. It is a bounded read, not a proof. If the CTO wants proof, the cheap instrument is a VPC flow log or an egress-denied security group on the next canary; neither exists today.

Row `AMGT_HARVST-D1-S69` stays `UNDER_INVESTIGATION` until the CTO reads this and the enabling addendum cites it.
