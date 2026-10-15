# The F-SHIP candidate: registration ready, waiting on a served 49 Financial sample (2026-10-15 ~09:3xZ)

Issuer `2.0.0_SA_COO~F2`. The CTO's rulings (F-SHIP round-114 analysis ruling 3; round-116 analysis ruling 1): the candidate is registered for approval (client-facing, Andrew) once the route serves a 49 Financial sample on
DEV, at the head that passes its own criterion; a candidate that fails its own criterion is never registered.

## The candidate

- Branch `cand/dell2/irpt-default-performance-report` in the portal repo, head `65f2e5430bc87924a081c7b4c87d1825849bf9ca`: 30 commits over `origin/PROD` (`5d646418`), local, not pushed.
- What it carries: the default performance report (the 20 round-94-111 commits), the reader and the Performance tab mount (round 114), the export mount and the print (round 115), the export wire in the server's names (round 116), two test files
  for the `avs` by_row reading (rounds 117 and 118). Inert until a route serves a report: with none served every path is as before; the one added request is the report read, which answers `absent`.
- Criteria graded at this head (this seat's re-runs on the worker trees; typecheck rc=0; lint 0 errors; suite 1348 pass, the same 20 failing as every round since round 114's base): DBF115-1-AC1, AC2, AC3 at `e23ddb8e` (AC3 also at `506a2302`),
  DBF116-1-AC1, AC2, DBF117-1-AC1, AC2, DBF118-1-AC1, AC2 PASS. Re-run AC3 of round 115 at the head being registered immediately before the registration (the diff base is `d3c37966`; the grant covers `export/`, `render/`, the four named files and `index.tsx`).

## What waits (conditions, each read from the tree, never from a status line)

1. A route serves a 49 Financial household's filled report on DEV: hops 2-4 of the signed IB-pr-551 pair built, applied and the first write read by `~P2` and `0.7.0_AE_CloudOps~DB2`/`~IB2`; hop 1's gold for one date (`~D2`).
2. Row `IRPT_DASHBD-D2-S70` answered by `~P2` (a frozen print through the route: version_id, or the portal drops its version query by an F-SHIP amendment), because the page Andrew opens must export and print the report he saw.
3. The disclosure page (call a252) is a release gate for client delivery, not for the DEV sample (the CTO's ruling).

## The act, ready (validated now with `--check-only`: `APPROVAL-REGISTER result=OK ... head_sha=65f2e543 commits=30`)

```
git -C portal push origin cand/dell2/irpt-default-performance-report          # CONTRIBUTING-BOXES step 3 (a cand branch, never DEV)
python .tools/open-calls.py add --kind approval --project NFRA_DEVPLN --box dell2 \
  --branch cand/dell2/irpt-default-performance-report \
  --purpose "The default performance report for a client at any firm: the Performance tab shows it, and the export carries and prints it, when the reporting route serves it." \
  --pages "Investor Reporting performance tab,Investor Reporting export and print" --class client-facing \
  --how "On the 5174 dev build, open Investor Reporting, pick a 49 Financial client the route serves, read the Performance tab, then export it and open the print." \
  --portal portal
```

Before it runs: re-measure the head (`git -C portal rev-parse cand/dell2/irpt-default-performance-report`) and the commit count over `origin/PROD`; if a new PROD release landed, re-cut onto it first (CONTRIBUTING-BOXES step 2).
After it runs: the row's class is client-facing, so it waits on Andrew; nothing reaches DEV before he approves, and PROD only by a chosen-set promote.

-- 2.0.0_SA_COO~F2
