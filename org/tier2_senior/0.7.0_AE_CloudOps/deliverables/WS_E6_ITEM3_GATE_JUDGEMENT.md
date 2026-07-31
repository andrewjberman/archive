# WS-E6 item 3 -- GATE JUDGEMENT: path tuning CANNOT be done honestly on the visible subset

**Author:** `0.7.0_AE_CloudOps~E` | **TO:** `NFRA_VELOCITY_ESTATE.WS-E6.harness-r4-trigger-binding`
**Asked by:** COO `20260731T173240Z` (a judgement, not a build; COO explicitly not steering)
**Measured:** 2026-07-31 ~17:35Z, this device | **Reproduce:** `ws_e6_item3_gate_measurement.py` (beside this file)

---

## VERDICT

> **GATED.** Item 3 cannot be done honestly against a 57-of-94 visible population.
> **Recommend E6 closes at items 1-2 + 5, with item 3 named as GATED** on the emitter question
> CTO owns as rail-owner.

This is not a claim that the data is *noisy*. It is a claim that the invisibility is **BIASED on an
axis orthogonal to path quality**, and that a map built on it would recommend **deleting routes that
work** -- with data, reproducibly, and defensibly.

---

## PREDICATE (stated first, per COO ruling 1 and CTO's own 87-vs-94 correction)

**Population:** ALL regular files under `.tools/` whose name starts with `comp-`. **94.**
**Emitter test:** the string `comp_log_auto` appears in the file's source.

> **This is a TEXT MATCH, so a file that MENTIONS `comp_log_auto` without calling it counts as an
> emitter. THE 37 IS THEREFORE A FLOOR ON INVISIBILITY, NOT A CEILING.** The error direction is
> conservative: the true invisible population is `>= 37`, never fewer. Stated because the same
> unstated-filter class already moved CTO's figure by 7, and all 7 fell one way.

---

## FINDING 1 -- invisibility tracks IMPLEMENTATION LANGUAGE, not usage

| | python | shell |
|---|---:|---:|
| EMITTERS (57) | 3 | 54 |
| NON-EMITTERS (37) | 22 | 15 |

**22 of 25 python comp-tools are invisible.** This is an artifact of how the shims were built: bash
shims call `comp_log_auto`; python wrappers (`comp-state` is the proven case, a `runpy.run_path`
wrapper) do not.

**Consequence:** a map that ranks selection paths on this data is ranking **python-vs-shell**, an
axis with no relationship to whether a route is good.

---

## FINDING 2 -- 7.9% of routes are UNCONVERTIBLE BY CONSTRUCTION

Of **19,823** tool-valued routes (`ROUTE-POSTERIOR` + `ROUTE-POSTERIOR-DISAMBIG`):

| slice | routes | share | |
|---|---:|---:|---|
| ALL recommended tools VISIBLE | 11,093 | 56.0% | the only cleanly measurable slice |
| SOME recommended tool invisible | 7,054 | 35.6% | conversion depressed / confounded |
| **EVERY recommended tool INVISIBLE** | **1,573** | **7.9%** | **can never convert** |

ANY-of-N converts (COO `065315Z`), so a route whose **entire** recommendation set is invisible
**cannot register a conversion however perfectly the agent complied.**

> **VERIFIED, not assumed:** 1,573 sits suspiciously close to R8's 1,571 EXCLUDED category-valued
> rows. I checked rather than report a coincidence as a result -- the family split is **1,573 of
> 1,573 `ROUTE-POSTERIOR`**, i.e. genuine tool-valued rows. Different population, coincidental
> proximity.

### The dead paths are the heavily-routed ones

| invisible tool | routes recommending it |
|---|---:|
| `comp-freshness` | 1,454 |
| `comp-learns-status` | 906 |
| `comp-fedobs` | 864 |
| `comp-dups` | 840 |
| `comp-axes` | 835 |
| `comp-dispatch` | 822 |
| `comp-whoread` | 635 |
| `comp-tool-health` | 614 |
| `comp-heat` | 608 |
| `comp-secrets` | 558 |
| `comp-honesty` | 546 |
| `comp-state` | 505 |

`comp-freshness` is recommended **1,454 times** and registers **zero** conversions, permanently.

---

## THE DECIDING ARGUMENT

Item 3's remit includes **retiring nudges that misfire**. A map built on this data would identify
the routes to `comp-freshness`, `comp-dispatch`, `comp-state` and their peers as **the
worst-performing paths in the estate** -- because they are guaranteed-dead **by instrumentation**,
not by agent behaviour.

> **THE MAP WOULD ARGUE FOR DELETING ROUTES THAT WORK.**

COO's standing fence warns that *"this path has no traffic"* is the false signal that would justify
**inserting** a router hop. The measurement says the sharper risk runs the other way: it justifies
**removing** a route -- and a removal is not recoverable by noticing later, because the memorized
head it was protecting is already gone.

This is the **rigorous-instrument-on-the-wrong-axis** class. It survives review *because* it is
internally consistent.

---

## THE CARVE-OUT I CAN DEFEND, AND WHY I RECOMMEND AGAINST IT

A strictly-scoped version is arguably honest: friction reduction on the **11,093 all-visible routes
only**, **zero retirement authority**, bound stated inline. Within that slice the comparisons are
sound.

Two reasons to hold anyway:
1. It tunes only the **best-instrumented** paths -- a selection effect on *which* paths get
   improved. Not a correctness error, but it must be named.
2. It excludes the **retirement** half, which is where both the value and the danger of item 3 live.
   That buys the safe third of the workstream at full coordination cost.

**Available on request; not recommended.**

---

## F6 -- INDEPENDENT OF ITEM 3, LIVE TODAY, SHOULD NOT WAIT ON THIS DECISION

Verifying the 103 routes unaccounted for by the three buckets above surfaced a third dead-path class:
**comp-which recommends five tool names that do not resolve at all.**

| recommended name | routes | resolves? | last recommended |
|---|---:|---|---|
| `comp-adapter-audit` | 1,290 | **no** (absent from `.tools/`, not on PATH) | 2026-07-30T19:36:25Z |
| **`pipescript`** | **735** | not on PATH; **PROHIBITED** | **2026-07-31T15:42:18Z** |
| `comp-semantic-estates` | 77 | **no** (renamed to `comp-estate`, forwarders deleted) | 2026-07-30T07:16:57Z |
| `comp-opalbizsem` | 8 | **no** | -- |
| `comp-portal-thread` | 3 | **no** | -- |

**POSITIVE CONTROL** (run so a stale-log artifact could not explain the result): `comp-blast` last
seen `2026-07-31T17:27:11Z`. The log is current and the retrieval works.

> **`pipescript` is under a flat Andrew-direct prohibition (2026-07-29) and CLAUDE.md records it as
> a RETIRED `rc=2` stub that is PROHIBITED. comp-which recommended it TODAY.**

~2,113 routes point at tools an agent cannot run. Unlike findings 1 and 2, **this is an active
defect rather than a measurement gap.**

**NOT ACTED ON:** comp-which's routing table is untouched -- standing fence, and it is a comp-tool
STANDARD surface (CTO gate). Routed to COO for CTO.

---

## Compliance with COO's four rulings (`1ee709c994`)

1. Figure ships with the bound **inline**: *"1.9% over 57 of 94 emitting tools; 37 structurally
   invisible, residual unquantified."* Never quoted bare.
2. **No populate-the-emitter campaign.** Not started, not proposed.
3. **The 36 stay `UNKNOWN`** in every citation here. Only `comp-state` is reported as
   proven-ran-while-invisible.
4. Emitter standard routed as **a finding with its denominator, not a task**. CTO holds it.
