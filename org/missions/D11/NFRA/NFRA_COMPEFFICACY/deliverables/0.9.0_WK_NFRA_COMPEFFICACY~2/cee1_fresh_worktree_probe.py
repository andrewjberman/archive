"""CE-e-1 / E1-AC2 -- THE STANDALONE FRESH-WORKTREE PROBE.

THE ONE FACT THIS CELL EXISTS TO CHANGE: a hash-pinned vendored model asset must render the SAME
BYTES in a FRESH LINKED WORKTREE as the MANIFEST declares. Before CE-e-1 it did not: on a box with
core.autocrlf=true and no eol attribute, `git worktree add` renders org/modules/graph/potion/model/
tokenizer.json CRLF (713,343 B) while org/modules/graph/potion/MANIFEST.json declares the LF bytes
(683,666 B), potion_embed.py:57-63 raises FAIL-CLOSED, and comp-which ranks LEXICALLY in every
worker slot with one stderr ALARM line as the only tell.

DELIBERATELY SELF-CONTAINED -- it imports nothing from the battery beside it and nothing from any
shared carrier. The CVO can re-run THIS ONE FACT without running everything, and a shared helper
underneath the two scripts would be exactly the shared dependency a per-member check cannot see.

IT CARRIES ITS OWN CLEANUP: the worktree and its branch are removed in a `finally`, on every exit
path (match, mismatch, exception, --help), and the removal is VERIFIED by re-reading
`git worktree list --porcelain` rather than trusted from the remove command's rc.

THE REF IT CUTS, and why it is not the literal string CLOUD (row NFRA_COMPEFFICACY-W2-S1):
the task order's bound says `git worktree add -b <b> /c/tmp/<slot> CLOUD`. At the time this cell
was worked the fix lived on the WORKER BRANCH and CLOUD was the PRE-FIX ref -- the issuer drains
worker branches, so a literal CLOUD cut measures the tree the fix has not reached yet. The default
here is THE BRANCH OF THE INVOKING WORKTREE, which IS `CLOUD` when the CVO re-runs this from the
main tree after the drain, and is the worker branch when the worker runs it before. `--ref` forces
any ref. The resolved ref, its sha, and whether it carries the .gitattributes entry are all PRINTED,
so the reading always says which tree it was taken in (ruling R-8).

  python cee1_fresh_worktree_probe.py                 # cut the invoking worktree's own branch
  python cee1_fresh_worktree_probe.py --ref CLOUD     # cut a named ref
  python cee1_fresh_worktree_probe.py --keep          # leave the worktree behind (debug only)

TOKEN: FRESH-WORKTREE-ASSET-MATCHES-MANIFEST -- printed ONLY on a total match, with its denominator.
rc 0 on the token, rc 1 on any mismatch or any failure to take the reading.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# deliverables/<serial>/ -> deliverables -> NFRA_COMPEFFICACY -> NFRA -> D11 -> missions -> org -> ROOT
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))

MODEL_DIR_REL = "org/modules/graph/potion/model"
MANIFEST_REL = "org/modules/graph/potion/MANIFEST.json"
ATTR_PATTERN = "org/modules/graph/potion/model/**"
TOKEN = "FRESH-WORKTREE-ASSET-MATCHES-MANIFEST"


def run(argv, cwd, timeout=600):
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def git(args, cwd=None, timeout=600):
    return run(["git"] + list(args), cwd or WS, timeout)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tracked_model_files(tree):
    rc, out, err = git(["ls-files", "-z", "--", MODEL_DIR_REL], cwd=tree)
    if rc != 0:
        return None, "git ls-files rc=%d: %s" % (rc, err.strip())
    names = [p for p in out.split("\0") if p.strip()]
    return sorted(names), ""


def present_on_disk(tree):
    d = os.path.join(tree, *MODEL_DIR_REL.split("/"))
    if not os.path.isdir(d):
        return []
    return sorted(n for n in os.listdir(d) if os.path.isfile(os.path.join(d, n)))


def worktree_paths(tree):
    rc, out, _ = git(["worktree", "list", "--porcelain"], cwd=tree)
    if rc != 0:
        return None
    return [ln.split(" ", 1)[1].strip().replace("\\", "/")
            for ln in out.splitlines() if ln.startswith("worktree ")]


def main(argv):
    args = list(argv)
    keep = "--keep" in args
    ref = ""
    if "--ref" in args:
        ref = args[args.index("--ref") + 1]

    t_start = time.time()
    print("CE-e-1 / E1-AC2 -- FRESH-WORKTREE PROBE of the vendored POTION model asset")
    print("  invoked from : %s" % HERE.replace("\\", "/"))
    print("  repo root    : %s" % WS.replace("\\", "/"))

    if not ref:
        rc, out, _ = git(["rev-parse", "--abbrev-ref", "HEAD"])
        ref = out.strip()
        if rc != 0 or not ref or ref == "HEAD":
            rc, out, _ = git(["rev-parse", "HEAD"])
            ref = out.strip()
        print("  ref          : %s  (DEFAULT = the invoking worktree's own branch; --ref overrides)" % ref)
    else:
        print("  ref          : %s  (--ref)" % ref)

    rc, out, err = git(["rev-parse", ref + "^{commit}"])
    if rc != 0:
        print("BLOCKED: ref %s does not resolve: %s" % (ref, err.strip()))
        return 1
    ref_sha = out.strip()
    print("  ref sha      : %s" % ref_sha)

    rc, out, _ = git(["show", "%s:.gitattributes" % ref_sha])
    carries = (rc == 0 and ATTR_PATTERN in out)
    print("  ref carries `%s` in .gitattributes : %s" % (ATTR_PATTERN, "YES" if carries else "NO"))

    rc, out, _ = git(["config", "core.autocrlf"])
    print("  core.autocrlf: %s" % (out.strip() or "(unset)"))

    slot = "C:/tmp/cee1-probe-%d-%d" % (os.getpid(), int(t_start))
    branch = "cee1-probe-%d-%d" % (os.getpid(), int(t_start))
    made = False
    verdict = 1
    try:
        print("")
        print("CUT: git worktree add -b %s %s %s" % (branch, slot, ref_sha))
        t0 = time.time()
        rc, out, err = git(["worktree", "add", "-b", branch, slot, ref_sha], timeout=600)
        print("  rc=%d  %.1fs  -> %s" % (rc, time.time() - t0, slot))
        if rc != 0:
            print("BLOCKED: worktree add failed: %s" % err.strip()[-400:])
            return 1
        made = True

        tracked, msg = tracked_model_files(slot)
        if tracked is None:
            print("BLOCKED: %s" % msg)
            return 1
        disk = present_on_disk(slot)
        print("")
        print("CENSUS in the FRESH tree %s" % slot)
        print("  tracked under %s/ : %d" % (MODEL_DIR_REL, len(tracked)))
        print("  present on disk under %s/ : %d  (%s)" % (MODEL_DIR_REL, len(disk), ", ".join(disk)))

        mpath = os.path.join(slot, *MANIFEST_REL.split("/"))
        if not os.path.isfile(mpath):
            print("BLOCKED: no manifest at %s" % mpath.replace("\\", "/"))
            return 1
        man = json.load(open(mpath, encoding="utf-8"))
        declared = man.get("model_files_sha256") or {}
        declared_b = man.get("model_files_bytes") or {}
        print("  manifest     : %s" % mpath.replace("\\", "/"))
        print("  manifest declares %d model_files_sha256 entr(ies)" % len(declared))

        rc, out, _ = git(["ls-files", "--eol", "--", MODEL_DIR_REL], cwd=slot)
        for ln in out.splitlines():
            print("  ls-files --eol: %s" % ln.strip())

        print("")
        print("COMPARE: fresh-tree bytes vs the manifest the loader reads, %d of %d tracked file(s)"
              % (len(tracked), len(tracked)))
        matched = 0
        unchecked = []
        for rel in tracked:
            base = rel.rsplit("/", 1)[-1]
            p = os.path.join(slot, *rel.split("/"))
            if not os.path.isfile(p):
                print("  [MISS] %-20s tracked but ABSENT on disk at %s" % (base, p.replace("\\", "/")))
                continue
            got = sha256_of(p)
            nbytes = os.path.getsize(p)
            want = declared.get(base)
            want_b = declared_b.get(base)
            if want is None:
                unchecked.append(base)
                print("  [NO-PIN] %-18s sha256 %s  %d B  -- the manifest declares no hash for this "
                      "member" % (base, got, nbytes))
                continue
            ok = (got == want) and (want_b is None or nbytes == want_b)
            matched += 1 if ok else 0
            print("  [%s] %-20s fresh sha256 %s  %d B" % ("MATCH" if ok else "DIFFER", base, got, nbytes))
            print("          %-20s manifest     %s  %s B" % ("", want, want_b))

        pinned = len(tracked) - len(unchecked)
        print("")
        print("RESULT: %d of %d tracked file(s) MATCH the manifest "
              "(%d pinned by the manifest, %d tracked-but-unpinned: %s)"
              % (matched, pinned, pinned, len(unchecked), ", ".join(unchecked) or "none"))
        if unchecked:
            print("  NOTE: a tracked member the manifest does not pin is NOT evidence of a match -- it is "
                  "an unpinned member, and it is reported here rather than counted as one.")
        if matched == pinned and pinned == len(tracked) and pinned > 0:
            verdict = 0
        else:
            verdict = 1
    finally:
        if made and not keep:
            print("")
            print("CLEANUP")
            rc, _, err = git(["worktree", "remove", "--force", slot])
            print("  git worktree remove --force %s  -> rc=%d %s" % (slot, rc, err.strip()[:200]))
            rc2, _, err2 = git(["branch", "-D", branch])
            print("  git branch -D %s  -> rc=%d %s" % (branch, rc2, err2.strip()[:200]))
            git(["worktree", "prune"])
            paths = worktree_paths(WS) or []
            still = [p for p in paths if p.lower() == slot.lower()]
            print("  git worktree list --porcelain: %d worktree(s); this slot still listed: %s"
                  % (len(paths), "YES -- LEAK" if still else "NO"))
            if still:
                verdict = 1
            if os.path.exists(slot):
                print("  WARN: %s still exists on disk" % slot)
                verdict = 1
        elif made:
            print("")
            print("CLEANUP SKIPPED (--keep): %s and branch %s left behind" % (slot, branch))

    print("")
    print("  elapsed %.1fs" % (time.time() - t_start))
    if verdict == 0:
        print(TOKEN)
    else:
        print("NO TOKEN -- the fresh worktree's model bytes do not all match the manifest, or the "
              "reading could not be taken, or the worktree leaked.")
    return verdict


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
