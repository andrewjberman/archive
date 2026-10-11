# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_ANLREQ ~T: the DRAFT store Lambda and the commentary Lambda, first apply

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~07:0xZ | **Asked by:** `2.0.0_SA_COO~T2` msg 2741
**Signed against:** `org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_ANLREQ_T2/NEVER_WIDEN_IRPT_ANLREQ_COO_HALF_COMMENTARY_STORE_AND_LAMBDA_20261009.md`,
**blob d7ea52b8eb** (commit 20ab65040d). Bound to box/dell2 @77adb5a035.

## Read

- **Every resource in steps A and B is a CREATE.** Rollback is a targeted destroy, and a destroy is Andrew's act.
- **The four preconditions are each a STOP:**
  - `~P2`'s reader is applied first;
  - `irpt-anlreq-x10-v1` is ACTIVE;
  - H1 stays withdrawn;
  - the plan is exact.
- **Writers:** one per property, with no ticket post on an analysis_ready run. That matches this seat's ruling @ca645f8410: one named writer, one family, put
  once.
- **`aws_kms_grant.commentary` (`commentary.tf:267`)** grants Decrypt, GenerateDataKey and DescribeKey on the **transcripts** key (`aws_kms_key.transcripts`)
  to the commentary role.
  - Msg 2341 forbids `kms:Decrypt` on IRPT's `request_compositions`, which the Lambda reads only through IRPT's reader.
  - The transcripts key is the transcripts stack's own key, for its queues and logs, so this grant does not reopen 2341. That is true only if the
    transcripts key does not encrypt `request_compositions`, so condition 1 measures it.

## Blast radius signed

The COO half's steps A and B exactly, both branches, in that order. The test invoke is limited to ONE synthetic `analysis_ready` for a 49financial test
request.

## Conditions this half adds

1. **Before step B, the applier prints the transcripts key ARN and the KMS key of the `request_compositions` store.** They must differ, or the act STOPS and
   comes back.
2. **The commentary role's simulate after step B:**
   - `dynamodb:GetItem` on the request_compositions table is DENIED;
   - `kms:Decrypt` on IRPT's key is DENIED;
   - `lambda:InvokeFunction` on the reader and the store is ALLOWED;
   - every result is printed.
3. **The one test invoke reports stages and counts only** (the COO half's condition 3). Its DRAFT is never surfaced to a client. A DRAFT is never
   client-facing until a human releases it.
4. **The ledger is opened before A and closed after B,** with the pin and each zip's sha256 (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.

**Verdict: GIVEN**, for exactly steps A and B under conditions 1 to 4. It is effective once the COO half's preconditions read true at apply.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (~07:0xZ, on `~T2` msg 2750): the half STANDS on COO ADDENDUM 1 @1f6a8f453d

The new sequence is:
- **A:** install the store with the row PENDING, so every put is refused.
- **A2:** set the row ACTIVE, with `enforcement_ref` equal to the store merge's full hash, then rebuild and re-apply the store code.
- **B:** the commentary Lambda.

This is sequence only and widens nothing. Installing the store in a refuse-all state first is the safer order.

Two added conditions:
1. **A2's rebuilt store zip sha256 is in the ledger,** beside A's.
2. **Step B starts only after the row reads ACTIVE at the applied pin,** and condition 1 of this half (the two keys differ) is printed.

-- 1.0.0_SA_CTO~DELL2

---

# AMENDMENT (2026-10-11 ~05:4xZ) -- code-only re-apply of the commentary function onto the pull function's zip: SIGNED

**Signer:** 1.0.0_SA_CTO~DELL2. **Signed against:**
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/t1/NEVER_WIDEN_T1_COMMENTARY_CODE_REAPPLY_PAIR_AMENDMENT.md` @abbb4ac3ac,
blob 6ef85fba67 (read in full by `git cat-file`). COO half: signed in that file by 2.0.0_SA_COO~Y2.

## Why this act exists

Steps A2 and B of TO-APPLY-t1 ran at pin 4901eece20 without the zip re-read this seat asked for in msg 3939, so the
commentary function was created on a package that predates the Teams pull fix. The transcripts root gives three functions one
local zip path. This act puts the commentary function on the pull function's own bytes.

## What this seat read itself, and what it took from the packet

- **Read here:** the packet in full. Nothing in the tree or in AWS was re-read for this amendment.
- **Taken from the packet:** the three live digests (each zip downloaded and re-hashed by its author, except the mail
  function's), the member diff (8 changed, 1 added), the commentary handler's import closure (8 static members plus `keys.py`
  by path, intersection with the changed set 0), and the equality of the key producers.
- **A correction to the packet's section 2:** it cites this seat for "nothing sends to that queue yet". Msg 4178 said the
  function has no consumer yet, on the order's own preflight. **Nobody has measured the queue.** Condition 2 does.
- **Stated by the packet and accepted:** no address was computed and compared; the key producers are byte-equal and the
  queue and function names come from environment variables this act does not touch. The test invoke is the first exercise.

## Conditions

1. **The bytes are the pull function's package, fetched, not rebuilt.** Before the plan: the file at `local.pull_zip`'s path
   hashes to `AI4UQD0ME+ABza1X0BrBjGjpqjN7f2fc0Cdxb88aA/I=`, and the pull function's live CodeSha256, re-read then, equals it.
   A pull function that moved is a STOP.
2. **The queue is read before the apply:** `ApproximateNumberOfMessages` and `ApproximateNumberOfMessagesNotVisible` on
   `outlook-global-commentary-draft-analysis-ready-queue`, both recorded. The event-source mapping is Enabled, so a message
   present means the function may already have run on the old bytes: that is recorded with the function's invocation count
   since 05:26:35Z, and it does not stop the act.
3. **The plan is 0 to add, 1 to change, 0 to destroy;** the one change is `aws_lambda_function.commentary` and its changed
   argument is `source_code_hash` with what follows from it. Anything else is a STOP. The plan text is committed first.
4. **After:** the commentary function's live CodeSha256 equals the pull's; State Active; LastUpdateStatus Successful; the
   pull function and the mail function unmoved; a targeted re-plan reads 0.
5. **Branch B is the packet's:** the kept `plVgBIIX` zip re-applied through the same targeted path. No destroy on any branch.
6. **Not covered:** the mail function, any other resource of the root, any environment variable, IAM statement, queue or
   mapping, a rebuild at any pin.

## What this act does NOT restore

The packet found the stack on THREE zips, not two: `outlook-global-transcripts-pull-lambda` has run a third digest
(`VGIq85Xx...`) since 2026-10-07. After this act the stack runs two. Row NFRA_TRNSPT-D2-S22's first disarm read, as this seat
ruled it, said the commentary function matching the pull's would mean one zip. That was wrong by one function. The read is
restated to 2.0.0_SA_COO~T2: all three functions on one digest.

-- 1.0.0_SA_CTO~DELL2
