<task_order>
<to_id>NFRA_MSBEFF.R5</to_id>
<title>KEY/PARTITION ENUMERATION PRIMITIVE — close the single largest measured rail-override demand: "which keys/partitions exist", which agents currently answer with raw aws calls because no comp-tool does</title>
<issued_by>1.0.0_SA_CTO~Z</issued_by>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<date>2026-07-23</date>
<status>pending</status>
<priority>P2 — highest MEASURED demand of any missing capability</priority>

<authority>
Andrew-direct 2026-07-23 (verbatim in NFRA_MSBEFF.R1R3 authority block): 0.8.0 works the full MSBEFF
remediation set; ~Z authors + delivers TOs direct. No standard-change gate needed (new capability).
CLAUDE.md Rule 21's own law is the trigger: "a repeat override for one intent = a coverage gap ->
build the tool."
</authority>

<evidence_base>
Rail log measurement (CS1-4, org/.../CASE_STUDY_1_MDPF_ARC.md): 597 DENYs, rising 175 (Jun) -> 421
(Jul). Class split: infra_grep 259 / aws_freshness 178 / aws_iam_inspect 85. The 178 aws_freshness
overrides are mostly NOT freshness questions — sampled reasons: "key-discovery for DS's staged Global
artifact", "content-enumeration of served per-firm key sets", "earliest-partition discovery for the
backfill-ceiling question, not freshness". NL corpus corroborates from the other side, signal-3,
agent-verbatim: "no comp-tool enumerates per-table partition dates" and "comp-freshness lacks an
arbitrary/raw-prefix mode (the recurring aws_freshness override; CVO-corroborated)".
</evidence_base>

<scope>
Give agents a first-class way to ask WHAT EXISTS, distinct from IS IT FRESH.
Shape is yours (a `comp-freshness --raw-prefix` mode or a separate `comp-keys` primitive — pick on
the evidence and say why). Required capability set, drawn from the actual override intents:
  A. Enumerate keys under an arbitrary prefix (not only modeled/registered artifacts).
  B. Per-table / per-prefix PARTITION DATE enumeration (earliest, latest, gaps) — the backfill-ceiling
     and depth questions.
  C. Existence check across a firm/scope set ("which of these served keys exist per firm").
Bind to the firm registry (data/firm_registry.json) where a firm axis applies, so scope questions are
complete-over a declared scope rather than a hand-typed list.
CARRY THE R1R3 OUTPUT CONTRACT: this tool ships WITH its coverage + plane/vintage lines (it reads a
live plane; say so).
LAW: this is an INSPECTION tool. Timestamps must be explicit-Z (`s3api`, not bare `aws s3 ls` local
time — VERIFICATION LAW 11, five prior tool-hits) and it must never render a zero as an answer without
its denominator (a true-zero on the wrong prefix is the misleading-PASS class).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-which "which keys exist under this prefix" + comp-freshness --help; read org/mcp/comp-which-rail.log for the aws_freshness override reasons (the requirements are literally written there by the agents who needed them)</run>
    <expect>The build's capability list is DERIVED from the logged override intents, with the denominator of overrides read stated.</expect></step>
  </phase>
  <phase id="2" when="before commit">
    <step><run>MUTANT: a prefix that does not exist must return a LOUD not-found with its denominator, never a clean empty (the "true 0 on the wrong pattern" class, corpus-named). Positive control on a prefix known to hold N keys.</run>
    <expect>Both on the record; controls run as SEPARATE invocations.</expect></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>Replay 3 real overrides from the rail log through the new tool.</run>
    <expect>All three answerable with no rail override needed; paste the before-override reason and the after-tool output.</expect></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
Shares the firm registry with NFRA_PSTMRT P1 (read-only consumer; do not alter its schema — v1 frozen-additive, ~Z gate). Shares output framing with NFRA_MSBEFF.R1R3 — build R1R3's helper first or land this tool with the contract retrofitted in the same wave.
</cross_domain_coordination>

<acceptance_criteria>
1. The three capabilities (arbitrary-prefix enumeration, partition-date enumeration incl. gaps, per-scope existence) are exercised on live estate prefixes, outputs pasted.
2. Not-found mutant + isolated positive control on the record.
3. Explicit-Z timestamps everywhere (grep the source: no bare `aws s3 ls` parsing of LastModified).
4. Three real rail-override intents replayed and answered without an override.
5. Registered per the registration invariant (coverage + plane declared) — it is a NEW tool, so it is the first live test of R1R3 condition (a).
6. Session log + compiler-tools-log line.
</acceptance_criteria>

<verification>3.0.0_SA_CVO~Z. Report to 1.0.0_SA_CTO~Z.</verification>
</task_order>
