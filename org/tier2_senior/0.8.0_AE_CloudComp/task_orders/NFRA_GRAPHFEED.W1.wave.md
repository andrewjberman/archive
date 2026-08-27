# TO — NFRA_GRAPHFEED.W1 — the graph-feed wave (6 sequenced items, Andrew GO LD-0299)

<task_order>
  <to_id>NFRA_GRAPHFEED.W1</to_id>
  <project>NFRA_GRAPHFEED</project>
  <issued_by>0.0.0_AB_MSTR (wave owner; Andrew-direct GO 2026-07-15 ~18:5xZ, verbatim in LD-0299)</issued_by>
  <issued_to>0.8.0_AE_CloudComp~Z</issued_to>
  <status>complete -- SPRING-CLEAN 2026-08-25 (S2): <project> field repaired from "NFRA_GRAPHFEED (registration in flight at COO; authority = L" to NFRA_GRAPHFEED, which is closed. Closed as a record act, not a work verdict. Prior status: pending</status>
  <priority>P1 (Andrew: "Start with 1) as that is the highest leverage, but proceed through all 6 items")</priority>

  <context>
    Evidence base: org/tier0_exec/0.0.0_AB_MSTR/deliverables/NFRA_GRAPH_ESTATE_ASSESSMENT_20260715.md
    (LD-0298 @ 263124baf) — read it FIRST; every claim below carries its instrument + vintage there.
    This is a SEQUENCED list per XXX.md batch-GO law: execute in order, skip nothing silently,
    stop only on an unmet dependency, and report each close with evidence (RAVC). CTO holds the
    arch gate on every TF diff/apply and every tool registration. Item 2 of Andrew's six (the
    GLOBGRPH_CODEHEAT_ENABLED=1 flip) is CTO's leg directly — your TO-2 below is the VERIFY half.
  </context>

  <work_items>

    <item id="TO-1" title="STANDING CSE EMITTERS — the loop's food supply (HIGHEST LEVERAGE, do first)">
      Problem: iceberg.globgrph.cse is STATIC at 342 events since the 07-09 SEMCTL close — the whole
      observation stack (FEDOBS 04:30Z nightly, MOTIF co-occurrence, PROMOTE effectiveness) federates
      over a frozen seed corpus. Emitter scripts EXIST (infra/aws/globgrph/cse_emit_{agent,deploy,
      frontend_coevolution,graphhead,promote}.py) but nothing standing runs them; the graph_head --full
      (~55k substantive events) stream is a defined-but-unlanded NFRA_CSE follow-on.
      Build: (a) the graph_head --full backfill (one-shot, appends to the append-only C0 log);
      (b) scheduled per-producer emits — follow the PROVEN globgrph producer pattern
      (fedobs_producer.tf: EventBridge cron -> one-shot Fargate task), sequenced AFTER the 02:00
      derive so vintages track the graph; CTO rules the exact schedule shape on your diff (same
      question class as LIVELEARN G1 — his ruling binds); (c) stamp cse in the branch-head marker
      (today: "cse: ABSENT FROM MARKER -- vintage unverifiable"; fix at the writer, both derive_runner
      stamp path and incremental_updater).
      Constraints: ADDITIVE ONLY — zero mutation of graph_nodes/graph_edges write paths; emitters
      idempotent (stable event_ids; re-run adds zero duplicates); a CSE-emit failure must never fail
      the nightly derive (mirror the best-effort pattern at derive_runner.py:1966-1975).
    </item>

    <item id="TO-2" title="VERIFY the codeheat flip (CTO executes the flip — item 2 is his)">
      After CTO's GLOBGRPH_CODEHEAT_ENABLED=1 apply lands: verify next scheduled run produces
      code_heat vintage &lt;30h (the freshness_alarm registry threshold) and comp-learns-status stops
      self-flagging BEHIND (today: lag=153.3h, binding=code_heat). Report the before/after pair.
    </item>

    <item id="TO-3" title="comp-axes v1 — the axis directory + the missing delta store">
      Build the THIN aggregator (LD-0298 sec-4): (1) DIRECTORY mode — every analytic axis with live
      vintage + top-3 entries + canonical drill command (hot/cold->comp-heat, danger->comp-pulse,
      data-freshness->comp-freshness, debt->comp-debt, debris->comp-debris, depth->comp-depth,
      gaps->comp-learns-status, signals->comp-fedobs). READ-ONLY aggregation — compute NOTHING new,
      call the existing readers; (2) SNAPSHOT mode — on each run append one dated row per axis to an
      append-only store (org/modules/graph/axes_history.jsonl + S3 mirror under the globgrph
      warehouse), giving every axis its first queryable time-series; (3) DELTA mode — diff two dated
      rows ("what got hotter/colder/more-dangerous since &lt;date&gt;"). Register per the COMPCLOSE
      registration invariant: manifest + tools_index + coverage-map + comp-which curated rule +
      routing-test additions; comp-manifest-check must PASS. CTO registration gate.
    </item>

    <item id="TO-4" title="comp-which top-k (Andrew 07-13 directive; COMPASSURANCE PRD)">
      Implement top-k retrieval per docs/architecture/NFRA_COMPASSURANCE_COMPWHICH_TOPK.md (Andrew
      verbatim: "top-5 with attached description"). HARD regression guard: the routing baseline that
      PASSED 2026-07-15 (org/tier2_senior/0.8.0_AE_CloudComp/deliverables/comp-which-routing-baseline.json
      + comp-which-routing-test.py: zero pollution, 100% gibberish abstention) must still pass; and
      measure the zero-result rate before/after on the live rail log (the corrected ~34% is the number
      this attacks — COMPASSURANCE §0 errata is the measurement law: full tally, no filtered grep).
    </item>

    <item id="TO-5" title="MSGRAPH S3 heat-map — GO condition met, execute">
      org/projects/NFRA_MSGRAPH/task_orders/NFRA_MSGRAPH.S3.heat-map.md was authored-ahead with GO
      held on "live MS nodes flowing into comp-kuzu" — that condition is MET (LD-0298: 4,498 MS_FILE
      + 1,021 MS_FOLDER verified in canonical kuzu at pin==HEAD). COO is formally re-staffing the TO
      to you; execute it as written once his re-staff lands (write-heat over last_modified_dt already
      carried on every MS_FILE). Component-3 (findability comp-tools) is NOT yours to start — CTO+COO
      are decomposing it; breadth widening awaits an Andrew scope word.
    </item>

    <item id="TO-6" title="Hygiene singles">
      (a) RCA + fix the kuzu incremental-updater failover (comp-kuzu today: "incremental refresh rc=2
      -> full reload fallback" = the ~10min cold path; make incremental succeed or make rc=2 loud);
      (b) disposition graph_contracts (last-write 695h — static-by-design or dead producer? document
      or fix, with evidence); (c) supply COO the current-state text for the stale NFRA_MSGRAPH.json
      registry refresh (his record, your facts).
    </item>

    <item id="TO-7" title="TRINO-LAYER-WIDE DELTA — exploration + design (Andrew-direct via COO 215450Z; LD-0299 AMENDMENT-1 @ 398f7124b; appended by COO per MSTR 215702Z, record-parity with the already-binding GO)">
      Andrew, VERBATIM (COO terminal ~21:5xZ): "this is something i wanted to explore for the trino
      layer as a whole, as we need delta on the trino analytics. i would refer it back to MSTR and
      0.8.0_AE~Z." Assessment-first per the LD-0298 pattern:
      (a) enumerate EVERY Trino analytics surface (code_heat, tool_activity, obs_findings,
      fedobs_observations, the comp-axes history store, node_health-unmaterialized, ms_heat-to-be)
      and rule which gets a DATED APPEND-ONLY SNAPSHOT SIBLING in Iceberg so day-over-day delta is
      a first-class Trino query; (b) ONE standard table shape + naming convention for delta-tracked
      analytics — the OPAL_STNDRD seam, one coordination line with 0.7.0~Z's nomenclature scope;
      (c) ms_heat = the concrete first instance (~5.5K rows/day, rides the ruled nightly-post-derive
      leg); (d) deliverable = design brief to CTO's gate; ANY DDL/derive-leg diff is CTO-gated per
      the standing wave rule. Sequenced AFTER TO-5; read-only exploration may interleave. TO-3's
      snapshot/delta store is the acknowledged primitive this generalizes.
    </item>

  </work_items>

  <compiler_tools_mandate>
    Before write: comp-which for every search (rail law); comp-kuzu for graph ground-truth (read the
    provenance header, note per-table vintages). Before commit: commit-gate auto; comp-manifest-check
    for any .tools/comp-* addition (registration invariant); comp-iam service + aws iam
    simulate-principal-policy (ONE --resource-arns per call, positive control SEPARATE, per Rule 22a)
    for ANY new IAM against new resources (EventBridge->ECS run-task, S3 mirror writes). After
    commit/deploy: verify on the LIVE primitive (a comp-tool DESIRED verdict is not an applied claim
    — Rule 22a); comp-fedobs vintage header is the TO-1 oracle.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    infra/aws/globgrph/* + infra/aws/terraform/globgrph/*: shared with 0.7.0_AE_CloudOps (derive-image
    rebuilds coordinate through 0.7.0 per the standing fedobs pattern — MCP them BEFORE any image
    rebuild) and with CTO (every apply). .tools/ + org/modules/graph/: comp-tool registry surface —
    CTO registration gate; do not collide with base-0.8.0's OPAL_CONSOLIDATION paths (your lane is
    NFRA-only per Andrew's standing ~Z ruling). MSGRAPH S3: COO owns the TO re-staff record.
  </cross_domain_coordination>

  <acceptance_criteria>
    TO-1: (1) cse_log_total &gt; 342 after the backfill AND strictly increasing across 2 consecutive
    scheduled runs, read from the SERVED comp-fedobs vintage header (not producer self-report);
    (2) comp-kuzu provenance header shows a stamped cse vintage (the ABSENT-FROM-MARKER line gone);
    (3) idempotency proof: re-run of each emitter adds 0 rows (event_id dedup, shown by count-before/
    count-after); (4) graph_nodes/graph_edges snapshot ids UNCHANGED by any emitter run.
    TO-2: code_heat computed_at &lt;30h on the morning after CTO's flip + comp-learns-status header
    shows binding fresh (BEHIND flag absent). Before/after pair quoted.
    TO-3: comp-axes directory prints all 8 axes each with a real vintage; two runs &gt;=24h apart
    produce 2 dated rows per axis in the history store; delta mode renders a nonzero diff on at least
    one axis; comp-manifest-check PASS; comp-which routes an axis-shaped question to it.
    TO-4: routing self-test PASS against the frozen baseline (zero pollution, 100% gibberish
    abstention preserved); top-5-with-descriptions served; zero-result rate re-measured on the full
    rail tally with the denominator printed.
    TO-5: per the S3 TO's own ACs (it is authored); plus write-heat visible on MS nodes in comp-kuzu.
    TO-6: (a) comp-kuzu cold path: incremental succeeds (no rc=2 fallback) on a HEAD-advance refresh,
    or the fallback is loud+explained; (b) graph_contracts disposition written with evidence;
    (c) COO confirms registry refresh landed.
    EVERY close: session log with Compiler Tools section (org/ref/SESSION_LOG_STANDARD.md) — a TO
    with no compiler check logged is NOT accepted complete (TO_COMPILER_GATE).
  </acceptance_criteria>

  <deliverables>
    Per-item RAVC closes to 0.0.0_AB_MSTR (wave owner) with evidence, CC 1.0.0_SA_CTO (gates) +
    2.0.0_SA_COO (record); session logs per standard; commits via safe-commit under your own author
    line through commit-gate.
  </deliverables>
</task_order>
