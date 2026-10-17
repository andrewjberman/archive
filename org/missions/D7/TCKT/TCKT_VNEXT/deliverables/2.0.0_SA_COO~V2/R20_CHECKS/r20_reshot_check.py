"""TCKT_VNEXT round 20 -- the FWD-11 RE-SHOT on the fixed DEV build (run-pair AMENDMENT 6, after the contrast fix of row TCKT_VNEXT-D2-S59): the mechanical legs.

  python r20_reshot_check.py              the live check: the result document, the saved shot, the ticket, the identity row
  python r20_reshot_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (reshot) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the shot (a judgment) and the issuer measures its
contrast from the pixels; this check holds what the world can contradict: the ticket still reads confirmed and completed, the one identity row is ABSENT, the
shot is a PNG of the recorded size taken by the filer at the DEV origin, the served sha is the one the order names.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_reshot/R20_RESHOT_RESULT.json"
SHOTS_DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_reshot/"
ORIGIN = "http://localhost:5174"
KEYS = {"browser_origin", "dev_sha", "filer", "mt_ticket", "shots", "row_deleted_at", "token_exp", "row_absent_after", "no_engine_call", "token_printed"}
SHOT_ROLES = ["filer_completed"]
PNG = b"\x89PNG\r\n\x1a\n"
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        return "token_printed or no_engine_call differs from the order"
    if doc["row_absent_after"] is not True or str(doc["row_deleted_at"]) <= str(doc["token_exp"]):
        return "the identity row was not deleted after exp and read absent"
    if not str(doc["filer"]).endswith("@opal.invalid"):
        return "the filer must be a synthetic @opal.invalid address"
    sha = str(doc["dev_sha"])
    if len(sha) < 12 or any(c not in "0123456789abcdef" for c in sha):
        return "dev_sha must be a hex sha of at least 12 characters"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the role %s" % SHOT_ROLES
    rec = shots["filer_completed"]
    if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN or rec.get("viewer") != doc["filer"]:
        return "the shot lacks path, bytes, the DEV origin or the filer as viewer"
    if not str(rec["path"]).startswith(SHOTS_DIR):
        return "the shot is saved outside %s" % SHOTS_DIR
    return None


def aws(*args, empty_ok=False):
    out = subprocess.run([AWS] + list(args) + ["--region", "us-east-1", "--output", "json"],
                         capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("aws %s rc=%d" % (" ".join(args[:2]), out.returncode))
    if not out.stdout.strip():
        if empty_ok:
            return None
        raise RuntimeError("aws %s printed nothing" % " ".join(args[:2]))
    return json.loads(out.stdout)


def item(table, key):
    out = aws("dynamodb", "get-item", "--table-name", table, "--key", json.dumps(key), "--consistent-read", empty_ok=True)
    return None if out is None else out.get("Item")


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
    rec = doc["shots"]["filer_completed"]
    try:
        data = open(rec["path"], "rb").read()
    except OSError as e:
        print("RUN-BAD the shot cannot be read: %s" % e)
        return 1
    if not data.startswith(PNG) or len(data) != int(rec["bytes"]):
        print("RUN-BAD the shot is not a PNG of the recorded size")
        return 1
    try:
        mt = item("opal-tickets", {"ticket_id": {"S": doc["mt_ticket"]}})
        if not mt or mt.get("ticket_type", {}).get("S") != "meeting_request":
            print("RUN-BAD the meeting ticket is missing or not a meeting_request")
            return 1
        meeting = mt.get("meeting", {}).get("M")
        if not meeting or meeting.get("status", {}).get("S") != "confirmed":
            print("RUN-BAD the ticket carries no confirmed meeting outcome")
            return 1
        if mt.get("status", {}).get("S") != "completed":
            print("RUN-BAD the ticket is not completed")
            return 1
        if item("opal-users-v2", {"PK": {"S": "USER#" + doc["filer"]}, "SK": {"S": "PROFILE"}}) is not None:
            print("RUN-BAD the filer row is still PRESENT")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (reshot) the completed confirmed ticket was read on %s at DEV %s, one shot saved as PNG, the filer row absent" % (ORIGIN, doc["dev_sha"][:12]))
    return 0


def good_doc():
    return {"browser_origin": ORIGIN, "dev_sha": "539b1ee70ba1b2a9b0c562a9169d9fcca1b7c18e", "filer": "f@opal.invalid", "mt_ticket": "TCK-1",
            "shots": {"filer_completed": {"path": SHOTS_DIR + "filer_completed.png", "bytes": 1000, "viewer": "f@opal.invalid", "origin": ORIGIN}},
            "row_deleted_at": "2026-10-17T10:00:00Z", "token_exp": "2026-10-17T09:30:00Z", "row_absent_after": True, "no_engine_call": True, "token_printed": False}


def self_test():
    g = good_doc()
    if doc_problem(g) is not None:
        return "good document refused: %s" % doc_problem(g)
    muts = {
        "PROD origin": lambda d: d.update(browser_origin="https://opalinvest.dev"),
        "another port": lambda d: d.update(browser_origin="http://localhost:5199"),
        "token printed": lambda d: d.update(token_printed=True),
        "row deleted before exp": lambda d: d.update(row_deleted_at="2026-10-17T09:00:00Z"),
        "no shot": lambda d: d["shots"].pop("filer_completed"),
        "two shots": lambda d: d["shots"].update(extra=dict(d["shots"]["filer_completed"])),
        "shot by another viewer": lambda d: d["shots"]["filer_completed"].update(viewer="x@opal.invalid"),
        "shot at another origin": lambda d: d["shots"]["filer_completed"].update(origin="https://opalinvest.dev"),
        "shot outside the dir": lambda d: d["shots"]["filer_completed"].update(path="C:/tmp/x.png"),
        "short sha": lambda d: d.update(dev_sha="539b1ee"),
        "non-hex sha": lambda d: d.update(dev_sha="zzzzzzzzzzzzzz"),
        "real address": lambda d: d.update(filer="someone@opalinvest.com"),
        "missing key": lambda d: d.pop("mt_ticket"),
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
        print("R20-RESHOT-SELFTEST-OK" if why is None else "R20-RESHOT-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
