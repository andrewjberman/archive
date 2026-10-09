# PART A -- portal paths: the 7-page core plus tenant.pages (round-5 ADDENDUM 1, folded into CN-q-3)

Worker `0.9.0_WK_LGIC_CANON~1`, slot ~1. Built in `lib/opal_portal_paths.py`; tests in `lib/tests/test_opal_portal_paths.py`.
Registry rows read from `infra/logic/registry/scopes.json` @a15fb36a4c (written by 4.0.0_SA_CRO; never written here).

## The derivation

A FIRM row with `tenant.kind` `client` and `tenant.surfaces.portal` true derives the core
(`/advisor-intelligence /macro /market /philosophy /portfolios /positioning /valuations`) plus `tenant.pages`. A missing or
empty `tenant.pages` yields the core only. Nothing is carded for a page the core or `tenant.pages` holds; the scoped-route
print for surface mdpf is kept.

## The three firms' derived sets (`python lib/opal_portal_paths.py <firm>`; each rc 0, CARDED 0)

| firm | tenant.pages | derived | carded |
|---|---|---|---|
| 49financial | `/trade-submission` | 8: core + `/trade-submission` | 0 |
| inflection | `[]` | 7: the core | 0 |
| cottonwood | `/attribution /factor-tilts /trade-submission` | 10: core + the 3 | 0 |

Each derived set equals the firm's `FIRM_ALLOWED_PATHS` entry in `portal/src/lib/firmAccess.ts` exactly.

## `--check` (live, `python lib/opal_portal_paths.py --check`, rc 0)

```
SKIP demo -- tenant.kind=demo, not a client firm (10 granted pages not graded)
CHECK: firms=4 pages=35 graded_firms=3 skipped_firms=1 stops=0 OK
```

Denominators: 4 firms in the map, 35 granted pages; 3 firms graded (25 pages: 8 + 7 + 10), 1 skipped (demo, 10 pages).
On a planted page (`--access <copy with '/zz-planted-page-r5' added to 49financial>`) it prints
`STOP 49financial /zz-planted-page-r5 -- no tenant.pages entry` and exits 1.

## One judgement the order did not state (surprise row LGIC_CANON-D1-W1-S31)

The map also holds a `demo` firm (10 granted pages); its scope row is `tenant.kind` `demo` with no `tenant.pages`. The rule
(ADDENDUM 1) is stated for client firms, and the order's criterion needs `--check` to pass live. `--check` therefore grades client
firms and lists every non-client firm as SKIP with its page count, never silently. If the demo tenant is to be graded, it needs
a ruling and a `tenant.pages` row in `scopes.json` (4.0.0_SA_CRO's file).

## Bar

`python -m pytest lib/tests -q -p no:cacheprovider` -> 214 passed (base 199 passed, 1 skipped; this module 14 tests).
