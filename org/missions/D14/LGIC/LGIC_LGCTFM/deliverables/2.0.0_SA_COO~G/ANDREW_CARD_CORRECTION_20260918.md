# CORRECTION to ANDREW_CARD.md -- read this beside the card, not instead of it

**The card:** `org/missions/D14/LGIC/LGIC_LGCTFM/deliverables/0.9.0_WK_LGIC_LGCTFM~3/ANDREW_CARD.md` @`554d1de05b`.
**Delivered to Andrew 2026-09-18 ~00:3xZ**, copied to `1.0.0_SA_CTO`.

**CONTENT HASH, per R-40 -- the card this correction is about, bound to its bytes and not to its path:** blob
`5a5f3e68bac86fe7d84c90ce42d16b0ceb5ddd5c`, **4,635 bytes**, read with `git rev-parse HEAD:<path>` and
`git cat-file -s`.

One measured caveat on the instrument, stated because it bit this seat mid-write: **`git hash-object <path>` returned
the SAME blob id** (it applies the clean filter for a tracked path), **but `wc -c` on the checked-out file reports
4,696 bytes, not 4,635** -- `core.autocrlf=true` renders the file CRLF in the worktree while the record is LF. So on
this box the HASH is safe from either instrument and the BYTE COUNT is not. Where a size is quoted as evidence it
comes from `git cat-file -s`.

## THE ONE LINE THAT WAS WRONG

The card's **RECOMMENDATION** reads:

> Accept the list as printed. The ranking rule is applied consistently: **the two rows touching a live,
> client-facing surface** sit above everything else, and every row in the top ten plus the full 179-row order was
> reproduced independently (not by whoever wrote the ranking engine) and matched the rule exactly, denominators below.

**There is exactly ONE such row, not two.** It is `T-0001`, the `opal-data-bd` S3 bucket.

**READ THE RECOMMENDATION AS:** *"the ONE row touching a live, client-facing surface -- T-0001, the `opal-data-bd`
bucket, 1 of 179 -- sits above everything else, and every row in the top ten plus the full 179-row order was
reproduced independently and matched the rule exactly."*

## WHAT IS NOT AFFECTED, measured rather than reassured

| claim | status |
|---|---|
| the card's TABLE of the top ten | **correct, unchanged** |
| the card's own analysis sentence (*"Rank 1 is the only irreversible-or-client-facing-or-live row in the top ten"*) | **correct** -- it already said ONE |
| the 179-row order | **correct**, re-derived independently twice |
| the 20-of-184 reproduction | **correct**, not impeached |
| the DECISION the card asks for | **unchanged** |

So the ranked list is still the right list, and the decision in front of Andrew is the same decision. What was wrong is
the summary written for the reader who decides without checking -- which is the half that matters most on a card.

## THE MEASUREMENT

Over **all 179 tensions** of the contract the card ranks
(`workflows/legacy_transform/blackdiamond-49financial/20260917T202556Z-bb29248/contract.json`):

```
  tensions ........................ 179   (denominator)
  irreversible == true .............. 0
  client_facing == true ............. 1   [T-0001]
  live == true ...................... 1   [T-0001]
  both client_facing AND live ....... 1   [T-0001]

  client_facing VALUE HISTOGRAM ..... {True: 1, False: 177, None: 1}
```

The histogram is why the `1` is trustworthy and a bare count would not have been: three distinct values prove the
accessor is reading a real cell rather than returning a constant.

**Found by `1.0.0_SA_CTO`** (msg 97745). **Re-derived here on a different accessor before this record was written**,
and that was not ceremony: the CTO's own message records that its FIRST accessor read the factor values at the top
level of each tension and returned **0 client_facing rows across 179** -- a confident zero that would have
contradicted the card entirely. The values live under `factors.<name>.value`. This seat printed
`tensions[0].factors`' real key set (`client_facing`, `irreversible`, `live`, `rules_colliding`) before believing any
count.

## WHY THIS IS A SEPARATE FILE AND NOT AN EDIT TO THE CARD

Two reasons, in order of weight:

1. **The card is already in Andrew's hands.** A silent edit to a document a reader is holding is not a correction; it
   is a different document with the same name. `1.0.0_SA_CTO`'s instruction was explicit: *"the correct act is a
   correction that reaches him BESIDE the card rather than a silent rewrite of a document already in his hands."*
2. **The gate refused the edit, correctly, and the refusal is worth recording.** This seat DID first edit the line in
   place. `.tools/owned-paths-validate.py` clause 4 (`ADHC_OWNPTH.004`, lane `TREE_DELIVERABLES`) refused the commit:
   *"deliverables/0.9.0_WK_LGIC_LGCTFM~3/ANDREW_CARD.md ... agent=2.0.0_SA_COO~G not in permitted_agents"*. A worker's
   deliverable folder admits exactly that serial. The edit was reverted with `git checkout --` and nothing of the
   worker's was changed. **The gate reached the better answer than the issuer did**, and the audited override that
   would have forced it through was not used.

## THE CLASS, because this is the fourth instance in one evening

`LGIC_LGCTFM-S6` files it. The family: `LGIC_LGCTFM-S3` (a criterion reading PASS on bytes its cell did not produce),
the CTO's own `S25R4-AC5` (a criterion id that exists in no order file and survives a count check), `LGIC_ENFORCE`
`S61` (a quote whose single clean grep hit is the wrong file), `LGIC_ENFORCE` `S62` (a right total with a wrong
split), and this one (a right table with a wrong summary). In every case the **evidence was sound and the sentence
above it was not**, and in every case a **second seat** caught it -- never the author.

**The cheap control for any future card:** state the claim as a **count with its denominator** (`1 of 179`), never as
a word (`the two rows`). A number invites the check a word does not.

**Not claimed:** that the card cell's own criterion `v1-card` should have caught this. That arm grades PRESENCE -- the
ranking rule verbatim, 10 of 10 tension ids -- and grading a prose summary against the population it characterises is
a NEW criterion, not a repair of that arm. It belongs to whoever cuts the next card cell.
