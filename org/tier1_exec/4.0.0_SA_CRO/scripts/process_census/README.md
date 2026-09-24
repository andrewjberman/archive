# process_census -- the efficiency ratio behind RCN-0016

Read-only. Git history only; writes one JSON to the path you give it.

    # estate mix for a window (prints primary mix, class touches, lines by class)
    python org/tier1_exec/4.0.0_SA_CRO/scripts/process_census/census.py 2026-09-17T00:00:00Z 2026-09-24T15:00:00Z <scratch>/census.json

    # per-project table from that JSON (commits, product commits, product lines, task-order files and KB, rounds)
    python org/tier1_exec/4.0.0_SA_CRO/scripts/process_census/projects.py <scratch>/census.json

Run both from the workspace root. The **efficiency ratio** is the `touches PRODUCT code` share in census.py's
PRIMARY block. Count the portal separately (`git -C portal log --all --no-merges --since=...`).

Classes (first match wins): PRODUCT = a code extension outside org/, docs/, .tools/, .claude/, rcg/; TOOLING = code
under .tools/, .claude/, org/mcp/, org/modules/; GOV_* = org/ and rcg/ records (task orders, surprise channel, logs,
message/audit logs, other records); DOCS = docs/; LAW = CLAUDE.md, org/XXX.md, AGENTS.md; DATA = everything else.

Known blind spots: code on another seat's unpushed branches; the portal repo; generated evidence dumps inflate
governance LINES (use the commit share as the headline). Target-specific parts: none -- the path classes are the
estate's layout and change only if the layout does.
