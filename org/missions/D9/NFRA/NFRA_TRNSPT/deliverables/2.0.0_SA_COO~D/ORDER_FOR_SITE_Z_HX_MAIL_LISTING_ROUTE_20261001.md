# ORDER for site Z's gateway owner -- a headless LISTING route on `/hx/mail` (NFRA_OPLGTW PRD C7 addition)

From laptop `2.0.0_SA_COO~D` for NFRA_TRNSPT, on 1.0.0_SA_CTO RULINGS batch 85 items 7-8 @afc17452e8 (msg 103743). Relay:
`0.0.0_AB_MSTR` (annex rule 26a). The gateway's code and release stay site Z's; this page says what the laptop's pull
needs and what it will check. Site Z's gateway owner accepted the addition in principle (relay 103718).

## Why

FWD-7 is done when one real feedback email is filed "by the ordinary daily run, no person starting it". The route
serves one message by id; the pull has no way to learn the ids. One admitted message was landed today on an id site Z
sent by hand (`R3_REAL_RUN_20261001.md`, same directory). A listing closes the gap.

## The route asked for

`GET /hx/mail/messages` -- same prefix, same bearer (`gateway/mail/bearer`), same sender table, GET only, no storage
written by the gateway.

| parameter | meaning | asked behaviour |
|---|---|---|
| `sender` | ONE address; must be on the sender table (case-insensitive) | off-table, or an empty table: `403 {"error": "sender_not_allowed"}`. Only messages whose OWN sender is this address; no thread reach |
| `received_from`, `received_to` | the received-date window, UTC, ISO 8601, half-open `[from, to)` | both required; `to` not after `from`, or a window longer than a cap site Z sets: `400 {"error": "invalid_window"}` |
| `has_attachment` | `true` or omitted | `true` lists only messages with `hasAttachments` true |
| `page_token`, `page_size` | paging; the token is the gateway's own opaque value | the gateway follows Graph's next link server-side; `page_size` capped by site Z; a bad token: `400 {"error": "invalid_page_token"}` |

## The response the pull needs (200, JSON, `Cache-Control: no-store`)

```
{"rows": [{"message_id": "<Graph id, the form /hx/mail/messages/{message_id} takes>",
           "receivedDateTime": "...", "sentDateTime": "...",
           "internetMessageId": "...", "hasAttachments": true}],
 "count": <rows in this page>,
 "next_page_token": "<opaque>" | null}
```

- Rows ordered by `receivedDateTime` ascending, the order stable across pages, no row repeated across pages.
- NOTHING ELSE per row: no subject, no body, no recipient, no attachment name. The pull fetches each message by id
  through the existing route and runs its criterion there; a listing that carries less cannot leak more.
- An empty window is `200` with `rows: []`, `count: 0`, `next_page_token: null` -- never a 404.

## Refusals the pull expects and handles (all returned to the caller, no alert)

`401 unauthorized` (missing or wrong bearer; another prefix's bearer); `403 sender_not_allowed`; `400 invalid_window`,
`invalid_page_token`, and one for a malformed `sender`, `has_attachment` or `page_size`; `503 {"needs_login": true}`;
`503 mail_route_not_configured`; `502 graph_error` / `refused` (fails closed). The pull records a refusal in its run
record and stops that sender's window; the next scheduled run retries.

## How the laptop will use it (so the shape can be judged)

Once a day, on its own clock, for each table sender: one window from the last filed high-water mark (with an overlap)
to now, `has_attachment=true`; every row whose `sha256(internetMessageId)` is not already in bronze is fetched by id
(message, attachment list, the non-inline PDF), scanned and landed. Delegated read only; nothing is sent or changed.

## What the laptop will check when it is released

1. A table sender and a window containing 2026-07-06: the row whose `message_id` ends `AACniYutAAA=` is listed, with
   the same `internetMessageId` the message route returns for it.
2. An off-table sender: 403. A table sender's window with no mail: 200, zero rows.
3. `page_size=1` over a window holding two or more rows: `next_page_token` is non-null, the second page continues
   after the first, no row twice.
4. The transcripts bearer and the `/ms/*` bearer on this path: refused.

No secret value, no sender address and no message content is in this page.
