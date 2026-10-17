"""IRPT_BCKEND workstream ~PS round 11 (issuer 2.0.0_SA_COO~S2) -- the check of one BUILD order: the reporting route serves the class_series object
(contract 0.4.0 `class_object`, written by a later cell of `~D2`) as one more `which` member, with the series file's gzip header.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. <repo_root> is the worker's worktree.

  IB251-1  IB-pr-620  `which=class_series` is a member of the reporting route
    AC1  the bound: the reporting tests pass, and the new test file exists with at least 6 tests naming class_series
    AC2  the behaviour: class_series is served from `account=<id>/class_series.json.gz` with Content-Encoding gzip, an uncovered account is refused before
         any storage call, a version_id on it is refused, a missing object is NOT_READY, manifest and series are unchanged, an unknown which is refused
    AC3  the seam + control: only entry.py and the new test file differ from the worker's branch point among source files, and the same AC2 behaviour run
         against the branch point's entry.py FAILS (the difference control)
"""
import base64
import importlib.util
import re
import subprocess
import sys
import types
from pathlib import Path

REP = "infra/aws/lambda/investor-reporting/reporting"
ENTRY = REP + "/entry.py"
NEWTEST = REP + "/tests/test_reporting_class_series.py"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("%s FAIL: %s" % (CID, msg))
    sys.exit(1)


def sh(args, cwd=None, timeout=110):
    return subprocess.run(args, cwd=str(cwd or ROOT), capture_output=True, text=True, timeout=timeout)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


class FakeS3:
    def __init__(self, objects):
        self.objects = objects
        self.gets = []
        self.lists = 0

    def get_object(self, Bucket, Key, **kw):
        self.gets.append(Key)
        if Key not in self.objects:
            raise ClientError("NoSuchKey")
        body, etag, enc = self.objects[Key]
        got = {"Body": types.SimpleNamespace(read=lambda: body), "ETag": etag}
        if enc:
            got["ContentEncoding"] = enc
        return got

    def get_paginator(self, name):
        outer = self

        class P:
            def paginate(self, Bucket, Prefix, Delimiter):
                outer.lists += 1
                seen = sorted({k[len(Prefix):].split("/", 1)[0] for k in outer.objects if k.startswith(Prefix)})
                yield {"CommonPrefixes": [{"Prefix": Prefix + s + "/"} for s in seen]}
        return P()


def behaviour(entry):
    """Returns a list of failure sentences (empty = the class_series member behaves)."""
    firm, raw, other = entry.default_firm(), "0010783709", "0000000001"
    bad = []
    if "class_series" not in getattr(entry, "OBJECTS", {}):
        return ["OBJECTS has no class_series member"]

    def key(r, w):
        return entry._split(entry._object_uri(firm, r, w))[1]

    if not key(raw, "class_series").endswith("/account=%s/class_series.json.gz" % raw):
        bad.append("the class_series key is not account=<id>/class_series.json.gz: %s" % key(raw, "class_series"))
    s3 = FakeS3({key(raw, "series"): (b"\x1f\x8bSERIES", '"es"', None), key(raw, "manifest"): (b'{"m":1}', '"em"', None),
                 key(raw, "class_series"): (b"\x1f\x8bCLASS", '"ec"', None)})
    entry._S3 = s3
    entry._RAW_BY_OPAQUE.clear()
    try:
        acc = entry._ids.opaque_account(firm, raw)
        ctx = types.SimpleNamespace(tenant=firm)

        def call(which, permitted, account=acc, query=None):
            event = {"pathParameters": {"account_id": account, "which": which}}
            if query:
                event["queryStringParameters"] = query
            return entry.reporting_read(None, {"permitted_account_set": permitted}, event, ctx)

        if entry.serve_series(raw, {raw}, "class_series") != b"\x1f\x8bCLASS":
            bad.append("serve_series did not return the class_series bytes")
        out = entry.http_response({"ok": True, "data": call("class_series", {acc})})
        if out.get("statusCode") != 200 or base64.b64decode(out["body"]) != b"\x1f\x8bCLASS":
            bad.append("the served class_series answer is not 200 with the object bytes")
        h = out.get("headers") or {}
        if h.get("Content-Encoding") != "gzip" or h.get("ETag") != '"ec"' or h.get("Content-Type") != "application/json":
            bad.append("class_series headers: want gzip, the ETag and application/json, got %r" % h)
        m = entry.http_response({"ok": True, "data": call("manifest", {acc})})
        if "Content-Encoding" in (m.get("headers") or {}):
            bad.append("manifest gained a Content-Encoding header")
        s = entry.http_response({"ok": True, "data": call("series", {acc})})
        if (s.get("headers") or {}).get("Content-Encoding") != "gzip":
            bad.append("series lost its gzip header")
        s3.gets.clear()
        s3.lists = 0
        try:
            call("class_series", {entry._ids.opaque_account(firm, other)})
            bad.append("an uncovered account was not refused")
        except entry.AccountNotCovered:
            if s3.gets or s3.lists:
                bad.append("an uncovered class_series account made a storage call")
        try:
            call("class_series", {acc}, query={"version_id": "abc123"})
            bad.append("a version_id on class_series was not refused")
        except entry.ReportingBadRequest:
            pass
        try:
            call("not_a_member", {acc})
            bad.append("an unknown which was not refused")
        except entry.ReportingBadRequest as e:
            if "class_series" not in str(e):
                bad.append("the unknown-which refusal does not list class_series")
        s3.objects.pop(key(raw, "class_series"))
        try:
            call("class_series", {acc})
            bad.append("a missing class_series object was not NOT_READY")
        except entry.ReportingNotReady:
            pass
    finally:
        entry._S3 = None
        entry._RAW_BY_OPAQUE.clear()
    return bad


def ac1():
    new = ROOT / NEWTEST
    if not new.is_file():
        fail("no %s" % NEWTEST)
    n = len(re.findall(r"^def test_[A-Za-z0-9_]*class_series[A-Za-z0-9_]*|^def test_", new.read_text(encoding="utf-8"), re.M))
    if n < 6:
        fail("the new test file holds %d tests; at least 6 are required" % n)
    p = sh([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"], cwd=ROOT / REP, timeout=115)
    out = p.stdout + p.stderr
    m = re.search(r"(\d+) passed", out)
    if p.returncode != 0 or not m or int(m.group(1)) < 39:
        fail("the reporting tests must pass with at least 39 passed (rc %d): %s" % (p.returncode, out[-300:].replace("\n", " | ")))
    print("OK: the reporting tests pass (%s passed), the new test file holds %d tests" % (m.group(1), n))


def ac2():
    bad = behaviour(load(ROOT / ENTRY, "entry_ut_251"))
    if bad:
        fail("; ".join(bad))
    print("OK: class_series is served from account=<id>/class_series.json.gz with gzip, refused uncovered before storage, version_id refused, missing NOT_READY, manifest and series unchanged")


def ac3():
    base = sh(["git", "merge-base", "HEAD", "box/dell2"]).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("cannot resolve the worker's branch point")
    changed = [f for f in sh(["git", "diff", "--name-only", base]).stdout.split() if f.startswith(("infra/", "lib/", ".tools/", "data/"))]
    others = [f for f in changed if f not in (ENTRY, NEWTEST) and "__pycache__" not in f]
    if others:
        fail("only %s and %s may differ from the branch point among source files; also differing: %s" % (ENTRY, NEWTEST, others[:5]))
    src = sh(["git", "show", "%s:%s" % (base, ENTRY)])
    if src.returncode != 0:
        fail("cannot read entry.py at the branch point")
    ctl = ROOT / REP / "entry_base_control_tmp.py"
    try:
        ctl.write_text(src.stdout, encoding="utf-8")
        if not behaviour(load(ctl, "entry_base_ctl_251")):
            fail("the difference control did not fail: the branch point's entry.py already passes the behaviour")
    finally:
        if ctl.exists():
            ctl.unlink()
    print("OK: only entry.py and the new test file differ; the branch point's entry.py fails the behaviour (the control)")


CHECKS = {"IB251-1-AC1": ac1, "IB251-1-AC2": ac2, "IB251-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p251_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT, CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
