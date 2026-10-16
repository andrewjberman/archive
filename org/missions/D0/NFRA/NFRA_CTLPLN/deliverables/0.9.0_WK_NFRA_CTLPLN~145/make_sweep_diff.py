#!/usr/bin/env python3
"""make_sweep_diff.py -- builds the unified diff that naming-gate.py grades in the CT-ca-1 sweep (CTO ruling 4).

Worker 0.9.0_WK_NFRA_CTLPLN~145. Standard library only, ASCII only, read-only (writes only the --out file).

  --rev base  the SET: every committed file at BASE (BASE.txt) that names the Lambda source map (git grep -l -F), restricted to
              the extensions naming-gate grades (.py .js .mjs .ts .tf .json .yaml .yml). Writes the set to SWEEP_SET.txt and
              a diff in which EVERY file is an added file with its base content (`--- /dev/null`).
  --rev work  the same SET, read from the WORKING TREE (a file no longer present counts as ABSENT and adds no lines), plus
              every file of the function-map folder (`infra/aws/lambda/ci/function-map/*.json`) if that folder exists.

naming-gate.py grades ADDED lines only, so this diff is the citation set graded as new content. Usage:
  python make_sweep_diff.py --rev base --out <diff>
  python make_sweep_diff.py --rev work --out <diff>
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE, capture_output=True).stdout.decode("utf-8").strip()
NEEDLE = "lambda-source-map"
GRADED = (".py", ".js", ".mjs", ".ts", ".tf", ".json", ".yaml", ".yml")
FOLDER_REL = "infra/aws/lambda/ci/function-map"


def base_commit():
    with open(os.path.join(HERE, "BASE.txt"), encoding="ascii") as f:
        return f.read().split()[0]


ORDER_REL = "org/missions/D0/NFRA/NFRA_CTLPLN/task-orders/NFRA_CTLPLN.TO-CT-ca-1.lambda-source-map-atomic-split.md"


def set_at_base():
    """The whole-repository SET (every committed file naming the map, graded types). A full-repository naming-gate run over
    this set did not finish inside the cell's bound (1.73 million added lines); see set_atomic() for the set that was graded."""
    r = subprocess.run(["git", "grep", "-l", "-F", "-e", NEEDLE, base_commit(), "--"], cwd=ROOT, capture_output=True)
    if r.returncode not in (0, 1):
        raise SystemExit("ERROR: git grep rc=%d" % r.returncode)
    names = []
    for ln in r.stdout.decode("utf-8", "replace").splitlines():
        prefix = base_commit() + ":"
        if ln.startswith(prefix):
            names.append(ln[len(prefix):])
    return sorted(p for p in names if p.lower().endswith(GRADED))


def set_atomic():
    """The cell's own citations at base: every GRADED file under the order's <paths> (the atomic set this cell changes), plus
    the CHANGELOG records of the Terraform roots (the changelog limb reads the function set). Read from the order file."""
    with open(os.path.join(ROOT, ORDER_REL), encoding="utf-8") as f:
        text = f.read()
    body = text.split("<paths>", 1)[1].split("</paths>", 1)[0]
    entries = [ln.strip() for ln in body.splitlines() if ln.strip()]
    tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", base_commit()], cwd=ROOT, capture_output=True)
    if tree.returncode != 0:
        raise SystemExit("ERROR: git ls-tree rc=%d" % tree.returncode)
    tracked = tree.stdout.decode("utf-8", "replace").splitlines()
    out = set()
    for e in entries:
        if e.endswith("/"):
            hit = [p for p in tracked if p.startswith(e)]
        else:
            hit = [p for p in tracked if p == e]
        out.update(p for p in hit if p.lower().endswith(GRADED))
    out.update(p for p in tracked if p.startswith("infra/aws/terraform/") and p.endswith("/CHANGELOG.json"))
    return sorted(out)


def read_base(path):
    r = subprocess.run(["git", "show", "%s:%s" % (base_commit(), path)], cwd=ROOT, capture_output=True)
    if r.returncode != 0:
        raise SystemExit("ERROR: git show base:%s rc=%d" % (path, r.returncode))
    return r.stdout


def section(path, data):
    text = data.decode("utf-8", "replace")
    lines = text.splitlines()
    out = ["diff --git a/%s b/%s" % (path, path), "new file mode 100644", "--- /dev/null", "+++ b/%s" % path]
    if not lines:
        return out, 0
    out.append("@@ -0,0 +1,%d @@" % len(lines))
    out.extend("+" + ln for ln in lines)
    return out, len(lines)


def main(argv):
    if "--rev" not in argv or "--out" not in argv:
        print("usage: make_sweep_diff.py --rev base|work --out <diff>")
        return 2
    rev = argv[argv.index("--rev") + 1]
    out_path = argv[argv.index("--out") + 1]
    atomic = "--set" in argv and argv[argv.index("--set") + 1] == "atomic"
    names = set_atomic() if atomic else set_at_base()
    if "--chunk" in argv:
        # --chunk i/K: the i-th of K contiguous slices of the SET (sorted), so one gate run stays under its bound
        i_s, k_s = argv[argv.index("--chunk") + 1].split("/")
        i, k = int(i_s), int(k_s)
        n = len(names)
        names = names[(i * n) // k:((i + 1) * n) // k]
        print("CHUNK %d/%d files=%d of %d" % (i, k, len(names), n))
    if rev == "base":
        if "--chunk" not in argv:
            setname = "SWEEP_SET_atomic.txt" if atomic else "SWEEP_SET_repo.txt"
            with open(os.path.join(HERE, setname), "w", encoding="ascii", newline="\n") as f:
                f.write("\n".join(names) + "\n")
        sources = [(p, read_base(p), "base") for p in names]
    elif rev == "work":
        sources = []
        absent = 0
        retired = {"org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rtf_1.py"}  # git rm'd by the cell
        sparse_base = 0
        for p in names:
            full = os.path.join(ROOT, p)
            if os.path.isfile(full):
                with open(full, "rb") as f:
                    sources.append((p, f.read(), "work"))
            elif p not in retired and subprocess.run(["git", "cat-file", "-e", "%s:%s" % (base_commit(), p)],
                                                     cwd=ROOT, capture_output=True).returncode == 0:
                # not held by this sparse worktree, outside the cell's <paths>: graded at its base bytes, which the cell does not change
                sources.append((p, read_base(p), "base-unchanged"))
                sparse_base += 1
            else:
                absent += 1
        print("WORK sparse-held-at-base=%d (graded at base bytes)" % sparse_base)
        fdir = os.path.join(ROOT, FOLDER_REL)
        extra = 0
        if os.path.isdir(fdir):
            for fn in sorted(os.listdir(fdir)):
                if fn.lower().endswith(".json"):
                    rel = FOLDER_REL + "/" + fn
                    with open(os.path.join(fdir, fn), "rb") as f:
                        sources.append((rel, f.read(), "work"))
                    extra += 1
        print("WORK set=%d absent=%d function_map_files=%d" % (len(names), absent, extra))
    else:
        print("ERROR: --rev must be base or work")
        return 2
    lines = []
    added_total = 0
    for p, data, _src in sources:
        sec, n = section(p, data)
        lines.extend(sec)
        added_total += n
    with open(out_path, "w", encoding="ascii", errors="replace", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print("DIFF rev=%s files=%d added_lines=%d out=%s" % (rev, len(sources), added_total, os.path.basename(out_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
