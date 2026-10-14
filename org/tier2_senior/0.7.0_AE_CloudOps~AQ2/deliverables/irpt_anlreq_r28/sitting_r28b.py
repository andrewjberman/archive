"""IRPT_ANLREQ TO-EXERCISE-R28b executor (0.7.0_AE_CloudOps~AQ2): the upload door D1-D4 and C1 as ONE synthetic internal viewer.

Addendum 1b: the users PROFILE row carries NO allowedFirmIds attribute, so the door takes access.prospect_owner().
Reuses sitting_r28.py (files, bodies, C1 closure, bun, expected price dates). Differences: the identity, no ticket arms, a
stop at once on NOT_AUTHORIZED, and C1 grades ANSWER bodies only (a refusal envelope is C1 NOT RUN).
The token is minted in this process and never written, printed or logged. Kept: status, code or state, sha256 only.

  --live --go    the sitting
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sitting_r28 as base  # noqa: E402

ANSWER_STATES = ("NEEDS_CORRECTION", "NORMALIZED")
LEGS = (("irpt-status", "MIVrDbv+/w8ioVB24xS97gnETVbNRCroDiY+Ne5osbA="),
        ("opal-ticket-api", "C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM="),
        ("irpt-ycharts-generate", "reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc="))


def code_of(b):
    """The refusal code of a refusal envelope, else the answer state."""
    if not isinstance(b, dict):
        return "UNPARSED"
    if b.get("ok") is False or "data" not in b:
        return str(((b.get("status") or {}).get("public_reason_code")) or "NO_CODE")
    d = b.get("data")
    return str(d.get("state")) if isinstance(d, dict) else "NO_STATE"


def is_answer(b):
    d = b.get("data") if isinstance(b, dict) and b.get("ok") is not False else None
    return isinstance(d, dict) and d.get("state") in ANSWER_STATES


def live(addr, args):
    import json

    import boto3
    import jwt as pyjwt

    ddb = boto3.client("dynamodb", region_name=base.REGION)
    outdir = Path(args.out)
    lines, tokens, results, detail, inputs = [], {}, {}, [], {}
    written, exps, starts = [], [], []

    def say(msg):
        line = "%s %s" % (base.iso(), msg)
        print(line, flush=True)
        lines.append(line)

    key = {"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}

    def cread():
        return ddb.get_item(TableName=base.USERS, Key=key, ConsistentRead=True).get("Item")

    def gsi():
        return ddb.query(TableName=base.USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]

    last = [0.0]

    def call(arm, body):
        wait = base.GAP - (time.time() - last[0])
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(base.BASE + base.DOOR, data=json.dumps(body).encode("utf-8"), method="POST")
        req.add_header("Authorization", "Bearer " + tokens["IV"])
        req.add_header("x-contract-version", "v1")
        req.add_header("Content-Type", "application/json")
        start = last[0] = time.time()
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                st, raw = r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            st, raw = e.code, e.read().decode("utf-8", "replace")
        starts.append(start)
        b = base.parsed(raw)
        say("request %s start=%s status=%s code=%s body_sha256=%s" % (arm, base.iso(start), st, code_of(b), hashlib.sha256(raw.encode()).hexdigest()))
        return st, b, raw

    def resolve(label):
        for _ in range(8):
            st, b, raw = call(label, base.door_body(label, args.date))
            d = b.get("data") if isinstance(b, dict) else None
            if not (isinstance(d, dict) and d.get("state") == "RESOLVING"):
                break
        return st, b, raw

    def fail_line(arm, st, b):
        return "%s FAIL %s %s" % (arm, st, code_of(b))

    stop = None
    try:
        lam = boto3.client("lambda", region_name=base.REGION)
        for fn, want in LEGS:
            got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            say("%s CodeSha256 %s" % (fn, "EQUAL" if got == want else "DIFFERENT"))
            if got != want:
                raise RuntimeError("a leg is not at its expected CodeSha256")
        if cread() is not None or gsi() != 0:
            raise RuntimeError("the address is not ABSENT before the sitting")
        say("pre-state: IV key ABSENT by ConsistentRead and the email index returns 0")
        now = base.iso()
        item = {"PK": key["PK"], "SK": key["SK"], "email": {"S": addr}, "firmId": {"S": "opal-capital"}, "status": {"S": "active"},
                "name": {"S": "IRPT_ANLREQ R28b synthetic internal viewer"}, "role": {"S": "user"}, "tier": {"S": "internal"},
                "userType": {"S": "test-filer"}, "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
        ddb.put_item(TableName=base.USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
        written.append(addr)
        back = cread()
        if back is None or back["status"]["S"] != "active" or "allowedFirmIds" in back:
            raise RuntimeError("the users row is not PRESENT as designed (active, no allowedFirmIds)")
        say("IV users row written (attribute_not_exists) and read back PRESENT: status active, no allowedFirmIds attribute")
        pem = boto3.client("secretsmanager", region_name=base.REGION).get_secret_value(SecretId=base.KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        say("signing key read (value never printed or written)")
        iat = int(time.time())
        claims = {"sub": addr, "iss": "opal-portal-auth", "aud": "opal-portal-api", "firmId": "opal-capital", "tier": "internal",
                  "role": "user", "userType": "test-filer", "name": "IRPT_ANLREQ R28b synthetic internal viewer",
                  "iat": iat, "exp": iat + base.LIFE}
        tokens["IV"] = pyjwt.encode(claims, pem, algorithm="RS256")
        exps.append(claims["exp"])
        say("token for IV minted (held in memory only) iat=%s exp=%s" % (base.iso(iat), base.iso(claims["exp"])))
        del pem

        default_price_date = base.expected_price_dates()
        before = default_price_date(None)
        bodies = {}
        # D1
        st, b, raw = call("D1", base.door_body("D1", args.date))
        d = b.get("data") if isinstance(b, dict) else None
        codes = base.d_codes(d) if isinstance(d, dict) else set()
        bodies["D1"] = raw
        if code_of(b) == "NOT_AUTHORIZED":
            results["D1"] = fail_line("D1", st, b)
            stop = "D1 answered NOT_AUTHORIZED: STOP, row removed, no other identity"
        elif st == 200 and is_answer(b) and d.get("state") == "NEEDS_CORRECTION" and "ACCOUNT_COLUMN_SEVERAL_VALUES" in codes:
            results["D1"] = "D1 NEEDS_CORRECTION ACCOUNT_COLUMN_SEVERAL_VALUES"
        else:
            results["D1"] = fail_line("D1", st, b)
            if isinstance(d, dict) and d.get("state") == "NORMALIZED":
                say("BLOCKING: a two-account file was ACCEPTED at D1")
                inputs["D1 (WRONG, stored)"] = d.get("input_id")
        detail.append("D1 status=%s code=%s findings=%s" % (st, code_of(b), sorted(codes)))
        if not stop:
            st, b, raw = resolve("D2")
            d = b.get("data") if isinstance(b, dict) else None
            bodies["D2"] = raw
            ok = st == 200 and is_answer(b) and d.get("state") == "NORMALIZED" and isinstance(d.get("input_id"), str)
            results["D2"] = "D2 NORMALIZED" if ok else fail_line("D2", st, b)
            d2_input = d.get("input_id") if ok else None
            if ok:
                inputs["D2"] = d2_input
            detail.append("D2 status=%s code=%s" % (st, code_of(b)))
            if code_of(b) == "NOT_AUTHORIZED":
                stop = "D2 answered NOT_AUTHORIZED: STOP"
        if not stop:
            st, b, raw = resolve("D3")
            d = b.get("data") if isinstance(b, dict) else None
            bodies["D3"] = raw
            pdate = (((d or {}).get("portfolio") or {}).get("options") or {}).get("price_date") if isinstance(d, dict) else None
            after = default_price_date(None)
            ok = st == 200 and is_answer(b) and d.get("state") == "NORMALIZED" and pdate in {before, after}
            results["D3"] = ("D3 NORMALIZED price_date=%s" % pdate) if ok else fail_line("D3", st, b)
            if is_answer(b) and d.get("state") == "NORMALIZED" and isinstance(d.get("input_id"), str):
                inputs["D3"] = d.get("input_id")
            detail.append("D3 status=%s code=%s price_date=%s expected_before=%s expected_after=%s" % (st, code_of(b), pdate, before, after))
            say("expected price date (New York prior trading day, lib/trading_calendar.py via default_price_date) before=%s after=%s" % (before, after))
            if code_of(b) == "NOT_AUTHORIZED":
                stop = "D3 answered NOT_AUTHORIZED: STOP"
        if not stop:
            st, b, raw = call("D4", base.door_body("D2", args.date))
            d = b.get("data") if isinstance(b, dict) else None
            ok = (st == 200 and is_answer(b) and d.get("state") == "NORMALIZED" and inputs.get("D2") is not None
                  and d.get("input_id") == inputs.get("D2"))
            results["D4"] = "D4 ACCEPTED" if ok else fail_line("D4", st, b)
            detail.append("D4 status=%s code=%s same_input=%s" % (st, code_of(b), ok))
        # C1: answers only
        c1 = "C1 NOT RUN no door arm answered"
        if bodies:
            notans = [k for k in ("D1", "D2", "D3") if k not in bodies or not is_answer(base.parsed(bodies[k]))]
            if notans:
                c1 = "C1 NOT RUN not an answer body: %s" % ",".join(notans)
            else:
                bun = base.find_bun()
                scratch = tempfile.mkdtemp(prefix="r28b_c1_")
                try:
                    commit, root = base.c1_prepare(scratch)
                    got = [base.c1_parse(bun, root, bodies[k]) for k in ("D1", "D2", "D3")]
                    say("C1 parseIrEnvelope from portal origin/PROD %s: %s" % (commit[:10], got))
                    c1 = "C1 PARSED 3 of 3 answers" if got == ["PARSED"] * 3 else "C1 FAIL %s" % got
                finally:
                    shutil.rmtree(scratch, ignore_errors=True)
        results["C1"] = c1
        bodies.clear()
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; the row is still removed after exp
        stop = stop or "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        tokens["IV"] = None
        if stop:
            say(str(stop))
        if written and exps:
            wait = max(exps) + 5 - time.time()
            if wait > 0:
                say("waiting %ds for exp %s to pass before removal" % (int(wait), base.iso(max(exps))))
                time.sleep(wait)
        for _ in written:
            try:
                ddb.delete_item(TableName=base.USERS, Key=key, ConditionExpression="attribute_exists(PK)")
                say("users row deleted (attribute_exists)")
            except Exception as e:  # noqa: BLE001
                say("DELETE of the row failed: %s" % str(e)[:160])
        rem = []
        deadline = time.time() + 300
        say("removal window: bounded 5 minutes, until %s" % base.iso(deadline))
        g = c = False
        while time.time() < deadline:
            c = cread() is None
            g = gsi() == 0
            say("removal read: GSI ABSENT=%s ConsistentRead ABSENT=%s" % (g, c))
            if g and c:
                break
            time.sleep(10)
        rem.append(("ABSENT GSI %s" if g else "PRESENT GSI %s") % addr)
        rem.append(("ABSENT CONSISTENT %s" if c else "PRESENT CONSISTENT %s") % addr)
        res = [results.get(arm) or "%s NOT RUN %s" % (arm, stop or "an earlier arm did not run") for arm in ("D1", "D2", "D3", "D4", "C1")]
        (outdir / "DOOR_RESULT.txt").write_text("\n".join(res) + "\n", encoding="utf-8")
        (outdir / "DOOR_REMOVAL.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        (outdir / "DOOR_TRACE.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (outdir / "DOOR_DETAIL.txt").write_text("\n".join(detail) + "\n", encoding="utf-8")
        (outdir / "DOOR_INPUTS.txt").write_text(
            "\n".join("%s tenant=49financial input_id=%s" % (k, v) for k, v in inputs.items()) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    addr = "irpt-r28-iv-%s@opal.invalid" % args.date
    if args.live and args.go:
        return live(addr, args)
    ap.error("choose --live --go")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
