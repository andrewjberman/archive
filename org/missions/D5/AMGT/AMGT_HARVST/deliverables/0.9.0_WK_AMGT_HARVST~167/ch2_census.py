"""ch2_census.py -- AMGT_HARVST HVST-ch-2 (round 93, row D1-S49). READ-ONLY.

Two censuses, one run (foreground, unbuffered; stdout is written with LF endings):

    python -u org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~167/ch2_census.py > org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~167/ch2_census.out

E1 -- the drift census over every stored report line. Every silver research-report row (the newest per
(security_key, report_id), the two misfiled rows of typed.MISFILED_REPORTS excluded as typed.reports_for does)
whose fund_evidence carries a recommendation header: raw = that header's body; silver = fund_relation.classify
(row fund, row fund_evidence) with initiate and interest folded into candidate; gold = continuation._line_stance(raw).
A disagreement prints DRIFT. The census is run on the worktree's own modules (both read lib/research/corpus/line_words.py).

E2 -- the gold census, no write. For every security with a continuation partition, continuation's
_resolve_fund_and_position is run TWICE on the SAME fetched items (one read per security, through
_read_reports_with_bytes against ONE silver read): BASELINE = continuation.py at commit bec8a53981 (pinned
with git show, loaded as a second module, never HEAD); NEW = the worktree continuation.py. A security whose
fund_of_record or last_stated_position differs (value, key set, or absent against present) prints MOVED.
AT_CURRENT says whether the security's NEWEST stored continuation object (highest LastModified, then key)
is at continuation.METHOD_VERSION. Nothing is written; the wrapper refuses every operation except
get_object, head_object, list_objects_v2 and get_paginator.

Budget (issuer order, preflight comp-iam): 4000 requests and 800 MiB in all; the run aborts before exceeding
either. Client: lib.research.harvest.store._default_client().
"""

import importlib.util
import io
import json
import os
import subprocess
import sys

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

# LF endings on stdout regardless of the console (Windows text mode would write CRLF)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="backslashreplace",
                              newline="\n", line_buffering=True)

from botocore.exceptions import ClientError  # noqa: E402

from lib.research.corpus import continuation as cont  # noqa: E402
from lib.research.corpus import fund_relation  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import typed  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

BASELINE_REV = "bec8a53981"
CONT_PATH = "lib/research/corpus/continuation.py"
SCRATCH = os.path.join(ROOT, ".scratch", "ch2")
BUDGET_REQUESTS = 4000
BUDGET_BYTES = 800 * 1024 * 1024


class ReadOnlyCounting(object):
    """Forwards the four read operations only; counts requests and bytes; aborts before the budget is exceeded."""

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


def short(text, n):
    """The first n characters of text on one line (absent for None)."""
    if text is None:
        return "absent"
    return str(text)[:n].replace("\r", " ").replace("\n", " ").replace("\t", " ")


def folded(relation):
    """The drift fold: initiate and interest are candidate words in continuation._line_stance."""
    return "candidate" if relation in ("initiate", "interest") else relation


def field_text(field):
    """The value text of one resolved field: the position's `text`, else the value as JSON, else absent."""
    value = field.get("value")
    if value is None:
        return "absent"
    if isinstance(value, dict) and "text" in value:
        return str(value["text"])
    return json.dumps(value, sort_keys=True)


def field_stance(field):
    value = field.get("value")
    if isinstance(value, dict):
        return value.get("stance", "holding" if "text" in value else "none")
    return "none"


def load_baseline():
    """continuation.py at BASELINE_REV, loaded as a second module (pinned; never HEAD)."""
    proc = subprocess.run(["git", "show", BASELINE_REV + ":" + CONT_PATH], cwd=ROOT, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit("git show %s:%s rc=%d: %s" % (BASELINE_REV, CONT_PATH, proc.returncode,
                                                         proc.stderr.decode("utf-8", "replace")[:300]))
    os.makedirs(SCRATCH, exist_ok=True)
    path = os.path.join(SCRATCH, "continuation_%s.py" % BASELINE_REV)
    with open(path, "wb") as fh:
        fh.write(proc.stdout)
    spec = importlib.util.spec_from_file_location("continuation_baseline", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def e1_drift(kept):
    """E1: silver classify against gold _line_stance on every kept row with a recommendation header."""
    compared = 0
    drift = 0
    for row in sorted(kept, key=lambda r: (str(r.get("security_key")), str(r.get("report_id")))):
        evidence = row.get("fund_evidence")
        body = fund_relation._header_body(evidence or "")
        if body is None:
            continue
        compared += 1
        silver_rel = folded(fund_relation.classify(row.get("fund"), evidence))
        gold_rel = cont._line_stance(body)
        if silver_rel != gold_rel:
            drift += 1
            print("DRIFT %s %s silver=%s gold=%s raw=%s" % (row.get("security_key"), row.get("report_id"),
                                                           silver_rel, gold_rel, short(body, 70)))
    print("CENSUS-SHARED-DRIFT rows=%d drift=%d" % (compared, drift))


def main():
    base = load_baseline()
    client = ReadOnlyCounting(store._default_client())

    # the silver rows are read ONCE (store.silver_latest); typed.reports_for is pointed at that read so that
    # each security's items come from the same fetch the census compares (the rule of typed.reports_for, as it reads)
    latest = store.silver_latest(typed.SOURCE, typed.TABLE, typed.RECORD_KEY_FIELDS, client=client)
    excluded = {(e["security_key"], e["report_id"]) for e in typed.MISFILED_REPORTS}
    kept = []
    for ident, row in latest.items():
        if (row.get("security_key"), row.get("report_id")) in excluded:
            print("# EXCLUDED-MISFILED %s %s" % (row.get("security_key"), row.get("report_id")))
            continue
        kept.append(row)
    print("# DENOMINATOR silver_latest_rows=%d kept_reports=%d excluded_misfiled=%d"
          % (len(latest), len(kept), len(latest) - len(kept)))
    print("# METHOD before = continuation.py at %s (git show, second module); after = the worktree continuation.py"
          % BASELINE_REV)
    print("# METHOD E1 silver = fund_relation.classify(row fund, row fund_evidence), initiate/interest folded to candidate;"
          " gold = continuation._line_stance(header body)")

    e1_drift(kept)

    def _reports_for(security_key, client=None):
        rows = [r for r in kept if r.get("security_key") == security_key]
        return typed._order_reports(rows)

    typed.reports_for = _reports_for

    prefix = gold.table_prefix(cont.TABLE)
    partitions = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix,
                                                                 Delimiter="/"):
        for common in page.get("CommonPrefixes", []) or []:
            partitions.append(common["Prefix"])
    partitions = sorted(set(partitions))
    print("# PARTITIONS prefix=%s n=%d" % (prefix, len(partitions)))

    securities = []
    partition_of = {}
    for partition_prefix in partitions:
        segment = partition_prefix[len(prefix):].rstrip("/")
        if not segment.startswith("security_key="):
            print("# SKIP-NONSECURITY-PARTITION %s" % partition_prefix)
            continue
        security_key = crosswalk.security_key_from_slash_safe(segment[len("security_key="):])
        if crosswalk.security_key_partition(security_key) != segment:
            print("# SKIP-PARTITION-ROUNDTRIP-MISMATCH %s" % partition_prefix)
            continue
        securities.append(security_key)
        partition_of[security_key] = partition_prefix

    moved = []        # (security_key, [(field, before_text, after_text, before_stance, after_stance), ...])
    unreadable = 0
    fields_moved = 0
    for security_key in securities:
        try:
            items_raw = cont._read_reports_with_bytes(security_key, client=client)
        except (ClientError, KeyError, ValueError) as exc:
            unreadable += 1
            print("# UNREADABLE %s %s" % (security_key, short("%s: %s" % (type(exc).__name__, exc), 200)))
            continue
        items = [(row, doc) for row, _raw, doc, _rk in items_raw]

        before = base._resolve_fund_and_position(items)
        after = cont._resolve_fund_and_position(items)

        changed = []
        for name, idx in (("fund_of_record", 0), ("last_stated_position", 1)):
            b, a = before[idx], after[idx]
            if b != a:
                changed.append((name, short(field_text(b), 60), short(field_text(a), 60),
                                field_stance(b), field_stance(a)))
        if changed:
            moved.append((security_key, changed))
            fields_moved += len(changed)
            for name, bt, at, _bs, _as in changed:
                print("MOVED %s field=%s before=%s after=%s" % (security_key, name, bt, at))
            for name, _bt, _at, bs, asn in changed:
                if bs != asn:
                    print("# STANCE %s field=%s before=%s after=%s" % (security_key, name, bs, asn))

    def newest_stored(security_key):
        """The newest stored continuation object of this security: highest LastModified, then key."""
        objs = []
        for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET,
                                                                     Prefix=partition_of[security_key]):
            for obj in page.get("Contents", []) or []:
                objs.append((obj["Key"], obj.get("LastModified")))
        if not objs:
            return None, None
        key, _lm = max(objs, key=lambda o: (o[1].isoformat() if o[1] is not None else "", o[0]))
        doc = json.loads(gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client).decode("utf-8"))
        return key, doc.get("method_version")

    moved_at_current = 0
    for security_key, _changed in moved:
        key, version = newest_stored(security_key)
        at_current = version == cont.METHOD_VERSION
        if at_current:
            moved_at_current += 1
        print("# NEWEST %s object=%s method_version=%s" % (security_key, key, version))
        print("AT_CURRENT %s %s" % (security_key, "yes" if at_current else "no"))

    print("# UNREADABLE-SECURITIES %d" % unreadable)
    print("CENSUS-GOLD-MOVE securities=%d moved=%d fields_moved=%d moved_at_current=%d gets=%d bytes=%d"
          % (len(securities), len(moved), fields_moved, moved_at_current, client.requests, client.bytes))


if __name__ == "__main__":
    main()
