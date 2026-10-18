"""HVST-ch-7 driver, run from the pinned worktree (C:/tmp/ch7-build at 091ebacda9). ASCII only.

Usage (always foreground, always `python -u`; the caller appends the output to ch7_run.log):
  python -u ch7_run.py --plan NAME [NAME ...]                       read only: pre-write comparison per name, nothing put
  python -u ch7_run.py --go-utc 2026-10-18T05:02:00Z NAME [NAME ...]  for each name in the order given: compare, write, read back, manifest
There is NO loop over the list, NO retry and NO background mode (COO half C-5). A name not in the list is a STOP. The driver
never calls dossier.write_one, never runs any module --write, and never calls etfs_compare_peers (C-6, C-9). The write window
is the issuer's GO (--go-utc) to GO+120 minutes; outside it the driver refuses. At the first anomaly it stops the batch.

Per name: (1) the served continuation is the gateway's pick (newest .json/.json.gz by LastModified then key) and must NOT already
be at the current method; continuation.build() in memory must have fields EQUAL (parsed values) to the served fields and the
same inputs; the new object must not exist; (2) continuation.write_one(name); (3) read back (Branch A); (4) the manifest line is
appended and fsynced BEFORE the read-back and before the next name.
"""
from __future__ import annotations

import argparse
import datetime
import gzip
import hashlib
import json
import os
import subprocess
import sys

WT = r"C:\tmp\ch7-build"
sys.path.insert(0, WT)
os.chdir(WT)

from lib.research.corpus import continuation, gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402

PIN = "091ebacda9"
ROUND = r"C:\dev\ajb_workspace\org\missions\D5\AMGT\AMGT_HARVST\deliverables"
OUT = ROUND + r"\0.7.0_AE_CloudOps~SC1\round93"
LIST_PATH = ROUND + r"\2.0.0_SA_COO_W1\round93\ch7_securities.txt"
LIST_SHA = "db965262ed4c02179c43bb8346a5c4d24953cc638b669c6a354dff36fae698ac"
MANIFEST = os.path.join(OUT, "ch7_written.out")
CURRENT = continuation.METHOD_VERSION
WINDOW_MIN = 120


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def stamp():
    return now().strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args):
    return subprocess.run(["git", "-C", WT] + list(args), capture_output=True, text=True, check=True).stdout.strip()


def norm(value):
    return json.loads(json.dumps(value, sort_keys=True, ensure_ascii=True))


def digest(value):
    return hashlib.sha256(json.dumps(norm(value), sort_keys=True, ensure_ascii=True).encode("ascii")).hexdigest()[:16]


def field_diffs(a, b):
    return [k for k in sorted(set(a) | set(b)) if (k in a) != (k in b) or a.get(k) != b.get(k)]


def list_objects(client, prefix):
    out = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=gold.HARVEST_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []) or []:
            out.append((obj["Key"], obj.get("LastModified")))
    return out


def gateway_pick(objects):
    rows = [{"key": k, "lm": (lm.isoformat() if lm is not None else "")} for k, lm in objects if k.endswith((".json", ".json.gz"))]
    if not rows:
        return None
    return max(rows, key=lambda r: (r["lm"], r["key"]))["key"]


def read_doc(client, key):
    raw = gold.gold_get("s3://%s/%s" % (gold.HARVEST_BUCKET, key), client=client)
    if key.endswith(".gz"):
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def in_manifest(name):
    if not os.path.exists(MANIFEST):
        return False
    return (" WROTE cont name=%s " % name) in open(MANIFEST, encoding="ascii").read()


def manifest_append(line):
    with open(MANIFEST, "a", encoding="ascii") as fh:
        fh.write(line + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def manifest_count():
    if not os.path.exists(MANIFEST):
        return 0
    return sum(1 for ln in open(MANIFEST, encoding="ascii") if " WROTE cont name=" in ln)


def readback(client, name, uri, built, served_doc):
    got = json.loads(gold.gold_get(uri, client=client).decode("utf-8"))
    problems = []
    if got.get("subject", {}).get("security_key") != name:
        problems.append("subject.security_key %r" % (got.get("subject"),))
    if got.get("method_version") != CURRENT:
        problems.append("method_version %r" % (got.get("method_version"),))
    if norm(got.get("fields")) != norm(built["fields"]):
        problems.append("fields differ from the build: %s" % ",".join(field_diffs(norm(got.get("fields") or {}), norm(built["fields"]))))
    if norm(got.get("inputs")) != norm(served_doc.get("inputs")):
        problems.append("inputs differ from the served object's")
    rec = dict(got)
    stored_sha = rec.pop("content_sha256", None)
    if hashlib.sha256(continuation._canonical_bytes(rec)).hexdigest() != stored_sha:
        problems.append("recomputed content_sha256 != stored")
    if uri.rsplit("/", 1)[-1] != "%s.json" % continuation._inputs_sha16(got.get("inputs", [])):
        problems.append("object name != _inputs_sha16(inputs)")
    for p in problems:
        print("READBACK-PROBLEM %s %s" % (name, p))
    ok = not problems
    print("READBACK name=%s fields=%d fields_digest=%s equal=%s" % (name, len(got.get("fields") or {}), digest(got.get("fields")), "PASS" if ok else "FAIL"))
    return ok


def one(client, name, plan, listed):
    if name not in listed:
        print("STOP: %s is not in the list; nothing written" % name)
        return 2
    if in_manifest(name):
        print("STOP: %s is already in the manifest" % name)
        return 2
    partition = store.entity_partition("security_key", name)
    prefix = "%s%s/" % (gold.table_prefix(continuation.TABLE), partition)
    objects = list_objects(client, prefix)
    served_key = gateway_pick(objects)
    if served_key is None:
        print("STOP: %s has no served continuation; nothing written" % name)
        return 4
    served_doc = read_doc(client, served_key)
    print("NAME %s partition=%s objects_before=%d served=%s method=%s" % (name, partition, len(objects), served_key.rsplit("/", 1)[-1], served_doc.get("method_version")))
    if served_doc.get("method_version") == CURRENT:
        print("STOP: %s is already served at %s (the list is wrong); nothing written" % (name, CURRENT))
        return 4
    built = continuation.build(name, client=client)
    diffs = field_diffs(norm(built["fields"]), norm(served_doc.get("fields") or {}))
    inputs_equal = norm(built["inputs"]) == norm(served_doc.get("inputs"))
    new_name = "%s.json" % continuation._inputs_sha16(built["inputs"])
    new_key = prefix + new_name
    exists = any(k == new_key for k, _lm in objects)
    print("COMPARE name=%s fields=%d changed=%d list=%s inputs_equal=%s new_object=%s exists=%s served_fields_digest=%s built_fields_digest=%s" % (
        name, len(built["fields"]), len(diffs), ",".join(diffs) or "none", inputs_equal, new_name, exists,
        digest(served_doc.get("fields")), digest(built["fields"])))
    if diffs or not inputs_equal or exists:
        print("STOP: %s pre-write comparison differs (fields changed %d, inputs_equal %s, exists %s); nothing written" % (name, len(diffs), inputs_equal, exists))
        return 4
    if plan:
        print("PLAN-ONLY %s; nothing put" % name)
        return 0
    try:
        document, result, _source_type = continuation.write_one(name, client=client)
    except Exception as exc:  # noqa: BLE001
        print("STOP (write_one): %s: %s -- the bucket state for %s is UNKNOWN until read" % (type(exc).__name__, exc, name))
        return 5
    head_obj = client.head_object(Bucket=result["bucket"], Key=result["key"])
    line = "%s WROTE cont name=%s key=%s VersionId=%s bytes=%d sha256=%s put_performed=%s existed=%s" % (
        stamp(), name, result["key"], head_obj.get("VersionId"), result["content_length"], result["sha256"],
        result["put_performed"], result["existed"])
    manifest_append(line)
    print(line)
    if not result["put_performed"] or result["existed"]:
        print("STOP: %s put_performed %s existed %s" % (name, result["put_performed"], result["existed"]))
        return 5
    if result["key"] != new_key:
        print("STOP: %s wrote %s, expected %s" % (name, result["key"], new_key))
        return 5
    after = list_objects(client, prefix)
    count_ok = len(after) == len(objects) + 1
    print("COUNT name=%s before=%d after=%d plus_one=%s" % (name, len(objects), len(after), "PASS" if count_ok else "FAIL"))
    ok = readback(client, name, result["uri"], built, served_doc)
    if not ok or not count_ok:
        manifest_append("%s READBACK-OR-COUNT-FAIL name=%s readback=%s plus_one=%s" % (stamp(), name, ok, count_ok))
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
    raw = open(LIST_PATH, "rb").read()
    if hashlib.sha256(raw).hexdigest() != LIST_SHA:
        print("STOP: the list sha256 differs")
        return 2
    listed = [ln.strip() for ln in raw.decode("ascii").splitlines() if ln.strip()]
    if len(listed) != 78:
        print("STOP: the list holds %d names, not 78" % len(listed))
        return 2
    if len(args.names) > 10 or len(set(args.names)) != len(args.names):
        print("STOP: at most 10 distinct names per command")
        return 2
    if not args.plan:
        if not args.go_utc:
            print("STOP: a write needs --go-utc (the time of the issuer's GO)")
            return 2
        go = datetime.datetime.strptime(args.go_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
        if not (go <= now() < go + datetime.timedelta(minutes=WINDOW_MIN)):
            print("STOP: now %s is outside the window %s to +%d minutes" % (stamp(), args.go_utc, WINDOW_MIN))
            return 3
    client = store._default_client()
    print("=== ch7_run.py plan_only=%s start %s HEAD=%s names=%d manifest_lines=%d ===" % (args.plan, stamp(), head[:10], len(args.names), manifest_count()))
    for name in args.names:
        if not args.plan and not (go <= now() < go + datetime.timedelta(minutes=WINDOW_MIN)):
            print("STOP: the window closed before %s" % name)
            return 3
        rc = one(client, name, args.plan, listed)
        if rc:
            print("=== batch STOPPED at %s rc=%d %s manifest_lines=%d ===" % (name, rc, stamp(), manifest_count()))
            return rc
    print("=== batch done %s manifest_lines=%d ===" % (stamp(), manifest_count()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
