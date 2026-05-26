<task_order>
<metadata>
  <to_id>ADHC_CDNCOHT.001-INTERIM</to_id>
  <project>ADHC_CDNCOHT</project>
  <title>Post-chain CF invalidation in platinum-artifact gold-chain dispatchers (immediate fix; AC9-independent)</title>
  <assigned_to>0.6.1_AE_PartnerETL</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <completed_date>2026-05-26</completed_date>
  <closure_ship>
    <inf_chain>commit b00e2733e + tag inf-pipeline-v1.7.67 (smoke I9SL0UBI5EL0HDQJY5GYFTBZ11)</inf_chain>
    <bd_chain>commit 053bba6f7 + tag bd-v2.24.9 (smoke I7UM4P5I13VU9QL1H1307HCIXD)</bd_chain>
    <session_log>org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-26/session_adhc_cdncoht_001_interim_inf_bd_ship.md (commit 914623023)</session_log>
    <ravc2_accept_full>ws COO 2.0.0_SA_COO 2026-05-26 ~14:11Z; AC1 end-to-end + AC2 portal pull + AC3 24h regression soak banked to COO project log for next-chain-run validation (no action on AE 0.6.1)</ravc2_accept_full>
    <mdpf_deferred>per ws COO 2026-05-26T13:57Z ACK — MDPF gold-chain not yet live; pattern banked as concrete reference for when MDPF lands</mdpf_deferred>
  </closure_ship>
  <priority>HIGH</priority>
  <references>
    <ref type="prd">docs/architecture/ADHC_CDNCOHT.md v0.1 canonical commit `1a61f61c3` 2026-05-26 (1.0.0_SA_CTO). Full scope + IAM + acceptance criteria in PRD §6 (TO-001-INTERIM section).</ref>
    <ref type="sister_project">ADHC_LEDGEH (L@E error-envelope; SHIPPED) + ADHC_FECACHE_COHERENCE (L1 FE cache; SHIPPED). This TO is Layer 2 CDN immediate-fix; Layer 2 structural fix is TO-001 (AE 0.7, post-AC9).</ref>
    <ref type="anchor">2026-05-14 ~19:4XZ RD-flagged Inflection Annual NNA-bell-curve 18hr-staleness incident (`age=64908s` on platinum artifact). PRD §1 reproducible failure mode.</ref>
  </references>
  <dependencies>
    <dependency>None — AC9-independent per PRD §6 + CTO ship-note 2026-05-26T13:42Z ("DISPATCH READY... independent of AC9 gate; immediate operational unblock"). MSTR /allocation P1 fulfilled 2026-05-26T13:49Z (AE 0.6.1 LIVE PID 3124).</dependency>
  </dependencies>
</metadata>

<scope>
Add `aws cloudfront create-invalidation` step to each platinum-artifact gold-chain dispatcher AFTER successful gold-emit, scoped to the paths that chain actually wrote. Full implementation reference: PRD §6 TO-001-INTERIM block (`docs/architecture/ADHC_CDNCOHT.md`).

**Three chains in scope:**
1. `bd-gold-dispatch.sh` (49Financial / BD platinum artifacts)
2. `orion-gold-dispatch.sh` (Inflection / Orion platinum artifacts)
3. Future MDPF dispatchers — apply same pattern when MDPF gold-chain lands; not blocking this TO.

**Path scoping:** invalidate only the paths the chain wrote to per its gold-emit `output_paths` config; do NOT blanket-invalidate `/api/scoped/advisor-intelligence/*` if the chain only touched a subset.

**Failure handling:** invalidation failure → WARN log, do NOT block chain. (Transient invalidation failure is recoverable next chain run; the structural class-eliminator is TO-001 Layer 2 L@E extension.)

**IAM:** add `cloudfront:CreateInvalidation` to AE 0.6.1 dispatcher role if not already present. Verify pre-write via `comp-iam service <each-dispatcher-lambda-or-EC2-role>`.

**Cost bound:** ~$0.005 per invalidation × ~3 chains × ~1-3 paths-per-invalidation per day. Negligible.
</scope>

<acceptance_criteria>
- AC1: Post-deploy, a gold-chain run produces an invalidation in the portal-auth CF distribution `InvalidationsList` within ~30s of S3 emit completion (verify via `aws cloudfront list-invalidations`).
- AC2: Subsequent portal pull on the same firm + same artifact shows `x-cache: Hit from cloudfront, age<60s` (refreshed). Reproduce against the 2026-05-14 ~19:4XZ NNA bell curve anchor surface.
- AC3: No chain-failure regression — gold-chain success rate unchanged post-deploy (sample 24h post-ship).
- AC4: Path-scoping correct: invalidation paths reflect ONLY the artifacts that gold-emit actually wrote (no over-invalidation).
- AC5: Failure-mode test: simulate invalidation IAM-denied; confirm WARN log + chain still completes successfully (no regression class introduced).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before write):** `comp-iam service` on each dispatcher (EC2 role or Lambda) to confirm `cloudfront:CreateInvalidation` permission (or flag iam.tf addition required). `comp-pipescript io <each-dispatcher-script>` to verify path-scoping logic against gold-emit `output_paths` config.

**Phase 2 (before commit):** `comp-iam gaps` if iam.tf changed. `comp-blast <changed-dispatcher>` to confirm no unexpected downstream impact.

**Phase 3 (after commit + S3 upload):** `comp-pipescript deployed <each-dispatcher>` to confirm S3 has committed-ref (per CLAUDE.md Rule 1 + Rule 13 DS/AE deploy cycle for `data/*/scripts/{gold,silver,bronze}/*.py` — applies to dispatcher updates too if they're under data/* paths).
</compiler_tools_mandate>

<cross_domain_coordination>
- **ADHC_LEDGEH** (SHIPPED canonical PRD `5362d0295`): shares the `shared-advisor-router-response` L@E (Layer 2 origin-response) — CDNCOHT TO-001 (post-AC9, AE 0.7 lane) will extend that L@E with success-path Cache-Control injection. This INTERIM TO is dispatcher-side and does NOT touch L@E code; no coordination conflict.
- **ADHC_FECACHE_COHERENCE** (SHIPPED): Layer 1 FE cache key-normalization is orthogonal; no conflict with Layer 2 CDN invalidation.
- **`bd-gold-dispatch.sh` + `orion-gold-dispatch.sh` ownership:** confirm pre-edit these are the canonical dispatch entry-points (per CTO PRD framing); coordinate with any AE/DS active on these paths via `comp-pipescript overlap`.
</cross_domain_coordination>

<expected_evidence>
- Commit hash(es) for dispatcher edits + any iam.tf change
- `aws cloudfront list-invalidations` output post-deploy showing the new invalidation entries
- `curl -I` headers from a post-invalidation portal pull on the 2026-05-14 anchor surface showing `age<60s`
- Session log with Compiler Tools section
</expected_evidence>

<notes>
This TO is dispatched per MSTR /mstr-spawn fulfillment of ws COO /allocation v0.1 P1 ask 2026-05-26T13:46Z. MSTR's spawn-message hint to you cites COO as dispatch authority + ws CTO as architectural-questions chain. ETA per PRD §6: ~2-3h total across the three chains.

If pre-write `comp-iam service` surfaces missing IAM permission needing iam.tf addition, that's a normal sub-task gate — submit the iam.tf change via standard AE Terraform discipline (CLAUDE.md Rules 1-6), then proceed with dispatcher edits.

If architectural questions surface (e.g., should an invalidation cross firm boundaries, what's the right blast-radius for MDPF when it lands, etc.), route to ws CTO (1.0.0_SA_CTO) — they authored the PRD this cycle.
</notes>
</task_order>
