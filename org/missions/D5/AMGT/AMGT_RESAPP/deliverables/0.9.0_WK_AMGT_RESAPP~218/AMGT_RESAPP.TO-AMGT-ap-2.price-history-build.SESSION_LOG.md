# Session log -- 0.9.0_WK_AMGT_RESAPP~218 on AMGT-ap-2

- Partition naming: <crossed axis>_<N>D (TRENDING_PRICE_90D ...), declared once in lib/research/api/rolling_windows.py price_window_axis; rows at <axis>#<as_of>#<generation_id>, pointer at <axis>#<as_of>/_CURRENT.
- Window rule: observations dated as_of - N calendar days .. as_of, the same rule the 30-day pull uses.
- History: bloomberg/harvest/bronze/price_history_px_last/date=<as_of>/{year_pull,daily_30d}.json via address() and store.bronze_put (write-once).
- No registry row was needed: address() accepted the table name.
- Not run: --live, price_axis_pull.py for real, any S3 or table write, any deploy.
