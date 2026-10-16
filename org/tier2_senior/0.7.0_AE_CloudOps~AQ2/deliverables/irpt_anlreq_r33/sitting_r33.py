"""IRPT_ANLREQ TO-EXERCISE-R33 executor (0.7.0_AE_CloudOps~AQ2): the release-33 sitting.

Three synthetic partner advisors (A and B in 49financial, C in cottonwood) with their partner rows and one synthetic internal
viewer (Addendum 1b shape), ONE RS256 token each held in this process only, never written, printed or logged. Arms: D1 A uploads,
D2 A analyses that input, D3 B analyses A's input, D4 C analyses A's input by its id; P2, P1 and P1M the internal viewer's three
uploads (no price date, a price date, a malformed one) counted by the exact log string in printed windows. Kept: status, finding
code or state, count and sha256 of each body; never a price date value, a body or a log line. No object is deleted. Every minted
row is removed after exp and read ABSENT.

Reuses ../irpt_anlreq_r28/sitting_r28.py (constants) and the shape of ../irpt_anlreq_r29/sitting_r29.py; only the arms change.

  --selftest      offline checks of the helpers (no AWS call)
  --live --go     the sitting
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

LEGS = (("irpt-status", "OOez8YSmE22btOqx28/fJdK9sxGNDGAumU5pMJ++6Ss="),
        ("irpt-ycharts-generate", "kxOEgpbspky10PYWQ28y0+7V2UXG28whJ2riMa4CkTE="))
BUCKET = "opal-data-irpt"
TENANTS = ("49financial", "cottonwood")
UPLOAD = "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=%s"
ANALYSIS = "/api/scoped/investor-reporting/analysis?selected_tenant=%s"
ANSWER_STATES = ("NEEDS_CORRECTION", "NORMALIZED")
LOG_GROUP = "/aws/lambda/irpt-ycharts-generate"
LOG_STRING = "IRPT_UPLOAD price_date_ignored=1"
LOG_BEFORE_S, LOG_AFTER_S = 5, 90      # the window of an arm: 5 s before its first request to 90 s after its last
P_GAP_S = 100                          # P arms start at least this long after the previous request, so their windows cannot overlap
IV_LIFE = 780                          # seconds; the internal viewer's token is minted just before P2 (the order caps it at 20 minutes)
# ONE market-value file for every upload (round numbers, one account, no client data). Amounts differ from every earlier sitting's file.
FILE = b"Ticker,Dollars,Acct Market Value\nSPY,100,28000000\nAGG,200,34000000\n"
TITLE = "SYNTHETIC release-33 sitting, do not action"
# The order names the two price date inputs; they are built from parts so no record or trace of this sitting carries a value.
PD_GOOD = "-".join(("2026", "01", "02"))
PD_BAD = "not" + "-a-" + "date"


def code_of(b):
    if not isinstance(b, dict):
        return "UNPARSED"
    if b.get("ok") is False or "data" not in b:
        return str(((b.get("status") or {}).get("public_reason_code")) or "NO_CODE")
    d = b.get("data")
    if isinstance(d, dict) and d.get("state"):
        return str(d.get("state"))
    return "ANSWER" if isinstance(d, dict) else "NO_DATA"


def is_answer(b):
    d = b.get("data") if isinstance(b, dict) and b.get("ok") is not False else None
    return isinstance(d, dict) and d.get("state") in ANSWER_STATES


def admitted(st, b):
    return isinstance(st, int) and st < 300 and isinstance(b, dict) and b.get("ok") is not False and isinstance(b.get("data"), dict)


def upload_body(token, filename, content, price_date=None):
    body = {"upload_token": token, "filename": filename, "file_base64": base64.b64encode(content).decode(), "file_type": "csv"}
    if price_date is not None:
        body["price_date"] = price_date
    return body


def analysis_body(req, input_id):
    return {"request_id": req, "client_id": None, "account_ids": [], "snapshot_id": None, "variant": "overview",
            "comparison_keys": [], "report_title": TITLE, "prepared_for": "SYNTHETIC", "input_id": input_id}


def sha(s):
    return hashlib.sha256(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def window_of(first_start, last_start):
    """The log window of an arm in epoch seconds: 5 s before its first request to 90 s after its last."""
    return first_start - LOG_BEFORE_S, last_start + LOG_AFTER_S


def windows_disjoint(wins):
    ordered = sorted(wins)
    return all(a[1] < b[0] for a, b in zip(ordered, ordered[1:]))


def count_window(logs, start_s, end_s):
    """(events scanned, events containing the exact string) in [start_s, end_s]; no event text is kept."""
    scanned = hits = 0
    pages = logs.get_paginator("filter_log_events").paginate(logGroupName=LOG_GROUP, startTime=int(start_s * 1000), endTime=int(end_s * 1000))
    for pg in pages:
        for e in pg.get("events", []) or []:
            scanned += 1
            if LOG_STRING in (e.get("message") or ""):
                hits += 1
    return scanned, hits


def list_store(s3):
    """(key, version_id) of every version and the delete-marker count under each tenant prefix, per tenant."""
    out = {}
    for t in TENANTS:
        items, markers = set(), 0
        for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix="irpt/%s/" % t):
            for v in pg.get("Versions", []) or []:
                items.add((v["Key"], v["VersionId"]))
            markers += len(pg.get("DeleteMarkers", []) or [])
        out[t] = (items, markers)
    return out


def selftest():
    assert code_of({"ok": False, "status": {"public_reason_code": "NOT_AUTHORIZED"}}) == "NOT_AUTHORIZED"
    assert code_of({"ok": True, "data": {"state": "NORMALIZED"}}) == "NORMALIZED"
    assert code_of("x") == "UNPARSED"
    assert admitted(200, {"ok": True, "data": {"a": 1}}) and not admitted(403, {"ok": False})
    assert upload_body("t", "f.csv", b"x")["file_type"] == "csv" and "price_date" not in upload_body("t", "f.csv", b"x")
    assert upload_body("t", "f.csv", b"x", PD_GOOD)["price_date"] == PD_GOOD and PD_GOOD != PD_BAD

    class FakeLogs:
        def __init__(self, events):
            self.events = events

        def get_paginator(self, name):
            assert name == "filter_log_events"
            outer = self

            class P:
                def paginate(self, **kw):
                    lo, hi = kw["startTime"], kw["endTime"]
                    yield {"events": [e for e in outer.events[:2] if lo <= e["timestamp"] <= hi]}
                    yield {"events": [e for e in outer.events[2:] if lo <= e["timestamp"] <= hi]}
            return P()
    ev = [{"timestamp": 1000, "message": "START"}, {"timestamp": 2000, "message": LOG_STRING}, {"timestamp": 3000, "message": "x " + LOG_STRING + "\n"},
          {"timestamp": 4000, "message": "IRPT_UPLOAD price_date_ignored=0"}, {"timestamp": 9000, "message": LOG_STRING}]
    assert count_window(FakeLogs(ev), 0.5, 5) == (4, 2), count_window(FakeLogs(ev), 0.5, 5)
    assert count_window(FakeLogs(ev), 8, 10) == (1, 1)
    assert count_window(FakeLogs(ev), 20, 30) == (0, 0)
    w1, w2, w3 = window_of(100, 100), window_of(100 + P_GAP_S, 100 + P_GAP_S), window_of(100 + 2 * P_GAP_S, 100 + 2 * P_GAP_S)
    assert windows_disjoint([w1, w2, w3]) and w1 == (95, 190)
    assert not windows_disjoint([window_of(100, 100), window_of(150, 150)])
    print("SELFTEST-OK helpers: code_of, admitted, upload_body, count_window (4 cases), window_of and windows_disjoint (positive and negative)")
    return 0


def live(args):
    import boto3
    import botocore.exceptions
    import jwt as pyjwt

    date = args.date
    outdir = Path(args.out)
    ddb = boto3.client("dynamodb", region_name=base.REGION)
    s3 = boto3.client("s3", region_name=base.REGION)
    lam = boto3.client("lambda", region_name=base.REGION)
    logs = boto3.client("logs", region_name=base.REGION)
    ids = {
        "A": dict(addr="irpt-r33-a-%s@opal.invalid" % date, firm="49financial", label="advisor A", kind="advisor"),
        "B": dict(addr="irpt-r33-b-%s@opal.invalid" % date, firm="49financial", label="advisor B", kind="advisor"),
        "C": dict(addr="irpt-r33-c-%s@opal.invalid" % date, firm="cottonwood", label="advisor C", kind="advisor"),
        "IV": dict(addr="irpt-r33-iv-%s@opal.invalid" % date, firm="opal-capital", label="internal viewer", kind="internal"),
    }
    lines, detail, results, tokens = [], [], {}, {}
    written_users, written_partner, exps, objects_before = [], [], [], None
    inputs, wins, log_lines = {}, {}, []
    last = [0.0]

    def say(msg):
        line = "%s %s" % (base.iso(), msg)
        print(line, flush=True)
        lines.append(line)

    def ukey(k):
        return {"PK": {"S": "USER#" + ids[k]["addr"]}, "SK": {"S": "PROFILE"}}

    def pkey(k):
        return {"email": {"S": ids[k]["addr"]}}

    def ptable(k):
        return "opal-partner-" + ids[k]["firm"]

    def uread(k):
        return ddb.get_item(TableName=base.USERS, Key=ukey(k), ConsistentRead=True).get("Item")

    def pread(k):
        return ddb.get_item(TableName=ptable(k), Key=pkey(k), ConsistentRead=True).get("Item")

    def gsi(k):
        return ddb.query(TableName=base.USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": ids[k]["addr"]}}, Select="COUNT")["Count"]

    def call(arm, who, path, body, min_gap=None):
        wait = (min_gap or base.GAP) - (time.time() - last[0])
        if wait > 0:
            time.sleep(wait)
        say("sending %s as %s now (UTC)" % (arm, who))
        req = urllib.request.Request(base.BASE + path, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Authorization", "Bearer " + tokens[who])
        req.add_header("x-contract-version", "v1")
        req.add_header("Content-Type", "application/json")
        start = last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                st, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            st, raw = e.code, e.read().decode("utf-8", "replace")
        b = base.parsed(raw)
        say("request %s as %s start=%s status=%s code=%s body_sha256=%s" % (arm, who, base.iso(start), st, code_of(b), sha(raw)))
        return st, b, raw, start

    def upload(arm, who, firm, token, filename, price_date=None, loop=True, min_gap=None):
        """The arm's answer, the arm's first and last request start. A RESOLVING answer is re-posted only when loop is true."""
        first = None
        for _ in range(8 if loop else 1):
            st, b, raw, start = call(arm, who, UPLOAD % firm, upload_body(token, filename, FILE, price_date), min_gap if first is None else None)
            first = first if first is not None else start
            d = b.get("data") if isinstance(b, dict) else None
            if not (isinstance(d, dict) and d.get("state") == "RESOLVING"):
                break
        return st, b, raw, first, start

    def mint(k, life):
        iat = int(time.time())
        i = ids[k]
        if i["kind"] == "advisor":
            key = "irpt-r33-adv-%s-%s" % (k.lower(), date)
            claims = {"sub": i["addr"], "iss": "opal-portal-auth", "aud": "opal-portal-api", "name": "IRPT_ANLREQ R33 synthetic %s" % i["label"],
                      "role": "user", "tier": "advisor", "firmId": i["firm"], "advisorKey": key, "advisorName": "IRPT_ANLREQ R33 synthetic %s" % i["label"],
                      "advisorRole": "viewer", "advisorId": key, "firmRole": "user", "iat": iat, "exp": iat + life}
        else:
            claims = {"sub": i["addr"], "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
                      "role": "user", "userType": "test-filer", "name": "IRPT_ANLREQ R33 synthetic internal viewer",
                      "iat": iat, "exp": iat + life}
        tokens[k] = pyjwt.encode(claims, pem_holder[0], algorithm="RS256")
        exps.append(claims["exp"])
        say("token for %s minted (held in memory only) iat=%s exp=%s" % (k, base.iso(iat), base.iso(claims["exp"])))

    def fail_line(arm, st, b):
        return "%s FAIL %s %s" % (arm, st, code_of(b))

    pem_holder = [None]
    stop = None
    d_blocked = None
    log_ok = True
    try:
        for fn, want in LEGS:
            got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            say("%s CodeSha256 %s" % (fn, "EQUAL" if got == want else "DIFFERENT"))
            if got != want:
                raise RuntimeError("a function is not at its expected CodeSha256")
        try:
            logs.filter_log_events(logGroupName=LOG_GROUP, startTime=int(time.time() * 1000) - 60000, endTime=int(time.time() * 1000), limit=1)
            say("log read probe on the function's log group: allowed")
        except botocore.exceptions.ClientError as e:
            log_ok = False
            say("log read probe DENIED (%s): P2, P1 and P1M will read UNREAD log denied and will not be sent" % e.response.get("Error", {}).get("Code"))
        for k in ids:
            if uread(k) is not None or gsi(k) != 0:
                raise RuntimeError("address %s is not ABSENT by ConsistentRead and GSI" % k)
            if k != "IV" and pread(k) is not None:
                raise RuntimeError("partner row %s is not ABSENT" % k)
        say("pre-state: four users keys ABSENT by ConsistentRead, four addresses return 0 on the email index, three partner keys ABSENT")
        objects_before = list_store(s3)
        for t in TENANTS:
            say("intake store BEFORE %s: %d versions, %d delete markers" % (t, len(objects_before[t][0]), objects_before[t][1]))
        detail.append("BEFORE " + " ".join("%s=%d versions/%d markers" % (t, len(objects_before[t][0]), objects_before[t][1]) for t in TENANTS))

        now = base.iso()
        for k, i in ids.items():
            if i["kind"] == "advisor":
                item = {"PK": ukey(k)["PK"], "SK": ukey(k)["SK"], "email": {"S": i["addr"]}, "firmId": {"S": i["firm"]},
                        "status": {"S": "active"}, "name": {"S": "IRPT_ANLREQ R33 synthetic %s" % i["label"]},
                        "role": {"S": "user"}, "tier": {"S": "advisor"},
                        "allowedFirmIds": {"L": [{"S": i["firm"]}]},
                        "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
            else:
                item = {"PK": ukey(k)["PK"], "SK": ukey(k)["SK"], "email": {"S": i["addr"]}, "firmId": {"S": "opal-capital"},
                        "status": {"S": "active"}, "name": {"S": "IRPT_ANLREQ R33 synthetic internal viewer"},
                        "role": {"S": "user"}, "tier": {"S": "internal"}, "userType": {"S": "test-filer"},
                        "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
            ddb.put_item(TableName=base.USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
            written_users.append(k)
            back = uread(k)
            if back is None or back["status"]["S"] != "active":
                raise RuntimeError("users row %s not PRESENT active" % k)
            if i["kind"] == "advisor":
                if [m.get("S") for m in back["allowedFirmIds"]["L"]] != [i["firm"]]:
                    raise RuntimeError("allowedFirmIds of %s is not the explicit list of its firm" % k)
                prow = {"email": {"S": i["addr"]}, "advisorKey": {"S": "irpt-r33-adv-%s-%s" % (k.lower(), date)},
                        "advisorName": {"S": "IRPT_ANLREQ R33 synthetic %s" % i["label"]}, "advisorRole": {"S": "viewer"},
                        "firmRole": {"S": "user"}, "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"},
                        "updatedAt": {"S": now}}
                ddb.put_item(TableName=ptable(k), Item=prow, ConditionExpression="attribute_not_exists(email)")
                written_partner.append(k)
                pb = pread(k)
                if pb is None or pb["email"]["S"] != i["addr"]:
                    raise RuntimeError("partner row %s not PRESENT" % k)
            say("%s users row%s written (attribute_not_exists) and read back PRESENT (status active%s)" % (
                k, " and partner row" if i["kind"] == "advisor" else "",
                ", explicit allowedFirmIds list of its one firm" if i["kind"] == "advisor" else ", no allowedFirmIds"))

        pem = boto3.client("secretsmanager", region_name=base.REGION).get_secret_value(SecretId=base.KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        pem_holder[0] = pem
        del pem
        say("signing key read (value never printed or written)")
        for k in ("A", "B", "C"):
            mint(k, base.LIFE)

        # D1: A uploads the market-value file
        st, b, raw, _f, _l = upload("D1", "A", "49financial", "irpt-r33-d1-%s" % date, "r33-d1.csv")
        d = b.get("data") if isinstance(b, dict) else None
        if code_of(b) == "NOT_AUTHORIZED":
            results["D1"] = fail_line("D1", st, b)
            stop = "D1 answered NOT_AUTHORIZED: STOP, rows removed, no other identity"
        elif st == 200 and is_answer(b) and d.get("state") == "NORMALIZED" and isinstance(d.get("input_id"), str):
            results["D1"] = "D1 NORMALIZED"
            inputs["D1"] = d["input_id"]
        else:
            results["D1"] = fail_line("D1", st, b)
            d_blocked = "D1 did not answer NORMALIZED: the analysis arms D2 to D4 need its input (the price date arms are independent and still run)"
        detail.append("D1 status=%s code=%s" % (st, code_of(b)))

        if not stop:
            if not d_blocked:
                # D2: A analyses A's input
                st, b, raw, _s = call("D2", "A", ANALYSIS % "49financial", analysis_body("irpt-r33-d2-%s" % date, inputs["D1"]))
                results["D2"] = "D2 ADMITTED" if admitted(st, b) else fail_line("D2", st, b)
                detail.append("D2 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
                # D3: B analyses A's input (same firm)
                st, b, raw, _s = call("D3", "B", ANALYSIS % "49financial", analysis_body("irpt-r33-d3-%s" % date, inputs["D1"]))
                if admitted(st, b):
                    results["D3"] = "D3 FAIL %s ADMITTED" % st
                    say("BLOCKING: D3 was ADMITTED -- advisor B reached advisor A's input")
                else:
                    results["D3"] = "D3 REFUSED NOT_AUTHORIZED" if code_of(b) == "NOT_AUTHORIZED" else fail_line("D3", st, b)
                detail.append("D3 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
                # D4: C (cottonwood) analyses A's input by its id, selected firm cottonwood
                st, b, raw, _s = call("D4", "C", ANALYSIS % "cottonwood", analysis_body("irpt-r33-d4-%s" % date, inputs["D1"]))
                if admitted(st, b):
                    results["D4"] = "D4 FAIL %s ADMITTED" % st
                    say("BLOCKING: D4 was ADMITTED -- the cottonwood advisor reached advisor A's input")
                else:
                    results["D4"] = "D4 REFUSED NOT_AUTHORIZED" if code_of(b) == "NOT_AUTHORIZED" else fail_line("D4", st, b)
                detail.append("D4 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
            else:
                say(d_blocked)

            # the price date arms: the internal viewer, three uploads of the same bytes, P2 first so P1 and P1M meet a resolved input
            if log_ok:
                mint("IV", IV_LIFE)
                for arm, pd, tok, fname, loop, gap in (("P2", None, "irpt-r33-p2-%s" % date, "r33-p2.csv", True, None),
                                                       ("P1", PD_GOOD, "irpt-r33-p1-%s" % date, "r33-p1.csv", False, P_GAP_S),
                                                       ("P1M", PD_BAD, "irpt-r33-p1m-%s" % date, "r33-p1m.csv", False, P_GAP_S)):
                    st, b, raw, first, lastreq = upload(arm, "IV", "49financial", tok, fname, price_date=pd, loop=loop, min_gap=gap)
                    d = b.get("data") if isinstance(b, dict) else None
                    wins[arm] = window_of(first, lastreq)
                    ok = st == 200 and is_answer(b) and d.get("state") == "NORMALIZED"
                    results[arm + "_up"] = (ok, st, code_of(b))
                    detail.append("%s upload status=%s code=%s sent_price_date=%s" % (arm, st, code_of(b), pd is not None))
                if not windows_disjoint(list(wins.values())):
                    raise RuntimeError("the P arms' log windows overlap")
                # every window must have closed before its logs are read
                time.sleep(max(0.0, max(w[1] for w in wins.values()) + 5 - time.time()))
                for arm in ("P2", "P1", "P1M"):
                    lo, hi = wins[arm]
                    want = 0 if arm == "P2" else 1
                    try:
                        scanned, hits = count_window(logs, lo, hi)
                    except botocore.exceptions.ClientError as e:
                        results[arm] = "%s UNREAD log denied" % arm
                        log_lines.append("LOG_WINDOWS %s %s to %s events_scanned=UNREAD (%s)" % (arm, base.iso(lo), base.iso(hi), e.response.get("Error", {}).get("Code")))
                        continue
                    log_lines.append("LOG_WINDOWS %s %s to %s events_scanned=%d matches=%d" % (arm, base.iso(lo), base.iso(hi), scanned, hits))
                    up_ok, st, code = results[arm + "_up"]
                    if up_ok and hits == want:
                        results[arm] = "%s NORMALIZED price_date_ignored=%d" % (arm, hits)
                    else:
                        results[arm] = "%s FAIL %s %s" % (arm, st, code if not up_ok else "count=%d" % hits)
                    say("log window %s %s to %s: %d events scanned, %d with the exact string (want %d)" % (arm, base.iso(lo), base.iso(hi), scanned, hits, want))
            else:
                for arm in ("P2", "P1", "P1M"):
                    results[arm] = "%s UNREAD log denied" % arm
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; every row is still removed after exp
        stop = stop or "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        for k in list(tokens):
            tokens[k] = None
        pem_holder[0] = None
        if stop:
            say(str(stop))
        if (written_users or written_partner) and exps:
            wait = max(exps) + 5 - time.time()
            if wait > 0:
                say("waiting %ds for exp %s to pass before removal" % (int(wait), base.iso(max(exps))))
                time.sleep(wait)
        for k in written_users:
            try:
                ddb.delete_item(TableName=base.USERS, Key=ukey(k), ConditionExpression="attribute_exists(PK)")
                say("%s users row deleted (attribute_exists)" % k)
            except Exception as e:  # noqa: BLE001
                say("DELETE of users row %s failed: %s" % (k, str(e)[:160]))
        for k in written_partner:
            try:
                ddb.delete_item(TableName=ptable(k), Key=pkey(k), ConditionExpression="attribute_exists(email)")
                say("%s partner row deleted (attribute_exists)" % k)
            except Exception as e:  # noqa: BLE001
                say("DELETE of partner row %s failed: %s" % (k, str(e)[:160]))
        rem = []
        deadline = time.time() + 300
        say("removal window: bounded 5 minutes, until %s" % base.iso(deadline))
        state = {}
        while time.time() < deadline:
            for k in ids:
                state[k] = (gsi(k) == 0, uread(k) is None, (k == "IV") or (pread(k) is None))
            say("removal read: " + " ".join("%s GSI=%s CONS=%s PARTNER=%s" % (k, *v) for k, v in state.items()))
            if all(all(v) for v in state.values()):
                break
            time.sleep(10)
        for k, i in ids.items():
            g, c, p = state.get(k, (False, False, False))
            rem.append(("ABSENT GSI %s" if g else "PRESENT GSI %s") % i["addr"])
            rem.append(("ABSENT CONSISTENT %s" if c else "PRESENT CONSISTENT %s") % i["addr"])
            if not p:
                rem.append("PRESENT PARTNER %s" % i["addr"])
        # the intake store AFTER, taken last so the resident's asynchronous work is in
        try:
            after = list_store(s3)
            obj_lines = []
            for t in TENANTS:
                added = sorted(after[t][0] - (objects_before[t][0] if objects_before else set()))
                gone = sorted((objects_before[t][0] if objects_before else set()) - after[t][0])
                say("intake store AFTER %s: %d versions (before %d), %d delete markers (before %d), added %d, vanished %d" % (
                    t, len(after[t][0]), len(objects_before[t][0]) if objects_before else -1, after[t][1],
                    objects_before[t][1] if objects_before else -1, len(added), len(gone)))
                detail.append("AFTER %s versions=%d markers=%d added=%d vanished=%d" % (t, len(after[t][0]), after[t][1], len(added), len(gone)))
                for key, ver in added:
                    obj_lines.append("OBJ %s %s %s" % (BUCKET, key, ver))
            (outdir / "OBJECTS_WRITTEN_R33.txt").write_text(
                "\n".join(["# intake store AFTER, bucket %s, tenants %s" % (BUCKET, ",".join(TENANTS))]
                          + ["# BEFORE/AFTER version counts: " + "; ".join(d for d in detail if d.startswith(("BEFORE", "AFTER")))]
                          + obj_lines + ["OBJ_COUNT %d" % len(obj_lines)]) + "\n", encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            say("AFTER listing failed: %s" % str(e)[:200])
        order = ("D1", "D2", "D3", "D4", "P2", "P1", "P1M")
        res = [results.get(arm) or "%s NOT RUN %s" % (arm, stop or d_blocked or "an earlier arm did not run") for arm in order] + log_lines
        (outdir / "DOOR_RESULT_R33.txt").write_text("\n".join(res) + "\n", encoding="utf-8")
        (outdir / "DOOR_REMOVAL_R33.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "DOOR_TRACE_R33.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (outdir / "DOOR_DETAIL_R33.txt").write_text("\n".join(detail) + "\n", encoding="utf-8")
        (outdir / "DOOR_INPUTS_R33.txt").write_text(
            "\n".join("%s input_id=%s" % (k, v) for k, v in inputs.items()) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.live and args.go:
        return live(args)
    ap.error("choose --selftest or --live --go")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
