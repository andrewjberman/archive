# LGIC_ENFORCE.TO-EN-n-1-r3 -- the gate's domain (round 3, cell EN-n-1): result and session log

Worker `0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-3-1`, branch `wk-lgic-enforce-3-1`,
cut from CLOUD @24bae9d9da. Everything here is LOCAL on that branch (never pushed).

## The bar

- `git rev-parse --abbrev-ref HEAD` -> `wk-lgic-enforce-3-1`; `test -d org && test -d .tools` -> `TREE-OK`.
- Grant: `.tools/naming-gate.py`, the project's surprise channel, this order's own deliverables folder and
  the order file itself (for the status flip). Fixed input `check_en_r3.py` read-only.

## Premises re-grounded

Reproduced RED at the cut, before any edit (matches the order's stated measurements exactly):
```
n2-denominator                   FAIL-N2-NO-DENOMINATOR
n2-coverage                      FAIL-N2-NO-COVERAGE
n2-declaration-subtraction       FAIL-N2-NO-SUBTRACTION
n2-record-tree-ungraded          FAIL-N2-RECORD-TREE-GRADED  (rc=1, a proof instance under org/ refused)
n2-resolving-path-exempt         FAIL-N2-CITATION-GRADED-AS-MINT (rc=1, a resolving repo-path citation refused)
n2-binary-needs-reason           FAIL-N2-BINARY-BYPASS-UNGRADED (rc=0, PASS 0 graded -- the bypass is silent)
regress-n2-tf-name-refuses               PASS-N2R-TF-NAME-STILL-REFUSES (already true, must not regress)
regress-n2-nonresolving-path-refuses     PASS-N2R-NONRESOLVING-PATH-REFUSES (already true, must not regress)
regress-n2-binary-with-reason-passes     PASS-N2R-REASONED-ATTRIBUTE-PASSES (already true, must not regress)
```
`.gitattributes` at the cut carries exactly 3 `binary` lines, all three under `org/modules/graph/potion/model/**`
or `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/{r2,r3}/seats/**` -- both record trees, matching
the order's "none needs a reason today" note.

The pinned baseline (A-7): reproduced the pre-state at `f1ecf97da7` exactly via a transient detached worktree
(`.worktrees/wk-lgic-enforce-3-1-pinread`, removed after the read) running the SAME invocation S41/S45 used:
`git diff 4b825dc642cb6eb9a060e54bf8d69288fbee4904 f1ecf97da7 -- 'org/missions/**/*.json'` fed to
`.tools/naming-gate.py --diff`. Result: `NAMING-GATE: WARN 3815 graded`, 2917 REFUSE lines across 90 distinct
files -- matches 3815/2917/90 exactly. Full detail in `GATE_DOMAIN_BASELINE.r3.md` beside this file.

## What was built

`.tools/naming-gate.py`, four changes:

1. **The domain, by subtraction (R-13, Rule 24(i)).** `RECORD_TREE_PREFIXES = ("org/", "docs/")`.
   `grade_file()` now returns `[]` immediately for any path under a record tree -- before any pre-image
   read, before the generated-file check, regardless of suffix ("never opened"). `run()` computes
   `domain_meta(files)` over every file in the parsed diff and every invocation now prints, unconditionally:
   `DENOMINATOR: N path(s) in this diff; declaration-tree domain = N MINUS EXCLUDED(org/, docs/) R = D path(s)`
   and `COVERAGE: U path(s) in the declaration domain the gate could not see (extension outside its graded
   set and not .gitattributes); S seen`. `EXCLUDED(org/, docs/)` names both trees literally on the
   DENOMINATOR line, satisfying the printed-subtraction contract (never a forward list).
2. **The citation exemption (R-11).** `_resolves_to_tracked(value)` checks, via `git cat-file -e HEAD:<value>`
   (memoized), whether a path-shaped literal (contains `/`, not a URI/ARN, no `..` segment) resolves to a
   tracked file at HEAD. `judge()` now returns `None` (not graded) for any literal that resolves -- a
   citation, never a mint. A non-resolving path-shaped literal (a typo, an invented file) reaches the matrix
   exactly as before and still refuses.
3. **`.gitattributes` grading (A-6).** New path type: `_is_gitattributes()` routes `.gitattributes` files to
   `_grade_gitattributes()`, which reads only ADDED lines (via the existing `apply_hunks`) and judges each
   with `_judge_gitattributes_line()`: a `binary` or `-diff` token among the line's attributes, on a target
   pattern NOT under a record tree, with no same-line `# reason` text after it, REFUSES naming the file and
   line; the same line with a reason PASSES; a target under a record tree is not graded (matches the 3
   existing lines' measured state).
4. **`run()`/`main()` wiring.** `run()` now returns `(rows, meta)`; `main()` prints `meta` before the row
   listing (both WARN and ENFORCE modes, on every successful run) and folds it into the verdict log.

No change to `classify()`, `carrier()`, the matrix's REFUSE/ALIAS/OUT-OF-PATTERN logic, or the generated-file
check for declaration-tree files -- a real `.tf` resource name and a non-resolving path literal reach the
SAME code path as before.

## Criteria

| id | subcommand | rc | verdict |
|---|---|---|---|
| N1R3-AC1 | n2-denominator | 0 | PASS-N2-DENOMINATOR-PRINTED |
| N1R3-AC2 | n2-coverage | 0 | PASS-N2-COVERAGE-PRINTED |
| N1R3-AC3 | n2-declaration-subtraction | 0 | PASS-N2-SUBTRACTION-PRINTED |
| N1R3-AC4 | n2-record-tree-ungraded | 0 | PASS-N2-RECORD-TREE-UNGRADED |
| N1R3-AC5 | n2-resolving-path-exempt | 0 | PASS-N2-RESOLVING-PATH-EXEMPT |
| N1R3-AC6 | n2-binary-needs-reason | 0 | PASS-N2-BINARY-NEEDS-REASON |
| N1R3-AC7 | regress-n2-tf-name-refuses | 0 | PASS-N2R-TF-NAME-STILL-REFUSES |
| N1R3-AC8 | regress-n2-nonresolving-path-refuses | 0 | PASS-N2R-NONRESOLVING-PATH-REFUSES |
| N1R3-AC9 | regress-n2-binary-with-reason-passes | 0 | PASS-N2R-REASONED-ATTRIBUTE-PASSES |
| N1R3-AC10 | (JUDGMENT, 3.0.0_SA_CVO) | n/a | see `GATE_DOMAIN_BASELINE.r3.md` |

9 of 9 mechanical criteria PASS-by-output. `selftest-arms` on the shared checker: 74 of 74 OK (unaffected
cells' injected arms still pass; the real-gate cell-2 criteria above are the direct evidence).

## Controls

- **Negative controls (S45's required discrimination), run against the REAL gate, not injected:** the same
  literal (`advi-49f-fwd2-exercise-queue`) as a `.tf` resource name still REFUSES (N1R3-AC7); the same
  citation path with a typo (`-typo-nope.md`) still REFUSES (N1R3-AC8); the same `-diff` attribute WITH a
  same-line reason still PASSES (N1R3-AC9).
- **The 955-record frame, at this tip:** `NAMING-GATE: PASS 0 graded` -- a disclosed 0-of-0 (DENOMINATOR and
  EXCLUDED both printed), matching R-15 ruling 2's required shape exactly, not a silent vacuity.
- **selftest-arms**, run after the fix: 74 of 74 OK (no cell outside EN-n-1 regressed).

## Rows filed

None. No surprise met the bar (the order's own premises reproduced exactly as stated; no capability
missing; no path outside grant needed).

## Limits

- **The citation exemption resolves against HEAD, not the worktree.** A literal citing a path staged but not
  yet committed reads as non-resolving (still graded/refused) until the commit lands. This matches every
  other HEAD-relative read already in the gate (`git show HEAD:<path>` for pre-images).
- **COVERAGE counts by extension only.** A file inside the declaration domain whose extension IS in
  `GRADED_EXT` but whose pre-image the gate could not read for some other reason (e.g. a binary-diff
  bypass, S42's unrelated finding) is counted as "seen" here, not as coverage loss. S42 is a separate,
  already-filed row and is not re-opened by this cell.
- **`.gitattributes` reason text is unvalidated prose** -- any non-empty text after `#` passes; the gate
  does not judge whether the stated reason is a GOOD one, only whether one was given (A-6's own bar).

## Commits (LOCAL on wk-lgic-enforce-3-1)

- The gate fix (`.tools/naming-gate.py`) and `GATE_DOMAIN_BASELINE.r3.md`, committed first.
- This file, the proof instance (pinning the artifact's commit hash) and the `pending` -> `complete` flip,
  committed second.
