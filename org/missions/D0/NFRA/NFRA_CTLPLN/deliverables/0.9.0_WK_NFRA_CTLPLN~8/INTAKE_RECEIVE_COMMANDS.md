# INTAKE_RECEIVE_COMMANDS -- what a receiving machine runs for one delivered pack

Tool: `org/devices/intake/intake_receive.py` (standard library only; Python 3.12 and 3.14). It makes no network request
and has no flag that adds an index. Set the device name first: `AGENTBUS_DEVICE` must be set (for example `dell1`); the
tool refuses to write a receipt without it. Replace `PACK` with the folder the pack was carried to (it holds the wheels,
each wheel's `.check.json` and `.delivery.txt`, and `MANIFEST.json`). Use the Python 3.14 interpreter on the Dells.

1. Verify the pack (read-only):

       python org/devices/intake/intake_receive.py verify --from PACK

   LAST line: `INTAKE-VERIFY pack=<dir> wheels=<n> verified=<v> checked=<c> stray=<s> ok=<True|False>`.
   `verified` = wheels whose bytes match the manifest; `checked` = wheels whose check record clears them (verdict
   "checked", same name, same SHA-256, eight checks numbered 1 to 8, check 8 "passed"); `stray` = files in the folder
   the manifest does not list. `ok=True` needs all wheels verified and checked and `stray=0`. Stop here on `ok=False`.

2. Prove into a NEW, EMPTY scratch folder (not inside PACK):

       python org/devices/intake/intake_receive.py prove --from PACK --scratch SCRATCH

   Each wheel is installed with `python -m pip install --no-index --no-deps --target SCRATCH/<file stem> <wheel>`, then
   each top-level module is imported in its own isolated subprocess. A receipt per wheel is written to `PACK/receipts/`.
   LAST line: `INTAKE-PROVE device=<name> python=<version> wheels=<n> installed=<i> imported=<m> import_missing_dep=<d> failed=<f> refused=<r> ok=<True|False>`.
   `installed` = pip succeeded; `imported` = every top-level module imported; `import_missing_dep` = installed but the
   import wants a package that is not in the pack (a finding, not a fault); `failed` = pip install failed;
   `refused` = not installed because verify failed for it. `ok=True` means nothing was refused and nothing failed to
   install. A line `INTAKE-PROVE-DETAIL import_failed=<k> no_module=<z>` just above it counts wheels whose own module
   failed to import and wheels with no importable module.

3. Send the receipts back: copy the folder `PACK/receipts/` to the issuer (the `*.receipt.<device>.json` files). Nothing
   else leaves the box, and nothing is written into a git tree.

4. Real install, on the box's own decision after reading the receipts (optional dry run first):

       python org/devices/intake/intake_receive.py install --from PACK --dry-run
       python org/devices/intake/intake_receive.py install --from PACK

   Same pip command with `--user` in place of `--target`. Refused (nothing installed) unless the pack verifies and every
   wheel has a receipt from THIS device, matching its bytes, reading `installed_imported` or `installed_import_failed`
   with only `import_missing_dep` causes. LAST line:
   `INTAKE-INSTALL device=<name> python=<version> wheels=<n> installed=<i> refused=<r> dry_run=<bool> ok=<bool>`.

Control: `python org/devices/intake/intake_receive.py selftest-unchecked` builds a synthetic pack in a temporary folder
with one wheel whose record reads "not_checked" and must end `installed=0 ... refused=1`; it leaves nothing behind.
