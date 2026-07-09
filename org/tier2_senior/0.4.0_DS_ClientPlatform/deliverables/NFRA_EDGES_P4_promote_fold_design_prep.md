# NFRA_EDGES P4 -- EDGE-PROMOTION folds into NFRA_PROMOTE: DESIGN PREP (build HELD for the P3 gate)

**Author:** 0.4.0_DS_ClientPlatform~B | **Date:** 2026-07-09 | **TO:** `NFRA_EDGES.P4.edge-promotion-folds-into-promote.md`
**Status:** DESIGN-PREP. **Build HELD** — the TO is `staged`, gated on P1–P3 landing + NFRA_PROMOTE coordination.
Written before any code, per the lesson institutionalized this session: the TO is the contract, the GO is a pointer.

**Joint TO.** `<issued_to>` = `0.5.0_AE_OpalETL` / `0.4.0_DS_ClientPlatform~B` (NFRA_PROMOTE lane) + `1.0.0_SA_CTO`
(governed-migration ratify) | CVO cert. **I do not own this alone**, and per req1's SoD I **author only** —
CTO arch-gates, CVO re-signs, **COO SoD-lands** the `cse_schema` bump. An author who lands their own governed
schema bump has collapsed the separation of duties.

---

## 0. What is already committed (grounded, not recalled)

- `cse_schema.SCHEMA_VERSION = 0.4`. `ProducerKind` = {git, agent, deploy, ide, ticket, doc, infra, api,
  approval, graph_head, **promote**}.
- The 0.3→0.4 bump rationale, verbatim: *"+ProducerKind.PROMOTE (governed 5th-producer emission-contract for
  the **promote-materializer's** MATERIALIZED/DEMOTED recognizer transition; back-compat additive)"*.
- `MIGRATION_NOTE`: *"Add a primitive -> version-bump + COMPUNIFY coverage-sweep (which compilers must now
  handle it)"*.
- The 5-invariant gate + lifecycle live in my `NFRA_PROMOTE_P1_promotion_engine.py`:
  CANDIDATE → MEASURED → PROPOSED → (ratify) → MATERIALIZED, with DEMOTED as the reverse.
- Invariant #2 (anti-Goodhart floor), verbatim: *"a coupling must recur across >= FLOOR distinct **producer
  sessions** to be a warrant; a single coincidental co-occurrence is not."* `MEANINGFUL_CO_OCCURRENCE_FLOOR =
  max(2, env PROMOTE_ANTI_GOODHART_FLOOR)`, clamped ≥2 so the floor can never be tuned away.
- Invariant #3: *"PROMOTE proposes; it never mutates the substrate"* (`auto_mutation: False`).
- Invariant #5: the full inspectable trail (`decompression_chain` carried from MOTIF).

---

## 1. TWO DESIGN PROBLEMS the TO's wording creates. Surfaced, not resolved by fiat.

### 1.1 req1 may be a category error: `ProducerKind` names the PRODUCER, not the CANDIDATE KIND

req1: *"NEW ProducerKind for edge-motif promotion via the GOVERNED schema-bump pattern … like R4 @0.4
ProducerKind.PROMOTE."*

But `ProducerKind.PROMOTE` was added to identify **who emits** the CSE event — the promote-**materializer** —
not **what** was promoted. An edge-motif promoted through the existing engine is emitted by that same
materializer. Its producer is unchanged; only the **candidate/target class** differs.

Adding a second `ProducerKind` to distinguish edge-motifs would therefore:
- **conflate producer-identity with candidate-kind** (two orthogonal axes collapsed into one enum), and
- **create a coverage-sweep GAP by construction.** `MIGRATION_NOTE` binds every added primitive to the
  COMPUNIFY sweep: a primitive no compiler emits is a fail-closed coverage gap. I ran that sweep for
  NFRA_EDGES P2 req5 — it already returns FAIL on 9 pre-existing gaps. A new, un-emitted `ProducerKind` makes
  it 10, and the gap would be *ours*.

**Proposal (for CTO, whose ratify this is):** the edge-motif rides the EXISTING `ProducerKind.PROMOTE`, and the
candidate kind is carried where candidate kind belongs — a `candidate_kind` field on the promotion candidate
(`edge_motif` vs `node_motif`), not a new producer enum. That satisfies the TO's actual objective ("NOT a new
mechanism … rides the existing 5-invariant gate") **more faithfully than its req1 wording does**, and it needs
no schema bump at all — which also means no SoD chain and no sweep gap.

**RATIFIED by CTO 123525Z (no bump), conditional on a reverse-consumer check on the enum. Condition DISCHARGED
— see §1.3. Two further facts, grounded while discharging it, make the bump worse than argued above.**

### 1.3 Reverse-consumer-acceptance on the ENUM — PASS; and `producer.kind` is a PARTITION COLUMN

**No consumer BRANCHES on `ProducerKind`.** Every estate use is emit-side (`cse_emit_agent/deploy/graphhead/
frontend_coevolution/gen_cse_seed`; `comp_promote_materializer:230` sets
`producer={"kind": ProducerKind.PROMOTE.value, "ref": commission_id}`). The only reads are a log line
(`cse_emit_promote:153`), that emitter's own self-test (`:203`), and a passthrough copy into the inspectable
trail (`comp_promote_materializer:252` — a label carried forward, not a dispatch). **Zero `if`/match on
`producer_kind` anywhere.** So `candidate_kind` on the candidate serves every kind-consumer that exists.

**The finding that settles it: `producer.kind` IS the CSE store's PARTITION column.**
`cse_store.py:16` — *"Partitioned by (source, event_date) == (producer.kind, execution ts date) — the
`cse_schema.PARTITION_COLUMNS` contract constant"*; Iceberg schema `:103` —
`NestedField(1, "source", StringType(), required=True)  # producer.kind`.

So a new `ProducerKind` does not merely add an enum member — it **mints a new partition** in a log the same file
declares *"immutable by construction … NEVER overwrite; NEVER delete."* We would partition an append-only event
log by **candidate kind** rather than by **producer**, durably and un-reversibly by that log's own contract. The
category error does not stay abstract; it lands in the storage layout permanently.

**`candidate_kind` is genuinely a NEW field** (checked, not assumed). `PromotionRecord.promotion_class` is the
TARGET routing key (`PROMOTION_CLASS_ROUTING[rec.promotion_class] -> target, owner`, derived by `_classify(c)`) —
i.e. what the candidate BECOMES (recognizer / primitive / directive / knowledge-node). That is a different axis
from what it CAME FROM. `candidate_kind` is additive on `PromotionRecord`: no schema change, no SoD chain, no
CVO re-sign, no sweep gap, no new partition.

**Near-miss, recorded because it nearly became a filed defect.** `comp_promote_materializer:104` reads
`producer_kind = ProducerKind.INFRA.value` — which looks inconsistent with the PROMOTE emission. It is not:
`:104` is `ManifestRecognizer.producer_kind` (a RECOGNIZER's kind; compilerkit emits as INFRA), while the promote
CSE is built at `:230` under `ProducerKind.PROMOTE`. Different producers, correctly distinguished. The
`"PROMOTE/MONITOR"` strings in `fedobs/promote_monitor.py` are labels in a monitor trail record, not CSE producer
kinds. Checked the context before filing, which is the only reason this is a footnote and not a retraction.

**If CTO rules the bump is wanted anyway**, then it is a governed `0.4 → 0.5` bump and the SoD chain binds:
author (me) → CTO arch-gate → CVO re-sign → **COO SoD-lands** → and the new primitive must be *emitted by a
registered compiler* in the same wave, or the sweep goes to 10 gaps and we have shipped the thing we gate against.

### 1.2 req3's measure-before-promote has a GRAIN MISMATCH — a Goodhart hole inside the anti-Goodhart invariant

Invariant #2 requires recurrence across **≥ FLOOR distinct producer SESSIONS**. An edge-motif's recurrence,
as built in P2, is over **LOCI** — distinct sinks (D1 recurrence 5) or distinct edges (D3 recurrence 4).

These are different populations, and the substitution is unsafe in the dangerous direction:

> A single commit can introduce all 5 of D1's guarded-fork sinks at once. Loci-recurrence = 5; producer-session
> recurrence = 1. Feeding loci-recurrence to a floor defined over sessions makes the **coincidence floor pass
> on a single coincidence** — precisely the case invariant #2 exists to reject.

That is the session's recurring shape one level in: **the guard's INPUT would be a proxy for the thing it
guards.** The floor would be satisfied by a measure that cannot detect the failure it screens for.

**Proposal (for the NFRA_PROMOTE plane owner + CTO):** an edge-motif candidate must carry BOTH signals and the
floor must bind on the **session** grain, not the locus grain:
- `locus_recurrence` (from P2 — evidence of the idiom's spatial spread), and
- `producer_session_recurrence` (distinct producer sessions in which the motif's member edges were introduced —
  derivable from the CSE/commit provenance already on the decompression chain).
Invariant #2 evaluates `producer_session_recurrence`. `locus_recurrence` informs the owner's ratify, never the floor.

**The gate must BITE on this**, and the bite-test writes itself: an edge-motif with `locus_recurrence = 5` and
`producer_session_recurrence = 1` must be **REJECTED** by invariant #2. If it promotes, the floor is vacuous on
edge-motifs and the phase should be rejected. A mutation that swaps the floor onto `locus_recurrence` must make
that test fail.

---

## 2. What P4 inherits and must NOT re-open (req2)

AC4 (collision-safe, unique-by-construction ids) and AC5 (`snapshot_ts` / CloudNode-conform / freshness-covered)
come from P1–P3. Promotion does not re-derive them. Concretely, the promoted edge-motif's id is P2's
`edgemotif:<idiom>:<sha1(canonical edge-set)>` — and the **idiom prefix is load-bearing identity** (D2/D3 carry
byte-identical edge-sets on the live estate; CTO is routing the PRD/TO wording amendment). Any promotion path
that re-keys or "simplifies" that id re-opens the silent-MERGE class.

---

## 3. Reversibility (req3, AC-2)

`promote → degrade → auto-demote` must be **proven on an edge-motif**, not assumed from the node-motif proof.
The demote path emits under the same producer contract (`MATERIALIZED`/`DEMOTED` transition). Exercise, do not
assert: a promoted edge-motif whose measure degrades below the floor must auto-demote, and a mutation disabling
the demote path must make that test fail.

---

## 4. Sequencing + who does what

1. **GATED**: P1–P3 land. P3's spec half is closed; req1/AC-1 are with `0.7.0_AE_CloudOps` + CVO~B.
2. **Coordinate with the NFRA_PROMOTE plane owner** — this is a PROMOTE extension tracked there, not an
   NFRA_EDGES core deliverable (TO `<status>`: "SCOPED OUT of NFRA_EDGES core").
3. Resolve §1.1 (CTO: schema semantics) and §1.2 (PROMOTE owner + CTO: floor grain) **before any build**.
   Both are contract-level questions; neither is mine to settle in a deliverable.
4. Author → CTO arch-gate → CVO re-sign → **COO SoD-lands** any bump. I author; I do not land.
5. RAVC COO~B + the NFRA_PROMOTE owner with a requirement-by-requirement conformance map, each qualification named.

---

## 5. Open questions to route (not to answer here)

1. **[1.0.0_SA_CTO]** Does the edge-motif ride the existing `ProducerKind.PROMOTE` with a `candidate_kind`
   field (no bump, no sweep gap), or does req1's literal "new ProducerKind" stand? The literal reading
   conflates producer with candidate-kind and manufactures a coverage gap.
2. **[NFRA_PROMOTE plane owner + 1.0.0_SA_CTO]** Invariant #2's floor is defined over producer SESSIONS; an
   edge-motif's recurrence is over LOCI. Which signal binds the floor? (Recommendation: sessions; loci informs
   the ratify only.)
3. **[2.0.0_SA_COO~B]** Who is the NFRA_PROMOTE plane owner for this fold, and is `0.5.0_AE_OpalETL` or I the
   primary author? The TO names both.
