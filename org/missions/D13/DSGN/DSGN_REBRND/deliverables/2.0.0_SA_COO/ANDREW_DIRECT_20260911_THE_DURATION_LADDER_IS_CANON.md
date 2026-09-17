# ANDREW-DIRECT 2026-09-11 -- THE DURATION LADDER IS CANON

**Recorded by:** `2.0.0_SA_COO~D` | **Project:** `DSGN_REBRND` | **Reaches:** cell `RB-s-4`, and the
`RB-s-7` contract when it is cut.

---

## THE WORDS, VERBATIM AND IN ORDER

Andrew's question, arriving mid-turn while this seat was building a replacement criterion:

> "UST orange is canonical and ULT red is canonical, what is the nature of your interest in those two?"

On being shown that `FactorTilts/constants.ts` still carried the full orange-to-red ladder while three
other writers had been moved to a navy ramp:

> "all five are canonical, revert and add FactorTilts as the sixth. These are the only colors that truly
> must stay locked in."

On `aum.ts`, whose keys are `'Aggressive' / 'Conservative' / 'Intermediate' / 'Short-Term' /
'Ultra Short-Term'`:

> "Those are earlier names, Aggressive is ULT, Conservative is LT, the rest are obvious"

> "That's right, Conservative is LT which is Blue. That must remain consistent. I thought we had already
> scanned through and changed any old names to the new ones but im not surprised there are little
> holdouts."

On sequence:

> "They must always be listed in the same order with same colors, it is duration order, UST ST INT LT
> ULT. Always this way, left to right."

> "or top to bottom if in a vertical context"

---

## WHAT IS LOCKED

| rung | constant | hex |
|---|---|---|
| UST | `PALETTE.orange500` | `#F97316` |
| ST | `PALETTE.amber500` | `#F59E0B` |
| INT | `PALETTE.green500` | `#10B981` |
| LT | `PALETTE.blue500` | `#3B82F6` |
| ULT | `PALETTE.red500` | `#EF4444` |

**VALUE and ORDER are both locked.** The sequence is always `UST, ST, INT, LT, ULT` along the reading
axis -- left to right when horizontal, top to bottom when vertical.

**AND THE SCOPE OF THE LOCK IS A GRANT AS MUCH AS A CONSTRAINT.** *"These are the only colors that truly
must stay locked in"* -- so every other colour in this round remains movable, including the semantic
palette, the surface ladder and the sentiment ramp.

---

## WHAT THIS CORRECTS, AND WHOSE ERROR IT WAS

`RB-s-4` was issued by this seat carrying the sentence *"Five unrelated hues for a strictly ordered
quantity is the defect this cell exists to remove."* **That sentence was wrong and it was mine.** The
five hues are firm convention -- the colours MEAN the models. I took "ordered quantity implies one hue"
from design theory, wrote it into a cell as a named defect, and never tested the premise against what
the estate actually holds. This is Rule 24's domain trap at the level of the CELL rather than the
criterion: choosing the domain is itself a claim, and I never falsified it.

The tell was sitting in the worker's own output and I read past it: `modelPortfolioColors.ts` still says
`// Ultra-Long Term (ULT) - Red` beside a navy hex. A colour with a NAME in a comment is a colour
somebody chose on purpose.

**The worker `0.9.0_WK_DSGN_REBRND~1` is not at fault and its conduct was correct twice over:** it
recorded `RB4-AC4` as a mechanical `FAIL` rather than reinterpreting the verdict, and it refused to edit
a categorical palette to turn a criterion green. Had it done either, the premise error would have
shipped green.

---

## THE SIX WRITERS

| # | writer | at `0e87cb9f99` | required |
|---|---|---|---|
| 1 | `holdings-shared.tsx` `PORTFOLIOS` | navy ramp | REVERT to canon |
| 2 | `HoldingsTab.tsx` `BOOK_COLOR_CYCLE` | navy ramp | REVERT to canon |
| 3 | `chartColors.ts` `MODEL_COLORS` | navy ramp | REVERT to canon (`AGG` keeps `opalIndigo`) |
| 4 | `modelPortfolioColors.ts` `MODEL_PORTFOLIO_COLORS` | navy ramp | REVERT to canon, aliases included |
| 5 | `FactorTilts/constants.ts` | **already canon** | leave as-is |
| 6 | `aum.ts` `getModelColor()` | **never was canon** | bring to canon + fix the shadowing bug |

Writer 6 was off canon BEFORE this round and three of its five are the wrong hue outright -- `LT` renders
green where canon is blue, `INT` purple-blue where canon is green, `UST` teal where canon is orange. It
also carries an independent lookup bug: `modelName.includes(key)` walks insertion order and
`'Short-Term'` precedes `'Ultra Short-Term'`, so `'Ultra Short-Term'.includes('Short-Term')` is true and
every UST model takes ST's colour. The teal line has never rendered.

**NOT authorized by this ruling:** renaming the legacy keys. `getModelColor` is called with names from
the API, so a rename without knowing what the API sends breaks the lookup. The name holdouts are an
observation for L10.

---

## THE INSTRUMENT

`task-orders/rb4-canon-check.py`, four arms, because the ladder is written in four grammars and an
instrument that reads one certifies the others clean while they are broken:

- **ARM A** rung-LABELLED sites (`id: 'UST'`, `name: 'Ultra-Short Term'`).
- **ARM B** POSITIONAL arrays with no rung token at all (`BOOK_COLOR_CYCLE` -- the writer that actually
  renders the `/positioning` chips -- and `MODEL_COLORS`).
- **ARM C** EARLIER-name keys. **BOUNDED, and the bound is load-bearing:** `'Intermediate'` and
  `'Short-Term'` also name maturity buckets in the sub-asset-class palettes, which are a deliberate
  green-by-duration ramp and are NOT the model ladder. Fired unbounded, arm C reported
  `holdings-shared.tsx:82` and `chartColors.ts:289` as off-canon when they are a different taxonomy.
  `'Aggressive'` and `'Conservative'` are unambiguously model names, so arm C fires only in a file
  carrying one of them.
- **ARM D** ORDER, on every ordered array. A keyed lookup `Record` is exempt and the exemption PRINTS.

Exercised before issue, on three trees: the canon tree, the navy tree (names all 13 off-canon lines plus
both positional writers), and a tree with no `portal/` at all -- which reads `CANON-BROKEN`, so an empty
sweep cannot score as a clean pass.

`task-orders/rb4-ramp-check.py` grades the half of the original premise that survives: the sentiment
scale is NOT canon and its rainbow IS a reading error. Current tree `ONE-HUE-RAMPED`; pre-cell tree
`RAINBOW-REMAINS`.
