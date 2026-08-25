# Task Order: ADVI_49NNAFIX — D1 canonical-NNA publish + D2 FIPS-34 lineage-rectify

**Status:** complete -- active -- D1 SHIPPED + FULLY CERTIFIED (ledger eb0cd93ee CLOSED + CVO gate-4 PASS + 06-16 nightly CLEAN PASS 8aba8c4b0); D2 FIPS '34'->'NJ' rectification SHIPPED (de1bb995d). CLOSE-ELIGIBLE pending CVO D2 FIPS-leak/USPS-uniform acceptance. [recon 2026-06-16 COO] -- SPRING-CLEAN 2026-08-25: project ADVI_49NNAFIX is complete; TO last touched 2026-06-16 predates project close 2026-06-16. Record act, not a work verdict.


**Project:** ADVI_49NNAFIX (1a3daf344, Andrew-direct ASAP)
**Assigned to:** 0.4.0_DS_ClientPlatform (data lane — canonical publisher + lineage)
**Design doc (PRD-grade, no re-authored PRD):** `docs/briefs/advi-49nnafix-project-request-20260612.md` (DE's brief — FE control-trace + live-S3 ground truth)
**Authority:** Andrew-direct via DE diagnosis → CTO registration 1a3daf344 → COO decomposition
**SEQUENCING (binding):** next-in-DS-queue **AFTER the live P0 recovery closes (R4/R5)** — does NOT preempt it. Then slots against ADVI_COTSNP.P0 at COO discretion; Andrew priority on THIS one is explicit.

---

## Context — DE's FE-vs-data triage (the discrimination that made registration instant)

Andrew surfaced 5 Segment Analytics bugs. DE traced FE control → live S3 ground truth and split them: **3 = DATA** (this TO), **1 = FE** (portal/RD lane, tracked separately — see below), and the OFC path works because it reads a DIFFERENT artifact (that discrimination is what proved these are publisher/data gaps, not FE).

---

## D1 — Publish `advisor_nna_canonical.json` for 49F/bd (publisher coverage, NOT new derivation)

49F's Continuous-NNA GEO/ADV views are EMPTY because the canonical artifact is missing — but the **inputs already exist** in 49F `cumulative_chart` (`nna_geo` / `nna_adv`). This is publisher COVERAGE, not new math.

- Publish `advisor_nna_canonical.json` with **schema-parity to inflection**: firm / geo / advisor series x weekly / monthly / quarterly + `window_bounds`.
- **Empty -> populated NEW surface** = standard verify, **NO never-widen hold** (CTO-confirmed: nothing served moves; a previously-empty view gains data).
- AC1: 49F Continuous-NNA GEO + ADV populate, schema-identical to inflection's canonical; weekly/monthly/quarterly all present with window_bounds.

## D2 — FIPS-34 leak in inflection `geo.states` — ASSESS lineage, then RECTIFY (Andrew-elevated)

Inflection `geo.states` leaks the FIPS numeric `'34'` where it should read `'NJ'`.

- **ASSESS via lineage trace:** bronze Orion-raw -> silver -> canonical. Determine whether `'34'` is an **Orion INPUT error** (arrives wrong from the source) or **OURS** (a transform drops the USPS mapping).
- **RECTIFY either way:** canonical `geo.states` = uniform USPS abbreviations, **0 FIPS leaks across BOTH firms** (49F + inflection). If Orion-input: map at the correct tier (don't silently fix in gold if silver should standardize — but per Rule 17, FIPS->USPS standardization is a dtype/representation normalization, confirm the correct tier in the trace). If ours: fix the dropping transform.
- **D2 MOVES served inflection output** (`'34'` -> `'NJ'`) = a **small justified drift-acceptance** — capture before/after in this TO's verification (the drift is the correction itself; CTO pre-accepted the shape).
- AC2: lineage trace documents Orion-vs-ours; canonical geo.states = uniform USPS, 0 FIPS leaks BOTH firms; before/after served diff captured.

---

## In-project DEFERRED (non-blocking, executor's choice)
- **Annual NNA series** (Year interval currently dead): DS emits the annual series OR FE hides the Year toggle — executor's choice, non-blocking on D1/D2.

## SEPARATE — do NOT absorb into this TO (tracked as its own item)
- **advisor-drill Continuous-ADV-AUM toggle regression** = a **PORTAL/FE bug** (interval/window dropped), **DE/RD lane**. The 4th of Andrew's 5 bugs. Routed separately by COO so it isn't miscategorized as data. NOT this DS TO's scope.

---

## Gates / standard discipline
- `from __future__ import annotations` on any gold/silver/bronze .py touched; `.tools/ds-commit-gate.sh` per .py edit.
- Rule 17: silver = dedup + dtype-standardization only; FIPS->USPS representation normalization — confirm the correct tier in the D2 trace, don't business-filter.
- Cross-firm separation: 49F/bd vs inflection both touched — keep firm buckets separate (no cross-ref); both must end at 0 FIPS leaks but via each firm's own path.
- DS owns the full commit->QA-deploy cycle (incl. aws s3 cp); validate on the SCHEDULED nightly artifacts, not an ad-hoc run.

## RAVC2 to COO
D1: 49F Continuous-NNA populated + schema-parity verified on the served canonical. D2: lineage-trace finding (Orion-vs-ours) + 0-FIPS-leak both firms + before/after served diff. CC CTO + CVO + DE (DE diagnosed it).

---

*Authored by 2.0.0_SA_COO 20260612T222000Z — Andrew-direct full-drive; CTO handoff 1a3daf344*
*QUEUED post-R5 (live P0 recovery closes first); DS picks up next — NOT an active-GO while P0 in-flight*
