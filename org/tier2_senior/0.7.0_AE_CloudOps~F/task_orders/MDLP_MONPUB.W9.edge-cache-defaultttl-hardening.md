<task_order>
<to_id>MDLP_MONPUB.W9.edge-cache-defaultttl-hardening</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~F</issued_to>
<date>2026-08-03</date>
<status>pending</status>
<priority>P1-adjacent (Andrew is watching the cache-invalidation family of work -- CVO 164133Z Andrew-direct relay; do not let it age)</priority>

<title>W9: stop the cache-control-injector being load-bearing for the /api/general/* TTL -- align the edge cache policy to 300s in Terraform</title>

<context>
CTO dispatch request 20260803T164247Z (registered as W9 in the MDLP_MONPUB spec 5b amendment).

THE DEFECT CLASS (config-disagreement, not an outage): the /api/general/* CloudFront behavior runs
cache policy Managed-CachingOptimized with DefaultTTL 86400 (24h). The EFFECTIVE ~5-min TTL exists
ONLY because the cache-control-injector Lambda@Edge stamps max-age=300 on responses. Consequences:
injector failure, detachment, or any NEW JSON-serving behavior shipped without the injector
SILENTLY inherits 24-HOUR edge caching -- the exact staleness-invisibility family this whole
project has been fixing (a diligent path whose absence leaves no trace).

CTO-endorsed hardening: align the cache policy DefaultTTL to 300 in Terraform so the TTL holds
with OR without the injector. Config-agreement fix; NO monitor, NO alarm (standing moratorium --
this is moratorium-clean by construction).

TECHNICAL NUANCE THAT SHAPES THE FIX (verify at Phase 1, do not take my word):
Managed-CachingOptimized is an AWS MANAGED policy -- its TTLs cannot be edited. If /api/general/*
indeed runs the managed policy, the fix is: author a CUSTOM cache policy in TF (DefaultTTL 300;
ground Min/Max TTL choices against current behavior -- injector stamps max-age=300, so MaxTTL must
not be below what correctness needs) and swap the /api/general/* behavior's cache_policy_id to it.
SCOPE CONTROL: swap ONLY the behavior(s) in scope; every OTHER behavior sharing the managed policy
keeps it unless CTO widens scope explicitly.
</context>

<scope>
1. Ground the current state: which distribution + behavior(s) serve /api/general/*, which cache
   policy each runs, and which OTHER behaviors share that policy (blast radius).
2. TF change per the nuance above (custom policy + targeted swap, or direct TTL edit if the policy
   turns out to be customer-managed). Commit-before-apply, .tools/safe-apply.sh, plan reviewed,
   0-diff after apply, tag + push --follow-tags per deploy rules (integrator-push discipline
   applies to the push leg -- coordinate with MSTR if the window binds).
3. Exercise the fix: after apply, verify on the LIVE distribution config (aws cloudfront
   get-distribution-config or comp-routes behaviors re-run) that the behavior's policy carries
   DefaultTTL 300 -- and verify the injector's stamped max-age still wins/agrees on a real
   response (curl response headers on a served JSON: Cache-Control present AND edge Age behavior
   consistent with 300s, not 86400).
4. OUT OF SCOPE: touching the injector itself; any other behavior's policy; anything that pages
   or alerts.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-routes behaviors</run>
      <expect>The /api/general/* behavior enumerated with its cache policy identity; full list of behaviors sharing that policy captured as the blast radius denominator (print it).</expect>
      <if_mismatch>STOP. If comp-routes cannot resolve the policy identity, ground on aws cloudfront get-distribution-config (operational read, no rail conflict) and record the gap to CVO as a comp-routes coverage finding.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on the distribution/behavior node (or comp-aws equivalent per comp-which routing)</run>
      <expect>Consumers of /api/general/* enumerated -- confirm the portal data paths (benchmarks JSON among them) and no consumer depends on LONG edge caching.</expect>
      <if_mismatch>STOP. A consumer relying on 24h caching is a design conflict -- surface to CTO before writing TF.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/terraform.exe plan (via the standard wrapper) on the TF change</run>
      <expect>Plan shows EXACTLY the intended resources: new custom cache policy (if managed-policy path) + the one behavior's cache_policy_id swap. ZERO changes to other behaviors, origins, or the injector association.</expect>
      <if_mismatch>STOP. Any additional resource in the plan = scope breach; do not apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>.tools/safe-apply.sh, then re-plan for 0-diff, then live verify: get-distribution-config on the behavior + a real response-header check on a served /api/general/* JSON</run>
      <expect>0-diff; live config shows DefaultTTL 300 on the behavior's policy; response headers consistent with a 300s TTL regime (injector still stamping, config now agreeing).</expect>
      <if_mismatch>STOP and report -- a live config that disagrees with a 0-diff plan is an instrument problem, not a deploy problem.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. Blast radius denominator printed at Phase 1 (behaviors sharing the policy), and the swap touched ONLY the in-scope behavior(s).
2. Plan reviewed with exact expected resource set; 0-diff after apply; tag pushed --follow-tags.
3. Live verify BOTH layers: distribution config (DefaultTTL 300) AND a real response exercising the path -- config read alone is not a behavioral claim (Rule 22a).
4. The injector remains attached and stamping (this TO removes its load-bearing status, not the injector).
5. Session log Compiler Tools section reproduces every <run> + observed output + pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<cross_domain_coordination>
W6 (portal client-cache invalidation) is in flight at 0.2.0_DT_PortfolioAnalytics and is the
watched-priority sibling -- W9 is edge-side, W6 is client-side; no shared files expected, but if
your grounding shows the SAME distribution/behavior being exercised by W6's invalidation tests,
MCP DT before applying so an invalidation test does not race your policy swap. CloudFront changes
also touch the shared-infra family: comp-routes behaviors is the pre-change gate per CLAUDE.md.
</cross_domain_coordination>

<references>
  <ref type="cto-dispatch">org/mcp/inbox/2.0.0_SA_COO/read/20260803T164247Z_1.0.0_SA_CTO_DISPATCH_REQUEST__W9__edge-cache_Default.md</ref>
  <ref type="spec">MDLP_MONPUB spec 5b amendment (CTO commit, 2026-08-03 ~163x Z)</ref>
  <ref type="andrew-priority">CVO 164133Z Andrew-direct relay (cache-invalidation findings watched)</ref>
</references>

<acceptance_note>
A TO completion report whose session log lacks the Compiler Tools reproduction is REWORK, not
COMPLETE (TO_COMPILER_GATE).
</acceptance_note>
</task_order>
