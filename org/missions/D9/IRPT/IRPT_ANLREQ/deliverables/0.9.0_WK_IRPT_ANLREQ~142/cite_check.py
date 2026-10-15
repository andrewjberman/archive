"""AR335-y-AC2: re-open every {file, line, text} cite in r41/PACKAGER_DOOR_READ.json.

Each cite's file is resolved from the worktree root (the folder holding org/ and .tools/). The cited line
number must exist and the cited text must be a substring of that line after stripping both.
Prints CITES-OK <n> of <n> when every cite holds; on the first miss prints CITES-BAD <file>:<line> and exits 1.
Reads files only; no AWS call, no network, no edit.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE / "r41" / "PACKAGER_DOOR_READ.json"
CITE_KEYS = {"file", "line", "text"}


def find_root(start):
    for candidate in [start] + list(start.parents):
        if (candidate / "org").is_dir() and (candidate / ".tools").is_dir():
            return candidate
    return None


def collect(node, out):
    if isinstance(node, dict):
        if CITE_KEYS <= set(node):
            out.append(node)
        for value in node.values():
            collect(value, out)
    elif isinstance(node, list):
        for value in node:
            collect(value, out)
    return out


def main():
    root = find_root(HERE)
    if root is None:
        print("CITES-BAD no-worktree-root")
        sys.exit(1)
    rec = json.loads(RECORD.read_text(encoding="utf-8"))
    cites = collect(rec, [])
    total = len(cites)
    file_cache = {}
    for cite in cites:
        rel = str(cite["file"])
        line_no = cite["line"]
        text = str(cite["text"]).strip()
        where = "%s:%s" % (rel, line_no)
        if rel not in file_cache:
            target = root / rel
            if not target.is_file():
                print("CITES-BAD " + where)
                sys.exit(1)
            file_cache[rel] = target.read_text(encoding="utf-8").splitlines()
        lines = file_cache[rel]
        if type(line_no) is not int or not 1 <= line_no <= len(lines):
            print("CITES-BAD " + where)
            sys.exit(1)
        if not text or text not in lines[line_no - 1].strip():
            print("CITES-BAD " + where)
            sys.exit(1)
    print("CITES-OK %d of %d" % (total, total))
    sys.exit(0)


if __name__ == "__main__":
    main()
