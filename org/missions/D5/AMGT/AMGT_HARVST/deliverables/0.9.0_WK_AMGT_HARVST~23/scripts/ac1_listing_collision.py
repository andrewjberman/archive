"""AC1 check for HVST-w-1 (row AMGT_HARVST-Z-W9-S1, listings half).

No vendor call, no network, no S3 read or write of any kind: `store.silver_append` (untouched,
lib/research/harvest/store.py is not in this worker's write grant) is called against a FAKE
in-process s3 client (`_StubS3`, same shape as `lib/opal_data_harvest/test_legacy_upload.py`'s
own stub and `lib/research/harvest/tests/test_store.py`'s) that honours `IfNoneMatch="*"` with
`PreconditionFailed` on a repeated key exactly as S3 does.

Proves, in order:
  (a) NEGATIVE CONTROL -- the direct, unwrapped `store.silver_append` call (the shape the
      listings path used AT HEAD, before this cell's fix) raises `PreconditionFailed` on the
      second of two same-second appends. Printed verbatim.
  (b) the SAME two appends through the repaired call site
      (`uploads._silver_append_retrying_object_name`, the wrapper the articles path already
      uses and this cell's fix now routes the listings path through) -- BOTH return a receipt,
      landing at two DISTINCT object names.
  (c) the row count landed across both keys equals the sum of the two row sets -- no row
      dropped.

Publisher-neutral: uses "ft" (source "ft"), not "sa", per BOUNDS 1.
"""

import datetime
import io
import os
import sys

sys.path.insert(0, os.getcwd())

from botocore.exceptions import ClientError  # noqa: E402

from lib.opal_data_harvest import uploads  # noqa: E402
import lib.research.harvest.store as store  # noqa: E402


class _StubS3:
    """Same shape as lib/opal_data_harvest/test_legacy_upload.py's `_StubS3` (itself modelled
    on lib/research/harvest/tests/test_store.py's own stub): honours IfNoneMatch="*" with
    PreconditionFailed, stores Metadata per key, has put_object/head_object/get_object and
    get_paginator("list_objects_v2")."""

    def __init__(self):
        self._objects = {}

    def put_object(self, Bucket, Key, Body, **kwargs):
        exists = (Bucket, Key) in self._objects
        if kwargs.get("IfNoneMatch") == "*" and exists:
            raise ClientError({"Error": {"Code": "PreconditionFailed", "Message": "stub"}}, "PutObject")
        body_bytes = Body if isinstance(Body, (bytes, bytearray)) else bytes(Body)
        self._objects[(Bucket, Key)] = {"body": body_bytes, "metadata": dict(kwargs.get("Metadata") or {})}
        return {"ETag": '"stub-etag"'}

    def head_object(self, Bucket, Key, **kwargs):
        obj = self._objects.get((Bucket, Key))
        if obj is None:
            raise ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "HeadObject")
        return {"Metadata": dict(obj["metadata"]), "ContentLength": len(obj["body"]), "ETag": '"stub-etag"'}

    def get_object(self, Bucket, Key, **kwargs):
        obj = self._objects.get((Bucket, Key))
        if obj is None:
            raise ClientError({"Error": {"Code": "NoSuchKey", "Message": "Not Found"}}, "GetObject")
        return {"Body": io.BytesIO(obj["body"]), "Metadata": dict(obj["metadata"]), "ContentLength": len(obj["body"])}

    def list_objects_v2(self, Bucket, Prefix="", **kwargs):
        contents = [{"Key": k} for (b, k) in self._objects if b == Bucket and k.startswith(Prefix)]
        return {"Contents": contents}

    def get_paginator(self, operation_name):
        assert operation_name == "list_objects_v2"
        outer = self

        class _Paginator:
            def paginate(self, **kw):
                yield outer.list_objects_v2(**kw)

        return _Paginator()


SOURCE = "ft"  # publisher-neutral: not "sa" (BOUNDS 1)
TABLE = "listing_hit"
RECORD_KEY_FIELDS = ("query_sha256", "fetch_date_utc", "search_page", "search_rank", "source")


def _row(search_rank, fetched_at):
    return {
        "query_sha256": "q" * 64,
        "fetch_date_utc": fetched_at.date(),
        "search_page": 1,
        "search_rank": search_rank,
        "source": SOURCE,
        "publisher": "ft",
        "article_id": "art-%d" % search_rank,
        "url": "https://example.com/%d" % search_rank,
        "search_query": "example query",
        "bronze_key": "ft/harvest/bronze/listing/date=%s/obj-%d.html" % (fetched_at.date(), search_rank),
        "fetched_at": fetched_at,
        "retrieval_mode": "live",
        "run_stamp": store.stamp(fetched_at),
    }


def _landed_row_count(client, source, table):
    prefix = store.table_prefix(source, "silver", table)
    total = 0
    for (bucket, key) in client._objects:
        if bucket == store.HARVEST_BUCKET and key.startswith(prefix) and key.endswith(".parquet"):
            import pyarrow.parquet as pq
            arrow_table = pq.read_table(io.BytesIO(client._objects[(bucket, key)]["body"]))
            total += arrow_table.num_rows
    return total


def main():
    fetched_at = datetime.datetime(2026, 9, 27, 12, 0, 0, tzinfo=datetime.timezone.utc)
    run_stamp = store.stamp(fetched_at)
    rows_a = [_row(1, fetched_at)]
    rows_b = [_row(2, fetched_at)]  # different record key (search_rank differs) -> same second

    # (a) NEGATIVE CONTROL -- direct, unwrapped store.silver_append, the shape the listings
    # path called AT HEAD before this cell's fix (uploads.py:277, pre-repair).
    control_client = _StubS3()
    store.silver_append(SOURCE, TABLE, rows_a, RECORD_KEY_FIELDS, run_stamp, client=control_client)
    control_failed = False
    control_error_text = None
    try:
        store.silver_append(SOURCE, TABLE, rows_b, RECORD_KEY_FIELDS, run_stamp, client=control_client)
    except ClientError as exc:
        control_failed = True
        control_error_text = str(exc)

    print("(a) NEGATIVE CONTROL -- direct store.silver_append, two same-second appends:")
    print("    first append: OK")
    print("    second append raised: %s" % (control_error_text if control_failed else "NOTHING -- CONTROL DID NOT REPRODUCE THE DEFECT"))
    if not control_failed:
        print("FAIL: negative control did not reproduce the collision at HEAD's unwrapped call shape")
        return 1

    # (b) the SAME two appends through the repaired call site.
    fixed_client = _StubS3()
    receipt_a = uploads._silver_append_retrying_object_name(
        fixed_client, SOURCE, TABLE, rows_a, RECORD_KEY_FIELDS, run_stamp,
    )
    receipt_b = uploads._silver_append_retrying_object_name(
        fixed_client, SOURCE, TABLE, rows_b, RECORD_KEY_FIELDS, run_stamp,
    )
    print("(b) repaired call site (_silver_append_retrying_object_name), same two appends:")
    print("    first receipt:  %r" % (receipt_a,))
    print("    second receipt: %r" % (receipt_b,))
    parts_a = set(receipt_a["parts"])
    parts_b = set(receipt_b["parts"])
    both_landed = bool(receipt_a["parts"]) and bool(receipt_b["parts"])
    distinct_names = parts_a.isdisjoint(parts_b)
    print("    both returned a receipt: %s" % both_landed)
    print("    distinct object names: %s (%r vs %r)" % (distinct_names, parts_a, parts_b))
    if not (both_landed and distinct_names):
        print("FAIL: repaired call site did not land both appends at distinct object names")
        return 1

    # (c) row count landed == sum of the two row sets, no row dropped.
    landed = _landed_row_count(fixed_client, SOURCE, TABLE)
    expected = len(rows_a) + len(rows_b)
    print("(c) row count landed across both keys: %d (expected sum of both row sets: %d)" % (landed, expected))
    if landed != expected:
        print("FAIL: row count landed does not equal the sum of the two row sets")
        return 1

    print("PASS: AC1 -- negative control reproduced the collision; the repaired call site lands both appends with no row dropped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
