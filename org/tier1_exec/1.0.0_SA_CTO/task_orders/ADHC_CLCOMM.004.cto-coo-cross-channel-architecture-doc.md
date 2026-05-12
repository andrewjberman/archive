<task_order>
  <metadata>
    <id>ADHC_CLCOMM.004.cto-coo-cross-channel-architecture-doc</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <co_implementer>2.0.0_SA_COO</co_implementer>
    <date>2026-04-30</date>
    <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
    <project_code>ADHC_CLCOMM</project_code>
    <prd_ref>docs/architecture/ADHC_CLCOMM.md (parent project) — TO-4 added 2026-04-30 per Andrew directive: "lessons learned from this process should also be used to benefit opal-agent-comms channels"</prd_ref>
    <effort>0.5 day (CTO+COO joint authoring)</effort>
    <gates_on>ADHC_CLCOMM.003 PASS + project Phase 1 close (verification empirically confirms isolation works; TO-4 codifies the pattern in light of empirical evidence + AE 0.5's three session-log observation sections).</gates_on>
    <gates_for>Project full closure (TO-4 ships → ADHC_CLCOMM 3-step atomic close)</gates_for>
  </metadata>

  <objective>
    Author `docs/architecture/AGENT_COMMS_ARCHITECTURE.md` — the cross-channel architecture doc that codifies the patterns surfaced during ADHC_CLCOMM execution. Covers BOTH `opal-agent-comms` and `complearns-agent-comms` plus a runbook for adding any future channel #3+. Andrew directive 2026-04-30: this is the structural mechanism by which CL-channel work benefits opal-channel and future work.

    Mines the "Cross-channel architecture observations" sections from TO-1 + TO-2 + TO-3 session logs (AE 0.5's empirical findings during execution) PLUS the architectural lessons identified pre-execution (channel-config pattern, role-based auth, isolation invariants).

    Authored jointly by 1.0.0_SA_CTO (architectural sponsor) + 2.0.0_SA_COO (process owner). Uses ADHC_COMPIL.003 §5 PRD authoring template discipline.
  </objective>

  <compiler_tools_mandate>
    <phase_1_before_write>
      - Read ADHC_CLCOMM.001 + .002 + .003 session logs in full. Extract every entry from the "Cross-channel architecture observations" sections. Synthesize into a list of patterns, anti-patterns, and gotchas — empirically grounded in the AE work.
      - Read `org/mcp/channels.json`, `org/mcp/agent-poller.py` (post-refactor), `org/mcp/server.py` (post-refactor) — confirm the actual implemented patterns match what the doc will describe.
      - `comp-blast org/mcp/server.py` + `comp-blast org/mcp/complearns_server.py` to confirm consumer scope (any tooling that reads channels.json should be enumerated in the doc).
      - Read `docs/architecture/PRD_AUTHORING_PROTOCOL.md` (ADHC_COMPIL.003 §5 mandate) — apply same discipline.
    </phase_1_before_write>
    <phase_2_before_commit>
      - Doc structure check: covers all four mandated sections (isolation invariants, adding-a-new-channel runbook, anti-patterns, channel-aware tool design checklist). No section is "TBD" or placeholder.
      - Cross-reference check: every architectural claim cites its evidence (AE session log section, code line, or commit hash).
      - Length check: target ~500-1000 lines (matches A2 PRD target shape). Don't pad; cut if over.
    </phase_2_before_commit>
    <phase_3_after_commit>
      - 3-step atomic project close (CTO PRD Status line + COO JSON + REGISTRY row move).
      - Append session-log entry to `org/compiler-tools-log.md`.
      - MCP AE 0.5.0 with project close + thanks + reference to the architecture doc as the canonical pattern for future work.
    </phase_3_after_commit>
  </compiler_tools_mandate>

  <scope>
    Single deliverable: `docs/architecture/AGENT_COMMS_ARCHITECTURE.md` (~500-1000 lines).

    **Mandatory sections:**

    1. **Channel inventory** — table of all channels with broker_port, inbox_dir, liveness_file, agent prefix routing, owner (per `channels.json`). Living index.

    2. **Isolation invariants** — the architectural properties that physically isolate channels from each other. Each invariant has:
       - Statement of the invariant (what must be true)
       - Why it matters (what breaks if violated)
       - Where it's enforced (which file/line)
       - How to verify (specific check)
       Examples: per-channel cwd; relative-path resolution in server.py; per-channel broker port; per-channel liveness/inbox/db files; per-channel hook matcher; per-channel role allowlist.

    3. **Adding a new channel — runbook** — step-by-step for channel #3+:
       - Add entry to `org/mcp/channels.json`
       - Copy `server.py` → `{channel}_server.py` with namespace edits
       - Copy `broker.py` → `{channel}_broker.py` with namespace edits
       - Copy inbox-watch.sh + check-inbox.sh with namespace edits
       - Update worktree `.mcp.json` + `.claude/settings.local.json`
       - Add `.tools/` PATH aliases
       - Verification checklist
       Result: zero code changes in the cross-channel layer (poller, role-auth) when adding channel #3.

    4. **Cross-channel anti-patterns** — what NOT to do, with empirical incident references:
       - Hardcoded ports (anti-pattern — was in agent-poller.py:45 pre-CLCOMM)
       - Prefix-matched auth (anti-pattern — was in server.py:603 pre-CLCOMM)
       - Absolute paths in server resource resolution (would break per-cwd isolation)
       - Channel name in tool decorators (would couple tools to specific channels)
       - Cross-channel inbox writes (servers must never write outside their own inbox_dir)

    5. **Channel-aware tool design checklist** — when authoring a new MCP tool, ask:
       - Does this tool need to query across channels (e.g., `get_org_summary`) or is it inherently per-channel (e.g., `register_agent`)?
       - Does it read role from serial? Use `parse_role()` helper, not prefix matching.
       - Does it use a port? Read from `channels.json`, not env var hardcode.
       - Is its hook matcher channel-specific? Match `mcp__{channel}__{tool}` exactly.
       - Does it write any artifact? Confirm path is per-channel-isolated.

    6. **Mining notes** — appendix listing the empirical observations from AE 0.5's TO-1/TO-2/TO-3 session logs that informed this doc. Each observation cited with serial + log path + commit hash where applicable. Not a doc body section; a transparency record so future authors can see the evidence trail.

    7. **Future channel scenarios** — light forward-looking section:
       - Hypothetical channel #3 (e.g., for partner-firm-specific dyads)
       - When to add a channel vs. reuse an existing one (decision tree)
       - Limits on channel proliferation (operational cost vs. isolation benefit)

    **Authoring split:**
    - CTO drafts §1, §2, §4, §5 (architectural rigor)
    - COO drafts §3, §6, §7 (process + mining + forward scenarios)
    - Joint review pass before commit
    - CTO commits canonical at `docs/architecture/AGENT_COMMS_ARCHITECTURE.md` (ANY_CTO scope)

    Use `.tools/safe-commit.sh` with explicit pathspec.
  </scope>

  <acceptance_criteria>
    1. `docs/architecture/AGENT_COMMS_ARCHITECTURE.md` exists. ~500-1000 lines. All 7 mandatory sections present.
    2. §1 channel inventory matches `org/mcp/channels.json` exactly (single source of truth).
    3. §2 isolation invariants: each invariant has statement + why + where-enforced + how-to-verify. No invariant is hand-wavy.
    4. §3 runbook tested by paper exercise: walk through "add a hypothetical TRADE-agent-comms channel" and verify the runbook produces a working stub. Document the exercise in the doc's mining notes (§6).
    5. §4 anti-patterns each cite empirical evidence (file:line or commit hash) where the anti-pattern appeared pre-CLCOMM.
    6. §5 checklist actionable — a future MCP tool author can use it as a pre-commit gate.
    7. §6 mining notes cite TO-1 + TO-2 + TO-3 session logs at observation-section granularity.
    8. PRD authoring discipline followed (PRD_AUTHORING_PROTOCOL.md): structured sections, evidence-cited claims, no placeholders.
    9. 3-step atomic project closure post-commit (JSON status complete + REGISTRY row move + parent ADHC_CLCOMM.md PRD Status updated to COMPLETE).
    10. RAVC4 to 2.0.0_SA_COO + Andrew with: AC1-AC9 evidence + commit hash + project closure summary.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT author this TO before TO-3 verification PASS — empirical grounding requires the channel actually working in practice. Premature authoring loses the empirical lessons.</rule>
    <rule>Do NOT include speculative architectural opinions without empirical anchor. Every claim cites evidence (file:line, commit hash, or AE session-log observation).</rule>
    <rule>Do NOT pre-commit to a specific 3rd channel design — §7 forward-scenarios stays light and decision-tree-shaped, not specification-shaped.</rule>
    <rule>Do NOT skip the §6 mining notes — the transparency record is what makes this doc credible to future authors.</rule>
    <rule>Do NOT use bare `git commit` — `.tools/safe-commit.sh` with explicit pathspec.</rule>
  </do_not>

  <deliverables>
    <deliverable type="document">docs/architecture/AGENT_COMMS_ARCHITECTURE.md (NEW; CTO+COO joint authoring)</deliverable>
    <deliverable type="closure">3-step atomic close of ADHC_CLCOMM project (JSON + REGISTRY + parent PRD Status)</deliverable>
    <deliverable type="ravc">RAVC4 to 2.0.0_SA_COO + Andrew with: AC1-AC9 evidence + project closure summary + lessons-learned recap</deliverable>
  </deliverables>
</task_order>
