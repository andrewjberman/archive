# Site-Z tool-owner routing register (0.0.0_AB_MSTR~Z)

Items found inside one project that belong to a tool or stack another seat owns. Each row names the owner, the routing
act and the condition that closes it. This seat routes and tracks; it does not fix. Append rows; close one by stating
the closing commit in its `state` cell.

| id | source | defect | owner | routed | state |
|---|---|---|---|---|---|
| ETFS_RIVALS-W5-S3 | ETFS_RIVALS r4 ruling 13 @6dcb0074e4 (1.0.0_SA_CTO~Z msg 28076) | the opal-gateway stack cannot be planned or deployed from a fresh worktree | gateway stack: NFRA_OPLGTW, `2.0.0_SA_COO~O` / `1.0.0_SA_CTO~O` (site Z) | 2026-10-01 23:0xZ by broker | ACCEPTED by `1.0.0_SA_CTO~O` (msg 28080), joined to NFRA_OPLGTW row Z-W21-S19; fix cut next round, accepted from a FRESH worktree; closing commit to follow |
| ETFS_RIVALS-W5-S7 | same | the naming gate reads package-relative paths as S3 keys | LGIC naming gate: LGIC_ENFORCE, laptop `2.0.0_SA_COO~G` | 2026-10-01 23:0xZ by bus (laptop 0.0.0_AB_MSTR carries) | PARKED: laptop `2.0.0_SA_COO~G` not live (laptop census 23:0xZ); un-parks when ~G is next seated, laptop 0.0.0_AB_MSTR hands it over |
| ETFS_RIVALS-W5-S14 | same | safe-ec2-deploy.sh's jq rewrite mangles non-ASCII in unrelated manifest entries | the deploy wrapper | 2026-10-01 23:0xZ by broker to `1.0.0_SA_CTO~Z` for confirmation | LIKELY CLOSED by NFRA_MCPINDEX MX-x-4 @842a3fcdb2 (09:39Z: the rewrite became a Python JSON parse/dump keeping escape style); the owner confirms against the W5-S14 reproduction |
| ETFS_RIVALS-S7 | same | to-decomp-ref-lint.py's resolver truncates worker codes at the first underscore; fix BEFORE the seating limb enforces | the lint: laptop `1.0.0_SA_CTO` (last fix @3f33315632) | 2026-10-01 23:0xZ by bus | OPEN |
| MSTRZ-GL-1 | this seat, 2026-10-01 ~22:5xZ, CLOUD pull-merge in a fresh linked worktree | gitlink-publication-check.sh resolves the submodule URL with `git -C "$ROOT/$SMPATH" config remote.origin.url`; when the submodule is NOT initialized that runs against the SUPERPROJECT, so it tests portal d79b9934e3 against ajb_workspace.git and refuses a published commit (false BLOCKED). The .gitmodules fallback never fires. Fix: use the submodule repo only when `rev-parse --show-toplevel` equals `$ROOT/$SMPATH`, else .gitmodules | the hook: adopted by `1.0.0_SA_CTO~Z` (msg 26074) from this seat's proposal | 2026-10-01 23:0xZ by broker | OPEN (interim: `git submodule update --init portal` in the worktree before a merge commit) |
