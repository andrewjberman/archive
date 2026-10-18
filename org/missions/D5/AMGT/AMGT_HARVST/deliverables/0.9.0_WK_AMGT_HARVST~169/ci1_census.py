"""ci1_census.py -- AMGT_HARVST HVST-ci-1 (round 94, row W165-S3). READ-ONLY.

For every stored partition that lib/research/corpus/substrate.py reads through
_pick_stored (FOUR tables: continuation, sector_template, fund_form, typecast):
list the partition, read every object, compute `wanted` with the SAME producer
call substrate.py makes for that table (substrate.py lines 214, 248, 268, 281),
count the objects whose `inputs` equal `wanted`. A partition with NO matching
object is the substrate's fallback case; for it this census prints the
key-order pick OLD (sorted(docs)[-1], reimplemented here) and the RULE (highest
method_version integer, then the later LastModified, the key breaking a tie),
and whether they name different objects (moves).

The census never imports _select_stored or any changed picker: OLD and RULE are
written in this file. Output is written by this script to ci1_census.out with
newline="\\n" (stdout carries the same lines).

Budget (round-94 preflight): 8000 requests and 1 GiB; the run stops at the
budget and prints BUDGET-EXCEEDED.

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
from lib.research.corpus import typecast  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

OUT_PATH = os.path.join(
    ROOT, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~169", "ci1_census.out",
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
    """Forwards the read operations only (get_object, head_object, list_objects_v2 via
    paginator); counts requests and bytes; refuses every other S3 operation."""

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


def old_pick(items):
    """OLD: the substrate's key-order fallback, reimplemented here: sorted(docs)[-1]."""
    key = sorted(it[0] for it in items)[-1]
    return next(it for it in items if it[0] == key)


def rule_pick(items):
    """RULE: highest method_version integer, then the later LastModified (a missing value never
    outranks a present one), then the greater key on an exact tie."""
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


def census_partition(client, name, table, partition, wanted_of, emit_fallback=True):
    """One partition: list, read every object, compute wanted, count input matches, fallback lines."""
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
    record = {"objects": len(items), "matches": 0, "fallback": False, "moves": False}
    if not items:
        return record
    wanted = wanted_of(partition, docs)
    matches = [it for it in items if it[2].get("inputs") == wanted]
    record["matches"] = len(matches)
    if matches:
        return record
    record["fallback"] = True
    old = old_pick(items)
    rule = rule_pick(items)
    record["moves"] = old[0] != rule[0]
    if emit_fallback:
        methods = ",".join(str(version_int(it[2])) for it in sorted(items, key=lambda i: i[0]))
        emit("FALLBACK %s %s objects=%d methods=%s old=%s/%d rule=%s/%d moves=%s" % (
            name, partition, len(items), methods,
            short(old[0]), version_int(old[2]),
            short(rule[0]), version_int(rule[2]),
            "yes" if record["moves"] else "no",
        ))
    return record


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


def census_table(client, name, table, partitions, wanted_of):
    stats = {"partitions": 0, "objects": 0, "input_match": 0, "no_input_match": 0, "moves": 0}
    for partition in partitions:
        rec = census_partition(client, name, table, partition, wanted_of)
        stats["partitions"] += 1
        stats["objects"] += rec["objects"]
        if rec["objects"] == 0:
            emit("EMPTY %s %s" % (name, partition))
            stats["no_input_match"] += 1
        elif rec["matches"] > 0:
            stats["input_match"] += 1
        else:
            stats["no_input_match"] += 1
        if rec["moves"]:
            stats["moves"] += 1
    emit("TABLE %s partitions=%d objects=%d input_match=%d no_input_match=%d" % (
        name, stats["partitions"], stats["objects"], stats["input_match"], stats["no_input_match"],
    ))
    return stats


def utc(hour):
    return datetime(2026, 10, 1, hour, tzinfo=timezone.utc)


def negative_control():
    def doc(version):
        return {
            "method_version": "amgt-corpus-continuation/%d" % version,
            "inputs": [{"key": "synthetic/stored.json", "sha256": "0" * 64}],
        }

    items = [
        ("98a4883c1b099e6b.json", utc(1), doc(1)),
        ("f174f7092a2d358e.json", utc(2), doc(2)),
        ("28404359eb0645c4.json", utc(3), doc(3)),
        ("4d837586380648bd.json", utc(4), doc(4)),
    ]
    wanted = [{"key": "synthetic/wanted.json", "sha256": "1" * 64}]
    if [it for it in items if it[2].get("inputs") == wanted]:
        emit("CONTROL-NEGATIVE-ERROR a synthetic object matched the synthetic wanted inputs")
        return
    old = old_pick(items)
    rule = rule_pick(items)
    emit("CONTROL-NEGATIVE synthetic old=%s/%d rule=%s/%d moves=%s" % (
        short(old[0]), version_int(old[2]), short(rule[0]), version_int(rule[2]),
        "yes" if old[0] != rule[0] else "no",
    ))


def main():
    global _OUT
    assert os.path.isdir(os.path.join(ROOT, "lib", "research", "corpus")), "run from the worktree root"
    _OUT = open(OUT_PATH, "w", newline="\n", encoding="utf-8")
    client = ReadOnlyCounting(store._default_client())
    try:
        plan = [
            ("continuation", continuation.TABLE, list_partitions(client, continuation.TABLE), continuation_wanted(client)),
            ("sector_template", sector_template.TABLE, list_partitions(client, sector_template.TABLE), sector_wanted(client)),
            ("fund_form", fund_form.TABLE, list_partitions(client, fund_form.TABLE), fund_wanted(client)),
            ("typecast", typecast.TABLE, [typecast.PARTITION], typecast_wanted(client)),
        ]
        for name, table, partitions, _w in plan:
            emit("PARTITIONS %s n=%d" % (name, len(partitions)))
        typecast_listed = list_partitions(client, typecast.TABLE)
        for extra in typecast_listed:
            if extra != typecast.PARTITION:
                emit("NOT-READ-BY-SUBSTRATE typecast %s" % extra)

        totals = {"tables": 0, "partitions": 0, "no_input_match": 0, "moves": 0}
        for name, table, partitions, wanted_of in plan:
            stats = census_table(client, name, table, partitions, wanted_of)
            totals["tables"] += 1
            totals["partitions"] += stats["partitions"]
            totals["no_input_match"] += stats["no_input_match"]
            totals["moves"] += stats["moves"]

        mnst = census_partition(
            client, "continuation", continuation.TABLE, crosswalk.security_key_partition("MNST_US_Equity"),
            continuation_wanted(client), emit_fallback=False,
        )
        emit("CONTROL-POSITIVE continuation MNST_US_Equity input_match=%s fallback=%s" % (
            "yes" if mnst["matches"] > 0 else "no",
            "yes" if mnst["fallback"] else "no",
        ))
        negative_control()
        emit("CENSUS-FALLBACK tables=%d partitions=%d no_input_match=%d moves=%d gets=%d bytes=%d" % (
            totals["tables"], totals["partitions"], totals["no_input_match"], totals["moves"],
            client.requests, client.bytes,
        ))
    except BudgetExceeded:
        emit("BUDGET-EXCEEDED gets=%d bytes=%d" % (client.requests, client.bytes))
        sys.exit(3)
    finally:
        _OUT.close()


if __name__ == "__main__":
    main()
