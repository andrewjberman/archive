"""ci3_census.py -- AMGT_HARVST HVST-ci-3 (round 94, CTO round-93 analysis item 2). READ-ONLY.

For each security that holds a continuation partition under amgt/harvest/gold/research-continuation/ (names sorted by
security key; 95 expected):
  SERVED = the stored object under amgt/harvest/gold/research_dossier/security_key=<KEY>/ that the gateway serves:
           infra/aws/ec2/opal-gateway/app/harvest_research.py lines 239-255 (pick_dossier below, copied), fed the
           _list_json rows (lines 72-73: .json and .json.gz keys) with as_of=None (the greatest as_of stamp).
  BUILT  = dossier.build(security_key, client) IN MEMORY. dossier.write_one is never called from this file.
fields: compared FIELD BY FIELD over the union of the two key sets, by parsed value (JSON round trip with sort_keys,
then ==); key order and whitespace never count. as_of and inputs are compared separately.

Inputs entries are {"key", "sha256"} (dossier._build_inputs). The kind of an entry is the module's own input family,
classified by the key prefix: continuation, fund_form, sector_template, typecast (the four table prefixes), model_block
(derived/model_block/, scoped_amgt.py:204), and picked_report (the module's picked_report_ids: any other key).
Cause, decided from the entries that differ for the name (never from the field name):
  inputs_continuation / inputs_fund_form for those two kinds; other:<kind> for any other kind; `other` when NO entry
  differs (the as_of stamp is then the only other difference; it is named in the NAME line, not assigned as a cause).

The S3 client is wrapped: only get_object, head_object, list_objects_v2 and the list_objects_v2 paginator, bucket
opal-data-harvest only. Budget: 30000 requests and 3 GiB over ALL slices (the parts file's SLICE lines).

Usage, from the worktree root:
  python -u <this file> --start S --stop E   one slice names[S:E]; appends to ci3_census.parts.out
  python -u <this file> --final              checks the parts file, runs the controls, writes ci3_census.out
"""

import argparse
import copy
import gzip
import io
import json
import os
import re
import sys
from collections import Counter
from datetime import timezone

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import continuation  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.corpus import fund_form  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import sector_template  # noqa: E402
from lib.research.corpus import typecast  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PARTS_PATH = os.path.join(HERE, "ci3_census.parts.out")
OUT_PATH = os.path.join(HERE, "ci3_census.out")

BUDGET_REQUESTS = 30000
BUDGET_BYTES = 3 * 1024 ** 3
GATEWAY_SUFFIXES = (".json", ".json.gz")  # harvest_research.py:72-73 (_list_json)
P_DOSSIER = "amgt/harvest/gold/research_dossier/security_key=%s/"  # harvest_research.py:45
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")  # harvest_research.py:65
MODEL_BLOCK_PREFIX = "derived/model_block/"  # scoped_amgt.py:204 (MODEL_BLOCK_POOL_PREFIX)
EXPECTED_NAMES = 95
CONTROL_NAME = "UNH_US_Equity"
ABSENT = object()
# The worktree is a sparse checkout that excludes integrations/; team_sheet.py (the only reader, line 131) then raises
# FileNotFoundError, which dossier._team_sheet_field records as a reason. The field map is read from the tracked
# blob at HEAD instead (git show HEAD:integrations/bloomberg/research/field_map.json), verified by its git blob id.
FIELD_MAP_PIN = os.path.join(ROOT, ".scratch", "field_map.HEAD.json")
FIELD_MAP_BLOB = "3b2829c3aa7ce572bea37a10b9bce8879cf13a96"

_SLICE_RE = re.compile(r"^SLICE start=(\d+) stop=(\d+) gets=(\d+) bytes=(\d+)$")
_CAUSE_RE = re.compile(r" cause=(\S+) ")


class BudgetExceeded(Exception):
    pass


CACHE_CAP_BYTES = 1024 ** 3  # read-through memo of repeated reads within ONE process (a memo hit is not an S3 request)


class Guarded(object):
    """Forwards the four read operations on the harvest bucket only; counts FETCHED requests and bytes against a budget.
    A repeated identical read inside the same process is answered from a read-through memo and counted as a hit."""

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


def pin_field_map():
    """(text) the field-map source team_sheet reads, pinned to the HEAD blob when the worktree copy is absent."""
    import hashlib
    from pathlib import Path
    from lib.research.corpus import team_sheet
    default = Path(str(team_sheet._FIELD_MAP_PATH))
    if default.exists():
        return "FIELD-MAP worktree-copy-present path=%s" % default.name
    with open(FIELD_MAP_PIN, "rb") as fh:
        data = fh.read()
    git_blob = hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()
    if git_blob != FIELD_MAP_BLOB:
        raise SystemExit("FIELD-MAP pin refused: git blob %s is not %s" % (git_blob, FIELD_MAP_BLOB))
    team_sheet._FIELD_MAP_PATH = Path(FIELD_MAP_PIN)
    return ("FIELD-MAP worktree-copy-absent pinned=HEAD-blob git_blob=%s sha256=%s bytes=%d"
            % (git_blob, hashlib.sha256(data).hexdigest(), len(data)))


def emit(lines, text):
    """One output line: printed now, kept for the parts file or the output file. ASCII only."""
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    lines.append(safe)


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
    """harvest_read._utc: the gateway's LastModified text (second precision, UTC, Z)."""
    if value is None:
        return None
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pick_dossier(rows, as_of):
    """COPY of harvest_research.py _pick_dossier (lines 239-255), unchanged in logic."""
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
    """(kinds of the entries that differ, count only in built, count only in served), entries as parsed values."""
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
    if not kinds:
        return "other"
    tokens = set()
    for kind in kinds:
        if kind == "continuation":
            tokens.add("inputs_continuation")
        elif kind == "fund_form":
            tokens.add("inputs_fund_form")
        else:
            tokens.add("other:" + kind)
    return ",".join(sorted(tokens))


def is_other(cause):
    return cause == "other" or "other:" in cause


def dossier_prefix(security_key):
    """The stored partition of the name, slash-safe (C-SLASH-SAFE-KEY, the form the writer uses). For every key without
    a '/' this equals the gateway's literal P_DOSSIER % key; a key with '/' (BP/_LN_Equity) is found only this way."""
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


def census_one(client, security_key, lines):
    key, doc, dup = served_of(client, security_key)
    if doc is None:
        emit(lines, "NO-STORED-DOSSIER %s dossier_objects_listed=%d" % (security_key, dup["objects"]))
        emit(lines, "NAME %s served=none/- as_of_served=none as_of_built=none fields_moved=none list=none "
                    "input_kinds_differ=none" % security_key)
        return
    try:
        built = dossier.build(security_key, client=client)
        built_fields = norm(built.get("fields") or {})
        served_fields = norm(doc.get("fields") or {})
        built_inputs = norm(built.get("inputs") or [])
        served_inputs = norm(doc.get("inputs") or [])
    except BudgetExceeded:
        raise
    except Exception as exc:  # recorded, never silently dropped
        emit(lines, "BUILD-ERROR %s %s: %s" % (security_key, type(exc).__name__, str(exc)[:160]))
        emit(lines, "NAME %s served=%s/%d as_of_served=%s as_of_built=none fields_moved=build-error list=none "
                    "input_kinds_differ=none" % (security_key, key.rsplit("/", 1)[-1][:8], version_int(doc),
                                                  doc.get("as_of")))
        return
    changed = field_diffs(built_fields, served_fields)
    kinds, only_b, only_s = input_difference(built_inputs, served_inputs)
    cause = cause_of(kinds)
    emit(lines, "NAME %s served=%s/%d as_of_served=%s as_of_built=%s fields_moved=%d list=%s input_kinds_differ=%s"
         % (security_key, key.rsplit("/", 1)[-1][:8], version_int(doc), doc.get("as_of"), built.get("as_of"),
            len(changed), ",".join(changed) or "none", ",".join(kinds) or "none"))
    emit(lines, "INPUTS %s served_object=%s dossier_objects_listed=%d distinct_as_of=%d dropped=%d "
                "inputs_list_equal=%s only_built=%d only_served=%d cause=%s"
         % (security_key, key, dup["objects"], dup["distinct_as_of"], dup["dropped"],
            "yes" if built_inputs == served_inputs else "no", only_b, only_s, cause))
    for field in changed:
        emit(lines, "DIFF %s %s cause=%s served=%s built=%s"
             % (security_key, field, cause, show(served_fields.get(field, ABSENT)),
                show(built_fields.get(field, ABSENT))))


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
    emit(lines, pin_field_map())
    names = security_names(client, lines)
    emit(lines, "SLICE-RANGE names_total=%d start=%d stop=%d first=%s last=%s"
         % (len(names), start, stop, names[start] if start < len(names) else "none",
            names[stop - 1] if 0 < stop <= len(names) else "none"))
    try:
        for security_key in names[start:stop]:
            census_one(client, security_key, lines)
    except BudgetExceeded as exc:
        emit(lines, "BUDGET-EXCEEDED gets=%d bytes=%d (%s) -- slice stopped; the name in progress is not recorded"
             % (client.requests, client.bytes, exc))
    emit(lines, "SLICE-CACHE start=%d stop=%d memo_hits=%d memo_bytes=%d" % (start, stop, client.hits, client._memo_bytes))
    emit(lines, "SLICE start=%d stop=%d gets=%d bytes=%d" % (start, stop, client.requests, client.bytes))
    with open(PARTS_PATH, "a", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(line + "\n")
    return 0


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


def parse_name_line(line):
    """(security_key, served token, fields_moved token) from a NAME line."""
    parts = line.split()
    sk = parts[1]
    served = [p for p in parts if p.startswith("served=")][0][len("served="):]
    moved = [p for p in parts if p.startswith("fields_moved=")][0][len("fields_moved="):]
    return sk, served, moved


def run_final():
    parts = read_parts()
    slices = recorded_slices(parts)
    used_gets = sum(g for _s0, _s1, g, _b in slices)
    used_bytes = sum(b for _s0, _s1, _g, b in slices)
    client = Guarded(store._default_client(), BUDGET_REQUESTS - used_gets, BUDGET_BYTES - used_bytes)
    names_lines = []
    names = security_names(client, names_lines)
    name_rows = [parse_name_line(ln) for ln in parts if ln.startswith("NAME ")]
    seen = Counter(sk for sk, _s, _m in name_rows)
    missing = [n for n in names if seen[n] == 0]
    duplicate = sorted(n for n in seen if seen[n] > 1)
    extra = sorted(n for n in seen if n not in set(names))
    if missing or duplicate or extra:
        print("PARTS-GAP missing=%s duplicate=%s extra=%s" % (",".join(missing) or "none",
                                                              ",".join(duplicate) or "none",
                                                              ",".join(extra) or "none"))
        return 1
    no_stored = sum(1 for _sk, served, _m in name_rows if served == "none/-")
    build_errors = sum(1 for _sk, _s, moved in name_rows if moved == "build-error")
    numeric = [(sk, int(m)) for sk, s, m in name_rows if m.isdigit()]
    unchanged = sum(1 for _sk, m in numeric if m == 0)
    moved_names = sum(1 for _sk, m in numeric if m > 0)
    fields_moved = sum(m for _sk, m in numeric)
    cause_other = 0
    for line in parts:
        if line.startswith("DIFF "):
            m = _CAUSE_RE.search(line)
            if m is not None and is_other(m.group(1)):
                cause_other += 1
    gets = sum(g for _s0, _s1, g, _b in slices)
    nbytes = sum(b for _s0, _s1, _g, b in slices)
    budget_marks = [ln for ln in parts if ln.startswith("BUDGET-EXCEEDED")]

    header = []
    emit(header, "CENSUS-HEADER HVST-ci-3 dossier census; SERVED = gateway pick (harvest_research.py 239-255, as_of=None);"
                 " BUILT = dossier.build in memory; fields compared by parsed value; cause from the differing input"
                 " entries (kinds: continuation, fund_form, sector_template, typecast, model_block, picked_report)")
    emit(header, "CENSUS-HEADER bucket=%s budget_requests=%d budget_bytes=%d slices_recorded=%d"
         % (gold.HARVEST_BUCKET, BUDGET_REQUESTS, BUDGET_BYTES, len(slices)))
    emit(header, pin_field_map())
    for line in names_lines:
        emit(header, line)

    controls_lines = []
    controls(client, controls_lines)
    emit(controls_lines, "CONTROL-READS final_gets=%d final_bytes=%d" % (client.requests, client.bytes))
    for line in budget_marks:
        emit(controls_lines, "PARTS-NOTE " + line)

    body = [ln for ln in parts if ln.startswith(("NAME ", "DIFF ", "INPUTS ", "BUILD-ERROR ", "NO-STORED-DOSSIER ",
                                             "SLICE start=", "SLICE-RANGE ", "SLICE-BUDGET-BEFORE ",
                                             "BUDGET-EXCEEDED ", "SKIP-"))]
    emit(controls_lines, "BUILD-ERRORS n=%d" % build_errors)
    final = ("CENSUS-DOSSIER-MOVE names=%d no_stored_dossier=%d unchanged=%d moved=%d fields_moved=%d "
             "cause_other=%d gets=%d bytes=%d" % (len(names), no_stored, unchanged, moved_names, fields_moved,
                                                  cause_other, gets, nbytes))
    all_lines = header + body + controls_lines + [final]
    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in all_lines:
            fh.write(line + "\n")
    print(final, flush=True)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="HVST-ci-3 dossier no-write census")
    ap.add_argument("--start", type=int)
    ap.add_argument("--stop", type=int)
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args(argv)
    if args.final:
        return run_final()
    if args.start is None or args.stop is None or args.stop <= args.start:
        ap.error("a slice needs --start S --stop E with E > S")
    return run_slice(args.start, args.stop)


if __name__ == "__main__":
    sys.exit(main())
