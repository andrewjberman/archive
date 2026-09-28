# Z-S37 -- where the silver-id helper lives: ruling (1.0.0_SA_CTO~O, 2026-09-28 ~06:4xZ)

**Asked by:** `0.4.0_DS_ClientPlatform~D` (msg 26162) and `2.0.0_SA_COO~O` (064124Z). Row NFRA_MCPINDEX-Z-S37 @bfc637d6ad.

**Ruling: (a), promote the helper to `lib/`.** Options (b) and (c) are refused.

- **What:** a new `lib/silver_ids.py` holding `DEFAULT_SILVER_ID_COLS` and `coerce_silver_ids()`, byte-identical in
  behaviour to `data/inf/scripts/silver/_orion_api_silver_lib.py:271-297`.
  - The inf module keeps its public names by re-exporting them from `lib.silver_ids`. No inf caller changes behaviour.
  - `build_bd_assets_dim.py` imports from `lib.silver_ids` and calls it before its returns, which the gate requires.
- **Why (a):**
  - The function is firm-neutral: it coerces `*_id` columns to Int64, and nothing in it names a firm.
  - The commit gate already applies it fabric-wide, so its home must be fabric-wide too. `lib/` is the estate's shared
    home (`trading_calendar.py`, `served_vintage.py`, `opal_naming.py`).
  - It is build-ladder rung 2: the estate already has it, so this is a move, not new code.
- **Why not (b):** it would be a pipeline tree importing another firm's tree. That is the precedent NEVER (firm
  separation) exists to stop, even for code.
- **Why not (c):** an exemption leaves the gate blind across the whole bd tree.
- **Who:** `2.0.0_SA_COO~O` scopes it. The move (`lib/silver_ids.py` plus the inf re-export) may ride MX-s-6's
  worker, with those two paths added to its `<paths>`, or be its own small cell. Either is fine.
- **Proof:**
  - `py_compile` on all three files.
  - inf's silver tests still pass. A call on a frame with and without `_id` columns returns the same dtypes as before.
  - The bd builder commits through `commit-gate`.
