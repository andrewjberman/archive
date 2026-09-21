# Result -- IRPT_FNTEND.TO-FE-s-56 (fe-s-14 control re-point + fixture prose)

Worker: `0.9.0_WK_IRPT_FNTEND~6`. Worktree: `C:/tmp/wk-irpt_fntend-9-7-fe-s-56` (branch
`wk-irpt_fntend-9-7-fe-s-56`), portal sub-worktree `C:/tmp/wk-irpt_fntend-9-7-fe-s-56/portal` (branch
`wk-irpt_fntend-9-7-fe-s-56-portal`).

## Half 1 -- fixtures prose

Confirmed stale at `portal/src/pages/InvestorReporting/fixtures/index.ts:77` (the `directory.unknown-cohort.json`
row). Cross-checked against `header/ScopeSummary.tsx:9-14`'s own docstring (FE-s-48, round-7 analysis item 6):
"a value the panel declines to assert is withheld, not unknown. An asserted UNKNOWN token keeps rendering as
'unknown'." Read the fixture's own data (`fixtures/directory.unknown-cohort.json`): its three cohort entries all
carry `authoritative: false` (the non-authoritative case, not an asserted UNKNOWN token), so `ScopeSummary`'s
withheld-rendering branch (`:70`, `:119-120`) is the one that fires -- the fixture's JSON data did not need a
matching change, only the prose describing it. Changed the `proves` string from "unknown renders as unknown,
never as false and never as Client" to "renders as withheld, never as unknown, never as false and never as
Client".

## Half 2 -- fe-s-14 control re-point

**First act:** ran `bun test __tests__/fe-s-14/allowlist.test.ts` at HEAD. It passed (5 pass / 0 fail) and its
`FIRMACCESS DIFF` test already printed `+0 -3` against `RETIREMENT_BASE` (`1f3ce9f0`) -- consistent with FE-s-49's
retirement of the three-firm grant. So that assertion (F14-AC3's main diff check) is already the correct,
re-pointed control the round-8 analysis describes -- confirmed, not edited.

**Search of the rest of `__tests__/fe-s-14/`:** read `published-map.test.ts`, `header.test.ts`, `one-firm.test.ts`,
`envelope.test.ts`, `gen-maps.ts` and `ambient-shims.d.ts` in full. None of them contains a committed-tree
git-diff control (no `execSync`/`git diff --numstat` call anywhere in those five files) -- so there is no
*different file* carrying a stale committed-tree-diff control.

**The stale control is inside `allowlist.test.ts` itself, in a DIFFERENT test than the one the issuer cleared.**
The `FIRMACCESS DIFF` test (F14-AC3, first sub-test) is correct. Its sibling, the `POSITIVE CONTROL: the numstat
reader is not a constant` test (same file, `:116-127`), was left byte-unchanged by FE-s-49 amendment 1 (its own
bound text, quoted in the already-filed row `IRPT_FNTEND-W2-S35`: "the positive control... stay unchanged").
That control diffs `BASELINE` (`edab15b5`) against the working copy for an UNRELATED file (`index.tsx`) and
refuses only a numstat starting `3\t0\t` -- the shape of the RETIRED grant's original addition (`+3 -0`, this
file's own docstring lines 5-8: "+3 -0 against edab15b5"). Since FE-s-49's re-point, the main test's expected
value is `+0 -3`, and the control's one-sided check does not refuse a reader stuck answering `0\t3\t...`
regardless of its arguments -- exactly the value the main test now wants. **That is the "known pair ... GAINED 3
entries" the round-8 analysis names**: the control's refused shape is the OLD (`+3 -0`, gained) pair, stale
against the NEW (`+0 -3`, retired) pair the re-pointed test now expects, so a constant-`0\t3` reader "can return
an answer the test would refuse" -- refused by nothing, because the control only ever watched for the opposite
constant.

**Fix:** added a second assertion to the POSITIVE CONTROL, refusing a numstat starting `0\t3\t` as well as
`3\t0\t`, so the control now discriminates against a reader stuck at EITHER shape (`allowlist.test.ts:129`).

**Discrimination (mutant), run and reverted before commit:** with the control's `raw` value temporarily replaced
by the literal string `'0\t3\tsrc/pages/InvestorReporting/index.tsx\n'` (a reader that always answers the
main test's expected shape, ignoring its arguments):
- with the FIXED control (both assertions active): `1 fail` -- `expect(line.startsWith('0\t3\t')).toBe(false)`
  received `true`, refused as intended.
- with only the OLD assertion active (`3\t0\t` check alone, the new one commented out): `5 pass / 0 fail` --
  the same mutant passed cleanly, proving the pre-fix control was blind to this exact defect.

The file was then restored to its final, intended state (`git diff` shows exactly the two-line prose comment
expansion plus the one added `expect` line; re-run after restoring: 20 pass / 0 fail across the whole
`fe-s-14/` directory).

## Whole-suite residual (F56-AC5)

`bun test src/pages/InvestorReporting` reads a stable 1-fail residual, unrelated to this cell's grant:
`__tests__/fe-s-49/admin-gate.test.ts` F49-AC8 finds 2 unrelated `App.tsx` hunks (an `ArrowLeftRight` icon
import and a `/trade-submission` route) from `2.0.0_SA_COO~D`'s `c29a8b86` still present at HEAD, where its own
assertion expects 0. Neither `App.tsx` nor `__tests__/fe-s-49/` is in this order's `<paths>`. Two other failures
present on the FIRST full-suite run (`fe-s-45` F45-AC2 / F45-AC10, port-bound dev-server spawns) cleared on the
SECOND full-suite run with no source change in between, consistent with already-filed rows
`IRPT_FNTEND-W1-S67`/`W1-S69` documenting that battery's load/port sensitivity. Filed as
`IRPT_FNTEND-W6-S2` (new row; F49-AC8's residual was not previously filed under that criterion name). F56-AC5 is
graded FAIL by its printed output as measured -- the whole-suite invocation is exactly as the order names it, and
the residual is out of this cell's grant to fix.

## Acceptance summary

| id | verdict | note |
|---|---|---|
| F56-AC1 | PASS | `tsc -b --noEmit`, rc=0 |
| F56-AC2 | PASS | line 77 now matches `withheld` |
| F56-AC3 | PASS | fe-s-1 fixtures.test.ts: 9 pass / 0 fail |
| F56-AC4 | PASS | fe-s-14/: 20 pass / 0 fail (after the control fix) |
| F56-AC5 | FAIL (out-of-grant residual) | 586 pass / 21 skip / 1 fail of 608; the 1 fail is `fe-s-49` F49-AC8, unrelated to `fixtures/index.ts` or `fe-s-14/` |
| F56-AC6 | RECORDED, no verdict (judgment) | material above |
