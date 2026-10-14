# Handoff -- 2.0.0_SA_COO~M1 (dell1), MDPF_SECCLASS, written 2026-10-14 ~14:5xZ, before the 21:00Z dell1 restart

Re-seat: `/watcher`, then `/canonical-drive MDPF_SECCLASS` is the live arm (org/ref/LIVE_ARMS.md, DIRECTED, 60m; a session cron `37 * * * *` dies with the session, so re-arm it). Lease FULL. Read STATUS.md first:
`org/missions/D8/MDPF/MDPF_SECCLASS/STATUS.md` (section "Next, in order", items 0 and 1).

## State (measured unless marked)

- **Round 24 closed to the CVO** (packet `org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/L8_DRAIN_END_PACKET_R24_20261014.md`, CVO ADJUDICATION_v23 and v24). **FWD-1 is REALIZED WHOLE** (CVO D1-C-S25). The other 16 FWDs are at their last recorded states (the board in the packet, all older than round 20).
- **Round 25 is EXECUTING** (issued `3e1365fdaa`, `fanout: 2 of 2`). Both cells are DRAINED and verified at trunk: SC-e-101 `b5f6b816a4` (re-based read `R25_CHECKS/r25_rebase_read.py` plus baseline `R25_CHECKS/baseline/REBASE_BASELINE_20261014.json`, captured 12:33Z), SC-e-102 `ee2cbf1023` (C_06 `sort_keys=True`). Worktrees and branches removed.
- **D1-W83-S5 is DISARMED** (row D1-S38, XA-a304). Open under me: **D1-W92-S2 ARMED** (D_03 republishes the firm and 56 advisor daily files in insertion order; the sorted-keys pair names them).
- No deploy ledger is open on this project (the e91, e97 and leg Q ledgers are CLOSED).

## What is owed, in order

1. **Tonight's 23:00Z scheduled fire (2026-10-14), chain end about 01:15Z Oct 15.** Read it: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R25_CHECKS/r25_rebase_read.py read --baseline org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R25_CHECKS/baseline/REBASE_BASELINE_20261014.json`
   (prints `R25-C` lines and `R25-REBASE ok=...`; the baseline is from the served objects BEFORE this fire, so `moved>0` and `dropped_from_window>0` are expected, the window rolls). Read the chain's stop first (runner stopped, no `gold/trigger-pending.json`).
   The D1-S27 bound is clause `s27` (at most $1,000 per firm date; the baseline read was max 165.09). Record the read in a deliverable beside the baseline and in STATUS.
2. **Sign the COO half** of the SC-e-102 pair: `NEVER_WIDEN_COO_HALF_SECCLASS_C06_SORTED_KEYS_20261014.md` (write it; model: `NEVER_WIDEN_COO_HALF_SECCLASS_C06_RETAINED_UNCLASSIFIED_20261012.md`). The CTO half is SIGNED @29827be5eb (C1: Branch 1's run is C_06 alone outside a fire window, restore target = the VersionId read IMMEDIATELY before it; C2: after the 21:00Z restart).
   Request: `NEVER_WIDEN_HALF_REQUEST_SECCLASS_C06_SORTED_KEYS_20261014.md`.
3. **Send SC1 the GO** for the STAGED order `org/tier2_senior/0.7.0_AE_CloudOps~SC1/task_orders/MDPF_SECCLASS.TO-SC-e102b.c06-sorted-keys-ship.md` (the message cites that path; hold: COO half signed, the 23:00Z fire read, the restart done, runner idle, finish 90 minutes before the next fire). SC1 is a live seat on dell1. Its check: `R25_CHECKS/e102_shipped_check.py` (`ok=False` at the base).
4. **Round-25 close:** `python .tools/round-close-check.py --project MDPF_SECCLASS --round 25`, `dep_stage` EXECUTING -> ROUND_CLOSE, L8 packet (cells, the re-base read, Branch 1 and leg G of the ship, the Positioning limb and FWD-1 already graded, W92-S2 disposed by the pair), send to `3.0.0_SA_CVO`.
5. **Leg G of the ship** is mine on the first scheduled fire after it (D_03 families and D_04's mix_summary: canonical-JSON equality on dates the fire did not re-derive; D_04 total within $0.000001).

## Carried

- **e57e61** (`TO-DEPLOY-e57e61`): L3 HELD. The 10-14 14:00Z run planned 0 US stocks (STATUS states the input condition). If no scheduled run plans one by the 10-20 14:00Z run, cut the seeded exercise as a round-26 item (CTO msg 5510).
- **Round 26 (after the CTO's round-25 analysis):** the 4 seed rows HPI, CUBE, GLPI, PCEF (this project is the list's writer, PRD C-WRITER; CTO msg 5510) under a never-widen pair; the DEMQUE<->SECCLASS sync cell (arrives with the CTO's CONTRACTS rows: classify the 23 of 131 landed DEMQUE fund names with no `etf-classifications` row on the scheduled path and prove one; state how a CUSIP-only security keys into a ticker-hashed table).
- **Andrew's:** the client-facing Black Diamond Mix restated-history PROD push (card names the AUA restatement +249..+263 and -30,914.72 on 10-09). Nothing else is reserved.
- Law change today (CLAUDE.md Portal): portal DEV is written only by `.tools/portal-merge-forward.sh`; no seat of mine does portal work.

## Hazards learned

- Time: `date -u` is authoritative; git log times print local (EDT, UTC-4).
- Never run `ui_walker_account.py secret`; `/ui-walk` arms and disarms itself (verify `DISARM ... REFUSED` after every run). Positioning walks need `--press "Satellites"` etc.; the Models table is cut by an inner scroll in the capture.
- A worker's order is the grant (`<paths>`); a seat-folder order to SC1 needs its own `<paths>` block naming the ledger and sentinel.
- `safe-commit.sh -F` with a message file written by the Write tool; add the `Co-Authored-By` trailer line.
- Leg Q lesson: list SC1's earlier SSM commands filtered by time before concluding a run "did not start"; my 11:14Z nudge said so wrongly.
- The inbox watcher expires every 30 minutes: re-arm on the `[WATCHER-EXPIRED]` notice the same turn.

## Added 2026-10-14 ~18:1xZ -- Andrew's four priorities (MSTR~DELL1 relay msg 5662 of laptop CTO msg 109202; no ruling of mine)

P2 Ticket Center (analysis request, trade, meeting channels) by Oct 24; P1 Investor Reporting by Nov 15; P3 Advisor Intelligence before Dec 1; P4 OPLGTW/MCPINDEX secondary. "Every other project is secondary to these three." **No box moves until Andrew answers;** the box-level directive "reaches you at the next box pass" (records `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261014_173xZ_DELIVERABLES_FOUR_PRIORITIES_AND_DATES.md` @3d904f51cd and `PLAN_20261014_DELIVERABLES_BOX_ORGANIZATION.md`, CLOUD 5ad9a6e07f). MDPF_SECCLASS is not named; its BD Mix data thread feeds Advisor Intelligence pages. Do not narrow, park or extend the project on this relay: wait for the box-pass directive, then follow it verbatim. Until then the live arm and the owed acts above stand.
