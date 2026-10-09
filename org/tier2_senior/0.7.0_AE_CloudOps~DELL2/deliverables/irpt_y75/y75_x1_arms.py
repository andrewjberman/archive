"""Y75 leg L4 / after-read 4 (X-1 actor): the test filer, ONE on-behalf template upload, and the refusal arms.

Shape taken from release 3's read 4 (TO-IB-yr-681 step 7), with every contract read out of the code
rather than remembered:
  route        reports/generate_installed.py:277 UPLOAD_ROUTE
  headers      _scope/resolve.py:104 TRUSTED_HEADERS, the nine names
  body fields  intake/uploads.py:102 required = {upload_token, filename, file_base64, file_type}
               and :103 optional; ANY other key refuses UPLOAD_FIELDS, so the body carries no extras
  token        intake/uploads.py:23 TOKEN = [A-Za-z0-9_-]{8,128}
  template     intake/template_reader.py:184 A1 in (ticker, symbol); :22 BASES for B1

No real email is printed. The advisor is identified only by its opaque adv- label, which is the
first 12 hex of sha256 of the lowercased email (the packet's own definition).
"""
import base64
import hashlib
import io
import json
import sys

import boto3

FIRM = "49financial"                      # F -- release 3's firm, so the write stays in its own tree
FILER = "irpt-y75-testfiler-20261009@opal.invalid"
FUNCTION = "irpt-ycharts-generate"
ROUTE = "POST /api/scoped/investor-reporting/analysis/inputs"
RAW_PATH = "/api/scoped/investor-reporting/analysis/inputs"
USERS = "opal-users-v2"
RUN = "y75x1-20261009"

CSV = b"Ticker,Dollars\nAAPL,10000\nMSFT,15000\n"   # 2 well-known listed tickers, as the order asks
BODY_SHA256 = hashlib.sha256(CSV).hexdigest()

ddb = boto3.client("dynamodb", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def adv(email):
    return "adv-" + hashlib.sha256(email.lower().encode()).hexdigest()[:12]


def put_filer():
    """The synthetic filer: OPAL_GLOBAL home, allowedFirmIds = [F], no login identity."""
    item = {
        "PK": {"S": "USER#" + FILER},
        "SK": {"S": "PROFILE"},
        "email": {"S": FILER},
        "firmId": {"S": "opal-capital"},
        "status": {"S": "active"},
        "userType": {"S": "service"},
        "name": {"S": "IRPT Y75 synthetic test filer"},
        "allowedFirmIds": {"L": [{"S": FIRM}]},
    }
    ddb.put_item(TableName=USERS, Item=item)
    back = ddb.get_item(TableName=USERS, Key={"PK": item["PK"], "SK": item["SK"]},
                        ConsistentRead=True).get("Item")
    return back is not None, sorted(back or {})


def event(advisor_email=None, tenant=FIRM, token=None, filer=FILER, firm_header="opal-capital"):
    headers = {
        "x-user-email": filer,
        "x-user-name": "IRPT Y75 synthetic test filer",
        "x-user-tier": "service",
        "x-user-role": "service",
        "x-firm-id": firm_header,
        "x-user-type": "service",
        "x-origin-verify": "cloudfront",
        # _authz/authz_dispatch.py:55-56,138 -- checked FIRST, before any scope work. Its absence
        # refused all four arms identically on the first attempt, which is why the arms are not
        # evidence until this is present.
        "x-contract-version": "v1",
    }
    qs = {"selected_tenant": tenant}
    if advisor_email is not None:
        qs["advisor_email"] = advisor_email
    body = {"upload_token": token, "filename": "y75_x1_template.csv",
            "file_base64": base64.b64encode(CSV).decode(), "file_type": "csv"}
    return {
        "version": "2.0", "routeKey": ROUTE, "rawPath": RAW_PATH,
        "headers": headers, "queryStringParameters": qs,
        "requestContext": {"http": {"method": "POST", "path": RAW_PATH}},
        "body": json.dumps(body), "isBase64Encoded": False,
    }


def invoke(ev):
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(ev).encode())
    raw = r["Payload"].read().decode("utf-8", "replace")
    try:
        out = json.loads(raw)
    except ValueError:
        return r.get("StatusCode"), r.get("FunctionError"), raw[:600], None
    inner = out
    if isinstance(out, dict) and isinstance(out.get("body"), str):
        try:
            inner = json.loads(out["body"])
        except ValueError:
            inner = out["body"]
    return r.get("StatusCode"), r.get("FunctionError"), out.get("statusCode") if isinstance(out, dict) else None, inner


def resolve_by_opaque(opaque, firm=None):
    """Find the email whose adv- label is `opaque`, scanning opal-users-v2.

    The caller passes the OPAQUE id, never an address: a real email given as a command-line
    argument would land in the session transcript, and the bounds say opaque ids only for real
    people. The address is used in memory to build the header and the query, and is never printed.
    """
    pg = ddb.get_paginator("scan")
    for page in pg.paginate(TableName=USERS):
        for it in page.get("Items", []):
            em = (it.get("email") or {}).get("S")
            if not em:
                continue
            if adv(em) == opaque and (firm is None or (it.get("firmId") or {}).get("S") == firm):
                return em
    return None


def main(argv):
    want = argv[1] if len(argv) > 1 else None
    if want is None:
        print("usage: y75_x1_arms.py <advisor_OPAQUE_id> [<unlisted_OPAQUE_id>]")
        return 2
    advisor = resolve_by_opaque(want, FIRM)
    if advisor is None:
        print("REFUSED: no active user in %s carries opaque id %s" % (FIRM, want))
        return 1
    unlisted = resolve_by_opaque(argv[2]) if len(argv) > 2 else None
    if len(argv) > 2 and unlisted is None:
        print("REFUSED: no user carries opaque id %s" % argv[2])
        return 1
    print("A opaque:", adv(advisor))
    if unlisted:
        print("U opaque:", adv(unlisted))
    print("body_sha256:", BODY_SHA256)
    ok, keys = put_filer()
    print("filer put + consistent get:", ok, "| item keys:", keys)
    print()

    res = {}
    # (4) the real on-behalf ADMIT
    tok4 = RUN + "-admit"
    sc, fe, http, ans = invoke(event(advisor_email=advisor, token=tok4))
    print("(4) ADMIT      lambda=%s err=%s http=%s" % (sc, fe, http))
    print("               answer:", json.dumps(ans)[:420])
    res["4"] = {"http": http, "answer": ans, "token": tok4}

    # (5) same filer, an advisor of another firm
    if unlisted:
        sc, fe, http, ans = invoke(event(advisor_email=unlisted, token=RUN + "-unlisted"))
        print("(5) UNLISTED   http=%s answer=%s" % (http, json.dumps(ans)[:240]))
        res["5"] = {"http": http, "answer": ans}

    # (6) tenant not on the filer's list
    sc, fe, http, ans = invoke(event(advisor_email=advisor, tenant="cottonwood", token=RUN + "-offlist"))
    print("(6) OFF-LIST   http=%s answer=%s" % (http, json.dumps(ans)[:240]))
    res["6"] = {"http": http, "answer": ans}

    # (7) ordinary own-firm upload, no advisor_email
    sc, fe, http, ans = invoke(event(advisor_email=None, tenant=FIRM, token=RUN + "-ownfirm"))
    print("(7) OWN-FIRM   http=%s answer=%s" % (http, json.dumps(ans)[:240]))
    res["7"] = {"http": http, "answer": ans}

    p = ("C:/Users/Test/AppData/Local/Temp/claude/C--dev-ajb-workspace/"
         "32a60855-c63b-4e98-b745-fa87f5d02864/scratchpad/y75_x1_result.json")
    with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"advisor_opaque": adv(advisor), "firm": FIRM, "body_sha256": BODY_SHA256,
                   "filer": FILER, "arms": res}, fh, indent=2, sort_keys=True)
    print()
    print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
