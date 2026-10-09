# Never-widen half (COO) -- OG-tm-1, add the Tax SMA master 08403355 to the daily pull, its silver conversion and the gateway's reader roles

By: `2.0.0_SA_COO~O` (issuer), 2026-10-09 ~01:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~39/NEVER_WIDEN_ASK_OG-tm-1.md` as drained
@b4375f2379 (Phase A @4afbece996).

Shape ruling: `1.0.0_SA_CTO~O` msg 32147, 2026-10-09 00:08Z. 08403355 without `slm` is "the same shape", on two
conditions. The ask's section 2 answers both from the code; the CTO half ratifies them.

## 1. SIGNED: the per-resource blast radius of section 3, applied by `-target` only (section 0 item 2)

The act may touch exactly these:
- `schwab/08403355/` prefixes;
- the new EventBridge rule and target `canonical-schwab-si2-08403355-daily-pull`, at `cron(45 10,22 * * ? *)`, which is
  30 minutes after 08242234 and 60 after 08335338;
- the SI2 box role's grants for `schwab/08403355/{bronze,_ops,meta/pulls}/*`;
- the silver scope list and the event rule row `schwab-08403355`;
- the two gateway Schwab roles' new-master prefixes;
- the puller code object, ETag `0017f9b549ca9f8013704f50c4327bed` becoming MD5 `e49aea76a8c634c9d49e6a7cccc51bdf`, a
  one-line diff;
- the converter artifact, sha256 `v2BztqbuhHD3gH95eMqCQzkjPEotvSoeIezEOfsxu90=` becoming the value rebuilt after item 1
  below. 2 of 12 members change.

Two plan drifts are OUTSIDE this half and must not ride the apply: `cot_rebalancer_runner_daily` in opal-assets and
`mcportal_grant_writer` in opal-gateway (row S5). The applier applies the section 1 `-target` lists and nothing else.

**Rollback per resource:** as the ask's section 4. The two existing masters' rules, grants, prefixes and data are
unchanged.

## 2. Section 0 decisions

1. **S4, the source mirror: REQUIRED BEFORE LEG C.** Amendment A2 adds `data/assets/scripts/silver/` (the four files of
   `data_assets_mirror.patch`) to the order's paths. The worker applies the patch to the source, runs that package's
   tests, and repins `silver.tf`'s `silver_build_commit.schwab` to the commit where source and package are equal. Leg C
   ships the artifact rebuilt from that pin. Its sha256 replaces the build-only value above in the apply order, and the
   applier re-reads it.
2. `-target` lists only (see section 1).
3. **The label:** the CTO's half ratifies `"Tax SMA basis"`.
4. **The first pull lands the 30-day window,** keeping the siblings' shape (Andrew: "via running it exactly same
   structure"). It brings 226 objects and 226 converter events at reserved concurrency 2. Accepted.
5. **The IAM replacement window: the planned replace, NOT option B.**
   - Option B would add a `lifecycle` departure to a shared resource.
   - The window is seconds long. The applier runs legs 6-8 outside [09:15,11:35)Z and [21:15,23:35)Z and away from the
     12:15Z sweep, when no bronze is landing.
   - A conversion that fails inside the window is re-converted by the daily 12:15Z sweep (sweep mode converts misses).

## 3. SIGNED: the order of legs and their timing (section 5)

- **Leg C first:** the converter artifact and opal-assets targets 4-9. Not before S4 is closed.
- **Leg B next:** the box grant, then the puller code object, outside the pull windows.
- **Leg A last:** the rule and target. The rule must not exist before legs C and B are in place.
- **The gateway roles:** independent of the pull legs. The contract hookup (master, four data prefixes, completion prefix)
  rides the next gateway release, r29 if its cut has not passed, else r30. Until that release, the roles grant nothing
  the gateway reads.
- **The QA pull:** 13:00-20:30Z, through the rule's own input.

## 4. Who acts

- The applies and the uploads (legs A, B, C and the roles): `0.7.0_AE_CloudOps~Z` (Andrew-direct ~22:0xZ, msg 32057),
  under one NEVER-2 ledger entry, `nfra-oplgtw-og-tm-1-taxsma-master`.
- The read-backs and the QA pull: the worker, by continuation.
- The puller's owning lane `0.6.2_AE_PartnerETL` is named here and told at the apply.

-- 2.0.0_SA_COO~O
