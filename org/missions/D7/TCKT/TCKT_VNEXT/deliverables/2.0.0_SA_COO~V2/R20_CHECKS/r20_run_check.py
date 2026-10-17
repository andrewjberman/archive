"""TCKT_VNEXT round 20 -- R20-rv-3 (PART 3, FWD-11): the filer's RENDERED read of one meeting ticket after the confirm and after completion,
re-read by an identity that did not write it. The MECHANICAL legs only; the screenshots are graded by the CVO (R20RV-AC1J, a judgment).

  python r20_run_check.py              the live check: the result file, the ticket, the identity rows, the routing, the six saved shots
  python r20_run_check.py --self-test  the offline document scan on a good and several bad documents (no AWS)

Prints RUN-OK (render) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). Every claim in the applier's result file
that the world can contradict is re-read: the ticket from the table, the three identity rows, the live routing, and each shot's file.
"""
import json
import os
import subprocess
import sys

RES = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/R20_RUN_RESULT.json"
SHOTS_DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_run/"
COORDINATOR = "jeanette@opalinvest.com"
ORIGIN = "http://localhost:5174"
KEYS = {"browser_origin", "dev_sha", "filer", "coordinator_identity", "bystander", "mt_ticket", "mt_confirmed_time", "completed_by",
        "routing_before", "routing_during", "routing_after", "shots", "row_deleted_at", "token_exp", "rows_absent_after",
        "no_engine_call", "token_printed"}
# the six shots of the run pair's AMENDMENT 5, by role
SHOT_ROLES = ["filer_waiting", "filer_confirmed", "coordinator_controls", "bystander_no_control", "filer_completed", "meeting_form"]
PNG = b"\x89PNG\r\n\x1a\n"
FUNCTION = "opal-ticket-api"
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    """Offline scan of the result document; None when it is well formed."""
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        return "token_printed or no_engine_call differs from the order"
    if doc["rows_absent_after"] is not True or str(doc["row_deleted_at"]) <= str(doc["token_exp"]):
        return "the identity rows were not deleted after the last exp and read absent"
    ids = [doc["filer"], doc["coordinator_identity"], doc["bystander"]]
    if len(set(ids)) != 3 or any(not str(i).endswith("@opal.invalid") for i in ids):
        return "the three identities must be distinct synthetic @opal.invalid addresses"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the six roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or not rec.get("viewer") or not rec.get("origin"):
            return "shot %s lacks path, bytes, viewer or origin" % role
        if rec["origin"] != ORIGIN:
            return "shot %s was taken at origin %r" % (role, rec["origin"])
        if not str(rec["path"]).startswith(SHOTS_DIR):
            return "shot %s is saved outside %s" % (role, SHOTS_DIR)
    if shots["filer_waiting"]["viewer"] != doc["filer"] or shots["filer_confirmed"]["viewer"] != doc["filer"] \
            or shots["filer_completed"]["viewer"] != doc["filer"]:
        return "the three filer shots must be taken as the filer"
    if shots["bystander_no_control"]["viewer"] != doc["bystander"]:
        return "the bystander shot must be taken as the bystander"
    if shots["coordinator_controls"]["viewer"] != doc["coordinator_identity"]:
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
        if (not meeting or meeting.get("status", {}).get("S") != "confirmed"
                or meeting.get("by", {}).get("S") != doc["coordinator_identity"]
                or meeting.get("time", {}).get("S") != doc["mt_confirmed_time"]):
            print("RUN-BAD the ticket carries no confirmation by the recorded coordinator identity at the recorded time")
            return 1
        if mt.get("status", {}).get("S") != "completed":
            print("RUN-BAD the ticket is not completed (shot 5 reads a completed ticket)")
            return 1
        for who in (doc["filer"], doc["coordinator_identity"], doc["bystander"]):
            if item("opal-users-v2", {"PK": {"S": "USER#" + who}, "SK": {"S": "PROFILE"}}) is not None:
                print("RUN-BAD an identity row is still PRESENT")
                return 1
        cfg = aws("lambda", "get-function-configuration", "--function-name", FUNCTION)
        matrix = json.loads(((cfg.get("Environment") or {}).get("Variables") or {}).get("ROUTING_MATRIX") or "{}")
        if (matrix.get("meeting_request") or {}).get("primary") != [COORDINATOR]:
            print("RUN-BAD the live meeting_request routing primary is not restored to exactly the coordinator")
            return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (render) ticket confirmed then completed, six shots saved as PNG, three identity rows absent, routing restored")
    return 0


def good_doc():
    def shot(role, who):
        return {"path": SHOTS_DIR + role + ".png", "bytes": 1000, "viewer": who, "origin": ORIGIN}

    f, c, b = "f@opal.invalid", "c@opal.invalid", "b@opal.invalid"
    return {"browser_origin": ORIGIN, "dev_sha": "6cdd0bfd917b", "filer": f, "coordinator_identity": c, "bystander": b,
            "mt_ticket": "TCK-1", "mt_confirmed_time": "t", "completed_by": f,
            "routing_before": {"primary": [COORDINATOR]}, "routing_during": {"primary": [c]}, "routing_after": {"primary": [COORDINATOR]},
            "shots": {"filer_waiting": shot("filer_waiting", f), "filer_confirmed": shot("filer_confirmed", f),
                      "coordinator_controls": shot("coordinator_controls", c), "bystander_no_control": shot("bystander_no_control", b),
                      "filer_completed": shot("filer_completed", f), "meeting_form": shot("meeting_form", f)},
            "row_deleted_at": "2026-10-17T01:00:00Z", "token_exp": "2026-10-17T00:30:00Z", "rows_absent_after": True,
            "no_engine_call": True, "token_printed": False}


def self_test():
    g = good_doc()
    if doc_problem(g) is not None:
        return "good document refused: %s" % doc_problem(g)
    muts = {
        "wrong origin": lambda d: d.update(browser_origin="http://localhost:5173"),
        "token printed": lambda d: d.update(token_printed=True),
        "row deleted before exp": lambda d: d.update(row_deleted_at="2026-10-17T00:00:00Z"),
        "five shots": lambda d: d["shots"].pop("filer_completed"),
        "bystander shot by filer": lambda d: d["shots"]["bystander_no_control"].update(viewer=d["filer"]),
        "completed shot by coordinator": lambda d: d["shots"]["filer_completed"].update(viewer=d["coordinator_identity"]),
        "shot at another origin": lambda d: d["shots"]["meeting_form"].update(origin="http://localhost:5199"),
        "shot outside the dir": lambda d: d["shots"]["meeting_form"].update(path="C:/tmp/x.png"),
        "routing not restored": lambda d: d.update(routing_after={"primary": ["x@opal.invalid"]}),
        "real address as identity": lambda d: d.update(filer="someone@opalinvest.com"),
        "missing key": lambda d: d.pop("dev_sha"),
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
        print("R20-RUN-SELFTEST-OK" if why is None else "R20-RUN-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    return live()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
