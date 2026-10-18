"""HVST-cj-4 step 4, READ ONLY, run from the pinned worktree (C:/tmp/cj4-build at 8f329a10b9). ASCII only.
  python -u cj4_after.py
Prints: the dossier object count (step 0 read 1479; expected 1479 + manifest lines), the continuation object count (446, unchanged),
the manifest line count and its names against cj4_names.txt, and per manifest name: the key exists, its VersionId equals the
manifest's, and the gateway's dossier pick rule (_pick_dossier, copied) over a fresh listing of its partition names the manifest key
(pick_equals_manifest=<n of n>). Writes nothing."""
from __future__ import annotations

import datetime
import os
import re
import sys

WT = r"C:\tmp\cj4-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, dossier, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BASE = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables"
MANIFEST = BASE + r"\0.7.0_AE_CloudOps~SC1\round95\cj4_written.out"
NAMES = BASE + r"\2.0.0_SA_COO_W1\round95\cj4_names.txt"
DOSSIER_START = 1479
CONT_START = 446
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")


def utc_text(value):
    if value is None:
        return None
    return value.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pick_dossier(rows):
    by_stamp = {}
    for r in rows:
        m = _AS_OF.search(r["key"])
        if m is not None:
            by_stamp.setdefault(m.group(1), []).append(r)
    if not by_stamp:
        return None
    stamp = max(by_stamp)
    return max(by_stamp[stamp], key=lambda r: (r["last_modified"] or "", r["key"]))


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
    rows = []
    for ln in open(MANIFEST, encoding="ascii"):
        m = re.search(r" WROTE dossier name=(\S+) key=(\S+) VersionId=(\S+) ", ln)
        if m:
            rows.append(m.groups())
    listed = [ln.strip() for ln in open(NAMES, encoding="ascii") if ln.strip()]
    dn, dp = count(client, dossier.TABLE)
    cn, cp = count(client, continuation.TABLE)
    print("COUNT research_dossier objects=%d partitions=%d start=%d plus_manifest=%s" % (dn, dp, DOSSIER_START, dn == DOSSIER_START + len(rows)))
    print("COUNT research-continuation objects=%d partitions=%d start=%d unchanged=%s" % (cn, cp, CONT_START, cn == CONT_START))
    print("MANIFEST WROTE lines=%d distinct names=%d names equal the list=%s" % (len(rows), len({r[0] for r in rows}), sorted(r[0] for r in rows) == sorted(listed)))
    ok_pick = 0
    ok_ver = 0
    for name, key, version in rows:
        head = client.head_object(Bucket=gold.HARVEST_BUCKET, Key=key)
        prefix = key.rsplit("/", 1)[0] + "/"
        lst = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []) or []:
                if o["Key"].endswith((".json", ".json.gz")):
                    lst.append({"key": o["Key"], "last_modified": utc_text(o.get("LastModified"))})
        picked = pick_dossier(lst)
        v_ok = head.get("VersionId") == version
        p_ok = picked is not None and picked["key"] == key
        ok_ver += 1 if v_ok else 0
        ok_pick += 1 if p_ok else 0
        if not (v_ok and p_ok):
            print("MISMATCH name=%s key=%s head_version=%s manifest_version=%s pick=%s" % (name, key, head.get("VersionId"), version, picked and picked["key"]))
    print("MANIFEST-CHECK names=%d version_equal=%d pick_equals_manifest=%d of %d" % (len(rows), ok_ver, ok_pick, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
