# ADVI_PERFRP — LAYER 5: is the round-1 cell partition MECE over the decomp's 36?

**Seat:** `0.4.0_DS_ClientPlatform~U` · **Stamped:** 2026-08-26T211146Z
**Status: LAYER 5 DISCHARGED** — ruled by `3.0.0_SA_CVO` 73731 and recorded in that cert `@c8eafa5975`; **RATIFIED** by `2.0.0_SA_COO` 73736.
**Push state of `c8eafa5975`: landed LOCAL, rides integration — MEASURED, not defaulted.** Two instruments: it is in `origin/CLOUD..HEAD`
(the local-only set, 9 commits) and `git branch -r --contains c8eafa5975` returns empty; positive control `4424c948f7` correctly returns
`origin/CLOUD`. ⚠ *My first control on this went stale mid-session — `origin/CLOUD` advanced d7cea57dd3 → 81f3dbac08 while I worked, which
turned my negative control positive. A push-state claim is PERISHABLE; the control was re-picked by construction rather than by memory.*
**Subject:** enforcement layer 5, left OPEN by `3.0.0_SA_CVO`'s cert `CERT_ADVI_PERFRP_TO_R1_DS_INSTANCE_20260825.md:29-36`
**Decomp under test:** `workflows/atom_decomposition/runs/advi-perfrp/20260824T201222Z/DECOMP.md` @1ce9b2d6bc (36 cells, CVO-certified @62598c1bfb, 36/36)

---

## 0. THE QUESTION, AND THE DOMAIN CORRECTION THAT COMES FIRST

CVO's cert asks: *"Whether the TO's declared set IS the decomp's complete criterion-bearing set."*

⛔ **THAT QUESTION CANNOT BE ANSWERED ABOUT ONE TO, AND ANSWERING IT THAT WAY PRODUCES A FALSE POSITIVE.**
Read against `TO-R1-DS` alone, `PRF-inv-1` and `PRF-inv-4` are (i) in the decomp, (ii) absent from the TO's 18, and
(iii) **absent from its `<decomp_context>` exclusion prose**, which names `d-*`, `c-2`/`c-3`, `e-1`, `f-1` and neither
of them. That is textbook Rule 24(i) "uncovered member" — and it is **WRONG**. `inv-1` is owned by `TO-R1-DE`;
`inv-4` is owned by `TO-R1-AE`, both in their own issuance halves.

**THE DOMAIN IS THE THREE ROUND-1 TOs JOINTLY, NEVER ONE TO.** Rule 24(i) says name the domain before hunting the
uncovered member; here the domain sits one level above where the question naturally reads. *"Not named in this TO"
is not "owned by nobody."*

---

## 1. INSTRUMENT

Word-boundary `PRF-[a-z]+-\d+` over **the ISSUANCE HALF ONLY** — the `<decomp_ref>` element and the
`cell_refs="..."` attributes — of **every `ADVI_PERFRP.TO-*` face in the estate. DENOMINATOR: 10 files found,
3 carry an issuance half.**

⛔ **THE INSTANCE IS THE WRONG ARTIFACT.** `proof-of-spec-check.py:169` and `:318` read `cell_refs` as declared in
the TO's issuance half, not from the proof instance. `3.0.0_SA_CVO` scanned the instance, got 3 against the
checker's 18, and recorded that reporting it would have been *"a fabricated finding against a lane whose work was
green"* (73642, forwarded by `2.0.0_SA_COO` as 73666). **It fails LOUD, toward a spectacular false finding.**

**Self-control:** for `TO-R1-DS` the two issuance surfaces agree exactly — `decomp_ref == cell_refs`, 18 each.

---

## 2. THE PARTITION — 36 = 30 + 2 + 4

| bucket | n | members |
|---|---|---|
| `TO-R1-DS` | 18 | `a-1..a-6`, `b-1..b-7`, `c-1`, `inv-2`, `inv-3`, `inv-5`, `inv-6` |
| `TO-R1-AE` | 5 | `c-1`, `c-2`, `c-3`, `inv-4`, `inv-5` |
| `TO-R1-DE` | 10 | `d-1..d-8`, `inv-1`, `inv-3` |
| **union of the three** | **30** | 18 + 5 + 10 = 33, minus the 3 shared = **30** |
| CVO-class | 2 | `e-1`, `f-1` |
| declared BOUNDARIES | 4 | `g-1`, `g-2`, `g-3`, `g-4` |

**30 + 2 + 4 = 36. COVERAGE COMPLETE.**

**The six not held by any TO are DECLARED OUT AT THE DECOMP'S OWN FACE — not merely unmentioned:**

| cell | decomp's own words | line |
|---|---|---|
| `PRF-e-1` | "CVO-class (s.11 #14) · a report per client/window on record with denominators" | `DECOMP.md:124` |
| `PRF-f-1` | "CVO-class control" | `DECOMP.md:130` |
| `PRF-g-1` | "**DEFERRED or GAP by ruling** (P-7; s.11 #1, #4, #8) — **no cell, no tile**" | `DECOMP.md:136` |
| `PRF-g-2` | method REUSED not re-derived; the OPAL_GLDRNS wrapper-trio disambiguation is "a routed COO follow-on, **not on this path**" | `DECOMP.md:137` |
| `PRF-g-3` | "INF + COT bindings — at their gates"; `inv-5` is the ONLY per-partner cell | `DECOMP.md:138` |
| `PRF-g-4` | "the Total Assets element + the insurance segment" — `ADVI_INSURE`'s cells; PERFRP shows insurance BESIDE via `inv-2` only | `DECOMP.md:139` |

**Cross-check on the axis most likely to hide an orphan — the invariants:**
`inv-1` DE · `inv-2` DS · `inv-3` DS+DE · `inv-4` AE · `inv-5` DS+AE · `inv-6` DS — **6 of 6 covered.**

---

## 3. EXCLUSIVITY — THE HALF-SPLITS, CHECKED ON *BOTH* FACES

Three cells carry two owners. **A half-split declared on one side only is a live Rule 24(i) exclusivity defect** —
each seat can then believe the other holds it. All three are declared on both faces, with complementary labels:

| cell | DS face | sibling face |
|---|---|---|
| `PRF-c-1` | "(emitter half)" | AE: "(publisher/IAM half)" |
| `PRF-inv-3` | "(producer half)" | DE: "(render half)" |
| `PRF-inv-5` | "(argument contract)" | AE: "(IAM half)" |

**No undeclared overlap. EXCLUSIVITY HOLDS.**

---

## 4. VERDICT

**The `TO-R1-DS` 18 ARE the complete criterion-bearing subset for the DS lane.** The decomp's 36 partition exactly
across three executing TOs, two CVO-class cells and four declared boundaries, with no uncovered member and no
undeclared overlap.

## 5. WHAT THIS DOES **NOT** CLAIM

⛔ **SET-LEVEL ONLY.** This establishes coverage and exclusivity over the cell-**id** space, plus the boundary and
CVO-class declarations read at the decomp's own face. **It does NOT adjudicate whether each cell's CONTENT sits in
the right lane** — whether `c-1`'s "emitter half" truly belongs to DS rather than AE is a semantic judgment on the
decomp's structure. By CVO's own framing (*"requires reading the decomp's structure against the TO's scope"*) that
half is the **cert judgment, which is CVO's**. This artifact exists so that judgment is made on a measured item
rather than a recollection; it does not make it.

**Second limb available on request:** the content-level lane-assignment pass. Sets are loaded; it can run immediately.

---

## Provenance
Measured by `0.4.0_DS_ClientPlatform~U` 2026-08-26T2111Z. Reported as MCP 73689 (`3.0.0_SA_CVO`) / 73690
(`2.0.0_SA_COO`). Seat re-scoped to layer 5 by `2.0.0_SA_COO` 73653 after that seat measured `TO-R1-DS` DISCHARGED
(73631) and the issuer ruled **(b) CONFIRMED DISCHARGED**. Nothing in this work touches
`build_package.py:266`'s stale-pin interlock or `D1_CATVIEWS`.
