"""OG-rl-14 (re-cut r28b) step 3 summary: parses r28b_tests_release.out (per-file pytest, new release tree aa75078e1b) and the Phase A baseline run on the live tree
(r28_tests_release.out is the 419297b525 run; r28_tests_baseline_full.out is the live tree 510c8cfed2 / rb22). usage: python r28b_tests_summary.py"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def parse(fn):
    files, cur = {}, None
    for ln in open(os.path.join(HERE, fn), encoding="utf-8").read().replace("\r", "").split("\n"):
        if ln.startswith("== "):
            cur = ln[3:].strip()
            files[cur] = {"passed": 0, "failed": 0, "errors": 0, "ids": [], "rc": None}
        elif cur is None:
            continue
        elif ln.startswith(("FAILED ", "ERROR ")):
            files[cur]["ids"].append(ln.split(" ", 1)[1].split(" - ")[0].strip().replace(chr(92), "/"))   # pytest prints backslash paths on this device
        elif ln.startswith("rc="):
            files[cur]["rc"] = ln[3:]
        else:
            for n, k in re.findall(r"(\d+) (passed|failed|error)", ln):
                files[cur]["errors" if k == "error" else k] += int(n)
    return files


def tot(fs):
    return sum(v["passed"] for v in fs.values()), sum(v["failed"] for v in fs.values()), sum(v["errors"] for v in fs.values())


rel = parse("r28b_tests_release.out")
old = parse("r28_tests_release.out")      # Phase A, 419297b525
base = parse("r28_tests_baseline_full.out") if False else None
out = []
p, f, e = tot(rel)
ids = sorted(i for v in rel.values() for i in v["ids"])
out.append("OG-rl-14 step 3 (r28b): release tree aa75078e1b (/c/tmp/og-rel24), each test file in its own pytest process, scratch AUDIT_PATH")
out.append("release tree aa75078e1b: files %d passed %d failed %d errors %d" % (len(rel), p, f, e))
out.append("release failing ids (%d): %s" % (len(ids), "; ".join(ids)))
BASE = ["tests/acceptance/test_local_acceptance.py::test_ogv2_a12", "tests/test_blackdiamond.py::test_mx_t13_catalog_gated",
        "tests/test_portal_grant.py::test_asker_portal_scope_admits_granted_channel", "tests/test_portal_grant.py::test_asker_portal_scope_refuses_other_channel",
        "tests/test_portal_index.py::test_portal_tools_catalog_refs_resolve", "tests/test_schwab_export_stream.py::test_ogx4_ac03",
        "tests/test_schwab_host_inputs.py::test_grant_writer_stages_the_contract_only_from_the_standard"]
out.append("baseline failing ids (7, from the live tree 510c8cfed2 run of Phase A, r28_tests_summary.out): in release failing set %d of 7; failing on release not in baseline %s; baseline not failing on release %s" % (
    sum(1 for b in BASE if b in ids), [i for i in ids if i not in BASE], [b for b in BASE if b not in ids]))
bg = rel.get("tests/test_deploy_base_guard.py")
out.append("tests/test_deploy_base_guard.py: release r28b %s; Phase A release 419297b525 %s; live baseline (6 passed 0 failed 0 errors)" % (
    (bg["passed"], bg["failed"], bg["errors"]), (old["tests/test_deploy_base_guard.py"]["passed"], old["tests/test_deploy_base_guard.py"]["failed"], old["tests/test_deploy_base_guard.py"]["errors"])))
for fn in ("tests/test_audit_lake_key_stamp.py", "tests/test_deploy_host_pip_no_upgrade.py", "tests/test_deploy_install_no_fetch.py", "tests/test_deploy_install_no_fetch_complete.py",
           "tests/test_audit_bytes_principal.py", "tests/test_audit_rivalfunds_args.py", "tests/test_schwab_audit.py"):
    v = rel.get(fn)
    out.append("%s: %s" % (fn, (v["passed"], v["failed"], v["errors"]) if v else None))
diff = [k for k in rel if (rel[k]["passed"], rel[k]["failed"], rel[k]["errors"]) != ((old.get(k) or {}).get("passed"), (old.get(k) or {}).get("failed"), (old.get(k) or {}).get("errors"))]
out.append("files whose (passed, failed, errors) differ from the Phase A run on 419297b525: %s" % diff)
out.append("pytest rc per file: nonzero in %s" % sorted(k for k, v in rel.items() if v["rc"] not in ("0",)))
s = "\n".join(out) + "\n"
open(os.path.join(HERE, "r28b_tests_summary.out"), "w", encoding="utf-8", newline="\n").write(s)
print(s)
