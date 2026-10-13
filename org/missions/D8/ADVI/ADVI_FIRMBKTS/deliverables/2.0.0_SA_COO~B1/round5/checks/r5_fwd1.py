"""ADVI_FIRMBKTS round 5, cells FB-h-1 and FB-h-2 (FWD-1's re-read of the 11 disagreements), issuer 2.0.0_SA_COO~B1.

  build  --dir-a A --dir-b B   cut the 22-location list (the 11 round-4 canonical disagreements, FWD1_R4_DISAGREEMENTS.json,
                               plus 11 locations both round-4 readers got right, seeded) as ONE blob in a parentless
                               one-commit history, and make two detached worktrees of it; write READING_KEY.json,
                               LOCATIONS.sha256 and READER_COMMIT.txt beside this file's round. Run once, at the cut.
  reader --reader A|B --dir D  grade one reader's directory (4 arms R1-R4, as round 4's r4_reader.py; independence by
                               construction: the index is LOCATIONS.json alone, one parentless commit, the cut's bytes).
  agree  --dir-a A --dir-b B   the issuer's real run: per field agreement and equality with the key, over the 22; the
                               11 named and the 11 controls are printed apart.
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
R5 = DELIV + "/2.0.0_SA_COO~B1/round5"
SEED = 20261013
FIELDS = ("system", "firm", "tier", "table")
ANS_FIELDS = FIELDS + ("contents",)
ENV = {"GIT_AUTHOR_NAME": "reader-cut", "GIT_AUTHOR_EMAIL": "reader-cut@opal.agent",
       "GIT_COMMITTER_NAME": "reader-cut", "GIT_COMMITTER_EMAIL": "reader-cut@opal.agent",
       "GIT_AUTHOR_DATE": "2026-10-13T07:00:00Z", "GIT_COMMITTER_DATE": "2026-10-13T07:00:00Z"}


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
    for d in (a.dir_a, a.dir_b):
        if os.path.exists(d):
            print("REFUSED: %s exists" % d)
            return 2
    root = _root(a.root)
    src = _load(os.path.join(root, R5, "FWD1_R4_DISAGREEMENTS.json"))
    rng = random.Random(SEED)
    dis = list(src["disagreements"])
    pool = sorted(src["agreed_and_right"], key=lambda r: r["r4_id"])
    rng.shuffle(pool)
    seen, ctl = set(), []
    for r in pool:
        if r["class"] in seen:
            continue
        seen.add(r["class"])
        ctl.append(r)
        if len(ctl) == len(dis):
            break
    items = [("disagreed", r) for r in dis] + [("control", r) for r in ctl]
    rng.shuffle(items)
    used, locs, key = set(), [], {}
    k4 = _load(os.path.join(root, DELIV, "2.0.0_SA_COO~B1", "round4", "READING_KEY.json"))
    for arm, r in items:
        while True:
            i = "%08x" % rng.getrandbits(32)
            if i not in used and "opal" not in i:
                used.add(i)
                break
        locs.append({"id": i, "location": r["location"]})
        key[i] = {"arm": arm, "class": r["class"], "bucket": r["bucket"], "r4_id": r["r4_id"],
                  "truth": k4[r["r4_id"]]["truth"]}
    body = json.dumps({"locations": locs}, indent=1, ensure_ascii=True) + "\n"
    sha = hashlib.sha256(body.encode("ascii")).hexdigest()
    blob = _git(root, "hash-object", "-w", "--stdin", inp=body)
    tree = _git(root, "mktree", inp="100644 blob %s\tLOCATIONS.json\n" % blob)
    commit = _git(root, "commit-tree", tree, "-m", "reader location list", env=True)
    for d in (a.dir_a, a.dir_b):
        _git(root, "worktree", "add", "--detach", d, commit)
    os.makedirs(os.path.join(root, R5), exist_ok=True)
    for name, text in (("READING_KEY.json", json.dumps(key, indent=1, ensure_ascii=True)),
                       ("LOCATIONS.sha256", sha + "\n"), ("READER_COMMIT.txt", commit + "\n")):
        with open(os.path.join(root, R5, name), "w", encoding="ascii", newline="\n") as fh:
            fh.write(text)
    print("OK: %d locations (%d disagreed in round 4, %d controls); sha256 %s; commit %s; worktrees %s %s"
          % (len(locs), len(dis), len(ctl), sha, commit, a.dir_a, a.dir_b))
    return 0


def reader(a):
    root = _root(a.root)
    res = []
    try:
        with open(os.path.join(a.dir, "LOCATIONS.json"), "rb") as fh:
            raw = fh.read()
        ids = [e["id"] for e in json.loads(raw.decode("ascii"))["locations"]]
        doc = _load(os.path.join(a.dir, "ANSWERS_%s.json" % a.reader))
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
        with open(os.path.join(root, R5, "READER_COMMIT.txt"), encoding="ascii") as fh:
            want_commit = fh.read().strip()
        with open(os.path.join(root, R5, "LOCATIONS.sha256"), encoding="ascii") as fh:
            want = fh.read().strip()
        same = hashlib.sha256(raw).hexdigest() == want
        print("  WORKTREE %s: inside=%s tracked=%s commits=%d head==cut=%s on disk=%s sha256 equals the cut: %s"
              % (a.dir, inside, tracked, len(log), head == want_commit, ondisk, same))
        res.append(("R3 the index is LOCATIONS.json alone, the history is the issuer's one commit, the files on disk are "
                    "LOCATIONS.json and ANSWERS_%s.json, the list is the cut byte for byte" % a.reader,
                    inside == "true" and tracked == ["LOCATIONS.json"] and log == [want_commit] and head == want_commit
                    and ondisk == sorted(["LOCATIONS.json", "ANSWERS_%s.json" % a.reader]) and same))
        wl = _git(a.dir, "worktree", "list", "--porcelain")
        print("  git worktree list (first lines): %s" % " | ".join(wl.split("\n")[:3]))
        res.append(("R4 the listing the CVO reads before grading was printed", bool(wl)))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.dir, type(e).__name__))
        res = [("ANSWERS_%s.json and LOCATIONS.json present" % a.reader, False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 5 READER %s: %d of 4 arms" % (a.reader, n))
    return 0 if n == 4 else 1


def agree(a):
    root = _root(a.root)
    key = _load(os.path.join(root, R5, "READING_KEY.json"))
    locs = {e["id"]: e["location"] for e in _load(os.path.join(a.dir_a, "LOCATIONS.json"))["locations"]}
    da, db = _load(os.path.join(a.dir_a, "ANSWERS_A.json")), _load(os.path.join(a.dir_b, "ANSWERS_B.json"))
    ra, rb = {x["id"]: x for x in da["answers"]}, {x["id"]: x for x in db["answers"]}
    print("readers: A=%s B=%s; locations=%d; key=%d" % (da.get("reader"), db.get("reader"), len(locs), len(key)))
    for arm in ("disagreed", "control"):
        ids = sorted(i for i, v in key.items() if v["arm"] == arm)
        line = ["ARM %-9s n=%d" % (arm, len(ids))]
        for f in FIELDS:
            ag = sum(1 for i in ids if _norm(ra[i][f]) == _norm(rb[i][f]) != "unknown")
            line.append("%s agree %d of %d" % (f, ag, len(ids)))
        allf = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) != "unknown" for f in FIELDS))
        right = sum(1 for i in ids if all(_norm(ra[i][f]) == _norm(rb[i][f]) == _norm(key[i]["truth"][f]) for f in FIELDS))
        line.append("all four agree %d of %d" % (allf, len(ids)))
        line.append("both equal the key on all four %d of %d" % (right, len(ids)))
        print(" | ".join(line))
        for i in ids:
            if not all(_norm(ra[i][f]) == _norm(rb[i][f]) == _norm(key[i]["truth"][f]) for f in FIELDS):
                print("  NOT-EQUAL %s class=%s key.table=%s A.table=%s B.table=%s" % (
                    i, key[i]["class"], key[i]["truth"]["table"], ra[i]["table"], rb[i]["table"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--dir-a", required=True)
    b.add_argument("--dir-b", required=True)
    b.add_argument("--root")
    r = sub.add_parser("reader")
    r.add_argument("--reader", choices=("A", "B"), required=True)
    r.add_argument("--dir", required=True)
    r.add_argument("--root")
    g = sub.add_parser("agree")
    g.add_argument("--dir-a", required=True)
    g.add_argument("--dir-b", required=True)
    g.add_argument("--root")
    a = ap.parse_args()
    return {"build": build, "reader": reader, "agree": agree}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
