"""HVST-ch-7 step 4 (ii) and (iii), READ ONLY, run from the pinned worktree (C:/tmp/ch7-build at 091ebacda9). ASCII only.
  python -u ch7_after.py
Prints: the dossier object count (step 0 read 1479), the continuation object count (step 0 read 368; expected 368 + 78 = 446),
the manifest line count, and per manifest line: the key exists, its VersionId equals the manifest's, and it is the gateway's pick
(newest .json/.json.gz by LastModified, then key) of its partition. Writes nothing."""
from __future__ import annotations

import os
import re
import sys

WT = r"C:\tmp\ch7-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

MANIFEST = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables\0.7.0_AE_CloudOps~SC1\round93\ch7_written.out"
DOSSIER_START = 1479
CONT_START = 368


def count(client, table):
    n = 0
    parts = set()
    pre = gold.table_prefix(table)
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=pre):
        for o in page.get("Contents", []) or []:
            n += 1
            parts.add(o["Key"][len(pre):].split("/")[0])
    return n, len(parts)


def main():
    client = store._default_client()
    dn, dp = count(client, "research_dossier")
    cn, cp = count(client, continuation.TABLE)
    print("COUNT research_dossier objects=%d partitions=%d start=%d unchanged=%s" % (dn, dp, DOSSIER_START, dn == DOSSIER_START))
    print("COUNT research-continuation objects=%d partitions=%d start=%d plus78=%s" % (cn, cp, CONT_START, cn == CONT_START + 78))
    rows = []
    for ln in open(MANIFEST, encoding="ascii"):
        m = re.search(r" WROTE cont name=(\S+) key=(\S+) VersionId=(\S+) ", ln)
        if m:
            rows.append(m.groups())
    print("MANIFEST WROTE lines=%d distinct names=%d" % (len(rows), len({r[0] for r in rows})))
    bad = 0
    current_ok = 0
    for name, key, version in rows:
        head = client.head_object(Bucket=gold.HARVEST_BUCKET, Key=key)
        part = key.rsplit("/", 1)[0] + "/"
        objs = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=part):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith((".json", ".json.gz")):
                    objs.append((o["LastModified"].isoformat(), o["Key"]))
        pick = max(objs)[1] if objs else None
        ok = head.get("VersionId") == version and pick == key
        current_ok += 1 if ok else 0
        if not ok:
            bad += 1
            print("MISMATCH name=%s key=%s head_version=%s manifest_version=%s gateway_pick=%s" % (name, key, head.get("VersionId"), version, pick))
    print("MANIFEST-CHECK names=%d version_equal_and_is_gateway_pick=%d mismatches=%d" % (len(rows), current_ok, bad))
    return 0


if __name__ == "__main__":
    sys.exit(main())
