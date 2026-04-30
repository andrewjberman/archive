<task_order>
  <id>ADHC_CLCOMM.005</id>
  <title>CTO — inbox-watch.sh hardening: eval-exclusion port + cl-inbox-watch orphan fix + universal design brief</title>
  <status>complete</status>
  <assigned_to>1.0.0_SA_CTO</assigned_to>
  <created_by>1.0.0_SA_CTO</created_by>
  <created_date>2026-04-30</created_date>
  <completed_date>2026-04-30</completed_date>
  <project>ADHC_CLCOMM</project>

  <context>
    ADHC_CLCOMM.json "blocking" section surfaced a side action from TO-2 cross-channel
    investigation: COMP branch commits c471b2fd9 (eval-exclusion guard) and d26a36492
    (awk column fix), authored by 2.1.0_SC_CompLearns, were on COMP only and had not
    been ported back to CLOUD inbox-watch.sh. Simultaneously, cl-inbox-watch.sh still
    carried the ppid==1 orphan guard bug that was fixed in inbox-watch.sh (944618d86)
    but never propagated to the CL variant.

    Andrew directive 2026-04-30: cherry-pick COMP fixes to CLOUD, fix cl-inbox-watch.sh
    orphan guard, and produce a universal design brief covering both channels (not
    addressed to any specific group, usable by both Opal agents and COMP_LEARNS agents).

    This TO is CTO-scope: org/mcp/** is BASE_EXEC lane (CTO direct ship). No other
    agent required.
  </context>

  <scope>
    1. Port eval-exclusion fix (grep -v eval in ps-ef fallback) to org/mcp/inbox-watch.sh
    2. Port eval-exclusion fix to org/mcp/cl-inbox-watch.sh
    3. Fix cl-inbox-watch.sh ppid==1 orphan guard: remove [ "$ppid" -eq 1 ] condition,
       change kill -0 target from $ppid (parent) to $pid (process itself)
    4. Rewrite org/mcp/INBOX_WATCH_DESIGN.md as a universal design brief covering both
       channels, all three 2026-04-30 fixes, and all four coverage options
    5. Update org/XXX.md Step 1b section C: add CronCreate Option 2 guidance for
       autonomous loop agents
    6. Commit all org/mcp/** changes under 1.0.0_SA_CTO authorship
  </scope>

  <deliverables>
    - org/mcp/inbox-watch.sh — eval-exclusion fix applied (grep -v eval)
    - org/mcp/cl-inbox-watch.sh — eval-exclusion fix + orphan guard fix
    - org/mcp/INBOX_WATCH_DESIGN.md — universal briefing, not addressed to any group
    - org/XXX.md — CronCreate Option 2 note in Step 1b section C
    - Commit under 1.0.0_SA_CTO author
  </deliverables>

  <acceptance_criteria>
    - inbox-watch.sh ps-ef fallback contains `grep -v eval` before awk
    - cl-inbox-watch.sh ps-ef fallback contains `grep -v eval` before awk
    - cl-inbox-watch.sh orphan guard: no `[ "$ppid" -eq 1 ]` condition; kill -0 tests $pid not $ppid
    - INBOX_WATCH_DESIGN.md contains no group-specific addressing; covers both channels
    - org/XXX.md Step 1b section C contains CronCreate guidance for autonomous agents
    - Single commit, CTO author
  </acceptance_criteria>

  <compiler_tools_mandate>
    <before_write>N/A — no gold/silver/bronze scripts; no portal components</before_write>
    <before_commit>N/A — bash scripts; py_compile gate does not apply</before_commit>
    <after_commit>N/A — no blast-radius change; org/mcp/** is infrastructure-only</after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    <!-- org/mcp/inbox-watch.sh and cl-inbox-watch.sh are infrastructure-only;
         no shared S3 artifacts or gold/silver/bronze scripts involved.
         org/XXX.md change is additive (new paragraph in Step 1b). -->
  </cross_domain_coordination>

  <completion_evidence>
    Committed 2026-04-30. All three script fixes applied and verified by read-back.
    INBOX_WATCH_DESIGN.md rewritten as universal brief. org/XXX.md updated with
    CronCreate Option 2 guidance.
  </completion_evidence>
</task_order>
