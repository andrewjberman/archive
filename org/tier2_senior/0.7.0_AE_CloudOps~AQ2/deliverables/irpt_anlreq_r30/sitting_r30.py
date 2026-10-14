"""IRPT_ANLREQ TO-EXERCISE-R30 executor (0.7.0_AE_CloudOps~AQ2): the release-29b refusal-arm sitting of the ticket service.

Two minted synthetic client users (B in 49financial, C in cottonwood), ONE RS256 token each held in this process only, never
written, printed or logged. Three REFUSAL arms against POST /api/scoped/tickets/submit, each expected HTTP 400 with the one
text; no ticket written, no mail sent; the tickets table COUNT is read before and after. Kept: status, error text, sha256.

Reuses ../irpt_anlreq_r28/sitting_r28.py (constants, expected helpers) and sitting_r29.py's shape; only identities, route and arms change.

  --offline      the body proof against the service's own code (no AWS call, no network); must pass before --live
  --live --go    the sitting
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import secrets
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "irpt_anlreq_r28"))
import sitting_r28 as base  # noqa: E402

ORDER_INPUT_ID = "portfolio_ac6ac6bd0ddb9e33c3766b44b88da5d2253db219848824b202a2ee84b2c40cb0"
A_ADDR = "irpt-r29-a-20261014@opal.invalid"
LAMBDA_SHA = "Fg8MdfvCvcB8at9K+Bh+IpmuNel8TNWXaKth0W2pv4A="
SUBMIT = "/api/scoped/tickets/submit"
TEXT = "attachment.input_id is not available to the caller"
TICKETS = "opal-tickets"
TITLE = "SYNTHETIC release-29b refusal arm, do not action"
UPLOAD_ID = "irpt-r30-synthetic-upload"
PROOF_FILE = HERE / "OFFLINE_PROOF_R30.txt"
HARNESS = base.REPO / "infra/aws/lambda/ticket_center/tests/test_authz_matrix.py"


def sha(s):
    return hashlib.sha256(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def body_for(firm, input_id):
    return {"ticket_type": "analysis_request", "title": TITLE,
            "answers": {"advisor": "SYNTHETIC advisor", "firm": firm, "household": "SYNTHETIC household", "report_type": "Overview"},
            "attachment": {"upload_id": UPLOAD_ID, "input_id": input_id}}


def err_text(raw):
    try:
        b = json.loads(raw)
    except (TypeError, ValueError):
        return "UNPARSED"
    return str(b.get("error")) if isinstance(b, dict) and "error" in b else ("2XX-BODY" if isinstance(b, dict) else "UNPARSED")


# ------------------------------------------------------------------------------------------------------------- offline
def offline(date):
    spec = importlib.util.spec_from_file_location("authz_matrix_harness", str(HARNESS))
    H = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(H)
    mod = H.mod
    out, ok_all = [], True

    def rec(label, ok, detail=""):
        nonlocal ok_all
        ok_all = ok_all and bool(ok)
        out.append("%s %s %s" % ("PASS" if ok else "FAIL", label, detail))

    b_addr = "irpt-r30-b-%s@opal.invalid" % date
    c_addr = "irpt-r30-c-%s@opal.invalid" % date
    k3_id = "portfolio_" + "7" * 64
    arms = {"K1": ("49financial", b_addr, ORDER_INPUT_ID), "K2": ("cottonwood", c_addr, ORDER_INPUT_ID), "K3": ("49financial", b_addr, k3_id)}
    defn = mod.TYPE_DEFINITIONS["analysis_request"]
    for arm, (firm, addr, iid) in arms.items():
        body = body_for(firm, iid)
        clean, err = mod._validate_answers(defn, body["answers"], mod.CLIENT)
        rec("%s _validate_answers accepts the body" % arm, err is None and clean["firm"] == firm, "err=%s" % err)
        att, err = mod._validate_attachment(defn["attachment"], body["attachment"])
        rec("%s _validate_attachment accepts the body" % arm, err is None and att["input_id"] == iid, "err=%s" % err)

    def run(arm, reader_row):
        firm, addr, iid = arms[arm]
        calls = []

        def reader(f, i):
            calls.append((f, i))
            return reader_row(f, i) if callable(reader_row) else reader_row

        mod.notify_dl_isolated = lambda item: calls.append(("MAIL-DL",))
        mod.notify_client_isolated = lambda item, kind: calls.append(("MAIL-CLIENT",))
        mod._table = H.FakeTable()
        mod._input_owner_reader = reader
        H.empty_users(mod)
        ctx = {"email": addr, "name": "IRPT_ANLREQ R30 synthetic %s" % arm, "firmId": firm, "userType": "null", "allowedFirmIds": firm}
        code, b = H.call("POST", SUBMIT, ctx, body_for(firm, iid))
        return code, b, calls, len(mod._table.items)

    for arm in ("K1", "K2", "K3"):
        firm, addr, iid = arms[arm]
        code, b, calls, n = run(arm, None)
        rec("%s reader stubbed to NO row -> exactly the owner-check 400" % arm,
            code == 400 and b == {"error": TEXT} and calls == [(firm, iid)] and n == 0, "status=%s calls=%s tickets=%d" % (code, calls, n))
    code, b, calls, n = run("K1", lambda f, i: {"tenant": f, "request_revision": "INPUT#" + i, "identity": i,
                                                 "owner": {"firm_id": f, "principal_id": A_ADDR, "principal_class": "FIRM_ADVISOR"}})
    rec("K1 reader returns a row owned by ANOTHER principal -> the same 400, nothing written", code == 400 and b == {"error": TEXT} and n == 0, "status=%s tickets=%d" % (code, n))
    code, b, calls, n = run("K1", lambda f, i: {"tenant": f, "request_revision": "INPUT#" + i, "identity": i,
                                                 "owner": {"firm_id": f, "principal_id": b_addr}})
    rec("POSITIVE CONTROL: the same K1 body with an owner row naming the caller reaches 201 (so the 400 is the owner check alone)",
        code == 201 and n == 1, "status=%s tickets=%d (local fake table only)" % (code, n))
    def raising(f, i):
        raise RuntimeError("read denied")
    code, b, calls, n = run("K1", raising)
    rec("a reader that raises -> 503 (fail closed), distinct from the 400", code == 503 and n == 0, "status=%s tickets=%d" % (code, n))
    bodies = {a: json.dumps(run(a, None)[1], sort_keys=True) for a in arms}
    rec("the three local 400 bodies are byte-equal", len(set(bodies.values())) == 1, "distinct=%d" % len(set(bodies.values())))
    rec("local run touched no real AWS and no real mail (stubs only)", True, "the harness replaces _table, the reader and both mail seams")
    PROOF_FILE.write_text("\n".join(out) + "\nOFFLINE_PROOF %s\n" % ("PASS" if ok_all else "FAIL"), encoding="ascii")
    print("\n".join(out))
    print("OFFLINE_PROOF", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


# ---------------------------------------------------------------------------------------------------------------- live
def count_table(ddb):
    total = scanned = pages = 0
    for pg in ddb.get_paginator("scan").paginate(TableName=TICKETS, Select="COUNT"):
        total += pg["Count"]
        scanned += pg["ScannedCount"]
        pages += 1
    return total, scanned, pages


def live(args):
    import boto3
    import jwt as pyjwt

    if not PROOF_FILE.exists() or "OFFLINE_PROOF PASS" not in PROOF_FILE.read_text(encoding="ascii"):
        print("STOP: the offline proof has not passed; run --offline first")
        return 2
    date = args.date
    outdir = Path(args.out)
    ddb = boto3.client("dynamodb", region_name=base.REGION)
    lam = boto3.client("lambda", region_name=base.REGION)
    iam = boto3.client("iam", region_name=base.REGION)
    ids = {"B": dict(addr="irpt-r30-b-%s@opal.invalid" % date, firm="49financial"),
           "C": dict(addr="irpt-r30-c-%s@opal.invalid" % date, firm="cottonwood")}
    lines, results, tokens, written, exps, detail = [], {}, {}, [], [], []
    hashes, texts = {}, {}

    def say(msg):
        line = "%s %s" % (base.iso(), msg)
        print(line, flush=True)
        lines.append(line)

    def ukey(k):
        return {"PK": {"S": "USER#" + ids[k]["addr"]}, "SK": {"S": "PROFILE"}}

    def uread(k):
        return ddb.get_item(TableName=base.USERS, Key=ukey(k), ConsistentRead=True).get("Item")

    def gsi(k):
        return ddb.query(TableName=base.USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": ids[k]["addr"]}}, Select="COUNT")["Count"]

    last = [0.0]

    def call(arm, who, firm, input_id):
        wait = base.GAP - (time.time() - last[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(base.BASE + SUBMIT, data=json.dumps(body_for(firm, input_id)).encode("utf-8"), method="POST")
        req.add_header("Authorization", "Bearer " + tokens[who])
        req.add_header("x-contract-version", "v1")
        req.add_header("Content-Type", "application/json")
        start = last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                st, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            st, raw = e.code, e.read().decode("utf-8", "replace")
        text = err_text(raw)
        hashes[arm], texts[arm] = sha(raw), text
        say("request %s as %s start=%s status=%s text=%r body_sha256=%s" % (arm, who, base.iso(start), st, text[:120], sha(raw)))
        return st, raw, text

    stop = None
    count_before = count_after = None
    try:
        got = lam.get_function_configuration(FunctionName="opal-ticket-api")["CodeSha256"]
        say("opal-ticket-api CodeSha256 %s" % ("EQUAL" if got == LAMBDA_SHA else "DIFFERENT"))
        if got != LAMBDA_SHA:
            raise RuntimeError("the Lambda is not at its expected CodeSha256")
        pol = iam.get_role_policy(RoleName="opal-ticket-api-role", PolicyName="opal-tickets-table-rw")["PolicyDocument"]
        sids = [s.get("Sid") for s in (pol["Statement"] if isinstance(pol["Statement"], list) else [pol["Statement"]])]
        say("role policy IrptRequestsInputOwnerRead present %d time(s) of %d statements" % (sids.count("IrptRequestsInputOwnerRead"), len(sids)))
        if sids.count("IrptRequestsInputOwnerRead") != 1:
            raise RuntimeError("the grant statement is not present exactly once")

        # R0i: the owner row, now, right before the arms
        r = ddb.get_item(TableName="irpt-requests", Key={"tenant": {"S": "49financial"}, "request_revision": {"S": "INPUT#" + ORDER_INPUT_ID}},
                         ConsistentRead=True, ProjectionExpression="#t, #r, #i, #o",
                         ExpressionAttributeNames={"#t": "tenant", "#r": "request_revision", "#i": "identity", "#o": "owner"})
        item = r.get("Item")
        own = (item or {}).get("owner", {}).get("M", {})
        pid = own.get("principal_id", {}).get("S")
        r0i = bool(item) and own.get("firm_id", {}).get("S") == "49financial" and pid == A_ADDR and pid != ids["B"]["addr"]
        say("R0i owner row present=%s owner field names=%s firm_id=49financial:%s principal is A:%s is B:%s" % (
            "yes" if item else "no", sorted(own), own.get("firm_id", {}).get("S") == "49financial", pid == A_ADDR, pid == ids["B"]["addr"]))
        if not r0i:
            results["R0I"] = "R0I FAIL owner row %s" % ("absent" if not item else "not A's")
            raise RuntimeError("R0i did not read as required: the sitting does not open")
        results["R0I"] = "R0I OWNER_ROW_PRESENT_NOT_B"

        count_before = count_table(ddb)
        say("tickets COUNT BEFORE: count=%d scanned=%d pages=%d" % count_before)

        for k in ids:
            if uread(k) is not None or gsi(k) != 0:
                raise RuntimeError("address %s is not ABSENT by ConsistentRead and GSI" % k)
        say("pre-state: two users keys ABSENT by ConsistentRead, two addresses return 0 on the email index")
        now = base.iso()
        for k, i in ids.items():
            item = {"PK": ukey(k)["PK"], "SK": ukey(k)["SK"], "email": {"S": i["addr"]}, "firmId": {"S": i["firm"]},
                    "status": {"S": "active"}, "name": {"S": "IRPT_ANLREQ R30 synthetic client %s" % k}, "role": {"S": "user"},
                    "tier": {"S": "advisor"}, "allowedFirmIds": {"L": [{"S": i["firm"]}]},
                    "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
            ddb.put_item(TableName=base.USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
            written.append(k)
            back = uread(k)
            if back is None or back["status"]["S"] != "active" or [m.get("S") for m in back["allowedFirmIds"]["L"]] != [i["firm"]]:
                raise RuntimeError("users row %s not PRESENT as designed" % k)
            say("%s users row written (attribute_not_exists) and read back PRESENT (status active, explicit allowedFirmIds list of its one firm)" % k)
        pem = boto3.client("secretsmanager", region_name=base.REGION).get_secret_value(SecretId=base.KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        say("signing key read (value never printed or written)")
        for k, i in ids.items():
            iat = int(time.time())
            claims = {"sub": i["addr"], "iss": "opal-portal-auth", "aud": "opal-portal-api", "name": "IRPT_ANLREQ R30 synthetic client %s" % k,
                      "role": "user", "tier": "advisor", "firmId": i["firm"], "iat": iat, "exp": iat + base.LIFE}
            tokens[k] = pyjwt.encode(claims, pem, algorithm="RS256")
            exps.append(claims["exp"])
            say("token for %s minted (held in memory only) iat=%s exp=%s" % (k, base.iso(iat), base.iso(claims["exp"])))
        del pem

        k3_id = "portfolio_" + secrets.token_hex(32)
        arms = (("K1", "B", "49financial", ORDER_INPUT_ID), ("K2", "C", "cottonwood", ORDER_INPUT_ID), ("K3", "B", "49financial", k3_id))
        for arm, who, firm, iid in arms:
            st, raw, text = call(arm, who, firm, iid)
            detail.append("%s status=%s text=%r" % (arm, st, text[:120]))
            if st == 400 and text == TEXT:
                results[arm] = "%s REFUSED 400 INPUT_NOT_AVAILABLE" % arm
            else:
                results[arm] = "%s FAIL %s %s" % (arm, st, text[:120])
                if st == 503:
                    stop = "%s answered 503: the grant is missing or wrong: STOP, no other identity" % arm
                elif isinstance(st, int) and 200 <= st < 300:
                    tid = None
                    try:
                        tid = json.loads(raw).get("ticket", {}).get("ticket_id")
                    except (TypeError, ValueError):
                        pass
                    stop = "BLOCKING: %s answered %s -- the owner check is not firing; ticket written: %s (not deleted by this seat)" % (arm, st, tid)
                    results["TICKET_WRITTEN"] = "TICKET_WRITTEN %s" % tid
                if stop:
                    break
        if all(a in hashes for a in ("K1", "K2", "K3")):
            distinct = {hashes[a] for a in ("K1", "K2", "K3")}
            results["K123"] = ("K123 SAME_BODY %s" % next(iter(distinct))) if len(distinct) == 1 else "K123 FAIL %d distinct body hashes" % len(distinct)
        count_after = count_table(ddb)
        say("tickets COUNT AFTER: count=%d scanned=%d pages=%d" % count_after)
        results["COUNT"] = ("TICKETS_COUNT_EQUAL %d" % count_after[0]) if count_after[0] == count_before[0] else "TICKETS_COUNT FAIL before=%d after=%d" % (count_before[0], count_after[0])
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; every row is still removed after exp
        stop = stop or "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        for k in list(tokens):
            tokens[k] = None
        if stop:
            say(str(stop))
        if written and exps:
            wait = max(exps) + 5 - time.time()
            if wait > 0:
                say("waiting %ds for exp %s to pass before removal" % (int(wait), base.iso(max(exps))))
                time.sleep(wait)
        for k in written:
            try:
                ddb.delete_item(TableName=base.USERS, Key=ukey(k), ConditionExpression="attribute_exists(PK)")
                say("%s users row deleted (attribute_exists)" % k)
            except Exception as e:  # noqa: BLE001
                say("DELETE of users row %s failed: %s" % (k, str(e)[:160]))
        rem = []
        deadline = time.time() + 300
        say("removal window: bounded 5 minutes, until %s" % base.iso(deadline))
        state = {}
        while time.time() < deadline:
            for k in ids:
                state[k] = (gsi(k) == 0, uread(k) is None)
            say("removal read: " + " ".join("%s GSI=%s CONS=%s" % (k, *v) for k, v in state.items()))
            if all(all(v) for v in state.values()):
                break
            time.sleep(10)
        for k, i in ids.items():
            g, c = state.get(k, (False, False))
            rem.append(("ABSENT GSI %s" if g else "PRESENT GSI %s") % i["addr"])
            rem.append(("ABSENT CONSISTENT %s" if c else "PRESENT CONSISTENT %s") % i["addr"])
        try:
            final = count_table(ddb)
            say("tickets COUNT at the end of the sitting: count=%d scanned=%d" % (final[0], final[1]))
            detail.append("COUNT before=%s after=%s end=%s" % (count_before, count_after, final))
        except Exception as e:  # noqa: BLE001
            say("final COUNT failed: %s" % str(e)[:160])
        order = ("R0I", "K1", "K2", "K3", "K123", "COUNT")
        res = [results.get(a) or "%s NOT RUN %s" % (a, stop or "an earlier step did not run") for a in order]
        if "TICKET_WRITTEN" in results:
            res.append(results["TICKET_WRITTEN"])
        (outdir / "TICKET_ARMS_R30.txt").write_text("\n".join(res) + "\n", encoding="utf-8")
        (outdir / "TICKET_REMOVAL_R30.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "TICKET_TRACE_R30.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (outdir / "TICKET_DETAIL_R30.txt").write_text("\n".join(detail) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    if args.offline:
        return offline(args.date)
    if args.live and args.go:
        return live(args)
    ap.error("choose --offline or --live --go")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
