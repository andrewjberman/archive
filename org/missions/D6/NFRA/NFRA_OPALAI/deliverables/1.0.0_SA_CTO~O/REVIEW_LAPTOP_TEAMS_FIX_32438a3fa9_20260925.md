# Pre-deploy read -- laptop 1.0.0_SA_CTO's Teams fixes, commit 32438a3fa9 (branch gw-teams-reader-fix)

**By:** `1.0.0_SA_CTO~O`, as agreed in point 5 of the release coordination. **Written:** 2026-09-25 ~21:4xZ.
**Read:** `git show 32438a3fa9`, 5 files, +131/-7. `app/graph.py:22-57` was also read for the byte path.

**Verdict: APPROVE WITH TWO CHANGES** before it deploys. Both are small. Without them, gap A does not serve the
Analyst, which is the reason gap A exists.

## What is sound

- **Gap B (`_get_messages`).** A Graph 500 on the `$select` page retries without `$select` and projects each message
  back to `_TEAMS_MSG_FIELDS`, so the caller's shape and fields are unchanged and nothing widens. Every other status
  still raises. `select_fallback: true` marks the page. Both `read_chat_messages` and `read_channel_messages` use it.
- **Gap A's classification** is SAFE in `destructive_ops` and listed in `data_entitlement.NATIVE_TOOLS`, and the pinned
  count moves. That is right, and it is the lesson `read_teams_attachment` taught.
- **Bytes:** `graph.call` returns `resp.content`, raw bytes, for a non-JSON response (`graph.py:57`), so `$value` is
  not decoded or corrupted. The `str(raw).encode` branch is a dead fallback and harmless.

## Change 1 (REQUIRED): the Opal Bloomberg identity cannot call the new tool

- `app/identity_scope.py`'s seed allowlist for `opalbloomberg@opalinvest.com` (`:43-60`) names the Teams read and serve
  set, and NOT `read_chat_message_images`. That identity is scoped and deny-by-default, so the Analyst and the future
  Opal_Agent would be REFUSED by the gateway itself.
- **Add `read_chat_message_images` to that SEED**, in the same commit, citing Andrew's word
  (`org/tier1_exec/4.0.0_SA_CRO/deliverables/ANDREW_DIRECT_20260925_170xZ_TEAMS_INLINE_IMAGES_GATEWAY_ROUTE_TO_CTO.md`).
  It is a read of content the identity already reads, so it is within frame (iii).
- **Put it in the seed, not the overlay file.** The overlay file is exactly the mechanism row NFRA_OPALAI-Z-S18 is
  about.

## Change 2 (REQUIRED): return the images as MCP image content, with a total cap

- The tool returns each image as a `data_base64` STRING inside a JSON dict. The model receives that as text, not as an
  image, so it cannot SEE the pasted screenshot, which is the whole point.
- A 2,000,000-byte image also becomes about 2.7 MB of text in the context.
- **Return each image as an MCP image content block** (FastMCP supports returning images), with metadata beside it. Cap
  the TOTAL bytes across a message's images as well as each image; about 1 MB total is a sane default. An image over
  the cap returns its size and a plain "too large to show" note, as now.

## Noted, not blocking

- **Audit:** `audit.py`'s `_ARGS_ALLOWLIST` does not declare `read_chat_message_images`, so its audit row omits the
  args. It fails closed, the same as NFRA_OPALAI-Z-W2-S2. It is worth one line in the same commit.
- **Test:** `test_identity_scope::test_scoped_deny_by_default` is RED because of the overlay row in Z-S18, not because
  of this diff. Changes 1 and 2 do not touch it.
- **The pinned tool count is recounted on the release base,** as the commit says. The base `f1f0fc6780` already
  carries `opal_asker_query`, and MCPORTAL's retry lands first.
