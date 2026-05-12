<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.007</id>
    <project>ADVI_INFETL</project>
    <title>Portal-route audit — gold vs platinum read matrix for every Inflection-serving API GW + Lambda@Edge function</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>normal</priority>
    <estimated_effort>~0.5d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 6 portal serve), §4.8 (portal route migration), §6 Phase 2 TO-7</ref>
    <ref type="output_target">docs/architecture/INFETL_PORTAL_ROUTE_MATRIX.md (NEW — created by this TO)</ref>
    <ref type="andrew_directive">"ONLY PLATINUM OUTPUTS ARE FED TO PORTAL, PERIOD." — Andrew direct 2026-05-07. Audit identifies which portal endpoints currently violate this contract.</ref>
    <ref type="downstream">TO-8 (gold→platinum read-path migration; multi-tranche, ~5-8d cumulative across 3-5 tranches) is gated on this audit's matrix output. TO-8 cannot be scoped or sequenced without it.</ref>
  </references>

  <context>
    INFETL's Andrew-directed architectural constraint: every Inflection portal API GW
    Lambda + Lambda@Edge function MUST read from platinum/* only. Any read from gold/*
    is a contract violation. This TO produces the AUDIT — the comprehensive matrix of
    every Inflection-serving function and its current read disposition (gold vs platinum).

    Per PRD §2: "Read paths are presumed to mix gold/* and platinum/* — Phase 0 audit
    produces the matrix." Suspected mix; this TO produces the empirical truth.

    Why RD owns this: route auditing is documentation + reverse-coverage work that fits
    RD's scope (Playwright-style verification + structural reads). DS owns code edits;
    this TO is read-only audit.

    Why ships pre-Phase 1: per CTO RAVC2 sequencing — "TO-7 ships pre-Phase-1 — RD can
    produce the matrix THIS afternoon if assigned now. That informs TO-8 tranche scoping
    (i.e., how many endpoints need migration; ~5 tranches estimated)." Audit is a
    standalone artifact; doesn't require any other Phase 1 TO to ship first.
  </context>

  <scope>
    <step>
      Enumerate every Inflection-serving function:
        a. Search infra/aws/lambda/ for any Lambda function whose handler reads from
           opal-data-inf bucket OR is invoked on Inflection-firm routes.
           Suggested patterns: grep for "opal-data-inf" + "inflec" + "inflection" +
           "advisor-intelligence" across infra/aws/lambda/**/*.py
        b. Search infra/aws/lambda/edge/ for Lambda@Edge functions on Inflection
           CloudFront distribution (per memory, distribution ID EVTSA9VEHNZVH).
        c. Cross-check via comp-routes trace inflection-* (compiler tool produces
           full routing graph).
        d. Cross-check API GW resource definitions in infra/aws/terraform/inf-pipeline/
           (or partners-api-pipeline/ if INF routes piggyback on partners-api).
    </step>
    <step>
      For each enumerated function, identify read disposition:
        - gold/* prefix reads (CONTRACT VIOLATION — flag for migration)
        - platinum/* prefix reads (COMPLIANT)
        - bronze/* prefix reads (UNUSUAL — flag for review; portal should never read bronze)
        - silver/* prefix reads (UNUSUAL — flag for review)
      Use grep on the Lambda source: `grep -E "s3://opal-data-inf/(gold|platinum|bronze|silver)" {handler}`
      Note: include wildcard patterns and key prefixes; not just literal paths.
    </step>
    <step>
      For each Lambda, record:
        - function_name (e.g., inflection-firm-data-fetcher)
        - file_path (e.g., infra/aws/lambda/.../lambda_function.py)
        - read_paths: list of S3 prefix patterns
        - portal_routes_served: which API GW paths or Lambda@Edge route patterns invoke this
        - migration_priority: HIGH (firm-level analytics; Andrew's primary concern), MEDIUM (advisor drill), LOW (rarely-invoked)
        - notes: any special concerns (auth gates, cache layers, schema dependencies)
    </step>
    <step>
      Author docs/architecture/INFETL_PORTAL_ROUTE_MATRIX.md with the following structure:

      # INFETL Portal Route Matrix
      **Authored:** {date} by 0.4.2_RD_AdvisorIntelligence (ADVI_INFETL.007)

      ## Executive summary
      - Total Inflection-serving functions: {N}
      - gold-reading (violations): {N1}
      - platinum-reading (compliant): {N2}
      - bronze/silver-reading (anomalies): {N3}

      ## Function inventory

      | function_name | file_path | read_paths | portal_routes_served | migration_priority | notes |

      ## Migration tranche proposal
      Group violations into 3-5 tranches by blast radius (e.g., Tranche 1: Firm overview;
      Tranche 2: Advisor drill; Tranche 3: Client drill).

      ## Risk register
      - Schema parity risks (which gold reads have JSON shape that differs from publisher
        platinum output)
      - Cache invalidation needs (CloudFront paths affected per tranche)
      - Auth dependencies (Lambda@Edge auth-validator-edge interactions)
    </step>
    <step>
      Cross-validate the matrix:
        comp-routes trace inflection-* (full path through to S3 reads)
        comp-blast platinum/firm/* — reverse cover (which functions DEPEND on platinum/firm
        artifacts; cross-check vs the matrix)
        comp-blast platinum/advisors/* — reverse cover for advisor drill functions
    </step>
    <step>
      Commit the matrix doc:
      .tools/safe-commit.sh --author "0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;"
      -m "doc(ADVI_INFETL.007): portal-route audit — gold vs platinum read matrix"
      -- docs/architecture/INFETL_PORTAL_ROUTE_MATRIX.md
      git push origin CLOUD.
    </step>
    <step>
      RAVC to COO: matrix file path + commit hash + summary count of gold-reading
      violations + proposed tranche count for TO-8 + any anomalies discovered.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-routes trace inflection-* — enumerate full paths from API GW → Lambda → S3</tool>
    <tool>comp-blast platinum/firm/* and platinum/advisors/* — reverse coverage check (which functions consume platinum currently; matrix should align)</tool>
    <tool>comp-pii audit — sanity check that no audited function reads cleartext PII directly (related but separate concern)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">docs/architecture/INFETL_PORTAL_ROUTE_MATRIX.md created with executive summary + function inventory table.</criterion>
    <criterion id="AC2">Every Inflection-serving function enumerated with explicit read_paths; no "unknown" entries (use compiler tools to remove ambiguity).</criterion>
    <criterion id="AC3">Each gold-reading violation flagged with migration_priority + tranche assignment.</criterion>
    <criterion id="AC4">Migration tranche proposal includes 3-5 tranches; each tranche bounded by blast radius (3-5 endpoints per tranche per CTO PRD §6 TO-8).</criterion>
    <criterion id="AC5">Risk register includes schema-parity, cache-invalidation, auth-dependency risks for each tranche.</criterion>
    <criterion id="AC6">comp-routes trace evidence cited inline (specific traces for ambiguous functions).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — TO-7 is fully independent and can ship first in Phase 1 sequence.</upstream>
    <downstream>
      TO-8 (multi-tranche read-path migration) is fully gated on this matrix.
      The cron-flip-ack TO (ADVI_INFETL.011) gate (d) requires this audit complete so
      migration risk is known before flipping cron ENABLED.
    </downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      Hidden gold reads via dynamic key construction (e.g., f"gold/{prefix}/{key}")
      that don't show up in literal-string grep. Mitigation: also grep for variable
      names like "GOLD_PREFIX", "S3_PREFIX_GOLD", and trace runtime via CloudWatch
      logs sampled from prior portal traffic.
    </risk>
    <risk>
      Lambda@Edge functions are deployed to us-east-1 only and may have stale source
      vs deployed code (Lambda@Edge has long replication time). Mitigation: comp-routes
      should resolve from deployed code; flag any drift via comp-pipescript deployed.
    </risk>
    <risk>
      Functions outside infra/aws/lambda/ that serve Inflection routes (e.g., partners-api
      pipeline shared functions). Audit must include partners-api-pipeline scope if
      Inflection routes piggyback there.
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. RD can ship the matrix in ~0.5d once unblocked. The matrix output gates TO-8 (which is ~5-8d cumulative migration) and the cron-flip-ack TO. Ships first in Phase 1 sequence per CTO recommendation.</message>
  </go_signal>
</task_order>
