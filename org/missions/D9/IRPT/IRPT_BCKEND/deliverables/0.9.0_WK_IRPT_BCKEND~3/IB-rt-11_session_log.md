# IB-rt-11 session log -- `0.9.0_WK_IRPT_BCKEND~3`

Worktree `/c/tmp/wk-irpt-2-3c`, branch `wk-irpt_bckend-2-3c`, cut at `72db64c153`.
Order handed pending at 2026-09-12T01:14:33Z; the amendment's B1-B7 governed.

## What the order asked and what the tree already had

Round 1 (IB-s-7) left a deterministic parser whose own fixture manifest named the four shapes
it could not represent: **non-USD currencies, nested/subtotalled groupings, multi-sheet
workbooks**, and it had no notion of a document that states its total twice. This cell fills
exactly those four. Nothing was rebuilt: `parse.py`, `corrections.py`, `settings.json` and the
five round-1 specimens are extended in place.

## The design decision the acceptance forced, and it was the right one anyway

Arm (d) requires the five round-1 specimens to parse **byte-identically**. The first build put
the currency verdict into `row_context`, which is inside `to_json()` -- and one round-1
specimen (`holdings_share_class.csv`) has a money column, so its digest moved. Measured, not
guessed: the comparator extracts the parser at a pin from git and runs both in fresh
interpreters.

The fix is not a suppression. The currency evidence belongs in its **own addressable place**
(`money_rows`, with `currency_evidence_digest()`), carried into the revision's provenance and
printed by the battery, because `to_json()` is the ROUND-1 CONTRACT SURFACE: a specimen whose
holdings, findings and totals are unchanged must still serialize identically, or every consumer
that pinned a digest is re-pinned for a cell that changed nothing they read. After the move,
5 of 5.

## The three premises I had to measure rather than assume

1. **`Market Value (CAD)` did not match the unit vocabulary at all.** `UNIT_HEADERS` is an exact
   lowercased match, so the parenthetical made the column invisible and the currency question
   was never asked. The unit lookup now reads the header's STEM and the currency coordinate
   keeps the FULL header -- inspecting a coordinate is not the same as putting the question.
2. **`_clean_number` stripped a bare `$` and nothing read it anywhere**, so `C$120,000` failed
   to parse and a CAD cell reported `UNPARSEABLE_QUANTITY` -- a true refusal for the wrong
   reason, useless to whoever has to fix it. Leading symbols are now removed from an ENUMERATED
   list that fails closed, and `source_value_verbatim` still carries the original text the
   symbol is read from.
3. **The stated total needed the same currency question as a holding.** Without it the CAD
   specimen produced a `TOTAL_MISMATCH` of the entire portfolio -- arithmetically true, and
   completely misleading.

## Where the check runs vs where the value is consumed

The issuer's note arrived mid-build: *"A CHECK THAT RUNS IN THE WRONG ENVIRONMENT PASSES ON A
BROKEN ARTIFACT."* The census answer is stark and is printed on arm (e): **`parse.py` is
declared by 0 of 214 functions**, so there is no runtime at all. Arm (e) does the closest
available thing -- the flat `/var/task` layout, a fresh interpreter, `-I`, the repo stripped
from `sys.path` -- and adds the arm that matters: with `settings.json` absent, the parser
REFUSES by name rather than defaulting to USD. `load_intake_controls` was changed to make that
refusal explicit, because the alternative relabels precisely when the policy fails to ship.

## Rows filed

| id | class / hazard | what |
|---|---|---|
| `W3-S34` | OBSERVATION / INERT | this cell's ordered `settings.json` edit moved a declared build input of `irpt-ycharts-generate` 20 minutes after slot ~2 deployed it. Measured from the S3 artifact: the `settings` subtree and `cautions` are byte-identical; only the sibling `intake_controls` key differs. |
| `W3-S35` | OBSERVATION / ARMED | the contract's `corrections` item is `additionalProperties:false` with four keys and no time field, so the WHEN cannot travel in the contract. |
| `W3-S36` | OBSERVATION / ARMED | `parse.py` is packaged by 0 of 214 functions; the first packaging must carry `settings.json` AND `fixtures/holdings/security_mapping.json` beside it. |

## Bounds honoured

No deploy, no Terraform root, no AWS write, no mailbox read, no vendor call. No credential, no
client name, no account number and no e-mail address in any specimen. Every specimen is
synthetic and says so on the arm; none was manufactured to resemble a real client's workbook.
