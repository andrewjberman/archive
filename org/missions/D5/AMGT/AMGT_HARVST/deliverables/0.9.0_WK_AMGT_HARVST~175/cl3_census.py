"""cl3_census.py -- AMGT_HARVST HVST-cl-3 (round 97, CTO round-96 analysis item 2). READ-ONLY, WRITES NOTHING.

Names: BP/_LN_Equity and NG/_LN_Equity (counted, names=2); UNH_US_Equity is the control (not counted).
  SERVED = the object under amgt/harvest/gold/research_dossier/security_key=<partition>/ that the gateway serves:
           the gateway's _pick_dossier rule (infra/aws/ec2/opal-gateway/app/harvest_research.py, def _pick_dossier at
           lines 270-287 at this HEAD; the order's "lines 239-255" is stale and names MISFILED_REPORTS), fed the
           _list_json rows of the CANONICAL partition only (harvest_research.py line 352), as_of=None (greatest stamp).
           The partition is crosswalk.security_key_partition(key), never a hand-typed encoding.
  BUILT  = dossier.build(security_key, client) IN MEMORY. dossier.write_one, gold_put and every write are never called;
           the Guarded client forwards only get_object, head_object, list_objects_v2 and its paginator, bucket
           opal-data-harvest only, and refuses every other operation by name.
Comparison: `fields` FIELD BY FIELD over the union of the two key sets, parsed values (JSON round trip with sort_keys,
then ==). as_of and inputs are compared separately; key order and whitespace never count.
Cause: decided from the inputs entries that differ (kind by key prefix), never from the field name:
  inputs_continuation, inputs_fund_form, model_block, sector_template, typecast, picked_report (a comma-joined set when
  several kinds differ). `other` when a field moves and NO input kind differs (every `other` is a surprise row).
  The as_of stamp is never a cause token: it is printed on the NAME line.
Guard (order section 1d, CTO model-block guard): per name that moves model_rows, PASS needs the build's model-block
  record status SERVED, a built stamp later than the stored dossier's stamp, and a valued-row count (figure.value not
  None) not lower than the stored count. The record is read by dossier._model_block_read on the SAME memoised client,
  the call dossier.build() itself makes (build() returns no record field; this is printed as GUARD-NOTE).
Budget: 6000 requests and 700 MiB (memo hits are not requests). Any budget breach prints BUDGET-EXCEEDED and no CENSUS line.

Usage, from the worktree root (foreground, one process):
  python -u <this file>
Writes cl3_census.out beside this file with newline="\\n" and echoes every line to stdout.
"""

import copy
import gzip
import hashlib
import io
import json
import os
import re
import sys
from collections import Counter
from datetime import timezone
from pathlib import Path

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import dossier  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import team_sheet  # noqa: E402
from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402
from lib.research.corpus import continuation, fund_form, sector_template, typecast  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cl3_census.out")
NAMES = ("BP/_LN_Equity", "NG/_LN_Equity")
CONTROL_NAME = "UNH_US_Equity"
BUDGET_REQUESTS = 6000
BUDGET_BYTES = 700 * 1024 ** 2
FIELD_MAP_BLOB = "3b2829c3aa7ce572bea37a10b9bce8879cf13a96"  # git blob of integrations/bloomberg/research/field_map.json at HEAD
GATEWAY_SUFFIXES = (".json", ".json.gz")  # harvest_research.py _list_json
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")  # harvest_research.py _AS_OF
MODEL_BLOCK_PREFIX = "derived/model_block/"  # scoped_amgt.MODEL_BLOCK_POOL_PREFIX
ABSENT = object()
CACHE_CAP_BYTES = 1024 ** 3


class BudgetExceeded(Exception):
    pass


class Guarded(object):
    """Forwards the four read operations on the harvest bucket only; counts FETCHED requests and bytes against the
    budget. A repeated identical read in this process is answered from a read-through memo (a memo hit is not a request)."""

    def __init__(self, client, max_requests, max_bytes):
        self._client = client
        self.requests = 0
        self.bytes = 0
        self.hits = 0
        self.max_requests = max_requests
        self.max_bytes = max_bytes
        self.exceeded = None
        self._memo = {}
        self._memo_bytes = 0

    def _bucket_ok(self, kwargs):
        if kwargs.get("Bucket") != gold.HARVEST_BUCKET:
            raise RuntimeError("census reads %s only; a call named bucket %r" % (gold.HARVEST_BUCKET, kwargs.get("Bucket")))

    def _memo_key(self, op, kwargs):
        return (op,) + tuple(sorted((k, repr(v)) for k, v in kwargs.items()))

    def _spend(self):
        self.requests += 1
        if self.requests > self.max_requests or self.bytes > self.max_bytes:
            self.exceeded = "requests=%d bytes=%d" % (self.requests, self.bytes)
            raise BudgetExceeded(self.exceeded)

    def get_object(self, **kwargs):
        self._bucket_ok(kwargs)
        key = self._memo_key("get", kwargs)
        if key in self._memo:
            self.hits += 1
            return {"Body": io.BytesIO(self._memo[key])}
        self._spend()
        resp = self._client.get_object(**kwargs)
        data = resp["Body"].read()
        self.bytes += len(data)
        if self.bytes > self.max_bytes:
            self.exceeded = "requests=%d bytes=%d" % (self.requests, self.bytes)
            raise BudgetExceeded(self.exceeded)
        if self._memo_bytes + len(data) <= CACHE_CAP_BYTES:
            self._memo[key] = data
            self._memo_bytes += len(data)
        return {"Body": io.BytesIO(data)}

    def head_object(self, **kwargs):
        self._bucket_ok(kwargs)
        key = self._memo_key("head", kwargs)
        if key in self._memo:
            self.hits += 1
            return self._memo[key]
        self._spend()
        resp = self._client.head_object(**kwargs)
        self._memo[key] = resp
        return resp

    def list_objects_v2(self, **kwargs):
        self._bucket_ok(kwargs)
        key = self._memo_key("list", kwargs)
        if key in self._memo:
            self.hits += 1
            return self._memo[key]
        self._spend()
        resp = self._client.list_objects_v2(**kwargs)
        self._memo[key] = resp
        return resp

    def get_paginator(self, operation_name):
        if operation_name != "list_objects_v2":
            raise RuntimeError("census is READ-ONLY: refuses paginator %r" % operation_name)
        outer = self

        class _Paginator(object):
            def paginate(self, **kwargs):
                outer._bucket_ok(kwargs)
                key = outer._memo_key("paginate", kwargs)
                if key in outer._memo:
                    outer.hits += 1
                    for page in outer._memo[key]:
                        yield page
                    return
                pages = []
                for page in outer._client.get_paginator("list_objects_v2").paginate(**kwargs):
                    outer._spend()
                    pages.append(page)
                    yield page
                outer._memo[key] = pages

        return _Paginator()

    def __getattr__(self, name):
        raise RuntimeError("census is READ-ONLY: refuses S3 operation %r" % name)


def emit(lines, text):
    """One output line: printed now and kept for the output file. ASCII only."""
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def field_map_line():
    """The field map team_sheet reads must be the HEAD blob (the worktree copy is verified by its git blob id)."""
    path = Path(str(team_sheet._FIELD_MAP_PATH))
    data = path.read_bytes()
    git_blob = hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()
    if git_blob != FIELD_MAP_BLOB:
        raise SystemExit("FIELD-MAP refused: %s git blob %s is not %s" % (path.name, git_blob, FIELD_MAP_BLOB))
    return "FIELD-MAP %s git_blob=%s verified=HEAD-blob" % (path.name, git_blob)


def norm(value):
    """Parsed-value form: the JSON round trip (sorted keys; tuples become lists)."""
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


def show(value):
    """First 70 characters of the parsed value's JSON text, or absent."""
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


def utc_text(value):
    if value is None:
        return None
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pick_dossier(rows, as_of):
    """COPY of harvest_research.py _pick_dossier (lines 270-287 at this HEAD), unchanged in logic."""
    by_stamp = {}
    for r in rows:
        m = _AS_OF.search(r["key"])
        if m is not None:
            by_stamp.setdefault(m.group(1), []).append(r)
    listed = sum(len(v) for v in by_stamp.values())
    dup = {"listed": listed, "distinct_as_of": len(by_stamp), "dropped": listed - len(by_stamp)}
    if not by_stamp:
        return None, None, dup
    stamp = (as_of if as_of in by_stamp else None) if as_of else max(by_stamp)
    if stamp is None:
        return None, None, dup
    newest = max(by_stamp[stamp], key=lambda r: (r["last_modified"] or "", r["key"]))
    return newest, stamp, dup


def version_int(document):
    value = document.get("method_version")
    if not isinstance(value, str):
        return -1
    try:
        return int(value.rsplit("/", 1)[1])
    except (IndexError, ValueError):
        return -1


def kind_of(key):
    """The module's own input family for one inputs entry, by key prefix."""
    if key.startswith(gold.table_prefix(continuation.TABLE)):
        return "continuation"
    if key.startswith(gold.table_prefix(fund_form.TABLE)):
        return "fund_form"
    if key.startswith(gold.table_prefix(sector_template.TABLE)):
        return "sector_template"
    if key.startswith(gold.table_prefix(typecast.TABLE)):
        return "typecast"
    if key.startswith(MODEL_BLOCK_PREFIX):
        return "model_block"
    return "picked_report"


def entry_text(entry):
    return json.dumps(entry, sort_keys=True, ensure_ascii=True)


def input_difference(built_inputs, served_inputs):
    """(sorted kinds of the entries that differ, count only in built, count only in served)."""
    b = Counter(entry_text(e) for e in built_inputs)
    s = Counter(entry_text(e) for e in served_inputs)
    only_b = b - s
    only_s = s - b
    kinds = set()
    for text in list(only_b) + list(only_s):
        entry = json.loads(text)
        kinds.add(kind_of(str(entry.get("key"))))
    return sorted(kinds), sum(only_b.values()), sum(only_s.values())


def cause_of(kinds):
    """Cause token(s) from the differing input kinds. Empty kinds -> `other` (the only unexplained cause)."""
    if not kinds:
        return "other"
    tokens = set()
    for kind in kinds:
        if kind == "continuation":
            tokens.add("inputs_continuation")
        elif kind == "fund_form":
            tokens.add("inputs_fund_form")
        else:
            tokens.add(kind)
    return ",".join(sorted(tokens))


def dossier_prefix(security_key):
    """The stored partition of the name (slash-safe, the writer's form): crosswalk.security_key_partition."""
    return gold.table_prefix(dossier.TABLE) + crosswalk.security_key_partition(security_key) + "/"


def served_of(client, security_key):
    """(served object key or None, served document or None, dup counts): the gateway's pick, read once."""
    rows = []
    for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=gold.HARVEST_BUCKET, Prefix=dossier_prefix(security_key)
    ):
        for obj in page.get("Contents", []) or []:
            rows.append({"key": obj["Key"], "last_modified": utc_text(obj.get("LastModified"))})
    listed = [r for r in rows if r["key"].endswith(GATEWAY_SUFFIXES)]
    picked, _chosen, dup = pick_dossier(listed, None)
    dup = dict(dup)
    dup["objects"] = len(rows)
    if picked is None:
        return None, None, dup
    uri = "s3://%s/%s" % (gold.HARVEST_BUCKET, picked["key"])
    raw = gold.gold_get(uri, client=client)
    if picked["key"].endswith(".gz"):
        raw = gzip.decompress(raw)
    return picked["key"], json.loads(raw.decode("utf-8")), dup


def record_of(client, security_key):
    """(block, record): the build's own model-block read (dossier._model_block_read, the call build() makes)."""
    try:
        return dossier._model_block_read(security_key, client)
    except BudgetExceeded:
        raise
    except Exception as exc:  # recorded as NOT_EXPOSED, never silently dropped
        return None, {"status": "NOT_EXPOSED", "object_key": None,
                      "reason": "%s: %s" % (type(exc).__name__, str(exc)[:160])}


def valued_rows(model_rows):
    """Count of model_rows entries whose figure carries a non-null value (parsed form)."""
    if not isinstance(model_rows, list):
        return 0
    return sum(1 for r in model_rows
               if isinstance(r, dict) and isinstance(r.get("figure"), dict) and r["figure"].get("value") is not None)


def guard_verdict(moved_model_rows, status, built_stamp, stored_stamp, valued_built, valued_stored):
    if not moved_model_rows:
        return "N/A-model_rows-unmoved"
    later = built_stamp is not None and (stored_stamp is None or built_stamp > stored_stamp)
    ok = status == "SERVED" and later and valued_built >= valued_stored
    return "PASS" if ok else "STOP"


def census_name(client, security_key, lines, results):
    key, doc, dup = served_of(client, security_key)
    if doc is None:
        emit(lines, "NO-STORED-DOSSIER %s dossier_objects_listed=%d" % (security_key, dup["objects"]))
        emit(lines, "NAME %s served=none/- as_of_served=none as_of_built=none fields_moved=none list=none "
                    "input_kinds_differ=none" % security_key)
        results.append({"name": security_key, "no_stored": True, "moved": None, "causes": [], "guard": "N/A-no-stored"})
        return
    try:
        built = dossier.build(security_key, client=client)
    except BudgetExceeded:
        raise
    except Exception as exc:  # recorded, never silently dropped
        emit(lines, "BUILD-ERROR %s %s: %s" % (security_key, type(exc).__name__, str(exc)[:160]))
        emit(lines, "NAME %s served=%s/%d as_of_served=%s as_of_built=none fields_moved=build-error list=none "
                    "input_kinds_differ=none" % (security_key, key.rsplit("/", 1)[-1], version_int(doc), doc.get("as_of")))
        results.append({"name": security_key, "no_stored": False, "moved": None, "causes": [], "guard": "N/A-build-error"})
        return
    built_fields = norm(built.get("fields") or {})
    served_fields = norm(doc.get("fields") or {})
    built_inputs = norm(built.get("inputs") or [])
    served_inputs = norm(doc.get("inputs") or [])
    changed = field_diffs(built_fields, served_fields)
    kinds, only_b, only_s = input_difference(built_inputs, served_inputs)
    cause = cause_of(kinds)
    emit(lines, "NAME %s served=%s/%d as_of_served=%s as_of_built=%s fields_moved=%d list=%s input_kinds_differ=%s"
         % (security_key, key.rsplit("/", 1)[-1], version_int(doc), doc.get("as_of"), built.get("as_of"),
            len(changed), ",".join(changed) or "none", ",".join(kinds) or "none"))
    emit(lines, "INPUTS %s served_object=%s dossier_objects_listed=%d distinct_as_of=%d dropped=%d "
                "inputs_list_equal=%s only_built=%d only_served=%d cause=%s"
         % (security_key, key, dup["objects"], dup["distinct_as_of"], dup["dropped"],
            "yes" if built_inputs == served_inputs else "no", only_b, only_s, cause if changed else "none"))
    for field in changed:
        emit(lines, "DIFF %s %s cause=%s served=%s built=%s"
             % (security_key, field, cause, show(served_fields.get(field, ABSENT)),
                show(built_fields.get(field, ABSENT))))

    # the model-block guard, read from the BUILD's own record, never from the stored dossier
    block, record = record_of(client, security_key)
    status = record.get("status")
    built_key = record.get("object_key")
    built_stamp = dossier._model_block_stamp(security_key, built_key) if built_key else None
    stored_keys = [e.get("key") for e in (doc.get("inputs") or [])
                   if str(e.get("key", "")).startswith(MODEL_BLOCK_PREFIX)]
    stored_key = stored_keys[0] if stored_keys else None
    stored_stamp = dossier._model_block_stamp(security_key, stored_key) if stored_key else None
    valued_built = valued_rows(built_fields.get("model_rows"))
    valued_stored = valued_rows(served_fields.get("model_rows"))
    moved_mr = "model_rows" in changed
    verdict = guard_verdict(moved_mr, status, built_stamp, stored_stamp, valued_built, valued_stored)
    emit(lines, "MODEL-BLOCK %s stored=%s built=%s" % (security_key, stored_key or "none", built_key or "none"))
    emit(lines, "GUARD-NOTE %s build() returns no model-block record field; status read by dossier._model_block_read "
                "on the same memoised client (the call build() makes)" % security_key)
    emit(lines, "GUARD %s model_block_status=%s built_stamp=%s stored_stamp=%s valued_rows_built=%d valued_rows_stored=%d "
                "verdict=%s" % (security_key, status, built_stamp or "none", stored_stamp or "none", valued_built,
                                valued_stored, verdict))
    results.append({"name": security_key, "no_stored": False, "moved": len(changed),
                    "causes": [cause for _f in changed], "guard": verdict})


def controls(client, lines):
    key, doc, _dup = served_of(client, CONTROL_NAME)
    if doc is None:
        emit(lines, "CONTROL-ERROR no stored dossier for %s" % CONTROL_NAME)
        return
    served = norm(doc.get("fields") or {})
    same = copy.deepcopy(served)
    positive = field_diffs(same, served)
    emit(lines, "CONTROL-POSITIVE %s stored_vs_stored fields_moved=%d" % (CONTROL_NAME, len(positive)))
    planted = copy.deepcopy(served)
    field = sorted(planted)[0]
    planted[field] = {"census_negative_control": True}
    negative = field_diffs(planted, served)
    emit(lines, "CONTROL-NEGATIVE %s planted fields_moved=%d" % (CONTROL_NAME, len(negative)))
    emit(lines, "CONTROL-DETAIL %s served_object=%s planted_field=%s list=%s"
         % (CONTROL_NAME, key, field, ",".join(negative) or "none"))


def write_out(lines):
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(line + "\n")


def main():
    lines = []
    if POOL_BUCKET_CHECK() is False:
        raise SystemExit("model-block pool bucket is not the harvest bucket; the census refuses")
    client = Guarded(store._default_client(), BUDGET_REQUESTS, BUDGET_BYTES)
    emit(lines, "CENSUS-HEADER CL-3 (round 97) dossier census of BP/_LN_Equity and NG/_LN_Equity; control UNH_US_Equity; "
                "SERVED = gateway pick (_pick_dossier, as_of=None, canonical partition); BUILT = dossier.build in memory; "
                "fields by parsed value; cause from the differing input entries")
    emit(lines, "CENSUS-HEADER bucket=%s budget_requests=%d budget_bytes=%d" % (gold.HARVEST_BUCKET, BUDGET_REQUESTS, BUDGET_BYTES))
    emit(lines, field_map_line())
    results = []
    try:
        for security_key in NAMES:
            census_name(client, security_key, lines, results)
        controls(client, lines)
    except BudgetExceeded as exc:
        emit(lines, "BUDGET-EXCEEDED gets=%d bytes=%d (%s) -- census stopped at the budget; no CENSUS line is written"
             % (client.requests, client.bytes, exc))
        write_out(lines)
        return 1
    emit(lines, "CONTROL-READS final_gets=%d final_bytes=%d" % (client.requests, client.bytes))
    no_stored = sum(1 for r in results if r["no_stored"])
    unchanged = sum(1 for r in results if r["moved"] == 0)
    moved = sum(1 for r in results if r["moved"] is not None and r["moved"] > 0)
    fields_moved = sum(r["moved"] for r in results if r["moved"] is not None)
    cause_other = 0
    for line in lines:
        if line.startswith("DIFF ") and " cause=other " in line:
            cause_other += 1
    guard_pass = sum(1 for r in results if r["guard"] == "PASS")
    guard_stop = sum(1 for r in results if r["guard"] == "STOP")
    build_errors = sum(1 for r in results if r["guard"] == "N/A-build-error")
    emit(lines, "BUILD-ERRORS n=%d" % build_errors)
    final = ("CENSUS-DOSSIER-MOVE-97 names=%d no_stored_dossier=%d unchanged=%d moved=%d fields_moved=%d "
             "cause_other=%d guard_pass=%d guard_stop=%d gets=%d bytes=%d"
             % (len(NAMES), no_stored, unchanged, moved, fields_moved, cause_other, guard_pass, guard_stop,
                client.requests, client.bytes))
    emit(lines, final)
    write_out(lines)
    return 0


def POOL_BUCKET_CHECK():
    return pool_reader.POOL_BUCKET == gold.HARVEST_BUCKET


if __name__ == "__main__":
    sys.exit(main())
