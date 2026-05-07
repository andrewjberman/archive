<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.06</id>
    <project>ADVI_FIRMSEP</project>
    <title>CONDITIONAL — cache-key partitioning for /api/general/* (gates on TO-FIRMSEP.00 finding)</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-07</completed_date>
    <completed_by>0.7.0_AE_CloudOps~B</completed_by>
    <disposition>MODE-A — closed N/A. Phase 0 audit (TO-FIRMSEP.00 RAVC1, accepted by COO 2026-05-07T20:05Z) confirms NO FIRE: cache-key partitioning is structurally not the right fix for the surfaced content-layer concern (BD/49F-only aggregates served at /api/general/* would yield N copies of the same blob if firm-keyed; the breach point if any is bucket-content level, not cache-key level). Surfaced concern queued separately as content-layer follow-up — CTO v0.2.2 PRD absorbed Andrew's intentional house-view ruling for json/portfolios/, json/peers/, json/latest/; json/model_portfolios/ flagged for eventual MDPF firm-partition (FIRMSEP.11 placeholder; gated on MDPF page build).</disposition>
    <priority>medium-conditional</priority>
    <estimated_effort>~0.25d documentation (if Phase 0 = NO) | ~0.5d implementation (if Phase 0 = YES)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.5 + §6 Phase 1 + §7 OQ5</ref>
    <ref type="gate">TO-FIRMSEP.00 RAVC1 binary disposition (AC5)</ref>
    <ref type="affected_routes">/api/general/* + /api/general/json-tiered/* (cloudfront-distribution.tf:430-499)</ref>
    <ref type="affected_origin">opal-data-portal-v2-json (multi-tenant)</ref>
    <ref type="affected_policies">Managed-CachingOptimized (658327ea-f89d-4fab-a63d-7e88639e58f6) + json_tiered_5min (3eda5c45-0def-4131-87bc-19a31223c270)</ref>
  </references>

  <context>
    This TO is CONDITIONAL on Phase 0 audit (TO-FIRMSEP.00) finding firm-specific data in
    opal-data-portal-v2-json paths WITHOUT firm partitioning in cache keys. Two modes:

      MODE-A (Phase 0 = NO firm-specific data found): close this TO with the audit doc as
        evidence. Document the negative finding in a brief RAVC. Effort ~0.25d (writing the
        close-out + filing).

      MODE-B (Phase 0 = YES firm-specific data found without partition): execute the
        cache-key partitioning fix. Effort ~0.5d.

    Do NOT start MODE-B before TO-FIRMSEP.00 RAVC1 lands AC5.

    MODE-B implementation shape (if it fires):
      1. Identify which CF behaviors are affected (per Phase 0 audit).
      2. Compose a new cache policy that includes firm in the cache key (mirror
         opal_scoped_advisor_by_firm pattern — query string `firm` + header `X-Firm-Id`).
      3. Associate the new policy with affected behaviors via Terraform.
      4. CF invalidation post-apply (the existing cache may have cross-firm entries).
      5. Smoke test: same /api/general/* path with two different firms returns
         firm-correct payloads.
      6. Tag bump portal-auth.
  </context>

  <scope>
    <step>
      Wait for TO-FIRMSEP.00 RAVC1 with AC5 disposition. Do not start before.
    </step>
    <step>
      MODE-A path (Phase 0 = NO):
        a. Brief RAVC1 to COO: "TO-FIRMSEP.06 closed N/A. Phase 0 audit (link) confirms no
           firm-specific data in opal-data-portal-v2-json without partition."
        b. Update org/projects/ADVI_FIRMSEP.json to mark FIRMSEP.06 status=closed-na with
           Phase 0 doc reference.
        c. Done.
    </step>
    <step>
      MODE-B path (Phase 0 = YES) — full execution:
        a. Author a new cache policy in portal-auth/cloudfront.tf (or wherever the existing
           opal_scoped_advisor_by_firm policy lives) named e.g. opal_general_by_firm.
           Composition: include `firm` query string + `X-Firm-Id` header in cache key.
           default_ttl + max_ttl mirror existing policy on the affected behavior (do NOT shrink).
        b. Update affected CF behaviors (per Phase 0 enumeration) to reference the new policy.
        c. terraform plan — should show: ADD new cache policy, MOD on N behaviors (cache_policy_id
           change). NO other changes. If anything else surfaces → ABORT, RAVC1 with anomaly.
        d. terraform apply during off-peak window.
        e. CF invalidation on affected paths: aws cloudfront create-invalidation
           --distribution-id EVTSA9VEHNZVH --paths "/api/general/*" "/api/general/json-tiered/*"
           (or narrower per Phase 0 enumeration).
        f. Empirical smoke test: same /api/general/* path with firm-A + firm-B JWTs returns
           firm-correct distinct payloads. Verify CW per-cache-policy hit-rate metric (hit
           count goes UP after cache warms).
        g. Tag bump portal-auth-v1.X.Y. Push --follow-tags. record-terraform-deploy.sh.
        h. RAVC2 to COO with plan/apply/invalidation/smoke.
    </step>
  </scope>

  <compiler_mandate>
    <tool>(MODE-B only) terraform plan — ADD 1 cache policy, MOD N behaviors, no other</tool>
    <tool>(MODE-B only) comp-cache collisions post-apply — confirm no key collisions</tool>
    <tool>(MODE-B only) CF invalidation receipt</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">TO-FIRMSEP.00 RAVC1 disposition consumed before any work.</criterion>
    <criterion id="AC2-A">(MODE-A) Brief close-out RAVC1 with Phase 0 doc reference.</criterion>
    <criterion id="AC2-B">(MODE-B) New cache policy authored + applied with firm + X-Firm-Id in cache key.</criterion>
    <criterion id="AC3-B">(MODE-B) CF invalidation completes successfully on affected paths.</criterion>
    <criterion id="AC4-B">(MODE-B) Empirical smoke: firm-A and firm-B JWTs hitting same path return firm-correct distinct payloads.</criterion>
    <criterion id="AC5-B">(MODE-B) Tag bump + push --follow-tags + record-terraform-deploy.sh.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>TO-FIRMSEP.00 RAVC1 with AC5 binary disposition.</upstream>
    <downstream>None.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>CONDITIONAL GO. Wait for TO-FIRMSEP.00 RAVC1. CTO suspicion: MODE-A likely (paths look firm-agnostic). Phase 0 verifies binary.</message>
  </go_signal>
</task_order>
