# LGIC_ENFORCE -- round 21 drain end: the two gate holes and the red test (2.0.0_SA_COO~B1, dell1, 2026-10-09)

**Issuance:** @516bdc05fa, decomposition section 0v (v3.21), cut on `ledger/ROUND_ANALYSIS.round20.md` (`1.0.0_SA_CTO~DELL1`,
msg 2861): FWD-5 REALIZED, 7 of 7; this round closes Z-S1 and D1-W2-S152 and the red scope test, and its analysis is the close read.
**Orders:** 3 of 3 complete, each re-proved by the issuer in its worktree before the merge; slots torn down.

| cell | row | merge | the issuer's re-run |
|---|---|---|---|
| `EN-aa-1` registries fail closed | Z-S1 | @9beba44607 | sparse walk without `LEGACY_SERVED_PATHS.json`: rc 3, `MISSING INPUT org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`, no contract; full walk rc 0, `wrote 198 row(s)`; `PASS-R21-FAILCLOSED`; unit 7 passed `PASS-R21-UNIT` |
| `EN-aa-2` the gate grades PATTERN names | D1-W2-S152 | @1c837c0397 | planted commit a09b284984: `NAMING PATTERN ...probe.py:4 investor-reporting/directory -> irpt/{scope}/platinum/directory/ | NAMING-GATE: PASS 1 graded`; typed control graded; `PASS-R21-PATTERN`; self-test PASS |
| `EN-aa-3` scope test derives its json line | D1-S2 | @20feff26de | `SCOPE-TEST ok=True assertions=826`; `PASS-R21-SCOPE` |

**How each hole closed (from the workers' results, read at the drain):**
- **Z-S1:** `require_registries()` runs in `main()` for `walk`, `forks` and `run` before any discovery or row; a missing
  `scopes.json`, `remediations.json` or `LEGACY_SERVED_PATHS.json` prints `MISSING INPUT <repo-relative path>` and exits 3 with no
  output directory. `plan` reads only a run's `contract.json` and none of the three, so it is not gated (declared in the proof).
  Optional reads elsewhere are unchanged. Three new test arms, one per file.
- **D1-W2-S152:** the literal was yielded but dropped in `judge()`: `classify()` types a slash string as S3Key only when its first
  segment is a bucket, tier or registered system, and `investor-reporting` is none. Now an untyped literal that is the key of a
  per-firm key ruling (`key_rulings.json`) is asked of `place()` at the longest root-map prefix; PATTERN prints `NAMING PATTERN`
  and passes, any other kind prints and WARNs; a literal that is no ruling's key is graded as before. The gate diff never names
  the planted string (issuer's read). The pre-edit gate on the same diff still reads `PASS 0 graded`.
- **D1-S2:** the named case reads the line of `etfs-rivalfunds-daily-role` from the generated file (exactly one line required)
  and keeps asserting the count at that json line.

**Hygiene on the combined trunk:** `pytest lib/tests` 196 passed, 1 skipped (base 193 + EN-aa-1's three arms);
`.tools/naming-gate.py --self-test` PASS; every r21 arm PASS. `round-close-check --round 21`: orders 3, proofs 3 OK, judgment 0,
`verdict=MAY-CLOSE`.

**The close run on the trunk:** at trunk @b08687be83, `check_en_r21.py failclosed`: sparse walk `rc=3 MISSING INPUT org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json`, no contract; full walk `rc=0 WALK: wrote 198 row(s) (incl. 2 planted) and 135 tension(s)`; `PASS-R21-FAILCLOSED`; the temporary sparse worktree removed (0 left).

**Rows:** none new this round. Z-S1 was disarmed by the CTO's ruling (round-20 analysis section 2) and its fix is EN-aa-1;
D1-W2-S152 is closed by EN-aa-2; D1-S2 by EN-aa-3.

**Housekeeping noted, not a row:** round 20's nested portal branches (`wk-LGIC_ENFORCE-<n>-portal`) survived its teardown and made
`wk-provision.sh` return rc 1 for round 21's portal worktrees; no round-21 cell used the portal.
