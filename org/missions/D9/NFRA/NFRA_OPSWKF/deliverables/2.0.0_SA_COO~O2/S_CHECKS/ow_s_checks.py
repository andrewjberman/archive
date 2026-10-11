"""NFRA_OPSWKF workstream S (FWD-8) -- the issuer's mechanical checks (2.0.0_SA_COO~O2).

  s1-record   OW-s1-AC1  the four-function read exists: one section per function, each with a verdict line and a
                         file:line basis that resolves in this tree
  s2-tests    OW-s2-AC1  the worker's named tests exist and pass
  s2-probe    OW-s2-AC2  the ISSUER's own probe of dashboard_api.lambda_handler: every route but users/me refuses a
                         caller who is not OPAL-INTERNAL (tier exactly internal OR firmId exactly opal-capital; PRD v0.6)
                         BEFORE any table or S3 access, and serves one who is, whichever comparison admits it;
                         users/me still answers a client-tier caller with its own row

  s9-tests    OW-s3-AC1  FWD-9: the worker's named tests of the submit handler exist and pass
  s9-probe    OW-s3-AC2  FWD-9: the ISSUER's own probe of submission_handler.lambda_handler: a caller who is not
                         OPAL-INTERNAL is answered 403 with the new check's own message before any table, user lookup or
                         mail, whatever the body; an Opal-internal caller posting a malformed ticket_id reaches the 400
  s9-regress  OW-s3-AC3  FWD-9: the submit handler's whole test directory passes (the pre-existing files included)

  s5-record   OW-s5-AC1  the second-door record exists, ASCII, with its five sections, a context_keys line, a
                         requests_30d line (a number or NO-METRIC) and a non-zero portal-API control

Prints <TOKEN>-OK or <TOKEN>-FAIL <reason>, exits 0 / 1. Run from the worktree root. Subprocesses are bounded (110 s).
"""
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DASH = Path("infra/aws/lambda/trade-pipeline/trade-dashboard-api")
DASH_TEST = DASH / "tests" / "test_internal_only.py"
S2_NAMES = ["test_internal_caller_served_on_every_route",
            "test_client_tier_refused_on_every_route",
            "test_service_tier_refused_on_every_route",
            "test_no_authorizer_context_refused_on_every_route",
            "test_refusal_touches_no_table_and_no_s3",
            "test_users_me_unchanged_for_client_tier",
            "test_opal_capital_firm_served_whatever_the_tier",
            "test_advisor_tier_of_another_firm_refused"]

S1_DOC = Path("org/missions/D9/NFRA/NFRA_OPSWKF/deliverables/0.9.0_WK_NFRA_OPSWKF~7/"
              "FOUR_FUNCTIONS_WHAT_A_NON_INTERNAL_CALLER_CAN_DO.md")
S1_FUNCTIONS = ["trade-submission-handler", "opal-research-pull-enqueue", "opal-portal-data-proxy",
                "opal-portal-content-api"]

BASE = "/api/general/trades"
# (path, query) -- the eight routed reads, the by-date branch the router reaches, and the router's default branch.
GATED = [
    (BASE + "/submissions", {}),
    (BASE + "/submissions/pending", {}),
    (BASE + "/submissions/by-status", {"status": "APPROVED"}),
    (BASE + "/submissions/by-initiator", {"email": "someone@opal.test"}),
    (BASE + "/submissions/by-approver", {"email": "someone@opal.test"}),
    (BASE + "/submissions/TRADE-20260101-abc", {}),
    (BASE + "/submissions/TRADE-20260101-abc/excel", {}),
    (BASE + "/users", {}),
    (BASE + "/submissions/by-date", {"date": "2026-01-01"}),
    (BASE + "/anything-else", {}),
]


SUB = Path("infra/aws/lambda/trade-pipeline/trade-submission-handler")
SUB_TEST = SUB / "tests" / "test_submit_internal_only.py"
S9_NAMES = ["test_opal_firm_caller_reaches_the_ticket_check",
            "test_tier_internal_caller_reaches_the_ticket_check",
            "test_client_tier_refused_with_the_new_message",
            "test_service_tier_refused_with_the_new_message",
            "test_outsider_without_email_gets_the_new_message_first",
            "test_refusal_touches_no_table_no_user_lookup_and_no_mail",
            "test_opal_caller_legacy_submit_still_stores"]
S9_MESSAGE = "Forbidden: trade submission answers Opal staff only"


def _strip(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def _tests(test_file=None, names=None):
    DASH_TEST = test_file or globals()["DASH_TEST"]
    S2_NAMES = names or globals()["S2_NAMES"]
    if not DASH_TEST.exists():
        return False, "absent: %s" % DASH_TEST.as_posix()
    src = DASH_TEST.read_text(encoding="utf-8")
    missing = [n for n in S2_NAMES if not re.search(r"^\s*def %s\(" % re.escape(n), src, re.M)]
    if missing:
        return False, "missing test(s): %s" % ", ".join(missing)
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", DASH_TEST.as_posix()]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    out = _strip(r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    bad = int((re.search(r"(\d+) failed", out) or [0, 0])[1]) + int((re.search(r"(\d+) error", out) or [0, 0])[1])
    if r.returncode != 0 or bad or passed < len(S2_NAMES):
        tail = [ln for ln in out.splitlines() if ln.strip()][-1:] or [""]
        return False, "rc=%d passed=%d failed+errors=%d need>=%d %s" % (r.returncode, passed, bad, len(S2_NAMES), tail[0])
    return True, "passed=%d" % passed


class _Tripwire:
    """Any attribute access is a touch: a refused caller must reach neither DynamoDB nor S3."""

    def __init__(self):
        object.__setattr__(self, "touched", [])

    def __getattr__(self, name):
        object.__getattribute__(self, "touched").append(name)
        raise AssertionError("touched %s" % name)


class _EmptyTable:
    def get_item(self, **_kw):
        return {}

    def query(self, **_kw):
        return {"Items": [], "Count": 0}

    def scan(self, **_kw):
        return {"Items": [], "Count": 0}


class _EmptyDDB:
    def Table(self, _name):
        return _EmptyTable()


def _event(path, query, claims):
    ev = {"rawPath": path, "queryStringParameters": query or None,
          "requestContext": {"http": {"method": "GET"}}}
    if claims is not None:
        ev["requestContext"]["authorizer"] = {"lambda": claims}
    return ev


def _probe():
    src = DASH / "src"
    if not (src / "dashboard_api.py").exists():
        return False, "absent: %s" % (src / "dashboard_api.py").as_posix()
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    sys.path.insert(0, str(src.resolve()))
    try:
        mod = importlib.import_module("dashboard_api")
    except Exception as e:  # noqa: BLE001
        return False, "import failed: %s" % e
    callers = {
        "client": {"email": "c@client.test", "tier": "client", "userType": "client", "firmId": "some-client-firm"},
        "service": {"email": "svc-x", "tier": "service", "userType": "service", "firmId": "null"},
        "advisor-other-firm": {"email": "a@partner.test", "tier": "advisor", "firmId": "49financial"},
        "dev-other-firm": {"email": "d@partner.test", "tier": "advisor", "userType": "Dev", "firmId": "49financial"},
        "empty-tier": {"email": "e@x.test", "tier": ""},
        "null-tier-null-firm": {"email": "n@x.test", "tier": "null", "firmId": "null"},
        "near-miss": {"email": "m@x.test", "tier": "Internal", "firmId": "opal-capital-x"},
        "no-context": None,
    }
    insiders = {
        "tier-internal": {"email": "staff@opal.test", "tier": "internal", "userType": "Dev", "firmId": "opal-capital"},
        "tier-internal-no-firm": {"email": "staff2@opal.test", "tier": "internal", "firmId": "null"},
        "advisor-tier-opal-firm": {"email": "staff3@opal.test", "tier": "advisor", "firmId": "opal-capital"},
    }
    refused = 0
    for who, claims in callers.items():
        for path, query in GATED:
            trip_d, trip_s = _Tripwire(), _Tripwire()
            mod.dynamodb, mod.s3 = trip_d, trip_s
            try:
                resp = mod.lambda_handler(_event(path, query, claims), None)
            except Exception as e:  # noqa: BLE001
                return False, "%s %s raised %s" % (who, path, e)
            code = resp.get("statusCode")
            touched = object.__getattribute__(trip_d, "touched") + object.__getattribute__(trip_s, "touched")
            if code != 403:
                return False, "%s %s answered %s, expected 403" % (who, path, code)
            if touched:
                return False, "%s %s touched %s before refusing" % (who, path, touched)
            refused += 1
    served = 0
    for who, internal in insiders.items():
        for path, query in GATED:
            mod.dynamodb, mod.s3 = _EmptyDDB(), _Tripwire()
            resp = mod.lambda_handler(_event(path, query, internal), None)
            code = resp.get("statusCode")
            if code not in (200, 404):
                return False, "%s %s answered %s, expected 200 or 404" % (who, path, code)
            served += 1
    mod.dynamodb, mod.s3 = _EmptyDDB(), _Tripwire()
    me = mod.lambda_handler(_event(BASE + "/users/me", {}, callers["client"]), None)
    if me.get("statusCode") != 200 or '"c@client.test"' not in me.get("body", ""):
        return False, "users/me for a client-tier caller answered %s" % me.get("statusCode")
    return True, "refused=%d of %d (%d outsiders x %d routes), served=%d of %d (%d insiders), users/me own row" % (
        refused, len(callers) * len(GATED), len(callers), len(GATED), served, len(insiders) * len(GATED), len(insiders))


def _s9_regress():
    d = SUB / "tests"
    if not d.exists():
        return False, "absent: %s" % d.as_posix()
    files = sorted(f.name for f in d.glob("test_*.py"))
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", d.as_posix()],
                           capture_output=True, text=True, timeout=110)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    out = _strip(r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) passed", out) or [0, 0])[1])
    bad = int((re.search(r"(\d+) failed", out) or [0, 0])[1]) + int((re.search(r"(\d+) error", out) or [0, 0])[1])
    if r.returncode != 0 or bad or not passed:
        return False, "rc=%d passed=%d failed+errors=%d across %d file(s)" % (r.returncode, passed, bad, len(files))
    return True, "passed=%d across %d test file(s)" % (passed, len(files))


def _s9_probe():
    src = SUB / "src"
    if not (src / "submission_handler.py").exists():
        return False, "absent: %s" % (src / "submission_handler.py").as_posix()
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    sys.path.insert(0, str(src.resolve()))
    try:
        mod = importlib.import_module("submission_handler")
    except Exception as e:  # noqa: BLE001
        return False, "import failed: %s" % e
    touched = []

    def trip(name):
        def _f(*_a, **_k):
            touched.append(name)
            raise AssertionError("touched %s" % name)
        return _f

    for name in ("get_user", "get_users_by_group", "send_approval_request"):
        if not hasattr(mod, name):
            return False, "handler module has no %s to guard" % name
    outsiders = {
        "client": {"email": "c@client.test", "tier": "client", "userType": "client", "firmId": "some-client-firm"},
        "service": {"email": "svc-x", "tier": "service", "userType": "service", "firmId": "null"},
        "advisor-other-firm": {"email": "a@partner.test", "tier": "advisor", "firmId": "49financial"},
        "dev-other-firm": {"email": "d@partner.test", "tier": "advisor", "userType": "Dev", "firmId": "49financial"},
        "near-miss": {"email": "m@x.test", "tier": "Internal", "firmId": "opal-capital-x"},
        "outsider-no-email": {"tier": "advisor", "firmId": "49financial"},
        "no-context": None,
    }
    insiders = {
        "tier-internal": {"email": "staff@opal.test", "tier": "internal", "firmId": "null"},
        "advisor-tier-opal-firm": {"email": "staff3@opal.test", "tier": "advisor", "firmId": "opal-capital"},
    }
    legacy = {"fund": "PFDE", "brokerage": "vident", "weights_as_of": "2026-09-25", "proposed_trades_as_of": "2026-09-25",
              "attestations": {"guidelines": True}, "securities": [{"ticker": "AAPL", "proposed_weight": 0.2}]}
    bodies = {"malformed-ticket": dict(legacy, ticket_id="not-a-ticket-id"), "legacy": legacy, "empty": {},
              "named-initiator": dict(legacy, initiator_email="someone.else@opal.test")}

    def call(claims, body):
        ev = {"requestContext": {"http": {"method": "POST"}}, "body": json.dumps(body)}
        if claims is not None:
            ev["requestContext"]["authorizer"] = {"lambda": claims}
        del touched[:]
        mod.dynamodb = _Tripwire()
        mod.get_user, mod.get_users_by_group = trip("get_user"), trip("get_users_by_group")
        mod.send_approval_request = trip("send_approval_request")
        resp = mod.lambda_handler(ev, None)
        t = list(touched) + object.__getattribute__(mod.dynamodb, "touched")
        try:
            msg = json.loads(resp.get("body") or "{}").get("message")
        except ValueError:
            msg = None
        return resp.get("statusCode"), msg, t

    refused = 0
    for who, claims in outsiders.items():
        for bname, body in bodies.items():
            code, msg, t = call(claims, body)
            if code != 403 or msg != S9_MESSAGE:
                return False, "%s / %s answered %s %r, expected 403 %r" % (who, bname, code, msg, S9_MESSAGE)
            if t:
                return False, "%s / %s touched %s before refusing" % (who, bname, t)
            refused += 1
    reached = 0
    for who, claims in insiders.items():
        code, msg, t = call(claims, bodies["malformed-ticket"])
        if code != 400 or msg != "ticket_id is malformed":
            return False, "%s / malformed-ticket answered %s %r, expected 400 ticket_id is malformed" % (who, code, msg)
        if t:
            return False, "%s / malformed-ticket touched %s before the 400" % (who, t)
        reached += 1
    return True, ("refused=%d of %d (%d outsiders x %d bodies) with the new message and nothing touched, "
                  "insiders at the 400=%d of %d") % (
        refused, len(outsiders) * len(bodies), len(outsiders), len(bodies), reached, len(insiders))


S5_DOC = Path("org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/"
              "NFRA_OPSWKF_SECOND_DOOR_AUTHORIZER_BYTES_AND_TRAFFIC_20261011.md")
S5_SECTIONS = ["trade-authorizer", "trade-auth-handler", "What the three functions answer through this API today",
               "Traffic, 30 days", "not_established"]


def _s5_record():
    if not S5_DOC.exists():
        return False, "absent: %s" % S5_DOC.as_posix()
    text = S5_DOC.read_text(encoding="utf-8")
    if any(ord(ch) > 127 for ch in text):
        return False, "non-ASCII in the record"
    heads = [h.strip() for h in re.findall(r"^## (.+)$", text, re.M)]
    missing = [x for x in S5_SECTIONS if not any(h.startswith(x) for h in heads)]
    if missing:
        return False, "no section for %s" % "; ".join(missing)
    if not re.search(r"^context_keys: \S", text, re.M):
        return False, "no 'context_keys:' line"
    m = re.search(r"^requests_30d: (\d+|NO-METRIC)\b", text, re.M)
    if not m:
        return False, "no 'requests_30d: <number or NO-METRIC>' line"
    c = re.search(r"^control_portal_api_30d: (\d+)\b", text, re.M)
    if not c or int(c.group(1)) <= 0:
        return False, "no 'control_portal_api_30d:' line with a number above zero"
    return True, "5 of 5 sections, requests_30d=%s, control=%s" % (m.group(1), c.group(1))


def _record():
    if not S1_DOC.exists():
        return False, "absent: %s" % S1_DOC.as_posix()
    text = S1_DOC.read_text(encoding="utf-8")
    if any(ord(ch) > 127 for ch in text):
        return False, "non-ASCII in the record"
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    by_fn = {}
    for p in parts:
        head = p.splitlines()[0].strip()
        for fn in S1_FUNCTIONS:
            if head.startswith(fn):
                by_fn[fn] = p
    missing = [fn for fn in S1_FUNCTIONS if fn not in by_fn]
    if missing:
        return False, "no section for %s" % ", ".join(missing)
    cites = 0
    for fn, body in by_fn.items():
        m = re.search(r"^non_internal_caller: (CAN|CANNOT|PARTLY) -- \S.{20,}$", body, re.M)
        if not m:
            return False, "%s: no 'non_internal_caller: CAN|CANNOT|PARTLY -- <what>' line" % fn
        if not re.search(r"^routes: \d+", body, re.M):
            return False, "%s: no 'routes: <n>' line" % fn
        found = re.findall(r"`([A-Za-z0-9_./-]+\.(?:py|mjs|js|ts|tf)):(\d+)(?:-(\d+))?`", body)
        if not found:
            return False, "%s: no `path:line` basis" % fn
        for path, a, b in found:
            f = Path(path)
            if not f.exists():
                return False, "%s: basis %s does not exist" % (fn, path)
            n = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
            if int(b or a) > n or int(a) < 1:
                return False, "%s: basis %s:%s is past the file's %d lines" % (fn, path, b or a, n)
            cites += 1
    return True, "4 of 4 functions, %d basis citation(s) resolve" % cites


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    sub = argv[0]
    token = "OW-" + sub.upper()
    fn = {"s1-record": _record, "s2-tests": _tests, "s2-probe": _probe,
          "s9-tests": lambda: _tests(SUB_TEST, S9_NAMES), "s9-probe": _s9_probe, "s9-regress": _s9_regress,
          "s5-record": _s5_record}.get(sub)
    if fn is None:
        print("unknown check %r" % sub)
        return 2
    ok, why = fn()
    print("%s-%s %s" % (token, "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
