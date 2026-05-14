<task_order>
  <metadata>
    <id>ADVI_INFFIN.015</id>
    <slug>dsc-581k-orphan-aggregation-investigation</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-14</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED 2026-05-14 by COO per Andrew direct promote via CTO MCP 17:30Z. Investigation starts immediately on CTO's parallel MCP framing; this TO ratifies + adds compiler mandate + structured acceptance criteria.</dispatch_unblock_condition>
    <project_code>ADVI_INFFIN</project_code>
    <priority>P1 — Andrew direct promote 2026-05-14 PM (was P3 data-integrity tech debt; promoted to P1 investigation independent of FE consumer presence)</priority>
    <sla>~1-2h wall investigation (CTO sizing)</sla>
  </metadata>

  <references>
    <ref type="empirical_anchor">DS~A Phase 1.1 RAVC2 17:08Z — 14-artifact sweep finding `s3://opal-data-inf/platinum/firm/nmec_nmnc_nna.json#total.total_aua = $202,602,212.50` vs 13 other platinum/firm/*.json canonical $203,183,160.52 = $580,948.02 gap</ref>
    <ref type="root_cause_pointer">INF_D_08.nmec_nmnc_nna.py:259-272 — `hh["aua"].sum()` builds INF_D_08-local household aggregation; likely upstream filtered join drops $581K of firm AUA</ref>
    <ref type="consumer_path_verify">DE 0.4 grep 17:13Z + 17:19Z — `grep -rn "nmec_nmnc_nna" portal/src/` ZERO matches (no FE consumer); orphan emit from FE perspective</ref>
    <ref type="repo_wide_consumer_grep">DS~A 17:25Z pre-touch grep — ZERO runtime consumers in `infra/`, `.tools/`, `data/`, `portal/`; 8 doc references in `docs/architecture/` + `docs/briefs/` (non-runtime)</ref>
    <ref type="andrew_direct">2026-05-14 PM via CTO: "we need to figure out who that 581k belongs to and why its not being rolled up. Task DS~C with it."</ref>
    <ref type="routing_rationale">CTO MCP 17:30Z — orphan-emit class is structurally distinct from wire-protocol-divergence class. Symptom-routing → grep-first (orphan drops to P3). Data-correctness routing → independent; orphan can be P1 if Andrew/CTO wants divergence resolved. Andrew exercised override authority.</ref>
    <ref type="related_recipe">COO MCP 17:19Z — Option B' (canonical-source `total_aua` + add explicit `unclassified_aua` field) recommended; Option C (drop `total_aua`) acceptable alternative. DS~A locked Option B' for opportunistic touch but downgraded to P3 (now superseded by P1 promote).</ref>
  </references>

  <context>
    The `nmec_nmnc_nna.json` artifact emits firm-level NMNC/NMEC/Existing AUA bucket aggregates + a `total.total_aua` field. The `total.total_aua` value diverges from firm canonical (`header_metrics.json#total.aua` + 12 other firm-emit paths) by $580,948.02 — the buckets sum to $202.6M while canonical reads $203.2M. The gap represents firm-AUA that the NMNC/NMEC/Existing classification logic at `INF_D_08.nmec_nmnc_nna.py` does not assign to any of the three buckets.

    Andrew direct promote framing: this is firm-level money that is uncategorized in the bucket model. The investigation should answer: which households/accounts/positions sum to $581K? Why are they excluded from NMNC + NMEC + Existing? Is the firm canonical wrong (should be $202.6M) or is the bucket aggregation wrong (should sum to $203.2M)?

    Per CTO routing observation: orphan-emit ≠ auto-P3. Data-correctness questions can be P1 independent of FE consumer presence. The grep-first discipline routes symptom-source-of-record questions; it does NOT route data-correctness questions.

    Investigation deliverable is RAVC2 with 3-question answers + recommendation. NOT shipping a fix yet. Fix authorization gates on recommendation + COO/CTO/Andrew ratify.
  </context>

  <objective>
    Produce evidence-bearing RAVC2 answering three questions:
    1. **WHO does the $581K belong to?** Account-grain identification: which households / accounts / positions sum to ~$580,948 in firm AUA but are not classified into NMNC, NMEC, or Existing buckets at `INF_D_08.nmec_nmnc_nna.py:259-272`?
    2. **WHY are they not being rolled up?** Empirical diff between the firm canonical aggregator (used by `INF_D_00c.portal_leaderboard.py` / `INF_D_00d` / etc. emitting $203.2M) and the INF_D_08-local `hh["aua"].sum()` aggregator emitting $202.6M. What filter / groupby / join condition / upstream column drops the $581K?
    3. **WHICH IS CORRECT?** Should the firm canonical be reduced to $202.6M (i.e., INF_D_08 bucket logic is correct + canonical over-counts), should the bucket aggregation be expanded to $203.2M (INF_D_08 logic misses), or is the divergence semantic (e.g., NMNC/NMEC/Existing classifications are by design definitionally non-exhaustive)?
  </objective>

  <scope>
    <files>
      <file action="readonly_investigate">data/orion/scripts/gold/INF_D_08.nmec_nmnc_nna.py — primary investigation surface (line 259-272 aggregation logic; trace upstream `hh` construction)</file>
      <file action="readonly_investigate">data/orion/scripts/gold/INF_D_00c.portal_leaderboard.py — comparison aggregator (emits canonical $203.2M)</file>
      <file action="readonly_investigate">data/orion/scripts/gold/INF_D_00d* — additional canonical-aggregator emitters</file>
      <file action="readonly_investigate">data/orion/scripts/silver/* — silver tier inputs feeding both aggregators (account list / household list / position list)</file>
      <file action="readonly_investigate">s3://opal-data-inf/platinum/firm/nmec_nmnc_nna.json + header_metrics.json + leaderboard.json + dashboard.json — empirical pull for cross-emit reconciliation</file>
      <file action="readonly_investigate">s3://opal-data-inf/silver/* — silver-tier empirical for upstream aggregation input</file>
      <file action="no_modify">No code changes in this TO. Investigation only.</file>
    </files>
  </scope>

  <phase id="1" when="before investigation start">
    <step>
      <run>comp-pipescript io INF_D_08.nmec_nmnc_nna</run>
      <expect>Surface column gaps (columns accessed but not loaded), upstream silver dependencies, portal consumers (zero per DE 0.4 grep). Confirm `hh` dataframe upstream sourcing.</expect>
      <if_mismatch>If comp-pipescript surfaces unexpected dependencies, document in RAVC2 §1.</if_mismatch>
    </step>
    <step>
      <run>comp-blast INF_D_08.nmec_nmnc_nna</run>
      <expect>Blast radius surface — what downstream artifacts read from this script. Should confirm orphan-emit status (no downstream consumers in portal; possibly downstream emit consumers in other gold scripts to verify).</expect>
      <if_mismatch>If blast surfaces non-zero downstream gold-script consumers, surface as cross-emit risk for fix authorization framing.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript io INF_D_00c.portal_leaderboard</run>
      <expect>Surface the canonical aggregator's upstream silver dependencies. Compare against INF_D_08 dependency surface — divergent upstream silver sourcing is likely root cause.</expect>
    </step>
  </phase>

  <phase id="2" when="during investigation">
    <step>
      <run>S3 empirical pull: aws s3 cp s3://opal-data-inf/platinum/firm/nmec_nmnc_nna.json - | jq '.' + aws s3 cp s3://opal-data-inf/platinum/firm/header_metrics.json - | jq '.total.aua' + aws s3 cp s3://opal-data-inf/platinum/firm/leaderboard.json - | jq '[.entries[] | select(.granularity == "ytd") | .total_aua] | add'</run>
      <expect>$202,602,212.50 from nmec_nmnc_nna.json + $203,183,160.52 from header_metrics + $203,183,160.52 from leaderboard YTD sum. Three-way confirmation of canonical vs divergent.</expect>
      <if_mismatch>Document drift; chain may have re-fired between probe and this pull.</if_mismatch>
    </step>
    <step>
      <run>Trace upstream — silver-tier read at INF_D_08 line ~X (whatever feeds `hh`): which silver table? Which households are dropped? Cross-reference against INF_D_00c silver read.</run>
      <expect>Identify a filter / groupby / join condition that produces the $581K delta. Candidate causes: (a) households missing `rep_id` mapping; (b) households missing from `accounts_v2` snapshot; (c) households not in `bucket_classification` derive step; (d) accounts with `is_closed=true` filter; (e) date-window cutoff mismatch.</expect>
      <if_mismatch>If no single condition produces $581K, multiple smaller filters may combine — enumerate top-N households contributing to the gap (account-grain probe).</if_mismatch>
    </step>
    <step>
      <run>Account-grain probe: identify the ~N households (likely a small set) that account for $581K AUA but appear in firm canonical aggregator + NOT in INF_D_08 `hh`. Hash-or-pseudonymize per PII discipline before logging in RAVC2.</run>
      <expect>Concrete WHO list — household IDs (pseudonymized) + AUA per household + per-household reason they're filtered upstream of INF_D_08.</expect>
    </step>
  </phase>

  <phase id="3" when="before RAVC2 close">
    <step>
      <run>comp-validate INF_D_08.nmec_nmnc_nna --artifact /tmp/nmec_nmnc_nna_post_investigation.json (if applicable — investigation does NOT ship a fix; this step skipped unless investigation surfaces a sentinel definition)</run>
      <expect>If applicable, comp-validate surfaces any regression-sentinel violations on the current emit. If investigation surfaces a new sentinel candidate (e.g., "total_aua must match header_metrics.total.aua within $1K"), propose for `gold_validate_config.yaml` add.</expect>
      <if_mismatch>Document in RAVC2 §5 for fix-TO scope.</if_mismatch>
    </step>
    <step>
      <run>Author RAVC2 with 3-question answers + recommendation + sentinel-candidate proposals</run>
      <expect>Single MCP to COO + CC CTO covering all 3 questions with concrete evidence (script line numbers + S3 paths + account-grain identifications + filter conditions).</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: Question 1 — WHO answered with account-grain identification + per-household AUA breakdown + pseudonymized household IDs (PII discipline)
    AC2: Question 2 — WHY answered with concrete script line + filter/groupby/join condition empirical diff (INF_D_08 vs INF_D_00c upstream sourcing)
    AC3: Question 3 — WHICH answered with recommendation: (a) fix bucket aggregator to capture missing $581K, (b) fix canonical aggregator to exclude over-counted $581K, (c) document divergence as semantic-by-design + add `unclassified_aua` field per Option B'
    AC4: Compiler mandate Phase 1 (3 comp-* runs) executed + outputs documented in RAVC2 §1
    AC5: S3 empirical pull (Phase 2 step 1) documented in RAVC2 §2 with verbatim jq output
    AC6: Sentinel-candidate proposals (if applicable) drafted for `gold_validate_config.yaml` add — non-blocking on this TO; gates on Andrew/CTO ratify
    AC7: NO code changes in this TO. Investigation only. RAVC2 is the deliverable.
    AC8: RAVC2 surfaces to COO + CTO; Andrew ratifies recommendation; fix-TO authoring follows ratify
  </acceptance_criteria>

  <compiler_tools_mandate>Phase 1 + Phase 3 (per phases above).</compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: None — investigation is read-only on S3 + local script files.
    PARALLEL-OK: DS~A continues INFGRO audit work (no INF_D_08 cross-traffic). DS~B continues INF_D_06a cash_drag perf. DS~D continues INFINC.
    NO PORTAL IMPACT: investigation has zero FE consumer surface (confirmed by DE 0.4 grep ZERO).
    FIX AUTHORIZATION GATES: post-investigation, fix-TO authoring gates on AC3 recommendation + Andrew ratify. Either (a) bucket-aggregator fix, (b) canonical-aggregator fix, or (c) Option B' field addition. Sequencing per Andrew/CTO call.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Investigation only. Fix-TO (if any) authored separately post-RAVC2 ratify.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. RAVC2 to COO + CC CTO with 3-question answers + recommendation
    2. Compiler mandate Phase 1 + Phase 3 outputs documented
    3. S3 empirical pull verbatim documented
    4. Account-grain WHO list (pseudonymized)
    5. Script-line WHY identification (empirical diff vs INF_D_00c aggregator)
    6. Sentinel-candidate proposals for gold_validate_config.yaml (non-blocking)
    7. Session log entry under `org/tier2_senior/0.4.0_DS_ClientPlatform/session_logs/DS_C_session4_phase_2_581k_investigation.md` (or appropriate session log slot)
  </deliverables>

  <ravc>DS~C RAVC2 to COO + CTO on AC1-8 PASS. Andrew ratifies recommendation; fix-TO follows.</ravc>

  <notes>
    **Andrew direct promote framing:** "we need to figure out who that 581k belongs to and why its not being rolled up." Investigation, not fix. The recommendation in AC3 is the bridge to fix-TO authoring.

    **Author identity:** `--author="0.4.0_DS_ClientPlatform~C <0.4.0_DS_ClientPlatform~C@opal.agent>"`.

    **PII discipline:** household-grain identification is sensitive. Pseudonymize household IDs in RAVC2 (e.g., `hh_5e7a3b` or first-4-of-hash). Cross-reference internal mapping if needed for fix-TO scoping; do NOT include raw household IDs in RAVC2 body.

    **Investigation orientation:** the gap is small (0.29% of firm AUA) but structurally meaningful (firm-money not classified into a bucket model that purports to be exhaustive). The investigation may surface that the bucket model is definitionally non-exhaustive (e.g., NMNC/NMEC/Existing classifications require certain account characteristics that some legitimate AUA doesn't carry), in which case Option B' (`unclassified_aua` field) becomes the structurally-correct fix. Alternatively, the investigation may surface an upstream filter bug, in which case fix-the-filter is correct.

    **Banking opportunity:** if the investigation surfaces a pattern that generalizes (e.g., "every gold script that builds its own household-aggregation should sentinel-test against canonical firm aggregation"), worth banking as `feedback_gold_aggregator_canonical_sentinel.md` or proposing v0.6 comp-tool candidate.
  </notes>
</task_order>
