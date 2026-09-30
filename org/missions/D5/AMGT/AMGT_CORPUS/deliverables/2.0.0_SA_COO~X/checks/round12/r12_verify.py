"""Round-12 after-state read (AMGT_CORPUS, CRPS-n-1 pair, after-state lines 1 and 5). Read-only.

Line 1: object and partition counts under the builder's prefix and the legacy prefix.
Line 5: for HEI, CPA and SHOP, the document `read_dossier` serves from the new prefix against the legacy prefix's newest
object carrying the same METHOD_VERSION; `fields` and `inputs` must be equal, and `artifact` must differ by construction.
"""
import json

from lib.research.corpus import dossier, gold
from lib.research.harvest import store

LEGACY_PREFIX = gold.table_prefix(dossier.TABLE).replace(dossier.TABLE, dossier.TABLE.replace("_", chr(45)))
NAMES = ("HEI_US_Equity", "CPA_US_Equity", "SHOP_CN_Equity")


def _census(client, prefix):
    parts = set()
    objects = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            objects.append((obj["Key"], obj["LastModified"]))
            parts.add(obj["Key"].split("/")[-2])
    return objects, parts


def main():
    client = store._default_client()
    new_prefix = gold.table_prefix(dossier.TABLE)
    new_objects, new_parts = _census(client, new_prefix)
    legacy_objects, legacy_parts = _census(client, LEGACY_PREFIX)
    print("prefix %s objects %d partitions %d" % (new_prefix, len(new_objects), len(new_parts)))
    print("prefix %s objects %d partitions %d" % (LEGACY_PREFIX, len(legacy_objects), len(legacy_parts)))
    for name in NAMES:
        served = dossier.read_dossier(name, client=client)
        doc = served["document"]
        partition = served["uri"].split("/")[-2]
        rows = [(k, t) for k, t in legacy_objects if k.split("/")[-2] == partition]
        legacy_docs = []
        for key, modified in rows:
            body = json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client).decode("utf-8"))
            if body.get("method_version") == dossier.METHOD_VERSION:
                legacy_docs.append((modified, key, body))
        if not legacy_docs:
            print("name %s legacy_current_method 0" % name)
            continue
        _modified, legacy_key, legacy = max(legacy_docs, key=lambda r: (r[0], r[1]))
        print("name %s served_prefix_new %s fields_equal %s cases_equal %s inputs_equal %s artifact %s legacy_artifact %s"
              % (name, served["uri"].startswith("s3://%s/%s" % (gold.HARVEST_BUCKET, new_prefix)),
                 doc["fields"] == legacy["fields"], doc["fields"]["cases"] == legacy["fields"]["cases"],
                 doc["inputs"] == legacy["inputs"], doc["artifact"], legacy["artifact"]))


if __name__ == "__main__":
    main()
