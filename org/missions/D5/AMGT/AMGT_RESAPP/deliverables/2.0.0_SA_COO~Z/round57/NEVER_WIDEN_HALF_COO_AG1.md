# AMGT_RESAPP round 57 -- `AMGT-ag-1` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-01 ~07:4xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names. Its parts:
- item 0: `CLOSURE_ROOTS` gains `lib.trading_calendar`;
- build + upload ONE artifact to `s3://opal-313476888478-lambda-artifacts/research/opal-amgt-scoped-api.zip`;
- ONE code-only `safe-apply`.

Executor `0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-ag-1.the-one-redeploy.md`; decomposition s.65 (s.65a is the
deploy-act list round-56 ruling 3 requires).

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `/QP4upEVzTjnHV2bAeIXIud0k0DgjDDGrlMgtm0uo7o=` |
| function LastModified | `2026-09-30T15:22:01.000+0000` (ac-3) |
| artifact S3 VersionId | `C9brZ5Qd6_.iSbxw3NKZOxHuDByQScll` (LastModified 2026-09-30T15:18:58Z, 40,117,280 B) |

Immediately before the build, re-read the CodeSha256. A moved one is a STOP and a re-sign.

## WRITERS OF THE PROPERTY: 2 seats, 1 path

The function's code has one write path: `build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply` on `infra/aws/terraform/harvest`.
Two projects drive it: AMGT_RESAPP (this act) and AMGT_HARVST (HVST-a-2 and HVST-i-4 deployed through it). Both owners were told at
07:1xZ (msgs 27576, 27577), and silence by 08:00Z means their merged changes ride. No other open order redeploys this function.

## THE FILE LIST (CONTENT-DIFF at the ag-2 drain tip `cb5f25b9de`, with item 0's closure line applied for the measurement only, against the live artifact: files 350, IDENTICAL 336, CHANGED 8, ADDED 6, REMOVED 0; `--build-only` rc=0 incl. the isolated-runtime arm)

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | af-1 dispatch, af-2 read functions, ag-0 | the collected/chatter route; T-1 fallback on per-name reads; `stale_trading_days`; `breakout_price`; breakout `score` x100 + `score_pct` / `pct_jump_pct` / `return_30d_pct`; `absent_reason` / `places_moved` on overlay axis reads |
| `lib/research/api/monthly_chatter.py` | ADDED | af-1 | the new route body |
| `lib/research/coverage/covered_universe.py` | ADDED | af-0 | the route's universe |
| `lib/trading_calendar.py` | ADDED | ag-0 + item 0 | staleness counts |
| `lib/research/api/case_rule.py` | CHANGED | CORPUS ab-3 `c4d3e8dfa2` | mixed-currency constructed input served null with reason (thesis/model) |
| `lib/research/corpus/dossier.py` | CHANGED | CORPUS ab-1 `0c234ef97d` | dossier model-block paths through slash-safe keys (BP/, NG/ now read) |
| `lib/research/harvest/publication_gold.py` | CHANGED | HARVST ae-1 phase A `1b55276f0d` | NON-INERT: the timeline routes no longer count quarantined sa wrong-object rows |
| `lib/opal_naming.py`, `infra/logic/registry/systems.json`, `scopes.json` | CHANGED | VENDOR display_name (`70c4aa2e1a`, `b5dc2e63d1`, NFRA_TRNSPT `8e9ed1b539`/`224058ea3f`) | none on the served path (naming metadata) |
| `lib/research/api/_harvest_prefixes.py` | CHANGED | af-4 | none (hash only; every prefix equal) |
| `lib/research/scores/peers_v.py`, `divergence.py`, `robustness.py` | ADDED to the package (newly imported by `read_scores`) | ag-2 `678e9ac1c5` (drained `cb5f25b9de`) | served score reasons in plain words, translated at serve time (stored `scores/v1` objects unchanged) |
| `lib/research/api/scoped_amgt.py` (ag-2 part) | CHANGED | ag-2 | `read_scores` / `ceo_profile_reading` / `read_description` plain wording; posture `absent_reason` when the verdict is `absent` |

A CHANGED or ADDED file outside this list at build time is a STOP.

**The riders' reads through the function's own role** (IAM simulate on `opal-amgt-scoped-api-role`, 06:5xZ): `s3:GetObject` on the
live HARVST quarantine object `seeking-alpha/harvest/silver/quarantine/date=2026-10-01/20261001T064759Z.json` is **allowed**;
`s3:ListBucket` with prefix `seeking-alpha/harvest/silver/quarantine/` is **allowed**; the same for `amgt/harvest/gold/research_dossier/`
(af-0) and GetObject on gold `article_security_mention/` (af-1). Negative control: `s3:PutObject` on the quarantine prefix reads
`implicitDeny`. This satisfies COO~H's condition (msg 27579): `publication_gold.sa_quarantined_keys` reads that prefix on every
timeline call, with no fallback.

## READERS

- The Security Analysis page on portal DEV and PROD reads `/api/scoped/amgt/*` through CloudFront -> API Gateway -> this function.
  DSGN round 15 (drained `78cf9877`) already reads the new names (`as_of_date`, `breakout_price`, `places_moved`, `absent_reason`).
- No other consumer of this function is known in the estate (the route table is the denominator: 18 routes, unchanged).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| item 0 | one line of the build script | `git revert` of its commit |
| upload | a new version of the artifact key (versioned bucket) | the prior VersionId above is the rollback input |
| code-only `safe-apply` | the function's code (source hash) and nothing else; no IAM, route, gateway or alias change | a code-only `safe-apply` with the prior artifact version (`C9brZ5Qd6_...`), restoring CodeSha256 `/QP4upEV...` |

## EXPECTED OUTCOME -- both branches, read from the code's own rules (never predicted)

- **Every route answers 200 where it did before; one new route answers 200.** `timeseries/collected/chatter` returns 95 rows from
  the gold snapshots (the covered denominator is read fresh). An empty month is absent; zero publishers are omitted (round-56 ruling 1).
- **Per-name and ranking reads on a day with no producer file** serve the latest COMPLETE generation, with `stale_trading_days` from
  the trading calendar. On a day WITH a file (after af-6's branch A), they serve that day with `stale_trading_days` 0. Both branches
  are graded by AC1 (FWD-33 C2 reads the equality either way).
- **Breakout price figures** move from fraction to percent (0.0921 -> 9.21). That move IS the FWD-34 fix; the page shows them as
  served.
- **Rider branches:** a timeline count for a name with quarantined sa rows may fall (HARVST ae-1). That is HARVST's intended
  correction, named here and not graded by this act.
- **AC1 and AC2 fail after the act -> ROLLBACK** per the table.

## WHAT THIS HALF DOES NOT COVER

No portal deploy or promote. No store write, no S3 delete, no vendor call. No IAM, route or gateway change: any of these in the plan is
a STOP.
