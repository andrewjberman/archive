# AMGT_RESAPP round 124 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO~DELL1` and `1.0.0_SA_CTO~DELL1`

**STATE: FINAL, 2026-10-19 ~21:5xZ, sent as the L10 slug. Every task order of the round is terminal (SC1 closed the cf-4 ledger `amgt-resapp-r124-cf4-not-available-words-redeploy-dell1` at `06e2549cc7`, 8 legs proven; I flipped cf-4 to complete); sections 1 to 3 are measured. No row graduated; I have not graded the judgment items myself.** Push state of every commit named: LOCAL on box/dell1, unread.

Round 124 is the CTO's round-123 analysis for the R1 track (`ledger/ROUND_ANALYSIS.round123.R1.md`, msg 8492, `@980ad8c80c`), issued at `5dae2841dd` (decomposition s.133, `fanout: 2 of 2 chains, cap 8`), amended at `77ce2ac555` (s.133a, cell `cf-6`).

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-cf-1` (Part A) | `run.py` reads `anthropic-api-key` in-process (boto3 Secrets Manager) for the filings command only; the key goes to the child's `env=` only | complete | worker-light ~527; merged `8de2494a24`; 8 tests (T1 to T8), proof VALID |
| `AMGT-cf-6` (Part B of the same order) | `run_filings.cmd` runs `py -3.12 -m lib.research.llm_batch.run filings` | complete | worker-light ~527 (re-seated); merged `3573dd735b`; 5 new tests; llm_batch directory `73 passed` (base 68); proof VALID; worker row `W527-S1` (test_run t12 re-scoped for the filings line) |
| `AMGT-cf-2` | the Peers absent-column lines and the chart line print `Not available` | complete | worker ~528; merged `6f65da85da`; 13 new tests (T1 to T4 per field: Cash, 5-yr growth Revenue, EBIT, FCF); shared-tree print tests `1 failed, 512 passed` (the one known failure; base `1 failed, 499 passed`); three existing assertions re-scoped by one line each; proof VALID |
| `AMGT-cf-3` | the issuer's before/after census | done (section 3) | `round124_prep/checks/r124_full_text_census.py` |
| `AMGT-cf-4` | the pack redeploy under the never-widen pair | applied by `0.7.0_AE_CloudOps~SC1` 20:54Z, KEEP sent | release pin `rel-amgt-cf4` `08b8ea9f8c` (parent `9281d3c0b2`; `render_pack.py` `023406bfda53` to `57160d25953f`); pair COO `58aa7802b5`, CTO `@5cf6ab5fe1` (msg 8526); plan 69 resources, 68 no-op, 1 update, 0 add, 0 destroy; rollback = the `ce-4` artifact `lAqLJzsuCCyjqF8whHTeBiOOBLd.HKaR` |
| `AMGT-cf-5` | the one further deliberate run of `OpalResearch-FilingsAnalyzer` | done, positive arm shown (section 2) | `tmp/llm_batch/filings_20261019T201355Z.log` |

## 2. `bp-5`: the positive arm (the CTO's grade, msgs 8353, 8497, 8499)

- **Run 1** (19:36Z, before cf-6): the key guard no longer blocked (cf-1), the log held 0 key prefixes, rc=1 inside the installed `anthropic 0.45.0` on Python 3.14.7 (row `AMGT_RESAPP-D1-S62`; 0 objects). `pip install` was NOT done: the user env `PIP_NO_INDEX=1` guards it and the estate's route is `org/devices/intake` with a CTO-signed approval; the CTO ruled option B (msg 8499, his 8497 yes withdrawn): the launcher runs on Python 3.12, where `anthropic 0.84.0` (the repo pin) is already installed.
- **Run 2** (20:13:55Z, through `py -3.12`, the merged launcher): `rc=0`, `exit=0`; `BATCH DONE: 8 of 8 analyzed, 0 UNRESOLVED-SOURCE, USD 4.2635`; `r109_g4_positive_arm_read.py --since 2026-10-19T20:13:00Z`: **8 analysis objects and 8 drafting objects written**, 0 `filing_attempt` objects, **mean `usage.usd` 0.5329** against the 0.80 threshold, `last_run.json` recorded `2026-10-19T20:13:56Z`, trigger now `due=False reason=no new filing`. **Key-prefix census: 0 `sk-ant-` matches in the run's log, in `lib/`, in `tmp/llm_batch/`, and in 97622 tracked files (`git grep`; positive control `ANTHROPIC_API_KEY` found in 103 files).**
- **The negative arm** is the Tue 2026-10-20 07:30 local organic fire (the trigger reads `due=False` today). It is event-gated and is not graded here. The billed amount of run 1 was not read (no console read); run 2's batch reports USD 4.2635.
- Open: row `AMGT_RESAPP-D1-S63` (the management task's launcher is on the same 3.14 SDK mismatch; not widened, per msg 8499).

## 3. The census and the live function after the redeploy (`cf-3`, `cf-4`; measured 2026-10-19)

- **Before the act** (live base `r124-full-live-before.json` against this checkout's handler over the same pool, `r124-full-local-candidate.json`): rich PEERS-COLUMN 1116 lines on 93 names, CHART 9 lines, OTHER 0; PDF 100 of 100 byte-identical; `WALMEX*_MM_Equity` uncapturable locally (Windows `*`), read live: 12 Peers lines, no chart line. The comparator was run on three controls first (identical captures: clean; a Peers-and-chart swap: clean; a swap that also touches Posture: 476 OTHER lines flagged).
- **After the act** (live `keJ3wDa8..`, rev `cdab5595`): **1128 Peers absent-column lines and 9 chart lines read `Not available` on the live rich export, 0 still `ABSENT`** (12 columns on 94 names, WALMEX included). SC1's same-session reads: PDF pack form YES 8 of 8, rich word swap YES 8 of 8 with 86 words moved (the figure measured before the act). Mine: leak scan 101 clean of 101; money vs page 16 of 16; cross-surface 8 of 8; rich exports 8 of 8, 0 `s3://`/`AMGT-`/vendor strings; worst route 9.3 s of 20 s; config env unchanged (`AMGT_AIFILL_ROOT` absent, mem 1769, timeout 29).
- **A census read that needs its explanation:** the live-after capture against the pre-act candidate differs on 7 names (BA, COST, HAL, HD, INTU, KMB, VLO; 789 rich lines and their PDF text) and is byte-identical on the other 93. Those 7 are exactly the names `cf-5`'s run re-analysed between the candidate capture and the after capture (new analysis and drafting text). A FRESH local candidate against today's pool equals the live-after capture on all 7 (rich and PDF): the live function serves this checkout's code on the current pool. The other `PACK FORM: NO (1 of 8)` line in the round-118 read set compares against an older before set (market-data lines), as in round 123; SC1's same-session read is YES 8 of 8.

## 4. For your judgment -- PENDING

For the CVO's L9: the CTO's item 2 (Model-sheet and chart status words) is MET if the 13 tests per field and the census above hold: the live function serves `Not available` on exactly the pair's lines. Item 1 (`bp-5`) is MET on the positive arm (section 2); its negative arm is Tue 07:30 local. **For the CTO (decided in msg 8526, restated):** the Posture, `y/y growth`, `<years>E`, Description, Exec Management and Model Cases `ABSENT` lines are the next round's cell with their own pair, `PeersTab.tsx` read alongside. The R1 track closes when round 124 closes with 0 graduated, `bp-5` proven and item 2 MET.

**Process findings (seat errors and gate facts named):** (1) my first `cf-6` order file was refused by `.tools/to-pipeline-gate.py` (ONE ISSUER PER ROUND is keyed to the round); I re-opened `cf-1` and extended it instead, which cost one re-seat of slot 527. (2) A bare message to `~H2` was refused by LD-0529; the CTO-ruled ledger commit rode an ADHOC order with an audited `pipeline-override` (`e78ded64e3`); H2 committed `d6f02e31aa` (28 paths). (3) The `pip install` the CTO authorised (msg 8497) was blocked by the standing `PIP_NO_INDEX=1`; I did not override it and asked (msg 8499 ruled B).

## 5. Open and carried

Row `S63`; row `W527-S1` (observation); the Tue 2026-10-20 07:30 negative arm; A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's); the next-round cell for the other `ABSENT` line kinds. Drain checks in the shared tree: llm_batch `73 passed`, print `1 failed, 512 passed` (the one known failure), api folder not re-run this round (no api file changed).
