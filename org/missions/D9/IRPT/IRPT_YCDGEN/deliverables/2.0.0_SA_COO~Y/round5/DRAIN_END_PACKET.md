# IRPT_YCDGEN round 5 -- drain-end packet (L8 compile input) for 3.0.0_SA_CVO

**Issuer:** `2.0.0_SA_COO~Y`, 2026-10-05 ~16:2xZ.
**Round 5:** the CTO's round-4 analysis @a1b47e6b3f (E1-E6) and REMEDIATION_v4 (W3-S6, S7), with W4-S4, issued in ONE
issuance @2f901c0a21.
**Risk:** WORLD.

## 1. Orders

| order | worker | merged | mechanical (re-run on the merged tree) |
|---|---|---|---|
| YCD-r-5 (12-request plan, request hash, lookup) | ~1 @beb0e52cfb; proof and row re-landed by a fresh ~1 @bcb83344c1 | 84a7af1854 | r-5.AC1 PASS (2), AC2 PASS (3), AC3 PASS (2) |
| YCD-p-5 (budgeted Overview map, six statistics wired) | ~2 @c89be80b44 | 306a315dc9 | p-5.AC1 PASS (8 requests for 99 holdings, 0 unread calls), AC2 PASS (5), AC3 PASS (6 of 6) |
| YCD-h-5 (Opal-held census and module) | ~3 @a2df1b5d80 | a979784ea4 | h-5.AC1 PASS (158 of 158: 86 OPAL_HELD, 72 NOT_HELD), AC2 PASS (7) |
| YCD-m-5 (map residuals R1, R2) | ~4 @3951983575 | bb0c22bd1e | m-5.AC1 PASS (0 placeholder labels; Multi p9.e08 lists "No data available"), AC2 PASS (4) |
| YCD-w-5 (Opal-held elements wired; join) | ~2 @c6dd878b32 | ff51386f38 | w-5.AC1 PASS (158 of 158 OPAL_HELD with a group), AC2 PASS (6) |

**5 of 5 orders are terminal.** All 12 checks PASS on CLOUD, and the research suite reads 135 passed (with the issuer
repair below).

**Issuer rulings** (each order's drain note):
- W1-S2: lookup `--region`.
- W2-S7: the benchmark ^SPXTR, confirmed at E6.
- W2-S8: p7.e15 is Opal's addition.
- W2-S9: DGS3MO has 2 years, so 1y statistics only; per-column compute is carried.
- W2-S10: no 0.95 coverage floor for OPAL_HELD; the held-of count is on the page.
- W3-S7: Opal holds the figures for at most 37 of 99 holdings; the worker's mappings are confirmed.

**Process notes:**
- The sparse worktrees (the disk was full) could not commit under `org/missions` (INDEX-ORPHAN). They were widened to every
  mission home. No commit carries an override.
- Two channel-union merges: base plus both appendices.

**JUDGMENT criterion owed at L9:** m-5.AC3, W4-S4 re-graded against the two PDFs: every row listed, labels read right, no
figure value. The new labels come from the rule's output. Multi p9.e08 is new.

**Issuer repair after the drain:** @05fc7afa6f. `runner._elements` keeps an OPAL_HELD source by its group. The first E6
attempt refused KeyError 'call' at the record build, before any lease or request. Test added.

## 2. The close acts

| act | state | evidence |
|---|---|---|
| E4 leg 1 (indexed level series on the merged runner) | **done** 12:15Z in ~D's freed slot: YCD-R5-E4-20261005T1215Z, PLAN requests=2, COMPLETE. The lookup printed the kept call live: 200 DATA, sha256 539579bb.., request_sha256 f464fb7e.., no_previous by contract (run G carried no hash) | `close/YCD-R5-E4-leg1_host_run.txt` |
| E4 leg 2 (the byte-identical request after today's close reaches YCharts) | **pending** after 20:00Z plus the vendor lag, and only once the session is live (below) | `close/ycdgen_r5_e4_host.sh` (same script) |
| E6 (the budgeted Overview: 8 requests, 6 + 2, 660 s; render, store, link) | **attempt 1 refused before the lease** (runner defect, fixed @05fc7afa6f). **Re-run held:** the stored YCharts session was evicted twice (14:41Z and 14:56Z), because Opal employees share the YCharts account and a new login evicts the stored session (Andrew via MSTR 105330). A research run cannot re-login; the next page job's refresh can | `close/YCD-R5-E6_host_run.txt`, `close/ycdgen_r5_e6_host.sh`, `close/e6_render_store.py` |

**Also measured this round:**
- The firewall window is in (122, 373] s (WAF-PROBE-20261005T1254Z-W330, @bb1b59c3f6).
- CTO batch 262: the jobs' read-back release is cut to 390 s, built @f1e101d19c, deploying after Y-6.

## 3. Rows

- **Ruled at the drain:** W1-S2, W2-S7, W2-S8, W2-S9, W2-S10, W3-S7.
- **Remediation progress:**
  - W3-S6: the inputs are wired; 1y only until a longer risk-free series.
  - S7: the request hash is built; the true arm's live leg is E4 leg 2.
  - W4-S4: R1 and R2 are closed by the rule; your re-grade is owed.

## 4. The direction after this round (Andrew-direct)

At ~14:3xZ Andrew turned the project toward **rebuilding the generation in Opal's cloud, with YCharts dependencies toward
zero** (verbatim @a812d50ff1). The CTO routed it (105307): 4.0.0_SA_CRO's brief addendum first, then the endpoint
revision (PRD v0.2). This seat's handoff to the CRO is
`deliverables/2.0.0_SA_COO~Y/HANDOFF_TO_CRO_ONPREM_GENERATION_20261005.md` @d87bed6db6. It covers the field contracts,
the per-variant cross-reference, the Opal data inventory and the gaps.

Round 5's maps, Opal-held feeds and six statistics carry into the insourced build (CTO 105307).

## 5. Carried (for the CTO's round-5 analysis / PRD v0.2)

1. A longer risk-free series (FRED lookback, or Bloomberg 3M in data.pkl), so the 3y-15y statistics compute; and a
   per-column (1y-15y) compute for the p7 tables.
2. E6 and E4 leg 2 once the session is live, or superseded by the in-house path.
3. Comparison and Multi coverage censuses (only the Overview has one).
