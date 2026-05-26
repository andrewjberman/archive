<task_order>
<metadata>
  <to_id>ADHC_CDNCOHT.001</to_id>
  <project>ADHC_CDNCOHT</project>
  <title>shared-advisor-router-response L@E success-path Cache-Control injection (Option 2 structural fix)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <shipped>2026-05-26T~15:33Z; commits 0a9c90b16 (handler) + be724538a (source-map) + 216dd8a45 (record); tag portal-auth-v1.16.1; 2 terraform applies (Lambda v2 publish 6s + CF distribution 4-behavior :1->:2 pin 1m20s); CF invalidation ID31U80S1MI2V6UGFRQDWOCHAF InProgress per AC7; AC1-AC2 deferred to consolidated TO-VAL per ws COO sequencing; AC3-AC7 closed</shipped>
  <priority>HIGH (canonical CDN staleness class-eliminator; sister to LEDGEH error-envelope already shipped)</priority>
  <references>
    <ref type="prd">docs/architecture/ADHC_CDNCOHT.md v0.2 canonical commit `c5262507c` 2026-05-26 (1.0.0_SA_CTO; REPAIR-AMENDMENT (a) accepting blanket pattern for TO-001-INTERIM). Full scope + AC + pseudocode in PRD §3.1 + §6.</ref>
    <ref type="sister_project">ADHC_LEDGEH TO-001 shipped `48977e269` 2026-05-14 — same `shared-advisor-router-response` L@E that this TO extends. Error-path verbatim preserved; success-path block added.</ref>
    <ref type="anchor">2026-05-14 ~19:4XZ RD 0.4.2 NNA bell-curve 18hr CDN staleness incident (`x-cache: Hit, age=64908s`). This TO + LEDGEH TO-001 close the structural class-eliminator pair for CDN cache coherence on platinum-artifact paths.</ref>
    <ref type="interim_completed">TO-001-INTERIM (AE 0.6.1 lane) SHIPPED 2026-05-26 (INF `b00e2733e` + BD `053bba6f7`); operational unblock. THIS TO supersedes the interim with the structural fix.</ref>
  </references>
  <dependencies>
    <dependency>AE 0.7 worker engagement — UNBLOCKED per Andrew sovereign-direct /mstr-spawn 2026-05-26T~15:11Z (override of AC9-gated hold for this serial).</dependency>
    <dependency>LEDGEH TO-001 already shipped — `48977e269` provides the L@E handler being extended.</dependency>
    <dependency>Coordinate with LEDGEH TO-001 (your other AE 0.7 pending TO) — both pending in your queue; either order is fine but consider running LEDGEH TO-001 first if not yet shipped (per file state, may still be staged-pending despite PRD canonical 5362d0295).</dependency>
  </dependencies>
</metadata>

<scope>
Extend `infra/aws/lambda-edge/shared-advisor-router-response/index.mjs` (currently ~65 LOC; post-extension ~85 LOC) with a success-path block per PRD §3.1 pseudocode.

**Add Cache-Control header `public, max-age=60, must-revalidate`** on HTTP 2xx responses for paths matching `/api/scoped/.../*.json` artifact-class filter (filter already exists in LEDGEH handler — REUSE the existing isArtifact check).

**Error-path behavior preserved VERBATIM:** structured JSON error envelope at HTTP 4xx per LEDGEH §3.2 must not regress. New logic operates ONLY when status is 2xx AND request matches artifact pattern.

**Terraform:** zero new resources. Existing Lambda + CF wiring intact. Refresh `source_code_hash` via `data.aws_s3_object.shared_advisor_router_response` re-read after S3 zip upload.

**lambda-source-map.json:** existing entry covers this Lambda; verify no metadata update needed.
</scope>

<acceptance_criteria>
- AC1: Post-deploy, a refreshed platinum artifact (e.g., `partner_analytics_quarterly.json`) returns CloudFront response with `Cache-Control: public, max-age=60, must-revalidate` header.
- AC2: Synthetic harness OR Andrew UAT: gold-chain emit at T0; portal pull at T0+90s shows `x-cache: Miss/RefreshHit; age<60s`; portal pull at T0+30s shows `x-cache: Hit; age<60s` (cached but freshly-revalidated within window).
- AC3: Error-path empirical reproduction (LEDGEH regression check): wrong-firmId artifact-class request still yields parseable JSON error envelope at HTTP 404 (no LEDGEH regression).
- AC4: `comp-iam service shared-advisor-router-response` post-deploy shows expected ops set unchanged (no IAM permission gaps).
- AC5: `terraform plan` 0-diff post-apply.
- AC6: L@E propagation wait verified (~15-30min post-apply per AE Lambda Deployment Protocol).
- AC7: CF distribution invalidation completed for `/api/scoped/advisor-intelligence/*` post-deploy.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before write):**
- `comp-routes behaviors` — verify CF behaviors #2/#3/#4/#12 still carry `shared-advisor-router-response` as origin-response trigger (confirm LEDGEH ship still active)
- `comp-iam service shared-advisor-router-response` — baseline IAM ops; expect no changes post-edit
- `comp-blast shared-advisor-router-response` — confirm no consumer expects current no-Cache-Control behavior

**Phase 2 (before commit):**
- `python -m py_compile` on the .mjs file's syntactic equivalent OR Node syntax check
- Read existing handler end-to-end; confirm error-path branches untouched by your edit

**Phase 3 (after deploy):**
- `comp-iam gaps` if iam.tf changed (don't expect changes; verify)
- `comp-pipescript deployed` not applicable to L@E; use `aws lambda get-function --function-name shared-advisor-router-response` for deployed-version verification
</compiler_tools_mandate>

<cross_domain_coordination>
- **LEDGEH TO-001 sister-coordination:** same L@E, same lane. If LEDGEH TO-001 file at `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADHC_LEDGEH.001.ae-shared-advisor-router-error-envelope.md` is still pending, consider executing LEDGEH first since CDNCOHT extends LEDGEH's handler. If LEDGEH already shipped (`48977e269` was prior session), CDNCOHT extension layers on top cleanly.
- **TO-001-INTERIM (AE 0.6.1) coordination:** AE 0.6.1 already shipped dispatcher-side CF invalidation for INF + BD chains. Your TO-001 structural fix makes the dispatcher invalidation operationally redundant (Cache-Control max-age=60 means CF naturally revalidates; dispatcher invalidation becomes belt-and-suspenders rather than primary). No coordination required; sibling layers.
- **ADHC_FECACHE_COHERENCE (SHIPPED `120df453`):** Layer 1 FE React Query — orthogonal; no interaction.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for L@E `.mjs` extension + Terraform source_code_hash refresh
- Tag `portal-auth-vX.Y.Z` (per CLAUDE.md Rule 6 post-apply tag discipline)
- `aws cloudfront list-invalidations` output post-deploy showing the new invalidation entry on `/api/scoped/advisor-intelligence/*`
- `curl -I` headers from post-deploy portal pull showing `Cache-Control: public, max-age=60, must-revalidate`
- LEDGEH error-path regression test evidence
- Session log with Compiler Tools section + archetype DEPLOY
</expected_evidence>

<notes>
This is the canonical "real fix" replacing AE 0.6.1's TO-001-INTERIM dispatcher-side invalidation discipline. The interim ships first (operational unblock) + this structural fix supersedes by making CF naturally revalidate at 60s intervals.

**Order recommendation:** consider running LEDGEH TO-001 first if not yet shipped — they target the same handler + LEDGEH establishes the error-path foundation that CDNCOHT TO-001 must preserve. Either way, MCP ws COO if scope ambiguity surfaces.

**TO-VAL (`ADHC_CDNCOHT.VAL.ae-empirical-regression-sweep`)** will be authored just-in-time after TO-001 RAVC2-Request lands. Effort ~30min-1h per PRD §6 — reproduce 18hr-staleness anchor pre-fix + confirm post-fix state.

**Andrew sovereign-direct AE 0.7 spawn 2026-05-26T~15:11Z** lifts AC9-gated hold for this serial (per /allocation #6 ALLOCATION-OVERRIDE-ABSORBED). If Andrew explicitly counters in next ~1 cycle, /allocation re-evaluates.

Architectural questions / PRD scope → ws CTO (1.0.0_SA_CTO). Dispatch / RAVC2 / blockers → me (2.0.0_SA_COO).
</notes>
</task_order>
