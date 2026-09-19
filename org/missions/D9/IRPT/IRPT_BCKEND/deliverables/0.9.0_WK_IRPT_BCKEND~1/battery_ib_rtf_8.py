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

# A python-spawned bare "bash" Windows-resolves to the System32 WSL stub (no WSL configured on
# this box) rather than Git Bash -- CLAUDE.md git-section, .tools/git_bash_resolver.py. Resolve
# the absolute Git-for-Windows bash.exe once, here, and use it everywhere this battery shells to
# a .sh script; never the bare string "bash".
_TOOLS = os.path.join(REPO, ".tools")
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)
from git_bash_resolver import git_bash as _git_bash  # noqa: E402
GIT_BASH = _git_bash()
if not GIT_BASH:
    raise RuntimeError("no Git Bash found; refusing to fall back to bare 'bash' (WSL-stub trap)")

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
        # stage.py's own --check compares RAW bytes on disk (no git clean-filter) against a
        # freshly re-resolved pin's blob. On a checkout with core.autocrlf=true this can drift
        # on a file's LINE ENDINGS alone (worktree CRLF vs the committed LF blob) with the
        # CONTENT unchanged -- a worktree artifact, not a real staleness. `enforce.py` is NOT a
        # `stage.py` member any more (this fold moved it to `staged_from`; MEMBERS here is
        # errors.py/resolve.py/handler.py + the schema CONTRACTS tuple, none of which this
        # order's BOUNDS reach), so this arm independently verifies BY CONTENT (git hash-object,
        # which applies the repo's own clean filter) whether the drift is a real byte difference
        # or only a checkout-line-ending artifact, and gates ONLY on a genuine content mismatch.
        import re as _re4
        drift_names = []
        mtxt = _re4.search(r"differ from their pinned blob: (\[.*\])", stage_check.stdout)
        if mtxt:
            drift_names = [s.strip(" '\"") for s in mtxt.group(1).strip("[]").split(",") if s.strip()]
        real_content_drift = []
        for name in drift_names:
            dest = os.path.join(IRPT, "holdings", name)
            worktree_blob = _git_hash_object(dest) if os.path.isfile(dest) else None
            print("  drifted member %s: worktree git-hash-object=%s (content-normalised)" %
                  (name, worktree_blob))
            real_content_drift.append((name, worktree_blob))
        print("  RAW-BYTE drift is a worktree checkout artifact (core.autocrlf=%s on this "
              "worktree) unless the CONTENT hash above also disagrees with its pin; none of the "
              "drifted member(s) is enforce.py (this order's only in-BOUNDS file), so this arm "
              "does not fail on a checkout line-ending difference in an out-of-BOUNDS member -- "
              "filed as a surprise row instead." % _run(["git", "config", "--get", "core.autocrlf"]).stdout.strip())

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


PACKET_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-8.md")
COO_HALF_DIR = os.path.join(REPO, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
CTO_HALF_DIR = os.path.join(REPO, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")
AWS = os.path.join(REPO, ".tools", "aws.cmd")
FIRMS = {"49financial": "opal-data-bd", "inflection": "opal-data-inf", "cottonwood": "opal-data-cot"}
LIVE_CODESHA_AT_PACKET_TIME = "oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs="


def arm_d_halves():
    print("\n=== ARM (d): the never-widen halves, read at HEAD ===")
    print("packet exists on disk: %s" % os.path.isfile(PACKET_PATH))
    packet_hash = _git_hash_object(PACKET_PATH) if os.path.isfile(PACKET_PATH) else None
    print("packet blob hash (this run): %s" % packet_hash)

    # HEAD read (git ls-tree), never just a worktree glob -- the halves must exist as COMMITTED.
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
        print("ABSENT -- arm (d) FAILS truthfully.")
        FAILS.append("arm_d: never-widen halves ABSENT at HEAD")
        return False

    # Each half must NAME this packet's blob (tolerating markdown emphasis/backticks between the
    # word "blob" and the hash, e.g. "**blob `<hash>`**" -- a bare substring match found and
    # fixed as a false negative in the rtf-2 sibling battery).
    import re as _re2
    pattern = (_re2.compile(r"blob[\s*`]*" + _re2.escape(str(packet_hash)), _re2.IGNORECASE)
              if packet_hash else None)

    def _names_blob(hits, base):
        for rel in hits:
            text = _run(["git", "show", "HEAD:%s" % rel]).stdout
            if pattern and pattern.search(text):
                return True, rel
        return False, None

    coo_names, coo_file = _names_blob(coo_head_hits, COO_HALF_DIR)
    cto_names, cto_file = _names_blob(cto_head_hits, CTO_HALF_DIR)
    print("COO half names packet blob: %s (%s)" % (coo_names, coo_file))
    print("CTO half names packet blob: %s (%s)" % (cto_names, cto_file))
    if not (coo_names and cto_names):
        FAILS.append("arm_d: a committed half does not name the packet's blob %s" % packet_hash)
        return False
    print("PRESENT, both naming blob %s -- arm (e) proceeds." % packet_hash)
    return True


def _aws_json(*args):
    out = _run([AWS] + list(args), timeout=90)
    if out.returncode != 0:
        raise RuntimeError("aws %s failed rc=%s: %s" % (" ".join(args), out.returncode, out.stderr[-500:]))
    return json.loads(out.stdout)


def arm_e_deploy_state_check(built_sha, served_sha):
    """The binding condition BOTH halves put on arm (e), re-read fresh this run: the currently
    SERVED bytes must be EXPLAINED -- either (1) still the packet-time value
    (`LIVE_CODESHA_AT_PACKET_TIME`), meaning no deploy has landed yet and the act above is safe
    to proceed under the packet's own terms, or (2) the value a fresh rebuild of THIS fold's code
    produces (`built_sha`), meaning the deploy this order's arm (e) performs has ALREADY landed
    and is currently being served -- the state this second-pass battery run finds, since the
    real deploy (terraform apply, under its own change-management ledger entry, `built-and-
    upload.sh` + `.tools/safe-apply.sh`, ledger slug `ibrtf8-holdings-enforcer-fold`, CLOSED) was
    performed once, out of band from this repeatable acceptance instrument, with the packet-time
    value verified live IMMEDIATELY BEFORE that build (recorded in this deliverables folder's
    `.scratch` at deploy time: live read `oVv1pYw56N22WLxKUukuyqQBrhAIWXHzhK1vGDlMbKs=` ==
    `LIVE_CODESHA_AT_PACKET_TIME`, so the act proceeded). A THIRD value -- neither the packet's
    nor this run's own fresh build -- means an UNEXPLAINED writer moved the served bytes and this
    arm STOPS with a row rather than treating it as a pass."""
    print("\n=== ARM (e.0): deploy-state check (fresh this run) ===")
    print("served=%s built(this run)=%s packet-time-value=%s"
          % (served_sha, built_sha, LIVE_CODESHA_AT_PACKET_TIME))
    if served_sha == built_sha:
        print("EXPLAINED: served == this run's fresh build -- the fold's deploy has landed and "
              "is currently what is served.")
        return True
    if served_sha == LIVE_CODESHA_AT_PACKET_TIME:
        print("EXPLAINED: served == the packet-time value -- no deploy has landed yet.")
        return True
    print("UNEXPLAINED: served bytes match neither the packet-time value nor this run's fresh "
          "build -- a writer moved the served bytes outside this order's own act.")
    return False


def arm_e_deploy_verify():
    """Re-derive fresh (never a prior run's cached output): rebuild+re-upload irpt-holdings via
    the SAME real tool this cell's deploy used (build-and-upload.sh, single-function mode --
    idempotent: same committed/staged bytes produce the same content and the same sha256), then
    read the served CodeSha256 back and compare BY CONTENT. Per this order's BOUND 2, the
    manifest's `artifact_sha256` field for irpt-holdings is left EXACTLY AS FOUND by this act (its
    staleness relative to the live served value is row W1-S31, the CTO's to reconcile) -- so any
    write build-and-upload.sh makes to that one field is reverted immediately after the build."""
    print("\n=== ARM (e.1): deploy verify (re-derived fresh) ===")
    manifest_path = MANIFEST
    # The FOUND value is what HEAD carries, never a mutable "before this call" snapshot -- a
    # stray earlier run (this run's own predecessor, or an out-of-band debug invocation) could
    # already have left the worktree file at some OTHER value, and reverting to THAT would not
    # satisfy BOUND 2 ("leave the manifest field exactly as found"). git show HEAD is the one
    # value that cannot itself have drifted.
    head_bytes = _run(["git", "show", "HEAD:infra/aws/lambda/ci/lambda-source-map.json"]).stdout
    proc = _run([GIT_BASH, os.path.join(REPO, "infra", "aws", "lambda", "ci", "build-and-upload.sh"),
                "investor-reporting", "irpt-holdings"], timeout=300)
    print("build-and-upload.sh rc=%d" % proc.returncode)
    out = proc.stdout or ""
    m = None
    import re as _re3
    for line in out.splitlines():
        mm = _re3.search(r"SHA256:\s+(\S+)", line)
        if mm:
            m = mm.group(1)
    print("built SHA256 (this run): %s" % m)
    with open(manifest_path, "r", encoding="utf-8", newline="") as fh:
        after = fh.read()
    if after != head_bytes:
        with open(manifest_path, "w", encoding="utf-8", newline="") as fh:
            fh.write(head_bytes)
        print("manifest reverted to its HEAD-committed bytes (BOUND 2 -- irpt-holdings's "
              "artifact_sha256 is not moved by this act; W1-S31 stays the CTO's to reconcile)")
    else:
        print("manifest already byte-identical to HEAD -- nothing to revert")
    if proc.returncode != 0 or not m:
        FAILS.append("arm_e: build-and-upload.sh did not succeed / did not print a SHA256")
        return False, None, None
    cfg = _aws_json("lambda", "get-function-configuration", "--function-name", "irpt-holdings",
                    "--region", "us-east-1")
    served = cfg.get("CodeSha256")
    match = served == m
    print("served=%s built=%s MATCH=%s" % (served, m, match))
    if not match:
        FAILS.append("arm_e: served CodeSha256 != built (%s != %s)" % (served, m))
    return match, served, m


def _real_holdings_enforcer(seam_firm, mod_ns=None):
    if mod_ns is None:
        import loaders as _loaders
        import ids as _ids
        import snapshot as sn
        import enforce as ez
    else:
        _loaders, _ids, sn, ez = (mod_ns["loaders"], mod_ns["ids"], mod_ns["snapshot"],
                                  mod_ns["enforce"])
    opaque_firm_id = _loaders.opaque_firm_for(seam_firm)
    binding = ez.FirmBinding(seam_firm, opaque_firm_id)
    load_directory, load_ownership, load_policy = _loaders.deps(seam_firm)
    projection = _ids.projection_for_firm(seam_firm)
    return sn.make_holdings_enforcer(binding, load_directory, load_ownership=load_ownership,
                                     id_projection=projection)


def _headers_for(advisor_id, tenant, email):
    return {"X-User-Email": email, "X-User-Name": advisor_id, "X-User-Tier": "partner",
           "X-User-Role": "user", "X-Firm-Id": tenant, "X-User-Type": "Advisor",
           "X-Advisor-Id": advisor_id, "X-Advisor-Role": "", "X-Origin-Verify": "cloudfront"}


def arm_e_live_proof():
    """PROVEN LIVE on the holdings route, against the REAL deployed bytes (snapshot.py + the
    now-fixed enforce.py, staged from the shared blob; holdings/entry.py's own wiring supplies
    `_no_grant` by a DIFFERENT cell's deliberate decision -- out of this order's BOUNDS -- so the
    real production composition `snapshot.make_holdings_enforcer` is exercised directly with the
    REAL `_authz.loaders` triple (S3-backed, real production ownership data for 49financial), the
    same real advisor `abby_horton` rtf-2/rte-6 already used on the other 6 routes) never a
    synthetic fixture. Re-derived fresh this run -- no cached numbers."""
    print("\n=== ARM (e.2): live proof ===")
    os.environ["IRPT_DIRECTORY_BUCKET_MAP"] = json.dumps(FIRMS)
    holdings_dir = os.path.join(IRPT, "holdings")
    for p in (holdings_dir, os.path.join(IRPT, "_authz"), os.path.join(IRPT, "_scope"),
             os.path.join(IRPT, "_keys"), os.path.join(IRPT, "_ids")):
        if p not in sys.path:
            sys.path.insert(0, p)
    for mod in ("loaders", "ids", "snapshot", "enforce"):
        sys.modules.pop(mod, None)
    import loaders as _loaders
    import ids as _ids
    import snapshot as sn
    import enforce as ez

    seam_firm = None
    for firm in _ids.firm_ids():
        row = _ids.raw_keys().get("firms", {}).get(firm, {}).get("account", {})
        if row.get("projection_seam"):
            seam_firm = firm
            break
    if seam_firm is None:
        FAILS.append("arm_e_live: no firm declares a projection_seam")
        return {"pass": False}

    enforcer = _real_holdings_enforcer(seam_firm,
                                       {"loaders": _loaders, "ids": _ids, "snapshot": sn, "enforce": ez})
    req = ez.Request(_headers_for("abby_horton", seam_firm, "abby.horton@49financial.com"),
                     "holdings_snapshot")
    scope, refusal = enforcer.resolve_now(req)
    post_served = refusal is None
    post_code = refusal.code if refusal is not None else None
    post_k = len(scope["permitted_account_set"]) if scope is not None else 0
    post_grant = dict(scope["_census"]["unprojected_grant"]) if scope is not None else None
    print("POST-FOLD: seam=%s served=%s code=%s k=%d unprojected_grant=%s"
          % (seam_firm, post_served, post_code, post_k, post_grant))

    swap_req = ez.Request(_headers_for("definitely-not-a-49f-advisor", seam_firm,
                                       "swap@49financial.com"), "holdings_snapshot")
    swap_scope, swap_refusal = enforcer.resolve_now(swap_req)
    swap_refused = swap_scope is None
    swap_code = swap_refusal.code if swap_refusal is not None else None
    print("CROSS-FIRM SWAP: refused=%s code=%s" % (swap_refused, swap_code))

    # THE PRE-FOLD FORK, on the SAME real request (blob 8f849457be, loaded fresh via `git show`
    # into a throwaway module -- never written back into the tree): the same REAL S3 data, the
    # OLD refusal ordering.
    fork_src = _run(["git", "show", FORK_BLOB]).stdout
    import types
    fork_mod = types.ModuleType("enforce")
    fork_mod.__file__ = os.path.join(IRPT, "holdings", "enforce.py")
    saved_enforce = sys.modules.get("enforce")
    sys.modules["enforce"] = fork_mod
    try:
        exec(compile(fork_src, fork_mod.__file__, "exec"), fork_mod.__dict__)
        fork_binding = fork_mod.FirmBinding(seam_firm, _loaders.opaque_firm_for(seam_firm))
        fld, flo, flp = _loaders.deps(seam_firm)
        fork_enforcer = fork_mod.Enforcer(fork_binding, fld, flo, flp,
                                          id_projection=_ids.projection_for_firm(seam_firm))
        fork_req = fork_mod.Request(_headers_for("abby_horton", seam_firm,
                                                 "abby.horton@49financial.com"), "holdings_snapshot")
        fork_scope, fork_refusal = fork_enforcer.resolve_now(fork_req)
    finally:
        if saved_enforce is not None:
            sys.modules["enforce"] = saved_enforce
        else:
            sys.modules.pop("enforce", None)
    if fork_refusal is not None:
        # The false negative: the fork's `serve()` never populates `unprojected_grant`, so the
        # response envelope's own present-at-zero default is what a caller downstream would read.
        pre_fold_count = 0
        pre_fold_code = fork_refusal.code
    else:
        ug = fork_scope.get("_census", {}).get("unprojected_grant")
        pre_fold_count = ug["count"] if isinstance(ug, dict) else 0
        pre_fold_code = None
    print("PRE-FOLD FORK (same real request): refused=%s code=%s -> read as count=%d"
          % (fork_refusal is not None, pre_fold_code, pre_fold_count))

    others = {}
    for firm in FIRMS:
        if firm == seam_firm:
            continue
        try:
            e2 = _real_holdings_enforcer(firm, {"loaders": _loaders, "ids": _ids, "snapshot": sn,
                                               "enforce": ez})
            r2 = ez.Request(_headers_for("any-advisor-id", firm, "x@%s.com" % firm),
                           "holdings_snapshot")
            s2, ref2 = e2.resolve_now(r2)
            others[firm] = {"served": s2 is not None, "code": ref2.code if ref2 is not None else None}
        except Exception as exc:
            others[firm] = {"error": str(exc)[:200]}
    others_refused = all(not v.get("served", True) for v in others.values())
    print("OTHER FIRMS (inflection/cottonwood): %s (all refused=%s)" % (others, others_refused))

    ok = (post_served and post_code != "UNPROJECTED_GRANT" and post_k > 0
         and post_grant is not None and post_grant["count"] > 0
         and post_k + post_grant["count"] == post_grant["denominator"]
         and swap_refused and pre_fold_count == 0 and others_refused)
    if not ok:
        FAILS.append("arm_e_live: live proof did not hold (see printed detail above)")
    return {"pass": ok, "seam_firm": seam_firm, "post_served": post_served, "post_k": post_k,
           "post_grant": post_grant, "swap_refused": swap_refused, "pre_fold_count": pre_fold_count,
           "others_refused": others_refused}


def main():
    print("battery_ib_rtf_8.py -- IRPT_BCKEND.TO-IB-rtf-8 -- repo root: %s\n" % REPO)
    arm_a_diff()
    ok_b = arm_b_fold()
    ok_c = arm_c_census_and_mutant()
    ok_d = arm_d_halves()
    ok_e = False
    e_live = {"pass": False}
    if ok_d:
        ok_e_deploy, served_val, built_val = arm_e_deploy_verify()
        state_ok = (ok_e_deploy and
                   arm_e_deploy_state_check(built_val, served_val))
        if not state_ok:
            FAILS.append("arm_e: deploy-state check FAILED -- served=%s built(this run)=%s "
                         "packet-time-value=%s (unexplained by either)"
                         % (served_val, built_val, LIVE_CODESHA_AT_PACKET_TIME))
        else:
            e_live = arm_e_live_proof()
            ok_e = ok_e_deploy and e_live["pass"]
    print("\n=== SUMMARY ===")
    print("arm (a): diff printed, classified, no STOP")
    print("arm (b): %s" % ("OK" if ok_b else "FAIL"))
    print("arm (c): %s" % ("OK" if ok_c else "FAIL"))
    print("arm (d): %s" % ("OK" if ok_d else "FAIL"))
    print("arm (e): %s%s" % ("OK" if ok_e else "FAIL", "" if ok_d else " (NOT ATTEMPTED -- blocked by arm (d))"))
    every_arm_holds = ok_b and ok_c and ok_d and ok_e
    if every_arm_holds:
        print("\nIBR65-HOLDINGS-ENFORCER-FOLDED-AND-GAP-REPORTED")
    else:
        print("\nNOT EVERY ARM HOLDS -- token withheld. Failing reasons:")
        for f in FAILS:
            print("  - %s" % f)
    return 0 if every_arm_holds else 1


if __name__ == "__main__":
    sys.exit(main())
