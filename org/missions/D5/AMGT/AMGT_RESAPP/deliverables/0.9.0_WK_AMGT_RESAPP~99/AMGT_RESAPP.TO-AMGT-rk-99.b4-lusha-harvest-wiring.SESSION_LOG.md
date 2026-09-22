# Session log -- `0.9.0_WK_AMGT_RESAPP~99` on `AMGT-rk-99` (round 25, B4 wiring)

Worktree `C:/tmp/wk-amgt-25-99`, branch `wk-amgt-25-99`, base `83d7edfe7d`.

1. First act: `git rev-parse --abbrev-ref HEAD` -> `wk-amgt-25-99`; `org/` and `.tools/` present -- TREE-OK.
2. Read the task order in full. Read `lib/research/harvest/lusha.py` and `lib/research/management/enrich.py`
   at the branch HEAD to confirm the measured state (line 264/659 content, KEPT_FIELDS, the three
   `_lusha_client` patches, the two guard tests) matched the order's text.
3. Snapshot working-tree bytes of both modules to `.scratch/r99/*.orig` (mutation discipline).
4. Wrote `.scratch/r99/ac0.py`, `ac4.py`, `ac5.py` byte-for-byte from the order.
5. Ran AC0 BEFORE any edit -- baseline: `pin_object commit`; `enrich_264`/`enrich_659` content matched;
   `production_lusha_writer_calls 0 []`; `existing_private_patches 3`; both modules `crlf 0 non_ascii_chars 0`;
   harvest suite `64 passed`; management suite `95 passed, 13 subtests passed`.
6. Added `enrich.lusha_client(api_key=None, client=None)` in `enrich.py` -- a thin wrap that looks up
   `_lusha_client` BY NAME at call time and returns its result unchanged; `_lusha_client` and
   `build_document` untouched.
7. Added `datetime` import, `_assert_no_contact_field(rows)` (the C-LUSHA-EXCEPTION guard),
   `harvest_company(...)` and a `_cli` (not run) to `lusha.py`; updated the module docstring from
   "NOT WIRED" to name `harvest_company` as the wired entry point.
8. Wrote `lib/research/harvest/tests/test_lusha_harvest.py`, 8 tests per AC1's named list, each deleting
   `LUSHA_API_KEY` and patching `enrich._estate_module` to raise if reached, with a stub Lusha client
   counting `_execute`/`contacts_prospecting` calls and a recorder in place of `lusha.write_contact_match`.
9. Ran AC1 (`test_lusha_harvest.py -v`) -- 8 passed, all 8 named tests PASSED.
10. Committed the three code/test files (`4a6255f6b512361d08fcd3e6f86e199f6f0252db`) so AC4/AC5's
    `git diff <pin> HEAD` has a real HEAD to diff against.
11. Re-ran AC2 (harvest suite, 72 passed = 64+8), AC3 (management suite, 95 passed/13 subtests, unchanged),
    AC4 (`changed_code_files` exactly the three files; `enrich_removed_lines 0`; `enrich_added_defs`
    exactly `['+def lusha_client(api_key=None, client=None):']`; `existing_private_patches 3`, unchanged
    from AC0's P0) and AC5 (all three files compile, 0 CRLF, 0 non-ASCII) -- all PASS.
12. Ran `py_compile` and `ruff check` on the three files directly (both clean) in addition to the
    `commit-gate` checks that ran inside `safe-commit.sh`.
13. Wrote this proof-of-spec instance, validated it with this worktree's own
    `.tools/proof-of-spec-check.py`, flipped `<status>` to `complete`, and committed the deliverables
    + task-order flip in a second commit.

No Lusha call made (0). `LUSHA_API_KEY` never read (every test deletes it from the environment and
patches `enrich._estate_module` to raise if the estate client is ever reached). No AWS call, no S3
write, no install. No existing test file touched. Branch `wk-amgt-14-50` / worktree
`C:/tmp/wk-amgt-14-50` never referenced, read, shown, diffed or checked out.
