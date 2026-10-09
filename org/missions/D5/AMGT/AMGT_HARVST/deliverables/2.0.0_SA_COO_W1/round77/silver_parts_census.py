"""HARVST round 77 -- read-only census of silver listing_hit and article parts per source since the runner's activation.

Lists every object under `store.table_prefix(<source>, "silver", <table>)` for the four FWD-18 sources and counts the parts
written at or after 2026-10-09T08:57Z. LISTs only; nothing is written. Run: `PYTHONPATH=. python <this file>`.
"""
import lib.research.harvest.store as store

SINCE = "2026-10-09T08:57"
SOURCES = ("bloomberg", "wsj", "barrons", "seeking-alpha")


def main():
    client = store._default_client()
    for source in SOURCES:
        for table in ("listing_hit", "article"):
            prefix = store.table_prefix(source, "silver", table)
            parts, recent, newest = 0, 0, ""
            for page in client.get_paginator("list_objects_v2").paginate(Bucket=store.HARVEST_BUCKET, Prefix=prefix):
                for obj in page.get("Contents", []) or []:
                    parts += 1
                    stamp = obj["LastModified"].isoformat()[:19]
                    newest = max(newest, stamp)
                    if stamp >= SINCE:
                        recent += 1
            print("%s %s: parts %d, since %sZ %d, newest %s" % (source, table, parts, SINCE, recent, newest))


if __name__ == "__main__":
    main()
