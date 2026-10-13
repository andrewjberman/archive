# FB-j-8 -- the slot pre-screen (0.7.0_AE_CloudOps~FB1, 2026-10-13T09:04:34Z)

**The empty first pass was NOT "no slot fired". Slots fire for every advisor; every fired slot is dropped on the model path.**

## The pre-screen (offline, no model call, no write)
- The generator's own `list_active_advisors()` returns 194 advisors; the served prefix holds 158 `exec_summary.json` (all 158 are inside the 194; 36 advisors
  have no served object and a regeneration would create them; 5 of the 194 have no `positions.json`).
- Over the 158 served-prefix ids, canonical home: `top_gainer` 157, `top_loser` 156, `concentration_risk` 124, `tax_loss_candidate` 156,
  `leaderboard_rank_delta` 0, `top_nna_mover` 80; advisors firing at least one slot: 158 of 158. The legacy home (frozen) gives IDENTICAL counts.
  Over all 194: 186, 185, 152, 170, 0, 87; any slot 189.
- `leaderboard_rank_delta` is 0 because `load_leaderboards` returns None for both the current and the prior week in both homes (the keys are absent):
  that slot cannot fire today for a data reason, not a gate.

## The control that makes it measured
- FB-j-6's invocation (10 advisors): the offline evaluators fire 42 slots for those ids; the generator's own metric `Opal/ExecSummary
  ExecSummarySlotDropped` read 42 in that invocation's window and nothing in the previous 14 days.
- This order's targeted invocation (10 other advisors, 39 fired slots offline): http 200, 10 artifacts, ZERO bullets, 7 s; the drop metric read 39. Served-prefix
  listing identical before and after (158 keys, sha256 d5d52e93...). So 81 of 81 fired slots were dropped in `_build_slot`, each in about 0.17 s.

## Where the drop happens, and what is not known
`_build_slot` wraps `_call_llm` and `validate_slot_response` in `except (..., Exception): metrics.emit_slot_dropped(); return None`, printing NOTHING, so the
function log holds only lifecycle lines. Measured preconditions: the function is not in a VPC; secret `anthropic-api-key` exists and the role allows
GetSecretValue on `anthropic-api-key-*`; layer `anthropic-sdk-deps:1` is python3.12-compatible with `anthropic` and `pydantic_core` (cpython-312) present. A failure
at about 0.17 s per call is consistent with an early HTTP error or an SDK error, not with 81 completed model calls. The exception class is NOT known and the order
forbids a model call from this seat.

## Not done, by the order
No evaluator, threshold, prompt or code file was changed; no non-dry invocation; no S3 write.

## The one-line next step (not applied)
Print the exception class and the first 200 characters of its text in `_build_slot`'s two `except` branches (the same form as FB-j-2), deploy under a pair, and
run one dry run. The record's own AC1 reads FAIL on purpose: the positive control failed.
