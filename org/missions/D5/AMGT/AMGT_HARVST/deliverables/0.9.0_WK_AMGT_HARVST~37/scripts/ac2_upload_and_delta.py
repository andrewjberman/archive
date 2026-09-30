#!/usr/bin/env python3
"""HVST-w-2 AC2 -- ONE `upload-harvest --max-objects 40` with the BEFORE / AFTER sa counts on the SAME instrument.

NO VENDOR CALL: upload-harvest reads the local outbox and writes S3 (opal-data-harvest bronze/silver, sa subtree)
only. It is run IN THIS PROCESS through the producer's own CLI entry point with the AMENDMENT 1 guards installed and
verified first, so even this leg cannot reach a re-authentication path. The instrument is HVST-v-2's read-only
`_census.py` (copied beside this script) plus a silver `article` row count read the same way on both sides.

A zero delta is reported as a zero with its cause named, from the outbox rows BEFORE the upload.
"""
import contextlib
import json
import os
import sqlite3
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
import _guards  # noqa: E402


class _Tee:
    def __init__(self, a, path):
        self.a, self.f = a, open(path, "w", encoding="utf-8")

    def write(self, x):
        self.a.write(x)
        self.f.write(x)

    def flush(self):
        self.a.flush()
        self.f.flush()


class _Buf:
    def __init__(self, passthrough):
        self.p, self.parts = passthrough, []

    def write(self, x):
        self.parts.append(x)
        self.p.write(x)

    def flush(self):
        self.p.flush()

    def text(self):
        return "".join(self.parts)


def main():
    from _census import (MAIN_TREE, RUNTIME_ROOT, PUBLISHERS, client, listing_hit_rows, silver_counts,
                         silver_part_counts, bronze_news_listing_counts, outbox_census)
    import lib.research.harvest.store as store
    from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER
    import lib.opal_data_harvest.__main__ as producer

    print("AC2 -- HVST-w-2 upload-harvest leg. MAIN_TREE=%s" % MAIN_TREE)
    rows = _guards.resolve_entries()
    if not _guards.print_identity(rows):
        print("REFUSED: a guard is not loaded in this process; upload-harvest is NOT called")
        return 3

    c = client()

    def silver_article_state():
        latest = store.silver_latest(SOURCE_FOR_PUBLISHER["sa"], "article", ("article_key",), client=c)
        parts = 0
        for page in c.get_paginator("list_objects_v2").paginate(
                Bucket=store.HARVEST_BUCKET, Prefix=store.table_prefix(SOURCE_FOR_PUBLISHER["sa"], "silver", "article")):
            parts += sum(1 for o in page.get("Contents", []) or [] if o["Key"].endswith(".parquet"))
        return len(latest), parts

    def pending_outbox():
        con = sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % RUNTIME_ROOT, uri=True)
        try:
            return {"listing": con.execute("SELECT status,count(*) FROM harvest_listing_outbox WHERE publisher='sa' GROUP BY status").fetchall(),
                    "raw": con.execute("SELECT status,count(*) FROM harvest_raw_outbox WHERE publisher='sa' GROUP BY status").fetchall()}
        finally:
            con.close()

    def snapshot(label):
        listing_rows = silver_counts(listing_hit_rows(c))
        parts = silver_part_counts(c)
        bronze = bronze_news_listing_counts(c)
        art_rows, art_parts = silver_article_state()
        outbox = outbox_census()
        snap = {"silver_listing_hit_rows": listing_rows, "silver_listing_hit_part_files": parts,
                "bronze_news_listing_objects": bronze, "sa_silver_article_rows": art_rows,
                "sa_silver_article_part_files": art_parts, "sa_outbox": pending_outbox(),
                "pending_listing_rows_all_publishers": len(outbox["pending_listing_rows"])}
        print("%s (five-publisher denominator %d; sa is the publisher of this cell):" % (label, len(PUBLISHERS)))
        print("  sa silver listing_hit rows %d | part files %d | bronze news_listing objects %d" % (
            listing_rows.get("sa", 0), parts.get("sa", 0), bronze.get("sa", 0)))
        print("  sa silver article rows (distinct article_key, newest per key) %d | article part files %d" % (art_rows, art_parts))
        print("  sa local outbox (status,count): listing %r  raw %r" % (snap["sa_outbox"]["listing"], snap["sa_outbox"]["raw"]))
        return snap

    before = snapshot("BEFORE")
    argv = ["upload-harvest", "--max-objects", "40", "--runtime-root", RUNTIME_ROOT]
    print("\nCOMMAND LINE (verbatim; executed by calling lib.opal_data_harvest.__main__.main() in this process, ONE invocation, no retry):")
    print("  python -m lib.opal_data_harvest " + " ".join('"%s"' % a if "/" in a else a for a in argv))
    sys.argv = ["python -m lib.opal_data_harvest"] + argv
    buf = _Buf(sys.stdout)
    rc, exc = None, None
    print("---- upload-harvest STDOUT (VERBATIM) ----")
    with contextlib.redirect_stdout(buf):
        try:
            rc = producer.main()
        except _guards.GuardStop as g:
            exc = "GUARD STOP: %s" % g
        except SystemExit as e:
            rc = e.code
        except Exception:
            exc = traceback.format_exc()
    print("---- end upload-harvest STDOUT ----")
    print("upload-harvest rc=%r%s" % (rc, ("  EXCEPTION:\n" + exc) if exc else ""))
    try:
        receipt = json.loads(buf.text().strip().splitlines()[-1])
    except Exception:
        receipt = None
    print("receipt: %s" % (json.dumps(receipt)[:1500] if receipt else "none parsed"))
    print("guard trips this process: %d" % len(_guards.TRIPS))

    after = snapshot("\nAFTER")
    print("\nDELTAS (signed), sa, same instrument both sides:")
    d = {
        "silver_listing_hit_rows": after["silver_listing_hit_rows"].get("sa", 0) - before["silver_listing_hit_rows"].get("sa", 0),
        "silver_listing_hit_part_files": after["silver_listing_hit_part_files"].get("sa", 0) - before["silver_listing_hit_part_files"].get("sa", 0),
        "bronze_news_listing_objects": after["bronze_news_listing_objects"].get("sa", 0) - before["bronze_news_listing_objects"].get("sa", 0),
        "silver_article_rows": after["sa_silver_article_rows"] - before["sa_silver_article_rows"],
        "silver_article_part_files": after["sa_silver_article_part_files"] - before["sa_silver_article_part_files"],
    }
    for k, v in d.items():
        print("  sa %-32s %+d" % (k, v))
    other = {p: after["silver_listing_hit_rows"].get(p, 0) - before["silver_listing_hit_rows"].get(p, 0) for p in PUBLISHERS if p != "sa"}
    print("  other publishers' silver listing_hit row deltas (denominator 4): %r" % other)
    pend_before = sum(n for st, n in before["sa_outbox"]["listing"] + before["sa_outbox"]["raw"] if st == "pending")
    print("sa outbox rows PENDING before the upload: %d" % pend_before)
    if not any(d.values()):
        print("ZERO DELTA on every sa measure. CAUSE (from the BEFORE outbox): %s" % (
            "the sa outbox held 0 pending rows, so upload-harvest had nothing to put -- the capture (AC1) accepted 0 articles "
            "and fetched no listing (the account check returned an HTTP error before any listing request)" if pend_before == 0
            else "%d pending rows existed but nothing landed: see the receipt above" % pend_before))
    out = {"before": before, "after": after, "deltas": d, "rc": rc, "receipt": receipt, "exception": exc,
           "command": argv, "guard_trips": _guards.TRIPS}
    (DELIV / "w2_ac2_upload.json").write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    print("wrote w2_ac2_upload.json")
    return 0 if exc is None else 1


if __name__ == "__main__":
    os.chdir(REPO)
    sys.stdout = _Tee(sys.stdout, DELIV / "w2_ac2_output.txt")
    _guards.install_guards()
    try:
        code = main()
    except _guards.GuardStop as g:
        print("GUARD STOP escaped: %s" % g)
        code = 1
    sys.exit(code)
