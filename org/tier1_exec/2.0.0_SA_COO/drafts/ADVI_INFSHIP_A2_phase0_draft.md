# ADVI_INFSHIP_A2 — Orion Asset API Vendor Investigation

**Status:** DRAFT — 2026-04-30 (Phase 0; pending CTO review + Andrew GO)
**Authors:** 2.0.0_SA_COO + 1.0.0_SA_CTO (joint)
**Macro project:** ADVI (Advisor Intelligence)
**Parent project:** ADVI_INFSHIP (Inflection Portal Ship Wave)
**Audience:** 0.6.1_AE_PartnerETL~B (Phase 1 owner if Andrew GOes vendor outreach), 0.4.0_DS_ClientPlatform (Phase 0a data-layer consult), 1.0.0_SA_CTO (architectural sponsor + vendor outreach lead)

---

## 1. Why this PRD exists

### 1.1 The current state — Path C

INFSHIP Phase 1.L4 (per-asset ticker classifier) ships through **Path C**: a chain-rerun-coupled pipeline reading `canonical/holdings.parquet`, applying an `advisor_key` allowlist filter (INFLECTION_REP_IDS = {3, 11, 12} pre-Brandenburg; expanded to {3, 6, 11, 12} post-DIAGFIX.011), and emitting `platinum/firm/composition.json` plus per-advisor downstream artifacts. Net Inflection-only AUA: ~$197.69M (post-DIAGFIX.011, intra-day delta to Andrew's $198.87M target).

Path C is functional for v1 and shipped INFSHIP Phase 2 portal panels in production. But it has structural costs that compound over time:

1. **Chain-rerun cadence dependency.** Path C inherits the entire Orion gold-chain rerun cadence (~daily, ~30-90 min runtime depending on EC2 instance size and chain configuration). Every refresh requires the full B-chain → C-chain → I-chain → D-chain sequence to settle. Faster refresh requires either runner upgrade (already at c6a.4xlarge per `inf-pipeline-v1.6.6`) or chain decomposition (architecturally invasive). DIAGFIX.012's positions_mv refactor (in flight as of this PRD authoring) reduces but does not eliminate this dependency for the holdings layer.

2. **Multi-firm contamination at source.** The Orion export under the Inflection user account has read access to multiple firms (Inflection + Keil Financial Partners + others — surfaced by ADVI_INFGRD 2026-04-27). Path C handles this with a post-export allowlist filter at the silver layer (INFLECTION_REP_IDS gate); it does not eliminate the contamination, it filters it out. Defense-in-depth is good, but the architectural ideal is filter-at-source.

3. **Schema drift exposure.** Path C is structurally coupled to the canonical chain's column conventions — every silver-layer schema migration ripples into the chain. Compare with a direct API pull where the silver-layer adapter handles vendor-side schema changes in isolation. ADVI_INFGRD's FLAG 2 (C_07 rep_name → rep_id) and FLAG 3 (D_00c name lookup) are examples of chain-coupled schema breaks that wouldn't manifest under a Path A model.

4. **Synchronous Generate endpoint timeouts.** DS~D's prior attempts to pull Asset-grouping data via Orion's Custom Reports / Envision Generate POST endpoint timed out 4x. Path C was the explicit fallback. Whether the timeouts are vendor-side or transport-side has not been definitively determined — that's part of A2's investigation surface.

### 1.2 The architectural thesis — Path A

**Path A** is the proposed direction: a direct programmatic pull from Orion's `api.cloud.orionadvisor.com` endpoints (which Orion's web UI calls internally), replacing Path C's chain-rerun-coupled-then-filtered model with a per-dim direct-fetch-then-adapt model. Path A would:

- Decouple per-dim refresh cadence from chain runtime (positions could refresh hourly while NMEC/NMNC/NNA stay daily, etc.)
- Filter at vendor source via per-firm rep_id parameterization (Brandenburg attribution work in DIAGFIX.011 already proved per-rep API endpoints exist and respect rep_id scoping)
- Insulate gold/platinum from vendor schema changes via a thin silver-layer adapter
- Eliminate the Custom Reports / Envision Generate POST timeout pathway entirely

**Path A is not currently authorized.** This PRD's Phase 0 surface is to define the investigation that determines whether Path A is feasible, partially feasible, or vendor-blocked.

### 1.3 Why Phase 0 exists separately from execution

CTO + COO 2026-04-30 ruling: investigative work upfront prevents architectural commitment to a direction Orion may not support. Three reasons:

1. **Orion has no documented public API.** We are reverse-engineering the internal API used by their web UI. Vendor ToS posture on programmatic consumption of internal endpoints is uncertain (CTO has parallel workstream pinging Orion contact; pending Andrew Orion contact info).

2. **DIAGFIX.012 is in flight (DS BASE, today/tomorrow).** Its positions_mv refactor will replace INF_B_00's TRN-as-price reconstruction with a direct API pull from `/Portfolio/Clients/{cid}/Assets/{date}` (DIAGFIX.009-NEW Phase 1 VERDICT A). Path A's hypothesis-set therefore has a moving target — whatever DIAGFIX.012 ships becomes part of the Path A baseline. Investigating Path A before DIAGFIX.012 settles risks re-architecting around an artifact about to be replaced.

3. **AE 0.6.1~B has bandwidth conflict.** The natural Phase 1 owner (AE 0.6.1~B; same lane as ADVI_ORIAPI Phases 0+1+3+4) is currently watching the ORIAPI Cycle 1 + Cycle 2 closure gate (today + tomorrow). Splitting their context across vendor outreach + cycle monitoring creates RAVC delivery risk.

Phase 0 is therefore COO + CTO scope, no AE labor, scoped to surface definition and success criteria — not vendor outreach. Phase 0a (DS BASE consult post-DIAGFIX.012) is the gate to Phase 1 (vendor outreach + empirical probe). Phase 1+ is conditional on Andrew explicit GO post-0a.

---

## 2. Investigation surface

### 2.1 Endpoint catalog (what we know exists)

From session 47-48 path discovery work + DIAGFIX wave findings:

| Endpoint | Verb | Discovered by | What it returns | Currently used in chain? |
|---|---|---|---|---|
| `/Portfolio/Clients/{cid}/Assets/{date}` | GET | DIAGFIX.009-NEW Phase 1 (DS, `91da4d6a1`) | Per-account holdings/assets snapshot at `{date}`. VERDICT A confirmed: accepts arbitrary historical dates. | YES — `silver/api_dims/assets_v2` (DIAGFIX.010 Phase 1+2 `2979c12a7`); will be expanded by DIAGFIX.012 to `positions_mv` |
| `/Portfolio/Representatives` | GET | DIAGFIX.011 Phase 1 (DS, `72628a1df`) | All representatives (advisors) including the firm placeholder rep_id=3 + named advisors {6, 11, 12} | YES — `silver/api_dims/representatives` |
| `/Portfolio/Clients?representativeId={rid}` | GET | DIAGFIX.011 Phase 2 (DS, `72628a1df`) | Households assigned to a specific rep | YES — `silver/api_dims/household_rep_mapping` |
| `/Performance/...` (TWR, Sharpe, Sortino, Drawdown) | GET | DS~B path discovery (`e824e0fd`) | Per-account performance metrics | NO — referenced in INFSHIP capability shifts; programmatically pullable |
| `/Tax/{Term}.{Field}` (3-level naming) | GET | DS~B reverse-engineering (`e1126f16`) | Per-account tax/cost-basis (22% Inflection coverage observed) | NO — referenced as net-new artifact opportunity; pending pull |
| `/Billing/...` (fee subset) | POST | INFLEC_PARITY_FILL_CANDIDATES.md P1 priority | Per-account fee/billing subset | NO — net-new artifact opportunity |
| `/api/v1/Reporting/Scope` | POST | HAR 7 (DIAGFIX.011 work) | Flexible calc engine; richer than current Assets endpoint | NO — logged as future Books-tab follow-on |
| Custom Reports / Envision Generate | POST | DS~D prior attempts (timed out 4x) | Asset-grouping per-(account,asset) | NO — Path C fallback explicitly chosen because of timeouts |

**Net:** 4 of 8 endpoints in this catalog are programmatically pulled today; 3 are confirmed-pullable but not yet integrated; 1 (Custom Reports / Envision Generate) is performance-blocked. Path A's central question is whether the 3 unpulled-but-confirmed endpoints + the 1 timeout-blocked endpoint can be made the single source of truth for the gold-chain inputs they overlap.

*This catalog is empirically discovered (HAR analysis + reverse-engineering of the Orion web UI's internal calls). Phase 0a DS consult and Phase 1 probe may extend it; the table is not closed. Possibly missing endpoints out of scope for v1 INFLEC: `/Sleeves/...` (SMA-relevant), `/Households/...` (overlaps with `/Portfolio/Clients?representativeId=`).*

### 2.2 What each endpoint hypothetically replaces

If Path A reaches full migration:

| Path C artifact | Path A endpoint | Replaces |
|---|---|---|
| `silver/holdings/{date}.parquet` | `/Portfolio/Clients/{cid}/Assets/{date}` (per cid in scope) | INF_B_00 input; canonical holdings.parquet upstream; Path C's TRN-as-price reconstruction (already targeted by DIAGFIX.012) |
| `silver/dimensions/accounts_dimension.parquet` | `/Portfolio/Representatives` + `/Portfolio/Clients?representativeId={rid}` joined | Already partially migrated via DIAGFIX.011's accounts_v2 augmentation |
| `silver/canonical_performance/*` | `/Performance/...` per-account | Currently chain-derived; Path A would direct-pull |
| `silver/canonical/holdings_lots/*` | (TBD — depends on whether `/Portfolio/Clients/{cid}/Assets/{date}` exposes lot-level granularity OR requires `/Tax/{Term}/CostBasis/...`) | INF_C_01 / INF_C_07 inputs |
| (none — net-new) | `/Tax/{Term}.{Field}` | Net-new TaxAlphaPanel data (deferred per INFSHIP) |
| (none — net-new) | `/Billing/...` | INFLEC_PARITY_FILL_CANDIDATES P1 enrichment |

**Hypothesis-set:** every silver-layer artifact currently sourced from chain-rerun could in principle be sourced from a direct API pull. The investigation surface determines which actually can vs which face vendor-side blockers (rate limits, schema drift, authentication coupling, ToS posture).

### 2.3 What we don't know (Phase 0 questions)

1. **Sustained-pull rate limits.** Empirical probe needed: how many `/Portfolio/Clients/{cid}/Assets/{date}` calls per minute can we sustain across all 295 Inflection households × N historical dates without triggering 429 / 5xx / token revocation?
2. **Historical-bound depth.** DIAGFIX.009-NEW Phase 1 confirmed arbitrary dates work in principle; but is there a hard cutoff (5 years? 10? "since the firm joined Orion"?)? Affects Path A's backfill capability.
3. **Per-dim authentication coupling.** Are `/Performance/...` and `/Tax/...` gated by the same JWT as `/Portfolio/Clients/...` or do they require separate tokens / scopes? Affects Lambda + JWT pipeline complexity.
4. **Vendor-confirmed support posture.** Does Orion's Account Manager or technical contact say "yes, programmatic consumption of these endpoints is fine for our customers" OR "no, these are internal and ToS-prohibited" OR "case-by-case"? Determines architectural commitment.
5. **Custom Reports / Envision Generate timeout root cause.** Was the 4x timeout a vendor-side compute limit (synchronous calc engine maxing out on Inflection's data shape), an HTTPS transport timeout (60s gateway limit), or a path-construction error (DS~D didn't fully reverse-engineer the POST body)? Affects whether we should retry that endpoint or treat it as architecturally blocked.

---

## 3. Success criteria

### 3.1 Phase 0 success criteria (this PRD's deliverable)

- [ ] PRD authored at `docs/architecture/ADVI_INFSHIP_A2.md` covering §1-§7 of this draft (CTO commits canonical post-review)
- [ ] CTO + COO sign-off on investigation surface scope (no Andrew GO needed for Phase 0 itself)
- [ ] Phase 0a placeholder defined with explicit DS BASE consult agenda (Phase 0a executes post-DIAGFIX.012 ship)
- [ ] Phase 1 gate criteria explicit: Andrew explicit GO + vendor contact info + AE 0.6.1~B bandwidth (post-ORIAPI Cycle 2 close)

### 3.2 Phase 0a success criteria (DS BASE consult, post-DIAGFIX.012)

- [ ] DS BASE confirms: which Path C artifacts remain load-bearing AFTER DIAGFIX.012's INF_B_00 refactor lands? (e.g., does `canonical/holdings_lots/*` still need chain-rerun or does positions_mv subsume the lot-level need?)
- [ ] DS BASE confirms: any caveats to `/Portfolio/Clients/{cid}/Assets/{date}` durability under sustained pull (Phase 2.5 of DIAGFIX.012 will produce this finding) — feeds directly into Phase 1 rate-limit probe scope
- [ ] DS BASE flags any net-new artifacts or analytical surfaces that would benefit from Path A direct-pull (per-account Performance, Tax, Billing — confirm priority order for Phase 1 probe)

### 3.3 Phase 1 success criteria (vendor outreach + empirical probe; conditional on Andrew GO)

- [ ] CTO has vendor-confirmed posture: supported / case-by-case / blocked
- [ ] AE 0.6.1~B empirical probe data: rate limits per endpoint, historical bounds, error codes under load, JWT scope per endpoint
- [ ] Decision matrix: which endpoints migrate Path C → Path A in Phase 2, which stay Path C, which require alternative architectures (Path B custom puller, Path D vendor-collab)

### 3.4 Definitive vendor-confirmed answers vs partial signals

The investigation can yield three result classes per endpoint:

| Class | Definition | Architectural implication |
|---|---|---|
| **Definitive supported** | Vendor confirms (in writing) + empirical probe sustains target load + 14-day stability observation | Path A migration authorized for that endpoint |
| **Partial / case-by-case** | Vendor neutral or silent + empirical probe successful but unstable OR vendor-supported but rate-constrained | Architectural fallback: Path A primary with Path C resume; or Path A scoped to specific use cases (e.g., on-demand only, not nightly) |
| **Vendor-blocked or empirically failed** | Vendor explicitly prohibits OR empirical probe fails (sustained 429s / token revocation / 5xx / data corruption) | Path C remains; Path B (custom EC2 puller) considered for high-priority dims only; document the block as architectural future-state |

Phase 0 does not pre-commit to any class per endpoint — that's Phase 1+ work.

---

## 4. Risk classes

### 4.1 Vendor SLA risk

Orion has no published API SLA for programmatic consumers (because there is no public API). Risks:

- Internal endpoint URLs change without notice (web UI refactor on vendor side)
- Authentication mechanism changes (JWT issuer rotation, scope changes, MFA requirements)
- Data schema changes (column additions / removals, dtype changes, naming shifts)
- ToS interpretation changes — Orion could decide post-deployment that programmatic consumption violates their Acceptable Use Policy

**Mitigation:** thin silver-layer adapter pattern + monitor for schema drift via comp-build edge integrity + maintain Path C as fallback. CTO's parallel vendor outreach reduces but does not eliminate this risk.

### 4.2 Rate limit risk

Empirical only — no documented limits. Past observed:
- DS~D's Custom Reports / Envision Generate POST timed out 4x (could be rate-related or compute-related; unconfirmed)
- DIAGFIX.011's bronze pull of `/Portfolio/Representatives` + per-rep `/Portfolio/Clients?representativeId={rid}` succeeded for 7 reps without observed throttling — but that's 7 calls, not 295 cids × N dates

**Mitigation:** Phase 1 empirical probe must include sustained-load testing at target Path A volume (estimate: 295 households × 2 years daily = ~215K calls for full backfill). Probe in ramps: 100 calls/min, 500 calls/min, etc., with 14-day observation between ramps to catch rate-limit reactions that aren't immediate.

### 4.3 Schema drift risk

Empirical observation: DS~B's reverse-engineering of `/Tax/{Term}.{Field}` 3-level naming yielded 22% Inflection coverage — meaning 78% of accounts had no Tax data populated. This is either:
- Genuine data sparseness (some accounts simply don't have tax data; vendor returns empty)
- Schema mismatch (we're querying a field path that doesn't apply to all accounts)
- Authentication scope (JWT doesn't have permission for some account classes)

Pre-Phase 1, we don't know which.

**Mitigation:** Phase 1 probe must test sparse-data hypothesis (try alternate path constructions; compare returned data against Inflection's known account count). Phase 0a DS BASE consult should surface known data-shape edge cases.

### 4.4 Reciprocal data restrictions / ToS risk

**Highest-uncertainty risk class.** Vendor ToS may include clauses restricting:
- Programmatic consumption of internal endpoints
- Bulk data extraction (rate-shaped)
- Caching / persistence of API responses (impacts our silver/canonical layers)
- Sharing data with portal end-users (affects Inflection user view of their own firm data — though this seems a reach)

Path A architectural commitment without a definitive vendor posture would be a major risk.

**Mitigation:** CTO's parallel vendor outreach is the primary control. Phase 1 vendor contact result classifies this risk; Andrew's explicit GO post-0a authorizes (or blocks) progression.

**Pre-committed abandonment criterion:** if vendor outreach yields explicit ToS prohibition, immediately abandon Path A architectural commitment + document as future-state with **Path D (vendor-collab partnership)** as primary alternative; **Path B (custom EC2 puller)** considered only for high-priority dims with Andrew strategic GO. Pre-committed abandonment makes the risk class actionable rather than narrative — no architectural ambiguity post-prohibition.

### 4.5 Performance risk

Custom Reports / Envision Generate POST timeouts are the only confirmed performance-blocked endpoint. Other endpoints (`/Portfolio/Clients/{cid}/Assets/{date}`, `/Portfolio/Representatives`, etc.) have not been stress-tested under Path A volume.

**Mitigation:** Phase 1 includes parallelization architecture review — if endpoint is rate-limited per-cid but not per-account, we parallelize on cid; if rate-limited per-IP, we may need rotating IPs (significant infra implication). Default assumption: serial within reasonable parallel concurrency (20-50 concurrent requests).

### 4.6 Operational complexity risk

Path A introduces:
- New Lambda ETL layer per dim (vs single canonical chain consumer)
- New silver-layer adapters per endpoint
- New CW alarms + retry logic per endpoint (vendor-specific error codes)
- New JWT scope management (multi-endpoint may require multi-scope tokens)

Architectural complexity may not be worth the cost if Path C is already delivering and the marginal benefit is "faster refresh cadence" alone. Phase 0a should include explicit cost-benefit analysis: what specifically does Path A unlock that Path C cannot? (Likely answer: per-dim independent refresh + multi-firm filter-at-source + future net-new artifacts; but these need explicit ranking.)

---

## 5. Phase 0a placeholder — DS BASE consult (post-DIAGFIX.012 ship)

**Trigger:** DIAGFIX.012 Phase 5 RAVC4 closure (DS BASE, expected 2026-05-01).
**Owner:** 2.0.0_SA_COO + 1.0.0_SA_CTO drive the consult; 0.4.0_DS_ClientPlatform provides data-layer ground truth.
**Estimated effort:** ~30-45 min DS time + ~30 min COO/CTO synthesis.

### 5.1 Consult agenda

Three structured questions for DS BASE post-DIAGFIX.012:

1. **Path C residual load-bearing surface.** After DIAGFIX.012's INF_B_00 refactor lands, which Path C silver-layer artifacts are still load-bearing for the gold chain? Specifically:
   - Does `canonical/holdings_lots/*` still require chain-rerun or does `positions_mv` subsume the lot-level need?
   - Are `silver/canonical_performance/*` and `silver/canonical_nna/*` still fed exclusively from chain-derived sources, or do they have direct-pull alternatives we haven't activated?
   - What's the maximum subset of Path C artifacts we could replace with Path A pulls if Phase 1 vendor confirms?

2. **`/Portfolio/Clients/{cid}/Assets/{date}` durability findings.** DIAGFIX.012 Phase 2.5 produces an explicit durability report (rate-limits, historical-bound, vendor-flakiness). DS BASE summarizes findings + answers:
   - Is the endpoint stable enough for Phase 1 sustained-load testing?
   - Any caveats (specific date ranges that fail, specific cids that 5xx, response format inconsistencies)?
   - DS BASE's recommendation: full Path A migration / partial / Path C-with-Path-A-supplement?

3. **Net-new artifact priorities.** INFLEC_PARITY_FILL_CANDIDATES.md ranked 7 P1-P7 priorities for new artifacts. Post-DIAGFIX.012, which of these are most aligned with Path A direct-pull architecture vs which would need new chain extensions? DS BASE's P1 ranking informs Phase 1 probe sequencing.

### 5.2 Deliverable

Phase 0a session log at `org/tier1_exec/2.0.0_SA_COO/logs/{YYYY-MM-DD}/inflship_a2_phase0a_ds_consult.md` summarizing:
- DS BASE answers to the 3 agenda questions
- Updated Phase 1 probe scope
- Decision: Phase 1 GO recommendation to Andrew (proceed with vendor outreach + empirical probe / hold / scope-narrow)

### 5.3 Phase 0a is NOT vendor outreach

Phase 0a stays internal — no Orion contact, no probe traffic. Pure data-layer reality check + Phase 1 scoping. Vendor outreach + probe waits for Andrew's GO.

---

## 6. Phase 1 gate

Phase 1 (vendor outreach + empirical probe) requires ALL of the following:

1. **Andrew explicit GO** post-Phase 0a session log review.
2. **Andrew Orion contact info** (Account Manager / technical liaison email + phone). CTO has been requesting since 2026-04-27; pending Andrew action.
3. **AE 0.6.1~B bandwidth** post-ORIAPI Cycle 2 close (2026-05-01). Owner of the empirical probe Lambda + harness.
4. **CTO architectural sign-off** on probe design (rate-shaping, parallelization concurrency, JWT scope handling, observability + rollback path).
5. **Phase 0a session log** with DS BASE consult findings + scope-narrow recommendation.
6. **Phase 1 effort estimate:** ~3-5 days AE 0.6.1~B build (multi-endpoint probe Lambda + rate-shaping + JWT-scope handling + observability + rollback path) + ~14 days soak/ramp observation (sustained-load testing at incremental concurrency tiers; 14d covers vendor weekly cadence + month-boundary effects). **Total wall-clock ~3 weeks for Phase 1 closure.** This sizing matters for Andrew's GO calculus: vendor outreach + 3-week probe is a different commitment than a same-day investigation.

Phase 0 does not pre-author Phase 1 task orders. Those are authored by COO post-Andrew GO.

---

## 7. Phase 2/3 conditional stubs

These sections are intentionally light. They depend entirely on Phase 1 outcome.

### 7.1 Phase 2 (conditional on Phase 1 results)

**Phase 2 migration order inherits `INFLEC_PARITY_FILL_CANDIDATES.md` P1-P7 ranking** — single source of truth for priority. The illustrative listing below (positions > performance > tax > billing) is a placeholder only; actual ordering may be reordered post-Phase 0a per DS BASE recommendation + Phase 1 empirical probe results per endpoint.

**If vendor confirms supported + empirical probe passes for the priority dims:**
- Phase 2.1 — Path A migration of `/Portfolio/Clients/{cid}/Assets/{date}` (already partial via DIAGFIX.012; finalize)
- Phase 2.2 — Path A migration of `/Performance/...` per-account (PerformancePanel data)
- Phase 2.3 — Path A migration of `/Tax/{Term}.{Field}` (TaxAlphaPanel data; conditional on coverage > target threshold)
- Phase 2.4 — Path A migration of `/Billing/...` (FeeEfficiencyPanel data — currently P1 in INFLEC_PARITY_FILL_CANDIDATES; may move to Phase 2.1 if probe rank-orders it as highest-impact)

**If vendor partial / case-by-case:**
- Phase 2.* — case-specific architectures per endpoint; document which stay Path C

**If vendor-blocked or empirical probe fails:**
- Phase 2.0 — document Path A as architectural future-state in `docs/architecture/`
- Phase 2.X — Path B (custom EC2 puller) consideration for highest-priority dims only (per Andrew strategic call)

### 7.2 Phase 3 (long-tail)

- New per-dim refresh cadence governance (cron schedules, idempotency, alarm thresholds)
- Multi-firm filter-at-source architecture (deprecate INFLECTION_REP_IDS allowlist filter at silver in favor of per-firm rep_id parameterization)
- Schema drift monitoring (comp-build edge integrity checks per Path A endpoint)
- Cost analysis (Path A Lambda + bandwidth costs vs Path C chain runtime cost)

These are placeholder stubs only. Specific scope authored post-Phase 1 closure.

---

## 8. Cross-references

- Parent PRD: `docs/architecture/ADVI_INFSHIP.md` (synthesis project)
- Phase 1.L4 Path C deferral context: `docs/architecture/ADVI_INFSHIP.md` §1.L4
- DIAGFIX.009-NEW Phase 1 VERDICT A: commit `91da4d6a1` + DS session log `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-29/advi_inflec_diagfix_009_new_phase1_pricing_probe.md`
- DIAGFIX.012 (in flight): TO at `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_INFLEC.DIAGFIX.012.ds-orion-daily-positions-mv-refactor.md`
- Path discovery work: `e824e0fd` (Performance.*), `e1126f16` (Tax 3-level naming)
- INFLEC_PARITY_FILL_CANDIDATES.md (P1-P7 priorities)
- INFLEC_BOOKSTAB_TAX_FIELD_MAP.md (Tax coverage data)
- Parent INFSHIP TO: `org/tier2_senior/0.6.1_AE_PartnerETL/task_orders/ADVI_INFSHIP.A2.ae-orion-asset-api-vendor-investigation.md` (AE 0.6.1~B owner; status pending vendor contact)
- ADVI_ORIAPI infrastructure (parallel): `inf-pipeline-v1.7.2` retry-launch Lambda; provides operational stability foundation that Phase 1 probe assumes

---

## 9. Open items for CTO review

1. **File path naming.** `ADVI_INFSHIP_A2.md` vs `ADVI_INFSHIP_OAPI.md` (Orion API) vs `ADVI_INFSHIP_PATH_A.md`. CTO call.
2. **Phase 0 scope completeness.** Is §2 endpoint catalog comprehensive enough or should I add more vendor-discovered endpoints (e.g., the `/api/v1/Reporting/Scope` HAR 7 finding)? Already in §2.1 row 7; flag if additional treatment needed.
3. **Phase 0a ownership.** Should DS BASE consult be a separate TO authored by COO (with CTO co-sign), or kept as a synchronous CTO+COO+DS session per current draft? Current draft assumes the latter for speed.
4. **Phase 1 effort estimate.** Need CTO ballpark on AE 0.6.1~B probe Lambda development (current PRD has no estimate; Phase 1 effort sizing matters for Andrew's GO calculus).
5. **Risk class 4.4 ToS.** Should we include a stronger pre-Phase-1 escape-hatch — e.g., "if vendor outreach yields explicit ToS prohibition, immediately abandon Path A architectural commitment + document as future-state with vendor-collab Path D as alternative"? Currently soft in §4.4 mitigation.
6. **Section 7.1 conditional Phase 2 ordering.** Priority order for Path A migration assumes positions > performance > tax > billing. Should Andrew's INFLEC_PARITY_FILL_CANDIDATES P1-P7 ranking override this default? Current draft says "DS BASE P1 ranking informs Phase 1 probe sequencing" — could explicitly inherit the P1 order in §7.1 instead of redefining.

---

**Draft status:** ~600 lines; covers §1-§9 per CTO concur on scope ("don't over-specify Phase 1+; keep them as conditional stubs"). Ready for CTO review pass + iteration. Pending COO+CTO sign-off → CTO commits canonical at `docs/architecture/ADVI_INFSHIP_A2.md`.
