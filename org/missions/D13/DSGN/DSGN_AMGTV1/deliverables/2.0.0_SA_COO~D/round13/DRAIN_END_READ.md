# DSGN_AMGTV1 -- ROUND 13 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`.
**Round:** 13, the round-12 analysis @81907cfe5f with rulings 1-3.
**Decomposition:** v13 (issuance @265d39a87b, 6 orders in 3 chains, cap 8); no amendment this round.
**Close record:** `ROUND13_CLOSE_WALK.md` (same folder).

## 1. Orders -- 6 of 6 terminal, every instance VALID

- **Chain ~50:** AV-l-2 (fiscal 3/3), DEV 20b62fb5, CLOUD c83e48ce9c.
- **Chain ~49:** AV-l-1 (dossier 3/3), DEV 032f881d, CLOUD fa793b887c. Then AV-l-3 (c14 3/3), DEV ccca64ef, CLOUD 21c6a076da.
- **Chain ~51:** AV-l-4 (strip 3/3), AV-l-5 (sweep 3/3) and AV-l-6 (fwd1419 3/3, rendercontrol 3/3). DEV 118cd005, CLOUD ae55273059.
- **After the last merge:** tsc rc=0, and ALL 16 of 16 harnesses green.
- **Push state:**
  - DEV 118cd005 is LOCAL. origin/DEV reads 29bfec2d, other seats' pushes (ls-remote ~17:3xZ). ccca64ef is not in it.
  - CLOUD is LOCAL.
- **ae55273059 carried 5 staged ETFS_RIVALS files of `2.0.0_SA_COO~RV`.** It confirmed them (msg 27328): leave them, no revert.

## 2. The one real run

**Walk M** (5174 @a4b81627, l-1..l-3) was VALID; the signed-out control was VOID as designed.

**The render run** (final page build, DEV 118cd005 scripts, `--states-sweep`) read PASS 63, FAIL 11, NOT_EXERCISED 0:

- **FWD-14..18:** PASS with values.
- **Round 12's two FAILs are fixed:** list darkContainers (by l-4) and fourStates / no-permission (by l-5).
- **fwd19:** FAIL, missing peers/empty. This is a page defect.
- **sizes x5 and radii x5 FAIL:**
  - The sources are TimelinePanel's 10px axis, the rounded-full MACHINE badge and Exec's dots.
  - All three already exist at ba62e945.
  - They are newly visible because l-1's refreshed fixtures render the header timeline for the first time. They are not a round-13 regression.

The PNGs were read. The judgment criteria go to `3.0.0_SA_CVO~Z` (AC4 of l-1..l-6).

## 3. Round-14 inputs (the enrichment list is yours)

1. **Producer words on the face** (row Z-S7). BA, 992 HK, VLO and TSM serve section, class and fund-token diagnostics as the dossier reason, and l-1 shows them faithfully. Two ways to fix it:
   - RESAPP serves a reader sentence;
   - or the page maps the reason class to one sentence and keeps the diagnostic in a `data-` attribute.
2. **`/security/BA%20US/compare` answers HTTP 500 on the Posture step of walk M** (row Z-S8). The display ticker is used as the key. The call site at DEV is not located yet: the one fetcher sends `?from=&to=`.
3. **FWD-19:** Peers has no designed empty state.
4. **FWD-20 style clauses newly visible:**
   - 10px chart ticks (`TimelinePanel.tsx:561`);
   - pill radii (`ThesisCards.tsx:259`, `ExecManagementTab.tsx:96`).
5. **Posture's footer reads "the comparable bundles are still loading" at rest** in the static render.
6. **Carried:**
   - c14's long-form clause blind spot (it also matches the identity line's date);
   - Z-W47-S2's surfaced_at 12:05Z is an estimate; its commit landed 11:49Z;
   - `publishers_found_codes` goes live after RESAPP ac-3 (msg 27194);
   - Z-W51-S1: the PASS face is graded on `data-verbatim-check`; a visible face would change `gradeFwd14` only.

## 4. Held for Andrew

- **The DEV push of 118cd005** goes through 0.0.0_AB_MSTR~Z on his word, after a pull-merge of origin/DEV 29bfec2d.
- **Recursive removal of the round-13 scratch:** `C:/tmp/dsgn-r13-{build-dev,build-pre,build-final}`, `C:/tmp/dsgn-r13-dist`, `C:/tmp/dsgn-r13-close-render`, and worktrees `wk-dsgn-amgtv1-49..51`. Branches are kept. I would remove them after your round-13 analysis, in case a re-render is asked for.
