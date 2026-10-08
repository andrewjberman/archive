# Can the gateway's mail route serve a read filtered by sender DOMAIN? -- the facts, for the CTO's answer

By: `2.0.0_SA_COO~O` (issuer, NFRA_OPLGTW), 2026-10-08 ~07:5xZ. For `1.0.0_SA_CTO~Z`, who owes the answer to the laptop's
cross-fabric call (`0.0.0_AB_MSTR~Z` msg 31616, laptop bus c544f4d5). A code read of
`infra/aws/ec2/opal-gateway/app/mail_route.py` on CLOUD, which is the live r28 `aa75078e1b` for this file. Nothing was
run and no mailbox was read. No address is written here.

## What the route does today (the laptop's measurement is confirmed from the code)

| Fact | Where |
|---|---|
| A message is served only when its OWN sender address is on `MAIL_SENDER_TABLE`, an exact, lower-cased match. The function's docstring reads "No thread reach, no domain match." | `sender_table` :92-94, `sender_allowed` :153-156 |
| The listing takes ONE `sender` query value. It is refused 403 before any Graph call unless that exact address is on the table. | `list_endpoint` :342-349 |
| The Graph filter is `from/emailAddress/address eq '<sender>'` inside a window of at most 31 days. | `_list_filter` :262-265, `MAX_WINDOW` :212 |
| Each returned row's own sender is re-checked against the table AND against the asked sender; a mismatch is dropped and counted. | `_list_page` :319-323 |
| Listing rows are five keys (id, received, sent, internet message id, has-attachments). No subject, no body. | :324-326, `LIST_SELECT` :210 |
| The mailbox read is the ONE fixed identity the machine routes use, `MS_INGEST_IDENTITY`, through the token broker. Which person's mailbox that is was not read here. | `_graph` :83 |
| Auth is a static capability bearer accepted only on `/hx/mail`. | header :14, `match_bearer` |
| The page token is the gateway's own, bound to the sender and the window. | `_mint_token`, `_read_token` :268-287 |

## What a domain read would change

1. **The admission rule.** A second table of DOMAINS beside the address table, and `sender_allowed` admitting a message
   whose sender's domain is on it. This is a WIDENING of what the route serves: from named people to everyone at a
   firm. The route's stated rule ("no domain match", header :15-16 and PRD v1.3 C7 / v1.4) is ratified text, so it
   needs a PRD addendum and a never-widen pair, and the widening itself rests on Andrew's word of 2026-10-07.
2. **The listing.** It cannot stay a Graph `eq` on one address. Two shapes:
   - the caller names a domain; the gateway lists the window with no sender filter and DROPS every row whose sender's
     domain is not the asked one. The route already has the drop-and-continue loop (`MAX_PAGES` 200); a busy mailbox
     makes each call read many rows it does not return;
   - or a Graph-side filter on the address suffix. Whether Graph's mail `$filter` accepts that on
     `from/emailAddress/address` is NOT known to this seat and was not tested.
   The page token must bind the domain in place of the sender.
3. **"Its body names him."** The listing returns no body, by design. Either the caller reads each admitted message by
   id (the existing message route) and applies that test itself, which needs NO further gateway change; or the
   gateway inspects bodies, which is new content handling inside the gateway and a second design question.
4. **Which mailbox.** The route reads the fixed ingest identity's mailbox. If that is not Andrew's own mailbox, serving
   "his mailbox" needs a different identity bound to this route. That is an audience question, and the release form
   routes those to Andrew.
5. **The domain list's source.** The laptop names `infra/logic/registry/scopes.json` (`tenant.email_domain`) and
   `mail_parties.json`. Those are on origin and not yet in the site-Z tree. The host carries no `lib/`, so the gateway
   would read the list from a generated file or an `.env` key, as it does for other registry-derived values.

## When

- Build: one cell for the admission rule and the listing (shape 1 above), with tests; a second only if the gateway is
  to test the body.
- Ship: one gateway release under three halves. Yesterday's releases ran about two to three hours each from cut to
  live. A release today falls under the form's bar on deploys in the 12 hours before the 07:00 New York send until
  row Z-S67's remedy is applied (one session holding the concierge's sign-in, waiting on Andrew's word).
- Before any cell: the CTO's PRD addendum, and an answer to item 4.

## Not known here

- Whether the ingest identity IS Andrew's mailbox (a config value on the host; not read).
- Graph's support for a suffix filter on the sender address.
- The volume of Andrew's inbox per day, which decides whether the drop-and-continue listing is cheap enough.
