"""TCKT_VNEXT round 23 -- FWD-5 ON DEV (cell R23-f5-1, ADJUDICATION_v21 by the CVO, relayed by the CTO msg 11772): an Opal person picks the next request from the queue alone.

  python r23_fwd5_check.py              the live check: the result document, the saved ticket records, the shots, both tickets (ABSENT), both identity rows (ABSENT)
  python r23_fwd5_check.py --self-test  the document scan on a good and several bad documents (no AWS)

Prints RUN-OK (fwd5) <detail> or RUN-BAD <reason>; exit 0/1. Read-only AWS reads (us-east-1). The CVO grades the shots (a judgment: the board unclipped, both
rows' type and age readable, the claim made from the board); this check holds what the world can contradict: two open tickets of DIFFERENT types were filed by
the filer, the picker's claim landed on exactly the chosen one and not the other, the picker did not open either ticket first, and everything synthetic is gone.
"""
import copy
import hashlib
import json
import os
import re
import subprocess
import sys

DIR = "org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r23_fwd5_dev/"
RES = DIR + "R23_FWD5_RESULT.json"
RECORD = DIR + "R23_FWD5_TICKET_ITEMS.json"
ORIGIN = "http://localhost:5174"
PROTECTED = {"TCK-20261017-da2a1987", "TCK-20261017-5af976ff"}
LABELS = {"service_request": "service request", "meeting_request": "meeting request", "other": "other", "trade_request": "trade request"}
KEYS = {"browser_origin", "filer", "picker", "chosen_ticket", "other_ticket", "board_read", "chosen_basis", "claim_via", "opened_before_claim",
        "shots", "token_exp", "rows_deleted_at", "tickets_deleted_at", "tickets_absent_after", "rows_absent_after", "no_engine_call",
        "token_printed", "shot_data_reviewed", "private_board"}
SHOT_ROLES = ["r23_rows_before", "r23_rows_claimed"]   # committed, clipped to the two synthetic rows
PRIVATE_ROLES = ["r23_board_full", "r23_board_claimed"]   # the full board, kept OUTSIDE the repo (the CTO, msg 11820)
PRIVATE_DIR = "C:/dev/_tckt_private_evidence/r23_f51/"
SHA = re.compile(r"^[0-9a-f]{64}$")
PNG = b"\x89PNG\r\n\x1a\n"
TID = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")
AWS = os.path.abspath(".tools/aws.cmd")


def doc_problem(doc):
    missing = sorted(KEYS - set(doc))
    if missing:
        return "missing key(s): %s" % missing
    if doc["browser_origin"] != ORIGIN:
        return "the browser origin is %r, not the one DEV origin %s" % (doc["browser_origin"], ORIGIN)
    if doc["token_printed"] is not False or doc["no_engine_call"] is not True or doc["shot_data_reviewed"] is not True:
        return "token_printed, no_engine_call or shot_data_reviewed differs from the order"
    for k in ("tickets_absent_after", "rows_absent_after"):
        if doc[k] is not True:
            return "%s must read True after the removal" % k
    if not all(str(doc[k]) > str(doc["token_exp"]) for k in ("rows_deleted_at", "tickets_deleted_at")):
        return "a removal happened before the last token exp"
    a, b = doc["chosen_ticket"], doc["other_ticket"]
    if a == b or not TID.match(str(a)) or not TID.match(str(b)) or a in PROTECTED or b in PROTECTED:
        return "the two tickets must be two distinct, unprotected ticket ids"
    for who in ("filer", "picker"):
        if not str(doc[who]).endswith("@opal.invalid") or doc[who] != str(doc[who]).lower():
            return "the %s must be a lower-case synthetic @opal.invalid address" % who
    if doc["filer"] == doc["picker"]:
        return "the picker must be a second identity, not the filer"
    if doc["claim_via"] != "board" or doc["opened_before_claim"] is not False:
        return "the claim must be made from the board without opening either ticket"
    if len(str(doc["chosen_basis"]).strip()) < 20:
        return "chosen_basis must say what the person read on the board"
    br = doc["board_read"]
    if not isinstance(br, dict) or sorted(br) != sorted([a, b]):
        return "board_read must carry exactly the two tickets"
    for t, r in br.items():
        if not isinstance(r, dict) or not str(r.get("type_label", "")).strip() or not str(r.get("age_text", "")).strip():
            return "board_read for %s lacks the type label or the age text read from the row" % t
    shots = doc["shots"]
    if not isinstance(shots, dict) or sorted(shots) != sorted(SHOT_ROLES):
        return "the shots must be exactly the roles %s" % SHOT_ROLES
    for role, rec in shots.items():
        if not isinstance(rec, dict) or not rec.get("path") or not rec.get("bytes") or rec.get("origin") != ORIGIN or not rec.get("viewer"):
            return "shot %s lacks path, bytes, viewer or the DEV origin" % role
        if not str(rec["path"]).startswith(DIR):
            return "shot %s is saved outside %s" % (role, DIR)
        if rec["viewer"] != doc["picker"]:
            return "shot %s must be taken as the picker" % role
        want = ("two_synthetic_rows", 2) if role == "r23_rows_before" else ("chosen_row", 1)
        if (rec.get("clipped_to"), rec.get("rows_visible")) != want:
            return "shot %s must be clipped to %s (%d row(s)), unaltered, not a composite" % (role, want[0], want[1])
    pb = doc["private_board"]
    if not isinstance(pb, dict) or sorted(pb) != sorted(PRIVATE_ROLES):
        return "private_board must carry exactly the roles %s" % PRIVATE_ROLES
    for role, rec in pb.items():
        if not isinstance(rec, dict) or not str(rec.get("path", "")).startswith(PRIVATE_DIR) or ".." in str(rec["path"]):
            return "private shot %s is not under %s" % (role, PRIVATE_DIR)
        if not SHA.match(str(rec.get("sha256", ""))) or not isinstance(rec.get("bytes"), int) or rec["bytes"] < 1:
            return "private shot %s lacks a sha256 or a byte size" % role
        if not all(isinstance(rec.get(k), int) and rec[k] > 0 for k in ("width", "height")):
            return "private shot %s lacks its pixel size" % role
    return None


def _ev(it):
    return [(e["M"]["action"]["S"], e["M"]["actor"]["S"].lower()) for e in it["events"]["L"]]


def record_problem(rec, doc):
    """rec = {"chosen": <get-item output>, "other": <get-item output>}, each saved whole BEFORE the delete."""
    try:
        c, o = rec["chosen"]["Item"], rec["other"]["Item"]
        if c["ticket_id"]["S"] != doc["chosen_ticket"] or o["ticket_id"]["S"] != doc["other_ticket"]:
            return "the saved records are not the two tickets of the document"
        tc, to = c["ticket_type"]["S"], o["ticket_type"]["S"]
        if tc == to:
            return "both tickets are of the type %r: the board must show two different types" % tc
        if "analysis_request" in (tc, to) or tc not in LABELS or to not in LABELS:
            return "a ticket type is an analysis request or unknown"
        for t, ty in ((doc["chosen_ticket"], tc), (doc["other_ticket"], to)):
            if LABELS[ty] != str(doc["board_read"][t]["type_label"]).strip().lower():
                return "the type label read on the board for %s does not match its type %s" % (t, ty)
        for it in (c, o):
            if it["requester"]["M"]["email"]["S"].lower() != doc["filer"]:
                return "a ticket's requester is not the filer"
        if c["status"]["S"] != "in_progress" or c["assignee"]["S"].lower() != doc["picker"]:
            return "the chosen ticket is not in_progress under the picker"
        if _ev(c) != [("created", doc["filer"]), ("claimed", doc["picker"])]:
            return "the chosen ticket's events are %s" % _ev(c)
        if o["status"]["S"] != "open" or o.get("assignee", {}).get("S"):
            return "the other ticket is not open and unassigned"
        if _ev(o) != [("created", doc["filer"])]:
            return "the other ticket's events are %s" % _ev(o)
    except (KeyError, TypeError, AttributeError) as e:
        return "the saved records do not carry the expected shape: %r" % (e,)
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
        print("RUN-BAD cannot read the result file or the saved ticket records: %s" % e)
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
        for role, pr in doc["private_board"].items():
            raw = open(pr["path"], "rb").read()
            if not raw.startswith(PNG) or len(raw) != pr["bytes"] or hashlib.sha256(raw).hexdigest() != pr["sha256"]:
                print("RUN-BAD private shot %s is not the recorded PNG (size or sha256)" % role)
                return 1
        for t in (doc["chosen_ticket"], doc["other_ticket"]):
            if item("opal-tickets", {"ticket_id": {"S": t}}) is not None:
                print("RUN-BAD the synthetic ticket %s is still PRESENT" % t)
                return 1
        for who in (doc["filer"], doc["picker"]):
            if item("opal-users-v2", {"PK": {"S": "USER#" + who}, "SK": {"S": "PROFILE"}}) is not None:
                print("RUN-BAD the identity row %s is still PRESENT" % who)
                return 1
        for t in sorted(PROTECTED):
            if item("opal-tickets", {"ticket_id": {"S": t}}) is None:
                print("RUN-BAD protected ticket %s is not present" % t)
                return 1
    except (RuntimeError, ValueError, KeyError, OSError, subprocess.SubprocessError) as e:
        print("RUN-BAD live read failed: %s" % e)
        return 1
    print("RUN-OK (fwd5) %s read the board, saw %s and %s, and claimed %s from the board without opening either; both tickets and both rows ABSENT; the protected tickets present"
          % (doc["picker"], doc["chosen_ticket"], doc["other_ticket"], doc["chosen_ticket"]))
    return 0


def _good():
    f, p = "tckt-r23-filer-20261021@opal.invalid", "tckt-r23-picker-20261021@opal.invalid"
    a, b = "TCK-20261021-0123abcd", "TCK-20261021-4567ef01"
    shots = {r: {"path": DIR + r + ".png", "bytes": 10, "origin": ORIGIN, "viewer": p, "clipped_to": "two_synthetic_rows" if r == "r23_rows_before" else "chosen_row", "rows_visible": 2 if r == "r23_rows_before" else 1} for r in SHOT_ROLES}
    private = {r: {"path": PRIVATE_DIR + r + ".png", "sha256": "a" * 64, "bytes": 10, "width": 1280, "height": 900} for r in PRIVATE_ROLES}
    doc = {"browser_origin": ORIGIN, "filer": f, "picker": p, "chosen_ticket": a, "other_ticket": b,
           "board_read": {a: {"type_label": "Service Request", "age_text": "(2 minutes)"}, b: {"type_label": "Other", "age_text": "(1 minute)"}},
           "chosen_basis": "Service Request, waiting 2 minutes, older than the Other row", "claim_via": "board", "opened_before_claim": False,
           "shots": shots, "token_exp": "2026-10-21T04:00:00Z", "rows_deleted_at": "2026-10-21T04:05:00Z", "tickets_deleted_at": "2026-10-21T04:05:30Z",
           "tickets_absent_after": True, "rows_absent_after": True, "no_engine_call": True, "token_printed": False, "shot_data_reviewed": True,
           "private_board": private}

    def s(v):
        return {"S": v}

    def ev(actor, action):
        return {"M": {"ts": s("t"), "actor": s(actor), "action": s(action)}}

    chosen = {"Item": {"ticket_id": s(a), "ticket_type": s("service_request"), "status": s("in_progress"), "requester": {"M": {"email": s(f)}},
                       "assignee": s(p), "events": {"L": [ev(f, "created"), ev(p, "claimed")]}}}
    other = {"Item": {"ticket_id": s(b), "ticket_type": s("other"), "status": s("open"), "requester": {"M": {"email": s(f)}},
                      "events": {"L": [ev(f, "created")]}}}
    return doc, {"chosen": chosen, "other": other}


def self_test():
    doc, rec = _good()
    if doc_problem(doc) or record_problem(rec, doc):
        print("RUN-BAD the good document did not pass: %s" % (doc_problem(doc) or record_problem(rec, doc)))
        return 1
    bad = []

    def mutate(name, fd=None, fr=None):
        d, r = copy.deepcopy(doc), copy.deepcopy(rec)
        if fd:
            fd(d)
        if fr:
            fr(r)
        if not (doc_problem(d) or record_problem(r, d)):
            bad.append(name)

    mutate("origin", lambda d: d.update(browser_origin="https://opalinvest.dev"))
    mutate("token printed", lambda d: d.update(token_printed=True))
    mutate("shot data not reviewed", lambda d: d.update(shot_data_reviewed=False))
    mutate("ticket still present", lambda d: d.update(tickets_absent_after=False))
    mutate("rows removed before exp", lambda d: d.update(rows_deleted_at="2026-10-21T03:00:00Z"))
    mutate("protected ticket", lambda d: d.update(chosen_ticket="TCK-20261017-da2a1987"))
    mutate("same ticket twice", lambda d: d.update(other_ticket=d["chosen_ticket"]))
    mutate("picker is the filer", lambda d: d.update(picker=d["filer"]))
    mutate("real address", lambda d: d.update(picker="alyssa@opalinvest.com"))
    mutate("claim via ticket page", lambda d: d.update(claim_via="ticket"))
    mutate("opened first", lambda d: d.update(opened_before_claim=True))
    mutate("no basis", lambda d: d.update(chosen_basis="x"))
    mutate("no age text", lambda d: d["board_read"][d["chosen_ticket"]].update(age_text=""))
    mutate("shot not clipped", lambda d: d["shots"]["r23_rows_before"].update(clipped_to="full_board"))
    mutate("three rows in the clip", lambda d: d["shots"]["r23_rows_claimed"].update(rows_visible=3))
    mutate("claimed shot as two rows", lambda d: d["shots"]["r23_rows_claimed"].update(clipped_to="two_synthetic_rows", rows_visible=2))
    mutate("before shot as one row", lambda d: d["shots"]["r23_rows_before"].update(clipped_to="chosen_row", rows_visible=1))
    mutate("shot as filer", lambda d: d["shots"]["r23_rows_before"].update(viewer=d["filer"]))
    mutate("private board in the repo", lambda d: d["private_board"]["r23_board_full"].update(path=DIR + "x.png"))
    mutate("private board path escapes", lambda d: d["private_board"]["r23_board_full"].update(path=PRIVATE_DIR + "../x.png"))
    mutate("private board no sha", lambda d: d["private_board"]["r23_board_claimed"].update(sha256="zz"))
    mutate("private board no pixel size", lambda d: d["private_board"]["r23_board_claimed"].pop("width"))
    mutate("private board missing", lambda d: d["private_board"].pop("r23_board_claimed"))
    mutate("same type", fr=lambda r: r["other"]["Item"]["ticket_type"].update(S="service_request"))
    mutate("analysis type", fr=lambda r: r["other"]["Item"]["ticket_type"].update(S="analysis_request"))
    mutate("label mismatch", fr=lambda r: r["other"]["Item"]["ticket_type"].update(S="meeting_request"))
    mutate("chosen not claimed", fr=lambda r: r["chosen"]["Item"]["status"].update(S="open"))
    mutate("claimed by the filer", fr=lambda r: r["chosen"]["Item"]["assignee"].update(S="tckt-r23-filer-20261021@opal.invalid"))
    mutate("other also claimed", fr=lambda r: r["other"]["Item"].update(status={"S": "in_progress"}, assignee={"S": "x@opal.invalid"}))
    mutate("other events extra", fr=lambda r: r["other"]["Item"]["events"]["L"].append(r["other"]["Item"]["events"]["L"][0]))
    mutate("requester not filer", fr=lambda r: r["chosen"]["Item"]["requester"]["M"]["email"].update(S="other@opal.invalid"))
    mutate("no Item", fr=lambda r: r["chosen"].pop("Item"))
    if bad:
        print("RUN-BAD mutants not caught: %s" % bad)
        return 1
    print("R23-FWD5-SELFTEST-OK (32 mutants)")
    return 0


if __name__ == "__main__":
    sys.exit(self_test() if "--self-test" in sys.argv else live())
