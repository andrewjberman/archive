# WS-C7 -- THE MIGRATION DENOMINATOR M: SIX CANDIDATE POPULATIONS, AND THE PRD'S FIGURE MATCHES NONE

**Author:** `0.7.0_AE_CloudOps~Z` -- **Gate:** `1.0.0_SA_CTO~Z` -- **Verify:** `3.0.0_SA_CVO~Z`
**Dispatched:** `2.1.0_SA_COO` `20260731T171907Z` -- *"the gate-maintained population of registered
tools -- the M in WS-C7's 'N of M existing tools migrated with the count printed'."*
**Basis: EXERCISED.** `comp-manifest-check completeness` run live 2026-07-31 ~17:33Z, rc=0.
**Constraint honoured:** *cite the gate, not an `ls`.* Every figure below is the gate's own printed
output or its declared substrate. The `ls` count appears once, labelled as NOT the population.

---

## 1. THE GATE'S OWN OUTPUT, QUOTED

```
[manifest-check] registration-invariant PASS: 87 tracked+committed comp-* executable(s)
    all accounted (tools_index 69 + excluded 18 + entries-tools 70) and ledgered (coverage-map 90).
PASS: routable + placement + self-routes + existence, over 69 registered tool(s).
```

---

## 2. THE FINDING -- **M IS NOT A NUMBER, IT IS A QUESTION ABOUT WHICH POPULATION**

The gate emits **six** distinct counts, each true, each meaning something different:

| candidate | value | what it is | migration-relevant? |
|---|---|---|---|
| `tools_index` | **69** | REGISTERED tools; the gate's own closing line says *"over 69 registered tool(s)"* | **strongest candidate** |
| tracked+committed universe | **87** | every tracked comp-* executable the invariant checks | candidate |
| `coverage-map` ledgered | **90** | placement ledger | no -- a different invariant |
| `entries-tools` | **70** | tools named in `entries[].tool` | no -- overlaps tools_index |
| `excluded_not_graph_use_cases` | **18** | declared NOT graph use-cases | **excluded by definition** |
| `.tools/comp-*` on disk | **94** | **NOT THE POPULATION** -- includes untracked | **no** (COO's constraint) |

**`69 + 18 = 87`** reconciles cleanly: the universe is registered plus excluded. **The other figures
are different invariants' denominators and are not interchangeable with M.**

> **RECOMMENDED M = 69**, on the gate's own words -- the closing line names 69 as the registered
> population, and the migration migrates *registered tools onto a boundary contract*. **The 18
> excluded are declared not-graph-use-cases and a contract cannot be imposed on a population that
> was excluded from routing.** *Recommended, not ruled -- the choice of population is the gate
> owner's, and my job was to produce the number and its provenance.*

---

## 3. **THE DELTA THE DISPATCH ANTICIPATED: THE PRD'S FIGURE MATCHES NOTHING**

COO's constraint: *"If the gate's number and the PRD's '~96' disagree, THE GATE IS RIGHT AND THE
DISAGREEMENT IS A FINDING. Report the delta; do not reconcile silently."*

| source | figure | delta vs gate's 69 | delta vs universe 87 |
|---|---|---|---|
| PRD | **~96** | **+27** | **+9** |
| `.tools/comp-*` on disk | 94 | +25 | +7 |

**`~96` matches NO figure the gate emits.** It is closest to the on-disk count (94) -- **which is the
one COO explicitly ruled out as the population**, and which includes untracked files.

> **I AM NOT RECONCILING IT.** The obvious story -- *"~96 was an `ls` of `.tools/comp-*` at some
> vintage"* -- is plausible, unverified, and exactly the kind of plausible explanation that
> forecloses a live discrepancy. **Reported as a delta with its candidates, not resolved.**

**And the estate's own law already predicts this drift:** CLAUDE.md records the comp-tool count as
**GATE-MAINTAINED, not prose-maintained**, and warns *"do NOT freeze a digit here: the prior frozen
'62/49' drifted to 78->79 within one session."* **The PRD froze `~96`. The gate says 69. This is
that warning, materialised in the document that sets WS-C7's acceptance.**

---

## 4. PROVENANCE OF THE DENOMINATOR ITSELF

| field | value |
|---|---|
| instrument | `comp-manifest-check completeness` |
| substrate | `org/modules/graph/graph-call-manifest.yaml` (`tools_index`, `excluded_not_graph_use_cases`) |
| vintage | live run 2026-07-31 ~17:33Z, rc=0, invariant **PASS** |
| device | site Z; **the substrate is COMMITTED and shared, so these figures are FABRIC-WIDE, not device-local** |

**Explicitly NOT used:** `org/mcp/comp-tool-runs.jsonl` and `comp-which-rail.log`, which are
**gitignored and device-local** -- any volume figure off them is per-device and never a fabric count
(COO's standing caveat, and CLAUDE.md `.gitignore:447`).

---

## 5. WHAT THIS MEANS FOR "N OF M MIGRATED"

**M is stable and citable today: 69 registered, on a PASSING invariant, from a committed substrate.**

**Two properties the migration must carry, both from the estate's own rules:**
1. **The count is the GATE's, never prose's.** WS-C7's acceptance already says *"the count printed
   by the gate, never by prose."* **This document is prose; it cites a gate run at a vintage.**
   **A migration report must re-run the gate, not quote this file.**
2. **M will move.** The gate is maintained; the population grows. **A migration stating `N of 69`
   without its vintage is the frozen-digit defect the PRD just demonstrated.**

---

## 6. ROUTED, NOT DECIDED

1. **Which population is M** -- I recommend 69 and did not choose. **Gate owner's call.**
2. **The PRD's `~96`** -- a delta of +27 against the gate, matching no emitted figure. **PRD is
   `lane=ANY_CTO`; `1.0.0_SA_CTO~Z` owns the correction.**
3. **Whether the 18 excluded tools need a boundary declaration at all.** They are excluded from
   *routing*; whether that also excludes them from the *recall contract* is a scope question I did
   not answer.

**CONTROL 2 CHECK:** nothing here types where an assertion sits. Not rail vocabulary.
