# CN_TREE_R3 -- the ONE judged tree for LGIC_CANON round 3

**Issued by** `2.0.0_SA_COO~G` with the round-3 issuance. **Read-only** to every worker.
**Consumers:** `CN-j-8` (judge F), `CN-j-9` (judge G) and `CN-j-10` (judge H) judge exactly these planes; `CN-j-11`
compares them. Every arm judges the SAME planes (ruling R-9 (i)).

THIS FILE CARRIES THE TREE'S FACTS AND NOTHING ELSE. IT DELIBERATELY CONTAINS NO VERDICT, NO AXIS GRADE, NO RULE
NUMBER AND NO STATEMENT OF WHICH RULES THE TREE ENGAGES. The judges are blind and the reach is what they PRODUCE. If
you are reading this as a judge and you expected a rule list, its absence is the design.

---

## Why this tree

Ruling R-9 (iv) requires a tree chosen to reach the canon rules no earlier judging reached. The choice was made at the
round-3 cut by reading `infra/logic/06_CONFORMANCE_LEDGER.md` sections 1 to 4 and `infra/logic/registry/scopes.json`
at CLOUD `809a8b4090`; the comparison is recorded in the issuance commit and is not repeated here, because a judge
reading this file must not learn what the chooser was looking for.

**The tree is the 49FINANCIAL family, with the estate's general-data product bucket beside it.** Object counts and
`newest` dates are the ledger's as of its last census and are **context, never acceptance values**.

---

## The planes

| plane | where | objects | newest | facts the record carries |
|---|---|---|---|---|
| `opal-data-assets/schwab/08242234/bronze/` | monolith | 7,695 | 09-12 | a Schwab master id |
| `opal-data-assets/schwab/08242234/silver/` | monolith | 9,406 | 09-12 | -- |
| `opal-data-assets/schwab/08335338/bronze/` | monolith | 7,473 | 09-12 | a second Schwab master id |
| `opal-data-assets/schwab/08335338/silver/` | monolith | 9,105 | 09-12 | -- |
| `opal-data-assets/schwab/08335338/gold/` | monolith | 4,217 | 08-11 | 2,108 json and 2,108 parquet objects |
| `opal-data-assets/blackdiamond/49f/bronze/` | monolith | 5,582 | 09-12 | scope segment is the firm's short form |
| `opal-data-assets/blackdiamond/49f/silver/` | monolith | 86 | 09-12 | -- |
| `opal-data-assets/blackdiamond/49f/gold/` | monolith | 1 | 07-18 | one object |
| `opal-data-assets/blackdiamond/49financial/bronze/` | monolith | 56 | 09-12 | scope segment is the firm's long form |
| `opal-data-assets/blackdiamond/49financial/silver/` | monolith | 58 | 09-12 | 29 of 58 objects are json |
| `opal-data-assets/blackdiamond/49financial/bronze_legacy/` | monolith | 931 | 08-25 | not written for 17 days at the census |
| `opal-data-assets/blackdiamond/49financial/silver_legacy/` | monolith | 7,921 | 08-25 | not written for 17 days at the census |
| `opal-data-bd/platinum/` | legacy firm bucket | 24,631 | 09-12 | served to the firm's portal users |
| `opal-data-bd/gold/` | legacy firm bucket | 74,841 | 09-12 | 44,782 json; carries `_state/`, `_parity/`, `meta/*_watermark.json` and `manifests/` prefixes |
| `opal-data-bd/silver/` | legacy firm bucket | 7,989 | 09-12 | 7 json; carries `meta/gap_manifest.json` |
| `opal-data-bd/bronze/` | legacy firm bucket | 174 | 09-12 | -- |
| `opal-data-bd/smartx/bronze/` | legacy firm bucket | 242 | 09-12 | 100% parquet |
| `opal-data-bd/code/` | legacy firm bucket | 255 | 08-21 | pipeline code under `bronze/`, `silver/`, `gold/`, `canonical/` |
| `opal-data-49financial/gold/` | firm bucket | 25,577 | 09-12 | 16,067 parquet, 8,859 json; keys start at the tier |
| `opal-data-etfs/silver/` | product bucket | 476 | 09-11 | market data on listed funds; attributable to no firm |
| `opal-data-etfs/gold/` | product bucket | 60 | 09-12 | 32 json, 28 parquet |
| `opal-data-etfs/platinum/` | product bucket | 38 | 09-12 | csv, html, pdf and json reports |
| `opal-data-portal-v2/platinum/advi/49financial/` | shared serving bucket | 19 | 09-01 | routed to the firm's users by the shared advisor router |

**The firm's identity** (`infra/logic/registry/scopes.json`): key `49financial`, class FIRM, long `49financial`,
short `49f`, bucket `opal-data-49financial` (provisioned), masters `08242234` and `08335338`, monolith scopes
`blackdiamond: 49f, 49financial`. The legacy bucket `opal-data-bd` is live and is recorded by the ledger as moving to
`opal-data-49financial`, a move in flight at the census.

---

## What you are asked to do with it

Judge every plane above on the canon's five axes, using `infra/logic/02_DOCTRINE.md` as your source of rules. Your
order names the exact output path, the columns, and what else you are given. Anything you would ask is a surprise row.

---

## Provenance

```
READ:        infra/logic/06_CONFORMANCE_LEDGER.md s.1-s.4 and infra/logic/registry/scopes.json at CLOUD 809a8b4090;
             the state-prefix facts from the canon's own R21 census line
COUNTS:      the ledger's own, as of its last census; context, never acceptance values
NOT READ:    the live S3 plane (this tree is judged from the record, as rounds 1 and 2 were)
CHOSEN BY:   2.0.0_SA_COO~G at the round-3 cut, per ruling R-9 (iv), on the comparison in the issuance commit
```
