"""ADVI_FIRMBKTS round 4: cut the readers' location list and build the two reader worktrees (FB-g-4, FB-g-5), issuer
2.0.0_SA_COO~B1. The CTO's ruling (ROUND_ANALYSIS.round3.md section 3 item 3): independence BY CONSTRUCTION -- two readers,
each in a worktree that holds ONLY the location list; the CVO lists each worktree before grading.

Construction: the list is written as ONE blob, wrapped in a one-file tree and a parentless commit (git plumbing, no branch,
no checkout of the project), and each reader's worktree is a detached worktree of that commit. The worktree therefore
holds `LOCATIONS.json` and nothing else, and `git log` in it shows one commit. A sparse checkout would hold the same single
path of a full history; this holds it of a one-commit history, so the listing and the log both carry the property.

--dir-a, --dir-b      the two worktree paths (outside any checkout; must not exist)
--sample N            placed classes sampled (default 150: N canonical + N legacy locations)
Run once, at the cut. Prints the sha256 of the list and the commit id the worktrees sit on.
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
OUT = DELIV + "/2.0.0_SA_COO~B1/round4"
SEED = 20261014
ENV = {"GIT_AUTHOR_NAME": "reader-cut", "GIT_AUTHOR_EMAIL": "reader-cut@opal.agent",
       "GIT_COMMITTER_NAME": "reader-cut", "GIT_COMMITTER_EMAIL": "reader-cut@opal.agent",
       "GIT_AUTHOR_DATE": "2026-10-11T12:00:00Z", "GIT_COMMITTER_DATE": "2026-10-11T12:00:00Z"}


def _git(root, *a, inp=None):
    env = dict(os.environ)
    env.update(ENV)
    data = inp.encode("ascii") if inp is not None else None  # bytes: text mode would write CRLF on Windows
    r = subprocess.run(["git", "-C", root] + list(a), input=data, capture_output=True, env=env)
    if r.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(a[:2]), r.stderr.decode("ascii", "replace").strip()[:200]))
    return r.stdout.decode("ascii", "replace").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir-a", required=True)
    ap.add_argument("--dir-b", required=True)
    ap.add_argument("--sample", type=int, default=150)
    a = ap.parse_args()
    for d in (a.dir_a, a.dir_b):
        if os.path.exists(d):
            print("REFUSED: %s exists" % d)
            return 2
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(root, DELIV, "mapping_v3.json"), encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    with open(os.path.join(root, DELIV, "census.json"), encoding="utf-8") as fh:
        census = json.load(fh)
    sample = {(b, c["prefix"]): c["sample_key"] for b, bd in census["buckets"].items() for c in bd["classes"]}
    placed = [r for r in rows if r.get("disposition") in ("MOVE", "HOME") and (r["bucket"], r["prefix"]) in sample
              and isinstance(r.get("dest"), dict) and r.get("address")]
    rng = random.Random(SEED)
    rng.shuffle(placed)
    chosen = placed[:a.sample]
    items = []
    for r in chosen:
        items.append(("canonical", r["address"], r))
        items.append(("legacy", "s3://%s/%s" % (r["bucket"], sample[(r["bucket"], r["prefix"])]), r))
    rng.shuffle(items)
    used, locs, key = set(), [], {}
    for arm, location, r in items:
        while True:
            i = "%08x" % rng.getrandbits(32)
            if i not in used and "opal" not in i:
                used.add(i)
                break
        locs.append({"id": i, "location": location})
        d = r["dest"]
        key[i] = {"arm": arm, "class": r["prefix"], "bucket": r["bucket"],
                  "truth": {"system": d["source"], "firm": d["scope"], "tier": d["tier"], "table": d["table"]}}
    body = json.dumps({"locations": locs}, indent=1, ensure_ascii=True) + "\n"
    sha = hashlib.sha256(body.encode("ascii")).hexdigest()
    blob = _git(root, "hash-object", "-w", "--stdin", inp=body)
    tree = _git(root, "mktree", inp="100644 blob %s\tLOCATIONS.json\n" % blob)
    commit = _git(root, "commit-tree", tree, "-m", "reader location list")
    for d in (a.dir_a, a.dir_b):
        _git(root, "worktree", "add", "--detach", d, commit)
    os.makedirs(os.path.join(root, OUT), exist_ok=True)
    with open(os.path.join(root, OUT, "READING_KEY.json"), "w", encoding="ascii", newline="\n") as fh:
        json.dump(key, fh, indent=1, ensure_ascii=True)
    with open(os.path.join(root, OUT, "LOCATIONS.sha256"), "w", encoding="ascii", newline="\n") as fh:
        fh.write(sha + "\n")
    with open(os.path.join(root, OUT, "READER_COMMIT.txt"), "w", encoding="ascii", newline="\n") as fh:
        fh.write(commit + "\n")
    n_c = sum(1 for v in key.values() if v["arm"] == "canonical")
    print("OK: %d locations (%d canonical, %d legacy) from %d placed classes of mapping_v3; sha256 %s; commit %s; "
          "worktrees %s %s" % (len(locs), n_c, len(locs) - n_c, len(placed), sha, commit, a.dir_a, a.dir_b))
    return 0


if __name__ == "__main__":
    sys.exit(main())
