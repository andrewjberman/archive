"""ch8_census.py -- AMGT_HARVST HVST-ch-8 (round 93, CTO round-92 analysis item 4). READ-ONLY.

For every security with a continuation partition under amgt/harvest/gold/research-continuation/:
the SERVED object is the gateway's pick (infra/aws/ec2/opal-gateway/app/harvest_research.py line 349,
copied here, with that line's .json/.json.gz row filter). AT_CURRENT when the served object's
method_version equals continuation.METHOD_VERSION. Otherwise built = continuation.build(security_key,
client) IN MEMORY (write_one is never called) and built["fields"] is compared with the served fields
FIELD BY FIELD over the union of the two key sets, by PARSED value: both sides pass a JSON round trip
(sort_keys) before ==, so key order and whitespace never count and tuple/list types do not count.

The S3 client is wrapped: only get_object, head_object, list_objects_v2 and get_paginator("list_objects_v2")
are forwarded; any other operation raises. Budget (order HVST-ch-8): 5000 requests and 1 GiB; the run
aborts before exceeding either.

Output: printed to stdout AND written with LF line endings to ch8_census.out beside this file.
Run from the worktree root:  python -u <this file>
"""

import copy
import gzip
import io
import json
import os
import sys
from collections import Counter

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import continuation  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "ch8_census.out")

BUDGET_REQUESTS = 5000
BUDGET_BYTES = 1024 ** 3
GATEWAY_SUFFIXES = (".json", ".json.gz")  # harvest_research.py:348 filter
UNDERSCORE_PREFIX = "amgt/harvest/gold/research_continuation/"  # harvest_research.py:46 (canonical, read first)
ABSENT = object()

_OUT = open(OUT_PATH, "w", encoding="utf-8", newline="\n")


def emit(line):
    text = line.encode("ascii", "backslashreplace").decode("ascii")
    print(text, flush=True)
    _OUT.write(text + "\n")
    _OUT.flush()


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


def norm(value):
    """Parsed-value form: the JSON round trip (sorted keys; tuples become lists)."""
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


def show(value):
    """First 70 characters of the parsed value, or 'absent'."""
    if value is ABSENT:
        return "absent"
    return json.dumps(value, sort_keys=True, ensure_ascii=True)[:70]


def field_diffs(built_fields, served_fields):
    """Field names whose parsed values differ over the union of the key sets (a missing key is not null)."""
    changed = []
    for name in sorted(set(built_fields) | set(served_fields)):
        b = built_fields.get(name, ABSENT)
        s = served_fields.get(name, ABSENT)
        if (b is ABSENT) != (s is ABSENT) or (b is not ABSENT and b != s):
            changed.append(name)
    return changed


def gateway_pick(objects):
    """objects: [(key, last_modified)]. harvest_research.py:349 -- newest .json/.json.gz row by
    (last_modified or "", key). Returns the key, or None when the partition holds no such object."""
    rows = [
        {"key": key, "last_modified": (lm.isoformat() if lm is not None else None)}
        for key, lm in objects
        if key.endswith(GATEWAY_SUFFIXES)
    ]
    if not rows:
        return None
    newest = max(rows, key=lambda r: (r["last_modified"] or "", r["key"]))
    return newest["key"]


def version_int(document):
    value = document.get("method_version")
    if not isinstance(value, str):
        return -1
    try:
        return int(value.rsplit("/", 1)[1])
    except (IndexError, ValueError):
        return -1


def short_name(key):
    """First 8 characters of the object name (the key's final path segment)."""
    if key is None:
        return "none"
    return key.rsplit("/", 1)[-1][:8]


def list_partition_prefixes(client, prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=gold.HARVEST_BUCKET, Prefix=prefix, Delimiter="/"
    ):
        for common in page.get("CommonPrefixes", []) or []:
            out.append(common["Prefix"])
    return sorted(set(out))


def list_objects(client, prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            out.append((obj["Key"], obj.get("LastModified")))
    return out


def served_of(client, partition_prefix):
    """(served_key, served_doc or None, objects) for one partition: the gateway's pick, read once."""
    objects = list_objects(client, partition_prefix)
    served_key = gateway_pick(objects)
    doc = None
    if served_key is not None:
        uri = "s3://%s/%s" % (gold.HARVEST_BUCKET, served_key)
        raw = gold.gold_get(uri, client=client)
        if served_key.endswith(".gz"):
            raw = gzip.decompress(raw)
        doc = json.loads(raw.decode("utf-8"))
    return served_key, doc, objects


def partition_of(prefix, security_key):
    return prefix + crosswalk.security_key_partition(security_key) + "/"


def control_positive(client, prefix):
    key = "MNST_US_Equity"
    served_key, served_doc, _objects = served_of(client, partition_of(prefix, key))
    built = continuation.build(key, client=client)
    changed = field_diffs(norm(built["fields"]), norm((served_doc or {}).get("fields") or {}))
    emit("CONTROL-POSITIVE %s fields_changed=%d" % (key, len(changed)))
    emit(
        "CONTROL-POSITIVE-DETAIL served=%s/%d method_version_is_current=%s list=%s"
        % (
            short_name(served_key),
            version_int(served_doc or {}),
            "yes" if (served_doc or {}).get("method_version") == continuation.METHOD_VERSION else "no",
            ",".join(changed) or "none",
        )
    )


def control_negative(client, prefix):
    key = "UNH_US_Equity"
    served_key, served_doc, _objects = served_of(client, partition_of(prefix, key))
    original = norm(served_doc)
    planted = copy.deepcopy(original)
    field = sorted(planted["fields"])[0]
    planted["fields"][field] = {"census_negative_control": True}
    changed = field_diffs(planted["fields"], original["fields"])
    emit("CONTROL-NEGATIVE fields_changed=%d" % len(changed))
    emit(
        "CONTROL-NEGATIVE-DETAIL name=%s planted_field=%s served=%s/%d list=%s"
        % (key, field, short_name(served_key), version_int(original), ",".join(changed) or "none")
    )


def main():
    client = ReadOnlyCounting(store._default_client())
    prefix = gold.table_prefix(continuation.TABLE)

    partitions = list_partition_prefixes(client, prefix)
    emit("PARTITIONS prefix=%s n=%d" % (prefix, len(partitions)))

    securities = 0
    at_current = 0
    names = 0
    unchanged = 0
    changed_names = 0
    fields_changed_total = 0
    inputs_equal_n = 0
    name_exists_n = 0
    build_errors = []
    nonjson_total = 0
    field_counts = Counter()
    name_segments = []

    for partition_prefix in partitions:
        segment = partition_prefix[len(prefix):].rstrip("/")
        if not segment.startswith("security_key="):
            emit("SKIP-NONSECURITY-PARTITION %s" % partition_prefix)
            continue
        security_key = crosswalk.security_key_from_slash_safe(segment[len("security_key="):])
        if crosswalk.security_key_partition(security_key) != segment:
            emit("SKIP-PARTITION-ROUNDTRIP-MISMATCH %s" % partition_prefix)
            continue
        securities += 1
        name_segments.append(segment)

        served_key, served_doc, objects = served_of(client, partition_prefix)
        nonjson = [k for k, _lm in objects if not k.endswith(GATEWAY_SUFFIXES)]
        if nonjson:
            nonjson_total += len(nonjson)
            emit("NONJSON-EXCLUDED %s n=%d" % (security_key, len(nonjson)))
        if served_key is None:
            emit("NO-SERVED-OBJECT %s objects=%d" % (security_key, len(objects)))
        served_doc = served_doc if served_doc is not None else {}

        if served_doc.get("method_version") == continuation.METHOD_VERSION:
            at_current += 1
            emit("AT-CURRENT %s served=%s/%d" % (security_key, short_name(served_key), version_int(served_doc)))
            continue

        names += 1
        try:
            built = continuation.build(security_key, client=client)
        except Exception as exc:  # recorded, never silently dropped
            build_errors.append(security_key)
            emit("BUILD-ERROR %s %s: %s" % (security_key, type(exc).__name__, str(exc)[:120]))
            continue

        built_fields = norm(built["fields"])
        served_fields = norm(served_doc.get("fields") or {})
        changed = field_diffs(built_fields, served_fields)
        inputs_eq = norm(built["inputs"]) == norm(served_doc.get("inputs"))
        target = partition_prefix + continuation._inputs_sha16(built["inputs"]) + ".json"
        exists = target in set(k for k, _lm in objects)

        emit(
            "NAME %s served=%s/%d fields_changed=%d list=%s inputs_equal=%s name_exists=%s"
            % (
                security_key,
                short_name(served_key),
                version_int(served_doc),
                len(changed),
                ",".join(changed) or "none",
                "yes" if inputs_eq else "no",
                "yes" if exists else "no",
            )
        )
        for field in changed:
            emit(
                "DIFF %s %s served=%s built=%s"
                % (
                    security_key,
                    field,
                    show(served_fields.get(field, ABSENT)),
                    show(built_fields.get(field, ABSENT)),
                )
            )
            field_counts[field] += 1
        if changed:
            changed_names += 1
            fields_changed_total += len(changed)
        else:
            unchanged += 1
        if inputs_eq:
            inputs_equal_n += 1
        if exists:
            name_exists_n += 1

    emit("CONTROL-START")
    control_positive(client, prefix)
    control_negative(client, prefix)

    for field in sorted(field_counts):
        emit("FIELD %s names_changed=%d" % (field, field_counts[field]))

    underscore_partitions = list_partition_prefixes(client, UNDERSCORE_PREFIX)
    underscore_segments = set(p[len(UNDERSCORE_PREFIX):].rstrip("/") for p in underscore_partitions)
    overlap = [s for s in name_segments if s in underscore_segments]
    emit(
        "PROBE-UNDERSCORE-PREFIX prefix=%s partitions=%d hyphen_partitions_also_underscore=%d"
        % (UNDERSCORE_PREFIX, len(underscore_partitions), len(overlap))
    )
    emit("PROBE-NONJSON-EXCLUDED total=%d" % nonjson_total)
    if build_errors:
        emit("BUILD-ERRORS n=%d names=%s" % (len(build_errors), ",".join(build_errors)))

    emit(
        "CENSUS-CONT-REBUILD partitions=%d at_current=%d names=%d unchanged=%d changed=%d fields_changed=%d "
        "inputs_equal=%d name_exists=%d gets=%d bytes=%d"
        % (
            securities,
            at_current,
            names,
            unchanged,
            changed_names,
            fields_changed_total,
            inputs_equal_n,
            name_exists_n,
            client.requests,
            client.bytes,
        )
    )
    _OUT.close()


if __name__ == "__main__":
    main()
