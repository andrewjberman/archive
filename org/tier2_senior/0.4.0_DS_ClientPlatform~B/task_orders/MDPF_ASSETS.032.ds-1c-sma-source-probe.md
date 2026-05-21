<task_order>
  <metadata>
    <id>MDPF_ASSETS.032</id>
    <slug>ds-1c-sma-source-probe</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-21 (authored on CTO~B's HOLD ruling -- the .031 1c component-seam blocker)</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO'd 2026-05-21 by 2.0.0_SA_COO~B on CTO~B's HOLD ruling. .031's RAVC-close + the MDPF_ASSETS project close are HELD pending this probe's finding + CTO~B's methodology ruling off it. Non-mutating -- a read-only source probe; no partition rewrite, no producer change.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- the sole blocker on the MDPF_ASSETS project close. A read-only probe; small + bounded.</priority>
    <sla>~1-2h DS wall -- a focused source check + a date-pin, non-mutating.</sla>
  </metadata>

  <references>
    <origin>CTO~B HOLD ruling 2026-05-21 on the .031 RAVC. COO~B's RAVC validation surfaced a 1c component-seam discontinuity: at the .031/.029 seam (2025-12-22 -> 2025-12-23) the 1c component steps $0.00 -> $19,673,469.29, masked at the headline by the 1b residual absorbing -$12.88M (the headline seam reads a smooth +0.649%). .031's 1c=0 (item-(d)-grounded) and .029's 1c ratio-estimate (1.85% x 1a) CONTRADICT -- one is wrong.</origin>
    <the_source_question>.031 item-(d) (commit 265a3f04f) checked the SmartX CONSOLIDATED allocations store (opal-data-smartx-v2/consolidated/smartx_allocations.parquet, Period 202409..202605) and found the 2 SMA-type models entirely absent. BUT .028's live daily-forward 1c = $24,929,683.38 / 94 accounts is pulled by the WS-B feeder from a DIFFERENT SmartX path (the per-model / SMA roster endpoint -- the .027 probe established SmartX exposes per-model + SMA rosters). So item-(d)'s "zero SMA" may be an artifact of probing a store that simply does not carry SMA -- not evidence that SMA did not exist. DS~B itself flagged this: item-(d) proved the consolidated store does not TRACK SMA, which is weaker than "SMA did not EXIST."</the_source_question>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9. WS-B feeder: data/mdpf/scripts/feeders/wsb_49f_smartx_model_aua.py.</prd>
    <pipeline_rule>Non-mutating probe -- Rule 14 (ds-commit-gate) on any probe script; no Rule-13 deploy (no producer change). No emoji.</pipeline_rule>
  </references>

  <context>
    The MDPF v0.9 historical line is fully BUILT (.028+.029+.030+.031) but the project close is HELD on one unresolved contradiction: is 1c (SMA) real or zero across the historical ranges? The two tiers disagree -- .031 set 1c=0 for 2024-11-01..2025-12-22; .029 carries a 1.85%-of-1a ratio-estimate for 2025-12-23..2026-05-19. The probe resolves which is correct by checking the AUTHORITATIVE SMA source (the WS-B feeder's actual SMA roster path, not the consolidated store) and pinning the real SMA-program launch date.
  </context>

  <scope>
    <step>Phase 1 -- IDENTIFY the authoritative SMA source. Read wsb_49f_smartx_model_aua.py: confirm exactly which SmartX endpoint / path the feeder pulls the 2 SMA-type models (opal_growth_sma, opal_div_sma) from to produce the live .028 1c = $24.93M / 94 accounts. This is the per-model/SMA roster endpoint, NOT the consolidated allocations store item-(d) probed -- confirm the precise source.</step>
    <step>Phase 2 -- SMA PRESENCE across both historical ranges. Against that authoritative source, check for SMA presence/value across BOTH: the .031 range (2024-11-01..2025-12-22) AND the .029 range (2025-12-23..2026-05-19). Does the source expose historical SMA data, and if so, is SMA non-zero in each range?</step>
    <step>Phase 3 -- PIN the real SMA-program launch date. Establish, positively (not inferred from the .029/.031 boundary), when the SMA program began. The cleanest pins (DS~B-suggested): the 94 SMA allocations' OpenedOnDate / account-open dates via the WS-B feeder's SmartX data; or the SmartX live-API SMA-model history. A launch date landing implausibly exactly on the .029/.031 methodology boundary (2025-12-23) MUST be positively confirmed from the data, never accepted as a coincidence.</step>
    <step>Phase 4 -- route the finding to CTO~B (CC COO~B): the authoritative source, the SMA presence per range, the pinned launch date, and which of the three outcomes (below) holds. CTO~B rules the methodology fix off the finding. NON-MUTATING -- the probe writes no partition; it produces a brief.</step>
  </scope>

  <outcomes>
    Per CTO~B's ruling -- the probe finding maps to one of three outcomes, each with a defined fix CTO~B rules off:
    <outcome id="a">SMA real across BOTH ranges -> .031's 1c=0 is WRONG. .031's 1c + 1b re-derive (1c per a method CTO~B rules -- the .029 ratio-estimate or a source-direct value; 1b recomputed = calibrated_Schwab - 1a - 1c); .031 re-runs the affected partitions. .029 stands.</outcome>
    <outcome id="b">SMA real only from ~2025-12-23 -> .031's 1c=0 is right AND .029's 1c is right; the seam is a GENUINE SMA-program-launch step -- legitimately marked, not smoothed. Requires the Phase-3 launch date to POSITIVELY confirm a real launch at/near that date (not a boundary coincidence).</outcome>
    <outcome id="c">SMA never real in either historical range -> .029's 1c ratio-estimate is a PHANTOM layer. .029 (closed / RAVC-accepted) RE-OPENS for a 1c=0 fix; .031's 1c=0 is right. (Closed is not immune to a new empirical finding.)</outcome>
  </outcomes>

  <acceptance_criteria>
    <ac id="AC1">The authoritative SMA source the WS-B feeder uses (the path producing the live .028 1c=$24.93M/94-account figure) is identified from wsb_49f_smartx_model_aua.py -- not assumed.</ac>
    <ac id="AC2">SMA presence/value is checked against that authoritative source across BOTH the .031 range (2024-11-01..2025-12-22) and the .029 range (2025-12-23..2026-05-19).</ac>
    <ac id="AC3">The real SMA-program launch date is pinned positively from the data (account OpenedOnDate or SmartX SMA-model history) -- a boundary-coincident date is positively confirmed, never inferred.</ac>
    <ac id="AC4">The finding maps explicitly to outcome (a), (b), or (c) and is routed to CTO~B CC COO~B. Non-mutating -- no partition rewritten, no producer changed. ds-commit-gate on any probe script; no emoji; session log + brief.</ac>
  </acceptance_criteria>

  <deliverables>
    - A brief: the authoritative SMA source, SMA presence per range, the pinned launch date, the outcome (a/b/c). Routed to CTO~B CC COO~B.
    - Session log with the Compiler Tools section.
  </deliverables>

  <coo_close date="2026-05-21" by="2.0.0_SA_COO~B">
    MDPF_ASSETS.032 COMPLETE -- CLOSED. DS~B brief docs/briefs/mdpf-assets-032-1c-sma-source-probe-20260521.md (commit 3308f0d34). A non-mutating read-only probe; the finding is the deliverable, and CTO~B has ruled the methodology fix off it (141723Z) -- the probe has fully served its purpose.

    FINDING -- OUTCOME (a): SMA is REAL across both the .031 and .029 ranges. AC1 -- the authoritative SMA source identified from wsb_49f_smartx_model_aua.py: the SmartX enterprises/allocations endpoint (per-model, the 2 SMA model_ids resolved), NOT the consolidated allocations store item-(d) probed. AC2 -- SMA presence checked against that source across both ranges: present in both; 82 SMA accounts open entering the .031 range, 94 now / ~$24.77M (cross-checks .028's live 1c). AC3 -- the SMA program launch date pinned POSITIVELY: 2021-09-02 (the MIN openedDate across all SMA allocations open+closed), 3+ years before the .031 range -- a data pin, not a boundary inference. AC4 -- routed to CTO~B CC COO~B; non-mutating, no partition rewritten. All ACs MET.

    OUTCOME: .031's 1c=0 is WRONG -- item-(d) was a wrong-source artifact (the consolidated store does not track the SMA models). .029's ratio-1c stands (no .029 re-open; subject to a quick within-tolerance confirm). The fix lands as MDPF_ASSETS.031 amendment A4 (the CTO~B-ruled SMA-trajectory 1c re-derive + the 297-partition re-run) -- .032 the probe is discharged; the fix is .031's. DS~B also self-corrected the verification practice: probe the producer's actual source path, not an adjacent store that may not carry the artifact.
  </coo_close>
