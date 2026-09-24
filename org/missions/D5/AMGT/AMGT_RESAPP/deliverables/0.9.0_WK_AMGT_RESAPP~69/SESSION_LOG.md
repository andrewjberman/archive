# Session log -- 0.9.0_WK_AMGT_RESAPP~69 on AMGT-rk-69

Worktree: C:/tmp/wk-amgt-17-69 (branch wk-amgt-17-69, cut from the round-17 issuance commit 87ce2e5971).

## What was built

1. `.tools/surprise-row-gate.py:1180` -- `_PROOF_BLOCK_RE` line-anchored on BOTH the opening and
   closing `<proof_of_spec>`/`</proof_of_spec>` tags, exactly the pattern the issuer's own 135-order
   population census validated: `re.compile(r"^[ \t]*<proof_of_spec>[ \t]*$(.*?)^[ \t]*</proof_of_spec>",
   re.M | re.S)`. `_order_criteria`'s whole-text fallback (`:1192`) is untouched -- a malformed order
   with no block tag still yields what it can. One sentence added to `_order_criteria`'s own docstring
   naming the anchoring and row `AMGT_RESAPP-Z-S176`.
2. `.tools/tests/test_acceptance_sweep.py` -- three arms appended (arms 8-10; no existing arm edited):
   - Arm 8, THE DISCRIMINATING ARM: a fixture order whose prose names `` `<proof_of_spec>...
     </proof_of_spec>` `` inline, both open and close, in backticks -- the exact shape rk-58's own
     order carries at its line 80 -- BEFORE a real block of 3 criteria. Proven against HEAD's OWN COPY
     of the gate (`git show HEAD:.tools/surprise-row-gate.py` loaded into a temp file via
     `importlib.util`), so the "before" half is measured, not assumed: HEAD's unanchored pattern binds
     to the prose's own inline open+close pair (the non-greedy body between them is just the ellipsis)
     and returns 0 criteria; the currently-loaded, edited gate returns all 3.
   - Arm 9: a normal order (real block only, no prose mention) -- the edited pattern's count is
     unchanged from HEAD's (both read 2 on the fixture).
   - Arm 10: an order with no `<proof_of_spec>` block tag at all -- the whole-text fallback (`:1192`,
     untouched) still yields its criteria (Z1, Z2).

## What was measured, not assumed (ISSUER RULE followed)

The population moved from the issuer's cut-time count of 135 orders to 137 at this worktree's spawn
(this order and its round-17 sibling `AMGT-rk-70` both landed as tracked task-order files in the same
issuance commit 87ce2e5971) -- expected per this order's own "re-measure before you edit" bound, not a
surprise. AC3 was run against the re-measured denominator (137 orders, 0 with zero criteria).

AC1's baseline was re-measured at spawn before editing: `PASS 126 / FAIL 1 / UNVERIFIABLE 33 of 160
criteria over 30 order(s)` -- identical to the issuer's own cited HEAD line, so no drift and the
criterion's primary bar (131/1/33 of 165 over 31) applied as written; post-fix measurement matched it
exactly, byte for byte.

Every regex containing `$` was written to a script file (`.scratch/make_mutant.py`,
`.scratch/run_mutant_battery.py`, `.scratch/ac3_probe.py`) or run from AC's own literal single-quoted
`python -c` invocation, never an inline double-quoted regex -- the ISSUER RULE in section 1, whose own
failure mode (silent `$(` command substitution eating the regex body) was independently re-derived while
drafting the mutation control below.

## Controls

- **Mutant**: `.scratch/mutant_gate.py`, a copy of the edited gate with `_PROOF_BLOCK_RE` reverted
  (by script, `.scratch/make_mutant.py`) to HEAD's unanchored form. Run against arm 8's own
  discriminating fixture (`.scratch/run_mutant_battery.py`): the mutant returns 0 criteria (matching
  the pre-fix defect), confirming the fix -- and the discriminating arm that proves it -- actually
  distinguishes the two patterns rather than passing regardless.
- **Determinism**: AC1's literal invocation run twice in succession against the same HEAD; `diff`
  reports no differences (byte-identical stdout both times).

## Other `<proof_of_spec>` parsers (WALLS, per section 1's own instruction)

Read-only check of `.tools/to-pipeline-gate.py`, `.tools/proof-of-spec-check.py` and
`.tools/direct-act-order.py` for the same unanchored-search shape: `to-pipeline-gate.py` does not parse
order-text `<proof_of_spec>` blocks by regex at all; `proof-of-spec-check.py` operates on the committed
`.proof_of_spec.json` instances, not order text; `direct-act-order.py` only WRITES `<proof_of_spec>`
blocks (a generator), never parses one back. No occurrence of the same unanchored shape found in any of
the three -- no row filed for this note.

## Verification runs

- `python .tools/surprise-row-gate.py --acceptance AMGT_RESAPP --round 14` -- pre-edit baseline matched
  HEAD's cited line; post-edit matched AC1's `<expect>` exactly.
- `python .tools/tests/test_acceptance_sweep.py` -- `RESULT: 0 arm(s) failed of 10`, `BATTERY PASS`.
- AC3's literal invocation (single-quoted `python -c`, importing the compiled pattern) -- `orders 137
  orders_with_zero_criteria 0 []`, `pattern_is_line_anchored True`.
- AC4's literal invocation -- both edited files: `compiles True`, `crlf 0`, `non_ascii_bytes` equal to
  the `merge-base HEAD SITEZ` figure printed beside it (`.tools/surprise-row-gate.py`: 2 == 2 pre-existing;
  `.tools/tests/test_acceptance_sweep.py`: 0 == 0).
- `python -m py_compile .tools/surprise-row-gate.py .tools/tests/test_acceptance_sweep.py` -- COMPILE-OK.
- `python -m ruff check .tools/surprise-row-gate.py .tools/tests/test_acceptance_sweep.py --target-version py39`
  -- All checks passed!
