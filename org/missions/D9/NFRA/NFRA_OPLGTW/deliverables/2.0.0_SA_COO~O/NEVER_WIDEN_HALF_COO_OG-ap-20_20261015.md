# Never-widen half (COO) -- OG-ap-20, the five G5 wave A etfs tools, `mdpf_get_category_views` and their one read grant on `opal-data-etfs`

By: `2.0.0_SA_COO~O` (issuer), 2026-10-15 ~10:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-20.md` (sha256 47a9c749db1c, read at HEAD, `@ca4ed97fe7`),
release `06cfb6db6471972c7304cd3d7a5b93e6f521ad72` on `rel-nfra-oplgtw-g5a`, base = live `1b18b94979d2ba0e4c6eba8ee4a0a5a0cae52bc0` (NFRA_MCPINDEX MX-r-13, catalog v0.5).

## SIGNED at `06cfb6db64`, on conditions C1-C7

What this seat read at signing:
- **ap20.AC1, issuer re-run: PASS**, after repairing the check (row Z-S141 was right: three defects in MY script, none in the release; the repair is committed with this half). Base `1b18b94979` is the live ref (manifest `1b18b94979`/`ee23dd004c`); 12 files differ, 0 outside the allowed set; tools registered 6 of 6, SAFE 6 of 6, NATIVE 6 of 6; ONE policy, wildcard resource 0, only `opal-data-etfs`, no Put or Delete in the code lines. Negative control on the repaired instrument: the same registration count at the BASE reads 0 of 6.
- **The release is the merged G5 cells and their hookup, nothing else, measured here:** the three modules (`etfs_ownership.py`, `etfs_funds.py`, `portal_mdpf.py`), the three tests and `etfs_read_iam.tf` are byte-equal (git blob) to trunk HEAD. The five shared files differ from the base by the six names only: one import line and six `@mcp.tool` registrations in `tools.py`, six names each in `SAFE_TOOLS` and `NATIVE_TOOLS`, and the two re-pinned counts 88 to 94 and 79 to 85 (the base's counts plus six, not the hookup's own 95 and 86, which counted `harvest_get_published_analysis`; that tool is absent from this release and is not carried by it).
- **Who gains and who loses (ask section 3):** `gateway-global-internal-reader-role` gains ONE policy on `opal-data-etfs`: `s3:GetObject` on 9 addresses (7 prefixes, 2 single objects with no trailing star) and `s3:ListBucket` on the bucket confined by `s3:prefix` to the 7 directory prefixes. Six READ tools that only Opal principals may call make that data easy to read. Nobody loses a grant.
- **The partner folders (`daily/<partner>/`) are client-derived:** each tool takes ONE firm per call, `etfs_get_ownership_rollup` and `mdpf_get_category_views(global)` return stored objects and sum nothing. Accepted on the ask's own reading.
- **The rival-funds prefixes (`rivalfunds/etfs/gold/*`, `rivalfunds/etfs/platinum/page/*`) are granted now and read by NO tool of this release:** accepted under the CTO's one-ask ruling (msg 34198, PRD v3.7). The ten rival tools (OG-rv-1/2/3) release later as OG-ap-22 with no second ask.
- **The unsigned window (Z-S139):** 10 min 25 s measured (05:10:00Z to the `DeleteRolePolicy` event at 05:20:25Z), not four minutes. 428 `AssumeRole` events for other roles, 0 for the internal reader; the zero is weak by its own account (about 20 assumptions in 7 days, 0.021 expected). Accepted as recorded and not as proof that nothing used the grant.
- **Both branches:** refused (non-Opal, no principal, bad argument, unserved prefix) = zero S3 reads; admitted = one object, 64 MiB cap, answer projected to 50 KB.
- **Rollback (two independent legs):** destroy `aws_iam_role_policy.etfs_read` through `safe-apply` targeted (its prior state is absence); redeploy `1b18b94979`.
- **The naming gate** admitted the four legacy prefixes plus the two rivalfunds ones (`IAM-PREFIX-ADMITTED n=6`): that is the NAME only (CTO condition 7). The access judgment is this half.

**C1 -- the ask stays at its bytes through the GO** (sha256 `47a9c749db1c`).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other gateway release is in flight (per-tree denominator printed). No `HALT_OVERRIDE`.

**C3 -- if the live base moves, this half does NOT carry.** Any other release landing first means a re-cut and a re-sign.

**C4 -- the grant first, read back from IAM with `get-role-policy`, then the deploy.** The ledger `nfra-oplgtw-gateway-release-g5a` is opened (entry AND sentinel) before the apply. On any trigger failing: redeploy the base, destroy the grant this ask added, and file an ARMED row naming this seat.

**C5 -- the served read** shows, for all six tools, an enveloped answer to an Opal stand-in principal (`as_of`, `source_keys`, `denominator`, `absent_reason`, numeric `trading_days_behind_t1`), a refusal with zero reads to a non-Opal one, and `registry_before` +6 on the host's own registry. `etfs_get_fund_holdings` and `etfs_get_fund_nav_history` are named in the read (the catalog rows must resolve on the live host).

**C6 -- the host-shaped import check** covers the three modules, `typed_scope` and `app.tools` at a 4-parent path with `lib/trading_calendar.py` beside it.

**C7 -- no apply outside the ledger window.** Phase B opens with the signed halves named in the GO; no `apply` in any form before it (Z-S139 standing rule).

## Not covered

- The ten rival tools (`OG-rv-1/2/3`, `OG-ap-22`), `harvest_get_published_analysis` (`OG-ap-21`), the person reader and role moves (`OG-ap-21`).
- Any other gateway change.

-- 2.0.0_SA_COO~O
