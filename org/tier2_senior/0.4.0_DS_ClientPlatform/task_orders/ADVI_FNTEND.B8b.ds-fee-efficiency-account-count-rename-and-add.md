<task_order>
  <metadata>
    <id>ADVI_FNTEND.B8b</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- ~B shipped 2026-04-15 22:40Z. C_08 _build_window (L322-393): RENAME account_count → accounts_as_primary; ADD accounts_touched via detail_window groupby (advisor, role).nunique(account_id). py_compile PASS. D_04 passthrough needs no change (L404 verbatim emit). DE pre-flight sent 22:37Z; data_contract.xml <shipped> block replaces <pending_fix>. Accuracy note on #3: broad-basis accounts_touched overcounts multi-role advisors' accounts (sum_over_roles ≥ top.account_count); this is structurally inherent to any "broad" interpretation and documented in data_contract.xml. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>A (followup)</wave>
    <priority>P2 (closes B8 acceptance gap #3 — account_count semantic violation)</priority>
  </metadata>

  <references>
    <ref type="parent">org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_FNTEND.B8.ds-fee-efficiency-role-breakdown.md (HOLD pending this fix; #1+#2 ACCEPTED-with-doc)</ref>
    <ref type="trigger">CTO Path C+ approval 2026-04-15 22:13Z + ~B B-TO sweep 22:11Z (Grant Boren top=268 vs sum=5 violates "exact for account_count")</ref>
  </references>

  <objective>
    Fix `role_breakdown.{role}.account_count` semantic violation. Current emission produces sum-of-roles ≠ top-level account_count (e.g. Grant Boren top=268 vs role-sum=5). The current field name implies an "exact" sum-to-top contract that the data does not honor.

    **Fix (per CTO direction):**

    1. **RENAME** `role_breakdown.{role}.account_count` → `role_breakdown.{role}.accounts_as_primary` (preserves the narrow basis: accounts where this advisor IS the primary holder of this role).

    2. **ADD sibling** `role_breakdown.{role}.accounts_touched` (broad basis: any account where the advisor has this role at all, sums to top-level account_count). This IS the field that maintains the "exact for account_count" contract.

    Both fields shipped per role per advisor.

    Verify post-nightly: `sum_over_roles(accounts_touched) == top_level.account_count` for spot-check advisors (Grant Boren and 5 others).
  </objective>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/D_04.client_portal_summary.py (or wherever role_breakdown is emitted — verify via comp-pipescript)</file>
      <file action="modify">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml (document the semantic distinction)</file>
    </files>
    <s3_writes>
      <write>s3://opal-data-bd/code/gold/D_04.client_portal_summary.py (or actual producer)</write>
    </s3_writes>
  </scope>

  <wire_contract>
    Schema (per role per advisor):
    - `accounts_as_primary`: int — narrow basis, primary-role count
    - `accounts_touched`: int — broad basis, sums to top-level account_count
    - (old `account_count` field DELETED — explicit rename, not aliased; FE consumers must update)
  </wire_contract>

  <acceptance_criteria>
    1. Old `account_count` field removed from `role_breakdown.{role}` output.
    2. New `accounts_as_primary` populated (numerically equals what old `account_count` was).
    3. New `accounts_touched` populated; `sum_over_roles(accounts_touched)` == top-level `account_count` per advisor (spot-check Grant Boren + 5 advisors).
    4. data_contract.xml updated documenting both fields' semantics.
    5. py_compile clean; S3 upload with documented etag.
    6. Coordinate with DE: FE consumer of `role_breakdown.{role}.account_count` must rename. Send DE pre-flight notice BEFORE shipping.
    7. Parent B8 TO flipped staged → complete with reference to this commit.
    8. Session log Compiler Tools reproduces every `<run>` + observed + pass/fail.
    9. MCP COMPLETE to COO + CTO with commit hash + S3 etag + spot-check parity table + DE notification trail.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io D_04 | grep -i role_breakdown</run>
        <expect>D_04 emits role_breakdown; locate emission site.</expect>
        <if_mismatch>If different producer, locate.</if_mismatch>
      </step>
      <step>
        <run>comp-platinum reverse role_breakdown.architect.account_count</run>
        <expect>FE consumer enumerated (likely FeeEfficiencyPanel or RoleBreakdownPanel).</expect>
        <if_mismatch>If consumer unknown, surface to COO before rename.</if_mismatch>
      </step>
      <step>
        <run>MCP send_message to 0.4.0_DE_ClientPlatform — heads up: role_breakdown.{role}.account_count being renamed to accounts_as_primary + new sibling accounts_touched. FE consumer needs corresponding patch.</run>
        <expect>DE acks; DE patches FE consumer in parallel.</expect>
        <if_mismatch>If DE flags blocker, hold ship.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/black_diamond/scripts/gold/D_04.client_portal_summary.py</run>
        <expect>PY_COMPILE_OK.</expect>
        <if_mismatch>Fix.</if_mismatch>
      </step>
      <step>
        <run>{D_04 dry-run for Grant Boren; dump role_breakdown values}</run>
        <expect>account_count absent; accounts_as_primary populated; accounts_touched populated; sum_over_roles(accounts_touched) == top.account_count.</expect>
        <if_mismatch>Investigate emission logic.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit + nightly">
      <step>
        <run>For 6 spot-check advisors: `jq '.role_breakdown | to_entries | map(.value.accounts_touched) | add' platinum/advisors/{id}/summary.json` vs `jq '.account_count' platinum/advisors/{id}/summary.json`</run>
        <expect>Equal in all 6 cases.</expect>
        <if_mismatch>Document divergence cases.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - DE (0.4.0_DE_ClientPlatform) — FE consumer of `role_breakdown.{role}.account_count` must rename in same window as DS ship. Pre-flight MCP mandatory at Phase 1.
  </cross_domain_coordination>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    B8b close → flip parent ADVI_FNTEND.B8 to complete with cross-ref.
  </next>
</task_order>
