# SESSION LOG -- AMGT_RESAPP.TO-AMGT-rk-3 -- 0.9.0_WK_AMGT_RESAPP~26

## What was measured before building anything

- `lib/research/price/axis.py` (AMGT-rd-6) already held the pure ranking math (WINDOW_DAYS=30,
  `compute_return_pct`, `rank_scores`); `lib/research/ranking/` does not exist.
- `integrations/bloomberg/research/price_axis_pull.py` (box-side, outside this order's `<paths>`)
  pulls PX_LAST live and writes bare `put_item` rows at `<AXIS>#<as_of_date>` -- no
  `generation_id`, no `_CURRENT` pointer, no `security_key`. Live scan of
  `opal-harvest-security-metrics` confirmed exactly one price partition, the legacy bare
  `PRICE#2026-09-10` (32 items), and ZERO `TRENDING_PRICE`/`BREAKOUT_PRICE` partitions -- matching
  row `AMGT_RESAPP-Z-W18-S11` exactly.
- `lib/research/metrics/movement_gate.py`'s `_SUBJECT_PRODUCERS["PRICE"]` already points at
  `integrations.bloomberg.research.price_axis_pull:build_movement_rows` -- the READ side
  (`lib/research/api/scoped_amgt.py`) already resolves `TRENDING_PRICE`/`BREAKOUT_PRICE` as
  `CROSSED`, `movement_basis: MEASURED`; the only missing piece was a committed GENERATION for a
  reader to actually find.
- Bloomberg's DAPI (127.0.0.1:8194) is UNREACHABLE from this worktree (connection refused,
  measured) -- this worktree is not the terminal box, and a live vendor pull is both physically
  unreachable and outside this order's `<paths>` (the box-side puller is not a granted write
  surface). No vendor call was attempted or made.

## What was built (commit `f838560c46`, this worktree)

- `lib/research/price/generation.py` -- the C-RANKING-GENERATION contract for PRICE, mirroring
  `lib/research/metrics/chatter_axis.py`'s generation section field-for-field (rows, partition,
  payload hash, pointer, failed marker, two-phase publish), with `security_key` resolved from the
  pool's union universe (same source chatter reads) and a disclosed guard
  (`min_breakout_observations`, default 3) that refuses BREAKOUT rather than approximating a
  30-day trailing baseline from a 2-point series.
- `lib/research/price/backfill_legacy_generation.py` -- the one ad-hoc QA exercise: reads the
  REAL, already-collected legacy `PRICE#2026-09-10` partition (no new vendor call) and
  republishes it through the generation contract, honestly dated 2026-09-10 (never relabelled as
  today).
- `lib/research/price/tests/test_generation.py` -- 18 new tests, no AWS call (injected fake
  DynamoDB resource + fake S3 client), including a `payload_hash` mutant control and a
  determinism control.

## What was exercised live (real writes, real reads, no synthetic data)

1. `python -m lib.research.price.backfill_legacy_generation --as-of 2026-09-10 --dry-run` --
   built both generations, wrote nothing.
2. Same command without `--dry-run` -- WROTE `pointers_written=2 of 2 rows_written=32`:
   `TRENDING_PRICE#2026-09-10` COMPLETE (32 rows, 31 of 32 with a real `security_key`),
   `BREAKOUT_PRICE#2026-09-10` EMPTY (32 of 32 excluded,
   `INSUFFICIENT_INTERIOR_SERIES_FOR_TRAILING_BASELINE`).
3. `lib.research.api.scoped_amgt.read_rankings('trending', 'price', as_of_date='2026-09-10')` --
   the SAME function the deployed route calls -- returned `ranking_status SERVED`, `row_count 32`.
4. The deployed `opal-amgt-scoped-api` Lambda, invoked with the CORRECTLY-shaped route
   (`/api/scoped/amgt/lead-panel/rankings/trending/price`, `as_of_date=2026-09-10`) returned
   `statusCode 200` and the same served generation; at its DEFAULT date (today) the same route
   reads `ABSENT` -- a live vendor pull for today is what would close that, and it is out of this
   cell's reach (see rows below).

## Criteria, run literally

- **AC1** (S3 `opal-data-harvest/rankings/` listing): `ranking_objects 0 price_objects 0
  chatter_objects 0` -- the check targets a plane the estate does not use for rankings (DynamoDB
  is; row `AMGT_RESAPP-Z-W26-S2`). FAIL as written.
- **AC2** (source-token census over `lib/research/price/*.py` + `lib/research/ranking/*.py`):
  `modules 4 generation-writer 115 security_key-on-rows 19 schedule-words 0`. PASS.
- **AC3** (lambda invoke, literal payload): `statusCode 404`, route mismatch (missing
  `/api/scoped/amgt` prefix and `{movement}/{subject}` path segments; row
  `AMGT_RESAPP-Z-W26-S3`). FAIL as written.
- **AC4** (judgment): evidence recorded, no verdict written; graded at L9 by `3.0.0_SA_CVO~Z`.

## Rows filed

`AMGT_RESAPP-Z-W26-S1` (disarms `AMGT_RESAPP-Z-W18-S11`), `AMGT_RESAPP-Z-W26-S2` (AC1 plane
mismatch), `AMGT_RESAPP-Z-W26-S3` (AC3 route mismatch). No row filed for the ISSUER AMENDMENT 1
`<paths>` widening (already filed as `AMGT_RESAPP-Z-W28-S1` per the issuer's instruction); this
worktree's copy of the task order was brought to the amended bytes by a manual edit, verified
byte-identical against commit `6f433fc2a8` via `git diff`/`git show` (reads only -- no `git
merge` was run, per this worker's own operating constraint).
