# in-VPC full-Nessie proof -- clean-lifecycle ledger (CTO condition 4)

**Status: RUN HELD** for CTO's clear-to-run signal (Approach A sequencing: run AFTER the live materialization's
applied-close lands on globgrph Nessie). Code BUILT + committed @d2e7e4d18. Nothing touched yet -- only the
read-only feasibility investigation (describe/list) has run.

## Gate + conditions (CTO, 2026-07-18, 195459Z -- verbatim intent)
- **APPROACH A APPROVED** (SSM tunnel + throwaway branch on prod Nessie) over B (a throwaway-Nessie deploy).
- **1. EC2 = the t4g.nano UTILITY box `i-07dccb1615503ac99` ONLY.** The Windows t3.large `i-0f3d57a97f14727af`
  is **OFF-LIMITS -- the SCHWAB client-data box (canonical-schwab-si2, Andrew-direct never-touch).** Ubuntu
  t3.small avoided too (nano is the safe pick).
- **2. SSM SESSION ONLY** -- zero writes to the box.
- **3. THROWAWAY BRANCH ONLY** (`genesis-verify-<uuid>`) -- NEVER main; scratch S3 Iceberg prefix only.
- **4. TEARDOWN + VERIFY** -- delete branch + scratch prefix, then verify branch absent from the ref list +
  prefix empty + zero orphans. (this ledger.)
- **5. SEQUENCING** -- run HELD until CTO signals the materialization applied-close has landed.
- **STOP + surface** if anything about the tunnel or branch surprises mid-run.

## RUN runbook (execute IN ORDER on CTO's clear-to-run)
```
# 0. record start here (RUN-START section below) BEFORE touching anything.
# 1. open the SSM port-forward tunnel to Nessie through the utility nano (background session):
aws ssm start-session --target i-07dccb1615503ac99 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters host=nessie.opal-globgrph.local,portNumber=19120,localPortNumber=19120
# 2. sanity: GET http://localhost:19120/api/v2/config -> 200 (Nessie reachable via the tunnel).
# 3. a scratch S3 warehouse prefix (reuse the sandbox pattern: a throwaway bucket, or a scratch prefix):
#    warehouse = s3://<scratch-bucket>/genesis-nessie-verify
# 4. run the proof (creates genesis-verify-<uuid> off main, commits C0 CSEs, reads back, tears down + verifies):
cd infra/system/sdk && ./genesis verify --nessie http://localhost:19120 \
  --warehouse s3://<scratch-bucket> demo --teardown
# 5. STOP + surface to CTO if any Nessie v2 REST shape / Iceberg-REST ref config surprises (see nessie_verify.py
#    helpers -- one-line fixes). Re-run after the fix.
# 6. independent teardown-verify (do NOT trust the tool's self-report alone):
curl -s http://localhost:19120/api/v2/trees | grep -c genesis-verify   # expect 0 (branch gone)
aws s3 ls s3://<scratch-bucket>/genesis-nessie-verify/ --recursive     # expect empty (prefix gone)
# 7. close the tunnel session. Delete the scratch bucket if one was created (like the sandbox lifecycle).
```

## RUN-START
- [ ] (fill at run-time: timestamp, the exact warehouse, the branch name, tunnel confirmed 200)

## RUN-RESULT
- [ ] (fill: loop_closed, branch round-trip PASS/FAIL, metadata_location on the branch, any API-detail fixes)

## TEARDOWN-VERIFY (the acceptance for a clean lifecycle)
- [ ] branch `genesis-verify-<uuid>` ABSENT from `GET /api/v2/trees` (independently, not the tool's word)
- [ ] scratch S3 prefix EMPTY (`aws s3 ls` recursive -> zero)
- [ ] main branch UNTOUCHED (never written)
- [ ] tunnel session closed; scratch bucket deleted (if created); zero orphans
- [ ] route the result (branch round-trip PASS + teardown-verified) to CTO as the in-VPC component-proof close
      (completes the residual @c6cf0ed91)

## Provenance
Andrew authorized the scope (2026-07-18, a scoped question). CTO gated Approach A + the 5 conditions (195459Z).
Code: `gensdk/loop/nessie_verify.py` + `genesis verify --nessie` (@d2e7e4d18). This is a COMPONENT proof
(re-proving Nessie, a reused/already-proven component) -- framework acceptance was already CTO-ruled complete;
this closes the "full end-to-end on real infra" residual.
