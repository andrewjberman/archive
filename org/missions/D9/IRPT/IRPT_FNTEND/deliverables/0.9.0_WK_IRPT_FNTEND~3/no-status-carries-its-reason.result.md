# FE-s-47 result -- a response with no status says why its state is unknown (AMENDMENT 1)

Worker `0.9.0_WK_IRPT_FNTEND~3`, order `IRPT_FNTEND.TO-FE-s-47`, round 8, issued by `2.0.0_SA_COO~F`,
reopened by amendment 1 (`1.0.0_SA_CTO` msg 96947, RULING V; row W3-S39).
Portal branch `wk-irpt_fntend-8-3-fe-s-47` at `3e84bce6` (LOCAL; portal FROZEN, never pushed).
Workspace branch `wk-irpt_fntend-8-3-fe-s-47` (LOCAL).

## 1. Verdict

- **All 10 mechanical criteria (AC1 to AC10):** PASS by output at the amended portal HEAD `3e84bce6`.
- **AC11:** recorded for L9, with no verdict.
- **AC10** passed on its first run at this HEAD (572 / 18 / 0 of 590). F41-AC5's control (row W3-S40, FE-s-46's) did not time out.

## 2. The change (portal `3e84bce6`)

`contracts/adapt.ts`, one hunk: the carry line in the order's exact form, and its two comment lines rewritten to state RULING V.

```diff
-    // FE-s-47 (1.0.0_SA_CTO's ruling): the explicit unknown carries its reason, and ONLY
-    // it does. A stated state carries the document's own reason exactly as before.
-    partialReason: statedState === null ? NO_STATUS_REASON : current.partialReason,
+    // FE-s-47 (1.0.0_SA_CTO's ruling): the explicit unknown carries a reason, and ONLY it
+    // gets the generic one. Amendment 1 (RULING V, msg 96947; row W3-S39): the document's
+    // own stated reason is never replaced -- the constant fills only a null. A stated
+    // state carries the document's own reason exactly as before.
+    partialReason: statedState === null ? (current.partialReason ?? NO_STATUS_REASON) : current.partialReason,
```

- Unchanged from the first run: `NO_STATUS_REASON` (`adapt.ts:176`) and the stated-state logic (`:299`, `:301`).
- `contracts/validate.ts` is unchanged. Its blob is `4fc0a042ae9c8bc02cef78af409a60e1628cc7e7` at HEAD and at DEV `1f3ce9f0`.
- `__tests__/fe-s-47/no-status-reason.test.ts`:
  - adds F47-AC9;
  - F47-AC6's reach now expects the document's own reason, and `NO_STATUS_REASON` only where the document stated none;
  - the committed-blob reader takes a revision (`blobAt`), so the before arm reads `f4b9ce89:adapt.ts` as its committed blob (RULING AC).
- `ambient-shims.d.ts` is unchanged.

## 3. Criteria (deciding runs, portal 3e84bce6, `IRPT_FE_DEV_PORT=5263` measured closed in the same call)

| id | deciding reading |
|---|---|
| F47-AC1 | `rc=0` |
| F47-AC2 | `... READS 0 PROBLEMS: yes`. The carried state is UNCERTAIN, the carried partialReason is the constant (the directory document states none), and the problems list is `[]` |
| F47-AC3 | `A STATED STATE NEVER CARRIES THE NO-STATUS REASON: 11 of 11` |
| F47-AC4 | `THE SAME DOCUMENT WITH ITS REASON STRIPPED IS REFUSED: yes` |
| F47-AC5 | `validate.ts UNCHANGED FROM DEV 1f3ce9f0: yes`. Both blob ids are `4fc0a042...` |
| F47-AC6 | `... CARRIES ITS REASON: 18 of 18`. There are 69 census lines, 29 of them outside `__tests__/`; 28 are subtracted and 1 is kept. resolve-scope's 2 arms carry the document's own reason |
| F47-AC7 | `NO STATUS-OPTIONAL OPERATION IS REFUSED FOR A REASONLESS UNCERTAIN: 9 of 9`. resolve-scope now carries its own reason |
| F47-AC8 | `THE MOUNTED STATUS PANEL SHOWS THE NO-STATUS REASON: yes` |
| F47-AC9 | `A DOCUMENT'S OWN REASON SURVIVES A MISSING STATUS: yes` |
| F47-AC10 | `572 pass`, `18 skip`, `0 fail`, `Ran 590 tests across 104 files. [71.79s]` |
| F47-AC11 | RECORDED, no verdict (L9, 3.0.0_SA_CVO) |

**F47-AC9's arms:**

- **The document states its reason.** resolve-scope's committed wire instance, with no status, goes through the real `parseIrEnvelope`. The carried partialReason is `"one account of four is outside the advisor's grant"`, and validate reports no problems.
- **The document states none.** The same body with `partial_reason: null` carries `NO_STATUS_REASON`.
- **The before arm.** `f4b9ce89`'s committed `carryAvailabilityFromStatus` is cut from the blob, transpiled with `Bun.Transpiler`, and run on the same adapted document. It returns the constant, so the document's own reason was REPLACED (row W3-S39).
- **The extraction control.** HEAD's carry, cut and run the same way, equals the real parser's data.

**Negative arm.** The same test was run with the amended working copy before the portal commit, while HEAD still held the old carry. The extraction control read `BROKEN` and the bar read `no` (7 pass, 1 fail).

**Determinism.** The 8 bar lines are identical between the standalone run and the whole-suite run at `3e84bce6`.

**The whole-suite log.** It also carries one inner summary, `0 pass / 2 skip / 0 fail`, `Ran 2 tests across 1 file`, followed by `CHILD EXIT: 0`. That is a test spawning a child `bun test`. The census of record is the final summary.

## 4. Rows

No new row. `IRPT_FNTEND-W3-S36..S41` stand as the first run filed them:

- W3-S39 is answered by this amendment.
- W3-S37 and W3-S38 go to the round-8 analysis, per the amendment.
- W3-S40 is FE-s-46's, and it did not fire on this run.

## 5. Notes the order asks for

- **`contracts/envelope.ts:231` is stale.** It says `status_required` is false on "ten of the twelve" response contracts. The committed `RESPONSE_STATUS_REQUIRED` marks 11 of 12 false, and only `analysis-requests` is true (F47-AC7 prints this). Not edited: envelope.ts is not in this grant.
- **`NO_STATUS_REASON`'s docstring** (`adapt.ts:169-175`) still describes the first-run rule, that the constant is carried whenever a response stated no state. The amendment keeps the constant as committed, so the docstring was left alone. The carry's own comment states the amended rule.
- **Page.tsx.** `render/Page.tsx:160` reads the same field AnswerStatus renders. It was not mounted separately.
- **Portal commit mechanics.** A pathspec commit of the two tracked files that changed, authored `0.9.0_WK_IRPT_FNTEND~3`.
