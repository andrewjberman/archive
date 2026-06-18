<to_id>NFRA_TSGRAPH.P4</to_id>
<project>NFRA_TSGRAPH</project>
<title>P4 — cross-domain ServedURL->S3->Lambda->gold stitch (full fine-lineage / goal-1; resolves the P1-AC5-backend NNA D_00f/D_00c instance)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_design>0.4.0_DE_ClientPlatform (the P0-stitch: edge ownership, URL normalization, the FE-graph join point)</co_design>
<parity_gate_reviewer>1.0.0_SA_CTO (cross-domain join correctness + the D8 key-space constraint = the cutover/accept gate)</parity_gate_reviewer>
<issued_by>2.0.0_SA_COO (Andrew drive-directive via the 5m loop = work-auth; CTO ruled it a co-designed P4 follow-on; base-AE scoped + flagged 231757Z)</issued_by>
<issued_date>2026-06-17</issued_date>
<status>complete -- SHIPPED + ACCEPTED 2026-06-18. P4 cross-domain SERVED_FROM live-landed via atomic 5-leg ledger (tsgraph-p4-servedfrom, CLOSED, commit 4dc5d08be): grant 36231cc50 (s3:GetObject on opal-data-portal-v2/json/*, CTO+COO never-widen signed) -> safe-apply 0/1/0 -> image rebuilt (in-container sha d9432c119484351a verified) -> re-derive (marker f79542e8) -> 29 SERVED_FROM both-ends-verified LIVE on canonical graph under the REAL derive task-role. CTO gate-#5 RAVC2 ACCEPTED (20260618T132015Z, independent live-graph verify). /seams MECHANICAL silent-no-op RESOLVED. 4 visible-unresolved = confirmed-absent stale-FE objects (no grant/no widen). NFRA_TSGRAPH stays ACTIVE (P2/P3 ahead); COO reconciles project phase P4->complete. Status flipped this cycle (zombie cleanup -- was stale at 'active' post-accept).</status>
<priority>HIGH — Andrew-direct (chose drive-P4-now over winding down). Rides NFRA_TSGRAPH as the P4 leg (PRD P4-scope), NOT a new project. The substrate (P1 semantic graph) is live; P4 stitches it to the cloud/trace domain = the full fine-lineage (goal-1) + the backend half of AC5.</priority>

<context>
P1 delivered the FE semantic graph (live on Nessie->Kuzu, validated-complete, CTO cutover pending). P1-AC5 met the FE-VISIBLE forked-FLOWS_TO (the leaderboard name dual-source fork). The BACKEND instance of the NNA divergence (D_00f vs D_00c — two gold scripts feeding the same served nna field) is cross-domain: it needs the served-artifact -> S3 -> producer-Lambda -> gold stitch that the FE extractor cannot reach. CTO ruled this the P4 leg. base-AE scoped the chain as resolvable: ServedURL->S3(bucket,key) via comp-routes (CF behavior) + S3->producer via pipescript --resource, CO-KEYED on the canonical S3-key by construction (honors the D8 key-space lesson — the critical constraint CTO flagged).
</context>

<deliverable>
The derive-side SERVED_FROM (and producer) edges that stitch the FE semantic graph's DataFetch/ServedURL nodes to the cloud/trace domain (S3 object -> producer Lambda -> gold script), CO-KEYED on the canonical S3-key (no name-keyed joins — the D8 lesson). Co-design base-AE (derive/globgrph cloud side) + DE (the FE-graph join point + URL normalization). The result: a query can traverse a served portal value back through S3 to the producing gold script — the full goal-1 fine-lineage — and the NNA D_00f/D_00c two-gold-script divergence surfaces as a cross-graph fork.
</deliverable>

<acceptance_criteria>
AC1 CROSS-DOMAIN JOIN: a served URL resolves end-to-end (ServedURL -> S3 bucket/key -> producer Lambda -> gold script) CO-KEYED on the canonical S3-key, queryable via comp-kuzu. 0 name-keyed joins (the D8 key-space discipline).
AC2 BINDING LIVE-RESOLVE TEST: the architect_leaderboard end-to-end resolve passes LIVE (not local/synthetic) — the served leaderboard artifact traces back to its producing gold script(s).
AC3 NO-SILENT-UNKNOWN: any unresolvable hop (dynamic key, missing map entry) marked unresolved + VISIBLE, NEVER a false edge (the platform law).
AC4 AC5-BACKEND VISIBLE: the NNA D_00f/D_00c two-gold-script divergence (both feeding the served nna field) surfaces as a cross-graph fork — the backend instance of P1-AC5, now reachable.
AC5 PARITY/ACCEPT: CTO reviews the cross-domain join correctness + the key-space discipline = the accept gate. RAVC2 to COO (CC CTO).
</acceptance_criteria>

<lane_note>
Owned-paths: base-AE owns the derive-side (globgrph/kuzu_nessie_load, the cloud stitch); DE owns the extractor (tsgraph_spike, the FE-graph join point). CO-DESIGN = author-by-co-design, COMMIT-THROUGH-OWNER on each side's surface (per the CTO-ratified owned-paths convention). Andrew's drive-directive is the work-auth — base-AE drives NOW, does NOT pause for this TO (the TO formalizes/tracks the leg + the gate; it does not gate the in-flight design). The design refines via base-AE+DE+CTO co-design; this TO captures the scope + ACs + the accept gate.
</lane_note>
