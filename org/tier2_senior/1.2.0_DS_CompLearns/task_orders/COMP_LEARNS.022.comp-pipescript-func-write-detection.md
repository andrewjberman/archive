<task_order>
  <metadata>
    <id>1.2.0_DS_CompLearns-2026-04-17-comp-learns-022-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>1.2.0_DS_CompLearns</issued_to>
    <date>2026-04-17</date>
    <status>complete</status><!-- Shipped 2026-04-21 by 1.2.0_DS_CompLearns. Commit 28ca6bd6. All 6 acceptance criteria pass. 16 new tests + 75 existing tests green. -->
    <project_code>COMP_LEARNS</project_code>
    <wave>022</wave>
  </metadata>

  <references>
    <ref type="dag_validation">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/gold_dag_validation_2026-04-16.md — three comp tool gaps identified</ref>
    <ref type="incident">gold_dag_validation 2026-04-16: comp-pipescript io reported B_02 WRITES as "(none detected)". Missed S3 put_object calls via helper functions (canonical_lots_unrealized_key, canonical_lots_realized_key). Would have caused B_02 || B_03 race condition if race conditions hadn't been manually inspected.</ref>
  </references>

  <context>
    During the gold chain DAG validation (2026-04-16), comp-pipescript io was used
    as the primary source of truth for script S3 reads/writes. Three structural
    gaps were identified that caused the tool to miss real dependencies:

    GAP 1 — FUNC-KEY WRITE DETECTION:
      B_02.canonical_lots.py L617-624 calls _s3.put_object(...) with Key=canonical_lots_unrealized_key(date_str)
      and Key=canonical_lots_realized_key(date_str). These are helper functions that
      construct S3 keys dynamically. comp-pipescript io's AST walker sees put_object
      with a function-call Key argument and cannot resolve the target prefix — it
      reports "WRITES: (none detected)". Consumer scripts reading these keys (B_03,
      C_05) are therefore not connected to B_02 as a producer. Race condition
      proposed in the original phase map (B_02 || B_03) would have corrupted data.

    GAP 2 — PREFIX-READ vs FUNC-WRITE CROSS-REFERENCE:
      When script A reads an S3 PREFIX (e.g., B_00 reads POSITIONS_CUBE_PREFIX =
      gold/timeseries/positions_cube/) and script B writes to that prefix via a
      FUNC-key (e.g., A_03 writes positions_cube_key(date)), the tool detects both
      independently but does NOT cross-reference them to flag the dependency edge.
      Implicit dep A_03 → B_00 was missed.

    GAP 3 — ROLLING-WINDOW PRIOR-RUN READ MIS-FLAGGED AS CIRCULAR:
      D_01 reads prior-run D_04 partner_analytics output for period-over-period
      delta computation. The tool treats this as a same-run circular dependency
      (D_01 ↔ D_04) rather than a temporal prior-run read. Manual inspection was
      required to resolve.
  </context>

  <objective>
    Extend comp-pipescript io to close these three gaps.

    FIX 1 — FUNC-KEY write resolution (HIGH PRIORITY):
    When the AST walker sees an S3 put_object / upload_file / upload_fileobj
    with a Key argument that is a function call (e.g., my_key_fn(date_str)),
    it must:
      (a) Locate the function definition in the same module (or an imported module
          from lib.config / lib.s3_keys / common key-helper modules in the repo)
      (b) Parse the function body for the return value
      (c) If the return value is a string literal or a concatenation of literals
          + f-string components, extract the PREFIX (portion up to the first {var}
          or the full literal if no var)
      (d) Register the extracted PREFIX as a WRITE target for the calling script

    This resolves B_02's two put_object calls to canonical_lots_unrealized/ and
    canonical_lots_realized/ prefixes.

    FIX 2 — PREFIX-read vs FUNC-write cross-reference:
    After FIX 1 lands, every FUNC-write resolves to a PREFIX. The existing
    PREFIX-read detection already works. Add a cross-reference step:
      For every PREFIX read in script A:
        Check every FUNC-write in other scripts.
        If FUNC-write resolved prefix == PREFIX read: emit dependency edge A ← B.
    Output should flag these as "IMPLICIT (via FUNC-key)" to distinguish from
    directly declared edges.

    FIX 3 — ROLLING-WINDOW prior-run read detection:
    When the AST walker sees an S3 read of a path that matches the script's own
    output path pattern (self-read) OR a downstream script's output path, flag
    it as a POSSIBLE rolling-window read rather than a circular dep. Surface
    a warning asking the author to confirm the read is for prior-run data (rolling
    window pattern) vs. current-run (true circular bug).

    Deliverable: updated comp-pipescript io implementation + test cases covering
    all three gaps using B_02, A_03, D_01 as fixtures. Test cases must fail
    against the current implementation and pass against the new.
  </objective>

  <acceptance_criteria>
    1. comp-pipescript io B_02 reports WRITES including canonical_lots_unrealized/
       and canonical_lots_realized/ prefixes.
    2. comp-pipescript io B_03 reports B_02 as a producer of canonical_lots_*
       artifacts (implicit edge surfaced).
    3. comp-pipescript io B_00 reports A_03 as a producer of positions_cube/
       (implicit edge surfaced).
    4. comp-pipescript io D_01 emits a rolling-window warning on the partner_analytics
       prior-run read rather than flagging a circular dep.
    5. Test fixtures added covering all three scenarios. Existing tests continue to pass.
    6. MCP COMPLETE to CTO + COO with commit hash + before/after output diff on
       the three scripts above.
  </acceptance_criteria>

  <notes>
    - This is a compiler tooling TO. No gold chain runtime impact.
    - Execute after AE's dispatcher restructure validates on QA runner.
    - Priority rationale: if the FUNC-write gap is not fixed, future DAG audits
      using comp-pipescript alone will miss race conditions. The tool is the
      primary source of truth for dependency analysis — its blind spots are
      silent data integrity risks.
  </notes>
</task_order>
