"""The tree-equal FOLD of PROD into DEV after a promote (CTO standing rule msg 10617; CTO ruling msg 10781 for the 2026-10-19 promote), issuer 2.0.0_SA_COO~D2.

Cuts a DEV-based branch in a scratch worktree of the portal repo, merges <prod_ref> into it, resolves an add/add conflict only on a path named in --allow by taking <prod_ref>'s bytes (any other
unmerged path stops the run), commits with --msgfile, and prints the two reads the approval row needs:
  READ 1  git diff --name-only origin/DEV HEAD   -- must equal --allow exactly (the files PROD gained that DEV lacks), nothing else;
  READ 2  git diff --name-only <prod_ref> HEAD   -- the files the fold tree still differs from PROD in, split into those under --release-paths (must be 0) and the rest (DEV-ahead files).
It writes nothing outside the scratch worktree and pushes nothing. Usage:
  python -I fold_prod_into_dev.py --portal <portal repo> --wt <new scratch path> --branch <cand/...> --prod-ref <ref> --msgfile <file> --allow <path> [--allow <path> ...] --release-paths <file listing one path per line>
"""
import argparse
import subprocess
import sys

ENV_NAME = "dell2"


def git(wt, *a, check=True, text=True):
    r = subprocess.run(["git", "-C", wt] + list(a), capture_output=True)
    if check and r.returncode != 0:
        raise SystemExit("git %s failed rc=%d: %s" % (" ".join(a[:3]), r.returncode, r.stderr.decode("utf-8", "replace")[:300]))
    return r if not text else (r.returncode, r.stdout.decode("utf-8"))


def lines(s):
    return sorted(x for x in s.split(chr(10)) if x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portal", required=True)
    ap.add_argument("--wt", required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--prod-ref", required=True)
    ap.add_argument("--msgfile", required=True)
    ap.add_argument("--allow", action="append", required=True)
    ap.add_argument("--release-paths", required=True)
    a = ap.parse_args()
    git(a.portal, "worktree", "add", "-b", a.branch, a.wt, "origin/DEV")
    import os
    env = dict(os.environ, GIT_AUTHOR_NAME=ENV_NAME, GIT_AUTHOR_EMAIL=ENV_NAME + "@opal.agent", GIT_COMMITTER_NAME=ENV_NAME, GIT_COMMITTER_EMAIL=ENV_NAME + "@opal.agent")
    r = subprocess.run(["git", "-C", a.wt, "merge", "--no-commit", "--no-ff", a.prod_ref], capture_output=True, env=env)
    print("merge rc=%d" % r.returncode)
    _, unmerged = git(a.wt, "diff", "--name-only", "--diff-filter=U")
    um = lines(unmerged)
    bad = [p for p in um if p not in a.allow]
    if bad:
        raise SystemExit("STOP: unmerged paths outside --allow: %s" % bad)
    for p in um:
        blob = git(a.wt, "show", "%s:%s" % (a.prod_ref, p), text=False).stdout
        with open(a.wt + "/" + p, "wb") as fh:
            fh.write(blob)
        git(a.wt, "add", p)
    print("conflicts resolved with the PROD side's bytes: %d %s" % (len(um), um))
    r = subprocess.run(["git", "-C", a.wt, "commit", "-q", "-F", a.msgfile], capture_output=True, env=env)
    if r.returncode != 0:
        raise SystemExit("commit failed: " + r.stderr.decode("utf-8", "replace")[:300])
    head = git(a.wt, "rev-parse", "HEAD")[1].strip()
    _, d1 = git(a.wt, "diff", "--name-only", "origin/DEV", "HEAD")
    read1 = lines(d1)
    print("fold head", head)
    print("READ 1: files differing from origin/DEV: %d" % len(read1))
    for p in read1:
        print("   ", p)
    ok1 = read1 == sorted(a.allow)
    print("READ 1 equals the allowed set exactly: %s" % ok1)
    _, d2 = git(a.wt, "diff", "--name-only", a.prod_ref, "HEAD")
    release = set(lines(open(a.release_paths, encoding="utf-8").read()))
    read2 = lines(d2)
    under = [p for p in read2 if p in release]
    print("READ 2: files differing from %s: %d, under the release paths: %d, DEV-ahead elsewhere: %d" % (a.prod_ref, len(read2), len(under), len(read2) - len(under)))
    for p in under:
        print("   UNDER RELEASE PATH:", p)
    print("FOLD OK" if ok1 and not under else "FOLD NOT OK")
    sys.exit(0 if ok1 and not under else 1)


if __name__ == "__main__":
    main()
