# DSGN_AMGTV1 -- ROUND 14 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`.
**Round:** 14, the round-13 analysis @1e7d4bac11 with rulings 1-8.
**Decomposition:** v14 (issuance @6f7593963d, 7 orders in 4 chains, cap 8); no amendment this round. One issuer amendment at the cut
(foldopen.cjs arm 2 compares shape, not values), recorded in v14.
**Close record:** `ROUND14_CLOSE_WALK.md` (same folder).

## 1. Orders -- 7 of 7 terminal, every instance VALID

- **Chain ~54:** AV-k-5 (modelhistory 3/3), DEV 973e1275, CLOUD 3caee92b1c.
- **Chain ~55:** AV-k-6 (styles 3/3, re-run by the issuer on the merged DEV), DEV 53a190ec, CLOUD 5aa7d32783.
- **Chain ~52:** AV-k-1 (reasonwords 3/3), AV-k-4 (execfooter 3/3), AV-k-2 (states 3/3); DEV 3561af6e, CLOUD 96515b61f4.
- **Chain ~53:** AV-k-7 (foldopen 3/3), AV-k-3 (peersempty 3/3); DEV a3f94ad3, CLOUD 12117185f0 (re-drained; see below).
- **After the last merge:** tsc rc=0, ALL 16 of 16 harnesses, every round-14 check 3 of 3 on the final DEV (the render ones re-run by the
  issuer: foldopen, peersempty, styles, rendercontrol 3 of 3 each, 00:08Z-00:39Z).
- **Chains were drawn from the helpers' MEASURED write sets**, not the analysis's "all 7 independent": cells 1, 2, 4 share
  ExecManagementTab/PostureTab and cells 2, 3, 7 share ui-contract-check.mjs. The one cross-chain overlap ruled at the cut merged clean.
- **Push state:** DEV a3f94ad3 is on origin/DEV inside b336b141 (ls-remote read ~04:4xZ). CLOUD push state: see the commit report.
- **Drain correction:** the ~53 drain was first credited to 52b8287a8b, which is an AMGT_RESAPP ae-2 merge; the ~53 branch was not on
  CLOUD. It was re-drained at 12117185f0 (byte-identical to the stranded working-tree copies).

## 2. The one real run

- **Signed-out control:** YES (the walk fails on the sign-in page).
- **Walk N** (5174 @e5ae0063 = DEV a3f94ad3) VALID: 146 shots, 0 guard aborts, 0 API issues (row Z-S8's /compare 500 did not recur),
  disarm proven.
- **The render run** on the final page build: **PASS 74, FAIL 0, NOT_EXERCISED 0, N/A 1 -- RESULT PASS.** FWD-14..19 PASS with values;
  fwd19 PASS (round 13's peers/empty FAIL gone); fourStates PASS; sizes and radii PASS in all six states; posture-cites-open PASS (20 == 20,
  8 == 8).
- **The PNGs were read.** The judgment criteria go to `3.0.0_SA_CVO~Z` (AC4 of k-1..k-7).

## 3. Round-15 inputs (the enrichment list is yours)

1. **Row Z-S9 -- an interface code on 6501's Exec:** "No officer list is in this name's pack yet: no M-1 management object has landed for
   this name ...". The live served management reason carries "M-1" and producer words; AV-k-1's mapping keeps a letter-dash-digit code,
   and the round-13 fixture's 6501 reason (an S3 path) predates the live wording, so execfooter.cjs could not see it. Either the shared
   mapping drops interface codes of that shape (with the fixtures refreshed from the live reasons), or the producer serves a reader
   sentence.
2. **The fixtures lag the live served reasons** (item 1's cause): the round-13 captures are carried into round 14 unchanged.
3. **Instrument findings (helpers, at the cut):** the `radii` clause accepts a pill on any element, so it cannot see C11's "pill for status
   dots and avatars only"; `ui-smoke.mjs --expect-text` crashes on an SVG element (innerText undefined).
4. **Posture reason 2 reads "Both names' fit scores are ABSENT rather than low"** -- a served drafted sentence carrying a status word in
   capitals (walk N, BA Posture); the page prints the draft as served.
5. **Carried:** c14's long-form clause blind spot; Z-W47-S2's surfaced_at estimate; `publishers_found_codes` after RESAPP ac-3 (msg 27194).

## 4. Held for Andrew

- **The portal DEV push of a3f94ad3** goes through 0.0.0_AB_MSTR~Z on his word, after a pull-merge of origin/DEV; the PROD promotion
  (analysis s.5) after it.
- **Recursive removal of the round-13 and round-14 scratch** (`C:/tmp/dsgn-r13-*`, `C:/tmp/dsgn-r14-*` incl. the nine green and stack roots,
  and worktrees `wk-dsgn-amgtv1-49..55`); branches kept. I would remove them after your round-14 analysis, in case a re-render is asked for.
