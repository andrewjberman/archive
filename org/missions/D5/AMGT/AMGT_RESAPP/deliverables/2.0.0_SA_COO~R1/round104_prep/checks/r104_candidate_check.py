"""AMGT_RESAPP round-104 PREP -- `AMGT-bk-1`: the overlay prints sub-phase lines for feed and peers, and its top band reuses the feed's rows; no served byte moves.

  PYTHONPATH=<repo root> python r104_candidate_check.py [--names K1,K2,...]

Runs the CHECKOUT's own handler in-process (live pool, GET only) and, for each name, the LIVE function (Lambda invoke, GET) for the same two routes:
    S1 the overlay prints the thirteen AMGT_SUBPHASE lines, each once (feed.imports, feed.snapshot, feed.items, feed.names; peers.read, peers.foreign, peers.subject_name, peers.subject_cap,
       peers.member_names, peers.reason_classes, peers.listed_identity, peers.numeric_tickers, peers.price_currency): the base prints none.
    S2 the sub-phases of feed sum within 10 percent or 25 ms of the AMGT_PHASE feed line, and the peers sub-phases within the peers line (same bound): nothing hides between them.
    E1 /overlay and /peers bodies equal the live function's for every name (request clocks `generated_at`/`read_at`/`served_at` blanked on both sides).
    E2 one LIST of the article_security_mention prefix per overlay request (the base reads two: the feed's and the top band's).
    E3 control: the top band handed ANOTHER subject's rows serves a different body (the equality arm can see the fault it guards).
Verdict: `R104 CANDIDATE: YES|NO (<n> of <m> arms)`; exit 0|1. At the base blob 84002d3fd559 S1 and E2 read NO.
"""
import contextlib
import io
import json
import re
import sys

import boto3
import botocore.client

sys.path.insert(0, ".")
from lib.research.api import scoped_amgt as m  # noqa: E402

NAMES = ["ASML_NA_Equity", "VLO_US_Equity", "KOFUBL_MM_Equity", "1299_HK_Equity", "BA_US_Equity", "SAN_FP_Equity"]
SUB = ["feed.imports", "feed.snapshot", "feed.items", "feed.names", "peers.read", "peers.foreign", "peers.subject_name", "peers.subject_cap", "peers.member_names",
       "peers.reason_classes", "peers.listed_identity", "peers.numeric_tickers", "peers.price_currency"]
_LAM = boto3.client("lambda", region_name="us-east-1")
CLOCKS = re.compile(r'"(generated_at|read_at|served_at)": "[^"]*"')


def event(key, route):
    return {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, route), "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key, route):
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event(key, route)).encode())["Payload"].read())
    return r.get("statusCode"), CLOCKS.sub(r'"\1": "X"', r.get("body") or "")


def local(key, route):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = m.handler(event(key, route))
    return r.get("statusCode"), CLOCKS.sub(r'"\1": "X"', r.get("body") or ""), buf.getvalue()


def list_count(call):
    """(result, number of ListObjectsV2 calls whose Prefix names article_security_mention) while `call` runs."""
    real = botocore.client.BaseClient._make_api_call
    seen = []

    def spy(self, op, params):
        if op == "ListObjectsV2" and "article_security_mention" in str(params.get("Prefix", "")):
            seen.append(params.get("Prefix"))
        return real(self, op, params)

    botocore.client.BaseClient._make_api_call = spy
    try:
        return call(), len(seen)
    finally:
        botocore.client.BaseClient._make_api_call = real


def parse(out):
    sub = {}
    names = []
    for mm in re.finditer(r"AMGT_SUBPHASE route=overlay phase=(\S+) ms=(\d+)", out):
        names.append(mm.group(1))
        sub[mm.group(1)] = int(mm.group(2))
    ph = {mm.group(1): int(mm.group(2)) for mm in re.finditer(r"AMGT_PHASE route=overlay phase=(\S+) ms=(\d+)", out)}
    return names, sub, ph


def within(part, whole):
    return abs(part - whole) <= max(25, 0.10 * whole)


def main():
    names = NAMES
    if "--names" in sys.argv:
        names = sys.argv[sys.argv.index("--names") + 1].split(",")
    s1 = s2 = e1 = e2 = True
    rows = []
    for key in names:
        (st, body, out), lists = list_count(lambda k=key: local(k, "overlay"))
        pst, pbody, _ = local(key, "peers")
        lst, lbody = live(key, "overlay")
        lpst, lpbody = live(key, "peers")
        got, sub, ph = parse(out)
        ok1 = sorted(got) == sorted(SUB)
        feed_sum = sum(sub.get(n, 0) for n in SUB if n.startswith("feed."))
        peers_sum = sum(sub.get(n, 0) for n in SUB if n.startswith("peers."))
        ok2 = ok1 and within(feed_sum, ph.get("feed", 0)) and within(peers_sum, ph.get("peers", 0))
        ok_e1 = (st == lst and body == lbody) and (pst == lpst and pbody == lpbody)
        ok_e2 = lists == 1
        s1, s2, e1, e2 = s1 and ok1, s2 and ok2, e1 and ok_e1, e2 and ok_e2
        rows.append((key, ok1, ok2, ok_e1, lists, feed_sum, ph.get("feed"), peers_sum, ph.get("peers")))
        print("%-18s S1 %s S2 %s E1 %s lists=%d | feed subs %s of %s ms, peers subs %s of %s ms" % (key, ok1, ok2, ok_e1, lists, feed_sum, ph.get("feed"), peers_sum, ph.get("peers")))
    # E3: the top band given another subject's rows serves a different body (control for E1)
    a, b = names[0], names[-1]
    real = m._overlay_top_band
    _, base_body, _ = local(a, "overlay")
    other = {}

    def foreign_rows(security_key, description, as_of_date, rows=None):
        if not other:
            other["rows"] = [r for r in m._timeline_snapshot_rows("article_security_mention", columns=m._OVERLAY_NEWS_COLUMNS, security_key=b) if r.get("security_key") == b]
        return real(security_key, description, as_of_date, rows=other["rows"])

    m._overlay_top_band = foreign_rows
    try:
        _, mutated, _ = local(a, "overlay")
    finally:
        m._overlay_top_band = real
    e3 = mutated != base_body
    print("E3 control: the top band handed %s's rows serves a different body for %s: %s" % (b, a, e3))
    arms = [("S1 thirteen sub-phase lines once each", s1), ("S2 sub-phases sum to their phase", s2), ("E1 overlay and peers bodies equal the live function's", e1),
            ("E2 one LIST of the mention table per overlay", e2), ("E3 the equality arm sees a wrong-subject top band", e3)]
    for name, ok in arms:
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in arms if ok)
    print("R104 CANDIDATE: %s (%d of %d arms)" % ("YES" if n == len(arms) else "NO", n, len(arms)))
    return 0 if n == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
