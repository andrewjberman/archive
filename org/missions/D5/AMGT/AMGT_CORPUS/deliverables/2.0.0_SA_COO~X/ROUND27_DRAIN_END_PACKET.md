# AMGT_CORPUS round 27 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X` (re-seated 2026-10-01 ~04:4xZ by `0.0.0_AB_MSTR~Z` on `1.0.0_SA_CTO~Z` msg 27498; placement
`CTO_PLACEMENT_20261001_043xZ_AMGT_FRIDAY_DEMO_RESTRUCTURE.md` section 3 step 1). **Decomposition:** v27.0 @`0e025b7beb`.
**Source:** round-26 analysis @`3a758833b7`.

## 1. The cells

| cell | `<risk>` | state | evidence |
|---|---|---|---|
| `CRPS-ac-1` ZERO-DOMINATED unit class | LOCAL | complete, merged `3a7cf75c4f` | AC1 `ac1 bbse3_unit ZERO-DOMINATED bbse3_count 6 of 10 keys 100 other_unit_changes 0 bands_unchanged True`; AC2 64 passed; pins read by content |
| `CRPS-ac-2` BBSE3 paired re-derive | WORLD | DONE, ledger `amgt-corpus-r27-ac2` CLOSED (5 legs) | section 2 |
| `CRPS-ac-3` owner rows for 2 base test failures | LOCAL | DONE at the cut | rows `Z-S72`, `Z-S73` @`32894174c0` |

**Ruling at the drain:** row `Z-W1-S25` (the worker's dividend exemption set `ZERO_DOMINATED_EXEMPT`) ruled **ACCEPT** as built,
TO-CRPS-ac-1 AMENDMENT 1 @`b239301bb1`. Without it the literal rule moves 334 dividend figures and breaks the round-26 dividend-yield
test.

## 2. The WORLD act ac-2 -- ledger `amgt-corpus-r27-ac2` (pair COO `e4b31a6f28` / CTO `3e49e4a8dc`)

The serializing dry run over **every one of 100 keys** (`checks/round27/ac2_dryrun.py`) predicted:
`ac2 keys 100 move_blocks 1 map_entries 1 unit 10 sign 10 currency 0 value 0 case_blocks 0 top 0 other 0 errors 0`. The act's
after-state equals it.

| leg | result | sentinel commit |
|---|---|---|
| gate | own call: 0 producer diff since `b239301bb1`; map == committed bytes; an untracked peer file (`lib/research/coverage/covered_universe.py`) is outside the import closure | `0e41f14441` (open) |
| a | 1 entry, BBSE3 `CAPITAL_EXPEND` texts only; the rebuilt map is byte-identical to a temp-map rebuild by the dry run's method (sha256 `2b1b5836...279f`) | `767b4e8c50` |
| b | map `767b4e8c50` | `639e486f68` |
| c | stamp `20261001T051828Z` equals its captured block (vintage stripped); 0 value, 0 case-value moves; exactly 1 new block object in S3 | `f19588c754` |
| d | one new BBSE3 dossier, 0 other names; changed keys `fields.model_rows`, `inputs`, `content_sha256`, `as_of`; `inputs_equal_now` 1/1 | `2f1cfcbff1` |
| v | over the newest block of 100 keys (37,746 figures): **UNRESOLVED 1, ZERO-DOMINATED 10**. Negative arms (CTO condition): TSM `CURR_ENTP_VAL` stays UNRESOLVED; BA `EQY_DPS` (newest stamp 09-30, not re-derived) keeps PER SHARE | this commit (close) |

**Ruling 2 held:** the sentinel was committed after every leg close; no leg close was lost this round.

**The served effect.** Over 100 keys, units that are not measured stay at 11, now in two named classes: UNRESOLVED 11 -> 1 and
ZERO-DOMINATED 0 -> 10. **Neither class is measured.** BBSE3's capital expenditure now says why it has no magnitude (6 of its 10 fiscal
years are exactly zero) instead of an unresolved sampling note. Its values and its UNRESOLVED sign are byte-unchanged.

## 3. Rows filed this round

| row | class | what |
|---|---|---|
| `Z-S74` | OBSERVATION, INERT | `provenance/validate.py:32` and `render_print.py:208` classify units on the retired `SEE field_map.json` prefix, so `UNRESOLVED-ON-...` and `ZERO-DOMINATED...` units read MEASURED there. Off the served path (`scoped_amgt.py:1261` imports only the overlay functions); ac-2 did not move it. A candidate enrichment item |
| `Z-W1-S25` | OBSERVATION | ruled ACCEPT (above) |

## 4. One instrument note
A first commit of leg b was refused because a peer's drain merge was in progress in the shared tree (`.git/MERGE_HEAD`, gone by
05:13Z). The retry landed; nothing of the peer's was touched.

## 5. Judgment criteria for L9
None. Round 27 carried only mechanical criteria (ac-1) and a paired served act graded on its own after-reads.

**Next, outside this round:** round 28, the Friday round (PRD v0.7 Addendum B: FWD-12 amended, FWD-20, FWD-21), cut by this seat
now in ONE issuance per placement section 3 step 3 (the addendum is SIGNED: CVO~Z @`089a39f74c`). It does not wait on the round-27
analysis.
