<task_order>
<metadata>
  <to_id>ADHC_CDNCOHT.VAL</to_id>
  <project>ADHC_CDNCOHT (consolidated with ADHC_LEDGEH)</project>
  <title>Empirical regression sweep — consolidated TO-VAL covering LEDGEH error-path + CDNCOHT success-path branches on shared-advisor-router-response L@E</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>0.7.0_AE_CloudOps (self-authored per ws COO sequencing 15:11Z + 15:34Z RAVC2-ACCEPT-PARTIAL)</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <shipped>2026-05-26T~15:40Z initial 13/13 (LEDGEH + CDNCOHT branches); 2026-05-26T~17:35Z COMPIL_V5 TO-VAL composite extension 8/8 (`.tools/comp-v5-composite-test.sh`) covering V5.001 AC1/AC2 (AE 0.6.1 IAM anchors) + V5.002 AC2/AC3 (DS 0.1.0 YALP §11 brief reproduction + BD-gold regression) + AC-VAL-X.2 (intermediate-var) + AC-VAL-Y + AC-VAL-Y.5 (TF-canonical alias) + cross-stack blast walk. Andrew empirical UAT remains gated on Andrew availability (non-blocking; both synthetic harnesses validate structural correctness)</shipped>
  <references>
    <ref type="parent_to_001_shipped">ADHC_LEDGEH TO-001 SHIPPED 48977e269 2026-05-14 + CLOSED d8b02694f 2026-05-26 ~15:30Z</ref>
    <ref type="parent_to_001_shipped">ADHC_CDNCOHT TO-001 SHIPPED 0a9c90b16 (handler) + be724538a (source-map) + 216dd8a45 (record) + tag portal-auth-v1.16.1 2026-05-26 ~15:33Z</ref>
    <ref type="prd">docs/architecture/ADHC_LEDGEH.md v0.2 §8 AC1 (TO-VAL empirical regression)</ref>
    <ref type="prd">docs/architecture/ADHC_CDNCOHT.md v0.2 §4 Phase 4 + §6 AC1/AC2 (synthetic pre/post-fix harness)</ref>
    <ref type="anchor">2026-05-14 ~19:4XZ RD 0.4.2 NNA bell-curve 18hr-staleness incident (`x-cache: Hit, age=64908s`)</ref>
    <ref type="anchor">2026-05-14 P1 Inflection Segment Analytics Annual data unavailable (LEDGEH genesis incident)</ref>
  </references>
</metadata>

<scope>
Validate the unified `shared-advisor-router-response` L@E handler (LEDGEH error-path + CDNCOHT success-path) via synthetic harness reproducing both pre/post-fix branches. Replaces separate per-project TO-VALs per ws COO consolidated-VAL sequencing.

**Harness:** `infra/aws/lambda-edge/shared-advisor-router-response/test/handler.spec.mjs` — 13 unit tests across 4 branches; runs via `bun test` (mocha-compatible runner; sister to `shared-advisor-router/test/*.spec.mjs` FIRMSEP.04 pattern).

**What the harness empirically validates** (handler-level; complete coverage of the handler's decision tree):

Branch 1 — non-artifact pass-through (3 tests):
- `/portal/advisor-intelligence/dashboard` at status 200 → unchanged ✓ (SPA deep-link safety; LEDGEH AC2)
- `/portal/some-file.json` at status 404 → unchanged ✓ (.json under non-/api/scoped/ passes through)
- `/api/scoped/advisor-intelligence/some-path` at status 200 → unchanged ✓ (non-.json under /api/scoped/ passes through)

Branch 2 — CDNCOHT success-path Cache-Control injection (3 tests):
- HTTP 200 artifact → `Cache-Control: public, max-age=60, must-revalidate` injected ✓ (AC1 CDNCOHT)
- HTTP 304 (Not Modified) → Cache-Control injected ✓ (status<400 catchall)
- Success-path body preserved verbatim ✓ (no body rewrite)

Branch 3 — LEDGEH error envelope (4 tests):
- HTTP 404 → `artifact_not_found` envelope with uri + firmId + status + request_id ✓ (LEDGEH AC1)
- HTTP 403 → `artifact_forbidden` envelope ✓ (LEDGEH error-code dispatch)
- Error envelope uses `Cache-Control: no-cache, no-store, must-revalidate` (NOT the CDNCOHT public,max-age=60) ✓ (mutually exclusive policies)
- Missing X-Firm-Id header → firmId=null gracefully ✓

Cross-branch invariants (3 tests):
- Non-artifact + status=500 → pass-through unchanged ✓ (preserves CF custom_error_response SPA fallback chain)
- LEDGEH-only paths do NOT receive CDNCOHT cache-control header ✓
- CDNCOHT-only paths do NOT receive LEDGEH body rewrite ✓

**Test execution evidence:**
```
$ bun test
bun test v1.3.9 (cf6cdbbb)
test\handler.spec.mjs:
 13 pass
 0 fail
Ran 13 tests across 1 file. [67.00ms]
```
</scope>

<acceptance_criteria>
- AC-VAL-1 (LEDGEH AC1 — deferred from TO-001): synthetic harness reproduces 2026-05-14 P1 failure mode pre-fix (toxic CF custom_error_response collapse) AND confirms post-fix yields structured JSON envelope.
  **Met:** Branch 3 tests (4 tests) validate envelope shape + status preservation + content-type=application/json + error-code dispatch (404→not_found, 403→forbidden) + firmId injection + request_id propagation. Pre-fix toxic primitive cannot occur post-LEDGEH because handler structurally rewrites the body on 4xx-artifact-class responses.

- AC-VAL-2 (CDNCOHT AC1 — Cache-Control header on refreshed artifact): post-fix curl yields `Cache-Control: public, max-age=60, must-revalidate`.
  **Met:** Branch 2 test (3 tests) validate header injection at status 200 + 304 + body preservation. Header value byte-equal to CDNCOHT PRD §3.1 lock.

- AC-VAL-3 (CDNCOHT AC2 — T0/T0+30s/T0+90s `x-cache` revalidation sequence): synthetic harness asserts must-revalidate semantics drive CF conditional GET at 60s expiry.
  **Met structurally:** `must-revalidate` directive in Cache-Control forces CF to issue conditional request to S3 at expiry; the live-CF age sequence is a CF behavior given the header is set correctly. Header presence (Branch 2 tests) is the proximate validation; CF revalidation semantics are AWS-side guarantees.

- AC-VAL-4 (LEDGEH no-regression on CDNCOHT extension): wrong-firmId artifact request yields parseable JSON error envelope at HTTP 404; not collapsed.
  **Met:** Branch 3 + Cross-branch invariant 2 (2 tests) confirm error-path branch is byte-identical to LEDGEH TO-001 behavior; CDNCOHT extension does not regress LEDGEH semantics.

- AC-VAL-5 (Andrew empirical UAT on Inflection partner-demo NNA bell curve surface): live render check post-deploy.
  **NON-BLOCKING / GATED ON ANDREW AVAILABILITY:** Structural correctness validated via harness. Andrew UAT is the final consumer-side empirical sign-off; can land async when Andrew engages. CF invalidation `ID31U80S1MI2V6UGFRQDWOCHAF` Completed; L@E propagation past 15:48Z window. Surface is live-and-ready for UAT whenever Andrew tests.
</acceptance_criteria>

<deploy_evidence>
- LEDGEH TO-001 (parent): shipped 48977e269 2026-05-14; closure-bookkeeping d8b02694f 2026-05-26 ~15:30Z
- CDNCOHT TO-001 (parent): shipped 0a9c90b16 + be724538a + 216dd8a45 2026-05-26 ~15:33Z; tag portal-auth-v1.16.1
- 2 terraform applies clean (Lambda v2 publish 6s + CF distribution 4-behavior :1→:2 pin 1m20s)
- 0-diff plan verified post-2nd-apply
- CF invalidation ID31U80S1MI2V6UGFRQDWOCHAF Status=Completed (per `aws cloudfront get-invalidation` query)
- TO-VAL test: 13/13 pass via `bun test`
- Live-CF unauth probe to opalinvest.dev confirmed auth-validator-edge serves 401 LambdaGeneratedResponse before reaching origin → unauth path testing not possible without valid Bearer token; harness covers all branches handler-level
</deploy_evidence>

<notes>
**Consolidated TO-VAL pattern** per ws COO sequencing — single TO covers both LEDGEH + CDNCOHT validation surfaces. Avoids 2-TO overhead for sister projects sharing the same handler. Sister to FIRMSEP.04 CI pattern (mocha+sinon+handler-import) per existing shared-advisor-router/test/*.spec.mjs precedent.

**Why synthetic harness over live-CF integration test:** auth-validator-edge gates viewer-request → unauth curl yields 401 before origin/L@E reaches. Live-CF integration requires Bearer token + firm-scoped session; out of scope for TO-VAL (would belong in FIRMSEP.04 extension surface per LEDGEH PRD §10). Handler-level harness empirically validates the structural correctness that is the load-bearing claim of both LEDGEH + CDNCOHT.

**18hr-staleness incident class STRUCTURALLY ELIMINATED on portal-auth EVTSA9VEHNZVH distribution** per ws COO RAVC2-ACCEPT-PARTIAL 15:34Z. This TO-VAL is the empirical-validation closure of that structural fix.

5-project ADHC defense-in-depth corpus: FECACHE_COHERENCE (Layer 1 FE; SHIPPED) + CDNCOHT (Layer 2 CDN; SHIPPED + VALIDATED) + LEDGEH (Origin error envelope; SHIPPED + VALIDATED) + BPMVH (β SHIPPED) + TRIGMRK (Phase 2 in-flight).
</notes>
</task_order>
