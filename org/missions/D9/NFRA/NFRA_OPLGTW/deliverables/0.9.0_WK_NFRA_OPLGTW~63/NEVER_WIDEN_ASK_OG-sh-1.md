# Never-widen ask -- OG-sh-1, the gateway tool `list_shared_folder(url)`

By: `0.9.0_WK_NFRA_OPLGTW~63`, 2026-10-13. Nothing is released or deployed by this order; this is the ask for the gateway
release that ships the tool. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-sh-1.shared-folder-tool-and-0929-read.md`.
Code commit: `47cee985ee` on branch `wk-NFRA_OPLGTW-63` (LOCAL).

## 1. The act

Add one MCP tool, `list_shared_folder(url)`, to the Gateway (`infra/aws/ec2/opal-gateway/app/tools.py`). It encodes the
sharing URL as Graph's share id (`u!` + unpadded base64url), GETs `/shares/{id}/driveItem`, and for a folder GETs
`/shares/{id}/driveItem/children` (name, id, size, lastModified, isFolder; `@odata.nextLink` followed up to 20 pages of 200,
Graph-host links only, each once). A file link returns its metadata. The two failures are distinct: `stage=resolve_failed`
and `stage=children_failed`.

## 2. Class

READ. `destructive_ops.SAFE_TOOLS` (so `classify()` returns SAFE, the guard is bypassed, no write class applies) and
`data_entitlement.NATIVE_TOOLS` (class `legacy`, so it is not `tool_unclassified`). It is not in `DATA_GRANT_TOOLS`, so a
profile does not confine it; an unprofiled principal passes on to the existing gates exactly as for `read_teams_attachment`.
Registered tool count 62 -> 63.

## 3. Reach

Only what is shared to the signed-in user. Every Graph call uses that user's own delegated token (`_run` -> `_user_token`),
so Graph enforces the user's permissions; a link the user cannot open fails at `resolve_failed`. The token's existing
`Files.ReadWrite.All` scope is unchanged (no IAM, no consent change). Only GETs. No write, send, upload or copy. The URL is
a capability link and is NOT written to the audit record (the tool passes empty args; `audit._ARGS_ALLOWLIST` omits an
undeclared tool's args by design). `read_teams_attachment` is unchanged.

## 4. Release

The next Gateway release cut from a commit that contains `47cee985ee` (the issuer merges bd-2 then sh-1). Files changed:
`app/tools.py`, `app/data_entitlement.py`, `app/destructive_ops.py`. Deploy path: `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`
via `safe-ec2-deploy.sh opal-gateway`, per `infra/aws/ec2/EC2_MANIFEST.json` `services.opal-gateway`.

## 5. Rollback

Redeploy the prior release ref. `EC2_MANIFEST.json` at this branch's base records `deployed_commit`
`185dc048881da2030efa11f4d0bfb8704b500c66` (deployed 2026-10-12T12:52:14Z) with `previous_deployed_commit`
`d9f2ebded95b638d4de9a701e1123bfbf051a5c1`. Rolling back to `185dc04888` removes the tool entirely (a new tool, no stored state,
nothing a client depends on yet). Re-read the manifest at ship time: the rollback ref is whatever `deployed_commit` is then.

## 6. Halves owed

`1.0.0_SA_CTO~Z` and `2.0.0_SA_COO~O`, against this file at its commit, before any deploy.
