"""IRPT_DASHBD round 150, workstream COTREAD (issuer 2.0.0_SA_COO~D2) -- DB-b-319, C1 of the Cottonwood Performance read path (CTO ruling A, msg 10134): the CODE. The 49F read function FORWARDS a Cottonwood request to the Cottonwood
read function. `served.py` gains a LITERAL one-entry forward map (firm cottonwood -> the environment variable that names the target), an injectable `forward_invoke` port on `Entry`, the method `_forward`, and one change in
`handle`: where the 49F function refuses a firm it cannot map (`bucket_for` raising), it forwards ONLY when the literal map names the firm and its environment names the target, AFTER the internal-caller test and the
allowed-firm narrowing; the original event goes over untouched, the response comes back untouched, any failure is NOT_READY, and neither the event nor the body is logged. The target runs its own full guard.

  DB185-1-AC1  the diff: only served.py and the new test file changed; served.py only at the agreed places (the map, the port, the method, the guard); the map is exactly one entry; the method logs nothing and edits no event
  DB185-1-AC2  the behaviour: cottonwood forwarded once with the original event and the reply untouched; the 49F path unchanged; other firms and a missing environment refused; the narrowing first; a failure NOT_READY; no body in any output
  DB185-1-AC3  the tests: at least six NEW tests carry `forward` in their name and the whole _authz test directory passes

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants
"""
import difflib
import io
import json
import os
import re
import subprocess
import sys
import contextlib
from pathlib import Path

BASE = "dc96ba2eb7"
AUTHZ = "infra/aws/lambda/investor-reporting/_authz/"
SERVED = AUTHZ + "served.py"
TESTS = AUTHZ + "tests/"
MARK = "BODY-MARKER-0Q7"
ROUTE = "GET /api/scoped/investor-reporting/directory/search"
EMAIL = "ops@opalinvest.com"
ENVNAME = "IRPT_FORWARD_COTTONWOOD_FUNCTION"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE))
    return r.stdout.decode("utf-8")


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    root = Path(root)
    out = subprocess.run(["git", "-C", str(root), "diff", "--name-only", BASE], capture_output=True, text=True)
    need(out.returncode == 0, "cannot diff against the base %s" % BASE)
    untracked = subprocess.run(["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True)
    changed = {x for x in (out.stdout + untracked.stdout).splitlines() if x.strip()}
    extra = [f for f in changed if f != SERVED and not (f.startswith(TESTS) and f.rsplit("/", 1)[-1].startswith("test_forward_cottonwood"))]
    need(not extra, "files outside the agreed set changed: %s" % extra[:4])
    need(SERVED in changed and any(f.startswith(TESTS) for f in changed), "served.py and a test_forward_cottonwood* file must both be in the diff")
    new, old = (root / SERVED).read_bytes().decode("utf-8"), git_show(root, SERVED)
    need("\r" not in new, "served.py must keep LF line endings")
    removed = [ln for ln in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0) if ln.startswith("-") and not ln.startswith("---")]
    added = [ln for ln in difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0) if ln.startswith("+") and not ln.startswith("+++")]
    need(len(removed) <= 8 and len(added) <= 70, "served.py may remove at most 8 lines and add at most 70 (removed %d, added %d)" % (len(removed), len(added)))
    m = re.search(r"^FORWARD_FUNCTION_ENV\s*=\s*(\{.*?\})\s*$", new, flags=re.M)
    need(m is not None and eval(m.group(1), {}) == {"cottonwood": ENVNAME}, "FORWARD_FUNCTION_ENV must be a LITERAL map of exactly {'cottonwood': '%s'}" % ENVNAME)  # noqa: S307
    fm = re.search(r"    def _forward\(self.*?(?=\n    def |\nclass |\Z)", new, flags=re.S)
    need(fm is not None, "no Entry._forward method")
    body = fm.group(0)
    need(not re.search(r"\bprint\(|\blogging\b|\blog\w*\(|\bsys\.std(out|err)\b|traceback", body), "_forward must not log or print anything")
    need(not re.search(r"\bevent\s*\[[^\]]+\]\s*=|event\.(update|setdefault|pop)\(", body), "_forward must not edit the event")
    need("json.dumps(event" in body or "forward_invoke(function_name, event)" in body, "_forward must hand over the original event")
    return True


# ------------------------------------------------------------------------------------------------ AC2
def check_behaviour(root):
    root = Path(root)
    pkg = root / AUTHZ.rstrip("/")
    inv = pkg.parent
    for p in (str(pkg), str(pkg / "tests"), str(inv / "_scope"), str(inv / "_keys"), str(inv / "_ids")):
        if p not in sys.path:
            sys.path.insert(0, p)
    for mod in [m for m in list(sys.modules) if m in ("served", "loaders", "enforce", "errors", "resolve")]:
        sys.modules.pop(mod, None)
    import served  # noqa: E402
    seen, calls = [], []

    def deps(tenant, *a, **k):
        seen.append(tenant)
        raise RuntimeError("stop after admission")

    def entry(row=None, invoke=None):
        row = row if row is not None else {"status": "active", "allowedFirmIds": ["cottonwood", "49financial", "inflection"]}

        def forward(name, event):
            calls.append((name, event))
            if invoke:
                return invoke(name, event)
            return {"statusCode": 200, "isBase64Encoded": True, "headers": {"content-encoding": "gzip"}, "body": MARK}
        return served.Entry(function_name="irpt-49f-reporting-read-lambda", operations={"directory_search": lambda *a: {}}, deps=deps,
                            opaque_firm_for=lambda *a, **k: None, routes={ROUTE: "directory_search"}, load_service_profile=lambda email: row, forward_invoke=forward)

    def event(selected="cottonwood", **more):
        headers = {"X-Contract-Version": served.CONTRACT_VERSION, "X-Firm-Id": "opal-capital", "x-origin-verify": "cloudfront", "x-user-email": EMAIL, "x-user-role": "user", "x-user-type": "user"}
        headers.update(more)
        return {"headers": headers, "routeKey": ROUTE, "queryStringParameters": {"selected_tenant": selected}}

    def reset():
        del seen[:], calls[:]
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps({"49financial": "b-49f"})
    os.environ[ENVNAME] = "irpt-cot-reporting-read-lambda"
    reset()
    ev = event()
    snap = json.dumps(ev, sort_keys=True)
    out = entry().handle(ev)
    need(len(calls) == 1 and calls[0][0] == "irpt-cot-reporting-read-lambda" and calls[0][1] is ev and json.dumps(ev, sort_keys=True) == snap, "cottonwood must be forwarded once to the named function with the original event, unchanged")
    need(out == {"statusCode": 200, "isBase64Encoded": True, "headers": {"content-encoding": "gzip"}, "body": MARK} and not seen, "the reply must come back untouched and the 49F function must reach no bucket of its own")
    reset()
    entry().handle(event(selected="49financial"))
    need("49financial" in seen and not calls, "the 49F path must be unchanged and never forward")
    for sel in ("inflection", "opal-capital2"):
        reset()
        o = entry().handle(event(selected=sel))
        need("FIRM_BINDING" in json.dumps(o, default=str) and not calls, "%s must be refused FIRM_BINDING and never forwarded" % sel)
    reset()
    o = entry().handle(event(**{"x-origin-verify": "forged"}))
    need(not calls and "FIRM_BINDING" in json.dumps(o, default=str), "a non-internal caller must be refused before the forward")
    reset()
    entry(row={"status": "active", "allowedFirmIds": ["49financial"]}).handle(event())
    need(not calls, "the allowed-firm narrowing must apply BEFORE the forward")
    reset()
    entry(row={"status": "active", "allowedFirmIds": ["cottonwood"]}).handle(event())
    need(len(calls) == 1, "a caller allowed cottonwood must be forwarded")
    reset()

    def boom(name, e):
        raise RuntimeError("secret " + MARK)
    o = entry(invoke=boom).handle(event())
    text = json.dumps(o, default=str)
    need("NOT_READY" in text and MARK not in text and "secret" not in text, "a forward failure must answer NOT_READY and leak nothing")
    reset()
    buf_out, buf_err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        entry().handle(event(**{"x-marker": MARK}))
    need(MARK not in buf_out.getvalue() + buf_err.getvalue(), "the forward must not print the event or the body")
    os.environ.pop(ENVNAME)
    reset()
    o = entry().handle(event())
    need("FIRM_BINDING" in json.dumps(o, default=str) and not calls, "without the environment name the forward must be refused")
    # the target: no forward environment, map holding cottonwood, a forged forwarder field admits nothing
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps({"cottonwood": "b-cot"})
    reset()
    forged = event(**{"x-origin-verify": "forged"})
    forged["forwarded_by"] = "irpt-49f-reporting-read-lambda"
    forged["requestContext"] = {"forwarded": True, "internal": True}
    o = entry().handle(forged)
    need(not seen and not calls and "FIRM_BINDING" in json.dumps(o, default=str), "a forged forward must be refused by the target's own guard")
    genuine = event()
    entry().handle(genuine)
    first = list(seen)
    reset()
    entry().handle(dict(genuine, forwarded_by="irpt-49f-reporting-read-lambda"))
    need(seen == first == ["cottonwood"], "a forwarder field must change nothing for the target: admitted by the signed headers alone")
    return True


# ------------------------------------------------------------------------------------------------ AC3
def check_tests(root):
    root = Path(root)
    new = set()
    for f in (root / TESTS).glob("test_forward_cottonwood*.py"):
        new |= set(re.findall(r"^def (test_\w+)\(", f.read_bytes().decode("utf-8"), flags=re.M))
    need(len([n for n in new if "forward" in n]) >= 6, "at least six NEW tests carry forward in their name, found %s" % sorted(new))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", str(root / TESTS.rstrip("/"))], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-500:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB185-1-AC1": check_diff, "DB185-1-AC2": check_behaviour, "DB185-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    served = ref / SERVED
    s0 = served.read_bytes()
    txt = s0.decode("utf-8")
    muts = {
        "the narrowing is skipped": ("            if forward_to:\n                return self._forward(event, forward_to, operation)\n", ""),
        "forwards without the env check": ("                if not forward_to:\n                    return refuse(operation or self.function_name, None, \"FIRM_BINDING\")\n", ""),
        "a failure leaks the class": ("            return refuse(operation or self.function_name, None, \"NOT_READY\")\n\n    def handle", "            raise\n\n    def handle"),
        "the event is edited": ("                return self.forward_invoke(function_name, event)\n", "                event['forwarded'] = True\n                return self.forward_invoke(function_name, event)\n"),
        "the body is printed": ("            return json.loads(reply[\"Payload\"].read())\n", "            print(reply)\n            return json.loads(reply[\"Payload\"].read())\n"),
    }
    n = 0
    try:
        for label, (a, b) in muts.items():
            need(a in txt, "selftest: the reference lacks the anchor for '%s'" % label)
            served.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
                check_diff(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                continue
            raise AssertionError("mutant passed: " + label)
    finally:
        served.write_bytes(s0)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB185-1-AC1": "OK: only served.py and the new test file changed; the forward map is a literal one entry; _forward logs nothing and edits no event",
               "DB185-1-AC2": "OK: cottonwood is forwarded once with the original event and the reply untouched; the 49F path is unchanged; other firms, a non-internal caller, a missing environment and an unlisted caller are refused; a failure is NOT_READY; nothing is printed; a forged forwarder field admits nothing",
               "DB185-1-AC3": "OK: six or more new forward tests exist and the whole _authz test directory passes"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
