# AMGT_RESAPP round 77 -- GROUP B draft notes (ba-5, ba-6, ba-7), `2.0.0_SA_COO~Z`, 2026-10-07 ~00:5xZ

Input: `ledger/ROUND_ANALYSIS.round76.md` @c8bbeeac10 rulings 6 and 7; `ledger/CTO_ADJUDICATION_REMEDIATION_ROWS_ROUND76.md`
ADDENDUM 1 @3bad4be9e0 (row Z-W20-S8). Deployed function `opal-amgt-scoped-api` CodeSha256 OVpDhfwD. Portal origin/DEV at the
draft: 13509c52 (the shared tree's portal checkout is a3ab197f, stale).

## 1. Measured at the cut

- **/thesis over 95 covered names (deployed, 95 of 95 read 200):** a filing driver chart is SERVED on 2 (BA, ASML NA) and
  ABSENT on 93; a segment breakdown serves rows on 12 and a reason on 83.
- **Ruling 6, where each defect lives: all three are on the page** (`portal/src/pages/SecurityAnalysis/components/`).
  - Three renders: `ThesisDriverChart.tsx` keys its open state on the passage id; ASML NA's 3 points share one id (P0086).
  - Axis ticks: its `YAxis` has no `tickFormatter`.
  - Column labels: the route ALREADY serves BA's `passage_table` (columns 737, 747, 767, 777, 787, Total; rows Cumulative
    deliveries, Deliveries; ay-4). The page reads `passage_table` in 0 places on DEV.
  - ASML NA's passage serves no `passage_table`: its labels and figures sit on separate lines, so under half its tokens are
    numeric and it is not read as a table. Ruling 7 refuses that chart, so no served repair is cut for it.
- **Ruling 7:** ASML NA's driver is "Issued ordinary shares outstanding", unit "number of shares"; its 5 segment rows are
  Authorized share capital, Other, Treasury shares, Major holders, Board holdings. PBR's 8 rows are all "Other" (royalty
  rates). A prototype of the class rule refused driver 1 of 2 and segments 2 of 12, and kept BA, BABA and HD (5 of 10 "Other").
- **Why those two names:** their stored excerpt holds the risk factors ONLY (no operating review). ASML NA keeps 70,000 of
  1,091,017 characters of one item. This is what ba-7 makes visible.
- **Section coverage over 95 names (newest stored source object):** a filing read on 12, a reason on 41, no object on 42. Of
  the 12: both sections on 9, operating review missing on 2 (ASML NA, PBR), risk factors missing on 1 (HAL); a section cut
  short on 8. BABA: risk 70,000 of 350,005; operating review 80,000 of 131,933.
- **BA one heading per segment** (Z-W266-S2): the served rows carry the right names (11 rows, 3 labels, interleaved); the page
  prints the label on every row. Page work.

## 2. The three cells

| id | title | slot | wave | risk | write surface |
|---|---|---|---|---|---|
| `AMGT-ba-5` | the page repairs: passage once per press, the served table drawn, axis ticks, one heading per segment, a refused chart reads its plain reason | `~271` | 0 | LOCAL (portal, DEV only) | `ThesisDriverChart.tsx`, new `PassageTable.tsx`, `SegmentBreakdown.tsx`, `types.ts`, `__harness__/` under `portal/src/pages/SecurityAnalysis/` |
| `AMGT-ba-6` | the class refusal: share-capital and one-label tables | `~272` | 0 | LOCAL | new `lib/research/filings/table_class.py`, `tests/test_table_class.py` |
| `AMGT-ba-7` | the passage section coverage | `~273` | 0 | LOCAL | new `lib/research/filings/section_coverage.py`, `tests/test_section_coverage.py` |

No edge inside the group: three chains. ba-5 needs a portal worktree (`--portal-ref` + `--node-modules link`); ba-6 and ba-7
need none.

## 3. Hookups for AMGT-ba-11 (the adapter cell, wave 1)

In `lib/research/api/scoped_amgt.py`:
1. Import, beside `:131`: `from lib.research.filings import section_coverage, table_class`. Both are stdlib-only at module
   scope (checked), so the package closure gains two small modules and no fetch stack.
2. `thesis_driver_chart` filing branch (`:3880`, before the SERVED return): `refusal = table_class.driver_refusal(thesis_driver,
   <the first verified point's passage text or None>)`. When not None, return `status: "ABSENT"` with `plain_reason: refusal`
   (the page shows it; ba-5 item 5), `refused: True`, `driver_series`, `points: []`, `points_count: 0`. The existing `reason`
   is system text and stays system text.
3. `read_segment_breakdown` (`:3778`, after `rows = _segment_rows(document)`): `refusal = table_class.segment_refusal(rows)`;
   a refused analysis is not a candidate for `best`. When every analysis read with rows is refused, return `{"rows": [],
   "reason": refusal, "source": None}`. The page already shows `reason`.
4. `/thesis` body (`:3678`, beside `segment_breakdown`): `bundle["passage_coverage"] =
   section_coverage.read_section_coverage(resolved_key or security_key, _pool_client, pool_reader.POOL_BUCKET)`. It costs one
   listing and up to two object reads per /thesis; the analysis read can be saved by passing `passage_map=` if ba-11 keeps
   the document `read_segment_breakdown` already read.
5. The print (`lib/research/print/render_pack.py:1351-1355`) prints `thesis_driver_chart` from the bundle verbatim, so it
   follows hookup 2 with no edit; whoever owns the print should confirm it prints `plain_reason`, not `reason`, for a refused
   chart.

Expected served effect after ba-11 + the redeploy: driver chart SERVED 2 -> 1 (ASML NA reads its reason); segment rows on
12 -> 10 (ASML NA and PBR read their reasons); `passage_coverage` on 95 of 95.

## 4. Checks, each dry-run at the base

| check | base | green arm |
|---|---|---|
| ba-5 AC1 (`r77_ba5.py --crit AC1`) | FAIL as expected (one press opens 3) | not run (needs the page change) |
| ba-5 AC2 | FAIL as expected (tables 0, no formatter, no plain reason shown) | not run |
| ba-5 AC3 | FAIL as expected (headings 0, label alone 4/3/4) | not run |
| ba-6 AC1, AC2, AC3 (`r77_ba6.py`) | FAIL as expected (module absent) | YES on all three with a scratch prototype |
| ba-7 AC1, AC2, AC3 (`r77_ba7.py`) | FAIL as expected (module absent) | YES on all three with a scratch prototype |

- The ba-5 instrument was run against portal origin/DEV 13509c52 exported to a scratch directory (`R77_PORTAL_SRC`,
  `R77_PORTAL_MODULES`), because the shared portal checkout is behind DEV. In the worker's worktree it reads `portal/` as cut.
- ba-5 AC1's controls (C1, C5) and AC2's (C5, C6, C10) and AC3's (C2, C6) PASS at the base, so the FAILs are the defects and not
  a broken instrument.
- ba-5 AC4 is a judgment criterion: the CTO's render review.

## 5. Scope readings made in the draft (the issuer's to keep or change)

1. **ba-5 is a portal cell on a DSGN_AMGTV1 page.** All of ruling 6 measured as page defects. It can be cut here (as drafted)
   or routed to `2.0.0_SA_COO~D`. If routed, the check files and the fixture go with it unchanged.
2. **Ruling 7's "one heading per segment on BA" moved from ba-6 to ba-5,** because it is page work on the same component set.
3. **"At the producer" in ruling 7** is read as where the chart and the breakdown are produced for the page. The stored
   driver and segment findings come from the model stage, which is not re-run, so a write-time refusal would move no
   served name. ba-6 edits no producer file.
4. **ba-5 item 5** (an ABSENT chart shows `plain_reason`) was added so a refused chart reads its reason; today the page
   prints a fixed "not in the model data yet" sentence for every ABSENT chart.
5. **No served repair for multi-line table passages** (labels and figures on separate lines) is cut: the one specimen is
   the chart ruling 7 refuses.

## 6. Open

- `portal/src/pages/SecurityAnalysis/types.ts` is in ba-5's paths (the point type gains `passage_table`, the chart type
  `plain_reason`). Any other round-77 portal cell touching the security page's types collides there.
- ba-5's worktree paragraph carries the token `PORTAL_REF_AT_CUT`.
- The ba-6 bound "fewer than half of the served breakdowns are refused" (AC3 C7) reads 2 of 12 today. The Bloomberg segment
  pull (item 6) does not write filing analyses, so it should not move this count; if it does, that is a row.
- A single-segment company whose rows all carry one real name is refused by class two, as ruled. None exists among the 12.
