<task_order>
  <metadata>
    <id>ADVI_ROLLUP.BDPLNNASCHEMA</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-24</date>
    <status>pending</status><!-- COO override GO 20260506T~1800Z — all 49EXEC gates cleared. Phase 0 audit complete (DS~C). RAVC2 sent. Awaiting COO Phase 1 GO. -->
    <project_code>ADVI_ROLLUP</project_code>
    <priority>P3 — schema-alignment cleanup; low-impact; prevents future silent-wrongness class bugs</priority>
    <origin>
      ADVI_ROLLUP dashboard blocking item (4): "DS BDPL_NNA.S1 schema-alignment TO draft (state vs client_state)". Surfaced during C_08 silent-wrongness recovery (2026-04-17 `9e537f9f`→`cd177553`): D_04 was silent-filling `Unknown` for a missing state-field column due to vocabulary drift between `state` (silver accounts field) and `client_state` (gold emit convention). The swap was fixed for CANONICAL_NNA_PREFIX but analogous `state` vs `client_state` inconsistency exists elsewhere in the gold chain and portal.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (C_08 silent-wrongness section) + BDPL_NNA concept doc if exists</ref>
    <ref type="predecessor">C_08 silent-wrongness fix (`cd177553` CANONICAL_NNA_ATOMIC_PREFIX→CANONICAL_NNA_PREFIX + D_04 'Unknown' state silent-fill caught)</ref>
    <ref type="investigation_target">All gold-layer scripts + platinum artifact schemas that reference `state` or `client_state`</ref>
  </references>

  <objective>
    Audit + align `state` vs `client_state` field naming across the BD gold chain + platinum artifacts + portal types. Eliminate silent-fill defaults on missing state fields (D_04 'Unknown' class of bug).

    Two paths (Phase 0 picks):

    **Path A — standardize on one name:**
    Pick canonical (likely `client_state` in gold/platinum for clarity; `state` in silver is raw source). Rename occurrences in the other name; update types.ts accordingly. DE/RD coordination required for portal type renames.

    **Path B — dual-name with explicit mapping:**
    Keep both names (silver=`state`, gold/platinum=`client_state`) but formalize the mapping in `lib/schema.py` or similar. Replace silent-fill 'Unknown' defaults with raise-on-missing to force upstream fix.

    Both paths share: eliminate any silent-fill 'Unknown' defaults — missing state should error or emit explicit `NULL`/None, never a silent placeholder.

    **EXPLICIT SCOPE LOCK:**
    - NO changes to silver-layer field names (out of scope; silver is source-of-truth)
    - NO retroactive portal-backfill (only forward emit changes)
    - NO cross-pod coordination required unless Path A portal-type renames (then DE TO follow-on)
    - NO widening of scope beyond state/client_state (other schema drifts = separate TOs)
  </objective>

  <scope>
    <files>
      <file action="audit">data/black_diamond/scripts/gold/*.py — grep for `state` and `client_state` references</file>
      <file action="audit">portal/src/types/*.ts + portal/src/**/*.tsx — grep for `state` and `client_state` field consumption</file>
      <file action="audit">data/black_diamond/scripts/gold/lib/*.py — schema module if present</file>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py + D_02.advisor_client_detail.py + any other D-tier with state handling — replace silent-fill with either raise-on-missing OR explicit None per Phase 0 decision</file>
      <file action="modify-if-path-A">Rename occurrences in chosen scripts; coordinate portal type renames via DE follow-on TO</file>
      <file action="modify-if-path-B">Formalize mapping in lib; update callers to use mapping</file>
      <file action="modify">data/black_diamond/scripts/gold/gold_validate_config.yaml — add state/client_state field-presence check + raise-on-silent-fill ERROR</file>
    </files>
  </scope>

  <deliverables>
    <deliverable id="audit-doc">
      `data/black_diamond/diagnostics/ROLLUP/state_schema_audit.md` — full enumeration of `state` vs `client_state` references across gold + platinum + portal. Include line numbers + current behavior (silent-fill / raise / null).
    </deliverable>
    <deliverable id="path-decision">
      Phase 0 session log picks Path A or Path B + rationale. If Path A, queue DE follow-on TO for portal rename coordination.
    </deliverable>
    <deliverable id="silent-fill-eliminated">
      Zero silent-fill 'Unknown' (or analogous) defaults for state fields anywhere in gold chain post-ship. Replaced with raise-on-missing OR explicit None/null.
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml block ERRORs on silent-fill 'Unknown' in state outputs.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">Audit doc ships with full state/client_state reference enumeration across gold + platinum + portal. No missed references.</ac>
    <ac id="2">Path A or Path B chosen with documented rationale in session log.</ac>
    <ac id="3">Zero silent-fill 'Unknown' defaults on state fields — grep confirms post-ship.</ac>
    <ac id="4">Validator block added; `comp-validate D_04` (and D_02 if touched) exits 0.</ac>
    <ac id="5">If Path A: DE follow-on TO spec drafted in session log for portal rename.</ac>
    <ac id="6">No regression on state-field consumption — `comp-transform schema-check` on affected portal components returns zero MISSING.</ac>
    <ac id="7">py_compile + ds-commit-gate exit 0; `comp-pipescript deployed` MATCH post-S3-upload.</ac>
    <ac id="8">MCP COMPLETE with commit hash + path chosen + silent-fill-count-before vs -after (both should be zero after).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>grep -rn "state\|client_state" data/black_diamond/scripts/gold/*.py data/black_diamond/scripts/gold/lib/*.py</run>
        <expect>Full reference enumeration. Use as foundation for audit doc.</expect>
        <if_mismatch>If excessive matches (state as Python keyword / state machines / etc.), refine to field-access patterns: `df\['state'\]` / `df\['client_state'\]` / `.state` / `.client_state` attribute access.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "'Unknown'\|\"Unknown\"" data/black_diamond/scripts/gold/*.py</run>
        <expect>Find silent-fill defaults. C_08 fix eliminated one; hunt for siblings.</expect>
        <if_mismatch>If 'Unknown' is used as legitimate classification in some contexts, distinguish from silent-fill usage in audit.</if_mismatch>
      </step>
      <step>
        <run>comp-transform schema-check ClientsTab AdvisorIntelligence</run>
        <expect>Portal schema-check surfaces any MISSING or unused state/client_state fields.</expect>
        <if_mismatch>Document every MISSING for DE follow-on TO.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-blast D_04 D_02</run>
        <expect>Consumer list for state-field emissions. Confirms portal components + any gold-downstream affected.</expect>
        <if_mismatch>Unexpected consumers = coordinate.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/D_02.advisor_client_detail.py</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix syntax.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/black_diamond/scripts/gold/D_04.client_portal_summary.py data/black_diamond/scripts/gold/D_02.advisor_client_detail.py data/black_diamond/scripts/gold/gold_validate_config.yaml</run>
        <expect>Exit 0.</expect>
        <if_mismatch>Fix flagged.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed D_04 D_02</run>
        <expect>MATCH on touched scripts.</expect>
        <if_mismatch>Re-upload.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "'Unknown'\|\"Unknown\"" data/black_diamond/scripts/gold/D_*.py</run>
        <expect>Zero silent-fill state defaults remain.</expect>
        <if_mismatch>Missed occurrence; patch.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/black_diamond/scripts/gold/D_04.client_portal_summary.py">
      Active history: CP-WP5 + COHORT-A closed 2026-04-22; TOPPOSOPAL staged. Coordinate with TOPPOSOPAL if concurrent — both are additive/surgical edits but on same file.
    </shared_resource>
    <shared_resource file="portal/src/types/*.ts">
      Path A rename touches portal types. Coordinate with DE/RD via follow-on TO authoring; this TO surfaces the work but doesn't execute portal-side changes.
    </shared_resource>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT modify silver-layer field names. Silver is source-of-truth; alignment happens at gold/platinum boundary.</rule>
    <rule>Do NOT expand scope beyond state/client_state. Other schema drifts = separate TOs.</rule>
    <rule>Do NOT make portal changes in this TO — DE follow-on only (if Path A chosen).</rule>
    <rule>Do NOT introduce new silent-fill defaults. All missing-field handling = raise-on-missing or explicit None/null.</rule>
  </do_not>
</task_order>
