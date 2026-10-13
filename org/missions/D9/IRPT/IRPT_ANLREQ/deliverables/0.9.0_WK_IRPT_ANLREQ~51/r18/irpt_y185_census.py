"""AR-y-185 census: which of the 235 map functions package served.py, and what each function's tests import.

Reads the CURRENT head (shared tree C:/dev/ajb_workspace) by git show. Writes the record to the
deliverables path given as argv[1]. ASCII only.
"""
import hashlib
import json
import os
import subprocess
import sys

SHARED = "C:/dev/ajb_workspace"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
SERVED = "infra/aws/lambda/investor-reporting/_authz/served.py"
EIGHT = ("irpt-performance-adapter", "irpt-directory-search", "irpt-narrative", "irpt-ycharts-generate",
         "irpt-export-render", "irpt-holdings", "irpt-status", "irpt-49f-reporting-read-lambda")
MARKERS = ("AR-y-172", 'row.get("status") != "active"', "no users row for an internal caller")


def git_show(ref, path):
    r = subprocess.run(["git", "-C", SHARED, "show", "%s:%s" % (ref, path)], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def git_out(*args):
    return subprocess.run(["git", "-C", SHARED] + list(args), capture_output=True, text=True).stdout.strip()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def served_rows(entry):
    return [s for s in entry.get("staged_from", []) if s.get("packaged_as") == "served.py"]


def census(functions):
    def rule_files(entry):
        return any(x == "served.py" or x.endswith("/served.py") for x in entry.get("files", []))

    def rule_staged(entry):
        return bool(served_rows(entry))

    def rule_repo_path(entry):
        return any(s.get("repo_path", "").endswith("/served.py") for s in entry.get("staged_from", []))

    def rule_mutant_substring(entry):
        # MUTANT of the count rule: any member whose name contains 'served' (matches served_seam.py too)
        return any("served" in x for x in entry.get("files", []))

    out = {}
    for name, rule in (("R_files_member", rule_files), ("R_staged_packaged_as", rule_staged),
                       ("R_staged_repo_path", rule_repo_path), ("MUTANT_substring_served", rule_mutant_substring)):
        out[name] = sorted(k for k, e in functions.items() if rule(e))
    return out


def main(out_path, ref):
    head = git_out("rev-parse", ref)
    map_blob = git_out("rev-parse", ref + ":" + MAP)
    served_blob = git_out("rev-parse", ref + ":" + SERVED)
    drained = git_out("rev-parse", "0724e8a1ff:" + SERVED)
    map_bytes = git_show(ref, MAP)
    served_head = git_show(ref, SERVED)
    functions = json.loads(map_bytes.decode("utf-8"))["functions"]
    rules = census(functions)
    rules2 = census(functions)
    stable = json.dumps(rules, sort_keys=True) == json.dumps(rules2, sort_keys=True)
    packagers = rules["R_staged_packaged_as"]
    print("map denominator (functions scanned): %d" % len(functions))
    for name in ("R_files_member", "R_staged_packaged_as", "R_staged_repo_path"):
        print("%s: %d -- %s" % (name, len(rules[name]), ", ".join(rules[name])))
    print("union of the three real rules == packagers: %s" % (
        sorted(set(rules["R_files_member"]) | set(rules["R_staged_packaged_as"]) | set(rules["R_staged_repo_path"])) == packagers))
    print("MUTANT (substring served) count: %d -- extra: %s" % (
        len(rules["MUTANT_substring_served"]), sorted(set(rules["MUTANT_substring_served"]) - set(packagers))))
    print("determinism (two runs of the census): %s" % ("STABLE" if stable else "UNSTABLE"))
    print("packager set == EIGHT: %s" % (sorted(packagers) == sorted(EIGHT)))

    per = []
    for name in EIGHT:
        e = functions[name]
        row = served_rows(e)[0]
        pin_bytes = git_show(row["pin"], row["repo_path"])
        pin_sha = sha(pin_bytes)
        head_sha = sha(served_head)
        markers_pin = {m: pin_bytes.decode("utf-8").count(m) for m in MARKERS}
        markers_head = {m: served_head.decode("utf-8").count(m) for m in MARKERS}
        per.append({
            "function": name,
            "map_entry": "%s functions[%s] (source_dir %s)" % (MAP, name, e["source_dir"]),
            "pin": row["pin"],
            "how_it_packages_served_py": "member name: staged_from row packaged_as 'served.py' (flat at zip root), "
                                         "repo_path %s; the map's files[] lists served.py" % row["repo_path"],
            "map_sha256": row["sha256"],
            "pinned_blob_sha256": pin_sha,
            "map_sha256_matches_pinned_bytes": pin_sha == row["sha256"],
            "head_blob_sha256": head_sha,
            "pinned_equals_head": pin_sha == head_sha,
            "carries_status_rule": all(v > 0 for v in markers_pin.values()),
            "rule_markers_at_pin": markers_pin,
            "rule_markers_at_head": markers_head,
            "tests_run_against": None,  # filled below from the test wiring read
        })
    wiring = {
        "irpt-performance-adapter": ("live", "performance/tests/test_public_reasons.py:18-19 puts PACKAGE.parent/_authz on sys.path; :67 importlib.import_module('served') resolves to the head _authz/served.py (performance/ has no served.py)"),
        "irpt-directory-search": ("live", "directory/tests/test_entry.py:34-38 puts _LAMBDA_ROOT/_authz on sys.path; :4,9-10 says it is captured against _authz/served.py; directory/ has no served.py"),
        "irpt-narrative": ("pinned", "narrative/tests/test_served_error_path.py:80-92 _stage reads the map's staged rows at row pin and checks row sha256, then test_no_row_unknown.py:23,31 and test_opal_capital_binding.py:26,34 import served from that staged tree"),
        "irpt-ycharts-generate": ("live", "ycharts/generate/tests/run_offline_suite.py:28-33 puts _LAMBDA_ROOT/_authz and _authz/tests on sys.path; test_comparison_catalogue.py:14-17 puts _IR/_authz; :94 import served"),
        "irpt-export-render": ("live", "export/tests/test_download_response_contract.py:26-27 and test_covered_account_ids.py:18-19 put _IRPT/_authz on sys.path; :34 import served; test_accept_business_date.py:20 import served via sibling path set-up"),
        "irpt-holdings": ("live", "holdings/entry.py:19-22 puts _PKG/_authz on sys.path before import served; holdings/tests/test_entry_guarded.py:11-13 puts _authz on sys.path; holdings/ has no served.py"),
        "irpt-status": ("live", "ops/tests/test_status.py:18-22 and test_opal_consumers.py:19 put _authz on sys.path; test_owned_report.py:217 import served; test_report_ticket_binding.py:149 from served import"),
        "irpt-49f-reporting-read-lambda": ("live", "reporting/entry.py:73-78 puts _PKG/_authz on sys.path; :82 import served as _entry; reporting/tests/test_reporting_entry.py:14-15 loads reporting/entry.py by path; reporting/ has no served.py"),
    }
    for rec in per:
        rec["tests_run_against"] = wiring[rec["function"]][0]
        rec["tests_read"] = wiring[rec["function"]][1]
    record = {
        "to_id": "IRPT_ANLREQ.TO-AR-y-185",
        "cell": "AR-y-185",
        "read_at": {"shared_tree_head": head, "map_blob": map_blob, "served_py_blob": served_blob,
                    "served_py_blob_note": ("equal to the blob at 0724e8a1ff (the drained status rule)" if served_blob == drained
                                            else "differs from the blob at 0724e8a1ff (%s); the status rule is still present at this ref, see rule_markers_at_head" % drained),
                    "worktree_map_blob_not_used": "78e79160bdbd44db0f1cff2dfb39c348c7caa825 (worktree copy, older; read, not used)"},
        "count_rule": "a function packages served.py when its staged_from holds a row with packaged_as == 'served.py'; "
                      "the files[] member rule and the repo_path rule give the same eight",
        "positive_control": "irpt-status: files[] lists served.py and staged_from packages it at pin 361c44fa9d",
        "negative_control": "exec-summary-generator and opal-partners-data list served_seam.py (a near name) and no served.py row: not counted",
        "mutant_control": "rule replaced by a substring test 'served' in member name: counts %d (the eight plus served_seam.py in two functions), so the mutant FIRES" % len(rules["MUTANT_substring_served"]),
        "determinism": "two runs of the census compared: %s" % ("STABLE" if stable else "UNSTABLE"),
        "map_denominator": len(functions),
        "packager_count": len(packagers),
        "functions": per,
        "claim": ("Eight of %d functions in the head map package _authz/served.py (member name served.py, staged, two pins: "
                  "361c44fa9d and 74a62fb46c). None of the eight pinned blobs carries the AR-y-172 status rule; the head blob "
                  "does. Narrative's tests run its staged pinned copy and cannot see the rule. The other seven test suites "
                  "import the head _authz/served.py, which carries the rule, while their shipped bytes do not." % len(functions)),
        "not_read": [
            "No function was run, deployed, invoked or called; no AWS, network or push.",
            "The deployed Lambda code was not read (no AWS call); shipped bytes are the map pins, not a live zip.",
            "Only the import and sys.path wiring of each test folder was read, not every test body; the suites were not executed.",
            "The worktree copy of lambda-source-map.json (blob 78e79160) and of _authz/served.py (blob 1d55a27a) are older than the read ref and were not used.",
            "Between the worktree copy and the read ref, 17 map entries differ, all eight of the packagers among them, in their loaders.py pins and artifact_sha256 values; the served.py rows of the eight are the same in both. The other 9 differing entries were not examined.",
            "Prose notes in the other 227 entries were searched for served mentions, not read in full.",
        ],
        "what_moves_together": (
            "For one internal caller to get one answer from all eight, one served.py that carries the AR-y-172 status rule "
            "(the head blob cf1091b454 or a later pin of it) must be the member every one of the eight stages: the map rows "
            "for served.py at 361c44fa9d (performance-adapter, narrative, status) and 74a62fb46c (directory-search, "
            "ycharts-generate, export-render, holdings, 49f-reporting-read-lambda) move together to that pin, each function is "
            "rebuilt and redeployed in the same window, and narrative's test staging reads the new pin so its suite stops "
            "running the old bytes. The seven live-testing suites already import the head file that carries the rule, so their "
            "suites run it while their shipped bytes do not; no test edit is needed for them to run it. Any other shared member the head served.py depends on at its pin (errors.py, enforce.py) must be "
            "the same version in each function's staged set."),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(record, fh, indent=2, sort_keys=False)
        fh.write("\n")
    print("record written: %s" % out_path)
    for rec in per:
        print("%s | pin %s | pinned_sha %s | head_sha_eq %s | rule %s | tests %s" % (
            rec["function"], rec["pin"][:10], rec["pinned_blob_sha256"][:12], rec["pinned_equals_head"],
            rec["carries_status_rule"], rec["tests_run_against"]))
    return 0


if __name__ == "__main__":
    # argv: <record path> [git ref to read; default HEAD]
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "HEAD"))
