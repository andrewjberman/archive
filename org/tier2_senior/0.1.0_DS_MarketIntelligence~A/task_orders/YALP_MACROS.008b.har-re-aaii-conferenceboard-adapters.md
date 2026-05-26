<task_order>
<metadata>
  <to_id>YALP_MACROS.008b</to_id>
  <project>YALP_MACROS</project>
  <title>Phase 2b Wave 2 partial — AAIIAdapter (sentiment.xls Cloudflare-gated) + ConferenceBoardAdapter (data-central JSON API cookie-session); 2 RICH HAR-derived adapter classes per ws CTO triage</title>
  <assigned_to>0.1.0_DS_MarketIntelligence~A</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending — GO dispatched cycle 114 extended carry-on</status>
  <priority>HIGH (TO-008 RAVC2-ACCEPTED 30bd38cf0; Andrew HAR triage 5-set RICH 2-of-5 unlocks +5 indicators coverage 73% → ~80%; ws CTO substrate-handoff MCP `20260526T~22:21Z` pre-positioned)</priority>
  <references>
    <ref type="upstream">TO-008 multi-source RE harness build RAVC2-ACCEPTED commit `30bd38cf0` (cycle 114 ratification); AdapterBase inheritance substrate</ref>
    <ref type="har_substrate">Andrew HAR triage 5-set per ws CTO MCP `20260526T~22:21Z`: (1) AAII `sentiment.xls` direct-download via Cloudflare cookie bundle (cf_clearance + __cf_bm); (2) Conference Board `data-central.conference-board.org/api/indicators` 8.25 MB JSON cookie-session (data_central_session + XSRF-TOKEN + ECONPORTALUSER + ECONPORTALUSERADDR + CFID/CFTOKEN)</ref>
    <ref type="aws_secrets">`aaii/credentials` + `conferenceboard/credentials` cookie bundles to be onboarded per ws CTO recommendation (or HAR bundles inlined direct if Secrets pre-stage not ready)</ref>
    <ref type="coverage_delta">+5 indicators: AAII Sentiment Bullish #52 + Neutral #53 + Bearish #54 (3) + CB CCI #43 + CB LEI #1 REPRESENTATIVE-path (2); pushes coverage 73.4% → ~80%</ref>
  </references>
  <dependencies>
    <dependency>None — TO-008 substrate ready + AdapterBase inheritance + Andrew HARs absorbed by ws CTO + pre-positioned via ws CTO substrate-handoff MCP</dependency>
  </dependencies>
</metadata>

<scope>
**Implement 2 HAR-derived adapter classes** extending TO-008 AdapterBase per ws CTO HAR triage RICH-class substrate. Output: 2 new adapter modules + shared cookie-bundle handling pattern per `c6_ycharts_cred_refresh.py` precedent.

**Substrate (2 deliverables):**

1. **`data/yang_macros_re/adapters/aaii_adapter.py`** — `AAIIAdapter` class
   - XLS direct-download `https://www.aaii.com/files/surveys/sentiment.xls`
   - Cookie-bundle authentication (`cf_clearance` + `__cf_bm` from Cloudflare gate; Andrew HAR captured)
   - Parse via `pandas.read_excel`
   - Map 3 indicators: AAII Sentiment Bullish (#52) + Neutral (#53) + Bearish (#54)
   - AWS Secrets `aaii/credentials` bundle source (or HAR bundle inlined if Secrets not pre-staged — clearly documented)
   - Standard AdapterBase contract: `fetch_series(series_id, start, end) → DataFrame[date, value, source_metadata]`

2. **`data/yang_macros_re/adapters/conference_board_adapter.py`** — `ConferenceBoardAdapter` class
   - Cookie-session API: POST `/api/authentication` then GET `/api/indicators` (8.25 MB JSON)
   - Sister endpoints: `/api/indicator-infos` (metadata enumeration for additional indicator discovery beyond CCI + LEI)
   - Cookie-bundle authentication (data_central_session + XSRF-TOKEN + ECONPORTALUSER + ECONPORTALUSERADDR + CFID/CFTOKEN)
   - Map 2+ indicators: CB CCI (#43) + CB LEI (#1 REPRESENTATIVE-path)
   - Stretch: enumerate `/api/indicator-infos` schema for additional 79-universe coverage discovery (post-MVP within scope; report findings inline)
   - AWS Secrets `conferenceboard/credentials` bundle source (or HAR inlined if Secrets not pre-staged)

**Shared cookie-bundle handling pattern:**
- Follow `c6_ycharts_cred_refresh.py` precedent for refresh + Secrets-write
- AdapterBase inheritance + `Observation` dataclass + `AdapterError` exception chain unchanged from TO-008

**Per CLAUDE.md Rules 13, 14, 14a, 15 binding** (DS owns full cycle + ds-commit-gate.sh + `--only` --safe-commit + `from __future__ import annotations`).

**Wave 5 RE-DEFERRED 6-PAID-no-substitute indicators UNCHANGED** — TO-008b does NOT touch architectural-call class. Default (c) RE-GAP acceptable-by-documentation per Andrew sovereign 21:00Z stands.

**Remaining HAR-RE-CANDIDATE indicators (9: AAII AssetAlloc ×3 + NAHB + NAR + UMich + NFIB + TIC + sister captures) DEFERRED to TO-008c follow-on** when Andrew completes additional HAR captures (parallel substrate-arrival in flight per ws CTO MCP).
</scope>

<acceptance_criteria>
- AC1: AAIIAdapter implements AdapterBase contract; live-fetches `sentiment.xls` via cookie bundle; parses 3 sentiment indicators (Bullish #52 + Neutral #53 + Bearish #54); empirical smoke-fetch values reported.
- AC2: ConferenceBoardAdapter implements AdapterBase contract; authenticates via cookie-session; live-fetches `/api/indicators`; parses CCI (#43) + LEI (#1) values + reports any additional 79-universe indicators discovered via `/api/indicator-infos`.
- AC3: AWS Secrets bundle handling pattern per `c6_ycharts_cred_refresh.py` precedent (or HAR inlined with clear documentation of Secrets onboard pending).
- AC4: ds-commit-gate exit-0 + `from __future__ import annotations` + LF-not-CRLF discipline.
- AC5: Coverage delta documented — pre-TO-008b 73.4% → post-TO-008b ~80% (or higher if CB schema enumeration unlocks additional indicators).

**Pass requires all 5 ACs MET.**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-pipescript io` on each new adapter before edit
- `comp-iam service` for AWS Secrets Manager read (verify `inf-gold-runner-ec2-role` or applicable role has `aaii/credentials` + `conferenceboard/credentials` access; surface gap if missing — Secrets onboard may need AE 0.7 lane)
- `comp-validate` post-fixture-run per adapter
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-008 substrate inheritance:** AdapterBase + Observation + AdapterError + secrets.py + boto3 + lru_cache from `30bd38cf0` unchanged.
- **AWS Secrets onboarding** for `aaii/credentials` + `conferenceboard/credentials` may require AE 0.7 lane coordination if Secrets are not pre-staged. AE 0.7 is currently LIVE (PID 24148; spawning per MDPF_OWNTS.002). Surface gap to ws COO if Secrets not accessible — light MCP route to AE 0.7 lane.
- **TO-008c follow-on** for remaining 9 HAR-RE-CANDIDATE indicators gated on Andrew's parallel HAR captures (NAHB + NAR + UMich + NFIB + TIC + AAII AssetAlloc). ws CTO will MCP separately when HARs land.
- **Phase 2c TO-009 RE test-pulls** sequences AFTER TO-008b RAVC2-ACCEPT. ~30-45min target wall for TO-008b per ~A pre-positioned plan.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing:
- Commit hashes (adapter ship + comp-validate exit-0)
- LIVE-VERIFIED smoke-fetch values for AAII 3 sentiment + CB CCI + CB LEI (+ any additional CB-discovered indicators)
- Coverage delta confirmation (~80% target or higher)
- AC1-AC5 evidence inline

**Target wall-time ETA:** ~30-45min per ~A pre-positioned plan (cascade-compression amplifier sustained across substrate-rich impl-class TOs). Sub-30min plausible if Secrets pre-staged + HAR-bundles cleanly translatable.

**Post-RAVC2-ACCEPT:** Phase 2c TO-009 RE test-pulls dispatch (multi-day scope; gates on TO-008+TO-008b RAVC2-ACCEPT both clear).
</deliverable_disposition>

<notes>
- TO-008b is the **fast-path narrow scope** unlocked by Andrew's 2 RICH HARs of 5 captured today. The other 9 HAR-RE-CANDIDATE indicators await additional HAR captures + are TO-008c follow-on territory.
- Per cascade-compression precedent (your TO-007 7-10min + TO-008 ~8min + cumulative substrate-density), ~30-45min ETA is conservative; sub-30min plausible.
- 16th memory candidate flagged from TO-013: `ycharts-macro-class-entitlement-gap-is-structural-not-cookie-eviction-class` — sister to LD-31 + Andrew sovereign 400-cookie-stale doctrine. Not in TO-008b scope but banking continues.
</notes>
</task_order>
