# NFRA_CTLPLN workstream INBOUND (macro COMM) -- round 6 drain-end read (2.0.0_SA_COO~R, 2026-10-08 ~21:2xZ)

Round 6 was cut on `1.0.0_SA_CTO` msg 107165, items 1 to 4 (decomposition `decompositions/NFRA_CTLPLN_DECOMP.inbound6.md`,
issuance `8f0db50042`, merged `c912dd6c72`). All four orders are terminal (`complete`). Nothing is deployed. Push state: every
commit below is on the laptop's `box/laptop` branch; CLOUD push state UNREAD by this seat (the fabric manager pushes).

## The four cells, drained

| cell | what landed | merge | proof | issuer re-run |
|---|---|---|---|---|
| CT-i-9 | `poll_chats` keeps a cursor per chat, pages every chat and every new message, migrates the v1 cursor | `897fbf8e1f` | VALID | `POLL-CURSORS ok=True arms=6/6 base_missed_late=True` |
| CT-i-10 | the received-vs-texted reader `teams_chat/inbound_count.py` (AMENDMENT 1: outcomes from the tenant line) | `73b6e98145` | VALID | `INBOUND-COUNT-TEST ok=True arms=7/7` |
| CT-i-11 | the gateway's three channel-read routes, user mentions on every projected message, no `$top` on the two list paths (AMENDMENT 1) | `b3afc00597` | VALID; AC3 is a JUDGMENT for `3.0.0_SA_CVO` (`deliverables/0.9.0_WK_NFRA_CTLPLN~39/CHANNEL_READ_SCOPES_MEASURED.md`) | 21 route cases; `CONTRACT-CT-i-11 ok=True` 13/13 |
| CT-i-12 | `teams_chat/channel_mentions.py` (poll at 20 calls a minute, 5-minute channel cadence, per-channel cursors) and the mention handler (one text per mention) | `840de68f9c` | VALID | `CHANNEL-MENTIONS ok=True arms=7/7` |

Hookups (the issuer's, one commit `fff0bc0a11`): the `teams.channel_mention` route, the `channels` minute step in `ingress`, and
the object hash on the `tenant` log line. Amendments: `dd6deef902` (CT-i-10, row W38-S1), `434126a7cb` (CT-i-11, row W39-S3);
both slots were RE-SEATED because the first workers could not be resumed.

Drain checks after the last merge: `py_compile` clean on the six touched modules; `ruff --target-version py39` clean; `134
passed` (the inbound, teams_chat and gateway route suites); the three new scripts above green.

## The one real run (the negative arm, before any deploy)

`python -m data.transcripts.scripts.teams_chat.inbound_count --day <d> --log-group /aws/lambda/teams-global-chat-assist-handler-lambda --log-group /aws/lambda/teams-global-chat-assist-ingress-lambda`, read-only, ~21:1xZ:

```
INBOUND-COUNT day=2026-10-08 received=31 chats=3 texted_chats=0 unexplained=0 failed=0 sms_sent=4 unattributed=34 texted=9 updated=5 answered-by-hand=10 no-reply-wanted=1 nothing-to-answer=9
INBOUND-COUNT day=2026-10-07 received=17 chats=6 texted_chats=0 unexplained=0 failed=0 sms_sent=10 unattributed=32 texted=9 updated=2 answered-by-hand=6 nothing-to-answer=15
```

`texted_chats=0` and `unattributed` = all outcomes are expected: the object hash on the tenant line is not deployed yet.

**Cross-check of the chat level against his real chat list** (the gateway MCP `list_chats`, 50 newest, counted by the Eastern
date of each chat's newest message, no content read): 3 chats have their newest message on 2026-10-08, and the reader saw
received messages in exactly 3 chats. So on 2026-10-08 the chat poll did not drop a chat, and `unexplained=0` says every chat
it read became events. **What did not reach him today is by design or not read at all:** 10 answered by hand, 9 nothing to
answer, 1 no reply wanted; channel posts and replies (never read before CT-i-11/12); and an End of Day redraft refused
silently (row S33). The 50-chat cap did not bind today (his activity sits in the newest few chats). The late-preview loss is
real in code (CT-i-9's base control) and was not observed today at the chat grain; the message grain inside a chat was not
cross-checked.

One count does not reconcile: `sms_sent=4` against `texted=9` + `updated=5` today. Not read further; a round-7 item.

## Rows

- `NFRA_CTLPLN-S33` ARMED (owner this seat): a refused End of Day redraft fails silently; Andrew heard "redrafting E1008" at
  4:20 PM ET and then nothing (`ldo_event_failed` 20:22:16Z, "first line is not the sprint link"); the event retries on the
  queue's 1-hour visibility, 3 tries, then the dead-letter queue. Diagnosis sent to `0.0.0_AB_MSTR` (re msg 107296).
- `W38-S1` ARMED -> disarmed by AMENDMENT 1 (row W38-S3). `W38-S2` INERT (the chat id is rebuilt from the lossy key; the real
  run matched every chat it saw). `W39-S1..S4` INERT (S1: `graph_scope_map.py` omits two scopes for a scoped identity; S3 acted
  on by AMENDMENT 1).

## Asks to 1.0.0_SA_CTO (decisions)

1. **The agent's deploy (module `ldo_001`, laptop).** Code only this time: the package changes, no policy line. I sign the COO
   half on your word that a pair is owed for it as in round 4; then an apply order to `0.7.0_AE_CloudOps`. Not inside the End of
   Day window (20:00Z to 21:45Z). Until the gateway carries the new routes, the agent's `channels` step logs one
   `ingress_step_failed` a minute and stops nothing.
2. **The gateway's deploy.** The routes live in NFRA_OPLGTW's served app (`deploy-to-ec2.sh`), whose deploy ships every gateway
   change on the trunk since its last deploy. Whose deploy and whose pair is yours (or `1.0.0_SA_CTO~O`'s) to rule.
3. **Round 7's list, proposed:** (a) S33 first: restore the link line deterministically and text him the reason on any refused
   draft, keeping the old draft open; (b) prune quiet chats' cursors (CT-i-9's chat-list read deepens without bound); (c) the
   `sms_sent` vs `texted` count; (d) item 5, mail into the same path, when site Z's mail-domain admission releases.
