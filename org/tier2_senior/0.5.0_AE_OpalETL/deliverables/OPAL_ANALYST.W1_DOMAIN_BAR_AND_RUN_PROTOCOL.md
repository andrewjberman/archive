# OPAL_ANALYST.W1 — DOMAIN BAR + run protocol (six Pod-2 pages)

**Author:** `0.5.0_AE_OpalETL~Z` · **TO:** OPAL_ANALYST.W1 @a438a40793 · **PRD:** §9 v1.4 @a233902bb8
**Method vintage:** `projects/ATOM_DECOMP/**` @d5eda6112f · **Axis:** copied verbatim from CVO~Z's W0
**Pod-2 census (INPUT, not evidence):** ARTIFACT_CENSUS_POD2.yaml @49cb88eade

> ## ⛔ THIS DOCUMENT IS COMMITTED **BEFORE ANY W1 MEASUREMENT**, AND THAT IS ITS ENTIRE POINT.
> Rule 14(b) requires the owner to state the domain bar *before* measuring, and W1 C3 requires that
> precedence be **verifiable, not asserted**. A bar written after the numbers are in is not a bar —
> it is a rationalisation with a threshold in it. **The commit order is the evidence.** Every W1
> `run.json` sets `domain_bar_ref` to this file; if a run's first measurement predates this commit,
> C3 fails and no amount of prose repairs it.

---

## 1. Scope and the denominator I am measuring against

Six pages, page grain, one run each. Census says **23 rendered artifacts across 20 panels**, plus 2
unrendered:

| page | panels (census) | artifacts (census) |
|---|---|---|
| `/cma` | 3 | 3 |
| `/positioning` | 3 | 5 |
| `/attribution` | 2 | 4 |
| `/factor-tilts` | 3 | 5 |
| `/valuations` | 5 | 5 |
| `/correlations` | 1 | 1 |

**These are the CENSUS's numbers, not mine, and they are input.** Each is a hypothesis my run
tests. Per W1 C6 every disagreement is named with the run's evidence and the run wins; **zero
disagreements on a page is a valid result and gets stated explicitly**, because an unstated zero is
indistinguishable from an unexamined one.

---

## 2. THE DOMAIN BAR — expected variance vs finding class

The bar exists to stop two opposite failures: calling normal variation a finding, and explaining a
real defect away as normal. **A bar that only ever produces findings is not a bar** (CVO~Z's W0
lesson, adopted).

### 2.1 Vintage / freshness

| observation | class |
|---|---|
| Artifact at **T-1** on a trading-day frontier | **EXPECTED.** Not a finding. Every AUM/holdings/trading artifact is T-1 unless it explicitly says otherwise. |
| Age explained by **weekend or market holiday** | **EXPECTED.** Resolve the calendar FIRST, always, before any staleness language (CLAUDE.md NEVER#1). |
| Artifact stale vs **its own declared cadence** (month-end producer read mid-month; event-driven producer with no event) | **EXPECTED — and recorded as an explicit NON-FINDING with the cadence cited.** `peer_performance` at 11 days is the type specimen: month-end IS its healthy state. |
| Artifact stale vs its own cadence **and** its prefix-siblings moved | **FINDING (F-VINTAGE).** The siblings are the control. |
| Producer is **operator-run / unscheduled** | **FINDING (F-SCHEDULE)** regardless of current freshness — CLAUDE.md's scheduled-pipeline rule; it freezes silently and invisibly. |
| A **count** that moved on a family declared unbounded (`_manifests/`) | **EXPECTED.** Not drift. |

**Trading-day arithmetic is mandatory** via `lib/trading_calendar.py`; a wall-clock age is never a
staleness finding. **A false outage is not a safe error** — it spends credibility and manufactures
pressure to "fix" a working pipeline.

### 2.2 Serving state (Rule 3 — the load-bearing axis for W1)

Declared · deployed · invoked · artifact-producing · **serving** stay separate per artifact.

| observation | class |
|---|---|
| Route declared in `App.tsx` and served on a live read | **EXPECTED.** This is the measured-good state W1 exists to establish (PRD §9.1.2 DESIRED → measured). |
| Route declared, **never checked** against a live read | **NOT A VERDICT.** Cell stays `UNMEASURED`. A route table is not a serving claim. |
| Route declared but **not served** | **FINDING (F-SERVE).** Not a discrepancy to reconcile away. |
| Panel renders from a key **nothing produces** | **FINDING (F-ORPHAN-CONSUMER).** The `getNonModelAssets` shape. |
| Artifact produced with **zero consumers** at the consumed end | **FINDING (F-ORPHAN-PRODUCER)** — but see 2.3; producer-side liveness does NOT rebut it. |
| CF returns **HTML for a missing JSON key** | **FINDING (F-MASK).** It fails as a parse error, not a clean 404, so it is invisible to a status-code check. |

### 2.3 Consumers

**Grounded at the CONSUMED end, always** (Rule 12; CVO~Z: it changed three W0 verdicts).
**Excluded from every caller count: the accessor's own definition and the export barrel** — include
them and everything reads as consumed. A count of callers states what it counted over.

### 2.4 Field tables

**The ARTIFACT is the denominator, not the panel.** A field table derived from what a component
renders captures only what the component draws — that is how MP's `aum-metrics` row enumerated 2 of
9 keys and omitted `total`, the scope-wide AUM figure. **Every field table is re-derived from the
live object and states `N of M` top-level keys.** Missing keys are a FINDING against the census
(F-CENSUS-THIN), not a silent extension.

### 2.5 What is explicitly NOT a finding

Cosmetic naming inconsistency; a TODO comment; a formatting difference; a count that moved on a
declared-unbounded family; a route redirecting **by design** (`/` → `/market`); an artifact whose
absence is **declared** in the census.

---

## 3. Cell-status discipline (M-6, adopted)

`MEASURED` / `UNMEASURED` / `INFERRED` / `NOT_MEASURABLE`.

⛔ **An OWNED UNKNOWN is `NOT_MEASURABLE` WITH ITS DISCRIMINATOR NAMED — never the string "owned
unknown" as a VALUE with status `MEASURED`.** CVO~Z did exactly that on two W0 cells and caught it
only on re-read. It is a hole wearing a measured label, and it is **invisible in the hole census** —
the one instrument whose entire job is to see holes. Every `NOT_MEASURABLE` cell names the
observation that would resolve it.

`INFERRED` is never cited as fact (14(f)) and never authorises an act.

---

## 4. Method-defect mitigations I adopt for all six runs

CVO~Z's `METHOD_READ.md` filed seven; each below is my standing handling so I do not re-decide it
privately six times. **A boundary decided independently per run is a convention, not a control.**

| # | Defect | My handling |
|---|---|---|
| **M-1** | 14(c) fan-out is unrunnable (`org/XXX.md` BANS Task/Explore agents) | **Single-author mode, DECLARED in every `run.json`** (`population_mode: SINGLE_AUTHOR_DIRECT`) with the compensating control stated: all independence burden falls on CVO~Z's certification pass, and I size the verifier packet for it. Not silently assumed. |
| **M-2** | Nobody is named to plant the mutant | **I plant it and SEAL it at plant time** in `MUTANT_SEALED.md`, committed BEFORE the verify pass, stating which constraint it violates **and why that constraint is not mechanically checkable.** Writing that justification is what stops me planting a soft one. |
| **M-3** | Mutant has no exit — the certified artifact would ship the planted falsehood | **A correction patch + a distinct `rectangle.final.certified.json` per run.** The mutant is the one part of this method designed to be wrong; its removal is never left to memory. |
| **M-4** | "Until DRY" satisfaction is invisible → gets asserted | **The DRY-establishing cycle emits a real patch with `changes: []` and a populated `unchanged_examined`.** The schema already supports it. No zero-change cycle is claimed without its artifact. |
| **M-5** | Rectangle has no grain for page/panel RELATIONS | **A `relations` block beside `entities`** (panel → displayed artifact → displayed vintage → label accuracy). ⛔ **NOT solved by widening the field set** — a page-level field on an artifact-grained axis is a Rule 24(ii) grain violation. Expect this to bite harder here than on MP: these six have real panel scaffolding, 20 panels across 6 pages. |
| **M-6** | `NOT_MEASURABLE` vs "owned unknown" | §3 above. |
| **M-7** | No route back when the P0 input is WRONG | **A required `input_corrections` array in every `run.json`** — contradicted claim, locator, owning seat — AND routed to the census owner. Four of my own MP census cells were wrong; a run that silently repairs its input inside its own artifact leaves the input wrong for the next reader. Makes the census improve monotonically instead of being re-contradicted six times. |

---

## 5. Field planes — CVO~Z's axis, copied verbatim, not retyped

`axis_declaration.json` is **copied byte-for-byte** from
`runs/portal-page-portfolios/20260811T1640Z/`, with only `entity_keys` repopulated per page. **A
retyped axis is a forked axis.**

- **PLANE A — MINE to measure**, arriving `MEASURED` with evidence: `producer`, `serving_state`,
  `consumer_set`, `vintage_grain`.
- **PLANE B — CVO~Z's**, arriving `UNMEASURED` and untouched: `canonical_name`, `business_meaning`,
  `vintage_semantics`, `disposition`, `notes`.
- **PLANE C — CVO~Z's, widening-gated**, arriving `UNMEASURED`: `analyst_serve_verdict`.

⛔ **I do not pre-fill a Plane B or C cell, even when the answer looks obvious.** The split is what
discharges Rule 24(iii) — fact and judgment on one axis fails intent-coherence — and a helpfully
pre-filled `business_meaning` is me exercising a pen Andrew delegated to CVO~Z.

**Exception, narrow and declared:** where a Plane-A measurement produces a relational observation
with no home (M-5), it goes in the `relations` block, **never** in a Plane-B `notes` cell.

---

## 6. Per-page sequence

1. Copy `axis_declaration.json`; repopulate `entity_keys` from the census (input).
2. Enumerate first-hand — routes, panels, fetches, served artifacts — **each count with its
   denominator**, and a retrieval that returned nothing distinguished from a surface that has
   nothing (C1).
3. Generate `rectangle.c0.json`, **every cell born UNMEASURED** (C2).
4. Measure Plane A only. Live reads for the served limb (C5) — never the route table alone.
5. Reconcile against the census; name every disagreement with evidence; **state zero explicitly**
   (C6). Populate `input_corrections` (M-7).
6. Iterate to DRY with the no-op patch made visible (C4/M-4).
7. Plant + seal the mutant (M-2). Hand the verifier packet to CVO~Z **per page as it reaches DRY,
   not batched** — certification must not become a six-page cliff.
8. CVO~Z certifies (C8) and lands semantics (C9). **I never sign my own run.**
9. Correction patch → `rectangle.final.certified.json` (M-3).

---

## 7. Standing prohibitions on this wave

No alert / alarm / SNS / SES / freshness-checker / `*-monitor` — **including anything a page's
decomposition makes look "easy to watch."** No new approval gate on another seat. **No deletion,
move, or cleanup of any served or served-adjacent artifact** — residue gets a disposition and a
recommendation, never an act (moving served output is NEVER#3). No shadow path, parallel emitter,
or standing comparator. No panel-grain decomposition. **The census is never run evidence.** No push
— lane commits; MSTR~Z integrates.
