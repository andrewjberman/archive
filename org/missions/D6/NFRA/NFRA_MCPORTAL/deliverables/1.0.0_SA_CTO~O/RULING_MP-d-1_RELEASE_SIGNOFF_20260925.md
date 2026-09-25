# CTO half of the NEVER-1 sign-off -- NFRA_MCPORTAL MP-d-1, the narrow gateway release (the RETRY)

**By:** `1.0.0_SA_CTO~O`, the PRD owner. **Written:** 2026-09-25 ~19:0xZ, after the first attempt's outage.
**Pairs with:** `2.0.0_SA_COO~O`'s amended MP-d-1 (@7d03f0ad19) and its ledger
`20260925T1636Z_nfra-mcportal-r2-gateway-release` (opened before the first act and closed ROLLED BACK with its
proof, on the worker branch in `C:/tmp/mp-2`, commits edfc201bf0 and fb46f88294).

**Owned plainly:** the first attempt went out without this half. My round-1 analysis (@667f442b8a, E4) ruled the
release narrow and did not supply the blast radius. NFRA_OPALAI's release had one (@592e319a06) and this one should have
too. Written now, before the retry.

## What the first attempt taught

The gateway was down about 17:14 to 17:31:22Z. The deploy script's `.env` printf lost the space before `"${REGION}"`,
so every value shifted one key. It was fixed at 83cbd1a605 and rolled back to `f1f0fc6780`, and the rollback is
verified live: `/health` 200, and `server.py`'s md5 equals `f1f0fc6780`'s. **The rollback path is therefore proven
today, not presumed.**

## The blast radius of the retry

- **Built from:** `rel-nfra-mcportal-r2-gateway-2`, cut at the deployed `f1f0fc6780` plus ONLY NFRA_MCPORTAL's gateway
  commits (MP-t-1 @98ad7e253f, MP-t-4 @17b7e01c0f, MP-g-1 @d0ba96d27c) and the deploy-script fix 83cbd1a605. The
  defective `rel-nfra-mcportal-r2-gateway` @c97839d7c8 is never used. The five foreign commits stay out, as before.
- **May touch:** the gateway process on its EC2 host.
  - New modules: `app/owner_gate.py` and `app/admin_grants.py`.
  - Changed: `app/admin_api.py`, `app/config.py` (the dashboard-owner list, C2) and `app/server.py` (routes).
  - The built dashboard bundle, pinned by its `mcportal` commit.
  - `deploy-to-ec2.sh`.
- **Must not touch:** any ALB rule, IAM policy, Terraform, secret, DynamoDB item, or the Claude-client paths. The
  handlers behind `/mcp` and the OAuth paths must be unchanged at the bytes.
- **The grant writer is NOT applied by this act.** That is MP-a-1. Until it is, every grant write from the dashboard
  fails CLOSED with a plain reason, and that is expected.

## Both branches, which the post-act reads must show

1. **Owner:** Andrew, signed in, loads `/` and gets the dashboard, and loads `/api/admin/...` and gets a structured
   answer (a grant write refused plainly while the writer is unapplied).
2. **Anyone else:** a signed-in non-owner is refused on `/` and on every `/api/admin/*` handler. `/sprint` stays open to
   any signed-in Opal account.
3. **Claude clients:** the MCP tool list read after the act equals the one read before (the same count and the same
   names). That shows the `/mcp` surface did not move.

## One condition on MP-g-1's header capture (privacy)

The capture records claim KEYS only. The one owner-key value it needs is written ONLY into the grant writer's owner
configuration, never into a log line, an audit record or a committed file. If the capture as built writes any claim
VALUE to a log, the retry does not ship until that is removed.

## Rollback, per key

Redeploy `f1f0fc6780`'s bytes through the same guarded script. This was proven today. The amended order adds the
automatic trigger: `/health` not 200 within 90 seconds of the restart rolls back at once. The `.env` render check runs
BEFORE the act, with distinct markers, each landing on its own key.
