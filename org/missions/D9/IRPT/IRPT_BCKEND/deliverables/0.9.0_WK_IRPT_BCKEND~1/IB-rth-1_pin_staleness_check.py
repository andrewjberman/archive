#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rth-1 -- pin-staleness probe (row IRPT_BCKEND-W1-S48).

MEASUREMENT-ONLY, no AWS call, no build, no apply. Confirms, offline, that
`infra/aws/lambda/ci/build-and-upload.sh`'s `staged_from` mechanism for
`_authz/loaders.py` -- shared into all 7 serving functions -- currently
resolves to a commit that PREDATES this cell's signed fix, so a rebuild
right now would silently redeploy pre-fix behaviour under a post-fix label.
See row IRPT_BCKEND-W1-S48 (surprise-channel/investigations/INVESTIGATION_v1.md)
for the full grounding this script's output backs.

NEVER PRINTED OR WRITTEN: nothing secret; no AWS call of any kind.
ASCII only. Python 3.12.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rth-1_pin_staleness_check_output.txt")
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
LOADERS_REL = "infra/aws/lambda/investor-reporting/_authz/loaders.py"
FIX_COMMIT = "385aff464618e54a3ff461793222bd44154d2499"
FIX_LOADERS_SHA256 = "0c086052e6e65d2cb411f15362862b1656bad0b2320f9756be6a32444b665765"
TO_REL = ("org/missions/D9/IRPT/IRPT_BCKEND/task-orders/"
          "IRPT_BCKEND.TO-IB-rth-1.the-inflection-serving-route-rectified-within-andrews-terms.md")
TARGETS = ["irpt-directory-search", "irpt-status", "irpt-holdings", "irpt-narrative",
           "irpt-export-render", "irpt-performance-adapter", "irpt-ycharts-generate"]
TOKEN = "IB-RTH-1-PIN-STALE-BUILD-BLOCKED-OUT-OF-GRANT"

LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode("ascii"), flush=True)


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120)
    return out.returncode, out.stdout


def main() -> int:
    emit("IB-rth-1 pin-staleness probe -- worktree HEAD %s" % git("rev-parse", "HEAD")[1].strip())
    emit("")

    with open(os.path.join(WS, SOURCE_MAP_REL), encoding="utf-8") as fh:
        sm = json.load(fh)
    pins = {}
    for fn in TARGETS:
        for s in sm["functions"][fn].get("staged_from", []):
            if s["repo_path"].endswith("_authz/loaders.py"):
                pins[fn] = s["pin"]
    uniq = set(pins.values())
    emit("(1) loaders.py staged_from pin, per target function:")
    for fn in TARGETS:
        emit("  %-28s pin=%s" % (fn, pins.get(fn)))
    one_pin = len(uniq) == 1
    emit("  distinct pins across 7 of 7 target functions: %d -> %s" % (len(uniq), "ONE SHARED PIN" if one_pin else "DIFFERS"))
    pin = next(iter(uniq)) if one_pin else None

    emit("")
    rc_anc, _ = git("merge-base", "--is-ancestor", pin, FIX_COMMIT) if pin else (2, "")
    is_ancestor = rc_anc == 0
    emit("(2) git merge-base --is-ancestor %s %s -> rc=%d -> %s"
         % (pin, FIX_COMMIT, rc_anc, "PIN PREDATES THE FIX (ancestor)" if is_ancestor else "NOT an ancestor"))

    _, range_log = git("log", "--oneline", "%s..%s" % (pin, FIX_COMMIT), "--", LOADERS_REL) if pin else (2, "")
    range_commits = [ln for ln in range_log.splitlines() if ln.strip()]
    emit("(3) git log --oneline %s..%s -- %s:" % (pin, FIX_COMMIT, LOADERS_REL))
    for ln in range_commits:
        emit("  %s" % ln)
    emit("  commits in range: %d" % len(range_commits))

    _, pinned_text = git("show", "%s:%s" % (pin, LOADERS_REL)) if pin else (2, "")
    pinned_sha = hashlib.sha256(pinned_text.encode("utf-8")).hexdigest()
    _, head_text = git("show", "HEAD:%s" % LOADERS_REL)
    head_sha = hashlib.sha256(head_text.encode("utf-8")).hexdigest()
    emit("")
    emit("(4) content at the pin vs content at HEAD:")
    emit("  pin  %s: %d bytes, sha256 %s" % (pin, len(pinned_text.encode("utf-8")), pinned_sha))
    emit("  HEAD %s: %d bytes, sha256 %s (expected fix: %s)"
         % (git("rev-parse", "HEAD")[1].strip(), len(head_text.encode("utf-8")), head_sha, FIX_LOADERS_SHA256))
    content_differs = pinned_sha != head_sha
    head_is_fix = head_sha == FIX_LOADERS_SHA256
    emit("  pin content != HEAD content: %s; HEAD content == the signed fix: %s" % (content_differs, head_is_fix))

    _, fix_paths = git("show", "--name-only", "--format=", FIX_COMMIT)
    touches_source_map = SOURCE_MAP_REL in fix_paths.splitlines()
    emit("")
    emit("(5) does the fix commit (%s) itself update %s: %s"
         % (FIX_COMMIT, SOURCE_MAP_REL, touches_source_map))

    to_text = open(os.path.join(WS, TO_REL), encoding="utf-8").read()
    import re
    # anchored to the TAG STANDING ALONE ON ITS OWN LINE -- the face also uses the literal
    # substring "<paths>" inline, in backticks, inside prose (the preflight's lane note), which
    # a bare r"<paths>(.*?)</paths>" would match FIRST and then run to the real closing tag,
    # swallowing everything between. `\n<paths>\n` requires the real block's own line.
    m = re.search(r"\n<paths>\n(.*?)\n</paths>", to_text, re.S)
    granted = [p.strip() for p in (m.group(1).splitlines() if m else []) if p.strip()]
    grants_source_map = any(SOURCE_MAP_REL == g or SOURCE_MAP_REL.startswith(g) for g in granted)
    emit("")
    emit("(6) this order's <paths> grant (%s):" % TO_REL)
    for g in granted:
        emit("  %s" % g)
    emit("  %s covered by the grant: %s" % (SOURCE_MAP_REL, grants_source_map))

    blocked = one_pin and is_ancestor and len(range_commits) >= 1 and content_differs and head_is_fix \
        and not touches_source_map and not grants_source_map
    emit("")
    emit("RESULT: build-blocked-by-stale-pin-and-out-of-grant CONFIRMED: %s" % blocked)
    if blocked:
        emit(TOKEN)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
