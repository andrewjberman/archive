# FE-s-47 result -- a response with no status says why its state is unknown

Worker `0.9.0_WK_IRPT_FNTEND~3`, order `IRPT_FNTEND.TO-FE-s-47`, round 8, issued by `2.0.0_SA_COO~F`.
Portal branch `wk-irpt_fntend-8-3-fe-s-47` at `f4b9ce89` (LOCAL; portal FROZEN, never pushed).
Workspace branch `wk-irpt_fntend-8-3-fe-s-47` (LOCAL).

## 1. Verdict

- **All 9 mechanical criteria (AC1 to AC9):** PASS by output at the final portal HEAD `f4b9ce89`.
- **AC10:** recorded for L9, with no verdict.
- **AC9's disclosure.** Its whole-suite census passed on run 4, the deciding run at the final HEAD. Runs 1 to 3 read red, and F41-AC5's CONTROL timed out on each of them.
  - That test is outside this grant and in FE-s-46's cell. It was not edited.
  - Row `IRPT_FNTEND-W3-S40` records it: OBSERVATION, ARMED, disarm_owner `0.9.0_WK_IRPT_FNTEND~1`.

## 2. The change (portal `8243b44b`, `contracts/adapt.ts`, the only non-test file changed)

```diff
@@ export const EXPLICIT_UNKNOWN_STATE: EnvelopeState = 'UNCERTAIN'
+export const NO_STATUS_REASON = 'The response carried no status stating its state, so its state is unknown.'
@@ export function carryAvailabilityFromStatus<T>(view: T, status: StatusEnvelope | null): T {
+  const statedState = status?.state ?? null
   const availability: Availability = {
-    state: status?.state ?? EXPLICIT_UNKNOWN_STATE,
+    state: statedState ?? EXPLICIT_UNKNOWN_STATE,
     sourceAsOf: status?.sourceAsOf ?? current.sourceAsOf,
-    partialReason: current.partialReason,
+    partialReason: statedState === null ? NO_STATUS_REASON : current.partialReason,
```

- The constant is declared once (`adapt.ts:176`). It is used once in production code (`adapt.ts:305`), and the test imports it.
- The words are plain and public. They name no host, no principal and no component, and they are not a `publicReasonCode`.
- The reason is supplied at the carry, which is the one place that knows whether the response stated a state. It is not supplied in `wireEnvelope`, so a stated state can never inherit it (the hazard the order names).
- `contracts/validate.ts` is unchanged. Its blob is `4fc0a042ae9c8bc02cef78af409a60e1628cc7e7` at HEAD and at DEV `1f3ce9f0`.
- Test files:
  - `__tests__/fe-s-47/no-status-reason.test.ts`, 7 tests.
  - `__tests__/fe-s-47/ambient-shims.d.ts`, type-only, with declarations copied character for character from fe-s-41 and fe-s-1.

Portal commits, all LOCAL:

- `8243b44b` -- the fix and the test.
- `fffb8454` -- the test reads each committed blob once. Run 1 timed F47-AC6 out at 10828 ms, with its bar already printed.
- `f4b9ce89` -- the line `F47-AC2 PROBLEMS: []` becomes `F47-AC2 VALIDATE -> problems list: []`. The proof checker's count-bar limb had read the `2` of `AC2` as a count (row W3-S41). Output label only.

## 3. Criteria (deciding runs, portal f4b9ce89, `IRPT_FE_DEV_PORT=5263` measured closed)

| id | deciding reading |
|---|---|
| F47-AC1 | `rc=0` |
| F47-AC2 | `... READS 0 PROBLEMS: yes`. The carried state is UNCERTAIN, the carried partialReason is the constant, and the problems list is `[]` |
| F47-AC3 | `A STATED STATE NEVER CARRIES THE NO-STATUS REASON: 11 of 11`. Nine directory-search arms, one per contract wire state; READY, QUEUED and RUNNING carry no reason code, and the other six carry the instance's code. Two resolve-scope arms carry the document's own partial_reason exactly |
| F47-AC4 | `THE SAME DOCUMENT WITH ITS REASON STRIPPED IS REFUSED: yes`, with the refusal `DirectoryEntry[0].availability: state 'UNCERTAIN' carries NEITHER partialReason NOR publicReasonCode` |
| F47-AC5 | `validate.ts UNCHANGED FROM DEV 1f3ce9f0: yes`. Both blob ids are `4fc0a042...`, and the working copy is clean |
| F47-AC6 | `... CARRIES ITS REASON: 18 of 18`. The census subtracts 28 of 29 sites and keeps 1 |
| F47-AC7 | `NO STATUS-OPTIONAL OPERATION IS REFUSED FOR A REASONLESS UNCERTAIN: 9 of 9`. Of 11 status-optional operations, 2 slices carry no availability, leaving 9. The control, with every reason stripped, is refused 9 of 9 |
| F47-AC8 | `THE MOUNTED STATUS PANEL SHOWS THE NO-STATUS REASON: yes`. AnswerStatus renders `Uncertain Qualified answer -- not a complete report Business date 2026-09-09 The response carried no status stating its state, so its state is unknown.`, and the control renders `... No reason stated` |
| F47-AC9 | `567 pass`, `18 skip`, `0 fail`, `Ran 585 tests across 103 files. [75.61s]` (run 4) |
| F47-AC10 | RECORDED, no verdict (L9, 3.0.0_SA_CVO) |

FE-s-47's 7 bar lines are identical at fffb8454 and f4b9ce89, and they read the same at 8243b44b.

Whole-suite runs:

| run | portal | pass / skip / fail of total | red tests |
|---|---|---|---|
| 1 | 8243b44b | 564 / 18 / 3 of 585 | F41-AC5 CONTROL 6000 ms; fe-s-13 `producer fixtures` 5265 ms; F47-AC6 10828 ms (this order's own, fixed at fffb8454) |
| 2 | fffb8454 | 566 / 18 / 1 of 585 | F41-AC5 CONTROL 6609 ms |
| 3 | fffb8454 | 566 / 18 / 1 of 585 | F41-AC5 CONTROL 6641 ms (the re-run the order grants) |
| fe-s-41 alone | fffb8454 | 10 / 0 / 1 of 11 | F41-AC5 CONTROL 5625 ms |
| 4 | f4b9ce89 | 567 / 18 / 0 of 585 | none (the deciding run) |

Run 4 was not a third re-run. Commit `f4b9ce89` moved the HEAD, and the census of record has to be read at the final HEAD.

The issuer's probe read 559 / 18 / 1 of 578. This order adds 7 tests, making 585. FE-s-47 turned no existing test red: every red test on every run was a timeout in fe-s-41 or fe-s-13, or this order's own F47-AC6 on run 1.

## 4. F47-AC6: the subtraction, from the committed tree

- **Census.** `git grep -n -E "EXPLICIT_UNKNOWN_STATE|'UNCERTAIN'|\"UNCERTAIN\"" HEAD` over the whole committed portal tree returns 65 lines. 36 are under `__tests__/` and 29 are outside it.
- **Buckets, 29 sites in all.** Each line is printed with its reason, and a line no rule covers is UNCLASSIFIED and breaks the bar.
  - NOT A WRITE: 15. Comments, the constant's declaration, imports, reads, and vocabulary lists or unions.
  - NOT A STATE: 3. Finding severities.
  - STATED, NOT SUPPLIED: 7. `STATE_FOR_WIRE`'s rename of a producer-stated UNCERTAIN, and six committed fixture documents that state it themselves.
  - NOT AN AVAILABILITY: 2.
    - `envelope.ts:233`: IrParsedEnvelope's own `state`. The test reads the committed interface to confirm it has no reason member.
    - `export/submit.ts:220`: a TabEnvelope inside `envelopeFromReceipt`. The test reads the enclosing signature.
  - OVERWRITTEN on every in-contract response: 1, `wireEnvelope` (`adapt.ts:237`).
    - Through a document adapter, a stated status replaces the state on 9 of 9 operations whose document carries an availability.
    - Through the status member, 9 of 9 contract states map to a stated view state.
    - The off-contract residue is printed and filed: a status with its required `state` missing keeps the default on the status's own availability (row W3-S37).
  - KEPT: 1, the carry (`adapt.ts:301`).
- **Reach of the kept site.** It was run on every operation whose document carries an availability, under both of the ruling's triggers (no status; a status with no state): 18 of 18 carry the reason. `analysis-requests` is refused by the parser before anything is adapted, because it requires a status.
- **The negative arm.** Before the fix was committed, the same census read HEAD's old carry line as UNCLASSIFIED, and the bar printed `17 of 18`. The read of the committed tree can say no.

## 5. Rows filed (INVESTIGATION_v2.md)

- `IRPT_FNTEND-W3-S36`: OBSERVATION, INERT. The wire instances have no `status` member to remove, because they are documents, not envelopes. The test wraps each in a v1 envelope and removes status.
- `IRPT_FNTEND-W3-S37`: OBSERVATION, INERT. A status member that omits its required state keeps wireEnvelope's reasonless default on its own availability. Fixing that means changing adaptStatusEnvelope, which is outside the grant.
- `IRPT_FNTEND-W3-S38`: OBSERVATION, INERT. On status-summary and status-job with no envelope status, the carry overwrites the status document's own PARTIAL on its availability. validate reports the disagreement, and this predates FE-s-47. It is the "other problem" F47-AC7 prints.
- `IRPT_FNTEND-W3-S39`: OBSERVATION, INERT. With no status, resolve-scope's own partial_reason on its availability is replaced by the constant, which follows the ruling's wording. The order does not say which reason wins; the top-level `ResolvedScope.partialReason` keeps it.
- `IRPT_FNTEND-W3-S40`: OBSERVATION, ARMED, disarm_owner `0.9.0_WK_IRPT_FNTEND~1`. F41-AC5's CONTROL made the whole-suite census red on 3 of 4 runs, and it also timed out run alone. The census passes or fails with the box's load, and fixing that is FE-s-46's cell.
- `IRPT_FNTEND-W3-S41`: OBSERVATION, INERT. proof-of-spec-check's count-bar limb reads the digit that ends a criterion id as a count (`.tools/proof-of-spec-check.py:1529`). I relabelled the test's line and edited nothing in `.tools/`.

## 6. Notes the order asks for

- **`contracts/envelope.ts:231` is stale.** It says `status_required` is false on "ten of the twelve" response contracts. The committed `RESPONSE_STATUS_REQUIRED` marks 11 of 12 false, and only `analysis-requests` is true (F47-AC7 prints this). Not edited: envelope.ts is not in this grant.
- **Page.tsx.** `render/Page.tsx:160` (`reasonText: nonEmpty(availability.partialReason)`) reads the same field AnswerStatus renders. It was not mounted separately; F47-AC8 mounts AnswerStatus, which the order names as its example.
- **Portal commit mechanics.** `git commit -- <paths>` cannot name an untracked file, so the three named paths were `git add`ed first for `8243b44b`. Only those three were added, and nothing else in the worktree was staged.
- **Line endings.** The channel's worktree copy was CRLF (index LF, `core.autocrlf=true`). The file is written as its committed blob plus the six rows, with `newline='\n'`, and the diff shows insertions only.
