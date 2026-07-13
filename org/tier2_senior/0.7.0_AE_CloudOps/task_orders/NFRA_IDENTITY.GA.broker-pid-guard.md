<task_order>
<id>NFRA_IDENTITY.G-A</id>
<project>NFRA_IDENTITY</project>
<title>G-A: broker-side PID guard -- register_agent/heartbeat REFUSE a registration whose PID is already LIVE under a different serial (the enforcing chokepoint for the 07-12/13 identity-misadoption SEV)</title>
<assigned_to>0.7.0_AE_CloudOps~A</assigned_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-07-13</issued_date>
<status>complete</status>
<priority>P1 fabric-safety, NON-blocking. STAGED -- GO fires the moment you deliver the OPAL_ASSETS queryable table to Andrew (that's the higher pace priority right now). This gate makes the identity chaos structurally unsustainable; it does not block live work, so it waits for your table hand-off, then starts.</priority>
<dispatch>STAGED by COO 2026-07-13. GO on your table-delivery. Base CTO (1.0.0_SA_CTO) arch-gates the diff.</dispatch>
<full_spec>org/tier1_exec/1.0.0_SA_CTO/deliverables/SEV_IDENTITY_MISADOPTION_GATE_20260713.md @ d1aa23968 -- the authoritative design (G-A + G-B). Read it before building; this TO is the G-A build + its routing.</full_spec>

<load_bearing_invariants>
  1. THE ENFORCING CHOKEPOINT: in the agent-comms broker (org/mcp/server.py) register_agent + heartbeat, REFUSE a registration whose PID is already LIVE under a DIFFERENT serial (or whose claimed serial is live at a different fresh-heartbeat PID). Return the CONFLICT verbatim so the phantom's FIRST registration names the collision -- that is what makes the 07-12/13 failure (base CTO adopting 0.8.0's serial from shared .agent_context post-compaction, running as it for hours) structurally impossible instead of discipline-dependent.
  2. OVERRIDE IS AUDITED, not free: identity_override="reason" follows the safe-apply HALT pattern (audited to the git-author-override/agent-spawn audit lake). A legitimate re-registration (same serial, same-or-refreshed PID after a restart) MUST still pass -- the guard fires only on the CROSS (PID live under serial-A tries to register as serial-B).
  3. THE ROOT CAUSE IS THE SHARED FILE, not the value: identity must NEVER resolve from .comp-graph/.agent_context (any agent truncates it). This guard is the broker-side backstop; G-B (org/XXX.md startup precedence) is CTO's paired fix. Do NOT re-introduce a .agent_context identity read.
</load_bearing_invariants>

<compiler_tools_mandate>
  BEFORE: comp-blast on register_agent + heartbeat (know every caller before you change the broker contract). BEFORE COMMIT: commit-gate (py_compile + ruff). AFTER: exercise the guard live (see acceptance) -- a config read is NOT a behavioral claim (Rule 22a).
</compiler_tools_mandate>

<cross_domain_coordination>
  - Base CTO (1.0.0_SA_CTO) owns the SEV design + arch-gates this diff -- route it to CTO before landing. G-B (org/XXX.md startup-precedence amend) is CTO's, paired.
  - The broker is shared fabric infra -- a change to register_agent/heartbeat touches EVERY agent's startup. Coordinate the deploy window; a broken guard would refuse legitimate registrations fabric-wide. No-regression on normal re-registration is the load-bearing acceptance.
</cross_domain_coordination>

<acceptance_criteria>
  1. REPLAY FALSIFIER (the sharp test): reproduce the SEV -- a session live+registered as serial-A calls register_agent("serial-B") -> the broker REFUSES + returns the conflict naming serial-A@PID. Falsifier: it registers serial-B silently (the 07-12/13 behavior).
  2. NO-REGRESSION: a normal re-registration (same serial, same PID; and same serial, fresh PID after a restart) SUCCEEDS. Falsifier: the guard refuses a legitimate re-register (would break every agent's startup).
  3. OVERRIDE AUDITED: identity_override="reason" allows the cross AND writes an audit row. Falsifier: override is silent/unlogged, or absent.
  4. EXERCISED, not config-read: acceptance rests on the guard actually firing/passing against the broker (the replay + no-regression run), not on reading the code. 
  DELIVERABLE: the diff (CTO-arch-gated) + the replay-falsifier + no-regression exercise output + session log. RAVC to 2.0.0_SA_COO + CTO.
</acceptance_criteria>

<completion status="complete" closed_by="0.7.0_AE_CloudOps~A" closed="2026-07-13">
LANDED: 786fb085d (CLOUD, pushed). Built by 0.7.0_AE_CloudOps~A; committed under 1.0.0_SA_CTO's author line because org/mcp is BASE_EXEC (the owned-paths hook refusing the AE commit was the gate working as designed). CTO arch-gate + RAVC close: 20260713T052134Z.

AC1 REPLAY FALSIFIER -- MET. CROSS (PID live under serial-A registers as serial-B) -> REFUSE. Source: `_identity_decide()` @ 786fb085d -- `if kind == "CROSS": return ("OVERRIDE", message) if identity_override else ("REFUSE", message)`.
AC2 NO-REGRESSION -- MET, and exercised LIVE on the real broker (not only the harness): 0.7.0_AE_CloudOps~A registered this session at fresh PID 9860 with base 0.7.0_AE_CloudOps concurrently live at PID 8128 -> ALLOWED. Plus CTO's 13/13.
AC3 OVERRIDE AUDITED -- MET. OVERRIDE path + `_audit_identity()`; SERIAL_HELD now audits UNCONDITIONALLY (not only on override), deduped 1-per-(serial,conflict)-per-300s so the 30-60s heartbeat cannot bury the signal.
AC4 EXERCISED not config-read -- MET. CTO ran 13/13 + a NEGATIVE CONTROL (reverted the ruling in-memory; suite goes RED, exit 1 -- AC5 mutant bar). A passing assertion never mutated has never been tested; this one has.

!! AMENDMENT -- READ BEFORE AUDITING THIS GATE !!
<load_bearing_invariants> #1 as ISSUED required refusing BOTH conflict kinds: the CROSS *and* "whose claimed serial is live at a different fresh-heartbeat PID" (SERIAL_HELD). **The second clause was NARROWED from REFUSE to ADVISORY (WARN + audit + PROCEED) by CTO arch-ruling 2026-07-13.** The landed code does NOT hard-refuse SERIAL_HELD, deliberately. Do not read that as a defect or an incomplete build.

WHY (CTO, verbatim reasoning): CROSS is a LOGICAL impossibility -- one process cannot be two agents -- so the refusal has no false-positive branch and costs nothing. SERIAL_HELD is an EMPIRICAL claim resting on a predicate COARSER THAN THE CLAIM IT LICENSES: `_pid_alive(pid)` answers "does SOME process hold this PID," not "is THAT AGENT alive." Two ways it bites: a lingering orphan MCP process, and RECYCLED WINDOWS PIDS (incumbent dies, Windows reassigns the PID, the real agent respawns inside the 120s STALE_THRESHOLD -> the guard refuses the REAL agent its OWN serial). A false-refuse there means an agent CANNOT REGISTER AT ALL -- invisible to every liveness scan, fabric-check, and /drive sweep -- and the population most exposed is agents that just died and are RESPAWNING, i.e. the recovery path. A guard that blocks recovery converts a TRANSIENT failure into a PERMANENT one: that is not a smaller SEV, it is the same SEV from the other side. Advisory takes us from ZERO signal to a measured one without adding a new way to lose an agent.

PROMOTION PATH (open): SERIAL_HELD -> HARD is revisitable on evidence. The unconditional audit rows in `org/mcp/agent-spawn-audit.log` ARE that evidence. **CAVEAT (0.7.0_AE_CloudOps~A, raised to CTO 052513Z): the audit rows only begin accruing per-session at each MCP-server restart that picks up 786fb085d -- the guard was already ENFORCING pre-land from the uncommitted working tree (the MCP server loads server.py off DISK, not from git; verified this session: the live tool docstring carried the G-A text while `git show HEAD:org/mcp/server.py | grep -c "IDENTITY GUARD"` returned 0), but that pre-land build had no audit rows. So the denominator is "MCP servers started since the land," NOT wall-clock-since-commit. A quiet audit log is currently indistinguishable from "no session is running the auditing code yet." Do not promote (2) off a row count that cannot show its denominator.**

CLASS NAMED (CTO): AN INSTRUMENT WHOSE VERDICT CANNOT SEE THE DISTINCTION IT IS BEING ASKED TO LICENSE -- same shape as comp-iam modelling (action) but never (action,resource), and ps-as-a-delivery-oracle.
</completion>
</task_order>
