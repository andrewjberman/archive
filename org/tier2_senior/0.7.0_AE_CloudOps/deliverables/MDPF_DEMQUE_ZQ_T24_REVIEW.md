# TO-DQ-t24 -- preflight refusal after prerequisite cleared

**Seat:** 0.7.0_AE_CloudOps~ZQ. **State:** t22 prerequisite passed; pending issuer amendment for warning/stop interfaces.
**archetype:** VALIDATE

## Current finding -- Oct9 approximately10:48 Eastern

Read exact resume dispatch 20261009T144505Z from COO~Q1. Re-ran dq_t22_quote.py on this tree:
Friday allowance0; Saturday allowance5858; finish2026-10-17; NTDQ-OK. The earlier dependency hold is discharged.
Read READ_HERE.md, round6 R1, the request, quote/actuals implementation, the existing historical client, and the two acceptance scripts.

TO-DQ-t24 requires stopping at the first vendor limit warning/refusal AND recording the stop through `bbg_quote.py --record`.
The current dependency interfaces do not supply that behavior:

1. `integrations/bloomberg/mcp/blp_client.py:historical_data` supports `on_response_error="raise"` for request-level rejection,
   but ignores `securityData.fieldExceptions` and does not expose a warning/event callback. A successful returned row can conceal
   that diagnostic. The required backfill cannot rely on its public returned data to determine that no warning occurred.
2. `data/mdpf/scripts/demque/bbg_quote.py:record_actual` unconditionally sets outcome DRAWN. Neither that function nor the CLI has
   a stop/outcome argument. Invoking the exact mandated CLI cannot append a line naming a stopped run's outcome. Relabeling a
   refusal DRAWN, rewriting the shared ledger afterward, or silently replacing the specified recorder is not the ordered contract.

Both dependency files are outside the write grant. Refusal clause applied: no implementation or one-shot registration, no vendor
draw, no auth action, no production actuals write. BLOCKING row MDPF_DEMQUE-Z-W1-S4 records the issue. The order remains pending.
Requested amendment: grant/assign an opt-in diagnostic surface on the existing historical client and an outcome/stop argument on
the quote recorder, preserving other callers; alternatively specify an approved stop-aware adapter/recording interface within grant.
This is an interface/grant issue, not a claim that every possible adapter design is impossible.

### Offline discrimination (no Bloomberg import/session or network)

`.scratch/t24-interface-probe.py` injected a stub blpapi module and stub session/message objects into the real historical client.
It supplied one returned row together with fieldExceptions carrying a limit diagnostic. It then supplied a request-level
responseError as a positive control. A temporary actuals file exercised the real recorder and was removed afterward:

```text
WARNING-NOT-SURFACED: fieldExceptions supplied; one row returned, no warning in result
POSITIVE-CONTROL responseError raised: LIMIT: request refused
RECORDER-ZERO-OUTCOME: DRAWN
RECORDER-STOP-UNSUPPORTED: record_actual() got an unexpected keyword argument 'outcome'
No vendor calls or production ledger writes; temporary actuals removed.
```

Probe rc0 means those assertions held, not that the production stop condition passed. `bbg_quote.py --help` confirms no outcome
argument. This synthetic probe establishes interface behavior; it is not evidence that Bloomberg issued a live warning today.
AC1/AC2 are not claimed passed. No CTO deployment-half request was made for an unreviewable implementation.

Compiler tools: known-path comp-which reads succeeded; the broader historical_data routing search timed out at90s, so the known
client file was read directly. Latest measured origin box/sitez e0444506857e2a9b05328d610eb4698ba2cc097e. Push state LOCAL; no push.

## Earlier prerequisite hold (resolved by the check above)

Read the exact COO~Q1 dispatch 20261009T140141Z / XB-20261009T133033Z-7a23 and its referenced task order.
Requested act: build the budgeted history backfill, then perform exactly one Bloomberg draw on Saturday Oct10 inside its quoted
allowance, with CTO~Z site-Z signature. The order explicitly says to start only after the t22 commit is in this tree and
`dq_t22_quote.py` returns NTDQ-OK.

At Oct9 approximately10:02 Eastern, ran:

```text
python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_DEMQUE_Q1/R7_CHECKS/dq_t22_quote.py
NTDQ-BAD rc=2 usage: bbg_quote.py [-h] [--quote FILE] [--record LEDGER] [--request FILE]
                    [--drawer DRAWER] [--cells CELLS] [--no-quote]
bbg_quote.py: error: unrecognized arguments: --today 2026-10-09
```

This proves the required local quote interface is not yet available; it does not establish the upstream task's status.
An attempted read of an inferred t22 order filename found no file and provides no status evidence. No substitute order was read.
The dependency hold is the order's explicit sequencing condition, not a new criterion or a refusal of the requested implementation.
Resume after the local prerequisite prints NTDQ-OK. No implementation, Bloomberg call, task registration, auth change, or AWS write
was performed. No timer was armed. The task remains pending; AC1 and AC2 have not been exercised for completion.

COO was ACKed and notified of the measured prerequisite failure. Compiler tools: comp-which routed the exact dispatch/order/check
paths to known-path reads; comp-to binds t24 to this session. Publication state LOCAL; this seat does not push.
Measured origin box/sitez: 3fe0b629e5368a463b5c9dddec40d70140f370cf.
