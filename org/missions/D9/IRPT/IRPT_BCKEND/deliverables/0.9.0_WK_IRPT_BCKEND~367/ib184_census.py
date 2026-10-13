"""IRPT_BCKEND IB-pr-518 (worker 0.9.0_WK_IRPT_BCKEND~367): member diff and census record for irpt-ycharts-generate.

Usage: python ib184_census.py <built_b1.zip> <built_b2.zip> <live.zip> <repo_root> <pin_commit> <base_commit>
          <source_map_sha256_before> <source_map_sha256_after_restore> <out_census.json>
Reads the three zips in memory (outside the worktree). Reads repo blobs with git cat-file at the pin.
Prints member NAMES and counts only; no client data is read. Writes the census JSON (not uploaded anywhere).
The signature instrument output is passed in via the two result files named by env SIG_BUILT and SIG_LIVE.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile

FN = "irpt-ycharts-generate"
REPO_PATH = {
    "maintained_sources.py": "infra/aws/lambda/investor-reporting/_scope/maintained_sources.py",
    "templates.json": "infra/aws/lambda/investor-reporting/ycharts/generate/templates.json",
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git_blob(root, pin, path):
    r = subprocess.run(["git", "-C", root, "cat-file", "-p", "%s:%s" % (pin, path)], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def attr_lines(path):
    out = []
    summary = None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("ATTR_MISMATCH: "):
            out.append(line)
        if line.startswith("signature_closure "):
            summary = line
    return out, summary


def parse_summary(s):
    d = {}
    for k, v in re.findall(r"(\w+)=(\d+)", s or ""):
        d[k] = int(v)
    return d


def main():
    b1, b2, live, root, pin, base, sm_before, sm_after, out = sys.argv[1:10]
    z1 = open(b1, "rb").read()
    z2 = open(b2, "rb").read()
    zl = open(live, "rb").read()
    built_sha, built2_sha, live_sha = sha(z1), sha(z2), sha(zl)
    bz = zipfile.ZipFile(b1)
    lz = zipfile.ZipFile(live)
    bn, ln = sorted(bz.namelist()), sorted(lz.namelist())
    print("built members=%d live members=%d" % (len(bn), len(ln)))
    print("only_in_built=%d only_in_live=%d" % (len(set(bn) - set(ln)), len(set(ln) - set(bn))))
    same, changed = 0, []
    for n in sorted(set(bn) & set(ln)):
        if bz.read(n) == lz.read(n):
            same += 1
        else:
            changed.append(n)
    print("identical_members=%d changed_members=%d" % (same, len(changed)))
    changed_rec = []
    for n in changed:
        leaf = n.split("/")[-1]
        bsha = sha(bz.read(n))
        if leaf not in REPO_PATH:
            print("CHANGED_OTHER: %s built_member_sha256=%s" % (n, bsha))
            changed_rec.append({"name": n, "built_member_sha256": bsha, "repo_blob_sha256_at_pin": None})
            continue
        blob = git_blob(root, pin, REPO_PATH[leaf])
        rsha = sha(blob) if blob is not None else None
        print("CHANGED: %s built_member_sha256=%s repo_blob_sha256_at_pin=%s equal=%s" % (n, bsha, rsha, bsha == rsha))
        changed_rec.append({"name": leaf, "built_member_sha256": bsha, "repo_blob_sha256_at_pin": rsha,
                            "repo_path": REPO_PATH[leaf]})
    bl, bs = attr_lines(os.environ["SIG_BUILT"])
    ll, ls = attr_lines(os.environ["SIG_LIVE"])
    bsum, lsum = parse_summary(bs), parse_summary(ls)
    rec = {
        "base_commit": base,
        "pin_commit": pin,
        "uploaded": False,
        "source_map": {
            "rows_edited_in_scratch_worktree": 1,
            "restored": True,
            "sha256_before": sm_before,
            "sha256_after_restore": sm_after,
        },
        "functions": [{
            "function": FN,
            "built_sha256": built_sha,
            "live_sha256": live_sha,
            "built_twice_identical": built_sha == built2_sha,
            "built_signature_mismatched": bsum.get("mismatched", -1),
            "live_signature_mismatched": lsum.get("mismatched", -1),
            "built_attribute_mismatched": bsum.get("attr_mismatched", -1),
            "live_attribute_mismatched": lsum.get("attr_mismatched", -1),
            "attribute_mismatch_lines_built": bl,
            "attribute_mismatch_lines_live": ll,
            "changed_members": changed_rec,
        }],
    }
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=2)
        fh.write("\n")
    print("census written: built_sha256=%s live_sha256=%s built_twice_identical=%s" % (built_sha, live_sha, built_sha == built2_sha))
    print("sig built: %s" % bs)
    print("sig live : %s" % ls)


if __name__ == "__main__":
    main()
