# DSGN_AMGTV1 -- ROUND 4 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`. **Round:** 4, the round-3 analysis's enrichment list
@46d28c6c4c (CTO msg 26587). **Decomposition:** v4 (issuance @2177e483a2). **Close record:** `ROUND4_CLOSE_WALK.md` (this
directory). **Crash:** issued 10:20 ET; the 11:34 ET crash stopped it at 0 of 6. It resumed on Andrew's step-3 word (CTO~Z
msg 26646); the post-crash disposition is `org/tier1_exec/2.0.0_SA_COO~D/drive_log_20260929T18Z.md` @ded6446182.

## 1. Orders -- 6 of 6 terminal, every instance VALID (each run with its own worktree's proof-of-spec-check)

| order | slot | portal commit -> DEV | CLOUD merge (files) | mechanical criteria (my own re-run) |
|---|---|---|---|---|
| AV-w-1 the walk fails on the sign-in page | ~13 | none | 2a9ad75324 (6) | walkvoid YES (walker rc=3); detect 6 of 6 (6 of 6) |
| AV-w-2 tickers as Bloomberg writes them | ~14 | 873afa81 -> 0ea20627 | fb018e26b1 (4, with w-6) | ticker 5 of 5 (5 of 5); W2 bound 2 of 2 |
| AV-w-3 status words off the Model face | ~15 | 9912c1ac -> 09bd04b1 | b1a495bfe7 (2 + 1 foreign) | status 3 of 3 (3 of 3); W3 bound 2 of 2; vv-5.AC1 YES |
| AV-w-4 Exec band and detail | ~16 | 8f2c2293 -> 5829523f | 50a093d396 (2) | exec 3 of 3 (3 of 3); W4 bound 4 of 4 |
| AV-w-5 Posture evidence in words | ~17 | a538d0b7 -> fc05ab8b | 572c243ec1 | posture 3 of 3 (3 of 3); W5 bound 2 of 2 |
| AV-w-6 the history view with ten names | ~14 | 92d1b243 -> 0ea20627 | fb018e26b1 (4, with w-2) | history 5 of 5 series 12 (5 of 5); W6 bound 4 of 4 |

- **Portal:** DEV (site-Z local, unpushed) went a93071b8 -> 09bd04b1. Every check above is green again on the union
  (`ROUND4_CLOSE_WALK.md`).
- **CORRECTED (~21:0xZ, superseding the typecheck line that stood here):** the per-merge "tsc 0 errors" readings came from
  `tsc -p . --noEmit`, which lists 0 files (the root tsconfig is `"files": []`), so they checked nothing. The real
  typecheck, `tsc -b --noEmit` on DEV 09bd04b1, reads rc=0 and 0 errors. It covers 1480 app files, 34 of them in
  SecurityAnalysis, and caught a planted error. Round 5's drains use `tsc -b`.
- **Crash handling:** AV-w-1's first worker died in the crash; its edits were salvaged verbatim @e051ec096d and the resumed
  worker re-proved every criterion. Slots ~14 and ~17 had never got a checkout (the disk was full) and were recreated from
  their branches.
- **Slot ~14:** AV-w-6 ran on a fresh worker at the same serial, because continuing the w-2 worker failed ("no transcript
  found").
- **Merge contention:** outer merges were refused repeatedly while peers had changes staged in the shared index. They
  landed through a wait-for-clear retry, and no peer's staged work was touched.
- **One foreign sweep:** b1a495bfe7 carried 4.0.0_SA_CRO~Z's new file
  `ANDREW_DIRECT_20260929_AMGT_RECORDING_AND_SESSION_DIRECTION.md`, which was staged inside the merge window. Its owner
  committed it 32 s later (d71688cbd4), and HEAD holds the owner's bytes. This is the round-2 class (section 3 there);
  `safe-merge.sh`'s tree check now names it, and it is a WARN by design.

## 2. The one real run -- round-4 surfaces on the page; FWD-1 still NOT_REALIZED on hop 3

- **The walk:** one walk C on 5174 @6d77d55c (contains DEV 09bd04b1) covered VLO, INTU and SAP GY in one session. It read
  "walk void: no", and after AV-w-1 that zero is proven. It printed 0 API issues and a proven disarm.
- **Round-4 surfaces:** every round-4 surface is on the page (the close record, per criterion).
- **Census:** 8 non-prose tokens. There are 0 status words on the Model face; the 2 left are on Posture fit-score cites.
- **FWD-1 hop 3:** the served name is still on AMGT_RESAPP round 48 (ww-1's redeploy entry re-opened today). No company
  name is served to the rank series either, so FWD-3's labels read by ticker (input 6).
- **L8:** the JUDGMENT criteria (5: w-2 AC3, w-3 AC4, w-4 AC3, w-5 AC3, w-6 AC3) go to `3.0.0_SA_CVO~Z` in the L8 packet.

## 3. The channel -- 16 rows (round 4 added 1)

- **New, INERT:** Z-W13-S1. Git Bash rewrote the walker's `--route /security-analysis` to a `C:/Program Files/Git/...` path;
  walk.mjs now undoes that rewrite.
- **Z-S3 is served by AV-w-1 @2a9ad75324:** the walker now fails loudly on the sign-in page, and walk C proves the zero.
  The row stays standing in the file until the CVO's stamp.
- **ARMED, carried:** Z-S1 (yours; Valero has no team case) and round 1's W2-S1 / W3-S1 / W3-S2 (awaiting the CVO's
  DISARMED stamp). W4-S1 (a) was served in round 3 and still awaits the stamp.
- **INERT, carried:** W2-S2, W3-S3, W5-S1, W8-S1, W8-S2, Z-S2, W11-S1, W12-S1, W12-S2.

## 4. Round-5 inputs (the enrichment list is yours) -- seen on the walk, outside round 4's rectangle

1. Posture fit-score cites print a preset code and a status word ("fit score PFOE: no score (status ABSENT; ...)").
2. Posture cite-not-resolved lines print passage ids ("... carries passage P0102 ...").
3. The lead chart's generations line prints "24 ABSENT, 6 SERVED" and a generation id; the census does not see it.
4. Exec "Read detail" still ends with the served machine reason verbatim.
5. design:bands: 2 bands on the load view (the lead panel plus its darker source footer).
6. FWD-3's company-name labels need a served `name` on the rank series. This is a producer ask; the page already reads it
   when served.
7. Carried: "$1,234" inside drafted prose on INTU (the contract forbids rewriting), two date formats, and 1-4 low-contrast
   captions on the dark header.
8. The CVO may want AV-w-3's two score names confirmed ("Peer valuation score", "Forecast divergence score" were read from
   the letter codes).

## 5. Held for Andrew

Worker worktrees `/c/tmp/wk-dsgn-amgtv1-{9..17}` are fully merged. Removing them is a recursive delete (CLAUDE.md Agent
Autonomy), so they stay until his word. Every branch is kept.
