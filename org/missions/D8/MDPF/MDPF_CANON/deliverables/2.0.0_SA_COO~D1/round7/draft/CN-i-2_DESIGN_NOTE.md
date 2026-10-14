# CN-i-2 (candidate for the round-7 recut) -- repair of the AUA Trend candidate after the CVO's NOT MET -- design note, 2.0.0_SA_COO~D1, 2026-10-14 ~16:4xZ

Draft only. Nothing here is issued. Inputs: the CVO's L9 on CN-i-1 AC4, adjudication row `MDPF_CANON-D1-C-S73` (NOT MET) and its graduation `MDPF_CANON-D1-C-S74` (REMEDIATION_v7, INERT: D1-W18-S7, D1-W18-S1, D1-W18-S3, D1-W17-S2),
read in `surprise-channel/adjudications/ADJUDICATION_v10.md`. The candidate (`cand/dell1/mdpf-canon-aua-trend-groups-and-as-of` @34cd12d2) is NOT landed; approval 6e63 is held for Andrew; the promote also waits on CN-j-2.

## What the CVO found, and what each item needs

1. **Colour (D1-W18-S7).** `Client Unsupervised` resolves to `PALETTE.orange500` (#f97316), the locked Ultra-Short Term hex (DESIGN.md C4): CIEDE2000 0.0 against it, where every other trend pair is 10.3 or more; the estate already
   moved Alternatives off orange500 for the same reason (`chartColors.ts` IV-e-70). Repair: a Client Unsupervised colour at least 10 CIEDE2000 from every other trend colour and from the five locked model colours; the CVO's computation is the
   instrument (a check arm, not a judgment). The Client chips are the order's own addition, so the colour is the cell's to choose; the locked colours are not.
2. **Tooltip null rows (D1-W18-S1).** `renderTrendTooltip` filters only `interp_total`, so a Client series that is null on a non-as-of date prints a `$0` row. Repair: filter null/undefined entries before the format; a mechanical arm over the pure grouping helper.
3. **Stack equals the Total (D1-W18-S3).** Not shown by the render. The worker's data arm classes 463 of 487 valued dates as a "model_aua rounding gap" with a worst residual in the billions; only 24 dates are exact. This is NOT a drawing defect and must not be
   repaired in the page: it needs a measured classification first (which dates, which series' difference, whether the gap is the pre-2026-05-15 history where per-model lines do not exist), and then a CTO ruling on what FWD-9 (6) promises
   ("to the cent" on which dates). REC: the round-7 analysis names this as a question before any cell; the cell draws what the served data supports and states the dates it does not claim.
4. **Not shown by the render.** The true remainder `Other AUA` on date A, no `-$0`, and the server's commit (the walk stamps none). Repair for the evidence, not the page: the next real run hovers the tooltip on the named dates and prints the commit
   the 5174 server carries (`git -C portal rev-parse HEAD` in its worktree, stated beside the screenshots).
5. **D1-W17-S2.** An unrestored module-level test stub in `test_global_fold_flag2.py` (CN-h-1's row; CN-h-1 itself pins the real loader with an autouse fixture); a test-hygiene item for the repair batch, not for the portal cell.

## Shape

One portal cell (LOCAL, `portal/src`; client-facing at the landing) over items 1, 2 and the evidence of 4, behind the CTO's ruling on item 3. Files: the same three portal files as CN-i-1 plus the colour module. It builds on the candidate branch
(`wk-MDPF_CANON-18-portal` / `cand/dell1/mdpf-canon-aua-trend-groups-and-as-of`), so the worker's base is that branch, not DEV. Its criteria (at most three mechanical): a colour-distance arm; a tooltip arm over the pure helper; the existing CN-i-1 module and
page arms unchanged. The landing stays Andrew's (client-facing), together with CN-l-2, after CN-j-2 is deployed.
