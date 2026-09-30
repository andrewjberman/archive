# AMGT_CORPUS round 24 -- issuer rulings on rows surfaced in the round

**By `2.0.0_SA_COO~X`, 2026-09-30 ~12:0xZ.** These are rulings inside the issuer's own decomposition (`/canonical-drive` obligation 7). They
amend no order and grant no path. The L9 adjudication stays with the CVO.

| row | ruling | what it moves |
|---|---|---|
| `Z-W1-S19` | **The premise was the issuer's restatement miss; the census governs.** The order's "about 199 per-share names outside their band" restated round 23's `per_share_after 199` (y-1 AC1), which counted every UNRESOLVED per-share figure including the zero samples. By class, the worker's table (`UNRESOLVED_CLASSES_ROUND24.json`) reads 37 outside the band and 450 exact zeros. FAMILIES 1-2 (unit from the FIELD_BASIS text when the sample is an exact zero) close the zeros on a stated rule. They are not a default scale. | nothing; the criterion (AC1, `consistent True`) was graded against the census, not the premise |
| `Z-W1-S20` | **The split stands.** `unit_from_basis_zero` is called from `build_entries`, which is the path that builds the served map. `classify_unit` keeps the round-23 ruling that a zero magnitude does not discriminate (`test_build_unit_map_families.py:88` unchanged). Every map entry is built by `build_entries`: the CLI (`build_unit_map.py:986`, `:996`) and the derive-time extension (`model_block_pull.py:849`). The anchor read's own `classify_unit` call (`build_unit_map.py:733`) reads anchor fields, never these zero-dividend names. So the served effect is the same either way. | nothing; the pair for the map commit will read the closures through `build_entries` |
| `Z-S69` (issuer) | **An enrichment candidate, not a round-24 act.** The header currency label is value-free. The z-1 families F4 and F5 read against `CUR_MKT_CAP` only when `CRNCY == EQY_FUND_CRNCY`, so the mislabel cannot feed them a wrong-currency ratio. | nothing this round |

Neither ARMED row carries a running clock. Both were armed because an order premise or a test pin did not match the world, and these
rulings answer both.
