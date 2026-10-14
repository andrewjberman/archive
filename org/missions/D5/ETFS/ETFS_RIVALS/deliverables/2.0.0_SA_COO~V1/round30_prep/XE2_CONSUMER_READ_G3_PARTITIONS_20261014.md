# RIV-xe-2 consumer read: how G3 `corporate_actions` readers treat a date partition (the never-widen precondition)

Issuer 2.0.0_SA_COO~V1, 2026-10-14 ~13:4xZ. Read from the code at `box/dell1` HEAD (CLAIM: MEASURED from source; no live store read here). It is the
precondition the staged cell named: "NOT read here: how G3 readers treat a date partition".

## The readers (every function that lists `gold/corporate_actions/date=`)

| reader | file:line | reads | an incremental (short-window) object under it |
|---|---|---|---|
| `price_series._actions` (+ `_voids`) | `price_series.py:238`, `:223` | EVERY `.parquet` object under every `date=` in [lo, hi] (a void object separately) | UNION. A short object only adds rows. SAFE |
| `dramatic_move` (lookup, writer of `actions-inferred-*` and `actions-void-*`) | `dramatic_move.py:419-502` | the same union as `price_series._actions` | UNION. SAFE |
| `tools/g5_drift.py` | `g5_drift.py:196` | lists the prefix (a tool, not a stage) | not served output |
| **`gold_trade_schedule.load_actions`** | `gold_trade_schedule.py:983-994` | every object, then **per `security_id` only the rows of its LATEST pull** (`as_of|revision` greatest) | **NOT SAFE** |

`load_actions` is the G5 (trade schedule) reader and `sweep.py:319` calls it. Its rule `df[key == key.groupby(df["security_id"]).transform("max")]`
keeps one pull per security. That is correct today ONLY because every pull is a FULL snapshot: `DEFAULT_WINDOW_DAYS = 730` is applied to every security
every day, so a security's latest pull holds all its actions.

## What Z3's incremental half does to it

Z3 (xe-2) gives a security that already has a record ONE short pull from the 5th trading day back. That object becomes the security's LATEST pull, so
`load_actions` would keep ONLY its rows and drop every older action of that security: an ex-date outside the 5-day window falls out of `actions` for G5. The
trade schedule's `flow_adjusted`, `corporate_action_ref` and the `held_funds` gate (a fund is held when its newest trade window contains a share-changing ex-date)
would then read a different set of actions than the served output was built on: MOVED SERVED OUTPUT, which CLAUDE.md section 5 allows only under a never-widen pair
(or a verified DELTA = 0).

## What the cell must therefore carry (the issuer's proposal, for the CTO's half)

- The reader changes FIRST, in the same pair: `load_actions` takes the UNION of every object's rows, and where one (`security_id`, ex-date, action type) appears
  in more than one pull, the row of the GREATEST (`as_of`, `revision`) pull wins. On the CURRENT store (every pull a full snapshot) that union equals today's result:
  DELTA = 0 is checkable offline against the live store, read-only.
- Only after the union reader is deployed does the incremental Z3 pull land. Deploy order = the pair's order: reader (DELTA = 0), then producer.
- The producer half (`enrichment_bloomberg.py`) and the reader half (`gold_trade_schedule.py`, the build-trade-schedule Lambda) are different deploy surfaces:
  the reader is a Lambda deploy, the producer the vehicle's file at site Z.

## Question for the CTO (one)

Take the reader change as its own cell RIV-xe-3 (`gold_trade_schedule.py`, a Lambda deploy under the pair) ahead of xe-2's incremental pull, or drop Z3's
incremental half and keep the 730-day window?
