<task_order>
<to_id>MDPF_GLOBAL.T3A.cache-census</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.7.0_AE_CloudOps~F</issued_to>
<date>2026-08-03</date>
<status>pending</status>
<priority>P1 (Andrew-direct GO 2026-08-03 ~20:15Z @3e2b23ebb3; parallel first-wave census -- T3.B invalidation design waits on this + T2.C)</priority>

<title>T3.A: Cache census, live-grounded -- every cache layer on the MDPF serve path mapped with MEASURED evidence</title>

<context>
MDPF_GLOBAL PRD Addendum C (docs/architecture/MDPF_GLOBAL_PRD.md s.C.2 T3 + s.C.4 T3.A row).

You are the right seat for this: your W9 (custom policy ce00305d, DefaultTTL 300 on /api/general/*)
and W9b (advisor-by-firm DefaultTTL 60) closed TODAY under MDLP_MONPUB -- this census must FOLD
THOSE FRESH STATES IN as the current baseline, not rediscover them.

THE SERVE PATH (COO comp-routes confirm 08-03, DESIRED plane): /api/general/mdpf/* behavior ->
edge trio viewer-request `auth-validator-edge` / origin-request `public-data-router` (platinum
rewrite) / origin-response `cache-control-injector` -> s3://opal-data-portal-v2/platinum/mdpf/*.

BANKED INSTRUMENT GAP (CVO register @aeca48e395, 08-03): comp-routes does NOT surface cache-policy
identities, and comp-blast is blind to CF path-pattern nodes. So the tool seeds the map but the
census GROUNDS ON THE LIVE DISTRIBUTION (get-distribution-config) -- this is written into the s.C.4
acceptance itself.

LAYERS TO MAP (denominator = every behavior on the MDPF serve path, printed):
1. CloudFront behavior cache policies -- LIVE get-distribution-config; per behavior: policy
   identity, Min/Default/Max TTL, and which behaviors share each policy.
2. Deployed `cache-control-injector` stamped TTLs -- the DEPLOYED edge version per Rule 22a
   (aws lambda get-function on the published version the distribution pins), NOT committed source.
3. Portal client caches -- React Query staleTime on the mdpf query keys + the 60-min in-memory
   TTLs in portal/src/api/endpoints/aum.ts (ACCOUNT_DIST_CACHE_TTL et al).
4. Any S3/proxy-level cache-control metadata on the served artifacts themselves.
</context>

<scope>
1. Produce ONE cache-map artifact (machine-readable + doc) under
   org/tier2_senior/0.7.0_AE_CloudOps~F/deliverables/MDPF_GLOBAL_T3A/: per layer, per behavior/key:
   TTL + invalidation mechanism + MEASURED evidence.
2. MEASURED means live response headers on the ACTUAL mdpf routes: Age / x-cache /
   cache-control observed (curl the served endpoints; capture full header sets, timestamped).
3. Print the denominator: every behavior on the serve path enumerated; per-layer coverage stated.
4. READ-ONLY: no policy edits, no invalidations fired (an invalidation is a mutation of served
   state), no new monitors/alarms (moratorium). T3.B implements; this WS maps.
5. Note for T3.B handoff: where the current TTL/invalidation posture could clash with a daily
   scheduled publish window (the T2.C clock, not yet ruled) -- flag, do not fix.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before census">
    <step>
      <run>comp-routes behaviors</run>
      <expect>The /api/general/* + advisor-by-firm behaviors enumerated with edge associations; cache-policy identity ABSENT (the banked gap) -- output seeds the behavior denominator only.</expect>
      <if_mismatch>If comp-routes now surfaces policy identities, the gap was closed -- note it to CVO and use both sources.</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions</run>
      <expect>mdpf-relevant React Query keys enumerated (client-cache layer seed); collisions listed if any.</expect>
      <if_mismatch>Note tool gaps; ground the client layer by reading portal/src/api/endpoints/aum.ts + the mdpf hooks directly.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="live grounding, before commit">
    <step>
      <run>aws cloudfront get-distribution-config ... # rail-checked: T3.A live cache census; comp-routes is cache-policy-blind (CVO register @aeca48e395), live distribution is the s.C.4-mandated ground</run>
      <expect>Every serve-path behavior's cache policy identity + TTLs captured from the LIVE distribution; behaviors sharing each policy enumerated (blast radius denominator).</expect>
      <if_mismatch>STOP. A census on the DESIRED plane alone fails the acceptance.</if_mismatch>
    </step>
    <step>
      <run>aws lambda get-function on the deployed cache-control-injector published version # rail-checked: Rule 22a deployed-artifact grounding; committed source is not the deployed edge</run>
      <expect>Deployed version's stamped max-age values extracted from the artifact the distribution actually pins.</expect>
      <if_mismatch>STOP. Source-plane TTL claims are INFERRED, not measured.</if_mismatch>
    </step>
    <step>
      <run>live header measurements: curl the actual mdpf routes (all four scopes + global)</run>
      <expect>Age / x-cache / cache-control captured per route, timestamped; consistent with the layer map or the inconsistency enumerated as a finding.</expect>
      <if_mismatch>An unexplained header/policy disagreement is a FINDING with an owner, not a silent row.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>report to COO + CTO: cache-map path + commit + per-layer denominators + T3.B clash flags</run>
      <expect>MCP report lands; census becomes T3.B's input.</expect>
      <if_mismatch>A report without denominators is REWORK.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Read-only census; no shared writes. T1.A (0.7.0_AE_CloudOps base) reads the same distribution
config concurrently -- read-only both sides, disjoint deliverables; you two are lanes of one base
serial, so coordinate session scheduling with MSTR/COO if seat concurrency binds. Your W9/W9b
fresh state is baseline input, already yours. Output feeds T3.B (yours, staged behind T2.C).
</cross_domain_coordination>

<acceptance_criteria>
Verbatim s.C.4 (CTO validates at close):
1. Per layer: TTL + invalidation mechanism + MEASURED evidence (live response headers:
   Age/x-cache/cache-control on the actual mdpf routes).
2. Denominator = every behavior on the serve path, printed.
Plus standing norms: every causal claim cites file:line @ commit or is labeled INFERRED; no new
alarms/monitors; scheduled-run evidence only where run evidence is cited.
Plus: session log includes a Compiler Tools section reproducing every <run> from
<compiler_tools_mandate> with observed output and explicit pass/fail vs <expect>. Missing rows =
REWORK, not COMPLETE.
</acceptance_criteria>

<references>
  <ref type="prd">docs/architecture/MDPF_GLOBAL_PRD.md (Addendum C s.C.2 T3 + s.C.4 T3.A row)</ref>
  <ref type="register">CVO comp-tool CF coverage gaps @aeca48e395 (comp-routes cache-policy identity; comp-blast CF path-pattern nodes)</ref>
  <ref type="baseline">Your W9/W9b closes (policy ce00305d DefaultTTL 300; advisor-by-firm DefaultTTL 60; tag portal-auth-v1.22.0)</ref>
  <ref type="go">Andrew-direct GO @3e2b23ebb3 (memo-doc s.5); CTO relay 20260803T200329Z</ref>
</references>

<dependencies><none/></dependencies>
</task_order>
