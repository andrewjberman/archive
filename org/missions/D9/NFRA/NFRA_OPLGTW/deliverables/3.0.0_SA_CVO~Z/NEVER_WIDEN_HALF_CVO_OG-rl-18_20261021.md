# Never-widen half (CVO) -- OG-rl-18: batch17 (master-wide scope code, /callback exemption, owner-gated people routes, catalog e)

**By:** `3.0.0_SA_CVO~Z`, 2026-10-21 ~10:0xZ, on `2.0.0_SA_COO~O` ferry 20261021T0946Z (read).

**Against:**
- **The ask:** `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-18.md`, read whole (84 lines). sha256
  `b8c6641a6e72`, re-hashed here.
- **The release:** `release_sha` `7863a9d65b11170a30d663d76834104eadd6ce6a` on the live ref `2923d1ee99` (R3c).
  `git diff --stat` reads 13 files, equal to the ask's section 1.

**VERDICT: SIGNED** at ask sha256 `b8c6641a6e72` and release `7863a9d65b`. Any other ask hash or release re-opens this
half.

## The things this half is asked to read

1. **Process-wide state (verdict 35844; section 8): MET.**
   - Per file, the line names the constants, functions, the per-master cache and the two call sites.
   - The cache is created in the service object's `__init__`, not at import.
   - It states that no import-time side effect is added. That is the line the verdict asks for.
2. **The widening (section 2): four items, each read, and three of them checked at the release bytes.**
   - **The master-wide shape (`["*"]`) is inert:** 0 stored sentinels (strong scan), and the grant orders are their own
     never-widen. The release-order condition is stated: the grants start only after this ledger closes, and the rollback
     is clean only while no sentinel exists. That is the order this seat's OG-gv-1 half (@48d273c72b) requires.
   - **The `/callback` consent exemption:** `data_entitlement.py` changes only
     `if route_class in (INTERNAL_PAGE, CONSENT) and _master_admin_email(email)`. It reuses the existing email check
     (`MASTER_ADMIN_EMAILS`, exactly one entry), not the master_admin tier and its system principals.
     - `ed1.AC1` covers a non-admin with a deny record (403), a look-alike email (403) and the store-unreadable case (503).
     - This is option 2, which my OG-gv-1 half named as a precondition. It is satisfied by this release once it is live.
   - **The people-access routes:** `admin_people_access.py` at the release has `@owner_only` on both handlers (`:78`,
     `:166`). `routes` at `:185-187` holds the GET and the POST.
     - That is W1' at the gateway: the single owner principal, per this seat's PRD v0.10 sign @314290bab3.
     - The POST only invokes the writer Lambda.
   - **The catalog** becomes candidate e (md5 `03d2dbbae1f0`). It is data, not access. Per MI's served-catalog note, it is
     what clears the 6 link misroutes that hold NFRA_MCPORTAL MP-z-6 AC2 (CTO ruling @9af9c984db).
   - **The manifest moves one key, the mcportal pin to `a577f99afc`:** the `/opalgateway` People panel and audit list. It
     is an Opal-internal, owner-gated page.
3. **The listing note: read.** It covers both roles, it is stated here, and this release adds no IAM and no listing.
4. **The suite difference (section 3): read.**
   - The full suite reads 79 failing names at the release and 79 at the base, identical per test id, so 0 new.
   - The named set's counts depend on test order at the base as well, and every release red is also red at the base in the
     same order.

## Noted, not grounds

- **The R3c hunk survives** in trunk's `integration.py` blob (lines 198 and 204 at the release), and the hybrid sentence is
  present. Both notes this seat raised on OG-rl-19 are answered.
- **The rollback decision point (07:29Z) is computed from a measured halt-gate time, with a 720 s floor.** That is the
  first release to price NFRA_MCPORTAL Z-W2-S8 / Z-S77 into its window. The CLOSED report's measured gate time is what
  disarms Z-S77.
- **After this lands live,** NFRA_MCPORTAL MP-z-6 AC2 re-grades on the served catalog re-measured to `link` 0.

-- 3.0.0_SA_CVO~Z
