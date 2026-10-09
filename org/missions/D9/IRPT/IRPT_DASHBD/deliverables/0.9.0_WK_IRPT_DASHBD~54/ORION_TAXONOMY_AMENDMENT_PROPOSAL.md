# Orion cashflow taxonomy -- amendment proposal for two flow classes (TO-DB-b-77, E5, row W49-S3)

Author: 0.9.0_WK_IRPT_DASHBD~54 | Round 37 | Status: PROPOSAL. `data/inf/scripts/silver/orion_cashflow_taxonomy.yaml` is NOT edited
by this cell; it governs as ratified until the CTO rules (ADDENDUM 5). Law applied: CLAUDE.md rule 24, `rcg/rulings/RULINGS.jsonl`
R-0006 and R-0009. Evidence: `MEASURED_EFFECT.json`, `TOKEN_CENSUS.json`, both beside this file.

## The proposed change (one line)

Add two OPTIONAL per-entry keys, `account_boundary: in|out` and (on the two tax entries only) `account_boundary_when: before_tax_return`,
to four existing entries -- Internal Account Journal In (`in`), Internal Account Journal Out (`out`), Federal Tax Withheld (`out`,
before-tax), State Tax Withheld (`out`, before-tax) -- and change no `bucket`, no `nna_direction` and no other entry.

## What the two classes are, and why the order exists

| Class | Ratified `bucket` | What the round-36 return adapter did | Rows in the sample's flow ledger (Complete status, full history) |
|---|---|---|---|
| Internal Account Journal In / Out | Internal | counted as account-boundary flows | 1,810 in, 1,357 out |
| Federal / State Tax Withheld | Return | counted as account-boundary outflows | 2,868 |

The departure lives today only in `orion_sources.json` (`inter_account_comment`, `tax_withheld_comment`), so two files disagree with no
ruling between them. Two facts frame the tax half. First, the vendor figure the adapter ties out to is reported Before-Tax and Net of
Fees (`reported_figure_methods` in `~49/INF_RETURNS_TIEOUT.json`): a before-tax comparison removes withholding from the return, so
treating it as a flow is a property of the return BASIS, not a re-description of the transaction type. Second, the choice of flow set
was made by fit to the vendor figure and is a HELD reading, not a vendor rule (`annualisation_basis` is held in the same file).

Alternatives weighed:

1. Move the buckets (journals Internal to NNA; tax Return to NNA out). REJECTED: `INF_C_01.canonical_nna.py` builds the served NNA
   set from `bucket == NNA`, so this would move served NNA and reverse CTO Items 1 and 2 of the 2026-05-11 ratification.
2. Add a new `bucket` value. REJECTED: `a05_ref_txn_classification.py` fails loud on any bucket outside its rule list, so the four
   entries would land UNRESOLVED.
3. Leave the departure in the adapter only. This is the status quo and the defect W49-S3 names (an unratified second truth).
4. Additive optional keys (PROPOSED): the only option that leaves every existing reader's input unchanged.

## MECE -- over the declared domain, by subtraction from a printed denominator

Declared domain: the 48 `type_desc` entries under `types:` in the taxonomy at HEAD (printed by parsing the file: Internal 19, Return 17,
NNA 9, CorporateAction 3 = 48; the file's own title and header say 43, which pre-dates the 2026-08-11 five-code amendment -- row
W54-S1). The domain was falsified before use by one unscoped read of the tax term over the whole corpus
(`comp-find -i --corpus all`, 64,024 files scanned): the bare token `Tax Withheld` returns 92 hits against 27 for
`State Tax Withheld` and 15 for `Federal Tax Withheld`, so the unqualified term reaches a third member (Foreign Tax Withheld) that
the domain must account for. That is why the census tokens are the full word-bounded names.

Subtraction, 48 entries: remove the 9 NNA entries (already boundary flows through `nna_direction`) = 39. Remove the 2 journal and the
2 Federal/State entries this proposal tags = 35. Of the 35 left, the members that plausibly cross an account's boundary by name are
THREE: Foreign Tax Withheld (33 audited rows), Foreign Dividend Tax (33) and Tax Credit (2). They are NOT tagged, and that is a DECLARED
exclusion, not an oversight: the round-36 sample carries no Foreign class in its flow ledger, so no fit was measured for them (the
adapter keeps them inside the value, as the 49 Financial producer keeps its foreign-tax withholding). Management Fee and Fee Credit are
also left untagged because the adapter handles the advisory fee on its own gross/net rail. The remaining 30 entries (exchanges, DRIP,
valuation adjustments, income, corporate actions, other fees) are left untagged on the ratified rationale; that is read from the
taxonomy's own `rationale` text, not re-measured, and is marked INFERRED. Within the 4 tagged entries the values are mutually
exclusive (`in` or `out`; absent = no account-grain treatment); the key and its qualifier were censused as new tokens and collide
with nothing (0 hits each).

## SAME GRAIN

The ratified taxonomy answers a FIRM-grain question: its journal rationale is "Journal In = Journal Out firm-wide (paired)",
which is true because the legs net to zero across the firm. The return adapter answers an ACCOUNT-grain question: one reported return
per account-window, where a journal leg leaves one account and arrives in another and so crosses the boundary of each account it
touches. The proposal does not stretch `bucket` to cover both. It names the account grain in the key itself (`account_boundary`) and
documents that `bucket` and `nna_direction` keep their firm grain. Withheld tax is the same: at firm grain it is a friction ruled into
Return (Item 2); at account grain the cash leaves the account. Two grains, two keys, no row asked to carry both in one field.

## INTENT COHERENCE

One axis, one intent. `bucket` carries "what is this row for firm cashflow accounting" (NNA / Internal / Return / CorporateAction).
`account_boundary` carries one different intent: "does this row's cash cross the account's own boundary, and which way, for a return
computed on that account". Neither key is overloaded. The pre-existing precedent is the second axis the estate already built:
`a05_ref_txn_classification.py` keeps `taxonomy_bucket` (ratified, verbatim) apart from `gips_class` (the TWR external-flow axis it
mints), and its docstring states the rule-24 intent-coherence judgment for doing so. The tax qualifier exists to keep intent coherent:
a withholding is a boundary outflow only when the return is computed before tax. An after-tax return leaves it inside the value. So the
tax entries carry `account_boundary_when: before_tax_return`, and a consumer on another basis ignores them. OPEN for the CTO, not
resolved here: `a05` classes taxes INTERNAL on `gips_class` and unmatched journals EXTERNAL-BY-DEFAULT in `c00_flow_ledger.py`. Those two
are different grain and basis statements, and this proposal does not touch either; whether the estate wants ONE account-grain TWR flow
axis is a later ruling.

## STATE COHERENCE -- the values this remedy does NOT move

Not moved (named, with the reader that proves it, read not run):

- `bucket` on all 48 entries. Journal In / Out stay Internal. Federal, State, Foreign Tax Withheld, Foreign Dividend Tax and Tax Credit
  stay Return. The 9 NNA entries are untouched, so `INF_C_01.canonical_nna.py` (reads `bucket`, `trans_type_desc`/`type_desc`,
  `nna_direction` only, via `yaml.safe_load`) builds the same inflow and outflow sets, and served NNA does not move (Item 2's
  NNA-outflow reduction stays).
- `nna_direction`: not set on any of the four entries.
- `a05_ref_txn_classification.py` reads `entry["bucket"]` and `entry.get("nna_direction")` and nothing else, so `gips_class`, the
  ref table and `c00_flow_ledger.py` (which consumes that table) are unchanged by new keys. Readers of `nna_direction` in code: three
  files (`INF_C_01`, `a05`, `c00`), censused in `TOKEN_CENSUS.json` (28 hits across 10 files in all).
- `row_count_audit`, `merged_from_categories`, the ratification history, and the 43-versus-48 header text: untouched.
- The firm's NNA, Internal and Return consumer outputs, and everything under `data/`, `infra/` and `portal/`: this cell edits none.

MOVED, and nothing else: the return adapter's flow set, which would read these keys from the ratified file instead of from
`orion_sources.json`. That adapter edit is a follow-on act outside this cell. Its measured effect on the round-36 sample is below.

## Measured effect on the returns (`MEASURED_EFFECT.json`)

One sample, one denominator: the round-36 tie-out, 562 account-windows, 0.35 pp, 252-day annualisation, the 2026-10-08 snapshot. The
rerun reproduces round 36's published headline exactly (24 gross, 421 net, miss classes 79/400/55/4, same output hash). 483 of the 562
are computable under every flow set; the other 79 have a broken link and can never be within.

| Flow set | Net-of-fee basis, within of 562 | Gross basis, within of 562 |
|---|---|---|
| RATIFIED (contributions and distributions only) | 293 | 43 |
| + journal pair only | 348 | 41 |
| + Federal/State tax only | 350 | 27 |
| PROPOSED (both) | 421 | 24 |

Net basis is the like-for-like one (the vendor figure is Net of Fees). The proposal adds 128 account-windows within tolerance on it, 55
from the journals and 57 from the tax pair with the remainder from their interaction. The gross basis FALLS from 43 to 24 under the
proposal, because the gross figure adds the fee back and is not comparable to a Net of Fees vendor figure; it is recorded, not preferred
(row W54-S2). These are fits to one sample at one snapshot: a measured count, not a vendor rule.

## Asks of the CTO

1. Rule on the additive keys (`account_boundary`, `account_boundary_when`) as the amendment, or on one of the rejected alternatives.
2. Rule whether the tax pair is in scope at all, given the before-tax qualifier, or whether only the journal pair is amended.
3. Rule the three declared-unmeasured members (Foreign Tax Withheld, Foreign Dividend Tax, Tax Credit): leave inside the value, or
   measure first.
