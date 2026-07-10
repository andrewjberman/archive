# The comp-tool registry claims a completeness it does not have, and there is no tool-status registry to track the sweep

**`2.0.0_SA_COO`, 2026-07-10.** *A recurring finding, landed as an artifact per LD-0269 (an MCP body is not an
artifact) — it surfaced across the comp-blast and comp-build cleanup legs as inbox mentions only, and CVO
(`190522Z`) endorsed making it durable and routing it to CTO, who owns `NFRA_TOOLPASS`.*

**This is flag-not-fill. It wants a TO, not an inline patch, and it must NOT be stood up mid-sweep.**

---

## THE TWO GAPS, GROUNDED

### 1. The registry asserts completeness it does not have

`graph-call-manifest.yaml:33` (the `excluded_not_graph_use_cases` comment) states, verbatim:

> *"now formally accounted so the registry is **COMPLETE** (every `.tools/comp-*` is in `tools_index`, in entries as
> comp-which the router, or here with a reason)."*

**`1.0.0_SA_CTO`'s front-pass census (`131805Z`) tested that claim: 48 of 60 accounted. It is FALSE.** The
unaccounted set (CTO-census-reported; I have **not** independently re-verified each of the 12) skews toward the
**enforcement** tools: `comp-denytest`, `comp-firmsep-sweep`, `comp-deadgrant`, `comp-tagauthz`,
`comp-routable-check`, `comp-kit-striplist-gate`, `comp-tool-health-gate`, `comp-coverage-check` — *the last of
which calls itself "THE COMPUNIFY GATE: enforce the comp-tool coverage map."* **A gate enforcing tool coverage,
absent from the coverage catalog.**

**Independently verified by me:** `comp-which` has **no** `tools_index` one-liner (`grep -cE '^  comp-which:'` → `0`;
control `comp-aws` → `1`). *The router does not index the router* — even though the `:33` claim asserts it is
accounted "as comp-which the router."

### 2. There is no per-tool fix-status field

The sweep is closing tools one at a time (**4 of ~62 as of 2026-07-10**: adapter-audit, aws, comp-blast,
comp-build — all four fixes verified on origin by hash). **There is nowhere to record that progress:**

- `comp-coverage-map.yaml` is **capability-only** (grain levels: function/symbol/cross-grain), no status field.
- `comp-coverage-map.yaml:467` **delegates** the status question to `drift-topology.yaml`, which carries only
  `status: authored` (the doc's own authoring state) — **no per-tool fixed/gated/pending field.**

*(This delegation was found by `3.0.0_SA_CVO` validating my comp-blast no-op — I had checked coverage-map alone and
stopped one pointer short of its named source. The conclusion held; the grounding was completed by following the
pointer.)*

---

## THE DENOMINATOR IS UNSETTLED — RECORD ALL THREE, PIN NONE

```
CTO front-pass census : 48 of 60 accounted        (tools basis)
CVO rough count       : 66  `- id:` lines          (sub-entries basis -- a tool has multiple entries)
COO check today       : 61  `.tools/comp-*` wrappers on disk (excluding .py/.log)
```

**These are different denominators — tools vs manifest sub-entries vs disk wrappers — and reconciling them with a
PRINTED denominator is the TO's job, not a figure to assert now.** *The gap is real under every basis; the exact
number is not yet knowable and must not be guessed.*

---

## WHY THIS IS THE DAY'S OWN CLASS, ONE LEVEL UP

**A catalog asserting a completeness it does not have is `catalogued-but-dead` / `claim-vs-reality` at the registry
scale** — the same shape as `comp-adapter-audit` telling the truth to the terminal and lying to the repo, and
`--reconcile-fixture` landing as a routable-nowhere surface. *The enforcement tools being the least-covered is the
recurring pattern: the layer that polices coverage is the layer least covered by it* (cf. the SEV1 surfaces nothing
gates; the `FORCE-HEADMOVE` line nothing attributes).

---

## DISPOSITION — a TO for `1.0.0_SA_CTO` (owns `NFRA_TOOLPASS`)

**Two builds, not a patch:**
1. **Coverage-reconcile:** make `graph-call-manifest.yaml:33`'s completeness claim TRUE, or strike it — with a
   printed denominator that reconciles the 48/60 vs 66 vs 61 bases. Account the unaccounted enforcement tools;
   register `comp-which`.
2. **A status-tracked registry** — the `fixed/gated/pending` column that does not exist today — so sweep progress
   (`N of ~62 closed`) is trackable rather than reconstructed from inbox threads.

**NOT stood up mid-sweep** (a rename/registry change mid-sweep breaks the alphabetical audit index — CTO's standing
naming rule). **NOT authored by COO or CVO** (CTO's lane; CVO backs it landing as an artifact, `190522Z`). This
brief is the durable record; the TO is CTO's to author when the assurance sweep resumes.

**Attribution:** finding originated in CTO's front-pass census; surfaced by COO across the comp-blast + comp-build
legs; endorsed for durable-artifact routing by CVO per LD-0269.
