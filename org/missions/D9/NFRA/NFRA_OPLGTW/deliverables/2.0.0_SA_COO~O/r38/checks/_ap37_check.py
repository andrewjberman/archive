#!/usr/bin/env python
"""OPLGTW OG-ap-37 grading: landing dell1's gateway release (AMGT_HARVST HVST-cd-2, 1753c741d9) on the sitez trunk.

Record W/ap37_landing.json = {"trunk_base_sha", "dell_sha", "merge_sha", "manifest_source": "dell1_commit"|"landing_row",
                              "manifest_sha": <the dell1 commit carrying the manifest; for dell1_commit>, "host_md5_record": <path; for landing_row>}.
mode 1 = merge shape and content (AC1); mode 2 = the manifest block (AC2). Stdlib only; reads the repo by git plumbing (never the working tree).
"""
import json
import re
import subprocess
import sys

GW = "infra/aws/ec2/opal-gateway/"
DELL_FILES = (GW + "app/harvest_research.py", GW + "tests/test_cd1_dossier_misfiled.py")
MANIFEST = "infra/aws/ec2/EC2_MANIFEST.json"
LIVE_NEW = "1753c741d988faa05fa424386bcd9aa0c5efbf71"
LIVE_OLD = "9d5b7125571520b977401634a01935924f4c9787"
# a path the merge may differ from trunk_base in, beyond the two dell1 files and the manifest: the ledger, its sentinel, and project trees
OTHER_OK = re.compile(r"^(org/critical_paths/(change_management|\.open_deploys)/|org/missions/|org/tier1_exec/|org/tier2_exec/)")


def git(*args, check=True):
    p = subprocess.run(("git",) + args, capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args[:3]), p.stderr.decode("utf-8", "replace")[:200]))
    return p.stdout


def blob(rev, path):
    p = subprocess.run(["git", "rev-parse", "%s:%s" % (rev, path)], capture_output=True)
    return p.stdout.decode().strip() if p.returncode == 0 else ""


def names(a, b):
    out = git("diff", "--name-only", a, b).decode("utf-8", "replace")
    return [x for x in out.splitlines() if x]


def manifest_block(rev):
    raw = git("show", "%s:%s" % (rev, MANIFEST))
    return json.loads(raw.decode("utf-8"))


def main():
    mode = sys.argv[2]
    rec = json.load(open(sys.argv[1], encoding="utf-8"))
    base, dell, merge = rec.get("trunk_base_sha", ""), rec.get("dell_sha", ""), rec.get("merge_sha", "")
    src = rec.get("manifest_source", "")
    for label, sha in (("trunk_base_sha", base), ("dell_sha", dell), ("merge_sha", merge)):
        if subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], capture_output=True).returncode != 0:
            print("%s %s is not a commit here" % (label, sha[:10]))
            print("RESULT: FAIL")
            return 1
    if mode == "1":
        parents = git("rev-list", "--parents", "-n", "1", merge).decode().split()[1:]
        target = dell   # the merge parent is dell1's release commit; the manifest commit (manifest_sha) may already be an ancestor of trunk_base
        two = len(parents) == 2 and parents[0] == base and parents[1] == target
        anc = subprocess.run(["git", "merge-base", "--is-ancestor", dell, merge], capture_output=True).returncode == 0
        mt = subprocess.run(["git", "merge-tree", "--write-tree", "--name-only", base, target], capture_output=True)
        conflicted = [x for x in mt.stdout.decode("utf-8", "replace").splitlines()[1:] if x and "/" in x and not x.startswith(("Auto-merging", "CONFLICT"))]
        conflicted = [x for x in conflicted if re.match(r"^[A-Za-z0-9_.@~/-]+$", x)]
        marker_paths = 0
        for p in conflicted:
            b = subprocess.run(["git", "show", "%s:%s" % (merge, p)], capture_output=True).stdout
            if re.search(rb"^(<<<<<<<|>>>>>>>) ", b, re.M):
                marker_paths += 1
        diff = names(base, merge)
        gw_diff = sorted(p for p in diff if p.startswith(GW))
        gw_ok = len(gw_diff) == 0   # trunk already carries dell1's two files byte-equal (the AMGT_HARVST worker lineage landed them); the merge changes no gateway byte
        dell_eq = all(blob(merge, p) == blob(dell, p) and blob(merge, p) != "" for p in DELL_FILES)
        tf = [p for p in diff if p.endswith(".tf")]
        outside = [p for p in diff if not (p.startswith(GW) or p == MANIFEST or OTHER_OK.match(p))]
        print("merge parents are exactly trunk_base and the dell1 commit: %s; dell1's release is an ancestor of the merge: %s; conflicted paths (merge-tree, the denominator): %d; conflict markers in %d of %d paths (want 0)" % (
            "yes" if two else "no", "yes" if anc else "no", len(conflicted), marker_paths, len(conflicted)))
        print("gateway paths differing from trunk_base: %d (want 0, the merge changes no gateway byte); the two dell1 files equal dell1's blobs in the merge: %s; terraform files differing %d (want 0); paths outside the allowed set %d (want 0)" % (
            len(gw_diff), "yes" if dell_eq else "no", len(tf), len(outside)))
        ok = two and anc and marker_paths == 0 and gw_ok and dell_eq and not tf and not outside
        print("RESULT: PASS" if ok else "RESULT: FAIL")
        return 0 if ok else 1
    # mode 2: the manifest block
    mf = manifest_block(merge)
    mb = manifest_block(base)
    svc = (mf.get("services") or {}).get("opal-gateway") or {}
    dep, prev = svc.get("deployed_commit"), svc.get("previous_deployed_commit")
    block_ok = dep == LIVE_NEW and prev == LIVE_OLD
    others_ok = all(((mf.get("services") or {}).get(k) == v) for k, v in (mb.get("services") or {}).items() if k != "opal-gateway")
    top_ok = {k: v for k, v in mf.items() if k != "services"} == {k: v for k, v in mb.items() if k != "services"}
    gw_other = {k: v for k, v in svc.items() if k not in ("deployed_commit", "previous_deployed_commit", "file_checksums", "deployed_at", "deployed_by")}
    gw_other_base = {k: v for k, v in ((mb.get("services") or {}).get("opal-gateway") or {}).items() if k not in ("deployed_commit", "previous_deployed_commit", "file_checksums", "deployed_at", "deployed_by")}
    gw_other_ok = gw_other == gw_other_base
    if src == "dell1_commit":
        ms = rec.get("manifest_sha", "")
        src_ok = bool(ms) and blob(merge, MANIFEST) == blob(ms, MANIFEST) or (bool(ms) and subprocess.run(["git", "merge-base", "--is-ancestor", ms, merge], capture_output=True).returncode == 0)
        src_line = "manifest source: dell1's own commit %s (an ancestor of the merge): %s" % (ms[:10], "yes" if src_ok else "no")
    elif src == "landing_row":
        hm = rec.get("host_md5_record", "")
        try:
            d = json.load(open(hm, encoding="utf-8"))
            d = d.get("body", d)
            eq, df = d.get("equal"), d.get("differ")
            src_ok = isinstance(eq, int) and eq >= 100 and df == 0 and d.get("tree_sha") == LIVE_NEW
        except Exception:
            eq, df, src_ok = None, None, False
        src_line = "manifest source: this landing's row, proven by a host md5 walk equal to the 1753c741d9 tree (equal %s, differ %s): %s" % (eq, df, "yes" if src_ok else "no")
    else:
        src_ok, src_line = False, "manifest source not named (want dell1_commit or landing_row)"
    print("manifest opal-gateway deployed_commit %s previous %s (want 1753c741d9 and 9d5b712557): %s" % ((dep or "none")[:10], (prev or "none")[:10], "yes" if block_ok else "no"))
    print("other services and the top level unchanged from trunk_base: %s; the gateway block's other keys unchanged: %s" % ("yes" if (others_ok and top_ok) else "no", "yes" if gw_other_ok else "no"))
    print(src_line)
    ok = block_ok and others_ok and top_ok and gw_other_ok and src_ok
    print("RESULT: PASS" if ok else "RESULT: FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
