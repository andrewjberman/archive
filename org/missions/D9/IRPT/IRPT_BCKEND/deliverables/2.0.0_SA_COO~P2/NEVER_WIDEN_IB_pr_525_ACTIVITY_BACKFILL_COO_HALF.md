# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-525 irpt-49f-reporting-gold-lambda (Design B: the stage-selection code release of IB-pr-523 and the chunked activity-and-lots backfill runs): SIGNED AT PACKET sha256 f6dd828322d4...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-14 ~02:2xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-525` (merged @368dd470e4) | **Applier (later orders, not this half's act):** the code release by `0.7.0_AE_CloudOps~IB2`; the chunked runs by the operator identity the CTO half names.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat releases or runs before the CTO half is signed at the same bytes AND the conditions below hold at that act.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~372/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-525.md`, sha256 `f6dd828322d4e17e4d7eb9838a2c0f8439515c5c787d986794b555e20dff68a3` (13,023 bytes; last commit `db437c7f61`). A half signed over different bytes is void.
- **Live and built:** CURRENT live CodeSha256 `J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg=` (hex `27a33ff7...`, LastModified 2026-10-13T12:39:43Z), which I re-read at ~02:2xZ: unchanged. Built CodeSha256 `BYe52LrfcJxuD22UKvDEgSG0SlldOp2H/fGLzS7jbfE=` (hex `0587b9d8...`, built twice byte-identical). **One changed member of 19:** `handler.py` (the IB-pr-523 change, +37 and -2 lines), equal to the repo blob at the pin; 0 signature and 0 attribute mismatches on either zip; the source map is untouched.
- **The served change:** a backfill event may select its stages. `"stages": ["lots"]` writes the activity partitions, the two lot partitions and a status object under the activity prefix for the range's days, and never computes or writes the returns or class partitions. A default event, and the scheduled path, behave as today; any other `stages` value is refused by name before any call. I re-ran the four arms' source (IB187-1, on the repo file) at the merge and read the packet's four arms on the BUILT bytes.
- **The proof the pair carries:** 0 returns partitions changed, by hash. The baseline (569 returns partitions, 4 activity partitions, listing digest `8c0afcb7...` over the sorted key and ETag lines of the returns prefix, read 2026-10-13) is re-taken after EVERY chunk and must be byte-equal.
- **Not widened:** no route, IAM, schedule or permission change; the function's role has no delete; versioning is Enabled (carried from the round-186 census, not re-measured here).

## What I checked myself before signing

- The three criteria of IB188-1 re-run on the merged tree: PASS. I read the packet in full, re-hashed it, and re-read the live CodeSha256. Before this round I read the diff of `handler.py` against its base blob (IB-pr-523) and the census it builds on (round 186).
- I did NOT re-run the build, the signature instrument, the arms on the built bytes or the baseline listing myself; they are the worker's, shown by the packet's hashes and by the check. The packet does not re-measure the bucket's versioning or the role's write set.

## Conditions of the code release and of the runs (the CTO half signs the same)

1. **Gate on the held ledger:** the trunk ledger `irpt-dashbd-thresholds-swap-20261013` (D2's; HELD at leg L7, awaiting the read of the 2026-10-14T11:41Z scheduled fire) must read CLOSED or SUPERSEDED before the code release opens its own ledger; the live function already runs that deploy's bytes (`J6M/...`). Neither act runs inside the 11:41Z fire window. Stale OPEN copies of its marker on other worktrees are named, never closed by the seat (NEVER-2).
2. **Digest gate and the release:** rebuild to `BYe52Lrf...`, any difference ABORTS; the Terraform path moves `s3_object_version` and `source_code_hash` only; plan 1 change, 0 destroy; `bash .tools/safe-apply.sh`; the Branch B S3 version `UcKN2ttQ...` re-named and re-read BEFORE any upload; the live CodeSha256 equal to `J6M/...` at the start read (any other value: STOP and re-census).
3. **Chunking is smaller than the packet's ceiling:** the packet derives about 4 days a chunk and leaves about 33 seconds of the 900-second timeout. **I sign no chunk above 2 trading days until a ONE-day lots-only real run has been timed; the first real run is ONE day (after its dry run); if a run takes more than 600 seconds, the next chunk is halved; any LOTS_SKIPPED, refusal, timeout or a changed returns digest STOPS the series.** A timeout mid-chunk can leave days half-written.
4. **Each run is a dry run FIRST** (`"dry_run": true` with the same stages), and the real run only when it is clean.
5. **The activity stage is not idempotent** (6,901 against 6,904 rows for one day): no landed day is re-run except by an explicit decision; the plan covers 2024-07-08 to 2026-10-06 oldest-first and stops before the four existing partitions.
6. **Branch B** as the packet states: the code release by the S3 version; new activity and lot objects removable only by an operator DELETE (Andrew's word); rewritten objects by version id, by an operator identity; what cannot be undone is stated. **Ledger** (NEVER-2) opened before the first write and closed at completion.
7. **The purpose gate, for the CTO half to weigh (not a safety condition of mine):** the census found NO reader of `account_activity_daily` anywhere in the repository (row D2-W372-S1). Filling 565 days of a table nothing reads moves no figure a person sees. The first real run should wait for the CTO's confirmation of which reader (the default report's, FWD-21's) will serve those figures.
8. **The after-read is a person's** (the default report shows contributions, withdrawals and income for a window longer than 4 days, on DEV); no seat can sign in.

Signed: `2.0.0_SA_COO~P2` at 2026-10-14T02:2xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
