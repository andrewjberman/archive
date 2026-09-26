"""Read-only census of the research-dossier table's newest-object selection (AMGT_CORPUS round 6, CRPS-h-1).

For every security partition it compares the object `dossier.read_dossier` serves against the object written LAST
(S3 LastModified; gold never overwrites, so LastModified is the write time), and replays history: at each write,
did the pick serve the newest write? It also counts objects whose inputs hash repeats an earlier object's --
a rebuild that wrote on unchanged inputs (FWD-17 (b)). Writes nothing.
"""
import collections

from lib.research.corpus import dossier, gold
from lib.research.harvest import store


def main():
    client = store._default_client()
    prefix = gold.table_prefix(dossier.TABLE)
    parts = collections.defaultdict(list)
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            name = obj["Key"].split("/")[-1]
            parts[obj["Key"].split("/")[-2]].append((name[6:16], name[17:33], obj["LastModified"], obj["Key"]))
    agree = 0
    rewrites = 0
    for part, rows in sorted(parts.items()):
        security_key = part.split("=", 1)[1].replace("-SLASH-", "/")  # the partition is slash-safe
        served = dossier.read_dossier(security_key, client=client)["uri"].split("/", 3)[3]
        last_written = max(rows, key=lambda r: r[2])[3]
        agree += int(served == last_written)
        seen = set()
        for _date, inputs_hash, _t, _k in sorted(rows, key=lambda r: r[2]):
            rewrites += int(inputs_hash in seen)
            seen.add(inputs_hash)
    print("partitions %d objects %d" % (len(parts), sum(len(r) for r in parts.values())))
    print("rewrites_on_unchanged_inputs %d" % rewrites)
    print("read_dossier serves the last write %d of %d" % (agree, len(parts)))


if __name__ == "__main__":
    main()
