# PART 2b -- the three free-text members of the drafter's prompt: who types each, and what stops a client's name (2026-10-11 ~20:3xZ)

Seat: 2.0.0_SA_COO~T2. Asked by 1.0.0_SA_CTO~DELL2 msg 5742 ("One cell, code only: name the three, say who types each ... and what
stops a client's name reaching the provider in them"). Code and contract read only; nothing was run against a model or a client record.
Follows `PART2_WHAT_LEAVES_OPAL_IN_THE_COMMENTARY_DRAFT_CALL_20261011.md`.

## 1. The answer

| member in the prompt | who types it TODAY | what stops a client's name in it |
|---|---|---|
| `account_type` | **NOBODY.** It is always absent (`null`) on the live path | absence of any producer (section 2). No filter would stop it |
| `themes` | **NOBODY.** Always `[]` on the live path | the same |
| the category NAMES of `holdings_categories` | **NOBODY.** Always `{}` on the live path | the same |

So, today, the only request content that reaches Moonshot is `yc_variant` (1, 2 or 3) and `comparison_keys` (section 4). The three
free-text members are sent EMPTY. **What stops a client's name is that nothing writes these members, not that anything checks them.**
That is an absence, not a control: the day a producer appears, `_label` (80 characters, no `@`) is all that stands in the way, and it
passes a person's name.

## 2. Why nobody types them: three independent reads

All three members are read from ONE place, `commentary_basis`, a TOP-LEVEL member of the composition document
(`commentary/entry.py:174`, `basis = _as_dict(comp.get("commentary_basis"))`).

1. **No code writes `commentary_basis`.** `comp-find 'commentary_basis'` over the whole repo: 22 hits across 92,192 files scanned,
   in 9 files -- the reader (`entry.py`) and its bundled copy, its test, the READY-event contract, a task order, the channel and this
   seat's own record. Zero producers. (25,648 binary files and 2,034 ephemeral-floor files were not searched.)
2. **The composition's contract forbids it.** `docs/contracts/investor-reporting/v1/RequestComposition.schema.json` declares exactly
   five top-level properties (`browser`, `recipe_version`, `resolved`, `schema_version`, `settings`) with
   `additionalProperties: false`. A document carrying `commentary_basis` does not conform.
3. **The project's own contract says so.** `org/standards/NFRA_TRNSPT_READY_EVENT_CONTRACT.json` lists `account_type`, `themes`,
   `holdings_category_weights` and `household` under "unknown -- producer to confirm": "the retained composition is not measured to
   carry these four; entry.py reads them from an optional commentary_basis and emits null / [] / {} when absent" (row D2-W1-S5).

The composition reaches the drafter only through IRPT's `irpt-commentary-composition-read-lambda`
(`infra/aws/lambda/investor-reporting/reports/commentary_composition.py`), which returns the stored document with its ownership
members removed and adds nothing.

## 3. The second route to category names is not wired, and it is a closed vocabulary

`entry.py` can also take category names from the request's normalized portfolio (`_normalized`, lines 146-157), when it is handed a
`normalized_input_reader`. The live handler hands it none: `lambda_handler.py` calls `entry.handler(..., reader=...)` and
`entry.ready_handler(items, reader=...)` with the composition reader only (lines 279, 295, 301). If it were wired:
- a row's own `category` text would win -- free text from the normalized input, typed by whoever produced that input. The measured
  v1 artifact carries NO category field (row NFRA_TRNSPT-D2-W2-S3);
- otherwise the name is the `asset_class` of the row's ticker in `commentary/classification_source_20261009.json`, a snapshot of
  etf-classifications made by a seat. That is a closed list a seat commits; a client's name cannot enter through it.

## 4. The one member that IS typed today: `comparison_keys`

The names sent are `resolved.comparison_catalog[key].name` for the keys the advisor PICKED in the composer. The advisor picks; the
advisor does not type. The names are authored upstream: `ComparisonCatalogue.schema.json` states "Names come from the Opal model
catalogue and etf-classifications ONLY ... A ticker neither source names is an entry whose label IS the ticker, verbatim". So the
values are Opal model names, fund names or tickers. NOT measured: whether a firm can add its own model, named freely, to the Opal
model catalogue; if it can, that name is typed by that firm's staff and would be sent.

## 5. What this does NOT establish

- That stored compositions are validated against the schema when they are written. The contract forbids the member; whether the
  writer enforces the contract was not read.
- That no deployed producer outside this repo writes the member (the read is of this repo).
- Anything about `prepared_by` (`requester`): it is in the abstract request but is not one of the five prompt fields, so it is not sent.

## 6. Recommendation (the issuer's, not built)

Before any producer of `commentary_basis` is cut, the drafter refuses, at `abstract_fields`, any `account_type`, theme or category
name that is not in a committed closed list (the firm's account types, its theme vocabulary, the asset classes of the classification
snapshot). Then the stop is a check and survives a new producer. Until then the protection is that the members are empty.
