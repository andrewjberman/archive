"""AMGT_RESAPP round 52, AMGT-ab-6 half measurement -- which names' SERVED dossier pick moves when the build carries dossier.py's
METHOD_VERSION /4 -> /5 (AMGT_CORPUS x-1, 597f0647ea; the only dossier.py change in ab-6's closure).
For every security_key partition under the research_dossier gold prefix, the pick is computed twice with the module's own pick rule
(`dossier._read_dossier_detail`), once with METHOD_VERSION forced to "amgt-corpus-dossier/4" (the deployed preference) and once at
HEAD ("/5"), and EVERY field of the picked document compared except the new `pack_shape` (so `cases`, which /thesis serves as the team's
cases, is included).
Prints the denominator, the names whose picked object moves, and among those the names whose served dossier_fields values move.
usage: python <this>   (from the repo root; S3 read-only)"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

FIELDS = ("thesis_pillars", "management", "fund_of_record", "last_stated_position")


def pick(key, client, method):
    saved = dossier.METHOD_VERSION
    dossier.METHOD_VERSION = method
    try:
        uri, doc, _cur = dossier._read_dossier_detail(key, client)
        return uri, doc
    finally:
        dossier.METHOD_VERSION = saved


def main():
    client = store._default_client()
    uri0, _ = pick("AZN_LN_Equity", client, dossier.METHOD_VERSION)
    prefix = uri0.split("security_key=")[0].split("/", 3)[3] + "security_key="
    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=uri0.split("/")[2], Prefix=prefix, Delimiter="/"):
        keys += [p["Prefix"][len(prefix):].rstrip("/").replace("-SLASH-", "/") for p in page.get("CommonPrefixes", []) or []]
    moved_pick, moved_fields = [], []
    for k in sorted(keys):
        u4, d4 = pick(k, client, "amgt-corpus-dossier/4")
        u5, d5 = pick(k, client, dossier.METHOD_VERSION)
        if u4 != u5:
            moved_pick.append(k)
            a4, a5 = (d4.get("fields") or {}), (d5.get("fields") or {})
            names = sorted((set(a4) | set(a5)) - {"pack_shape"})
            diff = [f for f in names if json.dumps(a4.get(f), sort_keys=True) != json.dumps(a5.get(f), sort_keys=True)]
            if diff:
                moved_fields.append((k, diff))
    print("names with a dossier: %d (HEAD METHOD_VERSION %s)" % (len(keys), dossier.METHOD_VERSION))
    print("served pick moves /4 -> /5: %d %s" % (len(moved_pick), moved_pick[:12]))
    print("of those, ANY dossier field value (all fields but the new pack_shape, incl. cases) moves: %d %s" % (len(moved_fields), moved_fields[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
