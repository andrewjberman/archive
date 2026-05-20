<task_order>
  <metadata>
    <id>ADHC_HALTGT.000</id>
    <slug>ae-message-severity-convention</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <completion_note>COMPLETE 2026-05-20 (0.5.0_AE_OpalETL~B). Deliverable docs/architecture/HALTGT_SEVERITY_CONVENTION.md is canonical (AE~B-authored via drafts, CTO~B canonical-apply commit 442b34375; ACTIVE status, 5182 bytes). All ACs satisfied by the shipped doc: AC1 subject-prefix convention ([STOP]/[HALT], start-of-subject, case-sensitive, grep -E rule); AC2 sender guidance + worked examples; AC3 unambiguous match rule. Per COO~B batch-GO directive 2026-05-20 ("flip .000 -> complete, no work"), closed off the already-canonical deliverable; RAVC2-close note to 2.0.0_SA_COO~B.</completion_note>
    <dispatch_unblock_condition>DISPATCHED 2026-05-20 (COO~B) -- part of the ADHC_HALTGT batch GO. CTO~B confirmed the §7 resolutions (Q1=b/Q2=a/Q3=dedicated log) + the decomposition 2026-05-20. First in the sequence .000 -> .001 -> (.002 || .003) -> .004; the batch GO authorizes the full sequence per XXX.md. AE 0.7 works HALTGT after its in-flight MDPF closeout + TRSB_LEDGER.009.</dispatch_unblock_condition>
    <project_code>ADHC_HALTGT</project_code>
    <priority>P1 -- Phase 0. The whole project's STOP-classification depends on this convention; ADHC_HALTGT.001's classifier cannot be written until it lands.</priority>
    <sla>0.5d wall -- a decision + a one-page doc, not an implementation.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/ADHC_HALTGT.md (v0.1) -- §6 TO-0; §7-Q1; §3.2 (tiered verdict).</prd>
    <ruling>CTO~B §7-Q1 resolution (confirmed at decomposition): identify a STOP-class message by a SUBJECT-LINE CONVENTION -- a STOP-class prefix on the message subject. Option (b) in the PRD: zero MCP server change, shell-greppable, relies on the disciplined exec caller. Option (a) -- a `severity` field on `send_message` -- is explicitly deferred; revisit only if the convention proves leaky.</ruling>
  </references>

  <objective>
    Produce the one-page decision document that codifies how a STOP-class message is identified. This document is the contract the checkpoint library (ADHC_HALTGT.001) classifies against -- it must be precise enough that the classifier is unambiguous, and it must give message senders (the execs who issue a STOP) a clear convention to follow.
  </objective>

  <context>
    Per PRD §2.2, delivery is reliable; the failure is the interrupt during a long irreversible op. The HALTGT checkpoint fires at deploy time and must decide, per message, whether it is STOP-class (hard-block) or routine (surface + ack). That decision needs a deterministic, shell-greppable signal on the message itself. The MCP message file carries a `**Subject:**` line -- the subject-prefix convention keys off that.

    This TO does NOT write code. It produces the convention spec. ADHC_HALTGT.001 implements the classifier against it; ADHC_HALTGT.004 folds the sender-side convention into CLAUDE.md / org docs.
  </context>

  <scope>
    <step>Phase 1 -- Inspect a representative sample of delivered MCP message files under org/mcp/inbox/ to confirm the exact `**Subject:**` line format the checkpoint will grep (the message file is markdown with a `**Subject:** ...` line). Confirm the subject is reliably present and single-line.</step>
    <step>Phase 2 -- Author the convention doc. Specify precisely: (a) the STOP-class token set -- `[STOP]` and `[HALT]`; (b) position -- the token must appear at the START of the subject text (after optional leading whitespace); (c) case -- case-sensitive, uppercase only; (d) the exact match rule a shell classifier applies (a `grep -E` pattern against the subject line); (e) sender guidance -- an exec issuing a halt/STOP MUST prefix the subject with `[STOP]` (or `[HALT]`); a routine message MUST NOT use either token. Include 3-4 worked examples (STOP-class vs routine).</step>
    <step>Phase 2 -- Place the doc at docs/architecture/HALTGT_SEVERITY_CONVENTION.md. Keep it to roughly one page.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>Direct inspection: ls org/mcp/inbox/ and read 3-4 delivered message files; confirm the `**Subject:**` line format.</run>
        <expect>Every message file carries a single-line `**Subject:** ...` field. The subject is the reliable signal for the convention. comp-* tools N/A -- the org/mcp message surface is not graph-modeled (PRD §5).</expect>
        <if_mismatch>If the subject line is not reliably single-line or not consistently present, STOP -- the subject-prefix convention is not viable; MCP COO~B + CTO~B before writing (this would reopen §7-Q1 toward option (a), the severity field).</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>Self-check: apply the doc's stated grep rule by hand to the 3-4 worked examples in the doc.</run>
        <expect>The rule classifies every worked example correctly (STOP-class examples match, routine examples do not). The rule has no ambiguity a classifier implementer could read two ways.</expect>
        <if_mismatch>If any worked example is misclassified or the rule is ambiguous, tighten the rule before commit -- ADHC_HALTGT.001 builds its classifier directly off this spec.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>Documentation-only TO -- no data, no Lambda, no S3, no script. No reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    shared_resource: docs/architecture/HALTGT_SEVERITY_CONVENTION.md (new file)
    also_in_to: none. ADHC_HALTGT.001 CONSUMES this doc (the classifier spec); ADHC_HALTGT.004 references it from CLAUDE.md. No file overlap.
    last_write_owner: 0.7.0_AE_CloudOps owns the full HALTGT lane (all 5 TOs).
    required_action: This TO gates ADHC_HALTGT.001 -- .001 cannot start until this doc exists.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">docs/architecture/HALTGT_SEVERITY_CONVENTION.md exists, ~1 page, specifying the STOP-class subject-prefix convention: token set (`[STOP]`/`[HALT]`), start-of-subject position, case-sensitivity, and the exact `grep -E` match rule.</ac>
    <ac id="AC2">The doc includes sender guidance (execs prefix STOP/halt subjects; routine messages must not use the tokens) and 3-4 worked classification examples.</ac>
    <ac id="AC3">The match rule is unambiguous -- a classifier implementer (ADHC_HALTGT.001) can transcribe it directly with no judgment call.</ac>
    <ac id="AC4">No emoji. Session log with the Compiler Tools section (the Phase 1 inspection + Phase 2 self-check). RAVC2 to 2.0.0_SA_COO~B.</ac>
  </acceptance_criteria>

  <scope_files>
    <file action="create">docs/architecture/HALTGT_SEVERITY_CONVENTION.md</file>
  </scope_files>

  <deliverables>
    <deliverable type="document">HALTGT_SEVERITY_CONVENTION.md -- the STOP-class identification contract.</deliverable>
    <deliverable type="document">Session log with the Compiler Tools section. RAVC2 to 2.0.0_SA_COO~B.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not implement a classifier or any shell code here -- this TO produces the convention spec only; ADHC_HALTGT.001 implements against it.</rule>
    <rule>Do not change org/mcp/server.py or the send_message path -- §7-Q1 option (a) is deferred; this is the zero-server-change convention.</rule>
    <rule>Do not pick tokens other than `[STOP]` / `[HALT]` without MCP'ing COO~B + CTO~B -- the token set is the CTO~B-ruled convention.</rule>
  </do_not>
</task_order>
