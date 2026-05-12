<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>prefetchquery-saturation-root-cause</id>
    <title>Root-cause investigation: localhost-only Distribution radial regression from AuthContext.prefetchQuery upgrade</title>
    <issued_to>0.4.0_DT_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-12</issued_date>
    <status>complete</status>
    <completed_date>2026-05-13</completed_date>
    <closure_disposition>SUPERSEDED-BY-SHARED.006</closure_disposition>
    <closure_note>SUPERSEDED 2026-05-13 ~00:25Z per CTO RAVC4 RATIFY (00:15Z). CTO + DT + RD converged on firmOverride-key-mismatch as the saturation root cause: AuthContext.prefetchQuery resolves firmOverride='bd'/'inf'/null at one moment; component mount resolves it to a different literal; React Query cache keys diverge; dedupe fails; second fetch competes on same HTTP/1.1 connection pool against cold Lambda; saturation. The fix is SHARED.006 firmOverride canonicalization (single L1 literal across all 4 namespace layers), NOT prefetch staggering / Vite proxy / HTTP/2 / staleTime tweaks. Step 6 prefetchQuery upgrade re-introduction gates on SHARED.006 ship + 24h empirical confirmation that saturation pattern doesn't recur. RCA collapses to a one-paragraph confirmation in SHARED.006's RAVC2 evidence ("RQ cache key parity between AuthContext.prefetchAdvisorIntelligence and BooksTab/Distribution useQuery consumers"). Path (a) per CTO 00:15Z framing.</closure_note>
    <priority>LOW — superseded</priority>
    <estimated_effort>SUPERSEDED — no separate investigation needed</estimated_effort>
    <dispatch_held>true</dispatch_held>
    <dispatch_note>Do not dispatch — SUPERSEDED by SHARED.006 firmOverride canonicalization per coordination path (a). SHARED.006 RAVC2 evidence will include the empirical-cache-key-parity check that this TO would have produced.</dispatch_note>
  </metadata>

  <references>
    <ref type="anchor_commit">6f81d13a (DE 0.4 BooksTab N1→useQuery migration that included Step 6 AuthContext.prefetchQuery upgrade)</ref>
    <ref type="hotfix_commit">ff54d611 (DE 0.4 revert of Step 6 only — DEV-only hotfix)</ref>
    <ref type="dt_pushed">c741c0e81 (DT 0.4 parent gitlink for the revert)</ref>
    <ref type="symptom_source">RD 0.4.2 5-flag list item 4 (Andrew visual sweep 2026-05-12 PM); DE 0.4 mid-audit checkpoint 22:55Z</ref>
  </references>

  <context>
    Step 6 of `6f81d13a` upgraded AuthContext to prefetchQuery shared data at login (one batch fetch instead of N component-mount fetches). PROD works correctly. Localhost dev rendered empty Overview radial — the prefetch storm appears to saturate either browser HTTP/1.1 concurrent-request limits or cold Lambda concurrency before the radial's mount-time query lands.

    DE 0.4 hypothesis: HTTP/1.1 6-connection-per-origin browser cap interacting with concurrent prefetch + a cold Lambda may serialize/queue requests differently than prod's warm path. Vite dev proxy may also be amplifying. Browser-specific differences possible (Chrome vs Firefox vs Safari fetch scheduling).

    Step 6 reverted as `ff54d611` to unblock dev. Original migration goal (cold-load latency reduction) still desirable; needs proper RCA before re-attempting.
  </context>

  <objective>
    Diagnose the localhost-only saturation pattern. Determine whether re-ship requires:
    - (a) prefetch staggering / batching policy change
    - (b) Vite dev proxy config change
    - (c) HTTP/2 enablement at dev proxy layer
    - (d) staleTime / Suspense wrapper change at consumer components
    - (e) some other root cause

    Output: written RCA + re-ship strategy. Re-implementation execution is a SEPARATE follow-on TO; this is investigation only.
  </objective>

  <scope>
    <files_read>
      <file>portal/src/contexts/AuthContext.tsx (post-revert state; the prefetch storm pattern from git history of 6f81d13a Step 6)</file>
      <file>portal/vite.config.ts</file>
      <file>portal/src/api/** (query client setup, fetch wrappers)</file>
      <file>portal/.env.development</file>
    </files_read>
    <files_written>
      <file action="create">org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/prefetchquery-saturation-rca.md</file>
    </files_written>
  </scope>

  <requirements>
    <requirement id="1">
      Reproduce the radial regression on localhost via `bun run dev`. Capture:
      - Browser DevTools Network panel timing during the prefetch storm
      - Which specific request "loses the race" to mount-time radial query
      - HTTP version actually negotiated (1.1 vs h2) at dev proxy
      - Concurrent-request count at peak
    </requirement>
    <requirement id="2">
      Test `bun run build && bun run preview` (production-build local server) and compare against `bun run dev` to isolate Vite dev-server vs build-pipeline behavior.
    </requirement>
    <requirement id="3">
      Test in Chrome + Firefox + Safari to identify browser-specific behavior (HTTP/1.1 6-connection-per-origin enforcement varies).
    </requirement>
    <requirement id="4">
      Inspect Lambda cold-start vs warm behavior on the relevant endpoints via CloudWatch logs around the saturation event.
    </requirement>
    <requirement id="5">
      Output `prefetchquery-saturation-rca.md` with:
      - RCA section (concrete root cause, not hypothesis)
      - Re-ship strategy section (specific recommendation: which of (a)-(e) above + concrete diff plan)
      - Estimated effort for re-implementation as a follow-on TO
    </requirement>
  </requirements>

  <cross_domain_coordination>
    <none_required>
      Investigation only — no production deploy. Re-implementation will be a separate follow-on TO that COO authors after RCA lands.
    </none_required>
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="1">`prefetchquery-saturation-rca.md` exists with concrete RCA (not hypothesis) + re-ship strategy.</criterion>
    <criterion id="2">Network-panel timing capture included as inline screenshot/markdown table or as a referenced supplementary file.</criterion>
    <criterion id="3">Browser-specific differences enumerated.</criterion>
    <criterion id="4">Re-ship effort estimate stated. If conclusion is "abandon this migration", justify with effort/benefit math.</criterion>
    <criterion id="5">DE 0.4 + RD 0.4.2 ACK the RCA before COO closes (DE has migration context, RD has visual-regression history).</criterion>
  </acceptance_criteria>

  <ravc_protocol>
    <ravc1>ACK + ETA (rough); confirm bandwidth or flag for later</ravc1>
    <ravc2>RCA committed; cite commit hash + summary findings; DE + RD ACK status</ravc2>
    <ravc4_close>COO accepts RCA + decides whether re-implementation TO is authored or scope abandoned</ravc4_close>
  </ravc_protocol>

  <notes>
    <note>DE 0.4 routing recommendation: DT 0.4 primary (Vite/build/proxy expertise), DE 0.4 backup (migration context), RD 0.4.2 helper for empirical browser repro. Lane assignment per DE 0.4 mid-checkpoint MCP 22:55Z.</note>
    <note>LOW priority — not blocking ADVI_SHARED Phase 1 authoring. Pick up at convenience.</note>
  </notes>
</task_order>
