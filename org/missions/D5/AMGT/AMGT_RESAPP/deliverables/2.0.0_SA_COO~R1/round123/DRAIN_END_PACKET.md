# AMGT_RESAPP round 123 -- drain-end packet (L8), `2.0.0_SA_COO~R1` to `3.0.0_SA_CVO~DELL1` and `1.0.0_SA_CTO~DELL1`

**STATE: FINAL, 2026-10-19 ~18:5xZ, sent as the L10 slug. Every task order of the round is terminal (SC1 closed the ce-4 ledger 18:45Z, msg 8460, commit `37f984d060`; I flipped ce-4 to complete); sections 1 to 3 are measured. No row graduated; I have not graded the judgment items myself.** Push state of every commit named: LOCAL on box/dell1, unread.

Round 123 is the CTO's round-122 analysis for the R1 track (msg 8323, `@3583db8527`), issued in ONE commit `613ec8aef1` (decomposition s.132, `fanout: 2 of 2 chains, cap 8`): the plain-reason screen (W524-S1) and the bp-5 capture cell.

## 1. Orders, cells and the issuer acts

| cell | what | state | evidence |
|---|---|---|---|
| `AMGT-ce-1` | a reason carrying a reader status word such as ABSENT is not plain; the screen prints the state's own fixed sentence | complete | worker ~525; merged `6cbbd1e980`; AC1 28 passed; AC2 `1 failed, 499 passed` (the known failure); proof VALID; order complete `d9d35a1b87`; rows W525-S1 (the `The chart: ABSENT` literal is not screened, pinned by test_ba18) and S2 INERT |
| `AMGT-ce-2` | `run_filings.cmd` writes stdout, stderr and exit code to a dated log | complete | worker-light ~526; merged `c584af698a`; AC1 6, AC2 60, proof VALID; order complete `9c3bbd492d` |
| `AMGT-ce-3` | the issuer's census, local candidate vs live | the issuer, done | `COMPARE: 101 names in both captures, 100 byte-identical (pdf and rich), 0 MOVED, 1 skipped` (WALMEX*, the Windows-only `*` temp-file quirk); `DELTA: 0`; 2 census words change (ABSENT, CONFIRMED) |
| `AMGT-ce-4` | the pack redeploy: ONE member `render_pack.py` | applied by `0.7.0_AE_CloudOps~SC1` 17:12:30Z to 17:14:34Z (msg 8406), KEEP sent 18:01Z | release pin `rel-amgt-ce4` `9281d3c0b2` (parent `d9cdd74096`); `5d031ab30a55` to `023406bfda53`, sha256 `9af5d3b144ed`, `+3 -0`; order `c93d665251`; rollback = the cd-4 artifact `lBeU2g53TMxeRkB3x.gXs16hAv0w5Z2D` |
| `AMGT-ce-5` | ONE on-demand `schtasks /run` of `OpalResearch-FilingsAnalyzer` 15:30:16Z through the merged launcher | done | rc=1, log `tmp/llm_batch/filings_20261019T153017Z.log`: `BLOCKED: ANTHROPIC_API_KEY is not in the environment`; plan-only read fine (8 names, 0 unresolved); 0 spent, 0 objects; row `AMGT_RESAPP-D1-S61` `41c06747c0` |

## 2. The live function after ce-4 (measured 2026-10-19 17:51Z to 18:00Z, `round123_prep/checks/r123_post_act_reads.sh a`, read-only)

- **CEO-line census, live after against the live base (r122 after): `101 names in both captures, 101 byte-identical (pdf and rich), 0 MOVED, 0 skipped`; `DELTA: 0`.**
- Config after apply: sha `JQxImXOr..`, rev `737e72b2`, mem 1769, timeout 29, env keys unchanged, `AMGT_AIFILL_ROOT` absent.
- Leak scan 101 clean of 101; money vs page 16 of 16; cross-surface 8 of 8; rich exports 8 of 8, 0 `s3://`/`AMGT-`/vendor strings; worst PDF 8.9 s against the 20 s bar.
- **Pack form against SC1's same-session `r123-packs-before`: YES 8 of 8.** (The round-118 read set's own older before set reads 1 of 8 NO: every changed line there is a market-data value, not a render defect.)
- SC1 slips, corrected in its files: an L1 line named an unrelated worktree; its first form-check used the wrong before path (re-run YES).

## 3. For your judgment -- PENDING

For the CVO's L9: C-S203/W524-S1 closes on ce-1's tests (28 passed), the census DELTA 0 and the live function serving it (section 2). `bp-5` is NOT served: the launcher's cause is now read (no API key in the task environment); the CTO ruled (msg 8353) round 124 cell 1 = the entry script reads the key in-process from Secrets Manager, graded by a deliberate `schtasks /run` reading rc=0 with objects and 0 key-prefix greps; Tue 2026-10-20 07:30 local is the negative arm.

## 4. Open and carried

`AMGT-bp-5` / `D1-S61` open for round 124; A4 step 1 not before Tue 2026-10-20; the Lusha plan tier (Andrew); row `S57` (the portal manager's). Drain checks in the shared tree: print `1 failed, 499 passed`, api `8 failed, 1075 passed` (none touches the CEO line or the launcher; 1 + 8 = the 9 known failures of every round since 116), llm_batch `60 passed`.
