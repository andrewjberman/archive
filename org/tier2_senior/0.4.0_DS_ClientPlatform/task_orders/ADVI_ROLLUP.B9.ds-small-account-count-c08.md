<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-04-15-advi-rollup-b9-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-15</date>
    <status>complete</status><!-- 0.4.0_DS_ClientPlatform~C, commit 0a98d9e9 (initial f2ec98d1 + account_id source fix); rerun 9cbfbde5 on QA: total=4765 small accts firm-wide, 15 advisors-with-zero, nulls-excluded=0, Travis Penfield=45. comp-validate C_08 exit 0. 2026-04-15. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>W3</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_ROLLUP_ADDENDUM_small_account_count.md</ref>
    <ref type="prd">docs/architecture/ADVI_ROLLUP.md (Wave 3 addendum)</ref>
    <ref type="companion">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_ROLLUP.B9.de-small-account-count-column.md (DE side, paired ship)</ref>
    <ref type="precedent">ADVI_FNTEND.B8 (fee-efficiency role breakdown, commit b9d9a3f3 — same C_08 + FeeEfficiencyPanel touchpoints)</ref>
  </references>

  <objective>
    Extend C_08.advisor_fee_efficiency.py with a per-advisor `small_account_count` scalar on every
    window row (qtd / ytd / trailing_1y / trailing_3y / max). Emitted in every `advisors[]` row of
    `gold/artifacts/advisor_fee_efficiency.json`.

    Threshold: module-level constant `SMALL_ACCOUNT_AUA_THRESHOLD_USD = 40_000`. Grep-able.

    "Attached to" = any role in `account_team` (architect / implementor / consultant / local_ops /
    additional_advisor) — same semantics as existing `account_count`. Do NOT restrict to one role.

    Edge-case rules (explicit):
    - NULL `account_aua` → EXCLUDED (log as `small_account_null_aua_excluded` count in summary stats).
    - Zero `account_aua` → INCLUDED.
    - Negative `account_aua` → INCLUDED.
    - Ghost / excluded / pseudonymized accounts → follow whatever `account_count` currently does. Do NOT diverge.

    Emit a summary line in run output: `small_account_count total firm-wide, advisors-with-zero-small-accounts count, nulls-excluded count`.

    **Coordination:** If ADVI_FNTEND.B8 gold rerun (commit b9d9a3f3) has not yet fired, piggyback
    this commit into the same C_08 rerun to save a nightly cycle. If B8 already landed, one more
    nightly is cheap.
  </objective>

  <wire_contract>
    gold/artifacts/advisor_fee_efficiency.json — every `advisors[]` row gains:
      `small_account_count: number` (required, default 0, never null)

    Ships alongside the existing required siblings: advisor, roles, account_count, aua?, fee_usd_total?, fee_bps?, role_breakdown?

    No optional shim — field is required-on-emit. DE TO picks up simultaneously; required type lands
    when this artifact ships.

    Post-pseudonymization note: confirm that `account_aua` is either ACCURATE-or-NULL (never
    sentinel-zeroed) before ship. If pseudonymization zeroes AUA to hide balance, those rows would
    incorrectly count as small. Verify with one spot-check pre-commit.
  </wire_contract>

  <acceptance_criteria>
    1. `SMALL_ACCOUNT_AUA_THRESHOLD_USD = 40_000` module-level constant in `C_08.advisor_fee_efficiency.py`.
    2. Every `advisors[]` row in emitted JSON carries `small_account_count` (integer, non-null, default 0).
    3. Firm-wide sum is a plausible small-account count (order "few hundred" not "tens of thousands" and not zero).
    4. Travis Cobb's row: `small_account_count > 0` (known to have low-balance sub-accounts).
    5. Summary stats line emits `total`, `advisors-with-zero-count`, `nulls-excluded` values.
    6. Post-pseudonymization verification: confirm `account_aua` is accurate-or-NULL, never sentinel-zeroed. Record spot-check in commit message.
    7. `comp-validate C_08` exits 0.
    8. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO audit requirement 2026-04-15).
    9. MCP COMPLETE to COO with commit hash + firm-wide sum + Travis count + summary-stats line.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io C_08</run>
        <expect>READS includes `account_team` and `advisor_fee_detail`; WRITES includes `advisor_fee_efficiency.json` -> D_04. No COLUMN GAPS.</expect>
        <if_mismatch>STOP. If new READ appears, surface to COO before writing code. If COLUMN GAPS non-empty, fix the load list first.</if_mismatch>
      </step>
      <step>
        <run>comp-blast C_08</run>
        <expect>Downstream consumers limited to D_04 + advisor_fee_efficiency readers (FeeEfficiencyPanel). No new portal components in blast.</expect>
        <if_mismatch>STOP. Document any new consumer and message its owning agent before writing.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>comp-pipescript deployed C_08</run>
        <expect>MATCH status (runner has latest source).</expect>
        <if_mismatch>Coordinate with AE before upload.</if_mismatch>
      </step>
      <step>
        <run>comp-validate C_08 --artifact /tmp/advisor_fee_efficiency.json</run>
        <expect>Exit 0. All ERROR checks pass. WARN count documented in session log.</expect>
        <if_mismatch>STOP. Do not commit until ERROR clean.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-blast advisor_fee_efficiency</run>
        <expect>Same consumer set as Phase 1 — no new downstream nodes appeared during write.</expect>
        <if_mismatch>Surface to COO. Likely indicates another agent committed a new consumer mid-flight.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    None. Can ship alone or piggyback ADVI_FNTEND.B8 C_08 rerun.
  </dependencies>

  <next>
    On commit: trigger C_08 rerun (QA runner), validate artifact carries `small_account_count`,
    signal COO. DE B9 TO fires after artifact lands on DEV.
  </next>
</task_order>
