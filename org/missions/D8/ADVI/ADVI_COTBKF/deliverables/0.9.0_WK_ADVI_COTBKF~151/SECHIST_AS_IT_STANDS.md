# SECHIST as it stands (round 79, CB-ca-1), read by 0.9.0_WK_ADVI_COTBKF~151

**Scope: tree_only.** MDPF_SECHIST is held by fabric dell1 (project.json: `"fabric": "dell1"`, `"placement": "DELL1"`, `"coo_lane": "2.0.0_SA_COO~H1"`).
Nothing of that fabric's data was read. No AWS, network or vendor call was made. The ask must go through 0.0.0_AB_MSTR~DELL2 (text in the JSON, key `ask_through_mstr`).

**Tree read at** commit 1a27c8cc13. Newest commit touching the project folder: f8e359debf (2026-10-10). Newest touching data/mdpf/scripts/: 8152a8ea42 (2026-10-11); the series writer itself: 3f81467e2a (2026-10-09).

## What the tree says
- Stage EXECUTING, status active. 24 task orders: 18 complete, 3 carried (t12, t17, t18), 3 issued (t20, t21, t22; open).
- Its own statement: C-SERIES (PRD :95) "ONE series per security ... Every screen reads this series"; as amended (ADDENDUM v0.3, :181-183) per day "the as-traded price, the dividend/interest cash and the total-return value".
- The writer `data/mdpf/scripts/silver/security_series_writer.py` is built (task order t13 complete) but writes nothing unless `switch=True` (:21, :119-125). No caller in data/mdpf/scripts passes it. The CTO ruling (KEEP, then PORT) says DEMQUE's `price_store` is the only live Yahoo writer until a later port window.
- **Existence of the history: not_established.** Code and a contract exist; no committed record shows a series landed. Scheduled: not_established (no infra declaration found). Populated: not_established.

## Fields and basis
- Columns: `date, as_traded_close, cash, total_return, source` (:37). `source` says per row where the point came from.
- `carries_a_basis`: true, by the column name and the writer's docstring ("as-traded price" :4; input "already as-traded" :9). The writer itself applies **no** split scaling (:75 takes the value unchanged; the split ratio only enters total_return, :83).
- The scaling is applied upstream in DEMQUE `yahoo_pull.py:63,110,130-136`: vendor Close with `auto_adjust=False` times every later split. So `as_traded_close` there is the split-undone vendor close, not the vendor Close alone. If the ADVI build then applies its own split scaling on top (v0.9 item 2), the value would be scaled twice: a question for the issuer, not measured.

## The 15 funds
Coverage is **not read**: `funds_in_history = 0` and `held_trading_days_covered = 0` mean NOT READ, not absent. The 20,718 held trading days (recounted: the 15 per-fund counts sum to 20,718) are shown as `unpriced_under_c_basis = 20718` only as **not shown covered**, not as shown uncovered (`unpriced_is_not_read = true`). Price equality with the vendor cache: not read.
A DEMQUE record (not SECHIST's) lists SGIIX and PCBIX as stale price files in its own store; it is not counted.
