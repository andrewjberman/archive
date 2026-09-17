# BATCH B COMBINED SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~27

Continuation of chain B under a CHANGED PROCEDURE (Andrew's word, relayed by 2.0.0_SA_COO~Z):
build and locally verify all five remaining chain-B cells this session, for ONE combined
CTO+COO never-widen co-sign and ONE combined deploy in a LATER continuation. No live act of
any kind this session: no ledger entry opened, no `terraform plan`/`apply`, no
`.tools/safe-apply.sh`, no Lambda redeploy, no real DynamoDB write, no real republish.

## Order applied (per the dispatch's own sequencing, since four cells edit one region)

1. **AMGT-rk-23** (isolated, different function) -- path-safe artifact names.
2. **AMGT-rk-24 adapter half** -- no-CIK/filings-store reason merge inside the drafting-merge region.
3. **AMGT-rk-25** -- `as_of_date` line in the same region, composing on top of rk-24.
4. **AMGT-rk-30 adapter half** -- `bundle["scores"]` after the posture line, applied last.
5. **AMGT-rk-20** -- different file entirely (`price_axis_pull.py` + `backfill_legacy_generation.py`), done in parallel with the above.

## Files touched

- `lib/research/print/render_pack.py` -- `security_key()` now also replaces `/` -> `-`.
- `lib/research/api/scoped_amgt.py` -- four edits: rk-23's local-only path-safe filename in
  `_read_drafting_document()`; rk-24's `FILINGS_PREFIX`/`_read_filing_source_object()` plus the
  merge in `read_thesis_bundle()`; rk-25's `as_of_date` line; rk-30's `SCORES_PREFIX`/
  `read_scores()` plus `bundle["scores"]`.
- `integrations/bloomberg/research/price_axis_pull.py` -- `main()` now routes through
  `lib.research.price.generation.compute_price_axis()`; `build_movement_rows()` itself is
  UNCHANGED (still required by `movement_gate.py`'s producer axis registry + its own test).
- `lib/research/price/backfill_legacy_generation.py` -- new `read_crossed_partition()`,
  `_attach_identity()`, `republish_crossed_generation()`, and a `--republish-crossed` CLI flag.
- `org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md` --
  two rows appended (S7, S8).

## Verification run this session (all local; no vendor call, no AWS write)

- `python -m py_compile` on every changed file: clean.
- `python -m ruff check --target-version py39` on every changed file: clean (fixed one
  unused-import and one unused-exception-binding it caught).
- `python -m pytest lib/research/ -q`: **490 passed**, including
  `lib/research/metrics/tests/test_producer_axis_registry.py` (which calls
  `price_axis_pull.build_movement_rows()` directly) and `lib/research/price/tests/` (28 tests,
  unaffected by the new `backfill_legacy_generation.py` additions).
- Per-cell constructed-input unit tests (monkeypatched pool clients / fake DynamoDB resources,
  no real S3 or DynamoDB reached) are transcribed in each cell's own
  `*.proof_of_spec.json` `acceptance[].output_evidence`.

## What is NOT done, by design

Every AC that names a live Lambda invoke or a live DynamoDB/S3 read against the DEPLOYED plane
is `UNCOMPUTABLE-BY-CONSTRUCTION` in this session's proof-of-spec instances -- the deployed
`opal-amgt-scoped-api` and the live metrics table are both untouched by this session, so running
those literal invocations now would report the PRE-FIX state, not evidence this session's code.
None of the five orders' `<status>` is flipped to `complete`.

## Next act (not this session's)

2.0.0_SA_COO~Z brings this combined diff to 1.0.0_SA_CTO~Z for ONE combined never-widen
co-sign covering all five acts' blast radius and per-key rollback; the actual deploy(s) and
`run_scores.py`/`price_axis_pull.py` producer runs happen in that later continuation, which
also re-runs every AC above against the live plane and flips `<status>` per order.
