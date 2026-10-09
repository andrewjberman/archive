"""AMGT_RESAPP round-83 PREP -- no Anthropic key value sits in a worker's files (row AMGT_RESAPP-D1-W324-S3).

  python r83_nokey.py <dir> [<dir> ...]

Walks every file under each dir (binary files read as bytes) for a key VALUE: `sk-ant-` followed by 20 or more key characters.
Prints only the file path and the hit count, never the value. A redacted stub (`sk-ant-` with fewer characters) is not a hit.
Verdict: R83 NOKEY: YES (0 hits) | NO, exit 0|1.
"""
from __future__ import annotations

import os
import re
import sys

KEY_RE = re.compile(rb"sk-ant-[A-Za-z0-9_-]{20,}")


def main(argv):
    if not argv:
        print("usage: r83_nokey.py <dir> [<dir> ...]")
        return 2
    files = 0
    hits = 0
    for top in argv:
        if os.path.isfile(top):
            walk = [(os.path.dirname(top), [], [os.path.basename(top)])]
        else:
            walk = os.walk(top)
        for base, _dirs, names in walk:
            for name in names:
                path = os.path.join(base, name)
                try:
                    data = open(path, "rb").read()
                except OSError as exc:
                    print("WARN: unreadable %s (%s)" % (path, exc.__class__.__name__))
                    continue
                files += 1
                n = len(KEY_RE.findall(data))
                if n:
                    hits += n
                    print("HIT %s: %d key value(s)" % (path, n))
    print("files scanned %d across %d path(s), key values found %d" % (files, len(argv), hits))
    print("R83 NOKEY: %s" % ("YES" if hits == 0 else "NO"))
    return 0 if hits == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
