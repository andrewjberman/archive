<task_order>
<id>MDPF_3FIRMS.3F-S1</id>
<title>Silver converter mechanism census + land the WS-5 event/sweep half + fix the .xlsx-hardcoded converter regex</title>
<project>MDPF_3FIRMS</project>
<workstream>WS-S (Silver)</workstream>
<issued_to>0.6.2_AE_PartnerETL~A</issued_to>
<joint_assignee>0.7.0_AE_CloudOps (Terraform half — the apply is his, not yours)</joint_assignee>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_at>2026-07-22T20:24Z</issued_at>
<status>staged</status>
<authorization>LD-0333 am.1 @2eef569d2 -> CTO cascade 200805Z -> COO decomposition.</authorization>

<references>
  <ref type="prd">docs/architecture/MDPF_3FIRMS_PRD.md §4 WS-S row 3F-S1; §2.5 RF-9; §8.6 (NEVER#5 ledger)</ref>
  <ref type="prior_work">your WS-5 converter half @6d1a15ef2 — COMMITTED, NOT DEPLOYED</ref>
</references>

<scope>
(a) **Per-source census table**: for every MDPF-feeding source, the tuple {event rule, sweep rule,
    converter script, DEPLOYED hash}. The deployed hash is the point — a repo hash is not a runtime.
(b) **Land the WS-5 event+sweep half** (@6d1a15ef2, committed NOT deployed) through the normal TF cycle.
(c) ⚠ **FIX THE `.xlsx`-HARDCODED CONVERTER REGEX.** RF-9, and it is a trap with a green face: **the
    `.xlsx` extension is hardcoded IN THE CONVERTER REGEX, so an S3-filter-only fix is a GREEN NO-OP** —
    it will pass and change nothing. The fix must be manifest-driven at the regex.

⛔ **VALIDATE ON `mode=="event"` IN THE MANIFEST, NOT ON "parquet landed."** A parquet file appearing
proves *some* path ran — most likely the sweep — and says nothing about whether the EVENT path works.
The event path and the sweep path must EACH be proven once, independently.

⛔ **YOUR PRE-HOLD APPLY GO WAS WITHDRAWN** by CTO under LD-0333, along with Andrew's 1425Z D2 GO. **This
TO does not restore it.** The Terraform apply is 0.7.0's half and requires his own authorization at
fire time. Do not carry any prior GO into this — re-read the carrier at fire time, never the message.

⛔ Terraform is the ONLY Lambda deploy mechanism. No console, no `aws lambda update-function-code`.
NEVER#5: the deploy-completion ledger opens at start and closes in-session, or rolls back loud.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-pipescript deployed</run>
      <expect>Per-tree MATCH/STALE/MISSING for every converter in scope; firm-separated sweep.</expect>
      <if_mismatch>STALE/MISSING is the census input, not a failure — record it. Never trust a producer self-report over the served/deployed artifact.</if_mismatch>
    </step>
    <step>
      <run>comp-iam service &lt;converter lambda&gt;   (0.7.0 half)</run>
      <expect>No missing permissions for the converter's boto3 calls.</expect>
      <if_mismatch>⚠ NECESSARY, NOT SUFFICIENT: comp-iam models (action), never (action, resource) — a role holding s3:GetObject on ANY bucket reports GRANTED for EVERY other. For a NEW bucket/prefix use `simulate-principal-policy` with ONE `--resource-arns` per call and a SEPARATE positive control.</if_mismatch>
    </step>
    <step>
      <run>Read the converter regex at source and confirm the .xlsx hardcode</run>
      <expect>The hardcode located at file:line @ commit-ish.</expect>
      <if_mismatch>If it is NOT hardcoded, RF-9's premise has changed — report before designing a fix for a defect that may not exist.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>.tools/commit-gate.sh on every .py touched</run>
      <expect>py_compile + ds-precommit-check + ruff clean; `from __future__ import annotations` present.</expect>
      <if_mismatch>STOP. Do not commit.</if_mismatch>
    </step>
    <step>
      <run>comp-iam gaps  (0.7.0 half, if iam.tf changed)</run>
      <expect>No new permission gaps.</expect>
      <if_mismatch>STOP; resolve before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>Exercise BOTH paths: one landed-file -> parquet via the EVENT path, and one via the SWEEP path</run>
      <expect>Manifest shows `mode=="event"` for the event exercise. Each path proven ONCE, separately.</expect>
      <if_mismatch>A parquet landing alone does NOT prove the event path. If only the sweep can be shown, say so explicitly — an unproven path is UNVALIDATED, never assumed working.</if_mismatch>
    </step>
    <step>
      <run>comp-pipescript deployed (re-run)</run>
      <expect>MATCH for the newly deployed converters — deployed == repo.</expect>
      <if_mismatch>A STALE after deploy means the artifact did not land. Verify against the runtime, not the build log.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<data_reprocess_scope>
  <reprocess_required>
    **The regex fix CHANGES WHICH FILES CONVERT** — that is its entire purpose. Files previously skipped
    because they were not `.xlsx` were never converted, so affected historical partitions are INCOMPLETE,
    not merely stale.
    - Phase-3 re-ingestion step: identify every source object the OLD regex skipped and the NEW regex
      matches; convert them via the sanctioned sweep path.
    - Verify with `s3api list-objects-v2` (explicit-Z) that post-ingest partition mtimes EXCEED the
      patch-commit time — time-of-patch is NOT time-of-data-freshness.
    - Downstream consumer freshness gate: notify DS (3F-S2 census) so the completeness denominators are
      recomputed AFTER the reprocess, not before.
    Rationale: two incidents in 7 days (C_08 silent-wrongness; SCOPEFIX INFLEC near-miss) where the code
    shipped, S3 had the new script, and consumers still read pre-patch data because nobody re-ran the
    converter.
  </reprocess_required>
</data_reprocess_scope>

<cross_domain_coordination>
  <resource path="Terraform + Lambda deploy" shared_with="0.7.0_AE_CloudOps">
    The TF apply half is HIS. Coordinate before either commits; a `-target`ed, named apply only.
  </resource>
  <resource path="silver partition denominators" shared_with="0.4.0_DS_ClientPlatform (3F-S2)">
    Your reprocess CHANGES DS's census denominators. MCP DS before and after.
  </resource>
</cross_domain_coordination>

<dependencies>
  <dependency agent="0.7.0_AE_CloudOps" task="TF apply half" status="blocked-on-spawn" blocking="true">
    0.7.0 is currently DARK (not registered). The TF half cannot proceed until he is respawned and
    ACKs. Spawn request is with MSTR/Andrew.
  </dependency>
</dependencies>

<acceptance_criteria>
1. Per-source table committed: {event rule, sweep rule, converter script, DEPLOYED hash} for every
   MDPF-feeding source.
2. The WS-5 event+sweep half is DEPLOYED via Terraform with a 0-diff apply, tagged, ledger opened AND
   closed.
3. The `.xlsx` hardcode is fixed AT THE REGEX (manifest-driven), not at the S3 filter — with the
   before/after file:line @ commit-ish cited.
4. **Event path AND sweep path each exercised once, separately.** Manifest `mode=="event"` observed for
   the event exercise. An unproven path is reported UNVALIDATED, never assumed.
5. Reprocess executed per `<data_reprocess_scope>` with post-ingest mtimes verified > patch-commit time.
6. **Session log Compiler Tools section reproduces every `<run>` with observed output and pass/fail vs
   `<expect>`. Missing rows = REWORK.**
</acceptance_criteria>

<escalation>Report to 2.0.0_SA_COO; CTO gates the apply. Escalate if the event path cannot be exercised — a sweep-only proof leaves half the mechanism unverified.</escalation>
</task_order>
