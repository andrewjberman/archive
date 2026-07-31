# WS-E8.1 — The C3 item population and its denominator

**Lane:** `0.7.0_AE_CloudOps` · 2026-07-31 ~16:50Z · **Read-only. Nothing applied, nothing touched.**
**TO:** `NFRA_VELOCITY_ESTATE.WS-E8.c3-state-labeling-series` (Andrew-direct ~1612-1615Z)
**Purpose:** the item list IS the denominator. Without it, *"we walked the C3 items"* cannot be
distinguished from *"we walked the C3 items we happened to enumerate."*

---

## 1. THE C3.ii POPULATION — 29 SEMANTIC VERTICALS

**Source:** `comp-estate --list` · **census vintage 2026-07-30** · resolver snapshot mtime `2026-07-30 13:11`.

```
29 C3.ii semantic verticals / 138 chains
   138 = 98 in-scope + 26 explicit-out + 14 unreviewed     (independently tallied; sums exactly)
```

| vertical | chains | | vertical | chains |
|---|---|---|---|---|
| advi-bd | 19 | | graph-platform | 4 |
| advi-inf | 14 | | smartx | 3 |
| news | 13 | | mdpf | 2 |
| trade-submission | 12 | | partners | 2 |
| market-overview | 11 | | insurance | 2 |
| macroeconomics | 9 | | security-scanner | 2 |
| portfolio-management | 9 | | advi-cot · factor-tilts · valuation | 1 each |
| model-portfolios | 8 | | correlation · positioning · cma | 1 each |
| portal-infra | 6 | | data-refresh · canonical-schwab · m365-mcp | 1 each |
| causality | 5 | | etf-reports · ceo-digest · ticketing | 1 each |
| ops-internal | 5 | | | |

**The footer count was not trusted on its own** — the table was tallied independently and the three
sub-counts reconcile to 138 exactly.

### Three verticals have ZERO in-scope chains

`causality` (5 chains: 2 out, 3 unreviewed) · `insurance` (2: 2 out) · `ops-internal` (5: 5 out).

**Open question for CTO, not resolved here:** is a zero-in-scope vertical still a C3 item to walk? It is a
declared vertical with no in-scope chain — so it either belongs in the walk (its state is *"nothing here is
in scope,"* which is itself a maintained fact) or it does not. **This changes the walk denominator by 3.**

---

## 2. THE C3.i POPULATION — 14 DETERMINISTIC STRUCTURES

**This answers the arch-gate's open question empirically, which was the point of enumerating rather than
ruling in the abstract.**

**Source:** `comp-estate --matrix` — *"14 structures x 29 verticals over 138 chains."*

**13 named `sys-*` structures + 1 `UNASSIGNED-RESIDUE` = 14 rows**, matching the declared count.

`sys-yang-analytics-engine` (8 verticals) · `sys-partner-serving-platform` (6) · `sys-estate-ops-platform`
(6) · `sys-market-intelligence-engine` (4) · `sys-causality-engine` (3) ·
`sys-portfolio-management-suite` (3) · `sys-cot-mdpf-assets` (2) · `sys-news-intelligence-engine` (2) ·
`sys-bd-medallion` (1) · `sys-inf-medallion` (1) · `sys-macro-data-engine` (1) · `sys-smartx-feed` (1) ·
`sys-trade-submission-engine` (1) · **`UNASSIGNED-RESIDUE` (7)**

### The answers to the two questions CTO left open

1. **Does the C3.i population come from `--structure` / the C3.i drill, or need its own enumeration?**
   **Neither.** `--structure SYS` is a **drill on ONE named system** — it *presupposes* the names and
   cannot enumerate them. **`--matrix` already carries the population**, so no new enumeration is required.
2. **Is C3.i a subset of C3.ii?** **No — and this matters for scoping the walk.** Per the ratified
   definitions, C3 is *"the DUAL-PARTITIONED rung — two complete partitions of the same C2-instance ground
   set."* C3.ii is **DECLARED, never discovered**; C3.i is **DISCOVERED, never declared** (union-find).
   **They partition the same 138 chains differently.** So *"and potentially c3.i"* adds **14 items with a
   different derivation and different failure modes**, not a refinement of the 29.

### `UNASSIGNED-RESIDUE` spans 7 verticals — a real gap, reported not resolved

`canonical-schwab, ceo-digest, etf-reports, news, ops-internal, ticketing, trade-submission`.
Their chains belong to **no named deterministic structure.** If the walk is done at C3.i granularity,
these 7 verticals' chains are reachable **only** through a residue bucket — which is a bucket, not a system,
and a state label on it would mean very little.

---

## 3. WHAT THIS ENUMERATION COULD NOT HAVE SEEN

Stated in the enumeration's own voice, per the standard this program applies to itself.

1. **AN UNDECLARED BUSINESS FUNCTION — BY CONSTRUCTION.** C3.ii is *DECLARED, never discovered.* This is a
   list of what has been **legislated**, not of what **exists**. A real business function nobody declared as
   a vertical **is not in this list and cannot be**. *No amount of care makes this list complete; only a
   naming act does.*
2. **ANYTHING CREATED OR RENAMED SINCE 2026-07-30.** The vertical **names** come from the
   `estate-coverage-resolver.json` snapshot (mtime 2026-07-30 13:11), not from live state — CLAUDE.md is
   explicit that keys are re-derived live but names are snapshot-served. **1 day old, well inside the
   tool's own 14-day staleness declaration**, and stated rather than assumed.
3. **THE SCOPE STATUS OF 14 CHAINS.** They are `unreviewed` — not in-scope, not out-of-scope. **Their state
   is unknown, and "unknown" is a legitimate state to walk, not a hole to quietly round off.**
4. **WHETHER A VERTICAL'S CHAIN SET IS ITSELF COMPLETE.** The 138 is a census of chains the census could
   find. The E1 registry already records that `comp-estate` **declares its own C0 roster unusable as a
   denominator** (it dropped 3 facts in a measured mdpf case), and that the chain listing *"inherits the
   same census vintage and is NOT a verified-complete enumeration."* **I am not laundering that caveat by
   re-quoting the number without it.**
5. **INTENT — the thing the whole series exists to add.** No mechanical enumeration carries it. That is the
   premise of Layer 2, not a defect of this list.

---

## 4. ONE INSTRUMENT NOTE — a third naive-predicate false positive today

A `grep -o 'sys-[a-z0-9-]*'` over the matrix returned **14 distinct names**, appearing to corroborate the
declared 14 structures. **It was wrong in a way that happened to look right.** The 14th was **`sys-name`**
— a literal token from the tool's own usage text, not a structure. The true composition is **13 named
structures + `UNASSIGNED-RESIDUE`**.

Two honest counts, both 14, meaning different things. Caught only by listing the members instead of
trusting the count.

> **A COUNT THAT MATCHES THE EXPECTED NUMBER IS THE EASIEST KIND OF WRONG ANSWER TO ACCEPT.** Corroboration
> is not verification; enumerate the members.

*(Third instance today: the paginated `length()` reporting 100 for 142; the `bc`-absent sweep reporting 0;
this. All three produced a plausible number rather than an error.)*

---

## 5. THE WALK DENOMINATOR — what CTO and Andrew would actually be walking

| scope | items |
|---|---|
| C3.ii only, all verticals | **29** |
| C3.ii excluding zero-in-scope verticals | **26** |
| C3.i only | **14** (13 named + residue) |
| C3.ii + C3.i (Andrew's *"and potentially c3.i"*) | **43** |

**These are not alternatives to choose by preference — they are different populations with different
completeness properties**, and the choice belongs to CTO's spec. Reported, not resolved.

---

## 6. POSTURE

Read-only throughout. No mechanism built, no labeling performed, no lifecycle value asserted — **all 14 E1
declarations remain `UNDECLARED` because the rule bank requires a producer assertion and no mechanism has
ever asked anyone.** That gap is what E8 exists to close, and closing it is a walk, not a script.

Fences intact: no INF, no ETFS, Inflection deferred (Andrew-direct), zero crons, apply nothing before
Aug-1 14:00Z.
