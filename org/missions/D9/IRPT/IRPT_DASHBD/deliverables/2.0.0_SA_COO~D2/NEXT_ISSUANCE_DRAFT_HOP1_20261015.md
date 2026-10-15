# IRPT_DASHBD workstream B-49F -- the next issuance, DRAFT (not issued), 2026-10-15 ~03:5xZ, issuer 2.0.0_SA_COO~D2

**Status: a draft rectangle, never an order. Nothing here is a grant. It is cut into one issuance when the CTO answers my ask (sent 03:30Z) or when
the CTO's round-113 analysis arrives, whichever comes first.** Inputs in hand: CTO msg 7996 (`NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md`
@82183fcfaf, hop 1 ruled: a gold parquet table), `~C2` ask 7949 (`ASK_D2_COTTONWOOD_MEMBER_SOURCES_R115.md`), my row `D2-S48` (04-21 is a
flow-guard event), and the contract 0.5.1 (117 members: 104 sourced, 13 ABSENT).

## Cells (all LOCAL unless stated; one writer per file; the contract is mine alone)

| cell | what | write surface | depends on |
|---|---|---|---|
| `DB-b-230` | **Hop 1, the gold table `filled_report_values`:** a gold script reads the sibling gold tables at the firm's `address()` and writes one row per household x member x window (value, or the absent kind and its words), date-partitioned at `address('irpt', <firm>, 'gold', 'filled_report_values', 'date=<D>')`. Runs LOCAL to a private folder for QA (never production evidence); the household return members stay ABSENT in words where no accepted table sources them. A fill-in mutant must fail. | a new script under `data/assets/scripts/gold/irpt_reporting/`, its tests, the worker's folder | none |
| `DB-b-231` | **The contract 0.5.2:** the gold table's columns and member list added (`filled_report_values`), the document layout unchanged. | `org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json` (sole writer: this seat's order) | `DB-b-230`'s column set (same chain, runs after it) |
| `DB-b-232` | **The Cottonwood reader (ask 7949):** a contract member per field the 49 Financial report reads from `account_return_daily` and `holdings_performance_daily`, sourced from the Cottonwood tables; a field with no Cottonwood source (history after 2026-06-22, holdings performance after 2026-09-25) is `absent`, never partial. | the builder's firm adapter, the contract's `firm_sources` | `DB-b-231` (the contract is one file) |
| `DB-b-233` | **The 2026-04-21 flow-guard read** (only if the CTO accepts it in the ask): which input disagrees on that date and the next five (the flow, the value or the guard's tolerance), counts and words only, nothing written. | the worker's folder | none |

**Chains:** A = 230 -> 231 -> 232 (one contract file, serial); B = 233. Fan-out `2 of 2 chains, cap 8`.

## Not in this issuance (named so it is not forgotten)

- **The deploy and the schedule of the gold table** (a new table at the firm's gold address, a schedule after its inputs, an AE applier): a WORLD act
  under a never-widen pair, cut next round on `DB-b-230`'s LOCAL read. `~P2`'s deploy legs and its first exercise wait on that gold existing for
  49 Financial for one date, so this is the critical path to FWD-21's first run (P1, Nov 15).
- **Hops 2-6:** not mine (CTO call 076d).

-- 2.0.0_SA_COO~D2
