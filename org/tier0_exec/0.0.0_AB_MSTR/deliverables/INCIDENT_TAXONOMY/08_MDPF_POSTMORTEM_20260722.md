# TAXONOMY 08 — `docs/references/MDPF_POSTMORTEM_20260722.md`

    size:      9,481 B / 149 lines
    modified:  2026-07-22
    role:      postmortem of OPAL_CONSOLIDATION / MDPF_REVAMP / MDPF_3FIRMS. Authored by
               0.0.0_AB_MSTR at Andrew's direct request. The document TRIGGER_LAYER was derived from
    axes:      see AXES.md

---

## 1. STRUCTURAL MEASUREMENT

149 lines: provenance note · **the one-sentence finding** · the defect class (RF ledger table) ·
"the part that should sting" · where the ontology is pointed wrong · solutions ranked · what NOT to
build · the honest meta-point · addendum.

**It opens by classifying itself.** The provenance note records that the document was dispatched as
required input reading to three lanes **while existing in no committed form**, caught by
`1.0.0_SA_CTO~Z` on load. *"Sixth-and-a-half instance of the class in one day, authored by the agent
who wrote it up."*

---

## 2. CLASSIFIED INCIDENTS

| # | incident | E | S | F | M | Det | Dir | Rec |
|---|---|---|---|---|---|---|---|---|
| 1 | RF-1 `PUBLISH_MAP` hardcoded 9-entry dict → `9/9 all_present=True` while Cottonwood is never served | E1 | S1 | F1 | M1 | D4 | X-CLEAN | N0 |
| 2 | RF-2 freshness gate partner set = one-element dict → Cottonwood staleness **never evaluated** | E1 | S1 | F8 | M1 | D4 | X-CLEAN | N0 |
| 3 | RF-3 six global fold sites null every pre-07-21 row → renders as **honest nulls, not an error** | E1 | S1 | F1 | M5 | D4 | X-CLEAN | N0 |
| 4 | RF-5 producer orchestration fixed at two firms while its helpers were already N-firm generic | E1 | S1 | F1 | M4 | D4 | X-CLEAN | N0 |
| 5 | RF-6 audit marker keys derived from config, not the world → controls 1–4 all pass on a cycle missing a firm | E1 | S1 | F8 | M1 | D4 | X-CLEAN | N0 |
| 6 | RF-9 `.xlsx` hardcoded in the converter **regex** → an S3-filter fix alone is a GREEN no-op | E1 | S1 | F8 | M8 | D4 | X-CLEAN | N0 |
| 7 | **`comp-constants check` ran thousands of times across the arc and never fired** — WRONG AXIS: it detects drift, and every firm map agreed perfectly while uniformly missing a firm | E1 | S7 | F8 | M6 | D7 | X-CLEAN | N0 |
| 8 | …WRONG LANGUAGE: the extractor is `ast.parse()`, Python-only; the one lane covering firm enumeration is `.mjs`/`.ts` | E1 | S7 | F1 | M6 | D7 | X-CLEAN | N0 |
| 9 | …WRONG ARTIFACT: the finding was recorded in a `notes:` free-text string — data for a human, not a gate condition | E1 | S6 | F8 | M14 | D7 | X-CLEAN | N0 |
| 10 | RF-14 `dump_enriched_templates.py` **exists, is gate-clean, and was never run** — while 4 months were spent ingesting BD at the wrong level | E1 | S10 | F1 | M14 | D4 | X-CLEAN | N0 |
| 11 | the ontology models firm as a **variance dimension** (never interchangeable) and has no concept of firm as an enumerable population with cardinality | E1 | S7 | F1 | M6 | D4 | X-CLEAN | N0 |
| 12 | **this postmortem itself was dispatched as required reading while uncommitted** | E1 | S6 | F8 | M14 | D4 | X-CLEAN | **N-SELF** |

**12 classified incidents.**

---

## 3. DISTRIBUTION

**Mechanism:** M1 **3** · M6 **3** · M14 **3** · M5 **1** · M4 **1** · M8 **1**

**Epistemic type:** E1 **12 (100%)** — *every single incident in this file is a FALSE-CLEAN.*

**Failure direction:** X-CLEAN **12 (100%)**

**Detection:** D4 **8** · D7 **4** · **D1 = 0** · **D2 = 0**

**Recurrence:** N-SELF **1**

> **100% E1 / 100% X-CLEAN / 0% designed-control.** No other file in the corpus is this uniform. This
> is what a single coherent failure class looks like when it is written up honestly: **an entire
> quarter's most expensive defect had exactly one shape and produced exactly one signal — green.**

---

## 4. DOCUMENT-SPECIFIC FINDINGS

**4.1 — The one-sentence finding is the corpus's best compression of M1:**

> **"Nearly every expensive defect across this arc was a structure that hardcoded the set of firms —
> and every detector we own is built to catch DISAGREEMENT between sites, while all of these were in
> perfect agreement and uniformly incomplete."**

**Adding a third firm did not break the code. It revealed that "two firms" was compiled into ~6
independent places, each internally consistent, each reporting green.**

**4.2 — The eleven-week timeline is the most damning artifact in the estate.** On **2026-05-08** the
`comp-constants-seed-multifirm.yaml` notes stated the defect verbatim, in the right file, naming
Cottonwood's absence from `FIRM_CONFIG` and `FIRM_BUCKET_MAP`. On **2026-07-22** MDPF_3FIRMS
discovered ~6 hardcoded firm enumerations missing Cottonwood. **The finding was written down eleven
weeks before it cost a quarter, inside a tool wired into the live universal commit gate that ran
thousands of times.** Three stacked blindnesses (wrong axis / wrong language / wrong artifact) meant
it could stop nobody.

> **"THE RECURRING FAILURE IS NOT MISSING INSTRUMENTS. IT IS INSTRUMENTS THAT EXIST, ARE CORRECT,
> AND HAVE NO TRIGGER."**

**4.3 — "Where the ontology is pointed wrong" is the deepest structural claim in the corpus.** The
rule bank models firm as a **variance dimension** — *firms NEVER interchangeable, adapter denies* —
which is a rigorous encoding of the SEPARATION hazard, heavily guarded by IAM deny, commit gate, and
`comp-firmsep-sweep`. **It has no concept of firm as a set that structures must be COMPLETE over.**

> **"OUR GUARDS ENCODE THE LAST INCIDENT, NOT THE CURRENT RISK. Cross-firm contamination is heavily
> instrumented. Firm OMISSION — which cost this entire quarter — is instrumented nowhere, in a system
> with 89 comp-tools."**

**4.4 — "What NOT to build" is the rarest section in the corpus.** *More detectors.* The estate has
89 comp-tools and the instrumentation is genuinely strong; **the gap is the trigger layer.** This is
the only place in 168KB that tells an agent to stop building instruments — and it is in a reference
file, not in doctrine.

**4.5 — The addendum closes the loop the same evening**: two enumeration-completeness gates were
built within hours. **"Findings got owners and gates the same evening. The eleven-week `notes:` line
had neither."** The diagnosis is therefore a demonstrated mechanism, not a proposal.

---

## 5. PRUNE VERDICT

| move | effect |
|---|---|
| **KEEP ENTIRE** | reference tier, dated, correctly placed, and it is the source TRIGGER_LAYER was derived from |
| **PROMOTE §"the ontology is pointed wrong"** | the separation-vs-omission asymmetry is a live architectural gap, not a historical note |
| **PROMOTE "what NOT to build" into doctrine** | it is the only anti-instrument-proliferation clause in the corpus and it currently sits in a reference file where doctrine cannot see it |
| **NOTE the 11-week timeline in AXES.md** | it is the empirical proof of M14's cost |

**KEEP. This 9KB file carries more decision-relevant content than any 30KB slice of the doctrine tier.**
