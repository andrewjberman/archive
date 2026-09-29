# IRPT_BCKEND.TO-IB-m24-241 -- directory bundle ships schwab_account_codes (row S217)

`0.9.0_WK_IRPT_BCKEND~82`, round 24 workstream ~M, direct act, cell `IB-mr-241`.

## What was done

Added two members to the `investor_reporting` bundle's `members` dict in `.tools/safe_deploy_core.py`
(commit `e40685bd00505bb2a20fb50aef27d9410fd746a3`):

```
"data/assets/scripts/gold/investor_reporting/schwab_account_codes.py": {
    "repo_path": "data/assets/scripts/gold/investor_reporting/schwab_account_codes.py",
    "sha_metadata_key": "schwab-account-codes-sha256",
},
"data/assets/scripts/gold/investor_reporting/schwab_account_codes.json": {
    "repo_path": "data/assets/scripts/gold/investor_reporting/schwab_account_codes.json",
    "sha_metadata_key": "schwab-account-codes-json-sha256",
},
```

Updated the closure comment above the entry: "8 files" -> "10 files", the two-import line -> three
(ids, trading_calendar, schwab_account_codes), and a new paragraph naming why both files are needed
(directory_runner.py's module-level `import schwab_account_codes as _sac`, row S217) and why the pair
extracts side by side (schwab_account_codes.py reads its JSON via `Path(__file__).resolve().parent`;
members are stored at their repo paths, both of which share
`data/assets/scripts/gold/investor_reporting/`). Read `schwab_account_codes.py` whole to confirm the
relative-path read (step 2 of the order) -- confirmed, no other path form used.

## Checks run

1. `python org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_M/R24_CHECKS/r24_directory_bundle_imports.py`
   -> `BUNDLE-IMPORTS 12 members`, rc=0 (criterion IBM24-241-AC1). Before the fix (base commit
   `78b1b7458f`): `NOT-IMPORTABLE: module-level sibling imports not in the bundle: ['schwab_account_codes']`,
   matching the task order's recorded dry-run.
2. `python -m pytest data/assets/scripts/gold/investor_reporting/tests -q -p no:cacheprovider` ->
   314 passed in 68.94s, rc=0.
3. `python -m py_compile .tools/safe_deploy_core.py` -> rc=0.

## Scope

Only the `investor_reporting` bundle entry's `members` dict and its closure comment were touched;
nothing else in the entry (bucket, s3_key, other members) changed. LOCAL only -- no upload, no
`--mint-bundle`, no push, per BOUNDS.

No surprises filed: every premise in the task order held (10 -> 12 member count, relative-path JSON
read, side-by-side extraction from repo-path storage).
