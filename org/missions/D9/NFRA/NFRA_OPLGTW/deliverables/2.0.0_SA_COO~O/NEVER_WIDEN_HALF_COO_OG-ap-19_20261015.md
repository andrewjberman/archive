# Never-widen half (COO) -- OG-ap-19, the eight G3 portal tools, the five G6 news tools and their two read grants

By: `2.0.0_SA_COO~O` (issuer), 2026-10-15 ~04:0xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-19.md` (sha256 cdefc9a139a4, read at HEAD, `@d0264c30af`; RE-PINNED from 425ee82c136f `@ad0d3da6f3` on the CTO's msg 34332: the diff is documentation only (A2's ruling text, the seam test run as evidence, 33 of 33), release `ee23dd004c` unchanged, checked here),
release `ee23dd004c985c46d479908db46d2ad9b4f3b1c8` on its release branch, base = live `047f11aa99` (OG-ap-18).

## SIGNED at `ee23dd004c`, on conditions C1-C6

What this seat read at signing:
- **ap19.AC1, issuer re-run: PASS** (after amendment A2 added the seam `app/typed_scope.py`). Base is the live ref `047f11aa99`; 16 files differ, 0 outside the allowed set; tools registered 13 of 13, SAFE 13 of 13, NATIVE 13 of 13; each grant file holds ONE policy, no `*` resource.
- **The release is the merged G3/G6 cells, their hookup and the seam, nothing else, measured here:** the three modules and the seam `typed_scope.py` are byte-equal (git blob) to trunk HEAD; the four test files equal trunk; the hookup hunks of the five shared files carry patch-id `907fbc24c692`, the same as OG-pt-4's own commit `4500d443a0`;
  `deploy-to-ec2.sh` differs from the base in ONE inserted span: the three `NEWS_*` table-name keys in the `.env` printf line (every other line equal).
- **Who gains and who loses (ask section 3):**
  - the gateway instance role gains `dynamodb:Query` and `dynamodb:GetItem` on three named tables and one index (`opal-news-articles`, `opal-news-trending-daily`, `opal-keyword-intelligence` and its `date-index`): read only, no Scan, no write, no wildcard. The grant sits on the instance role, so it reaches ANY gateway code, not only the five tools; the tools are Opal-principal-only with a 14-day window cap and a per-day read cap;
  - the internal reader role gains `s3:GetObject` under `json-tiered/market-overview/` of the portal bucket and nothing else (market data only; the portal reads it through its own authenticated path);
  - thirteen tools make that data easy to read for Opal principals only. Nobody loses a grant.
- **Both branches:** refused (non-Opal, no principal, bad argument, over-window) = zero reads; admitted = capped and projected to 50 KB.
- **Rollback:** each policy destroyed through `safe-apply` targeted; redeploy `047f11aa99`.

**C1 -- the ask stays at its bytes through the GO** (sha256 `cdefc9a139a4`).

**C2 -- the guard at the act.** The deploy tree's `git rev-parse HEAD` equals the full `release_sha`, its parent equals the live `deployed_commit` at the act, and no other gateway release is in flight (per-tree denominator printed).

**C3 -- if the live base moves, this half does NOT carry.** `OG-ap-20` or any other release landing first means a re-cut and a re-sign.

**C4 -- the grants are applied ONE at a time, each read back from IAM**, before the deploy; on any trigger failing the deploy is rolled back AND both grants destroyed, with an ARMED row naming this seat.

**C5 -- the served read** shows, for all thirteen tools, an enveloped answer to an Opal stand-in principal, a refusal with zero reads to a non-Opal one, and a numeric `trading_days_behind_t1` where the tool states freshness; `registry_before` +13 on the host's own registry and on the repo pin.

**C6 -- the host-shaped import check** covers the three modules, the seam `typed_scope` and `app.tools` at a 4-parent path with `lib/trading_calendar.py` beside it.

## Not covered

- `harvest_get_published_analysis` (own ask), the G5 wave A and category-views tools (`OG-ap-20`), `mdpf_get_category_views`.
- Any other gateway change.

-- 2.0.0_SA_COO~O
