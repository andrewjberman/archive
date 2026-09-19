#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-2 battery -- THE PARTIAL GRANT SERVED WITH ITS UNPROJECTED COUNT
DISCLOSED. CTO ruling @61627f39f9.

FIRST PASS (this run): arms (a), (b), (c) are graded for real, against the real code in this
worktree, THIS run. Arm (d) is EXPECTED to FAIL truthfully -- the never-widen halves cannot exist
before this order's own packet does, and the packet is written and committed by THIS same run,
one step ahead of the read that grades (d). Arm (e) (the deploy) does not run until (d) passes.

Prints IBR59-PARTIAL-GRANT-SERVED-WITH-DISCLOSURE only when EVERY arm holds, including (d).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# .../deliverables/0.9.0_WK_IRPT_BCKEND~1 -> up 7 to the worktree root
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
LAMBDA_ROOT = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting")
AUTHZ_DIR = os.path.join(LAMBDA_ROOT, "_authz")
TESTS_DIR = os.path.join(AUTHZ_DIR, "tests")
for _p in (AUTHZ_DIR, TESTS_DIR, os.path.join(LAMBDA_ROOT, "_scope"),
           os.path.join(LAMBDA_ROOT, "_keys"), os.path.join(LAMBDA_ROOT, "_ids")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ENTRY_FUNCTION_DIRS = ("directory", "export", "holdings", "narrative", "ops", "performance",
                       os.path.join("ycharts", "generate"))

COO_HALF_DIR = os.path.join(WS, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
CTO_HALF_DIR = os.path.join(WS, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")
PACKET_PATH = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-2.md")


def git_head():
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    return out.stdout.strip()


def git_hash_object(path):
    out = subprocess.run(["git", "hash-object", path], cwd=WS, capture_output=True, text=True,
                         timeout=30)
    if out.returncode != 0:
        return None
    return out.stdout.strip()


# --------------------------------------------------------------------------- arm (a): the tests
def arm_a_tests():
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q",
                            os.path.join(TESTS_DIR, "test_enforce.py")],
                          capture_output=True, text=True, timeout=180, cwd=WS)
    out = (proc.stdout or "") + (proc.stderr or "")
    n_passed, n_failed = 0, 0
    for token in out.split():
        pass
    import re
    mp = re.search(r"(\d+) passed", out)
    mf = re.search(r"(\d+) failed", out)
    n_passed = int(mp.group(1)) if mp else 0
    n_failed = int(mf.group(1)) if mf else 0
    all_pass = (proc.returncode == 0) and n_failed == 0 and n_passed > 0

    # INDEPENDENT RE-DERIVATION of the mutant claim -- never trust the pytest test's own
    # internal assertion alone. Same transplant helper the test imports, called fresh here.
    import mutant_ordering
    import fixtures as fx
    import enforce as ez

    def real_partial_result():
        deps = fx.Deps(ownership=fx.OWNERSHIP_PARTIAL_UNPROJECTED)
        binding = ez.FirmBinding(fx.TENANT, fx.OPAQUE_FIRM)
        e = ez.Enforcer(binding, deps.load_directory, deps.load_ownership, deps.load_policy)
        return e.serve(ez.Request(fx.headers(), "directory_search", "account", fx.A1),
                       lambda scope: {"accounts": list(scope["permitted_account_set"])})

    real_out = real_partial_result()
    mutant_ns = mutant_ordering.build_old_order_module(os.path.join(AUTHZ_DIR, "enforce.py"))
    deps2 = fx.Deps(ownership=fx.OWNERSHIP_PARTIAL_UNPROJECTED)
    mbinding = mutant_ns["FirmBinding"](fx.TENANT, fx.OPAQUE_FIRM)
    me = mutant_ns["Enforcer"](mbinding, deps2.load_directory, deps2.load_ownership,
                               deps2.load_policy)
    mutant_out = me.serve(mutant_ns["Request"](fx.headers(), "directory_search", "account", fx.A1),
                          lambda scope: {"accounts": list(scope["permitted_account_set"])})
    mutant_fires = (mutant_out.ok is False and mutant_out.code == "UNPROJECTED_GRANT")
    real_serves = (real_out.ok is True
                  and sorted(real_out.payload["accounts"]) == sorted([fx.A1, fx.A2])
                  and real_out.census["unprojected_grant"] == {
                      "count": 1, "denominator": 3, "kinds": {"UNPROJECTED-ID": 1}})

    return {
        "pytest_returncode": proc.returncode,
        "n_passed": n_passed,
        "n_failed": n_failed,
        "pytest_tail": out[-3000:],
        "real_serves_the_partial_case": real_serves,
        "real_census": real_out.census.get("unprojected_grant"),
        "mutant_fires": mutant_fires,
        "mutant_code": mutant_out.code,
        "pass": all_pass and real_serves and mutant_fires,
    }


# --------------------------------------------------------------------------- arm (b): the field
def _entry_py_paths():
    out = []
    for rel in ENTRY_FUNCTION_DIRS:
        p = os.path.join(LAMBDA_ROOT, rel, "entry.py")
        out.append(p)
    return out


def arm_b_disclosure_field():
    import served as _served

    paths = _entry_py_paths()
    denom = len(paths)
    wired = []
    rows = {}
    for p in paths:
        rel = os.path.relpath(p, WS)
        exists = os.path.isfile(p)
        imports_served = False
        if exists:
            with open(p, "r", encoding="utf-8") as fh:
                imports_served = "import served" in fh.read()
        rows[rel] = {"exists": exists, "imports_served": imports_served}
        if exists and imports_served:
            wired.append(p)
    census_ok = (len(wired) == denom == 7)

    # PRESENT-AT-ZERO, DIRECTLY ON THE SHARED FUNCTION: every route this function serves answers
    # through response_envelope(), and this proves its DEFAULT (no gap measured -> omitted arg)
    # still carries the field.
    zero_env = _served.response_envelope("some-op", "fir_x", {"k": 1})
    zero_present = ("unprojected_grant" in zero_env
                    and zero_env["unprojected_grant"] == {"count": 0, "denominator": 0,
                                                           "kinds": {}})

    # NON-ZERO: the same function fed a real measured gap.
    nonzero_env = _served.response_envelope("some-op", "fir_x", {"k": 1},
                                            unprojected_grant={"count": 22, "denominator": 43,
                                                                "kinds": {"UNPROJECTED-ID": 22}})
    nonzero_present = nonzero_env.get("unprojected_grant") == {
        "count": 22, "denominator": 43, "kinds": {"UNPROJECTED-ID": 22}}

    # ONE SHARED CALL SITE: response_envelope has exactly one caller inside served.py
    # (Entry.handle), which is what makes "wired == field present" a valid inference rather than
    # a per-route promise nobody enforces. Re-derived by reading the source fresh, not recalled.
    with open(os.path.join(AUTHZ_DIR, "served.py"), "r", encoding="utf-8") as fh:
        served_src = fh.read()
    call_sites = served_src.count("response_envelope(")
    # 1 def + 1 call = 2 occurrences of the literal "response_envelope(" as a definition/call
    # opener; the def itself also matches the substring, so this is DEF(1) + CALLS.
    def_count = served_src.count("def response_envelope(")
    calls_excluding_def = call_sites - def_count

    return {
        "denominator": denom,
        "wired": len(wired),
        "rows": rows,
        "census_verdict": "%d of %d entry.py import the shared served boundary" % (len(wired), denom),
        "zero_present": zero_present,
        "zero_envelope": zero_env,
        "nonzero_present": nonzero_present,
        "nonzero_envelope": nonzero_env,
        "response_envelope_call_sites_excluding_def": calls_excluding_def,
        "pass": census_ok and zero_present and nonzero_present and calls_excluding_def == 1,
    }


# --------------------------------------------------------------------------- arm (c): the row
def arm_c_consumer_obligation_row():
    import re
    path = os.path.join(WS, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "surprise-channel",
                        "investigations", "INVESTIGATION_v1.md")
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    m = re.search(r"```json\n(.*?)\n```", text, re.S)
    rows = json.loads(m.group(1))
    match = [r for r in rows if r.get("id") == "IRPT_BCKEND-W1-S28"]
    ok = (len(match) == 1 and match[0].get("class") == "OBSERVATION"
         and match[0].get("hazard_standing") == "ARMED"
         and match[0].get("disarm_owner") == "1.0.0_SA_CTO")
    return {
        "row_id": "IRPT_BCKEND-W1-S28" if match else None,
        "found": len(match),
        "class": match[0].get("class") if match else None,
        "hazard_standing": match[0].get("hazard_standing") if match else None,
        "disarm_owner": match[0].get("disarm_owner") if match else None,
        "total_rows_in_first_fence": len(rows),
        "pass": ok,
    }


# --------------------------------------------------------------------------- arm (d): the halves
def _half_files(directory, code_pattern):
    if not os.path.isdir(directory):
        return []
    return sorted(f for f in os.listdir(directory)
                 if f.startswith(code_pattern) and f.endswith(".md"))


def _committed_at_head(path):
    """Is this path's WORKING-TREE content identical to what HEAD carries for it -- i.e. does a
    commit already hold these exact bytes, so 'at HEAD' claims made from `git hash-object` on the
    working tree are not getting ahead of the commit that is supposed to carry them."""
    rel = os.path.relpath(path, WS)
    out = subprocess.run(["git", "cat-file", "-p", "HEAD:" + rel.replace(os.sep, "/")],
                        cwd=WS, capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        return False
    with open(path, "r", encoding="utf-8") as fh:
        working = fh.read()
    return out.stdout == working


def arm_d_halves():
    packet_hash = git_hash_object(PACKET_PATH) if os.path.isfile(PACKET_PATH) else None
    packet_committed_at_head = _committed_at_head(PACKET_PATH) if packet_hash else False
    coo_files = _half_files(COO_HALF_DIR, "NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-2_")
    cto_files = _half_files(CTO_HALF_DIR, "NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-2_")

    def names_blob(files_dir, files):
        out = []
        for f in files:
            p = os.path.join(files_dir, f)
            with open(p, "r", encoding="utf-8") as fh:
                out.append((f, ("blob " + str(packet_hash)) in fh.read() if packet_hash else False))
        return out

    coo_checked = names_blob(COO_HALF_DIR, coo_files)
    cto_checked = names_blob(CTO_HALF_DIR, cto_files)
    coo_ok = any(ok for _f, ok in coo_checked)
    cto_ok = any(ok for _f, ok in cto_checked)

    return {
        "packet_path": os.path.relpath(PACKET_PATH, WS),
        "packet_file_exists": os.path.isfile(PACKET_PATH),
        "packet_committed_at_head": packet_committed_at_head,
        "packet_blob_hash": packet_hash,
        "coo_half_dir": os.path.relpath(COO_HALF_DIR, WS),
        "coo_half_candidates": coo_files,
        "coo_half_names_packet_blob": coo_ok,
        "cto_half_dir": os.path.relpath(CTO_HALF_DIR, WS),
        "cto_half_candidates": cto_files,
        "cto_half_names_packet_blob": cto_ok,
        "pass": bool(packet_hash) and packet_committed_at_head and coo_ok and cto_ok,
    }


def main():
    report = {"git_head": git_head()}

    a = arm_a_tests()
    report["arm_a_tests"] = a
    print("ARM (a) TESTS: pytest rc=%s, %d passed / %d failed; real serves partial=%s "
          "census=%s; mutant fires=%s (code=%s)"
          % (a["pytest_returncode"], a["n_passed"], a["n_failed"],
             a["real_serves_the_partial_case"], a["real_census"], a["mutant_fires"],
             a["mutant_code"]))

    b = arm_b_disclosure_field()
    report["arm_b_disclosure_field"] = b
    print("ARM (b) DISCLOSURE FIELD: %s; zero-present=%s; nonzero-present=%s; "
          "response_envelope call sites (excl def)=%d"
          % (b["census_verdict"], b["zero_present"], b["nonzero_present"],
             b["response_envelope_call_sites_excluding_def"]))

    c = arm_c_consumer_obligation_row()
    report["arm_c_consumer_obligation_row"] = c
    print("ARM (c) CONSUMER-OBLIGATION ROW: id=%s found=%d class=%s hazard_standing=%s "
          "disarm_owner=%s"
          % (c["row_id"], c["found"], c["class"], c["hazard_standing"], c["disarm_owner"]))

    d = arm_d_halves()
    report["arm_d_halves"] = d
    print("ARM (d) NEVER-WIDEN HALVES AT HEAD: packet_file_exists=%s packet_committed_at_head=%s "
          "blob=%s; coo_half_present_naming_blob=%s (%d candidate file(s)); "
          "cto_half_present_naming_blob=%s (%d candidate file(s))"
          % (d["packet_file_exists"], d["packet_committed_at_head"], d["packet_blob_hash"],
             d["coo_half_names_packet_blob"], len(d["coo_half_candidates"]),
             d["cto_half_names_packet_blob"], len(d["cto_half_candidates"])))
    if not d["pass"]:
        print("ARM (d) STOP: at least one never-widen half is ABSENT at HEAD naming the "
              "packet's blob hash. This is the EXPECTED first-pass outcome (cell text: 'ABSENT "
              "-> STOP HERE: arm (d) FAILS truthfully'). Arm (e) (the deploy) does not run.")

    overall = a["pass"] and b["pass"] and c["pass"] and d["pass"]
    report["overall_pass"] = overall
    print(json.dumps(report, indent=1, default=str))
    if overall:
        print("IBR59-PARTIAL-GRANT-SERVED-WITH-DISCLOSURE")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
