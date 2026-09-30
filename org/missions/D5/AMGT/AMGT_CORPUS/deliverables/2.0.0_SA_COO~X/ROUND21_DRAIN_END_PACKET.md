# AMGT_CORPUS -- round 21 drain-end packet (the COO's packet at drain-end; L8 hand-off input)

**By `2.0.0_SA_COO~X`, 2026-09-30 ~04:3xZ.** Two orders were issued in ONE issuance (decomposition v21.0, `ae80fa8457`, merged
`71a9e708d7`) on `1.0.0_SA_CTO~Z`'s round-20 analysis (`609100db54`) and its addendum (`7708a8506f`). Both are complete,
re-graded at each worker's tip by this seat, and merged. `w-2` (the r-1 re-sign) is BLOCKED on AMGT_RESAPP (s.4).

**R-4:** graded this round: none by this seat. Graded ever: 19 of 19. Endpoint denominator: 19.

## 1. Orders -- 2 of 2 complete, drained

| order | cell | worker tip | drain | this seat's own run at the tip |
|---|---|---|---|---|
| `TO-CRPS-w-1` | the dossier records `pack_shape` from the fold's A/B picks (FWD-16's floor) | `0276f44fa6` | `f3b1a7405e` | proof VALID; AC1 `w1 pack_shape folders 96 pdf 48 docx 25 mixed 4 none 19 errors 0 sum_ok True control IMB_LN_Equity docx ADBE_US_Equity pdf AZN_LN_Equity pdf 6501_JP_Equity none`; AC2 `8 passed` |
| `TO-CRPS-w-3` | a cross-field unit-map discriminator that never guesses | `346d67244f` | `5dced3c458` | proof VALID; AC1 `w3 facts 9 of 9 answered resolved 8 unresolved 1 resolved_with_evidence 8 unresolved_with_reason 1 control SAP_GY_CURR_ENTP_VAL MILLIONS agrees True`; AC2 `24 passed`; the worker's mutant ("first hit, else MILLIONS") failed 2 tests |

**Merges.** Both were clean through `safe-merge.sh`. A peer's AMGT_HARVST merge held the shared index at 04:18Z; this seat waited
for it and did not touch it. w-3 appended one row (`Z-W2-S16`).

## 2. The one real run (`evidence/r21_real_run.txt`, CLOUD `5dced3c458`, 04:26:30Z)

- **w-1:** the census as above. The worker's `build()` test checks the source text only, so this seat called the real
  `build()` on three names (read-only; `build()` writes nothing). IMB `pack_shape docx` basis 1; ADBE `pdf` basis 1; 6501 `None`
  with `absent`.
- **w-3:** the nine facts with their evidence.

  | fact | result | cross-field ratio |
  |---|---|---|
  | 6501 SALES_REV_TURN | MILLIONS | 0.43 x market cap |
  | 8316 SALES_REV_TURN | MILLIONS | 0.39 |
  | 6501 CURR_ENTP_VAL | MILLIONS | 0.97 |
  | 9433 CURR_ENTP_VAL | MILLIONS | 1.36 |
  | 8035 CURR_ENTP_VAL | MILLIONS | 0.98 |
  | 8766 CURR_ENTP_VAL | MILLIONS | 0.88 |
  | 8316 NET_DEBT | MILLIONS | 1.13 |
  | 6501 BEST_SALES | MILLIONS | 0.48 |
  | TSM CURR_ENTP_VAL | UNRESOLVED | none: TWD fundamentals against a USD market cap, with no FX rate in the raw; not invented |

  In every resolved case, the ABSOLUTE hypothesis sits near 1e-6, which is in no band. The bands are asserted narrower than the
  1e6 gap.
- **Drain hygiene:** `py_compile` and ruff py39 clean; 155 passed (the research tests plus the dossier suites); the 3.9-floor
  census still reads 0 calls over 98 files.

## 3. The two served acts this round's cells make possible -- and what each still needs

1. **Serving `pack_shape` needs a `METHOD_VERSION` bump AND a dossier rewrite under a pair.**
   - This seat found a gap in its own cut. `dossier.write_one` writes nothing when the stored inputs equal the fresh ones and the
     method is unchanged, and `METHOD_VERSION` is still `amgt-corpus-dossier/4`. So `--write` today would serve no `pack_shape`.
     The bump is one line, inside this decomposition.
   - The expected-moves measurement for the pair's COO half (every name's served fields against `build()` now, read-only,
     `checks/round21/w1_expected_moves.py` -> `evidence/r21_w1_expected_moves.txt`) is running from HEAD `5b55a4ee1d` (started
     04:29:46Z). The COO half follows it; nothing is written before a signed pair.
2. **Writing the 8 resolved units into `field_map.json` needs a writer no cell built.**
   - `discriminate_facts` reads and reports; nothing applies its result to the map.
   - A hand edit of a served input is not this seat's act, so it is an enrichment candidate (s.6.1).
   - After it lands, the re-derive of the moved model blocks goes under a pair: 6501, 8316, 9433, 8035 and 8766. TSM does not
     move.

## 4. `w-2` -- BLOCKED on AMGT_RESAPP r51 `zz-1`, named

`lib/research/identity/crosswalk.py`'s newest commit is still `6a940b02b8`. Nothing is registered.

## 5. Rows -- dispositions for the L9

| row | state | note |
|---|---|---|
| `Z-W2-S16` (new) | INERT | (a) TSM: USD market cap vs TWD fundamentals, so no same-currency anchor; an ADR needs one (e.g. a TWD market cap or an FX field) before any read can decide. (b) `REVENUE_PER_SH` is unmeasured on 6501 and 8316 (2332 and 2687 exceed the 2000 per-share band), so the per-share x shares read is skipped there, and their SALES_REV_TURN resolves on the market-cap read alone. |
| `Z-W2-S15` | routed | to AMGT_RESAPP (round-20 ruling 2) |
| `Z-S63`, `Z-S66` | ARMED, carried | w-2 waits on AMGT_RESAPP r51 `zz-1` |
| `Z-S64` | carried | the migration item |

## 6. Enrichment candidates for the round-21 analysis

1. **An apply writer for discriminated units.** For example, `build_unit_map --apply-discriminated`, which writes each RESOLVED
   fact's per-security unit (and its now-classifiable sign) with the evidence as `derived_by`, never touching an UNRESOLVED
   fact. Then the unit-map commit, and the re-derive of the five moved blocks under a pair.
2. **The `pack_shape` rewrite:** the `METHOD_VERSION` bump plus the 95-name dossier rewrite, under the pair this seat is
   preparing (s.3.1). Then AMGT_RESAPP's pass-through serves it (round-20 ruling 3).
3. **TSM (and any ADR):** a same-currency anchor, or TSM stays UNRESOLVED by rule.
4. **`w-2`** carries on AMGT_RESAPP r51 `zz-1`.

## 7. Bounds and residue

- No served write, no S3 write, no `field_map.json` write and no vendor call this round.
- Drained worktrees `wk-crps21-1/2` were removed with their branches kept, under Andrew's 02:5xZ word (record `8c4f79e531`).
