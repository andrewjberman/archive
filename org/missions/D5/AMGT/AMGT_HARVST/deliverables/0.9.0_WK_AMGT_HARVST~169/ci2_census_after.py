"""ci2_census_after.py -- AMGT_HARVST HVST-ci-2 (round 94, row D1-W165-S3). READ-ONLY.

Started from ci1_census.py. For every partition of the four tables the substrate
reads through _pick_stored (continuation, sector_template, fund_form, typecast):
list, read every object, compute `wanted` with the same producer call substrate.py
makes, count input-matching objects (as ci1). For EVERY partition with NO
matching object, call the CHANGED substrate._pick_stored (through the counting
read-only client) and print one AFTER line that compares the changed module's
pick with two rules REIMPLEMENTED in this file: RULE (highest method_version
integer, then the later LastModified, the key breaking a tie) and OLD
(sorted(docs)[-1], the pre-change key-order fallback). The census never reads
continuation._select_stored or any changed picker to compute RULE or OLD.

CONTROL-DIFFERENCE runs the UNH-shaped four objects of the TO's step 1b(1) through
the real changed _pick_stored with a fake in-memory client, and prints whether the
module's pick equals RULE and differs from OLD.

Budget (round-94 preflight): 8000 requests and 1 GiB; the run stops at the budget
and prints BUDGET-EXCEEDED. Output is written by this script to ci2_census_after.out
with newline="\\n" (stdout carries the same lines).

Run from the worktree root:  python -u <this file>
"""

import io
import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import continuation  # noqa: E402
from lib.research.corpus import fund_form  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import sector_template  # noqa: E402
from lib.research.corpus import substrate  # noqa: E402
from lib.research.corpus import typecast  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

OUT_PATH = os.path.join(
    ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~169", "ci2_census_after.out",
)
BUDGET_REQUESTS = 8000
BUDGET_BYTES = 1024 ** 3

_OUT = None


def emit(line):
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
    _OUT.write(line + "\n")
    _OUT.flush()


class BudgetExceeded(Exception):
    pass


class ReadOnlyCounting(object):
    """Forwards the read operations only; counts requests and bytes; refuses every other S3 operation."""

    def __init__(self, client):
        self._client = client
        self.requests = 0
        self.bytes = 0

    def _spend_request(self):
        if self.requests >= BUDGET_REQUESTS or self.bytes > BUDGET_BYTES:
            raise BudgetExceeded()
        self.requests += 1

    def _spend_bytes(self, n):
        self.bytes += n
        if self.bytes > BUDGET_BYTES:
            raise BudgetExceeded()

    def get_object(self, **kwargs):
        self._spend_request()
        resp = self._client.get_object(**kwargs)
        data = resp["Body"].read()
        self._spend_bytes(len(data))
        return {"Body": io.BytesIO(data)}

    def head_object(self, **kwargs):
        self._spend_request()
        return self._client.head_object(**kwargs)

    def get_paginator(self, operation_name):
        assert operation_name == "list_objects_v2", operation_name
        outer = self

        class _Paginator(object):
            def paginate(self, **kwargs):
                for page in outer._client.get_paginator("list_objects_v2").paginate(**kwargs):
                    outer._spend_request()
                    yield page

        return _Paginator()

    def __getattr__(self, name):
        raise RuntimeError("census is READ-ONLY: refuses S3 operation %r" % name)


def version_int(document):
    """Census reading of method_version: the integer after the last '/' (the whole value when there is
    no '/'); -1 when missing, not a string, or unparsable."""
    value = document.get("method_version")
    if not isinstance(value, str):
        return -1
    try:
        return int(value.rsplit("/", 1)[-1])
    except ValueError:
        return -1


def short(key):
    """First 8 characters of the object name (the key's final path segment)."""
    return key.rsplit("/", 1)[-1][:8]


def name_of(key):
    return key.rsplit("/", 1)[-1]


def old_pick(items):
    """OLD: the pre-change key-order fallback, reimplemented here: sorted(docs)[-1]."""
    key = sorted(it[0] for it in items)[-1]
    return next(it for it in items if it[0] == key)


def rule_pick(items):
    """RULE: highest method_version integer, then the later LastModified (a missing value never
    outranks a present one), then the greater key on an exact tie. Reimplemented here."""
    def rank(it):
        key, lm, doc = it
        if lm is None:
            present, stamp = 0, 0.0
        else:
            present, stamp = 1, lm.timestamp()
        return (version_int(doc), present, stamp, key)

    return max(items, key=rank)


def list_partitions(client, table):
    prefix = gold.table_prefix(table)
    seen = set()
    for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=gold.HARVEST_BUCKET, Prefix=prefix, Delimiter="/"
    ):
        for common in page.get("CommonPrefixes", []) or []:
            seen.add(common["Prefix"][len(prefix):].rstrip("/"))
        for obj in page.get("Contents", []) or []:
            emit("TOP-LEVEL-OBJECT %s" % obj["Key"])
    return sorted(seen)


def census_partition(client, table, partition, wanted_of):
    """One partition: list, read every object, compute wanted, count input matches."""
    prefix = gold.table_prefix(table) + partition + "/"
    listing = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            listing.append((obj["Key"], obj.get("LastModified")))
    docs = {}
    for key, _lm in listing:
        uri = "s3://%s/%s" % (gold.HARVEST_BUCKET, key)
        docs[key] = json.loads(gold.gold_get(uri, client=client).decode("utf-8"))
    items = [(key, lm, docs[key]) for key, lm in listing]
    wanted = None
    matches = 0
    if items:
        wanted = wanted_of(partition, docs)
        matches = len([it for it in items if it[2].get("inputs") == wanted])
    return {"objects": len(items), "matches": matches, "items": items, "wanted": wanted}


def continuation_wanted(client):
    def wanted_of(partition, docs):
        if not partition.startswith("security_key="):
            emit("NOT-READ-BY-SUBSTRATE continuation %s" % partition)
            return None
        try:
            security_key = crosswalk.security_key_from_slash_safe(partition[len("security_key="):])
        except Exception as exc:  # noqa: BLE001 -- a census prints, never hides
            emit("UNPARSABLE-PARTITION continuation %s %s" % (partition, type(exc).__name__))
            return None
        if crosswalk.security_key_partition(security_key) != partition:
            emit("ROUNDTRIP-MISMATCH continuation %s" % partition)
            return None
        return continuation.current_inputs(security_key, client=client)
    return wanted_of


def sector_wanted(client):
    def wanted_of(partition, docs):
        if not partition.startswith("business_type="):
            emit("NOT-READ-BY-SUBSTRATE sector_template %s" % partition)
            return None
        return sector_template.current_inputs(partition[len("business_type="):], client=client)
    return wanted_of


def fund_wanted(client):
    def wanted_of(partition, docs):
        names = sorted({(d.get("subject") or {}).get("fund") for d in docs.values()} - {None})
        if len(names) != 1:
            emit("FUND-NAME-UNRESOLVED fund_form %s names=%s" % (partition, names))
            return None
        name = names[0]
        if "fund=%s" % fund_form._slug(name) != partition:
            emit("SLUG-MISMATCH fund_form %s name=%s" % (partition, name))
        return fund_form.current_inputs(name, client=client)
    return wanted_of


def typecast_wanted(client):
    def wanted_of(partition, docs):
        return typecast.current_inputs(client=client)
    return wanted_of


def census_table(client, name, table, method_version, partitions, wanted_of, totals):
    stats = {"partitions": 0, "objects": 0, "input_match": 0, "no_input_match": 0}
    for partition in partitions:
        rec = census_partition(client, table, partition, wanted_of)
        stats["partitions"] += 1
        stats["objects"] += rec["objects"]
        if rec["objects"] == 0:
            emit("EMPTY %s %s" % (name, partition))
            stats["no_input_match"] += 1
            continue
        if rec["matches"] > 0:
            stats["input_match"] += 1
            continue
        stats["no_input_match"] += 1
        # FALLBACK partition: the changed module's pick, through the counting read-only client.
        items = rec["items"]
        rule = rule_pick(items)
        old = old_pick(items)
        module_doc, module_uri, module_current = substrate._pick_stored(
            table, partition, rec["wanted"], method_version, client
        )
        module_name = name_of(module_uri)
        rule_name = name_of(rule[0])
        old_name = name_of(old[0])
        module_equals_rule = module_name == rule_name
        moved_from_old = module_name != old_name
        totals["fallback_partitions"] += 1
        if module_equals_rule:
            totals["module_equals_rule"] += 1
        if moved_from_old:
            totals["moved_from_old"] += 1
        emit("AFTER %s %s module=%s/%d rule=%s/%d old=%s/%d module_equals_rule=%s moved_from_old=%s current=%s" % (
            name, partition,
            short(module_name), version_int(module_doc),
            short(rule_name), version_int(rule[2]),
            short(old_name), version_int(old[2]),
            "yes" if module_equals_rule else "no",
            "yes" if moved_from_old else "no",
            "yes" if module_current else "no",
        ))
    emit("TABLE %s partitions=%d objects=%d input_match=%d no_input_match=%d" % (
        name, stats["partitions"], stats["objects"], stats["input_match"], stats["no_input_match"],
    ))
    return stats


def utc(day):
    return datetime(2026, 10, day, tzinfo=timezone.utc)


class _Body(object):
    def __init__(self, data):
        self._data = data

    def read(self):
        return self._data


class _Paginator(object):
    def __init__(self, objects):
        self._objects = objects

    def paginate(self, Bucket, Prefix):
        contents = [
            {"Key": k, "LastModified": self._objects[k]["LastModified"]}
            for k in sorted(self._objects) if k.startswith(Prefix)
        ]
        yield {"Contents": contents}


class _FakeClient(object):
    """In-memory client for the control only: no network, no counting."""

    def __init__(self):
        self._objects = {}

    def add(self, key, version, lm, inputs):
        doc = {"method_version": version, "inputs": inputs, "content_sha256": "sha-" + name_of(key)}
        self._objects[key] = {"Body": json.dumps(doc, sort_keys=True).encode("utf-8"), "LastModified": lm}

    def get_object(self, Bucket, Key):
        return {"Body": _Body(self._objects[Key]["Body"])}

    def get_paginator(self, operation_name):
        assert operation_name == "list_objects_v2"
        return _Paginator(self._objects)


def control_difference():
    """The UNH-shaped four of step 1b(1): none matches `wanted`; the changed module's pick must equal RULE and differ from OLD."""
    partition = crosswalk.security_key_partition("UNH_US_Equity")
    prefix = gold.table_prefix(continuation.TABLE) + partition + "/"
    fake = _FakeClient()
    stored = [{"key": "census-control/stored", "sha256": "1"}]
    wanted = [{"key": "census-control/wanted", "sha256": "2"}]
    rows = (
        (1, "98a4883c1b099e6b.json", 25),
        (2, "f174f7092a2d358e.json", 26),
        (3, "28404359eb0645c4.json", 27),
        (4, "4d837586380648bd.json", 28),
    )
    for version, name, day in rows:
        fake.add(prefix + name, "amgt-corpus-continuation/%d" % version, utc(day), stored)
    items = [(k, v["LastModified"], json.loads(v["Body"].decode("utf-8"))) for k, v in sorted(fake._objects.items())]
    document, uri, current = substrate._pick_stored(
        continuation.TABLE, partition, wanted, continuation.METHOD_VERSION, fake
    )
    module_name = name_of(uri)
    rule_name = name_of(rule_pick(items)[0])
    old_name = name_of(old_pick(items)[0])
    module_is_rule = module_name == rule_name and current is False
    differs = module_name != old_name
    emit("CONTROL-DIFFERENCE module_pick=%s old_pick_differs=%s" % (
        "rule_pick" if module_is_rule else "not_rule_pick",
        "yes" if differs else "no",
    ))
    emit("CONTROL-DIFFERENCE-DETAIL module=%s/%d rule=%s old=%s current=%s" % (
        short(module_name), version_int(document), short(rule_name), short(old_name), current,
    ))


def main():
    global _OUT
    assert os.path.isdir(os.path.join(ROOT, "lib", "research", "corpus")), "run from the worktree root"
    _OUT = open(OUT_PATH, "w", newline="\n", encoding="utf-8")
    client = ReadOnlyCounting(store._default_client())
    try:
        plan = [
            ("continuation", continuation.TABLE, continuation.METHOD_VERSION,
             list_partitions(client, continuation.TABLE), continuation_wanted(client)),
            ("sector_template", sector_template.TABLE, sector_template.METHOD_VERSION,
             list_partitions(client, sector_template.TABLE), sector_wanted(client)),
            ("fund_form", fund_form.TABLE, fund_form.METHOD_VERSION,
             list_partitions(client, fund_form.TABLE), fund_wanted(client)),
            ("typecast", typecast.TABLE, typecast.METHOD_VERSION,
             [typecast.PARTITION], typecast_wanted(client)),
        ]
        for name, table, _mv, partitions, _w in plan:
            emit("PARTITIONS %s n=%d" % (name, len(partitions)))
        for extra in list_partitions(client, typecast.TABLE):
            if extra != typecast.PARTITION:
                emit("NOT-READ-BY-SUBSTRATE typecast %s" % extra)

        totals = {"fallback_partitions": 0, "module_equals_rule": 0, "moved_from_old": 0}
        for name, table, method_version, partitions, wanted_of in plan:
            census_table(client, name, table, method_version, partitions, wanted_of, totals)

        control_difference()
        emit("CENSUS-FALLBACK-AFTER fallback_partitions=%d module_equals_rule=%d moved_from_old=%d gets=%d bytes=%d" % (
            totals["fallback_partitions"], totals["module_equals_rule"], totals["moved_from_old"],
            client.requests, client.bytes,
        ))
    except BudgetExceeded:
        emit("BUDGET-EXCEEDED gets=%d bytes=%d" % (client.requests, client.bytes))
        sys.exit(3)
    finally:
        _OUT.close()


if __name__ == "__main__":
    main()
