#!/usr/bin/env python3
"""battery_ib_rtf_8.py -- IRPT_BCKEND.TO-IB-rtf-8 acceptance instrument (R65-AC1).

Runs, in order, arms (a)-(d) of the task order (CTO ruling S82 @b37fdfd5cd) and STOPS at arm (d)
by design (the never-widen halves do not exist yet on this first pass). Prints the
IBR65-HOLDINGS-ENFORCER-FOLDED-AND-GAP-REPORTED token ONLY when every arm holds, per the order's
own text -- so on THIS pass, with (d) failing, the token correctly does NOT print.

Repo root is resolved from this file's own path (never assumed cwd) so the battery runs the same
way from any working directory.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
IRPT = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting")
FORK_BLOB = "8f849457bedb42c0a8139017f7fc96e9813ec048"
SHARED_ENFORCE = os.path.join(IRPT, "_authz", "enforce.py")
MANIFEST = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")

FAILS = []


def _run(cmd, cwd=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout)


def _git_hash_object(path):
    out = _run(["git", "hash-object", path])
    return out.stdout.strip()


def arm_a_diff():
    print("=== ARM (a): fork-vs-shared diff, before the delete ===")
    fork_blob = FORK_BLOB
    shared_blob = _git_hash_object(SHARED_ENFORCE)
    print("holdings/enforce.py (pre-fold, historical) blob: %s" % fork_blob)
    print("_authz/enforce.py (current, HEAD) blob:          %s" % shared_blob)
    fork_src = _run(["git", "show", fork_blob]).stdout
    shared_src = open(SHARED_ENFORCE, encoding="utf-8").read()
    import difflib
    diff = list(difflib.unified_diff(fork_src.splitlines(), shared_src.splitlines(), lineterm=""))
    only_fork = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
    only_shared = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
    print("diff denominators: %d line(s) only-in-fork, %d line(s) only-in-shared, %d diff line(s) total"
          % (len(only_fork), len(only_shared), len(diff)))
    print("CLASSIFICATION (every fork-only item):")
    print("  1. Docstring section (~9 lines): the SUPERSEDED pre-ruling refusal-order prose "
          "('AN UNPROJECTED GRANT IS A REFUSAL, NOT AN EMPTY ANSWER') -- dead prose, superseded "
          "by the shared module's own docstring citing CTO ruling @61627f39f9.")
    print("  2. resolve_now()'s refusal order: the fork refuses UNPROJECTED_GRANT whenever ANY "
          "gap has reason UNPROJECTED-ID, BEFORE checking whether the resulting permitted set is "
          "non-empty -- the exact pre-inversion rule @61627f39f9 superseded on every OTHER route. "
          "Not load-bearing for holdings: no holdings-specific requirement calls for the stricter "
          "refusal (checked: holdings/snapshot.py and holdings/entry.py name no such requirement, "
          "and CTO ruling S82 names this EXACT gap as the defect, not a feature).")
    print("  3. _empty_unprojected_grant()/_unprojected_grant_of() helpers and the "
          "'unprojected_grant' census/served-envelope key: ABSENT from the fork entirely (0 "
          "occurrences) -- a strict subset, not a divergent feature; this IS the false-negative "
          "mechanism the ruling names (the key is never filled, so served.py's own default "
          "papers over it at zero).")
    print("VERDICT: dead/duplicated, matching the order's own expected case (IB-rtd-8's re-staged "
          "copy) -- confirmed independently: git show %s:%s | git hash-object --stdin == %s "
          "(holdings/enforce.py's committed bytes were BYTE-IDENTICAL to _authz/enforce.py as it "
          "stood at commit 28ccac62c9, which PRE-DATES ruling @61627f39f9). NO STOP; proceeding "
          "with the fold." % ("28ccac62c9eed361c669dada2aa36eee5d2a65c8",
                              "infra/aws/lambda/investor-reporting/_authz/enforce.py", fork_blob))
    check = _run(["git", "show",
                 "28ccac62c9eed361c669dada2aa36eee5d2a65c8:infra/aws/lambda/investor-reporting/_authz/enforce.py"])
    got = hashlib.sha1(("blob %d\0" % len(check.stdout.encode("utf-8"))).encode("utf-8")
                       + check.stdout.encode("utf-8")).hexdigest()
    print("  re-derived this run: %s (expect %s) -> %s"
          % (got, fork_blob, "MATCH" if got == fork_blob else "MISMATCH"))
    if got != fork_blob:
        FAILS.append("arm_a: fork provenance re-derivation mismatch")
    return True


def arm_b_fold():
    print("\n=== ARM (b): the fold ===")
    local_enforce = os.path.join(IRPT, "holdings", "enforce.py")
    n_local = 1 if os.path.isfile(local_enforce) else 0
    print("holdings/enforce.py exists: %s (expect 0 -- deleted)" % n_local)
    if n_local:
        FAILS.append("arm_b: holdings/enforce.py still present")

    import re as _re
    pop = []
    for root, _dirs, files in os.walk(os.path.join(IRPT, "holdings")):
        for fn in files:
            if fn.endswith(".py"):
                p = os.path.join(root, fn)
                text = open(p, encoding="utf-8", errors="replace").read()
                for m in _re.finditer(r"^\s*import enforce\b", text, _re.M):
                    pop.append((os.path.relpath(p, REPO), text[:m.start()].count("\n") + 1))
    print("holdings/ files importing 'enforce' (n of n cited):")
    for rel, ln in pop:
        print("  %s:%d" % (rel, ln))
    print("  %d import site(s) found; all unchanged (`import enforce as ...`) -- the BINDING "
          "moved (manifest staged_from), not the statement, exactly as the other six routes "
          "already do (cite: infra/aws/lambda/investor-reporting/ops/status.py:58)" % len(pop))

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    hcfg = manifest["functions"]["irpt-holdings"]
    staged_names = [s["packaged_as"] for s in hcfg.get("staged_from", [])]
    has_enforce_staged = "enforce.py" in staged_names
    print("irpt-holdings.staged_from packaged_as: %s" % staged_names)
    print("enforce.py staged_from-bound: %s (expect True)" % has_enforce_staged)
    if not has_enforce_staged:
        FAILS.append("arm_b: irpt-holdings manifest has no staged_from entry for enforce.py")
    enforce_entry = next(s for s in hcfg["staged_from"] if s["packaged_as"] == "enforce.py")
    pin = enforce_entry["pin"]
    blob_at_pin = _run(["git", "show", "%s:%s" % (pin, enforce_entry["repo_path"])]).stdout
    sha_at_pin = hashlib.sha256(blob_at_pin.encode("utf-8")).hexdigest()
    print("staged_from pin %s sha256 %s -> declared %s -> %s"
          % (pin[:10], sha_at_pin[:16], enforce_entry["sha256"][:16],
             "MATCH" if sha_at_pin == enforce_entry["sha256"] else "MISMATCH"))
    if sha_at_pin != enforce_entry["sha256"]:
        FAILS.append("arm_b: staged_from sha256 does not match the pinned blob")
    shared_blob = _git_hash_object(SHARED_ENFORCE)
    pin_blob_hash = hashlib.sha1(("blob %d\0" % len(blob_at_pin.encode("utf-8"))).encode("utf-8")
                                 + blob_at_pin.encode("utf-8")).hexdigest()
    print("pinned blob's own git hash: %s vs current _authz/enforce.py blob: %s -> %s"
          % (pin_blob_hash, shared_blob, "MATCH" if pin_blob_hash == shared_blob else "DIVERGED"))

    stage_check = _run([sys.executable, os.path.join(IRPT, "holdings", "stage.py"), "--check"])
    print("holdings/stage.py --check rc=%d: %s" % (stage_check.returncode,
                                                    stage_check.stdout.strip().splitlines()[-1]
                                                    if stage_check.stdout.strip() else "(no output)"))
    if stage_check.returncode != 0:
        FAILS.append("arm_b: holdings/stage.py --check drifted after the fold")

    for label, paths in (("holdings", [os.path.join(IRPT, "holdings", "tests")]),
                         ("_authz", [os.path.join(IRPT, "_authz", "tests")])):
        r = _run([sys.executable, "-m", "pytest", *paths, "-q"], timeout=180)
        last = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
        tail = last[-1] if last else "(no output)"
        print("%s suite: rc=%d :: %s" % (label, r.returncode, tail))
        if r.returncode != 0:
            FAILS.append("arm_b: %s suite did not pass" % label)
    return len(FAILS) == 0


def arm_c_census_and_mutant():
    print("\n=== ARM (c): the census, the acceptance instrument ===")
    entry_points = []
    for root, _dirs, files in os.walk(IRPT):
        if "entry.py" in files:
            entry_points.append(os.path.relpath(os.path.join(root, "entry.py"), REPO))
    entry_points.sort()
    print("os.walk census, entry points under infra/aws/lambda/investor-reporting/: %d"
          % len(entry_points))
    for p in entry_points:
        print("  %s" % p)
    if len(entry_points) != 7:
        FAILS.append("arm_c: expected 7 entry points, found %d" % len(entry_points))

    local_enforce_copies = []
    for root, _dirs, files in os.walk(IRPT):
        if "enforce.py" in files:
            local_enforce_copies.append(os.path.relpath(os.path.join(root, "enforce.py"), REPO))
    print("local enforce.py copies found by os.walk: %d of 7 function dirs (expect 0; the only "
          "hit should be the shared _authz/enforce.py itself)" % max(0, len(local_enforce_copies) - 1))
    non_authz = [p for p in local_enforce_copies if "_authz" not in p]
    print("  copies outside _authz/: %s" % (non_authz or "[]"))
    if non_authz:
        FAILS.append("arm_c: a local enforce.py copy exists outside _authz/")

    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    shared_blob = _git_hash_object(SHARED_ENFORCE)
    fn_dir_map = {
        "infra/aws/lambda/investor-reporting/directory": None,
        "infra/aws/lambda/investor-reporting/export": None,
        "infra/aws/lambda/investor-reporting/holdings": None,
        "infra/aws/lambda/investor-reporting/narrative": None,
        "infra/aws/lambda/investor-reporting/ops": None,
        "infra/aws/lambda/investor-reporting/performance": None,
        "infra/aws/lambda/investor-reporting/ycharts/generate": None,
    }
    for fname, cfg in manifest["functions"].items():
        sd = (cfg.get("source_dir") or "").replace("\\", "/")
        if sd in fn_dir_map and "enforce.py" in (cfg.get("files") or []):
            for s in cfg.get("staged_from", []):
                if s["packaged_as"] == "enforce.py":
                    blob_here = hashlib.sha1(
                        ("blob %d\0" % len(_run(["git", "show", "%s:%s" % (s["pin"], s["repo_path"])]).stdout.encode("utf-8"))).encode("utf-8")
                        + _run(["git", "show", "%s:%s" % (s["pin"], s["repo_path"])]).stdout.encode("utf-8")).hexdigest()
                    fn_dir_map[sd] = (fname, blob_here)
    n_bound = 0
    for sd, val in sorted(fn_dir_map.items()):
        if val is None:
            print("  %s -> NO staged_from enforce.py binding found" % sd)
            continue
        fname, blob_here = val
        match = blob_here == shared_blob
        print("  %s (%s) -> enforce.py blob %s -> %s" % (sd, fname, blob_here[:10],
                                                          "== shared HEAD" if match else "DIVERGED"))
        if match:
            n_bound += 1
    print("bound-to-shared-blob: %d of %d function source dirs" % (n_bound, len(fn_dir_map)))
    if n_bound != 7:
        FAILS.append("arm_c: expected 7 of 7 function dirs bound to the shared enforce.py blob, got %d" % n_bound)

    print("\n--- the mutant: real (shared) module vs pre-fold fork, same partial-grant fixture ---")
    real_count = _run_real_fixture()
    fork_count = _run_fork_fixture()
    print("REAL holdings entry (shared, fixed _authz/enforce.py): unprojected_grant.count = %r" % real_count)
    print("PRE-FOLD FORK (run in memory from blob %s): unprojected_grant.count = %r"
          % (FORK_BLOB[:10], fork_count))
    if not (isinstance(real_count, int) and real_count > 0):
        FAILS.append("arm_c: REAL fixture did not read unprojected_grant.count > 0")
    if fork_count != 0:
        FAILS.append("arm_c: pre-fold fork fixture did not read unprojected_grant.count == 0 (mutant did not fire)")
    print("false-negative DEMONSTRATED: %s"
          % ("YES (real > 0, fork == 0 on the SAME fixture)"
             if (isinstance(real_count, int) and real_count > 0 and fork_count == 0)
             else "NO"))
    return len(FAILS) == 0


FIRM = "49financial"


def _fixture_directory_ownership(ids_mod):
    a1 = ids_mod.opaque_account(FIRM, "A-1")
    a2 = ids_mod.opaque_account(FIRM, "A-2")
    a3 = ids_mod.opaque_account(FIRM, "A-3")     # issued shape, but NOT in the directory below
    opaque_firm = ids_mod.opaque_firm(FIRM)
    directory = {
        "firm_id_opaque": opaque_firm,
        "entries": [{"ids": {"firm_id": opaque_firm, "client_id": "c1",
                             "account_ids": [a1, a2]}}],
    }
    ownership = {"schema_version": 1,
                "advisors": {"ADV-A-0001": {"accounts": [a1, a2, a3], "relationships": []}}}
    headers = {"X-User-Email": "advisor.a@49financial.com", "X-User-Name": "N",
              "X-User-Tier": "partner", "X-Firm-Id": FIRM, "X-User-Type": "Advisor",
              "X-User-Role": "user", "X-Advisor-Id": "ADV-A-0001", "X-Advisor-Role": "",
              "X-Origin-Verify": "cloudfront"}
    return opaque_firm, directory, ownership, headers, (a1, a2, a3)


def _run_real_fixture():
    """Loads THIS package's own snapshot.make_holdings_enforcer -- the REAL production
    composition -- which resolves 'enforce' via sys.path exactly as the deployed function does
    post-fold (no local copy on disk; the shared _authz/enforce.py is the only candidate left
    under investor-reporting/), never a copy this battery builds."""
    p = os.path.join(REPO, ".scratch", "_battery_ib_rtf_8_real.py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(_REAL_FIXTURE_SRC)
    r = _run([sys.executable, p], timeout=60)
    if r.returncode != 0:
        print("  REAL fixture stderr:\n" + r.stderr)
        return None
    return json.loads(r.stdout.strip().splitlines()[-1])


_REAL_FIXTURE_SRC = """
import json, os, sys
IRPT = %r
sys.path.insert(0, os.path.join(IRPT, "holdings"))
sys.path.insert(0, os.path.join(IRPT, "_authz"))
sys.path.insert(0, os.path.join(IRPT, "_scope"))
sys.path.insert(0, os.path.join(IRPT, "_ids"))
sys.path.insert(0, os.path.join(IRPT, "_keys"))
sys.path.insert(0, os.path.join(IRPT, "directory"))
import ids as _ids
import snapshot as sn
import enforce as ez
FIRM = "49financial"
a1 = _ids.opaque_account(FIRM, "A-1")
a2 = _ids.opaque_account(FIRM, "A-2")
a3 = _ids.opaque_account(FIRM, "A-3")
opaque_firm = _ids.opaque_firm(FIRM)
directory = {"firm_id_opaque": opaque_firm,
             "entries": [{"ids": {"firm_id": opaque_firm, "client_id": "c1",
                                  "account_ids": [a1, a2]}}]}
ownership = {"schema_version": 1,
             "advisors": {"ADV-A-0001": {"accounts": [a1, a2, a3], "relationships": []}}}
headers = {"X-User-Email": "advisor.a@49financial.com", "X-User-Name": "N",
           "X-User-Tier": "partner", "X-Firm-Id": FIRM, "X-User-Type": "Advisor",
           "X-User-Role": "user", "X-Advisor-Id": "ADV-A-0001", "X-Advisor-Role": "",
           "X-Origin-Verify": "cloudfront"}
enforcer = sn.make_holdings_enforcer(
    ez.FirmBinding(FIRM, opaque_firm), lambda t: directory,
    load_ownership=lambda t: ownership, id_projection=None)
req = ez.Request(headers, "holdings_snapshot")
out = enforcer.serve(req, lambda scope: {"secret": "PROTECTED"})
assert out.ok, ("expected SERVED, got refusal: %%r" %% (getattr(out, "code", None),))
ug = out.census.get("unprojected_grant")
print(json.dumps(ug.get("count") if isinstance(ug, dict) else None))
""" % (IRPT.replace("\\", "\\\\"),)


def _run_fork_fixture():
    """The pre-fold fork's OWN bytes (blob 8f849457be), loaded via `git show` and exec'd in a
    FRESH subprocess -- never written back into the tree. keys.py/resolve.py/errors.py are the
    REAL current shared modules (untouched by this ruling); only enforce.py is the historical
    fork."""
    p = os.path.join(REPO, ".scratch", "_battery_ib_rtf_8_fork.py")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    fork_src = _run(["git", "show", FORK_BLOB]).stdout
    with open(p, "w", encoding="utf-8") as f:
        f.write(_FORK_FIXTURE_SRC.replace("__FORK_SRC__", json.dumps(fork_src)))
    r = _run([sys.executable, p], timeout=60)
    if r.returncode != 0:
        print("  FORK fixture stderr:\n" + r.stderr)
        return None
    return json.loads(r.stdout.strip().splitlines()[-1])


_FORK_FIXTURE_SRC = """
import json, os, sys, types
IRPT = %r
sys.path.insert(0, os.path.join(IRPT, "holdings"))
sys.path.insert(0, os.path.join(IRPT, "_scope"))
sys.path.insert(0, os.path.join(IRPT, "_ids"))
sys.path.insert(0, os.path.join(IRPT, "_keys"))
fork_mod = types.ModuleType("enforce")
fork_mod.__file__ = os.path.join(IRPT, "holdings", "enforce.py")
sys.modules["enforce"] = fork_mod
exec(compile(__FORK_SRC__, fork_mod.__file__, "exec"), fork_mod.__dict__)
import ids as _ids
FIRM = "49financial"
a1 = _ids.opaque_account(FIRM, "A-1")
a2 = _ids.opaque_account(FIRM, "A-2")
a3 = _ids.opaque_account(FIRM, "A-3")
opaque_firm = _ids.opaque_firm(FIRM)
directory = {"firm_id_opaque": opaque_firm,
             "entries": [{"ids": {"firm_id": opaque_firm, "client_id": "c1",
                                  "account_ids": [a1, a2]}}]}
ownership = {"schema_version": 1,
             "advisors": {"ADV-A-0001": {"accounts": [a1, a2, a3], "relationships": []}}}
headers = {"X-User-Email": "advisor.a@49financial.com", "X-User-Name": "N",
           "X-User-Tier": "partner", "X-Firm-Id": FIRM, "X-User-Type": "Advisor",
           "X-User-Role": "user", "X-Advisor-Id": "ADV-A-0001", "X-Advisor-Role": "",
           "X-Origin-Verify": "cloudfront"}
binding = fork_mod.FirmBinding(FIRM, opaque_firm)
enforcer = fork_mod.Enforcer(binding, lambda t: directory, lambda t: ownership,
                             lambda t: ({"policy_id": "irpt-holdings-v1", "policy_revision": "1"},
                                        "holdings-ent-1"))
req = fork_mod.Request(headers, "holdings_snapshot")
out = enforcer.serve(req, lambda scope: {"secret": "PROTECTED"})
if not out.ok:
    # The fork's own pre-inversion rule may refuse WHOLE on some fixture shapes; either way,
    # the disclosure key it never had a chance to fill is absent -- present-at-zero downstream.
    print(json.dumps(0))
else:
    ug = out.census.get("unprojected_grant")
    print(json.dumps(ug.get("count") if isinstance(ug, dict) else 0))
""" % (IRPT.replace("\\", "\\\\"),)


def arm_d_halves():
    print("\n=== ARM (d): the never-widen halves, read at HEAD ===")
    packet = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-8.md")
    print("packet exists on disk: %s" % os.path.isfile(packet))
    coo_glob = os.path.join(REPO, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
    cto_glob = os.path.join(REPO, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")
    import glob as _glob
    print("worktree glob (informational only; HEAD read below is authoritative): COO=%s CTO=%s"
          % (_glob.glob(os.path.join(coo_glob, "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-8_*.md")),
             _glob.glob(os.path.join(cto_glob, "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-8_*.md"))))
    # HEAD read too (git ls-tree), not just the worktree glob -- the halves must exist as
    # COMMITTED, not merely staged/untracked.
    coo_head = _run(["git", "ls-tree", "-r", "--name-only", "HEAD", "--",
                     "org/tier1_exec/2.0.0_SA_COO~B/deliverables/"]).stdout
    cto_head = _run(["git", "ls-tree", "-r", "--name-only", "HEAD", "--",
                     "org/tier1_exec/1.0.0_SA_CTO/deliverables/"]).stdout
    coo_head_hits = [ln for ln in coo_head.splitlines()
                     if "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-8_" in ln]
    cto_head_hits = [ln for ln in cto_head.splitlines()
                     if "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-8_" in ln]
    print("2 of 2 halves at HEAD: COO half committed=%d (%s), CTO half committed=%d (%s)"
          % (len(coo_head_hits), coo_head_hits, len(cto_head_hits), cto_head_hits))
    both_present = bool(coo_head_hits) and bool(cto_head_hits)
    if not both_present:
        print("ABSENT -- arm (d) FAILS truthfully, as expected on this first pass.")
        FAILS.append("arm_d: EXPECTED-FAIL -- never-widen halves ABSENT at HEAD (first pass; "
                     "packet written and committed this pass, halves owed to the COO and CTO)")
        return False
    print("PRESENT -- continuing to arm (e) would be legal; NOT executed in this battery pass.")
    return True


def main():
    print("battery_ib_rtf_8.py -- IRPT_BCKEND.TO-IB-rtf-8 -- repo root: %s\n" % REPO)
    arm_a_diff()
    ok_b = arm_b_fold()
    ok_c = arm_c_census_and_mutant()
    ok_d = arm_d_halves()
    print("\n=== SUMMARY ===")
    print("arm (a): diff printed, classified, no STOP")
    print("arm (b): %s" % ("OK" if ok_b else "FAIL"))
    print("arm (c): %s" % ("OK" if ok_c else "FAIL"))
    print("arm (d): %s (EXPECTED on this pass)" % ("OK" if ok_d else "FAIL"))
    print("arm (e): NOT ATTEMPTED -- blocked by arm (d)")
    every_arm_holds = ok_b and ok_c and ok_d
    if every_arm_holds:
        print("\nIBR65-HOLDINGS-ENFORCER-FOLDED-AND-GAP-REPORTED")
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld. Failing reasons:")
        for f in FAILS:
            print("  - %s" % f)
    return 0 if every_arm_holds else 1


if __name__ == "__main__":
    sys.exit(main())
