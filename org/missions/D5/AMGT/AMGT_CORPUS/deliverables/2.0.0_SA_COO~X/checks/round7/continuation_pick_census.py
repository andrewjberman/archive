"""AMGT_CORPUS round 7 -- the issuer's read-only census for CRPS-i-1 (Z-S45). Writes nothing.

For every resolved name: does a stored continuation exist whose `inputs` equal current inputs AND whose
`method_version` is the producer's CURRENT one? If so, do BOTH readers (continuation.read_latest and
substrate.substrate()['continuation']) return that method version? A reader that returns an older method version
while a current-method match exists is a STALE PICK -- the 49/46 split of Z-S45.
"""
import json

from lib.research.corpus import continuation as C
from lib.research.corpus import gold, substrate
from lib.research.harvest import store


def main():
    client = store._default_client()
    names = C._resolved_security_keys(client=client)
    current_available = 0
    stale = 0
    for sk in names:
        wanted = C.current_inputs(sk, client=client)
        partition = store.entity_partition("security_key", sk)
        prefix = gold.table_prefix(C.TABLE) + partition + "/"
        has_current = False
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                doc = json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, obj["Key"]), client=client))
                if doc.get("inputs") == wanted and doc.get("method_version") == C.METHOD_VERSION:
                    has_current = True
        if not has_current:
            continue
        current_available += 1
        picked_a = C.read_latest(sk, client=client).get("method_version")
        picked_b = substrate.substrate(sk, client=client)["continuation"].get("method_version")
        if picked_a != C.METHOD_VERSION or picked_b != C.METHOD_VERSION:
            stale += 1
            print("stale_pick %s read_latest %s substrate %s" % (sk, picked_a, picked_b))
    print("continuation_pick names %d current_method_available %d stale_pick %d" % (len(names), current_available, stale))


if __name__ == "__main__":
    main()
