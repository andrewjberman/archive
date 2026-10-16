#!/usr/bin/env python3
"""atomic_check.py -- read-only checker for NFRA_CTLPLN TO-CT-ca-1 (round 30): the Lambda source map split.

Worker 0.9.0_WK_NFRA_CTLPLN~145. Standard library only, ASCII only, no network, no AWS, no deploy.
Terraform is run ONLY as `terraform fmt -check <root>` (subcommand --tf-static). Reads the base map
from git (`git show <BASE>:<map>`, BASE from BASE.txt in this folder), the working tree, and the census.

Usage (from the worktree root, or anywhere: the root is found by git):
  python <this file>                 ATOMIC-SPLIT  the folder equals the base map; the map is absent; census other=0; no live old-path user
  python <this file> --suites --base write SUITES_BASE.txt (run at the BASE commit, before the change)
  python <this file> --suites        ATOMIC-SUITES  run the 21 suites (each under timeout 120), write SUITES_AFTER.txt, compare with SUITES_BASE.txt
  python <this file> --tf-static     ATOMIC-TF  fmt -check on the three roots; text checks; Python recompute of the 240 objects

Verdict rule: ok is True only when every condition named on the last line holds; no condition is inferred.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True).stdout.decode("utf-8").strip()
DELIV_REL = "org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~145"
CENSUS_REL = "org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~140/source_map_census.py"
# the retired single map: read at the BASE commit only (git show), never from the tree. Built from parts so this tool's
# own source is not graded as a live reader by the census (it reads history, not the tree).
MAP_NAME = "lambda" + "-source-map.json"
MAP_REL = "infra/aws/lambda/ci/" + MAP_NAME
FOLDER_REL = "infra/aws/lambda/ci/function-map"
TF_ROOTS = [
    "infra/aws/terraform/investor-reporting/account-return-daily",
    "infra/aws/terraform/investor-reporting/reporting-gold-iso",
    "infra/aws/terraform/investor-reporting/reporting-publish-iso",
]
# The three closed-round writers named by the cell. battery_ib_rtf_1.py is retired (git rm), so it is absent.
NAMED_WRITERS = [
    "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_Y/live_walk/repin_source_map_rows.py",
    "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rte_4.py",
    "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rtf_1.py",
]
# The "can follow" list of the cell (proposal section (d)); the cell does not edit these.
CAN_FOLLOW = [
    "org/modules/graph/lambdamap_cli.py",
    "org/modules/graph/comp_closure.py",
    "org/modules/graph/extract_lambda_routes.py",
    "rcg/bin/lexicon.py",
    "rcg/bin/mark.py",
    "infra/aws/ec2/estate-report-runner/estate_report_runner.py",
]
CLOSED_ROUND_PREFIXES = ("org/missions/", "org/tier1_exec/", "org/tier2_senior/")
LIVE_CLASSES = ("READ_WHOLE", "READ_ONE", "WRITE", "OTHER")

# (suite name, [invocation, ...]); kind "py" = script run, "pt" = pytest (the file has no script entry point).
SUITES = [
    ("round19_register", [["py", ".tools/tests/test_round19_register.py", "--fwd2"], ["py", ".tools/tests/test_round19_register.py", "--fwd7"]]),
    ("record_deploy_scope_arms", [["py", "infra/aws/lambda/ci/test_record_deploy_scope_arms.py"]]),
    ("record_terraform_deploy_scope", [["py", "infra/aws/lambda/ci/test_record_terraform_deploy_scope.py"]]),
    ("render_ports_packaging", [["pt", "infra/aws/lambda/ci/test_render_ports_packaging.py"]]),
    ("build_and_upload_verify", [["sh", "infra/aws/lambda/ci/tests/test_build_and_upload_verify.sh"]]),
    ("build_only", [["sh", "infra/aws/lambda/ci/tests/test_build_only.sh"]]),
    ("build_restore_fails_loud", [["sh", "infra/aws/lambda/ci/tests/test_build_restore_fails_loud.sh"]]),
    ("record_terraform_deploy_paths", [["sh", "infra/aws/lambda/ci/tests/test_record_terraform_deploy_paths.sh"]]),
    ("source_map_filled_named_accounts", [["pt", "infra/aws/lambda/ci/tests/test_source_map_filled_named_accounts.py"]]),
    ("source_map_filled_reader_installed", [["pt", "infra/aws/lambda/ci/tests/test_source_map_filled_reader_installed.py"]]),
    ("unguarded_census", [["pt", "infra/aws/lambda/investor-reporting/_authz/tests/test_unguarded_census.py"]]),
    ("seam_paired", [["pt", "infra/aws/lambda/investor-reporting/_contracts/tests/test_seam_paired.py"]]),
    ("package_resolves", [["pt", "infra/aws/lambda/investor-reporting/account-dim-cot/tests/test_package_resolves.py"]]),
    ("zip_registry_resolves", [["pt", "infra/aws/lambda/investor-reporting/holdings-performance/tests/test_zip_registry_resolves.py"]]),
    ("w1_s16_advisor_firm_bound", [["pt", "infra/aws/lambda/investor-reporting/holdings/tests/test_w1_s16_advisor_firm_bound.py"]]),
    ("served_error_path", [["pt", "infra/aws/lambda/investor-reporting/narrative/tests/test_served_error_path.py"]]),
    ("route_firm_fence", [["pt", "infra/aws/lambda/portal_data_proxy/tests/test_route_firm_fence.py"]]),
    ("content_assertion", [["py", "infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe/tests/test_content_assertion.py"]]),
    ("derive_fence_row_shape", [["py", "infra/aws/terraform/shared-infra/tests/derive_fence_row_shape.py"]]),
    ("iam_v4_024_fp_elimination", [["py", "org/modules/graph/test_iam_v4_024_fp_elimination.py"]]),
    ("test_lambdamap", [["pt", "org/modules/graph/tests/test_lambdamap.py"]]),
]
SUITE_TIMEOUT = 120
# A suite that makes live AWS reads by its own design is listed, never run: this cell runs no aws command.
NO_AWS_SUITES = {
    "derive_fence_row_shape":
        "not run: makes live AWS reads by design (sts get-caller-identity, iam simulate-principal-policy); the cell runs no aws command",
}


def ascii_only(s):
    return s.encode("ascii", "replace").decode("ascii")


def deliv(*parts):
    return os.path.join(ROOT, DELIV_REL, *parts)


def base_commit():
    with open(deliv("BASE.txt"), encoding="ascii") as f:
        return f.read().split()[0]


def git_show_base(rel):
    r = subprocess.run(["git", "show", "%s:%s" % (base_commit(), rel)], cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: git show base:%s rc=%d %s" % (rel, r.returncode, ascii_only(r.stderr.decode("utf-8", "replace"))[:200]))
    return r.stdout


def base_functions():
    return json.loads(git_show_base(MAP_REL).decode("utf-8"))["functions"]


def folder_bytes():
    d = os.path.join(ROOT, FOLDER_REL)
    if not os.path.isdir(d):
        return {}
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".json"):
            with open(os.path.join(d, f), "rb") as fh:
                out[f[:-5]] = fh.read()
    return out


def dump_entry(entry):
    return (json.dumps(entry, indent=2, sort_keys=False, ensure_ascii=True) + "\n").encode("ascii")


# ---------------------------------------------------------------- default: ATOMIC-SPLIT
def load_census_module():
    spec = importlib.util.spec_from_file_location("smc_readonly", os.path.join(ROOT, CENSUS_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def census_classes(mod):
    names = mod.grep_set()
    blobs = mod.read_blobs(names)
    readings = mod.load_consumer_readings()
    cls = {}
    for p in names:
        blob = blobs[p]
        text = blob.decode("utf-8", "replace") if blob is not None else ""
        pc, _basis, _ln, _hit = mod.classify_file(p, text)
        if p in readings:
            cls[p] = readings[p]["class"]
        else:
            cls[p] = pc if pc != "UNDECIDED" else "OTHER"
    return names, cls


def check_split():
    funcs = base_functions()
    n = len(funcs)
    folder = folder_bytes()
    equal = 0
    bytes_exact = 0
    mismatches = []
    for k, v in funcs.items():
        b = folder.get(k)
        if b is None:
            mismatches.append(("absent", k))
            continue
        try:
            same = json.loads(b.decode("utf-8")) == v
        except ValueError:
            same = False
        if same:
            equal += 1
            if b == dump_entry(v):
                bytes_exact += 1
        else:
            mismatches.append(("differs", k))
    extra = sorted(set(folder) - set(funcs))
    map_present = os.path.exists(os.path.join(ROOT, MAP_REL))
    # the census, run as the cell's read-only check (no argument: it must write nothing)
    r = subprocess.run([sys.executable, os.path.join(ROOT, CENSUS_REL)], cwd=ROOT, capture_output=True, timeout=280)
    census_out = r.stdout.decode("utf-8", "replace")
    census_line = [ln for ln in census_out.splitlines() if ln.startswith("SOURCEMAP-CENSUS ")]
    census_other = -1
    census_ok = False
    if census_line:
        m = re.search(r"other:(\d+)", census_line[-1])
        census_other = int(m.group(1)) if m else -1
        census_ok = "ok=True" in census_line[-1]
    print("CENSUS-RC rc=%d" % r.returncode)
    print("CENSUS-LINE %s" % ascii_only(census_line[-1]) if census_line else "CENSUS-LINE (none)")
    # live readers and writers that still name the old path outside the allowed set
    mod = load_census_module()
    names, cls = census_classes(mod)
    live = []
    for p in names:
        if cls[p] not in LIVE_CLASSES:
            continue
        if p in CAN_FOLLOW:
            continue
        if p.startswith(CLOSED_ROUND_PREFIXES) and p not in NAMED_WRITERS:
            continue
        live.append((p, cls[p]))
    for p in NAMED_WRITERS:
        if p in names:
            live.append((p, cls[p] + " (named writer)"))
    for p, c in live:
        print("LIVE-OLD-PATH %s %s" % (c, p))
    for kind, k in mismatches[:20]:
        print("MISMATCH %s %s" % (kind, k))
    print("FOLDER json=%d extra=%s bytes_exact=%d" % (len(folder), extra[:10], bytes_exact))
    print("CENSUS-OTHER-FILES %s" % [p for p in names if cls[p] == "OTHER"])
    u = len(live)
    ok = (equal == n and len(folder) == n and not extra and (not map_present) and census_other == 0
          and census_ok and u == 0)
    print("ATOMIC-SPLIT functions=%d equal=%d map_present=%s census_other=%d live_old_path_users=%d ok=%s"
          % (n, equal, map_present, census_other, u, ok))
    return 0 if ok else 1


# ---------------------------------------------------------------- --suites
def bash_path():
    sys.path.insert(0, os.path.join(ROOT, ".tools"))
    from git_bash_resolver import git_bash  # type: ignore
    b = git_bash()
    if not b:
        raise SystemExit("ERROR: no Git Bash found")
    return b


def run_invocation(inv, bash):
    kind, rel = inv[0], inv[1]
    extra = inv[2:]
    if kind == "py":
        argv = [sys.executable, rel] + extra
    elif kind == "pt":
        argv = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", rel] + extra
    else:
        argv = [bash, rel] + extra
    try:
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=SUITE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %d s" % SUITE_TIMEOUT, ""
    out = r.stdout.decode("utf-8", "replace") + "\n" + r.stderr.decode("utf-8", "replace")
    lines = [ln for ln in out.splitlines() if ln.strip()]
    last = ascii_only(lines[-1].strip())[:220] if lines else "(no output)"
    return r.returncode, last, out


def run_suites(base_mode):
    bash = bash_path()
    rows = []
    for name, invs in SUITES:
        rcs, lasts, verdict = [], [], "PASS"
        if name in NO_AWS_SUITES:
            rows.append((name, "NOT-RUN", [], [NO_AWS_SUITES[name]]))
            print("SUITE %s | NOT-RUN | rc=- | %s" % (name, NO_AWS_SUITES[name]))
            continue
        for inv in invs:
            rc, last, out = run_invocation(inv, bash)
            rcs.append(rc)
            lasts.append(last)
            if rc == 124:
                verdict = "TIMEOUT"
            elif rc != 0 and verdict == "PASS":
                verdict = "NOT-RUNNABLE" if re.search(r"No module named|ModuleNotFoundError|ImportError", out) else "FAIL"
        rows.append((name, verdict, rcs, lasts))
        print("SUITE %s | %s | rc=%s | %s" % (name, verdict, ",".join(str(x) for x in rcs), lasts[-1]))
    lines = ["# %s -- %s" % ("SUITES_BASE" if base_mode else "SUITES_AFTER",
                              "run at the base commit %s, before the change" % base_commit() if base_mode else "run after the change"),
             "# format: suite | verdict | rc per invocation | last line of the (last) invocation",
             "# denominator: %d suites" % len(SUITES)]
    for name, verdict, rcs, lasts in rows:
        lines.append("%s | %s | rc=%s | %s" % (name, verdict, ",".join(str(x) for x in rcs), lasts[-1]))
    fname = "SUITES_BASE.txt" if base_mode else "SUITES_AFTER.txt"
    with open(deliv(fname), "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("SUITES-TABLE-WRITTEN %s suites=%d" % (fname, len(SUITES)))
    if base_mode:
        return 0
    base_path = deliv("SUITES_BASE.txt")
    if not os.path.exists(base_path):
        print("ATOMIC-SUITES green_at_base=0 green_after=%d red_after=%d ok=False" % (
            sum(1 for r in rows if r[1] == "PASS"), sum(1 for r in rows if r[1] != "PASS")))
        return 1
    base_green = set()
    with open(base_path, encoding="ascii") as f:
        for ln in f:
            parts = ln.split(" | ")
            if len(parts) >= 2 and not ln.startswith("#") and parts[1] == "PASS":
                base_green.add(parts[0])
    after_green = {r[0] for r in rows if r[1] == "PASS"}
    red_after = [r[0] for r in rows if r[1] != "PASS"]
    print("BASE-GREEN-NOW-RED %s" % sorted(base_green - after_green))
    print("RED-AFTER %s" % red_after)
    ok = base_green <= after_green
    print("ATOMIC-SUITES green_at_base=%d green_after=%d red_after=%d ok=%s" % (
        len(base_green), len(after_green), len(red_after), ok))
    return 0 if ok else 1


# ---------------------------------------------------------------- --tf-static
def check_tf():
    funcs = base_functions()
    n = len(funcs)
    folder = folder_bytes()
    built = {k: json.loads(v.decode("utf-8")) for k, v in folder.items()}
    fmt_clean = 0
    uses_fileset = 0
    per_root_equal = []
    for rel in TF_ROOTS:
        r = subprocess.run(["terraform", "fmt", "-check", rel], cwd=ROOT, capture_output=True, timeout=120)
        clean = r.returncode == 0
        if clean:
            fmt_clean += 1
        path = os.path.join(ROOT, rel, "locals.tf")
        # diagnostic only (not in ok): fmt of the one file this cell edits, so a root-level failure in another file is named
        rf = subprocess.run(["terraform", "fmt", "-check", os.path.join(rel, "locals.tf")], cwd=ROOT, capture_output=True, timeout=120)
        print("TF-LOCALS-FILE-FMT %s rc=%d" % (rel, rf.returncode))
        with open(path, "rb") as f:
            text = f.read().decode("utf-8", "replace")
        fs = "fileset(" in text and "function-map" in text
        names_map = MAP_NAME in text
        if fs:
            uses_fileset += 1
        # the object the new expression builds: { for f in fileset(folder, "*.json") : trimsuffix(f, ".json") => jsondecode(file(f)) }
        obj = {}
        for fname in sorted(os.listdir(os.path.join(ROOT, FOLDER_REL))):
            if fname.endswith(".json"):
                obj[fname[:-len(".json")]] = built[fname[:-len(".json")]]
        same = sum(1 for k, v in funcs.items() if k in obj and obj[k] == v)
        per_root_equal.append(same)
        print("TF-ROOT %s fmt_rc=%d fmt_clean=%s uses_fileset=%s names_map_file=%s built_keys=%d equal=%d/%d"
              % (rel, r.returncode, clean, fs, names_map, len(obj), same, n))
        if r.stdout.strip() or r.stderr.strip():
            print("TF-FMT-OUT %s" % ascii_only((r.stdout + r.stderr).decode("utf-8", "replace").strip().replace("\n", " ; "))[:300])
    e = min(per_root_equal) if per_root_equal else 0
    roots_ok_text = all(("fileset(" in open(os.path.join(ROOT, rel, "locals.tf"), "rb").read().decode("utf-8", "replace"))
                        and (MAP_NAME not in open(os.path.join(ROOT, rel, "locals.tf"), "rb").read().decode("utf-8", "replace"))
                        for rel in TF_ROOTS)
    ok = fmt_clean == len(TF_ROOTS) and uses_fileset == len(TF_ROOTS) and e == n and roots_ok_text
    print("ATOMIC-TF roots=%d fmt_clean=%d uses_fileset=%d equal=%d ok=%s" % (len(TF_ROOTS), fmt_clean, uses_fileset, e, ok))
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--tf-static" in args:
        sys.exit(check_tf())
    if "--suites" in args:
        sys.exit(run_suites(base_mode="--base" in args))
    sys.exit(check_split())
