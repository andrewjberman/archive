# ETFS_RIVALS round-8 L5 prep (2.0.0_SA_COO~RV), measured 2026-10-03 ~00:4x-01:0xZ, base CLOUD 75ad1e4d2e (= deployed pin)

The round-7 analysis (115645c4b4, section 3) rules that the ONE round-8 issuance is cut after the 2026-10-05 grades
(sa-1 J1, ui-5). These notes are the cells' WHAT YOU NEED TO KNOW, measured early.

## Item 1 -- W1-S46: the deadline-aware vendor timeout (CTO ruling 1)

- Today, the AI deadline is min(sweep.AI_DEADLINE_S 600 s, remaining - MARGIN_MS 150 s) (`sweep._ai_deadline_s`).
- `ai_stage._DeadlineClient` checks the deadline only BEFORE a call starts and AFTER it returns (Overrun is a BaseException).
- The call itself runs to `ai_client.TIMEOUT_S = 120` (`ai_client.py:22`, passed as `timeout=TIMEOUT_S` at `:37`).
- So the worst case is a call that starts at deadline-epsilon and ends 120 s later. That leaves 150 - 120 = 30 s for the
  republish.
- Republish cost, measured (CloudWatch REPORT, 14 days):
  - `rivalfunds-publish-page-lambda` n=29: p50 6.1 s, p90 8.3 s, p95 68.1 s, max 81.2 s;
  - the round-7 act-3 publish with refresh_a1 (daily Lambda, RequestId 480d8720): 117.5 s;
  - the CVO's measure: ~88 s.
- So the reserve must cover at least ~120 s (inferred: the in-sweep republish carries no refresh_a1, but its upper bound is
  the measured 117.5 s).
- Write set: `ai_client.py` (accepts a per-call timeout), `ai_stage.py` (the wrapper passes min(TIMEOUT_S, end - now)), and
  `sweep.py` (a REPUBLISH_RESERVE_S that the deadline subtracts).
- The plant for the check: a stub vendor that blocks until the timeout it is handed, and a context with little time
  remaining. Expected: the call gets timeout <= remaining - reserve, the AI step is FAILED with a deadline reason, the
  republish runs and publishes, and the total stays under the remaining time.

## Item 2 -- the 3 money-market keys in reader words (CVO P2)

- They are visible on the face only inside the STORED AI account prose (`rf-lead` paragraphs and the account text):
  - TSEL: "outside DGCXX_US_Equity";
  - PCLG: "moving cash-like DGCXX_US_Equity";
  - ETFT: "added IJGXX_US_Equity".
  The CVO counted these 3.
- The census's collapsed `<details>` missing-lists also carry underscore keys (NOW_US_Equity, 3491_TT_Equity, ...). That is
  not on the face, and it is a separate question for the register measure.
- The cause is inferred: the AI chain's cited rows carry the key where display_name has no readable name (cash-like lines
  with no G1 name), and the model writes the key it was given.
- The cell (render.py): substitute a whole stored key in AI prose with the page's one name for that key, falling back to a
  reader form for a cash-like line ("DGCXX money market fund"). Keep the key in a title. The stored account text is never
  rewritten.
- The 2026-10-05 G4 LONG_COMP_NAME may name DGCXX and IJGXX upstream. That is to be read Monday, before the cut.

## Repair cell (one cell, batched)

- Z-S16 is DISMISSED by the CVO (C-S26): it omits the claim rather than misstating it. NOT in the repair cell.
- Z-S17 is RETRACTED (row Z-S19). The 0 -> 0 exit row is CRO CALL 12's ratified contract: G5 keeps it and the page hides
  and counts it. Round 6's x-1.AC3 pins it. It is NOT in the repair cell.
- Z-S18: the census's holding-implied lookup is keyed in the wrong space. In gold_input_census.py, look the books up by the
  row's G1 key while the subject stays the rankings' key.
- D10: the G5 replay. No deployed route rebuilds G5: ONLY_STAGES excludes it, and run_gold_chain is idempotent per batch.
  Either a replay route in a cell, or the rows roll off around 10-08.

## Item 4 -- the walk-register remainder

- Being measured: C:/tmp/r8prep/register_r7.json (33 items vs rv-publish-1002r7).

## Item 4 -- the walk register, MEASURED (register_r7.json, rendered headless Chromium, 13 funds x 3 periods, visible only)

17 REALIZED, 8 PARTIAL, 6 NOT_REALIZED and 2 NOT_MEASURABLE_NOW, against rv-publish-1002r7 with rv-publish-1002r6 as the
control.

- **render.py, one write set:**
  - U07: the trend caption trimmed to dates and trading days;
  - U12: empty windows carrying a money-market note collapsed (4 runs, 12 windows);
  - U18: BASG's direction-verdict opening capped at 2 sentences;
  - U14: names in the AI prose mapped to the page's one display name (13 clashes in the opening lines, 26 in full text).
    This is the SAME mechanism as item 2's money-market keys.
  - The audit trail's data-status tables still show 56 internal code words (left out of rd-1 by its cut).
- **gold_input_census.py (goes into the rp-1 repair cell, same file as Z-S18):** the 44 "missing" price rows carry the
  reason "the rankings price it from the fund's own reported valuation" (`:183`), which contradicts "missing".
- **Superseded, no code:** U02 (default YTD) and U08 (audit split across two controls) conflict with Andrew's later layout
  word (~17:0xZ 10-02, record
  `org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20261002_17xxZ_RIVALFUNDS_LAYOUT_WALK_AND_BUILD.md`). The
  decomposition records them as superseded.
- **Data / issuer acts:**
  - D10: the G5 replay (6 n/a cells, rolling off around 10-08);
  - D12: I-2, the IDVZ/PFOE trend backfill.
- **Event-gated on the 2026-10-05 vehicle:** D04 (G4 at 601 securities), D05 (211 ticker names), D06 fixes 2-3, D11 (the
  30-character cuts).
- D13 needs the v0.8 leg (ACWI/IWM; the row cost is measured by the scripted vehicle).
- D07 is upstream (TrueShares, Bloomberg T-2). Naming late funds with a reason would be a census/render change.
- NOT_MEASURABLE_NOW: D08 (the scheduled account, 10-05) and U19 (Andrew's signed-in walk).
