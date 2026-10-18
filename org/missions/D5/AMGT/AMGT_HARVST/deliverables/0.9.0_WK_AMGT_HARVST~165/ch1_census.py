"""ch1_census.py -- AMGT_HARVST HVST-ch-1 (round 93, row D1-S52). READ-ONLY.

For every security with a continuation partition under
amgt/harvest/gold/research-continuation/: list the partition, read every
object, compute wanted = continuation.current_inputs(security_key, client),
keep the input-matching objects (the substrate's candidates). When one
carries continuation.METHOD_VERSION it counts under with_current. Otherwise
the census prints PICK: OLD is the pre-round-93 rule reimplemented HERE
(min by key); NEW is the changed continuation._select_stored; GATEWAY is the
rule of infra/aws/ec2/opal-gateway/app/harvest_research.py:349 copied here.

The S3 client is wrapped: only get_object, list_objects_v2, head_object and
get_paginator are forwarded; any other operation raises. Budget: 1500
requests and 500 MiB; the run aborts before exceeding either.

Run from the worktree root:  python -u <this file>
"""

import io
import json
import os
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import continuation  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

BUDGET_REQUESTS = 1500
BUDGET_BYTES = 500 * 1024 * 1024
TOTAL_REQUESTS_LIMIT_NOTE = "budget requests=%d bytes=%d" % (BUDGET_REQUESTS, BUDGET_BYTES)


class ReadOnlyCounting(object):
    """Forwards the four read operations only; counts requests and bytes."""

    def __init__(self, client):
        self._client = client
        self.requests = 0
        self.bytes = 0

    def _check(self):
        if self.requests > BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise SystemExit("BUDGET-EXCEEDED requests=%d bytes=%d -- aborted" % (self.requests, self.bytes))

    def get_object(self, **kwargs):
        self.requests += 1
        resp = self._client.get_object(**kwargs)
        data = resp["Body"].read()
        self.bytes += len(data)
        self._check()
        return {"Body": io.BytesIO(data)}

    def head_object(self, **kwargs):
        self.requests += 1
        self._check()
        return self._client.head_object(**kwargs)

    def list_objects_v2(self, **kwargs):
        self.requests += 1
        self._check()
        return self._client.list_objects_v2(**kwargs)

    def get_paginator(self, operation_name):
        assert operation_name == "list_objects_v2", operation_name
        outer = self

        class _Paginator(object):
            def paginate(self, **kwargs):
                for page in outer._client.get_paginator("list_objects_v2").paginate(**kwargs):
                    outer.requests += 1
                    outer._check()
                    yield page

        return _Paginator()

    def __getattr__(self, name):
        raise RuntimeError("census is READ-ONLY: refuses S3 operation %r" % name)


def _version_int(document):
    """Census's own reading of the method version: the integer after the last '/'; -1 when missing or unparsable."""
    value = document.get("method_version")
    if not isinstance(value, str):
        return -1
    try:
        return int(value.rsplit("/", 1)[1])
    except (IndexError, ValueError):
        return -1


def _short(key):
    return key[:8]


def main():
    client = ReadOnlyCounting(store._default_client())
    prefix = gold.table_prefix(continuation.TABLE)

    partitions = []
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix, Delimiter="/"):
        for common in page.get("CommonPrefixes", []) or []:
            partitions.append(common["Prefix"])
    partitions = sorted(set(partitions))
    print("PARTITIONS prefix=%s n=%d" % (prefix, len(partitions)))

    securities = 0
    with_current = 0
    no_current = 0
    no_input_match = 0
    new_equals = 0
    new_differs = 0
    old_equals = 0
    old_differs = 0
    skipped = 0

    for partition_prefix in partitions:
        segment = partition_prefix[len(prefix):].rstrip("/")
        if not segment.startswith("security_key="):
            skipped += 1
            print("SKIP-NONSECURITY-PARTITION %s" % partition_prefix)
            continue
        security_key = crosswalk.security_key_from_slash_safe(segment[len("security_key="):])
        if crosswalk.security_key_partition(security_key) != segment:
            skipped += 1
            print("SKIP-PARTITION-ROUNDTRIP-MISMATCH %s" % partition_prefix)
            continue
        securities += 1

        objects = []
        listing = client.get_paginator("list_objects_v2")
        for page in listing.paginate(Bucket=gold.HARVEST_BUCKET, Prefix=partition_prefix):
            for obj in page.get("Contents", []) or []:
                objects.append((obj["Key"], obj.get("LastModified")))

        docs = {}
        for key, _lm in objects:
            uri = "s3://%s/%s" % (gold.HARVEST_BUCKET, key)
            docs[key] = json.loads(gold.gold_get(uri, client=client).decode("utf-8"))

        wanted = continuation.current_inputs(security_key, client=client)
        candidates = [(key, lm, docs[key]) for key, lm in objects if docs[key].get("inputs") == wanted]

        if any(c[2].get("method_version") == continuation.METHOD_VERSION for c in candidates):
            with_current += 1
            continue

        no_current += 1
        if not candidates:
            no_input_match += 1
            print("NOINPUT %s partition_objects=%d" % (security_key, len(objects)))
            continue

        # OLD: the pre-round-93 rule, reimplemented here (min by key).
        old = min(candidates, key=lambda c: c[0])
        # NEW: the changed rule, read from the module.
        new = continuation._select_stored(candidates, continuation.METHOD_VERSION)
        # GATEWAY: copied from infra/aws/ec2/opal-gateway/app/harvest_research.py:349.
        gw_rows = [
            {"key": key, "last_modified": (lm.isoformat() if lm is not None else None)}
            for key, lm in objects
        ]
        newest = max(gw_rows, key=lambda r: (r["last_modified"] or "", r["key"]))
        gateway_key = newest["key"]

        new_key = new[0]
        same_new = new_key == gateway_key
        same_old = old[0] == gateway_key
        if same_new:
            new_equals += 1
        else:
            new_differs += 1
        if same_old:
            old_equals += 1
        else:
            old_differs += 1

        print(
            "PICK %s candidates=%d old=%s/%d new=%s/%d gateway=%s/%d new_equals_gateway=%s"
            % (
                security_key,
                len(candidates),
                _short(old[0]),
                _version_int(old[2]),
                _short(new_key),
                _version_int(new[2]),
                _short(gateway_key),
                _version_int(docs[gateway_key]),
                "yes" if same_new else "no",
            )
        )

    print("NO-INPUT-MATCH no_input_match=%d skipped=%d %s" % (no_input_match, skipped, TOTAL_REQUESTS_LIMIT_NOTE))
    print(
        "CENSUS-PICKER securities=%d with_current=%d no_current=%d new_equals_gateway=%d "
        "new_differs_from_gateway=%d old_equals_gateway=%d old_differs_from_gateway=%d "
        "gets=%d bytes=%d"
        % (
            securities,
            with_current,
            no_current,
            new_equals,
            new_differs,
            old_equals,
            old_differs,
            client.requests,
            client.bytes,
        )
    )


if __name__ == "__main__":
    main()
