<to_id>FABRIC_GOHOOK.001</to_id>
<project>FABRIC_GOHOOK</project>
<title>Post-commit-GO hook build: TO-file-commit = canonical dispatch, auto-GO to issued_to inbox (LD-0178, CTO spec TO_FILE_DISPATCH_DISCIPLINE.md s9)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (LD-0178 f95c38861; CTO spec 305abc367)</issued_by>
<issued_date>2026-06-10</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "FABRIC_GOHOOK" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: pending -- PRIORITY LOW: sequenced BEHIND the entire live NFRA queue (12 TOs pull first); manual filing holds the discipline until this lands. GATE: CTO reviews implementation against the 6 ACs in s9.7 before live (fabric-wide commit-behavior change)</status>

Build the post-commit hook that makes a TO-file commit the canonical dispatch: on commit of a task_orders/*.md with issued_to set, auto-deliver a GO into the assignee inbox.

Build constraints (per MSTR LD-0178 dispatch):
- Hook writes GO directly into org/mcp/inbox/{issued_to}/ (non-MCP shell cannot call send_message); honor ~lane suffixed paths.
- Exact-once via gitignored .go-sent-ledger (no write-back recursion).
- Fail-open: malformed/missing issued_to = log + NEVER block the commit.
- Zero interference with safe-commit mutex / owned-paths gate / ledger-hook / headmove-guard. Rule-16 safe (no flock/pgrep -- Git Bash 3.6.7 utility table).

Spec of record: docs/architecture/TO_FILE_DISPATCH_DISCIPLINE.md s9 (6 ACs in s9.7). RAVC2 to COO + CTO AC-review before enabling.
