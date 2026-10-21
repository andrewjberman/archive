"""TCKT_VNEXT round 23 -- FWD-4 ON DEV (cell R23-f4-1, the CTO's ruling msg 11766): one Opal sign-in files a ticket, claims it and completes it.

  python r23_fwd4_check.py              the live check: the result document, the saved ticket record, the shots, the ticket (ABSENT), the filer row (ABSENT)
  python r23_fwd4_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (fwd4) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the shots (a judgment); this check holds what
the world can contradict: the saved ticket record names ONE address as filer, assignee and the actor of the created, claimed and completed events, the
ticket and the filer row are gone, and the run never named a protected ticket or called the trade engine.
"""
import copy
import json
import os
import re
import subprocess
import sys

DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r23_fwd4_dev/"
RES = DIR + "R23_FWD4_RESULT.json"
RECORD = DIR + "R23_FWD4_TICKET_ITEM.json"
ORIGIN = "http://localhost:5174"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
KEYS = {"browser_origin", "filer", "firm", "ticket", "ticket_type", "claim_via", "complete_via", "shots", "token_exp", "row_deleted_at",
        "ticket_deleted_at", "ticket_absent_after", "row_absent_after", "no_engine_call", "token_printed"}
SHOT_ROLES = ["r23_form_filled", "r23_filed", "r23_claimed", "r23_completed"]
PNG = b"\x89PNG\r\n\x1a\n"
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not the one DEV origin %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True:
        return "token_printed or no_engine_call differs from the order"
    for k in ("ticket_absent_after", "row_absent_after"):
        if doc[k] is not True:
            return "%s must read True after the removal" % k
    if not all(str(doc[k]) > str(doc["token_exp"]) for k in ("row_deleted_at", "ticket_deleted_at")):
        return "a removal happened before the token exp"
    if doc["ticket"] in PROTECTED:
        return "the run's ticket is a protected ticket"
    if not re.match(r"^TCK-\d{8}-[0-9a-f]{8}$", str(doc["ticket"])):
        return "the ticket id is not a ticket id"
    if doc["ticket_type"] == "analysis_request":
        return "the ticket must be of a type other than an Analysis Request"
    if not str(doc["filer"]).endswith("@opal.invalid") or doc["filer"] != str(doc["filer"]).lower():
        return "the filer must be a lower-case synthetic @opal.invalid address"
    if doc["claim_via"] not in ("page", "direct") or doc["complete_via"] not in ("page", "direct"):
        return "claim_via and complete_via must each read page or direct"
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN or not rec.get("viewer"):
            return "shot %s lacks path, bytes, viewer or the DEV origin" % role
        if not str(rec["path"]).startswith(DIR):
            return "shot %s is saved outside %s" % (role, DIR)
        if rec["viewer"] != doc["filer"]:
            return "shot %s must be taken as the filer" % role
    return None


def record_problem(rec, doc):
    """rec = the ticket as `aws dynamodb get-item` printed it, saved whole BEFORE the delete."""
    it = rec.get("Item") if isinstance(rec, dict) else None
    if not isinstance(it, dict):
        return "the saved ticket record has no Item"
    try:
        who = doc["filer"]
        if it["ticket_id"]["S"] != doc["ticket"]:
            return "the saved record is another ticket"
        if it["ticket_type"]["S"] != doc["ticket_type"]:
            return "the saved record's type differs from the document"
        if it["status"]["S"] != "completed":
            return "the saved ticket is %r, not completed" % it["status"]["S"]
        if it["requester"]["M"]["email"]["S"].lower() != who:
            return "the requester is not the filer"
        if it["assignee"]["S"].lower() != who:
            return "the assignee (the claimer) is not the filer"
        acts = [(e["M"]["action"]["S"], e["M"]["actor"]["S"].lower()) for e in it["events"]["L"]]
        if [a for a, _ in acts] != ["created", "claimed", "completed"]:
            return "the events are %s, not created, claimed, completed" % [a for a, _ in acts]
        if any(w != who for _, w in acts):
            return "an event actor is not the filer: %s" % acts
        for field in ("claimed_by", "completed_by"):
            snap = it.get(field, {}).get("M", {})
            if snap.get("email", {}).get("S", who).lower() != who:
                return "%s names another address" % field
        if not it.get("claimed_at", {}).get("S") or not it.get("completed_at", {}).get("S"):
            return "claimed_at or completed_at is absent"
    except (KeyError, TypeError, AttributeError) as e:
        return "the saved record does not carry the expected shape: %r" % (e,)
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


def live():
    try:
        doc = json.load(open(RES, encoding="utf-8"))
        rec = json.load(open(RECORD, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print("RUN-BAD cannot read the result file or the saved ticket record: %s" % e)
        return 1
    p = doc_problem(doc) or record_problem(rec, doc)
    if p:
        print("RUN-BAD %s" % p)
        return 1
    try:
        for role, s in doc["shots"].items():
            raw = open(s["path"], "rb").read()
            if not raw.startswith(PNG) or len(raw) != s["bytes"]:
                print("RUN-BAD shot %s is not a PNG of the recorded size" % role)
                return 1
        if item("opal-tickets", {"ticket_id": {"S": doc["ticket"]}}) is not None:
            print("RUN-BAD the synthetic ticket is still PRESENT")
            return 1
        if item("opal-users-v2", {"PK": {"S": "USER#" + doc["filer"]}, "SK": {"S": "PROFILE"}}) is not None:
            print("RUN-BAD the filer row is still PRESENT")
            return 1
        for t in sorted(PROTECTED):
            if item("opal-tickets", {"ticket_id": {"S": t}}) is None:
                print("RUN-BAD protected ticket %s is not present" % t)
                return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (fwd4) %s filed, claimed and completed %s (%s) by one address, claim via %s and complete via %s; the ticket and the filer row ABSENT; the protected tickets present"
          % (doc["filer"], doc["ticket"], doc["ticket_type"], doc["claim_via"], doc["complete_via"]))
    return 0


def _good():
    who = "tckt-r23-filer-20261021@opal.invalid"
    shots = {r: {"path": DIR + r + ".png", "bytes": 10, "origin": ORIGIN, "viewer": who} for r in SHOT_ROLES}
    doc = {"browser_origin": ORIGIN, "filer": who, "firm": "cottonwood", "ticket": "TCK-20261021-0123abcd", "ticket_type": "service_request",
           "claim_via": "page", "complete_via": "page", "shots": shots, "token_exp": "2026-10-21T04:00:00Z", "row_deleted_at": "2026-10-21T04:05:00Z",
           "ticket_deleted_at": "2026-10-21T04:05:30Z", "ticket_absent_after": True, "row_absent_after": True, "no_engine_call": True, "token_printed": False}

    def s(v):
        return {"S": v}

    def ev(a):
        return {"M": {"ts": s("t"), "actor": s(who), "action": s(a)}}

    rec = {"Item": {"ticket_id": s(doc["ticket"]), "ticket_type": s("service_request"), "status": s("completed"),
                    "requester": {"M": {"email": s(who)}}, "assignee": s(who),
                    "events": {"L": [ev("created"), ev("claimed"), ev("completed")]},
                    "claimed_by": {"M": {"email": s(who)}}, "completed_by": {"M": {"email": s(who)}},
                    "claimed_at": s("t1"), "completed_at": s("t2")}}
    return doc, rec


def self_test():
    doc, rec = _good()
    if doc_problem(doc) or record_problem(rec, doc):
        print("RUN-BAD the good document did not pass: %s" % (doc_problem(doc) or record_problem(rec, doc)))
        return 1
    bad = 0

    def must_fail(name, d, r):
        nonlocal bad
        if not (doc_problem(d) or record_problem(r, d)):
            print("RUN-BAD mutant %s was not caught" % name)
            bad += 1

    def mutate(name, fd=None, fr=None):
        d, r = copy.deepcopy(doc), copy.deepcopy(rec)
        if fd:
            fd(d)
        if fr:
            fr(r)
        must_fail(name, d, r)

    mutate("origin", lambda d: d.update(browser_origin="https://opalinvest.dev"))
    mutate("token printed", lambda d: d.update(token_printed=True))
    mutate("ticket still present", lambda d: d.update(ticket_absent_after=False))
    mutate("row removed before exp", lambda d: d.update(row_deleted_at="2026-10-21T03:00:00Z"))
    mutate("protected ticket", lambda d: d.update(ticket="TCK-20261017-da2a1987"))
    mutate("analysis type", lambda d: d.update(ticket_type="analysis_request"))
    mutate("real address", lambda d: d.update(filer="alyssa@opalinvest.com"))
    mutate("missing shot", lambda d: d["shots"].pop("r23_completed"))
    mutate("shot as another viewer", lambda d: d["shots"]["r23_filed"].update(viewer="x@opal.invalid"))
    mutate("not completed", fr=lambda r: r["Item"]["status"].update(S="in_progress"))
    mutate("another claimer", fr=lambda r: r["Item"]["assignee"].update(S="other@opal.invalid"))
    mutate("another completer", fr=lambda r: r["Item"]["events"]["L"][2]["M"]["actor"].update(S="other@opal.invalid"))
    mutate("another requester", fr=lambda r: r["Item"]["requester"]["M"]["email"].update(S="other@opal.invalid"))
    mutate("events out of order", fr=lambda r: r["Item"]["events"]["L"].reverse())
    mutate("completed_by other", fr=lambda r: r["Item"]["completed_by"]["M"]["email"].update(S="other@opal.invalid"))
    mutate("no claimed_at", fr=lambda r: r["Item"].pop("claimed_at"))
    mutate("no Item", fr=lambda r: r.pop("Item"))
    if bad:
        return 1
    print("R23-FWD4-SELFTEST-OK (17 mutants)")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else live())
