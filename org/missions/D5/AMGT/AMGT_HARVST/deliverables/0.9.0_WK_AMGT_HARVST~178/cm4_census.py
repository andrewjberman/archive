"""cm4_census.py -- AMGT_HARVST HVST-cm-4 (round 98, CTO round-97 analysis item 4). READ-ONLY, WRITES NOTHING.

Part A: for EVERY name with a continuation partition (sorted by security key; the listing decides the count):
  SERVED = the object under amgt/harvest/gold/research_dossier/security_key=<partition>/ that the gateway serves:
           the gateway's _pick_dossier rule (infra/aws/ec2/opal-gateway/app/harvest_research.py, def _pick_dossier at
           lines 270-287 at this HEAD), fed the _list_json rows of the CANONICAL partition only, as_of=None (greatest
           stamp). The partition is crosswalk.security_key_partition(key), never a hand-typed encoding.
  BUILT  = dossier.build(security_key, client) IN MEMORY. This file contains no write call: dossier.write_one,
           gold_put and every put/delete/copy are absent; the Guarded client forwards only get_object, head_object,
           list_objects_v2 and its paginator, bucket opal-data-harvest only, and refuses every other operation by name.
Comparison: `fields` field by field over the union of the two key sets, parsed values (JSON round trip with sort_keys,
  then ==). as_of and inputs are compared separately; key order and whitespace never count.
Cause, decided from the inputs entries that differ (kind by key prefix), never from the field name:
  inputs_continuation, inputs_fund_form, model_block, sector_template, typecast, picked_report (comma-joined when several
  differ). `other` when a field moves and NO input entry differs (every `other` is a surprise row). `none` when no field
  moves. The as_of stamp is never a cause: it differs for every name and is printed on the NAME line.
Refresh rule (order section 1b, the refresh's own skip rule): ALLOWED moves_within_allowed=yes iff every moved field is in
  {fund_form_ref, model_rows} AND every differing input kind is in {continuation, fund_form, model_block}; otherwise
  skip_reason names the offending fields and kinds. no-stored -> n/a; build error -> no (the refresh cannot build it).
Guard (CTO model-block guard, NEVER_WIDEN_CJ4 condition 1), the rule of cl3_census.py: for a name that moves model_rows,
  PASS needs the BUILD's own model-block record status SERVED, a built stamp later than the stored dossier's stamp, and a
  valued-row count not lower than the stored count; otherwise STOP. A name that does not move model_rows reads
  N/A-model_rows-unmoved, and its record status is printed on its GUARD line for the reader.
  The record is read by dossier._model_block_read on the SAME memoised client (the call build() makes; build() returns
  no record field).
Controls: CONTROL-POSITIVE (stored vs stored) and CONTROL-NEGATIVE (one planted field) on UNH_US_Equity, in --final.
Budget: 14000 requests and 1.8 GiB over ALL slices (the parts file's SLICE lines). A memo hit is not a request. The memo
  is per process (read-through, capped at 1 GiB), so each slice starts cold and is measured on its own.

Usage, from the worktree root (foreground, one slice per command):
  python -u <this file> --start S --stop E   one slice names[S:E]; appends to cm4_census.parts.out
  python -u <this file> --final              checks the parts file, runs the controls, writes cm4_census.out
"""

import argparse
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

from lib.research.corpus import continuation  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.corpus import fund_form  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import sector_template  # noqa: E402
from lib.research.corpus import team_sheet  # noqa: E402
from lib.research.corpus import typecast  # noqa: E402
from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS_PATH = os.path.join(HERE, "cm4_census.parts.out")
OUT_PATH = os.path.join(HERE, "cm4_census.out")

BUDGET_REQUESTS = 14000
BUDGET_BYTES = int(1.8 * 1024 ** 3)
GATEWAY_SUFFIXES = (".json", ".json.gz")  # harvest_research.py _list_json
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")  # harvest_research.py _AS_OF
MODEL_BLOCK_PREFIX = "derived/model_block/"  # scoped_amgt.MODEL_BLOCK_POOL_PREFIX
CONTROL_NAME = "UNH_US_Equity"
FIELD_MAP_BLOB = "3b2829c3aa7ce572bea37a10b9bce8879cf13a96"  # git blob of integrations/bloomberg/research/field_map.json at HEAD
ALLOWED_FIELDS = frozenset(("fund_form_ref", "model_rows"))
ALLOWED_KINDS = frozenset(("continuation", "fund_form", "model_block"))
ABSENT = object()
CACHE_CAP_BYTES = 1024 ** 3

_SLICE_RE = re.compile(r"^SLICE start=(\d+) stop=(\d+) gets=(\d+) bytes=(\d+)$")
_CAUSE_RE = re.compile(r" cause=(\S+)")


class BudgetExceeded(Exception):
    pass


class Guarded(object):
    """Forwards the four read operations on the harvest bucket only; counts FETCHED requests and bytes against a budget.
    A repeated identical read inside the same process is answered from a read-through memo (a memo hit is not a request)."""

    def __init__(self, client, max_requests, max_bytes):
        self._client = client
        self.requests = 0
        self.bytes = 0
        self.hits = 0
        self.max_requests = max_requests
        self.max_bytes = max_bytes
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
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))

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
            raise BudgetExceeded("requests=%d bytes=%d" % (self.requests, self.bytes))
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
    """One output line: printed now and kept for the parts or output file. ASCII only."""
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


def field_map_line():
    """The field map team_sheet reads must be the HEAD blob (verified by its git blob id)."""
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


def list_partition_prefixes(client, prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(
        Bucket=gold.HARVEST_BUCKET, Prefix=prefix, Delimiter="/"
    ):
        for common in page.get("CommonPrefixes", []) or []:
            out.append(common["Prefix"])
    return sorted(set(out))


def security_names(client, lines):
    """The security keys with a continuation partition, sorted by key."""
    prefix = gold.table_prefix(continuation.TABLE)
    names = []
    for partition_prefix in list_partition_prefixes(client, prefix):
        segment = partition_prefix[len(prefix):].rstrip("/")
        if not segment.startswith("security_key="):
            emit(lines, "SKIP-NONSECURITY-PARTITION %s" % partition_prefix)
            continue
        security_key = crosswalk.security_key_from_slash_safe(segment[len("security_key="):])
        if crosswalk.security_key_partition(security_key) != segment:
            emit(lines, "SKIP-PARTITION-ROUNDTRIP-MISMATCH %s" % partition_prefix)
            continue
        names.append(security_key)
    return sorted(names)


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


def census_one(client, security_key, out):
    """Appends this name's lines to `out` (a local list); the caller keeps them only when the name completes."""
    key, doc, dup = served_of(client, security_key)
    if doc is None:
        emit(out, "NO-STORED-DOSSIER %s dossier_objects_listed=%d" % (security_key, dup["objects"]))
        emit(out, "NAME %s served=none/- as_of_served=none as_of_built=none fields_moved=none list=none "
                  "input_kinds_differ=none" % security_key)
        emit(out, "ALLOWED %s moves_within_allowed=n/a skip_reason=no-stored-dossier" % security_key)
        return
    served_token = "%s/%d" % (key.rsplit("/", 1)[-1], version_int(doc))
    try:
        built = dossier.build(security_key, client=client)
        built_fields = norm(built.get("fields") or {})
        served_fields = norm(doc.get("fields") or {})
        built_inputs = norm(built.get("inputs") or [])
        served_inputs = norm(doc.get("inputs") or [])
    except BudgetExceeded:
        raise
    except Exception as exc:  # recorded, never silently dropped
        emit(out, "BUILD-ERROR %s %s: %s" % (security_key, type(exc).__name__, str(exc)[:160]))
        emit(out, "NAME %s served=%s as_of_served=%s as_of_built=none fields_moved=build-error list=none "
                  "input_kinds_differ=none" % (security_key, served_token, doc.get("as_of")))
        emit(out, "ALLOWED %s moves_within_allowed=no skip_reason=build-error" % security_key)
        return
    changed = field_diffs(built_fields, served_fields)
    kinds, only_b, only_s = input_difference(built_inputs, served_inputs)
    cause = cause_of(kinds) if changed else "none"
    emit(out, "NAME %s served=%s as_of_served=%s as_of_built=%s fields_moved=%d list=%s input_kinds_differ=%s"
         % (security_key, served_token, doc.get("as_of"), built.get("as_of"), len(changed),
            ",".join(changed) or "none", ",".join(kinds) or "none"))
    emit(out, "INPUTS %s served_object=%s dossier_objects_listed=%d distinct_as_of=%d dropped=%d "
              "inputs_list_equal=%s only_built=%d only_served=%d cause=%s"
         % (security_key, key, dup["objects"], dup["distinct_as_of"], dup["dropped"],
            "yes" if built_inputs == served_inputs else "no", only_b, only_s, cause))
    for field in changed:
        emit(out, "DIFF %s %s cause=%s served=%s built=%s"
             % (security_key, field, cause, show(served_fields.get(field, ABSENT)),
                show(built_fields.get(field, ABSENT))))

    # the refresh's own skip rule (order 1b): a field or an input kind outside the allowed sets skips the name
    bad = [f for f in changed if f not in ALLOWED_FIELDS] + [k for k in kinds if k not in ALLOWED_KINDS]
    emit(out, "ALLOWED %s moves_within_allowed=%s skip_reason=%s"
         % (security_key, "no" if bad else "yes", ",".join(bad) or "none"))

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
    emit(out, "MODEL-BLOCK %s stored=%s built=%s" % (security_key, stored_key or "none", built_key or "none"))
    emit(out, "GUARD %s model_block_status=%s built_stamp=%s stored_stamp=%s valued_rows_built=%d valued_rows_stored=%d "
              "verdict=%s" % (security_key, status, built_stamp or "none", stored_stamp or "none", valued_built,
                              valued_stored, verdict))


def run_slice(start, stop):
    parts = read_parts()
    slices = recorded_slices(parts)
    for s0, s1, _g, _b in slices:
        if start < s1 and s0 < stop:
            print("SLICE-REFUSED start=%d stop=%d overlaps recorded start=%d stop=%d" % (start, stop, s0, s1))
            return 2
    used_gets = sum(g for _s0, _s1, g, _b in slices)
    used_bytes = sum(b for _s0, _s1, _g, b in slices)
    client = Guarded(store._default_client(), BUDGET_REQUESTS - used_gets, BUDGET_BYTES - used_bytes)
    lines = []
    emit(lines, "SLICE-BUDGET-BEFORE used_gets=%d used_bytes=%d" % (used_gets, used_bytes))
    emit(lines, field_map_line())
    names = security_names(client, lines)
    emit(lines, "SLICE-RANGE names_total=%d start=%d stop=%d first=%s last=%s"
         % (len(names), start, stop, names[start] if start < len(names) else "none",
            names[stop - 1] if 0 < stop <= len(names) else "none"))
    try:
        for security_key in names[start:stop]:
            g0, b0 = client.requests, client.bytes
            local = []
            census_one(client, security_key, local)
            lines.extend(local)  # a name is recorded only when it completes
            emit(lines, "COST %s gets=%d bytes=%d" % (security_key, client.requests - g0, client.bytes - b0))
    except BudgetExceeded as exc:
        emit(lines, "BUDGET-EXCEEDED gets=%d bytes=%d (%s) -- slice stopped; the name in progress is not recorded"
             % (client.requests, client.bytes, exc))
    emit(lines, "SLICE-CACHE start=%d stop=%d memo_hits=%d memo_bytes=%d" % (start, stop, client.hits, client._memo_bytes))
    emit(lines, "SLICE start=%d stop=%d gets=%d bytes=%d" % (start, stop, client.requests, client.bytes))
    with open(PARTS_PATH, "a", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(line + "\n")
    return 0


def read_parts():
    if not os.path.exists(PARTS_PATH):
        return []
    with open(PARTS_PATH, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def recorded_slices(parts):
    out = []
    for line in parts:
        m = _SLICE_RE.match(line)
        if m:
            out.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    return out


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


def token(line, prefix):
    for part in line.split():
        if part.startswith(prefix):
            return part[len(prefix):]
    return None


def run_final():
    parts = read_parts()
    slices = recorded_slices(parts)
    used_gets = sum(g for _s0, _s1, g, _b in slices)
    used_bytes = sum(b for _s0, _s1, _g, b in slices)
    client = Guarded(store._default_client(), BUDGET_REQUESTS - used_gets, BUDGET_BYTES - used_bytes)
    header = []
    names_lines = []
    names = security_names(client, names_lines)
    emit(header, "CENSUS-HEADER HVST-cm-4 dossier census (round 98); SERVED = gateway pick (_pick_dossier, as_of=None,"
                 " canonical partition); BUILT = dossier.build in memory; fields by parsed value; cause from the differing"
                 " input entries; refresh skip rule = fields in {fund_form_ref, model_rows} and input kinds in"
                 " {continuation, fund_form, model_block}; guard = cl3 rule (CTO NEVER_WIDEN_CJ4 condition 1)")
    emit(header, "CENSUS-HEADER bucket=%s budget_requests=%d budget_bytes=%d slices_recorded=%d"
         % (gold.HARVEST_BUCKET, BUDGET_REQUESTS, BUDGET_BYTES, len(slices)))
    emit(header, "CENSUS-HEADER memo: per process, read-through, cap 1 GiB; a slice starts cold; COST lines are"
                 " order-dependent within a slice")
    emit(header, field_map_line())
    for line in names_lines:
        emit(header, line)

    name_rows = [line for line in parts if line.startswith("NAME ")]
    allowed_rows = [line for line in parts if line.startswith("ALLOWED ")]
    seen = Counter(line.split()[1] for line in name_rows)
    seen_allowed = Counter(line.split()[1] for line in allowed_rows)
    missing = [n for n in names if seen[n] == 0]
    duplicate = sorted(n for n in seen if seen[n] > 1)
    extra = sorted(n for n in seen if n not in set(names))
    missing_allowed = [n for n in names if seen_allowed[n] == 0]
    dup_allowed = sorted(n for n in seen_allowed if seen_allowed[n] > 1)
    if missing or duplicate or extra or missing_allowed or dup_allowed:
        print("PARTS-GAP missing=%s duplicate=%s extra=%s missing_allowed=%s duplicate_allowed=%s"
              % (",".join(missing) or "none", ",".join(duplicate) or "none", ",".join(extra) or "none",
                 ",".join(missing_allowed) or "none", ",".join(dup_allowed) or "none"))
        return 1
    budget_marks = [ln for ln in parts if ln.startswith("BUDGET-EXCEEDED")]
    if budget_marks:
        print("BUDGET-EXCEEDED gets=%d bytes=%d" % (used_gets, used_bytes))
        return 1

    rows = []
    for line in name_rows:
        rows.append({"name": line.split()[1], "served": token(line, "served="),
                     "moved": token(line, "fields_moved="), "list": token(line, "list="),
                     "kinds": token(line, "input_kinds_differ=")})
    no_stored = sum(1 for r in rows if r["served"] == "none/-")
    build_errors = sum(1 for r in rows if r["moved"] == "build-error")
    numeric = [(r["name"], int(r["moved"])) for r in rows if (r["moved"] or "").isdigit()]
    unchanged = sum(1 for _n, m in numeric if m == 0)
    moved_names = sum(1 for _n, m in numeric if m > 0)
    fields_moved = sum(m for _n, m in numeric)
    cause_model_block_only = 0
    for r in rows:
        if (r["moved"] or "").isdigit() and int(r["moved"]) > 0 and r["list"] == "model_rows" and r["kinds"] == "model_block":
            cause_model_block_only += 1
    cause_other = 0
    cause_tally = Counter()
    for line in parts:
        if line.startswith("DIFF "):
            m = _CAUSE_RE.search(line)
            if m is not None:
                cause_tally[m.group(1)] += 1
                if m.group(1) == "other":
                    cause_other += 1
    skip_names = sum(1 for line in allowed_rows if token(line, "moves_within_allowed=") == "no")
    guard_lines = [line for line in parts if line.startswith("GUARD ")]
    guard_pass = sum(1 for line in guard_lines if line.rsplit("verdict=", 1)[-1] == "PASS")
    guard_stop = sum(1 for line in guard_lines if line.rsplit("verdict=", 1)[-1] == "STOP")
    guard_status_not_served_unmoved = sum(
        1 for line in guard_lines
        if line.rsplit("verdict=", 1)[-1] == "N/A-model_rows-unmoved" and token(line, "model_block_status=") != "SERVED")
    gets = sum(g for _s0, _s1, g, _b in slices)
    nbytes = sum(b for _s0, _s1, _g, b in slices)

    controls_lines = []
    controls(client, controls_lines)
    emit(controls_lines, "CONTROL-READS final_gets=%d final_bytes=%d (not in the totals: the slices are the census)"
         % (client.requests, client.bytes))
    emit(controls_lines, "BUILD-ERRORS n=%d" % build_errors)
    emit(controls_lines, "CAUSE-TALLY (DIFF lines by cause token) " + " ".join(
        "%s=%d" % (k, v) for k, v in sorted(cause_tally.items())))
    emit(controls_lines, "GUARD-UNMOVED-NOT-SERVED n=%d (names not moving model_rows whose build record is not SERVED)"
         % guard_status_not_served_unmoved)
    final = ("CENSUS-DOSSIER-MOVE-98 names=%d no_stored_dossier=%d unchanged=%d moved=%d fields_moved=%d "
             "cause_model_block_only=%d cause_other=%d skip_names=%d guard_pass=%d guard_stop=%d gets=%d bytes=%d"
             % (len(names), no_stored, unchanged, moved_names, fields_moved, cause_model_block_only, cause_other,
                skip_names, guard_pass, guard_stop, gets, nbytes))
    all_lines = header + parts + controls_lines + [final]
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in all_lines:
            fh.write(line + "\n")
    print(final, flush=True)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="HVST-cm-4 dossier no-write census")
    ap.add_argument("--start", type=int)
    ap.add_argument("--stop", type=int)
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args(argv)
    if pool_reader.POOL_BUCKET != gold.HARVEST_BUCKET:
        raise SystemExit("model-block pool bucket %r is not the harvest bucket; the census refuses" % pool_reader.POOL_BUCKET)
    if args.final:
        return run_final()
    if args.start is None or args.stop is None or args.stop <= args.start:
        ap.error("a slice needs --start S --stop E with E > S")
    return run_slice(args.start, args.stop)


if __name__ == "__main__":
    sys.exit(main())
