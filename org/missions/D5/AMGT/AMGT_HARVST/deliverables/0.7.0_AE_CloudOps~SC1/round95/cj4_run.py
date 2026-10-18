"""HVST-cj-4 driver, run from the pinned worktree (C:/tmp/cj4-build at 8f329a10b9). ASCII only.

Usage (always foreground, always `python -u`; the caller appends the output to cj4_run.log):
  python -u cj4_run.py --plan NAME [NAME ...]                        read only: every pre-write check per name, nothing put
  python -u cj4_run.py --go-utc 2026-10-18T07:45:00Z NAME [NAME ...]  per name in the order given: checks, write, read back, manifest
NO loop over the list, NO retry, NO background mode (COO half C-5). A name not in cj4_names.txt is a STOP. The driver never
calls continuation.write_one, never runs any module --write, never calls etfs_compare_peers (C-6, C-9). The write window is the
issuer's GO (--go-utc) to GO+150 minutes; outside it the driver refuses. At the first anomaly it stops the batch.

Per name, BEFORE the write (any failure is a STOP with nothing written for that name):
 (1) the served dossier is the gateway's pick (infra/aws/ec2/opal-gateway/app/harvest_research.py::_pick_dossier, copied);
 (2) dossier.build(name) in memory: the moved fields must be a SUBSET of {fund_form_ref, model_rows}; the differing inputs
     kinds a SUBSET of {continuation, fund_form, model_block};
 (3) the CTO's model-block guard (his half, condition 1), with dossier._model_block_read read again here:
     for a name whose build moves model_rows: the record reads SERVED; its object key's timestamp is LATER than the
     model-block stamp in the stored dossier's inputs; the number of model_rows ROWS WITH A VALUE (a list element whose
     ["figure"]["value"] is not None) is NOT lower than the served count; for a name that does not move model_rows: the record
     reads SERVED, or the served inputs carry no model block. The record's object key must equal the build's model_block input.
AFTER the write: the manifest line is appended and fsynced first, then the read-back (Branch A): subject, method_version,
every field but model_rows equal to the pre-write build, model_rows compared and counted, inputs equal, recomputed
content_sha256, object name as_of=<as_of>.<_inputs_sha16(inputs)>.json, partition count +1, and the gateway pick over the
new listing names the written key.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time

WT = r"C:\tmp\cj4-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, dossier, fund_form, gold, sector_template, typecast  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PIN = "8f329a10b9"
ROUND = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables"
OUT = ROUND + r"\0.7.0_AE_CloudOps~SC1\round95"
LIST_DIR = ROUND + r"\2.0.0_SA_COO_W1\round95"
NAMES_PATH = LIST_DIR + r"\cj4_names.txt"
NAMES_SHA = "ebcec99e045a59d0871b25532ff9d74b337c00ddefe568a4d5303cf86947567e"
MOVES_PATH = LIST_DIR + r"\cj4_expected_moves.txt"
MOVES_SHA = "ba4cd92ef19efc12f84a292de3df35743732ee9ac39291323611e31ab5ad88ff"
MANIFEST = os.path.join(OUT, "cj4_written.out")
WINDOW_MIN = 270  # AMENDMENT 3 (W1 msg 7970, aecf3f0243): the window ends 12:15:00Z (GO_UTC 07:45:00Z + 270 min); it was 150 min (10:15:00Z)
WINDOW_END_TEXT = "12:15:00Z"
MEMO_MARKERS = ("/research-continuation/", "/research-fund-form/", "/research_dossier/", "/sector-template", "/typecast",
                "/silver/", "/bronze/", "derived/model_block/")  # AMENDMENT 2: gold, silver, bronze and derived/model_block objects by FULL key
ALLOWED_FIELDS = {"fund_form_ref", "model_rows"}
ALLOWED_KINDS = {"continuation", "fund_form", "model_block"}
GATEWAY_SUFFIXES = (".json", ".json.gz")
_AS_OF = re.compile(r"as_of=(\d{4}-\d{2}-\d{2})\.")
MODEL_BLOCK_PREFIX = "derived/model_block/"
ABSENT = object()


class MemoClient:
    """AMENDMENT 2: a per-process read-through memo of get_object reads of IMMUTABLE keys (a gold, silver, bronze or
    derived/model_block object addressed by its full key; the key families are MEMO_MARKERS). It NEVER caches a listing
    (get_paginator), a head_object, the pick, the read-back of a key this process wrote, or anything read after the first write
    of that name (the driver switches the memo off at the put and on again at the next name). Every other attribute is
    forwarded to the real client unchanged. Counters: real requests vs memo hits."""

    def __init__(self, real):
        self._real = real
        self.enabled = True
        self._memo = {}
        self.written = set()
        self.real_gets = 0
        self.memo_hits = 0
        self.other_calls = 0

    def __getattr__(self, name):
        attr = getattr(self._real, name)
        if callable(attr) and name != "get_object":
            def counted(*args, **kwargs):
                self.other_calls += 1
                return attr(*args, **kwargs)
            return counted
        return attr

    def get_object(self, **kwargs):
        bucket, key = kwargs.get("Bucket"), kwargs.get("Key")
        cacheable = (self.enabled and key is not None and key not in self.written
                     and any(m in key for m in MEMO_MARKERS) and "VersionId" not in kwargs)
        ident = (bucket, key, kwargs.get("Range"))
        if cacheable and ident in self._memo:
            self.memo_hits += 1
            meta, data = self._memo[ident]
            return dict(meta, Body=io.BytesIO(data))
        self.real_gets += 1
        resp = self._real.get_object(**kwargs)
        if not cacheable:
            return resp
        body = resp["Body"]
        data = body.read() if hasattr(body, "read") else body
        meta = {k: v for k, v in resp.items() if k != "Body"}
        self._memo[ident] = (meta, data)
        return dict(meta, Body=io.BytesIO(data))

    def requests(self):
        return self.real_gets + self.other_calls


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def norm(value):
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


def field_diffs(a, b, skip=()):
    out = []
    for k in sorted(set(a) | set(b)):
        if k in skip:
            continue
        x, y = a.get(k, ABSENT), b.get(k, ABSENT)
        if (x is ABSENT) != (y is ABSENT) or (x is not ABSENT and x != y):
            out.append(k)
    return out


def digest(value):
    return hashlib.sha256(json.dumps(norm(value), sort_keys=True, ensure_ascii=True).encode("ascii")).hexdigest()[:16]


def utc_text(value):
    if value is None:
        return None
    return value.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    st = (as_of if as_of in by_stamp else None) if as_of else max(by_stamp)
    if st is None:
        return None, None, dup
    newest = max(by_stamp[st], key=lambda r: (r["last_modified"] or "", r["key"]))
    return newest, st, dup


def list_rows(client, prefix):
    rows = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            rows.append({"key": obj["Key"], "last_modified": utc_text(obj.get("LastModified"))})
    return rows


def served_pick(rows):
    listed = [r for r in rows if r["key"].endswith(GATEWAY_SUFFIXES)]
    picked, _st, dup = pick_dossier(listed, None)
    return picked, dup


def read_doc(client, key):
    raw = gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client)
    if key.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def kind_of(key):
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


def input_kinds_differ(built_inputs, served_inputs):
    b = {json.dumps(e, sort_keys=True) for e in built_inputs}
    s = {json.dumps(e, sort_keys=True) for e in served_inputs}
    kinds = set()
    for text in b ^ s:
        kinds.add(kind_of(str(json.loads(text).get("key"))))
    return sorted(kinds)


def model_block_input_key(inputs):
    for e in inputs or []:
        if kind_of(str(e.get("key"))) == "model_block":
            return str(e.get("key"))
    return None


def rows_with_value(model_rows):
    """How a 'row with a value' is counted: model_rows is a list of row dicts; a row has a value when row['figure']['value']
    is not None. A model_rows that is not a list (the {'value': None, 'absent': ...} shape) counts 0."""
    if not isinstance(model_rows, list):
        return 0
    n = 0
    for row in model_rows:
        fig = row.get("figure") if isinstance(row, dict) else None
        if isinstance(fig, dict) and fig.get("value") is not None:
            n += 1
    return n


def in_manifest(name):
    if not os.path.exists(MANIFEST):
        return False
    return (" WROTE dossier name=%s " % name) in open(MANIFEST, encoding="ascii").read()


def manifest_append(line):
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def manifest_count():
    if not os.path.exists(MANIFEST):
        return 0
    return sum(1 for ln in open(MANIFEST, encoding="ascii") if " WROTE dossier name=" in ln)


def one(client, name, plan, names, expected):
    if name not in names:
        print("STOP: %s is not in the list; nothing written" % name)
        return 2
    if in_manifest(name):
        print("STOP: %s is already in the manifest" % name)
        return 2
    t0 = time.time()
    r0, h0 = client.requests(), client.memo_hits
    client.enabled = True
    partition = store.entity_partition("security_key", name)
    prefix = "%s%s/" % (gold.table_prefix(dossier.TABLE), partition)
    rows_before = list_rows(client, prefix)
    picked, dup = served_pick(rows_before)
    if picked is None:
        print("STOP: %s has no served dossier; nothing written" % name)
        return 4
    served_doc = read_doc(client, picked["key"])
    served_fields = norm(served_doc.get("fields") or {})
    served_inputs = norm(served_doc.get("inputs") or [])
    served_mb_key = model_block_input_key(served_inputs)
    served_stamp = dossier._model_block_stamp(name, served_mb_key) if served_mb_key else None
    print("NAME %s partition=%s objects_before=%d served=%s as_of_served=%s method=%s served_model_block_stamp=%s" % (
        name, partition, len(rows_before), picked["key"].rsplit("/", 1)[-1], served_doc.get("as_of"),
        served_doc.get("method_version"), served_stamp))
    built = dossier.build(name, client=client)
    built_fields = norm(built.get("fields") or {})
    built_inputs = norm(built.get("inputs") or [])
    moved = field_diffs(built_fields, served_fields)
    kinds = input_kinds_differ(built_inputs, served_inputs)
    exp = expected.get(name)
    print("COMPARE name=%s moved=%s expected=%s match_expected=%s input_kinds_differ=%s built_as_of=%s" % (
        name, ",".join(moved) or "none", ",".join(sorted(exp)) if exp is not None else "n/a",
        (set(moved) == exp) if exp is not None else "n/a", ",".join(kinds) or "none", built.get("as_of")))
    if not set(moved) <= ALLOWED_FIELDS or not set(kinds) <= ALLOWED_KINDS:
        print("STOP: %s a moved field outside %s or an input kind outside %s; nothing written" % (
            name, sorted(ALLOWED_FIELDS), sorted(ALLOWED_KINDS)))
        return 4
    if not moved:
        print("STOP: %s the build moves no field (the list is wrong); nothing written" % name)
        return 4
    # the CTO's model-block guard
    mb_doc, record = dossier._model_block_read(name, client)
    new_key = record.get("object_key")
    new_stamp = dossier._model_block_stamp(name, new_key)
    built_mb_key = model_block_input_key(built_inputs)
    old_cnt = rows_with_value(served_fields.get("model_rows"))
    new_cnt = rows_with_value(built_fields.get("model_rows"))
    moves_rows = "model_rows" in moved
    status = record.get("status")
    key_ok = (built_mb_key == new_key) if status == "SERVED" else (built_mb_key is None)
    if moves_rows:
        guard = status == "SERVED" and new_stamp is not None and (served_stamp is None or new_stamp > served_stamp) and new_cnt >= old_cnt
    else:
        guard = status == "SERVED" or served_mb_key is None
    print("GUARD name=%s moves_model_rows=%s record_status=%s new_stamp=%s served_stamp=%s rows_with_value_new=%d rows_with_value_served=%d "
          "build_block_key_equals_record=%s guard=%s" % (
              name, moves_rows, status, new_stamp, served_stamp, new_cnt, old_cnt, key_ok, "PASS" if (guard and key_ok) else "FAIL"))
    if not guard or not key_ok:
        print("STOP: %s the model-block guard fails; nothing written" % name)
        return 4
    if plan:
        print("PLAN-ONLY %s; nothing put" % name)
        return 0
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            result = dossier.write_one(name, client=client)
    except Exception as exc:  # noqa: BLE001
        print(buf.getvalue(), end="")
        print("STOP (write_one): %s: %s -- the bucket state for %s is UNKNOWN until read" % (type(exc).__name__, exc, name))
        return 5
    print(buf.getvalue(), end="")
    if not result.get("wrote"):
        print("STOP: %s write_one printed unchanged / wrote 0 (the list is wrong)" % name)
        return 4
    uri = result["uri"]
    key = uri[len("s3://%s/" % gold.HARVEST_BUCKET):]
    client.enabled = False  # AMENDMENT 2: nothing read after the first write of this name, nor the key written, is memoised
    client.written.add(key)
    m = re.search(r"put_performed (\d) existed (\d)", buf.getvalue())
    put_performed, existed = (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
    head = client.head_object(Bucket=gold.HARVEST_BUCKET, Key=key)
    body = gold.gold_get(uri, client=client)
    line = "%s WROTE dossier name=%s key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s moved=%s rows_with_value_served=%d rows_with_value_new=%d seconds=%d requests=%d memo_hits=%d" % (
        stamp(), name, key, head.get("VersionId"), len(body), hashlib.sha256(body).hexdigest(), put_performed, existed,
        ",".join(moved), old_cnt, new_cnt, int(time.time() - t0), client.requests() - r0, client.memo_hits - h0)
    manifest_append(line)
    print(line)
    if put_performed != 1 or existed != 0:
        print("STOP: %s put_performed %s existed %s" % (name, put_performed, existed))
        return 5
    rows_after = list_rows(client, prefix)
    count_ok = len(rows_after) == len(rows_before) + 1
    picked_after, dup_after = served_pick(rows_after)
    pick_ok = picked_after is not None and picked_after["key"] == key
    print("COUNT name=%s before=%d after=%d plus_one=%s pick_names_written_key=%s" % (
        name, len(rows_before), len(rows_after), "PASS" if count_ok else "FAIL", "PASS" if pick_ok else "FAIL"))
    got = json.loads(body.decode("utf-8"))
    problems = []
    if got.get("subject", {}).get("security_key") != name:
        problems.append("subject.security_key %r" % (got.get("subject"),))
    if got.get("method_version") != dossier.METHOD_VERSION:
        problems.append("method_version %r" % (got.get("method_version"),))
    got_fields = norm(got.get("fields") or {})
    other = field_diffs(got_fields, built_fields, skip=("model_rows",))
    if other:
        problems.append("fields other than model_rows differ from the pre-write build: %s" % ",".join(other))
    rows_equal = got_fields.get("model_rows") == built_fields.get("model_rows")
    got_cnt = rows_with_value(got_fields.get("model_rows"))
    if not rows_equal:
        problems.append("model_rows differ between the two builds (rows_with_value build1=%d stored=%d)" % (new_cnt, got_cnt))
    if moves_rows and got_cnt < old_cnt:
        problems.append("stored rows_with_value %d is lower than served %d" % (got_cnt, old_cnt))
    if norm(got.get("inputs")) != built_inputs:
        problems.append("inputs differ from the pre-write build's")
    rec = dict(got)
    stored_sha = rec.pop("content_sha256", None)
    if hashlib.sha256(dossier._canonical_bytes(rec)).hexdigest() != stored_sha:
        problems.append("recomputed content_sha256 != stored")
    want_name = "as_of=%s.%s.json" % (got.get("as_of"), dossier._inputs_sha16(got.get("inputs", [])))
    if key.rsplit("/", 1)[-1] != want_name:
        problems.append("object name %s != %s" % (key.rsplit("/", 1)[-1], want_name))
    if not count_ok:
        problems.append("partition count is not +1")
    if not pick_ok:
        problems.append("the gateway pick does not name the written key")
    for p in problems:
        print("READBACK-PROBLEM %s %s" % (name, p))
    ok = not problems
    print("READBACK name=%s fields=%d fields_digest=%s model_rows_equal_between_builds=%s equal=%s" % (
        name, len(got_fields), digest(got_fields), rows_equal, "PASS" if ok else "FAIL"))
    if not ok:
        manifest_append("%s READBACK-OR-COUNT-FAIL name=%s problems=%d" % (stamp(), name, len(problems)))
        return 6
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--go-utc")
    ap.add_argument("names", nargs="+")
    args = ap.parse_args(argv[1:])
    head = git("rev-parse", "HEAD")
    if not head.startswith(PIN) or git("diff", PIN, "HEAD", "--", "lib/research"):
        print("STOP: tree is not %s with an empty lib/research diff (HEAD %s)" % (PIN, head))
        return 2
    raw = open(NAMES_PATH, "rb").read()
    if hashlib.sha256(raw).hexdigest() != NAMES_SHA:
        print("STOP: the names list sha256 differs")
        return 2
    names = [ln.strip() for ln in raw.decode("ascii").splitlines() if ln.strip()]
    mraw = open(MOVES_PATH, "rb").read()
    if hashlib.sha256(mraw).hexdigest() != MOVES_SHA:
        print("STOP: the expected-moves sha256 differs")
        return 2
    expected = {}
    for ln in mraw.decode("ascii").splitlines():
        parts = ln.split()
        if len(parts) == 2:
            expected[parts[0]] = set(parts[1].split(","))
    if len(names) != 75 or len(expected) != 75:
        print("STOP: the lists hold %d names and %d moves, not 75" % (len(names), len(expected)))
        return 2
    if len(args.names) > 5 or len(set(args.names)) != len(args.names):
        print("STOP: at most 5 distinct names per command")
        return 2
    go = None
    if not args.plan:
        if not args.go_utc:
            print("STOP: a write needs --go-utc (the time of the issuer's GO)")
            return 2
        go = datetime.datetime.strptime(args.go_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        if not (go <= now() < go + datetime.timedelta(minutes=WINDOW_MIN)):
            print("STOP: now %s is outside the window %s to +%d minutes" % (stamp(), args.go_utc, WINDOW_MIN))
            return 3
    client = MemoClient(store._default_client())
    print("WINDOW-CHANGE: the write window end is %s (AMENDMENT 3, W1 msg 7970); it was 10:15:00Z; GO_UTC stays 07:45:00Z; MEMO of immutable get_object reads ON (AMENDMENT 2, W1 msg 7961)" % WINDOW_END_TEXT)
    print("=== cj4_run.py plan_only=%s start %s HEAD=%s names=%d manifest_lines=%d ===" % (args.plan, stamp(), head[:10], len(args.names), manifest_count()))
    for name in args.names:
        if go is not None and not (go <= now() < go + datetime.timedelta(minutes=WINDOW_MIN)):
            print("STOP: the window closed before %s" % name)
            return 3
        rc = one(client, name, args.plan, names, expected)
        if rc:
            print("=== batch STOPPED at %s rc=%d %s manifest_lines=%d ===" % (name, rc, stamp(), manifest_count()))
            return rc
    print("=== batch done %s manifest_lines=%d ===" % (stamp(), manifest_count()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
