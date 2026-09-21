# MDPF_TAXSMA.TO-TX-a-2 -- result record

**Worker** `0.9.0_WK_MDPF_TAXSMA~2` · **cell** `TX-a-2` (decomp s.3, S07, FWD-5/6) · **branch**
`wk-mdpf_taxsma-1-2g` in `C:/tmp/wk-taxsma-2c` · **cut base** `fb5f7d6038` (the COO's working branch CLOUD at
spawn, per the identity line; `TX-a-1`'s Tax overlay in `dim_mdpf_aggregate_aua_timeseries.py` is drained and
present at this HEAD, git log confirms `aaee218e2a build(...TX-a-1...)` / `fb5f7d6038 drain(...TX-a-1...)`).
**Spec:** `org/missions/D8/MDPF/MDPF_TAXSMA/decompositions/MDPF_TAXSMA_DECOMP.md`@7f65001ab3 (s.3 TX-a-2, s.6
gates, s.8 bounds) and `org/standards/MDPF_TAXSMA_DATA_CONTRACT.json` v0.5.0 -- `operations`, `capability`,
`categories`, `artifacts`, `status_axes` -- whose enumerations are the only vocabulary used. **Input:** the
five engines TX-b-1/TX-b-2/TX-m-1/TX-m-2/TX-m-4 already built (`taxsma_snapshot.py`, `data/mdpf/scripts/silver/
taxsma_workbook.py`, `taxsma_membership.py`, `taxsma_reconcile.py`, `taxsma_assets.py`, all present at this
HEAD), and TX-a-1's own overlay functions (`dim_mdpf_aggregate_aua_timeseries.tax_additive_overlay` /
`apply_tax_to_global`), imported directly and never re-typed.

Every value below names its instrument, the UTC time it was measured, and its denominator.

## 1. What was built

This cell **edits an existing production Gold handler** (`data/mdpf/scripts/gold/mdpf_gold_consolidator.py`)
by ADDING one new section ("TX-a-2 (S07): THE TAX PRELUDE") plus one minimal, cited guard inside the existing
`_shape_category_views` by_model loop (the AC3/AC4 null-leaf fix -- a real defect Tax's arrival as a live SMA
member exposes; see s.3 below). No other existing line was refactored (checked by reading every hunk of
`git diff` before staging).

| Path | What | Instrument / evidence |
|---|---|---|
| `data/mdpf/scripts/gold/mdpf_gold_consolidator.py` (edited) | New imports (`taxsma_snapshot`, `taxsma_membership`, `taxsma_reconcile`, `taxsma_assets`, `taxsma_workbook` aliased `taxsma_silver`, `expected_last_trading_day`, `lib.opal_naming.address` aliased `taxsma_address`). New functions: `taxsma_capability_configured`, `taxsma_operational_control_key`/`_document`, `taxsma_category_gold_key`, `taxsma_coverage_fields`, `taxsma_apply_node_status`, `_firm49_base_excluding_tax`, `run_taxsma_prelude` (the S02->S19->S03->S04->S05 sequencer/gate), `apply_taxsma_overlay`, `write_taxsma_category_gold`. Wired into `build_all()`: the prelude runs isolated (A5) right after the L4-dims block and before the canonical-shaping block; `apply_taxsma_overlay` is the one call site that may change `arts["49financial"]`/`arts["global"]`; `taxsma_apply_node_status` + `write_taxsma_category_gold` run right after `shaped_cv` is fully built, before R1 completeness. Also: a 15-line guard added to the existing by_model loop in `_shape_category_views` (AC3/AC4). | `git diff --stat`, `py_compile`, `ruff check` (0 findings) |
| `data/mdpf/tests/taxsma/test_taxsma_consolidator.py` (new) | 21 tests across 9 classes, one class group per AC (AC3/AC4 share one regression class); synthetic Gateway envelopes, `LocalBronzeStore`/`LocalSilverStore`/`LocalDispositionStore`, a hand-built fake S3 double for the write test -- no real Gateway/S3/Graph/SharePoint/b00/0833/0824 call anywhere | `py -3.12 -m pytest data/mdpf/tests/taxsma/test_taxsma_consolidator.py -q`: `21 passed in 8.9s`, 2026-09-21T09:1xZ |
| `org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_2.py` (new) | the criterion probe: AC1..AC11 each run a `-k`-selected pytest subset in a fresh subprocess (vacuous pass refused); AC12 runs the WHOLE `data/mdpf/scripts/gold/tests` suite and checks the FAILING-ID SET against the 3 known pre-existing ids exactly (never a bare count, which a fix+new-break pair could hide) | 12 of 12 `AC1`..`AC12` invocations, s.4 below |

## 2. Design decisions this cell makes that the contract does not fix (declared, not hidden -- Rule 24(i)/(iii))

- **`taxsma_capability_configured()`** reads TWO new env vars this cell names itself (`TAXSMA_GATEWAY_BASE_URL`,
  `TAXSMA_CAPABILITY_BEARER`) -- the Gold Lambda's OWN copy of the base URL + bearer needed to call S02 live.
  This is deliberately NOT the Gateway's own `TAXSMA_WORKBOOK_BEARER`/`TAXSMA_WORKBOOK_IDENTITY`
  (`infra/aws/ec2/opal-gateway/app/config.py`, TX-g-1's), which validate the CALLER's presented bearer
  server-side -- a different config, on a different host, for a different question. Neither contract nor
  decomp names the Gold-side config key, and no TO grants me `TFM`/`TFA` to mint the Terraform variable that
  would populate it (that is TX-r-3's activation, held on G-A/G-W/G-P) -- so today, absent both env vars, the
  prelude is DISABLED by construction (AC11), matching TX-r-1's own plan ("an ad-hoc QA invocation ... records
  run_result DISABLED for Tax while the other firms complete").
- **`taxsma_coverage_fields`'s `freshness` derivation** (AUTH_REQUIRED / SOURCE_UNAVAILABLE / STALE / CURRENT)
  is this cell's own rule over the coverage entry's `reason_codes` and `value_status` -- the contract names the
  `freshness` enum but not a derivation function; declared here rather than left implicit.
- **`taxsma_apply_node_status` propagates only the 3 AC8-named reason codes** to the "SMA > ALT Strategies" and
  "SMA" nodes' own `reason_codes` list; the full `categories.wire_status_fields` bundle (AC7) attaches to the
  Tax MEMBER entry itself. The contract's `wire_status_fields` is one bundle; deciding which nodes carry the
  full bundle versus a propagated subset is this cell's own act, not fixed by the contract.
- **`write_taxsma_category_gold`'s schema** (one row: `firm_id`, `as_of`, `knowledge_date`, a JSON `payload`
  column) is this cell's own -- the contract's `artifacts.firm_category`/`global_category` name the CONTENT
  ("CANON category Gold with status extension") and the KEY (via `address()`), not a columnar schema (unlike
  `taxsma_assets.HISTORY_FIELDS`, which the contract does fix exactly).
- **The AC3/AC4 by_model null-leaf guard** treats an unknown/stale Tax leaf identically to any other member
  that might one day go null: OMITTED from `models_aum`/`sma_aum`/`member_aum`, never zero-filled, never
  crashing the loop. This is the SAME incident class `test_category_views_null_tail_guard.py` already pins one
  layer up (the scope-level `total`/`non_model` null guard); Tax's arrival as a LIVE, source-fed SMA member
  makes the by_model-loop version of that bug reachable for the first time, since every prior by_model member
  was either always-present or a Models member whose null-tail behavior nobody had exercised. This is a
  DEFECT-CLASS fix inside a function already granted to me (`GOLD/mdpf_gold_consolidator.py`), not a widening.

## 3. Real defect found and fixed (not a new surprise row -- squarely inside this cell's own AC3/AC4)

Before this cell's edit, `_shape_category_views`'s by_model loop did `sma_aum += value` (and the models/additive/
carve-out equivalents) UNCONDITIONALLY on `value = _last((entry or {}).get("model_value"))`. Since `_last()`
already returns `None` for a member whose latest slot is null (the exact shape the 2026-09-11 incident measured
for the FIRM-level `total`/`non_model` guard, `test_category_views_null_tail_guard.py`), a Tax leaf one day
behind would raise `TypeError: unsupported operand type(s) for +=: 'float' and 'NoneType'` OUT OF
`_shape_category_views` for that scope -- and that call site is NOT wrapped in `_isolated()`, so the raise would
abort `build_all()` for the WHOLE cycle: the identical incident class, one call site deeper, newly reachable
because Tax is the first by_model member with real, live source data that can legitimately go null day to day.
Fixed with a 15-line guard (cited above) that omits a null-valued member from every accumulation, mirroring the
existing law's OWN reasoning rather than inventing a new one. Proven by `TXA2AC3AC4NullLeafRegression` (2 tests:
the null-leaf arm and its present-leaf negative control, s.4 AC3/AC4 below).

## 4. Criteria, denominator 12 of 12

Probe: `cd C:/tmp/wk-taxsma-2c && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~2/probes/tx_a_2.py AC<n>`, run 2026-09-21T09:2xZ, HEAD `fb5f7d6038` (dirty vs HEAD: the 2 files this cell touches).

| id | what | measured | verdict |
|---|---|---|---|
| AC1 | S02..S05 in order, each gated | 3 tests (order dict shape, S02-failure gates off S19-S05, source-order call assertion in `build_all`) -- 3 passed | PASS |
| AC2 | (difference) failure vs disabled leaves other firms identical | 2 tests -- `apply_taxsma_overlay` identity on DISABLED, inflection/cottonwood byte-equal between FAILED and DISABLED -- 2 passed | PASS |
| AC3 | `_last` never zero-fills/inherits an unknown Tax leaf | shares `TXA2AC3AC4NullLeafRegression` (2 tests) -- 2 passed | PASS |
| AC4 | withhold behavior withholds, never zero-fills | same class as AC3 -- 2 passed | PASS |
| AC5 | `operational_control` at the one address, no business value | 3 tests (address equality, key-set schema assertion, 1-call-site census) -- 3 passed | PASS |
| AC6 | firm/global category Gold resolve through `address()` | 2 tests (address equality x2, fake-S3 write-path assertion) -- 2 passed | PASS |
| AC7 | every affected node carries `wire_status_fields` | 2 tests (exact key-set, no caller mutation) -- 2 passed | PASS |
| AC8 | the 3 named reason codes propagate, one arm per code | 1 test, all 3 codes in one parametrized loop -- 1 passed | PASS |
| AC9 | calendar unavailable fails closed, CALENDAR_UNAVAILABLE | 1 test -- 1 passed | PASS |
| AC10 | weekend/holiday: no new valuation date | 2 tests (Sunday, then Monday again) -- 2 passed | PASS |
| AC11 | capability unconfigured -> DISABLED, rest unchanged | 3 tests -- 3 passed | PASS |
| AC12 | MDPF Gold suite: only the 3 pre-existing ids fail | full-suite run, failing-id SET compared exactly against the 3 known ids -- 89 passed, 3 failed, 0 new, 0 fixed | PASS |

**Mutant control (discriminating power, not a criterion of its own):** disabled the S02-failure early-return
inside `run_taxsma_prelude` (one `return _failed(...)` replaced with `pass`), leaving the gating check but not
its consequence. Expected: the AC1 gating test and the AC2 isolation test fail; nothing else should. Observed:
`2 failed, 19 passed` -- exactly `TXA2AC1Order::test_an_s02_failure_gates_off_every_later_stage` and
`TXA2AC2FailureIsolation::test_failure_touches_only_49financial_and_global_never_the_other_two` failed (both
with `AttributeError: 'FailureResult' object has no attribute 'persist_outcome'`, the mechanical consequence of
S19 now running on a `FailureResult`); the other 19 tests, none of which depends on this gate, were unaffected.
Reverted via `cp` from a pre-mutant backup; `git diff` against the pre-mutant working tree shows 0 residual
lines (`grep -c MUTANT`: 0); `py_compile` + the full `test_taxsma_consolidator.py` run (21 passed) confirmed the
clean revert before staging.

## 5. MDPF Gold suite, before and after (bound 17, cell's own instrument)

- **Before my first edit** (measured at cut base `fb5f7d6038`, before touching `mdpf_gold_consolidator.py`):
  `python -m pytest data/mdpf/scripts/gold/tests -q` -> `92 tests collected`, **89 passed, 3 failed**, all three
  in `test_global_fold_flag2.py` (`test_carry_within_window_carries_and_labels`,
  `test_carry_beyond_window_absent_for_real`, `test_carry_source_is_measured_never_interpolated`) -- matching
  the task order's stated baseline exactly.
- **After my last edit** (measured 2026-09-21T09:15Z): same invocation -> `92 tests collected`, **89 passed, 3
  failed**, the SAME three ids, byte-identical failure messages. **No new failure; no fixed failure.**

## 6. Bounds and scope discipline

No deploy of any kind: no `aws s3 cp`, no `.tools/safe-deploy.sh`, no Lambda/S3 write, no run against live
data -- every store this cell exercises is `Local*` (in-process, no network); `write_taxsma_category_gold`'s
one test uses a hand-built fake S3 object, never `boto3`. No real account number, name or balance in any
fixture; `ACCOUNT_KEY = "0012345678"` is a synthetic ten-digit form built the same way `taxsma_membership`'s own
`normalize_account_key` derives one from an eight-digit workbook entry. Every S3-shaped key this cell computes
resolves through `lib.opal_naming.address()`, never a hand-typed literal (`taxsma_operational_control_key`,
`taxsma_category_gold_key`). Names/firm tokens: `_FIRM_SCOPE`-equivalent literals ("49financial", "global") are
the same bare scope tokens every sibling engine module and the consolidator itself already use throughout this
file (`SCOPES`, `FIRM_SCOPES`); no new firm-name literal was minted.
