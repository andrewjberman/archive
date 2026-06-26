# DATA_PLATFORM D3 -- Orion + Eclipse Architecture Spec

**Status:** DRAFT v0.1 -- 2026-06-26 (0.4.0_DS_ClientPlatform). For PRD S6 row D3 spec-of-record (RAVC CTO to promote to docs/architecture, ANY_CTO lane).
**TO:** `DATA_PLATFORM.D3.orion-eclipse-arch-spec.md`. **Consult:** 0.7.0_AE (auth/infra). **Verify:** 3.0.0_SA_CVO (reconcile vs live inf/Orion pipeline).
**Seeds (grounded):** `data/inf/manual_api/README.md` (Orion Envision), `data/inf/manual_api/PATH_DISCOVERY_MSTAR.md` (Orion Portfolio snapshot), `data/inf/scripts/bronze/pull_eclipse_portfolios.py` (Eclipse, 0.4.0~A-authored = my lane), `docs/architecture/ADVI_ORIAPI.md` (HAR Appendix A, field-level), `INF_B_00.canonical_holdings`.
**PENDING (v1.0 / CVO reconcile):** field-level depth from ADVI_ORIAPI Appendix A.2; the ~3.4% valuation-lag cause/grain/materiality; CVO reconcile vs the live inf/Orion pipeline.

> SPEC ONLY -- no build. Companion to D2 (Black Diamond). Where D2 is a single DataMining surface, D3 spans THREE distinct surfaces across TWO products (Orion + Eclipse) -- and the Eclipse trade/rebalance layer is the genuinely-hard frontier the supplant decision (D5/D4) turns on.

---

## 1. Objective

Orion Advisor is a portfolio-accounting + reporting aggregator (the inf/Inflection book); **Eclipse** (Orion's rebalancing product, a separate web property + ID-space) is the model/trade/rebalance layer. D3 specs the full REST surfaces, the cross-product join model, and the Orion-vs-Eclipse valuation-lag -- so we know what Orion/Eclipse aggregate and where the genuinely-hard trade/rebalance surface sits (vs the displaceable reporting surface). Contrast with D2: BD exposes ONE persisted-query export API; Orion exposes a saved-report export path AND a live Portfolio snapshot path, and Eclipse is a wholly separate product.

## 2. The three surfaces

### Surface 1 -- Orion Envision / ExcelReports (saved-query async export)

The reporting/dim path -- saved Excel-report queries run async + downloaded as CSV. Base `https://api.cloud.orionadvisor.com`. Lifecycle (README + ADVI_ORIAPI A.2):

```
GET  /api/v1/Reporting/Envision/ExcelReports                       -> list saved queries {id,name,category,...}
GET  /api/v1/Reporting/Envision/ExcelReports/Verbose/{id}?expand=all -> saved template incl requiredOptions
POST /api/v1/Reporting/Envision/ExcelReports/{id}/Generate          -> 201 + Location (run URL); 30-60s to ACK
GET  <Location>  (/Reporting/Envision/ExcelReports/Run/{runId})     -> 202 running / 200 + CSV body
```

- **Verbose-is-not-the-runtime-body gotcha:** Verbose returns `null` for `deliveryOptions`/`queryType`/`category`/`databaseIdList` and omits `entityIds`; the Generate body must populate all (`queryType:"Excel"`, `databaseIdList:[4698]`, `deliveryOptions:[DirectDownload/Csv/Aggregate]`, fill `requiredOptions` daterange + select-entity). Direct structural analog of D2's BD thin-envelope-vs-enriched-body.
- **Scope:** `select-entity` `entity:"Database"` + `entityIds:[]` = database-level pull (scope from `databaseIdList`); `entity:"RepresentativeGroup"|"Client"` + explicit `entityIds` = cohort-scoped (ADVI_ORIAPI A.3).
- **Generate is slow** (61s observed to 201; `timeout=180`); `reportFormat:"Xlsx"` returns ZIP-wrapped (detect `PK\x03\x04`).
- A.5 alt path: `POST /api/v1/Homepage/Action/DataSources/{id}` (stored-proc / dashboard-widget pulls) -- exploratory, low-priority.

### Surface 2 -- Orion Portfolio Assets snapshot (the per-day position pass-through)

The cleanest snapshot path (INF_B_00.canonical_holdings; PATH_DISCOVERY_MSTAR.md). Per-day position snapshot per client/account, no async run:

```
GET /api/v1/Portfolio/Clients/{clientId}/Assets/{date}?$top=50000&includeCostBasis=false   # date = MM-DD-YYYY
GET /api/v1/Portfolio/Accounts/{accountId}/Assets/{date}?$top=50000&includeCostBasis=false
GET /api/v1/Portfolio/Accounts/Simple/Search?search={prefix}&top={n}                        # account discovery
GET /api/v1/Portfolio/Lots                                                                   # lot-level (cost basis)
```

This is the snapshot-native value path (the inf analog of BD qt1 holdings) -- a direct per-account-per-day Assets list (MV/units), `includeCostBasis` toggles the lot/basis detail. The cleanest pass-through (PRD S3.3): minimal transform, direct snapshot. `/Portfolio/Lots` is the cost-basis spine (cf. BD's Tax Lot level in D2 §5).

### Surface 3 -- Eclipse (models / portfolios / rebalance)

A SEPARATE product: base `https://www.orioneclipse.com`, separate ID-space + JWT. The model/trade/rebalance layer (`pull_eclipse_portfolios.py`, my ~A lane):

```
GET /v1/portfolio/portfolios/simple   -> all firm portfolios + accountId/modelId join keys (the join spine)
GET /v1/portfolio/portfolios          -> + totalValue/managedValue/excludedValue/cash/lastRebalancedOn/numOfAssociatedAccounts
GET /v1/modeling/models               -> full Eclipse model catalog
GET /v1/modeling/models/{id}          -> per-model detail (AUM + composition tree)
```

- **/simple vs /full are BOTH pulled deliberately:** `/simple` carries `accountId` (the Orion-account join key) which `/full` lacks; `/full` carries the value/cash/rebalance detail `/simple` lacks. Joined on portfolio id in gold.
- This is the surface with no D2/BD analog -- model composition + rebalance state + managed-vs-excluded value = active portfolio MANAGEMENT, not reporting.

## 3. Auth / session / JWT model

- **Orion: Session JWT (HS512, ~10h TTL), header `Authorization: Session <jwt>`** (NOT Bearer). Acquired via Playwright sign-in on `inf-exporter` EC2 (`i-081ae6aafb394fb1a`), stored `s3://opal-data-inf/orion/jwt/current.json` with claims `{a_c:4698 (=DATABASE_ID, Inflection firm), a_ud, a_ed, cid, iss:orion, expires_at_iso}`. Refreshed by the `opal-inf-jwt-fetch` EventBridge cron (08:00 ET daily).
- **CSRF/Origin binding:** every request needs `App:OrionConnect`, `AppPath`, a per-session `BrowserSessionId` UUID, and `Origin`/`Referer` = the orionconnectapp host -- Orion validates these against the session CSRF token (ADVI_ORIAPI A.1). (Contrast D2/BD: a cookie-jar + IP-bind; Orion is JWT + Origin/CSRF-bind.)
- **Eclipse JWT is SEPARATE** (different ID-space). Acquisition priority (`pull_eclipse_portfolios.py`): (1) SM `orion/eclipse_jwt/current`; (2) local file/env; (3) **dynamic exchange** -- Orion JWT from SM -> `GET /v1/admin/Token` -> Eclipse JWT. Header `Authorization: Session <eclipse_jwt>` (also not Bearer). The Orion->Eclipse token exchange is the cross-product auth bridge.
- **OTP / 2FA:** Orion uses SMS 2FA; a persisted browser-profile device-cookie (`s3://opal-data-inf/orion/browser-profile/state.json`) keeps jwt-extract OTP-free (~30-90d); the `inf-otp-relay` Lambda (function URL) serves an OTP web form when required. inf-exporter EC2 stops after each extract (start it before an ad-hoc dispatch).

## 4. The join model (cross-surface + cross-product)

```
Orion DATABASE (a_c=4698, Inflection)
  -> Orion Client {clientId} -> Orion Account {accountId} -> Portfolio Assets snapshot (Surface 2) / Envision dims (Surface 1)
                                         |
                                  accountId (join key)
                                         v
Eclipse Portfolio {portfolioId} --(portfolios/simple: accountId+modelId)--> Eclipse Model {modelId} -> composition tree
                                  (portfolios/full: value/cash/lastRebalancedOn)
```

- **Orion<->Eclipse join = `accountId`** surfaced by `eclipse /portfolio/portfolios/simple` -> maps an Eclipse portfolio to its Orion account(s); `modelId` maps it to the Eclipse model. So the Orion position/value (Surface 2) and the Eclipse model/rebalance state (Surface 3) reconcile per account.
- Within Eclipse, the simple/full join is on portfolio id (§2.3).
- Envision (Surface 1) joins to the same Orion entities via `databaseIdList`/`entityIds` cohort scoping.

## 5. The valuation-lag (~3.4%, Orion vs Eclipse)

Characterized at **~3.4%** (per the inf feasibility briefs / DC-CHAR Orion findings -- cited, not re-derived here; Rule-22: the cause/grain/materiality decomposition is a v1.0 + CVO-reconcile item). Hypothesized drivers to confirm on-reconcile: (a) as-of timing -- Eclipse `lastRebalancedOn` / managed-value vs the Orion Portfolio Assets `{date}` snapshot are different as-of moments; (b) scope -- Eclipse `managedValue`/`excludedValue` partition vs Orion's full account Assets (excluded/held-away positions); (c) intra-day vs EOD pricing. Materiality: at ~3.4% this is a reconciliation/labeling concern for any cross-surface AUA, not a freshness defect -- the consumer must know WHICH surface's value it is showing. **CVO reconcile-on-served decomposes the 3.4% (AC3).**

## 6. The supplant frontier (feeds D5)

Per the DC-REV finding (the trade-plane is the genuine frontier; reporting is displaceable):
- **Surfaces 1 + 2 (Orion reporting + Portfolio snapshot) = T1 displaceable** -- saved-query exports + per-day position snapshots are deterministic repackages of custodian-raw (Fidelity-via-Orion); supplant = obtain the custodian-direct feed + replicate the join/snapshot. The bounded prerequisite (DC-REV): inf has NO Fidelity-direct feed -> Orion is the current ceiling; a Fidelity-direct feed is the load-bearing supplant lever.
- **Surface 3 (Eclipse models/rebalance) = T2-IP, the hard frontier** -- model composition + rebalance/trade generation is genuine vendor algorithm (active portfolio management), not trivially self-built. This is the Orion Dim-7 / DC-CHAR finding: Orion (via Eclipse) EXPOSES a computed trade/rebalance surface below our reach without owning the rebalance engine. The D5 self-build-vs-partner decision turns on THIS surface, not the reporting surfaces.

## 7. PENDING (v1.0 + verification)

- **Field-level depth:** lift the per-endpoint request/response field schemas from `docs/architecture/ADVI_ORIAPI.md` Appendix A.2 (Orion) + the Eclipse response shapes in `pull_eclipse_portfolios.py` into per-surface field tables (this draft specs the surfaces + lifecycle + join + auth; the exhaustive field catalog is the v1.0 fill, analogous to D2's pending qt1 enriched dump).
- **Valuation-lag decomposition (AC3):** confirm the ~3.4% cause/grain/materiality against live (timing vs scope vs pricing).
- **CVO reconcile (AC4):** verify this spec vs the live inf/Orion pipeline (INF_B_00 snapshot read; the Eclipse bronze pull; the join keys resolve).
- **RAVC2 COO + CTO** (AC5) on this draft -> CTO promotes to docs/architecture as v0.1 spec-of-record.

## 8. Cross-references

- **D2** (Black Diamond): the BD DataMining companion. D3's Surface 1 (saved-query export) is the structural analog of BD DataMining; Surface 2 (Portfolio snapshot) is the analog of BD qt1 holdings; BD has no Eclipse-class trade-plane analog.
- **DC-REV** (reverse-ETL map / supplant gradient): D3's §6 frontier (Orion reporting T1 / Eclipse trade-plane T2-IP) is the Orion-vendor row of the DC-REV tier table; inf is bounded at Orion (no Fidelity-direct) -- the custodian-direct-feed lever.
- **D5** (gold-replicate / self-build-vs-partner): consumes §6 -- the Eclipse trade/rebalance surface is the decision pivot.
- **D4** (informs the self-build-vs-partner economics with D5).
