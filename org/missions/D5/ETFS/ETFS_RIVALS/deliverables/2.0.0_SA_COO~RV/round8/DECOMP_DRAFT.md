# ETFS_RIVALS -- ROUND 8 DECOMPOSITION, DRAFT (not issued; the ONE issuance follows the 2026-10-05 grades)

```json
{
 "project": "ETFS_RIVALS",
 "round": 8,
 "status": "DRAFT",
 "analysis_ref": "org/missions/D5/ETFS/ETFS_RIVALS/ledger/ROUND_ANALYSIS.round7.md@115645c4b4 (section 3)",
 "register_ref": "org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~RV/round8/register_r7.json",
 "base_measured": "CLOUD 75ad1e4d2e (= the deployed pin)",
 "author": "2.0.0_SA_COO~RV",
 "cells_drafted": 4,
 "open_slot": "item 3 -- what the 2026-10-05 grades (sa-1 J1, ui-5) leave open"
}
```

**Why a draft.** The round-7 analysis (115645c4b4, section 3) rules that round 8 is cut after Monday's grades. Its item 3
does not exist until then, and a round gets ONE issuance. Everything measurable now was measured at the deployed pin, and
its checks are dry-run on this branch.

## Rulings at the cut (the issuer's, inside its decomposition)

1. **U02 and U08 are SUPERSEDED, with no cell.** Both conflict with Andrew's later layout word (~17:0xZ 2026-10-02:
   default YTD; "popup modal for full detail and citations"), record
   `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261002_17xxZ_RIVALFUNDS_LAYOUT_WALK_AND_BUILD.md`.
2. **Z-S16 is not cut.** The CVO dismissed it (C-S26, ADJUDICATION_v7.Z): a skipped step omits run_path, and no stored
   value is wrong.
3. **Z-S17 is not cut.** It is retracted by Z-S19: the 0 -> 0 G5 exit row is CRO CALL 12's ratified contract, and
   x-1.AC3 pins it.
4. **D10 (6 n/a exit cells) is not cut. Recommended: let them roll off around 2026-10-08.**
   - The cause is the 09-30 trims-to-zero, built before x-1. A G5 rebuild at the deployed code prices them (measured
     locally: C:/tmp/r7measure/g5pin).
   - No deployed route rebuilds G5: ONLY_STAGES excludes it, and run_gold_chain is idempotent per batch. A replay route
     is new code whose benefit lasts about 2 trading days once deployed.
   - The ad-hoc local gold write is QA-only and never production evidence.
   - The decision is the issuer's. If Monday's grades raise it, a replay-route cell joins the repair chain.
5. **D07 is upstream** (TrueShares layout, Bloomberg T-2). It is out of the rectangle, and naming late funds with a reason
   is a later census/render cell if asked.
6. **Event-gated, read Monday before the cut:** D04 (G4 at 601 securities), D05 (211 ticker names), D06 fixes 2-3 and
   D11 (the 30-character cuts) all depend on the 2026-10-05 vehicle run. Whatever stays open joins item 3.
7. **I-2 (D12, D13) needs a cell first, then issuer data acts.**
   - Andrew-direct ~20:3xZ 2026-10-03 un-parked it (card 6, @9fe6e6f111).
   - The scripted cost measurement for 2026-10-01 gave IDVZ 45 / PFOE 24 / ACWI 2,198 / IWM 1,979 rows (row Z-S20).
   - The leg's single per-date query caps at 2,000 rows and crashes the whole leg on overflow, and the gate is
     all-or-nothing. So the cell `RIV-lg-1` (below) lands before any gate flip or backfill.
   - Then the issuer's acts, each under its own pair:
     - the D12 gate and the IDVZ/PFOE backfill to inception;
     - the D13 gate and the controls' backfill from 2026-01-02. That is ~800k rows, and its budget threshold is named in
       the pair, because READ_HERE defines none.
     - the replay and the page measure, since about 4,200 more lines a day pass through G1/A1, and the page sits at 1.89 of
       2.10 MB.

## Cells and chains (cut by write set)

| chain | cells | writes | risk |
|---|---|---|---|
| `~1` | dt-1 | `ai_client.py`, `ai_stage.py`, `sweep.py` | SERVED |
| `~2` | an-1 -> rw-1 | `render.py` | SERVED |
| `~3` | rp-1 | `gold_input_census.py` | SERVED |
| `~4` | lg-1 | `collector_bloomberg.py`, `universe.py` | WORLD (the vehicle runs the CLOUD tree) |
| `~5..` | item 3 cells | after the grades | -- |

### `RIV-dt-1`: the deadline-aware vendor timeout (W1-S46, CTO ruling 1, item 1)

- The worst case today: a call starting at the deadline runs `ai_client.TIMEOUT_S` = 120 s, which leaves 30 s of the
  150 s margin for a republish.
- Republish measured: the publish-page Lambda over 14 days, n=29: p95 68.1 s, max 81.2 s. The act-3 publish with
  refresh_a1 took 117.5 s. The CVO measured ~88 s.
- Interface:
  - `chat(timeout=)`;
  - `_DeadlineClient` hands each call min(TIMEOUT_S, the time left);
  - `sweep.REPUBLISH_RESERVE_S` >= 88 s, subtracted from the remaining time.
- Check: `dt-1.AC1`, base FAIL 4. The fix PASSES, and the no-reserve and no-timeout mutants fail their own limbs.
- Organic trigger: the 09:00 ET sweep. A planted slow vendor still republishes.

### `RIV-an-1`: the AI prose reads each security under the page's one name (item 2 + U14's AI-text residue)

- The 3 money-market keys (DGCXX x2, IJGXX) sit in the stored prose. There are 13 casing clashes in the opening lines and
  26 in the full text.
- Interface: `render._rich` maps whole security keys and casing variants to `_NAMES`; a cash-like key reads
  "<TICKER> money market fund"; the original goes in a title; the stored row is unchanged. The `.rf-cite` citation list
  keeps its keys.
- Check: `an-1.AC1`, base FAIL 3. The clean fix PASSES; the leaky mutant fails (b) and (e).

### `RIV-rw-1`: the render remainder (U07, U12, U18)

- `rw-1.AC1` (U07): the trend caption reads the dates and trading days only, and the unit moves off it. Base FAIL 2.
- `rw-1.AC2` (U12): noted 0-trade windows collapse, with the notes kept inside. Base FAIL 2.
- `rw-1.AC3` (U18): an all-caps "CORP." ends a sentence, so the lead is two sentences. Base FAIL 1.
- Every control PASSES at base, and all PASS under the fix.
- Candidate fourth item if sized in: the audit trail's 56 code words. It needs its own check, and a fourth criterion
  carries a reason.

### `RIV-lg-1`: the Bloomberg leg carries index-control-sized holdings and switches D12 and D13 apart (row Z-S20)

- Measured: 4,246 rows for one date across the four new names. The cap is 2,000 per multi-fund query, and an overflow
  raises an uncaught RuntimeError, which crashes the leg.
- Interface (to fix at the cut):
  - an index control is queried on its own per date, with a cap sized from the measurement (>= 2,500 with headroom), and
    the range read never truncates silently;
  - an overflow is a per-name partial, never a leg crash;
  - `universe` splits the gate so the home funds (D12) and the controls (D13) switch independently.
- Organic trigger: the vehicle's 07:00 ET leg. The check plants a 2,300-row control beside the existing funds offline.
- Check: to be written at the cut, dry-run at base (it must FAIL: today's overflow is a crash).

### `RIV-rp-1`: the census repair (Z-S18 + the contradictory miss reason)

- `rp-1.AC1` (Z-S18): `alias` comes from the wide g1w and `books` from the 14-day g1, so a CUSIP resolved only in an older
  report misses its holding-implied price. Base FAIL 1; the fix PASSES.
- `rp-1.AC2`: a missing price never claims the rankings price it (`:183`, 44 served rows). Base FAIL 1; the fix PASSES.

## Monday, before the cut

Both reads have named owners and times (ROUND_ANALYSIS.round7.md ruling 2): the vehicle at 07:00 / 08:03 ET, and the sweep
at 09:00 ET. The cut reads both, adds the item-3 cells, re-runs every check above at the then-current base, and issues ONCE.
