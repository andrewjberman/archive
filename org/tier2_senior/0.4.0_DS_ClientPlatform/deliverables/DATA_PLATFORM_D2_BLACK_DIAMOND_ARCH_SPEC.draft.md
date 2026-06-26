# DATA_PLATFORM D2 -- Black Diamond Architecture Spec

**Status:** DRAFT v0.1 -- 2026-06-26 (0.4.0_DS_ClientPlatform). Spec-of-record for PRD S6 row D2.
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/DATA_PLATFORM.D2.black-diamond-arch-spec.md`
**Consult:** 0.7.0_AE_CloudOps (auth/session/IP-binding/infra). **Verify:** 3.0.0_SA_CVO (reconcile spec vs live BD / cot pipeline).
**Seeds:** `data/cot/scripts/bronze/cot_bronze_ingest.py`, `data/cot/scripts/bronze/templates/{table}.json`, `docs/architecture/COTETL_METHODOLOGY_THESIS.md`.
**Grounding:** local persisted template bodies (4/5 enriched, holdings is a thin envelope) + the live DataMining REST flow as implemented in `cot_bronze_ingest.py`. The FULL holdings (qt1) dimension/measure catalog is **PENDING the live-enriched dump** (see §7) -- the one section that requires the IP-bound on-box read.

> SPEC ONLY -- no build. This documents how Black Diamond aggregates + surfaces custodian data: the model we would have to replicate or replace to own the aggregation layer ourselves.

---

## 1. Objective

Black Diamond (BD) Wealth Solutions is a portfolio-accounting + performance-reporting aggregator. It ingests custodian feeds (Schwab, Fidelity, etc.), reconciles them into a firm-scoped book of record (accounts x holdings x tax-lots x transactions), and exposes that book through a **DataMining** query API. D2 specs that DataMining model -- the template/level/fact query shape, the auth/session model, the full per-table catalog, and BD's lot-vs-snapshot accounting methodology -- so we can reason about replicating or replacing the aggregation layer.

## 2. The DataMining REST flow (as implemented)

BD DataMining is a **persisted-query + async-execution + export-download** API. The proven flow (`cot_bronze_ingest.py`, reverse-engineered from a HAR capture, Brief 1):

```
GET  /datamining/auth/token                      (Cookie: .bd.identity jar) -> {access_token}   # opaque Bearer, short-lived
POST /datamining/request/v1/run    {template,asOfDate}  (Bearer)            -> {templateId(runId), resultGuid}
GET  /datamining/request/v1/run/{runId}/status   (Bearer)                   -> {statusMessage, isComplete}   # poll
GET  /Api/DataMining/ExportResults/{resultGuid}  (Cookie)                   -> xlsx bytes
```

Two-credential split is load-bearing: **catalog/template ops + run-execution authorize via the Bearer**; **the binary export download authorizes via the Cookie jar**. A run does not stream rows -- it materializes a server-side result identified by `resultGuid`, which the export endpoint then serves as an xlsx (`Sheet1` = data, `Timestamps` = the as-of/start/end metadata sheet, the canonical data-date source).

Status polling must detect the **error-while-incomplete** state: BD sets `statusMessage='Error'` with `isComplete=False` on a failed run, so polling `isComplete` alone hangs the full timeout. (Implemented: bail on `statusMessage in {error,failed,faulted}`.)

## 3. Auth / session / IP-binding model (AC2)

- **Root credential = the `.bd.identity` OIDC session cookie jar.** BD uses an IdentityServer (idsrv) OIDC session. `cot_bd_session_fetch.py` (0.6.2_AE) performs the interactive login on the IP-bound box and writes the full jar (`bd_identity` + `all_cookies[]` incl `.AspNetCore.Antiforgery`, `idsrv.session`, etc.) to **Secrets Manager `blackdiamond/cot/session`** as `{bd_identity, all_cookies[], captured_at, expires_at}`.
- **The FULL jar is required for `v1/run` (POST execution)** -- `.bd.identity` alone suffices for catalog/template GETs, but run-execution needs the antiforgery + idsrv session cookies. (`load_bd_session` prefers `all_cookies[]`, falls back to `bd_identity` alone.)
- **The Bearer is minted per-run** from the cookie via `GET /datamining/auth/token`; it is opaque and short-lived (mint fresh each run, do not cache off-box).
- **IP-binding (the hard infra constraint):** the BD session is bound to the **cot-exporter EC2 source IP** (`i-0643a5bee8a8feabf`). Off-box replay of the jar fails -- so every live BD read (bronze pull, the D2 enriched-template dump, any probe) MUST run on-box via SSM. This is why the exporter EC2 exists and why D2's enriched-dump is an AE-on-box step.
- **Session TTL is SHORT (~30-60 min effective)** -- the `cf_bm` bot-management cookie (~30 min) + idsrv idle gates the practical window, NOT the longer nominal `expires_at`. Do not assume a stated multi-hour TTL; a fresh session-fetch precedes any live-read campaign. (Banked: `reference_bd_session_real_ttl_short_dont_replay_offbox`.)
- **Firm isolation:** the session secret, bucket, and firm-id are per-partner (Model B): `blackdiamond/cot/session`, `opal-data-cot`, `cottonwood`. The bronze runner fails closed (`_assert_firm_separation`) if a non-cot firm-id is set without its own bucket, so a mis-set run aborts rather than cross-writing.

## 4. The template / level / fact model (AC1)

DataMining queries are **persisted star-schema selections**. A query = one `queryTypeId` (the table family) + an ordered set of **levels** (the dimension hierarchy) + **facts** (measure groups), persisted server-side under a `templateId`.

### 4.1 Thin envelope vs persisted body -- the key architectural fact

The repo `templates/{table}.json` are **THIN ENVELOPES** for the persisted templates: they carry only `{templateId, queryTypeId, dateRangeType, startDate, endDate, name, comment}`. The **full dimension/level/fact selection lives SERVER-SIDE under the templateId** and materializes only via `GET /datamining/request/v1/template/{id}` at runtime. `run_query` GETs the enriched body, re-stamps dates + `dateRangeType`, normalizes the run-body shape (adds 5 required-null fields, drops 3 rejected fields, adds top-level `asOfDate`), then POSTs `v1/run`.

- holdings (qt1, id 226355) is **envelope-only locally** (547 bytes, 0 levels) -- its full selection is the canonical example of server-side persistence; the D2 catalog for qt1 requires the live dump (§7).
- realized/unrealized (qt3/qt4) carry FULL enriched bodies locally (~120 KB, 8 levels, ~208 dims) -- captured at provision time.
- Per-call overrides are date-window only (`startDate`/`endDate` MM/DD/YYYY for `Custom`); the dimension/fact contract is fixed at the persisted template so the data shape stays the canonical contract (refine a query by re-persisting the template, not by code change).

### 4.2 The level hierarchy (the star)

Across tables BD exposes a consistent organizational spine, top-to-leaf:

```
Team -> Relationship -> [Portfolio Group] -> Portfolio -> Account -> Holding -> Tax Lot
```

Not every table selects every level; each table picks the levels its grain needs. The leaf level sets the row grain (Account x Holding for snapshots; Tax Lot for realized/unrealized gain detail; Transaction for the txn ledger).

### 4.3 Per-table catalog (the 5 cot tables)

Grounded in the local persisted bodies (holdings PENDING the live dump). Counts are dims = total selected dimensions across levels; measures = total across facts.

| Table | qt | templateId | dateRangeType | Levels | Dims | Measures | Leaf grain | Key measures |
|---|---|---|---|---|---|---|---|---|
| holdings | 1 | 226355 | Custom | **(server-side -- PENDING §7)** | -- | -- | Account x Holding (position snapshot) | Market Value, Units (Ending MV via `activityOptionId=1`) |
| transactions | 2 | 226274 | Custom | 5 (Transactions, Relationship, Portfolio, Account, Holding) | 63 | 5 | Transaction | Units, Market Value, Transaction Fee, Income, Account Fee |
| realized | 3 | (re-provision) | Custom | 8 (Tax Lot, Team, Relationship, Portfolio Group, Portfolio, Account, ...) | 209 | 7 | Tax Lot (closed) | Units, Cost Basis, Proceeds, Short-Term G/L, Long-Term G/L, Total Gain Loss |
| unrealized | 4 | (re-provision) | Custom | 8 (Tax Lot, Team, Relationship, Portfolio Group, Portfolio, Account, ...) | 208 | 11 | Tax Lot (open) | Units, Cost Basis, Amortization, Market Value, Short-Term G/L, Long-Term G/L |
| allocations | 5 | 226334 | Custom | 4 (Team, Relationship, Portfolio, Account) + parent/child allocation levels | 62 | 1 | Account (allocation rollup) | Market Value |

Notes:
- **qt5 allocations is the parent/child ALLOCATION query** (`childQueryAllocationLevelId`, `allocationMarketValueFactId`, `allocationCashInclusionId`) -- a Relationship/Account MV rollup. Known gotcha (banked): the Relationship MV double-counts rep-split rows (~2x); silver/gold MUST dedup before any relationship rollup.
- **Tax Lot dims** on qt3/qt4 are the cost-basis spine: `Open Date`, `Trade Date`, `Unit Cost`, `Inherited Date`, `Is Wash Sale` -- i.e. BD holds lot-grained acquisition + wash-sale state, not just net positions (see §5).
- **Date mode:** all 5 are `Custom` (absolute window), per ADVI_COTETL.AUAFIX-DATEMODE-B. For the snapshot tables (holdings/alloc/unrealized) BD returns the END-date snapshot regardless of window width, so the 14-day window is a holiday-gap FLOOR (span >=1 complete business day), not a restatement lookback; for transactions/realized the window is BD's ~14d restatement lookback.

## 5. Lots FIFO-vs-snapshot methodology (AC3)

BD exposes BOTH accounting views, and the cot methodology choice is the central architectural decision:

- **Snapshot view (qt1 holdings / Assets_Dim):** BD delivers the canonical position value per account per holding per day directly -- `Market Value` + `Units` with `activityOptionId=1` (Ending MV). This IS the book-of-record value; no reconstruction needed.
- **Lot-level cost-basis view (qt3 realized / qt4 unrealized):** BD maintains tax-lot-grained accounting -- each open/closed lot carries `Open Date`, `Unit Cost`, `Inherited Date`, `Is Wash Sale`, and BD computes `Cost Basis`, `Proceeds`, `Short-/Long-Term Gain-Loss` at the lot. BD's own realized G/L is therefore **lot-grained** (the custodian/BD lot-relief method -- FIFO/avg/spec-ID per account config -- resolved inside BD; we consume the resolved lot rows, we do not re-run the relief).

**The cot (COTETL) methodology = SNAPSHOT-FIRST** (`COTETL_METHODOLOGY_THESIS.md`): read daily value straight from the qt1 snapshot (`canonical_holdings` -> C_03 account_performance / D_00 clients), NOT by reverse-engineering value from the transaction/lots-FIFO chain. Contrast:

| | 49 Financial | Cottonwood (cot) |
|---|---|---|
| Value source | Transaction reverse-engineering: reconstruct holdings via the lots-FIFO chain (`holdings_lots -> canonical_lots -> account_gains -> performance`) to recover PRE-snapshot history | The SNAPSHOT -- qt1 delivers canonical per-account-per-day value directly |
| Lots-FIFO chain | Full (necessary for pre-snapshot value) | **Empty by design** (a snapshot has no lot open/close lineage) -- correct, not a defect |

Wiring cot through 49F's lots-FIFO value path is the anti-pattern that froze served-AUA at 06-09 (the served path read the dead lots chain instead of the live snapshot; the 2026-06-22 fix re-wired C_03/C_01 to the snapshot). Lot-derived fields (realized/unrealized FIFO G/L, lot-based returns) are **deliberately scoped** for cot: in-scope only if snapshot-derivable; otherwise explicit out-of-scope, never fabricated.

**Forward direction (Andrew-flagged):** use the BD `Assets_Dim` (qt1) tables as the daily-value mechanism directly -- the leanest snapshot path -- and, once proven on cot, retrofit 49F to snapshot-native daily value going forward (keeping reverse-engineering only for 49F pre-snapshot history).

## 6. What we'd replicate/replace to own the aggregation layer

BD's value-add (the layer we'd have to own) is, in order of supplant difficulty:
1. **Custodian feed ingestion + reconciliation** (Schwab/Fidelity raw -> reconciled positions) -- the hardest; multi-custodian normalization + break resolution. (Cross-ref D3 Orion/Eclipse, DC-REV reverse-ETL map.)
2. **Tax-lot accounting** (lot relief, wash-sale, cost-basis tracking across corporate actions) -- BD's lot engine; replicable but non-trivial (we already have a lots-FIFO chain for 49F).
3. **The dimensional book-of-record** (Team/Relationship/Portfolio/Account/Holding/TaxLot star) -- a modeling task; our silver/gold already materializes a comparable star.
4. **The query/export surface** (DataMining) -- the thinnest layer; a persisted-query API over the star.

The snapshot-first thesis implies we do NOT need to replicate (2) to own daily VALUE -- only to own gains/tax detail. Owning (1) is the strategic question DC-REV/D3 scope.

## 7. PENDING (the one live-read item) + verification

- **Live-enriched template dump (completes the §4.3 catalog for holdings qt1 + confirms all 5):** run `data/cot/scripts/bronze/dump_enriched_templates.py` ON-BOX (cot-exporter, IP-bound + a FRESH BD session) -> writes `s3://opal-data-cot/code/bronze/templates_enriched/{table}.json` + a per-table `levels/dims/measures` summary. Read-only (GET /template/{id} + one put_object/table; no run/land). **Owner DS, run-by 0.7.0_AE on-box** (the script exists + is gate-clean; not yet run -- `templates_enriched/` is empty as of 2026-06-26). On completion, fill the qt1 row of §4.3 from the dumped body.
- **CVO reconcile (AC4):** 3.0.0_SA_CVO verifies this spec against live BD (the enriched dump) + the cot pipeline (silver/gold column == `to_snake_case(BD display-name)`; the snapshot-first wiring; the qt5 dedup). The enriched dump IS the reconcile-to-live ground.
- **RAVC2 COO + CTO** (AC5) on this draft; finalize to v1.0 after the live dump + CVO reconcile.

## 8. Open items / cross-references

- D3 (Orion/Eclipse arch spec) + DC-REV (reverse-ETL map) cover the OTHER custodian/aggregator surfaces; D2 is BD-specific.
- The qt5 relationship-MV ~2x double-count (rep-split) is a known dedup requirement, not a BD defect to replicate.
- Advisor/rep dimensions are pruned from the cot templates (ADVI_COTETL Outcome B, no usable advisor segmentation v1) -- a cot scope choice, not a BD model limit.
