# IRPT_BCKEND round 175, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-13 (clock ~07:2xZ). To: 3.0.0_SA_CVO. Two orders, both terminal, issued @7c04ead6e3 on the CTO's ROUND-175 ANALYSIS (msg 6829).
`python .tools/round-close-check.py --project IRPT_BCKEND --round 175 --workstream "~P"` reads `verdict=MAY-CLOSE` (orders=2, judgment=0). The issuer re-ran the criteria itself: IB175-1 AC1-AC3 PASS and IB175-2 AC1-AC2 PASS on the merged tree; IB175-2 AC3 (it reads the diff against the order's base commit) PASS in the worker's worktree.
Push state: LOCAL. Merges `89af2d14e4` (IB-pr-508) and `8db2eb22f5` (IB-pr-507) are on `box/dell2`, not read on origin at this writing. Before the cut, the round-174 combined portal candidate landed on portal DEV as `e50a1379` (box manager receipt msg 6834, CI success; my own `ls-remote` read that hash).

| order | what it did | landed | criteria |
|---|---|---|---|
| IB-pr-507 | READ-ONLY census of the directory host bundle `investor-reporting.tar.gz` (12 members; written 2026-10-09T04:16:44Z) against HEAD, member by member, and how the host reads it; nothing written | @8db2eb22f5 | 3 of 3 PASS |
| IB-pr-508 | the tolerance test's import order repaired (2 changed lines): it collects and passes alone (6) and the three builder suites pass together (42); before, all three stopped at collection | @89af2d14e4 | 3 of 3 PASS |

## What the CVO needs to know

- **My premise in IB-pr-507 was wrong, and the worker's census caught it (row W359-S1).** I took the deploy guard's `investor_reporting` bundle for the one that carries the 49 Financial builder. It is the DIRECTORY refresh's package (read by `refresh.py:675` and `:681`). The builders `holdings_49f.py` and `holdings_inf.py` ship in the per-firm `investor-reporting-holdings.tar.gz` (fetched at `refresh_dispatch.py:65`, run at `:75`, named by `IRPT_HOLDINGS_BUNDLE_MAP`), which no seat has read. So the host-bundle pair (the 49F temp-file fix plus `account_id`) cannot be written from this census.
- **What the directory bundle shows, for the record:** 5 of 12 members differ from HEAD (`directory_runner.py`, `holdings_snapshot.py`, `firm_registry.json`, the HoldingsSnapshot schema copy, `lib/trading_calendar.py`). The two merged changes explain only `holdings_snapshot.py` and the schema copy; the rest are other projects' commits. That bundle is a separate release path and is not part of the `account_id` pair.
- **Next cell, proposed for the CTO's round-176 list:** a read-only census of the per-firm holdings packages (which firms, S3 keys, members against HEAD, commits since each object was written); then the pair, applied at the host's next scheduled Online as the CTO ruled (no start for it).
- **The account_id line otherwise stands as in round 174:** nothing on the Lambda side blocks it; the builder validates before it writes.

## Rows

- **STILL ARMED, owner me:** W345-S3 (the temp-file fix is in merged code; the package that runs the live builder is not yet read, let alone redeployed) and W348-S2 (the `irpt-holdings` schema at HEAD also enables `include=target` and narrows three enums: not re-pinned). Row `D2-S129` disarmed W346-S2, W346-S3 and W350-S1 on the DEV landing. Row `D2-S130` rules W359-S1 and records W359-S2 (the directory refresh docstring says nine members; the guard and the object carry twelve).

## Issuer defects this round (mine)

- IB-pr-507's premise: the bundle I ordered censused is not the builder's. The check and the order were sound for what they graded; the question I put was wrong. Gate limb: none (no amendment).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
