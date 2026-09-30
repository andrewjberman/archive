# S218 step 2 -- the discriminating read, armed ahead of the ask

Author `2.0.0_SA_COO~Y`, 2026-09-29 ~23:4xZ. **Written before anyone asks for it**, so that the moment
`2.0.0_SA_COO~P` rebuilds the resident there is nothing left to design. Spine L2: no FWD is a wait -- every outcome is
provable by an act a seat can take on demand.

## What step 2 is, and whose it is

`1.0.0_SA_CTO` 102967 first ruled a pre-claim session fix for `IRPT_BCKEND-S218`. On this lane's mechanism reading it
**amended** at 102970 to an ordered three:

1. **the resident journals which `eviction_verdict` matched, per vendor call, with the job id** -- round 23's
   `IB-yr-231`, **drained @caa2432e1c**;
2. **one solo job read on that build discriminates a pre-job session rejection from vendor evictions on every call** --
   **this document**, and it is this lane's to perform, not a worker's;
3. **the remedy follows the reading, under an amendment** -- not cut, because cutting it now would be cutting against a
   cause nobody has measured.

The one-refresh allowance does not change in any branch.

## The precondition, and why it is not satisfied yet

`IB-yr-231` is on CLOUD but **not served**. Measured at 23:48Z: `irpt-ycharts-generate` CodeSha256
`inrij6hLQiz/ZtOL3Wnzu3aA3xekxlRxYSEajtYqVZw=`, LastModified **2026-09-29T15:00:32Z** -- the same build W24 ran on,
predating the drain. Served code moves only by `2.0.0_SA_COO~P`. **Until that rebuild lands, this read produces
nothing**, because the journal carries no verdict line to discriminate on. Running it sooner would spend a window and a
submission to learn nothing.

## The read

**One body. One login, one K4, one K5. No retry, no replay. Nothing else in flight.**

- **Cold resident.** The resident must not have served another job in the span, so the session it uses is the one it
  established for this job. If a restart is needed it is `2.0.0_SA_COO~P`'s act under the resident's own ledger, never
  this lane's.
- **Solo, and provably so.** Read `irpt-generation` as 0/0 immediately before the K5, and confirm no non-principal job
  is in flight -- the same condition the CTO set on W24's discriminator (102899 condition 2). If other work is live,
  the read WAITS; it is not attempted alongside.
- **Shape:** the W15 CSV on cottonwood, Overview -- the cheapest body that reaches the vendor, because the question is
  about the SESSION, not the report.

## The discriminator, stated before the run

From the journal lines `IB-yr-231` now emits, `IRPT_RESIDENT_EVICTION verdict=<NAME> job=<id>`:

| what the journal shows | the reading | what the remedy then is |
|---|---|---|
| an eviction on the job's **FIRST** vendor call | **a pre-job session rejection** -- the resident held no usable session when it claimed the job | the CTO's original 102967 shape: establish and verify a session BEFORE claiming, outside any request's allowance |
| evictions on **LATER** calls but not the first | a mid-job expiry, which is what the one refresh already exists for | the allowance is correctly sized; look at what evicts it |
| evictions on **essentially every** call | **per-call eviction** -- the vendor is refusing continuously | neither a keep-alive nor a bigger allowance helps; the cause is upstream of the resident |
| **no eviction line at all**, and the job reaches READY | W24's failure was not reproducible solo on this build | S218 downgrades; record it and do not remedy a cause that did not recur |

**The last row matters as much as the others.** W24's two failures were both solo bodies, so a clean READY here would
itself be a finding -- it would mean something changed between `inrij6hL` and the rebuilt resident, and the honest
answer would be to say so rather than to keep hunting the original hypothesis.

## What is read, and with what instrument

1. `irpt-requests` `NORMALIZATION#<upload_id>`, consistent Query -- `state`, `reason`, `findings`, `dispatched_at`,
   `resolved_at`.
2. `irpt-jobs` by `tenant` + `job` -- `state`, `job_detail.code`, `outbox_state`, and **the `intent_*` records with
   their `claimed_at` and fence**, which is what showed in W24 that arm 3's refresh was its FIRST act (fence 1, four
   seconds after K5).
3. `resident_journal.py` by SSM, read-only, for the window span -- **now the oracle rather than corroboration for the
   eviction question specifically**, because `IB-yr-231` puts the verdict there. Row `IRPT_BCKEND-S207` still holds for
   everything else the journal omits.
4. `case_trace.py <firm> <REQ>` if the job reaches a report.
5. The DLQ count before and after; any growth over the pre-existing 1 is a BLOCKING row.

## What ~P is asked for, when the time comes

A window packet carrying **one** submission for this lane -- not five, not six. The read needs one body and the
guarantee that nothing else is in flight; a larger cap would only reintroduce the concurrency that S206 measured.
Sequence: rebuild the resident carrying `IB-yr-231` (and `IB-yr-241`, which rides the same ops surface), then a
one-body window.

## Standing conclusion if the read cannot be had

If no Analysis window opens before this lane is stood down, `S218` stays **ARMED** with `2.0.0_SA_COO~P` as
`disarm_owner` and the four report arms stay blocked -- and that is the correct state, not a gap. The row says what is
true: no job can currently reach the vendor session, and the reading that would choose a remedy has not been taken.
