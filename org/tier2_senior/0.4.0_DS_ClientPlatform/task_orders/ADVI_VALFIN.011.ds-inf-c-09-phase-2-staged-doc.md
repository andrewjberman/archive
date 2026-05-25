<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-23-valfin-011-inf-c-09-phase-2-staged-doc</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <re_routed_from>0.4.0_DS_ClientPlatform (base)</re_routed_from>
    <re_routed_at>2026-05-23T19:15Z UTC</re_routed_at>
    <re_routed_reason>Bundled re-route with sibling ADVI_VALFIN.010 per CTO toolkit option (c) -- DS~C lane re-routing via COO lane-routing-hub authority. Both .010 + .011 close LD-0018 findings (F1 + F2 respectively); siblings naturally pair in re-route. Original TO content + ACs + scope + not_authorized UNCHANGED -- only the recipient lane changes. Pick-up timing: "after current DEMOV1.004 attempt-9 completes; not blocking your current work."</re_routed_reason>
    <date>2026-05-23</date>
    <status>parked-per-ld-0018-f2-b-option-a</status>
    <closeout>Disposition amended 2026-05-25 by ws COO 2.0.0_SA_COO per Option α adoption of LD-0018 F2 (b) "park INF_C_09" option, triggered by VALFIN.012 PHASE A M-1 EMPIRICAL PRE-CHECK fee-independent verdict (DS~E session log commit 896eb8d7d). Original disposition framing (PHASE-2-STAGED doc per LD-0018 F2 (c)) is structurally superseded — the empirical pre-check that PHASE-2-STAGED would have enabled has been executed AND returned fee-independent, so the staging is not a deferred decision but rather a parked-permanently decision. INF_C_09 fee_status_audit historical aggregation gold script continues firing in production (no risk) but has zero downstream consumers wired AND zero structurally wanted. VALFIN.011 doc-only TO substantively obsolete under Path C.1; closure record preserves the audit trail for future Path C.2 reopening if Andrew sovereign rules differently (park is reversible per LD-0018 F2 design). MSTR Option α concur per ACK-COMPREHENSIVE 20260525T064xZ; CVO awareness CC. DS~C original issued_to retained as historical record; disposition amendment is ws COO authoring (POD4_OR_EXEC + ANY_EXEC lane permits).</closeout>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_VALFIN</project_code>
    <priority>P3 -- doc-only; preserves option-value of the Brief B #2 backfill rule while making the orphan-publisher status explicit for future-readers.</priority>
    <sla>~30 min wall (docstring edit + doc-of-record write + safe-commit + RAVC2).</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-23T17:34Z UTC. CTO LD-0018 F2
         architectural ruling: (c) PHASE-2-STAGED -- preserves option-value at
         trivial daily-compute cost + structurally fixes the framing problem
         (orphan code -> intentional Phase-2 staging). Sibling to ADVI_VALFIN.010
         (F1 placeholder-zero filter fix); both close LD-0018 findings, F1 + F2
         respectively. -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1)</prd>
    <cvo_verdict>org/tier1_exec/3.0.0_SA_CVO/logs/2026-05-23/cvo_loop_1530Z_LD0018_fee_imputation_verdict.md (commit 5cdd5fa7e) -- F2 finding section</cvo_verdict>
    <cto_ruling>CTO MCP 2026-05-23T17:24Z UTC -- (c) PHASE-2-STAGED selected over (a) wire-consumer + (b) park-publisher per v1.6 heuristic (reversible/cheapest/most-information-producing)</cto_ruling>
    <sibling_to>org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_VALFIN.010.ds-inf-c-09-placeholder-zero-filter-fix.md (F1 filter fix; ships independent of this TO)</sibling_to>
    <source_file>data/orion/scripts/gold/INF_C_09.fee_status_audit.py (the publisher to be doc'd)</source_file>
    <brief_b_source>2026-05-12 DS authorship per RD Brief B #2+#3 (the originating intent for the imputation rule)</brief_b_source>
  </references>

  <objective>
    Land a PHASE-2-STAGED disposition for INF_C_09 (the fee_status_audit publisher) per CTO LD-0018 F2 ruling. Two doc-only surfaces: (A) module-top docstring block on the producer script + (B) a doc-of-record in docs/briefs/ capturing the LD-0018 F2 resolution + the (a) wire-consumer Andrew-deferred product question. End-state: future-CTO/CVO reading INF_C_09 sees "intentional Phase-2 staging" instead of "orphan code class"; LD-0018 closes once F1 (sibling .010) + F2 (this) both ship + CVO ratifies.
  </objective>

  <context>
    CVO LD-0018 verify-channel verdict YELLOW (commit 5cdd5fa7e) found:
      - F1: placeholder-zero filter at INF_C_09.py:138-144 (61% accounts wrong first_known_fee_status_date). Chartered to DS as ADVI_VALFIN.010 (sibling; ships independent of this TO).
      - F2: ZERO downstream consumers wire the Brief B #2 backfill rule. The publisher runs daily; the methodology is published but never consumed.

    CTO architectural ruling 2026-05-23T17:24Z UTC: (c) PHASE-2-STAGED. Reasoning:
      - (a) WIRE A CONSUMER: product-strategy = Andrew authority (separately surfaced; not in this TO's scope).
      - (b) PARK PUBLISHER: destroys option-value; the Brief B #2 backfill rule was authored intentionally (2026-05-12 per DS for RD Brief B #2+#3); parking deletes the work.
      - (c) PHASE-2-STAGED: preserves option-value at trivial daily-compute cost + structurally fixes the framing problem -- the "orphan code class" framing IS the F2 finding's trigger; (c) converts to "intentional Phase-2 staging."

    The (a) wire-consumer product question stays deferred pending Andrew product call (Lambda billing aggregator OR FE historical reporting). CTO surfaces (a) to Andrew separately.
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- module-top docstring block on `data/orion/scripts/gold/INF_C_09.fee_status_audit.py`.

        Add (or extend existing module docstring) with a "PHASE-2-STAGED" block. Suggested text:

        ```
        # ============================================================
        # PHASE-2-STAGED (LD-0018 F2 CTO ruling 2026-05-23T17:24Z UTC)
        # ============================================================
        # This script implements the "Brief B #2 backfill rule" for
        # fee-status history (authored 2026-05-12 per DS for RD Brief
        # B #2+#3). The rule is intentionally PUBLISHED but currently
        # has ZERO downstream consumers (LD-0018 F2 finding, CVO
        # verdict 5cdd5fa7e).
        #
        # STATUS: Phase-2-staged pending Andrew product-strategy call
        # on consumer wiring -- either (a) Lambda billing aggregator
        # or (b) FE historical reporting. Neither is in current scope.
        #
        # Do NOT delete this publisher; the option-value of the
        # backfill methodology is preserved by daily emission. The
        # daily compute cost is trivial.
        # ============================================================
        ```

        Final wording at DS discretion; intent: (1) cite LD-0018 F2 + CTO ruling, (2) cite the originating intent (2026-05-12 DS / RD Brief B #2+#3), (3) cite the deferred (a) product question, (4) prohibit casual deletion.

      DELIVERABLE B -- doc-of-record at `docs/briefs/advi-valfin-011-fee-status-audit-phase-2-stage-20260523.md`.

        Short brief (~50-100 lines) capturing:
          - Why F2 was a finding (orphan-publisher pattern; CVO grep evidence).
          - CTO's three options (a/b/c) + the (a/b/c) trade-off reasoning.
          - CTO's ruling: (c) PHASE-2-STAGED per v1.6 heuristic.
          - The deferred (a) Andrew product question (Lambda billing aggregator vs FE historical reporting; either is a future project).
          - The (b) park-publisher option remains available IF the rule is later deprecated; (c) doesn't preclude (b) -- it just makes (b) an explicit-decision instead of an accidental-orphan-cleanup.
          - Cross-reference to .010 (F1 filter fix sibling) + the LD-0018 verdict file + the CTO ruling MCP.

      DELIVERABLE C -- safe-commit cycle + RAVC2 to COO + CC CVO.
    </in_scope>
    <out_of_scope>
      - The F1 placeholder-zero filter fix at INF_C_09.py:138-144 -- that's sibling TO ADVI_VALFIN.010.
      - Wiring a consumer (Lambda billing aggregator or FE historical reporting) -- deferred Andrew product call.
      - Parking the publisher (option b) -- explicitly preserved as latent option but NOT exercised in this TO.
      - Any logic change to INF_C_09 -- doc-only.
      - Touching INF_A_02 deprecation (separate cleanup if pursued).
      - Touching dispatch catalog or boot-script -- the publisher continues daily emission per (c).
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform.
    No cross-lane coord needed -- INF_C_09 + docs/briefs/* are both in DS-permissible owned-paths.
    CC CVO on the RAVC2 -- they're tracking LD-0018 closure; once F1 (.010) + F2 (this) both ship, CVO ratifies LD-0018 closed.
    CTO ruling is the authoritative source for the (c) decision; cite in the brief.
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>(read CVO LD-0018 verdict + CTO ruling MCP first)</run>
        <expect>Have CTO's (c) reasoning + CVO's F2 grep evidence in hand before writing the brief.</expect>
        <if_mismatch>STOP. The brief MUST cite the CTO reasoning verbatim/near-verbatim to be a faithful record.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_09.fee_status_audit.py docs/briefs/advi-valfin-011-fee-status-audit-phase-2-stage-20260523.md</run>
        <expect>Exit 0 -- py_compile clean on script (no logic change); brief is markdown so passes.</expect>
        <if_mismatch>STOP. Investigate gate failure (likely a syntax issue in the docstring block).</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>git log --oneline -1 -- data/orion/scripts/gold/INF_C_09.fee_status_audit.py + diff INF_C_09 stat</run>
        <expect>Single-file diff on docstring-only change; line count ~+15-25 (the block); zero logic-line modifications.</expect>
        <if_mismatch>STOP. Scope-creep guard -- if logic changed, this TO scope was violated.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">INF_C_09.fee_status_audit.py module-top docstring carries the PHASE-2-STAGED block citing: LD-0018 F2 + CTO ruling timestamp + Brief B #2 originating intent + deferred (a) product question + do-not-delete clause.</ac>
    <ac id="AC2">docs/briefs/advi-valfin-011-fee-status-audit-phase-2-stage-20260523.md exists, captures the F2 finding + CTO (a/b/c) trade-off + (c) ruling + deferred (a) Andrew product question + cross-refs to .010 sibling + LD-0018 verdict + CTO ruling MCP.</ac>
    <ac id="AC3">Zero logic change in INF_C_09 -- diff stat shows only docstring lines modified.</ac>
    <ac id="AC4">ds-commit-gate clean; safe-commit cycle clean.</ac>
    <ac id="AC5">Session log Compiler Tools section reproduces every &lt;run&gt; with observed output + pass/fail vs. &lt;expect&gt;.</ac>
    <ac id="AC6">RAVC2 to COO + CC CVO with all evidence; closes F2 portion of LD-0018. CVO can now ratify LD-0018 closed once .010 (F1) + .011 (F2) both ship.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Any logic change in INF_C_09 (scope guard; pure doc).
    - Parking the publisher (b) -- (c) explicitly preserves daily emission.
    - Building a consumer (a) -- product-strategy = Andrew authority, not this TO.
    - Touching INF_A_02 deprecation, dispatch catalog, or boot-script.
    - Acceptance flex on AC3 (zero-logic-change) -- empirical guard against scope-creep.
  </not_authorized>
</task_order>
