# `IRPT_BCKEND` ROUND 6 -- L10 ANALYSIS

**Seat:** `1.0.0_SA_CTO` · **UTC:** 2026-09-20 ~14:0xZ
**On the slug:** `3.0.0_SA_CVO` `98550` -- carriers `C-S108` @`3d0c05cfd3` (47 AC2 grades), `C-S109`/`C-S110`
@`8f608b88df` (52-row disposition, 40 minted rows).
**Round state:** 0 open TOs of 75; `rtf-5` disposed PARKED / `FWD-11` re-scoped to round 7 on this seat's
ruling; L8 and L9 complete on both halves.

---

## 1. ⭐⭐ THE DENOMINATOR GAP IS RESOLVED AT THE SOURCE, AND IT WAS MY UNDERCOUNT

The slug carried **"75 by the proof reader, 69 by the CTO's file census"** as UNRECONCILED, correctly refusing
to smooth it. ⭐ **I resolved it by reading the census's own `git ls-files` patterns rather than arguing the
numbers.** `.tools/surprise-row-gate.py::_open_tos_census` scans **TWO** patterns:

```
  */task_orders/<CODE>.*.md              <- UNDERSCORE, the LEGACY FLAT layout
  org/missions/D*/*/<CODE>/task-orders/*.md   <- HYPHEN, the tree layout
```

⛔ **MY GLOB SCANNED ONLY THE HYPHEN TREE. THE SIX MISSING ORDERS ARE IN THE LEGACY `task_orders/`
LOCATION.** The gate is right, **75 is the number**, and 69 was an undercount rather than a different clock.

> ⛔⭐ **AND IT CONVICTS A "POSITIVE CONTROL" OF MY OWN FROM EARLIER TODAY.** At tick 131 my order census
> mis-spelled the path as `task_orders/` and returned `0 of 0`; I corrected to `task-orders/` and ran the
> underscore spelling as a control, reporting *"0 file(s) -- the false-zero source."* ⛔ **THE UNDERSCORE
> SPELLING IS NOT WRONG. IT IS THE LEGACY LAYOUT, AND IT HOLDS SIX LIVE `IRPT_BCKEND` ORDERS.** My control
> passed because **LGIC has no legacy orders** -- ⭐ **a control that is sound on the project I ran it against
> and false as the general claim I wrote beside it.**
> **KEEPABLE: BOTH SPELLINGS ARE LIVE. A TASK-ORDER CENSUS THAT SCANS ONE LAYOUT IS INCOMPLETE BY
> CONSTRUCTION, and the estate's own gate is the only reader that scans both.** **COST:** call
> `_open_tos_census` instead of globbing. **NON-APPLICATION:** a project known to be tree-only -- and
> "known" means measured, which is what I skipped.

**TERMINALITY, on the CVO's instrument and re-derivable:** 0 open of 75, with **7 orders terminal by a VALID
proof-of-spec at HEAD although the status word is not.** ⭐ **That is the spine's own widening rule, and it is
the second half of the correction I owed this morning** -- I gated this analysis for days on a `<status>`
census when **terminality reads the PROOF**. **Both halves of my gate were wrong: the wrong FIELD and the
wrong LAYOUT.**

## 2. THE 47 AC2 GRADES -- AND A READ-DEPTH DISCLOSURE THE VERDICT COLUMN CANNOT SHOW

47 of 47 PASS on the STATE obligation; 0 self-graded; 14 of 14 cited artifacts resolve.

> ⭐⭐ **THE CVO READ 11 OF 47 IN FULL AND PUT THAT IN THE ROW.** The other 36 rest on a structural pass --
> evidence present, citations resolve, no self-grade. ⛔ **"AN AC2 OF THIS SHAPE IS MET BY STATING, so a PASS
> says the statement was made and supported, NOT that the thing described is sound."** A criterion with
> present evidence and resolving citations **can still answer its sub-questions badly**, and no verdict column
> can show that.
> ⭐ **AND THE TRIAGE PRODUCED TWO FALSE POSITIVES IT READ TO DISMISS** -- a 462-char "thin" answer that is a
> resolving pointer, and a "self-grade" hit that was *"arm (e) passed"* beside a criterion id. **A triage
> that never produces a false positive is not selecting; it is confirming.**

⛔ **AND THE PACKET'S SCOPE SENTENCE UNDERSTATES ITS OWN WORK BY A FACTOR OF TWENTY-THREE:** *"R70-AC2,
R60-AC2, and the other R\*-AC2s"* -- **that clause carries 45 criteria.** ⭐ **A later reader sizing this L9
from the packet would size 2 and get 47.** Flagged in the slug; recorded here because **a scope sentence is
the thing a successor quotes.**

## 3. THE 52 ROWS, AND ONE FIELD THAT WOULD MISROUTE A MACHINE

40 GRADUATED with a carrier minted in the same commit; 12 INERT evidence/process records DISMISSED; **0
DISARMED**; **34 keep an ARMED disarm block.** ⭐ **THE GRADUATION TRANSFERS THE CLOCK AND DISARMS NOTHING**
-- R-21 applied at scale, and the opposite of the error a sweep made this morning.

⛔ **`W1-S31`'s `disarm_owner` IS A PROSE PARAGRAPH RATHER THAN A SERIAL.** The CVO parsed the serial off the
front and said so, *"because anything routing on that field mechanically would misroute it."* ⭐ **That is the
sixth instance today of a field whose TYPE is not what its name implies**, and the first where the remedy is
simply *a human read it and flagged the shape*. **Ownership as dispositioned: 21 carriers to
`2.0.0_SA_COO~B`, 12 to this seat.**

**`S110` was GRADUATED, not dismissed** -- the CVO's call on a question the packet left open, and the right
one: ⛔ **dismissing it "would have converted an unmeasured control into a clean one by silence."**

## 4. THE FOUR CARRIES, ADOPTED AS MEASURED

1. ⛔ **`S110` -- THE NEGATIVE CONTROL IS VACUOUS WHILE `S100` IS ARMED.** A terminated client and a PERMITTED
   account both return `FIRM_BINDING`, so a refusal-asserting control **"would pass against a route with no
   entitlement checking at all."** ⭐ **Filed by the AE against its own evidence.** This taints the refusal
   side of `rtf-10`/`rtf-12` arm-(f) negative controls, **which carry never-widen halves I signed.**
   ⚠ **Bound travels verbatim: the SERVED-PATH grants are UNAFFECTED, and "no evidence either way" is NOT a
   claim the gap is unenforced.**
   ⭐ **This is the same class as three control errors of mine today and one of the CVO's** -- VACUOUS, WEAK,
   CONFOUNDED, and *aimed at a different threat*. **Five seats, one week's worth of the same defect in a day.**
2. **THE GRANT MOVED** -- live **44 accounts / 19 relationships** against the packet's **33 / 18**.
   ⛔ **A FUTURE ROUND RE-DERIVES, NEVER INHERITS.**
3. **THE LEDGER-RETROACTIVE CLASS** -- two seats, one evening, principal/apply cycles begun **before** the
   change-management ledger was opened. **EXPOSURE, not incident**; both closed clean (residue 0/0/0); ⚠ **the
   uncovered create->delete window was real.** NEVER-2 shape.
4. ⭐ **THE ROUND HEADLINE, and it is the sentence this round should be remembered by:** **THE SCOPE PLANE AND
   THE DATA PLANE HAVE DIVERGED.** An advisor is correctly identified, firm-bound, scope-resolved and told
   exactly how much of the book is withheld -- **and then served NO DATA on any tab.** **The refusal
   vocabulary works; the data paths do not.**

## 5. ⛔ WHAT ROUND 7 OWES, ENUMERATED BY SUBTRACTION FROM THIS ROUND'S OWN RESIDUE

| owed | why it is not this round's |
|---|---|
| **`FWD-11` / `rtf-5`** | PARKED on Andrew's security re-scope. ⛔ **Its un-park condition and owner ride the ORDER, not this analysis** -- a park without them is a filing. |
| **the `S100`/`S110` control repair** | the refusal-side evidence is vacuous until `S100` moves; ⛔ **the CELLS do not re-open, the EVIDENCE does** |
| **the DATA paths** | `performance` DEPENDENCY_UNAVAILABLE, `status` UNSUPPORTED_OPERATION, `export` excluded / still UNEXPECTED (`S104`/`S106`) -- **the headline, cut as work** |
| **the 44/19 re-derivation** | any cell inheriting 33/18 is inheriting a stale grant |

⚠ **NOT OWED AND EXPLICITLY SO: no back-fill of the 34 ARMED disarm blocks.** They are transferred clocks with
named owners, **not a backlog this round created.**

## 6. ⭐ THE METHOD NOTE, BECAUSE IT IS THE ROUND'S REAL YIELD

**Every substantive finding in this round arrived because a seat measured something it had been carrying.**
The AE filed a row against its own evidence. The CVO disclosed a read depth no verdict column shows, and
graduated a row it could have dismissed. The COO re-derived a count it had already reported. ⛔ **And this
seat gated the analysis for days on a census that was wrong in its FIELD and wrong in its LAYOUT, and learned
both only by being contradicted.**

> ⭐⭐ **THE ROUND'S TRANSFERABLE RULE: A NUMBER YOU HAVE REPORTED BEFORE IS THE ONE YOU WILL NOT RE-MEASURE,
> AND A CONTROL THAT PASSES IS THE ONE YOU WILL NOT RE-EXAMINE.** Both failures are invisible from inside the
> seat holding them, and in every instance today the correction came from **a different seat running a
> different instrument.**

---

**PUSH STATE:** measured in the send that carries this analysis.
