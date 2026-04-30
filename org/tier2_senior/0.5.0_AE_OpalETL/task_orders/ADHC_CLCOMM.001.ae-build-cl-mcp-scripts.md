<task_order>
  <metadata>
    <id>ADHC_CLCOMM.001.ae-build-cl-mcp-scripts</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-04-30</date>
    <status>complete</status>
    <project_code>ADHC_CLCOMM</project_code>
    <prd_ref>docs/architecture/ADHC_CLCOMM.md §3 + §4.1-§4.4 + §6 (canonicalized 2026-04-30 from feature_clb commit 5eac1f09f)</prd_ref>
    <effort>0.5-1 day</effort>
    <gates_on>None — independent of all live INFLEC/ORIAPI work; AE 0.5 has full bandwidth.</gates_on>
    <gates_for>ADHC_CLCOMM.002 (feature_clb config wire-up)</gates_for>
  </metadata>

  <objective>
    Build the four new MCP infrastructure files for the isolated `complearns-agent-comms` channel. CLOUD-branch work in `ajb_workspace`. The files mirror the existing `org/mcp/` ecosystem (server.py, broker.py, inbox-watch.sh, check-inbox.sh) with namespace-isolation edits per the canonical PRD §4.1-§4.4. After this TO ships, the new files exist on disk and on the CLOUD branch; the feature_clb worktree gains them via merge or filesystem copy in TO-2.

    Includes the §6 hidden-dependency resolution: `agent-poller.py` line 45 hardcodes `OPAL_BROKER_PORT` (default 7800). The CL channel runs on port 7801 — without modification, broker push channel notifications won't reach CL agents. TO-1 owns this decision: either modify the existing poller to support both ports OR ship a parallel `cl-agent-poller.py` variant.

    **NOTE 2026-04-30 (CTO):** An earlier amend proposed a heavier channel-agnostic refactor (channels.json registry + role-based auth) up-front. Reverted in light of AE 0.5's parallel work on prefix-routing-in-poller approach + AE's documented concern about env-var threading reliability on Claude Code hooks. Cross-channel refactor moved to TO-4 (architectural codification) where it benefits from empirical evidence (TO-3 verification PASS) before refactor. Sequencing: ship simple thing → verify → refactor with hindsight.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - Read `docs/architecture/ADHC_CLCOMM.md` end-to-end. The setup brief is the authoritative spec; nothing in this TO supersedes it.
      - `comp-blast org/mcp/server.py` + `comp-blast org/mcp/broker.py` to confirm scope of any cross-cutting consumers (expected: tooling that runs the server / broker; nothing in the data layer).
      - Read `org/mcp/server.py` lines 41, 51, 53, 54, 55, 69, 446, ~603 (deregister auth check) — confirm spec line numbers match current file (file may have drifted since 2026-04-30 brief authoring).
      - Read `org/mcp/broker.py` lines 31, 32 — same drift check.
      - Read `org/mcp/agent-poller.py` line 45 — confirm `OPAL_BROKER_PORT` hardcode is current.
    </phase_1_before_write>
    <phase_2_before_commit>
      - `python -c "import ast; ast.parse(open('org/mcp/complearns_server.py').read())"` — Python syntax clean.
      - `python -c "import ast; ast.parse(open('org/mcp/cl_broker.py').read())"` — Python syntax clean.
      - `bash -n org/mcp/cl-inbox-watch.sh` — shell syntax clean.
      - `bash -n org/mcp/cl-check-inbox.sh` — shell syntax clean.
      - `python -c "import ast; ast.parse(open('org/mcp/agent-poller.py').read())"` if you modify it — syntax clean.
      - `chmod +x org/mcp/cl-inbox-watch.sh org/mcp/cl-check-inbox.sh` — verify executable bit set.
      - Diff the new vs old: `diff org/mcp/server.py org/mcp/complearns_server.py` should show ONLY the 8 spec edits + the deregister auth widening; nothing else.
    </phase_2_before_commit>
    <phase_3_after_commit>
      - Verify `.tools/cl-inbox-watch` and `.tools/cl-check-inbox` are callable from PATH: `which cl-inbox-watch` returns the symlink (or copy) target.
      - Confirm `python org/mcp/complearns_server.py --help` (or equivalent dry-run) starts without import errors. Do NOT actually start the broker — that's TO-3 territory.
      - Append session-log entry to `org/compiler-tools-log.md`.
    </phase_3_after_commit>
  </compiler_tools_mandate>

  <scope>
    Four file creations + one file modification + .tools/ aliasing.

    1. `org/mcp/complearns_server.py` — copy `server.py`, apply 8 line-targeted edits per PRD §4.1 (lock file, inbox dir, liveness file, broker script, broker port env+default, logger name, FastMCP server name) + the deregister auth check widening (current `startswith("1.0.0") or startswith("2.0.0")` becomes `major_minor in ("1.0", "1.1", "2.0", "2.1")`).

    2. `org/mcp/cl_broker.py` — copy `broker.py`, apply 2 line-targeted edits per PRD §4.2 (port env+default to `CL_BROKER_PORT`/7801, db file to `cl_broker.db`).

    3. `org/mcp/cl-inbox-watch.sh` — copy `inbox-watch.sh`, change `INBOX_BASE` to `$SCRIPT_DIR/cl_inbox` (line ~25 per PRD §4.3). chmod +x.

    4. `org/mcp/cl-check-inbox.sh` — copy `check-inbox.sh`, change `INBOX_BASE` to `$SCRIPT_DIR/cl_inbox` (line ~17 per PRD §4.4). chmod +x.

    5. `org/mcp/agent-poller.py` — modify to read EITHER `OPAL_BROKER_PORT` (default 7800) OR `CL_BROKER_PORT` (default 7801) based on a channel-detection signal. Recommended approach: read agent serial from input, route by serial prefix (1.1.x / 2.1.x / 1.x.0_DS_CompLearns / 2.1.0_SC_CompLearns → CL channel; everything else → opal channel). Alternative: spawn a separate `cl-agent-poller.py` and have CL channel `hook_launch_poller.py` invoke it. AE judgment call — pick whichever is cleaner. Document the choice in the commit message + session log.

    6. `.tools/cl-inbox-watch` and `.tools/cl-check-inbox` PATH aliases per PRD §4.7. Match the install pattern of existing `.tools/inbox-watch` and `.tools/check-inbox` (symlink or copy — match what's already there).

    **Cross-channel architecture observations** — append a section "Cross-channel architecture observations" to the session log capturing any pattern, gotcha, or improvement opportunity surfaced during this work that should generalize to opal-agent-comms or future channels. Mined into TO-4 (architecture doc + cross-channel refactor) authoring per Andrew directive 2026-04-30. Light-touch addition to TO-1 scope; substantive refactor work moved to TO-4 with empirical grounding.

    Author: `0.5.0_AE_OpalETL <0.5.0_AE_OpalETL@opal.agent>`. Use `.tools/safe-commit.sh` with explicit pathspec (ADHC_OWNPTH.007 mandate). Single commit OK — all files are a coherent shipped unit.
  </scope>

  <acceptance_criteria>
    1. `org/mcp/complearns_server.py` exists. Diff vs `server.py` shows ONLY the 9 spec edits (8 line-targeted + 1 auth widening). Python syntax clean.
    2. `org/mcp/cl_broker.py` exists. Diff vs `broker.py` shows ONLY the 2 spec edits. Python syntax clean.
    3. `org/mcp/cl-inbox-watch.sh` exists with executable bit set. Diff vs `inbox-watch.sh` shows ONLY the `INBOX_BASE` change.
    4. `org/mcp/cl-check-inbox.sh` exists with executable bit set. Diff vs `check-inbox.sh` shows ONLY the `INBOX_BASE` change.
    5. `org/mcp/agent-poller.py` modified to support both ports (or `cl-agent-poller.py` exists as parallel variant). Channel-routing decision documented in commit message.
    6. `.tools/cl-inbox-watch` and `.tools/cl-check-inbox` callable from PATH (verify with `which`).
    7. Single commit on CLOUD branch with all six file additions/modifications. Author = AE 0.5.0 underscore form. Pushed to origin/CLOUD.
    8. Session log includes a "Cross-channel architecture observations" section (light-touch input to TO-4 architecture doc).
    9. RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC8 evidence + commit hash + channel-routing decision rationale.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT create `cl_inbox/` directory manually — `INBOX_DIR.mkdir(exist_ok=True)` in the new server creates it automatically on first start. Premature creation is harmless but unnecessary.</rule>
    <rule>Do NOT modify the existing `server.py`, `broker.py`, `inbox-watch.sh`, or `check-inbox.sh` — they continue to serve the org-wide channel. CL is purely additive.</rule>
    <rule>Do NOT skip the deregister auth widening in `complearns_server.py` — without it, 1.1.0_SA_CTO and 2.1.0_SA_COO cannot deregister agents on the CL channel (their primary control plane).</rule>
    <rule>Do NOT start the new broker or server during this TO — that's verification work in TO-3, after feature_clb wire-up is complete.</rule>
    <rule>Do NOT use bare `git commit` — `.tools/safe-commit.sh` with explicit pathspec only.</rule>
  </do_not>

  <deliverables>
    <deliverable type="code">org/mcp/complearns_server.py (NEW)</deliverable>
    <deliverable type="code">org/mcp/cl_broker.py (NEW)</deliverable>
    <deliverable type="code">org/mcp/cl-inbox-watch.sh (NEW, +x)</deliverable>
    <deliverable type="code">org/mcp/cl-check-inbox.sh (NEW, +x)</deliverable>
    <deliverable type="code">org/mcp/agent-poller.py (MODIFIED) OR org/mcp/cl-agent-poller.py (NEW) — AE channel-routing decision per scope item 5</deliverable>
    <deliverable type="code">.tools/cl-inbox-watch + .tools/cl-check-inbox (NEW PATH aliases)</deliverable>
    <deliverable type="document">Session log with "Cross-channel architecture observations" section (light-touch input to TO-4)</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + 1.0.0_SA_CTO with: AC1-AC9 evidence + commit hash + channel-routing decision rationale</deliverable>
  </deliverables>
</task_order>
