# NFRA_OPALAI -- round-2 enrichment list, PRE-DRAFT (not the analysis)

**Owner:** `1.0.0_SA_CTO~O`, on option 3 of the /next-steps Andrew approved ("i like all four", @bda25438c8).
**Status:** DRAFT. The round-1 L10 analysis is written only after `3.0.0_SA_CVO~O`'s slug. It will grade FWD-1..13,
adopt or amend this list, and add whatever the slug surfaces. This draft exists so round 2 can be cut the day the slug
lands, not a day later.

**Sources:** `ROUND1_ANALYSIS_INPUTS.md` (I-1..I-5), the S15 design note @b99ab96fdf, rows Z-S5/S6, Z-S18/S19 and
Z-W2-S2, and the gateway release-base rule @75117e60d6.

---

## The list, in cut order

1. **E1 -- the asker-scoping repair** (I-1 plus Z-S5). ONE cell, because both change `asker_scope.handle_asker_query`:
   - (a) the catalog gate is evaluated on the ASKER's class and firm, resolved from their verified Entra tenant, AND on
     the calling identity's. The stricter of the two wins. A non-Opal tenant is denied until a tenant-to-firm registry
     exists;
   - (b) the cited message is bound: it must be newer than a short window, and the reply may go ONLY to the same
     `chat_id`;
   - (c) in a group chat, the scope is the intersection over every human member, not the sender alone.

   Negative arms: an older message from a wider person is refused; a reply to a different chat is refused; a group chat
   containing an unprofiled member is refused.
2. **E2 -- the upload refused to the runtime** (Z-S18 and Z-S19, Andrew's option 2). `identity_scope` is keyed on
   (identity, OAuth client_id), and `opal_data_refresh_upload` is allowed to the operator's client only. The test points
   at a fixture overlay. **If Andrew's call 2 answer lets the Analyst seat's fence drop the upload now, that one-line
   fence change is cut FIRST, ahead of this whole list.**
3. **E3 -- switch the Analyst on for the asker tool.** Add `opal_asker_query` to the concierge seed allowlist, which
   ends the "deploys dark" state from Z-S6. **Only after E1 and E2 land**, because the tool goes live for the Teams path
   only once the bypass and the upload reach are closed.
4. **E4 -- consume the laptop's image reader** (I-5). The Analyst's serve skill uses `read_chat_message_images` for a
   message with pasted content, and says plainly when it cannot read one (FWD-2). This builds nothing new on the
   gateway, and assumes the laptop's release landed with review changes 1 and 2 (@4f06376378).
5. **E5 -- re-measure the Teams watch** after the laptop's gap-B fix. Blocker (2), reads failing with a live token, is
   read again before anything else is ruled on it. If it clears, the watch's remaining work is blocker (1), the token
   refresh the watch should own (C8).
6. **E6 -- the Bloomberg view server** (S15). It moves into `opal_ai/opal/mcp/bloomberg/` and is run by the operator
   over loopback HTTP; `Opal_Agent` gets one MCP URL.
   - First measurement: can `Opal_Agent` reach `127.0.0.1:8194` and `:8790`?
   - Contract question for the analysis: a server-side history cap on the agent-facing instance.
7. **E7 -- the batch cell:** the `_ARGS_ALLOWLIST` line for `opal_asker_query` (Z-W2-S2), and the teams-watch header
   naming its real consumers (I-3).
   It also carries **CI green (Z-S20):** `ci.yml` installs pytest and ruff; `portal_lookup.py`'s 15 ruff findings
   are FIXED, never waived; `run_checks.sh` reports ruff's real count. One green run on a real push is FWD-13's proof.
8. **E8 -- speed** (FWD-3, S9): real exchanges timed stage by stage against the 2026-08-20 baseline. Its first cell only
   MEASURES; the remedies are cut from what it finds.

## Deliberately NOT in this draft

- **The gateway move into `opal_ai`** (FWD-5 and FWD-11, S11 and S12). It is held by G-MOVE, which waits on Andrew's
  OPLGTW call.
- **Operator controls** (FWD-8's admit, narrow and remove): these ARE NFRA_MCPORTAL's Entitlements tab. This project
  grades FWD-8 against MCPORTAL's deliverable and builds no second admin surface.
- **The release flow** (S13, FWD-9): its first real exercise is E3's release. It is graded then, not built separately.
