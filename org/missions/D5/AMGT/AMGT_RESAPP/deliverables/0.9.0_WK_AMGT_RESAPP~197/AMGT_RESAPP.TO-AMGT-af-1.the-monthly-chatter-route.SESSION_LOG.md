# Session log -- 0.9.0_WK_AMGT_RESAPP~197 on AMGT_RESAPP.TO-AMGT-af-1.the-monthly-chatter-route

- Built lib/research/api/monthly_chatter.py, one dispatch branch in scoped_amgt.handler()'s timeseries block, and 7 tests. Code commit 45e4ac9009.
- Live local read (S3 read-only): 95 rows, as_of 2026-09-30, months 2026-01..2026-09, partial_months [], vintage = chatter_daily date=2026-09-30/part-20260930T181745Z.parquet + article_security_mention date=2026-09-30/part-20260930T134616Z.parquet. 63 of 95 rows carry a crosswalk name; 32 fall back to the security key.
- Per-publisher sum differs from collected on 0 name-months (the order asked for a row if any).
- AC2 PASS C1-C8, YES. AC1 FAIL as run: exit=1, 3 portal-fixture errors (row Z-W197-S1).
- Worktree sparse cone: added org/surprise_channel (the surprise-row gate needs its schema; first commit attempt was refused fail-closed for the missing file).
