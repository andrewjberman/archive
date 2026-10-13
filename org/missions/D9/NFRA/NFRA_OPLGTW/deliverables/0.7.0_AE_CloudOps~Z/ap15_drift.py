#!/usr/bin/env python
"""OG-ap-15: re-measure each family's package-vs-source drift, both ways FD2_DRIFT measured it.

Two pins, because the two numbers answer different questions and only one of them is the
order's table:

  PRE_FD1 (12a92ffa49^, the commit before OG-fd-1 landed in source)
      -> drift that predates the drain work entirely. This reproduces the order's table and
         FD2_DRIFT's drift_lines_without_drain_code: etf 19, orion 282, eclipse 398,
         blackdiamond 298 (207 compared + 91 for the file the package never received).
  PRE_FD2 (4c7e933975, the tree before the OG-fd-2 source change)
      -> the same drift PLUS the fd-1 drain code, i.e. FD2_DRIFT's drift_lines:
         etf 101, orion 359, eclipse 475, blackdiamond 375.

A vendored module the package never received cannot be diffed, so its SOURCE line count is
reported separately and added into drift_lines -- FD2_DRIFT's convention. Counting it is the
conservative direction: vendor-manifest.sh copies every manifest entry unconditionally, so a
rebuild ships that whole file.

Usage: python ap15_drift.py <pkg_commit>
"""
from __future__ import annotations

import difflib
import json
import os
import subprocess
import sys

FAMILIES = ["schwab", "etf", "orion", "eclipse", "blackdiamond"]
PRE_FD1 = "12a92ffa49^"
PRE_FD2 = "4c7e933975"


def git_bytes(ref_path: str) -> bytes | None:
    r = subprocess.run(["git", "show", ref_path], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def norm(b: bytes) -> list[str]:
    return b.replace(b"\r\n", b"\n").decode("utf-8", "replace").split("\n")


def diff_lines(src: bytes, pkg: bytes) -> int:
    return len([x for x in difflib.unified_diff(norm(src), norm(pkg), n=0)
                if (x.startswith("+") or x.startswith("-")) and not x.startswith(("+++", "---"))])


def measure(fam: str, pkg_commit: str, pin: str) -> dict:
    pkg = "infra/aws/lambda/opal-assets/opal-assets-silver-%s" % fam
    man = git_bytes("%s:%s/BUILD_MANIFEST.json" % (pkg_commit, pkg))
    if man is None:
        return {"error": "manifest unreadable at %s" % pkg_commit}
    mods = json.loads(man.decode("utf-8"))["vendored_modules"]
    compared, files, missing = 0, [], []
    for rel in mods:
        base = os.path.basename(rel)
        p = git_bytes("%s:%s/%s" % (pkg_commit, pkg, base))
        s = git_bytes("%s:%s" % (pin, rel))
        if s is None:
            missing.append({"file": base, "source": rel, "why": "no source at pin", "source_lines": None})
            continue
        if p is None:
            # Never vendored. A rebuild ships the whole file, so its source length IS the drift.
            # FD2_DRIFT's own count is the length of the newline-split list, which includes the
            # artifact (opal_strategy_matcher.py reads 91 there, 90 by wc -l). Matched so this
            # number equals the order's table rather than being 18 short of it.
            n = len(norm(s))
            missing.append({"file": base, "source": rel, "why": "MISSING_IN_PACKAGE", "source_lines": n})
            continue
        d = diff_lines(s, p)
        if d:
            compared += d
            files.append({"file": base, "source": rel, "drift_lines": d})
    missing_lines = sum(m["source_lines"] or 0 for m in missing)
    return {"modules": len(mods), "drift_lines": compared + missing_lines,
            "drift_lines_compared": compared, "drift_lines_missing_in_package": missing_lines,
            "files_differing": files, "not_compared": missing}


def main() -> int:
    pkg_commit = sys.argv[1]
    out = {"pkg_commit": pkg_commit, "pins": {"pre_fd1": PRE_FD1, "pre_fd2": PRE_FD2},
           "method": "package copy vs source at pin, CRLF-normalised, added+removed; a module missing from the package contributes its source line count",
           "order_table_convention": "pre_fd1", "families": []}
    for fam in FAMILIES:
        out["families"].append({"family": fam,
                                "pre_fd1": measure(fam, pkg_commit, PRE_FD1),
                                "pre_fd2": measure(fam, pkg_commit, PRE_FD2)})
    with open("ap15_drift_measured.json", "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print("%-13s %-28s %s" % ("family", "drift_lines (pre_fd1, ORDER)", "drift_lines (pre_fd2)"))
    for f in out["families"]:
        a, b = f["pre_fd1"], f["pre_fd2"]
        print("%-13s %-28s %s" % (f["family"],
              "%s (%s cmp + %s missing)" % (a["drift_lines"], a["drift_lines_compared"], a["drift_lines_missing_in_package"]),
              b["drift_lines"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
