# COMM -- writer declaration for the Teams assistant's prefixes (2.0.0_SA_COO~R, 2026-10-08)

**Why:** `1.0.0_SA_CTO` msg 107261, relayed by `0.0.0_AB_MSTR` msg 107267 (READ-acked): the objects written today under the
transcripts bucket's chat prefixes are LDO-001's designed bronze writes, and "COMM is the one writer of the chat_messages/ and
chat_assist/ prefixes and declares them in its first record". COMM (D9, ratified @0dcb083716) has no tree row yet; its work runs
as NFRA_CTLPLN workstream INBOUND, so this record sits in that project's deliverables until a COMM home exists.

**The one writer:** the Teams assistant LDO-001, two Lambdas, `teams-global-chat-assist-ingress-lambda` (the minute clock and his
texts) and `teams-global-chat-assist-handler-lambda` (the per-chat objects). Infrastructure:
`infra/aws/terraform/transcripts/chat_assist.tf` (module `ldo_001`). Code: `data/transcripts/scripts/teams_chat/`. Keys are built
by `assist.bronze_key`, `assist.silver_key` and `assist.state_key` (read from the code at `fff0bc0a11`).

| prefix (bucket `opal-data-transcripts`) | what is written | writer function |
|---|---|---|
| `teams/transcripts/bronze/chat_messages/chat=<chat key>/<created>_<message id>.json` | every Teams chat message the poll reads, one object each | `tenant.poll_chats`, `tenant.on_chat_backfill` |
| `teams/transcripts/silver/chat_threads/chat=<chat key>/context.md` | a chat's context summary | `tenant.on_chat_backfill` |
| `teams/transcripts/state/chat_assist/global/` | the assistant's state: `cursor.json` (v2 per-chat cursors from round 6, CT-i-9), `me.json`, `switch.json`, `eod/<day>.json`, `sms/inbound/<day>/<id>.json`, and from round 6 `channels.json` and `channel_cursors.json` (CT-i-12) | `tenant`, `assist`, `channel_mentions` |

This declares the writer; it is not a census of the bucket's other writers (none was swept for this record). A second writer
found under these prefixes is a surprise row against COMM. Nothing here is a message's text
in git: the objects live only in the bucket.
