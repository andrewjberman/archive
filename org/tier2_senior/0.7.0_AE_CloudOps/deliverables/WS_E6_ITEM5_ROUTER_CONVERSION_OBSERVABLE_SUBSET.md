# WS-E6 item 5 -- Router conversion rate, OBSERVABLE SUBSET

**Author:** `0.7.0_AE_CloudOps~E` | **TO:** `NFRA_VELOCITY_ESTATE.WS-E6.harness-r4-trigger-binding`
**Sequenced by:** COO `20260731T165027Z` | **Ruling in force:** COO `20260731T150921Z` (three-category form)
**Measured:** 2026-07-31 ~16:52Z, this device. Read-only.

---

## THE OBSERVABILITY BOUND -- FIRST, BECAUSE IT IS THE DELIVERABLE

**Any conversion rate below is computed over the tools that EMIT. It cannot see the ones that do not.**

| | count | |
|---|---:|---|
| `comp-*` tools on disk | **94** | the population |
| EMIT telemetry (call `comp_log_auto`) | **57** | the ONLY tools any rate can see |
| **DO NOT EMIT -- structurally invisible** | **37** | **39% of the estate's comp-tools** |

**HOW I KNOW -- source read, not inference.** Each file in `.tools/` was read for a `comp_log_auto`
call. This is deliberately *not* inferred from absence in the run sink, because **absence cannot
distinguish "never ran" from "cannot be seen"** -- and that distinction is the whole finding.

Of the 57 emitters: **56 observed, 1 never run here.**
Of the 37 non-emitters: **0 observed** (consistent with structural invisibility, and not itself proof of it).

### The proven case, measured rather than assumed

`comp-state` has **0 rows** in the sink **and demonstrably RAN** -- the 10 owned findings in
`org/critical_paths/.open_findings/` are its output, produced by the R4-A binding.
**Positive control:** `comp-which`, same device, same sink, **36 rows**. So the zero is a property of
the **instrument**, not of usage. Mechanism source-confirmed: `.tools/comp-state:28-29` is a
`runpy.run_path` wrapper and neither it nor `org/modules/graph/state_scan.py` calls `comp_log_auto`
(contrast `.tools/comp-blast:7`, which does).

**For the other 36 non-emitters the run count is UNKNOWN and is reported as unknown, never as zero.**
Only `comp-state` has independent evidence of having run while invisible.

---

## THE THREE-CATEGORY FORM (COO ruling, binding)

### ROUTED -- the conversion numerator/denominator

| | |
|---|---:|
| distinct routes converted | **41** |
| post-R8 stamped routes offered | **2,118** |
| **rate** | **1.9%** |

ANY-of-N converts; `N` is recorded so an ALL-of-N rate stays derivable with no re-baseline.

> **The numerator is DISTINCT ROUTES, not run rows.** 248 run rows carry a `route_id`, but `route_id`
> is **TTL-scoped, not single-use** (R8 test 4 pins exactly this), so one route legitimately stamps
> **6.05 runs on average**. Dividing rows by routes counts each of those as a separate conversion and
> inflates the rate to 11.3%. *I computed 11.3% first and corrected it before reporting.* The
> denominator is routes, so the numerator must be routes.

Route-side census, exclusions printed rather than folded in: **19,821** JOINABLE tool-valued
(**17,704** of them pre-R8 unstamped -- the honest historical tail, visible not hidden);
**1,571** EXCLUDED category-valued (`intent=` is not a tool list); **115** NOFIT no-match
(comp-which's honesty, not abandonment).

### UNROUTED-MANUAL -- NOT SEPARABLE

**11,265 rows carry no `route_id`. This population CONTAINS the trigger-fired runs and cannot be
split.**

### TRIGGER-FIRED -- **UNKNOWN, NOT ZERO**

**Nothing marks a run as hook-fired**, so the third category COO ruled cannot be counted today.

- Reporting it as **0** would be a false claim.
- Reporting it **inside UNROUTED-MANUAL** charges the bindings' successes to the router's gap --
  the exact inversion the ruling exists to prevent.

**For R4-A it is worse than unlabelled.** `comp-state` emits nothing, so R4-A's fires are
**structurally unobservable even if a trigger marker were added tomorrow**. F2 is therefore
load-bearing for E6's headline acceptance, not a reporting nicety.

---

## WHAT THIS RATE IS, AND WHAT IT IS NOT

> **IT IS NOT A FINDING ABOUT AGENTS.**

A low rate measured through an instrument that under-reports **by construction** is a measurement
**of the instrument**. R8 closed a 295x under-report for `comp-which` alone; **37 tools still emit
nothing at all**, so the residual under-report is **bounded below by that population and is not yet
quantified**. Any reading of 1.9% as "agents ignore the rail" is unsupported by this data.

**BOTH LIMBS ARE DEVICE-LOCAL.** The run sink is gitignored (`.gitignore:447`) and the rail log is
gitignored (`.gitignore:68`, `*.log`). **This is this device's traffic only.** It is not an estate
rate and must not be quoted as one; an estate figure is short by every other device, silently.

---

## RESIDUALS -- routed, not picked up

| # | item | owner |
|---|---|---|
| 1 | **F2 / the 37 non-emitters.** `comp-state` is not a one-off; 39% of comp-tools are structurally invisible. Fixing touches a comp-tool STANDARD surface. | CTO gate |
| 2 | **No trigger-fired marker.** Cheapest honest shape: an env flag the two hooks set around their comp-tool invocation -- precedented exactly by `COMP_SYNTHETIC_FIXTURE`, an execution-context tag stamped as a typed field. Additive-optional keys mean no schema migration. | CTO gate |
| 3 | **Rail dead-end**: `comp-which "what fires comp-state and when does a closeout happen"` top-routes to `comp-trigger` (score 1.50, EventBridge/Scheduler forensics). Matched "fires" on the AWS axis; nothing routes to the harness-side trigger layer. | COO routing |

Neither 1 nor 2 was built here: COO `165027Z` -- *"Do NOT fix F2 to make the measurement possible."*

---

## Provenance

`org/mcp/comp-tool-runs.jsonl` (**11,513 rows at 2026-07-31T16:53:51Z**, 0 malformed) -
`org/mcp/comp-which-rail.log` - source read of 94 `.tools/comp-*` files -
`org/critical_paths/.open_findings/` (10 R4-A findings).

> **EVERY COUNT HERE IS A SNAPSHOT, AND THE SINK MOVES WHILE YOU READ IT.** It is append-only and
> live: it went 11,433 -> 11,513 across this session's own reads, **because measuring it appends to
> it** -- several of those rows are my own `comp-*` calls made while producing this report. So
> re-running the numbers will not reproduce these digits exactly, and a mismatch is drift, not a
> discrepancy. The **ratios** are the durable claim; the absolute counts are timestamped for
> traceability, not frozen as truth. Anyone re-deriving should re-state their own instant.
Companion controls: `.tools/git-hooks/test-closeout-comp-state.sh` (@`11652bdb27`),
`.tools/git-hooks/test-deploy-pipescript-check.sh` (@`2a551cf117`).
