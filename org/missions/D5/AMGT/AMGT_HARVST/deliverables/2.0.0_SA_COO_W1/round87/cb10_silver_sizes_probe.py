"""HVST-cb-10 read: how big is each publisher's silver table, per table? (LIST only, no GET, read-only.)

An uploader `silver_append` reads every part of the target table (store.silver_latest, uncached in its process), so a
table's total size is the most one upload of that table can read. This lists the parts under each publisher's silver
prefix and prints, per table: part count and total MiB. Paginated and counted client-side; the denominator is printed.

Usage: python cb10_silver_sizes_probe.py <publisher> [<publisher> ...]
"""

import collections
import sys

sys.path.insert(0, r"C:\dev\ajb_workspace")
from lib.opal_data_harvest import harvest_grammar  # noqa: E402
from lib.research.harvest import store  # noqa: E402


def main():
    client = store._default_client()
    for publisher in sys.argv[1:]:
        source = harvest_grammar.SOURCE_FOR_PUBLISHER[publisher]
        prefix = store.table_prefix(source, "silver", "t")[:-2]  # derived, never typed: cut the placeholder table "t/"
        tables = collections.defaultdict(lambda: [0, 0])
        total = 0
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []) or []:
                total += 1
                table = obj["Key"][len(prefix):].split("/", 1)[0]
                tables[table][0] += 1
                tables[table][1] += obj["Size"]
        print("SILVER %s objects_listed=%d prefix=%s" % (publisher, total, prefix))
        for table, (parts, nbytes) in sorted(tables.items()):
            print("  table=%s parts=%d mib=%.1f" % (table, parts, nbytes / 1048576.0))


if __name__ == "__main__":
    main()
