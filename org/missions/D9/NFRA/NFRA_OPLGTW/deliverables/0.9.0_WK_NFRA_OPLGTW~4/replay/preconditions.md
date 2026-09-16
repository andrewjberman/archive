# OG-c-2 replay preconditions -- read 2026-09-16 ~19:00-19:05Z by 0.9.0_WK_NFRA_OPLGTW~4

Released terms read at CLOUD HEAD 68bd819cd8 (shared tree): order amended @7c44a2cf82 (hold replaced by RELEASED on
R-OG-4/R-OG-5); sign-off Half 1 s.6 and Half 2 s.E re-signed (four-object write set, zero-write dry run as STOP).

D_r = 2026-09-15 for both masters.

## STOP precondition -- dry run (replay/dry_run.py, output replay/dry_run.json)
- 08242234: bronze=11 results=11 errors=0 silver_writes=0 missing_dims=0 missing_facts=0 actions=[skipped-hole, skipped-idempotent] marker_dates=[2026-09-15] closure_preview qualified/qualified findings=0 objects=14
- 08335338: bronze=11 results=11 errors=0 silver_writes=0 missing_dims=0 missing_facts=0 actions=[skipped-hole, skipped-idempotent] marker_dates=[2026-09-15] closure_preview qualified/qualified findings=0 objects=15
- `DRYRUN: ZERO-WRITES`, rc 0.
- Positive controls on the wrapper: a head_object on a nonexistent silver dim key is recorded as a miss (already_converted -> False);
  a put_object is recorded and refused before reaching S3.

## Condition 1 (windows) -- 08335338 write planned ~19:1xZ: outside 09:30-10:30Z, 12:40-13:00Z, 21:30-22:30Z.

## Condition 3 -- deploy/pre_deploy.json (botocore version ABSENT; decided by the record's write_guard).

## Condition 4 (49F reads admitted by R-OG-4; every key read printed)
- READ list-objects-v2 opal-data-49financial gold/advi/_logs/chain_20260916 -> 9 objects (8 at 09:46Z, 1 at 12:45Z).
- READ get-object gold/advi/_logs/chain_20260916T124542Z.log VersionId znOeMrzHJT6Qr4Aw4u2Zy6ziTnE790CN (146 lines):
  first `CHAIN START date=2026-09-15 mode=production ...`, last `CHAIN OK date=2026-09-15 wall=135.2s`.
  prev_trading_day(2026-09-16) = 2026-09-15.
- Lock: host i-01003b035d2988dfb (bd-gold-layer-runner) state `stopped` (ec2 describe-instances, 19:03Z) -- no process can
  hold the mkdir lock. SSM list-commands returned 0 commands even UNFILTERED, so that instrument is NOT EVALUATED here.

## Condition 6 -- 08242234 has no consumer (OG-p-1 OGP1-AC9; G-B Half 2 s.D).
