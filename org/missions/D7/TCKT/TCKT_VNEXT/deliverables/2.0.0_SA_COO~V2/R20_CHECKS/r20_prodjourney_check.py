"""TCKT_VNEXT round 20 -- the FWD-11 JOURNEY ON PROD (run-pair AMENDMENT 8): the mechanical legs.

  python r20_prodjourney_check.py              the live check: the result document, the shots, the record of the deleted ticket, the ticket (ABSENT),
                                               both identity rows (ABSENT) and the live routing (restored)
  python r20_prodjourney_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (prodjourney) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the shots and the contrast (a judgment); this
check holds what the world can contradict: the synthetic ticket and both rows are gone, the routing is jeanette alone, the shots are PNGs of the recorded
size taken at the PROD origin by the right viewers, the page origin is PROD, Trade Request is absent from the type list, and the run never named Andrew's tickets.
"""
import json
import os
import subprocess
import sys

DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_prod2/"
RES = DIR + "R20_PROD2_RESULT.json"
RECORD = DIR + "R20_PROD2_TICKET_ITEM.json"
ORIGIN = "https://opalinvest.dev"
COORDINATOR = "jeanette@opalinvest.com"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
KEYS = {"browser_origin", "promote_proof", "filer", "coordinator_identity", "mt_ticket", "mt_confirmed_time", "routing_before", "routing_during",
        "routing_after", "type_options", "shots", "contrast_ratio", "fire_windows_answer", "row_deleted_at", "token_exp", "ticket_deleted_at",
        "ticket_absent_after", "rows_absent_after", "no_engine_call", "token_printed"}
SHOT_ROLES = ["prod_filer_waiting", "prod_coordinator_controls", "prod_filer_confirmed"]
PNG = b"\x89PNG\r\n\x1a\n"
FUNCTION = "opal-ticket-api"
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        return "token_printed or no_engine_call differs from the order"
    if doc["rows_absent_after"] is not True or doc["ticket_absent_after"] is not True:
        return "the rows and the ticket must read ABSENT after the removal"
    if not (str(doc["row_deleted_at"]) > str(doc["token_exp"]) and str(doc["ticket_deleted_at"]) > str(doc["token_exp"])):
        return "the removal happened before the last token exp"
    if doc["mt_ticket"] in PROTECTED:
        return "the run's ticket is one of Andrew's or the earlier synthetic ticket"
    ids = [doc["filer"], doc["coordinator_identity"]]
    if len(set(ids)) != 2 or any(not str(i).endswith("@opal.invalid") for i in ids):
        return "the filer and the coordinator must be two distinct synthetic @opal.invalid addresses"
    if not doc["promote_proof"] or not doc["fire_windows_answer"]:
        return "promote_proof and fire_windows_answer must be recorded"
    low = [str(o).lower().replace("_", " ") for o in (doc["type_options"] if isinstance(doc["type_options"], list) else [])]
    if not low:
        return "type_options must be the non-empty list of the New Ticket select's options"
    if any("trade request" in o for o in low):
        return "a Trade Request option is listed on PROD (Andrew's hold)"
    if not any("meeting request" in o for o in low):
        return "Meeting Request is not in the type list"
    try:
        if float(doc["contrast_ratio"]) < 4.5:
            return "the printed contrast %s is below 4.5:1" % doc["contrast_ratio"]
    except (TypeError, ValueError):
        return "contrast_ratio must be a number"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN or not rec.get("viewer"):
            return "shot %s lacks path, bytes, viewer or the PROD origin" % role
        if not str(rec["path"]).startswith(DIR):
            return "shot %s is saved outside %s" % (role, DIR)
    if shots["prod_filer_waiting"]["viewer"] != doc["filer"] or shots["prod_filer_confirmed"]["viewer"] != doc["filer"]:
        return "the two filer shots must be taken as the filer"
    if shots["prod_coordinator_controls"]["viewer"] != doc["coordinator_identity"]:
        return "the coordinator shot must be taken as the coordinator"
    for k, who in (("routing_before", COORDINATOR), ("routing_after", COORDINATOR), ("routing_during", doc["coordinator_identity"])):
        v = doc[k]
        if not isinstance(v, dict) or v.get("primary") != [who]:
            return "%s is not the sole primary %s" % (k, who)
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
    try:
        rec = json.load(open(RECORD, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD the deleted ticket's record cannot be read: %s" % e)
        return 1
    tid = (rec.get("ticket_id") or {}).get("S") if isinstance(rec.get("ticket_id"), dict) else rec.get("ticket_id")
    if tid != doc["mt_ticket"]:
        print("RUN-BAD the saved ticket record is not the run's ticket")
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
        if item("opal-tickets", {"ticket_id": {"S": doc["mt_ticket"]}}) is not None:
            print("RUN-BAD the synthetic ticket is still PRESENT")
            return 1
        for who in (doc["filer"], doc["coordinator_identity"]):
            if item("opal-users-v2", {"PK": {"S": "USER#" + who}, "SK": {"S": "PROFILE"}}) is not None:
                print("RUN-BAD an identity row is still PRESENT")
                return 1
        for keep in sorted(PROTECTED):
            if item("opal-tickets", {"ticket_id": {"S": keep}}) is None:
                print("RUN-BAD a protected ticket %s is no longer present" % keep)
                return 1
        cfg = aws("lambda", "get-function-configuration", "--function-name", FUNCTION)
        matrix = json.loads(((cfg.get("Environment") or {}).get("Variables") or {}).get("ROUTING_MATRIX") or "{}")
        if (matrix.get("meeting_request") or {}).get("primary") != [COORDINATOR]:
            print("RUN-BAD the live meeting_request routing primary is not restored to exactly the coordinator")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (prodjourney) filed, confirmed and read on %s; the synthetic ticket and both rows ABSENT; routing restored; the two protected tickets present" % ORIGIN)
    return 0


def good_doc():
    def shot(role, who):
        return {"path": DIR + role + ".png", "bytes": 1000, "viewer": who, "origin": ORIGIN}

    f, c = "pf@opal.invalid", "pc@opal.invalid"
    return {"browser_origin": ORIGIN, "promote_proof": "15bc21b3 carries 2a64d211", "filer": f, "coordinator_identity": c, "mt_ticket": "TCK-X",
            "mt_confirmed_time": "t", "routing_before": {"primary": [COORDINATOR]}, "routing_during": {"primary": [c]},
            "routing_after": {"primary": [COORDINATOR]}, "type_options": ["Service Request", "Meeting Request", "Other"],
            "shots": {"prod_filer_waiting": shot("prod_filer_waiting", f), "prod_coordinator_controls": shot("prod_coordinator_controls", c),
                      "prod_filer_confirmed": shot("prod_filer_confirmed", f)},
            "contrast_ratio": 10.1, "fire_windows_answer": "CTO and IB2: none open or due", "row_deleted_at": "2026-10-19T14:40:00Z",
            "token_exp": "2026-10-19T14:30:00Z", "ticket_deleted_at": "2026-10-19T14:41:00Z", "ticket_absent_after": True,
            "rows_absent_after": True, "no_engine_call": True, "token_printed": False}


def self_test():
    g = good_doc()
    if doc_problem(g) is not None:
        return "good document refused: %s" % doc_problem(g)
    muts = {
        "DEV origin": lambda d: d.update(browser_origin="http://localhost:5174"),
        "token printed": lambda d: d.update(token_printed=True),
        "ticket still present": lambda d: d.update(ticket_absent_after=False),
        "rows still present": lambda d: d.update(rows_absent_after=False),
        "ticket deleted before exp": lambda d: d.update(ticket_deleted_at="2026-10-19T14:00:00Z"),
        "row deleted before exp": lambda d: d.update(row_deleted_at="2026-10-19T14:00:00Z"),
        "andrew's ticket": lambda d: d.update(mt_ticket="TCK-20261017-5af976ff"),
        "earlier synthetic ticket": lambda d: d.update(mt_ticket="TCK-20261017-da2a1987"),
        "same identity twice": lambda d: d.update(coordinator_identity=d["filer"]),
        "real address": lambda d: d.update(filer="someone@opalinvest.com"),
        "trade request listed": lambda d: d["type_options"].append("Trade Request"),
        "meeting missing": lambda d: d.update(type_options=["Other"]),
        "low contrast": lambda d: d.update(contrast_ratio=1.25),
        "contrast not a number": lambda d: d.update(contrast_ratio="ten"),
        "two shots": lambda d: d["shots"].pop("prod_coordinator_controls"),
        "coordinator shot by filer": lambda d: d["shots"]["prod_coordinator_controls"].update(viewer=d["filer"]),
        "filer shot by coordinator": lambda d: d["shots"]["prod_filer_confirmed"].update(viewer=d["coordinator_identity"]),
        "shot at DEV origin": lambda d: d["shots"]["prod_filer_confirmed"].update(origin="http://localhost:5174"),
        "routing not restored": lambda d: d.update(routing_after={"primary": ["x@opal.invalid"]}),
        "window not the coordinator": lambda d: d.update(routing_during={"primary": [COORDINATOR]}),
        "no fire-window answer": lambda d: d.update(fire_windows_answer=""),
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
        print("R20-PRODJOURNEY-SELFTEST-OK" if why is None else "R20-PRODJOURNEY-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
