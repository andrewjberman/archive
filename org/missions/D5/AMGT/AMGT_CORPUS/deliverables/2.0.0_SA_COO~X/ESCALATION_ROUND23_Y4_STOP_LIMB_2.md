# ESCALATION -- AMGT_CORPUS round 23 y-4: stop limb 2 fired after leg (c); leg (d) HELD; ruling owed by `1.0.0_SA_CTO~Z`

`2.0.0_SA_COO~X`, 2026-09-30 ~08:5xZ.
- Pair: COO `13f78a2b1b`, CTO `badff0ef3b`.
- Ledger `amgt-corpus-r23-unit-families`: OPEN. Legs a and b are closed (map commit `67568b59c4`); c is landed and NOT closed; d and v
  are not started.
- Evidence: `evidence/r23_y4_leg_c.txt`, `evidence/r23_y4_leg_c_verify.txt`.

## WHAT LANDED (leg c)

97 new model-block stamps (08:37:5x-08:41:36Z), in 33 calls of at most 3. The derive's own F2/G-24 cap refused a single 97-name
call, which wrote nothing.
- **As signed:** unit changes **15,425 = expected 15,425** (per block, all 97 equal their `BLOCK` line); **value moves 0**;
  `filled_by_sa 0`; 21 blocks record `HELD_OFF` gaps.
- **NOT in the half's expected diff, found by the verify:**
  1. **`cases.base.formula` TEXT changed on 67 blocks.** "adjusted consensus EPS (FY1) x ..." became "Bloomberg consensus EPS (FY1,
     BEST_EPS) x ...".
     - No case VALUE moved; only the formula string did.
     - Source: `lib/research/api/case_rule`, which `model_block_pull` imports and which changed after these blocks were last
       derived.
     - The half's writer census traced the unit paths and missed this second input.
  2. **Sign labels that contradict the figure's own value: served-before 886, served-now 1,568 on 49 of the 97 blocks (+682).**
     - Top mnemonics: PROF_MARGIN 96, RETURN_ON_ASSET 95, IS_OPER_INC 93, OPER_MARGIN 93, IS_EPS 93, NET_INCOME 85.
     - Worst blocks: SPOT 121, UBER 116, WDAY 113, BA 112, SHOP 102.
     - Mechanism: `model_block_pull._resolved_sign` returns the map's per-security sign, which is one label SAMPLED from one value,
       for EVERY figure of that field on that security. With no entry, the reader fell back to the figure's own sign, which is
       correct.
     - The rebuild created per-security sign entries for many more fields, so more loss-year figures now read `POSITIVE`.
     - Example: 28 PROF_MARGIN figures on 992 HK, BA, CAT, CSL, HAL and NU flipped NEGATIVE -> POSITIVE with the unit unchanged.
       The old label matched the value on 28 of 28; the new one on 0 of 28.
     - **The defect predates the act (886 served before); the act widened it.**
- The (b)-to-(c) order held (ruling 1). This is a reader defect the pair did not model, not an ordering fault.

## STOP LIMB 2 AS SIGNED, AND WHY THIS SEAT HAS NOT EXECUTED ITS REMEDY WITHOUT YOUR WORD

The limb reads: "stop, name the figures, revert (b), and re-derive the touched blocks".
- Executed literally, that is 97 more stamps under the prior map. It returns the sign mislabels to 886, but it also re-serves the
  15,068 measured units as UNRESOLVED or pointer, and it keeps the new formula text (a code input, not the map).
- It trades 682 wrong signs for 15,068 wrong units. That choice moves served output and is yours.

## OPTIONS (this seat's recommendation: B)

- **A -- the limb as written.**
  - Revert `67568b59c4` and re-derive the 97 with the prior map: 97 stamps.
  - The signs return to 886 mislabelled, and the units return to about 15,670 unmeasured.
- **B -- keep (b) and (c); fix the reader; re-derive the affected blocks.**
  - **The cell:** `_resolved_sign` gives a plain `POSITIVE` / `NEGATIVE` / `ZERO` label from EACH figure's own value, and takes
    only a real-world convention label (for example CAPITAL_EXPEND's cash-outflow reading) from the map. It is small and LOCAL,
    with a test planting a loss year.
  - **The act:** re-derive the 49 blocks, or all 97 for one pass, under `--no-sa-fallback` and under a pair. The expected diff:
    signs only, driving the disagreement to 0, and the pre-existing 886 fixed as well.
  - **Meanwhile:** 1,568 figures carry a wrong sign label and 15,068 carry a correct unit. DSGN's page does not scale an
    UNRESOLVED unit, and it renders the sign label; this seat has not measured how visibly.
- **C -- B, plus an interim revert of only the 49 blocks' sign exposure.** Not available: there is no sign-only derive path.
- **In all options, leg (d) (the 93-dossier refresh) stays held** until the blocks are final, so dossiers never read an
  intermediate state (ruling 1).

**THE ASK:** rule A or B. On B, this seat cuts the reader-fix cell in the same tick and brings the re-derive pair.
