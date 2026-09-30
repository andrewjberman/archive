"""HVST-q-2 AC2: parse the REAL bbg bronze objects the 2026-09-30 silver rows name, under the base builder
(commit ff4405d3d5, loaded from git) and the new one. READ-ONLY: S3 LIST/GET only; no PUT, no delete, no vendor call.
"""
import datetime
import subprocess
import sys
import types

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lib.opal_data_harvest import silver_from_bronze as new_sfb  # noqa: E402
from lib.research.harvest import store  # noqa: E402

BASE_COMMIT = "ff4405d3d5"
DAY = "2026-09-30"
FETCHED = datetime.datetime(2026, 9, 30, tzinfo=datetime.timezone.utc)


def load_base():
    src = subprocess.run(["git", "show", "%s:lib/opal_data_harvest/silver_from_bronze.py" % BASE_COMMIT],
                         capture_output=True, check=True, cwd=ROOT).stdout.decode("utf-8")
    mod = types.ModuleType("lib.opal_data_harvest._q2_base_sfb")
    mod.__package__ = "lib.opal_data_harvest"
    exec(compile(src, "silver_from_bronze@" + BASE_COMMIT, "exec"), mod.__dict__)
    return mod


def main():
    base = load_base()
    cl = store._default_client()
    latest = store.silver_latest("bloomberg", "article", ("article_key",), client=cl)
    served = sorted((r for r in latest.values() if str(r["fetched_at"]).startswith(DAY)), key=lambda r: r["bronze_key"])
    print("served bbg silver rows fetched %s: %d" % (DAY, len(served)))
    ok, shortfalls = 0, []
    for i, row in enumerate(served, 1):
        key = row["bronze_key"]
        body = cl.get_object(Bucket=store.HARVEST_BUCKET, Key=key)["Body"].read()
        b = base.article_rows("bbg", body, "as_received", key, FETCHED, "backfill", "q2")
        n = new_sfb.article_rows("bbg", body, "as_received", key, FETCHED, "backfill", "q2")
        print("[%02d] %s\n     base: title=%r text_blocks=%d\n     new : title=%r text_blocks=%d published_utc=%s article_id=%s"
              % (i, key, b["title"], len(b["text_blocks"]), n["title"], len(n["text_blocks"]),
                 n["published_utc"], n["article_id"]))
        reason = None
        if not (n["title"] or "").strip():
            reason = "empty title"
        elif not n["text_blocks"]:
            reason = "0 text blocks"
        elif n["published_utc"] is None:
            reason = "no published date"
        if reason:
            shortfalls.append((key, reason))
        else:
            ok += 1
    for key, reason in shortfalls:
        print("SHORTFALL: %s -- %s" % (key, reason))
    print("REAL BBG OBJECTS PARSED NON-EMPTY: %d of %d" % (ok, len(served)))
    return 0 if served and ok == len(served) else 1


if __name__ == "__main__":
    sys.exit(main())
