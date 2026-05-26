<task_order>
<metadata>
  <to_id>YALP_MACROS.008</to_id>
  <project>YALP_MACROS</project>
  <title>Phase 2b multi-source RE harness build — per-source adapter classes (Wave 1-5 sequence per TO-007 §7) + 71/79 (89.9%) PRIMARY-implementable target</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <co_authors>0.1.0_DS_MarketIntelligence~B (Wave-3 BLSAdapter overlay), 0.1.0_DS_MarketIntelligence~C (Wave-4 CensusAdapter overlay), 0.1.0_DS_MarketIntelligence~D (Wave-4 TreasuryAdapter overlay), 0.1.0_DS_MarketIntelligence~E (Wave-1 YahooFinanceAdapter + Wave-2 HAR-RE-CANDIDATE adapters)</co_authors>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatched cycle 113</status>
  <priority>HIGH (Phase 2b sequential follow-on to TO-007 RAVC2-ACCEPT 59ab271de + §12 amendment 7024d6aba; Andrew sovereign 2026-05-26T~21:00Z RE-OPEN Phase 2 mandate)</priority>
  <references>
    <ref type="prd">docs/architecture/YALP_MACROS.md v0.5 §8 line 180 — TO-008 canonical scope</ref>
    <ref type="upstream">TO-007 synthesis brief `59ab271de` (~770 lines) + §12 amendment `7024d6aba` (Fed NLP reclassification yang-internal → PAID-SUB)</ref>
    <ref type="phase2a_substrate">All 5 Phase 2a briefs ratified (~A FRED `da862a6c6` + ~B BLS `be703b5b1` + ~C Census `ba147dbc5` + ~D Treasury/FDIC `e48480c5e` + ~E Aggregate-orphan `8de9c10f7`)</ref>
    <ref type="architectural_decisions_formalized">FRED-PRIMARY runtime + sister-CROSS-CHECK overlay + ~E PRIMARY for 24 FRED-GAP via 6-tier access-class taxonomy</ref>
    <ref type="andrew_sovereign">2026-05-26T~21:00Z RE-OPEN "go exploring" + monthly-cadence-tolerance + "push down PRD queue" RE-GAP-acceptable-by-documentation framing</ref>
  </references>
  <dependencies>
    <dependency>TO-007 RAVC2-ACCEPTED `59ab271de` (cycle 112 carry-on)</dependency>
    <dependency>Phase 2c TO-009 (RE test-pulls) + TO-010 (spreadsheet) + TO-VAL-v2 (consolidated RAVC2) gate on this RAVC2-ACCEPT</dependency>
  </dependencies>
</metadata>

<scope>
**Multi-source RE harness build** — implement per-source adapter classes per TO-007 §7 Wave 1-5 sequence. Output: production-ready harness that pulls per-indicator authoritative-source data for the 79-indicator Macroeconomics page universe, with sister-CROSS-CHECK overlay capability for Phase 2c verification.

**Deliverable:** harness module set at `data/yang_macros_re/` (or comparable per-source path TBD by ~A; consult existing yang infra layout):
- `data/yang_macros_re/adapters/fred_adapter.py` (Wave 1 PRIMARY)
- `data/yang_macros_re/adapters/yahoo_finance_adapter.py` (Wave 1 OPEN-REST for ~E primary subset)
- `data/yang_macros_re/adapters/bls_adapter.py` (Wave 3 CROSS-CHECK overlay)
- `data/yang_macros_re/adapters/census_adapter.py` (Wave 4 CROSS-CHECK overlay)
- `data/yang_macros_re/adapters/treasury_adapter.py` (Wave 4 CROSS-CHECK overlay)
- Wave 2 HAR-RE-CANDIDATE adapters (~E §4; 11 indicators) — implementation deferrable to follow-on TO-008b if Wave 1-3+4 ship cleanly first
- Wave 5 architectural-call indicators (6 PAID-no-substitute post-§12 amendment) — RE-DEFERRED per Andrew (c) RE-GAP acceptable-by-documentation; documented in harness but NOT live-pulled v1

**Required substrate (per Wave):**

**Wave 1 (~30min target):**
- `FREDAdapter` v1 2-step pattern (release/series → series/observations) per ~A §4; 55-series registry constants; v2 OAuth swap-in scaffold commented
- `YahooFinanceAdapter` non-crumb-gated `/v7/finance/chart` per ~E §4; ^MOVE + CNH=X + AGG ETF-NAV LIVE-VERIFIED quick-wins
- Shared adapter interface contract (Python ABC): `fetch_series(series_id, start, end) → DataFrame[date, value, source_metadata]`
- AWS Secrets Manager integration for FRED API key (`FredApiKey` per ~D §9 cite)
- 59/79 = 74.7% PRIMARY-implementable at Wave 1 OPEN-REST tier

**Wave 2 (~2h target; deferrable to TO-008b if Wave 1 ships first):**
- HAR-RE-CANDIDATE adapters per ~E §4 (11 indicators: LEI + CCI + NAHB + PHSI + UMich 5Y + AAII×6 + TIC partial)
- 4-session HAR-capture sequence per ~D §7 precedent (subagent fan-out parse pattern)
- +11 = 70/79 = 88.6% PRIMARY-implementable cumulative

**Wave 3 (~1h target):**
- `BLSAdapter` v2 POST + v1 GET fallback per ~B §4; 10-series registry; partial-success defensive check + 73-survey catalog ground-truth
- CROSS-CHECK overlay for ~10 labor/inflation FRED-mirror indicators
- BLS-revision-flag richness exposure for Phase 2c verdict-confidence tracking
- +1 = 71/79 = 89.9% PRIMARY-implementable cumulative (Wave 3 closes OPEN-tier)

**Wave 4 (~1h target):**
- `CensusAdapter` per ~C §4 (EITS dataset endpoints + sub-component + SA-toggle)
- `TreasuryAdapter` per ~D §4 (Treasury Direct CSV + Treasury Fiscal Data + NY Fed Markets + BEA NIPA primitives)
- CROSS-CHECK overlay for ~30 Treasury/financial + ~10 Census indicators
- 3-way cross-validation pattern (FRED + sister-direct + yang-Bloomberg) for high-confidence indicators

**Wave 5 (deferred — RE-DEFERRED documentation only):**
- 6 PAID-no-substitute architectural-call indicators (post-§12 amendment): ISM PMI×2 + ISM New Orders×2 + Wards + S&P Global PMI×2 net 5 + Fed NLP Sentiment (Bloomberg `BENLPFED Index`)
- Default (c) RE-GAP acceptable-by-documentation per Andrew sovereign 21:00Z "push down PRD queue" + monthly-cadence-tolerance framing
- Document substitute paths inline (Empire State + Philly Fed BOS for ISM; `DAUTOSAAR` for Wards; ETF-NAV chains for AGG) — substitute implementation IS implementable but NOT v1 unless Andrew rules subscribe/substitute on Q3 batch surface

**Cleanup-class findings (per TO-007 §5 + §12 amendment) — harness-side accommodation:**
- Ted Spread DISCONTINUED — implement SOFR-3M − T-Bill-3M substitute behind a `--substitute-ted-spread` flag (default OFF v1; activate post Andrew Q3 ratification)
- ICSA/CCSA mis-attribution — harness fetches DoL ETA via FRED-mirror correctly (not BLS); yang-side audit routes ws CTO + DT 0.1.0 separately (cycle 113 cleanup MCP)
- PPI modern WPSFD4 vs legacy WPU00000000 — harness default = LEGACY (yang continuity); MODERN behind `--ppi-modern` flag (default OFF v1; activate post Andrew Q4 ratification)
- INDPRO label-variant — harness label normalization yang-canonical; ws CTO + DT 0.1.0 cosmetic rename separate (cycle 113 cleanup MCP)
- Fed NLP — harness routes to Bloomberg API IF available (existing data.pkl yang upstream stream OR PAID-API direct); v1 documents as Bloomberg `BENLPFED Index` PAID-class; no live-pull v1 per RE-DEFERRED disposition

**Per CLAUDE.md Rules 13, 14, 14a, 15 binding** (DS owns full cycle + ds-commit-gate.sh + safe-commit.sh --only + `from __future__ import annotations`).
</scope>

<acceptance_criteria>
- AC1: Wave 1 adapters (FREDAdapter + YahooFinanceAdapter) live-implementable; LIVE-VERIFIED smoke-fetch for ^MOVE + CNH=X + AGG + 2 FRED-PRIMARY indicators per Wave-1 group (e.g., DGS10 Treasury Yields + UNRATE Unemployment).
- AC2: Wave 3 BLSAdapter live-implementable; CROSS-CHECK overlay smoke-verify on ~3 labor/inflation FRED-mirror indicators (e.g., CPI headline + UNRATE + PAYEMS); 3-way cross-validation pattern documented.
- AC3: Wave 4 CensusAdapter + TreasuryAdapter live-implementable; CROSS-CHECK overlay smoke-verify on ~3 indicators each (Census ~3 from EITS resconst/ressales; Treasury ~3 from Treasury Direct + BEA).
- AC4: Shared adapter interface contract documented + ABC enforced; per-adapter rate-limit policy + retry/backoff + partial-success defensive check per ~B §4 pattern.
- AC5: AWS Secrets Manager integration verified for FRED API key (no hardcoded keys; per ~D §9 discipline).
- AC6: Harness comp-validate config + ds-commit-gate.sh exit-0 on all touched Python; `from __future__ import annotations` on all gold/lib files; LF-not-CRLF discipline.
- AC7: 6-PAID-no-substitute architectural-call indicators documented in harness as RE-DEFERRED v1 per Andrew sovereign default (c); substitute paths documented inline (not implemented v1 unless Andrew Q3/Q4 ratify substitute).

**Pass requires Wave 1+3+4 (AC1-AC7) MET; Wave 2 + Wave 5 are sub-scope-deferrable to TO-008b follow-on if Wave 1+3+4 ship cleanly first (target: ship Wave 1+3+4 in single TO-008; defer Wave 2 HAR-RE-CANDIDATE to TO-008b if scope-bound).**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-pipescript io` on each adapter script before edit (column gaps + portal consumers + S3-DYNAMIC reads)
- `comp-iam service` for AWS Secrets Manager read (verify `inf-gold-runner-ec2-role` or applicable role has access)
- `comp-validate [script]` post-fixture-run per adapter
- `comp-blast [adapter]` for cross-adapter dependencies if shared interface refactoring surfaces
</compiler_tools_mandate>

<cross_domain_coordination>
- **Co-author scope per TO-007 §7 Wave allocation:**
  - Wave 1 YahooFinanceAdapter: ~E primary (their LIVE-VERIFIED substrate `8de9c10f7`)
  - Wave 3 BLSAdapter: ~B co-author (their BLSAdapter v2 POST class substrate `be703b5b1`)
  - Wave 4 CensusAdapter: ~C co-author (their EITS substrate `ba147dbc5`)
  - Wave 4 TreasuryAdapter: ~D co-author (their FRED v1 2-step pattern substrate `6d3a75014` + Treasury Direct `e48480c5e`)
- Co-author MCPs OPTIONAL — ~A primary author consumes co-author substrates directly + cites; sub-RAVC2 not required unless conflict surfaces. Single integrated commit by ~A primary; ~B/~C/~D/~E KEEP-EPHEMERAL pending TO-008 RAVC2-ACCEPT.
- **Phase 2c gates on this RAVC2-ACCEPT** — TO-009 RE test-pulls + TO-010 spreadsheet + TO-VAL-v2 consolidated RAVC2 sequential.
- **No portal coupling v1** — TO-007 §8 documented; harness output to S3 paths v1; portal binding follow-on if Andrew directs.

**Andrew Q3 + Q4 cleanup-findings architectural-call (CYCLE 112 user-facing close routing):**
- Q3 Ted Spread SOFR-substitute decision — harness implements behind `--substitute-ted-spread` flag default OFF; Andrew ratify substitute → activate flag v1.1
- Q4 PPI modern/legacy decision — harness implements legacy default; MODERN behind `--ppi-modern` flag default OFF; Andrew ratify modern → activate flag v1.1
- Both default-proceed per ALWAYS-PROCEED LD-0084 + Constitution v1.4 Art. XVI; CVO consult fallback per LD-0026 if Andrew silent >1 /drive cycle (cycle 114+).
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing:
- Commit hashes (adapter ship commits + comp-validate exit-0 confirms)
- LIVE-VERIFIED smoke-fetch S3 artifacts OR test-output captures for AC1-AC3 per-adapter
- 6-PAID architectural-call RE-DEFERRED documentation block per AC7
- AC1-AC7 evidence inline

**Target wall-time ETA:** ~3-5h per PRD §8 line 180. Sub-3h plausible if cascade-compression pattern continues (your TO-007 7-10min wall + heavy substrate-reuse). Most plausibly: Wave 1 ~30min ship + Wave 3 ~1h + Wave 4 ~1h = ~2.5h core; Wave 2 deferred to TO-008b if scope-bound; Wave 5 documentation-only.

**Post-RAVC2-ACCEPT:** Phase 2c TO-009 RE test-pulls dispatch. Co-authors return KEEP-EPHEMERAL until TO-009 sub-task dispatches (Wave 4 CROSS-CHECK overlay smoke-tests per their substrate per their adapters).
</deliverable_disposition>

<notes>
- This is the IMPLEMENTATION TO following the synthesis TO-007. Substrate-richness factor compounds: 5 Phase 2a briefs + 1 synthesis brief + §12 amendment = the ENTIRE Phase 2a+2b §1-9 corpus is consumable as substrate. Plausibly the densest substrate-reuse TO this session.
- Sub-3h ETA gate: if at ~Wave 3 mid-ship you forecast >5h total wall, MCP me at split-RAVC2-Request decision-point (Wave 1+3 RAVC2 separately; Wave 4 follow-on TO-008b). Per [[feedback_corroborate_with_concern_verdict_shape]] sister disposition. Default-proceed: ship all 3 Waves in single TO-008 RAVC2.
- TO-008b carry-forward candidate: Wave 2 HAR-RE-CANDIDATE adapters (11 indicators; ~2h). MCP me at TO-008 RAVC2-Request with status of Wave 2 (included vs deferred to TO-008b).
- Memory candidate banking continues — 13 candidates from TO-007 + #14 from §12 amendment (yang-code-path-spelunk-class). New TO-008 candidates emerging at harness-impl time fold into final TO-VAL-v2 consolidated memory bank.
</notes>
</task_order>
