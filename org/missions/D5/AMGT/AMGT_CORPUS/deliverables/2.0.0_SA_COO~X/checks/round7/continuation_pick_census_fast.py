"""AMGT_CORPUS round 7 -- the limb-4 gate census, fast form. Read-only. Writes nothing.

Same question and same output line as `continuation_pick_census.py`: for every resolved name, does a stored
continuation exist whose `inputs` equal current inputs AND whose `method_version` is the producer's CURRENT one?
If so, do BOTH readers return that method version?

Why a second instrument: the first called `substrate.substrate()` whole (every member, not only continuation) and
ran 95 names serially; two runs timed out at 900 s and 3000 s. This one calls the SAME two reader paths --
`continuation.read_latest` and substrate's own continuation member `substrate._continuation_member` (the exact
function `substrate()` uses for its `continuation` entry) -- and runs the names concurrently. No selection logic is
re-implemented here.
"""
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from lib.research.corpus import continuation as C
from lib.research.corpus import gold, substrate
from lib.research.harvest import store

WORKERS = 16


def _one(sk, client):
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
        return sk, False, None, None
    picked_a = C.read_latest(sk, client=client).get("method_version")
    entry, _document = substrate._continuation_member(sk, client)
    picked_b = entry.get("method_version")
    return sk, True, picked_a, picked_b


def main():
    t0 = time.time()
    client = store._default_client()
    names = C._resolved_security_keys(client=client)
    current_available = 0
    stale = 0
    errors = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(_one, sk, client): sk for sk in names}
        for fut in as_completed(futures):
            sk = futures[fut]
            try:
                _sk, has_current, picked_a, picked_b = fut.result()
            except Exception as exc:  # a failed read is a VALUE to report, never a silent zero
                errors += 1
                print("ERROR: %s %s: %s" % (sk, type(exc).__name__, exc))
                continue
            if not has_current:
                print("no_current_method %s" % sk)
                continue
            current_available += 1
            if picked_a != C.METHOD_VERSION or picked_b != C.METHOD_VERSION:
                stale += 1
                print("stale_pick %s read_latest %s substrate %s" % (sk, picked_a, picked_b))
    print(
        "continuation_pick names %d current_method_available %d stale_pick %d errors %d method %s elapsed_s %.0f"
        % (len(names), current_available, stale, errors, C.METHOD_VERSION, time.time() - t0)
    )
    sys.stdout.flush()


if __name__ == "__main__":
    main()
