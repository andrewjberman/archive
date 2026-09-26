"""AC1 -- DRAIN WHAT IS ALREADY HELD: BEFORE state from S3, ONE upload-harvest invocation through
the producer, AFTER state on the SAME instrument, sa's delta as a signed number.

NO VENDOR CALL IS MADE HERE: `upload-harvest` reads the local outbox and writes S3 only
(__main__.py:195-211). The only network plane touched is AWS.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(
    os.getcwd(), "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~22", "scripts"))

# `silver_counts` is NOT imported here: print_state RETURNS the per-publisher counts it printed, so
# importing it would be an unused import (ruff F401, commit-gate rule 14). The counts this script
# compares are therefore exactly the counts it printed -- one call, not two.
from _census import (MAIN_TREE, RUNTIME_ROOT, PUBLISHERS, client, listing_hit_rows, row_key,
                     silver_part_counts, bronze_news_listing_counts, outbox_census, print_state)

OUT_DIR = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                       "0.9.0_WK_AMGT_HARVST~22")

print("AC1 -- HVST-v-2, slot ~22")
print("MAIN_TREE placeholder EXPANDED to: %s" % MAIN_TREE)
print("runtime root passed to the producer: %s" % RUNTIME_ROOT)
print("")

c = client()

before_rows = listing_hit_rows(c)
before_parts = silver_part_counts(c)
before_bronze = bronze_news_listing_counts(c)
before_outbox = outbox_census()
before_counts = print_state("BEFORE", before_rows, before_parts, before_bronze, before_outbox)
before_keys = sorted({row_key(r) for r in before_rows})
print("  sa silver listing_hit rows BEFORE (explicit): %d" % before_counts.get("sa", 0))
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
after_outbox = outbox_census()
after_counts = print_state("AFTER", after_rows, after_parts, after_bronze, after_outbox)
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
sa_delta = after_counts.get("sa", 0) - before_counts.get("sa", 0)
print("")
print("AC1 sa silver listing_hit DELTA (signed): %+d" % sa_delta)
print("AC1 new record keys landed (all publishers): %d" % len(set(after_keys) - set(before_keys)))
print("AC1 upload-harvest rc: %d" % proc.returncode)

snapshot = {
    "main_tree_expansion": MAIN_TREE,
    "runtime_root": RUNTIME_ROOT,
    "publishers_denominator": len(PUBLISHERS),
    "publishers": list(PUBLISHERS),
    "before": {"silver_listing_hit_rows": before_counts,
               "silver_part_files": before_parts,
               "bronze_news_listing_objects": before_bronze,
               "row_keys": before_keys},
    "after": {"silver_listing_hit_rows": after_counts,
              "silver_part_files": after_parts,
              "bronze_news_listing_objects": after_bronze,
              "row_keys": after_keys},
    "sa_silver_listing_hit_delta": sa_delta,
    "upload_harvest": {"cmd": cmd, "rc": proc.returncode, "stdout": out, "stderr": err},
}
path = os.path.join(OUT_DIR, "ac1_before_after.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(snapshot, fh, indent=2, sort_keys=True)
print("wrote %s (AC3 reads its before.row_keys to split BEFORE from AFTER)" % path)
