# R20 (CTO ruling msg 31754): TXUE's one grounding FAIL, read before the cell is cut

**Reader:** `2.0.0_SA_COO~RV`, 2026-10-08 ~13:3xZ. **Source:** the served page
`s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-08/index.html` (manifest generated 13:08:17Z) and its
manifest. Denominator: 26 account items rechecked over 13 funds (2 per fund); 25 grounded, 1 shown as grounding FAIL
(manifest `ai_grounding.served` = 25). The one is TXUE's "The last 30 days" account.

## The account (as served, the sentences that carry the figure)

Lead paragraph: "Buying was otherwise spread across several names, led by Siemens Energy AG at $2.7 million and
repeated adds ..."

Observed: "Siemens Energy AG was added at $2.7 million, with additional adds at $1.5 million and $1.2 million."

## The check that failed it (as printed on the page)

"Grounding FAIL: figures not in any cited row: $1.2 million; ambiguous figure (matches more than one uncited fact;
cite one): $1.2 million: T10, T11, T12. Shown for audit, not a pass."

Two clauses, one figure. (1) No row the item CITES carries $1.2 million. (2) Three facts the item does NOT cite, T10,
T11 and T12, each round to $1.2 million, so the check cannot attach the figure to one of them on the account's behalf.

## The panel figure

TXUE's panel, table "Leaned into" for the 30-day window, row 4: "Siemens Energy AG +$1.2m, Single trade". The longer
windows show "Siemens Energy AG +$6.9m, Tilt, 4 trades". The account's $1.2 million AGREES with a panel row.

## Verdict

Neither of the two cases the ruling names, exactly. It is not a disagreement in the data: the figure the account states
is on the panel. It is not a defect in the check's arithmetic: the check did what its rule says with an uncited figure
that three facts could explain. It is a defect in what the account was made to do: it stated a figure and cited no row
for it, in a fund where three trades round to the same amount. The fix belongs where the words are made -- the prompt
requires a cited row for EVERY dollar figure in an Observed sentence, or the post-check sends one retry naming the
uncited figure and its candidate rows -- and is the same place R19 is fixed.

## Not read

- Which three trades T10, T11 and T12 are: the fact sheet the account was written against is not on the page or the
  audit page (0 occurrences of each id in `audit.html`); it is in the stored account object, not opened here.
- Whether the same shape (an uncited figure) exists in an account that PASSED because only one fact matched it: the
  check attaches such a figure silently. If so, 25 "grounded" overstates how many accounts cite every figure. One read
  of the stored account objects answers it; proposed as a clause of the round-28 cell's check.

## Also seen in this account (R19)

"The top R30 contributor", "contributed -0.25% in R30": the system's period code reaches the reader, as row C-S83 says.
