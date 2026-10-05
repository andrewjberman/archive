# DSGN_AMGTV1 -- ROUND 37 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-05 ~05:5xZ) -- THE BATCHED REPAIR AND THE READS

**Input:** decomposition v37 and the issuance @7360fee8d6, over PRD v0.15 @237d5d742f. Rectangle: the CTO's enrichment list
@9b2ed08fe2 (msg 29466). Base: portal DEV 56b71adb.

## 1. THE CELL (1 of 1 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 | outer drain |
|---|---|---|---|---|---|
| `AV-zo-1` | FWD-21 edge labels, FWD-8 no cross-currency average, FWD-10 the no-call date | ~99 | 7f679aee | repairs37 5/5 (issuer re-run); battery29 0 skipped | 07720859a5 |

The proof instance is VALID. No rows were filed. The CTO reviewed the portal change and **APPROVED** it (@1a6f5e6982, msg 29490):
FWD-21, FWD-8 and FWD-10 PASS. The DEV push is the merge onto origin/DEV 3e1aa46f, held at `0.0.0_AB_MSTR~Z` for Andrew's word.

## 2. THE CANDIDATE -- portal `85e24287` (worktree 92, branch `dsgn-r37-onto-dev`, LOCAL)

The candidate is origin/DEV 3e1aa46f plus `dsgn-r37-zo1`, merged `--no-ff`. It moves 6 files, +123/-38, and does not touch ModelTab.tsx
or modelSheet.ts. Issuer run:
- battery29 ALL PASS (0 skipped).
- round 37 repairs37 5/5; round 36 repairs36 5/5; round 35 changed35 5/5, payload35 4/4, cloud35 5/5; round 34 labels34 4/4,
  repairs34 4/4, peername34 4/4.
- **FWD-20 instrument** (`round35/checks/instrument/instrument35.cjs`, C:/tmp/r37-scratch-close): 4 of 4 arms, 755 s. The candidate
  reads 76 PASS / 0 FAIL / 1 N/A, so the collage change keeps the render contract.

## 3. THE REAL RUNS (walker slot 29488, granted by MSTR~Z between laptop Y-6 runs; ARMED ~05:27Z, DISARMED 05:48:58Z, login after REFUSED)

**Close walk** `round35/walk/closewalk35.mjs`, read-20261005T052733Z, on 5174 = 85e24287 against the live API. Names: BA, VLO, AMD
and MSFT US. **27 reads: 26 PASS, 1 FAIL, 0 ERROR.**
- The one FAIL is the BA "-100.0%" probe hit on dividends per share 2026, 0.01 -> 0.00: a real move to zero, graded PASS on reading
  in rounds 35-36 and in the countersigned grades.
- The FWD-24 control PASSes on MSFT US. The fwd21 labels hover clean at 30/90/365D.

**The reads, item 4 of the list** `round37/walk/reads37.mjs`, read-20261005T054042Z. **8 reads: 5 PASS, 2 FAIL, 1 ERROR.**

| read | result | issuer grade |
|---|---|---|
| fwd5-markers BA US | PASS | coverage-event marker 2026-01-26 -> the shared HeroDialog "January 26th, 2026", 1 row, 1 GET, 0 refused. No earnings marker is drawn: the designed empty state "Earnings dates are not on file for this company yet". |
| fwd5-markers AMD US | ERROR | AMD serves 0 events and 0 markers, so there is nothing to press. This is a served-data fact, not a page defect. |
| fwd5-own-first BA, AMD | PASS (vacuous) | shown order == served order. The day route serves Opal Data Harvest rows only and has no origin field, so "the firm's own publications come first" holds only vacuously. |
| fwd11-side-by-side | CAPTURE | Four 1440 PNGs plus computed styles. **The person's read (issuer):** /market is the dark navy card family end to end; /security-analysis is the light card family, PRD v0.9's deliberate FWD-12 choice (one navy identity band). They share the chart library, the shared tooltip and the type, not the card family. **JUDGMENT for the CTO/CVO: FWD-11 against FWD-12's chosen family.** |
| fwd19-panels BA, AMD | **FAIL** | The timeline and the identity header render PanelLoading and PanelError (DESIGNED). **What changed does not:** its loading is a lookalike skeleton (not PanelLoading), and on a 500 it shows NO error state, only the skeleton bars (`fwd19-BA-US-what-changed-error-panel.png`). Code: WhatChangedPanel.tsx's hand-rolled states. |
| fwd19-no-permission | PASS | PanelNoPermission renders on the real /security-analysis route for a SIMULATED non-Dev viewer (userType rewritten in the walker's own auth responses, browser-only, no server write): "You do not have access to this page. An Opal Capital administrator can grant it." |

## 4. OPEN -> ROUND 38 (enrichment candidates, for the CTO's list)

1. **FWD-19:** What changed renders the shared PanelLoading and PanelError (a 500 shows an error, never a skeleton).
2. **The CTO's non-blocking note (@1a6f5e6982):** cscTable keys money columns on a producer money marker, so a future non-money
   column keeps its average.
3. **FWD-11 judgment** (section 3), the CTO's or the CVO's.
**Producer, routed:** no peer member serves a price currency, so the Price column prints "Not averaged: currency not stated" on every
name until RESAPP serves one. AMD serves no timeline events. Own-publication origin is not a served field.
**Elsewhere:** the DEV push of 7f679aee onto 3e1aa46f on Andrew's word (held at MSTR~Z).
