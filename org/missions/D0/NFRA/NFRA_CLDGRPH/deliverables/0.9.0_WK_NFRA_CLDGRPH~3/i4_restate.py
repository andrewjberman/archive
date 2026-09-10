#!/usr/bin/env python3
"""NFRA_CLDGRPH TO-CG-I-4 -- the citation grammar, practised rather than proposed.

Prints every dated archive key this project's record cites, in the grammar the cell names:
bucket/key@ETag, with the LastModified and the byte length beside it. The ETags are READ
LIVE in this run (s3api head-object through i4_lib.aws_read, which ledgers every call), so
the table is a MEASURED vintage and not a transcription.

WHAT THE TABLE CAN AND CANNOT DO, said here because the difference is the whole cell:
it fixes the vintage of these keys AS OF THIS RUN. It does NOT recover the bytes any earlier
citation named. A citation restated into this grammar tomorrow, after tonight's derive, will
carry a DIFFERENT ETag for the same key -- which is exactly the point: the grammar makes the
movement visible instead of silent.

usage: python i4_restate.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i4_lib  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.join(HERE, "i4_census.capture.json")
OUT = os.path.join(HERE, "i4_restatement.capture.json")


def main():
    root = i4_lib.repo_root()
    if not os.path.exists(CENSUS):
        print("BLOCKED: %s absent -- run i4_census.py first." % os.path.basename(CENSUS))
        return 2
    cap = json.load(open(CENSUS, encoding="utf-8"))
    keys = sorted(set(r["key"] for r in cap["rows"]))

    print("  the keys this project's record cites, restated as bucket/key@ETag")
    print("  (claim: measured -- s3api head-object, this run; %d of %d distinct cited keys)"
          % (len(keys), len(keys)))
    table = []
    for k in keys:
        h = i4_lib.head(root, k, "restatement of a cited key into bucket/key@ETag")
        if h is None:
            print("    %s/%s@ABSENT -- the key the record cites is NOT IN THE BUCKET" % (i4_lib.BUCKET, k))
            table.append({"key": k, "status": "ABSENT"})
            continue
        print("    %s/%s@%s" % (i4_lib.BUCKET, k, h["etag"]))
        print("        LastModified %s  ContentLength %d" % (h["last_modified"], h["size"]))
        cited = [r for r in cap["rows"] if r["key"] == k]
        ov = len([r for r in cited if r["class"] == "OVERWRITTEN"])
        un = len([r for r in cited if r["class"] == "UNDECIDABLE"])
        print("        cited %d time(s) in the record: %d OVERWRITTEN, %d UNDECIDABLE"
              % (len(cited), ov, un))
        table.append({"key": k, "status": "PRESENT", "etag": h["etag"],
                      "last_modified": h["last_modified"], "size": h["size"],
                      "citations": len(cited), "overwritten": ov, "undecidable": un})
    with open(OUT, "w", encoding="ascii", newline="\n") as fh:
        json.dump({"claim_provenance": "measured", "bucket": i4_lib.BUCKET,
                   "restated": table}, fh, indent=1, sort_keys=True)
    print("  RESTATED_KEYS=%d of %d" % (len([t for t in table if t["status"] == "PRESENT"]), len(keys)))
    print("  capture: %s" % os.path.relpath(OUT, root).replace(os.sep, "/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
