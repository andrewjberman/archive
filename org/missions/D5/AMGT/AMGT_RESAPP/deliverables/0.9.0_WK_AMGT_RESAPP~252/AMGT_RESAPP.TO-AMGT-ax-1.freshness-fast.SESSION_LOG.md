# Session log -- 0.9.0_WK_AMGT_RESAPP~252 on AMGT_RESAPP.TO-AMGT-ax-1

- Captured /freshness through the route handler before any edit: before.json, 302 rows, cold read 34.2 s.
- Profile of the unchanged read: 123 store calls, 99 of them one-at-a-time pack ledger reads (17.3 s of 27 s).
- Change in lib/research/api/scoped_amgt.py: `_ledger_dates` (16-wide, each ledger read once), `serve_coverage_freshness`
  (60 s hold in served_cache, key freshness/view, stored only when every read completed), route calls the latter.
- after_equal.py: cold and warm both EQUAL 302 of 302 rows against before.json.
- Plant test lib/research/api/tests/test_freshness_fast.py: 5 passed; with the route on the unheld read, 2 fail.
- api suite: 661 passed. Code commit 242d94c616. No surprise row filed.
