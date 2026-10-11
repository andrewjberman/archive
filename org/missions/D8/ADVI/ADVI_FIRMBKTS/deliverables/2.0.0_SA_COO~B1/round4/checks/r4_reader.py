"""ADVI_FIRMBKTS round 4 check for cells FB-g-4 and FB-g-5 (the two blind readers), issuer 2.0.0_SA_COO~B1.

--reader A|B --dir <the reader's worktree> grades ANSWERS_<reader>.json against LOCATIONS.json in that worktree (4 arms).
Agreement between the readers is NOT graded here: it is the issuer's real run (r4_agree.py).
Arm R3 is the independence-by-construction arm (CTO, ROUND_ANALYSIS.round3.md section 3 item 3): the directory is a git
worktree whose index holds ONLY LOCATIONS.json, whose history is the one parentless commit the issuer cut, whose files on
disk are LOCATIONS.json and the reader's one answers file, and whose list is the issuer's cut byte for byte (sha256).
Arm R4 prints the listing the CVO reads before grading. Never edit this file.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
R4 = DELIV + "/2.0.0_SA_COO~B1/round4"
FIELDS = ("system", "firm", "tier", "table", "contents")


def _git(d, *a):
    r = subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reader", choices=("A", "B"), required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = a.root or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    res = []
    try:
        with open(os.path.join(a.dir, "LOCATIONS.json"), "rb") as fh:
            raw = fh.read()
        ids = [e["id"] for e in json.loads(raw.decode("ascii"))["locations"]]
        with open(os.path.join(a.dir, "ANSWERS_%s.json" % a.reader), encoding="utf-8") as fh:
            doc = json.load(fh)
        answers = doc.get("answers") or []
        got = [x.get("id") for x in answers]
        dup = len(got) - len(set(got))
        missing = set(ids) - set(got)
        extra = set(got) - set(ids)
        print("  locations=%d answers=%d duplicates=%d unanswered=%d unknown ids=%d"
              % (len(ids), len(answers), dup, len(missing), len(extra)))
        res.append(("R1 every location id is answered exactly once, by a named worker serial",
                    bool(ids) and not dup and not missing and not extra
                    and str(doc.get("reader", "")).startswith("0.9.0_WK_")))
        blank = [x.get("id") for x in answers
                 if not all(isinstance(x.get(f), str) and x.get(f).strip() for f in FIELDS)]
        print("  answers with a blank field: %d" % len(blank))
        res.append(("R2 every answer names system, firm, tier, table and contents (a field may read 'unknown')",
                    not blank and bool(answers)))
        ondisk = sorted(n for n in os.listdir(a.dir) if n != ".git")
        rc1, inside = _git(a.dir, "rev-parse", "--is-inside-work-tree")
        rc2, tracked = _git(a.dir, "ls-files")
        rc3, log = _git(a.dir, "log", "--format=%H")
        rc4, head = _git(a.dir, "rev-parse", "HEAD")
        with open(os.path.join(root, R4, "READER_COMMIT.txt"), encoding="ascii") as fh:
            want_commit = fh.read().strip()
        with open(os.path.join(root, R4, "LOCATIONS.sha256"), encoding="ascii") as fh:
            want = fh.read().strip()
        same = hashlib.sha256(raw).hexdigest() == want
        print("  WORKTREE %s: inside=%s tracked=%s commits=%d head==cut=%s on disk=%s sha256 equals the cut: %s"
              % (a.dir, inside, tracked.split(), len(log.split()), head == want_commit, ondisk, same))
        res.append(("R3 the worktree's index is LOCATIONS.json alone, its history is the issuer's one commit, its files "
                    "on disk are LOCATIONS.json and ANSWERS_%s.json, and the list is the cut byte for byte" % a.reader,
                    inside == "true" and tracked.split() == ["LOCATIONS.json"] and log.split() == [want_commit]
                    and head == want_commit and ondisk == sorted(["LOCATIONS.json", "ANSWERS_%s.json" % a.reader])
                    and same))
        rc5, wl = _git(a.dir, "worktree", "list", "--porcelain")
        print("  git worktree list (first lines): %s" % " | ".join(wl.split("\n")[:3]))
        res.append(("R4 the listing the CVO reads before grading was printed (worktree list, index, history, disk)",
                    rc1 == rc2 == rc3 == rc4 == rc5 == 0))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: %s (%s)" % (a.dir, type(e).__name__))
        res = [("ANSWERS_%s.json and LOCATIONS.json present" % a.reader, False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 READER %s: %d of 4 arms" % (a.reader, n))
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
