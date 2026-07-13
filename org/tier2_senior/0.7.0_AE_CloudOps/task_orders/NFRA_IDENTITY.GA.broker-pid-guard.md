<task_order>
<id>NFRA_IDENTITY.G-A</id>
<project>NFRA_IDENTITY</project>
<title>G-A: broker-side PID guard -- register_agent/heartbeat REFUSE a registration whose PID is already LIVE under a different serial (the enforcing chokepoint for the 07-12/13 identity-misadoption SEV)</title>
<assigned_to>0.7.0_AE_CloudOps~A</assigned_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-07-13</issued_date>
<status>pending</status>
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
</task_order>
