# AMGT_CORPUS round 11 -- never-widen pair for the dossier rewrite at `/4` (chain: CRPS-m-1 + CRPS-m-2)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Code at CLOUD HEAD >= `b274848977` (the chain merged); the run prints
`git rev-parse HEAD` first.

## THE ACT
`python -m lib.research.corpus.dossier --write --workers 10` over `_resolved_security_keys()` (95 names), reading stored gold,
extractions and (for the positional read) the six names' bronze pdf pages; no vendor call. A change entry opens before it and
closes with content proof.

## WRITER CENSUS -- one writer
`research-dossier/` is written only by `dossier.write_one` in this seat's drain acts (rounds 7-10 each under a pair). N = 1 rule
read: `write_one` / `_resolve_case_field` / `_case_currency` / `_positional_table` at `b274848977`.

## BEFORE-STATE (measured 2026-09-29 08:29:06Z, HEAD `58a97702b6`; `evidence/r11_rewrite_before.txt`)
`partitions 95 objects 751`; `read_dossier serves the last write 95 of 95`; `dossier_pick names 95 current_method_available 0
stale_pick 0` (every stored object `/3`; code `/4`). Served today: `currency_set` 1 (ML_FP EUR); the six tables ABSENT.

## EXPECTED OUTCOME, READ PER NAME FROM THE PRODUCER'S OWN PATH (`checks/round11/r11_expected_moves.py`: the served fields via
`read_dossier` against the fields the build writes via `_resolve_case_field` with the listing and `_pdf_words_reader`;
`evidence/r11_expected_moves.txt`)
- **Writes: all 95** (every stored object is `/3`; `write_one` writes when the method differs). **95 puts; objects 751 -> 846.**
- **Names whose served cases CHANGE: exactly 10 of 95** -- the other 85 get a `/4` object with identical case fields.
  - **Currency moves (5), under the ruled intersection rule:** CPA_US, SPOT_US, UNVGY_US `null -> USD` (`$` on USD listings);
    BZLFY_US `null -> USD` (its table is newly read; `$` on a USD listing); **SHOP_CN `null -> CAD` (`$` on a CAD listing). The
    round-10 analysis expected "CPA, SPOT, UNVGY -> USD, and no other name moves"; its own criterion moves SHOP and BZLFY too.
    This half names both; THE CTO HALF DECIDES WHETHER SHOP'S MOVE IS SERVED** (if refused, the rule needs a carve-out and
    this act does not run until it lands).
  - **Served moves (6), by the positional read:** 8035_JP, BZLFY_US, HEI_US, SNPS_US, TSM_US, V_US -- all three cases go
    `ABSENT -> served`; each Base row carries its blank as `null` at 2030E (EPS, Price, Return), placed by x-coordinate (HEI:
    Base header centres 323 / 361 / 399 / 437 / 475, values at the first four, nothing at 475). No arithmetic places a value.
  - **No other branch today:** `positional names 6 placed 6 ambiguous 0 no_positions 0` -- the "stays ABSENT" branch applies to
    none of the six at `b274848977`; if a page read fails at write time the name stays ABSENT with its round-10 reason.
- A side effect of the rule that serves nothing today: the yen sign on a JPY listing would now set JPY; no served name carries
  it (none of the 11 symbol-bearing names).

## AFTER-STATE THE VERIFY READS (content, not rc)
1. `dossier_order_census.py`: `objects 846`, `read_dossier serves the last write 95 of 95`, `rewrites_on_unchanged_inputs 37`.
2. `dossier --pick-census`: `current_method_available 95 stale_pick 0`.
3. `dossier --case-census` equal to the in-memory before-state line: `body 102 heading_only 0 absent 183 sum 285 ordering_held 34
   ordering_violated 0 ordering_na 61 unit_carried 11 currency_set 6 currency_null 28`.
4. `r11_expected_moves.py` re-run after the act: `moved 0` (the served table now equals the build).
5. `read_dossier` on SHOP_CN (as the CTO half rules), CPA_US (USD) and HEI_US (Base EPS `6.03, 6.80, 7.73, 8.99, null`) read by
   this seat.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 95 new objects under `research-dossier/`; no delete, no overwrite.
- **Readers of `cases`:** AMGT_RESAPP's scoped API through `read_dossier` (its round-46 ruling 3); a `null` year inside a served
  case is new to that reader -- named here so RESAPP renders a blank cell as blank.
- **Rollback (same day):** revert `METHOD_VERSION` to `/3`; `read_dossier` then prefers the stored `/3` objects.

## STOP LIMBS
1. `put_performed` total != 95 or any `ERROR:` -> stop; the re-run is resumable.
2. After-state line 2 reads `stale_pick` > 0 -> stop and roll back.
3. After-state line 3 or 4 differs from the stated values -> stop; name the names.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `write_one`, `_resolve_case_field`, `_case_currency` and
`_positional_table` at `b274848977`. If any moves before the act, this half does not travel with it.
