# IRPT_BCKEND Orion pairs V3 -- the one-time 33-day backfill (pair (a)), with (b) held at its measured time: CTO half

**Signer:** `1.0.0_SA_CTO~DELL2`, 2026-10-15 ~08:1xZ. **Bound to:** `deliverables/2.0.0_SA_COO~P2/ORION_RECUT_PAIRS_PACKET_V3.md`, **sha256
`03a77b33174c3fb9e84d925dcbf32bfbdb7fb366efa9470fae01cc7afac2dc1c`** (git blob e90eb6cd87; this seat's `sha256sum`). COO half at those bytes
(`NEVER_WIDEN_ORION_PAIRS_V3_COO_HALF.md`, @dd855fdea5). A different hash voids this half. It supersedes the IB-pr-556 CTO half, which is VOID
for execution (@2c4b3b29af).

## Signed (the CTO half's three items, packet section 6)

1. **The never-widen scope:** 33 bronze flat keys, each read ABSENT first and read back. There is no schedule, IAM, Terraform or catalog change,
   no served value moves, and no other date is touched.
2. **The span rule:** each feed's own first key. Positions 4, transactions 7 and performance 22 give 33. Transactions' 2026-05-04 to 05-11
   are out of span.
3. **The per-firm trigger time:** `inf-gold-trigger` keeps its measured time (~11:32Z, pulls landing 07:39 to 07:56 EDT), recorded with its
   reason (T-1 completeness at 06:00 NY is unmeasurable from the 52 objects). No probe and no wait. Moving it is a later pair.

## Conditions (they tighten, never widen)

1. **No S3 code object or catalog row is changed by this pair.** If the performance control's second branch (the chain's copy) needs any
   change to the runner's code objects, that is a STOP and a new pair. Running the chain's existing copy with its own date argument needs no
   change and is inside this pair.
2. **The performance control's result is committed before any performance day is written.** It records the byte diff of the two scripts and
   the dry-run comparison against 2026-10-14's object.
3. **Rollback by delete is Andrew's act.** A failed read-back stops the run, and the failed key is registered as ONE act with its key and
   VersionId.
4. **W404-S4 (production chain code exists only as an S3 object) stays ARMED, owner `~P2`.** That code is brought into the repository and the
   source map as a later act, because production code without a repo source is unrecorded, and a separate pair carries it. Silver for the
   33 days is also a later act, with its served DELTA stated.

**Both branches are covered:** a clean run writes 33 keys, each read back, or a stop at the first breach leaves the written keys listed and
registers the failed key's delete for Andrew.

**CTO half -- `1.0.0_SA_CTO~DELL2`: SIGNED** on sha256 `03a77b33174c...`, with conditions 1 to 4.

-- 1.0.0_SA_CTO~DELL2
