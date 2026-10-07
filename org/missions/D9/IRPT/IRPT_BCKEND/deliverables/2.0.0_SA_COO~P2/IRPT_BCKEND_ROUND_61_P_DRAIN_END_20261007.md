# L8 drain end -- IRPT_BCKEND round 61, workstream ~P

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-07 ~09:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile)
**Cut from:** the CTO round analysis @e363a194ed, section 5 (E-P1..E-P7). Issuance @561577da0d, decomposition section 54.

Every order of the round is terminal and merged:
- **Orders:** 7 of 7 (IB-pr-329..335).
- **Proof instances:** 7 of 7 VALID at their drains.
- **Judgment criteria:** 0.
- **Re-runs:** the issuer re-ran every build criterion in the worker's worktree, or on CLOUD, before or after the merge.
- **Worktrees and branches:** 0 left; all six removed explicitly.
- **Drain hygiene on merged CLOUD:**
  - directory suite: 181 passed;
  - performance suite: 252 passed;
  - release-census tests: 10 passed;
  - CI shell tests: `test_build_only.sh`, `test_build_artifact_key.sh` and `test_record_terraform_deploy_paths.sh` all PASS;
  - `py_compile`: OK.

## Orders

| order | item | slot | drain | criteria | real run at close |
|---|---|---|---|---|---|
| IB-pr-329 | E-P1 one S3 key per function (S343) | ~132 | @4df13fb3ae | IB61-1-AC1, AC2, G PASS (issuer re-ran AC1/AC2, read the 3-line diff) | BUILD_ONLY of the three reporting functions prints `key=` equal to each map `artifact_s3_key`. The next upload of these functions needs no manual copy-object |
| IB-pr-330 | E-P2 recorder stages only its own paths (S344) | ~133 | @a92094baed | IB61-2-AC1, G PASS (issuer re-ran AC1) | HEAD failed both arms before the fix. The recorder now commits the audit file only when it changed, and CHANGELOG append is idempotent per deploy. Exercised for real at the next release record |
| IB-pr-331 | E-P3 issuer-built release census (S337) | ~134 | @832b0cad5d; amendment 1 @a6c8cad56e (AC2 expects 4, not 19); instance + flip by the issuer | AC1, AC2 (amended), G PASS | REAL RUN on CLOUD b9411881a0. `irpt-directory-search` changed_members=3. `irpt-directory-refresh` changed_members=2, one of them a rider (row S357). Row W134-S1 explains 4 vs 19: the issuer re-read 3 of the disputed 15 members live against their blobs, and they are byte-equal |
| IB-pr-332 | E-P4 the adapter builds (W127-S1) | ~135 | @52d6068f97 | IB61-4-AC1, G PASS (issuer re-ran AC1) | BUILD_ONLY of `irpt-performance-adapter` exits 0 past the parity gate (sha EpkkyyOM..). W127-S1 disarms on that build |
| IB-pr-333 | E-P5 refresh manifest by dispatch date (S348) | ~136 | @f2fa74df85 (chain e) | IB61-5-AC1, G PASS (issuer re-ran) | Code only. The release and the driven fire are the issuer's, under the directory release packet beside this file |
| IB-pr-334 | E-P6 search serves the over-age branch (FWD-7) | ~136 (re-seated cold; the first subagent could not be resumed) | @f2fa74df85 (chain e) | IB61-6-AC1, AC2, G PASS (issuer re-ran) | BUILD_ONLY search zip: 24 members, `expiry.py` and `trading_calendar.py` added. Release under the same packet |
| IB-pr-335 | E-P7 FWD-2 replay on current bytes | ~137 | @7a95c1a772 | IB61-7-AC1, G PASS (issuer re-ran) | 21 live routes (get-routes = routes.json; the older 12-route table is stale). 84 arm cells, 0 driven failures. Authenticated and advisor arms are GATED (no test principal; Andrew's to name, analysis section 6 item 2). FWD-2 is NOT realized by this run |

## Rows filed in the round

| row | class | standing |
|---|---|---|
| W132-S1 | OBSERVATION, INERT | the builder's field-list script needed one line to emit `artifact_s3_key` (inside the granted file) |
| W134-S1 | OBSERVATION, INERT | census 4 vs 19; resolved by amendment 1 on the issuer's re-read |
| W136-S1 | OBSERVATION, INERT | `DIRECTORY_OVER_AGE` is not in `_authz/served.py` BOUNDARY_REASONS; the over-age status comes from expiry's envelope. Precondition of the directory release (consumer read) |
| W136-S2 | OBSERVATION, INERT | a builder run without BUILD_ONLY was started. The issuer verified that the S3 object (version S5vL.tP9.., 2026-10-06) and the live CodeSha are unchanged |
| W137-S1, W137-S2 | OBSERVATION, INERT | 15/15/17 GATED arms for want of an operation-shaped fixture; the face did not define "protected field" (the worker's definition is recorded) |
| S355 | DISMISSED | re-points S350's citation to S354 |
| S357 | OBSERVATION, INERT | irpt-directory-refresh runs a handler.py older than its recorded deploy commit; a release ships UIR-07 riders |

## Outside the round, closed in the window

- **Ledger irpt-inf-performance-serving-20261002: CLOSED** (leg A1 PASS under the second amendment @4d87781522). The COO half was re-signed twice.
- **Rows filed:** S349 disarms S335; S350 disarms S347; S354 is the CTO's filing of the laptop measurement.

## Not yet done (the issuer's, next)

- **The directory release** (E-P5 criterion 3, E-P6 criteria 2-3). Packet: `IRPT_BCKEND_R61_DIRECTORY_RELEASE_PACKET_20261007.md` beside this file. It needs the CTO half.
- **IRPT_CUSTDY a1-a4 and the render_export.cjs:240 refusal.** The CTO ruled these into this seat's NEXT issuance (msg 230).
