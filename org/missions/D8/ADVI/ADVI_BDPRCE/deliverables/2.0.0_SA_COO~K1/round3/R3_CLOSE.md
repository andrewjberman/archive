# ADVI_BDPRCE -- ROUND 3 CLOSE PACKET (L7 drain, task-order compile) -- 2.0.0_SA_COO~K1, 2026-10-14 ~06:xxZ, dell1

Round 3 = the amended rule, the list Andrew reads, and the exact-lot preconditions. Decomposition `decompositions/ADVI_BDPRCE_DECOMP_R3.md` (7 cells, 4 chains), issuance @94d1161b08, `fanout: 4 of 4 chains, cap 8`. All seven orders `LOCAL`; nothing served moved; nothing is pushed (box/dell1 LOCAL). Two CTO rulings landed mid-round and were absorbed inside the decomposition (Amendment 2, call d799; Amendment 3, call 19b2): the issuer reopened `BP-c-1` twice, re-ran `BP-c-2` twice and re-cut `BP-c-3` twice.

## 1. The seven orders (all complete; each re-run by the issuer, not taken from the worker's report)

| cell | merge | what the issuer re-read |
|---|---|---|
| `BP-c-4` is 500,000 a cap | @b1c22e968b | the sheet XML of three exports (500,000 / 500,000 / 489,203 data rows); 15 of 76 days at exactly 500,000, all from 2026-07-08; verdict CAP (inferred from the count pattern; no vendor setting is readable) |
| `BP-c-6` sentinel and Monday/Tuesday | @a4d5db390a | deployed package hash equals the function's CodeSha256 and the repo at 3709ae40d6; 7 of 7 post-deploy runs honest; the header-only Monday/Tuesday first export is the export window rule |
| `BP-c-1` R1 module | @2341c317b8 (Amendment 1), @85735d1b81 (Amendment 2), @3e085aa829 (Amendment 3) | `AMENDMENT = "R1.3"`; 53 test arms; per-row par test (Fixed Income AND ratio within 1 percent of 100), per-unit funds left alone, the served unit read from the served series (coarse bands [50, 200] / [0.5, 2]); the probe reads MORGAN STANLEY FIN LLC 0% 2029 as 100.0 per 100 and the eight round-2 par rows equal to the served price (8 of 8); no row changes unit |
| `BP-c-7` off-canonical lots | @47b7837acf | 1,859 lots in 353 price triples: 310 equal an older canonical version, 0 a daily file, 1,118 a named other source (the schwab RPS partition of 2026-07-23), 431 UNEXPLAINED (34 serve the text "nan"); counts recounted from the lots CSV |
| `BP-c-5` exact-lot key | @f3eaea3038 (first seat, measured FAIL), @2f9e7eb4f2 (second seat) | the five-column key folds 192 rows of the 2026-10-09 export (191 groups differing on Market Value, 1 on Inherited Date); PRD v1.3 adds `units`; the patched copy keys on six columns and the legacy output stays byte-equal; the zero is deferred to the first real export under the apply's pair (the recorded export has no Units column); the 500,000 lot rows in the record are on SYNTHETIC units and are not evidence |
| `BP-c-2` R1.3 replay | @284ca5a4f1 (R1.2), @71db825808 (R1.3) | 1,689 served rows: 747 unchanged, 599 changed, 160 carry-forward, 183 not recomputable; 759 prices move; 0 rows change unit (independent test); interpolated fates 16,025 "last traded <date>" and 2,372 unresolved (0 trade price); unit map 1 per 100 / 827 per unit / 60 unreadable of 888 assets; list md5 read equal |
| `BP-c-3` the FWD-7 packet | @90ef5aa850 | 15 prices move on the snapshot 2026-10-09 (99.18 percent of lots), 819 lots in 9 extract assets (6 moving assets are not in the extract); effect $90,964.76 on quantity x served price, recomputed by the issuer with exact fractions from the list and the extract; also $103,614.56 on the served market value and $358,069.95 on each lot's own price (726 of 819 lots carry a price other than the served one) |

## 2. What the packet asks of Andrew (FWD-7)

The page is `deliverables/0.9.0_WK_ADVI_BDPRCE~22/PACKET3.md` (absolute: `file:///C:/dev/ajb_workspace/org/missions/D8/ADVI/ADVI_BDPRCE/deliverables/0.9.0_WK_ADVI_BDPRCE~22/PACKET3.md`), with `MOVERS3.csv` and `PACKET3.json`. It names 15 moves; the largest by dollars are SIX FLAGS ENTERTAINMENT CORP COM (+$96,431.94, a carry-forward of a 2025-08-04 trade), EXXONMOBIL HOLDINGS CORP COM SHS (-$24,308.09) and SPACE EXPLORATION TECHN CORP CLASS A COM STK (+$18,280.14). The decision sentence is the worker's composition (row W22-S5): the order gave none verbatim. The CTO puts the packet to Andrew; nothing is served before his review.

## 3. Findings carried to the CTO

1. **The apply must page.** 15 of 76 exports hold exactly 500,000 rows from 2026-07-08 on, so the exports are not a complete lot population; the bronze prefix holds no daily key for most recent calendar days and no paging slice exists in readable S3 (rows W16-S1, S2; W23).
2. **The Monday and Tuesday export window** is the shared module's anchoring of the newest transactions chunk to the run date; since the honest sentinel (already live) the 2026-10-12 and 2026-10-13 sentinels cover zero transaction rows (row W18-S4, ARMED). It is the same cause as the 61,583 late-landed trade rows.
3. **Units (Amendment 3).** One served asset is per 100 (MORGAN STANLEY FIN LLC 0% 2029); 60 of 888 have no readable unit (59 with no pair); 19 served Fixed Income rows are withheld `unit_unreadable`; 12,070 Fixed Income trade rows on 102 assets are withheld in the window census, 11,687 of them on 88 assets that are not served. Fixed-income funds at ratios 1.04 to 1.08 stay withheld by the 1 percent band (rows W14-S8, W20-S9).
4. **Three bases for the dollar effect.** The packet's headline is quantity x served price; 726 of the 819 lots carry a different price, so the lot-price basis is $267,105.19 higher. Which is the true change in Andrew's book is not settled by the packet (row W22-S1).
5. **183 window rows are not recomputable** (151 no earlier trade, 19 unit unreadable, 3 carry refused, 10 ratio) and 2,372 interpolated rows have no replacement (2,120 no earlier trade).
6. **The lot market-value identity** fails on 21,471 of 196,641 priced snapshot lots (96 in moving assets).

## 4. ARMED rows (25, all with disarm_owner 2.0.0_SA_COO~K1) and what disarms each

The channel reads 108 rows, 54 open, 25 ARMED, 25 graduated, 29 dismissed (comp-surprise, 2026-10-14 05:46Z). Round-3 rows that stand ARMED: `W14-S5`, `W20-S1`, `W20-S2`, `W20-S5`, `W20-S6`, `W20-S8`, `W20-S9`, `W20-S11`, `W20-S13`, `W23-S1`, `W17-S1` (BLOCKING), `W16-S2` (BLOCKING), `W16-S1`, `W18-S4`. The CVO compiles the dispositions; this map says what removes each hazard.

| row | state after round 3 | disarmed by |
|---|---|---|
| `W14-S5` par-scaled carry (115.995 to 1.0) | closed by Amendment 3 and the R1.3 replay (reads 100.0, 0 rows change unit) | the CVO's adjudication; no further act |
| `W20-S1`, `S2`, `S5`, `S6` unit map on the lot extract | superseded by the served-pair map (S5 and S6 no longer hold) | the CVO's adjudication |
| `W20-S9`, `S11` fixed-income rows withheld for an absent unit | 19 served rows remain (BP-c-2) | a CTO call on the band and the 59 assets with no pair |
| `W20-S13` lot pairs set ISHARES CORE U.S. AGGREGATE BOND ETF at 3.5498 | trade pairs outrank lot pairs in BP-c-2's map | the CVO's adjudication |
| `W20-S8` the canonical object rewritten again | each replay re-reads it and prints the denominator (1,689 rows) | the writers stop rewriting it unannounced (round 4) |
| `W17-S1` (BLOCKING) key folds 192 rows | the key gains `units` (PRD v1.3); fixture cannot prove the zero | the first real export under the apply's pair reads 0 folded (round 4, WORLD, `0.7.0_AE_CloudOps~BP1`) |
| `W23-S1` the zero is not measurable on the recorded export | stated in the record | as `W17-S1` |
| `W16-S2` (BLOCKING) the 500,000-row cap | verdict CAP read | the paging design cell and then the apply (round 4) |
| `W16-S1` bronze keys exist only on some days | named in the plan | the paging design cell |
| `W18-S4` Monday/Tuesday sentinel over an empty export | cause named (window rule) | a code cell in the shared module (round 4, a producer change) |
| the seven round-1/2 rows (`W1-S3`, `W2-S2`, `W2-S4`, `W3-S3`, `W3-S4`, `W4-S2`, `W4-S8`) and `W6-S2`, `W7-S4`, `W10-S2`, `W12-S1` | as in `R2_CLOSE.md` section 5, now within reach of the merged R1.3 module and the packet | writers import R1.3 under FWD-7 pairs after Andrew's review |

## 5. Proposed round-4 enrichment list (the CTO's analysis rules it)

1. **The paging design for the exact-lot export, then the WORLD apply** of the Units and Cost Basis switch to `0.7.0_AE_CloudOps~BP1` under its never-widen pair, once both halves are signed and `0.0.0_AB_MSTR~DELL1` seats the lane; the zero-fold proof is read on the first real export.
2. **Writers import R1.3** under FWD-7 pairs after Andrew's review of the packet: the S_00 build and inject stage, the Lambda, the silver script, in that order.
3. **The Monday and Tuesday export window rule** in the shared bronze module (cause measured, fix not built).
4. **The 431 unexplained off-canonical lots** and the stale schwab RPS partition (newest 2026-07-23) that prices 1,118 more.
5. **The unit map's 59 assets with no pair** and the band for fixed-income funds, as a CTO call.
6. **The 2,372 unresolved interpolated rows:** what serves a price with no earlier trade.

## 6. Limits, not hidden

- The workers ran as Haiku 5.5; every report was re-run by the issuer; the issuer's own design of the unit map was wrong twice (the lot extract as the source, then too-tight bands and same-date pairs) and was corrected on the issuer's word, recorded in sections 1.000 and 1.0000 of `TO-BP-c-1`.
- Orphan directory `/c/dev/wk-bdprce-r3-17` (an unregistered partial checkout) is left for a human to remove; it is safe to delete. Branch `wk-ADVI_BDPRCE-15` keeps one superseded unpark commit (023dcee5b5).
- `round-close-check` verdict: see the commit that flips `dep_stage`.

-- 2.0.0_SA_COO~K1
