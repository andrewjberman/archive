<task_order>
  <metadata>
    <id>partners-api-changelog-malformed-json-repair</id>
    <slug>partners-api-changelog-malformed-json-repair</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. Ad-hoc follow-up to the CHANGELOG-scoping fix, no gate. Same cross-domain note: infra/aws/lambda/ci tooling-adjacent -- coordinate with AE 0.7.0 if needed; the CHANGELOG.json file itself is a deploy record, not lane-owned source.</dispatch_unblock_condition>
    <priority>P2 -- a pre-existing latent defect. infra/aws/terraform/partners-api/CHANGELOG.json is malformed JSON; record-terraform-deploy.sh's CHANGELOG write throws JSON.parse on it, so every future partners-api Terraform deploy fails to record. Not on a critical path, but it silently breaks deploy-recording for that pipeline.</priority>
    <sla>~1-2h wall -- a small malformed-JSON repair + verification. Smallest TO in the lane.</sla>
  </metadata>

  <references>
    <surfaced_by>0.5.0_AE_OpalETL RAVC2 on the record-terraform-deploy CHANGELOG-scoping fix (commit 1071d5719) -- the compaction pass skip-and-warned partners-api/CHANGELOG.json as malformed; flagged as an out-of-scope follow-up.</surfaced_by>
    <file>infra/aws/terraform/partners-api/CHANGELOG.json -- 232 lines. Confirmed INVALID JSON (jq parse fails).</file>
    <malformation>A valid JSON object (the canonical `{ ... "entries": [ ... ] }` form) ends at ~line 220. Lines 221+ are garbage appended AFTER the valid document: a dangling fragment (`"version": "partners-api-v1.7.0", "changes": [...]` with no enclosing object) followed by a separate duplicate `{ "version": "partners-api-v1.7.0", "changes": [...] }` object. Two JSON values + a fragment concatenated = unparseable.</malformation>
    <consequence>record-terraform-deploy.sh's CHANGELOG writer does `JSON.parse(existing CHANGELOG)` -- it throws on this file, so the partners-api CHANGELOG write is silently skipped on every deploy (the "Note: CHANGELOG.json write failed" path).</consequence>
  </references>

  <context>
    The record-terraform-deploy CHANGELOG-scoping fix (1071d5719) compacted 8 bloated CHANGELOG.json files. partners-api/CHANGELOG.json was correctly NOT compacted (it is 232 lines, not bloated) and skip-and-warned because it is malformed JSON. This TO repairs it. The repair is a contained JSON-correctness fix -- restore the file to a single valid JSON document so record-terraform-deploy.sh can parse and append to it.
  </context>

  <scope>
    <step>
      Phase 1 -- diagnose the trailing content. The valid object ends ~line 220. After it: a dangling `partners-api-v1.7.0` fragment + a duplicate `partners-api-v1.7.0` object. DETERMINE: is `partners-api-v1.7.0` ALREADY present as an entry inside the valid object's `entries[]` array?
      - If YES -> the trailing content is pure duplicate garbage; the repair is to delete everything after the valid object's closing brace.
      - If NO -> `partners-api-v1.7.0` is a real deploy entry that was appended but never merged into `entries[]`; the repair is to merge ONE clean v1.7.0 entry into `entries[]` in correct chronological position (matching the file's existing entry schema), then delete the trailing garbage.
    </step>
    <step>
      Phase 2 -- apply the repair so the file is a single valid JSON document in the canonical CHANGELOG shape (the same `{ ... "entries": [ ... ] }` shape record-terraform-deploy.sh reads/writes). Do NOT lose any genuine deploy entry; do NOT introduce a duplicate.
    </step>
    <step>
      Phase 3 -- verify: `jq '.' infra/aws/terraform/partners-api/CHANGELOG.json` parses clean; the entry set is correct (every real partners-api deploy entry present exactly once); and a simulated record-terraform-deploy.sh CHANGELOG-writer run against the repaired file succeeds (no JSON.parse throw). Commit per CLAUDE.md (safe-commit.sh, agent author).
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>jq -e '.entries[] | select(.version=="partners-api-v1.7.0")' infra/aws/terraform/partners-api/CHANGELOG.json 2>&1 ; echo "exit: $?"</run>
        <expect>Determines whether partners-api-v1.7.0 is already an entry in the valid object -- the Phase-1 duplicate-vs-unmerged decision. (jq will fail to parse the whole file; if so, extract the valid object first -- read lines 1..~220 -- and run the check against that.)</expect>
        <if_mismatch>If the valid-object boundary is not at ~line 220, locate the first balanced top-level `}` and treat everything after it as the trailing garbage.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>jq '.entries | length' infra/aws/terraform/partners-api/CHANGELOG.json</run>
        <expect>A clean integer -- the file parses, and the entry count reflects every real deploy entry exactly once.</expect>
        <if_mismatch>Still malformed or an entry lost/duplicated -- fix before closing.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>A JSON-correctness repair of a deploy-record metadata file; no S3 data, no pipeline data, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    <none/> -- infra/aws/terraform/partners-api/CHANGELOG.json is a deploy-record file, not lane-owned source; the repair commit should be clean. No edit to record-terraform-deploy.sh itself (that file is correct as of 1071d5719). If the owned-paths hook unexpectedly lane-blocks the commit, surface to COO per the established handoff pattern.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">infra/aws/terraform/partners-api/CHANGELOG.json parses as valid JSON (`jq '.'` succeeds) -- a single document in the canonical CHANGELOG shape.</ac>
    <ac id="AC2">The Phase-1 duplicate-vs-unmerged determination is documented; partners-api-v1.7.0 appears in `entries[]` exactly once (whether it was merged in or was already present + the trailing copy deleted) -- no genuine deploy entry lost, no duplicate introduced.</ac>
    <ac id="AC3">A simulated record-terraform-deploy.sh CHANGELOG-writer run against the repaired file succeeds (no JSON.parse throw) -- the defect that broke partners-api deploy-recording is cleared.</ac>
    <ac id="AC4">No emoji; CLAUDE.md Rule 16 honored. Session log with the Compiler Tools section. RAVC2 to COO with the before/after + the Phase-1 determination.</ac>
  </acceptance_criteria>

  <deliverables>
    - Repaired infra/aws/terraform/partners-api/CHANGELOG.json (valid JSON, canonical shape).
    - Session log under org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO.
  </deliverables>
</task_order>
