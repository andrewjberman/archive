<to_id>NFRA_COMPAWS.SFN-FIX</to_id>
<project>NFRA_COMPAWS</project>
<title>StepFunctions cert fix: SFN-INVOKES-NESTED-GAP -- ASL walker recurse nested Parallel/Map + emit SFN->Lambda INVOKES edges + re-cert (closes the comp-graph blast-radius coverage hole)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>1.0.0_SA_CTO (comp-aws owner -- spec'd this; architectural beat if the walker structure needs it); 3.0.0_SA_CVO (re-certifies the StepFunctions node class after)</consult>
<issued_by>2.0.0_SA_COO (orig 2026-06-10; CTO-spec'd refinement 2026-06-18 per the comp-aws-owner call on the AE TO-recon SFN coverage-hole finding)</issued_by>
<issued_date>2026-06-10 (CTO-spec refined 2026-06-18)</issued_date>
<status>complete</status>
<!-- CLOSEOUT 2026-06-29 (0.7.0_AE_CloudOps~B, COO self-pull GO 183228Z; readiness-read RAVC 183527Z). The CORE landed + was CVO-certified 06-08, BEFORE the 06-18 TO-refinement (the refinement post-dated the fix; the 06-18 recon mis-flagged it open -- stale-registry class). Grounded:
- AC1/AC2 (recursive walk + both Map syntaxes + both resource forms incl FunctionName-from-Parameters + arn co-key): DONE in HEAD -- comp_aws_cli.py:624-664 (_walk_asl_states recurses Branches/ItemProcessor/Iterator at any depth; _sfn_task_invokes resolves direct-arn + arn:aws:states::: SDK-integration Parameters.FunctionName/FunctionArn with the .$-runtime-ref guard). Fix e13e93391. AC1 RE-VERIFIED LIVE 2026-06-29: comp-kuzu STATE_MACHINE-[:INVOKES]->count = 27 on the HEAD-current canonical graph (full nested set, not the top-level-only subset).
- AC5 (CVO re-cert): cee3f6993 -- StepFunctions CERTIFIED 1.00, INVOKES 26/26 vs live truth, recall 0.346->1.0 (0 missed/spurious/dangling). AC4 (comp-iam reconcile vs complete set) rode the cert.
- AC3 (regression fixture): WAS the only gap -- AUTHORED 2026-06-29 (org/modules/graph/tests/test_sfn_asl_walker.py, 3 tests pass: nested Parallel + both Map syntaxes + both resource forms extracted, runtime-ref skipped, _walk_asl_states recursion-depth contract). tests/ is ANY_EXEC -> left in the working tree, HANDED TO CVO to commit in-lane (CVO is the re-cert owner). Substantively complete; CVO commits the guard + re-confirms.
-->
<!-- ORIGINAL: active -- queued (security-scanner correctness gap; behind AE live work, NOT backlog-buried) -->
<priority>SECURITY-CORRECTNESS GAP (CTO comp-aws-owner call 2026-06-18). comp-aws blast-radius is the DESTRUCTIVE-OP pre-gate (trade-recon teardown precedent: "0 cross-edges" before a teardown). The SFN-nested-Parallel blind spot means a "0 cross-edges" verdict could be FALSE for any of the 17 SFN-orchestrated Lambdas -- the exact by-EDGE-not-by-NAME failure the pre-gate exists to prevent. BOUNDED (1 STATE_MACHINE, 17 known edges, no imminent destructive op) -> queued behind AE's live work (P4 done; NFRA_GRAPHS D7/D8, INFRPT P2/P3 are live), but it gets a TO not a backlog row. STANDING MITIGATION until this lands: the BINDING INTERIM CAVEAT (manual SFN-Parallel cross-check before any destructive-op blast-radius; COO-enforced as the pre-gate driver; CTO-banked to the destructive-op-pre-gate memory).</priority>

<context>
AE's TO-recon zombie-sweep (2026-06-18) surfaced this open under NFRA_COMPAWS (then mis-flagged complete; COO-corrected to ACTIVE mid-ramp 796c6ecf3). CVO cert-authority: the StepFunctions node-class is genuinely UNCERTED (this gap blocks it). CTO comp-aws-owner: MATERIAL but bounded -- fix it. The graph models exactly 1 STATE_MACHINE whose 17 nested-Parallel Lambda invokes are under-extracted.
</context>

<scope>
PROBLEM: comp_aws_cli.py's ASL walker enumerates Lambda invokes from TOP-LEVEL States only; it does NOT recurse nested Parallel/Map containers -> ~17 SFN->Lambda INVOKES edges missing for the 1 STATE_MACHINE. comp-graph consumes the walker, so comp-blast/comp-iam UNDER-REPORT those edges (the SFN-nested blast-radius hole).

FIX (CTO spec):
1. ASL walker -- recurse into nested state containers at ANY depth:
   - Parallel.Branches[].States
   - Map.Iterator.States AND Map.ItemProcessor.States (handle BOTH the classic and the newer Distributed-Map syntax).
   Extract every Task state whose Resource is a Lambda invoke, at any nesting depth.
2. Match BOTH Lambda-invoke resource forms:
   (a) direct: Resource = arn:aws:lambda:...:function:NAME[:alias/version];
   (b) optimized service integration: Resource = arn:aws:states:::lambda:invoke (+ .waitForTaskToken) with Parameters.FunctionName = the arn/name -> RESOLVE FunctionName-from-Parameters too, not just the direct-arn form.
3. Emit SFN->Lambda INVOKES edges -- the SAME edge type comp-blast/comp-iam traverse -- for each extracted invoke, keyed on the resolved Lambda ARN (arn-form node_id, NOT name; the co-key discipline).
4. comp-iam -- check the SM execution role's lambda:InvokeFunction grants against the NOW-COMPLETE invoke set (comp-iam gaps for the SM role reconciles against all ~17, not the top-level subset).
Lane files: org/modules/graph/comp_aws_cli.py + extract_iam.py.
</scope>

<compiler_tools_mandate>
  <phase id="2" when="before commit">
    <step>
      <run>build the REGRESSION fixture: an ASL def with a Lambda Task nested in a Parallel branch AND one nested in a Map -> run the walker on it</run>
      <expect>The walker extracts BOTH nested invokes (and the top-level ones). This fixture guards the recursion so it cannot silently regress.</expect>
      <if_mismatch>STOP. If the fixture's nested invokes are not extracted, the recursion is incomplete -- the whole fix is the recursion.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-kuzu "MATCH (sm:STATE_MACHINE)-[:INVOKES]->(l) RETURN count(l)" on the live graph after re-derive</run>
      <expect>The 1 STATE_MACHINE's full invoke set (top-level + nested Parallel/Map) appears as INVOKES edges; count reconciles to the ASL ground truth (expect +~17 vs the prior top-level-only subset).</expect>
      <if_mismatch>The INVOKES count must reconcile to the hand-counted ASL invokes -- a miss means a nesting case (Parallel vs Iterator vs ItemProcessor, or the FunctionName-from-Parameters form) is still unhandled.</if_mismatch>
    </step>
    <step>
      <run>comp-blast on each previously-missed target Lambda + comp-iam gaps for the SM execution role</run>
      <expect>comp-blast on each previously-missed Lambda now shows the SM as an inbound edge; comp-iam gaps for the SM role runs against the COMPLETE invoke set.</expect>
      <if_mismatch>If a previously-missed Lambda still shows no inbound SM edge, the emit (step 3) or the arn-form co-key is wrong.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
The INVOKES edge type is consumed by comp-blast + comp-iam (the destructive-op pre-gate). This fix CHANGES their output (adds ~17 edges) -- that's the intended correctness fix, not drift. CVO re-certifies the StepFunctions node-class against the now-complete invoke set. Until this lands, the COO-enforced interim caveat (manual SFN-Parallel cross-check before destructive ops) is the standing mitigation. comp-aws extractor lane = AE; CTO-spec'd (owner).
</cross_domain_coordination>

<acceptance_criteria>
1. Full invoke set (top-level + nested Parallel/Map, both Map syntaxes, both resource forms incl FunctionName-from-Parameters) appears as INVOKES edges; count reconciles to ASL ground truth (+~17).
2. comp-blast on each previously-missed target Lambda now shows the SM as an inbound edge.
3. REGRESSION fixture committed: an ASL def with a Lambda Task nested in a Parallel branch AND one in a Map -> the walker extracts both (guards against silent recursion regression).
4. comp-iam gaps for the SM execution role runs against the complete invoke set.
5. CVO re-certifies the StepFunctions node-class.
6. Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail vs <expect>. Missing rows = REWORK.
RAVC2 to COO + CVO (CC CTO -- comp-aws owner).
</acceptance_criteria>

<dependencies>
  <dependency project="NFRA_COMPAWS" note="ACTIVE mid-ramp; this is the StepFn-cert ramp limb" status="active"/>
</dependencies>

<references>
  <ref type="spec">CTO comp-aws-owner spec, MCP 154924Z 2026-06-18</ref>
  <ref type="code">org/modules/graph/comp_aws_cli.py (ASL walker) + extract_iam.py</ref>
  <ref type="memory">destructive-op-pre-gate (the interim caveat; CTO-banked) + reference_comp_aws_graph_blast_radius_destructive_op_pregate</ref>
</references>

<lane_note>
AE (comp-aws extractor), CTO-spec'd (owner). QUEUED behind AE's live work -- not critical-path, but NOT backlog-buried (security-scanner correctness gap). The interim caveat binds the safety side IMMEDIATELY (COO-enforced); this TO closes the gap DURABLY. Ping CTO if the walker structure needs an architectural beat at authoring. AE flagged ready. CVO re-cert + RAVC2 to COO+CVO+CTO at close.
</lane_note>
