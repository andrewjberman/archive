# Chunking-Lambda Architecture -- proposed canonical-readiness additions (DS draft)

**By:** 0.4.0_DS_ClientPlatform (doc author), 2026-07-15. **For:** CTO to fold into
`docs/architecture/chunking_lambda_architecture.md` (CTO's owned surface) whenever the canonical-ization
is sequenced -- NO rush, no front-running. **Grounded on:** 0.7.0's validation review
(`chunking_lambda_pattern_validation_20260715.md` @ c21c5b08f) + the delta-6 drain 0.7.0 built by hand
today + the reference primitive. These close the two gaps 0.7.0 flagged as blocking "estate standard"
status -- both squarely in Andrew's "particularly backfills" scope (now OPAL_CONSOLIDATION P0).

Ready-to-drop section text below; edit freely.

---

## [PROPOSED new section] Multi-partition backfill drain (Gap-A)

The rest of this doc makes ONE partition safe. A backfill is MANY partitions, and that is a DIFFERENT
bound: the per-partition envelope (memory + wall) is proven, but a single run that converts every missing
partition sequentially in one invocation multiplies the wall by N and blows the timeout. Measured: 58
orion units x ~91 s runtime = ~88 min >> the 600 s Lambda ceiling -> the invocation times out partway,
DLQs, and leaves a PARTIAL drain plus noise. **Do not drain inside one invocation.**

**THE PATTERN: per-partition event fan-out, sweep = reconciliation-only.**

1. **Discover the frontier (reconciliation):** list the missing partitions = `bronze-present MINUS
   silver-present` (listing-based, key+ETag -- never HeadObject-as-acceptance). This is the drain work-list.
2. **Fan out ONE invocation per partition.** Each invocation converts exactly ONE partition, staying
   inside the measured per-partition envelope. Dispatch via S3 event / SQS / a fan-out dispatcher --
   never a loop inside a single Lambda.
3. **Gate parallelism with RESERVED CONCURRENCY** (0.7.0 ran the delta-6 drain at concurrency-2). Bounds
   cost, vendor/throttle pressure, and downstream load; makes the backfill's wall
   `~ceil(N / concurrency) x per-partition-wall` SPREAD across invocations, not one giant invocation.
4. **Every invocation is IDEMPOTENT** -- the same `partition_exists` skip-if-landed the converter already
   has. Redeliveries, retries, and a re-run sweep are all safe (at-least-once dispatch, exactly-once effect).
5. **THE SWEEP IS RECONCILIATION-ONLY.** It re-lists the frontier and re-dispatches stragglers; it MUST
   NOT itself convert. A sweep that converts re-creates the single-invocation timeout -- the exact failure
   this pattern exists to avoid.

**Why it is safe:** the per-partition ATOMIC contract (each partition lands whole-or-nothing on finalize)
means fan-out + retries can never half-land or double-land a partition. Idempotent skip + atomic finalize
= a restartable, resumable drain; a failed unit re-dispatches without failing the batch. **The heaviest
unit is the runtime-confirm vehicle** -- drain it first (or standalone) to read true max-memory-used before
fanning out the tail (the delta-6 sequencing: heaviest landed as the confirm, 57 lighter units followed).

---

## [PROPOSED upgrade to Contract 2] ETag==MD5 is an ENFORCED PRECONDITION, not an assumption (Gap-B)

The doc states the single-part + non-KMS assumption. A canonical standard must ENFORCE it, because the
identity **breaks silently** otherwise:
- **KMS-encrypted target:** the ETag is NOT the MD5 of the object bytes -> the verify compares two
  unrelated values and can pass or fail meaninglessly.
- **Multipart upload** (output > the multipart threshold, ~5 GB, or a multipart client): the ETag is a
  hash-of-part-hashes with a `-N` suffix, NOT the whole-object MD5.

**Canonical precondition (gate at adoption, per target bucket):** before the primitive may verify by
ETag==MD5, assert the target's default encryption is AES256 (SSE-S3, non-KMS) AND the write is single-part.
If EITHER fails -> **deny** (route the write elsewhere) OR **fall back to read-back-compare** (stream the
stored object back and hash it at bounded memory). Never trust ETag==MD5 on a KMS or multipart target.
Make this a preflight check the primitive/deploy runs, not a footnote a reader must remember.

---

## [PROPOSED promotion to REQUIRED] Write-verify-failure companion invariant

`finalize()` raises AFTER the put, so a failed verify leaves an UNVERIFIED object at the key. This is sound
ONLY if the caller upholds all three -- make them REQUIRED wherever the primitive is used, not optional:
1. **Never mark a raised conversion as converted** (a `StreamWriteUnverified`/any raise = NOT done).
2. **Landing acceptance is LISTING-based** (key+ETag+Size), never the object's mere presence -- an
   unverified object IS present.
3. **Idempotent same-key reconvert overwrites** the untrusted object on the next run.
If a caller treats the raise as success, or accepts landing by presence, the untrusted object leaks to
served. (Belt: the partition is never signalled downstream while un-converted.)

---

## Refinements already in flight (noted, not re-proposed)
- **Wall variance:** runtime wall was ~1.9x the dev-host (delta-6: 47 s -> 91 s). CTO is folding this into
  Section 8 -- weight the ~400 s dev-host bar STRICTLY (a ~350 s dev-host family can blow 600 s in runtime).
- **/tmp (ephemeral_storage) sizing:** the Section-3 disk dimension (my earlier proposal) IS this -- a
  Rule-5 explicit-sizing item for any family whose finalized parquet approaches the 512 MB default.
- **Second-family proof:** n=1 today (orion). Schwab CRS on the SAME primitive (PartnerETL, post-0833) is
  the natural second family -- two validated is the honest "canonical" threshold (0.7.0's bar, agreed).
