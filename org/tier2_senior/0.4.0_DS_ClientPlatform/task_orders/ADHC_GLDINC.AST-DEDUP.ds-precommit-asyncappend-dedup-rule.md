<to_id>ADHC_GLDINC.AST-DEDUP</to_id>
<project>ADHC_GLDINC</project>
<title>AST-DEDUP — ds-precommit-check.py rule: flag completion-order append feeding an order-sensitive dedup (the CLASS-N detector, at commit time)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (CTO arch-ruling queue item 230400Z — "ratified architecturally; needs a small tooling TO")</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete</status> -- ab0cd8ba0 (pushed CLOUD). check_completion_order_dedup() in .tools/ds-precommit-check.py: 3-part conjunction (append-under-as_completed/imap_unordered + pd.concat DATA-FLOW LINK + order-sensitive drop_duplicates NOT sort-guarded), per-function-scope. SEVERITY=WARN-first (advisory, 1-line _ASTDEDUP_SEVERITY ramp knob) -- fabric-shared checker + new heuristic + live genuine findings would freeze lanes if ERROR now. ACCEPTANCE: 2/2 fixtures FIRE (A_01 73ec87a84^ L192, A_04 9a89926fd^ L120); 0 FP on live bd gold (67 files; data-flow link killed the C_02/C_01 same-function-conjunction FPs); post-fix A_01/A_04 SILENT; checker passes own gate. Durable regression: test_ds_precommit_check.py +4 cases (1 FIRE + 3 SILENT: index-slot/sort-guarded/unrelated-dedup), suite 7/7. PHASE-3 sweep (211 files bd/cot/inf x gold/silver/bronze): 3 CLASS-N findings = cot A_01, cot A_04, bd silver compact-realized -> routed CTO+COO, converging w/ AE 0.6.0 CENSUS-XT. Known gap: pool.add_done_callback append undetected. RAVC2 -> COO.
<priority>Low — small tooling TO; no gate on GLDINC</priority>

<references>
  <ref type="ruling">CTO 20260611T230400Z — class discriminator = parallel-load assembly shape; mechanically detectable at commit</ref>
  <ref type="fixtures">A_01 pre-fix (oracle-fix 73ec87a84 parent) + A_04 pre-fix (9a89926fd parent) = known-positive shapes; A_03/B_01/build_canonical_prices_v2/A_00/E_02-10 = known-negative CLASS-I (index-slot)</ref>
  <ref type="tooling-lineage">docs/architecture/ADHC_DSFLOW.md (ds-precommit-check rule family)</ref>
</references>

<scope>
Add one AST rule to `.tools/ds-precommit-check.py`: WARN/ERROR when a list/dict built by append-or-update inside an `as_completed(...)` loop (or equivalent completion-order construct: `imap_unordered`, callback-append under a pool) flows into an order-sensitive dedup — `drop_duplicates(keep='last')` / `keep='first'` / `dict`-last-write-wins keyed assembly — within the same function scope. The rule fires on the CONJUNCTION (completion-order build + order-sensitive consumer), not on either alone: index-slot assembly (`results[i] = ...`) and unordered-build-without-dedup stay silent. Would have caught A_01 + A_04 at commit time.
Severity: match the existing rule family's convention (ERROR if the family blocks; WARN-first rollout acceptable if FP risk emerges in Phase-2 testing — document the choice).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read .tools/ds-precommit-check.py rule structure; git show the A_01/A_04 pre-fix shapes (73ec87a84^ / 9a89926fd^) as positive fixtures</run>
      <expect>Rule-plugin pattern understood; both positive fixtures' exact AST shapes extracted.</expect>
      <if_mismatch>STOP. Surface structural surprises to COO.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Rule unit test: positive on both pre-fix fixtures; negative sweep across ALL of data/black_diamond/scripts/gold/*.py at current HEAD</run>
      <expect>2/2 positives fire; 0 false positives on the live tree (every current script is post-fix or CLASS-I — any hit is an FP unless it's a genuinely new CLASS-N, which is a FINDING to route, not an FP).</expect>
      <if_mismatch>STOP. An FP on live CLASS-I scripts (the slug-sentinel lesson, memory reference_path_rename_test_failure...) means the conjunction predicate is too loose — tighten before commit.</if_mismatch>
    </step>
    <step>
      <run>.tools/ds-commit-gate.sh .tools/ds-precommit-check.py</run>
      <expect>All checks exit 0 (the checker passes its own gate).</expect>
      <if_mismatch>Fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Full-tree sweep: run the updated checker across data/*/scripts/{gold,silver,bronze}/*.py; report hit counts to CTO+COO</run>
      <expect>Hit list = CLASS-N candidates only (cross-check against CENSUS-XT results when available — the two deliverables should converge).</expect>
      <if_mismatch>Divergence from the census = adjudication item for CTO, not silent reconciliation.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **ADHC_GLDINC.CENSUS-XT (0.6.0_AE_PartnerETL, staged same-day):** independent detector of the same class — Phase-3 cross-check is deliberate redundancy, coordinate delivery timing via MCP so CTO adjudicates both together.
- `.tools/ds-precommit-check.py` is fabric-shared tooling — every DS agent's commits run it. A too-loose rule blocks the whole DS lane; the Phase-2 zero-FP bar is load-bearing.
</cross_domain_coordination>

<acceptance_criteria>
- Rule fires on both pre-fix fixtures (A_01, A_04 shapes) and produces 0 false positives on the current bd gold tree.
- Severity choice (ERROR vs WARN-first) documented in the commit message + session log.
- Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`. Missing rows = REWORK.
- RAVC2 evidence to COO: commit hash + fixture test output + full-tree sweep summary.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Commit-time tooling only; no data-path changes.</no_reprocess_needed></data_reprocess_scope>
