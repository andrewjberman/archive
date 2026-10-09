# CN-q-2 portal paths, round 5 -- 49financial

Source: `python lib/opal_portal_paths.py 49financial --json` (row `infra/logic/registry/scopes.json` key `49financial`; surfaces portal=true, mdpf=true, pipeline=true).

Derived + carded = the 8 paths `FIRM_ALLOWED_PATHS['49financial']` carries today (portal/src/lib/firmAccess.ts, read only).

## Derived (1)

- `/portfolios` -- the row's `tenant.surfaces.mdpf` is true; `/portfolios` is the page App.tsx routes to ModelPortfolios, which asks `/api/general/mdpf/{firmId}/...` (the scoped-route pattern of MDPF_CANON PRD DEC-5 FWD-2, here `/api/general/mdpf/49financial/...`).

## Carded (7)

owner of every card: Andrew. Reason, same for each: no rule maps a surface to this page: portal/src/App.tsx routes it with no firm slot and no surface marker, and the only surface-to-page mapping the estate states is mdpf -> /portfolios; granting the page is a product ruling recorded in portal/src/lib/firmAccess.ts, owned by Andrew.

| path | owner | why carded |
|---|---|---|
| `/advisor-intelligence` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/macro` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/market` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/philosophy` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/positioning` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/trade-submission` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |
| `/valuations` | Andrew | no surface-to-page rule produces it; App.tsx gives it no firm slot and no surface marker |

## Notes

- The `portal` and `pipeline` surfaces map to no page by any stated rule, so they derive nothing.
- No path is both derived and carded; an unknown firm and a MASTER row both exit 2 (`REFUSED`).
