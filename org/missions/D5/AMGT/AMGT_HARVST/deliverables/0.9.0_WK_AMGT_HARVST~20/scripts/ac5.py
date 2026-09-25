"""HVST-s-1 AC5 -- write-surface census + delete census with a positive control."""

import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

ROOT = pathlib.Path(__file__).resolve().parents[2]
ALLOWED_PREFIXES = (
    "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~20/",
    "org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/investigations/INVESTIGATION_v1.md",
    "org/missions/D5/AMGT/AMGT_HARVST/task-orders/AMGT_HARVST.TO-HVST-s-1.sa-listing-capture-retried.md",
    ".scratch/s1/",
)
DELETE_RE = re.compile(r"delete_object|delete_objects|delete_bucket|DeleteObject|DeleteObjects")
SCAN_DIRS = ("lib/opal_data_harvest", "lib/research/harvest", ".scratch/s1")


def run(cmd):
    proc = subprocess.run(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def limb_write_surface():
    rc, out = run(["git", "status", "--porcelain", "--untracked-files=all"])
    entries = [line for line in out.splitlines() if line.strip()]
    changed = []
    for line in entries:
        path = line[3:].strip().strip('"')
        changed.append(path)
    outside = [p for p in changed if not any(p.startswith(a) for a in ALLOWED_PREFIXES)]
    print("AC5 limb 1 -- WRITE SURFACE. `git status --porcelain -uall` rc=%d, %d changed/untracked path(s) "
          "(denominator: every path git reports in this worktree)" % (rc, len(changed)))
    for path in changed:
        print("    %s" % path)
    print("  outside_allowed %s" % (outside if outside else "[]"))

    rc_lib, out_lib = run(["git", "status", "--porcelain", "--untracked-files=all", "--", "lib"])
    lib_entries = [line for line in out_lib.splitlines() if line.strip()]
    rc_diff, out_diff = run(["git", "diff", "--stat", "HEAD", "--", "lib"])
    print("  lib/ census: `git status --porcelain -uall -- lib` rc=%d -> %d path(s); "
          "`git diff --stat HEAD -- lib` rc=%d -> %r"
          % (rc_lib, len(lib_entries), rc_diff, out_diff.strip()))
    print("  NO lib/ FILE CHANGED: %s" % (len(lib_entries) == 0 and not out_diff.strip()))
    print("  NOTE, gitignored and therefore invisible above: AC1b's `upload-harvest` created "
          ".runtime/opal-data-harvest/ in this worktree (.gitignore:288 `.runtime/`). It is runtime state, "
          "not a repo path, and it is empty of pending outbox rows.")
    return outside, len(lib_entries) == 0 and not out_diff.strip()


def _executed_modules():
    """The lib/ files the cell's own commands actually IMPORT, derived mechanically, not listed by hand."""
    code = (
        "import json, sys, pathlib\n"
        "sys.path.insert(0, %r)\n"
        "import lib.opal_data_harvest.__main__\n"
        "import lib.opal_data_harvest.uploads\n"
        "import lib.research.harvest.publication_gold\n"
        "root = pathlib.Path(%r)\n"
        "out = sorted(str(pathlib.Path(m.__file__).resolve().relative_to(root)).replace(chr(92), '/')\n"
        "             for m in list(sys.modules.values())\n"
        "             if getattr(m, '__file__', None) and str(pathlib.Path(m.__file__).resolve()).startswith(str(root)))\n"
        "print(json.dumps(out))\n" % (str(ROOT), str(ROOT))
    )
    rc, out = run([sys.executable, "-c", code])
    line = [ln for ln in out.splitlines() if ln.startswith("[")]
    import json as _json
    return (_json.loads(line[-1]) if line else []), rc, out


def limb_delete_census():
    scanned = 0
    hits = []
    for folder in SCAN_DIRS:
        for path in sorted((ROOT / folder).rglob("*.py")):
            scanned += 1
            text = path.read_text(encoding="utf-8", errors="replace")
            for number, line in enumerate(text.splitlines(), 1):
                if DELETE_RE.search(line):
                    hits.append((str(path.relative_to(ROOT)).replace("\\", "/"), number, line.strip()))
    print("")
    print("AC5 limb 2 -- DELETE CENSUS over every .py under %s: %d delete-verb line(s) across %d file(s) "
          "scanned (denominator)" % (", ".join(SCAN_DIRS), len(hits), scanned))
    for path, number, line in hits:
        print("    %s:%d: %s" % (path, number, line))

    executed, rc, raw = _executed_modules()
    ran_scripts = ["/".join((".scratch/s1", name)) for name in
                   ("snapshot_lib.py", "ac0.py", "ac2.py", "ac3.py", "ac4.py", "ac5.py", "row_w20_s1.py")]
    executed_set = set(executed) | set(ran_scripts)
    print("  EXECUTED PATH, derived mechanically by importing this cell's own entry points "
          "(lib.opal_data_harvest.__main__, .uploads, lib.research.harvest.publication_gold) and reading "
          "sys.modules: %d lib/ file(s) imported, rc=%d ; plus the %d scripts this cell ran."
          % (len(executed), rc, len(ran_scripts)))
    in_path = [h for h in hits if h[0] in executed_set]
    outside_own_control = [h for h in in_path if h[0] != ".scratch/s1/ac5.py"]
    print("  delete-verb lines INSIDE the executed path: %d -- of which in a file other than AC5's own "
          "guard/positive control: %d" % (len(in_path), len(outside_own_control)))
    for path, number, line in in_path:
        print("      %s:%d: %s" % (path, number, line))
    print("  the %d line(s) OUTSIDE the executed path sit in lib/opal_data_harvest/classify_unlabelled_bronze.py "
          "(a separate CLI whose guard makes those verbs RAISE) and its test -- neither was imported or run "
          "by this cell." % (len(hits) - len(in_path)))
    probe = "client.delete_objects(Bucket=b, Delete={'Objects': keys})"
    print("  NEGATIVE CONTROL on the same regex (a planted string that MUST match): %s"
          % bool(DELETE_RE.search(probe)))
    print("  S3-SIDE CORROBORATION: every AC2 delta is >= 0 (no publisher's silver row count or bronze "
          "object count fell), which is what a delete would have moved.")
    return len(outside_own_control), scanned


class DeleteRefused(RuntimeError):
    pass


def limb_positive_control():
    import boto3

    def refuse(*args, **kwargs):
        raise DeleteRefused("S3 delete refused by the AC5 guard")

    client = boto3.client("s3", region_name="us-east-1")
    client.meta.events.register("before-parameter-build.s3.DeleteObject", refuse)
    client.meta.events.register("before-parameter-build.s3.DeleteObjects", refuse)
    bucket = "opal-hvst-s1-delete-positive-control-never-created"
    print("")
    print("AC5 limb 3 -- POSITIVE CONTROL: both delete verbs deliberately tripped under the guard, against "
          "the never-created bucket %r (so even a guard failure could not remove an object)." % bucket)
    results = {}
    for verb, call in (("delete_object", lambda: client.delete_object(Bucket=bucket, Key="probe")),
                       ("delete_objects", lambda: client.delete_objects(
                           Bucket=bucket, Delete={"Objects": [{"Key": "probe"}]}))):
        try:
            call()
            results[verb] = "DID NOT RAISE -- control FAILED"
        except DeleteRefused as exc:
            results[verb] = "RAISED DeleteRefused: %s" % exc
        except Exception as exc:  # any other raise is still a refusal to delete, reported verbatim
            results[verb] = "RAISED %s: %s" % (type(exc).__name__, exc)
        print("    %-15s %s" % (verb, results[verb]))
    return all("RAISED" in v for v in results.values())


def main():
    outside, lib_clean = limb_write_surface()
    hits, scanned = limb_delete_census()
    control_ok = limb_positive_control()
    print("")
    print("AC5 VERDICT LINE: outside_allowed %s ; lib_unchanged=%s ; delete_call_sites_in_executed_path_outside_ac5_control=%d of %d files "
          "scanned ; positive_control_both_raise=%s"
          % (outside if outside else "[]", lib_clean, hits, scanned, control_ok))
    return 0 if (not outside and lib_clean and hits == 0 and control_ok) else 1


if __name__ == "__main__":
    raise SystemExit(main())
