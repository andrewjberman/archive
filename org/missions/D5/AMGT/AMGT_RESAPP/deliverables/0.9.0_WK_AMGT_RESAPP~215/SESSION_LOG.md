# 0.9.0_WK_AMGT_RESAPP~215 session log -- AMGT-an-6 (round 64 repairs)

- Re-grounded: worktree wk-AMGT_RESAPP-215 at 34e9d1be75, org/.tools present. The branch's r64_served.py was the pre-amendment check (row Z-W215-S1); ran the CLOUD @13dc3f05ba copy from .scratch.
- Table read (read-only GetItem): etf-classifications holds the slash-free keys 'BP' (BP PLC, equity, Energy) and 'NG' (no name, equity, Utilities); 'BP/' and 'NG/' return None.
- Mapping: bare 'BP/' -> crosswalk.slash_safe_key -> 'BP-SLASH-' -> drop the trailing token -> 'BP'. Confirmed by name against the crosswalk or model-block header name.
- Stored management bodies carry no source_stamp: the route serves object_as_of from the key (2026-10-02T1840Z), labelled as from the key.
- Census --days 7: 5 500s across 22415 invocations, one signature (REPORT Status: timeout).
- Commit f9245a8404 (code, tests, census, row); the proof instance and this log follow in a second commit.
