"""OG-rl-2 AC1 (PRD v1.4 release acceptance) against the SERVED gateway: the laptop's four checks (order 103750) plus the
issuer's two page-token negative arms. Never prints a bearer, an address, a body or a value.

usage: python _lst_arms.py <route_names.json>
Prints one line per condition (9), then: LIST ARMS <n> of 9.
"""
import importlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import boto3

sys.path.insert(0, os.path.join(os.getcwd(), "data", "transcripts", "scripts", "outlook"))
BASE = "https://mcp.opalinvest.dev"
KNOWN_MSG_TAIL = "AACniYutAAA="  # the laptop's check 1: a table sender's message received 2026-07-06
doc = json.load(open(sys.argv[1], encoding="utf-8"))
sm = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
bearer = {k: sm.get_secret_value(SecretId=doc[k]["secret_name"])["SecretString"].strip() for k in ("transcripts", "mail")}
bearer["ms"] = sm.get_secret_value(SecretId="opal/mcp/ms-ingest-token")["SecretString"].strip()
authors = list(importlib.import_module("criterion").DEFAULT_AUTHORS)
primary = [a for a in authors if a.lower().split("@")[0] == "manav" and a.lower().endswith("@opalinvest.com")][0]
other = [a for a in authors if a != primary][0]
LIST = doc["mail"]["prefix"] + "/messages"


def get(path, who, **query):
    url = BASE + path + ("?" + urllib.parse.urlencode(query) if query else "")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + bearer[who]})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8") or "{}")
        except ValueError:
            return e.code, {}


arms = []
# 1. a listed row equals the message route's internetMessageId
st, body = get(LIST, "mail", sender=primary, received_from="2026-07-06T00:00:00Z", received_to="2026-07-07T00:00:00Z")
rows = body.get("rows") or []
hit = [r for r in rows if str(r.get("message_id", "")).endswith(KNOWN_MSG_TAIL)]
same = False
if hit:
    st2, msg = get(doc["mail"]["probes"]["message"].format(prefix=doc["mail"]["prefix"], message_id=hit[0]["message_id"]), "mail")
    same = st2 == 200 and msg.get("internetMessageId") == hit[0].get("internetMessageId")
keys_ok = all(set(r) == {"message_id", "receivedDateTime", "sentDateTime", "internetMessageId", "hasAttachments"} for r in rows)
arms.append(("known row listed, internetMessageId equal, rows minimal (%d rows)" % len(rows), st == 200 and same and keys_ok, st))
# 2a. off-table sender refused
st, _ = get(LIST, "mail", sender="nobody@example.invalid", received_from="2026-07-06T00:00:00Z", received_to="2026-07-07T00:00:00Z")
arms.append(("off-table sender", st == 403, st))
# 2b. empty window
st, body = get(LIST, "mail", sender=primary, received_from="2020-01-01T00:00:00Z", received_to="2020-01-02T00:00:00Z")
arms.append(("empty window 200, 0 rows, null token", st == 200 and body.get("rows") == [] and body.get("count") == 0
             and body.get("next_page_token") is None, st))
# 3. paging page_size=1 continues without a repeated row
win = dict(sender=primary, received_from="2026-08-01T00:00:00Z", received_to="2026-08-31T00:00:00Z", has_attachment="true")


def page_all(window):
    """Follow next_page_token with page_size=1; returns (ids, pages, first_token, all_200, last_status)."""
    ids, tok, n, first, good, last = [], None, 0, None, True, None
    while n < 20:
        params = dict(window, page_size="1", **({"page_token": tok} if tok else {}))
        last, payload = get(LIST, "mail", **params)
        if last != 200:
            good = False
            break
        ids += [r["message_id"] for r in payload.get("rows") or []]
        tok = payload.get("next_page_token")
        first = first or tok
        n += 1
        if not tok:
            break
    return ids, n, first, good, last


seen, pages, first_token, ok3, st = page_all(win)
ok3 = ok3 and len(seen) >= 2 and len(seen) == len(set(seen)) and first_token is not None
arms.append(("paging page_size=1: %d rows over %d pages, no repeat" % (len(seen), pages), ok3, st))
# 4. the transcripts and /ms/* bearers refused on the listing path
st_t, _ = get(LIST, "transcripts", **win)
st_m, _ = get(LIST, "ms", **win)
arms.append(("transcripts bearer refused", st_t == 401, st_t))
arms.append(("/ms bearer refused", st_m == 401, st_m))
# 5. a page token with an altered sender or window is refused 400
st_s, _ = get(LIST, "mail", **dict(win, sender=other, page_size="1", page_token=first_token or "x"))
st_w, _ = get(LIST, "mail", **dict(win, received_to="2026-08-30T00:00:00Z", page_size="1", page_token=first_token or "x"))
arms.append(("token replayed under another table sender refused", st_s == 400, st_s))
arms.append(("token replayed under an altered window refused", st_w == 400, st_w))
# 6. a token carrying a raw Graph URL is refused 400
raw = "https://graph.microsoft.com/v1.0/me/messages?$skiptoken=abc"
st, _ = get(LIST, "mail", **dict(win, page_size="1", page_token=raw))
arms.append(("raw Graph URL token refused", st == 400, st))
n = 0
for label, ok, st in arms:
    print("arm %-62s status=%s %s" % (label, st, "OK" if ok else "FAIL"))
    n += 1 if ok else 0
print("LIST ARMS %d of %d" % (n, len(arms)))
