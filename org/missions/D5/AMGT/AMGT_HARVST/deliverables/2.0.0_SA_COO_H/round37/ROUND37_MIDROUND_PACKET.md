# AMGT_HARVST round 37 -- mid-round packet (L8 input, partial) -- `2.0.0_SA_COO~H`, 2026-10-02 ~07:2xZ

Round-36 analysis @e38e50aa55 -> issuance @f45007adc7 (decomposition section 50). Three of the four cells are done.
aj-4 is STAGED on Andrew's hand-solved ft sign-in (card to `0.0.0_AB_MSTR~Z`, 07:06Z), so this packet is partial.
The drain-end packet follows when aj-4 is terminal.

| cell | result | evidence |
|---|---|---|
| `HVST-aj-1` grader (~90) | Bands anchor on the presentation: `challenge_presented` from the transport when a record carries it, else the http-ledger 403 inside the run span (row Z-W90-S12). `requests` are counted inside the monitor windows only, and 0 windowed requests reads NOT_EVALUATED. | merge @fdd7442696; `aj-1.AC2.output.txt` PASS on round 36's pinned windows: bbg 9 non-void / 9 passed (18 void, 27 presented), barrons NOT_EVALUATED (0) |
| `HVST-aj-2` monitor (issuer act) | Window2 preserved; window3 open from 06:52:23Z (pid 22892); stays up for the life of FWD-11 | `aj-2.AC2.output.txt` PASS (+545 s across 600 s) |
| `HVST-aj-3` barrons (issuer act) | Ordinary barrons backfill from 07:05:45Z (pid 30424) inside window3; job 1 stored 3 new; nothing provoked | `aj-3.AC2.output.txt` PASS: 24 windowed requests, 0 presented, MET-BY-ABSENCE |
| `HVST-aj-4` ft keep-alive | STAGED (Andrew) | `aj-4.AC2.py` FAIL at the base (no record) |

**For your grade of limb 2a.** These are the grader's verdicts at 07:17Z; this seat does not grade them.
- Round 36's windows: bbg MET; wsj, ft and sa MET-BY-ABSENCE; barrons NOT_EVALUATED.
- Live windows: barrons MET-BY-ABSENCE on 24 monitored requests.
- To re-run over all three windows: `python -m lib.opal_data_harvest.load_window_grade --json`.

Limb 2b stays open (ruling 4, no provoked challenge). ft limb (1) is aj-4.
