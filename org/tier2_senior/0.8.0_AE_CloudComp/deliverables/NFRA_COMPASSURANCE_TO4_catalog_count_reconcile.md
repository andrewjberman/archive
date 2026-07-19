# NFRA_COMPASSURANCE TO-4 -- Catalog Truth / One Denominator: record-reconcile

**Author:** 0.8.0_AE_CloudComp~Z | **Date:** 2026-07-19 | **Vintage:** HEAD `4aeed452`
**Authorization:** COO direct (184926Z) -- "EXECUTE the record-reconcile DIRECTLY under the
proceed-all GO (PRD-2 scope, no TO needed)." | **archetype:** VALIDATE

## TO-4's charge (PRD-2 §6, F-4)

> "One denominator. Reconcile 46 / 66 / 63 / ~30; make comp-which print the count it actually routes
> over. Absorbs the vocabulary gaps TO-2's COVERAGE-GAP log produces."

The 2026-07-13 defect: the catalog reported **four disagreeing tool counts** (`RULES`=46 / manifest=66 /
comp-which footer="of 63" / CLAUDE.md="~30"), and the router could not state how many tools it routes
over.

## Finding: TO-4 is LARGELY ABSORBED by NFRA_COMPCLOSE + the registration flow

Two of the three sub-deliverables landed via NFRA_COMPCLOSE (Phases A/C/D) and the canonical registration
flow, verified at HEAD `4aeed452`:

1. **comp-which no longer prints a fixed "of 63".** `.tools/comp-which:1482` now prints
   `top %d of %d % (len(ranked), len(r.ranked))` -- the **per-query ranked-candidate count**, computed at
   runtime for that query. The hardcoded catalog-size claim is gone; the count it prints IS the count it
   ranked over. (Source-confirmed, not inferred.)

2. **There is now ONE reconciling authority.** `comp-manifest-check` (registration-invariant) is a
   fail-closed gate that ACCOUNTS FOR EVERY tracked comp-* executable -- "registration by declaration"
   (COMPCLOSE Phase A, the DISK-IMPLIES-REGISTERED gate, mutant-killed). It PASSES at HEAD:
   `78 tracked+committed comp-* executable(s) all accounted (tools_index 60 + excluded 15 + entries-tools
   65) and ledgered (coverage-map 82)`. The "four disagreeing counts" are no longer a defect: they were
   never the same quantity.

## The reconciled count table (HEAD 4aeed452) -- these measure DIFFERENT things

| source | count | what it actually counts | 2026-07-13 |
|---|---|---|---|
| tracked comp-* executables on disk | **78** | physical files; every one accounted by the registration invariant | -- |
| tools_index (routable catalog) | **60** | tools comp-which will route TO | ("~30" / "of 63") |
| manifest distinct tools | **65** | distinct tools referenced across entries | 38 |
| manifest entries | **97** | tool x use_case rows (97/97 carry use_case) | 66 |
| curated RULES (fast-path) | **73** | comp-which curated rules (the precision layer) | 46 |
| coverage-map homed | **82** | 35 tools[] + 47 meta_tools[]; one-home invariant | -- |

**These are not four measurements of one thing that disagree; they are six measurements of six different
things.** 78 = executables on disk. 60 = routable. 65 = distinct tools carrying manifest vocabulary. 97 =
tool x use_case rows. 73 = curated rules (a fast-path subset). 82 = coverage-map homings. The registration
invariant reconciles them (all 78 accounted). The catalog GREW ~2x since 07-13 (registration flow:
comp-genesis, comp-describe, comp-kuzu, comp-pulse, comp-assets, comp-debris, comp-gitdrill, comp-icedrill,
comp-pydeps, ...) -- the counts moved because the estate did, not because they drifted.

## Residual 1 (known limitation, NOT a routing failure): cohort-C 13.8% "catalog cannot retrieve itself"

The TO-1 harness reports cohort C (catalog self-consistency) at **13.8% zero (12/87)** at the RULES layer.
Characterized (in-process scoring at HEAD, no rail pollution) -- the 12 entries whose own use_case text
scores zero against the curated RULES:

```
  comp-aws (x5 sub-function use_cases -- TF-control / never-widen-diff / cert-classify / snapshot-diff / multi-state)
  comp-coverage · comp-gitdrill · comp-honesty · comp-shell · comp-tool-health · comp-xref · comp-which (own entry)
```

**PRECISE CLAIM (do not overstate):** this is a **curated-RULE coverage gap**, NOT a routing failure. These
12 tools have manifest use_case vocabulary but no matching curated fast-path RULE, so they rely on the
POSTERIOR/manifest-fuzzy backstop. The harness's LIVE-binary measurement shows only **2/87 fail to route
at all** -- the other 10 still route via the posterior. So: 12 tools lack a curated safety-net rule; 2 have
no route at all. This is exactly the **C-4 coverage-backlog** territory (the self-populating catalog blind
spot). It is a NAMED, BOUNDED known limitation -- carried forward, not closed silently.

## Residual 2 (routed OUT -- not mine to fix): CLAUDE.md prose count line is stale (LAW)

`CLAUDE.md:64` reads *"you don't need to know all ~60 tools ... the registries carry the true number --
**62 executables / 49 routable at 2026-07-14**"*. That specific snapshot is **STALE**: current is **78
executables / 60 routable**. (The line already self-discloses it is a snapshot and defers to the
gate-maintained registries -- "the count is GATE-MAINTAINED, not prose-maintained" -- which softens it, but
the digits are factually wrong.)

**CLAUDE.md is LAW -> ROUTED TO 1.0.0_SA_CTO for the edit (per COO 184926Z). I do NOT self-edit CLAUDE.md.**
Recommended: `62 executables / 49 routable at 2026-07-14` -> `78 executables / 60 routable at 2026-07-19`,
or drop the digits and keep only the gate reference (prose-maintained numbers are exactly what this line
warns against).

## Disposition

TO-4 = **substantially COMPLETE via NFRA_COMPCLOSE + this reconcile.** The "one denominator" is delivered as
the registration invariant (all 78 executables accounted); comp-which prints its per-query ranked count.
Residuals: (1) cohort-C 13.8% curated-coverage gap = a NAMED known limitation feeding the C-4 backlog;
(2) the CLAUDE.md prose-count refresh = routed to CTO (law). Project-JSON status reconcile = COO's lane
(not touched here). No CLAUDE.md edit, no COMPROUTE record touched.
