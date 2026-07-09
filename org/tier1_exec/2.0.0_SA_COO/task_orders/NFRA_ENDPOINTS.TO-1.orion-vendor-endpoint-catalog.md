# Task Order: NFRA_ENDPOINTS TO-1 -- Orion vendor-endpoint catalog (REST-vendor variant, retrofit the existing uncataloged probes)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-08-nfra-endpoints-to1-orion</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-07-08</date>
    <status>complete -- CLOSED 2026-07-09T20:35Z (2.0.0_SA_COO). Evidence: CTO independently VERIFIED all 4 vendor catalogs PRESENT ON DISK 2026-07-09 (BD=data/black_diamond/API; Orion=data/inf/API, Orion being Inflection's platform with domains envision/portfolio/eclipse, Eclipse folded in; SmartX; +1). Project org/projects/NFRA_ENDPOINTS.json is status=complete, completed=2026-07-08, blocking='None -- COMPLETE'. REAP HISTORY, recorded deliberately: this TO was flagged as a stale-TO-on-a-complete-project during /drive cycle 1 and I REFUSED to reap it, because 'a stale TO on a complete project' and 'an open TO proving the project is NOT complete' are indistinguishable from the TO side -- reaping first destroys the evidence. CTO's on-disk catalog verification is the evidence that discriminates them, and it arrived 5 hours later. The hold was correct; the reap is now grounded rather than assumed.</status>
    <dispatch_state>DISPATCHED + GO 2026-07-08 (Andrew-direct via CTO decomp directive; PRD d7b8c9ba2). Orion FIRST per PRD SS9 -- highest existing-value-to-uncover (real probe work already exists, uncataloged). DS~A is the natural owner: just built the data/black_diamond/API/ reference instance + is available + warm on this exact pattern. TO-1 of a per-vendor sequence (Orion -> SmartX retrofit -> Eclipse stand-up -> Schwab file-feed assess).</dispatch_state>
    <gate_note>Gates: none upstream. CTO arch-gates the convention + the Orion catalog's grounded-completeness; CVO certs the claims are REAL captures (roster-is-a-floor honesty). REST-vendor variant (PRD SS4a).</gate_note>
  </metadata>

  <objective>Catalog Orion's vendor-API surface into the canonical REST-vendor variant (PRD SS4a), retrofitting the EXISTING uncataloged probe work (data/inf/manual_api/probe_inflec_billing.py et al. + data/inf/api-recon/ -- a parallel fee-data investigation sitting undiscoverable to other agents, the EXACT class that just bit BD) into a structured, grounded, reusable catalog. Mirror the data/black_diamond/API/ reference instance you just built.</objective>

  <decisions_resolved>PRD SS12 (COO decomposition): Q2 field-dictionary DEPTH = need-driven, not completeness-for-its-own-sake -- REQUIRE a field-level dictionary where field-depth is actually used (as BD's 741-field was, for the fee investigation); a route-catalog suffices where field-depth isn't yet needed. Q3 catalog<->runtime-graph = NOTE as a future integration, do NOT build in v1. Q1 (Schwab file-feed variant) is deferred to the Schwab-assess TO, not this one.</decisions_resolved>

  <requirements>
    <requirement id="1">Location: place the catalog VENDOR-named per the BD precedent (data/black_diamond/ was vendor-named because BD is shared bd+cot). GROUND whether Orion is Inflection-only or a shared vendor first: if shared, data/orion/API/ (vendor-named, cross-referenced from data/inf/); if Inflection-only, data/inf/API/ is acceptable but note the vendor is Orion. Pick + justify per the shared-vs-single-firm test. cot-firm-sep unaffected (this is vendor-API knowledge, not firm data).</requirement>
    <requirement id="2">STRUCTURE (REST-vendor variant, PRD SS4a -- mirror data/black_diamond/API/): README.md (index) + AUTHENTICATION.md (Orion's auth/session model) + domains/{domain}/DOMAIN.md (what it is + HOW it was found -- grounding) + endpoints/README.md (route catalog) + endpoints/payloads/ (REAL captured req/resp + a field_dictionary.csv/md where field-depth is needed) + tools/ (the query harness) + findings/ (the parallel fee-data investigation writeup, so it's discoverable). Lowercase folders / uppercase docs.</requirement>
    <requirement id="3">DISCOVERY PLAYBOOK (PRD SS5): (a) bundle-grep Orion's JS for embedded route/host strings; (b) fold in the existing probe captures (data/inf/manual_api + api-recon) as the grounded evidence; (c) apply ROSTER-IS-A-FLOOR -- catalog OBSERVED endpoints, be HONEST about the undiscovered floor (do NOT present an inferred endpoint as a cataloged fact).</requirement>
    <requirement id="4">FIRM-SEP-NO-DEFAULTS (PRD SS6, NEVER#1, BINDING): any tools/ script under this catalog reads the firm from an explicit param/env + ABORTS if unset or cross-firm -- NO firm default, ever (the commit-gate caught exactly this on bd_endpoint_sweep.py; same standing rule here).</requirement>
    <requirement id="5">GROUNDING + ERRATA (PRD SS7): every cataloged endpoint/field is backed by a REAL capture (HAR/bundle-grep/live probe), cited in DOMAIN.md "how it was found." Any correction NOTES the superseded claim + WHY it existed (traceable errata, NOT silent delete) -- the roster-is-a-floor + BD-IP-bound-reversal discipline.</requirement>
    <requirement id="6">Commit under your author line (data lane). Cross-link the PRD (docs/architecture/NFRA_ENDPOINTS_PRD.md). RAVC me + CTO on the catalog; CVO certs the claims are grounded.</requirement>
  </requirements>

  <compiler_tools_mandate>
    <phase name="before_write">comp-which for any Orion pipeline/artifact you touch; ground the existing probe locations (data/inf/manual_api, data/inf/api-recon) before cataloging.</phase>
    <phase name="before_commit">.tools/commit-gate.sh on any tools/ .py (it will catch a firm-default -- fix to no-default like bd_endpoint_sweep.py); confirm no firm-sep violation on the shared tool.</phase>
    <phase name="after_commit">CVO cert request (grounded-claims / roster-is-a-floor honesty). One-sentence why if a comp tool doesn't fit a cataloging step.</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>MIRRORS the data/black_diamond/API/ reference instance (your build). Same convention; keep them consistent so the pattern generalizes cleanly.</item>
    <item>The parallel Orion fee-data investigation is the highest-value uncover (same class that bit BD) -- catalog it so it's discoverable, don't leave it in loose probe scripts.</item>
    <item>Follow-on TOs sequence after Orion (SmartX retrofit / Eclipse stand-up / Schwab file-feed assess) -- flag COO if the Orion build surfaces convention refinements to fold into those.</item>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion>data/{orion|inf}/API/ exists with the REST-vendor structure (README + AUTHENTICATION + domains/{d}/DOMAIN.md + endpoints/README + payloads/ + tools/ + findings/), mirroring data/black_diamond/API/.</criterion>
    <criterion>Every cataloged endpoint/field is GROUNDED in a cited real capture (no assumed-as-fact); the undiscovered surface is honestly flagged as a floor.</criterion>
    <criterion>The tools/ harness is firm-parameterized with NO firm default (commit-gate clean).</criterion>
    <criterion>The existing uncataloged Orion probe/fee-investigation work is folded in + discoverable. CVO certs the claims are real captures.</criterion>
  </acceptance_criteria>

  <references>
    <ref type="prd">docs/architecture/NFRA_ENDPOINTS_PRD.md (CTO 2026-07-08, Andrew-direct; commit d7b8c9ba2)</ref>
    <ref type="reference">data/black_diamond/API/ (the proven reference instance, this session)</ref>
    <ref type="project">org/projects/NFRA_ENDPOINTS.json</ref>
  </references>
</task_order>
```
