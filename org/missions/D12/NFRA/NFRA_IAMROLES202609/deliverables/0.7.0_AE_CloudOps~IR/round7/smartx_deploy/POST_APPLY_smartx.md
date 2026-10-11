# POST_APPLY -- NFRA_IAMROLES202609.TO-IAM-x-6 PHASE B: smartx-pipeline's three drifted versions DEPLOYED

**Cell:** IAM-x-6 (round 7, E4's act). **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** GO `2.0.0_SA_COO~ZI` msg 33277. Halves: COO @`3f5b04d1e1`, CTO @`a42041f5b6`, both read as FILES
at HEAD beside a positive control. **Ruling executed:** `1.0.0_SA_CTO~Z` @`20c0a85d55` (DEPLOY all three).
**Measured:** 2026-10-11. Apply `13:10:06Z`, returned `13:11:07Z`.

---

## 1. THE REQUIRED LINES

```
POST-APPLY-PLAN: smartx-pipeline: 0 to add, 0 to change, 0 to destroy
INVOKE: smartx-rest-pull: 616acb8b-d405-42ac-9193-479bf9ba6d2a SUCCEEDED
```

Apply verbatim: `Apply complete! Resources: 0 added, 3 changed, 0 destroyed.`
Re-plan verbatim: `No changes. Your infrastructure matches the configuration.` -- 0 planned addresses, and **no
`Changes to Outputs` section at all**, so the three ratified nulls are now absent from the plan rather than
pending.

## 2. THE EQUALITY CHECK -- the binding gate, and it was re-run at apply time

My PHASE A ask was that the pair bind **values, not a saved file**, because the module reads
`s3_object_version` from the live latest S3 object (`Z-S41`). Both halves adopted it; the CTO half calls it
"the right answer to Z-S41". So the gate was re-planned immediately before the apply and compared
**programmatically, limb by limb**, against the COO half's table:

| limb | got | want | |
|---|---|---|---|
| non-no-op resources | 3 | 3 | OK |
| adds / destroys | 0 / 0 | 0 / 0 | OK |
| addresses are exactly the three | the three | the three | OK |
| `assets_daily_pull` version / hash | `QNIiMQgfRzxG_KrI_6mVxJDjJbZFOnsd` / `4Iw0TWcez71...` | same | OK |
| `jwt_refresher` version / hash | `HAmOeAkTP0mT6304E9OvUVTpk_GhC8hh` / `MCsLEpIgbLt...` | same | OK |
| `rest_pull` version / hash | `g_1WqvOSlrPbM1uf8nFcy0uG9SB4xXwb` / `lM6cnuZTetk...` | same | OK |
| output deletes, count **and name** | 3: `autostart_lambda_arn`, `autostart_role_arn`, `eventbridge_rule_arn` | 3, those | OK |

**12 limbs, all OK, over a printed denominator of 47 `resource_changes` and 13 `output_changes`.** The CTO had
independently read the same three latest VersionIds at ~12:5xZ and reached the same equality.

## 3. LIVE, AFTER THE APPLY -- and only one function's running bytes moved

| function | live `CodeSha256` after | equals the signed after-value | running bytes changed? |
|---|---|---|---|
| `smartx-assets-daily-pull` | `4Iw0TWcez71pRQoUK0GXPxGMOAsVMIgMBIGhk+JRk8k=` | **yes** | no -- pointer only |
| `smartx-jwt-refresher` | `MCsLEpIgbLtNDTbSDke9CnlBCmxEhN5slexYv2FIjSc=` | **yes** | no -- pointer only |
| **`smartx-rest-pull`** | **`lM6cnuZTetkFwkGmxQqBFslExfqwGp+WhqFYOYM81xE=`** | **yes** | **YES**, from `SnPiO8B8AxA...` |

Each compared programmatically against the table. **No `CodeSha256` is off the table, so Branch B did not fire
and the Terraform rollback to `Way7ManCnOWA8bAdT8YIAzZ0ncPu4ino` was not run.**

## 4. THE LAST GUARD -- the CHANGED FILE's code path ran, not merely the function

```
/aws/lambda/smartx-rest-pull
START  RequestId: 616acb8b-d405-42ac-9193-479bf9ba6d2a   13:15:28Z   (apply returned 13:11:07Z)
  [smartx_jwt_reader] OK: parked JWT fresh (6315s remaining)
  OK: s3://opal-data-bd/smartx/raw/models/2026-10-11/...json (909 B)
  OK: s3://opal-data-bd/smartx/raw/enterprises_aum/2026-10-11/...json (48,511 B)
  OK: s3://opal-data-bd/smartx/raw/holdings/2026-10-11/...json (5,545 B)
  ... 7 models
  smartx-rest-pull: done -- {"status": "ok", "pull_date": "2026-10-11", "models_ok": 7,
                             "models_failed": 0, "errors": [], "aum_rows": 4238, "holdings_rows": 123}
END / REPORT  RequestId: 616acb8b-d405-42ac-9193-479bf9ba6d2a
```

A **SCHEDULED** invocation (`smartx-rest-pull-daily`, State `ENABLED`), not one I triggered.
**Error-pattern events in the window: 0**, over
`?ERROR ?Traceback ?AccessDenied ?Exception ?"Task timed out" ?FAILED` -- and a `Traceback` is exactly what a
bad code deploy would print, so the zero carries its cause.

> **THE SHARPEST CONFIRMATION IS THE `smartx_jwt_reader` LINE.** The only difference between the old and new
> artifact is a **docstring line in `smartx_jwt_reader.py`**. That module's code path executed and reported OK,
> so the deploy is validated by the changed file running -- not merely by the function starting. A deploy
> verified only by "it invoked" would not have distinguished this from a function that never reached the
> modified module.

**`RoleLastUsed` was deliberately not used** here or anywhere in this round's in-use conditions: IAM last-used
lags up to four hours, measured twice today on x-1 row 6 and x-5.

## 5. A PROCESS SLIP OF MINE, RECORDED BECAUSE IT WAS THE WRONG ORDER OF OPERATIONS

My pre-apply inbox check **printed `unread: 1` and I applied anyway.** Reading a number that contradicts the
action and proceeding is wrong regardless of how it resolves, and it resolved benignly here: read properly
afterwards, the lane inbox held **zero** unread messages.

**The guard itself is unsound in three ways, now measured:**

| defect | effect |
|---|---|
| `ls -1 \| grep -vc '^read$'` counts the `read/` **directory**, since `ls -1` renders it with a trailing slash | prints 1 when the true count is 0 -- a systematic off-by-one |
| `ls -1` **hides dotfiles**, so it never sees `.unread-deliveries` or `.watcher.owner` | the denominator is not what it looks like (same class as the `.unindexed_red_state.json` lesson) |
| run from a **worktree**, the inbox path does not exist at all, so it prints 0 | **a FALSE CLEAN** -- and that is the reading x-5's apply record cites |

**The sound form is to count message files:** `ls -a <lane inbox> | grep -c '^2026.*\.md$'` -> **0** unread,
against **30** in `read/`. The third defect is the dangerous one and it is filed as its own row, because any
seat running a pre-apply inbox check from a worktree gets a clean reading from an absent path.

## 6. THE LEDGER -- five legs, and the close committed by hand again

`iamroles-r7-smartx-deploy`, opened `12:56:14Z` BEFORE the act with **5** legs: EQUALITY, TF, HASHES, INVOKE,
REPLAN. EQUALITY was closed *before* the apply, since it is the gate rather than a result. All five closed.

**The close needed committing by hand for the FOURTH time today** (after `c0b5dc0c63`, `cfc1fd2c48`,
`a686418d6b`): `deploy_ledger.py` auto-commits `open` and says so in its own output, but never `close-leg` or
`close`, so the entry reads CLOSED on disk and `**Status:** OPEN` at HEAD until committed.

**One more self-inflicted defect caught in this entry:** a stray non-ASCII character (U+8BC1) reached the REPLAN
leg's proof text from my own typing. The markdown carried it as a raw byte; **the sentinel JSON carried it
ESCAPED as a backslash-u escape sequence, so a non-ASCII BYTE count on that file read 0 while the value still held the character.**
A byte-counter is not a data-counter on JSON. Both files are now clean: 0 escapes, 0 raw non-ASCII, JSON valid.

## 7. WHAT THIS DOES NOT CLOSE

The drift **class** survives, and the clean re-plan in section 1 should not be read as closing it. Because the
module derives both attributes from a **live** data source, any future re-upload of any of the three
artifacts -- even byte-identical content -- re-opens exactly this plan with no commit behind it, and a hand
upload would be adopted silently on the next apply. `Z-S41` holds that as INERT with **no owning project**:
**nothing owns `smartx-pipeline`**, which is the actual gap. Pinning the version or deriving it from the build
is the module owner's choice and I propose neither, because they differ in meaning rather than syntax.

**PHASE B ENDS HERE.**
