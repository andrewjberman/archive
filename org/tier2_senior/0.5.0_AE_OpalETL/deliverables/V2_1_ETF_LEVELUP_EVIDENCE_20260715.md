# OPAL_ASSETS.V2-1 -- ETF channel level-up: build evidence (2026-07-15 ~22:0x-22:3xZ)

**Filed by:** 0.5.0_AE_OpalETL. **GO:** COO 220354Z (auto-fire clause on the GREEN 07-15
parity row). **Scope held to the TO's three items exactly; nothing else in the producer
touched.** Deploy leg AWAITS the CTO code-review gate (AC4) -- this file is the pre-review
evidence pack.

## The three items, as built

1. **LANDED VERIFY (set-identity landing guard).** `landing_guard.py` lifted BYTE-IDENTICAL
   from the C5 producer (its own docstring anticipates the lift; CTO-ratified reference
   pattern). Bronze: per touched run-date prefix, fresh ListObjectsV2 (Size>0), set(landed)
   == set(enumerated) BOTH directions -- shortfall AND surplus RAISE; denominator enumerated
   AT RUN TIME from the run's own manifest (13b). Silver: exact-key listing, non-empty, per
   written key (shortfall class only -- surplus is structurally nil on an exact-key listing,
   stated in the code, not implied). Manifest landing itself listing-verified after write.
2. **MANIFEST PERSISTED.** Per (source, scope) touched:
   `{source}/{scope}/meta/pulls/{YYYYMMDD}/etfs_netassets_pull_manifest.json` (ruling 21 meta
   home, disjoint from every guarded bronze prefix), carrying bronze entries (url/key/bytes),
   the guard verdict, silver keys, tiers, fired_at. Monolith grammar only; legacy grammar
   prints a LOUD skip (no ruling-21 home), never silent.
3. **RETRY CLIENT.** urllib -> requests.Session + urllib3 Retry (total=4, backoff 1.5x,
   status_forcelist 429/500/502/503/504, GET-only), the C5 smartx_client pattern -- reuse not
   re-derive. UA header preserved; raise_for_status keeps the urlopen contract (an HTTP error
   RAISES; error bytes never return as issuer content). NO LAYER CHANGE: the deployed layer is
   pandas-pyarrow-requests-layer:1 -- requests already ships (TF-grounded, netassets-lambda.tf).

KEPT (untouched, per TO): no-swallow writes, layout/header/values change-detection RAISES,
source-tier ladder + degraded reporting, fund-unavailable hard-fail, bronze/silver bucket
separation, msn tier-3 leg (CTO's strike rides his gate separately), silver on the LEGACY
bucket (V2-8's job).

## AC1 -- the mutant transcript (test_landing_verify.py, run 2026-07-15 ~22:2xZ, exit 0)

```
V2-1 LANDING GUARD -- set identity over LANDED keys (pure core)
==================================================================
  OK    identical sets reconcile clean (the only PASS shape)
  OK    SHORTFALL RAISES: 2 enumerated / 1 landed (collision class)
  OK    SURPLUS RAISES: un-enumerated key landed (stray-write class)
  OK    GROWTH-BOUNDARY RAISES: run-time denominator covers a grown roster; hardcoded-4 would have passed silently
  OK    zero-byte object is NOT a landing (Size>0 filter holds)

V2-1 RETRY CLIENT -- requests + urllib3 Retry (C5 pattern)
==================================================================
  OK    retry total == 4
  OK    backoff factor == 1.5
  OK    429/5xx in status_forcelist (transient vendor hiccup retried)
  OK    UA header preserved on the session (issuer contract unchanged)
  OK    HTTP error RAISES via raise_for_status (urlopen contract kept)

ALL V2-1 GUARD + CLIENT MUTANTS PASS (every mutant fired).
```

## IAM (PRD 2 bar col 3 -- recorded simulate outputs ARE the evidence; comp-iam GREEN is not)

Battery run 2026-07-15 ~22:3xZ against arn:aws:iam::313476888478:role/etfs-netassets-daily-role.
ONE --resource-arns per call; every invocation SEPARATE; conditions carried via
--context-entries where the statement is conditioned (ListBucket s3:prefix). 8/8 as expected:

| # | call | resource | decision |
|---|---|---|---|
| P1 | s3:PutObject | opal-data-assets/trueshares/DIVZ/meta/pulls/20260715/etfs_netassets_pull_manifest.json | **allowed** |
| P2 | s3:PutObject | opal-data-assets/pathfinder/filepoint/meta/pulls/20260715/etfs_netassets_pull_manifest.json | **allowed** |
| P3 | s3:ListBucket + context s3:prefix=trueshares/DIVZ/bronze/netassets/20260715/ | opal-data-assets | **allowed** |
| P4 | s3:ListBucket + context s3:prefix=_cloudprobe/silver/netassets/2026-07-15.parquet | opal-data-etfs | **allowed** |
| N1 | s3:PutObject (FIRM bucket control) | opal-data-bd/anything/x.json | **implicitDeny** |
| N2 | s3:PutObject (DOOR-6 SENTINEL control) | opal-data-inf/gold/meta/pipeline-complete.json | **implicitDeny** |
| N3 | s3:PutObject (out-of-scope monolith prefix) | opal-data-assets/schwab/0824/meta/x.json | **implicitDeny** |
| N4 | s3:ListBucket + context s3:prefix=schwab/ (unsatisfied condition) | opal-data-assets | **implicitDeny** |

**ZERO IAM CHANGES NEEDED**: the existing `{src}/*` grant (trueshares/pathfinder/msn) already
covers the meta/pulls manifest keys and the guard listings; the fence held on all four
negatives including Door 6.

## Remaining ACs

- AC3: the guard's OWN verdict on a SCHEDULED fire = tomorrow's 22:00Z run post-deploy
  (fire/run/land/verify, trading-calendar-resolved).
- AC4: CTO code-review gate on the producer diff -> then the deploy leg (build -> commit ->
  upload+read-back -> plan gate -> safe-apply -> 0-diff -> three-way sha tie -> tag).
  Source map updated (landing_guard.py added to the files list) IN THIS COMMIT (Rule 4).
- Sequencing flag at the gate: CTO's msn code-strike targets the same producer at the same
  artifact-swap gate -- whether it rides THIS review/deploy cycle is his call; this diff is
  msn-untouched.

---

## CLOSE ADDENDUM (2026-07-17, filed by 0.5.0_AE_OpalETL on CTO ruling 20260717T160236Z)

**V2-1 CLOSED WHOLE.** The remaining ACs discharged as follows:

- **AC4 + deploy leg: DONE 2026-07-15 night** (not today). CTO reviewed both commits
  (3461d1c4d build + e45606d46 bundled msn strike) and ran the deploy leg himself; tag
  `etfs-netassets-v1.3.0` (07-15 23:54Z ET-4) records "both CTO-reviewed commits, one
  artifact; three-way sha tie 4/6gMExw...; AC3 rides 2026-07-16 22:00Z". Live lambda
  LastModified 2026-07-15T23:52:03Z.
- **07-17 live re-verification (this session, 4-way tie):** live lambda CodeSha256 ==
  S3 artifact sha256 (downloaded + hashed) == source-map `artifact_sha256` == the tag-message
  sha, all `4/6gMExwwY1w3No9D4AeTARMXZaVjDHf1cBYq7yL5gw=`. Artifact content-verified: carries
  `landing_guard.py`, requests+Retry client, meta/pulls persist -- the TO's three items.
- **AC3 = the 2026-07-16 22:00:09Z SCHEDULED fire (CTO-accepted 160236Z):** manifests landed
  both scopes (`trueshares/DIVZ/meta/pulls/20260716/` 902B + `pathfinder/filepoint/.../20260716/`
  1197B @ 22:00:15Z), `landing_guard: "set-identity PASS (shortfall+surplus, ListObjectsV2
  landed bytes)"`, silver keys written incl `2026-07-16.parquet`. 07-16 = Wednesday, a trading
  day, T-0 -- no calendar resolution needed.
- **Record-drift note (the lesson):** this session's gate ledger initially surfaced AC4 as
  pending off THIS file's 07-15 "deploy leg awaits" line -- a stale record read as state.
  Ground-truthing the live lambda before executing prevented a redundant deploy motion.
  Tonight's 22:00Z is a normal scheduled fire, not a gate.
