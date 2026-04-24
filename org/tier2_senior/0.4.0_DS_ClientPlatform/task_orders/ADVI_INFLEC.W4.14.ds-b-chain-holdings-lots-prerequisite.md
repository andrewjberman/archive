<task_order>
  <metadata>
    <id>ADVI_INFLEC.W4.14</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to><!-- ~A lane per Andrew 2026-04-22 INFLEC DS reassignment (commit 5f6c0bc3) -->
    <date>2026-04-24</date>
    <status>staged</status><!-- Gates on AE 0.6.1 W4.13 PROD chain completion (SSM b9d0bff8 running); COO fires GO on W4.13 COMPLETE MCP from AE. -->
    <project_code>ADVI_INFLEC</project_code>
    <wave>W4</wave>
    <phase_label>W4.14 (B-chain holdings_lots prerequisite; unblocks firm_composition.json + downstream lot-level portal surfaces)</phase_label>
    <priority>P1 — last structural gap in INFLEC v1 gold chain; blocks firm_composition.json emit (confirmed W4.12 PASS surfaced this as data-reality gap, not pipeline defect)</priority>
    <origin>
      Surfaced by ~A's W4.12 validation 2026-04-22T22:16:10Z: "firm_composition.json NOT PRODUCED (I_D03 graceful no-op). Root cause: gold/holdings/ is empty — I_B01 (holdings_lots B-chain) has never run on INF. I_D03 exits 0 with WARN when gold/holdings/ is absent. This is by design. Resolution: B-chain (I_A01 → I_A02 → I_A03 → I_B01) must run before firm_composition is available. This is a separate TO — not a W4.12 blocker if the B-chain is scheduled."
      CTO NO REDLINE on W4.12 flex 2026-04-24T124110Z confirmed B-chain queue under ~A's lane.
    </origin>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFLEC.md (W4 gold-chain architecture)</ref>
    <ref type="precedent">data/black_diamond/scripts/gold/A_01.advisor_assignments.py — BD analog for I_A01 INF adaptation</ref>
    <ref type="precedent">data/black_diamond/scripts/gold/A_02.fee_rate_history.py — BD analog for I_A02 (INF already has stub from W4.7; may extend or keep stub depending on Orion fee data availability)</ref>
    <ref type="precedent">data/black_diamond/scripts/gold/A_03.positions_cube.py — BD analog for I_A03 positions_cube</ref>
    <ref type="precedent">data/black_diamond/scripts/gold/B_01.holdings_lots.py — BD analog for I_B01 holdings_lots</ref>
    <ref type="incident">SSM 5a5d779a crash at I_A03 (W4.9 re-dispatch) — presumed memory pressure on c6a.2xlarge with 2,851 accts × 2,408 days O(n*k) expansion. Runtime-config mitigation mandatory in this TO.</ref>
    <ref type="related_active">AE 0.6.1 W4.13 first PROD gold chain (SSM b9d0bff8); W4.14 gates on W4.13 completion to avoid runner contention + establish I_A03 behavior on PROD runner before B-chain shipping</ref>
  </references>

  <objective>
    Author + ship B-chain scripts (I_A01, I_A02 extension if fee data available, I_A03 with memory mitigation, I_B01) on Orion/INFLEC data. Goal: `gold/holdings/` populated with per-account-per-date holdings_lots; downstream I_D03 re-runs to emit `platinum/firm/composition.json` on the next full chain cycle. Ship tested, deployed, full-chain-validated.

    **EXPLICIT SCOPE LOCK:**
    - NO new C-chain or D-chain scripts (those waves complete)
    - NO portal-side work (pure gold-layer)
    - NO BD script modifications (INF adaptation only under `data/orion/scripts/gold/`)
    - I_A02 extension OPTIONAL — keep stub if Orion fee data remains unavailable per W4.7 finding
    - I_A03 MUST include memory mitigation (chunking OR runner-size config note; document choice in Phase 0)
  </objective>

  <scope>
    <files>
      <file action="create-or-extend">data/orion/scripts/gold/I_A01.advisor_assignments.py — if not already shipped in W4.7 (verify)</file>
      <file action="create-or-extend">data/orion/scripts/gold/I_A02.fee_rate_history.py — extend from W4.7 stub if Orion fee data newly available; else document persistent stub</file>
      <file action="create-or-extend">data/orion/scripts/gold/I_A03.positions_cube.py — with mandatory memory-pressure mitigation (chunking OR runner-size note)</file>
      <file action="create">data/orion/scripts/gold/I_B01.holdings_lots.py — adapted from BD B_01 for Fidelity single-custodian, household grain, ticker keying, NaT guard</file>
      <file action="modify">data/orion/scripts/gold/inf-gold-dispatch.sh — add I_A01-I_A03 + I_B01 to CHAIN_FULL in correct dependency order</file>
      <file action="read-only">data/black_diamond/scripts/gold/A_01.advisor_assignments.py + A_02.fee_rate_history.py + A_03.positions_cube.py + B_01.holdings_lots.py (precedent reference; inline adaptations only)</file>
      <file action="read-only">data/orion/scripts/gold/gold_validate_config.yaml — add I_B01 validator block (units>=0, price>0, date non-null, cash stub price=1.0 sentinel)</file>
    </files>
  </scope>

  <orion_adaptations>
    Standard INF conventions (consistent with your prior W4.7/W4.8/W4.9 work):
    - No `lib.config` / `lib.s3_layout` — inline constants + `opal-data-inf` bucket
    - No cross-custodian merge (Fidelity single-custodian)
    - `household_id` as relationship grain (NOT `relationship_id`)
    - `ticker` as canonical asset identifier (NOT `asset_name`)
    - AUA terminology: `total_aua` / `tagged_aua` / `fee_earning_aua` — NEVER `managed_aua`
    - NaT guard on all date joins per `d87377a5` mandate
    - No emojis in any print/log (CLAUDE.md Rule)
    - ds-commit-gate mandatory pre-commit (CLAUDE.md Rule 14)
  </orion_adaptations>

  <i_a03_memory_mitigation>
    SSM 5a5d779a crashed at I_A03 on c6a.2xlarge. 2,851 accounts × 2,408 days × O(k) ticker universe = multi-GB dataframe in naïve groupby/pivot. Two acceptable paths — pick in Phase 0:

    **Path A — script-level chunking:**
    Process positions_cube in date-ranges of ~90 days or account-ranges of ~250 accounts; write partitioned parquet incrementally; concat at end. No runner-size change.

    **Path B — runner-size bump:**
    Request c6a.4xlarge or c6a.8xlarge from AE 0.7 for inf-gold-layer-runner; document in EC2_MANIFEST + infra TF. Costs more per run but simpler code.

    Document choice + rationale in Phase 0 step. If Path B, MCP AE 0.7 for infra change BEFORE shipping code.

    `--skip-existing` flag on re-runs per ~A's earlier recommendation (avoid recomputing completed date partitions).
  </i_a03_memory_mitigation>

  <dependencies>
    <dependency task="ADVI_INFLEC.W4.13" status="pending" agent="0.6.1_AE_PartnerETL" description="First PROD gold chain run (SSM b9d0bff8); establishes I_A03 behavior on PROD runner; W4.14 gates on W4.13 COMPLETE MCP"/>
    <dependency task="ADVI_INFLEC.W4.12" status="pending-flex-accepted" description="~A to flip pending→complete per CTO NO REDLINE 2026-04-24T124110Z; not hard gate on W4.14 scheduling but should be resolved for clean REGISTRY"/>
  </dependencies>

  <deliverables>
    <deliverable id="b-chain-scripts">
      All B-chain scripts + A-chain prerequisites authored + pre-commit-gate clean + pushed CLOUD + uploaded to `s3://opal-data-inf/code/gold/`.
    </deliverable>
    <deliverable id="i-a03-mitigation-documented">
      Phase 0 session log cites chosen mitigation path (A chunking OR B runner-size) + empirical rationale (memory profile estimate OR runtime-config MCP to AE 0.7).
    </deliverable>
    <deliverable id="full-chain-green">
      Full inf-gold-dispatch.sh `--chain full --skip-existing` dispatch completes cleanly; `gold/holdings/` populated; `platinum/firm/composition.json` emitted on downstream D-chain run (I_D03 no longer graceful no-op).
    </deliverable>
    <deliverable id="validator-block">
      gold_validate_config.yaml block for I_B01 output: field presence (date, account_id, ticker, units, price, mv) + units>=0 + price>0 + date non-null + MV>=0.
    </deliverable>
  </deliverables>

  <acceptance_criteria>
    <ac id="1">I_A01/I_A03/I_B01 scripts authored (I_A02 extended or stub-retained with documented reason) under `data/orion/scripts/gold/`. All ship via pre-commit-gate (py_compile + ds-commit-gate.sh both exit 0).</ac>
    <ac id="2">I_A03 memory mitigation: Phase 0 session log cites Path A (chunking implemented) OR Path B (runner-size bump coordinated with AE 0.7 before code ship). Chain run on selected path completes without OOM or timeout.</ac>
    <ac id="3">inf-gold-dispatch.sh updated to include I_A01→I_A02→I_A03→I_B01 in CHAIN_FULL; `comp-pipescript deployed` MATCH post-upload.</ac>
    <ac id="4">`--chain full --skip-existing` dispatch runs clean end-to-end (ResponseCode 0 SSM); `gold/holdings/` partitions populated; spot-check 3 sample accounts (architect+implementor+consultant grain) — units signed correctly, prices non-zero for non-cash tickers, cash lots price=$1.00.</ac>
    <ac id="5">`platinum/firm/composition.json` emitted on the same chain run (I_D03 no longer graceful no-op). Field-presence check passes + non-zero totals.</ac>
    <ac id="6">gold_validate_config.yaml I_B01 block added; `comp-validate I_B01 --artifact /tmp/holdings_lots_sample.parquet` exits 0.</ac>
    <ac id="7">Session log Compiler Tools section reproduces every `<run>` + observed + pass/fail vs `<expect>`.</ac>
    <ac id="8">MCP COMPLETE to COO with: commit hash + chain SSM command_id + ResponseCode + `gold/holdings/` partition count + `platinum/firm/composition.json` existence + 3-account spot-check MV totals.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="discovery">
      <step>
        <run>comp-pipescript io B_01</run>
        <expect>BD B_01 READS/WRITES surfaced; identify fields INF can source from Orion TRN + canonical_prices.</expect>
        <if_mismatch>If BD B_01 uses columns not available in Orion, document adaptation path in Phase 0 session log.</if_mismatch>
      </step>
      <step>
        <run>comp-pipescript io A_03</run>
        <expect>BD A_03 positions_cube READS/WRITES; identify memory-profile-relevant operations (groupby/pivot/join scale).</expect>
        <if_mismatch>If scale differs materially from BD (INF has 2,851 accts vs BD ~6,500), document in mitigation choice.</if_mismatch>
      </step>
      <step>
        <run>python3 -c "import pyarrow.parquet as pq; t = pq.read_table('s3://opal-data-inf/silver/positions_cube/<latest>.parquet') if exists else None; print(t.num_rows if t else 'ABSENT')"</run>
        <expect>Confirm silver/positions_cube absent (expected — B-chain has not yet run) OR note exists + row count.</expect>
        <if_mismatch>If silver/positions_cube exists, B-chain may already be partially done — halt + MCP COO.</if_mismatch>
      </step>
    </phase>

    <phase id="1" when="before write">
      <step>
        <run>comp-pipescript io inf-gold-dispatch</run>
        <expect>CHAIN_FULL enumerated; identify insertion point for I_A01-I_A03 + I_B01 (after A_00, before C-chain).</expect>
        <if_mismatch>If dispatch already has A-chain entries pointing to stubs, verify + update with real script filenames.</if_mismatch>
      </step>
      <step>
        <run>comp-blast B_01 (BD reference)</run>
        <expect>Downstream BD consumers surfaced; confirm INF I_B01 has analogous consumer footprint (I_D03 composition + any lot-level portal readers).</expect>
        <if_mismatch>If unexpected BD consumers, evaluate whether INF needs parallel downstream scripts authored in W4.14 or carried as W4.15 follow-on.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>python -m py_compile data/orion/scripts/gold/I_A01.advisor_assignments.py data/orion/scripts/gold/I_A03.positions_cube.py data/orion/scripts/gold/I_B01.holdings_lots.py</run>
        <expect>Exit 0 for all 3 (+ I_A02 if extended).</expect>
        <if_mismatch>Fix syntax errors before commit.</if_mismatch>
      </step>
      <step>
        <run>.tools/ds-commit-gate.sh data/orion/scripts/gold/I_A01.advisor_assignments.py data/orion/scripts/gold/I_A03.positions_cube.py data/orion/scripts/gold/I_B01.holdings_lots.py</run>
        <expect>Exit 0 — py_compile + AST undefined-name scanner clean.</expect>
        <if_mismatch>Fix flagged issues before commit (CLAUDE.md Rule 14).</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit">
      <step>
        <run>comp-pipescript deployed I_B01 I_A03 I_A01</run>
        <expect>MATCH on all three after S3 upload.</expect>
        <if_mismatch>STALE = re-upload missing scripts; verify S3 key correctness.</if_mismatch>
      </step>
      <step>
        <run>comp-validate I_B01 --artifact /tmp/holdings_lots_sample.parquet</run>
        <expect>Exit 0; all ERROR checks pass; validator block for I_B01 added to config.</expect>
        <if_mismatch>Iterate validator config or fix data shape until exit 0.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-inf/gold/holdings/ | tail -5</run>
        <expect>Populated partitions post-chain-run; non-empty.</expect>
        <if_mismatch>Chain did not write holdings; inspect SSM log at `/tmp/inf_gold_logs/`.</if_mismatch>
      </step>
      <step>
        <run>aws s3 ls s3://opal-data-inf/platinum/firm/composition.json</run>
        <expect>Exists with mtime from this chain run (no longer I_D03 graceful no-op).</expect>
        <if_mismatch>I_D03 still graceful no-op = I_B01 output malformed or not picked up; debug.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource file="data/orion/scripts/gold/inf-gold-dispatch.sh">
      Post-W4.13 state (AE 0.6.1 shipped dispatch.sh updates for aws→boto3 bootstrap); coordinate with AE 0.6.1 if they push dispatch.sh changes during W4.14.
    </shared_resource>
    <shared_resource file="data/orion/scripts/gold/gold_validate_config.yaml">
      Additive I_B01 block; low conflict risk.
    </shared_resource>
    <downstream_pending>Portal composition surfaces consume firm_composition.json post W4.14 — future DE wiring (W5.x) gated on W4.14 completion.</downstream_pending>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT skip I_A03 memory mitigation. The 5a5d779a crash class is the primary risk; unmitigated I_A03 will crash this TO.</rule>
    <rule>Do NOT modify BD scripts. INF adaptations only under `data/orion/scripts/gold/`.</rule>
    <rule>Do NOT author D-chain scripts in this TO — W4.10/W4.3-4.5 covers those.</rule>
    <rule>Do NOT use `managed_aua` or `asset_name` as field names. See `<orion_adaptations>`.</rule>
    <rule>Do NOT dispatch full chain until `comp-pipescript deployed` MATCH on all new scripts.</rule>
  </do_not>
</task_order>
