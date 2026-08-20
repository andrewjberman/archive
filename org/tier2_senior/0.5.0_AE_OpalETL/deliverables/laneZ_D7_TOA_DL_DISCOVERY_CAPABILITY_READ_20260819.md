# D7_TICKETING.TO-AC-SITEZ — TO-A output: DL discovery + on-box capability read
**seat:** 0.5.0_AE_OpalETL~Z · **date:** 2026-08-19 (~19:20–19:45Z) · **vintage:** PRD @36a7fbd70e (verified unchanged to HEAD 1ba0845ae4) · **archetype:** TRACE
**mode:** READ-ONLY throughout — no writes, no consent grants, no env/config touched. All Graph reads on the two STANDING gateway identities.

---

## 1. U1 — DL inventory (the Andrew one-liner's facts, each pinned)

| Firm | DL address | Evidence class | Pin |
|---|---|---|---|
| 49 Financial | **`49@opalinvest.com`** ("Opal 49") | MEASURED | direct `toRecipients` of a real partner request: "Trade Request Question", jack.stulack@49financial.com → [49@opalinvest.com, alyssa.keith@, manav.shah@], 2026-08-13T14:34:50Z, Graph message id `...ADEQUbvAAA=` |
| Inflection WM | **`inflection@opalinvest.com`** ("Inflection") | MEASURED | direct `toRecipients` of a real intake-shaped request: "ISRG" ("do you have a perspective on ISRG?... Meeting on Wednesday"), Peter@inflectionwealth.com → [inflection@opalinvest.com], 2026-08-04T00:17:47Z, id `...AC_Axe0AAA=`; corroborated in quoted headers of the "Gina Anderson retirement account analysis" thread (Yang→Peter+Inflection@, 07-24) |
| Cottonwood CA | **NOT FOUND** | MEASURED ABSENCE (scoped) | zero results for `to:cottonwood@opalinvest.com`, `to:cot@opalinvest.com`, `to:cca@opalinvest.com` and no cottonwood-domain partner mail under full-text "Cottonwood"/"Cottonwood Capital" — **searched in Andrew@opalinvest.com's mailbox only** (the one mailbox this identity can search; a DL Andrew is not a member of would be invisible here). Firm canonical: Cottonwood Capital Advisors, abbrev `cot` (docs/reference/cottonwood-cot-canonical-abbreviation-standard-20260608.md) |

Positive control for the `to:` probe form: `to:49@opalinvest.com` returned rows on the same instrument in the same session.
**Type (classic DL vs M365 Group vs shared mailbox) is UNDETERMINED for both found addresses** — the gateway MCP surface exposes no directory/groups read (measured below), and this determines the "monitorable mailbox present?" half of Q3. Delivery to Andrew's inbox proves distribution-to-members behavior only.

## 2. U2 — Graph permission state on the gateway app registration (was UNKNOWN)

- **App registration:** App-2 "M365-MCP-Graph", `CLIENT_ID=adb3c23a-82d2-48f4-b62a-0538d682dcff`, `TENANT_ID=6810043e-d171-4adc-9975-068b35e179da` (APPLIED: read on-box from `/opt/opal-gateway/.env`, the unit's one `EnvironmentFile=` at line 10 of `/etc/systemd/system/opal-gateway.service`).
- **APPLIED scope envelope = the code default** — `.env` sets NO `GRAPH_SCOPES` override (var-name enumeration of the live env file: 20 vars, none GRAPH_SCOPES). Code default (`app/config.py:48-56`, deployed md5 `20836f8a...` == repo): `User.Read Mail.Read Mail.Send Mail.ReadWrite Calendars.ReadWrite Files.ReadWrite.All Sites.Read.All Chat.ReadWrite ChatMessage.Send Team.ReadBasic.All Channel.ReadBasic.All ChannelMessage.Read.All ChannelMessage.Send OnlineMeetings.ReadWrite OnlineMeetingTranscript.Read.All Presence.Read.All Notes.ReadWrite.All`.
- **All delegated, never Application** (token_broker.py:6; IT_REQUEST.md: "every permission is Microsoft Graph delegated (never Application)") — a token only reaches the signed-in user's own data.
- **NO group-mail-capable scope consented:** no `Group.Read.All`, no `GroupMember.Read.All`, no `Mail.Read.Shared`.
- **Consent mechanics (the cost of any new scope):** tenant disables user self-consent → new scope = IT admin-consent round-trip, AND the scope list is PINNED FOUR-WAY (config.py == .env.example == IT_REQUEST.md == App-2 consent screen); any drift = the infinite admin-approval loop, measured twice (CVO 154315Z; Andrew+IT 2026-06-24). A group-mail scope add is NOT a one-click.

## 3. CVO-P0-1 — on-box capability grep (TO-B's §6 existence check) → **TO-B DOES NOT COLLAPSE**

SSM `AWS-RunShellScript` on `i-07dccb1615503ac99` (cmd `912d34e5-5838-4a5e-b11c-509ce9cd619b`), service `active`:

- **`/groups` in the DEPLOYED app: 0 hits** over the printed denominator of **31 .py files** under `/opt/opal-gateway/app`.
- **`users/` (other-mailbox Graph path): 0 hits** — every mail read is `/me/...` (delegated self-mailbox), corroborated live: this session's own search calls resolved through `users('2e21f8e5...')/messages` = the signed-in user.
- **shared-mailbox read path: NONE** — all `shared` hits are SHARED_SECRET auth-kind + the SharePoint "Shared" site; the only special mailbox machinery is the fixed OTP-mailbox reader (otp.py, delegated, Andrew's own mailbox).
- Instrument validity: the zeros are positive-controlled (the `shared` grep in the same command returned 20 rows) and denominator-framed; the inline `grep-rc=` echoes captured `head`'s rc, not grep's, and are DISCARDED as evidence.
- **Deployed-currency chain closed:** on-box md5 of server.py/tools.py/config.py/graph.py/token_broker.py == repo working tree == EC2_MANIFEST checksums @deployed_commit `81615fbd3e` (2026-08-15, 0.7.0_AE_CloudOps). And the deployed app was EXERCISED live by this session's own Graph reads through it.
- **R8 correction (supporting-evidence hygiene):** the PRD's "gateway app is NOT repo-resident (zero source files in-repo)" is stale — `infra/aws/ec2/opal-gateway/` is TRACKED at exactly the deployed commit (OPAL_GWRENAME landed it). The on-box read still ruled per the TO; the repo proxy is now strong.

**TO-B shape (for AE + COO):** the 4.1 build is REAL — no existing primitive to expose-and-wire. Two viable shapes, and the DL-type answer (Q3) picks between them:
- **(a) DL-membership delivery — zero new Graph consent:** add the Analyst identity `opalbloomberg@opalinvest.com` as a member of each DL → DL mail lands in its OWN mailbox → readable under already-consented `Mail.Read` via the existing `/me` path. The new gateway primitive reduces to a filtered read (`to:<DL> since:<cursor>`) + durable cursor. Membership add is an Exchange-admin act (IT/Andrew), not a Graph consent.
- **(b) group-mailbox / shared-mailbox read:** `/groups/{id}/...` or `/users/{dl}/messages` — requires `Group.Read.All` or `Mail.Read.Shared` = the four-way-pin consent round-trip per §2.

## 4. U3 — ticketing-center thread: NONE EXISTS → proposal recorded

- Analyst identity (`opalbloomberg@opalinvest.com`) team membership: exactly **1** — "Opal Capital" (`9c4ab816-548f-47af-913c-ad5d5086f5ad`), channels = {General, End of Day Updates}. No ticketing team/channel anywhere on either identity (Andrew's 5 teams enumerated: Opal OCIO, Opal CIO Office for 49 Financial, 49 Financial Internal Channel, Opal Consulting, Opal Capital).
- **PROPOSAL:** create a standard channel **"Ticketing Center" in the "Opal Capital" team** — the one team the Analyst is already in; the buzz then rides already-consented `ChannelMessage.Send` with zero membership or consent change. (Channel creation is a write — deferred past read-only TO-A; owner: Andrew one-click or bless the Analyst creating it.)

## 5. Analyst identity-scope finding (bears on TO-C)

`search_email` on the Analyst identity is **server-side DENIED**: `identity_scope_denied` — "scoped to a server-side tool allowlist... (OPAL_ANALYST PRD 4.3; widening is an Andrew ruling — route via 0.0.0_AB_MSTR~Z)". The guard fails closed and correctly. Consequence: the TO-C intake loop's mail-read on the Analyst identity needs EITHER the 4.1 primitive added to the Analyst allowlist at TO-B (natural), OR an allowlist widening ruling. Priced into TO-B/TO-C, not a blocker for TO-A.

## 6. The Andrew one-liner (routed via MSTR~Z)

> D7 TO-A: DLs found — 49F = `49@opalinvest.com`, Inflection = `inflection@opalinvest.com` (both measured off real partner requests); **Cottonwood: none found — confirm its DL or say the word and we add one.** Monitorable-mailbox: undetermined for both (need: are these classic DLs, M365 Groups, or shared mailboxes?) — **simplest v1 path is adding `opalbloomberg@opalinvest.com` as a member of each DL (zero new Graph consent, mail lands in the Analyst's own consented mailbox); the alternative (group/shared-mailbox read) costs an IT admin-consent round-trip** (no Group.Read.All / Mail.Read.Shared consented on App-2, and scope adds are the four-way-pin drift hazard). Ticketing thread: none exists — propose a "Ticketing Center" channel in the "Opal Capital" team (the one team the Analyst is in). One line back: (1) Cottonwood DL? (2) DL type / bless the membership-add path? (3) bless the channel?

## 6a. AMENDMENT 1936Z — ANDREW-DIRECT (relayed by 0.0.0_AB_MSTR~Z from his console, verbatim): *"We need to either change this email or create a new email to opalsupport@opalinvest.com. Can't be broadcasting 'opalbloomberg' externally"*

Effect on §3 option (a): the membership-add path survives ONLY with a non-broadcasting address. Candidate mechanism (MSTR~Z framing, at Andrew as one-liner item 4): an ALIAS `opalsupport@opalinvest.com` on the EXISTING Opal Bloomberg mailbox — delivery stays in the consented `/me` mailbox, so the zero-new-consent property is preserved; outbound send-as opalsupport. A separate NEW mailbox would break the delegated-`/me` consent path and re-price TO-B. Tenant-admin act = Andrew/IT-hand. Read §3(a) through this amendment.

**TO-B pricing note (2.0.0_SA_COO~Z 193929Z, INFERRED class — M365 default-config knowledge, NOT measured on this tenant): the alias mechanism is ASYMMETRIC.** Delivery-IN to the alias is free and preserves `/me` consent; outbound PRESENTATION as the alias additionally requires the tenant org setting `SendFromAliasEnabled` (M365 default OFF) — with it off, Graph-sent replies present as the primary (`opalbloomberg@`), the exact broadcast Andrew ruled against, discovered only at first outbound reply. Discharging check for TO-B (one line, IT/Andrew-hand or a permitted Graph read): verify `SendFromAliasEnabled`; if false, remedies are enable-it (tenant-wide) or INVERT — make `opalsupport@` the PRIMARY and `opalbloomberg@` the alias (same mailbox, same consent, presentation inverted; likely the cleaner shape for Andrew's intent). Prices TO-B/TO-C only — TO-A's scope never fires outbound.

## 6b. RULED 2026-08-20 ~0046Z (@c7aa4bb03a, relayed by MSTR~Z): D7 INTAKE PIVOTS TO A CLIENT-FACING DASHBOARD FORM — NO EMAIL INGESTION AT ALL

Consequences for this record: **every email-ingestion option in §3, §6, and §6a is DEAD BY RULING** — do not build, exercise, or price against them (TO-B stood down as scoped; the DL-membership and group-mailbox paths, the opalsupport alias/invert mechanics, and the SendFromAliasEnabled question are all MOOT, no action ever needed). What SURVIVES: the U1/U2/U3/capability measurements themselves (true at their vintage), the **U3 channel proposal — APPROVED** (creation rides the re-cut TO-C from CTO~Z's gate), and TAC-1, which **CLOSES fully-answered** (the one-liner was its gate-out). TAC-2's acceptance is re-cut at the gate; its DL-mail path is not exercised.

## 7. Surprise channel (banked, no action)

audit-archive-invoker at session start printed 3 integrity findings on this box: `ledger-hook-audit.log` + `rcg-sweep-audit.log` non-append edits (baseline≫live-head — plausibly the device-axis baseline class), `jq-ban-override-audit.log` live-missing (fail-closed error). Surfaced to MSTR~Z in the kickoff ACK; not adjudicated here.
