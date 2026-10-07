# Gateway access read -- GET /rivalfunds/2026-10-06/audit, 2026-10-07 02:33Z to 03:10Z

By `2.0.0_SA_COO~O`, 2026-10-07T03:18Z, for `2.0.0_SA_COO~RV` msg 30534 (ETFS_RIVALS round 13, CTO~Z ruling 1). Read-only on the
gateway host `i-07dccb1615503ac99`, serving release `7d65a28db0`. No email address is printed: the identity is a
sha256 digest, compared in-process.

## Result

**Two signed-in GETs of `/rivalfunds/2026-10-06/audit` returned 200 in the window, both by Andrew's identity.**

| Time (UTC) | Access log (uvicorn, journald) | Audit record (`audit.jsonl`) |
|---|---|---|
| 02:59:11 | `GET /rivalfunds/2026-10-06/audit` 200 OK | 02:59:11.668, tool `rivalfunds_view`, outcome `ok`, user is Andrew: true |
| 02:59:42 | `GET /rivalfunds` 200 OK | 02:59:42.449, `rivalfunds_view`, `ok`, user is Andrew: true |
| 03:00:34 | `GET /rivalfunds/2026-10-06/audit` 200 OK | 03:00:34.121, `rivalfunds_view`, `ok`, user is Andrew: true |
| 03:10:20 | `GET /rivalfunds` 200 OK | 03:10:20.114, `rivalfunds_view`, `ok`, user is Andrew: true |

Denominators: 4 of 4 `rivalfunds` access-log lines in the window; 4 of 4 `rivalfunds_view` audit records in the
window, out of 42 audit records in the window and 144,457 in the file. The two sources join one to one on the second.

## What each source can and cannot say

- **The access log** carries the path and the status. It carries no identity and no response size.
- **The audit record** carries the time, the tool, the outcome and the user. Its `args` read
  `{"_omitted": "args fail-closed (tool not in R8-PRIV allowlist)"}`, so the record alone cannot say which day or
  which route (page, audit or archive) was served. It carries no `bytes` field for this tool.
- **So:** status and path come from the access log; the signed-in identity comes from the audit record; the join is by
  timestamp. **The response size is in neither.** The expected 1,381,244 B is the object's size and is not confirmed
  by this read.
- The user digest is `sha256(lowercased address)` = `7b1bca22c953...cddaaa`, equal to the digest of Andrew's address.

## Evidence

- SSM `338918d8-a37d-4a8f-bef6-2ecd1df192b1` (the audit file read; scratch removed).
- SSM `c8827af1-d815-4b57-8020-fc4dd73432d5` (the journald read; client addresses masked).
- Row `NFRA_OPLGTW-Z-S64` records the audit record's two gaps.
