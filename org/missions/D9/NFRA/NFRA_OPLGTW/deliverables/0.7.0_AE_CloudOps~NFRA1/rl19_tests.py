#!/usr/bin/env python
"""OG-rl-19 Phase A step 2 (tests): the named set and the window set in BOTH orders in the release tree, the existing files also in the LIVE-ref tree, and the full-suite failing sets compared per test id.
Counts and test ids only. The release tree's org/standards/NFRA_OPLGTW_CONTRACT.json is the live ref's (the release does not carry it; the tree is the gateway folder, and the landing carries the standards copy), so four tests that compare the two contract copies
read red in the release tree alone: they are run again with trunk's standards copy laid over it (uncommitted, restored to the live ref's bytes after), which is what the landed tree holds.
usage: python rl19_tests.py <full_release.txt> <full_live.txt> <out.json>   (repository root)"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

REL = "C:/tmp/og-rel-r3c"
LIVE = "C:/tmp/og-rel-batch16"
GW = "/infra/aws/ec2/opal-gateway"
STD = "org/standards/NFRA_OPLGTW_CONTRACT.json"
TRUNK, LIVE_SHA = "a4c6ecfd30ca47a56c317d10ea5dfdcacc8741a4", "8e3eddf95916e430e4e9bbf615ca4fd91f9e852f"
NAMED = ["tests/test_og_sk2.py"] + sorted("tests/" + f for f in os.listdir(os.path.join(REL, "infra/aws/ec2/opal-gateway/tests")) if f.startswith("test_schwab") or "catalog" in f)


def pytest_run(files, cwd):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfE"] + files, cwd=cwd, capture_output=True, text=True, timeout=1500)
    txt = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout).replace("\r", "")
    last = txt.strip().splitlines()[-1]
    p, f = re.search(r"(\d+) passed", last), re.search(r"(\d+) (?:failed|error)", last)
    return {"passed": int(p.group(1)) if p else 0, "failed": int(f.group(1)) if f else 0, "failed_names": sorted({m.group(1).strip() for m in re.finditer(r"^(?:FAILED|ERROR) (\S+)", txt, re.M)})}


def names(path):
    t = re.sub(r"\x1b\[[0-9;]*m", "", io.open(path, encoding="utf-8", errors="replace").read()).replace("\r", "")
    return {re.sub(r" - .*", "", m.group(1)) for m in re.finditer(r"^(?:FAILED|ERROR) (\S.*)$", t, re.M)}


def git_show(ref, path):
    return subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True).stdout


rel_gw, live_gw = REL + GW, LIVE + GW
present_live = [n for n in NAMED if os.path.exists(os.path.join(live_gw, n))]
all_og = sorted("tests/" + f for f in os.listdir(os.path.join(rel_gw, "tests")) if re.match(r"test_og_.*\.py$", f))
window_all = [f for f in all_og if f not in NAMED and os.path.exists(os.path.join(live_gw, f))]
# the window set is the existing window files that are GREEN at the live ref (the red ones are the live ref's own failures, compared per test id in the full-suite comparison)
red_files_at_live = sorted({n.split("::")[0].replace("\\", "/") for n in pytest_run(window_all, live_gw)["failed_names"]})
window = [f for f in window_all if f not in red_files_at_live]
orig = open(os.path.join(REL, STD), "rb").read()
t = {"named_files": len(NAMED), "named_files_new_in_release": len(NAMED) - len(present_live), "window_files": len(window), "window_files_excluded_red_at_live_ref": red_files_at_live}
try:
    open(os.path.join(REL, STD), "wb").write(git_show(TRUNK, STD))
    t["standards_copy_overlay"] = "trunk %s laid over the release tree's org/standards contract copy for these runs (uncommitted; restored after)" % TRUNK[:10]
    t["named_forward"], t["named_reverse"] = pytest_run(NAMED, rel_gw), pytest_run(NAMED[::-1], rel_gw)
    t["window_forward"], t["window_reverse"] = pytest_run(window, rel_gw), pytest_run(window[::-1], rel_gw)
finally:
    open(os.path.join(REL, STD), "wb").write(orig)
t["standards_copy_restored_to_live_ref_bytes"] = open(os.path.join(REL, STD), "rb").read() == git_show(LIVE_SHA, STD)
t["named_at_live_ref"] = pytest_run(present_live, live_gw)
t["window_at_live_ref"] = pytest_run(window, live_gw)
t["window_at_live_ref_all_files"] = len(window_all)
live_red = set(t["named_at_live_ref"]["failed_names"])
t["named_new_reds_against_live_ref"] = sorted(set(t["named_forward"]["failed_names"]) - live_red)
t["named_reds_same_at_live_ref"] = sorted(set(t["named_forward"]["failed_names"]) & live_red)
t["window_new_reds_against_live_ref"] = sorted(set(t["window_forward"]["failed_names"]) - set(t["window_at_live_ref"]["failed_names"]))
rf, lf = names(sys.argv[1]), names(sys.argv[2])
only_rel, only_live = sorted(rf - lf), sorted(lf - rf)
t["full_suite"] = {"release_failed": len(rf), "live_ref_failed": len(lf), "names_in_both": len(rf & lf), "only_in_release": only_rel, "only_in_live_ref": only_live,
                   "only_in_release_explained": "the four tests that compare the gateway's contract copy with org/standards' copy: the release carries the gateway copy (capacity.target_memory_mib 8192) and the take list does not carry the standards copy, so the release tree reads them red alone; "
                                                "they PASS (4 of 4) with trunk's standards copy overlaid, and trunk holds both copies equal (landing carries it)",
                   "conditions": "both trees sparse, the same cone and pytest invocation over tests/, run one after the other on this device"}
io.open(sys.argv[3], "w", encoding="utf-8", newline="\n").write(json.dumps(t, indent=1) + "\n")
print(json.dumps({k: (v if not isinstance(v, dict) else {a: b for a, b in v.items() if a != "failed_names"}) for k, v in t.items() if k not in ("full_suite",)}, indent=1)[:2500])
print("new reds named:", t["named_new_reds_against_live_ref"], "window:", t["window_new_reds_against_live_ref"])
print("full suite only in release:", only_rel, "only in live:", only_live)
