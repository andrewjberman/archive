# MAIL_ROUTE_MEASURED -- NFRA_CTLPLN.TO-CT-i-3, step 1

By 0.9.0_WK_NFRA_CTLPLN~31, 2026-10-07. Everything below is a READ of code and documents in the worktree
(branch wk-NFRA_CTLPLN-31). No request was made: no gateway call, no mailbox read, no model call. BLIND: whether the
deployed gateway matches this source is not measured; the cited relay documents say site Z read the SERVED code at
opal-gateway `daa56d81ac7c91795f1a9c47b2c2430cb3879e24` for the by-id routes, and the listing route (OG-hl-1) is in this
tree's source but its release is not measured here.

## 1. What the gateway's headless mail route allows today

Route source: `infra/aws/ec2/opal-gateway/app/mail_route.py`. Caller: `data/transcripts/scripts/outlook/gateway_mail.py`.
Contract as relayed: `org/tier0_exec/0.0.0_AB_MSTR/deliverables/RELAY_20261001_1151Z_SITEZ_GATEWAY_OWNER_HX_MAIL_REQUEST_CONTRACT_FOR_COO_D.md`
(by-id routes) and `.../RELAY_20261001_1252Z_LAPTOP_COO_D_103750_HX_MAIL_LISTING_ROUTE_ORDER.md` (the listing).

| question | answer | file:line |
|---|---|---|
| which paths | four, all GET: `/hx/mail/messages` (listing), `/hx/mail/messages/{id}`, `.../{id}/attachments`, `.../{id}/attachments/{aid}` | mail_route.py:7-11, 48-53 |
| can it LIST messages | yes, for ONE named sender per call and a window of at most 31 days; rows carry only id, receivedDateTime, sentDateTime, internetMessageId, hasAttachments (no sender, subject or body) | mail_route.py:7, 24-26, 210, 333-377; gateway_mail.py:131-165 (`list_page`, `list_rows`) |
| does it return a body | yes, the by-id message answer carries `body` ({contentType, content}), `subject`, `from`, `toRecipients` | mail_route.py:55-58, 401-402; relay 1151Z "Response shapes" |
| which senders it admits | ONLY a message whose own sender address is an exact member of `MAIL_SENDER_TABLE` (today 3 addresses, the YCharts authors). "No thread reach, no domain match." Any other sender: `403 sender_not_allowed`; an empty table refuses everything | mail_route.py:15-16, 92-94, 153-156, 342-349, 395-400; gateway config.py:246 |
| the listing's sender | `sender` must itself be on the table, else 403; so a listing of "everything addressed to Andrew" does not exist | mail_route.py:342-349 |
| auth | one static bearer, secret `gateway/mail/bearer`, read by name at call time | gateway_mail.py:37-39, 61-66; mail_route.py:105-143 |
| write verbs | none: every Graph call is a GET through a fail-closed path allowlist | mail_route.py:19, 63-70 |

`gateway_mail.py:16` still says "There is NO listing route"; the same file defines `list_page` at :131, so that docstring
sentence is stale against its own code (the listing was added after it was written).

## 2. What a read of his mailbox for requests under clause 9 needs that the route does not give

Clause 9 admits a message by the sender's DOMAIN (five domains) and by the body naming Andrew. The route admits by exact
sender ADDRESS from a 3-address table and has no domain match (mail_route.py:154 states "no domain match"). Concretely:

1. **No enumeration by domain or by recipient.** The listing needs one table-listed `sender`; the clause needs every message
   to him from any address at five domains. A new listing parameter (a domain, or "all mail to the mailbox in a window") is
   a C7 addition on NFRA_OPLGTW.
2. **No admission by domain.** A message from a firm address not in `MAIL_SENDER_TABLE` is refused 403 before its body is
   returned (mail_route.py:399-400). The gateway's table would have to be widened to domains, which changes what the
   gateway serves and is its owner's decision.
3. **The listing rows carry no sender** (mail_route.py:210, row keys), so a caller cannot pre-filter by domain from the
   listing and would have to fetch each message by id; each of those is a 403 unless admitted by item 2.
4. **Two tests, one place.** The clause says a failing message is not passed to a model. The route returns the body to the
   caller regardless, so the clause is enforced by `considered()` in the caller (built in `mail_requests.py`), BEFORE
   the model; the gateway cannot do it for the caller.
5. **A poll clock and an event.** Nothing today turns a read into a `mail.messages` event for the tenant; that is the
   deploy order after the drain (the order's preflight says so).
6. **Not measured:** whether the laptop principal may read the bearer secret (relay 1151Z says that is not measured).

Result: this cell builds the consideration and the handler; the real read cannot be made until the gateway change in items
1-2 exists.

## 3. Where the estate records each of the five firms' mail domains

Clause 9 names Cottonwood, Inflection, 49 Financial, Alongside, and Opal (internal). Read by `lib.opal_naming.load_registry()`
the way `outlook/criterion.py:23-30` does (scopes with `class == FIRM`, `tenant.email_domain`), restricted here to
`tenant.kind == "client"` so the demo tenant is not a sixth firm.

| firm | path | key | value claim | status |
|---|---|---|---|---|
| Cottonwood | `infra/logic/registry/scopes.json` (scope `cottonwood`); mirrored by `data/firm_registry.json` firms[].email_domain; portal `portal/src/lib/firmAccess.ts:151` FIRM_EMAIL_DOMAINS | `tenant.email_domain` | held (Andrew ruling recorded in firm_registry.json `_meta.grounding.email_domain`; no `measured` field) | recorded |
| Inflection | same | same | held (same grounding) | recorded |
| 49 Financial | same | same | held (same grounding) | recorded |
| Alongside | none. No scope in scopes.json, no firms[] row in firm_registry.json, no entry in FIRM_EMAIL_DOMAINS or `comp-constants.config.yaml:667`. The word appears only as a mission label (`.tools/comp_missions.py:658` "EXTERNAL.ALONGSIDE") | none | absent | NO recorded mail domain: row filed, BLOCKING for this firm only |
| Opal (internal) | none in the firm records: no OPAL scope with a tenant, no firms[] row, no FIRM_EMAIL_DOMAINS key (the portal treats `opal-capital` as the internal firm id with no domain, firmAccess.ts:21). The domain string occurs only (a) inside the gateway's own constant `infra/aws/ec2/opal-gateway/app/sender_gate.py:27` `_OPAL_DOMAIN`, its Teams sender gate, and (b) inside two author addresses in `data/transcripts/assets/authors.json:5,11` and `criterion.py:36` | none | absent from the firm records (a held constant in the gateway's code, a different service's source) | NO recorded mail domain in the firm records: row filed, BLOCKING for this firm only; nothing is read from the gateway's constant or typed |

So three of five load. The build reads those three, considers mail from no other domain, and `--check-domains` is run with
`--expect-missing 2`.

## 4. What telling a mail requester the outcome would need (not built)

Reply by mail is not built. It would need: a send route on the gateway (today none exists and the mail route is GET only,
mail_route.py:19), a Graph send grant for the gateway identity (not in the delegated read scope this route uses), a decision
whether the outcome goes out as Andrew's own message or from a service address, and Andrew's `1` before anything is sent,
as nothing goes to a Teams chat without his `1` (assist.py module docstring). Until then a mail request ends at the text to
Andrew; he answers the requester himself.
