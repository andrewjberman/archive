<task_order>
  <metadata>
    <id>ADVI_VALFIN.001</id>
    <slug>ds-books-tab-validation-spearhead</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <co_owner>0.4.0_DE_ClientPlatform -- owns the portal-consumer-confirm half (Phase 3 comp-platinum reverse + sanity that the books-tab component renders against the corrected gold artifact). 0.4.0_DS leads the gold-side validation + corrections. Full visual FE-display verification is TO-6 (cross-cutting), not this TO.</co_owner>
    <date>2026-05-22</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <!-- GO ON PICKUP 2026-05-22. COO holds full authority for the remainder of this session (Andrew directive 2026-05-22; CTO + MSTR sessions down). ADVI_VALFIN PRD v0.1 just landed; TO-1 is the spearhead per priority order TO-1 -> TO-2 -> TO-3. -->
    <project_code>ADVI_VALFIN</project_code>
    <priority>P1 -- THE SPEARHEAD. The Inflection books/ tab cost-basis cluster is the lowest-confidence surface in the ADVI product per PRD section 2. First and deepest validation pass. Findings either correct in-place or route to the active ADVI lane that owns the surface.</priority>
    <sla>3-5 days wall, multi-agent. 9 gold scripts + the books-tab portal surface. The 3-layer method per PRD section 3 -- verify-channel data, meta-analysis correctness, portal-consumer confirm -- applied per surface.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1) -- section 6 TO-1 + section 3 method + section 5.3 (the comp-graph does not model gold write edges; empirical aws s3 ls is the substitute).</prd>
    <project_json>org/projects/ADVI_VALFIN.json</project_json>
    <coordinates_with>
      <p>ADVI_INFGRO (active) -- the GRO decomposition + advisor-book-growth overlap. INF_C_07 / INF_C_08 / INF_D_00c book-growth rollups live in INFGRO's blast radius. MCP COO + INFGRO lane BEFORE editing those three.</p>
      <p>ADVI_INFETL (active) -- daily ETL. INF_B_* (holdings/lots) sit downstream of INFETL's silver/bronze stage. MCP COO + INFETL lane BEFORE editing if a finding lands on the upstream feed (vs the INF_B gold transform itself).</p>
      <p>ADVI_INFLEC / ADVI_INFFIN / ADVI_INFINC / ADVI_DWSPLT / ADVI_SHARED (all complete) -- past corrections inform context; findings against their already-closed surfaces go into THIS brief as a documented regression, not as a reopen of their projects, unless a real defect is discovered (then RAVC re-open via COO).</p>
    </coordinates_with>
  </references>

  <context>
    The ADVI product is built and visually finished, but its numbers and methodology have not been validated end-to-end. The books/ tab cost-basis cluster -- cost basis, tax lots, realized capital gains, unrealized capital gains, and advisor book growth -- is the lowest-confidence surface. TO-1 is the spearhead: validate every key number on the books tab, confirm methodology, and CORRECT what validation finds.

    Validation is NOT completion -- corrections close the loop. A finding is triaged: in-place fix (gold/silver/bronze edit, this lane), or route to the active ADVI project that owns the surface (INFGRO / INFETL), or surface to COO if the defect spans projects.
  </context>

  <scope>
    <in_scope>
      Nine gold scripts + their portal renders:
      - INF_B_00 canonical_holdings
      - INF_B_01 holdings_lots
      - INF_B_01b classify_new_securities
      - INF_B_02 canonical_lots
      - INF_B_03 account_gains
      - INF_C_05 client_tax_liability
      - INF_C_07 advisor_attribution (book-growth rollup -- INFGRO-coordinated)
      - INF_C_08 advisor_fee_efficiency (book-growth rollup -- INFGRO-coordinated)
      - INF_D_00c portal_leaderboard (book-growth rollup -- INFGRO-coordinated)

      For each: confirm artifact EXISTS, FRESH, SCALED, NOT-FROZEN on S3 (the verify-channel 4-check); run an independent reasonableness check (per-component series-walk, day-over-day plausibility, sentinel case studies on a known advisor/account); document the methodology (the calc, the inputs, the caveats); confirm the portal books-tab component reads the correct artifact + renders the expected fields.

      For each books-tab number -- cost basis, tax lots, realized gains, unrealized gains, advisor book growth -- the artifact-match + reasonableness + methodology trio must all PASS or the number gets a correction.
    </in_scope>
    <out_of_scope>
      Any non-books-tab surface (performance, NNA/GRO, attribution mix, fee efficiency outside book-growth, dimensions, headers, leaderboard outside the book-growth rollup) -- that is TO-2 (rest-of-Inflection).
      49 Financial -- that is TO-3.
      Visual / UI DESIGN changes (front-end DATA correctness is in scope; front-end DESIGN is not).
      New metrics / cohorts / views.
      Pipeline re-architecture -- corrections only, not redesigns; if a finding warrants structural change it goes to a separate PRD.
      Full visual /frontend-dev verification -- that is TO-6 (cross-cutting). This TO confirms the portal consumer is wired correctly, not that the page passes Playwright visual ACs.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io [each of the 9 scripts] + comp-pipescript feeds + comp-pipescript consumers</run>
        <expect>Per script: producer Lambda + S3 output key identified; READS load list complete (zero COLUMN GAPS); known feeds + consumers enumerated. PORTAL CONSUMERS section names the books-tab component for the books-tab-rendering scripts.</expect>
        <if_mismatch>STOP. A COLUMN GAP = a load-list defect that the validation pass exists to catch. Surface to COO with the gap before any correction work begins. A missing portal consumer means the artifact is orphaned -- candidate for triage (deprecate or wire).</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls each gold-output S3 key + spot-fetch the latest partition with `aws s3 cp ... | head` (or jq-tool a small sample)</run>
        <expect>Artifact EXISTS, FRESH (mtime within the expected daily refresh window -- typically within last 24h on a weekday), SCALED (file size plausible, not a near-empty stub), NOT-FROZEN (latest mtime newer than the prior partition's). Method per PRD section 3 + the /verify-channel skill discipline; producer self-report does NOT substitute.</expect>
        <if_mismatch>The 4-check failure IS the finding. Document the specific failure (EXISTS/FRESH/SCALED/NOT-FROZEN), assess whether it is a TO-5 pipeline-robustness issue (cross-cutting) or a TO-1 in-scope defect; route accordingly.</if_mismatch>
      </step>
      <step>
        <run>comp-blast [each of the 9 scripts]</run>
        <expect>Cross-domain blast intersects only the coordination set: ADVI_INFGRO (for INF_C_07/INF_C_08/INF_D_00c book-growth rollups) and ADVI_INFETL (for INF_B_* upstream feed). Other active ADVI projects (DEMOV1 / ECLDAT / FIRMSEP) should not appear in the blast for these 9 scripts; if they do, that is itself a finding.</expect>
        <if_mismatch>Surface the unanticipated downstream to COO BEFORE corrections so the cross-domain coordination block is updated and the right lane is MCP-coordinated.</if_mismatch>
      </step>
      <step>
        <run>Methodology read of each script's compute + the Yang rubric (docs/reference/yang-original-scripts/YANG_SCRIPTS_RUBRIC.md) cross-ref where applicable</run>
        <expect>The calc + inputs + caveats are explicit and defensible. For each books-tab number, the methodology is documentable in plain English to a reader who has not read the code.</expect>
        <if_mismatch>If methodology is unclear, ambiguous, or carries an undocumented caveat that the UI label does not surface, that is a real finding -- the validation pass exists to catch this exact failure family (audit-completeness vs behavior-correctness, per PRD section 3.2).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit any correction">
      <step>
        <run>comp-blast [the corrected function/script]</run>
        <expect>No NEW downstream nodes appeared during the fix. The blast radius pre-correction == the blast radius post-correction.</expect>
        <if_mismatch>STOP. A new downstream means another agent committed a consumer mid-flight -- surface to COO before committing the correction; resolve the cross-pipeline conflict first.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh [touched files] + .tools/ds-precommit-check.py + ruff check (per CLAUDE.md Rule 14 universal pre-commit gate)</run>
        <expect>All three exit 0. py_compile clean, AST-undefined-name scan clean, ruff clean. PEP-604 syntax on Python 3.9 runners (Rule 15 from __future__ import annotations enforced).</expect>
        <if_mismatch>STOP. Do not commit until the gate is clean.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-validate [each corrected script] --artifact [the rebuilt artifact]</run>
        <expect>Exit 0. All ERROR checks pass. WARN count documented in the session log + the validation brief.</expect>
        <if_mismatch>STOP. Do not signal RAVC2 until exit 0.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse [each books-tab artifact]</run>
        <expect>Portal consumer wired to the corrected artifact; the books-tab component reads the right S3 key + the right fields.</expect>
        <if_mismatch>Surface to TO-6 (FE display verification cross-cutter) -- a portal-side wiring fix or a stale React Query key. Do NOT silently fix in this TO; FE-side corrections coordinate with the Pod 4 DE lane.</if_mismatch>
      </step>
      <step>
        <run>.tools/safe-deploy.sh on every gold-script commit (CLAUDE.md Rule 13 -- atomic commit -> push -> S3 upload -> deployed-MATCH cycle)</run>
        <expect>The cycle completes; deployed runner has the corrected code; SSM dispatch (QA) successful; subsequent gold run consumes the fix.</expect>
        <if_mismatch>The deploy didn't propagate -- gold script edit committed but runner running stale per CLAUDE.md memory (S3-pull dispatchers don't auto-propagate). Re-fire the cycle.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - ADVI_INFGRO (active) -- the book-growth rollups INF_C_07 / INF_C_08 / INF_D_00c are in INFGRO's blast radius. MCP COO + 0.4.0_DS_ClientPlatform (or the INFGRO-lane agent) BEFORE editing those three. A finding against a book-growth surface gets routed to INFGRO unless it is a localized defect this lane can fix without overlapping INFGRO's in-flight work.
    - ADVI_INFETL (active) -- daily ETL. INF_B_* (holdings/lots) sit downstream of INFETL's silver/bronze stage. MCP COO + INFETL lane BEFORE editing if a finding traces to the upstream silver/bronze feed (vs the INF_B gold transform itself).
    - ADVI_INFLEC / ADVI_INFFIN / ADVI_INFINC / ADVI_DWSPLT / ADVI_SHARED (all complete) -- past corrections; findings against their already-closed surfaces document in THIS brief as a regression; reopen the closed project only if a real defect is discovered (RAVC re-open via COO).
    - ADVI_DEMOV1 / ADVI_ECLDAT / ADVI_FIRMSEP -- not in the books-tab blast; no expected overlap.
    - TO-4 (Jan-2021 floor) / TO-5 (pipeline robustness) / TO-6 (FE display) / TO-7 (meta-analysis) -- cross-cutting peer TOs. Route findings to them where their scope is the right home (e.g., a FRESH/NOT-FROZEN failure goes to TO-5; a portal-display defect goes to TO-6; a methodology-judgment finding goes to TO-7).
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">For each books-tab number -- cost basis, tax lots, realized capital gains, unrealized capital gains, advisor book growth -- the value on the page matches the gold artifact value (artifact-match). The match is empirically demonstrated, not inferred (open the page, read the number, fetch the artifact, compare). Mismatches CORRECTED or routed.</ac>
    <ac id="AC2">Each number passes an independent reasonableness check: per-component series-walk + day-over-day plausibility bound + a sentinel-advisor / sentinel-account case study; documented in the brief. Bare identity-reconciliation (Sigma == aggregate) is necessary-not-sufficient per the documented identity-1-masks-class failure mode.</ac>
    <ac id="AC3">Each number's methodology is documented in plain English in the brief: the calc, the inputs, the caveats. If the calc carries a non-obvious caveat the UI label does not surface, the brief flags it (routes to a TO-7 meta-analysis finding or directly to COO if product-judgment-altitude).</ac>
    <ac id="AC4">Every finding (an AC1 / AC2 / AC3 fail) lands one terminal disposition: (a) corrected in-place (gold/silver/bronze fix committed + comp-validate clean + deployed via safe-deploy) and the brief cites the correction commit; OR (b) routed to the right project / lane via MCP coordination + the brief cites the routing message ID. No finding left in "noted" without disposition.</ac>
    <ac id="AC5">ZERO out-of-scope edits -- no non-books-tab surface touched (no TO-2 territory); no visual/UI design change; no pipeline re-architecture; no commit outside the 9 in-scope scripts + their direct call-chain. AC5 verified via .tools/safe-commit.sh's contamination guard on every commit.</ac>
    <ac id="AC6">Session log + validation brief: docs/briefs/advi-valfin-001-inflection-books-tab-validation-YYYYMMDD.md. Compiler Tools section reproduces every <run> from <compiler_tools_mandate> with observed output + pass/fail vs <expect>. RAVC2 to 2.0.0_SA_COO. 3.0.0_SA_CVO is independently validating commits in this scope via its continuous loop -- keep findings citation-grounded.</ac>
  </acceptance_criteria>

  <deliverables>
    - The validation brief (docs/briefs/advi-valfin-001-...md) covering all 9 scripts + 5 books-tab numbers: per-number artifact-match + reasonableness + methodology + finding-disposition.
    - Correction commits for each in-place finding (CLAUDE.md Rule 13 safe-deploy cycle for each gold/silver/bronze edit).
    - MCP coordination messages for findings routed to INFGRO / INFETL / TO-5 / TO-6 / TO-7 / COO.
    - Session log(s) per participating role (DS lead + DE co-owner) with the Compiler Tools section.
    - Joint RAVC2 to 2.0.0_SA_COO (one-sender by agreement between 0.4.0_DS + 0.4.0_DE).
  </deliverables>

  <do_not>
    <rule>Do NOT edit any non-books-tab surface (no TO-2 territory). The PRD's priority order is TO-1 first AND deepest; do not let scope creep dilute the spearhead.</rule>
    <rule>Do NOT make visual / UI DESIGN changes (FE DATA correctness is in scope; FE DESIGN is not). FE display verification beyond consumer-wiring confirm is TO-6.</rule>
    <rule>Do NOT re-architect any pipeline. Corrections only. If a finding warrants structural redesign, surface to COO as a separate-PRD candidate.</rule>
    <rule>Do NOT sweep findings to "documented" without disposition. Every finding lands corrected-or-routed (AC4).</rule>
    <rule>Do NOT touch a book-growth surface (INF_C_07 / INF_C_08 / INF_D_00c) without first MCP-coordinating with COO + the ADVI_INFGRO lane (PRD Appendix D + this TO's cross_domain_coordination block).</rule>
    <rule>Do NOT bypass the CLAUDE.md Rule 13 safe-deploy cycle on any gold-script commit. Committed != deployed.</rule>
    <rule>No emojis in code, logs, or CLI transcripts (ASCII-only, CLAUDE.md "No emojis in code").</rule>
  </do_not>
</task_order>
