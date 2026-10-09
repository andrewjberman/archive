"""r1_emit.py -- MDPF_CANON round 1, cell CN-a-2 (issuer 2.0.0_SA_COO~D1): THE ONE PARQUET WRITER.

Usage (repo root of the checkout under test): python <this file>

PRD v2.9 CONTRACTS (the key string, the gold artifact, the firm gold writer), DEC-2 (parquet per day, the vintage in
the key, history never rewritten, no second write path) and M16 (a run made partial on purpose cannot read PASS).
Module under test: data/mdpf/scripts/gold/mdpf_gold_parquet.py, its interface fixed by the order:
  ARTIFACTS                                   the four snake_case artifacts
  partition_uri(scope, artifact, date)         -> address("mdpf", scope, "gold", artifact, f"date={date}", object="data.parquet")
  client_for_scope(scope, boto3_module=None)   -> an S3 client; a firm scope assumes os.environ["GOLD_WRITER_ROLE_ARN_<SCOPE>"]
                                                  through sts and REFUSES (raises) when it is unset; "global" uses its own
  write_partition(s3, scope, artifact, date, records) -> "written" | "unchanged" | "conflict"; never overwrites
  run_status(intended_scopes, built_scopes)    -> "PASS" only when every intended scope was built, else "PARTIAL"
Nothing here touches AWS: the S3 client and the boto3 module are in-memory fakes.

Arms:
  1 KEYS       every scope (49financial, inflection, cottonwood, global) x artifact: partition_uri == address(...).
  2 UNTYPED    the module's source carries no "s3://" and no "opal-data-" literal (every address from the builders).
  3 WRITE ONCE first write "written"; the same records again "unchanged" with no second put; other records "conflict"
               and the stored bytes untouched.
  4 ROUND TRIP the stored object is parquet whose rows read back equal the records written.
  5 SESSIONS   a firm scope assumes exactly its env ARN; an unset ARN raises; "global" assumes nothing.
  6 STATUS     run_status: all intended built -> PASS; one missing -> PARTIAL (M16).
  7 WIRED      mdpf_gold_consolidator.py imports mdpf_gold_parquet and calls write_partition and run_status;
               build_package.py ships mdpf_gold_parquet.py.
Prints one line per arm and "ROUND 1 PARQUET WRITER: <k> of <n> arms"; exit 0 only when every arm passes.
"""
import importlib.util
import io
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
TREE = os.environ.get("R1_TREE") or ROOT  # the positive control points this at a reference tree; lib/ always comes from ROOT
GOLD_DIR = os.path.join(TREE, "data/mdpf/scripts/gold")
MOD = os.path.join(GOLD_DIR, "mdpf_gold_parquet.py")
CONS = os.path.join(GOLD_DIR, "mdpf_gold_consolidator.py")
PKG = os.path.join(TREE, "infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py")
sys.path[:0] = [ROOT, GOLD_DIR]
from lib.opal_naming import address  # noqa: E402

SCOPES = ("49financial", "inflection", "cottonwood", "global")
FIRMS = ("49financial", "inflection", "cottonwood")
ARTS = ("account_distribution", "account_units", "aggregate_aua_timeseries", "aum_metrics")


class NoSuchKey(Exception):
    pass


class FakeS3:
    def __init__(self):
        self.store, self.puts = {}, 0

        class _E:
            pass
        self.exceptions = _E()
        self.exceptions.NoSuchKey = NoSuchKey

    def _k(self, Bucket, Key):
        return (Bucket, Key)

    def head_object(self, Bucket, Key):
        if self._k(Bucket, Key) not in self.store:
            import botocore.exceptions as be  # noqa: PLC0415
            raise be.ClientError({"Error": {"Code": "404", "Message": "Not Found"}}, "HeadObject")
        return {"ContentLength": len(self.store[self._k(Bucket, Key)])}

    def get_object(self, Bucket, Key):
        if self._k(Bucket, Key) not in self.store:
            raise NoSuchKey(Key)
        return {"Body": io.BytesIO(self.store[self._k(Bucket, Key)])}

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts += 1
        self.store[self._k(Bucket, Key)] = Body if isinstance(Body, (bytes, bytearray)) else Body.read()
        return {}


class FakeBoto3:
    def __init__(self):
        self.assumed = []

    def client(self, svc, **kw):
        if svc == "sts":
            outer = self

            class STS:
                def assume_role(self, RoleArn, RoleSessionName, **k):
                    outer.assumed.append(RoleArn)
                    return {"Credentials": {"AccessKeyId": "A", "SecretAccessKey": "S", "SessionToken": "T"}}
            return STS()
        return FakeS3()

    class session:  # noqa: N801 -- mirrors boto3.session.Session
        class Session:
            def __init__(self, **kw):
                self.kw = kw

            def client(self, svc, **kw):
                return FakeS3()

    def Session(self, **kw):  # noqa: N802
        return FakeBoto3.session.Session(**kw)


def load():
    spec = importlib.util.spec_from_file_location("mdpf_gold_parquet", MOD)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


arms = []


def arm(label, fn):
    f = []
    try:
        detail = fn(f) or ""
    except Exception as e:  # noqa: BLE001 -- an arm that raises is a failed arm, said in its line
        f.append("RAISED: " + (str(e).splitlines() or [repr(e)])[0][:200])
        detail = ""
    arms.append((label, not f, detail if not f else " | ".join(f)))


M = {}


def a_keys(f):
    if not os.path.exists(MOD):
        f.append(f"MISSING: {os.path.relpath(MOD, TREE)}")
        return ""
    M["m"] = m = load()
    if tuple(sorted(m.ARTIFACTS)) != tuple(sorted(ARTS)):
        f.append(f"ARTIFACTS = {m.ARTIFACTS!r}")
    n = 0
    for sc in SCOPES:
        for art in ARTS:
            want = address("mdpf", sc, "gold", art, "date=2026-10-08", object="data.parquet")
            got = m.partition_uri(sc, art, "2026-10-08")
            n += 1
            if got != want:
                f.append(f"{sc}/{art}: {got} (want {want})")
    return f"{n} of 16 partition URIs equal address()"


def a_untyped(f):
    if not os.path.exists(MOD):
        f.append("MISSING module")
        return ""
    src = open(MOD, encoding="utf-8").read()
    for lit in ("s3://", "opal-data-"):
        if lit in src:
            f.append(f"TYPED: the module source carries {lit!r}")
    return "no s3:// and no opal-data- literal in the module"


def a_write_once(f):
    m = M.get("m")
    if not m:
        f.append("INPUT: module not loaded")
        return ""
    s3 = FakeS3()
    recs = [{"data_as_of": "2026-10-08", "metric": "total_assets", "value": 1.5}]
    r1 = m.write_partition(s3, "global", "aum_metrics", "2026-10-08", recs)
    p1 = s3.puts
    r2 = m.write_partition(s3, "global", "aum_metrics", "2026-10-08", recs)
    snap = dict(s3.store)
    r3 = m.write_partition(s3, "global", "aum_metrics", "2026-10-08", [{"data_as_of": "2026-10-08", "metric": "total_assets", "value": 2.0}])
    if r1 != "written":
        f.append(f"first write -> {r1!r}")
    if r2 != "unchanged" or s3.puts != p1 and r2 == "unchanged":
        f.append(f"same records -> {r2!r}, puts {p1} -> {s3.puts}")
    if r3 != "conflict":
        f.append(f"other records -> {r3!r}")
    if s3.store != snap:
        f.append("CONFLICT OVERWROTE the stored object")
    M["s3"], M["recs"] = s3, recs
    return "written, unchanged (no second put), conflict (bytes untouched)"


def a_round_trip(f):
    s3 = M.get("s3")
    if not s3:
        f.append("INPUT: arm 3 did not run")
        return ""
    import pyarrow.parquet as pq  # noqa: PLC0415
    ((_, key), body), = [(k, v) for k, v in s3.store.items()]
    rows = pq.read_table(io.BytesIO(body)).to_pylist()
    if rows != M["recs"]:
        f.append(f"read back {rows!r} != written {M['recs']!r}")
    if not key.endswith("/date=2026-10-08/data.parquet"):
        f.append(f"stored key {key}")
    return f"parquet round trip equal at {key}"


def a_sessions(f):
    m = M.get("m")
    if not m:
        f.append("INPUT: module not loaded")
        return ""
    fb = FakeBoto3()
    saved = {k: os.environ.get(k) for k in [f"GOLD_WRITER_ROLE_ARN_{x.upper()}" for x in FIRMS]}
    try:
        for fm in FIRMS:
            os.environ[f"GOLD_WRITER_ROLE_ARN_{fm.upper()}"] = f"arn:aws:iam::1:role/test-{fm}"
        for fm in FIRMS:
            m.client_for_scope(fm, boto3_module=fb)
        if fb.assumed != [f"arn:aws:iam::1:role/test-{x}" for x in FIRMS]:
            f.append(f"firm scopes assumed {fb.assumed!r}")
        before = list(fb.assumed)
        m.client_for_scope("global", boto3_module=fb)
        if fb.assumed != before:
            f.append("global assumed a role")
        del os.environ["GOLD_WRITER_ROLE_ARN_49FINANCIAL"]
        try:
            m.client_for_scope("49financial", boto3_module=fb)
            f.append("an unset firm ARN did not raise (a silent fallback to the Lambda's own credentials)")
        except Exception:  # noqa: BLE001 -- the refusal is the pass
            pass
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return "each firm assumes its env ARN; global assumes none; an unset ARN refuses"


def a_status(f):
    m = M.get("m")
    if not m:
        f.append("INPUT: module not loaded")
        return ""
    if m.run_status(set(SCOPES), set(SCOPES)) != "PASS":
        f.append("all built does not read PASS")
    if m.run_status(set(SCOPES), {"global", "49financial"}) != "PARTIAL":
        f.append("two of four built does not read PARTIAL")
    return "PASS only when every intended scope was built"


def a_wired(f):
    cons = open(CONS, encoding="utf-8").read()
    pkg = open(PKG, encoding="utf-8").read()
    if not re.search(r'(?m)^\s*(import mdpf_gold_parquet|from mdpf_gold_parquet import)', cons):
        f.append("the consolidator does not import mdpf_gold_parquet")
    for fn in ("write_partition", "run_status"):
        if not re.search(r'\b%s\(' % fn, cons):
            f.append(f"the consolidator never calls {fn}()")
    if '"mdpf_gold_parquet.py"' not in pkg:
        f.append("build_package.py does not ship mdpf_gold_parquet.py")
    return "the consolidator imports and calls the writer; the package ships it"


arm("KEYS: 16 partition URIs equal address(mdpf, scope, gold, artifact, date=..., object=data.parquet)", a_keys)
arm("UNTYPED: the writer module types no s3:// and no opal-data- string", a_untyped)
arm("WRITE ONCE: written, then unchanged with no second put, then conflict with the stored bytes untouched", a_write_once)
arm("ROUND TRIP: the stored object is parquet and its rows equal the records", a_round_trip)
arm("SESSIONS: a firm scope assumes its own env ARN (unset refuses); global assumes none", a_sessions)
arm("STATUS: run_status reads PASS only when every intended scope was built (M16)", a_status)
arm("WIRED: the consolidator imports and calls the writer; the package ships the module", a_wired)

ok = 0
for label, passed, detail in arms:
    ok += passed
    print(f"{'ARM PASS' if passed else 'ARM FAIL'} {label} :: {detail}")
print(f"ROUND 1 PARQUET WRITER: {ok} of {len(arms)} arms")
sys.exit(0 if ok == len(arms) else 1)
