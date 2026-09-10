# EG-s-28 RESULT -- the unresolved record names its provider

**TO:** `ETFS_GUARDRAIL.TO-EG-s-28` | **worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` |
**branch:** `wk-etfs_guardrail-2-1` | **base:** `32ae4ede66` (the issuance commit; grant resolves from HEAD)
| **outcome_ref:** FWD-10 | **cell:** `EG-s-28`

## THE CHANGE, IN ONE PARAGRAPH

`data/etfs/scripts/coverage/remediate.py` gains one accessor, `_provider_for(partner)`, which is the
single reader of `_PROVIDER_BY_PARTNER` and returns the same honest-absence string rung 3 has always
used (`<no provider mapped>`) for an unmapped partner. `remediate_month` resolves it ONCE beside the
producer and writes `"provider"` into **all four** `unresolved.append` sites -- the dry-run plan, the
no-invoke/no-producer case, the rung-1-raised case and the rung-2-no-slice case. `rung3_stop_and_ask`
now reads the same accessor, which is the same value it computed before, so the ask artifact a person
authorises egress on is byte-identical. Nothing in the ladder's behaviour moves: rungs 1-2 still never
write to S3, class B still stops without a re-run, and this cell deploys nothing.

## S28-AC1 -- PASSES BY OUTPUT

**invocation:** `timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs28_unresolved_names_its_provider.py`
**rc=0**, final line `EGS28-EVERY-UNRESOLVED-NAMES-ITS-PROVIDER`, `arms: 6 of 6 evaluated; assertions failed: 0`.
Full transcript: `EG-s-28_S28-AC1_battery_output.txt` beside this file.

- **(a) THE DEFECT REPRODUCES FIRST.** Pre-change bytes taken from `git show 32ae4ede66:data/etfs/scripts/coverage/remediate.py`
  and resolved BY CONTENT (15011 B, sha256 `25ff4dbed4af6545...`, matched against the pin the battery
  prints), never by ancestry. AST census over that source: **4** `unresolved.append` sites at lines
  240 / 248 / 261 / 272, each with keys `['date','class','reason']` -- **0 of 4 carry `provider`**. A
  ladder run on the pre-change module: **3 of 3** records LACK the field. The premise held, so the
  battery did not stop.
- **(b) EVERY SITE IS FIXED.** Same AST census on the changed file: **4 of 4** sites carry `provider`,
  denominator unchanged 4 -> 4 (no site was deleted to make the count read clean), each site named with
  the branch it serves. Three ladder runs covering every record-producing branch: 3 of 3, 3 of 3, 3 of 3
  records name `Black Diamond`, cottonwood's mapped vendor.
- **(c) AN UNKNOWN PROVIDER STILL READS AS UNKNOWN.** An unmapped partner yields exactly one distinct
  value over 3 records, `<no provider mapped>` -- not `None`, not the string `"None"`, and no mapped
  vendor name leaked onto it. POSITIVE control: it proves the honest-absence path can still fire.
- **(d) THE TERMINAL MESSAGE NOW NAMES A REAL PROVIDER -- the DIFFERENCE control.** The SAME dates and
  the SAME partner, built into `coverage_unresolved.json` shape before and after, both passed through the
  orchestrator's OWN `_normalize_unresolved` + `_build_terminal_email`
  (`lambda_function.py`, 47075 B, sha256 `8d8cb2c23d7c00d9...`, read-only, not edited):
  - BEFORE: `2026-08-04 | cottonwood | (not stated)` for **3 of 3** rows.
  - AFTER: `2026-08-04 | cottonwood | Black Diamond` for **3 of 3** rows; `(not stated)` appears
    nowhere in the message body.
  Engaged against the same input disengaged, which a positive control could not have shown.
- **(e) NOTHING ELSE MOVED, AND THE DEPLOY GAP IS MEASURED NOT CLOSED.**
  `python -m pytest data/etfs/scripts/coverage/tests/test_remediate.py -q` by its own path:
  BEFORE (pre-change code AND pre-change tests, rebuilt from `32ae4ede66`) **rc=0, 12 passed**;
  AFTER **rc=0, 16 passed** (+4, purely additive, nothing removed). Rung 3's ask is identical before and
  after (`generated_at` aside), and an unresolved record CARRYING the new field produces the same ask --
  no leak into the egress artifact. DEPLOYED `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/remediate.py`
  sha256 `3c3ce6c5cfcce654...` (11011 B, measured) **!=** BUILT sha256 `401bed2ace84d156...` (16550 B,
  measured) **!=** PRE-CHANGE `25ff4dbed4af6545...` -- the prefix was already behind this repo before
  this cell touched anything. Per `S33`/`S34`, an upload to that prefix does not reach the box (the
  renderer pulls the coverage package only inside an `except ImportError` branch and `/opt/etfs-reports/coverage/`
  persists on EBS), so this pair UNDERSTATES the gap to the running plane. This cell closes neither.
- **(f) NO SEND, NO INVOKE, NO EGRESS.** Four denominators from the run: 10 stubbed calls across 5 ladder
  runs, of which 0 put_object; 0 of 0 AWS attempts through the orchestrator's stubbed boto3 clients
  (`_build_terminal_email` BUILDS, `_send_terminal_unresolved` was never called); 0 hits for each of 5
  send/invoke/HTTP tokens in `remediate.py`; and **1** real AWS call in total, a read-only `GetObject`
  on our own artifact prefix for arm (e) -- 0 sends, 0 invokes, 0 writes, 0 vendor egress.

## PERMANENT COVERAGE (4 new arms in the estate's own suite)

`data/etfs/scripts/coverage/tests/test_remediate.py`, 12 -> 16 tests:
`test_egs28_every_append_site_writes_provider_denominator_from_source` (an AST fence on the PROPERTY, so
a FIFTH site added later that forgets the field FAILS the suite rather than shipping a mixed artifact),
`test_egs28_ladder_run_over_every_branch_names_the_provider`,
`test_egs28_unmapped_partner_reads_as_unknown_never_a_guess`,
`test_egs28_rung3_ask_record_shape_is_unchanged`. The neighbouring suites were run READ-ONLY for
invariance: `test_coverage_gate.py` + the orchestrator's three test modules + the coverage tests =
**64 passed**.

## ROW FILED

`ETFS_GUARDRAIL-W1-S33` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO`): the unresolved record has a
FIFTH writer outside this cell's grant -- `render_month_end.py:1000-1008` builds its own unresolved
records on the `--no-ladder` path, without `remediate.py` and without `provider`, so that path still
renders `(not stated)`; and `W4-S6`'s remedy (1) is to thread exactly that flag into the driven run.
Not repaired here: the renderer is `EG-s-26`'s live surface and out of this cell's bounds.

## BOUNDS OBSERVED

No renderer edit, no orchestrator edit, no ladder behaviour change, no deploy, no served key written,
no SES send, no Lambda invoke, no vendor egress.
