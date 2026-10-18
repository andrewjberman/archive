"""AMGT_HARVST HVST-ch-7, issuer's own read-back of the research-continuation objects (2.0.0_SA_COO~W1). READ ONLY.

Reads the seat's manifest (ch7_written.out). For each WROTE line: lists the name's partition by the gateway's pick rule
(newest LastModified as an ISO string, then key), and prints whether the manifest key is the newest, its method_version,
whether its stored content_sha256 equals the sha256 of the canonical JSON of the document without that key, whether its
inputs and fields equal the PREVIOUS newest object's, and the partition's object count. Then prints the table total and the
dossier object count. Run from the repo root:  python -u <this file>
"""
import hashlib
import json
import sys

sys.path.insert(0, ".")
from lib.research.corpus import continuation, dossier, gold   # noqa: E402
from lib.research.harvest import store                        # noqa: E402

MANIFEST = "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.7.0_AE_CloudOps~SC1/round93/ch7_written.out"


def list_partitions(client, counter):
    """Every object under the continuation table, grouped by partition: {partition: [(last_modified_iso, key)]}."""
    prefix = "amgt/harvest/gold/%s/" % continuation.TABLE
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


def fetch(client, counter, key):
    counter[0] += 1
    return json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client).decode("utf-8"))


def manifest_rows():
    rows = []
    for line in open(MANIFEST, encoding="utf-8"):
        if " WROTE cont " in line:
            parts = dict(p.split("=", 1) for p in line.split() if "=" in p)
            rows.append((parts["name"], parts["key"]))
    return rows


def main():
    client = store._default_client()
    counter = [0]
    objs = list_partitions(client, counter)
    print("LISTED partitions=%d objects=%d" % (len(objs), sum(len(v) for v in objs.values())))
    rows = manifest_rows()
    seen = set()
    bad = 0
    for name, key in rows:
        ordered = sorted(objs.get(key.rsplit("/", 1)[0], []))
        newest = ordered[-1][1] if ordered else None
        prev = ordered[-2][1] if len(ordered) > 1 else None
        new = fetch(client, counter, key)
        body = {k: v for k, v in new.items() if k != "content_sha256"}
        sha_ok = hashlib.sha256(continuation._canonical_bytes(body)).hexdigest() == new.get("content_sha256")
        old = fetch(client, counter, prev) if prev else {}
        ok = (newest == key and new.get("method_version") == continuation.METHOD_VERSION and sha_ok
              and new.get("fields") == old.get("fields") and new.get("inputs") == old.get("inputs")
              and new.get("subject", {}).get("security_key") == name)
        bad += 0 if ok else 1
        seen.add(name)
        print("OBJ %s newest=%s method=%s sha_ok=%s fields_equal_prev=%s inputs_equal_prev=%s prev_method=%s "
              "partition_objects=%d %s"
              % (name, newest == key, new.get("method_version", "?").rsplit("/", 1)[-1], sha_ok,
                 new.get("fields") == old.get("fields"), new.get("inputs") == old.get("inputs"),
                 str(old.get("method_version", "none")).rsplit("/", 1)[-1], len(ordered), "OK" if ok else "BAD"))
    dossiers = gold.gold_list(dossier.TABLE, client=client)
    print("VERIFY manifest_names=%d distinct=%d bad=%d table_objects=%d dossier_objects=%d gets=%d"
          % (len(rows), len(seen), bad, sum(len(v) for v in objs.values()), len(dossiers), counter[0]))


main()
