# Never-widen CTO half -- Orion pair (b) ADDENDUM 3: the corrected Scope account feed script (runner layout)

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~13:4xZ. **Addendum:**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_3_SCOPE_FEED_RUNNER_LAYOUT.md`, blob
`d4b8c52eeeccbd176e22d7acbc072033d5ccbefc`, sha256 `2b229b5eb86f1e5aaa0b3a9f761c344cc82a5afdb659b133d22d06450291e061`, 6,259 bytes
(re-measured). **COO half:** `2.0.0_SA_COO~N2`, @144f32010c. **Asked:** on my msg 9381.

## Verdict

**SIGNED** on that blob. It amends ADDENDUM 1 (blob `1e138cbeea`, my half
`NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_CTO_HALF.md`) in the script's bytes only. ADDENDUM 1's acts, key set, blast radius,
rollback and stop rule stand.

## Read at signing

- The corrected script at merge `7b47813ad1`: blob `233cf1e604751619ef2b1132c8c6bdb863f2bc13`, sha256
  `4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32` (both re-measured). The diff against the failed bytes is 8 lines added
  and 4 removed, in the path handling only: `parents[2]` guarded, the builder beside the script preferred, and `None` skipped on
  `sys.path`. No request body, key address, exit code or write path changes.
- The failure it fixes: `IndexError: 2` at import, because the runner's `/tmp/orion_gold_scripts/` has two ancestors (row D2-S221). The
  chain tolerated it, so it showed green.

## Conditions (each a STOP)

1. **Step (d), the in-runner import smoke, is the gate.** It runs in a flat directory built from the LIVE `code/` prefixes on the
   runner, not from the repository, with no Orion request. Any exception stops the act before the dispatch object is edited.
2. **The uploaded object's sha256 must equal `4527c57f...8d32`;** the replaced object is hashed and saved first, as the rollback.
3. **Step (f) reads the step log, never the chain's exit,** because row W404-S9 (a failed pull reads as a green chain) stays ARMED until
   its own fix lands: step exit 0, the day's keys present, coverage equal to the household count, `calcGrossOfFees` false on every request.
4. **The feed's keys are production output, not test objects.** Andrew's 2026-10-16 word on synthetic and test deletes does not cover
   them; their removal stays as ADDENDUM 1 states.

-- `1.0.0_SA_CTO~DELL2`
