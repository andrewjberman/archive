# MX-r-3 -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-27 ~02:0xZ)

**Act:** the opal-gateway narrow release in `NFRA_MCPINDEX.TO-MX-r-3.narrow-release`, cut at the LIVE `df724ef284` plus
only NFRA_MCPINDEX's gateway commits. Deployer `0.9.0_WK_NFRA_MCPINDEX~1`, issuer `2.0.0_SA_COO~O`. Asked by the
issuer's file message `20260927T013546Z`.
**Authority for this half:** Andrew's self-drive arming term, "Served output still moves only under a never-widen
sign-off (CTO half + a second, non-acting half)" (`ANDREW_DIRECT_20260926_03xxZ_SELF_DRIVE_O_FABRIC.md` @56050d290d).
**Second half owed:** a non-acting seat, `3.0.0_SA_CVO~O`. The issuer and the deployer are acting seats.

## The commits (NFRA_MCPINDEX's, on CLOUD, touching `infra/aws/ec2/opal-gateway`, oldest first)

650c9a99cb (c-2), 119a49eef0 (c-4), 37f208249f (c-5), 4bfab1bcf2 + 8829b066d1 (d-2), 81d37aafda, 2c25c4c831,
84a725073b, d36d31f8c5, bc0cde67f0 (t-8), e1cdb12550 (v-6), bcb48cf626 (c-5). The worker's census at its cut is the
binding list; this half covers exactly these served-code changes and no others.

## Blast radius, read from the diffs against `df724ef284`

1. **Classification composition** (`destructive_ops.py`, `integrations/base.py`, `integrations/registry.py`):
   **DELTA = 0 on every served path.**
   - `read_teams_attachment` is ALREADY `SAFE` in the live code (`destructive_ops.py:34` at df724ef284), so the order's
     "becomes SAFE" moves nothing.
   - The composed tag is consulted only inside `destructive_ops.classify`, AFTER `SAFE_TOOLS` and `DESTRUCTIVE_OPS`, so
     no native tool's class can change.
   - `classify` is reached only on the native `_run` path (`tools.py:141` `guard.enforce`, `tools.py:155`
     `blast_cap.evaluate`). Integration tools run through `run_integration_tool` -> `guard.enforce_min_tier`
     (`integrations/base.py:119-150`, `guard.py:80-95`), which never calls `classify`. So the 14 declared classes
     (MX-c-5) gate nothing that was not gated before.
   - `registry.py`'s new `composed_refused` can only DROP a tool, never add one. A drop would show as a tool-count
     change, which the 46 = 46 guard catches.
2. **`data_entitlement.py`**: `INDEX_TOOLS` (5 tools: 3 `portal_index`, 2 `opal_discover`) join `TOOL_CLASSES` as
   `legacy`. They exist only if their integrations register, and neither does (item 4). A restricted profile is denied
   them exactly as every other non-Schwab tool. DELTA = 0 while dormant.
3. **`DATA_CATALOG.yaml`**: parsed structurally at both commits. Top-level keys added: `silver_datasets` only; changed:
   `built_at_git_head` only; **`channels` identical (15 of 15)**. `catalog_gate` indexes only `channels.*.artifacts`
   (`graphql_plumbing/catalog_gate.py:62-66`), and `query_v0` and the asker path read through it. The only reader of
   `silver_datasets` is the dormant `portal_index` (`integration.py:166`). So `opal_asker_query`'s answers, including
   Alyssa Keith's portal-only grant (OA-g-3), have DELTA = 0.
4. **New integrations `opal_discover`, `portal_index`**: DORMANT. They register only when named in
   `ENABLED_INTEGRATIONS` (`server.py:85`, `config.py:227-228`).
5. Tests and the routing harness are not served.

## Writers of the named property (NEVER-1: count them) -- CORRECTED 2026-09-27 ~03:2xZ

**SUPERSEDED on these bytes:** the first version said "N = 1: the host `.env` ... the act does not touch it". That was
WRONG, and `3.0.0_SA_CVO~O` caught it (second half @9ca9e44fea, row NFRA_MCPINDEX-Z-C-S17).

**N = 2.** (1) `deploy-to-ec2.sh:196` rewrites the whole host `.env` on EVERY deploy, with the literal
`ENABLED_INTEGRATIONS=ycharts opal_portal globgrph` (re-read at `df724ef284` and at HEAD: same line, same literal,
and no MCPINDEX commit touches the script). (2) Any hand edit of the host `.env` since the last deploy.
`config.py:227-228` reads the value; it does not write it. So THIS ACT DOES WRITE the property. DELTA = 0 holds only if the
live `.env` already carries that exact literal; a live value naming `schwab`, say, would be REMOVED by the deploy.
Of the 12 commits, 3 mention the name, and every such line is a docstring, a comment or a test string.

**Condition added (CVO~O's, adopted by this half):** before the upload, read the live `.env`'s `ENABLED_INTEGRATIONS`
over SSM. If it is not exactly `ycharts opal_portal globgrph`, STOP.

## A second served input: the dashboard bundle -- ADDED 2026-09-27 ~03:5xZ

Neither half named it at signing; `3.0.0_SA_CVO~O` found it (addendum, row NFRA_MCPINDEX-Z-C-S18 @12fff6fc33).
`deploy-to-ec2.sh:80-92` (at `df724ef284`) builds the dashboard bundle from the nested `mcportal` checkout, at whatever
commit it is on, and ships it in the artifact. The live bundle is `a3bff71ffa` (`EC2_MANIFEST.json`
`services.opal-gateway.mcportal_commit`). The worker's `/c/tmp/mx-rel/mcportal` reads `a3bff71ffa` (rev-parse, 03:5xZ). So
DELTA = 0 holds for the bundle too.

**Condition added (CVO~O's, adopted):** before the upload, `/c/tmp/mx-rel/mcportal` HEAD must be `a3bff71ffa`. On any other
commit, STOP.

## Both branches, read from the producer's rule

- **At GO (integrations dormant), IF the SSM read matches the script's literal:** DELTA = 0 on every served answer,
  and the tool list stays 46 = 46. **If it does not match:** the deploy would move `ENABLED_INTEGRATIONS`, so STOP. No
  such branch is signed.
- **After Andrew's G-A word enables either integration:** the tool list grows and the new tools serve. That is a
  separate act with its own sign-off. This half does NOT sign it.

## Rollback, per key

- Code: redeploy `df724ef284`'s artifact through the same release script, with the 90-second health rollback. The order
  requires that rebuild shown before the act (step 4). The manifest record reverts with it.
- Data: none written by this act.

## Guards required at GO

The SSM read of the live `ENABLED_INTEGRATIONS` equals `ycharts opal_portal globgrph` BEFORE the upload (else STOP); the
`mcportal` checkout at `a3bff71ffa` BEFORE the upload (else STOP); on-box `/health` = 200; the MCP tool list diff = 46 = 46 (this is also what catches a `composed_refused` drop);
the NEVER-2 ledger `nfra-mcpindex-r2-gateway-release` opened before the upload and closed after; off-hours GO; announcement through `0.0.0_AB_MSTR~Z` and the agentbus.

**Note for the issuer (not a condition):** `tests/test_entitlement_admin.py` does not exist at `df724ef284`, and
119a49eef0, 84a725073b and bc0cde67f0 edit it. A per-commit apply onto the live base conflicts there (measured on a
scratch worktree, since removed). It is a test file, so it does not change the blast radius above. Expect it at the cut.

**CTO half: SIGNED**, for the act above as bounded here, by `1.0.0_SA_CTO~O`.
