# NFRA_OPALAI round 2 -- item-0 close run, deliberate arms: the run file (2.0.0_SA_COO~AI, 2026-10-09 ~07:1xZ)

Ruling: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_UNBLOCK_OPALAI_CLOSE_RUN_DELIBERATE_ARMS_20261009.md`
(fold of unblock `UB-20261009T054344Z-1afa`, CVO-signed with the FWD-1 limit below). Card:
`CLOSE_RUN_CARD_20261002.md` in this folder; these arms stand in for its step 3 as the cutover gate (C5).

## Registered rows (C3) -- written before the release; nothing below is designed after r29

| arm | chat_id | message_id | sender (measured) | key (C2) | expected result |
|---|---|---|---|---|---|
| (b) refused, run FIRST | `19:2e21f8e5-55ca-45c1-91b9-a4607bf28d4f_ad037ea5-fee8-412e-9da9-15c6cf2a4fbc@unq.gbl.spaces` | `1791494553407` | Andrew Berman, oid `2e21f8e5-...`, 2026-10-08T21:22:33Z | `json/benchmarks/etf_returns.json` | refused `asker_no_profile`, with the how-to-get-access line, and no data read |
| (a) admitted, run SECOND | same chat | `1791494398066` | Alyssa Keith, oid `ad037ea5-...`, 2026-10-08T21:19:58Z | `json/benchmarks/etf_returns.json` | the figure, the as-of date, the source and the scope; the CVO grades J2 against the portal for that date |

Invocation per arm (C1: read-only; no Teams send; the answer returns to this seat only):
`opal_asker_query(chat_id=<row>, message_id=<row>, key="json/benchmarks/etf_returns.json")`.

## Measured at registration (2026-10-09 ~07:0xZ)

| item | value | claim |
|---|---|---|
| both message ids exist with the senders above | `read_chat_messages` on the chat, top 15 | measured |
| the key is catalogued and servable | `opal_describe`: catalogued, channel `benchmarks_and_models`, firm_scope `opal-internal`, gate SERVE | measured |
| the key's channel is inside Alyssa's grant | OA-g-3 proof of spec: `portal_channels` includes `benchmarks_and_models`, operations `[query]`, dates `rolling_complete_window` | held (recorded 2026-09-27, not re-read from DynamoDB) |
| the key's as-of value | SUPERSEDED 2026-10-09 ~08:5xZ (UB-9a05): the served object reads `data_as_of` **2026-10-07**, `generated_at` 2026-10-08T12:04:14Z (`gateway_query_catalog`, 5 ETFs). The 2026-08-10 first written here was the catalog row's certification value (held) and is stale | measured |
| the key's write cadence | the publisher rewrites the key daily at about 12:04Z, so the served value can move between arm (a) and the CVO's read | measured once (`generated_at`); the daily cadence is the CRO's reading, held |
| the gateway's reading principal | `whoami` reads `Andrew@opalinvest.com`, not an `opalbloomberg` principal as the CRO approach states. The tool takes the asker from the message SENDER, so the caller's identity does not decide either arm | measured |
| the CVO can read the key itself (C2) | the key is a plain catalog key served through `gateway_query_catalog`; the CVO's own read is the CVO's act | held |

Before r29 serves, `write_class_denied` is the expected reading and is not a FAIL (C4). Arm (a)'s as-of date is read
against a `rolling_complete_window` grant; whatever the gateway returns is recorded raw and graded, never
predicted here.

## The clock (C4)

The arms run at the first read after NFRA_OPLGTW r29 (`NFRA_OPLGTW.TO-OG-rl-15`, `<status>pending</status>` at
07:0xZ) serves, never before. That order fixes its own window from 11:00Z.

## Results (filled at the run)

| arm | run at (UTC) | raw response | pinned reference read (same minute) | verdict |
|---|---|---|---|---|
| (b) | | | n/a | |
| (a) | | | `gateway_query_catalog("json/benchmarks/etf_returns.json")`: `data_as_of`, `generated_at`, raw body | the CVO's J2 grade |

**J2 grades against the pinned reference read**, taken by this seat in the same minute as arm (a), never against a later
portal read: the key is rewritten daily at about 12:04Z, so a later read can differ from a correct answer.

## What a pass does and does not prove

On PASS of both arms the card's "After a pass" acts follow: OA-t-1 r2 and OA-t-3 r2 merge, the BG launch retires (PRD
C11), OA-e-8 measures speed. Per the CVO's sign-off limit, the arms prove the gateway's entitlement mechanism only.
FWD-1 stays NOT_REALIZED until step 4's released Analyst answers a real portal-figure question on its own and the CVO
grades it. Step 4 (the Analyst relaunch) is `0.0.0_AB_MSTR~Z`'s PROCEED act under /govern.
