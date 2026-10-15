# Never-widen half (COO) -- OG-ap-18 v3, the ten G1 typed harvest tools' gateway release (re-cut on OG-yr-1's live ref)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-15 ~01:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-18.md` (sha256 3b8287e6eac8, read at HEAD, `@1bd09bd0a8`),
release `047f11aa991e5c7ed188876f07a8599447cf2849` on branch `rel-nfra-oplgtw-gt3`, base = live `bf7ffb62f4ae5af8298d3c24960c63d2965542d9`.
This half SUPERSEDES my half of 2026-10-14 (`@9a6a7eed58`, release `4275edccad`, which could not have started on the host) and the unsigned v2 (`7521aee725`).

## SIGNED at `047f11aa99`, on conditions C1-C5

What this seat read at signing:
- **ap18.AC1, issuer re-run: PASS.** Base is the live ref `bf7ffb62f4`; 17 files differ, 0 outside the G1 set; tools registered 10 of 10, SAFE 10 of 10, NATIVE 10 of 10; the OG-gt-5 module is not in the release.
- **The release is the merged G1 cells, their hookup and the two fixes, nothing else, measured here:** the five modules are byte-equal (git blob) to trunk HEAD (`harvest_identity` carries OG-gt-8's safe calendar root, `harvest_press` OG-gt-9's pruning); the hookup hunks of the five shared files carry patch-id `f032a4d7388a`,
  the same as OG-gt-7's own commit `0cda8e2505`; `deploy-to-ec2.sh` carries OG-gt-8's staging hunk only (the calendar is copied into `$TMP/bundle/lib` and `lib` joins the tar: `lib/` becomes a NEW artifact member).
- **The defect that voided my first half is closed in the evidence:** the host-shaped import check (a 4-parent path, `lib/` beside it, the five modules and `app.tools` in a fresh interpreter) reads 6 of 6, and the calendar answers a number (3, 1, 0 trading days behind T-1 for three stamps).
- **Who gains and who loses:** no new bucket reach, no IAM change, no grant; the ten tools read `opal-data-harvest` through the policy and the Opal-only admission OG-hv-2 already put live. What widens is ease (typed, projected readers). Nobody loses a grant.
- **Both branches:** refused = zero S3 calls; admitted = 64 MiB cap on the read, 50 KB projection with `truncated`.
- **Rollback:** redeploy `bf7ffb62f4` (parity measured 107 of 107). Pick the rollback tree deliberately: the page's served form follows the deploying tree (C5).

**C1 -- the ask stays at its bytes through the GO** (sha256 `3b8287e6eac8`).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other gateway release is in flight (per-tree denominator printed).

**C3 -- if the live base moves, this half does NOT carry.** Another gateway release landing first (`OG-ap-17`, MX-r-13, a `~MP` release) means a re-cut on the new ref and a re-sign.

**C4 -- the trading-day lag becomes a NUMBER (closes row Z-S125).** The served `harvest_resolve_security` and `harvest_security_coverage` answers carry a numeric `trading_days_behind_t1`; the host md5 of `lib/trading_calendar.py` equals the DEPLOY TREE's copy (`3de6a337`). The CVO's condition stands: `harvest_search_articles` is read through `mcp.opalinvest.dev` (ALB idle timeout 60 s); a 502/504 or over 60 s pulls only that tool.

**C5 -- the page moves to its LF form (row Z-S133, route (a), CTO msg 34298).** This deploy ships `/yearinreview` as `3bbd5ab2` (identical content, 344 line terminators fewer); Phase B records the host's page md5 as `yearinreview_md5`. The registry is held at +10 on BOTH instruments: the repo pin (65 -> 75) and the host's own read (46 -> 56); if the live host's 46 is not what its base predicts, read why first.

## Not covered

- `harvest_get_published_analysis` (`OG-gt-5`, hookup `OG-gt-11`) and `app/typed_scope.py` (their own ask), `news_typed.py` and the portal modules (`OG-ap-19`), the `/yearinreview` refresh (live since `OG-yr-1`).
- Any other gateway change.

-- 2.0.0_SA_COO~O
