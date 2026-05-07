<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.00</id>
    <project>ADVI_FIRMSEP</project>
    <title>Phase 0 — shared bucket + cache policy classification audit</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <priority>high</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.5 + §6 Phase 0</ref>
    <ref type="andrew_directive">2026-05-07 "containment of data in those cached layers is paramount"</ref>
    <ref type="andrew_routing">2026-05-07 "TOs go to 0.7.0_AE_CloudOps~B" (sub-agent ~B specifically; primary ~A continues INFETL Phase 1)</ref>
    <ref type="cto_finding">PRD §2 G6 — opal-data-portal-v2-json multi-tenant origin; cache-key composition unverified for Managed-CachingOptimized + json_tiered_5min</ref>
    <ref type="related_to">FIRMSEP.06 (CONDITIONAL — gates on this audit's findings)</ref>
  </references>

  <context>
    CTO read-side audit confirmed cache-layer compartmentalization is structurally
    sound for /api/scoped/advisor-intelligence/* — opal_scoped_advisor_by_firm
    cache policy includes firm + X-Firm-Id header.

    UNREAD: whether /api/general/* (which routes to opal-data-portal-v2-json shared
    multi-tenant origin) carries any firm-specific data. Cache policies for those
    behaviors are Managed-CachingOptimized (AWS managed) + json_tiered_5min (custom,
    ID 3eda5c45-0def-4131-87bc-19a31223c270). If firm-specific data flows through
    these paths without firm partitioning in cache key, cross-firm cache poisoning
    is structurally possible.

    LOW severity adjacent: tier-router-edge defined in portal-auth/lambda-edge.tf:82-100
    but no behavior associates it. Either dead code or wired via console — opaque
    enough to surface in same audit.

    This TO produces the audit doc. FIRMSEP.06 (cache-key partition fix) gates on
    findings — if opal-data-portal-v2-json holds only firm-agnostic content,
    FIRMSEP.06 closes N/A.
  </context>

  <scope>
    <step>
      Enumerate opal-data-portal-v2-json bucket contents — list top-level prefixes:
        aws s3 ls s3://opal-data-portal-v2-json/
      For each prefix, classify firm-specific|firm-agnostic. If firm-specific, note
      whether path includes firm slug, query needs firm filter, or content is mixed.
    </step>
    <step>
      Read public-data-router/index.mjs Lambda@Edge — does it firm-partition? path or
      query basis? Document logic with line refs.
    </step>
    <step>
      AWS CLI describe both cache policies referenced by /api/general/* + /api/general/json-tiered/*:
        aws cloudfront get-cache-policy --id Managed-CachingOptimized
        aws cloudfront get-cache-policy --id 3eda5c45-0def-4131-87bc-19a31223c270
      Document cache-key composition: query strings (whitelisted), headers, cookies.
    </step>
    <step>
      tier-router-edge — confirm association status:
        Read cloudfront-distribution.tf — search for tier-router-edge ARN refs in
        any behavior block.
        AWS describe-distribution + grep behaviors for the function ARN.
      Outcome: live (note behavior + path), dead (recommend removal in Phase 4 carry),
      or console-wired (FLAG to COO).
    </step>
    <step>
      Author docs/architecture/ADVI_FIRMSEP_PHASE0_AUDIT.md with:
        - Bucket prefix table (prefix | firm-specificity | rationale)
        - public-data-router routing logic summary + line refs
        - Cache policy composition table (policy | query whitelist | header whitelist | cookie whitelist)
        - tier-router-edge association status verdict
        - VERDICT for FIRMSEP.06 GO|N/A — based on whether firm-specific data flows
          through opal-data-portal-v2-json paths without firm partition in cache key
        - VERDICT for tier-router-edge FIRMSEP carry-over — keep|remove|investigate
    </step>
    <step>
      Pre-commit gate is doc-only — no .py/.tf in this TO; safe-commit.sh standard
      doc commit. Path: docs/architecture/ADVI_FIRMSEP_PHASE0_AUDIT.md.
    </step>
    <step>
      Owned-paths note: docs/architecture/ADVI_FIRMSEP_* may need a CLOUD_OPS_OR_ETL
      lane exception in .owned-paths.yaml (mirror INFETL_* + INFLEC_* precedent).
      If safe-commit.sh blocks, add the lane in same commit. Coordinate with primary
      AE 0.7 ~A if any conflict.
    </step>
    <step>
      git push origin CLOUD. RAVC0 to COO with audit doc commit hash + summary
      verdict (FIRMSEP.06 GO or N/A).
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-routes trace public-data-router — confirm routing logic + firm awareness</tool>
    <tool>comp-blast opal-data-portal-v2-json — reverse cover (who reads from it)</tool>
    <tool>aws cloudfront get-cache-policy for both policy IDs — empirical composition</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">docs/architecture/ADVI_FIRMSEP_PHASE0_AUDIT.md committed + pushed CLOUD</criterion>
    <criterion id="AC2">Each opal-data-portal-v2-json top-level prefix classified firm-specific|firm-agnostic with rationale</criterion>
    <criterion id="AC3">Both cache policy compositions documented (query/header/cookie whitelists)</criterion>
    <criterion id="AC4">tier-router-edge association status reconciled (live|dead|console-wired)</criterion>
    <criterion id="AC5">Explicit FIRMSEP.06 verdict line: "GO — fix cache-key partition for [path patterns]" OR "N/A — opal-data-portal-v2-json is firm-agnostic"</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent, ships first.</upstream>
    <downstream>FIRMSEP.06 conditional fire (GO|N/A). FIRMSEP Phase 1 TOs (.01-.05) ship in parallel — not gated on .00.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:50Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Andrew direct routing to AE 0.7~B (fresh session). Phase 0 ships first; Phase 1 TOs (.01-.05) arrive in parallel batch — author your sequence based on bandwidth. Phase 0 audit is the gate for FIRMSEP.06 only; the rest are independent.</message>
  </go_signal>
</task_order>
