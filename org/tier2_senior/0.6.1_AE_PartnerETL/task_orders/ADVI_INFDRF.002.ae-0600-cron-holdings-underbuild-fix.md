<task_order>
  <metadata>
    <id>ADVI_INFDRF.002</id>
    <slug>ae-0600-cron-holdings-underbuild-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-15 -- Andrew-flagged URGENT. Root-cause + fix; no gate.</dispatch_unblock_condition>
    <project_code>ADVI_INFDRF</project_code>
    <priority>P1 -- Andrew-flagged URGENT. The 06:00 daily cron systematically under-builds canonical holdings; the Inflection portal serves short-holdings numbers most of every day until an on-demand full chain corrects it. Live data-quality defect.</priority>
    <sla>Fast -- Andrew wants it quick. Root-cause + fix + a verifying chain run.</sla>
  </metadata>

  <references>
    <diagnosis>DS~A BE root-cause diagnosis 2026-05-15 (Andrew-flagged URGENT). Evidence: gold/canonical/holdings_2026-05-15.parquet 06:00 version = 11,413 rows / 801 accounts / mv 204.6M; 17:57Z full-chain version = 29,552 rows / 865 accounts / mv 203.8M (== canonical header total.aua exactly). holdings_2026-05-14 showed the same pattern (06:00 short, fixed only by a 20:49Z from-INF_B_00 run). DS~A's read: CHAIN_INCREMENTAL omits INF_B_00 (canonical_holdings).</diagnosis>
    <directive>Andrew direct 2026-05-15 -- flagged the Inflection live-portal data drift URGENT.</directive>
    <context_note>AE 0.6.1 authored the ADVI_INFINC incremental-pipeline design brief (commit 2920719f8) -- it holds the chain-mode / CHAIN_INCREMENTAL context. This TO is routed to AE 0.6.1 for that reason.</context_note>
  </references>

  <context>
    The "Segment Analytics WA count 685 -> 744" drift symptom Andrew flagged has its root cause here: the 06:00 daily cron produces a SHORT gold/canonical/holdings_{date}.parquet (2026-05-15: 11,413 rows / 801 accounts vs the correct 29,552 / 865), and the portal serves those short numbers until an on-demand full chain re-runs and corrects them. 744 is the CORRECT WA count; 685 was the short-build regression. DS~A's read is that the incremental chain mode (CHAIN_INCREMENTAL) omits INF_B_00 (canonical_holdings) from the daily build. This is an AE chain-orchestration / cron-mode root-cause-and-fix task.
  </context>

  <objective>
    The 06:00 daily Inflection cron produces a COMPLETE gold/canonical/holdings_{date}.parquet -- the same full canonical holdings the on-demand full chain produces -- so the portal serves correct holdings-derived numbers from 06:00 onward, with no need for an on-demand full chain to correct it.
  </objective>

  <scope>
    <item>ROOT-CAUSE -- confirm DS~A's read: determine exactly why the 06:00 build is short. Is CHAIN_INCREMENTAL (in orion-gold-dispatch.sh) omitting INF_B_00 (canonical_holdings)? Is the 06:00 cron invoking the wrong chain mode? Is INF_B_00's omission from incremental intentional-but-wrong-for-this-cron, or an outright bug? Characterize before fixing.</item>
    <item>FIX -- make the 06:00 daily cron produce complete canonical holdings. Depending on the root cause: include INF_B_00 in the chain mode the 06:00 cron uses, or point the cron at a mode that does. Respect the ADVI_INFINC incremental-pipeline architecture -- the goal is a CORRECT daily build, not necessarily a full 70-min rebuild; if INF_B_00 / canonical_holdings genuinely must run daily, that is the fix.</item>
    <item>DEPLOY -- any Terraform/cron change per CLAUDE.md Rules 1/9; orion-gold-dispatch.sh changes per the EC2 / dispatch deployment standard (S3 artifact model). Verify with a chain run.</item>
    <item>SCOPE BOUNDARY -- this is the chain-orchestration / cron fix. The INF_D_04 geo count-reconciliation defects are ADVI_INFDRF.001 (DS~A). Do not fix INF_D_04 logic here.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">Root cause of the 06:00 short holdings build identified + documented (why CHAIN_INCREMENTAL / the 06:00 cron omits INF_B_00 / canonical_holdings).</ac>
    <ac id="AC2">Fix applied -- the 06:00 daily cron build produces a complete gold/canonical/holdings_{date}.parquet (row/account count + mv matching the full-chain output, == canonical header total.aua).</ac>
    <ac id="AC3">Deployed per CLAUDE.md (Terraform for any cron/infra change; orion-gold-dispatch.sh per the EC2/dispatch standard); tagged + pushed if a pipeline change.</ac>
    <ac id="AC4">Verified by a chain run / the next 06:00 cron fire: the daily holdings build is complete. Smoke-test + validate per Andrew's /loop directive -- compare the daily-build holdings parquet against the full-chain baseline; carry the evidence in the RAVC2.</ac>
    <ac id="AC5">No emoji in code/logs. If the fix touches the ADVI_INFINC incremental-mode definition, scope is coordinated with ADVI_INFINC (surface to COO).</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>comp-iam if any Lambda/role op changes; comp-blast on orion-gold-dispatch.sh / the affected chain node before changing it; deployed-verify after.</compiler_tools_mandate>

  <cross_domain_coordination>
    ADVI_INFINC overlap -- CHAIN_INCREMENTAL is the incremental chain mode; you authored the INFINC incremental design brief, so you hold the context. If the fix changes the incremental-mode script set, coordinate the scope with ADVI_INFINC (it is mid-Phase-1) and surface to COO.
    ADVI_INFETL owns the 06:00 cron / EventBridge -- if the fix is cron-config (not chain-mode), coordinate with AE 0.7.0 (the ADVI_INFETL infra owner).
    Sibling ADVI_INFDRF.001 (DS~A) fixes the INF_D_04 geo reconciliation defects -- independent; both feed the same project.
    CHAIN RUN -- coordinate the verifying chain run with COO; there is a pending INFGRO firm_return_pct_twr + ADVI_BIWNDW.002 co-landing INF chain run -- avoid redundant cycles.
  </cross_domain_coordination>

  <deliverables>
    <item>Root-cause writeup + the 06:00-cron-holdings fix deployed + verified by a chain run.</item>
    <item>Session log + RAVC2 to COO + CC DS~A + CC CTO.</item>
  </deliverables>

  <ravc>0.6.1_AE_PartnerETL RAVC2 to COO + CC DS~A + CC CTO on AC1-5.</ravc>

  <notes>
    Andrew-flagged URGENT -- move fast. This is the root cause of the data drift Andrew flagged: the portal serves short-holdings numbers most of every day. DS~A's diagnosis (the S3 object-version evidence) is the input -- characterize the exact mechanism, then fix. You hold the CHAIN_INCREMENTAL context as the INFINC brief author. Coordinate the chain run with COO. No emoji.
  </notes>
</task_order>
