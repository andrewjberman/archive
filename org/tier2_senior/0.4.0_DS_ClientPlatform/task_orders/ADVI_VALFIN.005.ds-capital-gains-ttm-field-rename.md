<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-23-valfin-005-cap-gains-rename</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-05-23</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_VALFIN</project_code>
    <priority>P1 -- LD-0012 CVO YELLOW verdict follow-on; misleading field-name in production-facing portal payload + a senior reader (Andrew) materially mis-read it.</priority>
    <sla>~1d wall (DS half this TO); portal-side type rename as a follow-on once DE pod-4 is re-laned.</sla>
    <!-- GO ON AUTHOR by 2.0.0_SA_COO base 2026-05-23T06:35Z. CVO LD-0012 P1 follow-on
         per spot_check_0453Z_LD0012_capital_gains_verdict.md (commit 1247fa15b).
         DS Base Phase-2 forensic (commit f55ef0dc7) confirmed: computation is correct,
         broadly distributed across 609 accounts, no data defect; FIELD NAME is the
         sole defect. -->
  </metadata>

  <references>
    <prd>docs/architecture/ADVI_PRODUCT_VALIDATION.md (v0.1)</prd>
    <project_json>org/projects/ADVI_VALFIN.json</project_json>
    <cvo_verdict>org/tier1_exec/3.0.0_SA_CVO/logs/2026-05-23/spot_check_0453Z_LD0012_capital_gains_verdict.md (commit 1247fa15b)</cvo_verdict>
    <ds_phase2_forensic>org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-23/session_valfin_001_phase2_methodology_findings.md (commit f55ef0dc7)</ds_phase2_forensic>
    <tier0_ledger>org/tier0/ledger/LD-0012.md (MSTR escalation of Andrew F-005 magnitude-sanity trigger)</tier0_ledger>
  </references>

  <objective>
    Eliminate the misleading field name `capital_gains_ttm` across the gold-script emit + portal consumer chain. The field computes delta UNREALIZED gain over TTM (verified-correct by DS Phase-2 forensic + CVO ratify), not realized capital gains. Rename to `unrealized_gain_change_ttm` to match semantics. End-state: portal payload + types + render carry the truthful name; no senior reader can mis-read it again; backwards-compat shim ensures no production read-break during the transition.
  </objective>

  <context>
    DS surfaced peter_lee `capital_gains_ttm = -$54,807,679` during ADVI_VALFIN.001 Phase-1. Andrew read the raw field name in a session log and reacted to the implied semantic (large realized capital loss); MSTR LD-0012 escalated to CVO; CVO ran /verify-channel + decomposition + spot-checks; verdict YELLOW (computation correct, field-name misleading). DS Phase-2 forensic (this morning, commit f55ef0dc7) closed the magnitude question definitively: 609 peter_lee accounts, broadly distributed delta_unrealized, top contributors are all `ug_end=0` positions (sold-during-TTM converting unrealized -> realized OR market decline to flat), no perf-table bug, no single-account dominance.

    The defect is purely the field name. Portal display was already partially fixed in INFFIN.019 Fix C (the panel does the right thing visually), but the underlying field name persists across:
    - data/orion/scripts/gold/INF_D_02.advisor_client_detail.py (compute fn + dict key + book.json emit)
    - data/orion/scripts/gold/INF_D_00.portal_aggregates.py (firm-scope sister)
    - portal/src/pages/AdvisorIntelligence/_shared/types.ts:934 + :1100
    - portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx:571
    - portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx:839
    - portal adapter layer (where the field flows from API JSON -> typed React state)

    LANE NOTE: DE pod-4 was killed by Andrew/MSTR LD-0014 (separate INFGRO cancellation context). The portal-component type rename half cannot ship until DE 0.4 is re-spawned. This TO carves the work so DS can ship the gold-script half + the adapter shim + the dual-key emit immediately, AND the portal types update lands later as a Phase B once DE is back.

    The shim is the key mechanism: gold emits BOTH `capital_gains_ttm` (deprecated) + `unrealized_gain_change_ttm` (new) into platinum book.json + portal_aggregates JSON. The adapter accepts either. Portal consumers continue reading `capital_gains_ttm` until DE swaps the types. Zero break during transition.
  </context>

  <scope>
    <in_scope>
      PHASE A -- DS-OWNED HALF (this TO; ships immediately):
        1. Rename in data/orion/scripts/gold/INF_D_02.advisor_client_detail.py: compute fn + internal dict key. The book.json EMIT writes BOTH keys (old + new) with identical values during the transition window.
        2. Rename in data/orion/scripts/gold/INF_D_00.portal_aggregates.py (firm-scope sister) -- same dual-emit pattern.
        3. The dual-emit guarantees portal continues reading the old key while DE catches up. No production read-break.
        4. Update any cross-references in the same gold scripts (docstrings, log messages, comments) for clarity.
        5. Commit + safe-deploy cycle per CLAUDE.md Rule 13. Tag verification: deployed-script matches committed-ref.
        6. Document in session log: the dual-emit pattern + the rationale (DE re-spawn dependency) + the shim-removal trigger (Phase B once DE swaps consumers).

      PHASE B -- DE-OWNED HALF (separate follow-on TO; gated on DE pod-4 re-spawn):
        1. portal/src/pages/AdvisorIntelligence/_shared/types.ts:934 + :1100 -- rename type field.
        2. portal/src/pages/AdvisorIntelligence/_shared/AdvisorBookView.tsx:571 -- swap consumer reference.
        3. portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx:839 -- swap consumer reference.
        4. portal adapter layer -- swap accessor to read the NEW key + drop the old-key fallback.
        5. After Phase B ships + portal deploys: trigger Phase C (gold-script dual-emit collapse to new-key-only).

      PHASE C -- DUAL-EMIT COLLAPSE (gated on Phase B production-deploy verification):
        1. DS removes the old `capital_gains_ttm` key emit from both gold scripts.
        2. Single source of truth post-Phase-C: `unrealized_gain_change_ttm`.
        3. Phase C ship documented in the brief as the structural-rename close.

      DELIVERABLES (this TO covers Phase A only; Phases B + C bank as follow-on TOs):
        - INF_D_02.advisor_client_detail.py edited + committed + deployed.
        - INF_D_00.portal_aggregates.py edited + committed + deployed.
        - Sentinel verify: opal-data-inf/platinum/{advisor_id}/book.json carries BOTH keys with identical values; spot-check on peter_lee book.json + 2 other advisors.
        - Session log + brief entry describing the dual-emit pattern + Phase B/C plan.
        - RAVC2 to COO with all evidence.
    </in_scope>
    <out_of_scope>
      - The Phase B portal type rename (separate TO when DE re-spawns).
      - The Phase C dual-emit collapse (gated on Phase B).
      - Any computation logic change to capital_gains_ttm / unrealized_gain_change_ttm -- the value is correct + verified-correct; this TO is purely cosmetic (field rename).
      - Any other field rename in the same files (scope-creep guard; the F-005 surface is this one field).
      - The portal display change (INFFIN.019 Fix C already shipped the right visual; no further FE display work in this TO).
    </out_of_scope>
  </scope>

  <cross_domain_coordination>
    Lead: 0.4.0_DS_ClientPlatform (DS pod-4 base; this TO is DS-only for Phase A).
    Co-owner Phase B/C: 0.4.0_DE_ClientPlatform (currently KILLED by MSTR LD-0014; awaiting re-spawn).
    NO INFGRO coordination (separate lane, recently cancelled).
    The dual-emit shim eliminates a hard cross-domain dependency for Phase A.
    CC CVO on the RAVC2 -- they ratified the YELLOW verdict + flagged this TO.
  </cross_domain_coordination>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io INF_D_02</run>
        <expect>READS includes silver/api_dims/tax_realized + tax_unrealized + accounts_dimension + platinum/advisors/{id}/book.json upstream chain. WRITES platinum/advisors/{id}/book.json. No COLUMN GAPS for capital_gains_ttm.</expect>
        <if_mismatch>STOP. If a COLUMN GAP surfaces on capital_gains_ttm, the field is computed from data the script doesn't load -- diagnose before the rename.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse capital_gains_ttm</run>
        <expect>Portal consumers enumerated: AdvisorBookView.tsx:571 + ClientsTab.tsx:839 + types.ts:934 + :1100 (per CVO verdict file). No surprise consumers.</expect>
        <if_mismatch>STOP. If a 6th consumer surfaces, scope-correction needed before write.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>.tools/ds-commit-gate.sh INF_D_02.advisor_client_detail.py INF_D_00.portal_aggregates.py</run>
        <expect>Exit 0. py_compile + AST undefined-name scanner + ruff all PASS.</expect>
        <if_mismatch>STOP. Do not commit if gate fails.</if_mismatch>
      </step>
      <step>
        <run>git diff --stat</run>
        <expect>Two files modified (INF_D_02 + INF_D_00). Diff lines limited to the rename + dual-emit logic (no scope-creep). Sentinel string `unrealized_gain_change_ttm` appears in BOTH files; sentinel string `capital_gains_ttm` ALSO still appears in BOTH files (the dual-emit deprecated key).</expect>
        <if_mismatch>STOP. Scope-creep or missing dual-emit key. Re-scope before commit.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>.tools/safe-deploy.sh (deploy cycle per CLAUDE.md Rule 13: push -> S3 upload -> comp-pipescript deployed MATCH -> SSM dispatch)</run>
        <expect>Cycle exits 0. comp-pipescript deployed INF_D_02 + INF_D_00 = MATCH.</expect>
        <if_mismatch>STOP. Investigate deployed-vs-committed drift before signaling AE.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-inf/platinum/advisors/peter_lee/book.json /tmp/peter_lee_post_rename.json + jq '.tax_exposure'</run>
        <expect>BOTH keys present: `capital_gains_ttm` AND `unrealized_gain_change_ttm`, identical values. Sentinel check on 2 other advisors as well.</expect>
        <if_mismatch>STOP. Dual-emit not landing -- investigate before declaring Phase A done.</if_mismatch>
      </step>
      <step>
        <run>comp-blast capital_gains_ttm</run>
        <expect>Same 5 consumers as Phase 1 (no new consumers added during the write window).</expect>
        <if_mismatch>Surface to COO. Likely indicates another agent introduced a new consumer mid-flight.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <acceptance_criteria>
    <ac id="AC1">INF_D_02.advisor_client_detail.py emits BOTH `capital_gains_ttm` (deprecated) + `unrealized_gain_change_ttm` (new) with identical values in the tax_exposure block.</ac>
    <ac id="AC2">INF_D_00.portal_aggregates.py emits BOTH keys at the firm-scope sister path with identical values.</ac>
    <ac id="AC3">Sentinel verify: peter_lee book.json (+ 2 other advisors) carry both keys with matching numerics after deploy.</ac>
    <ac id="AC4">Computation logic UNCHANGED (the value is correct; this TO is cosmetic rename only). Pre/post-deploy snapshot of peter_lee `capital_gains_ttm` should match within rounding.</ac>
    <ac id="AC5">Deploy cycle clean: comp-pipescript deployed = MATCH on both scripts; tag bumped if applicable.</ac>
    <ac id="AC6">Session log includes Compiler Tools section reproducing every &lt;run&gt; with observed output + pass/fail vs. &lt;expect&gt;.</ac>
    <ac id="AC7">Brief entry documents: the dual-emit pattern + the Phase B/C follow-on plan + the shim-removal trigger.</ac>
    <ac id="AC8">RAVC2 to COO + CC CVO with all 7 ACs evidence + the sentinel check output.</ac>
  </acceptance_criteria>

  <not_authorized>
    - Changing the computation logic (the value is correct).
    - Renaming any field OTHER than `capital_gains_ttm` (scope-creep guard).
    - Removing the old key in this TO (the dual-emit is the shim; collapse is Phase C, gated on DE Phase B).
    - Touching the portal types/components in this TO (Phase B is DE lane; LD-0014 killed DE pod-4; await re-spawn).
    - Cutting acceptance flex on AC3 (the sentinel-verify) -- the dual-emit must be empirically confirmed in platinum book.json, not asserted from script edit alone.
    - Acceptance flex on AC4 (computation-unchanged) -- the value MUST be identical pre/post-deploy or this is a regression, not a rename.
  </not_authorized>
</task_order>
