"""ADVI_FIRMBKTS round 6, cell FB-i-1 (FWD-1: ONE blind read of all 150 canonical locations under the stated face), issuer 2.0.0_SA_COO~B1.

  build  --dir D     cut the 150-location list (the canonical arm of round 4's READING_KEY.json, the same 150 locations with fresh ids)
                     as ONE blob in a parentless one-commit history and make one detached worktree of it; write READING_KEY.json,
                     LOCATIONS.sha256 and READER_COMMIT.txt beside this file's round. Run once, at the cut.
  reader --dir D     grade the one reader's directory (4 arms R1-R4: the index is LOCATIONS.json alone, one parentless commit,
                     the cut's bytes, answers complete). Agreement is not graded here.
  agree  --dir D     the issuer's real run: per field equality with the key over the 150 (the key's `table` is the mapping's own
                     dest.table; the key never travels), and the not-equal locations named.
Plain ASCII output. Never edit this file after the cut.
"""
import argparse
import hashlib
import json
import os
import random
import re
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
R4 = DELIV + "/2.0.0_SA_COO~B1/round4"
R6 = DELIV + "/2.0.0_SA_COO~B1/round6"
SEED = 20261013
FIELDS = ("system", "firm", "tier", "table")
ANS_FIELDS = FIELDS + ("contents",)
ENV = {"GIT_AUTHOR_NAME": "reader-cut", "GIT_AUTHOR_EMAIL": "reader-cut@opal.agent",
       "GIT_COMMITTER_NAME": "reader-cut", "GIT_COMMITTER_EMAIL": "reader-cut@opal.agent",
       "GIT_AUTHOR_DATE": "2026-10-13T08:00:00Z", "GIT_COMMITTER_DATE": "2026-10-13T08:00:00Z"}


def _root(arg=None):
    return arg or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _git(root, *a, inp=None, env=False):
    e = dict(os.environ)
    if env:
        e.update(ENV)
    data = inp.encode("ascii") if inp is not None else None
    r = subprocess.run(["git", "-C", root] + list(a), input=data, capture_output=True, env=e)
    if r.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(a[:2]), r.stderr.decode("ascii", "replace").strip()[:200]))
    return r.stdout.decode("ascii", "replace").strip()


def _norm(v):
    return re.sub(r"[^a-z0-9]", "", str(v).lower())


def _load(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def build(a):
    if os.path.exists(a.dir):
        print("REFUSED: %s exists" % a.dir)
        return 2
    root = _root(a.root)
    k4 = _load(os.path.join(root, R4, "READING_KEY.json"))
    locs4 = {e["id"]: e["location"] for e in _load(a.locations)["locations"]}
    ids = sorted(i for i, v in k4.items() if v["arm"] == "canonical")
    rng = random.Random(SEED)
    rng.shuffle(ids)
    used, locs, key = set(), [], {}
    for r4 in ids:
        while True:
            i = "%08x" % rng.getrandbits(32)
            if i not in used and "opal" not in i:
                used.add(i)
                break
        locs.append({"id": i, "location": locs4[r4]})
        key[i] = {"arm": "canonical", "class": k4[r4]["class"], "bucket": k4[r4]["bucket"], "r4_id": r4,
                  "truth": k4[r4]["truth"]}
    body = json.dumps({"locations": locs}, indent=1, ensure_ascii=True) + "\n"
    sha = hashlib.sha256(body.encode("ascii")).hexdigest()
    blob = _git(root, "hash-object", "-w", "--stdin", inp=body)
    tree = _git(root, "mktree", inp="100644 blob %s\tLOCATIONS.json\n" % blob)
    commit = _git(root, "commit-tree", tree, "-m", "reader location list", env=True)
    _git(root, "worktree", "add", "--detach", a.dir, commit)
    os.makedirs(os.path.join(root, R6), exist_ok=True)
    for name, text in (("READING_KEY.json", json.dumps(key, indent=1, ensure_ascii=True)),
                       ("LOCATIONS.sha256", sha + "\n"), ("READER_COMMIT.txt", commit + "\n")):
        with open(os.path.join(root, R6, name), "w", encoding="ascii", newline="\n") as fh:
            fh.write(text)
    print("OK: %d locations (the canonical arm of round 4); sha256 %s; commit %s; worktree %s" % (len(locs), sha, commit, a.dir))
    return 0


def reader(a):
    root = _root(a.root)
    res = []
    try:
        with open(os.path.join(a.dir, "LOCATIONS.json"), "rb") as fh:
            raw = fh.read()
        ids = [e["id"] for e in json.loads(raw.decode("ascii"))["locations"]]
        doc = _load(os.path.join(a.dir, "ANSWERS.json"))
        answers = doc.get("answers") or []
        got = [x.get("id") for x in answers]
        dup, missing, extra = len(got) - len(set(got)), set(ids) - set(got), set(got) - set(ids)
        print("  locations=%d answers=%d duplicates=%d unanswered=%d unknown ids=%d"
              % (len(ids), len(answers), dup, len(missing), len(extra)))
        res.append(("R1 every location id is answered exactly once, by a named worker serial",
                    bool(ids) and not dup and not missing and not extra and str(doc.get("reader", "")).startswith("0.9.0_WK_")))
        blank = [x.get("id") for x in answers
                 if not all(isinstance(x.get(f), str) and x.get(f).strip() for f in ANS_FIELDS)]
        print("  answers with a blank field: %d" % len(blank))
        res.append(("R2 every answer names system, firm, tier, table and contents (a field may read 'unknown')",
                    not blank and bool(answers)))
        ondisk = sorted(n for n in os.listdir(a.dir) if n != ".git")
        tracked = _git(a.dir, "ls-files").split()
        log = _git(a.dir, "log", "--format=%H").split()
        head = _git(a.dir, "rev-parse", "HEAD")
        inside = _git(a.dir, "rev-parse", "--is-inside-work-tree")
        with open(os.path.join(root, R6, "READER_COMMIT.txt"), encoding="ascii") as fh:
            want_commit = fh.read().strip()
        with open(os.path.join(root, R6, "LOCATIONS.sha256"), encoding="ascii") as fh:
            want = fh.read().strip()
        same = hashlib.sha256(raw).hexdigest() == want
        print("  WORKTREE %s: inside=%s tracked=%s commits=%d head==cut=%s on disk=%s sha256 equals the cut: %s"
              % (a.dir, inside, tracked, len(log), head == want_commit, ondisk, same))
        res.append(("R3 the index is LOCATIONS.json alone, the history is the issuer's one commit, the files on disk are "
                    "LOCATIONS.json and ANSWERS.json, the list is the cut byte for byte",
                    inside == "true" and tracked == ["LOCATIONS.json"] and log == [want_commit] and head == want_commit
                    and ondisk == sorted(["LOCATIONS.json", "ANSWERS.json"]) and same))
        wl = _git(a.dir, "worktree", "list", "--porcelain")
        print("  git worktree list (first lines): %s" % " | ".join(wl.split("\n")[:3]))
        res.append(("R4 the listing the CVO reads before grading was printed", bool(wl)))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.dir, type(e).__name__))
        res = [("ANSWERS.json and LOCATIONS.json present", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 6 READER: %d of 4 arms" % n)
    return 0 if n == 4 else 1


def agree(a):
    root = _root(a.root)
    key = _load(os.path.join(root, R6, "READING_KEY.json"))
    locs = {e["id"]: e["location"] for e in _load(os.path.join(a.dir, "LOCATIONS.json"))["locations"]}
    doc = _load(os.path.join(a.dir, "ANSWERS.json"))
    ra = {x["id"]: x for x in doc["answers"]}
    print("reader=%s; locations=%d; key=%d" % (doc.get("reader"), len(locs), len(key)))
    ids = sorted(key)
    line = ["canonical n=%d" % len(ids)]
    for f in FIELDS:
        eq = sum(1 for i in ids if _norm(ra[i][f]) == _norm(key[i]["truth"][f]))
        unk = sum(1 for i in ids if _norm(ra[i][f]) == "unknown")
        line.append("%s equals the key %d of %d (unknown %d)" % (f, eq, len(ids), unk))
    allf = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(key[i]["truth"][f]) for f in FIELDS))
    line.append("all four equal the key %d of %d" % (allf, len(ids)))
    print(" | ".join(line))
    for i in ids:
        if not all(_norm(ra[i][f]) == _norm(key[i]["truth"][f]) for f in FIELDS):
            print("  NOT-EQUAL %s class=%s key=%s answer=%s" % (
                i, key[i]["class"], "/".join(key[i]["truth"][f] for f in FIELDS), "/".join(ra[i][f] for f in FIELDS)))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--dir", required=True)
    b.add_argument("--locations", required=True, help="round 4's LOCATIONS.json (an issuer-held copy)")
    b.add_argument("--root")
    r = sub.add_parser("reader")
    r.add_argument("--dir", required=True)
    r.add_argument("--root")
    g = sub.add_parser("agree")
    g.add_argument("--dir", required=True)
    g.add_argument("--root")
    a = ap.parse_args()
    return {"build": build, "reader": reader, "agree": agree}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
