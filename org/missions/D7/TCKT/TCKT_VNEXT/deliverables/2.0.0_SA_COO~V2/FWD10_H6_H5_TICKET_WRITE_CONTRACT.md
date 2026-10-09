# CONTRACT -- NFRA_TRNSPT FWD-10, hop H6 -> H5: the commentary drafter writes its draft onto a Ticket Center ticket

Status: **v0.2** (2026-10-09; records the shipped behaviour, at `~T2`'s request in msg 2210; see section 8) -- v0.1 AGREED by both sides on 2026-10-08 -- proposed by `2.0.0_SA_COO~V2` (TCKT_VNEXT, the H5 / C-TICKET owner) to `2.0.0_SA_COO~T2` (NFRA_TRNSPT, H6).
It becomes AGREED when `~T2` commits an acceptance line in section 7. Routing: `1.0.0_SA_CTO~DELL2` msg 1779
(Andrew-direct record @a4fdb78bbe). PRD rows: NFRA_TRNSPT C-TICKET (`prd/NFRA_TRNSPT_PRD.md:118`), S20 (`:227`).

## 1. What is live today (measured at HEAD = deployed opal-ticket-api, source map da43155418, CodeSha256 y0UF...)

| need in C-TICKET | state | evidence |
|---|---|---|
| ticket type `analysis_request` | LIVE | `infra/aws/lambda/ticket_center/lambda_function.py:74-90` |
| requester may claim and complete their own ticket, all types | LIVE | `_sod_block` `:1040-1048` (requester clause removed; only "complete by assignee once claimed" kept) |
| requester name and firm on the ticket | LIVE | `create_ticket` `:977-987` (firm = `answers.firm`, server-checked against allowedFirmIds) |
| report reference on the ticket | LIVE, internal-human only | `report_ticket` `:1163-1205` (`report_ref.request_id`) |
| a SERVICE identity that may write a commentary ticket | ABSENT | `principal_class` `:247-263` knows only `svc-ticket-form`, `svc-analyst-intake`; any other service subject is UNRESOLVABLE |
| a field for the DRAFT text | ABSENT | `_new_item` `:451-500` |
| the 2026-08-12 security-state read before client-derived text enters a ticket | NOT DONE | C-TICKET precondition |

## 2. The call (H6 -> H5)

ONE call on the EXISTING write path; no second write path, no direct DynamoDB write, no Lambda-to-Lambda invoke past the authorizer
(the file's own law, `:6-7`).

```
POST {api_base}/api/scoped/tickets
Authorization: Bearer <svc-commentary token>      # Secrets Manager, `.token` of the JSON value -- the svc-analyst-intake
                                                  # precedent (integrations/ticketing/intake/runner.py:5-6)
Content-Type: application/json
```

Body (every field below is REQUIRED unless marked):

```json
{
  "ticket_type": "analysis_request",
  "title": "Draft commentary -- <firm> (<report_type>)   [v0.2: never built from household]",
  "source": "commentary:<request_id>",
  "answers": {
    "advisor": "<from the report request>",
    "firm": "<the report's firm id>",
    "household": "<v0.2: OPTIONAL for svc-commentary -- OMIT the key when the report carries none; never a placeholder>",
    "report_type": "Overview | Comparison | Multi-Comp",
    "comparison_model": "<required unless Overview>",
    "add_commentary": true
  },
  "attachment": {"upload_id": "<the report input's upload_id>", "input_id": "portfolio_<64 hex>"},
  "report_request_id": "<the READY report's request_id>",
  "draft_commentary": {
    "text": "<the draft, plain text, <= 8000 chars>",
    "model": "<model id the drafter called>",
    "generated_at": "<ISO-8601 UTC>",
    "status": "DRAFT"
  },
  "requester_email": "<the report generator's email>  (optional; display-grade)",
  "requester_name": "<optional; display-grade>"
}
```

## 3. What H5 builds so the call works (the TCKT_VNEXT cell)

1. `svc-commentary` principal class: `sub == "svc-commentary" AND userType == "service"`; MATRIX `CREATE` only. No LIST, GET,
   CLAIM, COMPLETE or REPORT.
2. On CREATE by `svc-commentary` only: accept `report_request_id` (stored as `report_ref = {request_id}`, the same shape
   `report_ticket` writes) and `draft_commentary` (validated: `status` must be `DRAFT`; text <= 8000 chars; no other keys).
   Any other principal sending either field gets a 400.
3. `answers.firm` must be within `svc-commentary`'s allowedFirmIds (the existing server check, `:983`).
4. The ticket is created `open` and routed by the existing ROUTING_MATRIX `analysis_request` entry. The DL notice fires as for any
   CREATE (`notify_dl_isolated`, `:995`) and carries NO draft text (`draft_commentary` joins the DL-prohibited fields).
5. Before the first draft is written, H5 reads the 2026-08-12 security finding against the deployed ticket table and API and
   records the read.

## 4. Responses H6 must handle

| status | meaning | H6 action |
|---|---|---|
| 201 `{"ticket": {...}}` | written | log `ticket_id`; done |
| 400 | contract violation (field, firm outside allowedFirmIds, bad draft) | dead-letter; NO retry |
| 403 | token not `svc-commentary` / not service | dead-letter; NO retry |
| 5xx / timeout | transient | retry via the H1 DLQ policy; the report is never blocked |

H6 never retries a 201 (no idempotency key in v0.1 -- see open item O2).

## 5. Stub (until H5 lands)

`~T2` stubs this call by asserting the body against section 2 and returning a synthetic 201 with
`ticket_id = "TCK-00000000-stub0000"`. No live write until H5's deploy closes.

## 6. Open items (named, not decided here)

- **O1 -- who mints the `svc-commentary` token** and whether the portal authorizer passes `userType: service` for it. The
  `svc-analyst-intake` token is the precedent; its issuer (TO-D, laptop) is the owner to ask. Routed to `1.0.0_SA_CTO~DELL2`.
- **O2 -- duplicate tickets.** A report filed through an Analysis Request ticket already has a ticket. v0.1 creates a NEW
  ticket for the draft. Appending the draft to the existing ticket needs the report to know its ticket (it does not today:
  `report_ref` lives on the ticket only). Proposed for the next round, not this one.
- **O3 -- `add_commentary`. RULED by `~T2` (msg 1816):** H6 drafts for EVERY READY report and sends `add_commentary: true`. Was: The form already asks it (`:87`, default false). Whether H6 drafts only when it is true is
  `~T2`'s and the CTO's call; this contract carries it as `true` on the drafted ticket either way.

## 7. Acceptance

- `2.0.0_SA_COO~V2` (H5): proposed v0.1, 2026-10-08.
- `2.0.0_SA_COO~T2` (H6): ACCEPTED v0.1 @a8410fcca3, msg 1816 (2026-10-08T22:33Z), recorded here by `~V2` at `~T2`'s request; H6 is `NFRA_TRNSPT.TO-TR-t12`.

## 8. v0.2 -- what shipped (opal-ticket-api live since 2026-10-09T01:01:08Z; handler file sha256 01534e2d..., box/dell2 3b04c040fc)

| item | v0.1 | v0.2, as shipped |
|---|---|---|
| `answers.household` | required | OPTIONAL for `svc-commentary` ONLY (type data `optional_for`, F10-l-2; CTO msg 1875). Omit the key. The ticket stores no household and no placeholder. Humans still must answer it |
| `title` | built from household | any non-empty string up to 300 characters (`create_ticket`). Use `Draft commentary -- <firm> (<report_type>)`; never put client identity in the title (C-KIMI) |
| firm check | the token's `allowedFirmIds` | the token carries NO firm reach. `answers.firm` must be in `COMMENTARY_ALLOWED_FIRMS` = `49financial,cottonwood,inflection` (env, never ALL). Any other firm returns 400 `requester_firm '<firm>' is outside the principal's allowed firms` |
| token (O1) | open | RESOLVED: secret `opal/ticketing/svc-commentary`, value JSON with `.token`. Claims: sub/name `svc-commentary`, userType/tier `service`, iss `opal-portal-auth`, aud `opal-portal-api`, exp 90 days (minted 2026-10-09 ~02:1xZ; rotate by exp - 14d). Readers today: the dell2 and dell1 agent users (row TCKT_VNEXT-D2-S9). H6's Lambda role needs its own grant, which is H6's pair |
| O2 (same ticket) | open | Package side: C-PACKAGE route `POST /tickets/{id}/package` is LIVE, and its principal ships EMPTY (refuses everyone) until IRPT_ANLREQ's L5 binds it. Draft side: H6 creates a new ticket (v0.1 unchanged) |

**Proven live** (applier `0.7.0_AE_CloudOps~DELL2`, leg M, @5c513af524):
- a `svc-commentary` CREATE with no household returns 201 (TCK-20261009-a1052909);
- an off-list firm returns 400 with the firm message;
- LIST returns 403;
- the token returns no firm data on non-ticket routes.

Section 4's response table stands.
