"""AC2, second leg -- the ONE `upload-harvest` invocation that pushes what the capture just took
to S3, with the SAME S3 instrument AC1 used on both sides of it.

NO VENDOR CALL: `upload-harvest` reads the local outbox and writes S3 only.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(
    os.getcwd(), "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~22", "scripts"))

import lib.research.harvest.store as store
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
# `silver_counts` is NOT imported (ruff F401): print_state RETURNS the counts it printed, so the
# deltas below are computed from exactly the numbers that were printed, by one call and not two.
from _census import (MAIN_TREE, RUNTIME_ROOT, PUBLISHERS, client, listing_hit_rows, row_key,
                     silver_part_counts, bronze_news_listing_counts, outbox_census, print_state)

OUT_DIR = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~22")


def silver_article_counts(c):
    """{publisher: silver `article` part-file count} -- the capture's article bodies land here."""
    counts = {}
    for pub, source in sorted(SOURCE_FOR_PUBLISHER.items()):
        prefix = store.table_prefix(source, "silver", "article")
        n = 0
        for page in c.get_paginator("list_objects_v2").paginate(
                Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                if obj["Key"].endswith(".parquet"):
                    n += 1
        counts[pub] = n
    return counts


print("AC2 second leg -- upload-harvest for what the capture took")
print("MAIN_TREE placeholder EXPANDED to: %s" % MAIN_TREE)
print("")

c = client()
before_rows = listing_hit_rows(c)
before_parts = silver_part_counts(c)
before_bronze = bronze_news_listing_counts(c)
before_articles = silver_article_counts(c)
before_outbox = outbox_census()
before_counts = print_state("BEFORE (post-capture, pre-upload)", before_rows, before_parts,
                            before_bronze, before_outbox)
print("  silver article PART FILES per publisher: %r" % (before_articles,))
before_keys = sorted({row_key(r) for r in before_rows})
print("")

cmd = [sys.executable, "-m", "lib.opal_data_harvest", "upload-harvest",
       "--max-objects", "40", "--runtime-root", RUNTIME_ROOT]
print("INVOCATION (ONE, no retry loop): %r" % (cmd,))
proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out = proc.stdout.decode("utf-8", "replace")
err = proc.stderr.decode("utf-8", "replace")
print("upload-harvest rc=%d" % proc.returncode)
print("---- upload-harvest STDOUT (VERBATIM) ----")
print(out)
print("---- upload-harvest STDERR (VERBATIM) ----")
print(err)
print("---- end producer output ----")
print("")

after_rows = listing_hit_rows(c)
after_parts = silver_part_counts(c)
after_bronze = bronze_news_listing_counts(c)
after_articles = silver_article_counts(c)
after_outbox = outbox_census()
after_counts = print_state("AFTER", after_rows, after_parts, after_bronze, after_outbox)
print("  silver article PART FILES per publisher: %r" % (after_articles,))
after_keys = sorted({row_key(r) for r in after_rows})
print("")

print("DELTAS (signed), silver listing_hit rows, denominator 5 publishers:")
for p in PUBLISHERS:
    d = after_counts.get(p, 0) - before_counts.get(p, 0)
    print("  %-8s %+d  (%d -> %d)" % (p, d, before_counts.get(p, 0), after_counts.get(p, 0)))
print("DELTAS (signed), bronze news_listing objects:")
for p in PUBLISHERS:
    d = after_bronze.get(p, 0) - before_bronze.get(p, 0)
    print("  %-8s %+d  (%d -> %d)" % (p, d, before_bronze.get(p, 0), after_bronze.get(p, 0)))
print("DELTAS (signed), silver article part files:")
for p in PUBLISHERS:
    d = after_articles.get(p, 0) - before_articles.get(p, 0)
    print("  %-8s %+d  (%d -> %d)" % (p, d, before_articles.get(p, 0), after_articles.get(p, 0)))
sa_delta = after_counts.get("sa", 0) - before_counts.get("sa", 0)
print("")
print("AC2 sa silver listing_hit DELTA over the upload leg (signed): %+d" % sa_delta)
print("AC2 upload-harvest rc: %d" % proc.returncode)

snapshot = {
    "before": {"silver_listing_hit_rows": before_counts, "silver_part_files": before_parts,
               "bronze_news_listing_objects": before_bronze,
               "silver_article_part_files": before_articles, "row_keys": before_keys},
    "after": {"silver_listing_hit_rows": after_counts, "silver_part_files": after_parts,
              "bronze_news_listing_objects": after_bronze,
              "silver_article_part_files": after_articles, "row_keys": after_keys},
    "sa_silver_listing_hit_delta": sa_delta,
    "upload_harvest": {"cmd": cmd, "rc": proc.returncode, "stdout": out, "stderr": err},
}
path = os.path.join(OUT_DIR, "ac2_upload.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(snapshot, fh, indent=2, sort_keys=True)
print("wrote %s" % path)
