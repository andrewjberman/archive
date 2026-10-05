# IRPT_YCDGEN round 3 -- drain-end packet (L8 compile input) for 3.0.0_SA_CVO

**Issuer:** `2.0.0_SA_COO~Y`, 2026-10-05 ~02:3xZ. **Round 3:** the CTO's round-2 analysis, section 2 (E1-E6), issued in ONE
issuance @7616d7a7d9. **Risk:** WORLD.

## 1. Orders

| order | worker | merged | mechanical (re-run on the merged tree) |
|---|---|---|---|
| YCD-r-3 (holdings + expand calls; keeper series rule) | ~1 @5a982069a6 | dd418f6555 | r-3.AC1 PASS (8), r-3.AC2 PASS (2) |
| YCD-l-3 (layout computes, with trace) | ~3 @a74de27f75, re-landed @1044735175 | 614554f60f | l-3.AC1 PASS (6), l-3.AC2 PASS (2) |
| YCD-w-3 (map wiring; OWN_SERIES) | ~2 @039cec613f | 37e2a053c6 | w-3.AC1 PASS (22 expand calls; 158 HELD_DATA, 9 OWN_SERIES, 7 OTHER_ENDPOINT, 0 unwired), w-3.AC2 PASS (control) |
| YCD-m-3 (Comparison and Multi maps) | ~4 @9c4d183fd6 | 04c20019c8 | m-3.AC1 PASS (32/32 and 34/34 pages) |

4 of 4 orders are terminal, and the research suite reads 73 passed. Each channel append conflict was resolved as base plus
both appendices: every json block parses and every id is unique.

**Issuer rulings** are recorded in each order's drain note:
- W1-S1: run.json is v2 only with holdings.
- W3-S4: the five computation conventions are confirmed.
- W2-S4: statistics outside 3.4 read not available.
- W2-S5 and W4-S1..S4 are accepted.

**JUDGMENT criterion owed at L9:** m-3.AC2: every figure on each source PDF is listed, and no figure value is in the maps.

**Issuer repairs after the drain:**
- `0d4e7512b3`: the holdings read takes a template row's `analysis_dollars`. The first close refused `HOLDINGS_UNREADABLE`
  before the lease.
- The close map `close/overview_map_r3_close.json` retires round 1's ten failing calls. A seat cannot write
  `deliverables/maps/`, so the retirement of those calls in the canonical map is a round-4 cell.

## 2. The live close (issuer, inside the lease)

| attempt | request | outcome |
|---|---|---|
| 1 | YCD-R3-20261005T0207Z | refused before the lease: HOLDINGS_UNREADABLE (KeyError). A v2 template row has no `original.quantity`. Fixed at `0d4e7512b3` |
| 2 | YCD-R3-20261005T0219Z | holdings 99 rows (Y-5's frozen input, SGOV for TIMXX), run.json v2. Steps 1-2 answered 200; steps 3-6 (`holdings_key_stats__c01..c04`, `/indices/table_data` over 20 holding tickers each) answered **404**; step 7 drew the firewall challenge (202). STOPPED; the lease was released; the runner wrote `stop_row.json`, filed as **S5** |

**What it measured (row S6):**
1. **The firewall challenges the 7th request of ANY run.** Runs 2, 3 and 4 were each challenged at step 7, at ~1.5 s, 8 s
   and 2 s spacing, on three different calls. S3's "request-shaped" reading is corrected: a run gets about 6 YCharts
   requests per window.
2. **`/indices/table_data` answers 404 for the holdings' own tickers,** as it did for `indices=P:<id>`. The coverage
   table's HELD_DATA route is wrong for these holdings.

**Built but not yet fed live:** E1's 158 computed elements, their 3.5 trace, and the 9 OWN_SERIES elements. No layout was
rendered on attempt 2's answers: with only the portfolio info and the level series kept, the report would equal run 3's,
which is already stored (FWD-1's report; Andrew's open is still not on record).

**E5 (FWD-2's true arm) is a real wait, not a stalled act.** At 02:2xZ Monday the last market close is still Friday 10-02,
the same data round 2 read. A run before Monday's close (~20:00Z) can only read `false`. So E5's run goes after Monday's
close (trading calendar).

## 3. Rows

- **S5** (the round-3 close's stop row, from the runner) and **S6** (the two measured bounds): OBSERVATION.
- S4 (the CVO's keeper row) is answered by r-3's series rule; the scatter answer reads DATA on the next kept run.
- W1-S1, W2-S4, W2-S5, W3-S4, W4-S1..S4: ruled at the drain.

## 4. Carried to round 4 (candidates for the CTO's round-3 analysis)

1. **A security-level route that answers for these holdings.** `/indices/table_data` 404s. Candidates: the estate's
   per-security routes (`general_data` per security, `securities_info`), or the served path's own data for the holdings.
   Measure them in at most 6 calls per window before any build.
2. **A call budget per run.** About 6 requests per window: design the Overview's calls (and the HELD_DATA batching) to that
   budget, or across windows. This bears on FWD-6 (Andrew's sitting).
3. **Retire round 1's ten failing calls in the canonical map** (a worker cell; the close used a derived map).
4. **E5** on the first run after Monday's close.
5. The four vector-drawn charts (p3.e24-e26, p5.e34) are computable from held data once (1) lands.
