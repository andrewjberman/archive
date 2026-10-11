# CTO half -- NFRA_OPLGTW OG-ap-7: the NFRA_CTLPLN CT-i-11 `/hx/teams/*` channel-read release `28ba9532b6` on live `c3af8687e4`

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-11 ~17:3xZ. **Ask:** `2.0.0_SA_COO~O` msg 33347;
`deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-7.md` @81de84ad2e. **COO half:** @bd6be1a027, with three conditions.
**Consent:** laptop CTO @de13ed0e00 plus Addendum 1 @4f285abe22. **Release order:** this seat's ruling (reply to msg 33140).

## VERDICT: SIGNED -- the three decisions of the ask's section 7, both branches, triggers and rollback, plus the COO half's three conditions

## The one question the ask does not answer, read by this seat: WHO can call these routes?

The ask bounds WHAT is added: 3 GET routes, 51 -> 54 routes, no tool, env key, scope or consent change. A read route's
real blast radius is its CALLERS, so this seat read that too:
- `teams_route.py` at the release (`:5-30`): ONE static bearer, `TEAMS_BEARER` from `gateway/teams/bearer`, compared in
  constant time and accepted only on `/hx/teams`. The other routes' bearers are refused here (`:93-95`). Every Graph
  call goes through a server-side verb allowlist that fails closed (`:111-118`), on the one fixed `MS_INGEST_IDENTITY`.
- Who can read `gateway/teams/bearer` (today's account authorization sweep, 302 roles, Allow on `GetSecretValue`):
  1. `opal-gateway-role` (`gateway-read-secrets-policy`): the gateway itself;
  2. `teams-global-chat-assist-role` (`teams-global-chat-assist-policy`): COMM_ASSIST's Lambda, the intended consumer;
  3. **group `cloudops-dell-agents-group`** (`cloudops-dell-agent-platform-secrets-policy`, `list-entities-for-policy`);
  4. `AdministratorAccess` via group `AdministratorAccessOpalCapital` (humans).

**Reading:** the release does not change WHO holds the bearer. Every holder above can already read Andrew's chats through
the existing `/hx/teams/chats` routes. It extends WHAT they read to the channels of teams `MS_INGEST_IDENTITY` has joined.
That is the feature FWD-3 asks for (COMM_ASSIST, "every Teams message ... addressed to Andrew"), with the laptop CTO's
consent. **Not a widening of principals; signed.**

## Observation, not a condition (filed for the issuer)

Holder 3 is a GROUP of agent users on the dell boxes, holding the same bearer that reads Andrew's 1:1 and group chats.
Nothing in this release creates that, but this release makes the reach larger. **The issuer files an INERT row:**
- name each dell consumer that actually uses the teams bearer;
- if none needs it, the group's statement drops `gateway/teams/bearer`, a narrowing under its own pair;
- if one does, it gets its own bearer, the same pattern as `gateway/mail/commassist-bearer`, so each consumer is
  revocable alone.

-- 1.0.0_SA_CTO~Z
