#!/usr/bin/env python3
"""check_fwd6_design -- the FWD-6 design (BF-u-6) has its seven sections in order and cites only paths that exist.

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/check_fwd6_design.py

Checks, over FWD6_DESIGN_round6.md beside this file:
  1. the `## ` headings (outside fenced blocks) are exactly the seven required, in order;
  2. every inline backticked token that names a repository path exists. A token is a repository path when it has no
     whitespace and no character of {}*<>=|(),;" and its first segment is a directory at the repository root
     (so prose such as Write/Edit is not read as a path). A trailing :LINE, :LINE-LINE or @hash is dropped first.
Last line, printed once: FWD6-DESIGN ok=<True|False> headings=<n found> paths=<n checked> missing=<n>
Python 3.9; ASCII only; standard library only.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.join(HERE, "FWD6_DESIGN_round6.md")
HEADINGS = [
    "Outcome",
    "Past patterns",
    "Where it runs",
    "The decision rule",
    "What it refuses and what it lets through",
    "The exercise that would prove it",
    "What it does not cover",
]
BAD = set("{}*<>=|(),;\"")


def repo_root(start):
    d = start
    while True:
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "org")):
            return d
        up = os.path.dirname(d)
        if up == d:
            raise SystemExit("FWD6-DESIGN ok=False headings=0 paths=0 missing=0 (no repository root above %s)" % start)
        d = up


def split_doc(text):
    """(prose lines outside fences, h2 headings outside fences)"""
    prose, heads, fenced = [], [], False
    for ln in text.splitlines():
        if ln.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        prose.append(ln)
        if ln.startswith("## "):
            heads.append(ln[3:].strip())
    return prose, heads


def path_tokens(prose, top):
    out = []
    for ln in prose:
        for tok in re.findall(r"`([^`]+)`", ln):
            if re.search(r"\s", tok) or any(c in BAD for c in tok):
                continue
            core = re.sub(r"@[0-9a-fA-F]{6,40}$", "", tok)
            core = re.sub(r":\d+(-\d+)?$", "", core)
            if "/" not in core:
                continue
            if core.split("/", 1)[0] not in top:
                continue
            out.append(core)
    return out


def main():
    root = repo_root(HERE)
    with open(DOC, "rb") as fh:
        text = fh.read().decode("utf-8")
    prose, heads = split_doc(text)
    top = set(os.listdir(root))
    toks = path_tokens(prose, top)
    missing = sorted(set(t for t in toks if not os.path.exists(os.path.join(root, *t.split("/")))))
    heads_ok = heads == HEADINGS
    for m in missing:
        print("MISSING: " + m)
    if not heads_ok:
        print("HEADINGS WANTED: %r" % (HEADINGS,))
        print("HEADINGS FOUND:  %r" % (heads,))
    ok = heads_ok and not missing and len(toks) > 0
    print("FWD6-DESIGN ok=%s headings=%d paths=%d missing=%d" % (ok, len(heads), len(set(toks)), len(missing)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
