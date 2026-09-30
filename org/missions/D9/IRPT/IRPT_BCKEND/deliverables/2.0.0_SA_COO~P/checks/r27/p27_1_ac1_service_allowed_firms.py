"""Round 27 AC (IB-pr-271, row S238, CTO 103318) -- the served boundary refuses a SERVICE principal's selected firm outside its
allowedFirmIds, and changes nothing else.

Usage: python p27_1_ac1_service_allowed_firms.py <worktree root>
Drives the REAL `_authz/served.py` Entry.handle (no AWS call): step 2 of the boundary, where an internal subject may select a
registry firm. The profile read is injected through the constructor keyword the order names, `load_service_profile`
(callable email -> profile row dict or None; may raise).
HARNESS CONTROLS (must hold at the base AND after the change, else the harness is wrong, not the code):
  H1  a NON-internal subject (x-firm-id cottonwood, no service/Dev marker) selecting inflection -> FIRM_BINDING
  H2  an internal user subject (x-firm-id opal-capital, x-user-type user) selecting inflection -> admitted (deps called with it)
ADMISSION ORACLE: "admitted" = the boundary called deps(<selected>) (step 3 reached with the selected firm as VERIFIED).
ARMS (the change):
  A   service subject, row allowedFirmIds "cottonwood", selects cottonwood   -> NOT FIRM_BINDING
  B   same subject selects inflection                                         -> FIRM_BINDING
  C   service subject, row WITHOUT allowedFirmIds, selects inflection         -> NOT FIRM_BINDING (unrestricted, today's behaviour)
  D   service subject, row allowedFirmIds "ALL", selects inflection           -> NOT FIRM_BINDING
  E   service subject whose profile read RAISES, selects cottonwood           -> FIRM_BINDING (fail closed)
  F   service subject, row allowedFirmIds ["cottonwood","49financial"] (list), selects 49financial -> NOT FIRM_BINDING
Pass line: P27-1-AC1 PASS. Base: FAIL (Entry does not accept load_service_profile), with H1/H2 passing.
"""
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
PKG = root / "infra/aws/lambda/investor-reporting"
for p in (PKG / "_authz", PKG / "_scope", PKG / "_keys", PKG / "_ids"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(
    {"opal-capital": "b-opal", "cottonwood": "b-cot", "inflection": "b-inf", "49financial": "b-49f"})


def fail(msg):
    print("P27-1-AC1 FAIL: " + msg)
    sys.exit(1)


import served  # noqa: E402

ROUTES = {"GET /api/scoped/investor-reporting/directory/search": "directory_search"}
OPS = {"directory_search": lambda *a: {}}


def headers(firm, user_type, email="svc-irpt-analysis@opalinvest.com"):
    h = {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": firm, "x-origin-verify": "cloudfront",
         "x-user-email": email, "x-user-role": "user"}
    if user_type:
        h["x-user-type"] = user_type
    return h


def event(h, selected):
    return {"headers": h, "routeKey": "GET /api/scoped/investor-reporting/directory/search",
            "queryStringParameters": {"selected_tenant": selected}}


def is_firm_binding(result):
    return "FIRM_BINDING" in json.dumps(result, default=str)


SEEN = []


def deps(tenant, *a, **k):
    """The boundary calls deps(tenant) with the VERIFIED tenant only after step 2 admits it; recording the call is the
    admission oracle (a crash inside the new branch never reaches it, whatever envelope the handler then returns)."""
    SEEN.append(tenant)
    raise RuntimeError("harness stop after admission")


def run(entry, h, selected):
    del SEEN[:]
    try:
        out = entry.handle(event(h, selected))
    except Exception as exc:  # noqa: BLE001 -- an exception is an outcome to grade, never a pass
        out = {"_raised": "%s: %s" % (type(exc).__name__, str(exc)[:160])}
    out = dict(out) if isinstance(out, dict) else {"_out": out}
    out["_admitted_as"] = list(SEEN)
    return out


def admitted(out, selected):
    return selected in out.get("_admitted_as", [])


base_entry = served.Entry(function_name="irpt-directory-search", operations=OPS, deps=deps,
                          opaque_firm_for=lambda *a, **k: None, routes=ROUTES)
h1 = run(base_entry, headers("cottonwood", None, "advisor@cottonwood.test"), "inflection")
if not is_firm_binding(h1) or admitted(h1, "inflection"):
    fail("HARNESS H1: a non-internal subject selecting another firm was not refused FIRM_BINDING (%s)" % str(h1)[:200])
h2 = run(base_entry, headers("opal-capital", "user", "ops@opalinvest.com"), "inflection")
if not admitted(h2, "inflection"):
    fail("HARNESS H2: an internal user subject selecting a registry firm did not reach deps('inflection') (%s)" % str(h2)[:200])
print("  harness controls H1 (FIRM_BINDING) and H2 (admitted past step 2) hold")

ROWS = {
    "svc-cot@opalinvest.com": {"email": "svc-cot@opalinvest.com", "userType": "service", "allowedFirmIds": "cottonwood"},
    "svc-open@opalinvest.com": {"email": "svc-open@opalinvest.com", "userType": "service"},
    "svc-all@opalinvest.com": {"email": "svc-all@opalinvest.com", "userType": "service", "allowedFirmIds": "ALL"},
    "svc-list@opalinvest.com": {"email": "svc-list@opalinvest.com", "userType": "service",
                                "allowedFirmIds": ["cottonwood", "49financial"]},
}


def loader(email):
    if email == "svc-boom@opalinvest.com":
        raise RuntimeError("profile store unreadable")
    return ROWS.get(email)


try:
    e = served.Entry(function_name="irpt-directory-search", operations=OPS, deps=deps,
                     opaque_firm_for=lambda *a, **k: None, routes=ROUTES, load_service_profile=loader)
except TypeError as exc:
    fail("Entry does not accept load_service_profile (%s)" % exc)

arms = [
    ("A", "svc-cot@opalinvest.com", "cottonwood", False),
    ("B", "svc-cot@opalinvest.com", "inflection", True),
    ("C", "svc-open@opalinvest.com", "inflection", False),
    ("D", "svc-all@opalinvest.com", "inflection", False),
    ("E", "svc-boom@opalinvest.com", "cottonwood", True),
    ("F", "svc-list@opalinvest.com", "49financial", False),
]
for name, email, sel, want_refused in arms:
    out = run(e, headers("opal-capital", "service", email), sel)
    adm = admitted(out, sel)
    refused = is_firm_binding(out) and not adm
    if want_refused and not refused:
        fail("arm %s (%s selects %s): want FIRM_BINDING, got admitted=%s out=%s" % (name, email, sel, adm, str(out)[:200]))
    if not want_refused and not adm:
        fail("arm %s (%s selects %s): want admitted (deps called with %r), got %s" % (name, email, sel, sel, str(out)[:200]))
    print("  arm %s OK: %s selects %s -> %s" % (name, email, sel, "FIRM_BINDING" if refused else "admitted: deps(%r)" % sel))
print("P27-1-AC1 PASS (2 harness controls, 6 arms)")
