"""Round 46 HVST-as-3 plant (row Z-S85): the named field census chooses the SERVED row by the reader's rule.

Reads the live served barrons rows of bronze key 00b99ce0... (three parts with equal run_stamp and fetched_at) in S3 key order
and folds them through `round46/field_census.py` `served_choice`. It must land on the row `store.silver_latest` serves (the
`-r2` part, 74 columns). MUTANT: the old run_stamp rule (strict >, first-read wins a tie) must land on the pre-round part.
Read-only. Prints `PLANT RESULT: PASS|FAIL`.
"""

import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, *([os.pardir] * 8)))
sys.path.insert(0, ROOT)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import store  # noqa: E402

KEY = ("barrons/harvest/bronze/article/article_hash=00b99ce07f3f6ed1e5435c9ea98794aac29fb61393a33ca13975e036df87758e/"
       "20261002T074454Z.json")

spec = importlib.util.spec_from_file_location("field_census", os.path.join(HERE, "field_census.py"))
census = importlib.util.module_from_spec(spec)
spec.loader.exec_module(census)


def main():
    c = store._default_client()
    prefix = store.table_prefix("barrons", "silver", "article")
    parts = []
    for page in c.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
        parts += [o["Key"] for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet")]
    hits = []
    for k in parts:
        for r in pq.read_table(io.BytesIO(c.get_object(Bucket=store.HARVEST_BUCKET, Key=k)["Body"].read())).to_pylist():
            if r.get("bronze_key") == KEY:
                hits.append((k, r))
    print("rows for the key: %d (%s)" % (len(hits), ", ".join(k.rsplit("/", 1)[-1] for k, _ in hits)))
    held, held_part = None, None
    for k, r in hits:
        if census.served_choice(held, held_part, r, k):
            held, held_part = r, k
    mut, mut_part = None, None
    for k, r in hits:
        if mut is None or str(r.get("run_stamp")) > str(mut.get("run_stamp")):
            mut, mut_part = r, k
    latest = store.silver_latest("barrons", "article", ("article_key",), client=c)
    served = latest.get((hits[0][1]["article_key"],)) if hits else None
    print("census served_choice -> %s (%d columns)" % (held_part.rsplit("/", 1)[-1], len(held)))
    print("store.silver_latest  -> record_hash %s; census row record_hash %s" % (served and served.get("record_hash"), held.get("record_hash")))
    print("MUTANT run_stamp rule -> %s (%d columns)" % (mut_part.rsplit("/", 1)[-1], len(mut)))
    ok = (len(hits) >= 3 and held_part.endswith("-r2.parquet") and len(held) == 74
          and served is not None and served.get("record_hash") == held.get("record_hash")
          and not mut_part.endswith("-r2.parquet"))
    print("PLANT RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
