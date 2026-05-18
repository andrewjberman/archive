<task_order>
  <metadata>
    <id>record-terraform-deploy-changelog-scoping-fix</id>
    <slug>record-terraform-deploy-changelog-scoping-fix</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-18</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED GO 2026-05-18. Ad-hoc tooling fix, no project, no gate. One cross-domain note: record-terraform-deploy.sh is shared CI tooling AE 0.7.0 has touched (ADHC_DRIFTD.003) -- see cross_domain_coordination.</dispatch_unblock_condition>
    <priority>P2 -- tooling debt, not on any critical path. infra/aws/terraform/inf-pipeline/CHANGELOG.json is 88,832 lines and grows ~12k lines per deploy; it bloats git operations + every CHANGELOG read. Worth fixing but not urgent.</priority>
    <sla>~2-4h wall -- a scoped fix to the CHANGELOG writer + a conservative one-time compaction.</sla>
  </metadata>

  <references>
    <surfaced_by>AE 0.7.0 RUNDATE-DISPATCH-IMPL session 2026-05-18 -- flagged record-terraform-deploy.sh writes a ~12k-line CHANGELOG entry per deploy: it dumps the full repo `git log` since the previous inf-pipeline deploy (1986 commits this run) into the `commits` array, and `functions_updated` lists ALL functions managed by the pipeline, not just the changed ones.</surfaced_by>
    <file>infra/aws/lambda/ci/record-terraform-deploy.sh -- the CHANGELOG.json writer is a temp-JS block (`TMPJS_CHANGELOG`, ~lines 416-540): `functions_updated: updatedFunctions.sort()` (~line 501), `commits: gitLogRecords` (~line 502), the git-log fetch (~line 436-459), legacy-array-form handling (~line 510).</file>
    <prior_touch>ADHC_DRIFTD.003 (2026-05-13) already edited this file's git-log block (NUL-safe parsing) -- comments at ~line 407. The DRIFTD lane has context here.</prior_touch>
    <changelog_path>infra/aws/terraform/{pipeline}/CHANGELOG.json -- current sizes: inf-pipeline 88,832 lines, bd-pipeline 17,332, portal-auth 16,564, news 8,853, yang 6,958; others 1.9-2k.</changelog_path>
  </references>

  <context>
    record-terraform-deploy.sh records each Terraform deploy into infra/aws/terraform/{pipeline}/CHANGELOG.json. Two writer behaviors bloat it:
    1. `commits[]` is built from a repo-wide `git log` over the entire commit range since the previous deploy of that pipeline -- so a CHANGELOG entry carries ~2,000 commits (12k lines) the vast majority of which touched nothing in the pipeline.
    2. `functions_updated` lists every function the pipeline manages, not the functions whose source actually changed in this deploy.
    The result: inf-pipeline/CHANGELOG.json at 88,832 lines, growing ~12k/deploy. The fix scopes both fields to the deploy's actual relevant content, plus a conservative one-time compaction of the existing bloat.
  </context>

  <scope>
    <step>
      Phase 1 -- scope the `commits[]` field. The CHANGELOG entry's `commits` array should carry only commits RELEVANT to the pipeline being deployed -- commits that touched the pipeline's source paths -- not the full repo git-log. record-terraform-deploy.sh already knows the PIPELINE and its functions/source dirs (it does per-function `git log -1 -- <source_dir>`). Scope the git-log fetch with a pathspec restricted to the pipeline's source directories (and the pipeline's Terraform dir). Preserve the ADHC_DRIFTD.003 NUL-safe parsing. If a deploy genuinely has zero pipeline-touching commits, an empty array is correct.
    </step>
    <step>
      Phase 2 -- scope `functions_updated`. Emit only the functions whose source SHA actually changed since the previous CHANGELOG entry, not all managed functions. The per-function source-SHA the script already computes is the basis -- diff it against the prior entry's record.
    </step>
    <step>
      Phase 3 -- conservative one-time compaction of the existing CHANGELOG.json files. For each pipeline's CHANGELOG.json, trim the oversized `commits[]` arrays in HISTORICAL entries to the same scoped/relevant set (or, if the per-entry pipeline-relevant set cannot be reconstructed retroactively, cap each historical `commits[]` at a reasonable bound, e.g. the most recent N, with a note). PRESERVE every entry's version, date, functions, and all non-commits metadata -- this trims a derived informational field, it does NOT delete deploy history. Verify entry COUNT is unchanged before/after per file. The legacy array-form CHANGELOG (inf-pipeline) noted at ~line 510 needs its shape respected.
    </step>
    <step>
      Phase 4 -- verify + commit. Run record-terraform-deploy.sh in a dry-run / test mode if one exists, or simulate the JS writer against a sample, to confirm a new entry is scoped (small). Commit per CLAUDE.md (safe-commit.sh, agent author).
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>sed -n '400,540p' infra/aws/lambda/ci/record-terraform-deploy.sh</run>
        <expect>The CHANGELOG writer block is visible -- the git-log fetch, gitLogRecords, updatedFunctions, the legacy-array handling. Ground the edit in the actual current code.</expect>
        <if_mismatch>If the line range has shifted, locate the TMPJS_CHANGELOG block and the `commits:` / `functions_updated:` keys directly.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>for f in infra/aws/terraform/*/CHANGELOG.json; do echo "$(wc -l < "$f") $f"; done</run>
        <expect>Post-compaction line counts materially reduced from the pre-fix baseline (inf-pipeline was 88,832). Entry counts unchanged (verified separately via a jq length check per file).</expect>
        <if_mismatch>If an entry count changed, the compaction deleted history -- revert and redo conservatively.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>CI tooling + a JSON record-file edit; no S3 data, no pipeline data, no reprocessing. CHANGELOG.json is a deploy-record metadata file.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    record-terraform-deploy.sh (infra/aws/lambda/ci/) is shared CI tooling. AE 0.7.0 edited it under ADHC_DRIFTD.003 (NUL-safe git-log parsing) and is the CloudOps/CI lane. Before committing: MCP 0.7.0 to confirm no concurrent edit to record-terraform-deploy.sh and to give them awareness (it is their lane-adjacent tooling). IF the owned-paths pre-commit hook lane-blocks an 0.5.0 commit to infra/aws/lambda/ci/, do NOT force past it -- surface to COO; 0.7.0 commits on your behalf (the ADHC_OWNPTH.010 XXX.md handoff pattern). The CHANGELOG.json files under infra/aws/terraform/{pipeline}/ are deploy records, not lane-owned source -- the compaction commit should be clean.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">A new CHANGELOG entry's `commits[]` carries only commits that touched the deployed pipeline's source/Terraform paths -- not the full repo git-log. Demonstrated on a test/dry-run or a simulated writer run.</ac>
    <ac id="AC2">`functions_updated` lists only functions whose source actually changed in the deploy, not all managed functions.</ac>
    <ac id="AC3">The existing CHANGELOG.json files are compacted: historical `commits[]` arrays trimmed/scoped; line counts materially reduced (inf-pipeline well under its 88,832 baseline). Entry COUNT per file is unchanged (jq-verified) -- no deploy history deleted; version/date/functions metadata intact.</ac>
    <ac id="AC4">The ADHC_DRIFTD.003 NUL-safe git-log parsing is preserved; the legacy array-form CHANGELOG shape is respected; no emoji; CLAUDE.md Rule 16 honored (record-terraform-deploy.sh is local-runtime).</ac>
    <ac id="AC5">Session log with the Compiler Tools section. RAVC2 to COO with the before/after line counts + the entry-count-unchanged verification + the 0.7.0 coordination record.</ac>
  </acceptance_criteria>

  <deliverables>
    - Fixed infra/aws/lambda/ci/record-terraform-deploy.sh (scoped commits[] + functions_updated).
    - Compacted infra/aws/terraform/*/CHANGELOG.json files.
    - Session log under org/tier2_senior/0.5.0_AE_OpalETL/logs/2026-05-18/ with the Compiler Tools section.
    - RAVC2 to COO.
  </deliverables>
</task_order>
