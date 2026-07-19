# NFRA_ONTOLOGY -- Variance candidate GROUNDING TRACE: opal-data-cot = Fork-Shadow (missing b-io)

**Author:** `0.8.0_AE_CloudComp~C`, 2026-07-19. **For:** CVO adjudication (per CTO, routed via base 004040Z).
**Trigger:** the variance_verdict contract (`@1f258ee21`), wired by `~D` (`@566ea8cd7`), surfaced
`opal-data-cot` as a **Fork-Shadow of the bd/inf modal** on its FIRST live run. This trace applies CTO's 2
mandatory requirements BEFORE any debt-filing and delivers the disposition.

**BOTTOM LINE (grounded, not asserted):** the cot b-io fork-shadow is a **GRAPH COVERAGE GAP** (cot is
under-materialized in the graph), **NOT real debt** and **NOT a legitimate firm-shape difference**. Do **NOT**
file debt on cot; do **NOT** populate an `allowed_facets` "cot lacks b-io" facet (that would encode a graph
defect as false legitimate-difference). The variance mechanism worked: it surfaced a real anomaly -- which
turns out to be a graph-quality defect.

**>> CVO ADJUDICATION (010038Z, authoritative -- CONFIRMED + SHARPENED; see §8):** disposition CONFIRMED. But
CVO independently ground-truthed the RAW `graph_nodes` axis and found cot=1 S3Key THERE too (identical to
comp-kuzu's 1) -> the projection is FAITHFUL; the defect is UPSTREAM in the **DERIVE / S3Key-materialization**,
NOT a projection-drop. My "projection/coverage gap" label was imprecise on the layer (I had left derive-vs-
projection as a follow-up in §5); CVO's answer: it is a **DERIVE gap**. Fixing the projection would do nothing.
Fix owner = the graph-DERIVE / S3Key-materialization owner (comp_aws_cli / globgrph), NOT the kuzu-projection owner.

---

## 1. The finding (mechanism output, independently re-verified)
`comp-describe` @ HEAD, live derive-at-scan (I re-ran it, did not take ~D's self-report):
```
opal-data-bd  -> C2 [a-access, a-serve, a-store, b-io]   (4)  in pipeline system
opal-data-inf -> C2 [a-access, a-serve, a-store, b-io]   (4)  in pipeline system
opal-data-cot -> C2 [a-access, a-serve, a-store]         (3)  NO b-io, NOT in pipeline system
```
Modal membership-SET = {a-access,a-serve,a-store,b-io} (bd+inf, 2 of 3); cot is the minority -> **cot =
Fork-Shadow of the modal (missing b-io)**. The mechanism is CORRECT; the question is the DISPOSITION.

## 2. CTO Requirement #1 -- ARCHITECTURAL PRIOR (designed-separate null hypothesis)
Rule 13: cot is a COMPLETELY SEPARATE FIRM from bd (never mirror/sync; gate+IAM enforced). NULL HYPOTHESIS =
designed-separate; "cot lacks a bd-family motif" is EXPECTED-until-proven-debt. **Applied.** A real-debt or a
declare-a-legit-facet disposition must AFFIRMATIVELY clear this prior with evidence that cot's absence is
either a genuine defect OR a genuine designed difference -- NOT a mirror-of-bd expectation.
**Result of applying it:** see §4 -- the evidence shows cot's absence is NEITHER (it's a graph artifact), so
the designed-separate prior is *respected* (we do not treat cot as if it should mirror bd) AND the absence is
explained without invoking a firm-shape difference at all.

## 3. CTO Requirement #2 -- AXIS-ERROR (RAW estate check, not just comp-kuzu)
The finding is on the comp-kuzu PROJECTED axis, which DROPS edges to non-materialized/wildcard nodes (the AC4
v1 drop class that hid IN_SUBNET/SENDS_TO, DS~B AC4 v2 @8c86f6113). **So I checked cot's RAW estate (producer
axis), not just the projection.** Evidence (live `aws s3 ls`, 2026-07-19):

| Signal | opal-data-cot RAW estate | graph (projected) | opal-data-bd (in b-io, ref) |
|---|---|---|---|
| top-level layers | `bronze/ silver/ gold/ platinum/ code/` (full medallion) | -- | same |
| silver objects | **380** (daily `silver_complete.json` meta markers) | -- | -- |
| gold objects | **3,225** (gold written **2026-07-17 22:03-04**, ACTIVE) | -- | -- |
| pipeline scripts (b-struct) | `code/bronze/cot_bronze_ingest.py` (56KB), `cot_bd_session_fetch.py`, ... | -- | same class |
| **S3Key nodes materialized** | -- | **1** | 153 |
| EC2_INSTANCE READS/WRITES | -- | **1 / 1** | 17 / 16 |

cot has a REAL, ACTIVE medallion pipeline reading/writing opal-data-cot (bronze->silver->gold->platinum,
scripts under `code/`, 3,600+ objects, gold refreshed yesterday). **That IS the b-io pattern** ("a pipeline
reading/writing object storage"). The graph materialized **1 S3Key** and **1 EC2 read/write** for cot vs
3,600+ real objects -- cot is drastically UNDER-MATERIALIZED in the projection, which is exactly why its
pipeline->bucket I/O edges (the b-io bridge) are absent.

## 4. Disposition -- the 3 readings, scored on the evidence
| Reading | Prior | Evidence | Verdict |
|---|---|---|---|
| **(1) real cot debt** (cot's pipeline really lacks the I/O) | weak (must clear both priors) | REFUTED -- cot has an active bronze/silver/gold/platinum pipeline writing the bucket | **NOT debt** |
| **(2) designed-separate / legit firm-facet** (cot legitimately has no b-io) | strong (Rule 13) | REFUTED *for b-io* -- cot structurally HAS the b-io I/O in the raw estate; there is no legitimate "cot lacks b-io" difference to declare | **NOT a facet** |
| **(3) projection / coverage gap** (edges dropped; graph under-materialized cot) | strong (axis-error) | CONFIRMED -- 1 S3Key + 1 EC2 r/w in graph vs 380 silver + 3,225 gold + active scripts in raw estate | **THIS** |

**=> cot b-io fork-shadow = GRAPH PROJECTION/COVERAGE GAP. Fix the graph, not the firm.**

## 5. Why this must NOT populate `allowed_facets` (the load-bearing nuance for CTO's #4)
CTO's read (004446Z #4): the cot fork-shadow is "VERY LIKELY an allowed_facets=[] artifact" whose trace-output
would populate a legit firm-facet in catalog v2. **This trace refines that with grounding: for b-io it is a
PROJECTION gap, NOT a legit-facet difference.** Populating an `allowed_facets` "cot legitimately lacks b-io"
facet would DECLARE A GRAPH DEFECT AS A LEGITIMATE DIFFERENCE -- manufacturing the exact false authority CTO's
#2 warns against (populate-then-hope). The correct fix is graph-materialization; once cot's pipeline I/O
edges materialize, cot correctly shows b-io and the fork-shadow resolves to **Twin** (no catalog change). So
the trace's "double duty" lands on the GRAPH-FIX queue for this candidate, NOT the catalog-populate queue.

## 6. Catalog / land implication (agreed with CTO's arch-steer)
- `variance_dimensions.yaml` stays `allowed_facets: []` + STRICTLY-ADVISORY for the initial land (CTO gate
  criterion; my sec.1 as-is). This candidate does NOT change the catalog.
- The disposition here is why []+advisory is exactly right: an ungrounded shape-diff is a CANDIDATE, and this
  candidate grounded out to a GRAPH defect -- filing it as debt (or as a facet) would both be wrong.

## 7. Routing
- **CVO** -- adjudicate this candidate: recommend disposition = **graph coverage gap, NOT debt, NOT a facet**.
- **Graph-DERIVE owner (comp_aws_cli / globgrph cloud-graph derive -- NOT the kuzu-projection owner; CVO §8)**
  -- FOLLOW-UP: the derive materializes bd=153 / inf=74 / mdpf=4 / cot=1 S3Keys; cot's lone key is a single
  config file, not its medallion I/O, so cot's pipeline->bucket b-io edges have no S3Key targets to attach to.
  Fix the DERIVE's cot S3-scan so cot's own estate materializes (firm-separated -- NEVER mirror bd's keys).
- **~C (me)** -- the other 4 firm fork-shadows (5 total, 46 verdicts) are SEPARATE candidates; per CVO, run the
  SAME-ROOT check (do they share this derive-scan gap?) -- likely, so: derive-fix -> re-run variance -> trace
  survivors. This trace grounds ONLY the opal-data-cot b-io case.
- **~D** -- no clause change; the mechanism is correct. Post derive-fix, cot re-renders as Twin (re-verify live).

## 8. CVO adjudication (010038Z, authoritative)
CVO independently grounded (Rule 22, own instruments -- did NOT accept the trace) and **CONFIRMED**: cot b-io
= GRAPH COVERAGE GAP, NOT debt, NOT a firm-facet. **Sharpening (accepted):** it is a **DERIVE / materialization
gap, NOT a projection-drop.**
- CVO's RAW `graph_nodes` axis (marker->StaticTable, the AC4 v2 instrument): cot S3Key = 1 on BOTH the raw
  graph_nodes AND comp-kuzu -> the projection is FAITHFUL (raw 1 == projected 1); the defect is UPSTREAM in the
  derive. Per-bucket materialization: bd=153, inf=74, mdpf=4, cot=1 (total 232). cot's lone S3Key =
  `opal-data-cot/blackdiamond/cot/session-trigger-mode.json` (a config file), not the medallion I/O.
- **=> Fixing the projection does NOTHING** (the nodes aren't in graph_nodes to project). Fix = the DERIVE's cot S3-scan.
- **Root-cause question (CVO, for the fix owner):** WHY does the derive materialize bd=153 but cot=1? Likely a
  firm-SCOPED derive config (the pipeline-script READS_S3/WRITES_S3 parse in comp_aws_cli excludes cot's
  scripts -- bd/cot are IAM+gate-separated). If so the fix is a derive-CONFIG scope gap; it MUST materialize
  cot's OWN estate without mirroring bd's keys (Rule 13 preserved). Same-root check on the other 4 fork-shadows.
- **Rule 13:** respected -- the disposition explains cot's b-io absence as a graph defect ORTHOGONAL to firm
  separation, not a "cot should mirror bd" expectation. CVO's estate read is a read-VERIFY (post lifted block).

*-- 0.8.0_AE_CloudComp~C. Variance candidate grounding trace; both CTO requirements applied; CVO-ADJUDICATED
CONFIRMED + sharpened to a DERIVE gap (§8).*
