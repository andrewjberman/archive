# NEVER-WIDEN -- COO HALF: ETFS_RIVALS pk-1 + al-1 -- deploy the five rivalfunds Lambdas at CLOUD 92cf1f322b (ADDENDUM 5 item 2)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~19:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** ROUND_ANALYSIS.round10.md ADDENDUM 5 @a8fb9c1df1: the reader alignment first (RIV-al-1, drained 2d78ef2151: 22 of 22
identity call sites pass the parsekey; one key across rankings, trend, census on the two-listing plant), then ONE deploy pair for
pk-1 + al-1 with the ADDENDUM 1 census riding it. Package suite at the pin's code: 768 passed, 2 skipped, 0 failed.
**Timing:** before 2026-10-07 07:00 ET. The vehicle's market pull writes the first `security_parsekey` values into G4 at 07:00 ET
(eb-1 + pk-1 ride the CLOUD working tree), and the 07:00 ET marker publish (this Lambda code) is the first reader of them.

## VERDICT: SIGNED

Conditions: the pin is CLOUD 92cf1f322b; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (50a2248fe9, deployed 17:31Z, ledger etfs-rivalfunds-round12)

Measured: `git diff 50a2248fe9 92cf1f322b` over what `rivalfunds_package.py` stages:
- `gold_holding_contribution.py`, `gold_trade_schedule.py` -- RIV-pk-1 (the parsekey join; `GOLD_VERSION` gold_trade_schedule/2 -> /3);
- `gold_buying_trend.py`, `gold_input_census.py`, `sweep.py` -- RIV-al-1 (the three readers pass the parsekey);
- `enrichment_bloomberg.py` -- eb-1 + pk-1's request side: runs on the vehicle, not in a Lambda path that calls Bloomberg;
- `lib/trading_calendar.py` -- NFRA_MCPINDEX MX-f-1: two NEW functions (`_to_weekday`, `weekly_production_day`), 0 lines removed;
- `infra/logic/registry/` -- a new `commonwealth` VENDOR row and one IRPT_YCDGEN policy state flip; `homes.page(...)` and every
  rivalfunds address resolve unchanged (read at the pin).
NOT carried: round 13's RIV-fe-1 / RIV-lk-1 (in flight on their branch) -- their own pair later.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-pk1-al1`).
2. **`safe-apply` of `C:/tmp/rv_apply13.tfplan`** from `C:/tmp/rv-r8` detached at 92cf1f322b after `rivalfunds_package.py`
   (plan text `C:/tmp/rv_plan13.txt`, copied beside this half): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` +
   `last_modified` only. Before = the round-12 set (daily vOcweDKE, fetch NJEhVOcs, canonical S5Q1EsSv, silver 4cA4RBMy, publish
   r+H1xDcI) -- live, read by the plan; after = daily NLWa+glx, fetch pzoscnfB, canonical pX4xe2wJ, silver hJ/zqsdO, publish
   B5srwuWE. No environment change.
3. **No republish.** Nothing on the 10-06 page changes until G4 carries parsekeys: live G4 has no `security_parsekey` column today,
   so every reader's parsekey map is empty and its keys equal today's (al-1.AC2's control arm; pk-1's "no parsekey -> own key").

## EXPECTED OUTCOME -- BOTH BRANCHES OF THE PRODUCERS' RULES

- **Tonight (no parsekey in G4):** holding_contribution, buying_trend, input_census and the hold gate resolve exactly today's keys.
  G5: the batch chain's G5 step on a date it rebuilds writes a NEW `-v<NN>` revision stamped gold_trade_schedule/3 (gt-1's rule: a
  different producer_version is a new revision), with today's rows; a date it does not touch keeps its object.
- **From 2026-10-07 07:00 ET (G4 with parsekeys):** a CUSIP/ISIN-keyed holding takes the Bloomberg key another fund's row carries
  in the window (Nebius: GQGU N97284108 -> NBIS_US_Equity), in the rankings, the trend, the census, G5 and the hold gate alike.
- **The ADDENDUM 1 census rides this pair as the post-act read:** after the 07:00 ET vehicle run, every (CUSIP/ISIN key, Bloomberg
  key) pair the join merges across all funds, with a count, from the first G4 carrying parsekeys; a merged pair that is not one
  security is the failure arm (stop, roll back, row). The added PARSEKYABLE_DES points of that run are read from its result.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 50a2248fe9 set (live) | the 92cf1f322b set | a saved plan from a detached worktree at 50a2248fe9 after `rivalfunds_package.py`, `safe-apply` |
| gold/trade_schedule (+ G6 flow_reconciliation following it) dates the batch chain rebuilds | newest -v<NN> at gold_trade_schedule/2 | a new -v<NN+1> at /3, same rows tonight | the code rollback; superseded revisions stay (never overwritten) |
| gold A1 tables (holding_contribution, buying_trend, input_census) from the 2026-10-07 marker publish | CUSIP-keyed rows for CUSIP-only holdings | merged under the Bloomberg key when a parsekey joins | the code rollback + one refresh publish |
| platinum/page from 2026-10-07 | one security can show twice (Nebius) | shown once | as above |

Not in this act: round 13 main (gw-1 gateway release, fe-1, lk-1) -- their own pair(s).
