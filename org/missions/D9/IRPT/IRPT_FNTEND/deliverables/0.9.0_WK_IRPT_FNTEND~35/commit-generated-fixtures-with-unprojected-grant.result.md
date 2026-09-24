# IRPT_FNTEND.TO-FE-s-85 -- result (0.9.0_WK_IRPT_FNTEND~35)

**Disclosure (HOW step 8):** this cell is a DATA-OBJECT check, not a rendered visual assertion -- the
order's own BOUNDS section declares C-S176's five-part visual control rule N/A, WITH REASON, at cut time
("this cell's criteria are DATA-OBJECT checks ... F85-AC3's git-object read IS this cell's control"). No
dev server was started (none of this cell's four mechanical criteria touch a rendered route); no PNG was
captured. Every number below is either a `git show <commit>:<path>` read, JSON-parsed and counted, or a
`bun`/`tsc` process exit.

## Read first (HOW step 1)

`portal/DESIGN.md` C1-C12, `portal/CLAUDE.md`, the PRD's FWD-12 ENDPOINT row and F9 CONTRACTS clause
(v0.10 @4bc62712f2), the CTO's round-13 analysis (@4bc62712f2), and `REMEDIATION_v10.md`. This cell's
substance is round-13's own finding, restated verbatim in the task order: `gen-corpus.ts`'s `envelope()`
helper was fixed to emit `unprojected_grant` on every entry, but the two sibling files it writes
(`fe-s-13-wire.json`, `fe-s-14-print-v1.json`) were never committed -- only `default.json` (a round-12
hand repair) landed. `gen-corpus.ts` itself is READ-ONLY to this cell (round 13 already fixed it); the
grant is to regenerate and commit its OUTPUT only.

## The fix

1. Confirmed the pre-fix state at the committed git object (round-14 base, portal HEAD `467354c9`):
   `fe-s-13-wire.json` 0 of 9, `fe-s-14-print-v1.json` 0 of 2 carried `unprojected_grant`; `default.json`
   read 12 of 12 -- matching the order's own claim exactly.
2. Ran the generator's documented invocation (`bun run src/pages/InvestorReporting/__tests__/fe-s-13/gen-corpus.ts`):
   `REQUEST RECORDS: 12 of 12; SMOKE KEYS: 9; PUBLISHED MAP KEYS: 12 of 12 DECLARED; PRINT MAP KEYS: 2`
   (F85-AC2's denominator, matched).
3. Diffed every regenerated working-tree file against HEAD before touching git: `fe-s-13-wire.json` (47
   insertions) and `fe-s-14-print-v1.json` (10 insertions) are PURELY ADDITIVE `unprojected_grant`
   blocks (`{"count":0,"denominator":1,"kinds":[]}` at each of 9 / 2 request-record keys respectively) --
   no other field or value touched, read the full diffs myself. `default.json` and twelve
   `fixtures/wire/requests/*.request.json` files also show as modified in `git status`, but `git diff
   --stat` carries ZERO lines for any of them -- CRLF-normalization touch artifacts only (this box's
   `core.autocrlf=true`), not content changes. Per the order's own instruction ("do not re-commit
   [default.json] unless the generator's run changed its content"): it did not, so it is not re-committed
   here, and the round-12 hand repair stands undisturbed at 12 of 12.
4. Committed the two fixtures FIRST (portal commit `34174c39`), then wrote the checker
   (`__tests__/fe-s-85/verify-git-object.mjs`, plain node/bun, no framework) and committed it separately
   (portal commit `b8c0a3fd`) -- both on branch `wk-irpt_fntend-14-85-fe-s-85-portal`, LOCAL only, per
   BOUNDS ("PORTAL IS FROZEN").
5. Ran the checker against the fixture commit: `GIT-OBJECT fe-s-13-wire.json: 9 of 9`, `... fe-s-14-print-v1.json:
   2 of 2`, `... default.json: 12 of 12`, all `carry unprojected_grant` -- read AT THE COMMITTED GIT
   OBJECT, per the order's own instruction, never the working tree.

## Control (HOW step 4 -- a control is a claim)

Ran the checker's wrong-state arm against the round-14 base commit (`467354c9`, the state BEFORE this
cell's fix): `0 of 9`, `0 of 2`, `12 of 12` -- the checker genuinely distinguishes the pre-fix state from
the post-fix state; it is not a pass-through. Also confirmed the checker's null-handling matches the
order's exact spec ("counts entries with a non-null `unprojected_grant` key present ... ABSENT does
not"): the implementation checks BOTH key-presence (`hasOwnProperty`) AND `!== null`, not presence alone.

## Order defect found (surprise row `IRPT_FNTEND-W35-S1`, BLOCKING/ARMED, disarm owner `2.0.0_SA_COO~F`)

F85-AC3's literal `<invocation>` (`cd <WS>/portal && bun __tests__/fe-s-85/verify-git-object.mjs
<your-commit-hash>`) cannot succeed as written on TWO counts, independently confirmed live:

- **Path.** The checker must live under this cell's `<paths>` grant
  (`portal/src/pages/InvestorReporting/__tests__/fe-s-85/`), matching every one of this project's 220+
  existing `__tests__/fe-s-N/` directories (none sit at `portal/__tests__/`). Run with only `<WS>`
  expanded, the bare `__tests__/fe-s-85/verify-git-object.mjs` path fails identically whether the hash
  argument is the literal bracket text or a real hash: `error: Module not found
  "__tests__/fe-s-85/verify-git-object.mjs"`, rc=1.
- **Hash notation.** `<your-commit-hash>` is not a member of this order's own declared
  `<placeholders>WS, PORT</placeholders>`, so `proof-of-spec-check.py`'s ENFORCE alignment limb cannot
  expand it, and it is not even valid literal bash: run completely unexpanded and unquoted, bash's own
  redirection parser raises a syntax error before `bun` is invoked at all (confirmed live).

Per `IRPT_FNTEND-S31`'s ruling (a corrected invocation belongs in the task-order FILE, never only a
worker's self-substituted proof record -- the same standard `IRPT_FNTEND-W34-S1` already applied to
FE-s-84's F84-AC5), **F85-AC3 is graded FAIL in this worker's proof instance on the literal invocation.**
The substance the criterion exists to prove -- `unprojected_grant` surviving to the committed git object
at all three files -- is independently demonstrated above, at the grant-consistent path, against the real
fixture commit, with a genuine negative control. Disarmed when the issuing COO amends F85-AC3's
`<invocation>` (grant-consistent path, and either a declared `COMMIT` placeholder or another resolution
for the hash substitution) and this worker or a successor re-runs and flips this TO `complete`.

## Criteria

- **F85-AC1** (typecheck): PASS. `tsc -b --noEmit` rc=0.
- **F85-AC2** (generator denominators): PASS. `SMOKE KEYS: 9`, `PRINT MAP KEYS: 2` as required.
- **F85-AC3** (committed git object): originally FAIL as literally written (order defect, filed
  `IRPT_FNTEND-W35-S1`; substance proven supplementarily at the grant-consistent path: `9 of 9`, `2 of 2`,
  `12 of 12`). The issuing COO (2.0.0_SA_COO~F) amended F85-AC3's `<invocation>` in the task order (correct
  path, `$(git rev-parse HEAD)` substitution) and independently re-verified live against this worker's own
  commit before amending. Re-run here against the corrected invocation exactly as it now reads in the TO:
  PASS -- `fe-s-13-wire.json: 9 of 9`, `fe-s-14-print-v1.json: 2 of 2`, `default.json: 12 of 12`, rc=0.
  `IRPT_FNTEND-W35-S1` disarmed by the amendment per its own disarm_owner clause.
- **F85-AC4** (whole IRPT_FNTEND suite): PASS. `650 pass`, `0 fail`, `27 skip`, 2706 expect() calls, 677
  tests across 127 files.
- **F85-AC5** (judgment, CVO at L9): RECORDED, no verdict self-given. The committed fixture content is the
  generator's genuine, unmodified output (diffs shown above are purely additive `unprojected_grant`
  blocks, nothing hand-edited); `default.json` was not touched (zero content diff, confirmed by
  `git diff --stat`) and remains the round-12 hand repair, data-equivalent to itself.

## Push state

LOCAL only, both repos. Workspace branch `wk-irpt_fntend-14-85-fe-s-85` (this file, the surprise row, the
proof-of-spec instance). Portal branch `wk-irpt_fntend-14-85-fe-s-85-portal`, commits `34174c39` (the two
fixtures) and `b8c0a3fd` (the checker), both on top of round-13's close `467354c9`.
