"""IRPT_ANLREQ TO-EXERCISE-R29 executor (0.7.0_AE_CloudOps~AQ2): the partner-advisor sitting of release 29.

Three synthetic partner advisors (A and B in 49financial, C in cottonwood) with their partner rows, one synthetic internal
viewer (Addendum 1b shape), ONE RS256 token each held in this process only, never written, printed or logged. Kept: status,
finding code or state, and sha256 of each body. No object is deleted. Every minted row is removed after exp and read ABSENT.

Reuses ../irpt_anlreq_r28/sitting_r28.py (constants, C1 closure, bun, expected price dates); only identities and arms change.

  --live --go    the sitting
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "irpt_anlreq_r28"))
import sitting_r28 as base  # noqa: E402

PAIR = base.REPO / ("org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release29/"
                    "NEVER_WIDEN_PAIR_ANLREQ_RELEASE29_ORDINARY_VIEWER_AND_SHARES_WORDS_THREE_LEG.md")
LEGS = (("irpt-status", "yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg="),
        ("irpt-ycharts-generate", "5TRFZf6Grgd9V9jWBVu2QDPRVbgfWBjsuuw8rtf8hRA="))
BUCKET = "opal-data-irpt"
TENANTS = ("49financial", "cottonwood")
UPLOAD = "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=%s"
ANALYSIS = "/api/scoped/investor-reporting/analysis?selected_tenant=%s"
ANSWER_STATES = ("NEEDS_CORRECTION", "NORMALIZED")
SHARES_CODE = "SHARES_PRICE_SOURCE_NOT_COMPOSED"
# Distinct amounts from release 28's file, so no stored input collides with the c449 input.
FILE_D1 = b"Ticker,Dollars,Acct Market Value\nSPY,100,26000000\nAGG,200,32000000\n"
FILE_D6 = b"Ticker,Dollars,Acct Market Value\nSPY,100,27000000\nAGG,200,33000000\n"
FILE_D5 = b"Ticker,Shares\nSPY,10\nAGG,5\n"
TITLE = "SYNTHETIC release-29 sitting, do not action"


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


def upload_body(token, filename, content):
    return {"upload_token": token, "filename": filename, "file_base64": base64.b64encode(content).decode(), "file_type": "csv"}


def analysis_body(req, input_id):
    return {"request_id": req, "client_id": None, "account_ids": [], "snapshot_id": None, "variant": "overview",
            "comparison_keys": [], "report_title": TITLE, "prepared_for": "SYNTHETIC", "input_id": input_id}


def expected_words():
    text = PAIR.read_text(encoding="utf-8")
    m = re.search(r'with the words "([^"]+)"', text)
    if not m:
        raise RuntimeError("the pair's section 4b words were not found")
    return m.group(1)


def sha(s):
    return hashlib.sha256(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def list_store(s3):
    """(key, version_id) of every version and delete marker under each tenant prefix, per tenant."""
    out = {}
    for t in TENANTS:
        items, markers = set(), 0
        for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix="irpt/%s/" % t):
            for v in pg.get("Versions", []) or []:
                items.add((v["Key"], v["VersionId"]))
            markers += len(pg.get("DeleteMarkers", []) or [])
        out[t] = (items, markers)
    return out


def live(args):
    import boto3
    import jwt as pyjwt

    date = args.date
    outdir = Path(args.out)
    ddb = boto3.client("dynamodb", region_name=base.REGION)
    s3 = boto3.client("s3", region_name=base.REGION)
    lam = boto3.client("lambda", region_name=base.REGION)
    ids = {
        "A": dict(addr="irpt-r29-a-%s@opal.invalid" % date, firm="49financial", label="advisor A", kind="advisor"),
        "B": dict(addr="irpt-r29-b-%s@opal.invalid" % date, firm="49financial", label="advisor B", kind="advisor"),
        "C": dict(addr="irpt-r29-c-%s@opal.invalid" % date, firm="cottonwood", label="advisor C", kind="advisor"),
        "IV": dict(addr="irpt-r29-iv-%s@opal.invalid" % date, firm="opal-capital", label="internal viewer", kind="internal"),
    }
    lines, detail, results, tokens = [], [], {}, {}
    written_users, written_partner, exps, objects_before = [], [], [], None
    inputs = {}

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

    last = [0.0]

    def call(arm, who, path, body):
        wait = base.GAP - (time.time() - last[0])
        if wait > 0:
            time.sleep(wait)
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
        return st, b, raw

    def upload(arm, who, firm, token, filename, content):
        for _ in range(8):
            st, b, raw = call(arm, who, UPLOAD % firm, upload_body(token, filename, content))
            d = b.get("data") if isinstance(b, dict) else None
            if not (isinstance(d, dict) and d.get("state") == "RESOLVING"):
                break
        return st, b, raw

    def fail_line(arm, st, b):
        return "%s FAIL %s %s" % (arm, st, code_of(b))

    stop = None
    bodies = {}
    try:
        for fn, want in LEGS:
            got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            say("%s CodeSha256 %s" % (fn, "EQUAL" if got == want else "DIFFERENT"))
            if got != want:
                raise RuntimeError("a leg is not at its expected CodeSha256")
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
                        "status": {"S": "active"}, "name": {"S": "IRPT_ANLREQ R29 synthetic %s" % i["label"]},
                        "role": {"S": "user"}, "tier": {"S": "advisor"},
                        "allowedFirmIds": {"L": [{"S": i["firm"]}]},
                        "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
            else:
                item = {"PK": ukey(k)["PK"], "SK": ukey(k)["SK"], "email": {"S": i["addr"]}, "firmId": {"S": "opal-capital"},
                        "status": {"S": "active"}, "name": {"S": "IRPT_ANLREQ R29 synthetic internal viewer"},
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
                prow = {"email": {"S": i["addr"]}, "advisorKey": {"S": "irpt-r29-adv-%s-%s" % (k.lower(), date)},
                        "advisorName": {"S": "IRPT_ANLREQ R29 synthetic %s" % i["label"]}, "advisorRole": {"S": "viewer"},
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
        say("signing key read (value never printed or written)")
        for k, i in ids.items():
            iat = int(time.time())
            if i["kind"] == "advisor":
                key = "irpt-r29-adv-%s-%s" % (k.lower(), date)
                claims = {"sub": i["addr"], "iss": "opal-portal-auth", "aud": "opal-portal-api", "name": "IRPT_ANLREQ R29 synthetic %s" % i["label"],
                          "role": "user", "tier": "advisor", "firmId": i["firm"], "advisorKey": key, "advisorName": "IRPT_ANLREQ R29 synthetic %s" % i["label"],
                          "advisorRole": "viewer", "advisorId": key, "firmRole": "user", "iat": iat, "exp": iat + base.LIFE}
            else:
                claims = {"sub": i["addr"], "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
                          "role": "user", "userType": "test-filer", "name": "IRPT_ANLREQ R29 synthetic internal viewer",
                          "iat": iat, "exp": iat + base.LIFE}
            tokens[k] = pyjwt.encode(claims, pem, algorithm="RS256")
            exps.append(claims["exp"])
            say("token for %s minted (held in memory only) iat=%s exp=%s" % (k, base.iso(iat), base.iso(claims["exp"])))
        del pem

        words = expected_words()

        # D1: A uploads the market-value file
        st, b, raw = upload("D1", "A", "49financial", "irpt-r29-d1-%s" % date, "r29-d1.csv", FILE_D1)
        d = b.get("data") if isinstance(b, dict) else None
        bodies["D1"] = raw
        if code_of(b) == "NOT_AUTHORIZED":
            results["D1"] = fail_line("D1", st, b)
            stop = "D1 answered NOT_AUTHORIZED: STOP, rows removed, no other identity"
        elif st == 200 and is_answer(b) and d.get("state") == "NORMALIZED" and isinstance(d.get("input_id"), str):
            results["D1"] = "D1 NORMALIZED"
            inputs["D1"] = d["input_id"]
        else:
            results["D1"] = fail_line("D1", st, b)
            stop = "D1 did not answer NORMALIZED: the analysis arms need its input, STOP"
        detail.append("D1 status=%s code=%s" % (st, code_of(b)))

        if not stop:
            # D2: A analyses A's input
            st, b, raw = call("D2", "A", ANALYSIS % "49financial", analysis_body("irpt-r29-d2-%s" % date, inputs["D1"]))
            results["D2"] = "D2 ADMITTED" if admitted(st, b) else fail_line("D2", st, b)
            detail.append("D2 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
            # D3: B analyses A's input (same firm)
            st, b, raw = call("D3", "B", ANALYSIS % "49financial", analysis_body("irpt-r29-d3-%s" % date, inputs["D1"]))
            if admitted(st, b):
                results["D3"] = "D3 FAIL %s ADMITTED" % st
                say("BLOCKING: D3 was ADMITTED -- advisor B reached advisor A's input")
            else:
                results["D3"] = "D3 REFUSED NOT_AUTHORIZED" if code_of(b) == "NOT_AUTHORIZED" else fail_line("D3", st, b)
            detail.append("D3 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
            # D4: C (cottonwood) analyses A's input by its id, selected firm cottonwood
            st, b, raw = call("D4", "C", ANALYSIS % "cottonwood", analysis_body("irpt-r29-d4-%s" % date, inputs["D1"]))
            if admitted(st, b):
                results["D4"] = "D4 FAIL %s ADMITTED" % st
                say("BLOCKING: D4 was ADMITTED -- the cottonwood advisor reached advisor A's input")
            else:
                results["D4"] = "D4 REFUSED NOT_AUTHORIZED" if code_of(b) == "NOT_AUTHORIZED" else fail_line("D4", st, b)
            detail.append("D4 status=%s code=%s admitted=%s" % (st, code_of(b), admitted(st, b)))
            # D5: A uploads the Shares file
            st, b, raw = upload("D5", "A", "49financial", "irpt-r29-d5-%s" % date, "r29-d5.csv", FILE_D5)
            d = b.get("data") if isinstance(b, dict) else None
            bodies["D5"] = raw
            fnd = [f for f in ((d or {}).get("findings") or []) if isinstance(f, dict) and f.get("code") == SHARES_CODE] if isinstance(d, dict) else []
            got_words = fnd[0].get("description") if fnd else None
            eq = isinstance(got_words, str) and got_words == words
            say("D5 finding words sha256 %s, pair 4b words sha256 %s, byte-equal=%s" % (sha(got_words) if isinstance(got_words, str) else "NONE", sha(words), eq))
            ok = st == 200 and isinstance(d, dict) and d.get("state") == "NEEDS_CORRECTION" and bool(fnd) and eq and d.get("input_id") is None
            results["D5"] = ("D5 NEEDS_CORRECTION %s" % SHARES_CODE) if ok else fail_line("D5", st, b)
            detail.append("D5 status=%s code=%s finding=%s words_equal=%s input_id_none=%s" % (
                st, code_of(b), bool(fnd), eq, (d or {}).get("input_id") is None if isinstance(d, dict) else None))
            # D6: the internal viewer on both routes
            st6a, b6a, raw6a = upload("D6a", "IV", "49financial", "irpt-r29-d6-%s" % date, "r29-d6.csv", FILE_D6)
            d6 = b6a.get("data") if isinstance(b6a, dict) else None
            up_ok = st6a == 200 and is_answer(b6a) and d6.get("state") == "NORMALIZED" and isinstance(d6.get("input_id"), str)
            an_ok = False
            st6b = None
            b6b = None
            if up_ok:
                inputs["D6"] = d6["input_id"]
                st6b, b6b, _raw = call("D6b", "IV", ANALYSIS % "49financial", analysis_body("irpt-r29-d6-%s" % date, d6["input_id"]))
                an_ok = admitted(st6b, b6b)
            results["D6"] = "D6 UNCHANGED" if (up_ok and an_ok) else "D6 FAIL %s %s" % (st6a if not up_ok else st6b, code_of(b6a if not up_ok else b6b))
            detail.append("D6 upload status=%s code=%s ; analysis status=%s code=%s admitted=%s" % (
                st6a, code_of(b6a), st6b, code_of(b6b) if b6b is not None else None, an_ok))

        # C1: the bodies of D1 and D5, answers only
        c1 = "C1 NOT RUN no door arm answered"
        if bodies:
            notans = [k for k in ("D1", "D5") if k not in bodies or not is_answer(base.parsed(bodies[k]))]
            if notans:
                c1 = "C1 NOT RUN not an answer body: %s" % ",".join(notans)
            else:
                bun = base.find_bun()
                scratch = tempfile.mkdtemp(prefix="r29_c1_")
                try:
                    commit, root = base.c1_prepare(scratch)
                    got = [base.c1_parse(bun, root, bodies[k]) for k in ("D1", "D5")]
                    say("C1 parseIrEnvelope from portal origin/PROD %s: %s" % (commit[:10], got))
                    c1 = "C1 PARSED 2 of 2 answers" if got == ["PARSED"] * 2 else "C1 FAIL %s" % got
                finally:
                    shutil.rmtree(scratch, ignore_errors=True)
        results["C1"] = c1
        bodies.clear()
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; every row is still removed after exp
        stop = stop or "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        for k in list(tokens):
            tokens[k] = None
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
            (outdir / "OBJECTS_WRITTEN_R29.txt").write_text(
                "\n".join(["# intake store AFTER, bucket %s, tenants %s" % (BUCKET, ",".join(TENANTS))]
                          + ["# BEFORE/AFTER version counts: " + "; ".join(d for d in detail if d.startswith(("BEFORE", "AFTER")))]
                          + obj_lines + ["OBJ_COUNT %d" % len(obj_lines)]) + "\n", encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            say("AFTER listing failed: %s" % str(e)[:200])
        order = ("D1", "D2", "D3", "D4", "D5", "D6", "C1")
        res = [results.get(arm) or "%s NOT RUN %s" % (arm, stop or "an earlier arm did not run") for arm in order]
        (outdir / "DOOR_RESULT_R29.txt").write_text("\n".join(res) + "\n", encoding="utf-8")
        (outdir / "DOOR_REMOVAL_R29.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "DOOR_TRACE_R29.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (outdir / "DOOR_DETAIL_R29.txt").write_text("\n".join(detail) + "\n", encoding="utf-8")
        (outdir / "DOOR_INPUTS_R29.txt").write_text(
            "\n".join("%s input_id=%s" % (k, v) for k, v in inputs.items()) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    if args.live and args.go:
        return live(args)
    ap.error("choose --live --go")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
