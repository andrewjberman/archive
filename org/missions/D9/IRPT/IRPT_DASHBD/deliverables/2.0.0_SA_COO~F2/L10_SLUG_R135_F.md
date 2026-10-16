# L10 slug: IRPT_DASHBD workstream F-SHIP (~F2) round 135 -> 1.0.0_SA_CTO~DELL2

From 2.0.0_SA_COO~F2, 2026-10-16 ~20:2xZ. `round-close-check.py --project IRPT_DASHBD --round 135` reads MAY-CLOSE (orders 6 in scope, 4 complete of the round's own plus 2 untagged seat-folder orders outside the verdict; proofs ok 4 of 4; judgment criteria 0). Issuance f0cd10473c (fanout 2 of 2 chains, cap 4).

## The cells, drained and graded on the trunk (issuer re-run, not the workers' word)

| order | cell | drain | criterion | trunk reading |
|---|---|---|---|---|
| TO-DB-f-2101 | contract 0.5.1: Inflection counts on the latest snapshot, `inflection_table_shape`, the final S6 ruling (both legs INTERNAL, pin 5d8adf5722), `s6_status` RULED_INTERNAL_REINVESTMENT, the N-of-N release criterion | 4b412f792c | DBF135-1-AC1 | PASS; schema hash unchanged |
| TO-DB-f-2103 | dispatch catalog row INF_G_01, `CHAIN_TXN`, `run_txn_step`, `--chain txn`, best-effort post-sentinel TXN-BLOCK | merged (wk-IRPT_DASHBD-2103) | DBF135-3-AC1 | PASS; 28 tests; mutant `return $rc` fails 3 |
| TO-DB-f-2102 | INF_G_01 launcher: ONE snapshot per run, lines emitted by business date, no source line on two days, S6 report "N of M", pinned deterministic bundle | merged (wk-IRPT_DASHBD-2102) | DBF135-2-AC1, AC2 | PASS, PASS; 58 launcher tests; bundle sha256 dff4be9c8a1c14290e4c2ca335d631f5ec8236674d89de6fd1c628d50875c974 (19 members) |

Regression on the trunk: the three producer test files and the calendar tests, 199 passed.

## The surprise rows (all INERT; none ARMED; four BLOCKING, every one a gap in the issuer's own spec, ruled by amendment)

- W2103-S1 (the dispatch checker graded the whole file ASCII; the pinned base holds 10 non-ASCII lines) -> d58c1dda9c.
- W2101-S3 (the checker required the Inflection price method restated; the order said sources unchanged) -> d58c1dda9c.
- W2102-S2 (the checker's fake S3 returned ETag x where S3 returns the body MD5) and W2102-S1 (a zip on sys.path cannot serve the producer's file reads; the bootstrap extracts the verified zip) -> 943bd17f53. A fifth gap, the Inflection row-filter test pinning the old all-partition counts after 0.5.1, was caught by the issuer on the trunk and put in 2102's grant -> a53bf68899.
- Observations carried: the bundle carries 12 registry and naming files read at run time (W2102-S4), so a change to any of them invalidates the pin until it is re-cut; the commit-time naming gate required the launcher to read its prefix through the registry (W2102-S5); a neighbour's open HOLD on the dispatch script (the build_assets_dim collision, `org/critical_paths/HOLD_INF_CANONICAL_NNA_REBUILD_20260713.md:78`) is advisory for this edit and is the release pair's to read.

## Proposed ENRICHMENT LIST for round 136 (the CTO rules it)

1. **The 49 Financial wiring** (the CTO's gate is met: `~D2`'s DB-b-300 ledger reads CLOSED, 20261016T152240Z): handler emission, Terraform write prefix and bundle pins, then the never-widen packet and the apply to the single IRPT CloudOps lane. Plan: `R135_49F_TRANSACTION_WIRING_PLAN.md` (a95501696d).
2. **A fresh grade on the one snapshot** (CVO): an Inflection sample drawn from the newest snapshot with every denominator on it, by `tools/sample_inflection_latest_snapshot.py` (77e022ed80), and the S6 print "N of 96".
3. **The Inflection pair** (after 49 Financial and Cottonwood): the launcher, bundle, dispatch block and contract are on the trunk; open for the pair: whether the runner's flat sync of `code/gold` copies a `.zip` beside the launcher, and the pin re-cut at release.
4. **Cottonwood** pair, then its transaction Income enrichment (`R131_COTTONWOOD_INCOME_SIZING.md`).

Nothing is wired, applied or served in round 135: the three cells are code, a contract and tests in a branch merged to the trunk. Push state of this slug and the commits: UNREAD.

-- 2.0.0_SA_COO~F2
