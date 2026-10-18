"""AMGT_HARVST HVST-cj-5, issuer's own read-back of the research_dossier objects (2.0.0_SA_COO~W1). READ ONLY.

Reads the seat's manifest (cj5_written.out) and the list files. For each WROTE line: lists the name's partition, applies the
gateway's dossier pick (harvest_research.py::_pick_dossier: the greatest as_of stamp in the object name, then the greatest
LastModified, then the key), prints whether the manifest key is the pick, the method version, whether the stored
content_sha256 equals the sha256 of the canonical JSON of the document without that key, which `fields` differ from the
dossier that was served before (the pick over the other objects) and whether that set is within {fund_form_ref, model_rows},
and whether it equals the census's expected move list for the name. Then the table and continuation object counts.
Run from the repo root:  python -u <this file>
"""
import hashlib
import json
import re
import sys

sys.path.insert(0, ".")
from lib.research.corpus import continuation, dossier, gold   # noqa: E402
from lib.research.harvest import store                        # noqa: E402

DELIV = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/"
MANIFEST = DELIV + "0.7.0_AE_CloudOps~SC1/round95/cj5_written.out"
NAMES = DELIV + "2.0.0_SA_COO_W1/round95/cj5_names.txt"
EXPECTED = DELIV + "2.0.0_SA_COO_W1/round95/cj5_expected_moves.txt"
ALLOWED = {"fund_form_ref", "model_rows"}
AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")


def list_table(client, counter, table):
    prefix = "amgt/harvest/gold/%s/" % table
    objs = {}
    token = None
    while True:
        params = {"Bucket": gold.HARVEST_BUCKET, "Prefix": prefix}
        if token:
            params["ContinuationToken"] = token
        resp = client.list_objects_v2(**params)
        counter[0] += 1
        for item in resp.get("Contents", []):
            stamp = item["LastModified"].isoformat() if item.get("LastModified") else ""
            objs.setdefault(item["Key"].rsplit("/", 1)[0], []).append((stamp, item["Key"]))
        if not resp.get("IsTruncated"):
            return objs
        token = resp.get("NextContinuationToken")


def pick(rows):
    """The gateway's rule: the greatest as_of stamp, then the greatest LastModified, then the key."""
    by_stamp = {}
    for last_modified, key in rows:
        m = AS_OF.search(key)
        if m is not None:
            by_stamp.setdefault(m.group(1), []).append((last_modified, key))
    if not by_stamp:
        return None
    return max(by_stamp[max(by_stamp)])[1]


def fetch(client, counter, key):
    counter[0] += 1
    return json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client).decode("utf-8"))


def manifest_rows():
    rows = []
    for line in open(MANIFEST, encoding="utf-8"):
        if " WROTE dossier " in line:
            parts = dict(p.split("=", 1) for p in line.split() if "=" in p)
            rows.append((parts["name"], parts["key"]))
    return rows


def expected_moves():
    out = {}
    for line in open(EXPECTED, encoding="utf-8"):
        name, fields = line.split()
        out[name] = set(fields.split(","))
    return out


def main():
    client = store._default_client()
    counter = [0]
    objs = list_table(client, counter, dossier.TABLE)
    total = sum(len(v) for v in objs.values())
    print("LISTED table=%s partitions=%d objects=%d" % (dossier.TABLE, len(objs), total))
    rows = manifest_rows()
    listed_names = [line.strip() for line in open(NAMES, encoding="utf-8") if line.strip()]
    expect = expected_moves()
    bad = 0
    equal_expected = 0
    for name, key in rows:
        part = key.rsplit("/", 1)[0]
        listing = objs.get(part, [])
        picked = pick(listing)
        before_key = pick([r for r in listing if r[1] != key])
        new = fetch(client, counter, key)
        old = fetch(client, counter, before_key) if before_key else {}
        body = {k: v for k, v in new.items() if k != "content_sha256"}
        sha_ok = hashlib.sha256(dossier._canonical_bytes(body)).hexdigest() == new.get("content_sha256")
        nf, of = new.get("fields") or {}, old.get("fields") or {}
        moved = {f for f in set(nf) | set(of) if nf.get(f) != of.get(f)}
        within = moved <= ALLOWED
        same_as_expected = moved == expect.get(name, set())
        equal_expected += 1 if same_as_expected else 0
        ok = (picked == key and new.get("method_version") == dossier.METHOD_VERSION and sha_ok and within
              and new.get("subject", {}).get("security_key") == name and name in listed_names)
        bad += 0 if ok else 1
        print("OBJ %s pick_is_manifest=%s method=%s sha_ok=%s moved=%s within_allowed=%s equals_census=%s "
              "as_of_new=%s as_of_before=%s objects_in_partition=%d %s"
              % (name, picked == key, new.get("method_version", "?").rsplit("/", 1)[-1], sha_ok,
                 ",".join(sorted(moved)) or "none", within, same_as_expected, new.get("as_of"), old.get("as_of"),
                 len(listing), "OK" if ok else "BAD"))
    cont = list_table(client, counter, continuation.TABLE)
    names_manifest = {n for n, _ in rows}
    print("VERIFY manifest_names=%d distinct=%d list_names=%d equal_list=%s bad=%d equals_census=%d table_objects=%d "
          "continuation_objects=%d gets=%d"
          % (len(rows), len(names_manifest), len(listed_names), names_manifest == set(listed_names), bad,
             equal_expected, total, sum(len(v) for v in cont.values()), counter[0]))


main()
