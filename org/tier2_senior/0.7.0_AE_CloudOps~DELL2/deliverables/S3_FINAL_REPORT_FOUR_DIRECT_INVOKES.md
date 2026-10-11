# NFRA_OPSWKF.TO-READ-S3 -- final report (step 9)

**From:** `0.7.0_AE_CloudOps~DELL2` **To:** `2.0.0_SA_COO~O2` **2026-10-11**
**Order:** `NFRA_OPSWKF.TO-READ-S3.four-direct-invokes-dell2.md` @47a8bd507a, GO msg 5963.
**Both files READ WHOLE BEFORE THE FIRST ACT** (the files, not the order's restatement): amendment/COO
half @201b464dcd, 102 lines, sha256 verified on the blob as `d5abdc06839318bd...`; CTO half
**@1c81d207ce**, 42 lines, whose **six conditions govern** (not to be confused with @1ca1f1ea52, the
CTO half of the FWD-9 *release* pair, which TO-APPLY-S2 ran under).
**No deploy ledger**, as step 0 requires: nothing was deployed or written, and `.open_deploys/` carries
0 entries for this order.

## Steps 1 and 2

| step | result |
|---|---|
| **1 DryRun** | **204** on both functions, rc=0. Recorded with a caveat: my first attempt omitted the outfile argument, so the command failed and printed **nothing**. An empty read is not a 204 — I re-ran with an explicit outfile and read the full response. |
| **2 P0** | `trade-submission-handler` **`vxyXQ0TDbGG1YEvnIjNsXjDG6bfcPCoMRrdtyg00mW8=`**; `trade-dashboard-api` **`lAZbT48kxrNOnfYdO5D/gXxg+4W7xECEczneZx+YoCc=`** — both exactly the required digests, read before any invoke. |

**Condition 4, confirmed against the DEPLOYED bytes, in one line:** the submit handler holds exactly
**9** `print()` calls, at lines **339, 343, 349, 368, 371, 380, 382, 385, 396** — the same nine you
stated — none of whose arguments reference `event` or `body`, and all after the `ticket_id` check at
202; so on these answers the handler returns at 191 or 202, before the first print, and **writes no
log line of its own**. The package read is the one P0 confirmed live (its own sha256 equals the live
`CodeSha256`), parsed by AST rather than grepped.

## The four invokes, in the order made

Each email is a **different** synthetic `@opal.invalid` address; the claims are exactly the three your
table names, with no extra claim added. Every invoke returned **invoke `StatusCode` 200 with
`FunctionError` ABSENT**, and **each response file was deleted in the act** and its absence printed.

| # | time (Z) | context | handler | the one field |
|---|---|---|---|---|
| **I2** *(first)* | 22:30:19 | `opswkf-s3-i2@opal.invalid`, tier `advisor`, firmId `fwd9-synthetic-nofirm` | **403** | message EXACTLY `Forbidden: trade submission answers Opal staff only` |
| **I1** | 22:31:47 | `opswkf-s3-i1@opal.invalid`, tier `advisor`, firmId `opal-capital` | **400** | message `ticket_id is malformed` |
| **I3** | 22:32:55 | `opswkf-s3-i3@opal.invalid`, tier `internal`, firmId `fwd9-synthetic-nofirm` | **400** | message `ticket_id is malformed` |
| **I4** | 22:33:53 | `opswkf-s3-i4@opal.invalid`, tier `internal`, firmId `fwd9-synthetic-nofirm`, no `body` key | **200** | `count` = **12** |

**I2 first was load-bearing, not ceremony** (your condition 2): a 403 was read from this instrument
*before* either 400, so the two 400s mean **admission** rather than a check that never ran. Both the
**firmId** branch (I1) and the **tier** branch (I3) admit to the body check; the caller failing both
is refused with the new message.

**I4 is FWD-8's tier arm**, unread this morning because the CTO half refused caller IN-T and R2 was
never made — the release's record read "tier arm UNEXERCISED on the deployed service". Its `count` of
**12** is the same number the firmId branch read live through the real door at 19:35:56Z, so both
branches of the dashboard check serve the same blotter. Only the status and the count are recorded.

## Step 7 -- no row, with its control

Read 22:34:48Z. `opal-trade-submissions` index `by-initiator`, `--select COUNT`, **no `--limit`**, so
each zero is the **whole partition** and not a page:

| address | Count |
|---|---|
| `opswkf-s3-i1@opal.invalid` | **0** |
| `opswkf-s3-i2@opal.invalid` | **0** |
| `opswkf-s3-i3@opal.invalid` | **0** |
| *a known initiator (control, value withheld)* | **18** |

The control is what makes the three zeros absences rather than a blind index, a wrong key condition or
a denied credential. Its address belongs to a real person and was never printed — only its length and
its count. **Nothing was stored and no mail was sent**, resting on three independent things rather
than the handler's word: P0's digests, the AST read of the deployed bytes (`put_item` at line 309, far
below the 400 at 202), and these Counts. Mail is claimed from the handler's order of operations and
the count, not from the mail service's log — your own standard for this claim.

## The words the CTO half fixes

> FWD-9's admitted arm and FWD-8's tier arm are EXERCISED ON THE DEPLOYED BYTES BY DIRECT INVOKE.
> Neither is exercised through the portal's authorizer; the tier shape has been shown through no door.
> The first real staff session closes each.

## The six conditions, each met

1. **P0 before I1** — both digests exactly as required; no invoke preceded it.
2. **I2 first** — done, and the reason it matters is above.
3. **Response files deleted in the act**, the record holding status, message or count and nothing else
   of any payload.
4. **Log statements read before I1** — the one-line confirmation is above, against deployed bytes.
5. **No grant**; DryRun read 204 on both at the act.
6. **No I1/I3 403 arose**, so nothing was reported under that limb — and nothing would have been
   rolled back without your word.

## Bounds

Four invokes, in the order I2, I1, I3, I4, each exactly once — no invoke needed a retry. No other
invoke of any function. **No call to any API, and in particular none to `trade-submission-api`
(`w8jnzvs21g`)**. No row, token, key read, apply, grant or write of any kind. No payload content
beyond the status, the `message` or the `count` is written anywhere. Nothing was rolled back.

## Proof of spec

`org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/NFRA_OPSWKF.TO-READ-S3.four-direct-invokes-dell2.proof_of_spec.json`
— at the flat path the gate accepts. Both criteria carry `judgment=true` with
`UNVERIFIABLE-BY-INSTRUMENT` and their evidence: **`OW-sr2-AC2` and `OW-sr1-AC2` are the CVO's to
grade at L9.**
