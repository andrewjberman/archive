<task_order>
<id>NFRA_PASSCRAFT.TO-1</id>
<project>NFRA_PASSCRAFT</project>
<title>P1 -- the recon-scaffolding SDK (8-move checklist + 12-shape hunt-order taxonomy + archetype->probe map) + `comp-passcraft recon <tool>` that runs ONLY the mechanical moves and STOPS at the verdict door (AC1/AC4 anti-harness)</title>
<assigned_to>0.8.0_AE_CloudComp</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_PASSCRAFT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>P1 -- FOUNDATION. Runs in PARALLEL with TOOLGRAPH-TO-1. `.tools/comp-passcraft` is a NEW tool -> NOT `.tools/**->BASE_EXEC` daylight-held; build may start now.</priority>
<dispatch>GO 2026-07-10 by 2.0.0_SA_COO~A on Andrew's DIRECT spawn release. CTO~A arch-gate PASS on the TO set. THIS IS A DISPATCH POINTER -- the FULL arch-gated spec (scope, locked_invariants, acceptance_criteria, references) is the authoritative source; read it before building.</dispatch>
<full_spec>org/projects/NFRA_PASSCRAFT/task_orders/NFRA_PASSCRAFT.TO-1.recon-scaffolding-sdk.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. ANTI-HARNESS (PRD sec.0 / AC1 / AC4): no component may compute a pass/fail. `comp-passcraft recon` STOPS at the verdict door -- it has NO verdict engine. If it reads like a harness, it is WRONG. AC1 = show it emits an evidence pack + ZERO verdict; AC4 = inject a KNOWN-DEFECTIVE-verdict tool and prove PASSCRAFT does not auto-flag it (no verdict engine) yet surfaces the archetype's lead probes.
  2. rc-check every evidence command (non-zero rc = INVOCATION-ERROR, not a verdict). Read-only on the estate; self-write-surface only.
  3. SOVEREIGN BOUNDARY: no bd / 49F / Schwab / opal-data-bd read or target (comp-blast cache = names only).
</load_bearing_invariants>
<diff_gate>ROUTE EVERY BUILD DIFF back to 1.0.0_SA_CTO~A for the arch-gate BEFORE it is treated as landed. CTO~A gates diffs, not just the TO set. RAVC to 2.0.0_SA_COO~A on completion.</diff_gate>
</task_order>
