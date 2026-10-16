"""IRPT_ANLREQ TO-RUN-FWD1 window 3, STEP 0, the door probe (0.7.0_AE_CloudOps~AQ2). Addendum 3 section 3 as amended (amendment 2).

  python probe_run3.py --selftest
  python probe_run3.py --live --go --out <new folder outside the repository>

ONE synthetic internal viewer irpt-r3p-iv-<YYYYMMDD>@opal.invalid (a users row written with attribute_not_exists, ONE RS256 token held in this
process only, exp at most 20 minutes, never written, printed or logged). For each candidate in the fixed order ALPPL, APPL, BREIT, SREIT, ZQXWVK:
post a synthetic CSV (header `Ticker,Dollars,Acct Market Value`; rows `SPY,100,26000000` and `<candidate>,50,5000000`) to the UPLOAD ROUTE ONLY;
if and only if the first answer is RESOLVING, wait at least 15 s and post the SAME upload (same upload token and file) ONCE more and keep that
answer; at most two posts per candidate, ten in all; posts at least 16 s apart. Never a correction, never the analysis route. Kept per
candidate: HTTP status, the state or finding code, whether a suggestion is present (and the suggested symbol, a public ticker), the finding's
actions list, the body sha256. The intake store (bucket opal-data-irpt, prefix irpt/49financial/) is listed BEFORE and AFTER (versions, delete
markers, counts, every new object by key and VersionId; nothing is deleted). The row is removed AFTER the token's exp (bounded 5-minute ABSENT
read by the email GSI and a ConsistentRead) in a finally.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "irpt_anlreq_r28"))
import sitting_r28 as base  # noqa: E402

CANDIDATES = ("ALPPL", "APPL", "BREIT", "SREIT", "ZQXWVK")
UPLOAD = "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial"
BUCKET, PREFIX = "opal-data-irpt", "irpt/49financial/"
LIFE = 1020
GAP = 16
WANT = {"irpt-status": "+TcZDWmwE7uv3sUwos2+jn1lbKyQikK+13nNBzD6q4A=", "irpt-ycharts-generate": "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE="}


def sha(raw):
    return hashlib.sha256(raw if isinstance(raw, bytes) else raw.encode("utf-8")).hexdigest()


def csv_for(cand):
    return ("Ticker,Dollars,Acct Market Value\nSPY,100,26000000\n%s,50,5000000\n" % cand).encode("ascii")


def describe(status, body, cand):
    """(label, qualifies, suggestion_symbol_or_None, actions) from one answer. No body text is kept."""
    if not isinstance(body, dict):
        return "UNPARSED", False, None, []
    data = body.get("data") if body.get("ok") is not False else None
    if not isinstance(data, dict):
        return "ERROR:%s" % (((body.get("status") or {}).get("public_reason_code")) or "NO_CODE"), False, None, []
    state = str(data.get("state") or "NO_STATE")
    findings = [f for f in (data.get("findings") or []) if isinstance(f, dict)]
    mine = [f for f in findings if str(f.get("value") or "").upper() == cand]
    own = [f for f in mine if f.get("code") == "TICKER_NOT_FOUND"]
    codes = sorted({str(f.get("code")) for f in (mine or findings)})
    label = state + (":" + ",".join(codes) if codes and state != "NORMALIZED" else "")
    if state == "NEEDS_CORRECTION" and own:
        sug = own[0].get("suggestion")
        sym = str(sug.get("symbol")).upper() if isinstance(sug, dict) and sug.get("symbol") else None
        return label, True, sym, [str(a) for a in (own[0].get("actions") or [])]
    acts = [str(a) for a in ((mine[0].get("actions") if mine else None) or [])]
    return label, False, None, acts


def select(results):
    """U1 Yes, U2 No, U3 Replace by the signed rule; a row with no qualifying candidate is None (UNEXERCISED)."""
    q = [(c, r) for c, r in results if r["qualifies"]]
    sug = [c for c, r in q if r["suggestion"]]
    u1 = sug[0] if sug else None
    u2 = sug[1] if len(sug) > 1 else None
    rest = [(c, r) for c, r in q if c not in (u1, u2)]
    nosug = [c for c, r in rest if not r["suggestion"]]
    u3 = nosug[0] if nosug else (rest[0][0] if rest else None)
    return {"U1": u1, "U2": u2, "U3": u3}


def gate(results):
    """The CTO's SET 2 STOP conditions (msgs 9337 and 9380): ZQXWVK must read NEEDS_CORRECTION:TICKER_NOT_FOUND with no suggestion; all five
    reading TICKER_CHECK_FAILED stops. Returns (ok, reason)."""
    by = {c: r for c, r in results}
    z = by.get("ZQXWVK")
    if not z or z["label"] != "NEEDS_CORRECTION:TICKER_NOT_FOUND" or z["suggestion"]:
        return False, "ZQXWVK did not read NOT_FOUND without a suggestion: %s" % (z["label"] if z else "NOT PROBED")
    if results and all(r["label"].endswith("TICKER_CHECK_FAILED") for _, r in results):
        return False, "all five candidates read TICKER_CHECK_FAILED"
    return True, "ZQXWVK reads NOT_FOUND"


def selftest():
    ok = {"ok": True, "data": {"state": "NEEDS_CORRECTION", "findings": [{"code": "TICKER_NOT_FOUND", "value": "zzz", "actions": ["ACCEPT_SUGGESTION", "REPLACE_TICKER"], "suggestion": {"symbol": "ZZY"}}]}}
    assert describe(200, ok, "ZZZ") == ("NEEDS_CORRECTION:TICKER_NOT_FOUND", True, "ZZY", ["ACCEPT_SUGGESTION", "REPLACE_TICKER"])
    nos = {"ok": True, "data": {"state": "NEEDS_CORRECTION", "findings": [{"code": "TICKER_NOT_FOUND", "value": "QQQ", "actions": ["REPLACE_TICKER"]}]}}
    assert describe(200, nos, "QQQ") == ("NEEDS_CORRECTION:TICKER_NOT_FOUND", True, None, ["REPLACE_TICKER"])
    other = {"ok": True, "data": {"state": "NEEDS_CORRECTION", "findings": [{"code": "TICKER_DATA_NOT_ENTITLED", "value": "BREIT", "actions": ["REVIEW"]}]}}
    assert describe(200, other, "BREIT") == ("NEEDS_CORRECTION:TICKER_DATA_NOT_ENTITLED", False, None, ["REVIEW"])
    assert describe(200, {"ok": True, "data": {"state": "RESOLVING"}}, "X")[:2] == ("RESOLVING", False)
    assert describe(200, {"ok": True, "data": {"state": "NORMALIZED"}}, "X")[:2] == ("NORMALIZED", False)
    assert describe(403, {"ok": False, "status": {"public_reason_code": "NOT_AUTHORIZED"}}, "X")[0] == "ERROR:NOT_AUTHORIZED"
    assert describe(500, None, "X")[0] == "UNPARSED"

    def r(q, s):
        return {"qualifies": q, "suggestion": s}
    res = [("A", r(True, "A1")), ("B", r(False, None)), ("C", r(True, "C1")), ("D", r(True, None)), ("E", r(True, "E1"))]
    assert select(res) == {"U1": "A", "U2": "C", "U3": "D"}
    assert select([("A", r(True, None)), ("B", r(True, None))]) == {"U1": None, "U2": None, "U3": "A"}
    assert select([("A", r(False, None))]) == {"U1": None, "U2": None, "U3": None}
    assert select([("A", r(True, "A1")), ("B", r(True, "B1")), ("C", r(True, "C1"))]) == {"U1": "A", "U2": "B", "U3": "C"}
    assert csv_for("ALPPL") == b"Ticker,Dollars,Acct Market Value\nSPY,100,26000000\nALPPL,50,5000000\n"
    nf = {"label": "NEEDS_CORRECTION:TICKER_NOT_FOUND", "suggestion": None}
    cf = {"label": "NEEDS_CORRECTION:TICKER_CHECK_FAILED", "suggestion": None}
    assert gate([("ALPPL", cf), ("ZQXWVK", nf)]) == (True, "ZQXWVK reads NOT_FOUND")
    assert gate([("ALPPL", nf), ("ZQXWVK", cf)])[0] is False
    assert gate([("ALPPL", nf), ("ZQXWVK", dict(nf, suggestion="X"))])[0] is False
    assert gate([("ALPPL", nf)])[0] is False
    print("SELFTEST-OK probe helpers: describe (6 shapes), select (4 cases incl. UNEXERCISED and the no-suggestion preference), csv_for, gate (4 cases)")
    return 0


def list_store(s3):
    items, markers = {}, 0
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for v in pg.get("Versions", []) or []:
            items[(v["Key"], v["VersionId"])] = v["Size"]
        markers += len(pg.get("DeleteMarkers", []) or [])
    return items, markers


def live(args):
    import boto3
    import jwt as pyjwt
    date = args.date
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = args.tag
    order = [c.strip().upper() for c in args.order.split(",")] if args.order else list(CANDIDATES)
    addr = "irpt-%s-iv-%s@opal.invalid" % (tag, date)
    ddb = boto3.client("dynamodb", region_name=base.REGION)
    lam = boto3.client("lambda", region_name=base.REGION)
    s3 = boto3.client("s3", region_name=base.REGION)
    key = {"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}
    lines, results = [], []
    state = {"token": None, "last": 0.0, "posts": 0}

    def say(msg):
        line = "%s %s" % (base.iso(), msg)
        print(line, flush=True)
        lines.append(line)

    def cread():
        return ddb.get_item(TableName=base.USERS, Key=key, ConsistentRead=True).get("Item")

    def gsi():
        return ddb.query(TableName=base.USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]

    def post(cand, tok, gap=GAP):
        wait = gap - (time.time() - state["last"])
        if wait > 0:
            time.sleep(wait)
        state["posts"] += 1
        body = {"upload_token": tok, "filename": "%s-%s.csv" % (tag, cand.lower()), "file_base64": base64.b64encode(csv_for(cand)).decode(), "file_type": "csv"}
        req = urllib.request.Request(base.BASE + UPLOAD, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Authorization", "Bearer " + state["token"])
        req.add_header("x-contract-version", "v1")
        req.add_header("Content-Type", "application/json")
        start = state["last"] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                st, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            st, raw = e.code, e.read().decode("utf-8", "replace")
        return st, base.parsed(raw), raw, start

    written, exp, stop = False, None, None
    before = after = None
    try:
        for fn, want in WANT.items():
            got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            say("%s CodeSha256 %s" % (fn, "EQUAL" if got == want else "DIFFERENT"))
            if got != want:
                raise RuntimeError("a Lambda digest differs from the pin")
        if cread() is not None or gsi() != 0:
            raise RuntimeError("the probe viewer address is not ABSENT")
        before = list_store(s3)
        say("intake BEFORE bucket %s prefix %s: %d versions, %d delete markers" % (BUCKET, PREFIX, len(before[0]), before[1]))
        now = base.iso()
        item = {"PK": key["PK"], "SK": key["SK"], "email": {"S": addr}, "firmId": {"S": "opal-capital"}, "status": {"S": "active"},
                "name": {"S": "IRPT_ANLREQ R3 probe synthetic internal viewer (%s)" % tag}, "role": {"S": "user"}, "tier": {"S": "internal"},
                "userType": {"S": "test-filer"}, "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
        ddb.put_item(TableName=base.USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
        written = True
        back = cread()
        if back is None or back["status"]["S"] != "active" or "allowedFirmIds" in back:
            raise RuntimeError("the viewer row is not PRESENT as designed")
        say("probe viewer row written (attribute_not_exists) and read back PRESENT")
        pem = boto3.client("secretsmanager", region_name=base.REGION).get_secret_value(SecretId=base.KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        iat = int(time.time())
        claims = {"sub": addr, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal", "role": "user",
                  "userType": "test-filer", "name": "IRPT_ANLREQ R3 probe synthetic internal viewer", "iat": iat, "exp": iat + args.life}
        state["token"] = pyjwt.encode(claims, pem, algorithm="RS256")
        exp = claims["exp"]
        del pem
        say("token minted (held in memory only) iat=%s exp=%s" % (base.iso(iat), base.iso(exp)))
        halted = None
        for cand in order:
            if halted:
                say("PROBE %s NOT PROBED: %s" % (cand, halted))
                results.append((cand, dict(status=None, label="NOT_PROBED", qualifies=False, suggestion=None, actions=[], sha=None, posts=0)))
                continue
            if time.time() > exp - 150:
                say("PROBE %s NOT PROBED: the token window is nearly spent" % cand)
                results.append((cand, dict(status=None, label="NOT_PROBED", qualifies=False, suggestion=None, actions=[], sha=None, posts=0)))
                continue
            tok = "irpt-%s-%s-%s" % (tag, cand.lower(), date)
            st, b, raw, _ = post(cand, tok)
            state.setdefault("first_post", base.iso())
            label, q, sug, acts = describe(st, b, cand)
            n = 1
            if label == "RESOLVING":
                say("PROBE %s first answer RESOLVING; the SAME upload is posted once more (amendment 2)" % cand)
                st, b, raw, _ = post(cand, tok, gap=args.repost_wait)
                label, q, sug, acts = describe(st, b, cand)
                n = 2
            say("PROBE %s status %s %s suggestion=%s%s actions=%s body_sha256 %s posts %d" % (cand, st, label, "yes" if sug else "no", (" " + sug) if sug else "", ",".join(acts), sha(raw), n))
            results.append((cand, dict(status=st, label=label, qualifies=q, suggestion=sug, actions=acts, sha=sha(raw), posts=n)))
            state["last_answer"] = base.iso()
            if args.zq_first and cand == "ZQXWVK" and (label != "NEEDS_CORRECTION:TICKER_NOT_FOUND" or sug):
                halted = "ZQXWVK did not read NOT_FOUND without a suggestion (%s): the SET ends and the window STOPS" % label
                say("STOP-GATE " + halted)
        after = list_store(s3)
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; the row is still removed after exp
        stop = "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        state["token"] = None
        if written and exp:
            wait = exp + 5 - time.time()
            if wait > 0:
                say("waiting %ds for exp %s to pass before removal" % (int(wait), base.iso(exp)))
                time.sleep(wait)
        if written:
            try:
                ddb.delete_item(TableName=base.USERS, Key=key, ConditionExpression="attribute_exists(PK)")
                say("probe viewer row deleted (attribute_exists)")
            except Exception as e:  # noqa: BLE001
                say("DELETE of the probe viewer row failed: %s" % str(e)[:160])
        deadline = time.time() + 300
        g = c = False
        while time.time() < deadline:
            c, g = cread() is None, gsi() == 0
            say("removal read: GSI ABSENT=%s ConsistentRead ABSENT=%s" % (g, c))
            if g and c:
                break
            time.sleep(10)
        rem = ["F1 ABSENT GSI %s" % addr if g else "F1 PRESENT GSI %s" % addr, "F1 ABSENT CONSISTENT %s" % addr if c else "F1 PRESENT CONSISTENT %s" % addr]
        sel = select(results) if results else {"U1": None, "U2": None, "U3": None}
        new = sorted(set(after[0]) - set(before[0])) if before and after else None
        doc = {"order": order, "first_post_utc": state.get("first_post"), "last_answer_utc": state.get("last_answer"), "repost_wait_s": args.repost_wait,
               "results": [dict(candidate=c, **r) for c, r in results], "selection": sel, "removal": rem, "stop": stop,
               "intake_before": None if not before else {"versions": len(before[0]), "markers": before[1]},
               "intake_after": None if not after else {"versions": len(after[0]), "markers": after[1]},
               "new_objects": None if new is None else [{"key": k, "version_id": v, "size": after[0][(k, v)]} for k, v in new]}
        (out / "probe_results.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
        (out / "probe_trace.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        ok_, why_ = gate(results) if results else (False, "no results")
        say("GATE %s: %s" % ("OK" if ok_ else "STOP", why_))
        say("SELECTION U1=%s U2=%s U3=%s (None = UNEXERCISED); new intake objects: %s" % (sel["U1"], sel["U2"], sel["U3"], "unread" if new is None else len(new)))
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default="")
    ap.add_argument("--tag", default="r3p", help="viewer tag: r3p for SET 1, r3q for SET 2")
    ap.add_argument("--order", default="", help="comma list of candidates in order (default ALPPL,APPL,BREIT,SREIT,ZQXWVK)")
    ap.add_argument("--repost-wait", type=int, default=GAP, help="seconds from a candidate's first post to its one re-post (SET 3: 90)")
    ap.add_argument("--zq-first", action="store_true", help="end the SET at ZQXWVK when it does not read NOT_FOUND without a suggestion")
    ap.add_argument("--life", type=int, default=LIFE, help="token life in seconds (at most 1200)")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.life > 1200:
        ap.error("--life is at most 1200 seconds (20 minutes)")
    if a.live and a.go and a.out:
        return live(a)
    ap.error("choose --selftest, or --live --go --out <folder>")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
