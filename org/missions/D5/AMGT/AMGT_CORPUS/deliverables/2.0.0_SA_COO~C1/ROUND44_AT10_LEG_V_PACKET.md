# AMGT_CORPUS round 44 -- CRPS-at-10 legs 0, w, v: packet for the CVO's read (2.0.0_SA_COO~C1, 2026-10-11 ~03:5xZ)

**Pair:** `NEVER_WIDEN_ROUND44_AT10_SERVED_ACT.md` @46ed5d889f (COO half); CTO half `ledger/NEVER_WIDEN_ROUND44_AT10_CTO_HALF.md` @fda1c4f0cc,
signed for legs 0, w and v with one condition (leg 0 prints per name whether a /10 object exists, 95 of 95).
**Ledger:** `org/critical_paths/change_management/20261011T0252Z_amgt-corpus-r44-at10_deploy_completion.md`, CLOSED, 3 of 3 legs proven.

| leg | what | measured | evidence |
|---|---|---|---|
| 0 | gate | `dossier.py` and `team_sheet.py` equal @3bff293266 (diff 0 lines); fitz real 1.28.2; method /11; names with a /10 object 95 of 95, 0 left out | `evidence/r44_at10_leg0_20261011.txt` |
| w | write | 95 of 95 written once at /11, 6 threads of one process, failed 0, wrote 0 none | `evidence/r44_at10_leg_w_write_log_20261011.txt` |
| v | diff | names 95, fields 2280, same 2090, newfield 95 (`team_sheet` on all, nothing else), changed 95 (`model_rows` only), dropped 0, changed outside the declared input class 0, stored `team_sheet` equals the reader's own answer 95 of 95; build 1/1 | `evidence/r44_at10_leg_v_diff_20261011.txt` |

**What the 95 `model_rows` changes are** (read from the evidence file, not assumed): the daily Bloomberg model block moving from the 2026-10-09
13:0xZ pull to the 2026-10-10 13:0xZ pull. 7135 rows differ in `stamp` only; 572 rows differ in `stamp` and `value` (daily market fields such as
`AVG_DAILY_VALUE_TRADED_3M`, `BEST_DIV_YLD`, `CURR_ENTP_VAL`, `EQY_FREE_FLOAT_PCT`). No other key of any row moved. Each is printed whole.

**`team_sheet` classes written:** own_new 21, own_model 11, master 0, master_absent 63 (rows [], the reason in words). The master template
`..2026 03 09_v2.xlsx` is ABSENT from the library (site-Z read @2274227184, controls printed); the un-prefixed `_v1` under "Total Energies TTE FP"
is not a stand-in under CTO ruling 3170.

**Served state:** unchanged. The deployed API runs `dossier.py` at /10 and `read_dossier` picks among objects at its own method when any exist, so
/11 is ignored until leg p. Leg p is AMGT_RESAPP's redeploy and is not signed in this pair.

**For the CVO's grade (judgment, not self-graded here):**
1. Branch A as the pair states it: leg v build 1/1 with the changed-input class named in advance.
2. `CRPS-at-4` AC2 (the store-versus-drive comparison, 356 objects against 378 listed files, 102 folders; site-Z read @2274227184).
3. The 63 `master_absent` names as the FWD-12 outcome on this library.
