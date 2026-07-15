# NFRA_GRAPHFEED TO-4 -- comp-which top-k: REVIEW-FIRST verdict (Andrew-direct 07-15 ~21:0xZ honored)

**Author:** 0.8.0_AE_CloudComp~Z · **Date:** 2026-07-15 ~21:3xZ · **Wave:** LD-0299
**Instruction of record:** deliverables/ANDREW_DIRECT_20260715_TO4_compwhich_review_first.md
("you shouldnt need to touch any of comp-whichs description or top-k ... review the current
state of that before touching it at all")

## Verdict: THE DIRECTIVE IS ALREADY BUILT. ZERO code change made or needed.

**1. The build exists and predates this wave:** `c52f83612` (1.0.0_SA_CTO~Z, **2026-07-13
18:07 ET** -- the same day as the PRD): "TOP-3 + full ranking spilled to YAML (Andrew) + THE
ABSTAIN IS NOW PROGRAMMATIC, rc=1." Live output today: `MATCHES (top 3 of 58 -- score is
overlap, NOT a confidence)` with a per-candidate description, PLUS the full ranked+described
list of ALL 58 routable tools written to `.comp-graph/which/rank-<pid>.yaml` on every call --
strictly MORE information than a literal top-5. The PRD's verbatim "top-5" vs the landed k=3+
full-yaml: a k flip is a one-line change with zero evidence it is wanted; Andrew's word is
"top-3 with great descriptions that are working great." NOT TOUCHED.

**2. Measured effects of the landed build (FULL tally, the SS0 errata measurement law --
13,192 log lines read, nothing filtered; 502 unparsed lines disclosed = multi-line q= text
spillover, not routing rows):**
- **The legacy cascade is DEAD in practice:** bare-`ROUTE` = 1,487 rows all-time, **0 rows**
  post-c52f83612 across **1,930** comp-which decision rows (ROUTE-POSTERIOR 1,898 +
  NOFIT-POSTERIOR 23 + on-rails fallback RUN-GREP/GLOB 9). The 18.8% legacy share the errata
  measured is retired by the same change that landed top-3.
- **Explicit abstains post-top-3:** 32/1,930 = **1.66%** (the programmatic "I HAVE NOTHING"
  working; all-time abstain share was 2.5%).
- Frozen routing baseline re-run this session: **PASS** (zero pollution, 100% gibberish
  abstention) -- the TO-4 regression guard holds with no change made.

**3. The one measurement TO-4 names that CANNOT be honestly produced from tags: the ~34%
zero-result rate.** That number was a CONTENT-LEVEL cohort adjudication (SS0 errata, cohort R);
the rail log carries NO per-row zero-result marker (verified: the only zero-ish token estate-
wide is `count=0` on 110 comp-grep/comp-glob rows -- a different construct, search-emptiness
not routing-uselessness). Re-deriving 34%'s before/after requires the cohort-R construct
definition from its author. **Inventing a tag-level proxy here would repeat the errata's exact
defect** (a retrieval pattern silently excluding the evidence; three agents did it in one day).
ROUTED: construct-definition ask to CTO~Z (the SS0 adjudicator); the before/after runs when the
construct is in hand, as a measurement-only follow-up.

**4. Findings for the record:**
- LD-0298 sec-2's "Andrew's 07-13 top-k redesign is NOT built" was **FALSE at write time**
  (built 07-13 18:07 ET; assessed 07-15 17:40Z) -- a stale record saying something false with
  authority (verification law #8). No fault chased; noted so the wave TO's premise is corrected.
- The 07-13 PRD's file:line citations pin @52d008f4c, which is PRE-c52f83612 -- anyone
  re-reading the PRD should treat its comp-which mechanics sections as superseded by the landed
  build, not just its SS2 numbers by SS0.

## AC disposition
- "routing self-test PASS against the frozen baseline" -- **MET** (re-run this session, PASS).
- "top-5-with-descriptions served" -- **MET AS BUILT** (top-3 on-screen + all-58 ranked+described
  in the per-call yaml; Andrew-direct confirms the built shape is the wanted shape).
- "zero-result rate re-measured on the full rail tally with the denominator printed" -- tag-level
  full tally DONE (denominators above); the content-level 34% construct routed to its author --
  the only honest path per the errata's own law.
