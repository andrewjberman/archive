"""TCKT_VNEXT round 21 -- the TRADE REQUEST ATTACHMENT READ-BACK ON PROD (cell R21-rv-1, the CTO's round-20 analysis, msg 11235): the mechanical legs.

  python r21_tradejourney_check.py              the live check: the result document, the saved ticket record, the shots, the ticket (ABSENT),
                                                the filer row (ABSENT), the filer row (ABSENT) and the residue object(s) (PRESENT, the CTO ruling msg 11005) and the two protected tickets (present)
  python r21_tradejourney_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (tradejourney) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the shots (a judgment); this
check holds what the world can contradict: the synthetic ticket, the filer row and the uploaded object are gone, the bytes read back equal the bytes
uploaded, the object sat under the firm's trade-form prefix, the shots are PNGs of the recorded size taken at the PROD origin by the filer, and the run
never named Andrew's tickets or called the trade engine.
"""
import json
import os
import re
import subprocess
import sys

DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r21_trade_prod/"
RES = DIR + "R21_TRADE_RESULT.json"
RECORD = DIR + "R21_TRADE_TICKET_ITEM.json"
ORIGIN = "https://opalinvest.dev"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
NOT_THIS_RUN = PROTECTED | {"TCK-20261019-c50b4967", "TCK-20261019-2d6d1a25", "TCK-20261019-b931d737", "TCK-20261019-814ee603"}
KEYS = {"browser_origin", "promote_proof", "filer", "firm", "ticket", "filename", "content_type", "size", "sha256_uploaded", "sha256_readback",
        "s3_bucket", "s3_key", "type_options", "shots", "fire_windows_answer", "token_exp", "row_deleted_at", "ticket_deleted_at",
        "residue", "ticket_absent_after", "object_left_present", "row_absent_after", "no_engine_call", "token_printed", "open_body_keys", "listener_before_press"}
SHOT_ROLES = ["prod_trade_form_filled", "prod_trade_filed"]
TYPES = {"application/pdf": ".pdf", "text/csv": ".csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx"}
PNG = b"\x89PNG\r\n\x1a\n"
SHA = re.compile(r"^[0-9a-f]{64}$")
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        return "token_printed or no_engine_call differs from the order"
    for k in ("ticket_absent_after", "row_absent_after", "object_left_present"):
        if doc[k] is not True:
            return "%s must read True after the removal" % k
    if not all(str(doc[k]) > str(doc["token_exp"]) for k in ("row_deleted_at", "ticket_deleted_at")):
        return "a removal happened before the token exp"
    if doc["ticket"] in NOT_THIS_RUN:
        return "the run's ticket is a protected ticket or one of the earlier synthetic tickets"
    if not isinstance(doc["open_body_keys"], list) or "url" not in doc["open_body_keys"]:
        return "the recorded Open body key names do not carry url"
    if doc["listener_before_press"] is not True:
        return "the response listener was not registered before the Open press"
    if not str(doc["filer"]).endswith("@opal.invalid"):
        return "the filer must be a synthetic @opal.invalid address"
    if not doc["promote_proof"] or not doc["fire_windows_answer"]:
        return "promote_proof and fire_windows_answer must be recorded"
    if not re.match(r"^[A-Za-z0-9_-]+$", str(doc["firm"])):
        return "the firm is not a plain firm id"
    if doc["s3_bucket"] != "opal-data-%s" % doc["firm"]:
        return "the bucket %r is not the firm's own bucket" % doc["s3_bucket"]
    if not str(doc["s3_key"]).startswith("portal/%s/state/ticket_attachments/trade-form/" % doc["firm"]) or str(doc["s3_key"]).endswith("/"):
        return "the object key is not under the firm's trade-form prefix"
    if TYPES.get(doc["content_type"]) is None or not str(doc["filename"]).lower().endswith(TYPES[doc["content_type"]]):
        return "the filename extension does not agree with the content type"
    if isinstance(doc["size"], bool) or not isinstance(doc["size"], int) or not (1 <= doc["size"] <= 1048576):
        return "the synthetic file must be 1 byte to 1 MiB"
    pfx = "portal/%s/state/ticket_attachments/trade-form/" % doc["firm"]
    res = doc["residue"]
    if not isinstance(res, list) or not res or any(not isinstance(r, dict) or set(r) != {"key", "version_id"} for r in res):
        return "residue must be a non-empty list of {key, version_id}: the objects left PRESENT (the CTO's ruling, msg 11005)"
    if any(not str(r["key"]).startswith(pfx) or str(r["key"]).endswith("/") or not str(r["version_id"]).strip() for r in res):
        return "a residue entry is outside the trade-form prefix or has no version id"
    if doc["s3_key"] not in [r["key"] for r in res]:
        return "the run's own object is not named in the residue"
    if not SHA.match(str(doc["sha256_uploaded"])) or doc["sha256_uploaded"] != doc["sha256_readback"]:
        return "the bytes read back are not the bytes uploaded"
    low = [str(o).lower().replace("_", " ") for o in (doc["type_options"] if isinstance(doc["type_options"], list) else [])]
    if not any("trade request" in o for o in low):
        return "Trade Request is not in the type list"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN or not rec.get("viewer"):
            return "shot %s lacks path, bytes, viewer or the PROD origin" % role
        if not str(rec["path"]).startswith(DIR):
            return "shot %s is saved outside %s" % (role, DIR)
        if rec["viewer"] != doc["filer"]:
            return "shot %s must be taken as the filer" % role
    return None


def aws(*args, empty_ok=False):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"], capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d %s" % (" ".join(args[:2]), out.returncode, out.stderr.strip()[-200:]))
    if not out.stdout.strip():
        if empty_ok:
            return None
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def item(table, key):
    out = aws("dynamodb", "get-item", "--table-name", table, "--key", json.dumps(key), "--consistent-read", empty_ok=True)
    return None if out is None else out.get("Item")


def object_present(bucket, key, version_id):
    """True/False from a head-object at the recorded version: only a 404 reads ABSENT; any other failure (403, network) raises, never reads absent."""
    out = subprocess.run([AWS, "s3api", "head-object", "--bucket", bucket, "--key", key, "--version-id", version_id, "--region", "us-east-1"], capture_output=True, text=True, timeout=120)
    if out.returncode == 0:
        return True
    if "404" in out.stderr or "Not Found" in out.stderr:
        return False
    raise RuntimeError("head-object failed without a 404: %s" % out.stderr.strip()[-200:])


def live():
    try:
        doc = json.load(open(RES, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD cannot read the result file: %s" % e)
        return 1
    why = doc_problem(doc)
    if why:
        print("RUN-BAD %s" % why)
        return 1
    try:
        rec = json.load(open(RECORD, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD the deleted ticket's record cannot be read: %s" % e)
        return 1
    flat = json.dumps(rec)
    if (rec.get("ticket_id") or {}).get("S") != doc["ticket"] and rec.get("ticket_id") != doc["ticket"]:
        print("RUN-BAD the saved ticket record is not the run's ticket")
        return 1
    if "trade_request" not in flat or doc["s3_key"] not in flat:
        print("RUN-BAD the saved ticket record is not a trade_request carrying the uploaded object's key")
        return 1
    for role, s in doc["shots"].items():
        try:
            data = open(s["path"], "rb").read()
        except OSError as e:
            print("RUN-BAD shot %s cannot be read: %s" % (role, e))
            return 1
        if not data.startswith(PNG) or len(data) != int(s["bytes"]):
            print("RUN-BAD shot %s is not a PNG of the recorded size" % role)
            return 1
    try:
        if item("opal-tickets", {"ticket_id": {"S": doc["ticket"]}}) is not None:
            print("RUN-BAD the synthetic ticket is still PRESENT")
            return 1
        if item("opal-users-v2", {"PK": {"S": "USER#" + doc["filer"]}, "SK": {"S": "PROFILE"}}) is not None:
            print("RUN-BAD the filer row is still PRESENT")
            return 1
        for r in doc["residue"]:
            if not object_present(doc["s3_bucket"], r["key"], r["version_id"]):
                print("RUN-BAD a residue object is not PRESENT at its recorded version")
                return 1
        for keep in sorted(PROTECTED):
            if item("opal-tickets", {"ticket_id": {"S": keep}}) is None:
                print("RUN-BAD a protected ticket %s is no longer present" % keep)
                return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (tradejourney) Trade Request filed with one attachment on %s and the bytes read back equal; the synthetic ticket and the filer row ABSENT; the residue object(s) PRESENT at the recorded version; the protected tickets present" % ORIGIN)
    return 0


def good_doc():
    def shot(role):
        return {"path": DIR + role + ".png", "bytes": 1000, "viewer": "tf@opal.invalid", "origin": ORIGIN}

    return {"browser_origin": ORIGIN, "promote_proof": "8cd45f62 carries 2a64d211", "filer": "tf@opal.invalid", "firm": "cottonwood", "ticket": "TCK-X",
            "filename": "synthetic.csv", "content_type": "text/csv", "size": 8, "sha256_uploaded": "a" * 64, "sha256_readback": "a" * 64,
            "s3_bucket": "opal-data-cottonwood", "s3_key": "portal/cottonwood/state/ticket_attachments/trade-form/x/synthetic.csv",
            "type_options": ["Trade Request", "Service Request", "Meeting Request", "Other"],
            "shots": {"prod_trade_form_filled": shot("prod_trade_form_filled"), "prod_trade_filed": shot("prod_trade_filed")},
            "fire_windows_answer": "CTO, IB2 and Y2: none open or due", "token_exp": "2026-10-19T20:30:00Z", "row_deleted_at": "2026-10-19T20:40:00Z",
            "ticket_deleted_at": "2026-10-19T20:41:00Z", "residue": [{"key": "portal/cottonwood/state/ticket_attachments/trade-form/x/synthetic.csv", "version_id": "v1"}],
            "ticket_absent_after": True, "object_left_present": True, "open_body_keys": ["expires_in", "filename", "url"], "listener_before_press": True, "row_absent_after": True, "no_engine_call": True, "token_printed": False}


def self_test():
    g = good_doc()
    if doc_problem(g) is not None:
        return "good document refused: %s" % doc_problem(g)
    muts = {
        "DEV origin": lambda d: d.update(browser_origin="http://localhost:5174"),
        "token printed": lambda d: d.update(token_printed=True),
        "engine called": lambda d: d.update(no_engine_call=False),
        "ticket still present": lambda d: d.update(ticket_absent_after=False),
        "object not left present": lambda d: d.update(object_left_present=False),
        "no residue": lambda d: d.update(residue=[]),
        "residue lacks the run's key": lambda d: d.update(residue=[{"key": "portal/cottonwood/state/ticket_attachments/trade-form/y/o.csv", "version_id": "v"}]),
        "residue outside the prefix": lambda d: d["residue"].append({"key": "portal/cottonwood/state/other/o.csv", "version_id": "v"}),
        "residue without a version": lambda d: d["residue"][0].update(version_id=" "),
        "row still present": lambda d: d.update(row_absent_after=False),
        "ticket deleted before exp": lambda d: d.update(ticket_deleted_at="2026-10-19T20:00:00Z"),
        "row deleted before exp": lambda d: d.update(row_deleted_at="2026-10-19T20:00:00Z"),
        "andrew's ticket": lambda d: d.update(ticket="TCK-20261017-5af976ff"),
        "the meeting run's ticket": lambda d: d.update(ticket="TCK-20261019-c50b4967"),
        "a round-20 trade ticket": lambda d: d.update(ticket="TCK-20261019-814ee603"),
        "open body without url": lambda d: d.update(open_body_keys=["expires_in", "filename"]),
        "listener after the press": lambda d: d.update(listener_before_press=False),
        "real filer": lambda d: d.update(filer="someone@opalinvest.com"),
        "bad firm": lambda d: d.update(firm="a/b"),
        "other firm's bucket": lambda d: d.update(s3_bucket="opal-data-other"),
        "key outside the prefix": lambda d: d.update(s3_key="portal/cottonwood/state/other/x.csv"),
        "key is the prefix": lambda d: d.update(s3_key="portal/cottonwood/state/ticket_attachments/trade-form/"),
        "extension disagrees": lambda d: d.update(filename="synthetic.pdf"),
        "type refused by the door": lambda d: d.update(content_type="text/plain", filename="s.txt"),
        "empty file": lambda d: d.update(size=0),
        "file too large": lambda d: d.update(size=20000000),
        "bytes differ": lambda d: d.update(sha256_readback="b" * 64),
        "hash malformed": lambda d: d.update(sha256_uploaded="zz", sha256_readback="zz"),
        "trade request not listed": lambda d: d.update(type_options=["Meeting Request", "Other"]),
        "one shot": lambda d: d["shots"].pop("prod_trade_filed"),
        "shot by another viewer": lambda d: d["shots"]["prod_trade_filed"].update(viewer="x@opal.invalid"),
        "shot at DEV origin": lambda d: d["shots"]["prod_trade_filed"].update(origin="http://localhost:5174"),
        "no fire-window answer": lambda d: d.update(fire_windows_answer=""),
        "missing key": lambda d: d.pop("ticket"),
    }
    for name, mut in muts.items():
        d = json.loads(json.dumps(g))
        mut(d)
        if doc_problem(d) is None:
            return "mutant not caught: %s" % name
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = self_test()
        print("R21-TRADEJOURNEY-SELFTEST-OK" if why is None else "R21-TRADEJOURNEY-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
