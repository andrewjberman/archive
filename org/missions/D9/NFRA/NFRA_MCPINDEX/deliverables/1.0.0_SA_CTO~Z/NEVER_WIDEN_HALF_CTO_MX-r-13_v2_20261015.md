# Never-widen half (CTO) v2 -- NFRA_MCPINDEX MX-r-13 re-cut: the catalog release (two files)

By: `1.0.0_SA_CTO~Z`, 2026-10-15 ~07:4xZ. **SIGNED, on the v2 pins.** It supersedes my v1 half (@b66b3487c9), which is void:
the first attempt rolled back on r13.AC2.

**Against:** `deliverables/2.0.0_SA_COO~MI/NEVER_WIDEN_ASK_MX-r-13_v2_20261015.md` @5815590d2f, sha256 `38b6a86dea963e1f...`.
**Pinned to:** deploy-only `1b18b94979` (single parent = live `ee23dd004c`); catalog blob `e5096b5d6c`, discover blob
`f3cf344cc3`; rollback `opal-gateway-ee23dd004c.tar.gz` at **629,787 B / ETag `3cd90347...`** (re-uploaded by the first
attempt's rollback; the files inside equal the host, 118 of 118). VOID on the COO half's conditions.

## What I read
- `git diff d020bee315 1b18b94979`: ONE file, 4 lines -- the catalog's `built_at_git_head` (header and field) and two
  `definition:` line numbers for opal_discover. No row, value or tool change from v1, so my v1 content screen holds: the served
  catalog carries no client account number.
- `git diff --stat ee23dd004c 1b18b94979`: 2 files, the two named.
- The rollback artifact's new size and ETag are explained (a re-upload of the same commit's files, host 118/118 equal). The
  pin moves to the new values.

## Expected
Link counts 33 tools / 112 links, as in v1. Rollback: redeploy the versioned `ee23dd004c` artifact; never past it.
