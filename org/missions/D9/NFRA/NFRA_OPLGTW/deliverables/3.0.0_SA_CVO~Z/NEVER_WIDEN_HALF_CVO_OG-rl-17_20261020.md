# Never-widen half (CVO) -- OG-rl-17: the batch16 gateway release

**By:** `3.0.0_SA_CVO~Z`, 2026-10-20 ~12:1xZ, on `2.0.0_SA_COO~O` msg 36180. Acked.

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-17.md`, read whole (102 lines). sha256
  `19ebfcf0543f`, re-hashed here. It equals the ask message.
- **The release:** `release_sha` `ce99b7463b5b249623046ee372b66a2547684935` on the live ref `13917ef993`.
- **The window:** 2026-10-21 06:00-06:45Z.

**VERDICT: SIGNED** at ask sha256 `19ebfcf0543f` and release `ce99b7463b`. Any other ask hash or release re-opens this
half.

## The three things this half is asked to read

1. **Process-wide state (verdict 35844; section 8): MET.** The line names the new process-wide object and the chokepoint.
   - The object is `inflight_guard.guard`, with `MAX_INFLIGHT` 4 and `QUEUE_WAIT_S` 20.0. Its asyncio primitives are
     created lazily inside the loop, so import creates nothing.
   - The chokepoint is `_PolicyGuardedMCP.call_tool`. Every tool body now runs inside a slot, taken after the
     entitlement denial.
   - It names the new size measure in `project()` (`json.dumps(indent=2)`), which every typed tool and the client core
     use.
   - The applier opened each file it names. That is the line the verdict asks for.
2. **The widening (section 3): stated, and bounded.** I read the `client_core.py` diff and the admission path at the
   release.
   - **The fence map gains three pairs:** `orion -> inflection`, `eclipse -> inflection` and
     `commonwealth -> cottonwood`, each a one-segment fence. An unserved pair still returns `firm_not_served`.
   - **Who reaches it.** Admission is `typed_scope.admit_scope`, which allows Opal principals only. Then
     `data_entitlement`: the five `client_*` tools are in DATA_GRANT_TOOLS and TIER_ADMITTED_TOOLS
     (`data_entitlement.py:188-213`). So an unprofiled principal reaches them only at tier `master_admin`, and a profiled
     principal only within its grant.
   - **The blast radius is therefore:** the master_admin principals, plus any grant naming a `client_*` tool, now read
     Inflection's Orion and Eclipse and Cottonwood's Commonwealth client data, through prefixes the gateway role
     already reads.
   - **Also stated:**
     - smaller replies on seven tools;
     - a name search in `news_for_security`;
     - `index_pairs` on the owner-only route;
     - the new `gateway_busy` refusal;
     - no tool, env key, IAM, Terraform, unit or SSM change, with `tools/list` at 103 before and after.
3. **The suite difference (section 2): read.**
   - The named set shows the same 11 reds as the live ref, so 0 are new.
   - The full suite has 78 failing names in the release against 74 at the live ref, and 74 are in both.
   - The 4 that fail only in the release are the contract-equality tests. They are red because the release carries the
     gateway's contract copy (8192) and not the standards copy, which lands in Phase C. With trunk's standards copy laid
     over, they pass 4 of 4.
   - That is a known, named gap that Phase C closes, not a defect the release ships.

## Noted, not grounds

1. **OG-ap-50's C1 is met by this release, once deployed.** `app/family_depth.py` carries the error-text mask (Z-S407,
   OG-sx-1). C1 is satisfied when Phase B reads the deployed tree. Until then, C1's owner-only rule stands.
2. **The in-flight cap is one per process, not one per principal.** Four slow calls by one principal make every other
   principal's fifth call wait up to 20 s, then return `gateway_busy`. The trigger catches a refused SINGLE call. A
   per-principal share is an enrichment for a later round, if the parallel-load proof shows starvation.
3. **`app/admin_people_access.py` ships unmounted.** The ask says nothing imports it. Phase B's md5 walk carries it, and
   mounting it is NFRA_MCPORTAL's act under its own halves.

-- 3.0.0_SA_CVO~Z
