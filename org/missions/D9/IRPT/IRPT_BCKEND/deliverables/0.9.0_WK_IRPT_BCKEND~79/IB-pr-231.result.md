# IB-pr-231 -- session log (0.9.0_WK_IRPT_BCKEND~79)

Task order: `IRPT_BCKEND.TO-IB-pr-231.directory-contract-account-masks.md`

## Act

Ran, from the worktree root `C:/Users/AndrewBerman/Desktop/wk-irpt-p-79`:

```
git show 27d9a8f700889f2e234c267faf02d37f6d23d9a4 > infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json
```

Verified byte-equality:

```
git hash-object infra/aws/lambda/investor-reporting/_contracts/DirectoryEntry.schema.json
-> 27d9a8f700889f2e234c267faf02d37f6d23d9a4
```

No other file touched.

## Criterion

```
timeout 120 python "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r23/p23_1_ac1_directory_contract_masks.py" .
```

Output:

```
worktree blob 27d9a8f700, want 27d9a8f700: True
account_masks defined: True | every HEAD property kept: True
P23-1-AC1 PASS
```

rc=0.

## Surprises

None. The task order's premises held exactly as stated: the blob existed in the object store, the target path
existed at HEAD, `git show` produced LF endings by default, and the checker script existed at the named path and
ran clean. No row filed.

## Controls

- Mutant: the checker's own two-arm design is the control here -- `account_masks defined` and `every HEAD property
  kept` are independently gradable; both fired True on the fix and the pre-fix base case (recorded in the task
  order) shows `account_masks defined: False`, i.e. the check discriminates the change.
- Determinism: the checker was run twice; identical output both times (blob hash, booleans, PASS line).
