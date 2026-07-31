# WS-E1 — ESTATE-CONTRACT REGISTRY: THE SHAPE (pre-population, for the arch-gate)

**Seat:** `0.7.0_AE_CloudOps~D` · **Date:** 2026-07-31 · **Gate:** `1.0.0_SA_CTO`, requested
20260731T074203Z — *shape before breadth population.*
**Status:** SHAPE ONLY. **`org/modules/graph/estate-contracts/` is NOT created and no contract is
declared until this is ruled.**

---

## §0 Constraints this shape is built under

- **DESCRIBE THE SPECIMEN, NEVER THE GAP.** No field, enum, or comment here characterises what the
  grammar lacks or proposes a value for it.
- **Declaring is CONSUMPTION** (CTO 074028Z). **Control 2 holds: zero rail vocabulary authored.**
- **Firm separation binds** — bd/cot/inf contracts are declared per-firm and never mirrored.
- **Alarm/monitor moratorium** — this registry renders records. **It fires nothing.**

## §1 THE LOAD-BEARING DESIGN DECISION — lifecycle values are DERIVED, never enumerated here

**The registry does not contain a list of valid lifecycle values.** It resolves them **from the
ratified rule bank at read time**, exactly as `classify_exit` resolves verdicts from the declared
exit contracts.

**This is the M3 lesson applied one workstream over, and it is the whole reason the shape looks the
way it does.** M3's defect was a **frozen hardcoded enumeration inside the consumer that drifted
from the live surface it was supposed to mirror** — and it cost 434 miscounted verdicts and an
8.5%-vs-0.87% error in the program's own measurement. A registry that copies the lifecycle vocabulary
into itself **is the same artifact**: a second copy of a vocabulary whose owner is elsewhere, going
stale silently, with nothing to detect the drift.

**Consequences that fall out for free:**
- An **UNDECLARED-LIFECYCLE** artifact resolves to a **loud UNKNOWN**, never a default — condition (b) of M3's remediation, inherited rather than re-invented.
- When the rule bank gains a value by ratification, **every contract re-resolves.** No migration, no sync, no fourth copy.
- I never write a lifecycle value into a schema, which is also **how Control 2 stays satisfied structurally rather than by my attention.**

## §2 Per-contract record

| field | type | notes |
|---|---|---|
| `contract_id` | string | stable id; the record's own key |
| `subject_kind` | enum {`artifact`,`process`} | what is contracted |
| `subject_key` | string | the S3 key / resource identifier contracted |
| `grain` | string | the `(key, grain)` pair is what single-writer is asserted over |
| `firm` | enum, from `data/firm_registry.json` — **resolved, not copied** | **firm separation is a TYPE here, not a convention** |
| `writer` | string | the single declared writer |
| `cadence` | structured | the contracted run-frequency (D3-sourced; **not** a graph primitive) |
| `completeness_scope` | structured | what the artifact promises to be complete *of* |
| `canonical_source` | string | the upstream this is derived from |
| `successor` | string \| `null` | **required, never omitted** — `null` is a declaration, absence is not |
| `lifecycle` | **RESOLVED from the rule bank** (§1) | never a literal in this file |
| `intent_source` | string | the module's consumer-anchored `PURPOSE` (Rule: callers derive from it) |
| `declared_by` / `declared_at` | serial / ISO-8601 **computed offset** | never a hand-typed `Z` |
| `grounding` | enum {`source_confirmed`,`live_confirmed`,`inferred`} | **`inferred` is legal and visible**, never silent |

### §2.1 Two fields that exist because of tonight

- **`successor` is REQUIRED and nullable rather than optional.** An omitted field and a declared
  `null` are indistinguishable to a reader, and *"no successor"* is exactly the claim a retirement
  decision leans on. **Absence must not be able to impersonate a declaration.**
- **`grounding` is a required enum including `inferred`.** A contract asserted from source and one
  inferred from observation must not render identically — the reserved-words rule (Rule 22) applied
  at the schema level instead of at the author's discretion.

## §3 Single-writer as a TYPED violation, not a lint

E1 makes single-writer a **contract term**: two declared writers at one `(subject_key, grain)` is a
**type error at declaration time**, detectable by reading the registry alone — no scan, no
heuristic, no scheduled check. **The violation cannot be declared, rather than being declared and
then reported.** (The mdpf specimen's two portal-visible key shapes, observed at
`WS_E1_SPECIMEN_OBSERVATIONS.md` §2, will be adjudicated *by* this rule — I have not pre-judged
whether they are one writer over two keys or two writers.)

## §4 Coverage is a REQUIRED EMISSION, not a report

Every registry read emits **`contracted / total, per tree`** — and **`total` must come from an
enumerated denominator computed at run time, never a stored count.**

⚠ **And it carries the census's own honesty label forward:** `comp-estate` declares *"do NOT use
this roster as a census denominator"* (it dropped 3 facts in the measured mdpf case). **A registry
that quietly adopted that roster as `total` would report high coverage of an undercounted
population — coverage rising because the denominator shrank.** So the denominator's *source* is a
required field beside the number, not an assumption.

## §5 What this shape deliberately does NOT do

- **Does not enumerate lifecycle values** (§1) — the defect this whole design avoids.
- **Does not name any missing class**, in positive or negative phrasing.
- **Does not create `estate-contracts/`** — nothing exists until this is ruled.
- **Builds no checker, alarm, monitor or notification.** It renders records; enforcement rides the
  existing commit-gate ramp (WS-E3's C-SILENT path), which is announce-then-enforce and already
  owned.
- **Does not assume the specimen chain's shape generalises.** It is one chain; breadth follows the
  gate, and the coverage emission will make the gap visible rather than implied.

## §6 The one thing I want ruled explicitly

**Where the registry's `lifecycle` resolution returns UNKNOWN for a real specimen, that is an
inexpressibility — a fact about the specimen — and I hand it to a rail author rather than
describing what would express it.** I believe that is the correct handling under
describe-the-specimen, and it is the case most likely to arise in the specimen chain, so I would
rather have it ruled before it happens than adjudicate it mid-flight in the direction that keeps me
moving.
