"""r3_f7_delta.py -- ADVI_FIRMBKTS FB-f-10 DELTA_TOOL (window act 3), issuer 2.0.0_SA_COO~B1.

Brings the destination of the F7 copy equal to a FRESH manifest of the served classes of opal-data-bd. Unlike
r3_f7.py copy (which never overwrites), this tool OVERWRITES a destination key that differs from the manifest, so it is
the one place an overwrite can happen, and it refuses to do that without a per-key rollback.

  plan    --manifest F --keep-newer-than ISO   read-only. Classifies every manifest object against the destination
                                          listing: ABSENT, EQUAL, DIFFERS (present, not equal, last modified at or
                                          before ISO: an overwrite), KEPT-NEWER (present, not equal, last modified AFTER
                                          ISO: a producer's own write under `canonical`, NEVER overwritten), REFUSED (no
                                          class or address() refuses the key); reports destination versioning and the
                                          source keys that changed since the manifest (a stale source is never copied).
                                          ISO is the instant the mode moved: it is required, there is no default.
  apply   --manifest F --keep-newer-than ISO --dir D [--execute] [--budget-seconds N] [--workers K]
                                          without --execute: the plan and 'DRY RUN: no write'. With --execute: refuses
                                          unless destination versioning is Enabled (when any key DIFFERS); records every
                                          overwritten key's prior VersionId, ETag and size to D/F7_DELTA_ROLLBACK.tsv
                                          BEFORE the first write; copies absent and differing keys with
                                          CopySourceIfMatch on the manifest ETag; deletes nothing; resumable.
  rollback --record F [--execute]         restores each recorded key to its recorded prior version (copy of that
                                          version over the key); dry-run without --execute.
  selftest                                no AWS: six cases against a fake client; prints SELFTEST PASS n of n.

Plain ASCII; no key (a client id) is printed, only counts. Standard library + boto3 (via r3_f7).
"""
import argparse
import concurrent.futures
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r3_f7 as f7  # noqa: E402


def classify(objs, table, naming, have, s3=None, newer=None):
    """Return dict of lists: absent, equal, differs, kept_newer, refused. `have` maps dst -> (size, etag); `newer` is the
    set of destination keys last modified after the mode-move instant (a producer's own write: never overwritten)."""
    newer = newer or set()
    out = {"absent": [], "equal": [], "differs": [], "kept_newer": [], "refused": []}
    for src, size, etag in objs:
        dst, why = f7.place(src, table, naming)
        if why:
            out["refused"].append((src, why))
            continue
        cur = have.get(dst)
        if cur is None:
            out["absent"].append((src, dst, etag))
        elif cur == (size, etag):
            out["equal"].append((src, dst, etag))
        elif cur[0] == size and ("-" in etag or "-" in cur[1]) and s3 is not None:
            src_sha = f7._sha_manifest_version(s3, src, etag)
            if src_sha is not None and f7._sha(s3, f7.DST_BUCKET, dst) == src_sha:
                out["equal"].append((src, dst, etag))
            else:
                out["kept_newer" if dst in newer else "differs"].append((src, dst, etag))
        else:
            out["kept_newer" if dst in newer else "differs"].append((src, dst, etag))
    return out


def _versioning(s3):
    try:
        return s3.get_bucket_versioning(Bucket=f7.DST_BUCKET).get("Status", "None")
    except Exception as e:  # noqa: BLE001 -- a read that cannot run is not 'Enabled'
        return "UNREADABLE:" + type(e).__name__


def _parse_iso(s):
    import datetime
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)


def _list_dest(s3, cutoff):
    """(have, newer): destination key -> (size, etag), and the keys last modified after `cutoff`."""
    have, newer = {}, set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=f7.DST_BUCKET, Prefix=f7.DST_ROOT):
        for o in page.get("Contents", []):
            have[o["Key"]] = (o["Size"], o["ETag"].strip('"'))
            if o["LastModified"] > cutoff:
                newer.add(o["Key"])
    return have, newer


def _plan(manifest, s3, naming, table, cutoff):
    objs = f7._read_manifest(manifest)
    have, newer = _list_dest(s3, cutoff)
    src_now = {}
    for lst in f7._list_many(s3, f7.SRC_BUCKET, [p for p, _ in table]).values():
        for k, s, e in lst:
            src_now[k] = (s, e)
    c = classify(objs, table, naming, have, s3, newer)
    stale = sum(1 for src, size, etag in objs if src_now.get(src) != (size, etag))
    return objs, c, stale


def _print_plan(objs, c, stale, ver):
    print("DELTA PLAN objects=%d absent=%d equal=%d differs=%d kept-newer=%d refused=%d (denominator: manifest objects)"
          % (len(objs), len(c["absent"]), len(c["equal"]), len(c["differs"]), len(c["kept_newer"]), len(c["refused"])))
    print("  OVERWRITES=%d destination-versioning=%s source-changed-since-manifest=%d" % (len(c["differs"]), ver, stale))
    if not c["absent"] and not c["differs"] and not c["refused"]:
        print("DELTA PLAN: NOTHING TO DO (every manifest key present and equal)")


def cmd_plan(a):
    s3, naming, table = f7._s3(), f7._builders(), f7.classes()
    objs, c, stale = _plan(a.manifest, s3, naming, table, _parse_iso(a.keep_newer_than))
    _print_plan(objs, c, stale, _versioning(s3))
    return 0 if not c["refused"] else 1


def cmd_apply(a):
    s3, naming, table = f7._s3(), f7._builders(), f7.classes()
    objs, c, stale = _plan(a.manifest, s3, naming, table, _parse_iso(a.keep_newer_than))
    ver = _versioning(s3)
    _print_plan(objs, c, stale, ver)
    if c["refused"]:
        print("REFUSED: %d manifest object(s) have no placement; nothing written" % len(c["refused"]))
        return 1
    if not a.execute:
        print("DRY RUN: no write")
        return 0
    if c["differs"] and ver != "Enabled":
        print("REFUSED: %d overwrite(s) and destination versioning is %s; no per-key rollback exists, nothing written"
              % (len(c["differs"]), ver))
        return 1
    os.makedirs(a.dir, exist_ok=True)
    rec = os.path.join(a.dir, "F7_DELTA_ROLLBACK.tsv")
    with open(rec, "a", encoding="ascii", newline="\n") as fh:
        for src, dst, etag in c["differs"]:
            try:
                h = s3.head_object(Bucket=f7.DST_BUCKET, Key=dst)
                fh.write("%s\t%s\t%s\t%d\n" % (dst, h.get("VersionId", "null"), h["ETag"].strip('"'), h["ContentLength"]))
            except Exception as e:  # noqa: BLE001 -- no prior version recorded means no write to that key
                print("REFUSED: prior version of an overwrite key not readable (%s); nothing written" % type(e).__name__)
                return 1
        fh.flush()
        os.fsync(fh.fileno())
    print("ROLLBACK RECORD %s rows=%d" % (rec, len(c["differs"])))
    todo = c["absent"] + c["differs"]
    t0 = time.time()

    def one(item):
        src, dst, etag = item
        if time.time() - t0 > a.budget_seconds:
            return "budget"
        try:
            s3.copy_object(Bucket=f7.DST_BUCKET, Key=dst, CopySource={"Bucket": f7.SRC_BUCKET, "Key": src},
                           CopySourceIfMatch=etag, MetadataDirective="COPY", ServerSideEncryption="AES256")
            return "ok"
        except Exception as e:  # noqa: BLE001
            m = str(e)
            return "stale" if ("PreconditionFailed" in m or "412" in m) else "error:" + m[:100]

    done = stale_n = errs = left = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(one, todo):
            if r == "ok":
                done += 1
            elif r == "stale":
                stale_n += 1
            elif r == "budget":
                left += 1
            else:
                errs += 1
    print("DELTA RUN copied=%d stale-source=%d errors=%d not-reached(budget)=%d" % (done, stale_n, errs, left))
    print("DELTA COMPLETE: re-run plan" if (left == 0 and errs == 0) else "DELTA INCOMPLETE: run this command again")
    return 0 if errs == 0 else 1


def cmd_rollback(a):
    s3 = f7._s3()
    rows = []
    with open(a.record, encoding="ascii") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line:
                dst, vid, etag, size = line.split("\t")
                rows.append((dst, vid, etag, int(size)))
    print("ROLLBACK PLAN rows=%d" % len(rows))
    if not a.execute:
        print("DRY RUN: no write")
        return 0
    ok = bad = 0
    for dst, vid, _etag, _size in rows:
        try:
            s3.copy_object(Bucket=f7.DST_BUCKET, Key=dst, CopySource={"Bucket": f7.DST_BUCKET, "Key": dst, "VersionId": vid},
                           MetadataDirective="COPY", ServerSideEncryption="AES256")
            ok += 1
        except Exception:  # noqa: BLE001
            bad += 1
    print("ROLLBACK RUN restored=%d errors=%d" % (ok, bad))
    return 0 if bad == 0 else 1


class _Fake:
    """Just enough of an S3 client for the self-test: a destination dict and a copy log."""

    def __init__(self, dest, versions):
        self.dest, self.versions, self.copies = dest, versions, []

    def head_object(self, Bucket, Key):
        s, e = self.dest[Key]
        return {"VersionId": self.versions.get(Key, "v0"), "ETag": '"%s"' % e, "ContentLength": s}

    def copy_object(self, Bucket, Key, CopySource, **kw):
        if kw.get("CopySourceIfMatch") == "STALE":
            raise RuntimeError("PreconditionFailed 412")
        self.copies.append((Key, CopySource.get("VersionId"), kw.get("CopySourceIfMatch")))


def cmd_selftest(a):
    table = [("gold/artifacts/", "advi/49financial/platinum/artifacts/{tail}")]

    class _N:
        @staticmethod
        def address(domain, scope, tier, table_, part, obj):
            return "s3://%s/advi/49financial/platinum/%s/%s/%s" % (f7.DST_BUCKET, table_, part, obj)

    objs = [("gold/artifacts/x/a.json", 10, "e1"), ("gold/artifacts/x/b.json", 10, "e2"),
            ("gold/artifacts/x/c.json", 10, "e3"), ("elsewhere/z.json", 5, "e9")]
    pre = f7.DST_ROOT
    have = {pre + "artifacts/x/b.json": (10, "e2"), pre + "artifacts/x/c.json": (10, "OLD")}
    objs.append(("gold/artifacts/x/d.json", 10, "e4"))
    have[pre + "artifacts/x/d.json"] = (10, "FRESH")
    cl = classify(objs, table, _N, have, None, {pre + "artifacts/x/d.json"})
    checks = []
    checks.append(("absent key classified ABSENT", [o[0] for o in cl["absent"]] == ["gold/artifacts/x/a.json"]))
    checks.append(("equal key classified EQUAL and not copied", [o[0] for o in cl["equal"]] == ["gold/artifacts/x/b.json"]))
    checks.append(("differing key classified DIFFERS (an overwrite)", [o[0] for o in cl["differs"]] == ["gold/artifacts/x/c.json"]))
    checks.append(("a differing key written after the mode move is KEPT-NEWER, never an overwrite",
                   [o[0] for o in cl["kept_newer"]] == ["gold/artifacts/x/d.json"]
                   and "gold/artifacts/x/d.json" not in [o[0] for o in cl["differs"]]))
    checks.append(("a key no class owns is REFUSED, not copied", [o[0] for o in cl["refused"]] == ["elsewhere/z.json"]))
    fk = _Fake({pre + "artifacts/x/c.json": (10, "OLD")}, {pre + "artifacts/x/c.json": "VER7"})
    h = fk.head_object(f7.DST_BUCKET, pre + "artifacts/x/c.json")
    checks.append(("a prior VersionId is readable before an overwrite", h["VersionId"] == "VER7" and h["ETag"] == '"OLD"'))
    try:
        fk.copy_object(Bucket="b", Key="k", CopySource={"Bucket": "s", "Key": "k"}, CopySourceIfMatch="STALE")
        stale_refused = False
    except RuntimeError:
        stale_refused = True
    checks.append(("a copy whose source ETag changed is refused by the precondition", stale_refused and not fk.copies))
    n = 0
    for name, ok in checks:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
        n += 1 if ok else 0
    print("SELFTEST %s %d of %d" % ("PASS" if n == len(checks) else "FAIL", n, len(checks)))
    return 0 if n == len(checks) else 1


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan")
    p.add_argument("--manifest", required=True)
    p.add_argument("--keep-newer-than", required=True)
    q = sub.add_parser("apply")
    q.add_argument("--manifest", required=True)
    q.add_argument("--keep-newer-than", required=True)
    q.add_argument("--dir", required=True)
    q.add_argument("--execute", action="store_true")
    q.add_argument("--budget-seconds", type=int, default=100)
    q.add_argument("--workers", type=int, default=24)
    r = sub.add_parser("rollback")
    r.add_argument("--record", required=True)
    r.add_argument("--execute", action="store_true")
    sub.add_parser("selftest")
    a = ap.parse_args()
    sys.exit({"plan": cmd_plan, "apply": cmd_apply, "rollback": cmd_rollback, "selftest": cmd_selftest}[a.cmd](a))


if __name__ == "__main__":
    main()
