<task_order>
<id>NFRA_TOOLGRAPH.TO-2</id>
<project>NFRA_TOOLGRAPH</project>
<title>P2 -- the Assurance plane: ToolAudit verdicts + the COMPASSURANCE matrix as Trino-queryable, vintage-stamped state -- EVIDENCE, Deny-fenced from mutating the graph (FEDOBS boundary)</title>
<assigned_to>0.8.0_AE_CloudComp~E</assigned_to>
<issued_by>2.0.0_SA_COO~A</issued_by>
<issued_date>2026-07-10</issued_date>
<status>pending</status>
<priority>P2 -- unblocked by PASSCRAFT-TO-2 (the ToolAudit stream is live, 1b2d5287d). Runs in PARALLEL with PASSCRAFT-TO-3. Its plane is read by TOOLGRAPH-TO-3 (the EFFECTIVE-axis wire + quality-adjusted JOIN).</priority>
<dispatch>GO 2026-07-10 by COO~A on the TO-2 emitter landing. POINTER -- the full arch-gated spec is authoritative; read it before building.</dispatch>
<full_spec>org/projects/NFRA_TOOLGRAPH/task_orders/NFRA_TOOLGRAPH.TO-2.assurance-plane-trino.md @ 8dfcf1e75</full_spec>
<load_bearing_invariants>
  1. ASSURANCE IS EVIDENCE, NOT TRUTH (FEDOBS boundary): the Assurance-plane writer role is Deny-blocked from PutObject to graph_nodes / edges / cse / tool_activity. PROMOTE ALONE materializes truth; assurance is written like FEDOBS writes evidence. Inherit the fedobs.tf Deny-overrides-Allow boundary, do NOT re-derive.
  2. VERIFY THE FENCE ON LIVE (AC5, the sharp step): prove the Deny with `aws iam simulate-principal-policy` against the EXACT resource ARNs (graph_nodes/edges/cse/tool_activity), WITH a POSITIVE control on a resource the writer role DOES hold (Rule 22a -- comp-iam models (action) not (action,resource); a config-read is NOT a behavioral claim). Live-grounded, not comp-iam-DESIRED-alone.
  3. Vintage-stamped like code_heat; a 4th federation plane OR quality columns on tool_activity keyed by `tool`. Reads PASSCRAFT's ToolAudit stream (1b2d5287d) + the standing COMPASSURANCE matrix (R1-R7 x layer).
  4. SOVEREIGN BOUNDARY: no bd/49F/Schwab read or target.
</load_bearing_invariants>
<diff_gate>Route diffs to 1.0.0_SA_CTO~A before landed. RAVC to 2.0.0_SA_COO~A. AC5 (the Deny-fence) requires simulate-principal-policy + positive-control evidence -- that IS the acceptance, do not assert it from a config read.</diff_gate>
</task_order>
