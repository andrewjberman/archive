<task_order>
<id>safe-commit-F-read-override-fix</id>
<project>ad-hoc (NFRA-tooling; Andrew-requested, CTO-approved)</project>
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<status>staged</status>
<priority>P2 (Andrew-requested, NOT urgent/not-blocking; BUILD POST-MDPF-CUTOVER -- see gate)</priority>
<date>2026-07-21</date>

<references>
  <ref type="finding">CVO safe-commit -F-read finding (Andrew-requested); CTO approval + spec @ CTO 230431Z</ref>
  <ref type="record">LD-0276 (-F mandated for non-trivial commit bodies); F-010 (git gate denies -m with backtick/$( )</ref>
</references>

<hard_gate>
DO NOT BUILD/APPLY UNTIL THE MDPF_REVAMP CUTOVER + the cot-rebalancer deploy have LANDED. safe-commit.sh is
the CORE commit gate EVERY agent uses; a change to it (even additive) during the live P0 risks the whole
fabric's commit path while agents are mid-cutover (DS incremental producer commits, 0.6.2 cot deploy, all
coordination commits). Not urgent (DS works around it). COO releases this gate + routes the spawn post-cutover.
</hard_gate>

<objective>
Make safe-commit.sh read the system-current-override trailer from the -F commit-body FILE (in addition to
the existing -m read), so the LD-0276-mandated -F path can carry the override that the F-010 git gate blocks
on -m (a -m body with $( is denied). Restores the mandated commit path's ability to carry the override
(15 DS overrides is the current tax of the gap).
</objective>

<scope>
  <in>
    - safe-commit.sh ~:535-540 (the override-trailer read): ALSO parse the override trailer from the -F file's
      contents, not only from the -m argument. F-010-safe: the -F file is NEVER shell-parsed, so reading the
      override from it introduces no injection surface (unlike -m).
    - Preserve the existing -m read (additive, no behavior removal for -m callers).
  </in>
  <out>
    - The :530 trigger SCOPE-CALIBRATION (over-firing on DS WIP ledgers) is DEFERRED to post-fix (CTO ruled:
      land the -F-read fix first, re-assess the over-rate after). NOT in this TO.
    - No other safe-commit behavior change.
  </out>
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>Read safe-commit.sh :530-545 (the trigger + override-read block) + confirm the -F file path variable</run>
      <expect>Locate the exact -m override read; identify the -F file var to read the trailer from.</expect>
      <if_mismatch>STOP. Ground the exact lines before editing a core gate.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>Self-test: a -F commit carrying `# system-current-override: <reason>` in the body -> the override is READ + honored (matches the -m behavior). A -F body WITHOUT the trailer -> unchanged (no false override).</run>
      <expect>-F-carried override satisfies the gate identically to -m; F-010 gate still denies -m-with-$(. No regression on either path.</expect>
      <if_mismatch>STOP. Do not commit a core-gate change that regresses either path.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
  - CVO (3.0.0_SA_CVO): FOUND the bug -> VERIFIES the fix (independence: verify not build). Confirm a -F-carried override satisfies the gate + no regression, on the real safe-commit.sh.
  - CTO (1.0.0_SA_CTO): approved the fix; may gate the apply (COO to confirm at spawn-time).
</cross_domain_coordination>

<acceptance_criteria>
  1. safe-commit.sh reads the system-current-override from the -F file (verified: a -F commit with the trailer is honored, identically to -m).
  2. No regression: -m path unchanged; F-010 git gate still denies -m-with-$(; a -F body without the trailer is a clean no-override.
  3. CVO independently VERIFIES (found -> confirms) on the real gate.
  4. Session log Compiler Tools section reproduces the self-test + observed result.
</acceptance_criteria>

<dependencies>
  <dependency agent="MDPF_REVAMP cutover + cot deploy" task="land before touching the core commit gate" status="pending (COO releases post-cutover)"/>
</dependencies>
</task_order>
