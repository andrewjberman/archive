<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-08-03-monpub-w6</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.2.0_DT_PortfolioAnalytics (portal lane)</issued_to>
    <date>2026-08-03</date>
    <status>complete</status>
    <project_code>MDLP_MONPUB</project_code>
  </metadata>

  <objective>
    Make a DataRefresh rollback visible to open portal sessions: the portal QueryClient runs
    staleTime Infinity + gcTime Infinity + 12h localStorage persistence (evicted only at logout),
    and the DataRefresh UI fires ZERO invalidateQueries after a rollback succeeds -- so an open
    session NEVER sees restored data, and a page reload rehydrates the OLD data from localStorage.
    This client layer -- not the CloudFront edge (5min TTLs via cache-control-injector) -- is what
    Andrew watched fail on 07-31. Fix: queryClient.invalidateQueries on rollback success in the
    DataRefresh page, scoped to the data query keys the rollback affects.
  </objective>

  <context>
    Source: CVO Andrew-direct audit @30a13b89b1 (task 2, CloudFront cache census included).
    Census facts to carry: 7 invalidation creators estate-wide; /json-tiered/* (no /api prefix) is
    NOT covered by the rollback's /api/general/* invalidation path -- if the affected queries read
    /json-tiered/*, the client invalidation is the ONLY working layer, state that in the commit.
    Portal work: main worktree stays on DEV (Rule 19); comp-cache collisions at Phase 1 per the
    FE-state auto-rule; frontend-dev screenshot verification if any visual surface changes (none
    expected -- this is behavior only).
  </context>

  <compiler_tools_mandate>
    Phase 1:
      <run>comp-cache collisions</run>
      <expect>enumerate the query keys the DataRefresh rollback affects; no collisions introduced</expect>
      <if_mismatch>a shared key invalidation would refetch unrelated surfaces -- scope the key list, flag to CTO if ambiguous</if_mismatch>
    Phase 3 (exercise, the criterion that can fail):
      <run>in a live session: load Model Portfolios (cache warm), execute a rollback from DataRefresh, return WITHOUT logout/reload</run>
      <expect>the surface shows the restored vintage (query refetched); ALSO verify a reload does not resurrect old localStorage data</expect>
      <if_mismatch>invalidation key list is wrong or the persistence layer rehydrates -- widen keys or add persister purge, re-exercise</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>  <!-- portal-only; no other active TO touches the DataRefresh page or QueryClient config -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. EXERCISED both ways: (a) pre-fix, an open session does NOT show restored data after a
       rollback (reproduce the defect once, on record); (b) post-fix, the same flow shows restored
       data WITHOUT logout, and a page reload also shows it (persistence layer covered).
    2. SCOPE: the invalidated key list is enumerated in the commit; no blanket
       queryClient.clear() unless justified in writing (a full clear is the easiest-pass shortcut
       -- it also nukes every unrelated surface's cache; named forbidden unless argued).
    3. Portal discipline: DEV branch, typescript clean, comp-surface-check on the portal side
       (this touches the must-always-be-right Model Portfolios read path).
  </acceptance_criteria>

<completion date="2026-08-03" by="2.0.0_SA_COO">
W6 COMPLETE: DEV e77e8b6f (13/13 mechanical battery, SURFACE_ACK audited), typecheck gate caught+fixed a real TS error pre-merge (DEV 5ef651b2). PROD promote LANDED: c6f561b6, tag portal-v2.1.155 PEEL-VERIFIED, CI run 30837075543 success (gh run view --json), pointer committed, main tree back on DEV. PROD no longer mislabels version-based rollbacks; rollback success invalidates the 29-prefix client cache. Gate-3 dual-TTL authenticated header capture done on this deployed page (Age 81/82 <300; Age 20 <60). Live-occasion full exercise stays PENDING-LIVE-OCCASION, non-blocking per spec 5c. Closed on Andrew-direct closeout ruling 2026-08-03 ~1750Z (visual smoke passes).
Project closed Andrew-direct (COO terminal, 2026-08-03 ~1750Z): "WE can closeout this project, everything looks good for data refresh and the associated paths/lambdas/etc, visual smoke passes."
</completion>
</task_order>
