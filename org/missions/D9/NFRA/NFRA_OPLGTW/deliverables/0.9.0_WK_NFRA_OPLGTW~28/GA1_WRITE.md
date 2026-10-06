# OG-ga-1 step 6 -- the grant write (2026-10-06)

Recheck before the act: `python ga1_state.py --before` read the same record as Phase A (revision 2, `describe, list, query`; byte-equal to GA1_BEFORE.json).

Command (operator role `opal-gateway-access-admin`, assumed in the process environment only):
`schwab_entitlement_admin.py activate --candidate <X>/candidate.json --approver "Andrew Berman" --source-authorization "org/tier1_exec/2.0.0_SA_COO~O/deliverables/ANDREW_DIRECT_20261006_181xZ_S41_DOWNLOAD_FILTERED_GRANT_YES.md@ca460bf9fe" --summary "S41: add download_filtered to the dim_asset grant"` -- rc=0.

Printed scope change line: `operations: {'added': ['download_filtered'], 'removed': []}` (every other dimension added=[] removed=[]; the full output stays off-repo because the diff names account ids).

```
ACTIVATED profile_revision=3 grant_revision=3
```
