# IRPT_YCDGEN round 2 -- drain-end packet (L8 compile input) for 3.0.0_SA_CVO

**Issuer:** `2.0.0_SA_COO~Y`, 2026-10-04 ~23:2xZ. **Project:** IRPT_YCDGEN (D9/IRPT), FULL lease. **Round 2:** the CTO's round-1
analysis @34daa80ad5, section 2 (E1-E5), issued in ONE issuance @4182c82353. **Risk:** WORLD.

## 1. Orders

| order | worker | status | merged | mechanical |
|---|---|---|---|---|
| YCD-r-2 (E4 previous-run index, E5 stop row) | 0.9.0_WK_IRPT_YCDGEN~1 @fd43467321 | complete | 988a62c350 | r-2.AC1 PASS (6), r-2.AC2 PASS (4+4) |
| YCD-c-2 (E3 coverage table, probe map) | 0.9.0_WK_IRPT_YCDGEN~3 @c41213cc7f | complete | 14254f9b70 | c-2.AC1 PASS (176/176), c-2.AC2 PASS (2 calls) |
| YCD-m-2 (E2 vector-drawn charts, two gaps) | 0.9.0_WK_IRPT_YCDGEN~2 @9880d0fb36 | complete | 9cfc9da211 | m-2.AC1 PASS (4/4), m-2.AC2 PASS (4), m-2.AC3 PASS control (249/249) |

3 of 3 orders are terminal. Every check was re-run on the merged tree, and the research suite reads 56 passed.

**JUDGMENT criteria owed at L9:**
- **m-2.AC4**, the m-1.AC2 re-grade: every number, table and chart on the source Overview PDF is listed as an element. The
  map now holds 253 elements, with the new ones at p3.e24-e26 and p5.e34; p14.e03 lists six columns and p13.e04 has
  its header word again. Grade it against the PDF in row W2-S2.
- **c-2.AC3** (C-FIRM): no figure value is in `deliverables/maps/overview_coverage.json` or `coverage_probe_map.json`.

## 2. E1 -- the thread's last hop (FWD-1, FWD-6)

The fresh short-lived signed link to the run-3 report was printed to Andrew in this seat's session at ~22:1xZ (CTO 105002
relays his "all recs approved", card 1). It was not stored and its query string was not logged. **Andrew opening it is
his act and is not yet confirmed in this session.** It is recorded in the run record when he says so.

## 3. The one real run of the round's outcomes (issuer close, live)

`close/ycdgen_r2_close_host.sh` ran on the resident host, inside the served lease, 8 s per call, with no generate call:
- YCD-R2-20261004T2315Z-A ran with `--bootstrap-index`;
- YCD-R2-20261004T2315Z-B followed 10 s later.

Output: `close/YCD-R2-20261004T2315Z_host_run.txt`.

| outcome | measured |
|---|---|
| **E4 / FWD-2**, previous-answer lookup | The index was bootstrapped at `ycharts_runs/index=latest/latest_by_portfolio.json`. Run A: both calls `no_previous`. Run B: both calls `false` against run A (the answers did not change). The `true` arm is pinned by r-2's tests |
| **E3 / FWD-3**, the OTHER_ENDPOINT probe | `scatter_plot_data` (POST) with the documented metric ids: 200 with `data.series` (round 1's ids answered 400). `general_data` with `xAxis=metrics`: 200 DATA, 3 categories. Both routes answer for a model portfolio |
| **E5 / C-SESSION**, the stop row | Not triggered: neither run stopped. The behaviour is pinned by r-2's tests; row S3 filed the round-1 stops |
| clocks | A: ycharts 1,255 ms, waiting 8,000 ms. B: ycharts 794 ms, waiting 8,000 ms |

**One defect found:** the keeper labels the scatter answer IDENTIFIERS although it carries a data series (`data.series`).
C-KEEP's shape rule does not know that key. This is a round-3 candidate.

## 4. Rows

- W3-S2 (the three-class enum has no member for "computable from the portfolio's own kept series") and W3-S3 (probe
  placeholders cannot reach per-holding calls; HELD_DATA needs a runner step that reads the frozen upload): OBSERVATION.
  Their `surfaced_at` reads 2026-10-05T00:30Z; the worker reports the true time as ~2026-10-04T22:52Z.
- S1 (disarmed by S2) and S3 (the CVO's): unchanged.

## 5. Carried to round 3 (candidates for the CTO's round-2 analysis)

1. **The HELD_DATA build: 167 elements.** A runner step reads the frozen upload's holdings and calls the security-level
   routes (`table_data` and `fund_data` with real tickers, one at a time in the lease). The layout computes the weighted
   values. Row W3-S3.
2. **The OTHER_ENDPOINT build: 7 elements.** Re-point those elements to the two probed routes. Re-map the four new chart
   elements (p3.e24-e26, p5.e34) through the coverage classes.
3. **C-KEEP's shape rule** reads a `series` answer as DATA.
4. **Index granularity (from r-2):** a STOPPED run with kept calls replaces the portfolio's index entry, so its missing
   calls read `no_previous` next time. Make the entry per call.
5. Retire the `table_data indices=P:` calls (steps 04-12) from the Overview map: they answer 400/404, and step 7 draws the
   firewall's challenge every time.
