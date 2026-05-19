<task_order>
  <metadata>
    <id>MDPF_ASSETS.015</id>
    <slug>dsb-wsd2-etf-identity2-over-attribution-probe-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <closure>SUPERSEDED 2026-05-18 (Andrew-direct path). Identity_2 over-attribution was resolved without the probe-then-cap path this TO scoped. DS Base shipped `8d9325558` (WS-D.2 wsd_partner_held_etf.py: real Schwab-RPS partner-held-ETF value replaces the v1 model_aua x target_weight ESTIMATE -- the MDPF.011 account-join payoff) and `2e815b467` (WS-A aggregator consumes partner_held_etf -- identity_2 PASS end-to-end). Result on live opal-data-mdpf: min_public_residual moved from -$427,370.31 (ERROR) to +$2,089,090.53 (PASS, all 4 Opal ETFs >= 0: DIVZ +$74.0M / IDVZ +$12.4M / PFDE +$2.089M / PFOE +$2.826M); identity_1 + identity_3 still PASS; opal_aggregate_aua = $1,855,162,297.17 reconciliation OVERALL PASS. The realized fix is fix-path (a) "DATA-FIX: refine the held_partner basis from target-weight to actual position-level" -- the same path this TO's Phase 0 would have recommended -- but bypassed the probe phase via Andrew direct routing. Project JSON `MDPF_ASSETS.json` phase narrative already records this supersession; this TO file flipped to `complete` for status parity. Close-of-record commits: `8d9325558`, `2e815b467`, `01a51e5d7`. -- 2.0.0_SA_COO</closure>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO 2026-05-18 (COO). Not gated. WS-D.2 (.009, DS~B) shipped the §3.3 ETF decomposition wiring + the §7 identity-2 gate; the end-to-end run via .013 surfaced identity_2_etf_residual = ERROR (min_public_residual −$427,370.31) -- a small negative public_residual, the exact ERROR-class the gate exists to catch. The platinum-aggregate publish gates §7-clean on identity_2 -- this TO is now THE remaining MDPF Phase-2-close blocker. Probe-first: the fix path (cap held_partner, refine held_partner basis, or a CTO-ratified tolerance) depends on what Phase 0 finds.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- the LAST MDPF Phase-2 blocker. All other feeders + aggregator (WS-A/B/C/D.1/D.2/E + .011/.012/.013) are complete + RAVC2-accepted; the §7-clean platinum publish gates only on identity_2 clearing.</priority>
    <sla>Phase 0 ~0.5d (probe, read-only). Phase 1-2 ~1d if it is a simple cap/data-fix, longer if Phase 0 lands on a contract-tolerance decision that needs CTO ratify (escalates first).</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md §3.3 (held_partner derives from model_composition is_opal_etf x model_aua_positions), §5 (etf_net_assets feeder), §6 (platinum etf_decomposition[]), §7 identity 2 (etf_total == Σ held_partner + public_residual; negative public_residual = ERROR -- partner over-attribution), §7 ruling iii (v1 held_partner is target-weight-based; public_residual is an ESTIMATE, label honestly).</contract>
    <wsd2_to>MDPF_ASSETS.009 (DS~B, COMPLETE) -- WS-D.2 shipped the §3.3 wiring + the identity-2 gate. The negative-public_residual ERROR fixture verified the gate logic; this TO is its first real-data trigger. v1 caveat from .009: public_residual is target-weight estimate, not exact.</wsd2_to>
    <agg_evidence>.013 end-to-end run (DS~A, commits 1757fe364 + d2c751cfc): identity_1 PASS, identity_3 PASS, identity_2_etf_residual ERROR (min_public_residual −$427,370.31). All other §7 checks pass. The aggregator's negative-public_residual exit-non-zero is exactly the contract behavior (ERROR-class, not WARN). DS~A correctly did NOT upload a known-ERROR platinum artifact.</agg_evidence>
    <etf_universe>Per contract §3.3 + the .003 / .009 work: 4 Opal ETFs -- DIVZ + IDVZ (held by NO Opal model -> public_residual = full net-assets, identity-2 cannot ERROR on these) + PFDE + PFOE (line-item holdings in 7 of 9 Inflection Opal models per .003 §4.3, and per WS-B in the 49F Opal models too). So the −$427,370.31 minimum is on PFDE and/or PFOE.</etf_universe>
    <feeders>etf_net_assets: opal-data-mdpf (WS-D.2 wired the WS-D.1 feed; .009). model_composition: opal-data-mdpf (WS-B 49F + WS-C Inflection, with the is_opal_etf flag on PFDE/PFOE/DIVZ/IDVZ rows). model_aua_positions: opal-data-mdpf (WS-B + WS-C).</feeders>
  </references>

  <context>
    Identity 2 is: for each ETF, etf_total_net_assets == Σ_partner held_partner + public_residual. held_partner is the partner-advised slice (already inside that partner's model_aua via the §3.5 no-double-count rule); public_residual (Cohort 0) is the measured plug -- ETF float held outside Opal's advised base. A NEGATIVE public_residual means Σ held_partner > etf_total -- partner attribution exceeds the ETF's actual net assets, which is structurally impossible (you cannot advise more of an ETF than exists). The −$427K is small in absolute terms but unbounded in semantics: it MUST resolve.

    The v1 caveat the WS-A contract ruling iii spells out: v1 held_partner is target-weight-based -- held_partner(partner, ETF) = Σ_{model in partner} [ target_weight(model, ETF) × model_aua(model) ]. That is NOT the same as the partner's actual position in the ETF -- it is what the partner WOULD hold if every account were perfectly on-target. Real portfolios drift below target (cash drag, partial rebalance, account-level deviations); a target-weight estimate is typically HIGHER than actual positions. That structural over-estimation is the most likely root cause of the small negative public_residual, but Phase 0 must verify before the fix path is chosen.

    Three candidate fix paths -- Phase 0 picks one (or escalates):
    (a) DATA-FIX: refine the held_partner basis from target-weight to actual position-level (if accounts_v2 or a holdings feed carries the per-account ETF position). Cleanest if the data exists.
    (b) BOUND-FIX: cap held_partner at etf_total per ETF, floor public_residual at 0, label the cap (carry the v1-estimate caveat honestly per ruling iii). This is what the §6 platinum etf_decomposition[] block could carry as a v1 compromise.
    (c) CONTRACT-TOLERANCE: the v1 target-weight estimate has irreducible noise on the order of $hundreds-of-thousands. Either ratify a small negative-tolerance band in §7 identity 2 (e.g. abs(public_residual) <= 0.1% of etf_total downgrades from ERROR to WARN) or accept (b) as the v1 behavior. CTO ratification required.

    None of these is silently picked. Phase 0 produces the evidence; CTO ratifies the path.
  </context>

  <scope>
    <step>Phase 0 -- PROBE (read-only). Resolve, with evidence:
      (a) WHICH ETF (PFDE / PFOE / both?) carries the negative public_residual, and by how much per-partner. Pull the .013 aggregator's etf_decomposition output (or recompute from the feeds) and surface the per-(ETF, partner) held_partner values vs etf_total.
      (b) WHICH partner over-attributes (49F via WS-B, Inflection via WS-C, or both contributing). For each over-attributing (partner, ETF) pair, compute held_partner exactly (Σ target_weight × model_aua over the partner's models with is_opal_etf on this ETF), confirm vs the aggregator output, and quantify the surplus.
      (c) WHY -- distinguish the candidate causes with empirical evidence: (i) target-weight estimation drift (compute the partner's ACTUAL ETF position from a holdings feed if available -- accounts_v2 / SmartX holdings / BD holdings -- and compare to the target-weight estimate); (ii) etf_net_assets date / staleness mismatch (compare the etf_net_assets as_of_date vs the model_aua_positions as_of_date); (iii) model_aua scope mismatch (an account in the model that should not be counted toward that ETF). Land a one-paragraph verdict per ETF.
      (d) Recommend ONE of fix paths (a)/(b)/(c) above, grounded in the Phase-0 evidence. Surface to COO + CTO before Phase 1 if (c) is recommended -- a contract-tolerance change is a CTO call.</step>
    <step>Phase 1 -- implement the Phase-0-confirmed fix. Per the rule: the WS-A aggregation script owns the §3.3 decomposition (single-owner) -- if Phase 1 changes held_partner or public_residual computation, it changes in mdpf_aggregate_aua.py, not in a WS-D.2 fork. If Phase 0 lands on a DATA-FIX (refine held_partner basis), wire the actual-position holdings feed into the §3.3 decomposition (etf_net_assets stays untouched; the change is on the held_partner side). If (b) cap-floor, implement the cap in mdpf_aggregate_aua.py with a labeled v1 caveat in the platinum etf_decomposition[] block (ruling iii). If (c) contract-tolerance, ratify FIRST, then implement the WARN-vs-ERROR threshold. Rule 15; ds-commit-gate exit 0; comp-pipescript io on mdpf_aggregate_aua.py before write.</step>
    <step>Phase 2 -- verify end-to-end. Re-run mdpf_aggregate_aua.py against the live opal-data-mdpf feeds. Identity_2 PASS for all 4 Opal ETFs (public_residual >= 0 for PFDE + PFOE; DIVZ + IDVZ unchanged at full-net-assets). Identity_1 + identity_3 still PASS. The platinum aggregate is §7-clean and PUBLISHABLE -- coordinate with COO on the publish trigger.</step>
  </scope>

  <gate_verdict_policy>
    The §7 identity_2 gate is ERROR-class (negative public_residual exits non-zero) -- unchanged by this TO except that Phase 0 may recommend a CTO-ratified WARN tolerance. Until this TO closes, the aggregator correctly refuses to publish a known-ERROR platinum artifact (.013's behavior is the spec, not a bug).
  </gate_verdict_policy>

  <compiler_tools_mandate>
    <phase id="0" when="before write">
      <step>
        <run>comp-pipescript io on mdpf_aggregate_aua.py + on any holdings-feed script the data-fix candidate would touch.</run>
        <expect>What the aggregator reads/writes for etf_decomposition; where the per-account holdings data lives if a data-fix is the path.</expect>
        <if_mismatch>Resolve before Phase 1.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>comp-blast on the aggregator function touched + comp-validate mdpf_aggregate_aua --artifact &lt;new platinum&gt; if a validate config exists.</run>
        <expect>Blast radius is mdpf_aggregate_aua + the platinum artifact only; the aggregator exits 0 all-pass with identity_2 cleared.</expect>
        <if_mismatch>Exit 1 = BLOCKED, do not signal complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <reprocess_required>If Phase 1 changes held_partner / public_residual in mdpf_aggregate_aua.py, the platinum aggregate re-materializes on the next aggregator run (forward; no backfill of upstream producers). No silver/gold feeder modified.</reprocess_required>
  </data_reprocess_scope>

  <cross_domain_coordination>
    SINGLE-OWNER: the §3.3 decomposition logic lives in mdpf_aggregate_aua.py (DS~A). If Phase 1 changes that script, DS~B coordinates the edit with DS~A (the .013 author) so there is no concurrent-edit hazard -- single owner per the .009 cross_domain_coordination rule ("if decomposition code must change, it changes in the WS-A script, one owner"). Inputs (model_composition + model_aua_positions + etf_net_assets) are not modified by this TO. If Phase 0 recommends a CTO-ratified contract-tolerance change (fix path c), the contract amendment is CTO's call -- escalate FIRST.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Phase-0 probe brief: per-(ETF, partner) over-attribution quantified; root-cause verdict (target-weight drift / date mismatch / scope mismatch); recommended fix path (a/b/c) with evidence. If (c) was recommended, it was escalated to CTO BEFORE Phase 1 -- not silently implemented.</ac>
    <ac id="AC2">Phase 1 implements the Phase-0-confirmed fix path in mdpf_aggregate_aua.py (single owner; coordinate the edit with DS~A). The v1-estimate caveat is labelled honestly per ruling iii if a cap-floor is implemented.</ac>
    <ac id="AC3">Phase-2 end-to-end: identity_2 PASS for all 4 Opal ETFs (public_residual >= 0 PFDE + PFOE; DIVZ + IDVZ unchanged). identity_1 + identity_3 still PASS. The platinum aggregate is §7-clean.</ac>
    <ac id="AC4">No emoji; ds-commit-gate exit 0 on every .py edit; Rule 15 where applicable; session log with the Compiler Tools section. RAVC2 to COO. On AC3 close the MDPF Phase-2 platinum-aggregate publish gate is CLEAR -- notify COO so the publish trigger can fire.</ac>
  </acceptance_criteria>

  <deliverables>
    - Phase-0 probe brief (per-ETF over-attribution + root-cause verdict + recommended fix path).
    - The Phase-0-confirmed fix in mdpf_aggregate_aua.py (single owner -- coordinate with DS~A).
    - The Phase-2 verified §7-clean platinum aggregate.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
