# COMM_ASSIST round 9 -- drain-end read: the laptop side of FWD-4 is built; its deploy is parked on site Z (2.0.0_SA_COO~R, 2026-10-09 ~01:4xZ)

Issuance `4b7b1bd011` (merged `af564065fb`), decomposition `decompositions/COMM_ASSIST_DECOMP.round9.md`. Both orders terminal.
Nothing deployed. Push state: `box/laptop`, LOCAL.

| cell | landed | merge | proof | issuer re-run |
|---|---|---|---|---|
| CA-m-1 | `MailGateway` (bearer from `MAIL_BEARER_SECRET`), `mail_poll.poll`: per firm domain, own cursor, 300 s cadence, 20 calls, first run silent, one `mail.messages` event per message on `mail:<id>` | `68ef6d0cdd` | VALID | `MAIL-POLL ok=True arms=8/8` (two planted mutants caught by the worker) |
| CA-m-2 | every considered mail texted once with a draft reply in his voice and `CLIENT <firm>` / `Opal`; work lines only for a request; a failed draft still texts; `1` on mail points to Outlook; never sent | `b986bd863f` | VALID | `MAIL-DRAFT ok=True arms=7/7 base_texts_client_no_request=0`; `INBOUND-MAIL-TEST 15/15` |

Hookup `31980c736e`: `tenant.ingress` gains `"mail": _safe("mail", _poll_mail)`. The step returns `not-configured` and calls
nothing until the function has `MAIL_BEARER_SECRET`, so no failure is logged each minute before the deploy. After the hookup,
every agent check is green (list in the hookup commit).

## Deploy: PARKED, owner 2.0.0_SA_COO~R

**Un-park condition:** site Z deploys NFRA_OPLGTW OG-md-1 with the firm domains on its domain table (today it is BUILT AND HELD,
`15b08fdca1`, table empty).

**The pair it will need** (C-PACKAGE: the half lists every packaged file):
- the package (`teams_chat/` with `mail_poll.py`, `mail_requests.py`, `assist.py`, `tenant.py`);
- the new environment variable `MAIL_BEARER_SECRET` (the secret's name) on both functions;
- the agent role's read of that one secret;
- a bearer value the gateway's `MAIL_BEARER` accepts, issued by site Z.

**Its exercise:** FWD-4 needs one real client email naming Andrew, texted with a draft and the flag.

## Observation (not a row)

`mail_requests.py --check-domains` reads `firms=4/5` (one party has no recorded domain), as at round 3 (CT-i-5). The domain table
site Z admits should be read against the same five parties when it ships.
