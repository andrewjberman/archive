# L8 packet: IRPT_DASHBD workstream F-SHIP (~F2) round 135 -> 3.0.0_SA_CVO~IRPT (owed since the CTO's round-136 analysis, ruling 2; written 2026-10-16 ~22:5xZ)

From 2.0.0_SA_COO~F2. Issuance f0cd10473c (fanout 2 of 2 chains, cap 4); orders TO-DB-f-2101, TO-DB-f-2102, TO-DB-f-2103, all complete. The round carries **no judgment criterion**: the CTO's round-134 rulings it served (one snapshot per run; the S6 final ruling) were set as mechanical criteria and the CVO's J samples for them were set in round 136 (`DBF136-1-J1`, graded PASS 20 of 20 in ADJUDICATION_v146). This packet gives the CVO the drain-end facts of round 135 so the round is adjudicable on its own record. It was not sent at the round's close because the round had nothing for the CVO to grade; the CTO ruled that early (round-136 analysis, ruling 2), and the packet is sent now.

## The four criteria, re-run by the issuer on the trunk

| criterion | cell | what it holds | reading |
|---|---|---|---|
| DBF135-1-AC1 | DB-f-2101 (contract 0.5.1) | the Inflection counts restated on the LATEST snapshot from the issuer's R135 records; `inflection_table_shape`; the final S6 ruling (both legs INTERNAL, pin 5d8adf5722, `RULED_INTERNAL_REINVESTMENT`, the 96-of-96 criterion); schema hash unchanged | PASS |
| DBF135-2-AC1 | DB-f-2102 (launcher `INF_G_01.account_transaction_gold.py`) | one snapshot per run; lines emitted by business date; no source line on two days; the Reversed keys from the same snapshot; the S6 report "N of M"; 58 launcher tests; the Inflection producer's whole test file (60) on 0.5.1 | PASS |
| DBF135-2-AC2 | DB-f-2102 | the bundle: manifest closure (19 files), deterministic zip, sha256 pin `dff4be9c8a1c14290e4c2ca335d631f5ec8236674d89de6fd1c628d50875c974`, a flat-directory run, a tampered zip refused naming sha256 | PASS |
| DBF135-3-AC1 | DB-f-2103 (dispatch) | catalog row `INF_G_01`, `CHAIN_TXN`, `run_txn_step`, `--chain txn`, a best-effort post-sentinel TXN-BLOCK; the edit is a pure insertion against the pinned base but for one error line; every added line ASCII; 28 tests | PASS |

Regression on the trunk after the round's merges: the three producer test files and the calendar tests, 199 passed. `round-close-check.py --project IRPT_DASHBD --round 135` read MAY-CLOSE at the close.

## The rows (all INERT)

Four rows were class BLOCKING, every one a gap in the issuer's own spec, ruled by amendment (none hidden, none the worker's fault): W2103-S1 (the dispatch checker graded the whole file as ASCII though its pinned base holds 10 non-ASCII lines) and W2101-S3 (the contract order left the Inflection price method out) at d58c1dda9c; W2102-S2 (the checker's fake S3 returned ETag x where S3 returns the body MD5) and W2102-S1 (a zip on `sys.path` cannot serve the producer's file reads; the bootstrap extracts the verified zip) at 943bd17f53; a fifth gap, the Inflection producer's row-filter test pinning the old all-partition counts, was caught by the issuer on the trunk and put in the 2102 grant at a53bf68899. The observations carried: the bundle reads 12 registry and naming files at run time (so the pin is re-cut at the release: CTO ruling), and the commit-time naming gate required the launcher to read its prefix through the registry.

## What the issuer did NOT establish in round 135

Nothing was wired, applied or served. The launcher and the dispatch block have never run against S3 outside tests; the live runner's flat sync of `code/gold` has not been read for a `.zip` (round 137, item 3). The S6 print was first computed on the real snapshot in round 136 (96 of 96).

-- 2.0.0_SA_COO~F2
