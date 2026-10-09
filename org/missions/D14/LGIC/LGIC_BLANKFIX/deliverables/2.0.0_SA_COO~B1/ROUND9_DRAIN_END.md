# LGIC_BLANKFIX -- round 9 drain end (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @0267c8d4f3, `decompositions/LGIC_BLANKFIX_DECOMP.round9.md`, cut on `ledger/ROUND_ANALYSIS.round8.md` @2ba21c4271.
**Orders:** 6 of 6 complete. Each was re-proved by the issuer in the slot's worktree before its chain-end merge: every criterion
re-run, then `proof-of-spec-check`, then `safe-merge`. Worktrees and slot branches are removed.

| cell | item | serves | merge | proof re-run by the issuer |
|---|---|---|---|---|
| `BF-x-6` | E6, holes on the newly mapped roots | FWD-2, FWD-7 | @1db8c77646 | `NEW-ROOTS-FILL ok=True mapped=78 before=41 after=0 roots_worked=5 rows=37 refused=0`; `CADENCE-TEST ok=True cases=59` |
| `BF-x-3` | E3, switch-on wiring (W1-S19, W1-S20) | FWD-6 | @227b029251 | `SWITCH-ON ok=True arms=11 held=11`; `NAMING-APPLY-GATE-SELF-TEST: PASS` |
| `BF-x-4` | E4, the audited override (W1-S21, arm H) | FWD-6 | @227b029251 | `OVERRIDE-ARMS ok=True arms=12 held=12`; `NAMING-GATE-SELF-TEST: PASS`; **BX4-AC3 judgment, ungraded** |
| `BF-x-2` | E2, S12 fixtures in the overlay | FWD-6 | @441b279ac9 | `ROOTCHECK-TEST ok=True`; `FWD6-ARMS ok=True arms=7 held=7` |
| `BF-x-1` | E1, the H8 rule | FWD-2 | @441b279ac9 | `ROOTCHECK-TEST ok=True`; `H8-RULE ok=True owned=10 not_asked=10 hole_before=51 hole_after=41 mapped=78` |
| `BF-x-5` | E5, counted at the caller (W4-S6) | FWD-2 | @441b279ac9 | `ROOTCHECK-TEST ok=True cases=324`; `CALLER-COUNT ok=True uncounted_before=17 uncounted_after=0 counted_at_caller=17` |

**Drain hygiene at each merge:**
- `pytest lib/tests` reads 193 passed, 1 skipped, the same as the base.
- Every `lib/tests/test_opal_naming_*.py` reads ok, including `SCOPE-TEST ok=True assertions=831` after AMENDMENT 2.
- `org/mcp/naming-place.enforce` is absent at every merge and on the trunk.
- `org/naming-place-override-audit.log` is absent on the trunk.

## The real run at the close

`python lib/opal_naming.py census --all-roots` was run on the trunk, at base a5a5a5313b, which carries every merge above and the
CRO's write of the BF-x-6 rows @cc85ec34f5. Its output is `ALL_ROOTS_round9.txt` beside this file:

`ALL-ROOTS ok=True roots_total=87 mapped=78 unmapped=9 completed=78 stopped=0 items=2263 right=558 fix=1460 not_asked=222 pattern=23
carded=0 refused=0 hole=0 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=0 other_holes=0
stale_hints=0 uncounted=1 counted_at_caller=17`

**Against round 8, as the analysis asks:**
- **Round-8 close:** `mapped=63 hole=10 uncounted=17` (`ALL_ROOTS_round8.txt`).
- **Round-9 base:** `mapped=78 hole=51 uncounted=17` (`ALL_ROOTS_round9_base.txt`).
- **Round-9 close:** `mapped=78 hole=0 uncounted=1 counted_at_caller=17`.

How each figure moved:
- **Holes:** the 41 on the newly mapped roots fell to 0 through the CRO's rows. The 10 H8 holes fell to 0 through the NOT-GRADED to NOT-ASKED rule, which is why `not_asked` went from 174 to 222.
- **The 17 module inputs:** they print `COUNTED-AT-CALLER` and no `UNCOUNTED` line remains on a mapped root.
- **`uncounted=1`:** this is the unmapped root `shared-infra` (`UNMAPPED infra/aws/terraform/shared-infra names=157 uncounted=1`). It is one of the 9 held entries, which the analysis keeps out of round 9.

## Rows

| row | kind | state |
|---|---|---|
| `D1-S1` | issuer, instrument | `round-close-check.py` exact-matches `complete`, so an order status like `complete -- proof ...` reads as open. Its owner is not this seat. |
| `D1-W1-S1` | worker, cut defect | BF-x-1's checker read the 63-root baseline. Ruled by AMENDMENT 1 @0a5d9b2e47. |
| `D1-S2` | issuer, cut defect | The scope test pinned `uncounted` as the last ALL-ROOTS field. Ruled by AMENDMENT 2 @c7b15a3f5e. |
| `D1-W2-S1` | worker, OBSERVATION | The apply gate's directory (pre-plan) mode has no placement step. Only the plan stage can refuse. |
| `D1-W2-S2` | worker, OBSERVATION | `org/naming-place-override-audit.log` is gitignored by `*.log`, so override rows stay on the box that wrote them. This bears on the switch-on call. |

## Open for the round-9 analysis

- **BX4-AC3 (judgment, `3.0.0_SA_CVO`).** The question: do the three switch-on preconditions now hold (W1-S19, W1-S20, W1-S21)?
  - Artifacts: `deliverables/0.9.0_WK_LGIC_BLANKFIX~2/exercise_switch_on.py` and `deliverables/0.9.0_WK_LGIC_BLANKFIX~2/exercise_override.py`.
  - The four scripts: `.tools/safe-commit.sh`, `.tools/safe-apply.sh`, `.tools/naming-gate.py` and `.tools/naming-apply-gate.py`.
  - Rows D1-W2-S1 and D1-W2-S2.
  - `round-close-check` reads `verdict=REFUSED` on this one ungraded judgment, so `dep_stage` stays `EXECUTING` until it is graded.
- **The switch-on itself** is `1.0.0_SA_CTO`'s to rule after that grade. Two inputs bear on it:
  - The override's audit is box-local (D1-W2-S2).
  - The gate trusts an audit row that is under 600 s old and names the refused name, and a seat that can append to the log can forge one. This is declared in BF-x-4's proof.
- **Not in round 9, carried forward:** the 9 held entries, including `shared-infra`'s one uncounted name; and W4-S7, W4-S8 and W5-S2, which sit with the CRO.
