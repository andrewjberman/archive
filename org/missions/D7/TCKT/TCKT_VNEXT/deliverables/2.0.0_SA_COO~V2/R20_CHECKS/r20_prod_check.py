"""TCKT_VNEXT round 20 -- the FWD-11 PROD leg (run-pair AMENDMENT 6 draft, R20_RV/R20_PROD_LEG_AMENDMENT_DRAFT.md): the mechanical legs only.

  python r20_prod_check.py              the live check: the result document, the two saved shots, the ticket, the identity row
  python r20_prod_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (prod) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the two shots (a judgment); this
check holds what the world can contradict: the ticket still reads confirmed and completed, the one identity row is ABSENT, each shot is a PNG of
the recorded size, the page origin is the PROD site, the New Ticket type list carries Meeting Request and NOT Trade Request (Andrew's hold).
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/R20_PROD_RESULT.json"
SHOTS_DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod/"
ORIGIN = "https://opalinvest.dev"
KEYS = {"browser_origin", "promote_proof", "filer", "mt_ticket", "type_options", "shots", "row_deleted_at", "token_exp",
        "row_absent_after", "no_engine_call", "token_printed"}
SHOT_ROLES = ["prod_filer_completed", "prod_meeting_form"]
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
    if not doc["promote_proof"]:
        return "no proof that the re-cut is promoted"
    opts = doc["type_options"]
    if not isinstance(opts, list) or not opts:
        return "type_options must be the non-empty list of the New Ticket select's options"
    low = [str(o).lower().replace("_", " ") for o in opts]
    if any("trade request" in o for o in low):
        return "a Trade Request option is listed on PROD (Andrew's hold)"
    if not any("meeting request" in o for o in low):
        return "Meeting Request is not in the type list"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the two roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN \
                or rec.get("viewer") != doc["filer"]:
            return "shot %s lacks path, bytes, the PROD origin or the filer as viewer" % role
        if not str(rec["path"]).startswith(SHOTS_DIR):
            return "shot %s is saved outside %s" % (role, SHOTS_DIR)
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
    for role, rec in doc["shots"].items():
        try:
            data = open(rec["path"], "rb").read()
        except OSError as e:
            print("RUN-BAD shot %s cannot be read: %s" % (role, e))
            return 1
        if not data.startswith(PNG) or len(data) != int(rec["bytes"]):
            print("RUN-BAD shot %s is not a PNG of the recorded size" % role)
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
    print("RUN-OK (prod) the completed confirmed ticket was read on %s, two shots saved as PNG, Trade Request absent from the type list, the filer row absent" % ORIGIN)
    return 0


def good_doc():
    def shot(role):
        return {"path": SHOTS_DIR + role + ".png", "bytes": 1000, "viewer": "f@opal.invalid", "origin": ORIGIN}

    return {"browser_origin": ORIGIN, "promote_proof": "4e1e35bf is an ancestor of origin/PROD", "filer": "f@opal.invalid",
            "mt_ticket": "TCK-1", "type_options": ["Analysis Request", "Meeting Request", "Other"],
            "shots": {r: shot(r) for r in SHOT_ROLES}, "row_deleted_at": "2026-10-17T05:00:00Z", "token_exp": "2026-10-17T04:30:00Z",
            "row_absent_after": True, "no_engine_call": True, "token_printed": False}


def self_test():
    g = good_doc()
    if doc_problem(g) is not None:
        return "good document refused: %s" % doc_problem(g)
    muts = {
        "DEV origin": lambda d: d.update(browser_origin="http://localhost:5174"),
        "trade request listed": lambda d: d["type_options"].append("Trade Request"),
        "trade_request listed": lambda d: d["type_options"].append("trade_request"),
        "meeting missing": lambda d: d.update(type_options=["Analysis Request"]),
        "empty options": lambda d: d.update(type_options=[]),
        "no promote proof": lambda d: d.update(promote_proof=""),
        "token printed": lambda d: d.update(token_printed=True),
        "row deleted before exp": lambda d: d.update(row_deleted_at="2026-10-17T04:00:00Z"),
        "one shot": lambda d: d["shots"].pop("prod_meeting_form"),
        "shot by another viewer": lambda d: d["shots"]["prod_filer_completed"].update(viewer="x@opal.invalid"),
        "shot at DEV origin": lambda d: d["shots"]["prod_filer_completed"].update(origin="http://localhost:5174"),
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
        print("R20-PROD-SELFTEST-OK" if why is None else "R20-PROD-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
