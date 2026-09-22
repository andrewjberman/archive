# RESULT -- `IRPT_BCKEND.TO-IB-rtn-1`: the capture tool, sixth repair -- timeout recognized by TYPE or deadline STATE only, never message text under any name

**Worker:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtn-1.the-capture-tool-timeout-by-type-or-deadline-state-only.md`.
Design direction is `1.0.0_SA_CTO`'s own round-13 analysis (@`e107b84d38`, section "Round 14"),
REVERSING its own round-12 sign-off acceptance of row `W13-S6` (the "tool's own deadline firing"
exact-message fallback), stated as this cell's arms (a)-(g).

## First: this cell exists because a prior sign-off was wrong

`IB-rtm-1`'s `isOwnDeadlineMessage` -- an EXACT-STRING equality against the one message this
tool's own configured `GOTO_TIMEOUT_MS` deadline produces -- was accepted by the CTO at round-12
sign-off as satisfying arm (a)'s "tool's own deadline firing" clause. `3.0.0_SA_CVO~B`'s own
typed-pair companion diagnostic proved that acceptance wrong: an exact-string equality is STILL a
message-text comparison, and a `TypeError` and a plain `Error` sharing the identical text `Timeout
60000ms exceeded` both wrongly retried and succeeded, neither with any deadline behind it. The CTO
reversed itself. This cell implements that reversal.

## Arm (c) -- baseline reproduction, before touching source

`3.0.0_SA_CVO~B`'s R13 typed-pair companion diagnostic, run UNCHANGED against the UNCHANGED
`IB-rtm-1`-repaired source (blob `058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`, HEAD before this
cell's edits -- confirmed equal to that named blob via `git cat-file -p | sha256sum`), with the
blob passed explicitly: `typeOnlyPairFails=true`, reproducing the defect exactly as stated -- the
genuine `TimeoutError` case, the same-text plain-`Error` case, and the same-text `TypeError` case
all showed `writes=1, success=true` (wrongly retried), while the punctuation-changed and ordinary
certificate-error controls correctly stayed terminal. Saved as
`IB-rtn-1_baseline_r13_typed_pair_companion.json`. R11, R10, R9, R8, and R12 (blob explicit)
diagnostics, run unchanged, saved as `IB-rtn-1_baseline_r{11,10,9,8,12}*.json` -- this round's own
pre-edit reference point, distinct from any earlier round's.

## Arm (a) -- the repair

**`infra/aws/ec2/investor-reporting-export/capture-session.cjs`, committed at `b99067c3bc`:**

`isOwnDeadlineMessage` is DELETED entirely -- not weakened, not narrowed. `require('playwright')`
now also destructures `errors`. Replaced by `isRecognizedTimeout(error)`: `error instanceof
playwrightErrors.TimeoutError` (Playwright's own error class -- guarded by an existence check so a
test double exposing no `errors.TimeoutError` degrades to the second path, the same fail-mode
idiom this file already uses elsewhere) OR `error.name === 'TimeoutError'`. Neither path reads
`error.message`. There is no message-string comparison anywhere in this predicate, or anywhere
else in this file, under any name -- confirmed by reading the full committed file (no residual
`isOwnDeadlineMessage` call site; the identifier survives only in historical-repair comments).

## Arm (b) -- the versioned typed-timeout fixture

`fixture_ib_rtn_1_typed_timeout_v1.cjs` (new file, new name, `FIXTURE_VERSION = 1`, committed at
`188a483e37`). Unlike `harness_ib_rtm_1.cjs`'s synchronous relabeled-Error mocks, this fixture
races `page.goto()`'s verification call between a hung navigation and a GENUINE Node `setTimeout`
(real elapsed event-loop time, `realTimerFired=true`, `elapsedMs` recorded on every run) whose
rejection carries either a real instance of the SAME class exposed to the source as
`playwright.errors.TimeoutError` (GOOD) or a plain untyped `Error` with the identical message text
(BAD). Against the repaired blob: GOOD recovers (`writes=1, success=true`), BAD stays terminal
(`writes=0, success=false`), both with `realTimerFired=true` and comparable `elapsedMs` -- proving
the discriminator is error TYPE, never whether a real async timer fired (it did, in both). Note
for the record: because `TimeoutErrorClass` sets `.name = 'TimeoutError'` and the BAD case's
message never matches round-13's now-deleted fixed 60000ms string, this fixture's own pair does
NOT discriminate round-13 code from round-14 code (both scored `pairOk=true`) -- it is not a
regression detector for THIS defect; that role is `3.0.0_SA_CVO~B`'s R13 companion (arm (c)/(d)).
This fixture's purpose is narrower and different: proving the ACCEPTED predicate genuinely
recognizes a real async deadline, per arm (b)'s own text ("not a bare `throw new Error()`
relabeled"). Both runs (against the repaired blob, and against the pre-round-14 blob as context)
saved as `IB-rtn-1_fixture_typed_timeout_v1_repaired.json` /
`..._prerepair_negative_control.json`.

## Arm (d) -- acceptance: all diagnostics post-repair, both named-historical flips, the new fixture

Reproduced by `battery_ib_rtn_1.py --arm typed` (R114-AC1, token
`IBR114-TYPE-OR-DEADLINE-STATE-ONLY-SPLIT-PAIR-HOLDS`), rc=0, output committed as
`R114-AC1_final_output.txt`.

- R13 typed-pair companion, unmodified, against the CURRENT COMMITTED blob
  (`17aff45ed837a3a6e62fb2ce0410075b62a499dd`, git-object-derived via `git rev-parse HEAD:<path>`):
  `typeOnlyPairFails` flips `true` -> `false`. The genuine `TimeoutError` case still recovers
  (`writes=1, success=true`); the `TypeError` and plain-`Error` twins sharing IDENTICAL message
  text are BOTH now terminal (`writes=0, success=false`) -- closes `W13-S6`'s counterexample for
  real. The punctuation-changed and unrelated-message controls behave as designed (unaffected /
  still recovers by type, respectively), proving the classification is type-based, not
  message-based.
- R11, unmodified, against the same blob, diffed against this round's OWN pre-edit baseline:
  exactly ONE case flips ("same-origin timeout then clean": `writes=1,success=true` ->
  `writes=0,success=false`), the R11 case that throws an untyped `Error()`. Every other one of R11's
  11 cases is unchanged.
- R12, unmodified, blob passed EXPLICITLY, diffed against this round's OWN pre-edit baseline:
  exactly ONE retry case flips ("actual timeout positive control", same shape as R11's), the
  overall `taxonomyCounterexample`/`cleanupCounterexample` verdicts and the cleanup-pair cases
  unaffected.
- R10, R9, R8, unmodified: results arrays BYTE-IDENTICAL to this round's own pre-edit baseline --
  zero drift.
- The new fixture (arm (b)): both cases `realTimerFired=true`; GOOD recovers, BAD stays terminal.

## Arm (e) -- the two named-historical flips, explicitly declared, not a regression

R11's "same-origin timeout then clean" and R12's "actual timeout positive control" both throw an
untyped `Error()` (no `.name` set) to simulate a timeout. Under this round's redesign both are now
EXPECTED to report TERMINAL, per the CTO's round-13 analysis's explicit, prospective ruling: "from
this round on, retry means typed-or-deadline-state only." Each is diffed against its own
round-14-baseline result above and labeled INTENDED, never silently, never described as "still
passing." **No production code bends to keep either green** -- `isRecognizedTimeout` reads only
`error.name`/`instanceof`, nothing else. This is the ONE explicit, ruled exception to "never
weaken an existing check to make a new case pass" (this order's own BOUNDS); it applies to these
two named cases and nothing else -- every other existing S125/S126/S127/C-S153/C-S158/C-S159/
C-S170/C-S171/C-S180/C-S187 check is unweakened, per arm (d)'s byte-identical/unaffected results
above.

## Arm (g) -- metadata fixes, no publish replay

**C-S174** (`battery_ib_rtm_1.py`'s own check, committed at `188a483e37`): widened from a `[:12]`
hash PREFIX comparison to the FULL 64-hex-char hash string on both `CRLF_VALUE` and `BLOB_VALUE`.
Re-ran `battery_ib_rtm_1.py --arm metadata`: still rc=0, `IBR113-METADATA-C174-C187-CORRECTED` --
the full values were already genuinely present in the cited text, so widening the check changes
nothing about the verdict, only the strength of what it certifies.

**C-S194** (`IRPT_BCKEND.TO-IB-rtm-1`'s own proof instance, committed at `188a483e37`): the
`result.md` artifact row was still pinned to the STOPPED blob `586021b506d99288182b7479dc13f1181cd3ba6d`
at commit `cb56783c98` (a pre-publish snapshot of that round's continuation pass, left stale after
the publish completed). Re-pinned to the FINAL result blob `af259448fd8f1eb4d118fa4e7e9b95a7eb1c04ce`
at commit `9423390c47` (the result-update commit that reconciled arm (g)'s completed-publish
narrative), both re-derived via `git rev-parse <ref>:<path>` against the git object -- never a raw
working-tree read. `proof-of-spec-check` re-run on the edited instance: VALID rc=0, no criterion
verdict changed.

`battery_ib_rtn_1.py --arm metadata` (R114-AC2, token `IBR114-METADATA-C174-C194-CORRECTED`),
rc=0, output committed as `R114-AC2_final_output.txt`.

## Arm (f) -- the packet, STOPPED (both never-widen halves absent)

`IB-rtn-1_NEVER_WIDEN_PACKET.md` written and committed at `115f053837` (blob
`7e3d70b90d67fc50d1cb7f73fb383fb5e662107a`),
documenting the exact blast radius (ONE file, `capture-session.cjs`, blob
`17aff45ed837a3a6e62fb2ce0410075b62a499dd`), every hash git-object-derived (`git cat-file -p
<blob> | sha256sum`, cross-checked with `git show HEAD:<path> | sha256sum`, agreeing), and the
rollback path. Censused this session (`Glob` over
`org/tier1_exec/{1.0.0_SA_CTO,2.0.0_SA_COO~B}/deliverables/` for any filename containing
`IB-rtn-1`): 0 of 0 found. Per the order's own arm (f) ("STOP here unless BOTH halves ... are at
HEAD naming this NEW packet's blob"), this worker does NOT open the ledger entry, does NOT publish
to S3, does NOT update the README's hash line, and does NOT claim host-side or S3-side
verification. **`<status>` stays `pending`, with this blocking state stated**, per the order's own
`<proof_of_spec>` instruction. The publish, and the README hash-line update, remain available to a
later pass once both halves land.

## Surprises

None filed this pass. Every premise checked (the pre-edit blob equaled the named
`058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`; the baseline reproduced the stated defect exactly;
the repair split as designed; both named-historical cases flipped in exactly the way and only the
way the CTO's round-13 analysis anticipated; the packet gate's own STOP condition held as
designed). No path was absent, no capability was missing, no reading of the frozen BOUNDS was in
tension with arm (a)'s text.
