# L8 drain end -- IRPT_CUSTDY round 6

**Issuer:** `2.0.0_SA_COO~K2` (dell2) | **Date:** 2026-10-07 ~14:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile; no JUDGMENT criterion this round)

Round 6 is the round-5 analysis's E1-E3 (`1.0.0_SA_CTO~DELL2` @f6160117ce), one issuance @fed55f91cc (`fanout: 2 of 2 chains, cap 8`)
from `decompositions/IRPT_CUSTDY_DECOMP.round6.md`. All three orders are terminal and merged; 0 linked IRPT_CUSTDY worktrees.

| order | worker | drain | proof | real run on dell2 |
|---|---|---|---|---|
| CU-f-1 (E1) not-covered end to end | ~14 | @65511fc814 (chain A); portal e355d193 (branch `wk-IRPT_CUSTDY-14-portal`, on 99addd80, not on DEV) | VALID: AC1 pytest passed, AC2 bun `0 fail` (`bun --no-install`, node_modules linked) | `hop3_real_run`: 14 household documents, 14 distinct household ids; each of the 4 not-covered accounts alone in its own document with a non-empty reason; `validate_document` admits 14 of 14 |
| CU-f-3 (E3) anchor probe bounded | ~14 (re-seated) | @65511fc814 (chain A) | VALID: AC1 `HOP3-TIMED ... seconds=62.2 within_120=True ... si_ok=14 si_labels_rule1=12 si_labels_rule2=2`, AC2 9 passed | issuer re-run: `HOP3-TIMED advisor=matthew_gooch seconds=85.9 within_120=True households=10 accounts=14 si_ok=14 si_labels_rule1=12 si_labels_rule2=2` (before: 148.2 s, also 133 s / 194 s) |
| CU-f-2 (E2) tracer retired | ~15 | @0143c19ac1 (chain B) | VALID: AC1 `failed=0 errors=0` | -- |

**The one real run at close** (~14:3xZ, dell2): `HOP3-REAL-RUN advisor=matthew_gooch as_of=2026-09-30 households=10 accounts=14 uncovered=0
held_si=0 not_in_directory=4 of=18 not_covered=4 error=none`, and the timed check above. E1 criterion (3) and E3 are graded on these; the
output file holds client figures and stays in the issuer's scratchpad, uncommitted.

**What replaced the listing (E3, row W14-S3):** the per-day S3 listing cost ~0.05 s; the time was 309 sequential silver-position reads in
`_holdings_before_first` (~84 s). The probe now prefetches the span's days once (16 workers) and filters each to the probe's accounts in
pyarrow before the pandas decode. The gold manifest carries nothing about silver holdings, so the ruling's manifest option did not apply.
Anchor rules and labels unchanged. Margin note: dell2 network variance is large (62-86 s after; 133-194 s before).

**Drain checks on CLOUD:** `SUITE dir=data/assets/scripts/gold/irpt_custody/tests passed=147 failed=0 errors=0 skipped=0 xfailed=1` @65511fc814; py_compile OK on the three changed scripts; `hop3_real_run.py --self-test` all ok. Worktrees: 0 linked IRPT_CUSTDY; portal branch `wk-IRPT_CUSTDY-14-portal` kept for the CTO review.

**FWD-1 thread: NOT LIVE** (unchanged reason). Hops 1-4 run on real data for all 18 granted accounts inside 120 s; the template renders a
covered household and a not-covered account locally. Hop 5's served render waits on IRPT_BCKEND (the print kind that mounts the document) and
on the template's DEV landing (Andrew); hop 6 is Andrew's.

## Rows of the round

| row | class | standing | note |
|---|---|---|---|
| W14-S1 | OBSERVATION | INERT | the not-covered portal test builds its document inline (synthetic) because the existing test is coupled to the shared fixture; accepted by the issuer (S12) |
| W14-S2 | OBSERVATION | INERT | the inherited tracer test red on the slot's base; retired on CLOUD by CU-f-2 (S10) |
| W14-S3 | OBSERVATION | INERT | the ruling's premise (a listing; a manifest as the fix) did not hold; the cost was sequential silver reads; fixed by prefetch + filter |
| S12 | OBSERVATION | GRADUATED | the round's close and real-run grade |

**For the round-6 analysis (not rows):** the portal candidate e355d193 (extends the reviewed 99addd80 line) for CTO review; DEV landing on
Andrew's word. The 30 'not described' holdings in the real render (carried from round 5). The remaining hop-3 time outside the probe
(`unkeyed_lookup.build_context` ~25-30 s, the returns load ~14-22 s) if the 120 s bound needs more margin before scheduling.

-- 2.0.0_SA_COO~K2
