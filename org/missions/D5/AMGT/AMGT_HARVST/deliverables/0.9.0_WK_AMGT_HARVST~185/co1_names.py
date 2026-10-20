"""co1_names.py -- AMGT_HARVST HVST-co-1 (round 100, CTO round-99 analysis item 1). READ-ONLY, WRITES NOTHING but its own
out file (co1_names.out beside this file).

For each guard-stopped name (BZLFY_US_Equity, PBR_US_Equity, TSM_US_Equity), in sorted order: names each valued
model_rows row that the build (dossier.build, in memory) drops against the stored dossier the gateway serves, and the
cause of each drop, decided from the two Model blocks the two dossiers cite and never from the mnemonic's name.

Method reused unchanged from deliverables/0.9.0_WK_AMGT_HARVST~180/cn2_pbr.py (served pick, build in memory, finder,
cause decision). SERVED = a copy of harvest_research._pick_dossier (as_of=None, greatest stamp, canonical partition of
  crosswalk.security_key_partition), checked against infra/aws/ec2/opal-gateway/app/harvest_research.py lines 270-287.
BUILT  = dossier.build(name, client) IN MEMORY. This file contains no write call. The Guarded client forwards
  get_object, head_object, list_objects_v2 and its paginator on opal-data-harvest only, and refuses every other
  operation by name. No Bloomberg, no model call, no gateway call.

Identity of a model_rows entry = source | mnemonic-or-label | fiscal_year-or-fiscal_period of its figure. Rows are matched
  as a multiset on identity. A stored VALUED row with no built VALUED row of the same identity is a ROWMISS; a built
  valued row with no stored counterpart is a ROWNEW. Valued = the guard's own rule (figure.value not null).

Cause (CAUSE line), read from the two blocks through dossier._figure_for_row_key (the build's own lookup):
  build_rule_dropped_it           no built model_rows entry carries the row's source and key
  field_absent_in_new_block       the built block carries no figure for the key
  value_null_in_new_block         the built block's figure for the key is present with a null value
  row_moved_to_other_fiscal_year  the built block's valued figure for the key is for another fiscal year
  other                           none of the above (a surprise)

Controls (rule 22): CONTROL-POSITIVE UNH_US_Equity (served vs built, same finder) and CONTROL-NEGATIVE (one valued row
removed from a copy of BZLFY's stored model_rows, compared with the SAME finder).
Budget: 4500 requests and 700 MiB across the whole run, counted on the last line.

Usage, from the worktree root (foreground): python -u <this file> > .scratch/co1_stdout.txt
"""

import copy
import gzip
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import timezone

ROOT = os.getcwd()
sys.path.insert(0, ROOT)

from lib.research.corpus import dossier  # noqa: E402
from lib.research.corpus import gold  # noqa: E402
from lib.research.corpus import substrate  # noqa: E402
from lib.research.coverage import pool_reader  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.identity import crosswalk  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "co1_names.out")
NAMES = ["BZLFY_US_Equity", "PBR_US_Equity", "TSM_US_Equity"]
# the guard's own counts as the guard printed them on the 2026-10-20 fire (rows_stored, rows_built, rows_missed)
EXPECT = {"BZLFY_US_Equity": (56, 55, 1), "PBR_US_Equity": (56, 55, 1), "TSM_US_Equity": (54, 53, 1)}
CONTROL = "UNH_US_Equity"
BUDGET_REQUESTS = 4500
BUDGET_BYTES = 700 * 1024 * 1024
GATEWAY_SUFFIXES = (".json", ".json.gz")
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")  # harvest_research.py _AS_OF
MODEL_BLOCK_PREFIX = "derived/model_block/"  # scoped_amgt.MODEL_BLOCK_POOL_PREFIX

LINES = []


class BudgetExceeded(Exception):
    pass


class Guarded(object):
    """Forwards the read operations on the harvest bucket only; counts fetched requests and bytes against the budget.
    A repeated identical read inside this process is answered from a read-through memo (a memo hit is not a request)."""

    def __init__(self, client, max_requests, max_bytes):
        self._client = client
        self.requests = 0
        self.bytes = 0
        self.hits = 0
        self.max_requests = max_requests
        self.max_bytes = max_bytes
        self._memo = {}

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
        self._memo[key] = data
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


def emit(text):
    """One output line: printed now and kept for the output file. ASCII only."""
    safe = text.encode("ascii", "backslashreplace").decode("ascii")
    print(safe, flush=True)
    LINES.append(safe)


def norm(value):
    """Parsed-value form: the JSON round trip (sorted keys; tuples become lists)."""
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


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


def dossier_prefix(security_key):
    """The stored partition of the name (the writer's form): crosswalk.security_key_partition."""
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
    picked, _stamp, dup = pick_dossier(listed, None)
    dup = dict(dup)
    dup["objects"] = len(rows)
    if picked is None:
        return None, None, dup
    raw = gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, picked["key"]), client=client)
    if picked["key"].endswith(".gz"):
        raw = gzip.decompress(raw)
    return picked["key"], json.loads(raw.decode("utf-8")), dup


def block_bytes(client, key):
    """The raw landed Model block object (a memo hit when the build already read it)."""
    body = client.get_object(Bucket=pool_reader.POOL_BUCKET, Key=key)["Body"]
    return body.read()


def valued(row):
    """A model_rows entry whose figure carries a non-null value (the guard's rule, dossier-side census valued_rows)."""
    fig = row.get("figure") if isinstance(row, dict) else None
    return isinstance(fig, dict) and fig.get("value") is not None


def valued_count(rows):
    if not isinstance(rows, list):
        return 0
    return sum(1 for r in rows if valued(r))


def row_key(row):
    return row.get("mnemonic") or row.get("label") or "?"


def row_period(row):
    fig = row.get("figure") or {}
    return str(fig.get("fiscal_year") or fig.get("fiscal_period") or "-")


def identity(row):
    return "%s|%s|%s" % (row.get("source"), row_key(row), row_period(row))


def printable(text):
    return text.replace(" ", "_")


def find_misses(stored_rows, built_rows):
    """(missed, new, duplicate identities): stored valued rows with no built valued row of the same identity (a multiset
    match), and built valued rows left unmatched. The same finder serves the census controls."""
    pool = defaultdict(list)
    for r in built_rows:
        if valued(r):
            pool[identity(r)].append(r)
    missed = []
    for r in stored_rows:
        if not valued(r):
            continue
        bucket = pool.get(identity(r))
        if bucket:
            bucket.pop(0)
        else:
            missed.append(r)
    new = [r for bucket in pool.values() for r in bucket]
    s_ids = Counter(identity(r) for r in stored_rows if valued(r))
    b_ids = Counter(identity(r) for r in built_rows if valued(r))
    dups = sorted(["stored:" + k for k, v in s_ids.items() if v > 1] + ["built:" + k for k, v in b_ids.items() if v > 1])
    return missed, new, dups


def same_key_rows(row, rows):
    return [b for b in rows if b.get("source") == row.get("source") and row_key(b) == row_key(row)]


def figure_text(fig):
    if fig is None:
        return "none"
    period = fig.get("fiscal_year") or fig.get("fiscal_period") or "-"
    return "scope=%s period=%s value=%s unit=%s" % (fig.get("scope"), period, json.dumps(fig.get("value")), fig.get("unit"))


def built_text(row, built_rows):
    """The built counterpart of a stored row: its value and period, or its absent reason, or its absence."""
    same = same_key_rows(row, built_rows)
    if not same:
        return "absent:no built model_rows entry with source=%s key=%s" % (row.get("source"), row_key(row))
    b = next((x for x in same if valued(x)), same[0])
    if valued(b):
        return "value=%s period=%s" % (json.dumps(b["figure"].get("value")), row_period(b))
    return "absent=%s period=%s" % (b["figure"].get("absent"), row_period(b))


def decide_cause(row, built_rows, stored_block, built_block):
    """(cause token, evidence), decided from the two blocks through the build's own lookup, never from the key's name."""
    key = row_key(row)
    fy = row_period(row)
    sfig, sreason = dossier._figure_for_row_key(stored_block, key)
    bfig, breason = dossier._figure_for_row_key(built_block, key)
    if not same_key_rows(row, built_rows):
        cause = "build_rule_dropped_it"
    elif bfig is None:
        cause = "field_absent_in_new_block"
    elif bfig.get("value") is None:
        cause = "value_null_in_new_block"
    elif str(bfig.get("fiscal_year") or bfig.get("fiscal_period") or "-") != fy:
        cause = "row_moved_to_other_fiscal_year"
    else:
        cause = "other"
    evidence = ("stored_block_figure[%s]=%s stored_row_period=%s; built_block_figure[%s]=%s built_block_reason=%s"
                % (key, figure_text(sfig), fy, key, figure_text(bfig), (breason or sreason or "none")[:120]))
    return cause, evidence


def cause_word(missed, stored_block, built_block, built_rows):
    if not missed:
        return "none", []
    causes = []
    for r in missed:
        c, _ev = decide_cause(r, built_rows, stored_block, built_block)
        causes.append(c)
    distinct = sorted(set(causes))
    return (distinct[0] if len(distinct) == 1 else "mixed"), causes


def name_report(client, name, served_rows_by_name):
    """One guard-stopped name: the NAME, BLOCK, ROWMISS, CAUSE, ROWNEW lines and its DROPPED-ROW line."""
    served_key, served_doc, dup = served_of(client, name)
    if served_doc is None:
        emit("NAME-NO-STORED-DOSSIER %s dossier_objects_listed=%d" % (name, dup["objects"]))
        return
    built = dossier.build(name, client=client)
    served_rows = (served_doc.get("fields") or {}).get("model_rows")
    built_rows = (built.get("fields") or {}).get("model_rows")
    served_rows_by_name[name] = served_rows

    stored_block_key = next((e.get("key") for e in (served_doc.get("inputs") or [])
                             if str(e.get("key", "")).startswith(MODEL_BLOCK_PREFIX)), None)
    built_doc, built_record = dossier._model_block_read(name, client)
    built_block_key = built_record.get("object_key")
    emit("NAME %s served=%s built_as_of=%s stored_block=%s built_block=%s"
         % (name, served_key, built.get("as_of"), dossier._model_block_stamp(name, stored_block_key),
            dossier._model_block_stamp(name, built_block_key)))
    emit("DUPLICATES %s dossier_objects_listed=%d distinct_as_of=%d dropped=%d built_record_status=%s"
         % (name, dup["objects"], dup["distinct_as_of"], dup["dropped"], built_record.get("status")))
    emit("BLOCK-KEYS %s stored=%s built=%s" % (name, stored_block_key, built_block_key))

    stored_raw = block_bytes(client, stored_block_key)
    built_raw = block_bytes(client, built_block_key)
    stored_block = json.loads(stored_raw.decode("utf-8"))
    built_block = json.loads(built_raw.decode("utf-8"))

    sub = substrate.substrate(name, client=client)
    tc, sc = sub["typecast"], sub["sector_template"]
    stored_derived = dossier._model_rows(tc, sc, name, stored_block,
                                         {"status": "SERVED", "object_key": stored_block_key}, client)
    built_derived = dossier._model_rows(tc, sc, name, built_block,
                                        {"status": "SERVED", "object_key": built_block_key}, client)
    for label, block, raw, derived, key, rows in (
            ("stored", stored_block, stored_raw, stored_derived, stored_block_key, served_rows),
            ("built", built_block, built_raw, built_derived, built_block_key, built_rows)):
        figures = block.get("figures") or []
        figs_valued = sum(1 for f in figures if f.get("value") is not None)
        emit("BLOCK %s %s key=%s bytes=%d figures=%d figures_valued=%d unresolved=%d model_rows_valued_by_guard_rule=%d"
             % (name, label, key, len(raw), len(figures), figs_valued, len(block.get("unresolved") or []),
                valued_count(derived)))
        emit("REPRODUCE %s %s block_rows_equal_dossier_rows=%s dossier_rows_valued=%d block_rows_valued=%d"
             % (name, label, "yes" if norm(derived) == norm(rows) else "no", valued_count(rows), valued_count(derived)))

    rows_stored = valued_count(served_rows)
    rows_built = valued_count(built_rows)
    missed, new, dups = find_misses(served_rows, built_rows)
    emit("IDENTITY-DUPLICATES %s stored_built=%s" % (name, ",".join(dups) or "none"))
    emit("COUNTS %s model_rows_entries stored=%d built=%d valued stored=%d built=%d"
         % (name, len(served_rows or []), len(built_rows or []), rows_stored, rows_built))
    for row in missed:
        cause, evidence = decide_cause(row, built_rows, stored_block, built_block)
        emit("ROWMISS %s stored_value=%s built=%s"
             % (printable(identity(row)), json.dumps(row["figure"].get("value"))[:60], built_text(row, built_rows)[:80]))
        emit("CAUSE %s %s %s block_keys stored=%s built=%s"
             % (printable(identity(row)), cause, evidence, stored_block_key, built_block_key))
    for row in new:
        emit("ROWNEW %s value=%s period=%s" % (printable(identity(row)), json.dumps(row["figure"].get("value"))[:60],
                                                 row_period(row)))
    cause, _causes = cause_word(missed, stored_block, built_block, built_rows)
    emit("DROPPED-ROW %s rows_stored=%d rows_built=%d rows_missed=%d rows_new=%d cause=%s"
         % (name, rows_stored, rows_built, len(missed), len(new), cause))
    if name in EXPECT and (rows_stored, rows_built, len(missed)) != EXPECT[name]:
        emit("DEVIATION-FROM-ISSUER-EXPECTATION %s rows_stored=%d rows_built=%d rows_missed=%d (issuer expects %d, %d, %d); "
             "the counts are the finding" % ((name, rows_stored, rows_built, len(missed)) + EXPECT[name]))


def controls(client, served_rows_by_name):
    """CONTROL-POSITIVE (UNH, served vs built, same finder) and CONTROL-NEGATIVE (one valued row removed from a copy of
    BZLFY's stored model_rows, compared with the same finder)."""
    uk, udoc, _udup = served_of(client, CONTROL)
    if udoc is None:
        emit("CONTROL-ERROR no stored dossier for %s" % CONTROL)
    else:
        ubuilt = dossier.build(CONTROL, client=client)
        u_served = (udoc.get("fields") or {}).get("model_rows")
        u_built = (ubuilt.get("fields") or {}).get("model_rows")
        umissed, unew, _udups = find_misses(u_served, u_built)
        emit("CONTROL-POSITIVE %s rows_missed=%d rows_new=%d rows_stored=%d rows_built=%d served_object=%s"
             % (CONTROL, len(umissed), len(unew), valued_count(u_served), valued_count(u_built), uk))
        for row in umissed:
            emit("CONTROL-ROWMISS %s %s" % (CONTROL, printable(identity(row))))
    base = served_rows_by_name.get("BZLFY_US_Equity")
    if not base or not any(valued(r) for r in base):
        emit("CONTROL-ERROR no BZLFY_US_Equity stored valued rows to plant a deletion in")
        return
    planted = copy.deepcopy(base)
    idx = next(i for i, r in enumerate(planted) if valued(r))
    gone = planted.pop(idx)
    nmissed, _nnew, _ndups = find_misses(base, planted)
    matched = len(nmissed) == 1 and identity(nmissed[0]) == identity(gone)
    emit("CONTROL-NEGATIVE planted_row_dropped rows_missed=%d identity=%s matched_planted=%s"
         % (len(nmissed), printable(identity(gone)), "yes" if matched else "no"))


def run():
    if pool_reader.POOL_BUCKET != gold.HARVEST_BUCKET:
        raise SystemExit("model-block pool bucket %r is not the harvest bucket; the census refuses" % pool_reader.POOL_BUCKET)
    client = Guarded(store._default_client(), BUDGET_REQUESTS, BUDGET_BYTES)
    emit("CO1-HEADER HVST-co-1 (round 100) guard-stopped names dropped-row finder; SERVED = gateway pick of the stored "
         "dossier; BUILT = dossier.build in memory; identity = source|key|period; cause from the two Model blocks")
    emit("CO1-HEADER bucket=%s budget_requests=%d budget_bytes=%d names=%s"
         % (gold.HARVEST_BUCKET, BUDGET_REQUESTS, BUDGET_BYTES, ",".join(NAMES)))
    emit("IDENTITY-RULE a row's identity is source|mnemonic-or-label|fiscal_year-or-fiscal_period of its figure; "
         "rows matched as a multiset on identity; ROWMISS = stored valued row with no built valued row of that identity")

    served_rows_by_name = {}
    for name in sorted(NAMES):
        try:
            name_report(client, name, served_rows_by_name)
        except BudgetExceeded:
            raise
        except Exception as exc:  # noqa: BLE001 -- recorded on the output, the other names still run
            emit("NAME-ERROR %s %s: %s" % (name, type(exc).__name__, str(exc)[:200]))
    controls(client, served_rows_by_name)
    emit("GUARD-STOPS names=%d gets=%d bytes=%d" % (len(NAMES), client.requests, client.bytes))
    return 0


def main():
    rc = 1
    try:
        rc = run()
    except BudgetExceeded as exc:
        emit("BUDGET-EXCEEDED (%s)" % exc)
    finally:
        with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            for line in LINES:
                fh.write(line + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
