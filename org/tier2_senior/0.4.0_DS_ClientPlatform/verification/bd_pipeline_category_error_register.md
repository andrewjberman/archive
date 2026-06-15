# BD-Pipeline Category-Error Scan + End-to-End Validation Register

**Mandate:** Andrew-direct (2026-06-15) — a 3-agent drive on the bd pipeline that scans for
**category errors** (a diagnosis resting on a wrong premise) and validates **end-to-end** for
certainty that (1) the diagnosis is actually correct AND (2) the fix is correct AND non-breaking.

**Trio + roles**
- `0.4.0_DS_ClientPlatform` (DS) — data-lane **diagnosis + implementation**; surfaces premise-corrections up front (verify-before-build). **Scribe** of this register.
- `3.0.0_SA_CVO` (CVO~A) — **independent** diagnosis re-derivation + adversarial fix-correctness/non-breaking check. **Certainty gate** — CVO~A verdicts are authoritative; re-derived from ground truth (live S3 / served), never self-report.
- `0.6.0_AE_PartnerETL` (AE) — bd **chain / dispatcher / deploy / runtime** (infra-side: C4/C5/C6) + `gold_dispatch.sh` (CLOUD_OPS_OR_ETL) wiring legs.

**Scribe rule:** DS records each item + its DS ground-truth re-derive; CVO~A returns verdicts via MCP and DS transcribes them into the `[CVO~A]` fields verbatim (CVO~A may also edit directly). AE fills infra-side fields. Nothing ships without a CVO~A `(a)/(b)/(c)` PASS.

---

## Category-error taxonomy (the premise errors we hunt)

A category error makes a diagnosis **confidently wrong**, so a fix built on it is wrong or breaking. The gate for every class: **re-derive the diagnosis from ground truth (live S3 / served artifact / deployed code) BEFORE accepting the diagnosis OR the fix.**

- **C1 SOURCE / GRANULARITY mismatch** — diagnosis names a source that's the wrong shape/grain for the target schema.
- **C2 REPRESENTATION inconsistency** — same semantic, wrong encoding, passed through un-normalized (e.g. FIPS `34` vs USPS `NJ`).
- **C3 PRESENCE / ABSENCE artifact** — data reads as absent when it's present-but-zero, or a query drops a dimension (`SampleCount>0` is the tell).
- **C4 SELF-REPORT vs SERVED** — trusting `rc=0` / producer claim / proxy instead of the served artifact / live state (stale-deployed-script class).
- **C5 LANE / OWNERSHIP mis-attribution** — work routed to the wrong owner/lane.
- **C6 MECHANISM / STATE conflation** — a gate/control keyed on the wrong mechanism or state (e.g. sentinel keyed data-day vs serving-day; `set-alarm-state` re-flip in-period; Lambda@Edge rewritten-uri).

**Validation bar (per item):** (a) **diagnosis certified** (independently re-derived from ground truth) · (b) **fix correct** (achieves the AC, verified on served/nightly artifact — no ad-hoc gold runs) · (c) **fix non-breaking** (no served-output regression, no downstream-consumer break, never-widen respected — DELTA proven or sign-off obtained).

Status legend: `OPEN` · `DX-VERIFY` (CVO re-deriving diagnosis) · `BUILD-HELD` · `SHIPPED-VALIDATING` · `CERTIFIED` (CVO a+b+c PASS) · `REJECTED`.

---

## Items

### D1 — 49NNAFIX: 49F canonical NNA publisher  ·  category C1  ·  status DX-VERIFY / BUILD-HELD
- **Premise under test (TO):** "reshape bd `cumulative_chart` `nna_geo`/`nna_adv` into `advisor_nna_canonical.json` — publisher coverage, not new math."
- **DS ground-truth re-derive:** bd served `cumulative_chart.json` `nna_geo`/`nna_adv` = flat **cumulative weekly time-series** (`{description, categories, data:[{date,<STATE>,_inflow,_outflow}]}`), **0 window vocabulary** (grep weekly/monthly/quarterly/window/QTD/1Y/MAX = 0). AC1 requires the **canonical windowed cube** (firm/advisor/geo × weekly/monthly/quarterly + `window_bounds`). inf's `INF_D_00f` derives the canonical from the **atomic** table (`gold/canonical/canonical_nna_{date}.parquet`), NOT cumulative_chart — siblings. ⇒ **premise INSUFFICIENT (C1).**
- **Corrected plan:** PORT `INF_D_00f` → bd publisher reading bd atomic `gold/canonical/nna/{date}.parquet` (cols `date, account_id, architect`=advisor, `client_state`=geo, `nna_clean, daily_inflow/outflow`); emit `s3://opal-data-bd/platinum/firm/advisor_nna_canonical.json` schema-identical, firm-separated, FIPS-defensive (bd `client_state` already 0-leak).
- **(a) Diagnosis certified [CVO~A]:** IN PROGRESS — CVO~A re-deriving (i) cumulative_chart insufficiency, (ii) atomic `gold/canonical/nna` is the correct parity source, (iii) port is additive + non-breaking.
- **(b) Fix correct [CVO~A]:** PENDING (build held).
- **(c) Non-breaking [CVO~A]:** PENDING — additive NEW artifact, no existing served series moved (to confirm).
- **Owners:** DS (impl) · CVO~A (verify) · AE (`gold_dispatch.sh` wiring leg, CLOUD_OPS_OR_ETL).
- **Notes:** premise correction surfaced to COO 182220Z; build held for CVO~A (a) + COO greenlight.

### D2 — 49NNAFIX: inf `geo.states` FIPS leak  ·  category C2  ·  status SHIPPED-VALIDATING
- **Diagnosis:** inf served `geo.states` keyed `34` (FIPS) where `NJ` expected; Orion-input inconsistency (silver `accounts_v2` `state='34'` for 2 NJ accounts), our transform never normalizes FIPS→USPS.
- **DS ground-truth re-derive:** served canonical had key `34`, no `NJ`; silver `accounts_v2` (snapshot 2026-06-15) `state='34'`×2, all other 17 values USPS; `INF_D_00f` reads `state` straight. ⇒ Orion input + ours-fails-to-normalize. (Discarded an initial false-positive: 9 `account_count=34` leaf values were NOT state keys.)
- **Fix:** silver `build_accounts_v2` FIPS→USPS map (Rule 17 representation-normalization); non-FIPS/null/`Other`/unknown pass through (no row drop, no business filter). Committed `468f19b7e`, deployed `code/silver/` (md5==ETag), unit-tested, gate-clean.
- **(a) Diagnosis certified [CVO~A]:** PENDING.
- **(b) Fix correct [CVO~A]:** PENDING — validates on 6/16 nightly (`geo.states` `34`→`NJ`).
- **(c) Non-breaking [CVO~A]:** D2 deliberately MOVES served `34`→`NJ` = CTO-pre-accepted drift; before-baseline captured (`verification/ADVI_49NNAFIX/d2_geo_states_before_20260615.json`), after = 6/16. PENDING CVO confirm.
- **Owners:** DS · CVO~A.

### A_02 — fee_rate_history incremental cutover  ·  category infra(C4/C6)  ·  status SHIPPED-VALIDATING (AE 0.7-driven)
- **Gate:** 5 consecutive clean value-for-value nights (06-11..06-15) parity DELTA=0 (AE 0.7 signed).
- **Fix:** 3 `gold_dispatch.sh` edits (CATALOG `--incremental`, `INCREMENTAL_CAPABLE +A_02`, `GLDINC_SHADOW_SET` remove). Lane = CLOUD_OPS_OR_ETL (AE — confirmed `.owned-paths.yaml:844`; DS edit would be owned-paths-blocked).
- **(a)/(b)/(c) [CVO~A + AE 0.6]:** parity-gate cross-check + 06-16 post-nightly served-didn't-move verify — PENDING.
- **Owners:** AE 0.7 (drive) · CVO~A + AE 0.6 (cross-check).

### SCAN-01 — bd served geo C2 sweep (FIPS/representation)  ·  category C2  ·  status CERTIFIED-CLEAN (DS; CVO confirm optional)
- **Scan:** bd served `platinum/firm/cumulative_chart.json` geo nodes (`geo`/`nna_geo`/`geo_drill`/`nna_geo_drill`/`geo_aua_grain`) for FIPS-numeric state keys.
- **Result:** CLEAN — all USPS (`AR AZ CA FL GA KS NC NY TX`...), **0 FIPS-numeric**. bd atomic `client_state` also clean (49 distinct, 0 numeric, `NJ` present). ⇒ cross-firm 0-FIPS confirmed (inf via D2, bd already clean at atomic + served).
- **Owner:** DS. (Negative result — no fix needed.)

---

*Scribe: 0.4.0_DS_ClientPlatform. Append new bd-pipeline items as the scan surfaces them; CVO~A returns (a)/(b)/(c) verdicts; nothing ships without CVO~A a+b+c PASS.*
