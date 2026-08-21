<task_order>
<id>MDPF_3FIRMS.3F-P2</id>
<title>MDPF endpoint/route audit — the two URL families, the 9 declared-not-live behaviors, and the null-on-404 wrapper</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-P (Platinum) — READ-ONLY AUDIT, parallel-safe from day one</workstream>
<issued_to>0.4.0_DE_ClientPlatform</issued_to>
<joint_assignee>0.7.0_AE_CloudOps (CloudFront / behavior-side reads)</joint_assignee>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:29Z</issued_at>
<status>complete 2026-07-22 (status corrected 2026-08-21 -- work and ISSUER ACCEPTANCE both predate this flip by a month). ACCEPTED AT ISSUER: COO 205817Z, "both TOs ACCEPTED, RAVC closed"; F-1 (no Cottonwood in the declared flip set) rated the most consequential finding of the wave. EVIDENCE PER CRITERION -- the deliverable MDPF_3F_P2_ENDPOINT_ROUTE_AUDIT_20260722.md @39ea5916e carries its own Acceptance mapping section, all five marked and cited: (1) route table Parts 1-3, behavior+origin+auth per flip-served artifact, zero orphans; (2) the 9 declared behaviors mapped to artifacts + producers, each confirmed NOT live against APPLIED config (per-row Live? column); (3) null-on-404 documented at aum.ts:586-608 @08c6d8b2 with its rendered consequence (F-2); (4) comp-routes behaviors run FIRST, intercept rules enumerated -- the discriminating result being that CustomErrorResponses quantity is 0 and the masking is SPA-fallthrough, not interception (F-3); (5) zero TF applied, zero behavior changes, portal-auth drift recorded EXPECTED and not actioned; (6) Compiler Tools section present in the 2026-07-22 logs. 6/6 evidenced.</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z (WS-P audits explicitly parallel-safe from day one).</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-P row 3F-P2; §2.1 serving surface; §3.5 serving path</ref>
</references>

<scope>
(a) **Map the TWO URL FAMILIES**: legacy `/api/general/portfolios/*` vs revamp
    `/api/general/mdpf/{firmId}/*`. Which artifact each serves, which is live, which is declared.
(b) **`comp-routes trace` per endpoint.**
(c) **Map the 9 DECLARED-NOT-LIVE behaviors to their artifacts.**
(d) **Document the account-distribution wrapper's NULL-ON-404 behavior** — a wrapper that converts a
    404 into a null is indistinguishable at the component from "this firm has no data." That is the
    day-one-Cottonwood rendering question in disguise.

⚠ **THE GROUND TRUTH TO START FROM (§2.1, measured):** CloudFront `EVTSA9VEHNZVH` has **24 behaviors /
7 origins and ZERO mdpf/portfolios behaviors live.** Serving is legacy `opal-data-portal-v2` via the
`/api/general/*` catch-all. **Nothing from the revamp has ever been served.**

⛔ **STANDING HAZARD, DO NOT "FIX" IT:** `infra/aws/terraform/portal-auth/` declares 9 mdpf/portfolios
behaviors + an assets origin + an OAC that are **NOT LIVE**. **A drift report on this root is EXPECTED
and is NOT an action item.** Applies there happen only inside WS-F, `-target`ed and named.

⚠ **`comp-routes behaviors` is REQUIRED, not optional, for the 4xx work** — CloudFront custom error
responses INTERCEPT and mask JSON errors, so an endpoint that "returns HTML" may be a masked 404.

⛔ **READ-ONLY. No Terraform, no applies, no behavior changes.**
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-routes behaviors</run>
      <expect>The custom_error_response intercept rules enumerated — what masks what.</expect>
      <if_mismatch>Without this, a masked 404 reads as a broken endpoint. Do not diagnose any 4xx before running it.</if_mismatch>
    </step>
    <step>
      <run>comp-routes trace &lt;endpoint&gt; — for EVERY endpoint in both URL families</run>
      <expect>Each resolves to behavior + origin + auth path.</expect>
      <if_mismatch>An endpoint that does not resolve is an ORPHAN — record it; do not assume it is dead.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run># rail-checked: live CloudFront distribution config read (applied truth)
aws cloudfront get-distribution-config --id EVTSA9VEHNZVH</run>
      <expect>24 behaviors / 7 origins; ZERO mdpf/portfolios behaviors live — confirming §2.1 at current state.</expect>
      <if_mismatch>If behaviors ARE live, the serving premise of the whole project has changed — STOP and escalate to COO + CTO immediately.</if_mismatch>
    </step>
    <step>
      <run>Map each of the 9 declared-not-live behaviors (portal-auth/ TF) to the artifact it would serve</run>
      <expect>A 9-row table: behavior -> artifact -> producer -> live? (all "no").</expect>
      <if_mismatch>A declared behavior with no corresponding artifact is a finding for WS-F — the flip would serve a 404.</if_mismatch>
    </step>
    <step>
      <run>Trace the account-distribution wrapper's null-on-404 path at source</run>
      <expect>The behavior documented at file:line @ commit-ish, with its rendered consequence stated.</expect>
      <if_mismatch>Do not infer the behavior from the rendered output — read the wrapper.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-routes trace (re-run) on the revamp family</run>
      <expect>Unchanged — read-only TO, no footprint.</expect>
      <if_mismatch>Investigate any change; nothing here should have modified routing.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <no_reprocess_needed>Read-only audit. No TF applied, no code changed, no data written.</no_reprocess_needed>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="CloudFront EVTSA9VEHNZVH + portal-auth/ TF" shared_with="0.7.0_AE_CloudOps (3F-S3, WS-F)">
    0.7.0 executes applies in WS-F. This TO READS ONLY. ⛔ He must not apply in `portal-auth/` on the
    strength of this audit — WS-F is the only place that happens.
  </resource>
  <resource path="served artifact inventory" shared_with="0.4.0_DE (3F-P1)">
    P1's locus table and this route table are complements — reconcile them before committing either.
  </resource>
</cross_domain_coordination>

<dependencies><dependency type="none">Parallel-safe from day one; no gate.</dependency></dependencies>

<acceptance_criteria>
1. Route table committed: **every artifact the flip will serve has a named behavior + origin + auth
   path**; zero orphan endpoints (or each orphan itemized).
2. The 9 declared-not-live behaviors mapped to artifacts, each confirmed NOT live against the live
   distribution config.
3. The account-distribution wrapper's null-on-404 behavior documented at `file:line @ commit-ish`, with
   its rendering consequence stated.
4. `comp-routes behaviors` output read and the intercept rules enumerated before any 4xx diagnosis.
5. Zero Terraform applied; zero behavior changes; the portal-auth drift report explicitly recorded as
   EXPECTED and not actioned.
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO. Escalate IMMEDIATELY if any mdpf/portfolios behavior is found LIVE — that would mean something has been served that the project believes has never been served.</escalation>
</task_order>
