<task_order>
<to_id>ADHOC.record-terraform-deploy-cotenant-sweep-fix</to_id>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_to>0.8.0_AE_CloudComp~B</issued_to>
<date>2026-08-03</date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "record-terraform-deploy-cotenant-sweep-f" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>P2 (deploy-record integrity; interim discipline already issued to DT by CTO -- post-commit diff verify)</priority>

<title>record-terraform-deploy.sh: stop sweeping co-tenant dirty hunks of lambda-source-map.json into deploy-record commits</title>

<context>
LIVE INSTANCE (2026-08-03): DT's yang deploy-record commit fa6f891aeb swept 0.7.0_AE_CloudOps~E's
UNCOMMITTED inf files-list hunk of infra/aws/lambda/ci/lambda-source-map.json into a commit
authored by DT -- the map is now ahead of the repo record for an entry its committer never touched
(~E + MSTR notified 16:06Z by DT, who caught it post-commit).

MECHANISM (source-grounded @46d4b1110d): infra/aws/lambda/ci/record-terraform-deploy.sh
  :457  git diff --quiet <map>   -- skips only if the WHOLE file is unchanged
  :463  git add <map>            -- stages the WHOLE file, co-tenant hunks and all
The map is a SHARED file (exact-file owned-paths rule .owned-paths.yaml:1472 exists precisely
because every pipeline's deploys write it), so concurrent-agent dirty state is the normal case,
not an edge case. Note the script ALREADY computes the legitimately-changed function set (~:643,
used for the source-map-sha reconcile) -- the comparison substrate for this fix exists in-script.

CTO-endorsed fix shape (msg 20260803T162132Z to COO): pre-commit diff check inside the script --
if the map delta contains hunks OUTSIDE the deploying module's entries, ABORT naming the
co-tenant hunks, or warn-and-require an explicit audited override flag.

Same instrument-honesty genre as your R4-A TO (ADHOC.r4a-closeout-trigger-false-attribution-fix,
also staged at your seat) -- pick them up together; sequence at your discretion.
</context>

<scope>
1. In record-terraform-deploy.sh, before the :463 git add: parse the map's unstaged delta
   (git diff -U0 on the map), derive the set of function entries with changed hunks, and compare
   against the deploying module's legitimately-changed function set the script already computes.
   - Delta entries ALL within the deploying set -> proceed exactly as today.
   - Any delta entry OUTSIDE it -> ABORT before staging, printing each co-tenant entry name and
     the owning hunk, with remediation text (co-tenant commits their hunk first, or override).
   - Override: an explicit env flag (e.g. SWEEP_OVERRIDE="<reason>") that proceeds and appends an
     audited line (timestamp, deployer, co-tenant entries, reason) to an org/ audit log -- follow
     the existing GIT_COMMIT_AUTHOR_OVERRIDE audit-line pattern. No silent path.
2. Do NOT change: the CHANGELOG co-staging (:673, already module-scoped), the resource-map
   delegation (:146-147), the source-map-sha reconcile, or any deploy mechanics.
3. Check record-resource-deploy.sh (the :147 delegate) for the same whole-file-stage pattern on
   its {module}-resource-map.json; if the class exists there, fix it in the same shape (per-module
   resource maps may be single-tenant -- if so, record WHY it is out of class instead of patching).
4. No alarms, no SNS, no notification machinery (standing moratorium) -- the deliverable is an
   ABORT/audit gate inside the existing script, nothing that pages anyone.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-grep "record-terraform-deploy" infra .tools org</run>
      <expect>Caller census enumerated (deploy protocols, docs, any wrapper). No caller passes staged co-tenant state on purpose; nobody depends on the sweep.</expect>
      <if_mismatch>STOP. A caller relying on whole-file staging is a design conflict -- surface to COO+CTO before writing.</if_mismatch>
    </step>
    <step>
      <run>git log --oneline -5 -- infra/aws/lambda/ci/lambda-source-map.json</run>
      <expect>fa6f891aeb present in recent history (the live instance); note whether further sweeps landed since -- each is evidence for the abort path's remediation text.</expect>
      <if_mismatch>Document what you find; proceed.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Exercise BOTH directions in a scratch working tree: (a) NEGATIVE CONTROL -- plant a dirty co-tenant hunk on a non-deploying entry, run the record step, expect ABORT naming that entry and ZERO commit created; (b) POSITIVE CONTROL (separate invocation) -- only the deploying module's entries dirty, expect the record commit to proceed byte-identical to today's behavior; (c) OVERRIDE -- same as (a) with the flag set, expect commit + audited line.</run>
      <expect>All three discriminate: (a) aborts, (b) passes, (c) passes with audit line. Print the audit line verbatim in your log.</expect>
      <if_mismatch>STOP. A gate that cannot fail is not a gate; do not commit until all three behave.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>git log --oneline -3 -- infra/aws/lambda/ci/record-terraform-deploy.sh</run>
      <expect>Your fix commit present, no interleaved co-edit.</expect>
      <if_mismatch>Surface to COO.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. Negative control: co-tenant dirty hunk -> ABORT pre-stage, entry named, zero commit. Exercised, output reproduced in log.
2. Positive control (isolated invocation): deploying-module-only delta -> proceeds unchanged. Exercised.
3. Override path: audited line written (timestamp, deployer, co-tenant entries, reason); no silent variant exists. Exercised.
4. record-resource-deploy.sh either fixed in the same shape or ruled out-of-class with the reason recorded.
5. Session log Compiler Tools section reproduces every <run> + observed output + pass/fail vs <expect>. Missing rows = REWORK.
</acceptance_criteria>

<cross_domain_coordination>
The script is written by every pipeline deploy (DT + full AE set). The FIX touches only the ci/
script itself. Interim discipline (DT post-commit diff verify) stands until this lands -- your
close message should tell DT + CTO the interim discipline can be retired. The swept ~E hunk
itself is ~E's to reconcile (already notified); do NOT revert or re-commit their map entry.
</cross_domain_coordination>

<references>
  <ref type="cto-route">org/mcp/inbox/2.0.0_SA_COO/read/20260803T162132Z_1.0.0_SA_CTO_ROUTE__record-terraform-deploy.sh_sweeps.md</ref>
  <ref type="live-instance">commit fa6f891aeb (yang deploy-record sweeping ~E's inf hunk)</ref>
  <ref type="sibling">org/tier2_senior/0.8.0_AE_CloudComp/task_orders/r4a-closeout-trigger-false-attribution-fix.md</ref>
</references>

<acceptance_note>
A TO completion report whose session log lacks the Compiler Tools reproduction is REWORK, not
COMPLETE (TO_COMPILER_GATE).
</acceptance_note>
</task_order>
