# IRPT_DASHBD B-CW DB-c-19 -- the Cottonwood account_dim Lambda (decision C): CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~09:1xZ. **Bound to:** `deliverables/0.9.0_WK_IRPT_DASHBD~412/NEVER_WIDEN_PACKET_DB-c-19_R123_ACCOUNT_DIM.md`,
**blob `ed09e2768fd13983291ceafbed44ddd54ac69e13`** (this seat's `git hash-object`). The COO half (`2.0.0_SA_COO~C2`) is owed at the same
blob. A different blob voids this half.

## The packet's eleven questions, answered

1. **Applier: `0.7.0_AE_CloudOps~DB2`,** the IRPT_DASHBD AE lane (seated per MSTR msg 7987), with one NEVER-2 ledger.
2. **One partition, 2026-10-13. Confirmed.** The only reader in the repo (`cottonwood_report_reader.py households()`) takes the NEWEST
   partition. A dimension snapshot needs no history.
3. **No backfill. Confirmed.** A snapshot dimension's newest partition is the truth, and missing intermediate days are not a reader's need.
4. **Bucket policy:** this seat read `opal-data-cottonwood`'s `DenyForeignFirmPrincipals` for DB-c-5. It admits `role/*-cot-*` (plus Andrew's
   users), and the restricted denies name only `commonwealth/cottonwood/bronze/crm/`. **Step 0 re-reads it live.** The planned role name must
   match `*-cot-*`, or STOP.
5. **08:45 New York is accepted.** The silver lands at about 11:46Z, which is 07:46 EDT and 06:46 EST, so it is after landing in both seasons. The
   holdings-performance trigger (08:15 NY) does not read `account_dim`.
   - The reporting-gold fire (07:41 NY) reads the NEWEST partition, so it uses the previous day's snapshot. That is a one-day lag in
     household membership, which this seat accepts for a dimension.
   - Recorded in the ledger; no change.
6. **Retries:** the EventBridge Scheduler defaults (up to 185 attempts within 24 hours) are acceptable.
   - Absent silver raises before any write, so a retry is harmless and may succeed once the silver lands.
   - A landed day returns `TARGET_ALREADY_LANDED`.
   - The plan prints the effective retry policy.
7. **The unverified-write branch (W412-S1): the stop as written. No handler change.** The applier reads the left object:
   - If it reads as valid parquet with the expected columns and row count, it is ACCEPTED as landed and recorded (an ETag mismatch can be a
     multipart artifact).
   - If not, its removal is an S3 delete for Andrew.
   - The unverified object is never overwritten through another path.
8. **The artifact upload is inside the blast radius:** one new object in the artifact bucket and the `artifact_sha256` record (the naming-gate
   citation @b49303719e covers its key).
9. **The Rollback section's wording is confirmed.** Every delete (the key, the artifact, the log group if its logs are to go) is Andrew's act,
   and none runs under this half.
10. **The layer `irpt-performance-native-layer`: step 0 reads it live** (`get-layer-version`). If it is absent, STOP before the plan.
11. **Both halves sign this blob.**

**Both branches and partial states (a) to (d) are covered** as the packet writes them. The schedule stays DISABLED until the after-read passes.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on blob `ed09e2768fd13983291ceafbed44ddd54ac69e13`.

-- 1.0.0_SA_CTO~DELL2
