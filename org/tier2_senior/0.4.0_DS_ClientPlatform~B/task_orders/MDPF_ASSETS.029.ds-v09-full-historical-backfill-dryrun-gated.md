<task_order>
  <metadata>
    <id>MDPF_ASSETS.029</id>
    <slug>ds-v09-full-historical-backfill-dryrun-gated</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-05-20 (authored on .028 RAVC-accept + CTO~B .029-scoping directive)</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO'd 2026-05-20 by 2.0.0_SA_COO~B on the .028 RAVC-accept (CTO~B output-confirm). The GO covers PHASE 0 ONLY -- a non-mutating dry-run + mechanism validation. PHASE 1 (the actual historical partition rewrite) is HARD-STOPPED inside this TO: it does NOT execute on this GO; it is an explicitly-Andrew-gated second step (CTO~B carries the Phase-0 dry-run findings + a go/no-go-to-rewrite recommendation to Andrew; COO~B flips the Phase-1 gate only on Andrew's sign-off).</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF critical path. The .016-equivalent historical backfill, re-scoped to PRD v0.9. Brings the full aggregate_aua_timeseries historical series onto the v0.9 full-Schwab-49F basis. SUPERSEDES the .016 Option-(a) split-basis (which split at 2026-03-11 only because certified_aua's earliest partition was 03-11 -- moot under v0.9, since Schwab + SmartX both have daily data back to 2024 per Andrew 2026-05-20).</priority>
    <sla>Phase 0: ~1h DS wall -- a non-mutating dry-run + a small scratch-location sample validation + the findings brief. [SLA CORRECTED 2026-05-20 by 2.0.0_SA_COO~B, from a wildly over-padded "~3-5h" -- a padded SLA suppresses stall-detection: .029 sat un-picked-up ~2h under cover of the inflated number. Track this TO by its work ARTIFACT (the .029 session log + commits + brief on origin), NOT by an elapsed-SLA clock; if 30-40min pass post-session-engagement with no .029 log appearing, escalate to CTO~B.] Phase 1 (Andrew-gated, NOT on this GO): ~2-3h -- the partition rewrite + verification.</sla>
    <deadline>Phase 0 prompt -- it gates the Andrew go/no-go. Phase 1 has no date; it ships when Andrew signs off.</deadline>
  </metadata>

  <references>
    <prd>docs/architecture/MDPF_ASSETS.md PRD v0.9 (8951ce8f0) -- §3.4 + §3.0.1 the formula of record. 49F = full Schwab 49F book; 1b = Schwab_49F_whole - 1a - 1c (SMA-exclusive); aggregator 3-term.</prd>
    <origin>CTO~B .029-scoping directive 2026-05-20, on the .028 RAVC-accept. Andrew 2026-05-20: Schwab + SmartX both have daily data back to 2024 -> the WHOLE historical series can backfill accurately on v0.9, superseding the .016 split-basis. Andrew constraint, verbatim intent: "be ginger / nondestructive until we know for sure how we're gonna do it."</origin>
    <predecessor>.028 (v0.9 49F re-scope, COMPLETE 2026-05-20, commit dd3cd4d22) shipped the v0.9 daily-forward methodology -- WS-E 1b SMA-exclusive residual + aggregator 3-term. .029 applies that same v0.9 methodology to the HISTORICAL series. .016 (the v0.7/v0.8-era backfill) stays closed as historical record; .029 is a fresh TO.</predecessor>
    <hard_constraint>Andrew "be ginger / nondestructive." The historical aggregate_aua_timeseries partitions are NOT to be rewritten until the v0.9 backfill methodology is proven on a dry-run and Andrew has explicitly signed off. Phase 0 is non-mutating by construction; Phase 1 is the gated rewrite.</hard_constraint>
    <pipeline_rule>Rule 13/14/15 apply to any Phase-1 code. Phase 0 is non-mutating (no commit, no deploy, no partition write).</pipeline_rule>
  </references>

  <context>
    .028 put v0.9 live daily-forward. The historical aggregate_aua_timeseries series is still on the older bases (the .016 backfill was v0.7/v0.8-era, with the Option-(a) 2026-03-11 split forced by certified_aua's start date). Under v0.9 the 49F basis is the full Schwab book, and Schwab + SmartX both have daily data to 2024 -- so the whole series CAN be re-materialized on one consistent v0.9 methodology, no split. But rewriting historical partitions is destructive; per Andrew's "be ginger" directive this TO proves the methodology on a non-mutating dry-run FIRST, and the actual rewrite is a separate Andrew-gated step.
  </context>

  <scope>
    <step>PHASE 0 -- DRY-RUN + MECHANISM VALIDATION (this GO; NON-MUTATING). No partition is written, no artifact mutated, no S3 object overwritten. Produce:
      (a) BACKFILL MECHANISM -- how the v0.9 historical series is re-materialized: the per-date inputs (Schwab 49F whole via the crosswalk + SmartX 1a/1c), the date range (target: full series to 2024), the script/path plan.
      (b) PARTITION-WRITE PLAN -- exactly which aggregate_aua_timeseries partitions/objects Phase 1 would rewrite, and how (overwrite-in-place vs versioned vs side-by-side), with the blast radius (downstream consumers of the historical series).
      (c) SAMPLE VALIDATION -- re-materialize a SMALL sample of historical dates v0.9-style IN A SCRATCH LOCATION (not the live series), and validate them: at least one sample date cross-checked against the live .028 v0.9 daily-forward run for an overlapping date (must reconcile), plus plausibility on older dates (no $0 1a, day-over-day within market bounds).
      (d) RISK / blast radius -- what breaks if the rewrite is wrong; the rollback story.</step>
    <step>PHASE 0 deliverable -- a dry-run findings brief at docs/briefs/, routed to 1.0.0_SA_CTO~B (CC 2.0.0_SA_COO~B). HARD STOP here. Do NOT proceed to Phase 1. CTO~B reviews the brief + carries a go/no-go-to-rewrite recommendation to Andrew.</step>
    <step>PHASE 1 -- HISTORICAL PARTITION REWRITE. DISPATCH-HELD / EXPLICITLY ANDREW-GATED. Does NOT execute on this TO's initial GO. Only after Andrew signs off the rewrite (via CTO~B) does COO~B flip the Phase-1 gate. Phase 1 then: re-materialize the historical aggregate_aua_timeseries on the v0.9 methodology per the approved plan; per-date methodology_version=v0_9; preserve a rollback path; Rule 13 commit + deploy; verify the rewritten series reconciles + the daily-forward/.028 boundary is clean.</step>
    <step>PHASE 1 deliverable (post-Andrew-gate) -- RAVC2 to COO~B CC CTO~B: the rewrite transcript, the full-series reconciliation, the boundary check, deployed commit + S3 MATCH.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC0">PHASE 0 is fully non-mutating -- no partition write, no artifact mutation, no S3 overwrite, no commit. [If any mutation is needed to validate, it goes to a scratch location, never the live series.]</ac>
    <ac id="AC1">Phase-0 brief delivers (a) mechanism, (b) partition-write plan + blast radius, (c) a sample-date validation incl. at least one overlapping-date cross-check vs the .028 v0.9 daily-forward run, (d) risk/rollback. Routed to CTO~B CC COO~B.</ac>
    <ac id="AC2">HARD STOP after Phase 0 -- Phase 1 does NOT execute on this GO. The TO records that the rewrite is gated on an explicit Andrew sign-off relayed via CTO~B.</ac>
    <ac id="AC3">[Phase 1, post-Andrew-gate only] Historical aggregate_aua_timeseries re-materialized on v0.9; per-date methodology_version=v0_9; the daily-forward boundary with .028 reconciles; rollback path preserved; Rule 13 deploy; RAVC2.</ac>
  </acceptance_criteria>

  <out_of_scope>
    The legacy-emit re-scope (build_legacy_compat_emit.py -> v0.9) -- separate TO MDPF_ASSETS.030, gates on this TO. Re-opening .016 (closed, historical record). The daily-forward v0.9 methodology (.028, already live). Any partition rewrite WITHOUT the explicit Andrew sign-off -- structurally forbidden by AC2.
  </out_of_scope>

  <deliverables>
    - Phase 0: a non-mutating dry-run + mechanism-validation brief (docs/briefs/), routed to CTO~B CC COO~B. HARD STOP.
    - Phase 1 (post-Andrew-gate): the v0.9 historical re-materialization + RAVC2.
  </deliverables>
</task_order>
