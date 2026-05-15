<task_order>
  <metadata>
    <id>ADHC_COMPIL_V4.030</id>
    <slug>ae-comp-blast-check-consumers</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-14</date>
    <status>active</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>UNBLOCKED — Wave 3 RAVC2 received (890f8d2fe). Wave 4 dispatched 2026-05-15. .030 retitled per CTO ratify (Option C): scope generalized to phantom-consumer-class sweep via `comp-blast --check-consumers`.</dispatch_unblock_condition>
    <project_code>ADHC_COMPIL_V4</project_code>
    <priority>P1 — phantom-consumer sweep diagnostic; ADHC_TRIGMRK + ADHC_LEDGEH + ADHC_FECACHE_COHERENCE + ADHC_BPMVH companion (4-project ADHC defense-in-depth corpus structural cousin)</priority>
    <sla>~1 day wall per PRD §15.4 sizing (unchanged; scope generalize doesn't expand implementation surface significantly since comp-blast already walks downstream dependency-chain)</sla>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-030 (update pending; retitle absorbed at next ratchet pass)</ref>
    <ref type="anchor_incidents">AE 0.6.1 ADHC_TRIGMRK 3-incident anchor (chain_full_20260514_141419 + earlier same-day + 18:14Z incident #3 "Lambda emits pending-marker assuming dispatcher daemon that doesn't exist"). Three defects all instances of single phantom-consumer pattern per CTO ratify framing.</ref>
    <ref type="cto_ratify">CTO MCP 2026-05-14 ~19:0XZ — Option C `comp-blast --check-consumers` flag extension ENDORSE. Semantic alignment (comp-blast answers "what breaks if I change X?" → zero consumers = phantom). Reuse over new subcommand. CI-friendly exit-code semantics (exit 0 if ≥1 consumer; exit 1 if zero). Supersedes T7 `comp-trace --check-consumer` framing.</ref>
    <ref type="phantom_consumer_pattern">[[feedback-phantom-consumer-marker-pattern]] memory entry (CTO §3.4 cross-reference target; COO authors as memory batch entry #10). Generalized rule: before emitting marker/event/signal, verify consumer exists + has corresponding handler wired.</ref>
    <ref type="defense_in_depth_corpus">4-project ADHC corpus: LEDGEH `5362d0295` + FECACHE_COHERENCE `120df453` + BPMVH `49f2af6fd` + TRIGMRK `2b5e8b39b`. This tool surfaces structural class shared across the corpus (TRIGMRK is the most-direct instance).</ref>
    <ref type="cross_link">Wave 4 sibling: .025 skipgate + .032 vectorize-audit. Related-but-orthogonal-concern to .025 — phantom-consumer vs partition-coverage. Sister to v0.6 candidate `comp-validate fe-cache-freshness` (DE 0.4 brief `ebce828ac`).</ref>
  </references>

  <context>
    Producer/consumer wire boundaries in the system can fail in two structurally distinct ways:

    **Wire-protocol-divergence** (e.g. ADVI_SHARED.006 `?firm=` vs `?firmId=`): both producer and consumer exist; they disagree on the wire-format. Recovery via bidirectional translator pattern.

    **Phantom-consumer** (e.g. ADHC_TRIGMRK incident #3 Lambda pending-marker no-daemon): producer emits but consumer was never built. Silent failure — producer "succeeds" but downstream effect is null. **This TO surfaces the phantom-consumer class structurally.**

    `comp-blast` already walks downstream dependency-chain for any node — it answers "what breaks if I change X?" by enumerating downstream consumers. **Adding `--check-consumers` flag exits 0 if ≥1 consumer enumerated, exit 1 if zero.** Direct integration into pre-commit gates + `safe-deploy.sh` pre-flight checks + CI nightly drift detection.

    **Coverage scenarios:**
    - Single-node check: `comp-blast {producer} --check-consumers` → exit 0/1
    - Sweep mode: `comp-blast --check-consumers --all-producers` → list ALL producer nodes with zero consumers (CI-suitable for nightly drift detection)
    - Pre-commit gate: `.tools/safe-deploy.sh` adds `comp-blast --check-consumers ${produces_marker_lambdas}` before terraform apply

    **Producer-class coverage:**
    - S3 emit (gold script writes platinum artifact)
    - Lambda emit (Lambda writes S3 marker or invokes downstream)
    - SSM Parameter write (Lambda writes parameter; consumer reads via boot script or daemon)
    - Chain marker emit (`gold/trigger-mode.json`, `pipeline-complete.json`, `chain-trigger.json` per TRIGMRK incident anchor)
    - SQS publish (Lambda publishes; consumer Lambda subscribes)
    - SNS publish (similar)
    - Schema version emit (`gold/meta/schemas/{script_id}.json`)
    - Partition provenance emit (`gold/meta/partition_provenance/{script_id}/{date}.json`)
    - Skip-coverage manifest (`gold/meta/skip-coverage/{script_id}.json`)
    - Empty-sentinel emit (`gold/meta/empty/{script_id}/{date}.empty`)

    **Stale-marker as derivable special case:** producer emits marker `M` to S3 path `P`. Consumer `C` reads `P` and gates on freshness. If `C` doesn't exist (zero-consumer case) → stale-by-design (the original .030 stale-marker scope). General phantom-consumer detection covers both stale-marker and post-Path-2-cutover marker-class disappearance scenarios.
  </context>

  <objective>
    Add `--check-consumers` flag to existing `comp-blast` tool. Detects producer nodes with zero downstream consumers across producer-classes enumerated above. CI-suitable exit-code semantics. Sweep mode + per-pipeline scope. Retroactive validation on ADHC_TRIGMRK 3-incident anchor + ADHC_LEDGEH wire-boundary + ADHC_FECACHE_COHERENCE FE-cache + ADHC_BPMVH bronze-pmv axes.
  </objective>

  <scope>
    <files>
      <file action="modify">.tools/comp-blast (add `--check-consumers` flag; reuse existing downstream-walk infra)</file>
      <file action="modify">org/modules/graph/comp-tools.yaml (registry update for new flag; +exit-code semantics doc)</file>
      <file action="create_optional">org/modules/graph/phantom-consumer/{pipeline}.yaml (per-pipeline phantom-consumer baseline for nightly drift detection; OPTIONAL pending sweep-mode usage)</file>
      <file action="readonly_reference">docs/architecture/ADHC_COMPIL_V4.md §15.4 TO-030 (retitle absorbed at CTO next ratchet pass)</file>
      <file action="readonly_reference">docs/architecture/ADHC_TRIGMRK.md §3.4 phantom-consumer pattern banking (CTO canonical 2b5e8b39b)</file>
    </files>
  </scope>

  <phase id="1" when="before write">
    <step>
      <run>comp-blast inf-gold-trigger (existing tool surface verify)</run>
      <expect>Tool walks downstream from Lambda; enumerates S3 paths written + downstream consumers per existing dependency-chain logic.</expect>
      <if_mismatch>If tool doesn't surface marker emits, --check-consumers extension requires graph-data extension first; document scope expansion.</if_mismatch>
    </step>
    <step>
      <run>grep -rn "gold/meta/\|pipeline-complete\.json\|chain-trigger\.json" data/orion/scripts/gold/ infra/aws/lambda/inf-gold-trigger/ | head -30</run>
      <expect>Marker writer call sites enumerated (preserve original .030 stale-marker scope as the special case).</expect>
    </step>
    <step>
      <run>aws s3 ls s3://opal-data-inf/gold/meta/ + aws ssm describe-parameters --parameter-filters Key=Name,Option=BeginsWith,Values=/inf/ (TRIGMRK Path 2 SSM Parameter `/inf/gold/last-trigger-mode` per canonical)</run>
      <expect>Manifest-pair baseline established across S3 + SSM Parameter producer-classes.</expect>
    </step>
  </phase>

  <phase id="2" when="implementation">
    <step>
      <run>Add `--check-consumers` flag to comp-blast. Logic: walk downstream from {node}; if downstream-consumer count == 0, exit 1 with diagnostic; else exit 0.</run>
      <expect>~30-50 LOC addition; reuses existing walk infra.</expect>
    </step>
    <step>
      <run>Add `--all-producers` sweep mode (optional pair with --check-consumers): enumerates all producer nodes in graph; outputs producers with zero consumers.</run>
      <expect>~20-30 LOC addition.</expect>
    </step>
    <step>
      <run>Update org/modules/graph/comp-tools.yaml registry entry for new flag + exit-code semantics doc.</run>
      <expect>Registry reflects flag.</expect>
    </step>
  </phase>

  <phase id="3" when="validation">
    <step>
      <run>comp-blast inf-gold-trigger --check-consumers (PRE-Path-2-cutover state)</run>
      <expect>Exit 1 — TRIGMRK incident #3 anchor empirically validated. Lambda emits markers; consumer daemon doesn't exist; zero consumers.</expect>
      <if_mismatch>If exit 0 surfaces, graph-data must be missing producer-emit nodes. Surface for graph extension.</if_mismatch>
    </step>
    <step>
      <run>comp-blast --check-consumers --all-producers --pipeline inf</run>
      <expect>Sweep mode outputs all INF producer nodes with zero consumers. ADHC_TRIGMRK markers should appear; potentially others discovered.</expect>
    </step>
    <step>
      <run>Retroactive validation against 3-incident TRIGMRK anchor + 4-project ADHC corpus structural cross-check</run>
      <expect>Tool flags marker pair(s) that raced in #1/#2/#3; doesn't false-positive on FECACHE_COHERENCE/BPMVH/LEDGEH (different defect classes; not phantom-consumer).</expect>
    </step>
  </phase>

  <phase id="4" when="post-commit">
    <step>
      <run>Run on BD pipeline scope (--pipeline bd)</run>
      <expect>No crashes; BD-specific producers enumerated; any BD-side phantom consumers surfaced.</expect>
    </step>
    <step>
      <run>Integrate `.tools/safe-deploy.sh` pre-flight check: `comp-blast --check-consumers ${producer_nodes_in_diff}` before terraform apply for Lambdas with marker-emit patterns</run>
      <expect>Pre-deploy phantom-consumer detection blocks safe-deploy if regression detected. Optional follow-on Phase 4 if scope permits.</expect>
    </step>
  </phase>

  <acceptance_criteria>
    AC1: `comp-blast --check-consumers {producer}` exit 0/1 semantics functional
    AC2: `comp-blast --check-consumers --all-producers` sweep mode functional with --pipeline inf/bd scope
    AC3: Retroactive validation: ADHC_TRIGMRK incident #3 anchor (pre-Path-2-cutover state) → exit 1 with diagnostic naming the phantom-consumer Lambda producer
    AC4: Stale-marker subset (original .030 scope) covered as derivable case — markers writers emit to S3 paths; if consumer count = 0, exit 1 flags stale-by-design
    AC5: Producer-class coverage: S3 emit + Lambda emit + SSM Parameter write + chain marker + schema/provenance/skip-coverage/empty-sentinel emits
    AC6: comp-tools.yaml registry updated with new flag + exit-code semantics doc
    AC7: BD pipeline scope test (--pipeline bd) functional without crash
    AC8: Optional Phase 4 .tools/safe-deploy.sh pre-flight integration documented (NOT required for this TO close; opens follow-on)
    AC9: No false-positives on FECACHE_COHERENCE / BPMVH / LEDGEH classes (different defect classes; not phantom-consumer)
    AC10: Session log + RAVC2 MCP to COO
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: existing comp-blast surface verify + marker-writer grep + S3/SSM manifest pair baseline
    Phase 2: --check-consumers flag + --all-producers sweep + comp-tools.yaml registry
    Phase 3: retroactive validation + 4-project ADHC corpus cross-check (no false-positive on non-phantom-consumer classes)
    Phase 4: BD pipeline test + safe-deploy.sh pre-flight integration (optional)
  </compiler_tools_mandate>

  <cross_domain_coordination>
    HARD DEPENDENCIES: Wave 1+2+3 RAVC2.

    COORDINATES WITH:
    - ADHC_TRIGMRK TO-001 (operational Path 2 Lambda rewrite; AE 0.6.1) — THIS TO is structural-diagnostic companion. ADHC_TRIGMRK incident #3 anchor is the empirical-of-record retroactive validation case.
    - v0.6 candidate `comp-validate fe-cache-freshness` (DE 0.4 brief `ebce828ac`) — sister: that tool detects FE-cache queryKey-URL decoupling; this tool detects producer-consumer phantom class. Both are pre-deploy structural-discipline integrations.
    - Phantom-consumer pattern memory entry `feedback_phantom_consumer_marker_pattern.md` (COO batch #10) — banking the structural rule this tool enforces operationally.

    NO PORTAL CHANGES.
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>Compiler-tool development.</no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    1. `comp-blast --check-consumers` flag (exit-code semantics)
    2. `comp-blast --check-consumers --all-producers` sweep mode (pipeline-scoped)
    3. org/modules/graph/comp-tools.yaml registry update
    4. Optional org/modules/graph/phantom-consumer/{pipeline}.yaml baselines
    5. Retroactive validation on ADHC_TRIGMRK 3-incident anchor (exit 1 confirmed)
    6. BD pipeline scope test
    7. Optional Phase 4 safe-deploy.sh pre-flight integration documented
    8. Session log + RAVC2
  </deliverables>

  <ravc>AE 0.7 RAVC2 to COO on AC1-10 PASS.</ravc>

  <notes>
    **Retitle history:** .030 was originally `ae-stale-marker` (Wave 4 stale-marker-specific scope). CTO ratified Option C generalization 2026-05-14 ~19:0XZ: retitle to `ae-comp-blast-check-consumers` + scope generalize from stale-marker-specific to phantom-consumer-class. Stale-marker subset preserved as derivable special case (producers emitting markers where consumer-count = 0 = stale-by-design). Semantic alignment with comp-blast surface (answers "what breaks if I change X?" → zero consumers = phantom).

    **Coord with AE 0.6.1's ADHC_TRIGMRK TO-001:** their fix is operational (Lambda Path 2 rewrite); this is diagnostic structural-detection. Complementary not duplicate. ADHC_TRIGMRK 3-incident anchor is empirical-of-record for retroactive validation here. Coord at ship time.

    **CI integration follow-on (optional Phase 4):** `.tools/safe-deploy.sh` pre-flight check on Lambda code changes detects producer-with-zero-consumers BEFORE terraform apply. Pairs with v0.6 `comp-validate fe-cache-freshness` (pre-deploy fe-cache audit). Phase 4 NOT required for this TO close; opens follow-on TO if scope demands.

    **Author identity:** `--author="0.7.0_AE_CloudOps <0.7.0_AE_CloudOps@opal.agent>"`.

    **Filename rename:** original file `ADHC_COMPIL_V4.030.ae-stale-marker.md` renamed to `ADHC_COMPIL_V4.030.ae-comp-blast-check-consumers.md` per slug change. Git mv preserves authorship trail.
  </notes>
</task_order>
