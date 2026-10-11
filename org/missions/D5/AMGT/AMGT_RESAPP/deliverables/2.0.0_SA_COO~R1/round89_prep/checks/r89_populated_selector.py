"""AMGT_RESAPP round 89 item 1 (CTO~DELL1 round-88 analysis) -- condition 4 DRIVEN against a POPULATED watchlist. ISSUER ACT (`AMGT-nn-1`).

  python r89_populated_selector.py            (repo root, PYTHONPATH=<repo root>)

Round 88's live read was byte-equal on 6 of 6 firms but every list it compared was the 2-byte empty list: a filter that drops
everything also returns `[]`, so on empty lists the equality cannot tell "ignores the selector" from "drops everything". This
drives the DEPLOYED reader (the member read out of the live function's own code package, its sha256 printed) over a COPY of the
watchlist store held in memory -- two firms' lists planted NON-EMPTY -- through the route's own `handler`. NOTHING is written to
the served store, no network call is made for the lists, and no Bloomberg call is made.
    S1 per firm F (other firm O): the read with NO selector returns F's planted tickers, and only F's (the lists are populated).
    S2 per firm F: an off-list selector (O) on each channel this route could read -- query `selected_tenant`, query `selectedTenant`,
       header `x-selected-tenant` -- returns bytes EQUAL to the no-selector read.
    S3 per firm F: no read carries any of O's planted tickers.
    S4 negative control: the same comparison run over a reader WRAPPED to drop every list when a selector is present fails S2
       (a filter that drops everything is distinguishable on populated lists; it was not on empty ones).
Verdict: R89 POPULATED SELECTOR: YES|NO (exit 0|1).
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import urllib.request
import zipfile

FN = "opal-amgt-scoped-api"
MEMBER = "lib/research/api/scoped_amgt.py"
PREFIX = "/api/scoped/amgt"
STORE = {"firm_a": ["AAPL", "MSFT", "NVDA"], "firm_b": ["TSLA", "AMZN"]}
HEADERS_FOR = {  # (kind, name) -> how the selector rides
    "query selected_tenant": ("query", "selected_tenant"),
    "query selectedTenant": ("query", "selectedTenant"),
    "header x-selected-tenant": ("header", "x-selected-tenant"),
}


def say(ok, label):
    print("%s %s" % ("PASS" if ok else "FAIL", label))
    return ok


def load_deployed_reader():
    import boto3

    f = boto3.client("lambda", region_name="us-east-1").get_function(FunctionName=FN)
    cfg = f["Configuration"]
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f["Code"]["Location"], timeout=120).read()))
    name = [n for n in z.namelist() if n.replace("\\", "/").endswith(MEMBER)][0]
    body = z.read(name)
    print("   deployed function %s CodeSha256 %s LastModified %s" % (FN, cfg["CodeSha256"], cfg["LastModified"]))
    print("   reader = %s read from that package: %d bytes, sha256 %s" % (MEMBER, len(body), hashlib.sha256(body).hexdigest()[:16]))
    tmp = tempfile.mkdtemp(prefix="r89_reader_")
    path = os.path.join(tmp, "scoped_amgt_deployed.py")
    with open(path, "wb") as fh:
        fh.write(body)
    spec = importlib.util.spec_from_file_location("scoped_amgt_deployed", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def event(firm, selector=None):
    ev = {
        "rawPath": "%s/watchlist" % PREFIX,
        "requestContext": {"http": {"method": "GET"}},
        "headers": {"x-firm-id": firm},
        "queryStringParameters": None,
    }
    if selector:
        kind, name = selector[0]
        if kind == "query":
            ev["queryStringParameters"] = {name: selector[1]}
        else:
            ev["headers"][name] = selector[1]
    return ev


def run(handler, firm, selector=None):
    r = handler(event(firm, selector))
    return r.get("statusCode"), r.get("body") or ""


def tickers(body):
    try:
        return [row.get("ticker") for row in json.loads(body)]
    except Exception:  # noqa: BLE001 -- a non-list body is its own finding
        return None


def drive(handler, label):
    ok_all = True
    detail = []
    for firm, other in (("firm_a", "firm_b"), ("firm_b", "firm_a")):
        c0, b0 = run(handler, firm)
        t0 = tickers(b0)
        s1 = c0 == 200 and t0 == STORE[firm]
        detail.append("   %s: no selector -> %s %s (planted %s)" % (firm, c0, t0, STORE[firm]))
        equal = True
        leak = False
        for chan, kind_name in HEADERS_FOR.items():
            c1, b1 = run(handler, firm, (kind_name, other))
            same = (c1, b1) == (c0, b0)
            equal = equal and same
            ts = tickers(b1) or []
            leak = leak or any(t in ts for t in STORE[other])
            detail.append("     off-list %-26s -> %s %s byte-equal=%s" % (chan, c1, ts, same))
        ok_all = ok_all and s1 and equal and not leak
        detail.append("     S1 populated=%s S2 byte-equal on every channel=%s S3 no leak of %s=%s" % (s1, equal, other, not leak))
    print("   [%s]" % label)
    for line in detail:
        print(line)
    return ok_all


def main():
    reader = load_deployed_reader()
    import lib.research.watchlist.store as store

    real_list = store.list_starred
    store.list_starred = lambda firm_id: list(STORE.get(firm_id, []))
    try:
        positive = drive(reader.handler, "the deployed reader")

        original = reader.handler

        def drops_everything(ev):
            h = {str(k).lower(): v for k, v in (ev.get("headers") or {}).items()}
            q = ev.get("queryStringParameters") or {}
            if q.get("selected_tenant") or q.get("selectedTenant") or h.get("x-selected-tenant"):
                return {"statusCode": 200, "headers": {}, "body": "[]"}
            return original(ev)

        control = drive(drops_everything, "NEGATIVE CONTROL: a reader that drops every list when a selector is present")
    finally:
        store.list_starred = real_list
    s123 = say(positive, "S1-S3 the deployed reader: populated lists, byte-equal on every selector channel, no cross-firm entry")
    s4 = say(not control, "S4 the negative control FAILS the same comparison (the instrument discriminates on populated lists)")
    ok = s123 and s4
    print("R89 POPULATED SELECTOR: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
