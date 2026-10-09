"""MS-rr-1: drive ONE domain refusal through the deployed app/asker_scope.py and print the SEAM line. Fakes only."""
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone

ap = argparse.ArgumentParser()
ap.add_argument("--gateway", required=True)
gw = os.path.abspath(ap.parse_args().gateway)
sys.path.insert(0, gw)
audit_path = os.path.join(tempfile.mkdtemp(prefix="rr1_"), "audit.jsonl")
os.environ["AUDIT_PATH"] = audit_path
os.environ.pop("AUDIT_S3_BUCKET", None)
os.environ.setdefault("TENANT_ID", "11111111-1111-1111-1111-111111111111")
os.environ.setdefault("CLIENT_ID", "test-client")
os.environ.setdefault("CLIENT_SECRET", "test-secret")

from app import asker_scope as asc, audit, context, data_entitlement as de, query_v0  # noqa: E402
from app import admin_refusals                                                         # noqa: E402
from app.config import get_config                                                      # noqa: E402

OPAL, ASKER, CALLER = ("11111111-1111-1111-1111-111111111111", "33333333-3333-3333-3333-333333333333",
                       "66666666-6666-6666-6666-666666666666")
CALLING, SENDER, CHAT, KEY = "caller@opalinvest.com", "pat@gmail.com", "19:chat-rr1@unq.gbl.spaces", "json/test/rr1.json"


class Store:
    def __init__(self, recs):
        self.r = recs

    def get(self, key):
        return self.r.get((key.pk, key.sk))


def graph(token, method, path, params=None, **kw):
    if "/messages/" in path:
        return {"from": {"user": {"tenantId": OPAL, "id": ASKER, "displayName": "Pat Sender"}},
                "createdDateTime": (datetime.now(timezone.utc) - timedelta(seconds=20)).isoformat(),
                "body": {"content": "q"}}
    if path.endswith("/members"):
        return {"value": [{"userId": CALLER, "tenantId": OPAL, "email": CALLING},
                          {"userId": ASKER, "tenantId": OPAL, "email": SENDER}]}
    return {"chatType": "oneOnOne"}


context.authorized_tenants = lambda: frozenset({OPAL})
get_config().AUDIT_PATH = audit_path
query_v0._catalog = lambda: {"rows_by_key": {KEY: {"key": KEY, "verdict_class": "serve", "allowlist": "ALLOWLISTED",
                                                    "firm": "", "_channel": "cha"}}}
query_v0._fetch_capped = lambda key: (b'[{"a": 1}]', 10)
pk, gk = de.profile_key(OPAL, ASKER), de.grant_key(OPAL, ASKER, 1)
scope = {"masters": list(de.MASTERS[:1]), "datasets": ["dim_position"], "accounts": {de.MASTERS[0]: ["ACC1"]},
         "dates": {"mode": "rolling_complete_window"}, "columns": {"dim_position": ["col1"]},
         "operations": ["query"], "portal_channels": ["cha"]}
store = Store({(pk.pk, pk.sk): {"tid": OPAL, "oid": ASKER, "profile_kind": "restricted", "status": "active",
                                "revision": 1, "grant_revision": 1},
               (gk.pk, gk.sk): {"tid": OPAL, "oid": ASKER, "revision": 1, "status": "active", "scope": scope}})
asc.clear_reply_bindings()
context.set_current_principal(context.make_principal(OPAL, CALLER, CALLING), "client-1")
out = asc.handle_asker_query(CHAT, "msg-1", KEY, None, token="tok", calling_email=CALLING,
                             graph_call=graph, store=store, audit_log=audit.log_call)
rows = []
if os.path.exists(audit_path):
    rows = [json.loads(ln) for ln in open(audit_path, encoding="utf-8").read().splitlines() if ln.strip()]
ref = [r for r in rows if r.get("tool") == "asker_sender_refusal"]
if not ref:
    sys.exit("refusal not written (outcome code=%s)" % out.get("code"))
listed = admin_refusals.list_refusals()
if not listed:
    sys.exit("refusal written but list_refusals returned no rows")
print("SEAM user=%s sender_email=%s listed_sender_email=%s" % (
    ref[0].get("user"), ref[0].get("args", {}).get("sender_email"), listed[0].get("sender_email")))
