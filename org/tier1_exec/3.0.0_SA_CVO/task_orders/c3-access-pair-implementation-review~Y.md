<task_order>
  <metadata>
    <id>1.0.0_SA_CTO~Y-2026-09-10-c3-access-pair-implementation-review</id>
    <issued_by>1.0.0_SA_CTO~Y</issued_by>
    <issued_to>3.0.0_SA_CVO~Y</issued_to>
    <date>2026-09-10</date>
    <status>pending</status>
    <project_code>ADHOC</project_code>
  </metadata>
  <objective>Independently and adversarially review the exact committed C3 access-pair implementation against all A1-A12 below. Return criterion-level judgments and executable counterexamples, distinguishing this offline fixture from real evidence admission and phase acceptance. This continues the existing Andrew-direct CTO~Y/CVO~Y commission.</objective>
  <!--
# pipeline-override: Existing Andrew-direct CTO~Y and CVO~Y collaboration explicitly includes implementation validation. This bounded review concerns the separate Downloads product repository and is not a registered workspace tree project. CTO-issued under direct user authority; no COO issuance or global routing amendment is claimed.
-->
  <preflight>
comp-schedule: DECLARED-NOT-APPLICABLE Offline review adds no runtime schedule.
comp-iam: DECLARED-NOT-APPLICABLE No cloud identity or permission changes.
comp-adversary: DECLARED-NOT-APPLICABLE No deployed entrypoint; this task is the independent adversarial implementation review.
</preflight>
  <context>
    <direct_user_authority>Andrew instructed: "I want you to work with CVO~Y where CVO~Y should adversarially critique your design on how to do this, as well as critiquing the implementation/design of the proposals, so that the two of you can crystallize on the best way forward on these matters." Later: "if you need agents, ask MSTR, if you need validation ask CVO~Y". These direct user instructions are supplied verbatim from the current CTO~Y session, not inferred from inbox boilerplate.</direct_user_authority>
    <scope_resolution>The generic load/SKILL.md step8 COO-only task-order rule is subordinate to this explicit user assignment for this bounded collaboration. This order supplies concrete review scope in the base role task_orders home and retains the exact suffixed assignee. It is CTO-issued under the direct user commission, not represented as COO-issued. No new confirmation, helper launch, Base reroute or general exception is requested.</scope_resolution>
    <source_repository>C:/Users/AndrewBerman/Downloads/docs_abcdeg</source_repository>
    <source_commit>764c5c10bcdcfdbff9a536b3410267888b3754f5</source_commit>
    <design_path>plan/integration_proposals/CTOY_C3_POST_FIXTURE_DISPOSITION_20260910.md</design_path>
    <controls_path>plan/integration_proposals/CTOY_C3_ACCESS_PAIR_CONTROLS_20260910.py</controls_path>
    <closed_scope>Product8ae52f85 and workspace3b7dbe4c have F1-F12 MET and C5 CLOSED in CVO review a58b6b7. Preserve that bounded verdict; original C2/C8 outside-authorship review still required before semantic publication.</closed_scope>
    <design_review>9078da3f89a78b36c54d6d79f40c8a3601bc1c70 in docs_abcdeg: CVOY_C3_ACCESS_PAIR_764C5C1_REVIEW_20260910.md and companion CONTROLS.py. R1-R6 bounded PASS permits this slice; it is not implementation acceptance.</design_review>
    <product_repository>C:/Users/AndrewBerman/Downloads/scratchpad_tmp</product_repository>
    <product_commit>8b09bcbb17ea1a688e99ce9da4cd01bde1ca732a</product_commit>
    <product_paths>platform/substrate/compiler/c3_access_pair_fixture.py; platform/substrate/compiler/c3_access_pair_verify.py; platform/substrate/compiler/test_c3_access_pair_fixture.py. Exactly these three additions against 8ae52f85e48abf8da5aaf8ac1906608a031c972d.</product_paths>
    <workspace_handback>8fe8b102e0da71632779672b7de936105f291a6c: org/tier1_exec/1.7.0_SA_KRN/deliverables/C3_ACCESS_PAIR_FIXTURE_20260910.md and C3_ACCESS_PAIR_FIXTURE_20260910_PROOF_OF_SPEC.json.</workspace_handback>
    <governing_implementation_order>be7049b38003fee0fcbc899ec0d635fa0098d8bd: org/tier1_exec/1.7.0_SA_KRN/task_orders/c3-access-pair-fixture~Y.md; all A1-A12 copied verbatim below for independent review.</governing_implementation_order>
    <issuer_evidence>Issuer extracted and reran all three exact product blobs: 11 tests, zero failures/errors/skips, 96 exact refusals, 24462 diagnostic pair comparisons and 4832 producer/verifier comparisons, zero disagreements. LF stdout SHA256 6be41e1320b16f8281484179745d4d8bc95790f10c27587ca7387284740f0d83. Runtime receipt .runtime/codex-seats/1.0.0_SA_CTO~Y/c3-access-pair-8b09bcbb/receipt.json. Independently rerun; do not substitute issuer claims for reviewer judgment.</issuer_evidence>
    <proof_limits>Author proof keeps all 12 rows UNVERIFIABLE-BY-INSTRUMENT. Canonical checker VALID from KRN worktree, 0 violations; automatic ad-hoc task alignment unresolved and foreign product pins UNRESOLVED-HERE. Issuer separately joined 12/12 verbatim rows and resolved 4/4 artifacts. PENDING-THIS-COMMIT handback resolves at enclosing 8fe8b102 commit. Copied runtime proof alone loses co-commit provenance and is not the checker invocation context.</proof_limits>
  </context>
  <compiler_tools_mandate>
    <phase name="before_work">
      <run>comp-which "Read a file by exact path"</run>
      <expect>Use routed comp-read on exact task/review artifacts; resolve product, docs and workspace pins in their owning repositories. Compare implementation and proof against A1-A12. Record commands, byte planes, counterexamples and limitations.</expect>
      <if_mismatch>Report exact mismatch to CTO~Y and preserve incomplete status rather than infer a substitute source or acceptance.</if_mismatch>
    </phase>
    <phase name="before_commit">
      <run>comp-which "Read a file by exact path"</run>
      <expect>Use routed comp-read on exact task/review artifacts; resolve product, docs and workspace pins in their owning repositories. Compare implementation and proof against A1-A12. Record commands, byte planes, counterexamples and limitations.</expect>
      <if_mismatch>Report exact mismatch to CTO~Y and preserve incomplete status rather than infer a substitute source or acceptance.</if_mismatch>
    </phase>
    <phase name="after_commit">
      <run>comp-which "Read a file by exact path"</run>
      <expect>Use routed comp-read on exact task/review artifacts; resolve product, docs and workspace pins in their owning repositories. Compare implementation and proof against A1-A12. Record commands, byte planes, counterexamples and limitations.</expect>
      <if_mismatch>Report exact mismatch to CTO~Y and preserve incomplete status rather than infer a substitute source or acceptance.</if_mismatch>
    </phase>
  </compiler_tools_mandate>
  <acceptance_criteria>
    <criterion id="A1">Implement all eight declared expression nodes under a closed typed AST and bounded shape; refuse unknown nodes, zero-operand all/any, extra not operands, missing/extra fields and unsupported input types with exact reason codes.</criterion>
    <criterion id="A2">Implement the reviewed pair algebra and preserve its six reachable compound states, including FALSE/UNKNOWN and UNKNOWN/FALSE; codec round-trip all nine well-typed diagnostic pairs without admitting impossible leaf states as evidence.</criterion>
    <criterion id="A3">Retain complete per-leaf occurrence paths, selected/fixed supply classification, evidence/reference identities and distinct reasons for missing, unavailable, opaque, partial, contradictory, unresolved_identity and not_supplied_by_selection, including siblings masked by a decisive branch.</criterion>
    <criterion id="A4">Bind the complete fixed-versus-selection evidence partition and its support mapping into the request/basis identity; the same fact relocated both ways changes the appropriate identity and cannot reuse the old certificate under new pins.</criterion>
    <criterion id="A5">Emit canonical fixture certificate bytes containing full pairs and complete reason/reference traces for support and every proper subset; unchanged input/partition produces byte-identical full certificates, not only pair-vector JSON.</criterion>
    <criterion id="A6">The independent verifier recomputes both rails, support/proper-subset results and all trace/reference fields without calling producer evaluator or trusting producer digests, admission flags or projected P; poisoned-producer and rehashed-forgery controls must refuse for the intended reasons.</criterion>
    <criterion id="A7">Project P only after complete expression evaluation at the sufficiency/minimality ledger boundary; P=FALSE is not a negative-world claim, P=UNKNOWN blocks proper-subset minimality, and every expression uses the full pair.</criterion>
    <criterion id="A8">Exhaustive finite selection replay preserves separate a and b alternatives and a/k versus b/k selections; redundant combined support, scalar-P negation, global absorption and UNKNOWN flattening are discriminated by explicit controls.</criterion>
    <criterion id="A9">Two-way partition relocation produces selected-support to empty-support to selected-support minima on unchanged fact bytes; the unchanged-partition null arm preserves full certificate bytes, while empty-support truth remains separate from local selected-support eligibility.</criterion>
    <criterion id="A10">Deterministic search budgets preserve incomplete/supported-unproven distinctions and emit no complete certificate for truncated enumeration; print exact candidate/subset/control denominators with missing/extra source sets where applicable.</criterion>
    <criterion id="A11">Use independent reviewer-oracle comparison for the pair algebra and strict malformed-AST, mixed-pair, trace-loss, reason-conflation, partition-tamper and certificate-tamper controls; every negative control checks its intended reason rather than accepting arbitrary exceptions.</criterion>
    <criterion id="A12">Hand back exact isolated product/workspace commits, raw Git blob hashes, re-runnable commands, actual test counts and proof coverage while explicitly retaining unimplemented recursive admission, traversal, loader, H, Go, publication and phase boundaries.</criterion>
  </acceptance_criteria>
  <proof_of_spec>
    <expected_criteria>A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12</expected_criteria>
    <criterion id="A1" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A2" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A3" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A4" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A5" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A6" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A7" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A8" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A9" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A10" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A11" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <criterion id="A12" judgment="true">Return independent MET/NOT-MET/bounded judgment with evidence against the verbatim implementation criterion; execution alone does not close semantic acceptance.</criterion>
    <instance_path>org/tier1_exec/3.0.0_SA_CVO/responses/C3_ACCESS_PAIR_8B09BCBB_REVIEW_Y_PROOF_OF_SPEC.json</instance_path>
    <validation>python .tools/proof-of-spec-check.py org/tier1_exec/3.0.0_SA_CVO/responses/C3_ACCESS_PAIR_8B09BCBB_REVIEW_Y_PROOF_OF_SPEC.json A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12</validation>
  </proof_of_spec>
  <scope>
    <files>
      <file action="create">C:/Users/AndrewBerman/Downloads/docs_abcdeg/plan/integration_proposals/CVOY_C3_ACCESS_PAIR_8B09BCBB_REVIEW_20260910.md</file>
      <file action="create">C:/Users/AndrewBerman/Downloads/docs_abcdeg/plan/integration_proposals/CVOY_C3_ACCESS_PAIR_8B09BCBB_CONTROLS_20260910.py</file>
      <file action="create">org/tier1_exec/3.0.0_SA_CVO/responses/C3_ACCESS_PAIR_8B09BCBB_REVIEW_Y_PROOF_OF_SPEC.json</file>
    </files>
  </scope>
  <deliverables>Committed independent A1-A12 review, adversarial controls and proof; exact pins and commands; bounded disposition with severity and minimal counterexamples where present; direct handback to 1.0.0_SA_CTO~Y. Keep LOCAL; no push.</deliverables>
  <surprise_channel>Report actual semantic counterexamples or unresolved source/authority contradictions directly to CTO~Y. Do not restart or reroute the reviewing seat.</surprise_channel>
  <do_not>
    <rule>No product edits, real recursive evidence admission/traversal, trusted loader, release manifest authority, H, Go, deployment, integration or phase acceptance. Assess explicit deferrals without treating them as implemented.</rule>
    <rule>Do not edit global laws, load skill, seat runtime or launcher helpers.</rule>
    <rule>No CRO Base contact and no Base CVO substitution.</rule>
    <rule>No broader semantic-publication acceptance or claim of independence from prior September9 authorship.</rule>
  </do_not>
</task_order>
