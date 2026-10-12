# IB165-1 -- the names of the opening and closing value members

**Decision: CONTRACT_NAMES_NONE.** No contract file enumerates the members of `optional_facts.value_facts`, so there is no ground to rename either side. No product file was edited.

Base: `a7e7a53715`. Record: `IB165-1_value_member_names.json`.

## The two sets of names

| Names | Emitters (cite) |
|---|---|
| `start_value`, `end_value` | `performance/holdings_gold.py:273`, `performance/f49_engine.py:229`, `performance/orion_adapter.py:169-170`; fixture `narrative/fixtures/performance_report_inf.json:443-444` |
| `beginning_market_value`, `ending_market_value` | `performance/bd_adapter.py:194-195` only |

So three of four producers use `start_value` / `end_value`; Black Diamond alone uses the market-value names. The portal adapter (not read here) is said by the row to read the market-value names, which holdings, 49F and Orion answers do not carry.

## What the contract says

Both copies of `PerformanceReport.schema.json` (`docs/contracts/investor-reporting/v1/...:332-337`, `infra/aws/lambda/investor-reporting/_contracts/...:328-334`) type `value_facts` as object-or-null with no `properties`; the description reads "start and end values only when supported". Both fixtures carry `value_facts: null`. No other file under the two contract folders names either pair. The contract is open on these names.

## In-repo readers

`test_f49_engine.py:97` reads `start_value` / `end_value`; `normalize.py:245` reads a `start_value` of its own cells dict (not `value_facts`). Nothing in the repo reads the market-value names.

## For the CTO

To close the gap the contract must first name the members. Whichever pair is named, the side that disagrees renames: naming `beginning_market_value` / `ending_market_value` moves three producers (a served-name change under a never-widen pair, plus the f49 test and the fixture); naming `start_value` / `end_value` moves `bd_adapter.py` and the portal adapter.

Not established: the portal adapter's reads; whether another report schema exists outside the two folders read.
