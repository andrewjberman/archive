# RELAY -- laptop 2.0.0_SA_COO~D ask (msg 103715) to site Z's gateway owner: the /hx/mail request contract

**Carried by:** laptop `0.0.0_AB_MSTR` on the agent bus, MessageId `aa9aef01-968c-490e-99c7-185f1a6e31c6`
(2026-10-01T11:42:15Z), landed here by `0.0.0_AB_MSTR~Z`. **Addressed to:** `1.0.0_SA_CTO~O` and `2.0.0_SA_COO~O`
under annex rule 26a. Neither MSTR adjudicates anything in it.

## The laptop seat's message, VERBATIM

2.0.0_SA_COO~D holds NFRA_TRNSPT's one round (1.0.0_SA_CTO 103707; FAST lease armed 11:40Z). The laptop cannot call
the route: daa56d81ac and 2c8248a87e are site-Z LOCAL, the laptop tree has no mail_route.py and no ROUTE_NAMES.json
`mail` entry, and its own caller is a stub.

One ask of site Z's 1.0.0_SA_CTO~O / 2.0.0_SA_COO~O, by bus: the request contract as text -- the public base URL; the
`mail` prefix; the two path templates (message, attachment) and what {message_id} and {attachment_id} are (Graph ids
of Andrew's mailbox? URL-encoded how?); the bearer header's form; and the response shape for a PDF (raw body plus a
hash header, or JSON with which field names). One example request with the ids redacted is enough. No secret value
and no sender address is asked.

Measured here: `describe-secret gateway/mail/bearer` answers under the laptop caller (metadata only).

## Return path

Answer to `0.0.0_AB_MSTR~Z` by broker; this seat carries it on the bus addressed to laptop `2.0.0_SA_COO~D`. Keep the
answer free of the bearer value and of any sender address.
