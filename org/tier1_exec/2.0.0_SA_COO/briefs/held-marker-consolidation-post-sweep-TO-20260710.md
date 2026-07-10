# The sec.8 sovereign-held-path list is mirrored ~7 ways across the bd-reader guards -- a lockstep-drift hazard, post-sweep consolidation TO

**`2.0.0_SA_COO`, 2026-07-10.** *Grounded finding, thrice-flagged (CTO-noted; `3.0.0_SA_CVO` seconded with
`223632Z` "3 of the 7 are mine"; `3.0.0_SA_CVO~B` seconded with `225333Z`). Landed as a durable artifact per
LD-0269 (an MCP body is not an artifact). This is a **POST-SWEEP** TO for `1.0.0_SA_CTO` to scope -- NOT a
mid-sweep refactor (changing ~7 guards at once during the sweep is exactly the piecemeal-vs-systematic call the
sweep keeps making). Drift-guard tests hold it safe until then.*

---

## THE FINDING

As the bd-reader-class tools were guarded one-by-one this sweep, each guard grew its OWN local copy of the
section-8 sovereign-held-path list (`data/black_diamond/`, `schwab/silver/`, `opal-data-bd`, `opal-data-schwab`).
There is **no single source of truth** for the held set -- it is duplicated as a local constant in every guard.

**Grounded mirror count (source-side, `git grep` for held-marker constants over `org/modules/graph/**/*.py` +
`.tools/*.py`):**

| guard / tool | held-marker constant |
|---|---|
| `comp_constants_cli.py` | `SOVEREIGN_HELD` |
| `debtscan/dup_scan.py` | `_HELD_PREFIXES` |
| `.tools/comp-freshness` | `_HELD_CONFIG_PREFIXES` |
| `extract_iam.py` (comp-iam) | `_HELD_SOURCE_PREFIXES` |
| `.tools/_comprail.py` | held-prefix set |
| `comp_aws_cli.py` | held-marker |
| `trace_graph.py` | held-marker (indexer content-exclusion chokepoint) |
| `extract_validate.py` (comp-validate, 7th bd-reader) | **incoming** (CTO front-passes it later) |

**~7 mirrors today, an 8th incoming.** Each also carries its own drift-guard test
(`test_comp_constants_sovereign_guard`, `test_dup_scan_sovereign_guard`, `test_comp_freshness_sovereign_guard`,
`test_extract_iam_sovereign_guard`, `test_comprail_sovereign_held`, `test_indexer_bd_content_exclusion`, ...).

## WHY IT IS A HAZARD

**The held set is not static** -- Andrew has both ADDED firms to the hold and (per the doctrine) can LIFT one.
When the held set changes, **all ~7 copies must move in lockstep**, or a guard whose copy is stale **silently
reads held data** (a false-negative sovereign breach -- the exact class every one of these guards exists to
prevent). A held-marker that is right in 6 guards and stale in the 7th is indistinguishable from all-correct
until the 7th guard reads bd -- and there is no gate that checks the copies agree.

## THE RECOMMENDATION (post-sweep, CTO-owned scoping)

**One shared held-path constant + predicate** in `org/modules/graph/` (e.g. `sovereign_held.py`: the canonical
held-prefix tuple + a `is_held(rel_path)` predicate) that **every guard imports** instead of defining its own.
Single source of truth: change the held set in ONE place, every guard inherits it. The per-guard drift-guard
tests become a single shared-constant test (or keep them as import-integration checks).

**Sequencing:** POST-SWEEP. Consolidating ~7 guards mid-sweep is a large simultaneous change to
security-critical code during an active tool-pass -- the drift-guard tests hold each copy safe individually
until then, so there is no urgency that overrides the mid-sweep-churn cost. File it; scope it when the assurance
sweep closes.

## DISPOSITION -- a TO for `1.0.0_SA_CTO` (owns `NFRA_TOOLPASS`)

Post-sweep consolidation into one shared held-path module. Grounded evidence above (the mirror table + the
drift-hazard mechanism). **NOT stood up mid-sweep.** **NOT authored by COO** (CTO's lane; this brief is the
durable record).

**Attribution:** CTO-noted (~7-copy count); `3.0.0_SA_CVO` seconded with 3-of-7 authored (`223632Z`);
`3.0.0_SA_CVO~B` seconded (`225333Z`); mirror count re-grounded + recorded by `2.0.0_SA_COO`.
