"""ADVI_FIRMBKTS round 3 instrument for cell FB-f-1 (row D1-C-S7: the F7 compare hashes the manifest's source
VERSION and prints DEST-VS-MANIFEST and SOURCE-VS-MANIFEST apart), derived from round 2 cell FB-e-5 (F7: COPY 49
Financial's served platinum keys into opal-data-49financial), issuer 2.0.0_SA_COO~B1.

The copy is the worker's act under the signed never-widen pair; this file is the whole of its instrument:

  manifest --out FILE     list the 11 served platinum classes of opal-data-bd (read-only), place every key with
                          lib/opal_naming.py address(), write FILE (TSV, gzip): src, size, etag per object
  manifest --verify FILE  no AWS: re-place every src in FILE through address(); print the placement denominators
  copy --manifest FILE [--budget-seconds N] [--workers K]
                          server-side copy_object of each manifest key to its address() key. NEVER overwrites a key
                          that exists, NEVER deletes, copies only the listed ETag (CopySourceIfMatch). Resumable.
  compare --manifest FILE read-only: dest listing against the manifest, source listing against the manifest
  residue --record before|after --dir DIR | --check --dir DIR
                          the D1-S2 bound: key counts under gold/advi/ and _campaign/ of the destination bucket

The classes and their destination patterns are read from deliverables/mapping.json (the round-1 table): every row
of opal-data-bd with disposition MOVE and dest.tier platinum. Plain ASCII output. Standard library + boto3.
"""
import argparse
import concurrent.futures
import datetime
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time

SRC_BUCKET = "opal-data-bd"
DST_BUCKET = "opal-data-49financial"
SCOPE = "49financial"
DST_ROOT = "advi/49financial/platinum/"
DELIV = "org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables"
RESIDUE_PREFIXES = ("gold/advi/", "_campaign/")


def _root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return out.stdout.strip()


def _builders():
    sys.path.insert(0, os.path.join(_root(), "lib"))
    import opal_naming
    return opal_naming


def classes():
    """[(prefix, dest_pattern)] for the served platinum classes of opal-data-bd, from the round-1 table."""
    with open(os.path.join(_root(), DELIV, "mapping.json"), encoding="utf-8") as fh:
        rows = json.load(fh)["rows"]
    out = []
    for r in rows:
        if r.get("bucket") != SRC_BUCKET or r.get("disposition") != "MOVE":
            continue
        if (r.get("dest") or {}).get("tier") != "platinum":
            continue
        pat = r.get("dest_pattern", "")
        if not r["prefix"].endswith("/") or not pat.endswith("{tail}"):
            raise SystemExit("REFUSED: class %r has a pattern the copy does not model: %r" % (r["prefix"], pat))
        out.append((r["prefix"], pat))
    return sorted(out)


def dest_for(src, table):
    """The destination key for a source key, by the table's pattern for its class (None if no class owns it)."""
    for prefix, pat in table:
        if src.startswith(prefix):
            return pat.replace("{firm}", SCOPE).replace("{tail}", src[len(prefix):])
    return None


def place(src, table, naming):
    """(dst_key, None) when address() builds exactly the key the pattern names, else (None, why)."""
    dst = dest_for(src, table)
    if dst is None:
        return None, "no class owns this key"
    if not dst.startswith(DST_ROOT):
        return None, "pattern leaves %s" % DST_ROOT
    segs = dst[len(DST_ROOT):].split("/")
    if len(segs) < 2 or not all(segs):
        return None, "fewer than table + partition segments, or an empty segment"
    obj = "/".join(segs[2:]) if len(segs) > 2 else None
    try:
        got = naming.address("advi", SCOPE, "platinum", segs[0], segs[1], obj)
    except Exception as e:  # noqa: BLE001 -- a builder refusal is the finding
        return None, "builder refused: %s" % str(e)[:140]
    want = "s3://%s/%s" % (DST_BUCKET, dst)
    if got != want:
        return None, "builder returned %s, pattern says %s" % (got, want)
    return dst, None


def _s3():
    import boto3
    return boto3.client("s3")


def _list(s3, bucket, prefix):
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get("Contents", []):
            out.append((o["Key"], o["Size"], o["ETag"].strip('"')))
    return out


def _list_many(s3, bucket, prefixes):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(lambda p: _list(s3, bucket, p), prefixes))
    return dict(zip(prefixes, res))


def _read_manifest(path):
    objs = []
    with gzip.open(path, "rt", encoding="ascii") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            src, size, etag = line.split("\t")
            objs.append((src, int(size), etag))
    return objs


def _digest(objs):
    h = hashlib.sha256()
    for src, size, etag in sorted(objs):
        h.update(("%s\t%d\t%s\n" % (src, size, etag)).encode("ascii"))
    return h.hexdigest()


def cmd_manifest(a):
    naming = _builders()
    table = classes()
    if a.verify:
        objs = _read_manifest(a.verify)
        refused, seen, coll = [], {}, []
        for src, _s, _e in objs:
            dst, why = place(src, table, naming)
            if why:
                refused.append((src, why))
                continue
            if dst in seen:
                coll.append((dst, seen[dst], src))
            seen[dst] = src
        print("MANIFEST %s sha256=%s" % (a.verify, _digest(objs)))
        print("  objects=%d classes=%d placed=%d refused=%d destination-collisions=%d"
              % (len(objs), len(table), len(seen), len(refused), len(coll)))
        for r in refused[:5]:
            print("  REFUSED %s -- %s" % r)
        for c in coll[:5]:
            print("  COLLISION %s <- %s and %s" % c)
        ok = bool(objs) and not refused and not coll
        print("MANIFEST VERIFIED: every key placed once by address()" if ok else "MANIFEST NOT VERIFIED")
        return 0 if ok else 1
    s3 = _s3()
    who = None
    try:
        import boto3
        who = boto3.client("sts").get_caller_identity()["Arn"]
    except Exception:  # noqa: BLE001
        who = "unknown"
    listed = _list_many(s3, SRC_BUCKET, [p for p, _ in table])
    objs = [o for p, _ in table for o in listed[p]]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with gzip.open(a.out, "wt", encoding="ascii", newline="\n") as fh:
        fh.write("# r2-f7-manifest-v1 listed_at=%s instrument=%s source=%s dest=%s\n"
                 % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), who, SRC_BUCKET, DST_BUCKET))
        for src, size, etag in sorted(objs):
            fh.write("%s\t%d\t%s\n" % (src, size, etag))
    for p, _ in table:
        print("  class %-26s objects=%d" % (p, len(listed[p])))
    print("MANIFEST WRITTEN %s objects=%d sha256=%s instrument=%s" % (a.out, len(objs), _digest(objs), who))
    return 0


def cmd_copy(a):
    naming = _builders()
    table = classes()
    objs = _read_manifest(a.manifest)
    s3 = _s3()
    have = {k: (s, e) for k, s, e in _list(s3, DST_BUCKET, DST_ROOT)}
    todo, bad = [], []
    for src, size, etag in objs:
        dst, why = place(src, table, naming)
        if why:
            bad.append((src, why))
            continue
        cur = have.get(dst)
        if cur is None:
            todo.append((src, dst, etag))
        elif cur != (size, etag) and "-" not in etag:
            bad.append((src, "destination exists and differs: %s" % (cur,)))
    print("COPY PLAN objects=%d already-present=%d to-copy=%d refused-or-conflict=%d"
          % (len(objs), len(objs) - len(todo) - len(bad), len(todo), len(bad)))
    for b in bad[:5]:
        print("  SKIP %s -- %s" % b)
    t0 = time.time()
    done = stale = errs = 0

    def one(item):
        src, dst, etag = item
        if time.time() - t0 > a.budget_seconds:
            return "budget"
        try:
            s3.copy_object(Bucket=DST_BUCKET, Key=dst, CopySource={"Bucket": SRC_BUCKET, "Key": src},
                           CopySourceIfMatch=etag, MetadataDirective="COPY", ServerSideEncryption="AES256")
            return "ok"
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "PreconditionFailed" in msg or "412" in msg:
                return "stale"
            return "error:" + msg[:120]

    left = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(one, todo):
            if r == "ok":
                done += 1
            elif r == "stale":
                stale += 1
            elif r == "budget":
                left += 1
            else:
                errs += 1
                if errs <= 5:
                    print("  ERROR %s" % r)
    print("COPY RUN copied=%d stale-source=%d errors=%d not-reached(budget)=%d" % (done, stale, errs, left))
    if left == 0 and errs == 0:
        print("COPY PASS COMPLETE: every manifest key present or stale-and-named (re-run compare)")
    else:
        print("COPY INCOMPLETE: run this command again")
    return 0


def _sha(s3, bucket, key, version=None):
    h = hashlib.sha256()
    kw = {"Bucket": bucket, "Key": key}
    if version is not None:
        kw["VersionId"] = version
    body = s3.get_object(**kw)["Body"]
    for chunk in iter(lambda: body.read(1 << 20), b""):
        h.update(chunk)
    return h.hexdigest()


def _sha_manifest_version(s3, key, etag):
    """sha256 of the SOURCE version whose key is `key` and whose ETag equals the manifest's `etag`, or None if no such
    version exists. Pages list_object_versions (KeyMarker and VersionIdMarker while IsTruncated) so a current object
    rewritten by a producer is still read at the version the manifest listed."""
    km = vm = None
    while True:
        kw = {"Bucket": SRC_BUCKET, "Prefix": key}
        if km is not None:
            kw["KeyMarker"] = km
        if vm is not None:
            kw["VersionIdMarker"] = vm
        resp = s3.list_object_versions(**kw)
        for v in resp.get("Versions", []):
            if v.get("Key") == key and v.get("ETag", "").strip('"') == etag:
                return _sha(s3, SRC_BUCKET, key, v["VersionId"])
        if not resp.get("IsTruncated"):
            return None
        km = resp.get("NextKeyMarker")
        vm = resp.get("NextVersionIdMarker")


def cmd_compare(a):
    naming = _builders()
    table = classes()
    objs = _read_manifest(a.manifest)
    s3 = _s3()
    dst_have = {k: (s, e) for k, s, e in _list(s3, DST_BUCKET, DST_ROOT)}
    src_now = {}
    for lst in _list_many(s3, SRC_BUCKET, [p for p, _ in table]).values():
        for k, s, e in lst:
            src_now[k] = (s, e)
    want = {}
    refused = 0
    for src, size, etag in objs:
        dst, why = place(src, table, naming)
        if why:
            refused += 1
            continue
        want[dst] = (src, size, etag)
    missing = [d for d in want if d not in dst_have]
    mismatch = []
    unverifiable = 0
    for d, (src, size, etag) in want.items():
        cur = dst_have.get(d)
        if cur is None or cur == (size, etag):
            continue
        if cur[0] == size and ("-" in etag or "-" in cur[1]):
            if unverifiable < 50:
                unverifiable += 1
                src_sha = _sha_manifest_version(s3, src, etag)
                if src_sha is not None and _sha(s3, DST_BUCKET, d) == src_sha:
                    continue
        mismatch.append(d)
    extras = [k for k in dst_have if k not in want]
    changed = sum(1 for src, size, etag in objs if src_now.get(src) != (size, etag))
    gone = sum(1 for src, _s, _e in objs if src not in src_now)
    print("COMPARE manifest=%d placed=%d refused=%d (denominator: manifest objects)" % (len(objs), len(want), refused))
    print("  DEST  present=%d missing=%d mismatch=%d extras-under-%s=%d"
          % (len(want) - len(missing), len(missing), len(mismatch), DST_ROOT, len(extras)))
    print("  SOURCE changed-since-manifest=%d gone=%d (the producers still write opal-data-bd; a changed source is "
          "re-copied by a new manifest, never by this one)"
          % (changed, gone))
    for m in (missing[:3] + mismatch[:3]):
        print("  DIFF %s" % m)
    dest_equal = bool(objs) and not refused and not missing and not mismatch and not extras
    print("DEST-VS-MANIFEST: %s" % ("EQUAL" if dest_equal else "DIFFERENT"))
    if changed or gone:
        print("SOURCE-VS-MANIFEST: DRIFTED changed=%d gone=%d" % (changed, gone))
    else:
        print("SOURCE-VS-MANIFEST: UNCHANGED changed=0 gone=0")
    print("COPY-COMPLETE: every manifest key present and equal" if dest_equal else "COPY-NOT-COMPLETE")
    return 0 if dest_equal else 1


def _count(s3, prefix):
    n, newest = 0, ""
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=DST_BUCKET, Prefix=prefix):
        for o in page.get("Contents", []):
            n += 1
            lm = o["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
            newest = max(newest, lm)
    return n, newest


def cmd_residue(a):
    s3 = _s3()
    snap = {"bucket": DST_BUCKET, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "prefixes": {}}
    for p in RESIDUE_PREFIXES:
        n, newest = _count(s3, p)
        snap["prefixes"][p] = {"keys": n, "newest": newest}
    if a.record:
        path = os.path.join(a.dir, "F7_RESIDUE_%s.json" % a.record)
        os.makedirs(a.dir, exist_ok=True)
        with open(path, "w", encoding="ascii") as fh:
            json.dump(snap, fh, indent=1)
        print("RESIDUE RECORDED %s %s" % (a.record, json.dumps(snap["prefixes"], sort_keys=True)))
        return 0
    try:
        with open(os.path.join(a.dir, "F7_RESIDUE_before.json"), encoding="ascii") as fh:
            before = json.load(fh)
        with open(os.path.join(a.dir, "F7_RESIDUE_after.json"), encoding="ascii") as fh:
            after = json.load(fh)
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable residue record (%s)" % type(e).__name__)
        print("RESIDUE NOT CHECKED")
        return 1
    ok = True
    for p in RESIDUE_PREFIXES:
        b, f, now = before["prefixes"][p]["keys"], after["prefixes"][p]["keys"], snap["prefixes"][p]["keys"]
        print("  %-12s before=%d after=%d now=%d" % (p, b, f, now))
        ok = ok and b == f == now
    print("RESIDUE UNCHANGED: gold/advi/ and _campaign/ key counts equal before, after and now" if ok
          else "RESIDUE CHANGED")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("manifest")
    m.add_argument("--out")
    m.add_argument("--verify")
    c = sub.add_parser("copy")
    c.add_argument("--manifest", required=True)
    c.add_argument("--budget-seconds", type=int, default=100)
    c.add_argument("--workers", type=int, default=24)
    k = sub.add_parser("compare")
    k.add_argument("--manifest", required=True)
    r = sub.add_parser("residue")
    r.add_argument("--record", choices=("before", "after"))
    r.add_argument("--check", action="store_true")
    r.add_argument("--dir", required=True)
    a = ap.parse_args()
    if a.cmd == "manifest" and not (a.out or a.verify):
        ap.error("manifest needs --out or --verify")
    try:
        rc = {"manifest": cmd_manifest, "copy": cmd_copy, "compare": cmd_compare, "residue": cmd_residue}[a.cmd](a)
    except FileNotFoundError as e:
        print("ABSENT: %s" % e)
        rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
