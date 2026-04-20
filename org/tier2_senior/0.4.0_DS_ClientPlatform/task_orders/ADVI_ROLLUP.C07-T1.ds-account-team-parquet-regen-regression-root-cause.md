<task_order>
  <metadata>
    <id>ADVI_ROLLUP.C07-T1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- ~A surfaced during B1/B3/B4 validator sweep 2026-04-15 22:27Z -->
    <date>2026-04-15</date>
    <status>complete</status><!-- COO flip 2026-04-16 13:38Z. COMPLETE-IN-FACT via ~A RCA f49aa9bd + ~B B3.fix 544877cc. Deliverable memo present: docs/analysis/2026-04-15_c07_account_team_regression_rca.md. Decision-tree outcome was Option 3: "C_07 ran and output populated, but D_02 reads wrong path -> D_02 code fix (B3.fix scope)" — confirmed; B3.fix D_02 L358 added `relationship_id` to _load_account_team column list + L2272 WARN-LOUD replaces silent-skip. No remaining C_07-layer investigation needed. -->
    <project_code>ADVI_ROLLUP</project_code>
    <wave>3 (FE correctness — C_07 producer triage)</wave>
    <priority>P1 per CTO 2026-04-15 22:28Z (root cause of B3 team_attribution=[] on 153/153)</priority>
  </metadata>

  <references>
    <ref type="trigger">~A B1/B3/B4 validator sweep MCP 2026-04-15 22:27Z — B3 `team_attribution = []` on ALL 153/153 sampled clients; 2026-04-02 stale detail.json found = partial rerun scope</ref>
    <ref type="cto_ruling">1.0.0_SA_CTO B3 ruling 2026-04-15 22:28Z — P1 root-cause investigation required</ref>
    <ref type="related">ADVI_FNTEND.B3.ds-fee-summary-team-attribution (parent TO, blocked until C_07 resolved)</ref>
    <ref type="related">ADVI_ROLLUP.B3.fix (defense-in-depth follow-up — warn-loud vs silent-skip)</ref>
  </references>

  <objective>
    Root-cause why `gold/views/account_team.parquet` is empty/broken/stale post-rerun. Evidence:
    - D_02 L2272-2296 silent-skips team_attribution population when `account_team is None OR account_team.empty OR 'relationship_id' column missing`.
    - Post-rerun sample: 153/153 clients in `gold/entities/clients/0/detail.json` have `team_attribution = []`.
    - `acct_z0819052671/detail.json` shows data_as_of 2026-04-02, generated 2026-04-07 — NOT overwritten in today's rerun (regen scope was partial).

    **Investigation surface:**
    1. Verify `gold/views/account_team.parquet` post-rerun state: present? row count? relationship_id column populated?
    2. `comp-pipescript io C_07` — confirm C_07 is the producer; enumerate reads.
    3. `comp-pipescript deployed C_07` — runner version MATCH vs STALE.
    4. Check the rerun chain definition (`CHAIN_FULL` post-DH-1) — did C_07 run in the 19:35Z chain-complete? (Check `s3://opal-data-bd/gold/logs/partial_b01_20260415_180736.log` per AE's recovery run.)
    5. If C_07 did run, inspect its upstream (probably silver/account_team sources) for missing partition.
    6. Spot-check other `gold/entities/clients/{advisor_slug}/detail.json` for pre-rerun data — quantify rerun partial scope.

    **Decision tree:**
    - If C_07 didn't run in rerun → scope fix (add to CHAIN_CANONICAL) OR document that team_attribution depends on a pipeline step not in A→D.
    - If C_07 ran but output is empty → inspect silver input; surface to DS for upstream fix.
    - If C_07 ran and output is populated but D_02 reads wrong path → D_02 code fix (probably B3.fix scope).

    **Deliverable:** memo at `docs/analysis/2026-04-15_c07_account_team_regression_rca.md` with decision tree outcome + recommended remediation (patch scope, TO ID if another TO needed).
  </objective>

  <scope>
    <files>
      <file action="create">docs/analysis/2026-04-15_c07_account_team_regression_rca.md</file>
      <file action="reference_only">data/black_diamond/scripts/gold/C_07*.py (producer)</file>
      <file action="reference_only">data/black_diamond/scripts/gold/D_02.advisor_client_detail.py L2272-2296 (consumer)</file>
    </files>
  </scope>

  <wire_contract>
    Read-only investigation. No S3 writes, no code patches. Memo surfaces the root cause; follow-on TOs execute remediation.
  </wire_contract>

  <acceptance_criteria>
    1. Root cause identified with direct evidence (log line, file listing, or parquet inspection).
    2. Decision-tree outcome documented (which of 3 branches hit).
    3. Remediation path recommended: specific TO ID (new or existing) that fixes it.
    4. Quantification of rerun partial scope: how many `gold/entities/clients/*/detail.json` files were NOT overwritten in the 19:35Z chain close.
    5. Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail.
    6. MCP COMPLETE to COO + CTO with memo path + root cause one-liner + recommended fix TO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws s3 ls s3://opal-data-bd/gold/views/account_team.parquet --human-readable</run>
        <expect>File present with recent mtime (19:35Z or later if rerun covered it).</expect>
        <if_mismatch>If absent or stale mtime, C_07 didn't run — scope-fix path.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io C_07 &amp;&amp; comp-pipescript deployed C_07</run>
        <expect>C_07 enumerated; deployed MATCH with current code.</expect>
        <if_mismatch>If STALE, flag to AE (deploy needed). If unknown, locate C_07.</if_mismatch>
      </step>
      <step>
        <run>grep 'C_07' data/black_diamond/scripts/runner/gold_dispatch.sh | head</run>
        <expect>C_07 appears in CHAIN_CANONICAL or equivalent; confirms dispatcher includes it.</expect>
        <if_mismatch>If absent, C_07 is out-of-chain; document gap.</if_mismatch>
      </step>
      <step>
        <run>aws s3 cp s3://opal-data-bd/gold/logs/{latest chain log} - | grep -iE 'C_07|account_team'</run>
        <expect>C_07 invocation visible; success/failure line identified.</expect>
        <if_mismatch>Confirms C_07 absent from chain fire.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after investigation">
      <step>
        <run>python -c "import pandas as pd; df = pd.read_parquet('s3://opal-data-bd/gold/views/account_team.parquet'); print(df.columns, len(df), df.head())"</run>
        <expect>If file exists: row count + column list; detect relationship_id presence.</expect>
        <if_mismatch>Investigate schema drift.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <none/>
  </dependencies>

  <next>
    C07-T1 close → recommended-fix TO dispatched (scope fix to CHAIN, upstream fix, or D_02 patch). Unblocks B3 final close.
  </next>
</task_order>
