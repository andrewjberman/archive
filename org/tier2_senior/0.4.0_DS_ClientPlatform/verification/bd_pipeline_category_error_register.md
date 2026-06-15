# BD-Pipeline Category-Error Scan + End-to-End Validation Register

**Mandate:** Andrew-direct (2026-06-15) — a 3-agent drive on the bd pipeline that scans for
**category errors** (a diagnosis resting on a wrong premise) and validates **end-to-end** for
certainty that (1) the diagnosis is actually correct AND (2) the fix is correct AND non-breaking.

**Trio + roles**
- `0.4.0_DS_ClientPlatform` (DS) — data-lane **diagnosis + implementation**; surfaces premise-corrections up front (verify-before-build). **Scribe** of this register.
- `3.0.0_SA_CVO` (CVO, base — the SINGLE trio verifier per Andrew-direct 20260615T191720Z; the spawned `~A` session was a broker-suffix-strip duplicate, flagged to MSTR for reap) — **independent** diagnosis re-derivation + adversarial fix-correctness/non-breaking check. **Certainty gate** — CVO verdicts are authoritative; re-derived from ground truth (live S3 / served), never self-report.
- `0.6.0_AE_PartnerETL` (AE) — bd **chain / dispatcher / deploy / runtime** (infra-side: C4/C5/C6) + `gold_dispatch.sh` (CLOUD_OPS_OR_ETL) wiring legs.

**Scribe rule:** DS records each item + its DS ground-truth re-derive; CVO returns verdicts via MCP and DS transcribes them into the `[CVO]` fields verbatim (CVO may also edit directly). AE fills infra-side fields. Nothing ships without a CVO `(a)/(b)/(c)` PASS.

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

### D1 — 49NNAFIX: 49F canonical NNA publisher  ·  category C1  ·  status SHIPPED (gzip-fixed; ledger L1/L2/L3/L5 closed; only L4 CVO render-confirm open)
- **GATE-4 (CVO 201855Z):** integrity + parse PASS (~291ms, no freeze). DEGRADATION found — falsified my gzip assumption: CF auto-compress caps at 10MB so the ~32MB raw artifact (ContentEncoding=null) was served UNCOMPRESSED. **DS-caught-by-CVO C6 transport-mechanism error.**
- **FIX SHIPPED (81798abf0): pre-gzip at origin.** `_write_json_s3` writes gzipped + `Content-Encoding: gzip`. Served object now **1.76MB** (Size 1,760,321, ETag d37a0ce8, LastModified 20:26:25Z) — CF serves the pre-compressed body past the 10MB cap, browser decompresses. Decompresses to the IDENTICAL parity-exact json (firm MAX $1,373,359,476.76, 50 states, 5350 client leaves, all_pass) — **zero data/dimension loss** (no sampling/top-N/drop). .py re-deployed gzip (md5==ETag 668f873d). Sibling timeseries_chart.json (33.8MB raw) = same-class follow-up for D_00b lane.
- **AE activation (c91a1335 / 0f62f6720):** PHASE_D5 own-phase wired+deployed (runs the gzip .py → 6/16 nightly produces 1.76MB gzipped). runner-IAM CLOSED (bd-exporter-ec2-role bucket-wide PutObject; no staleness trap). Ledger gldinc-d1-d00f L1/L2(v2)/L3(v2)/L5 CLOSED.
- **REMAINING:** L4 = CVO gate-4 RENDER browser-confirm only (5350-client React render-no-freeze; needs authed 49F session; low-risk given sub-second parse + 1.76MB). Transfer + integrity = DONE.
- **CVO gate-c CLEARED (200904Z):** 38MB = TRANSPORT non-breaking (same edge path serves 33.8MB timeseries; Lambda@Edge rewrite→CF/S3, no proxy cap; empty→populated = improvement). "Drop client series" OUT (continuous-ADV drill renders it); reduction lever IF gate-4 freezes = weekly-sample/top-N (reversible).
- **PUBLISHED + served-verified (S3 bytes, not local):** `s3://opal-data-bd/platinum/firm/advisor_nna_canonical.json` (34,019,956 B, LastModified 2026-06-15T20:15:26Z, ETag cd9d4e33). firm_id=49financial, 50 USPS states (0 FIPS, NJ), 61 advisors, reconciliation.all_pass=True/delta=0.0, fee null, firm MAX $1,373,359,476.76 == cumulative_chart parity exact. The previously-EMPTY 49F NNA-geo surface is now populated.
- **AE never-widen distinction (cross-item catch):** D_00f is a served MOVEMENT (empty→34MB), NOT DELTA=0 like A_02/P1 → the CVO size-gate clearance IS its never-widen sign-off. AE C4-verified md5==ETag + caught the PHASE_D5 mechanism (chain:full runs hardcoded PHASE blocks, not catalog lists → list-only wire = silent no-run; own-phase PHASE_D5 is the load-bearing leg).
- **REMAINING:** L4 = CVO gate-4 (live DistributionTab render-no-freeze); AE runner-IAM verify (bd-gold-layer-runner PutObject on platinum/firm/* — else nightly stale after my one-time publish) + PHASE_D5 activation (ongoing freshness) + served-movement deploy_ledger. Then D1 FULLY CLOSED.
- **BUILD RESULT (89d4ac6a7, deployed code/gold md5==ETag 4eab7327; dry-run on live bd S3):** `D_00f.advisor_nna_canonical.py`. AC-F4b.1 PASS, W1 PASS (geo **50 states USPS / 1247 cities / 5350 client leaves**; I1/I2/I3 to-the-cent all 9 windows; W6 all_pass), series-tie exact. **GATE-2 parity anchor EXACT: firm MAX nna $1,373,359,476.76 == served cumulative_chart cumulative total, to the cent.** Gate-1 (schema inf-identical + USPS states + advisors-by-name + fee=null + nmnc/nmec populated + client drill) + Gate-3 (0 FIPS, NJ present) PASS on the validate artifact. Gate-4 (served json + DistributionTab render) PENDING publish.
- **3 impl category-errors the dry-run gate caught (DS own code):** (1) nna_clean flag-vs-value → value=nna_txn; (2) INF_D_00f:478 nna_clean = NaT-drop not bd column → renamed nna_dated (CVO's naming-trap warning, real); (3) bd account_id/relationship_id NON-NUMERIC strings ('z...') → ported int()/to_numeric collapsed dims to empty → fixed to string keys. Each = a confidently-wrong fix killed pre-deploy by the local dry-run gate. Plus float-rounding-accumulation (44 sub-cent W1 fails) → full-precision invariants + round-at-serialize.
- **GATE-C OPEN (CVO + FE call):** artifact = 38MB (inf 2.47MB; bd 15x scale). Correctly-tiered; gzip ~3-5MB but browser parses 38MB + DistributionTab 5350 client leaves. Served publish + AE dispatcher-activation HELD on CVO gate-c verdict (accept vs reduce: top-N clients / drop client series).
- **Premise under test (TO):** "reshape bd `cumulative_chart` `nna_geo`/`nna_adv` into `advisor_nna_canonical.json` — publisher coverage, not new math."
- **DS ground-truth re-derive:** bd served `cumulative_chart.json` `nna_geo`/`nna_adv` = flat **cumulative weekly time-series** (`{description, categories, data:[{date,<STATE>,_inflow,_outflow}]}`), **0 window vocabulary** (grep weekly/monthly/quarterly/window/QTD/1Y/MAX = 0). AC1 requires the **canonical windowed cube** (firm/advisor/geo × weekly/monthly/quarterly + `window_bounds`). inf's `INF_D_00f` derives the canonical from the **atomic** table (`gold/canonical/canonical_nna_{date}.parquet`), NOT cumulative_chart — siblings. ⇒ **premise INSUFFICIENT (C1).**
- **Corrected plan:** PORT `INF_D_00f` → bd publisher (`D_00f.advisor_nna_canonical.py`, POD4) reading bd atomic `gold/canonical/nna/{date}.parquet`; emit `s3://opal-data-bd/platinum/firm/advisor_nna_canonical.json` schema-identical, firm-separated (`firm_id=49financial`), FIPS-defensive (bd `client_state` already 0-leak).
- **Finalized build spec (verify-before-build complete):**
  - advisor grain = `architect`; geo = `client_state` (INLINE on nna rows — no accounts_v2 join inf needs); household/client = `relationship_id`.
  - **NNA value = `nna_txn` (= `daily_inflow - daily_outflow`), NOT `nna_clean`.** ⚠️ DS-caught-by-DS C-error: `nna_clean` is a BOOLEAN quality FLAG (`(components & NNA_CLEAN_MASK)==MASK`, C_01:219), NOT the dollar value — my earlier "nna value = nna_clean" was a flag-vs-value category error; summing it would have produced a garbage publisher. **OPEN CRUX before authoring:** does the canonical sum `nna_txn` over ALL rows or only `nna_clean=True` rows? Must MATCH the existing bd NNA surface convention (cumulative_chart producer) so the canonical agrees with what's already served — trace that aggregation before authoring.
  - **nmnc/nmec = SOURCEABLE** → `accounts_dimension_latest` has `relationship_id` + `relationship_first_seen_date` (household inception, the `first_trade_date` analog). Populate.
  - **client names = SOURCEABLE** → `relationship_display_name`.
  - **fee_paying/no_fee = NULL (not zero)** → bd has NO clean per-account `is_fee_earning` (`advisor_fee_detail` is advisor-grain). Per CVO gate-1: emit null, consumers tolerate it (Inflection precedent). `fee_rate_history`-derivation = possible later follow-up, not v1.
- **(a) Diagnosis certified [CVO]:** **CERTIFIED** (20260615T191233Z, independently re-derived from inf code + live bd S3). (i) cumulative_chart insufficient — CONFIRMED (decisive: `INF_D_00f` L83-85 — cumulative_chart/INF_D_00d is the LOSSY-weekly-sample SIBLING of the same atomic source; canonical is summed from the atomic over window bounds). (ii) bd atomic `gold/canonical/nna` = correct parity source — CONFIRMED (exact cols; geo clean 48 states 0-numeric NJ-present). Real C1.
- **(b) Fix approach certified [CVO]:** **CERTIFIED** — PROCEED with build. (served-verify pending post-deploy.)
- **(c) Non-breaking [CVO]:** **CONFIRMED + STRONGER** — target `opal-data-bd/platinum/firm/advisor_nna_canonical.json` does NOT exist (moves no series; cumulative_chart untouched = never-widen OK) AND the portal ALREADY consumes it (`advisor-intelligence.ts:383` + `DistributionTab.tsx:1237` "SOLE NNA source for GEO state L1/city L2") = populates a live-but-starved consumer, needed now.
- **CVO served-verify gates (post-deploy, on the artifact not rc=0):** (1) schema inf-IDENTICAL (windows QTD/YTD/MAX/1Y/3Y + fee_view + geo) AND matches portal consumer (states USPS-keyed 'TX', advisors by name); (2) firm-separated (reads+writes opal-data-bd only); (3) FIPS-defensive PRESERVED through aggregation (client_state stays USPS, don't reintroduce); (4) verify SERVED json + DistributionTab geo render post-deploy.
- **Owners:** DS (impl) · CVO (verify) · AE 0.6 (`gold_dispatch.sh` wiring leg, CLOUD_OPS_OR_ETL).
- **Status:** **CLEARED-TO-BUILD** (CVO a+approach CERTIFIED). Building the ~900-line port now; deploy gated on CVO served-verify + AE dispatcher-wiring + no COO objection.

### D2 — 49NNAFIX: inf `geo.states` FIPS leak  ·  category C2  ·  status SHIPPED-VALIDATING
- **Diagnosis:** inf served `geo.states` keyed `34` (FIPS) where `NJ` expected; Orion-input inconsistency (silver `accounts_v2` `state='34'` for 2 NJ accounts), our transform never normalizes FIPS→USPS.
- **DS ground-truth re-derive:** served canonical had key `34`, no `NJ`; silver `accounts_v2` (snapshot 2026-06-15) `state='34'`×2, all other 17 values USPS; `INF_D_00f` reads `state` straight. ⇒ Orion input + ours-fails-to-normalize. (Discarded an initial false-positive: 9 `account_count=34` leaf values were NOT state keys.)
- **Fix:** silver `build_accounts_v2` FIPS→USPS map (Rule 17 representation-normalization); non-FIPS/null/`Other`/unknown pass through (no row drop, no business filter). Committed `468f19b7e`, deployed `code/silver/` (md5==ETag), unit-tested, gate-clean.
- **(a) Diagnosis certified [CVO]:** PENDING.
- **(b) Fix correct [CVO]:** PENDING — validates on 6/16 nightly (`geo.states` `34`→`NJ`).
- **(c) Non-breaking [CVO]:** D2 deliberately MOVES served `34`→`NJ` = CTO-pre-accepted drift; before-baseline captured (`verification/ADVI_49NNAFIX/d2_geo_states_before_20260615.json`), after = 6/16. PENDING CVO confirm.
- **Owners:** DS · CVO.

### A_02 — fee_rate_history incremental cutover  ·  category infra(C4/C6)  ·  status DEPLOYED-VALIDATING (AE 0.7-driven)
- **Gate:** 5 consecutive clean value-for-value nights (06-11..06-15) parity DELTA=0 (AE 0.7 signed).
- **Fix:** 3 `gold_dispatch.sh` edits (CATALOG `--incremental`, `INCREMENTAL_CAPABLE="A_00 A_02 C_06"`, `GLDINC_SHADOW_SET` remove). Lane = CLOUD_OPS_OR_ETL (AE — `.owned-paths.yaml`; DS edit would be owned-paths-blocked).
- **Deploy:** DEPLOYED CLEAN 06-15 15:21Z (repo md5==S3 ETag 5a9869b9...; AE 0.6 C4 PASS). First LIVE incremental run = 06-16 nightly.
- **(a)/(b)/(c) [CVO + AE 0.6]:** trio cross-check #1 = 06-16 AM — served output non-regressed + CATALOG actually runs `--incremental` on the REAL runner (not just shadow nights). PENDING (nightly-gated).
- **Owners:** AE 0.7 (drive) · CVO + AE 0.6 (cross-check).

### P1 — GLDINC: load_flows incremental cutover  ·  category infra(C4/C6)  ·  status CUTOVER-READY (AE 0.6 LEAD)  ·  next bd cutover behind A_02
- **Gate:** 7 consecutive byte-identical nights (`gold/_parity/load_flows/`, 06-08..06-15); 06-15 scorecard exact_match_rate=100, key/row deltas=0, all headline diffs 0, clean_night_counter=7, cutover_ready=true, restatement_fallback=false (AE 0.6 ground-truthed).
- **Fix (planned) — CORRECTED (AE ground-truth 191954Z; my first draft was wrong, see Note):** P1/`load_flows` is NOT a standalone script — it's a shared-lib primitive (`load_flows_from_transactions[_windowed]` in `data/black_diamond/scripts/gold/lib/nna_flows.py`); the windowing is INTERNAL to the lib, not a dispatcher flag. So the A_02 3-edit template does NOT apply.
  - **Dispatcher leg (AE, the ONLY dispatcher edit):** REMOVE the `GLDINC_P1_SHADOW` block (`gold_dispatch.sh` ~1308-1327, the `gldinc_p1_shadow.py` stanza). NO CATALOG edit, NO `INCREMENTAL_CAPABLE` edit (C_01/C_02/C_03 carry only `--upload`, no `--incremental` flag plumbed — adding them would no-op/error). `bash -n` clean, 0 functional change (block is non-fatal/observational).
  - **.py leg (DS, POD4):** **α2 (DS lean, pending verify-before-build):** make the oracle entry point `load_flows_from_transactions()` internally delegate to the windowed path — a single switch point in `lib/nna_flows.py`, C_01/C_02/C_03 untouched (byte-identical callers), smallest blast radius. (α1 = edit 3 consumer call-sites; rejected unless α2's verify fails.) The P1 AC1 "oracle unchanged" was a SHADOW-phase invariant; cutover intentionally lifts it. DELTA=0 preserved (windowed == the 7-night shadow-proven result). DS to confirm α2 by reading the lib before authoring.
- **(a)/(b)/(c) [CVO]:** PENDING — sequence behind A_02 + D1; CVO certifies BOTH legs (`.py` α2 switch + dispatcher shadow-removal). AE opens a fresh deploy-completion ledger at cutover-execute (DELTA=0 ⇒ no never-widen hold, mirrors A_02).
- **Owners:** AE 0.6 (lead/parity + dispatcher leg) · DS (`.py` α2 leg) · CVO (cert).
- **Note 1 (DS-caught-by-AE C-error — twin-class-doesn't-transfer):** my first P1 register draft asserted "same mechanics as A_02 (CATALOG `--incremental` + `INCREMENTAL_CAPABLE` add)". WRONG — I transferred the A_02 standalone-script template to a shared-lib primitive without reading P1's own mechanism. AE ground-truthed it (no CATALOG entry, no `--incremental` plumbed, not in `GLDINC_SHADOW_SET`, has its own shadow block). Exactly the "twin's class doesn't transfer — read the candidate's OWN mechanism" trap. Corrected above.
- **Note 2 (AE self-caught C4):** AE nearly reported "P1 stalled — `nna_flows.py` windowed fn never authored" off a `grep lib/nna_flows.py` at repo ROOT (file-not-found ≠ function-absent). Ground-truth re-derive falsified it: real path present, repo md5==deployed md5 (71922f4a...) C4 PASS, P1 live. A wrong-path grep masquerading as "absent" = C4-adjacent self-report trap.

### SCAN-02 — inf-vs-bd served-artifact coverage diff (49F publisher-coverage gap CLASS)  ·  category C1/C5  ·  status CANDIDATES (portal-consumer trace pending)
- **Scan:** diff `opal-data-inf/platinum/firm/` vs `opal-data-bd/platinum/firm/`. inf serves ~12 artifacts bd does NOT: `activity_scan`(+1y/max/qtd/ytd), `cash_drag`(+variants), `concentration_risk`, `client_directory`, `clients_tab`, `firm_composition`, `firm_concentrations`, `nmec_nmnc_nna`, `top_holdings`, `partner_analytics`(base), `header_metrics_fresh`, `advisor_nna_canonical`(=D1).
- **CAVEAT (avoid the category error):** a raw name-diff asserting these as "gaps" is itself a C1/C5 error — inf and bd are different firms with legitimately different surfaces. Each candidate needs a 49financial portal-consumer trace: does a rendered 49F surface consume it (→ REAL gap, fill via inf-publisher port like D1) vs is it inflection-only (→ firm difference, not a gap)?
- **Partial ground-truth (strengthens, doesn't yet close):** 49F IS a partner (`portal/.../AdvisorIntelligence/_partners/49financial/`) and its `index.tsx` renders the firm-agnostic `_shared` surfaces (`DistributionTab`, `PartnerAnalytics`, `AdvisorsTab`, `ClientsTab`) with `BD_SOURCE_ATTRIBUTION`. The candidate artifacts are consumed by those `_shared` components + the inflection panel. D1 (`advisor_nna_canonical`) is the PROVEN instance (CVO: `DistributionTab.tsx:1237` SOLE NNA source — live-but-starved for 49F). So the gap CLASS is real; the per-artifact list is not yet certified.
- **(a) [CVO]:** PENDING — per-artifact 49financial consumer trace (which rendered `_shared`/49F components fetch each missing artifact firm-scoped for bd).
- **Owners:** DS + DE (portal-consumer trace) · CVO (certify which are real gaps). Likely escalates to COO for a coverage-gap PRD if N real gaps confirmed.

### SCAN-01 — bd served geo C2 sweep (FIPS/representation)  ·  category C2  ·  status CERTIFIED-CLEAN (DS; CVO confirm optional)
- **Scan:** bd served `platinum/firm/cumulative_chart.json` geo nodes (`geo`/`nna_geo`/`geo_drill`/`nna_geo_drill`/`geo_aua_grain`) for FIPS-numeric state keys.
- **Result:** CLEAN — all USPS (`AR AZ CA FL GA KS NC NY TX`...), **0 FIPS-numeric**. bd atomic `client_state` also clean (49 distinct, 0 numeric, `NJ` present). ⇒ cross-firm 0-FIPS confirmed (inf via D2, bd already clean at atomic + served).
- **Owner:** DS. (Negative result — no fix needed.)

---

*Scribe: 0.4.0_DS_ClientPlatform. Append new bd-pipeline items as the scan surfaces them; CVO returns (a)/(b)/(c) verdicts; nothing ships without CVO a+b+c PASS.*
