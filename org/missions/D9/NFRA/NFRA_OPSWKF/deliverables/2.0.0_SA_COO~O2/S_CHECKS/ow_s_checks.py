"""NFRA_OPSWKF workstream S (FWD-8) -- the issuer's mechanical checks (2.0.0_SA_COO~O2).

  s1-record   OW-s1-AC1  the four-function read exists: one section per function, each with a verdict line and a
                         file:line basis that resolves in this tree
  s2-tests    OW-s2-AC1  the worker's named tests exist and pass
  s2-probe    OW-s2-AC2  the ISSUER's own probe of dashboard_api.lambda_handler: every route but users/me refuses a
                         caller whose tier is not internal BEFORE any table or S3 access, and serves an internal one;
                         users/me still answers a client-tier caller with its own row

Prints <TOKEN>-OK or <TOKEN>-FAIL <reason>, exits 0 / 1. Run from the worktree root. Subprocesses are bounded (110 s).
"""
import importlib
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
            "test_users_me_unchanged_for_client_tier"]

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


def _strip(s):
    return re.sub(r"\x1b\[[0-9;]*m", "", s)


def _tests():
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
        "client": {"email": "c@client.test", "tier": "client", "userType": "client"},
        "service": {"email": "svc-x", "tier": "service", "userType": "service"},
        "empty-tier": {"email": "e@x.test", "tier": ""},
        "null-tier": {"email": "n@x.test", "tier": "null"},
        "no-context": None,
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
    internal = {"email": "staff@opal.test", "tier": "internal", "userType": "Dev"}
    for path, query in GATED:
        mod.dynamodb, mod.s3 = _EmptyDDB(), _Tripwire()
        resp = mod.lambda_handler(_event(path, query, internal), None)
        code = resp.get("statusCode")
        if code not in (200, 404):
            return False, "internal %s answered %s, expected 200 or 404" % (path, code)
        served += 1
    mod.dynamodb, mod.s3 = _EmptyDDB(), _Tripwire()
    me = mod.lambda_handler(_event(BASE + "/users/me", {}, callers["client"]), None)
    if me.get("statusCode") != 200 or '"c@client.test"' not in me.get("body", ""):
        return False, "users/me for a client-tier caller answered %s" % me.get("statusCode")
    return True, "refused=%d of %d (5 callers x %d routes), internal served=%d of %d, users/me own row" % (
        refused, 5 * len(GATED), len(GATED), served, len(GATED))


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
    fn = {"s1-record": _record, "s2-tests": _tests, "s2-probe": _probe}.get(sub)
    if fn is None:
        print("unknown check %r" % sub)
        return 2
    ok, why = fn()
    print("%s-%s %s" % (token, "OK" if ok else "FAIL", why))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
