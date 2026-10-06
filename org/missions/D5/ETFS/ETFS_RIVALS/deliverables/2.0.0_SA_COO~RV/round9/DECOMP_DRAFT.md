# ETFS_RIVALS round 9 -- DECOMPOSITION DRAFT (PREPARED, NOT ISSUED)

**Author:** `2.0.0_SA_COO~RV`, 2026-10-05 ~16:3xZ. **Status:** draft for the round-8 analysis. The issuance reads
`1.0.0_SA_CTO~Z`'s ROUND_ANALYSIS.round8.md enrichment list as its rectangle; this draft holds the cells already ruled.

## Ruled inputs

- Row Z-S29 + CTO~Z ruling (B), 2026-10-05 16:22Z: G5 rebuilds ONLY the named funds and carries every other fund's rows
  byte-equal; then D12 Step B runs. Proof: the per-date census reading 0 other-fund deltas. (A) refused.
- Same ruling: IDVZ/PFOE join the daily pull through a rivalfunds-owned gate file; no Positioning file is written or read
  differently (`integrations/bloomberg/` is under Andrew's no-modify order).
- CTO~Z msg 29624 term 4: security_universe gets its own invocation, built INCREMENTALLY (the prior universe plus that day's
  G1), never a 504-date rescan (the round-8 P1 timeout, 900 s / 1024 MB).
- Carried: ui-5 J1 NOT MET (CVO C-S28: 22 ticker-form names unchanged), enrichment item 3.

## Cells (3 on 3 chains, no edge between them)

### `RIV-nf-1` -- the trade schedule rebuilds only the named funds (Z-S29)
- Measured: `gold_trade_schedule.run_stage` builds one G5 object (and its G6) per report date from every fund's windows
  (`:933-970`); `hold_funds` leaves a fund OUT of the new object (`:95-101`), so it cannot keep a fund's prior rows.
- Interface: the stage event `rebuild_funds` (a list of tickers). With it, for each scope date the new G5 object is the
  newest prior G5 object's rows for every fund NOT named (byte-equal, row order kept) plus freshly inferred rows for the
  named funds; G6 likewise from the newest prior G6 object. A date with no prior object builds every fund as today.
  Without `rebuild_funds` nothing changes. The import batch carries it: `collector_bloomberg` import mode records
  `rebuild_funds` on its fetch-bloomberg marker when its event names them, and `sweep.run_gold_chain` passes the marker's
  value to the trade-schedule stage.
- Check: a fixture of two funds with a prior G5/G6 object, rebuilt with `rebuild_funds=['IDVZ']`: the other fund's rows equal
  the prior object's; IDVZ's rows are the fresh inference; control: without the key both funds are re-inferred.

### `RIV-gf-1` -- a rivalfunds-owned gate file for the Bloomberg leg gates
- Measured: `universe.d12_enabled()` reads only the process environment (`universe.py:36-37`); the vehicle sets no D12
  variable and its file `integrations/bloomberg/pipeline/scheduled_daily_pull.cmd` may not be edited.
- Interface: `data/etfs/scripts/rivalfunds/leg_gates.json` ({"RIVALFUNDS_LEG_D12": "0"|"1", ...}); a gate reads `"1"` when
  the environment says `"1"` OR the file says `"1"`; the environment can never turn a file `"1"` off (one direction, so a
  Lambda and the vehicle agree). The file ships with every gate `"0"`; flipping D12 is a one-line commit under its pair.
- Check: env unset + file D12 "1" -> `d12_enabled()` True and IDVZ reads bloomberg_primary; file "0" + env unset -> False
  (control); env "1" + file "0" -> True.

### `RIV-su-2` -- security_universe as its own incremental invocation
- Measured: round 8's `gold_security_universe.handler_entry` rescans 3 years of G1 (504 report dates) and ran the publish
  Lambda into its 900 s timeout at 1024/1024 MB (deploy addendum 1); the publish-path call is removed (b166e04416).
- Interface: `handler_entry({"date", "sink", "mode": "incremental"|"seed"})`: `incremental` reads the newest prior
  universe object and the G1 of the as-of date only, and writes the merged list; `seed` builds from scratch in bounded
  date chunks with a cursor (the canonical stage's `_budget_s` pattern). An `only:["build-security-universe"]` stage runs
  it, and the 09:00 sweep runs it after publish-page.
- Check: a prior universe + one new G1 date -> the new object adds the new securities, keeps first_seen of the old ones,
  advances last_seen; it reads exactly 1 G1 object (counted); control: `seed` over 3 dates equals the incremental result.

## Round-8 analysis (CTO~Z msg 29706, 16:42Z; file lands after PARITY CLOSED): 8 items

1. G5 named-fund rebuild, then Step B under its pair -> `RIV-nf-1` (above).
2. The IDVZ/PFOE gate file -> `RIV-gf-1` (above).
3. security_universe incremental -> `RIV-su-2` (above).
4. C-S35, AI-text links within the 2 MB cap -> `RIV-ln-1`. Measured on the captured 10-05 render context: 428 of 860 page
   names are carried by more than one KEY FORM of a security (CUSIP, `ENEL_IM_Equity`, `ENEL IM Equity`), and
   `render._render_page` keeps a name only when ONE key carries it (render.py:1769) -- every such name renders plain
   ('Enel SpA' 3 keys: plain; 'E.On Se' 1 key: linked). Check ln-1.AC1 base: FAIL as expected ((a) FAIL, control PASS).
5. C-S36, the 22 ticker-form names -> `RIV-nm-3`, chained after item 6. Measured: 135 keys in the 10-05 name map carry a
   ticker-form name; 0 sit in any fund's latest holdings (they are past holdings the trade log and rankings still show);
   128 were never in any G4 date and 7 are in G4 with no name. G4 enrichment asks only for current holdings, so the cause is
   the name map's KEY SPACE, not today's capacity block. Remedy: one bounded name pull (LONG_COMP_NAME) for the page keys
   with no name, inside item 6's budget, persisted so it is asked once.
6. S24, a measured capacity budget, no backfill until it exists -> `RIV-cb-1`.
7. Classify the G5 history drift (176 dates), read only, no replay -> `RIV-gd-1` (LOCAL; a report from a script).
8. Triage the 8 stale OPEN rows -> issuer act, not a cell.

## Not cells

- D12 Step B (the import) is an act after `RIV-nf-1` deploys, under its own pair; its proof is the per-date census.
- The live G5 history differing from current code on 176 dates: CTO~Z's round-8 analysis question, not an act now.
