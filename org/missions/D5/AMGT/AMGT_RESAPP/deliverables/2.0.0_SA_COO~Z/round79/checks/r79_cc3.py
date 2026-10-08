"""AMGT_RESAPP round 79 -- AMGT-cc-3, the store reader of the Seeking Alpha collector's job records.

  python r79_cc3.py --crit AC1|AC2|AC3 --where local

AC1 (build) `lib/research/freshness/collector_read.py` on a FAKE store client (no network):
  F0 the module imports and loads neither lib.research.harvest.store nor pyarrow;
  F1 two companies with records read as read, each dated by its greatest stored article time;
  F2 a company whose only record holds no article reads as checked, with no date;
  F3 a company with no folder reads no_record and never "not collected";
  F4 a malformed object is counted, named and not used as a date;
  F5 the slash name BP/_LN_Equity is found under its slash-safe folder;
  F6 a listing that raises does not raise out: every company reads unreadable, none carries a date;
  F7 ONE listing per call, bodies fetched for covered folders only, no other client method touched;
  F8 a body that cannot be fetched makes that one company unreadable and leaves the others as they were;
  F9 the September pilot object under the old tables never becomes a date;
  F10 compact_stamp turns a last-read time into the stamp form the other columns use;
  F11 a company with more records than the cap has only the newest ones fetched, and is named.
AC2 (build) the same function on the REAL store (read-only: one listing by the module, two by this check, GETs):
  R1 it returns without raising and its read finished;
  R2 every covered name has a state (95 of 95), each with the eight fields, each state one of read/checked/no_record;
  R3 the module's bucket and prefix equal the builder's (lib.research.harvest.store);
  R4 each covered name's state and date equal this check's own recount, compared only for names whose folder did
     not change between this check's listing before and after the call; 90 or more names compared, 0 differ;
  R5 the counts are at or above the floor measured at the cut (records are write-once, so these never fall):
     23 covered names with a record, 11 read;
  R6 no date is the pilot's 2026-09-11, and BABA, BA and COST each read at or after the date measured at the cut.
AC3 (bound) the freshness test folder passes, and `collector_record.py` and the schema file hold the bytes of the cut.
Verdict: R79 CC3 <crit> SERVED: YES|NO (exit 0|1). Nothing is written to any store.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys

MODULE = "lib.research.freshness.collector_read"
STATE_FIELDS = ("state", "last_read", "newest_job_finished_at", "newest_job_status", "stored_by_newest_job",
                "records", "rejected", "sentence")
PILOT_KEY_FORM = "seeking-alpha/harvest/bronze/symbol/%s/20260911T040304Z.json"
TIME = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
# Blob ids at the cut (git rev-parse HEAD:<path> at 44fe98b15e).
PINNED = (
    ("lib/research/freshness/collector_record.py", "848e4f19a6773687ad36119ab34329af538170c9"),
    ("lib/research/freshness/seeking_alpha_job_record.schema.json", "1040d31b7f27fcb1c762e4a898aa014f7cc10abd"),
)
# Measured at the cut, 2026-10-08T10:0xZ: 105 objects, 104 folders, 23 of 95 covered names with a record.
FLOOR_WITH_RECORD = 23
FLOOR_READ = 11
PILOT_FLOOR = (
    ("BABA_US_Equity", "2026-10-06T23:15:47Z"),
    ("BA_US_Equity", "2026-10-07T01:33:47Z"),
    ("COST_US_Equity", "2026-10-07T11:27:36Z"),
)
MIN_COMPARED = 90


def _root():
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _clause(results, name, cond, detail=""):
    results.append(bool(cond))
    print("%s %s %s" % ("PASS" if cond else "FAIL", name, str(detail)[:200]))


def _verdict(crit, results):
    ok = bool(results) and all(results)
    print("R79 CC3 %s SERVED: %s" % (crit, "YES" if ok else "NO"))
    return 0 if ok else 1


def _load(results, crit):
    try:
        import importlib
        return importlib.import_module(MODULE)
    except Exception as exc:  # noqa: BLE001 -- the build check reports any import failure as its first clause
        _clause(results, "F0 %s imports" % MODULE, False, "%s: %s" % (type(exc).__name__, exc))
        _verdict(crit, results)
        return None


def _rec(key, finished, stored, newest, status="new_articles"):
    return {"schema_version": 1, "security_key": key, "finished_at": finished, "status": status, "stored": stored,
            "newest_article_stored_at": newest}


class _FakeStore(object):
    """A dict of key -> bytes behind the three calls the module may make. Pages hold two keys each."""

    def __init__(self, objects, fail_list=False, fail_get=()):
        self.objects = dict(objects)
        self.fail_list = fail_list
        self.fail_get = set(fail_get)
        self.lists = []
        self.gets = []
        self.other = []

    def get_paginator(self, name):
        if name != "list_objects_v2":
            self.other.append("get_paginator:" + str(name))
        return self

    def paginate(self, **kwargs):
        self.lists.append(dict(kwargs))
        if "Delimiter" in kwargs:
            self.other.append("Delimiter")
        prefix = kwargs.get("Prefix") or ""
        keys = sorted(k for k in self.objects if k.startswith(prefix))

        def pages():
            if self.fail_list:
                raise RuntimeError("planted listing failure")
            for at in range(0, len(keys), 2):
                yield {"Contents": [{"Key": k, "Size": len(self.objects[k])} for k in keys[at:at + 2]]}
            if not keys:
                yield {}
        return pages()

    def get_object(self, Bucket=None, Key=None, **kwargs):  # noqa: N803 -- the store client's own argument names
        self.gets.append(Key)
        if Key in self.fail_get:
            raise RuntimeError("planted body failure")
        if Key not in self.objects:
            raise KeyError(Key)
        return {"Body": io.BytesIO(self.objects[Key])}

    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        self.other.append(name)
        raise AttributeError(name)


def _plant(mod):
    """The planted store: (objects, covered keys, the one uncovered folder's key, AAA's oldest keys)."""
    from lib.research.freshness import collector_record as cr

    bucket, prefix = mod.job_record_location()

    def key_of(security_key, stamp):
        return "%s%s/%s.json" % (prefix, cr.partition_for(security_key), stamp)

    def body(obj):
        return json.dumps(obj).encode("utf-8")

    objects = {}
    # AAA: two records, the greatest article time is the date.
    objects[key_of("AAA_US_Equity", "20261005T090000Z")] = body(
        _rec("AAA_US_Equity", "2026-10-05T09:00:00Z", 3, "2026-10-05T08:59:10Z"))
    objects[key_of("AAA_US_Equity", "20261007T013300Z")] = body(
        _rec("AAA_US_Equity", "2026-10-07T01:33:00Z", 1992, "2026-10-07T01:32:41Z"))
    # BBB: one record with an article.
    objects[key_of("BBB_US_Equity", "20261006T120000Z")] = body(
        _rec("BBB_US_Equity", "2026-10-06T12:00:00Z", 7, "2026-10-06T11:58:00Z"))
    # CCC: only a no-article record.
    objects[key_of("CCC_LN_Equity", "20261007T031005Z")] = body(
        _rec("CCC_LN_Equity", "2026-10-07T03:10:05Z", 0, None, status="no_new_articles"))
    # DDD: no folder at all, but the September pilot object sits under the old tables.
    objects[PILOT_KEY_FORM % cr.partition_for("DDD_US_Equity")] = body({"pilot": True})
    # EEE: one malformed object (off the contract) and nothing else.
    eee_bad = key_of("EEE_US_Equity", "20261007T050000Z")
    objects[eee_bad] = body({"schema_version": 1, "security_key": "EEE", "finished_at": "yesterday", "status": "",
                             "stored": -1, "newest_article_stored_at": "2026-10-07T04:59:00Z"})
    # FFF: one good record and one object that is not JSON.
    fff_bad = key_of("FFF_US_Equity", "20261007T060000Z")
    objects[fff_bad] = b"not json {"
    objects[key_of("FFF_US_Equity", "20261006T060000Z")] = body(
        _rec("FFF_US_Equity", "2026-10-06T06:00:00Z", 2, "2026-10-06T05:59:00Z"))
    # The slash name.
    objects[key_of("BP/_LN_Equity", "20261007T042800Z")] = body(
        _rec("BP/_LN_Equity", "2026-10-07T04:28:00Z", 4, "2026-10-07T04:27:21Z"))
    # GGG: seven records, one a day; the cap keeps the newest.
    for day in range(1, 8):
        objects[key_of("GGG_US_Equity", "2026100%dT000000Z" % day)] = body(
            _rec("GGG_US_Equity", "2026-10-0%dT00:00:00Z" % day, 1, "2026-10-0%dT00:00:00Z" % day if day > 1 else None))
    # A folder nobody covers.
    uncovered = key_of("ZZZ_US_Equity", "20261007T070000Z")
    objects[uncovered] = body(_rec("ZZZ_US_Equity", "2026-10-07T07:00:00Z", 1, "2026-10-07T06:59:00Z"))
    covered = ["AAA_US_Equity", "BBB_US_Equity", "CCC_LN_Equity", "DDD_US_Equity", "EEE_US_Equity", "FFF_US_Equity",
               "BP/_LN_Equity", "GGG_US_Equity"]
    return objects, covered, uncovered, {"eee_bad": eee_bad, "fff_bad": fff_bad, "key_of": key_of, "prefix": prefix,
                                         "bucket": bucket}


def _shape_ok(state):
    return isinstance(state, dict) and all(f in state for f in STATE_FIELDS)


def ac1():
    results = []
    mod = _load(results, "AC1")
    if mod is None:
        return 1
    loaded = [m for m in ("lib.research.harvest.store", "pyarrow") if m in sys.modules]
    _clause(results, "F0 the module imports and loads neither the harvest store module nor pyarrow", not loaded, loaded)
    try:
        objects, covered, uncovered, extra = _plant(mod)
        store = _FakeStore(objects)
        out = mod.seeking_alpha_by_security(list(covered), client=store)
        by = out["by_security"]
        read = out["read"]
    except Exception as exc:  # noqa: BLE001 -- a build that raises fails every clause below, named once
        _clause(results, "F1 the function answers on the planted store", False, "%s: %s" % (type(exc).__name__, exc))
        return _verdict("AC1", results)
    loaded = [m for m in ("lib.research.harvest.store", "pyarrow") if m in sys.modules]
    _clause(results, "F0b still neither after a call", not loaded, loaded)
    shapes = sorted(k for k in covered if not _shape_ok(by.get(k)))
    a, b = by.get("AAA_US_Equity") or {}, by.get("BBB_US_Equity") or {}
    _clause(results, "F1 two companies with records read as read, dated by the greatest stored article time",
            not shapes and sorted(by) == sorted(covered)
            and a.get("state") == "read" and a.get("last_read") == "2026-10-07T01:32:41Z" and a.get("records") == 2
            and b.get("state") == "read" and b.get("last_read") == "2026-10-06T11:58:00Z"
            and read.get("read_completed") is True,
            "AAA %s %s; BBB %s %s; missing fields %s" % (a.get("state"), a.get("last_read"), b.get("state"),
                                                         b.get("last_read"), shapes))
    c = by.get("CCC_LN_Equity") or {}
    _clause(results, "F2 a company whose only record holds no article reads as checked, with no date",
            c.get("state") == "checked" and c.get("last_read") is None
            and "not collected" not in str(c.get("sentence", "")).lower(), "%s %s" % (c.get("state"), c.get("sentence")))
    d = by.get("DDD_US_Equity") or {}
    _clause(results, "F3 a company with no folder reads no_record, never not collected",
            d.get("state") == "no_record" and d.get("last_read") is None
            and "not collected" not in str(d.get("sentence", "")).lower(), "%s %s" % (d.get("state"), d.get("sentence")))
    e, f = by.get("EEE_US_Equity") or {}, by.get("FFF_US_Equity") or {}
    named = list(read.get("rejected") or [])
    _clause(results, "F4 a malformed object is counted, named and not used as a date",
            e.get("state") == "no_record" and e.get("last_read") is None and e.get("rejected") == 1
            and f.get("state") == "read" and f.get("last_read") == "2026-10-06T05:59:00Z" and f.get("rejected") == 1
            and sorted(named) == sorted([extra["eee_bad"], extra["fff_bad"]]),
            "EEE %s rejected %s; FFF %s %s rejected %s; named %d" % (e.get("state"), e.get("rejected"), f.get("state"),
                                                                    f.get("last_read"), f.get("rejected"), len(named)))
    s = by.get("BP/_LN_Equity") or {}
    _clause(results, "F5 the slash name is found under its slash-safe folder",
            s.get("state") == "read" and s.get("last_read") == "2026-10-07T04:27:21Z",
            "%s %s" % (s.get("state"), s.get("last_read")))
    wanted_gets = set(k for k in objects if k.startswith(extra["prefix"]) and k != uncovered)
    capped_out = set(extra["key_of"]("GGG_US_Equity", "2026100%dT000000Z" % day)
                     for day in range(1, 8 - int(getattr(mod, "MAX_RECORDS_PER_COMPANY", 5))))
    _clause(results, "F7 one listing per call, bodies fetched for covered folders only, no other client method touched",
            len(store.lists) == 1 and store.lists[0].get("Prefix") == extra["prefix"]
            and store.lists[0].get("Bucket") == extra["bucket"]
            and uncovered not in store.gets and set(store.gets) == wanted_gets - capped_out
            and len(store.gets) == len(set(store.gets)) and not store.other,
            "listings %d; gets %d of %d wanted; uncovered fetched %s; other calls %s"
            % (len(store.lists), len(store.gets), len(wanted_gets - capped_out), uncovered in store.gets, store.other))
    g = by.get("GGG_US_Equity") or {}
    cap = getattr(mod, "MAX_RECORDS_PER_COMPANY", None)
    _clause(results, "F11 a company over the cap has only its newest records fetched, and is named",
            cap == 5 and g.get("state") == "read" and g.get("last_read") == "2026-10-07T00:00:00Z" and g.get("records") == 5
            and list(read.get("capped") or []) == ["GGG_US_Equity"],
            "cap %s; GGG %s %s records %s; capped %s" % (cap, g.get("state"), g.get("last_read"), g.get("records"),
                                                        read.get("capped")))
    _clause(results, "F9 the September pilot object under the old tables never becomes a date",
            all(not str((by.get(k) or {}).get("last_read") or "").startswith("2026-09-11") for k in covered)
            and not any("/bronze/" in k for k in store.gets), "DDD %s" % (d.get("last_read"),))
    # F6: a listing that raises.
    try:
        broken = _FakeStore(objects, fail_list=True)
        out6 = mod.seeking_alpha_by_security(list(covered), client=broken)
        by6, read6 = out6["by_security"], out6["read"]
        ok6 = (sorted(by6) == sorted(covered) and all(_shape_ok(by6[k]) for k in covered)
               and all(by6[k]["state"] == "unreadable" and by6[k]["last_read"] is None for k in covered)
               and all("could not be read just now" in str(by6[k]["sentence"]) for k in covered)
               and read6.get("read_completed") is False and bool(read6.get("reason")) and not broken.gets)
        detail6 = "states %s; read_completed %s" % (sorted(set(v.get("state") for v in by6.values())),
                                                    read6.get("read_completed"))
    except Exception as exc:  # noqa: BLE001
        ok6, detail6 = False, "raised %s: %s" % (type(exc).__name__, exc)
    _clause(results, "F6 a listing that raises does not raise out: every company reads unreadable, none has a date",
            ok6, detail6)
    # F8: one body that cannot be fetched.
    try:
        bbb_key = extra["key_of"]("BBB_US_Equity", "20261006T120000Z")
        partial = _FakeStore(objects, fail_get=[bbb_key])
        out8 = mod.seeking_alpha_by_security(list(covered), client=partial)
        by8, read8 = out8["by_security"], out8["read"]
        ok8 = (by8["BBB_US_Equity"]["state"] == "unreadable" and by8["BBB_US_Equity"]["last_read"] is None
               and by8["AAA_US_Equity"] == by["AAA_US_Equity"] and by8["CCC_LN_Equity"] == by["CCC_LN_Equity"]
               and read8.get("read_completed") is False and list(read8.get("bodies_failed") or []) == [bbb_key])
        detail8 = "BBB %s; AAA %s; read_completed %s; failed %d" % (
            by8["BBB_US_Equity"].get("state"), by8["AAA_US_Equity"].get("state"), read8.get("read_completed"),
            len(read8.get("bodies_failed") or []))
    except Exception as exc:  # noqa: BLE001
        ok8, detail8 = False, "raised %s: %s" % (type(exc).__name__, exc)
    _clause(results, "F8 a body that cannot be fetched makes that one company unreadable and leaves the others",
            ok8, detail8)
    try:
        stamps = (mod.compact_stamp("2026-10-07T01:32:41Z"), mod.compact_stamp(None), mod.compact_stamp("yesterday"))
    except Exception as exc:  # noqa: BLE001
        stamps = ("raised %s" % type(exc).__name__,)
    _clause(results, "F10 compact_stamp gives the stamp form the other columns use, and None for no date",
            stamps == ("20261007T013241Z", None, None), stamps)
    return _verdict("AC1", results)


def _list_folders(client, bucket, prefix):
    """{folder -> sorted object keys} for keys shaped <prefix><folder>/<name>.json; ONE paginated listing."""
    out = {}
    count = 0
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            count += 1
            parts = obj["Key"][len(prefix):].split("/")
            if len(parts) == 2 and parts[0].startswith("security_key=") and parts[1].endswith(".json"):
                out.setdefault(parts[0], []).append(obj["Key"])
    return dict((k, sorted(v)) for k, v in out.items()), count


def ac2():
    results = []
    mod = _load(results, "AC2")
    if mod is None:
        return 1
    try:
        import boto3
        from lib.research.coverage.covered_universe import covered_security_keys
        from lib.research.freshness import collector_record as cr
        from lib.research.harvest import store

        covered = list(covered_security_keys())
        uri = store.address_of("seeking-alpha", "state", "job_record",
                               store.entity_partition("security_key", "BA_US_Equity"), object_name="x.json")
        bucket = uri[len("s3://"):].split("/", 1)[0]
        prefix = store.table_prefix("seeking-alpha", "state", "job_record")
        client = boto3.client("s3", region_name="us-east-1")
        before, objects_before = _list_folders(client, bucket, prefix)
    except Exception as exc:  # noqa: BLE001 -- the check's own read failing is a FAIL with its reason, never a pass
        _clause(results, "R0 this check's own read of the store", False, "%s: %s" % (type(exc).__name__, exc))
        return _verdict("AC2", results)
    try:
        out = mod.seeking_alpha_by_security(list(covered))
        by, read = out["by_security"], out["read"]
        raised = None
    except Exception as exc:  # noqa: BLE001
        by, read, raised = {}, {}, "%s: %s" % (type(exc).__name__, exc)
    _clause(results, "R1 the function returns on the real store without raising, and its read finished",
            raised is None and read.get("read_completed") is True,
            raised or "objects listed %s; bodies read %s; rejected %d; reason %s" % (
                read.get("objects_listed"), read.get("bodies_read"), len(read.get("rejected") or []), read.get("reason")))
    if raised is not None:
        return _verdict("AC2", results)
    states = {}
    for key in covered:
        states[(by.get(key) or {}).get("state")] = states.get((by.get(key) or {}).get("state"), 0) + 1
    good = [k for k in covered if _shape_ok(by.get(k)) and by[k]["state"] in ("read", "checked", "no_record")
            and (by[k]["last_read"] is None or TIME.match(str(by[k]["last_read"])))
            and ((by[k]["state"] == "read") == (by[k]["last_read"] is not None))]
    _clause(results, "R2 every covered name has a state: read, checked or no_record, a date only on read",
            len(covered) == 95 and len(good) == len(covered) and len(by) == len(covered),
            "%d of %d covered; states %s" % (len(good), len(covered), states))
    try:
        got = mod.job_record_location()
    except Exception as exc:  # noqa: BLE001
        got = "raised %s" % type(exc).__name__
    _clause(results, "R3 the module's bucket and prefix equal the builder's", got == (bucket, prefix),
            "%s against %s" % (got, (bucket, prefix)))
    after, objects_after = _list_folders(client, bucket, prefix)
    compared, differ, moved = 0, [], 0
    for key in covered:
        folder = cr.partition_for(key)
        if before.get(folder) != after.get(folder):
            moved += 1
            continue
        objs = []
        for okey in (after.get(folder) or []):
            try:
                objs.append(json.loads(client.get_object(Bucket=bucket, Key=okey)["Body"].read().decode("utf-8")))
            except ValueError:
                objs.append(None)
        want = cr.seeking_alpha_state(objs)
        have = by.get(key) or {}
        compared += 1
        if (have.get("state"), have.get("last_read")) != (want["state"], want["last_read"]):
            differ.append("%s have %s %s want %s %s" % (key, have.get("state"), have.get("last_read"), want["state"],
                                                       want["last_read"]))
    _clause(results, "R4 state and date equal this check's own recount on every name whose folder did not change",
            compared >= MIN_COMPARED and not differ,
            "compared %d of %d (folders that changed during the run: %d); differ %d %s; objects %d then %d"
            % (compared, len(covered), moved, len(differ), differ[:2], objects_before, objects_after))
    with_record = sum(1 for k in covered if (by.get(k) or {}).get("state") in ("read", "checked"))
    read_n = states.get("read", 0)
    _clause(results, "R5 the counts are at or above the floor measured at the cut",
            with_record >= FLOOR_WITH_RECORD and read_n >= FLOOR_READ
            and with_record + states.get("no_record", 0) == len(covered),
            "with a record %d (floor %d); read %d (floor %d); checked %d; no_record %d"
            % (with_record, FLOOR_WITH_RECORD, read_n, FLOOR_READ, states.get("checked", 0), states.get("no_record", 0)))
    pilot_dates = [k for k in covered if str((by.get(k) or {}).get("last_read") or "").startswith("2026-09-11")]
    pilots = [(k, (by.get(k) or {}).get("state"), (by.get(k) or {}).get("last_read")) for k, _ in PILOT_FLOOR]
    pilots_ok = all((by.get(k) or {}).get("state") == "read" and str((by.get(k) or {}).get("last_read") or "") >= floor
                    for k, floor in PILOT_FLOOR)
    _clause(results, "R6 no date is the pilot's 2026-09-11; BABA, BA and COST read at or after the cut's dates",
            not pilot_dates and pilots_ok, "pilot-dated %s; %s" % (pilot_dates, pilots))
    return _verdict("AC2", results)


def ac3():
    results = []
    root = _root()
    env = dict(os.environ)
    env["PYTHONPATH"] = root
    run = subprocess.run([sys.executable, "-m", "pytest", "lib/research/freshness/tests", "-q", "-p", "no:cacheprovider",
                          "--color=no"], capture_output=True, text=True, cwd=root, env=env)
    lines = [ln for ln in (run.stdout or "").splitlines() if ln.strip()]
    last = lines[-1] if lines else (run.stderr or "").strip()[-160:]
    _clause(results, "B1 the freshness test folder passes", run.returncode == 0 and " passed" in last
            and "failed" not in last and "error" not in last, last)
    for path, pinned in PINNED:
        got = subprocess.run(["git", "hash-object", "--", path], capture_output=True, text=True, cwd=root).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", path], capture_output=True, text=True,
                               cwd=root).stdout.strip()
        _clause(results, "B2 %s holds the bytes of the cut" % path, got == pinned and not dirty,
                "blob %s pinned %s%s" % (got[:12], pinned[:12], "; uncommitted change" if dirty else ""))
    return _verdict("AC3", results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    sys.path.insert(0, _root())
    return {"AC1": ac1, "AC2": ac2, "AC3": ac3}[a.crit]()


if __name__ == "__main__":
    sys.exit(main())
