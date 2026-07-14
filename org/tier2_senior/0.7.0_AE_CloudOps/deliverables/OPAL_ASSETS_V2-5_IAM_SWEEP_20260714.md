# OPAL_ASSETS.V2-5 -- THE 22a IAM SWEEP (0.7.0's half of the bronze close-out certificate)

**Measured:** 2026-07-14T06:22:24Z, live `aws iam simulate-principal-policy`, us-east-1, account 313476888478.
**Measured by:** 0.7.0_AE_CloudOps. **Merge target:** DS's V2-5 certificate table (cells cite block IDs below,
attributed "0.7.0 (simulate, 20260714T0622Z)").
**Raw evidence:** `OPAL_ASSETS_V2-5_IAM_SWEEP_RAW_20260714/<block-id>.json` (one raw simulate output per block).
**Re-runnable:** `OPAL_ASSETS_V2-5_iam_sweep.sh` (read-only; simulate evaluates policy, writes nothing).

## COVERAGE DENOMINATOR (state it, per verification law 10)

- **Certificate channels: 7** (schwab/08242234, schwab/08335338, orion, eclipse, cottonwood [blackdiamond],
  smartx, etf [trueshares]). **Channels covered by a live producer-role sweep: 7/7.**
- **Roles swept: 5/5 live monolith producer identities** -- `opal-assets-ingest-router-role` (orion +
  eclipse + blackdiamond/cottonwood), `quartz-si2-spike-role` (schwab 0824 + 0833 daily REST box),
  `opal-schwab-monolith-remap-role` (schwab aux: one-time remap + pre-floor Glacier leg),
  `etfs-netassets-daily-role` (trueshares; also HOLDS pathfinder + msn scopes), `smartx-assets-pull-role`
  (smartx/*). Roster grounded APPLIED, not DESIRED: `list-entities-for-policy` on all 8
  `opal-assets-write-*` policies + `list-role-policies`/`get-role-policy` per role, live 06:1xZ.
- **Calls: 46, one `--resource-arns` per call** (mode-1 false-deny structurally excluded). Positive
  controls = separate invocations (R04, Q04, M05, E03, S02). `--context-entries s3:prefix` passed on every
  conditioned ListBucket statement (R06, Q04, M05, E04, S03); two rows (R07, Q05) deliberately re-run the
  SAME conditioned statement WITHOUT context and are labeled `instrument` -- they demonstrate mode-2
  false-deny (implicitDeny byte-identical to a real deny) and are NOT policy verdicts.
- **Result: 46/46 expectation-MATCH, 0 mismatch, 0 call errors.**

## PER-ROLE BLOCKS

### BLOCK R -- opal-assets-ingest-router-role (channels: orion/inflection, eclipse/inflection, blackdiamond/cottonwood)
| ID | Action | Resource (exact ARN) | Control | Verdict |
|---|---|---|---|---|
| R01 | s3:PutObject | opal-data-assets/orion/inflection/bronze/holdings/2026-07-14/sweep-probe.jsonl.gz | target | **allowed** |
| R02 | s3:PutObject | opal-data-assets/eclipse/inflection/bronze/accounts/2026-07-14/sweep-probe.jsonl.gz | target | **allowed** |
| R03 | s3:PutObject | opal-data-assets/blackdiamond/cottonwood/bronze/holdings/2026-07-14/sweep-probe.json | target | **allowed** |
| R04 | s3:GetObject | (R01 key) | positive, separate | **allowed** (read-back-verify law) |
| R05 | s3:GetObject | opal-data-inf/bronze/2026-07-14/sweep-probe.json | target | **allowed** (source read) |
| R06 | s3:ListBucket | opal-data-inf, context s3:prefix=bronze/2026-07-14/ | conditioned | **allowed** |
| R07 | s3:ListBucket | opal-data-inf, NO context | instrument | implicitDeny (mode-2 demo, not a verdict) |
| R08 | s3:PutObject | opal-data-bd/bronze/sweep-negative-probe | negative | **explicitDeny** (fence belt 2) |
| R09 | s3:PutObject | opal-data-inf/gold/meta/pipeline-complete.json (DOOR 6) | negative | **explicitDeny** (fence belt 3) |
| R10 | s3:PutObject | opal-data-assets/schwab/08242234/bronze/sweep-negative-probe | negative | implicitDeny (out-of-scope monolith prefix) |
| R11 | s3:DeleteObject | opal-data-assets/orion/inflection/bronze/sweep-negative-probe | negative | implicitDeny (additive-only) |

**Verdict: IAM CLEAN.** Fence PROVEN both directions: cannot mutate a source (R08 explicit), cannot touch
Door 6 (R09 explicit, s3:*), cannot cross into another channel's monolith tree (R10), cannot delete even
its own tree (R11).

### BLOCK Q -- quartz-si2-spike-role (channels: schwab/08242234 + schwab/08335338; the write-only box)
| ID | Action | Resource | Control | Verdict |
|---|---|---|---|---|
| Q01 | s3:PutObject | opal-data-assets/schwab/08242234/bronze/ACC/20260714/sweep-probe.zip | target | **allowed** |
| Q02 | s3:PutObject | opal-data-assets/schwab/08335338/bronze/ACC/20260714/sweep-probe.zip | target | **allowed** |
| Q03 | s3:PutObject | opal-data-assets/schwab/08242234/_ops/daily_pull/sweep-probe.json | target | **allowed** (run manifest) |
| Q04 | s3:ListBucket | opal-data-assets, context s3:prefix=schwab/08242234/bronze/ | conditioned + positive | **allowed** (skip index) |
| Q05 | s3:ListBucket | opal-data-assets, NO context | instrument | implicitDeny (mode-2 demo) |
| Q06 | s3:GetObject | opal-data-assets/schwab/08242234/bronze/sweep-probe.zip | negative | implicitDeny (**write-only invariant holds**) |
| Q07 | s3:PutObject | opal-data-bd/bronze/sweep-negative-probe | negative | **explicitDeny** (DenyBdPlane) |
| Q08 | s3:PutObject | DOOR 6 key | negative | **explicitDeny** (DenyInfPlane) |
| Q09 | s3:PutObject | opal-data-assets/orion/inflection/bronze/sweep-negative-probe | negative | implicitDeny (out-of-scope prefix) |
| Q10 | s3:PutObject | opal-data-assets/schwab/**99999999**/bronze/sweep-negative-probe | negative | implicitDeny (**invented master denied -- never-commingle is a property of the ROLE**) |

**Verdict: IAM CLEAN.** The C3 header's "AUTHORED, NOT APPLIED" is now stale: `quartz-si2-monolith-write`
is live inline on the role (list-role-policies 06:1xZ; the role also carries `quartz-si2-backfill-08335338`
+ `quartz-si2-spike-inline`). Masters enumerated, wildcard master refused (Q10), box cannot read the
consolidated estate (Q06), firm planes explicit-denied (Q07/Q08).

### BLOCK M -- opal-schwab-monolith-remap-role (schwab aux; one-time remap + Glacier pre-floor leg)
| ID | Action | Resource | Control | Verdict |
|---|---|---|---|---|
| M01 | s3:GetObject | opal-data-schwab/08242234/bronze/sweep-probe.zip | target | **allowed** (staging read) |
| M02 | s3:PutObject | opal-data-assets/schwab/08335338/bronze/sweep-probe.zip | target | **allowed** |
| M03 | s3:RestoreObject | opal-data-schwab/01_raw/CRS20230117.RLD | target | **allowed** (thaw; grant REMOVED at migration close per CTO ruling) |
| M04 | s3:GetObject | opal-data-schwab/01_raw/CRS20230117.RLD | target | **allowed** (H1 master observation + tier-3 MD5) |
| M05 | s3:ListBucket | opal-data-schwab, context s3:prefix=08242234/bronze/ | conditioned + positive | **allowed** |
| M06 | s3:GetObject | opal-data-assets/schwab/08242234/bronze/sweep-probe.zip | negative | implicitDeny (**cannot read the monolith** -- verify-by-listing design) |
| M07 | s3:DeleteObject | opal-data-schwab/01_raw/CRS20230117.RLD | negative | implicitDeny (**cannot delete a byte**) |
| M08 | s3:PutObject | opal-data-bd/bronze/sweep-negative-probe | negative | **explicitDeny** (DenyBdPlane) |
| M09 | s3:PutObject | DOOR 6 key | negative | **explicitDeny** (DenyInfPlane) |
| M10 | s3:GetObject | opal-data-schwab/backfill/sweep-negative-probe | negative | implicitDeny (read scoped to master bronze + 01_raw only) |

**Verdict: IAM CLEAN** for its lifecycle stage. NOTE for the closure step already ruled: `PreFloorRestore`
(M03) is scheduled for REMOVAL when the Glacier fill completes -- this sweep will need a one-block re-run
then (expect M03 -> implicitDeny) to certify the closure.

### BLOCK E -- etfs-netassets-daily-role (channel: etf/trueshares; role also HOLDS pathfinder + msn)
| ID | Action | Resource | Control | Verdict |
|---|---|---|---|---|
| E01 | s3:PutObject | opal-data-assets/trueshares/DIVZ/bronze/netassets/2026-07-14/sweep-probe.json | target | **allowed** (**tonight's C4 AC1 first landing is NOT IAM-blocked -- pre-flight PASS**) |
| E02 | s3:PutObject | opal-data-assets/trueshares/IDVZ/bronze/netassets/2026-07-14/sweep-probe.json | target | **allowed** |
| E03 | s3:GetObject | (E01 key) | positive, separate | **allowed** (read-back-verify) |
| E04 | s3:ListBucket | opal-data-assets, context s3:prefix=trueshares/DIVZ/bronze/ | conditioned | **allowed** |
| E05 | s3:PutObject | opal-data-etfs/bronze/netassets/2026-07-14/sweep-probe.json | target | **allowed** (legacy grammar until cutover) |
| E06 | s3:PutObject | opal-data-bd/bronze/sweep-negative-probe | negative | implicitDeny (**no-grant only -- NO fence on this role**) |
| E07 | s3:PutObject | DOOR 6 key | negative | implicitDeny (**no-grant only -- NO explicit deny on this role**) |
| E08 | s3:PutObject | opal-data-assets/schwab/08242234/bronze/sweep-negative-probe | negative | implicitDeny (out-of-scope prefix) |

**Verdict: IAM CLEAN on grants; fence gap OBSERVED (see recommendations).** Grant source is the role's own
inline `s3-rw-etfs-bronze-silver` (the standalone `opal-assets-write-trueshares` policy is attached to
nothing -- fine: the grants live inline, sweep attests APPLIED reality). Role holds pathfinder/* + msn/*
write scopes ahead of their producers landing -- same channel family (C4/0.5.0-owned), noted not flagged.

### BLOCK S -- smartx-assets-pull-role (channel: smartx/*; C5 pull engine)
| ID | Action | Resource | Control | Verdict |
|---|---|---|---|---|
| S01 | s3:PutObject | opal-data-assets/smartx/model/bronze/holdings/20260714/sweep-probe.json | target | **allowed** |
| S02 | s3:GetObject | (S01 key) | positive, separate | **allowed** (AC10 re-derive) |
| S03 | s3:ListBucket | opal-data-assets, context s3:prefix=smartx/model/bronze/ | conditioned | **allowed** (distinct-landing guard) |
| S04 | s3:PutObject | opal-data-bd/bronze/sweep-negative-probe | negative | implicitDeny (**no-grant only -- NO fence**) |
| S05 | s3:PutObject | DOOR 6 key | negative | implicitDeny (**no-grant only**) |
| S06 | s3:PutObject | opal-data-assets/trueshares/DIVZ/bronze/sweep-negative-probe | negative | implicitDeny (out-of-scope prefix) |
| S07 | s3:PutObject | opal-data-smartx-v2/sweep-negative-probe | negative | implicitDeny (old pipeline bucket, no grant) |

**Verdict: IAM CLEAN on grants; fence gap OBSERVED (same class as BLOCK E).** The TF's `smartx = ["*"]`
scope wildcard (honest-wildcard-over-wrong-enumeration, flagged in monolith.tf) is visible live: the grant
is `smartx/*`, so S06-style cross-channel denial holds but intra-smartx scope enumeration awaits C5's
roster grounding (0.5.0 narrows it).

## HONEST LIMITS OF THIS INSTRUMENT (what 46/46 does NOT attest)

1. **Identity-plane only.** `simulate-principal-policy` as invoked here evaluates the ROLE's policies; it
   does not fold in resource-plane bucket policies. Known live interaction: `opal-data-schwab` carries
   `DenyUnencryptedObjectUploads` (runtime Puts need the AES256 SSE header regardless of these verdicts).
   The monolith itself: SSE-S3/AES256 default, NO bucket-policy deny statement (13a reversed) -- so the C3
   file's open SSE fork is RESOLVED-AS-BUILT: producer grants are encryption-complete, no KMS grants needed.
2. **allowed != exercised.** These are policy verdicts, not landed bytes. The behavior layer is attested
   separately (C2 close validation; C4 AC1 tonight on the scheduled run's artifact, listing-based; C3/C5
   producers' own landed-bytes evidence).
3. **The "no other writer" negative is bounded.** "No identity holds smartx/pathfinder/msn write policy
   attachments" is grounded (list-entities-for-policy, all 8 policies); "no OTHER role in the account holds
   an inline monolith write grant" was NOT exhaustively swept (that requires enumerating every role's every
   inline policy account-wide). Bounded-unknown, stated.

## RECOMMENDATIONS (CTO's to disposition -- surfaced, not applied)

1. **Attach `opal-assets-one-way-fan-in-fence` to `etfs-netassets-daily-role` and `smartx-assets-pull-role`.**
   Both currently protect the sources and Door 6 by NO-GRANT ONLY (E06/E07, S04/S05); the fence upgrades
   that to provable incapability (explicit Deny). It is never-widen-safe by construction (a Deny only
   narrows) and was designed attachable ("every future ingest producer after it"). One caveat to check at
   attach time: the fence's belt 1 NotResource denies mutations OUTSIDE the monolith -- netassets still
   legitimately writes opal-data-etfs (E05 legacy grammar) until the C4 cutover, so for THAT role the
   attach belongs AFTER cutover (belt 1 would kill the legacy write path today). smartx-assets-pull-role
   has no such conflict and could take the fence now.
2. **Remap-role closure re-run:** on Glacier-fill completion, re-simulate M03 expecting implicitDeny after
   the ruled grant removal.

-- 0.7.0_AE_CloudOps, 2026-07-14
