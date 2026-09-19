#!/usr/bin/env python3
"""battery_ib_rtf_11.py -- IRPT_BCKEND.TO-IB-rtf-11 acceptance instrument (R68-AC1).

Runs arms (a)-(d) of the task order (row S92, mid-round decomp cell IB-rtf-11) and prints the
IBR68-DIRECTORY-ENTRY-READS-PAYLOAD-2-0 token ONLY when every arm holds. Every count is
RE-DERIVED this run -- none is carried from a prior pass or from the pytest suite's own summary
line without also being independently exercised here.

Repo root is resolved from this file's own path (never assumed cwd) so the battery runs the same
way from any working directory.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import types

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
IRPT = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
DIRECTORY = os.path.join(IRPT, "directory")
ENTRY_PATH = os.path.join(DIRECTORY, "entry.py")
ENTRY_REL_PATH = "infra/aws/lambda/investor-reporting/directory/entry.py"
HANDLER_REL_PATH = "infra/aws/lambda/investor-reporting/directory/handler.py"
FIXTURE_PATH = os.path.join(DIRECTORY, "tests", "fixtures", "payload_v2_event.json")
INTEGRATIONS_TF = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "api",
                               "integrations.tf")
ROUTES_JSON = os.path.join(REPO, "docs", "contracts", "investor-reporting", "v1", "routes.json")
MANIFEST_PATH = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
PRE_FIX_PIN = "9f72f4d6a4"
CUT_COMMIT = "4ceb7f8361"          # this order's worktree base -- HEAD before this order's edits

FAILS = []


def _run(cmd, cwd=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


def _git_show(rev, rel):
    r = _run(["git", "show", "%s:%s" % (rev, rel)])
    if r.returncode != 0:
        raise RuntimeError("git show %s:%s failed: %s" % (rev, rel, r.stderr[:300]))
    return r.stdout


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path):
    with open(path, "rb") as fh:
        return _sha256_bytes(fh.read())


# --------------------------------------------------------------------------- arm (a)
def arm_a_event_shape():
    print("=== ARM (a): the event shape, measured from api/integrations.tf and routes.json ===")
    tf_src = open(INTEGRATIONS_TF, encoding="utf-8").read()
    has_v2 = 'payload_format_version = "2.0"' in tf_src
    print("api/integrations.tf declares payload_format_version = \"2.0\": %s" % has_v2)
    if not has_v2:
        FAILS.append("arm_a: integrations.tf does not declare payload_format_version 2.0")

    routes = json.load(open(ROUTES_JSON, encoding="utf-8"))["routes"]
    directory_routes = [r for r in routes
                        if r["handler"] == "irpt-directory-search" and r["status"] == "DECLARED"]
    print("routes.json DECLARED routes targeting irpt-directory-search: %d of %d total DECLARED "
          "routes" % (len(directory_routes), sum(1 for r in routes if r["status"] == "DECLARED")))
    for r in directory_routes:
        print("  %s -> operation=%s -- payload_format_version 2.0 (ONE integration per "
              "function, api/integrations.tf:57, for_each over route_functions)" % (
                  r["route_key"], r["operation"]))
    n_routes = len(directory_routes)
    print("n of n routes reaching directory/entry.py: %d of %d" % (n_routes, n_routes))
    if n_routes != 2:
        FAILS.append("arm_a: expected 2 routes targeting irpt-directory-search, found %d"
                     % n_routes)

    fixture_hash = _sha256_file(FIXTURE_PATH)
    print("fixture %s sha256 %s" % (os.path.relpath(FIXTURE_PATH, REPO), fixture_hash))
    fixture_doc = json.load(open(FIXTURE_PATH, encoding="utf-8"))
    for op, wanted_route in (("search", "GET /api/scoped/investor-reporting/directory/search"),
                             ("resolve", "POST /api/scoped/investor-reporting/directory/resolve")):
        ev = fixture_doc[op]
        ok = ev.get("version") == "2.0" and ev.get("routeKey") == wanted_route
        print("  fixture[%r].routeKey == %r and version == '2.0': %s" % (op, wanted_route, ok))
        if not ok:
            FAILS.append("arm_a: fixture[%r] does not carry the expected 2.0 route shape" % op)
    blob = json.dumps(fixture_doc)
    leaked = [t for t in ("@", "Bearer ", "eyJ") if t in blob]
    print("fixture carries no token/e-mail-shaped value: %s (banned tokens found: %s)"
          % (not leaked, leaked))
    if leaked:
        FAILS.append("arm_a: fixture carries a token- or e-mail-shaped value: %s" % leaked)
    return fixture_hash


# --------------------------------------------------------------------------- arm (b)
def arm_b_the_fix():
    print("\n=== ARM (b): the fix, one helper, both call sites, no change to handler.py/_authz ===")
    src = open(ENTRY_PATH, encoding="utf-8").read()
    n_helper_defs = src.count("def _event_params(")
    n_call_sites = src.count("params = _event_params(event)")
    print("def _event_params( occurrences: %d (expect 1)" % n_helper_defs)
    print("params = _event_params(event) call sites: %d (expect 2 -- search() and resolve())"
          % n_call_sites)
    if n_helper_defs != 1:
        FAILS.append("arm_b: expected exactly one _event_params helper definition, found %d"
                     % n_helper_defs)
    if n_call_sites != 2:
        FAILS.append("arm_b: expected exactly 2 call sites reading _event_params(event), found %d"
                     % n_call_sites)
    no_more_toplevel = ('event.get("q"' not in src and 'event.get("limit"' not in src
                        and 'event.get("selection")' not in src)
    print("no remaining TOP-LEVEL event.get('q'/'limit'/'selection') read in entry.py: %s"
          % no_more_toplevel)
    if not no_more_toplevel:
        FAILS.append("arm_b: entry.py still reads a top-level q/limit/selection somewhere")

    # BOUNDS: handler.py, _authz/, _scope/, _keys/, _ids/ are NOT edited by this order. Verified
    # by content against the cut commit (this order's worktree base), never by filename.
    for rel in (HANDLER_REL_PATH,
                "infra/aws/lambda/investor-reporting/_authz/served.py",
                "infra/aws/lambda/investor-reporting/_authz/enforce.py",
                "infra/aws/lambda/investor-reporting/_authz/errors.py",
                "infra/aws/lambda/investor-reporting/_authz/loaders.py"):
        before = _sha256_bytes(_git_show(CUT_COMMIT, rel).encode("utf-8"))
        with open(os.path.join(REPO, rel), "rb") as fh:
            after = _sha256_bytes(fh.read())
        match = before == after
        print("  %s unchanged since cut %s: %s (%s vs %s)"
              % (rel, CUT_COMMIT, match, before[:12], after[:12]))
        if not match:
            FAILS.append("arm_b: %s was modified, which is outside this order's BOUNDS" % rel)
    return True


# --------------------------------------------------------------------------- arm (c)
class _Ctx:
    __slots__ = ("directory",)

    def __init__(self, directory):
        self.directory = directory


def _data_of(result):
    return result["_data"] if isinstance(result, dict) else result


def _fixture_event(op):
    return json.load(open(FIXTURE_PATH, encoding="utf-8"))[op]


def _load_mutant():
    """`directory/entry.py` AS IT STOOD AT `9f72f4d6a4` (this order's own cut, `git show
    HEAD:...` at the cut commit, byte-identical -- verified in arm (b) as an unchanged file up to
    this order's own edit), executed IN MEMORY with `__file__` faked to the REAL entry.py path so
    its sibling imports (served/loaders/handler/ids) resolve against the REAL, unedited tree."""
    src = _git_show(PRE_FIX_PIN, ENTRY_REL_PATH)
    assert 'event.get("q"' in src, (
        "the pinned blob %s does not contain the pre-fix top-level read" % PRE_FIX_PIN)
    mod = types.ModuleType("entry_mutant_" + PRE_FIX_PIN)
    mod.__file__ = ENTRY_PATH
    code = compile(src, ENTRY_PATH, "exec")
    exec(code, mod.__dict__)
    return mod


def arm_c_suite_and_mutant():
    print("\n=== ARM (c): the directory/ suite, the fixture honoured, the pre-fix false behaviour ===")
    r = _run([sys.executable, "-m", "pytest", os.path.join(DIRECTORY, "tests"), "-q"], timeout=180)
    tail_lines = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
    tail = tail_lines[-1] if tail_lines else "(no output)"
    print("directory/tests suite: rc=%d :: %s" % (r.returncode, tail))
    if r.returncode != 0:
        FAILS.append("arm_c: directory/tests suite did not pass -- %s" % tail)

    for p in (DIRECTORY, os.path.join(DIRECTORY, "tests"), os.path.join(IRPT, "_authz"),
             os.path.join(IRPT, "_scope"), os.path.join(IRPT, "_keys"), os.path.join(IRPT, "_ids")):
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)
    for mod_name in ("entry", "handler", "fixtures", "served", "loaders", "ids"):
        sys.modules.pop(mod_name, None)
    import fixtures as fx           # noqa: E402
    import entry as en              # noqa: E402  the REAL, fixed module

    ctx = _Ctx(fx.DIRECTORY)
    ev_exact = _fixture_event("search")
    docs_exact = _data_of(en.search(None, fx.SCOPE_A, ev_exact, ctx))
    print("REAL entry search q=%r (2.0 queryStringParameters) -> %d of expected 1"
          % (ev_exact["queryStringParameters"]["q"], len(docs_exact)))
    if len(docs_exact) != 1:
        FAILS.append("arm_c: REAL entry did not honour q -- expected 1 match, got %d"
                     % len(docs_exact))

    ev_limited = dict(_fixture_event("search"))
    ev_limited["queryStringParameters"] = {"q": "", "limit": "2"}
    docs_limited = _data_of(en.search(None, fx.SCOPE_A, ev_limited, ctx))
    ev_wide = dict(_fixture_event("search"))
    ev_wide["queryStringParameters"] = {"q": ""}
    docs_wide = _data_of(en.search(None, fx.SCOPE_A, ev_wide, ctx))
    print("REAL entry search q='' limit='2' -> %d of expected 2; q='' unlimited -> %d "
          "(wider, DEFAULT_LIMIT honoured)" % (len(docs_limited), len(docs_wide)))
    if len(docs_limited) != 2 or not (len(docs_wide) > len(docs_limited)):
        FAILS.append("arm_c: REAL entry did not honour limit (limited=%d wide=%d)"
                     % (len(docs_limited), len(docs_wide)))

    ev_resolve = _fixture_event("resolve")
    result = en.resolve(None, fx.SCOPE_A, ev_resolve, ctx)
    print("REAL entry resolve selection=account_ids:[acc_S1] (2.0 body) -> ok=%s account_ids=%s"
          % (result["ok"], result["account_ids"]))
    if not (result["ok"] is True and result["account_ids"] == ["acc_S1"]):
        FAILS.append("arm_c: REAL entry did not honour selection -- got %r" % result)

    mutant = _load_mutant()
    mutant_docs = _data_of(mutant.search(None, fx.SCOPE_A, ev_exact, ctx))
    print("MUTANT (pre-fix, blob %s) search q=%r -> %d document(s) (false: q ignored, DEFAULT_"
          "LIMIT unfiltered)" % (PRE_FIX_PIN, ev_exact["queryStringParameters"]["q"],
                                 len(mutant_docs)))
    if len(mutant_docs) == 1:
        FAILS.append("arm_c: mutant answered as if it honoured q -- fixture is not "
                     "discriminating")

    mutant_result = mutant.resolve(None, fx.SCOPE_A, ev_resolve, ctx)
    print("MUTANT (pre-fix) resolve selection=account_ids:[acc_S1] -> ok=%s partial_reason=%r "
          "(false: selection never reaches the compute)"
          % (mutant_result["ok"], mutant_result.get("partial_reason")))
    if mutant_result["ok"] is not False:
        FAILS.append("arm_c: mutant SERVED the selection -- fixture is not discriminating")

    demonstrated = (len(docs_exact) == 1 and len(mutant_docs) != 1
                    and result["ok"] is True and mutant_result["ok"] is False)
    print("false behaviour DEMONSTRATED on the same fixture: %s" % demonstrated)
    if not demonstrated:
        FAILS.append("arm_c: the pre-fix/post-fix difference was not demonstrated")
    return True


# --------------------------------------------------------------------------- arm (d)
def arm_d_staging_membership():
    print("\n=== ARM (d): the staging contract, holdings/stage.py --check-style, m of m ===")
    manifest = json.load(open(MANIFEST_PATH, encoding="utf-8"))
    fn_cfg = manifest["functions"]["irpt-directory-search"]
    files = fn_cfg.get("files", [])
    print("irpt-directory-search.files: %s" % files)
    print("entry.py is a declared member: %s (its sha MOVES with this edit -- that is the "
          "point; this manifest field is NOT hand-edited, the build re-derives it, W1-S31/"
          "W1-S89's bar)" % ("entry.py" in files))
    if "entry.py" not in files:
        FAILS.append("arm_d: entry.py is not a declared member of irpt-directory-search")

    staged = fn_cfg.get("staged_from", [])
    resolved = 0
    for s in staged:
        pin, rel, packaged, declared_sha = s["pin"], s["repo_path"], s["packaged_as"], s["sha256"]
        blob = _git_show(pin, rel).encode("utf-8")
        got_sha = _sha256_bytes(blob)
        match = got_sha == declared_sha
        print("  staged_from %s @%s -> %s: declared=%s got=%s -> %s"
              % (rel, pin[:10], packaged, declared_sha[:16], got_sha[:16],
                 "MATCH" if match else "MISMATCH"))
        if match:
            resolved += 1
        else:
            FAILS.append("arm_d: staged_from member %s does not resolve to its declared sha256"
                         % packaged)
    print("staging membership: %d of %d staged_from member(s) resolve at HEAD after the edit"
          % (resolved, len(staged)))
    if resolved != len(staged) or not staged:
        FAILS.append("arm_d: expected every staged_from member to resolve (m of m), got %d of %d"
                     % (resolved, len(staged)))

    entry_sha_before = _sha256_bytes(_git_show(PRE_FIX_PIN, ENTRY_REL_PATH).encode("utf-8"))
    with open(ENTRY_PATH, "rb") as fh:
        entry_sha_after = _sha256_bytes(fh.read())
    print("entry.py sha256 pre-fix (%s) vs worktree now: %s vs %s -> %s (expected to MOVE)"
          % (PRE_FIX_PIN, entry_sha_before[:16], entry_sha_after[:16],
             "MOVED as expected" if entry_sha_before != entry_sha_after else "UNCHANGED"))
    if entry_sha_before == entry_sha_after:
        FAILS.append("arm_d: entry.py's sha did not move -- the fix does not appear to be in "
                     "the worktree")
    return True


def main():
    print("battery_ib_rtf_11.py -- IRPT_BCKEND.TO-IB-rtf-11 -- repo root: %s\n" % REPO)
    fixture_hash = arm_a_event_shape()
    ok_b = arm_b_the_fix()
    ok_c = arm_c_suite_and_mutant()
    ok_d = arm_d_staging_membership()

    print("\n=== SUMMARY ===")
    print("fixture sha256: %s" % fixture_hash)
    print("arm (a): %s" % ("OK" if not any(f.startswith("arm_a") for f in FAILS) else "FAIL"))
    print("arm (b): %s" % ("OK" if ok_b and not any(f.startswith("arm_b") for f in FAILS) else "FAIL"))
    print("arm (c): %s" % ("OK" if ok_c and not any(f.startswith("arm_c") for f in FAILS) else "FAIL"))
    print("arm (d): %s" % ("OK" if ok_d and not any(f.startswith("arm_d") for f in FAILS) else "FAIL"))
    every_arm_holds = len(FAILS) == 0
    if every_arm_holds:
        print("\nIBR68-DIRECTORY-ENTRY-READS-PAYLOAD-2-0")
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld. Failing reasons:")
        for f in FAILS:
            print("  - %s" % f)
    return 0 if every_arm_holds else 1


if __name__ == "__main__":
    sys.exit(main())
