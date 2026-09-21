# IRPT_BCKEND -- **ROUND 7 ANALYSIS (L10)**, `1.0.0_SA_CTO`

**Date:** 2026-09-21 ~05:0xZ · laptop · CLOUD
**Reads:** `3.0.0_SA_CVO`'s L9 slug `98958` @`357565e863` · `2.0.0_SA_COO~B`'s completion report `98947` ·
the L8 packet `ledger/IRPT_BCKEND_ROUND7_L8_COMPILE.md` @`86cdf14fbe`
**Consumed by:** `2.0.0_SA_COO~B`'s round-8 recut, in ONE issuance (Rule 27 L10 order).

---

## 1. THE ROUND IS TERMINAL AND THE GRADES STAND

**ACCEPTED, unchanged:** `R72-AC2`, `R73-AC2`, `R74-AC2`, `R75-AC2` all **PASS**, in the `grades` carrier on row
`C-S123` with each criterion's pinned proof instance and reason. All four arrived marked
**UNVERIFIABLE-BY-INSTRUMENT by their own workers and none was self-graded** -- the half that usually fails
quietly, working.

**`R74-AC2` PASS on the cell's own bound is CORRECT and I am recording why**, because it is the grade most
open to being misread later: route resolution in `tenants.py` is proven for all three firms; the live 2-of-3
shortfall is an S3 404 in `_authz/served.py::enforcer_for`, **UPSTREAM of `route_for` and outside the bound**.
**A cell is graded against its own bound.** The blocker does not vanish -- it graduates as `W3-S50`, and the
slug names me as its owner. **Accepted: `W3-S50` is mine.**

## 2. ⭐ FWD-5: I AFFIRM THE CVO'S REFUSAL, AND IT OVERRULES THE COMPLETION REPORT'S HEADLINE

`2.0.0_SA_COO~B` graded **FWD-5 realized on the served plane**. `3.0.0_SA_CVO` refused and graded
**ADVANCED, NOT REALIZED**. **I affirm the refusal.** Read against FWD-5's own text in PRD v0.15, its DONE
WHEN names a replay **for all three registry client firms**, and its PROOF names an unassigned account, an
unmatched join, a blended model, a multi-relationship membership, **unique underlying holdings reconciling
BEFORE AND AFTER the overlay**, and coverage/join exceptions **carrying denominators**. The evidence is one
granted account on one firm returning HTTP 200. **Even this project's own share of FWD-5 is the reconcile
control and the denominators, and a 200 touches neither.**

⭐ **THE REASON IS THE PART THAT TRAVELS, AND I AM ADOPTING IT AS THIS PROJECT'S LANGUAGE: REMOVING A BLOCKER
IS NOT REALIZING AN OUTCOME.** `S100` was a refusal defect standing in front of FWD-5. Fixing it was real work
and is graded as real work -- `R75-AC2` PASS. **But the outcome's own DONE WHEN names an exercise nobody has
run.** This is the estate's EXPOSURE-versus-INCIDENT distinction moved up to outcome grading.

⚠ **NOT A CRITICISM OF THE PACKET.** The completion report was honest, enumerated, and told the CVO to
enumerate rather than asserting completeness -- which is the reason the miss was catchable at all.

## 3. FWD-2 REMAINS **SPLIT**, AND "PARTIALLY REALIZED" IS NOT MINTED

The packet offered REALIZED or PARTIALLY REALIZED. **`3.0.0_SA_CVO` measured "PARTIALLY REALIZED" at 3
occurrences in 170,239 files -- all three being tonight's own packet and its inbox copy.** ⛔ **Minting an
outcome value inside an L9 is a schema change without the Rule 24 four-postulate record, and I refuse it
too.** This project already carries the vocabulary: **SPLIT** (round 6) and **ADVANCED, NOT REALIZED**
(rounds 2, 3).

- **Containment half: REALIZED, untouched by round 7** -- met by the `rtb-1`/`sb-3` batteries, revoked grant
  against a warm cache included.
- **Serving half: ADVANCED, NOT REALIZED**, on `W3-S50` (inflection) and `W1-S43` (submit-wiring).
- **FWD-2 STAYS SPLIT.**

⭐ The CVO disclosed nearly getting this wrong in the other direction -- its first read graded FWD-2 unrealized
from round 7's deliverables alone, and round 6's compile shows the containment exercise WAS run. **"Has this
EVER been graded" is a different question from "does THIS ROUND contain it", and only the first is right for
an outcome that spans rounds.** I am recording that as a standing read for every future FWD grade on this
project.

## 4. ⛔ MY OWN DENOMINATOR WAS WRONG, AND THE RULE I WROTE CAUSED IT

Censusing this project for this analysis, my instrument returned **73 orders, 8 non-terminal**. The round
reports **79, 0 open**. I did not accept either figure and ran the gate's own resolver.

**THE RESOLVER IS RIGHT AND ITS DOCSTRING SAYS SO: it globs BOTH ROOTS** --
`*/task_orders/<CODE>.*.md` (**legacy flat, UNDERSCORE**) and
`org/missions/D*/*/<CODE>/task-orders/*.md` (**tree, HYPHEN**).
Measured: **tree 73 + legacy 6 = 79, exactly.** The six are `IB-rt-5`, `rtc-2`, `rtc-6`, `rtc-8`, `rtc-9`,
`rtd-3`, all `.pointer.md`.

⛔⛔ **THE UNDERCOUNT IS CAUSED BY A RULE I WROTE MYSELF THIS SESSION.** In tick 1 I read
`task_orders/` (underscore), got a false zero, and wrote the corrective into my own loop prompt: *"order
counts come from `task-orders/` WITH A HYPHEN."* That rule **fixed tick 1's instance and created this one** --
it is not that one root is right, it is that **THIS PROJECT HAS ORDERS ON BOTH.**

⭐ **THE KEEPABLE: A RULE DISTILLED FROM ONE FAILURE CAN BE EXACTLY WRONG FOR THE NEXT INSTANCE ON THE SAME
AXIS** -- and it is more dangerous than the original error, because it now carries the authority of a lesson
learned and rides in a recurring prompt. **The correct rule is not a path; it is CALL THE GATE'S OWN
RESOLVER**, which already reads both roots and applies `_proof_terminal`. **COST: one import instead of a
glob. NON-APPLICATION: a project measured to have orders on only one root -- and that is a MEASUREMENT, not
an assumption.** ⚠ **Measured for the two projects in my drive scope: `MDPF_TAXSMA` legacy 0, `NFRA_MCPINDEX`
legacy 0, so every in-scope header figure I published in ticks 1-6 stands.** The defect reached only this
out-of-scope read.

**TERMINALITY, on the resolver: `0 open of 79`, with 7 orders terminal by a VALID proof instance at HEAD whose
status word is not terminal.** The round IS terminal. ⚠ **And "0 open" here is a PROOF-based zero, not a
status-word zero -- the two differ by exactly those 7.**

## 5. WHAT ROUND 8 COVERS -- the recut is `2.0.0_SA_COO~B`'s, in ONE issuance

1. **`W3-S50` -- inflection serving route.** The S3 404 in `_authz/served.py::enforcer_for`, upstream of
   `route_for`. ⚠ **Bounded by Andrew-direct `98869` answer 2, whose terms are his and are NOT widened here:**
   *"Root access is not possible ... Minting a new principal for this matter may be redundant and roundabout
   but if that is the only way it can be rectified then so be it. If it cannot be done, then we will make new
   buckets ... I would prefer it is not necessary to do that."* **So: rectify the existing bucket FIRST; a
   minted principal only if rectification cannot be done; new buckets are the LAST resort and he has said he
   would prefer not; the root console is NOT an option.** Owner of the row is me; the cell is the round's.
2. **`W1-S43` -- export submit-wiring**, deployed `submit_export` NOT_READY.
3. **The status-word hygiene: 7 orders terminal-by-proof with un-flipped status words.** ⚠ **This is
   BOOKKEEPING, not re-work** -- the proofs are VALID at HEAD and terminality already reads from them. It is
   worth a cell because every seat that censuses by status word gets a wrong number, which is the same class
   as §4 above, three projects over.

⛔ **NOT IN ROUND 8, and stated so it is not silently adopted: FWD-5's realization exercise.** Its DONE WHEN
names a three-firm replay with reconcile-before-and-after and denominators, and its OWNER line names
**`IRPT_FNTEND`** for the exercise with **this project** holding join correctness, the reconcile control, the
denominators and the revision-bound `HoldingsSnapshot`. **Round 8 may build this project's share; it cannot
realize FWD-5 alone, and a round-8 report claiming FWD-5 REALIZED will be refused on the same grounds.**

## 6. ⛔⛔ THE 110 STALE OWNED ROWS -- I GIVE THEM AN OWNER RATHER THAN CARRYING THEM AGAIN

The gate emitted, **nine times and NOT as a refusal**: *"110 OPEN, owned remediation rows under
`IRPT_BCKEND` have not moved for 2 or more rounds ... a row that EXISTS, is OPEN and is OWNED goes stale
silently and no rowlessness limb will ever see it (S75) ... clearing them needs its own cell with an owner."*

⭐ **A DISCLOSURE WITH NO OWNER IS HOW 110 BECOMES 130**, and the CVO was right that its slug cannot move them.
**MY RULING: this is a ROUND-8 CELL, owned by `2.0.0_SA_COO~B` as the issuer, and its output is a
DISPOSITION-PER-ROW, not a bulk close.** Three bounds on it, so it cannot become a sweep:
- **Each row is dispositioned on its own evidence.** A row that is still live stays live and says so.
- ⛔ **NO ROW IS CLOSED BY AGE.** "Has not moved for 2 rounds" is a STALENESS signal about the PROCESS, never
  evidence about the HAZARD -- the label-versus-evidence inversion this estate has measured repeatedly.
- **The cell prints its denominator and the per-disposition counts**, so the next round can see whether 110
  fell because rows were disposed or because the census narrowed.

## 7. WHAT I AM NOT DOING

**No task order is cut here** -- L6 is `2.0.0_SA_COO~B`'s and this analysis is its input (Rule 27). **No
apply, no deploy, no seat.** The estate is under Andrew's ~02:4xZ **no-new-seats** hold and nothing here asks
for one. **`W3-S50` is mine as a row owner; the cell that acts on it is the round's.**

## 8. STATE AT THIS READ

| | |
|---|---|
| round 7 | **TERMINAL**, 0 open of **79** (proof-based, both roots) |
| served deploys | **4 of 4 live**, drained, independently verified (live sha at target, `proof-of-spec-check` VALID rc=0 on the issuer's own run, first-parent diff) |
| judgment criteria | **4 of 4 PASS**, none self-graded |
| FWD-2 | **SPLIT** -- containment REALIZED, serving ADVANCED-NOT-REALIZED |
| FWD-5 | **ADVANCED, NOT REALIZED** (refusal affirmed) |
| carried to round 8 | `W3-S50`, `W1-S43`, status-word hygiene, the 110-row disposition cell |
| push state | `357565e863` and this analysis **LOCAL**; only `0.0.0_AB_MSTR` pushes CLOUD |
