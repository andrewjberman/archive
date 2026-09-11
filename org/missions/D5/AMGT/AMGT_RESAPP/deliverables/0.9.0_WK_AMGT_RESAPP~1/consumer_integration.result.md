# AMGT-rb-2 -- THE FISCAL BLOCK, WIRED TO THE CONSUMER: result

**Worker:** `0.9.0_WK_AMGT_RESAPP~1` -- **Task order:** `AMGT_RESAPP.TO-AMGT-rb-2.fiscal-block-wired-to-consumer.md`
(AMENDMENT 1, `<paths>` now grants `lib/research/print/` + `lib/research/provenance/`) -- **Read at:** HEAD
`15dd12638b` (this worktree's cut; carries the amended order + AMGT-rb-1's landed direction fix).

## (a) THE NAMED CONSUMER

The concrete provenance/print consumer that reads `model_block` for the served analyst pack:

- **Module:** `lib/research/print/render_pack.py` (AMGT-s-5, "Adam's artifact, server-side" -- the PDF/txt
  research pack).
- **Function:** `load_model_block(sec_key: str) -> dict` (called from `build_pack(security)`, BLOCK 1 "the
  pasted Excel model block").
- **The derived key it reads:** `DELIVERABLES / f"model_block_{sec_key}.json"` (the LOCAL copy of the
  original `derived/model_block/<security_key>/<stamp>/model_block.json` engine).
- **Second consumer of the same lane:** `lib/research/provenance/render_print.py::render_model_block()` /
  `main()` (AMGT-s-3, the print-path fragment) -- `main()` takes a `model_block.json` path as its one CLI
  argument and produces `provenance_render_<security_key>.md`. `render_pack.py` imports
  `render_figure_line` from this module directly, so both consumers share the same per-figure line format.

## (b) WIRED TO THE CORRECTED LANE -- DONE

**The smallest correct switch: an OVERLAY read of the fye key, applied only to the in-memory dict each
consumer returns/renders -- the original `model_block_<security_key>.json` file on disk is never opened for
write, never overwritten, never aliased (STORE_CONTRACT rule 1; see AC3).**

Two new functions in `lib/research/provenance/render_print.py` (the lower-level module both consumers
already share via the existing `render_figure_line` import):

- `load_corrected_price_overlay(deliverables_dir, sec_key) -> dict[fiscal_year, row]` -- reads
  `model_block_fye_<sec_key>.json` (AMGT-r-1's corrected local copy) IF it has landed for that security;
  returns `{}` (a true no-op) if it has not -- never a vendor call, never an error on absence.
- `apply_corrected_price_overlay(model_block, overlay) -> dict` -- for every FISCAL-YEAR (not header)
  `PX_LAST` figure, replaces `value`/`vintage` with the overlay's `price`/`price_date` when the overlay has
  an entry for that figure's `fiscal_year`, and appends `" (fiscal-period join, model_block_fye)"` to
  `source` for provenance. Mutates and returns the SAME in-memory dict; nothing is written back to disk.

Wired at both call sites:

- `render_pack.py::load_model_block()` now reads the original file, then calls
  `apply_corrected_price_overlay(mb, load_corrected_price_overlay(DELIVERABLES, sec_key))` before returning.
- `render_print.py::main()` now calls the same two functions (using `in_path.parent` as the deliverables
  dir and the model block's own `security_key`/`in_path.stem`) before `render_model_block()`.

## (c) MEASURED, THROUGH THE WIRED CONSUMER (BABA US Equity, FY2025)

| | value | vintage/date | source |
|---|---|---|---|
| Original `model_block` lane, read DIRECTLY off disk (unwired, bypass) | **146.58** | `2026-09-10T23:20:19Z` (landing timestamp) | `bloomberg-dapi` |
| Corrected `model_block_fye` lane (AMGT-r-1) | **132.23** | `2025-03-31` (fiscal period end) | -- |
| **WIRED consumer** (`render_pack.load_model_block("BABA_US_Equity")`, live-exercised) | **132.23** | `2025-03-31` | `bloomberg-dapi (fiscal-period join, model_block_fye)` |

The wired consumer returns the fiscal-period price (132.23), NOT the calendar-year price (146.58) -- the
exact end-to-end difference AC1/AC2 require. The original on-disk `model_block_BABA_US_Equity.json` file is
verified byte-unchanged (`git diff --stat` shows 0 changes to that path; a direct re-read off disk still
returns 146.58) -- the overlay is applied only to the value this function RETURNS, never persisted back.

The overlay applies uniformly to all 3 landed securities (no security-specific code): SAP GY Equity FY2016
82.81 (was a 2-day-gap calendar figure), BA US Equity FY2016 155.68, BABA US Equity FY2016 79.03 -- all
three now carry the `(fiscal-period join, model_block_fye)` source tag, confirming the wiring fired for
every security the corrected lane has landed for, not just BABA.

## END-TO-END TEST

`integrations/bloomberg/research/tests/test_consumer_wiring.py` (5 new tests, discovered by
`pytest integrations/bloomberg/research/tests`):

1. `test_original_model_block_lane_carries_the_calendar_year_price_unchanged` -- negative control: the
   on-disk file still carries 146.58 (STORE_CONTRACT rule 1 holds).
2. `test_wired_consumer_load_model_block_returns_fiscal_period_price_not_calendar_year` -- AC1's exact
   difference arm: `render_pack.load_model_block` returns 132.23, not 146.58, vintage 2025-03-31, source tags
   the overlay.
3. `test_wired_consumer_render_print_main_path_also_overlays` -- the SAME wiring exercised through
   `render_print`'s functions directly, plus a rendered-markdown check ("132.23" present, "146.58" absent).
4. `test_header_price_untouched_by_the_overlay` -- the header PX_LAST snapshot (not a fiscal-period pairing)
   is untouched.
5. `test_overlay_is_a_no_op_when_no_corrected_lane_has_landed` -- `apply_corrected_price_overlay({})` is a
   true no-op, proving the wiring degrades safely for any security without a landed corrected lane.

`python -m pytest integrations/bloomberg/research/tests -q` -> **10 passed** (the 5 pre-existing fye tests
unchanged + these 5).

## ALSO -- THE PROVENANCE RENDER OUTPUT (CTO holes-scan tick 2, msg 21330)

`provenance_render_BABA_US_Equity.md` (and the SAP GY / BA US siblings) are within this TO's `<paths>` grant
(`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/`) and are this SAME worker slot's own deliverables (AMGT-s-3,
same slot `~1`), not a different worker's/peer's artifact -- regenerating them is in-surface and does not
touch anyone else's write grant. **Regenerated all three** via the now-wired named consumer, exactly as
AMGT-s-3's own proof-of-spec instance ran it (`python -m lib.research.provenance.render_print
<model_block_<security_key>.json>`):

- `provenance_render_BABA_US_Equity.md`: FY2025 line now reads `132.23 ... as of 2025-03-31` (was `146.58
  ... as of 2026-09-10T23:20:19Z`); 10 of 10 fiscal-year PX_LAST lines changed (BABA's full corrected
  history), 0 non-price lines changed.
- `provenance_render_SAP_GY_Equity.md` / `provenance_render_BA_US_Equity.md`: regenerated too for
  consistency (both December filers, small pre-existing gaps of 0-2 days; 10 lines each changed to the exact
  fiscal-period price/date rather than the near-adjacent calendar-year one).

**NOT regenerated:** `pack_SAP_GY_Equity.pdf`/`.txt` (AMGT-s-5's Adam's-artifact PDF). The coordinator's ALSO
instruction named the provenance render output specifically; no BABA (or BA US) PDF pack exists yet to be
stale in the first place (AMGT-s-5 only ever ran `build_pack` for SAP GY Equity, whose pre-existing gap was
already only 2 days), and regenerating SAP's existing PDF was not asked for and would not demonstrate the
C-S16 difference this cell exists to prove. Left as-is; a future cell can regenerate/produce the PDF packs
once round 3's `.tsx` serving path exists (AMENDMENT 1's own scope note: no `.tsx` is served yet).

## STORE_CONTRACT rule 1 (AC3)

`derive_fye_fixed.py` is untouched by this cell (still committed at `17f7cba834`, still the distinct
`model_block_fye` engine). The original `model_block_<security_key>.json` files are verified byte-unchanged
on disk (`git diff --stat` against each shows 0 changes). Nothing was overwritten or aliased -- the wiring is
entirely an in-memory overlay applied by the two consumer functions.
