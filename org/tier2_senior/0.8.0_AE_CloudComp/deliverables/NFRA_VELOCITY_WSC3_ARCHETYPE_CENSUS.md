# NFRA_VELOCITY WS-C3 -- Archetype Census + Pattern Inventory

**TO:** `NFRA_VELOCITY_CORE.WS-C3.archetype-census-and-pattern-inventory` @d9131fdd7
**Author:** `0.8.0_AE_CloudComp~C` | **Gate:** `1.0.0_SA_CTO~Z` | **Verify:** `3.0.0_SA_CVO~Z` (after gate)
**Measured:** 2026-07-31 ~11:20-11:40Z, site Z.

> **EVERY COUNT IN THIS DOCUMENT CARRIES ITS INSTRUMENT AND ITS VINTAGE.** Two of the three
> populations below are LIVE and MOVING; one is DEVICE-LOCAL. A bare number here would be wrong
> within the hour, and one of them was wrong within 20 minutes of my own first reading.

## S.0 SHAPING CORPUS (declared first, per `dynamic_rails.held_out_fence`)

Exhaustively, what this census drew on:
1. `org/modules/graph/NFRA_ONTOLOGY_RULE_BANK.yaml` @HEAD -- `dynamic_rails`, `c1_frontend_adapter`,
   `typed_violations`, `type_tuple`, `variance`, `roles`, `relations`, `contextual_types`.
2. `org/modules/graph/NFRA_ONTOLOGY_C2C3_CANONICAL.yaml` -- `c2_motif_families`.
3. `comp-kuzu` live graph (2 census queries: per-plane edge-type, per-plane node-label).
4. `comp-manifest-check completeness` -- the tool-population denominators.
5. `org/mcp/comp-which-rail.log` -- the demand signal. **DEVICE-LOCAL.**

**NOT drawn on, and not opened:** `ADVI_PERFORMANCE`, `MDPF_GLOBAL`. No surface of either appears
here as an example, and no artifact was authored to make a pattern look covered. Per the fence's
`verifiable_without_breaching` clause, this corpus is checkable against the schema above WITHOUT
reading the fenced surfaces. Per `binds_on`, I treat the fence as binding the CAUSAL PATH, not the
seat -- "I am not the ADVI seat" is not a defence and was not relied on.

---

## S.1 FINDING 1 (BLOCKING FOR THE CENSUS AS SPECIFIED): "PER-PLANE" IS NOT WELL-DEFINED

The TO asks for **per-plane motif frequency**. There are TWO different things called "plane", and
they are not the same axis:

| | vocabulary | values | source
|---|---|---|---|
| A | `type_tuple.plane.enum` | source, projection, desired, applied, live, mixed, graph-cache | rule bank (the INTENT-vs-CONFIG observation axis)
| B | graph `layer` property | see below | the live graph (a SUBSTRATE/fabric axis)

**And axis B is INTERNALLY INCONSISTENT between nodes and edges** -- this is the load-bearing half:

```
NODE  n.layer   portal 11338 | ms 5728 | aws 2047 | pipeline 1337 | semctl 23     (5 values, 20473 nodes)
EDGE  e.layer   aws (53 types) | ms (2 types) | semctl (1 type)                    (3 values, 40912 edges)
                                          instrument: comp-kuzu, DB built 2026-07-31T06:07:26Z, Nessie HEAD current
```

**NODES HAVE A `portal` PLANE AND EDGES DO NOT.** `portal` is the LARGEST node population at
**11338 / 20473 = 55.4%**, and there is not a single `portal` edge. The frontend edges that the
rule bank's own `c1_frontend_adapter` calls *"the FRONTEND mass"* -- `RENDERS` 2447 and
`PROP_PASSES` 1382 -- are labelled **`aws`**, while their endpoints are labelled `portal`.

> **CONSEQUENCE: a per-plane motif frequency keyed on `e.layer` CANNOT SEPARATE THE FRONTEND FROM
> THE CLOUD, because 97.9% of the frontend flow is filed under `aws`.** Any per-plane edge census
> reports the frontend as cloud. This is not a data-quality nit; it is the census's own axis being
> unable to express the distinction the workstream exists to measure.

**I have NOT resolved this by choosing an axis.** Choosing would be authoring an ontology decision
in a census TO, and the TO says a census implying a vocabulary change is **WS-C1 round 2 and routes
to CTO~Z**. The census below is therefore published on axis B (`e.layer` / `n.layer`) **with the
inconsistency stated on every table**, and the axis question is routed.

---

## S.2 THE ARCHETYPE CENSUS (axis B, denominators printed)

### S.2.1 Edge-type frequency by plane

**Denominator: 40912 edges / 56 (plane, edge_type) rows. Instrument: `comp-kuzu`, DB built
2026-07-31T06:07:26Z (age 5.2h at measurement), Nessie HEAD current (pin == marker HEAD).**

| plane | edges | share | distinct edge types
|---|---|---|---|
| `aws` | 24377 | 59.6% | 53
| `ms` | 11423 | 27.9% | 2 (`CONTAINS` 5712, `OWNED_BY` 5711)
| `semctl` | 5112 | 12.5% | 1 (`CONTAINS`)

**RECONCILED: 56 rows, 24377 + 11423 + 5112 = 40912 = the DB's own reported edge count.** Stated
because the reconciliation caught a real error -- in MY VERIFIER, not in the data. My first parse
used the character class `[A-Z_]+` for edge-type names, which **silently drops every type
containing a digit**: it lost `READS_S3` (323) and `WRITES_S3` (275), summing to exactly the 598
shortfall, and would have had me "correct" a correct figure downward. **A total that does not
reconcile against the instrument's own denominator is the only reason that surfaced.**

**Top edge types, `aws` plane** (denominator 24377):
`HAS_FIELD` 4269 | `RENDERS` 2447 | `READS_FIELD` 2110 | `CALLS` 1623 | `CONTAINS` 1566 
`PROP_PASSES` 1382 | `DECLARES` 1344 | `INSTANTIATES` 1298 | `REFERENCES_TYPE` 1129 | `FLOWS_TO` 961

**The `ms` and `semctl` planes are STRUCTURALLY DEGENERATE for motif analysis: 3 distinct edge
types across 16535 edges (40.4% of all edges), and all three are containment/ownership.** No flow,
no control, no transform. **40% of the estate's edge mass cannot carry a motif** on this axis.

### S.2.2 The tick-29 uncovered-edge gap, carried forward WITH re-measurement

Rule bank `c1_frontend_adapter` records: **11 live edge types / 3912 edges unmapped, of which
`RENDERS` 2447 + `PROP_PASSES` 1382 = 97.9% frontend** (vintage: comp-kuzu @2026-07-23T14:52Z).

**RE-MEASURED 2026-07-31: `RENDERS` = 2447, `PROP_PASSES` = 1382. BOTH UNCHANGED.** The
97.9% concentration stands. Verdict `11/11 bind additively, 0/11 need new ratified vocabulary`
is unaffected by anything measured here.

### S.2.3 Vintage drift on the rule bank's own printed denominators

The rule bank's D1/D2 `graph_evidence` figures are stamped `comp-kuzu 2026-07-23`. Re-measured
against the live graph 2026-07-31 -- **7 of 11 unchanged, 4 MOVED:**

| edge type | rule bank @07-23 | live @07-31 | delta
|---|---|---|---|
| `WRITES` | 562 | 551 | **-11**
| `READS` | 712 | 703 | **-9**
| `TRIGGERS` | 145 | 149 | +4
| `EMITS_TO` | 144 | 145 | +1
| FLOWS_TO / WRITES_S3 / READS_S3 / FETCHES / PUBLISHES_TO / RUNS / INVOKES | -- | -- | unchanged

> **THIS IS NOT A DEFECT AND MUST NOT BE READ AS ONE.** The rule bank STAMPED those figures with
> their instrument and date, which is precisely why the drift is detectable at all. **A vintaged
> denominator that ages is the system working; an unvintaged one that ages is the frozen-digit
> defect.** Recorded here as evidence that the stamping practice pays, and as a caution that
> `WRITES` and `READS` both DECREASED -- direction noted, **cause NOT investigated and NOT claimed.**

### S.2.4 Declared-but-zero-live

| declared set | count | zero-live members | basis
|---|---|---|---|
| `contextual_types` | 10 | **3** -- `Service`, `Person`, `Organization` | rule bank INTENT ANNOTATION (CTO~Z ruling 2026-07-23): forward-declared cross-plane vocabulary; zero live is their EXPECTED state until their plane binds
| `variance.labels` | 6 | **2 UNEMITTABLE** -- `Superseded`, `Orphan` | source-confirmed `summary_corpus.py:582` (`Orphan/Superseded deferred v1`); 4 emission sites produce only Fork-Shadow/Canonical/Twin
| `roles` | 14 | **UNMEASURED** | role assignment is edge-derived per-instance; not measured by this census
| `relations` | 10 | **UNMEASURED** | requires binds_up-to-live-edge rollup; not run

**`Superseded` and `Orphan` are a DIFFERENT KIND of zero than the contextual types.** The
contextual types are zero-by-intent with a named binding event. **These two are zero because NO
CODE CAN EMIT THEM** -- declared at `labels`, defined at `catalog`, asserted on the FLAGS side at
`polarity`, phrased at `variance_dimensions.yaml:80`, and implemented nowhere. Carried here because
a census that lists them as "declared" without that distinction reproduces the exact error that
made them look live to three agents.

---

## S.3 PATTERN INVENTORY

**pattern -> archetype -> instantiating tools -> gap.** Pattern denominator: **16** = 12 canonical
C2 motif families (`NFRA_ONTOLOGY_C2C3_CANONICAL.yaml#c2_motif_families`, Andrew-ratified
2026-07-30) + 4 typed debt shapes (rule bank `typed_violations`, landed @880f527cc).

| # | pattern | archetype | instantiating tool(s) | gap
|---|---|---|---|---|
| 1 | scheduled-ingest | flow | comp-freshness, comp-estate | cadence is D3-contract-sourced; no contracts exist yet
| 2 | staged-transform | flow | comp-pipescript, comp-dataflow | --
| 3 | orchestrated-compute | control | comp-aws, comp-routes | --
| 4 | fanin-quorum | flow | -- | **NO TOOL**
| 5 | publish-serve | flow | comp-routes, comp-surface-check | --
| 6 | scheduled-publish | flow | comp-freshness | --
| 7 | generative-publish | flow | -- | **NO TOOL**
| 8 | api-serve | boundary | comp-routes | --
| 9 | edge-route | boundary | comp-routes | --
| 10 | access-guard | guard | comp-iam | `(action)` only, never `(action, resource)` -- Rule 22a
| 11 | enrichment-writeback | flow | -- | **NO TOOL**
| 12 | watchdog-observe | observe | -- | **NO TOOL** (and moratorium-adjacent: do not build one unasked)
| 13 | **LEGACY_WRITER** | debt | comp-legacywriter | derivation needs D3 contracts; 0 exist
| 14 | **CLOBBER** | debt | comp-clobber, comp-legacywriter | comp-clobber keys on KEY not (BUCKET,KEY) and does not model call DIRECTION
| 15 | **TRIGGER_MISSEQUENCE** | debt | -- | **NO TOOL.** *(Carried WITHOUT DEBTLOOPS provenance -- CTO~Z found it has none and is correcting the PRD. Do not cite the memo for it.)*
| 16 | **SILENT_RESIDENT** | debt | comp-legacywriter (gated @b5854411b) | gate is live but INERT: 0 declarations exist

**5 of 16 patterns (31.3%) have NO instantiating tool.**

---

## S.4 THE COMPRESSION RATIO -- PUBLISHED AGAINST EVERY CANDIDATE DENOMINATOR

**FINDING 2: "REGISTERED TOOLS" IS NOT ONE POPULATION. IT IS FIVE**, all emitted by
`comp-manifest-check completeness` in a SINGLE run (instrument-cited, 2026-07-31 ~11:20Z):

```
87  tracked+committed comp-* executables      69  tools_index        18  excluded
70  entries-tools                             90  coverage-map (ledgered)
```

Against the PRD's "~96" and a bare `ls` returning 94. **Seven numbers for one concept.**

**PATTERN COUNT = 16** (12 ratified motif families + 4 typed debt shapes; both cited above).

| tool denominator | ratio (16 / N) | reading
|---|---|---|
| `tools_index` 69 | **0.23** | 1 pattern per 4.3 tools
| entries-tools 70 | 0.23 | --
| tracked executables 87 | 0.18 | --
| coverage-map 90 | 0.18 | --
| PRD "~96" | 0.17 | --

> **THE PRD'S EXPECTATION IS CONFIRMED -- AND I AM FLAGGING THAT RATHER THAN RESTING ON IT.**
> The PRD predicts the inventory is "far smaller than the tool count." It is, by ~4-6x, on every
> denominator. **CTO~Z asked me to say so if the ratio came out near 1. It did not.** But the
> confirmation is weaker than it looks and the reason is structural: **I built the pattern count
> from two RATIFIED CATALOGUES (12 + 4), not from an independent enumeration of observed motifs.**
> A catalogue is curated to be small. **So this ratio substantially measures the curation of the
> catalogue, not the redundancy of the tool estate** -- it would come out near this value whether
> or not the tools are actually redundant. **The honest form: 16 CATALOGUED patterns vs 69-96
> tools. It is NOT evidence that ~4 tools implement each pattern**, and I would not let it be
> cited that way.

---

## S.5 RANKED TOOL-GAP LIST

**RANKING CRITERION, stated: (1) patterns with NO tool rank above patterns with a tool that has a
NAMED coverage limit; (2) within each band, DEBT shapes rank above flow/observe shapes, because
the debt shapes are the ones whose absence lets a kill-list act unguarded.** Not impression.

| rank | gap | why it ranks here
|---|---|---|
| 1 | **TRIGGER_MISSEQUENCE has no tool** | a typed debt shape with ZERO instrument; an edge firing against D2 topological+temporal order is undetectable today
| 2 | **fan-in / quorum has no tool** | flow pattern, no instrument; a quorum that silently degrades to 1-of-N is invisible
| 3 | **enrichment-writeback has no tool** | flow pattern, no instrument; writeback loops are where CLOBBER lives
| 4 | **generative-publish has no tool** | flow pattern, no instrument
| 5 | `comp-clobber` keys on KEY, not (BUCKET,KEY), and ignores call DIRECTION | a NAMED limit on a live debt tool; 8 of 11 reported multi-writer sinks were cross-firm path matches
| 6 | `comp-iam` models `(action)` never `(action, resource)` | named, already law (Rule 22a); listed for completeness, NOT new
| 7 | watchdog-observe has no tool | **DELIBERATELY RANKED LAST.** Building one is monitoring machinery under a standing moratorium; the gap is real, the build is not authorised

**Demand-signal input, and why it is NOT used to rank:** see S.6.

---

## S.6 FINDING 3: THE DEMAND SIGNAL IS DEVICE-LOCAL, LIVE, AND 92.7% UNATTRIBUTED

`org/mcp/comp-which-rail.log`, the PRD's "187 rail-override intents":

```
PRD           187
CTO~Z         261   (2026-07-31, earlier tonight)
me            330   (2026-07-31 ~11:20Z)
me            399   (2026-07-31 ~11:35Z -- 69 lines later, SAME SESSION)
```

**FOUR readings, each correct at its moment.** The log is **UNTRACKED** (`.gitignore:68`,
verified by `git ls-files --error-unmatch` + `git check-ignore`, positive control: `CLAUDE.md`
reads TRACKED) and **APPEND-ONLY AND LIVE**. So a rail-override count needs **a device label AND a
vintage** -- per-device alone is insufficient, which is one bound past LD-0362's caveat.

Verdict distribution at n=399 (reconciles exactly: 346+41+5+4+3 = 399):
`ROUTE-POSTERIOR` 346 | `RUN-GREP` 41 | `DENY` 5 | `RUN-GLOB` 4 | `NOFIT-POSTERIOR` 3

> **A HYPOTHESIS OF MINE, MEASURED AND FALSIFIED:** I suspected the measurer was inflating the
> signal -- every comp-* call appends, including this census's own queries. **Measured: 1 line of
> 399 carries my serial. The hypothesis is FALSE**; the growth is other seats working concurrently
> tonight. Recorded because I would otherwise have published an observer-contamination caveat that
> the data does not support.

**BUT: only 29 of 399 lines (7.3%) carry a `serial=` field at all.** 92.7% of the demand signal is
**UNATTRIBUTED** -- it cannot be joined to who asked. **That is why S.5 does NOT rank by demand
volume:** ranking by an unattributed, device-local, live-growing count would produce a
confident-looking order resting on a population whose composition is unknown. The criterion in S.5
is structural instead, and stated.

---

## S.7 WHAT THIS CENSUS DID NOT MEASURE

- **Roles and relations zero-live rollup** -- not run (S.2.4). Listed UNMEASURED, not zero.
- **Motif INSTANCE frequency** -- this census measures EDGE-TYPE frequency per plane, not how often
  each of the 12 motif families instantiates. **The TO's phrase "motif frequency" is not fully
  discharged**, and it cannot be on axis B until the node/edge plane inconsistency (S.1) is
  resolved -- a motif spans nodes and edges whose planes disagree.
- **Cause of the WRITES/READS decrease** -- direction reported, cause not investigated.
- **Fabric-wide anything.** Two of three populations are device-local.

## S.8 ROUTED TO CTO~Z (not self-authored)

1. **The plane-axis question (S.1)** -- node/edge `layer` inconsistency + the `type_tuple.plane`
   vs `layer` collision. Implies a vocabulary decision => **WS-C1 round 2**, not a census edit.
2. **`Superseded`/`Orphan` as a distinct class of zero-live (S.2.4)** -- whether the rule bank
   should mark unemittable declarations distinctly from forward-declared ones.
3. **The compression ratio's real meaning (S.4)** -- it measures catalogue curation more than tool
   redundancy; if the PRD intends the latter, the pattern count needs an independent enumeration.
