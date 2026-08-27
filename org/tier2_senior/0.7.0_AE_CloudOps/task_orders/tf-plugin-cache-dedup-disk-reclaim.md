<to_id>tf-plugin-cache-dedup-disk-reclaim</to_id>
<project>ad-hoc (CVO P1 finding 20260612T131323Z; no registered project)</project>
<title>TF plugin-cache dedup — set TF_PLUGIN_CACHE_DIR machine-wide, then confirm-gated purge of 30 duplicated AWS provider copies (~20GB reclaim)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CVO finding routed 131323Z; MSTR ground-truth 131300Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "ad-hoc (CVO P1 finding 20260612T131323Z;" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: staged</status>
<priority>P1-operational — C: at 96% with transient 100% spike 13:05Z; every fresh `terraform init` adds ~700MB until fixed</priority>

<references>
  <ref type="finding">CVO MCP 20260612T131323Z — 30x terraform-provider-aws_v5.100.0_x5.exe (~700MB each) = 21GB under infra/aws/terraform/*/.terraform/providers; TF_PLUGIN_CACHE_DIR verified unset; 4 copies freshly pulled in last 24h (aaii-v2/causality/news-v2/smartx-v2 lifecycle inits)</ref>
</references>

<scope>
1. **Cache config (do first):** set `TF_PLUGIN_CACHE_DIR=%USERPROFILE%\.terraform.d\plugin-cache` machine-wide (`setx`) AND `plugin_cache_dir` in `%APPDATA%\terraform.rc` (or `~/.terraformrc` for the Git Bash path — cover whichever the fabric's `.tools/terraform.exe` invocations actually read; verify empirically with TF_LOG). Create the cache dir.
   **CONCURRENCY CAVEAT (evaluate before flipping):** Terraform's plugin cache is documented as NOT safe for concurrent `terraform init` across processes. This fabric runs multi-agent. Mitigations to evaluate: (a) accept-and-document (inits are rare + exec-serialized through safe-apply/deploy wrappers), (b) wrap init in the workspace mkdir-mutex pattern, or (c) per-agent cache dirs (still bounds copies at N-agents, not N-modules). Pick one, document the choice in the TO closeout — do not silently default.
2. **Verify:** a `terraform init` on one module pulls/links from the cache (no new ~700MB under the module).
3. **Purge (Andrew-confirm-gated — recursive delete class):** after (1)+(2) verified, delete the per-module `.terraform/providers` dirs (regenerable via `terraform init`). ~20GB reclaim. Per CLAUDE.md autonomy rules this recursive deletion REQUIRES human confirmation — present Andrew the exact dir list + sizes and proceed only on his confirm. Modules with imminent planned applies: re-init immediately after purge to avoid surprising the next deploy.
4. **Do NOT touch** the secondary consumers CVO listed (.git packs, .bun, Docker, ms-playwright, Desktop/"New folder") — out of scope; surface separately if Andrew wants a broader pass.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>du -sh infra/aws/terraform/*/.terraform/providers 2>/dev/null | sort -rh | head -35; echo $TF_PLUGIN_CACHE_DIR</run>
      <expect>Reproduce CVO's census (~30 dirs, ~700MB each); env confirmed unset.</expect>
      <if_mismatch>State changed since the finding — re-derive before acting (verify-before-fix).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="after cache config, before purge">
    <step>
      <run>terraform init on ONE low-stakes module (pick a 0-pending-diff one); inspect module .terraform/providers + cache dir</run>
      <expect>Provider resolved FROM the cache (symlink/copy semantics per platform); no new full ~700MB copy in the module dir; module still plans 0-diff.</expect>
      <if_mismatch>STOP. Do not purge anything while the cache path is unproven.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="purge">
    <step>
      <run>Present Andrew the exact rm list + total size; on confirm, delete; then terraform init + plan on 2 spot-check modules</run>
      <expect>Both re-init from cache and plan with no provider errors; disk reclaim ~20GB verified (df before/after).</expect>
      <if_mismatch>Restore path = terraform init re-pulls from registry (slow but safe); surface any plan diff to COO immediately.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- Touches EVERY terraform root module's local state dir — coordinate with any in-flight terraform work before the purge step (currently none live; re-check at execution). The OpalETL causality teardown (COO-timing-held) uses terraform — sequence the purge before or cleanly after, not during.
</cross_domain_coordination>

<acceptance_criteria>
- TF_PLUGIN_CACHE_DIR effective for the fabric's actual invocation paths (PowerShell + Git Bash), demonstrated with one cached init.
- Concurrency-mitigation choice documented.
- Purge executed only on Andrew confirm; ~20GB reclaimed (df evidence); 2 spot-check modules re-init + plan clean.
- Session log Compiler Tools section reproduces every `<run>` + observed output + pass/fail vs `<expect>`.
- RAVC2 evidence to COO; CC CVO (finding originator) for verify-channel close.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Local tooling/disk hygiene; no data-path changes.</no_reprocess_needed></data_reprocess_scope>
