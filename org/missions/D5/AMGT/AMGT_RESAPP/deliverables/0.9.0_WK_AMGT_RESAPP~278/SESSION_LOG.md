# SESSION_LOG 0.9.0_WK_AMGT_RESAPP~278 -- AMGT-ba-12
- Item 1: moved block_all_sockets into watchlist/tests/conftest.py plus an autouse fixture; 5 of 5 tests blocked.
- Item 2: pytest prepend-mode registers lib/research/harvest as top-level `harvest` when a harvest/test_*.py file is collected; serp.py's `from harvest import ...` then hits that package. Fixed in test_ceo_search._load_serp_module (set the stale entry aside during the import).
- Item 3: harvest_serp refuses max_pages != 1 as its first act; plant test in harvest/tests/test_bright_data_serp.py.
- Item 4: two DynamoDB query reads; record in LEGACY_ROWS_Z-W19-S16.md.
