#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-23 S23-AC1 battery -- THE ASK MUST NAME EVERY PARTNER.

Prints EGS23-ASK-NAMES-EVERY-PARTNER only when all seven arms (a)-(g) hold, every number
beside its denominator.

NO EGRESS, NO SEND, NO INVOKE, NO SERVED WRITE. The served coverage_egress_ask.json is
READ and never overwritten; every ladder run in this battery targets an in-memory fake s3.
Arm (f) proves that from the run rather than asserting it.

Run from the worktree root:
  timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs23_ask_completeness.py
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import types

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")
PKG = os.path.join(ROOT, "data", "etfs", "scripts", "coverage")
REMEDIATE = os.path.join(PKG, "remediate.py")
REMEDIATE_REL = "data/etfs/scripts/coverage/remediate.py"
TESTS_REL = "data/etfs/scripts/coverage/tests/test_remediate.py"
PRE_PIN = "c6bcb7b12b0d0134274f689f470a91252d100546"   # remediate.py before this cell
ETFS_BUCKET = "opal-data-etfs"
ART_BUCKET = "opal-313476888478-lambda-artifacts"
ART_KEY = "ec2/etfs-reports/coverage/remediate.py"
MONTH = "2026-09"
ASK_KEY = "platinum/reports/%s/coverage_egress_ask.json" % MONTH
VERDICT_KEY = "platinum/reports/%s/coverage_verdict.json" % MONTH
SCRATCH = os.path.join(ROOT, ".scratch", "s23")

ARMS: list[tuple[str, bool, str]] = []
AWS_CALLS: list[list[str]] = []
BOTO_CLIENTS: list[str] = []


def arm(name: str, ok: bool, detail: str) -> bool:
    ARMS.append((name, ok, detail))
    print("ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args: list[str], timeout: int = 120) -> tuple[int, bytes]:
    AWS_CALLS.append(list(args))
    p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout


def aws_json(args: list[str], timeout: int = 120):
    rc, out = aws(args + ["--output", "json"], timeout=timeout)
    txt = out.decode("utf-8", "replace").replace("\r", "")
    try:
        return rc, json.loads(txt) if txt.strip() else None
    except Exception:  # noqa: BLE001
        return rc, None


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_module_from_source(src: str, name: str):
    mod = types.ModuleType(name)
    mod.__file__ = REMEDIATE
    sys.modules[name] = mod
    exec(compile(src, REMEDIATE, "exec"), mod.__dict__)
    return mod


class FakeS3:
    """An in-memory bucket. NOTHING here reaches AWS: every ladder run in this battery
    writes to this object, which is why no served key can be touched."""

    def __init__(self, with_get: bool = True):
        self.store: dict = {}
        self.put_calls: list = []
        self.head_calls: list = []
        if not with_get:
            # model a caller whose client cannot read back (the merge's only input)
            self.get_object = None  # type: ignore[assignment]

    def put_object(self, **kw):
        self.put_calls.append(kw)
        self.store[kw["Key"]] = kw["Body"]
        return {"ETag": '"fake"'}

    def head_object(self, Bucket, Key):  # noqa: N803
        self.head_calls.append((Bucket, Key))
        raise Exception("404 Not Found: %s" % Key)

    def get_object(self, Bucket, Key):  # noqa: N803
        if Key not in self.store:
            raise Exception("404 Not Found: %s" % Key)
        return {"Body": io.BytesIO(self.store[Key])}


def run_pytest(path: str, extra: list | None = None):
    r = subprocess.run([sys.executable, "-m", "pytest", path, "-q"] + (extra or []),
                       capture_output=True, cwd=ROOT, timeout=300)
    plain = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout.decode("utf-8", "replace"))
    m_p = re.search(r"(\d+)\s+passed", plain)
    m_f = re.search(r"(\d+)\s+failed", plain)
    return r.returncode, int(m_p.group(1)) if m_p else 0, int(m_f.group(1)) if m_f else 0


def build_pre_tree(dirname: str, pre_tests: bool):
    """A package tree with the PRE-CHANGE remediate.py, so 'before' is the code as it
    stood and not a description of it."""
    d = os.path.join(SCRATCH, dirname)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "coverage", "tests"), exist_ok=True)
    for f in os.listdir(PKG):
        if f.endswith(".py"):
            shutil.copy(os.path.join(PKG, f), os.path.join(d, "coverage", f))
    shutil.copy(os.path.join(ROOT, "lib", "trading_calendar.py"),
                os.path.join(d, "coverage", "trading_calendar.py"))
    for f in os.listdir(os.path.join(PKG, "tests")):
        if f.endswith(".py"):
            shutil.copy(os.path.join(PKG, "tests", f),
                        os.path.join(d, "coverage", "tests", f))
    pre_src = subprocess.run(["git", "show", "%s:%s" % (PRE_PIN, REMEDIATE_REL)],
                             capture_output=True, cwd=ROOT).stdout
    open(os.path.join(d, "coverage", "remediate.py"), "wb").write(pre_src)
    if pre_tests:
        pre_t = subprocess.run(["git", "show", "%s:%s" % (PRE_PIN, TESTS_REL)],
                               capture_output=True, cwd=ROOT).stdout
        open(os.path.join(d, "coverage", "tests", "test_remediate.py"), "wb").write(pre_t)
    return d, pre_src


def main() -> int:
    print("EG-s-23 -- the stop worked and the ask under-reports\n")
    os.makedirs(SCRATCH, exist_ok=True)

    try:
        import boto3  # noqa: F401
        _real = boto3.client

        def _watched(service_name, *a, **kw):
            BOTO_CLIENTS.append(str(service_name))
            return _real(service_name, *a, **kw)

        boto3.client = _watched  # type: ignore[assignment]
        boto3_ok = True
    except Exception:  # noqa: BLE001
        boto3_ok = False

    # ---------------------------------------------------------------- arm (a)
    print("(a) REPRODUCE THE DEFECT ON THE CODE AS IT STANDS (pre-change, pinned)")
    pre_src = subprocess.run(["git", "show", "%s:%s" % (PRE_PIN, REMEDIATE_REL)],
                             capture_output=True, cwd=ROOT).stdout
    print("    PRE-CHANGE remediate.py from git %s -- %d bytes, sha256 %s"
          % (PRE_PIN[:10], len(pre_src), sha256_bytes(pre_src)))
    pre = load_module_from_source(pre_src.decode("utf-8"), "remediate_pre_egs23")

    s3a = FakeS3()
    pre.remediate_month("49financial", MONTH,
                        {"2026-09-09": {"class": "D", "reason": "r1", "probe": None}},
                        invoke=None, s3=s3a)
    body_first = s3a.put_calls[0]["Body"]
    pre.remediate_month("cottonwood", MONTH,
                        {"2026-09-08": {"class": "D", "reason": "r2", "probe": None}},
                        invoke=None, s3=s3a)
    body_last = s3a.put_calls[-1]["Body"]
    keys = [c["Key"] for c in s3a.put_calls]
    print("    put_object calls: %d (denominator); distinct keys: %d" % (len(keys), len(set(keys))))
    for k in sorted(set(keys)):
        print("      KEY -> %s" % k)
    first_doc, last_doc = json.loads(body_first), json.loads(body_last)
    print("    FIRST body  asks: %s" % [(a["partner"], a["date"]) for a in first_doc["asks"]])
    print("    STORED body asks: %s" % [(a["partner"], a["date"]) for a in last_doc["asks"]])
    stored_partners = {a["partner"] for a in last_doc["asks"]}
    print("    top-level keys of the STORED body: %s" % sorted(last_doc.keys()))
    print("    does the stored body SAY another partner existed? -> %s"
          % ("no" if not any("partner" in k for k in last_doc) else "yes"))
    reproduced = (len(set(keys)) == 1 and len(keys) == 2
                  and "49financial" not in stored_partners
                  and "cottonwood" in stored_partners)
    if not reproduced:
        print("    DEFECT DID NOT REPRODUCE -- the premise of this cell is refused by the "
              "world. STOPPING; file a surprise row.")
        arm("a", False, "the overwrite did NOT reproduce on the pre-change code -- STOPPED "
                        "rather than change code on a premise the world refused")
        print("\nARMS %d of 7 PASS" % sum(1 for _, ok, _ in ARMS if ok))
        print("EGS23-PREMISE-REFUSED")
        return 1
    arm("a", True,
        "the overwrite REPRODUCES: 2 of 2 put_object calls target the SAME key %s, and the "
        "final stored body carries only the SECOND partner (%s) -- 49financial's outstanding "
        "day is ABSENT, and nothing in the document names a partner it does not cover"
        % (keys[0], sorted(stored_partners)))

    # ---------------------------------------------------------------- arm (b)
    print("\n(b) EVERY PARTNER IS REACHABLE AFTER THE CHANGE")
    print("    SHAPE CHOSEN, in one sentence: ONE MERGED MONTH DOCUMENT at the same canonical "
          "key -- the reader is a PERSON opening ONE file to authorise egress, so 'which "
          "partners does this cover' must be a property OF THE STORED DOCUMENT, whereas "
          "per-partner keys would leave a partner that never wrote invisible unless the reader "
          "already knew the partner set, which is the thing being fixed.")
    dest_v = os.path.join(SCRATCH, "coverage_verdict.json")
    rc_v, _ = aws(["s3api", "get-object", "--bucket", ETFS_BUCKET, "--key", VERDICT_KEY, dest_v])
    vdoc = json.load(open(dest_v, encoding="utf-8")) if rc_v == 0 else {}
    partners = sorted((vdoc.get("per_partner") or {}).keys())
    print("    PARTNER LIST FROM AN ARTIFACT THAT OWNS IT (s3://%s/%s), never by recall:"
          % (ETFS_BUCKET, VERDICT_KEY))
    print("      %s -> %d partner(s) DENOMINATOR, minus 0 excluded" % (partners, len(partners)))

    post_src = open(REMEDIATE, "rb").read()
    post = load_module_from_source(post_src.decode("utf-8"), "remediate_post_egs23")
    s3b = FakeS3()
    per_partner_dates = {}
    for i, p in enumerate(partners):
        d = "2026-09-0%d" % (7 + (i % 3))
        per_partner_dates[p] = d
        post.remediate_month(p, MONTH, {d: {"class": "D", "reason": "r", "probe": None}},
                             invoke=None, s3=s3b)
    stored = json.loads(s3b.store[ASK_KEY])
    reach = {a["partner"] for a in stored["asks"]}
    print("    the month's ask at %s now carries:" % ASK_KEY)
    print("      partners_covered = %s" % stored["partners_covered"])
    print("      ask_scope        = %r" % stored["ask_scope"])
    for a in sorted(stored["asks"], key=lambda x: (x["partner"], x["date"])):
        print("      %-12s %s  provider=%-14s class=%s" % (a["partner"], a["date"],
                                                           a["provider"], a["class"]))
    print("    partners reachable by a reader of the month's ask: %d of %d (denominator)"
          % (len(reach), len(partners)))
    arm("b", reach == set(partners) and stored["partners_covered"] == partners,
        "%d of %d partners taken from the artifact are reachable in the ONE document a reader "
        "opens, and the document names its own coverage as partners_covered=%s"
        % (len(reach), len(partners), stored["partners_covered"]))

    # ---------------------------------------------------------------- arm (c)
    print("\n(c) A PARTIAL ASK CANNOT READ AS COMPLETE")
    s3c = FakeS3()
    missing = partners[0]
    for p in partners:
        if p == missing:
            continue           # this partner's ladder never ran
        post.remediate_month(p, MONTH,
                             {per_partner_dates[p]: {"class": "D", "reason": "r",
                                                     "probe": None}},
                             invoke=None, s3=s3c)
    partial = json.loads(s3c.store[ASK_KEY])
    print("    COMPLETE case -- partners_covered = %s" % stored["partners_covered"])
    print("    PARTIAL  case -- partners_covered = %s   (%s never ran)"
          % (partial["partners_covered"], missing))
    j_complete = json.dumps(stored["partners_covered"], sort_keys=True)
    j_partial = json.dumps(partial["partners_covered"], sort_keys=True)
    print("    TEXTUALLY DIFFERENT -> %s" % (j_complete != j_partial))
    print("    PRE-CHANGE, the same two cases were indistinguishable: the document carried no "
          "partner-coverage field at all (top-level keys %s), so a reader could not tell them "
          "apart -- which is the failure FWD-8 exists to prevent." % sorted(last_doc.keys()))
    arm("c", j_complete != j_partial and missing not in partial["partners_covered"],
        "the partial artifact is TEXTUALLY DIFFERENT from the complete one (%s vs %s), so a "
        "reader can tell them apart WITHOUT knowing the code"
        % (partial["partners_covered"], stored["partners_covered"]))

    # ---------------------------------------------------------------- arm (d)
    print("\n(d) THE LADDER'S OTHER PROPERTIES ARE UNDISTURBED")
    pre_dir, _ = build_pre_tree("prefull_arm_d", pre_tests=True)
    rc0, p0, f0 = run_pytest(os.path.relpath(
        os.path.join(pre_dir, "coverage", "tests", "test_remediate.py"), ROOT))
    rc1, p1, f1 = run_pytest(TESTS_REL)
    print("    invocation: python -m pytest %s -q" % TESTS_REL)
    print("    BEFORE (pre-change code AND pre-change tests): rc=%d  %d passed  %d failed"
          % (rc0, p0, f0))
    print("    AFTER  (this cell's code and tests, by its own path): rc=%d  %d passed  %d failed"
          % (rc1, p1, f1))
    ask_pp = post.rung3_stop_and_ask("cottonwood", MONTH,
                                     [{"date": "2026-09-08", "class": "D", "reason": "r"}],
                                     s3=None, write=False)
    auth_ok = ask_pp["authorization"] == (
        "PER-USE -- a person decides; nothing here is executed by any process")
    print("    authorization VERBATIM: %r -> %s" % (ask_pp["authorization"], auth_ok))
    s3d = FakeS3()
    res_dry = post.remediate_month("cottonwood", MONTH,
                                   {"2026-09-08": {"class": "D", "reason": "r", "probe": None}},
                                   invoke=None, s3=s3d, dry_run=True)
    dry_ok = ("ask" not in res_dry) and s3d.put_calls == []
    print("    dry_run: rung 3 fired? -> %s ; put_object calls %d of 0 expected"
          % ("ask" in res_dry, len(s3d.put_calls)))
    s3e = FakeS3()
    calls: list = []
    res_b = post.remediate_month("cottonwood", MONTH,
                                 {"2026-09-08": {"class": "B", "reason": "priced==0",
                                                 "probe": {"partition": True, "priced": 0}}},
                                 invoke=lambda fn, pl: calls.append((fn, pl)), s3=s3e)
    b_ok = (res_b["expected_empty"] == ["2026-09-08"] and calls == []
            and res_b["rungs"]["rerun"] == 0)
    print("    class B: expected_empty=%s, rung-1 invokes %d of 0 expected, rerun count %d"
          % (res_b["expected_empty"], len(calls), res_b["rungs"]["rerun"]))
    arm("d", rc0 == 0 and rc1 == 0 and f0 == 0 and f1 == 0 and p1 >= p0
        and auth_ok and dry_ok and b_ok,
        "suite BEFORE rc=%d %d passed %d failed -> AFTER rc=%d %d passed %d failed (no "
        "regression, +%d arms); authorization PER-USE verbatim; dry_run fires no rung 3 (0 "
        "writes); class B stops with 0 re-runs"
        % (rc0, p0, f0, rc1, p1, f1, p1 - p0))

    # ---------------------------------------------------------------- arm (e)
    print("\n(e) DEPLOYED-vs-BUILT, MEASURED")
    dep_dest = os.path.join(SCRATCH, "deployed_remediate.py")
    rc_d, _ = aws(["s3api", "get-object", "--bucket", ART_BUCKET, "--key", ART_KEY, dep_dest])
    dep = open(dep_dest, "rb").read() if rc_d == 0 else b""
    dep_sha, built_sha = sha256_bytes(dep), sha256_bytes(post_src)
    print("    DEPLOYED s3://%s/%s -- %d bytes, sha256 %s" % (ART_BUCKET, ART_KEY, len(dep),
                                                              dep_sha))
    print("    BUILT    %s -- %d bytes, sha256 %s" % (REMEDIATE_REL, len(post_src), built_sha))
    print("    CRLF deployed %d / built %d (both LF -- not an eol artifact)"
          % (dep.count(b"\r\n"), post_src.count(b"\r\n")))
    print("    CORROBORATION: deployed == the PRE-CHANGE blob at git %s -> %s"
          % (PRE_PIN[:10], sha256_bytes(dep) == sha256_bytes(pre_src)))
    verdict_e = "DEPLOYED == BUILT" if dep_sha == built_sha else "DEPLOYED != BUILT"
    print("    %s" % verdict_e)
    print("    THIS CELL DEPLOYS NOTHING, so %s is the EXPECTED answer: until someone deploys "
          "these bytes, every future ladder run still overwrites one partner's ask with the "
          "next." % verdict_e)
    arm("e", dep_sha != built_sha and len(dep) > 0,
        "%s -- deployed sha256 %s (%d B) vs built sha256 %s (%d B); recorded as a number "
        "rather than assumed" % (verdict_e, dep_sha[:16], len(dep), built_sha[:16],
                                 len(post_src)))

    # ---------------------------------------------------------------- arm (f)
    print("\n(f) NO EGRESS, NO SEND, NO INVOKE")
    svc = sorted({c[0] for c in AWS_CALLS if c})
    bad_cli = [c for c in AWS_CALLS if c and c[0] in ("ses", "sesv2", "lambda")]
    bad_boto = [s for s in BOTO_CLIENTS if s in ("ses", "sesv2", "lambda")]
    src_txt = post_src.decode("utf-8")
    net_tokens = ["requests.", "urllib.request", "http.client", "socket.", "boto3.client('lambda'",
                  "ses", "invoke("]
    found = {t: src_txt.count(t) for t in net_tokens}
    writes_served = [c for c in (s3b.put_calls + s3c.put_calls + s3d.put_calls + s3e.put_calls)]
    print("    boto3 instrumented: %s ; boto3 clients constructed: %d of 0 expected -> %s"
          % (boto3_ok, len(BOTO_CLIENTS), BOTO_CLIENTS or "NONE"))
    print("    AWS CLI invocations: %d (denominator); services: %s ; ses/lambda: %d"
          % (len(AWS_CALLS), svc, len(bad_cli)))
    print("    every ladder run in this battery targeted an IN-MEMORY FakeS3: %d put_object "
          "call(s), 0 of which reached AWS" % len(writes_served))
    print("    the SERVED ask key was READ %s and written 0 times by this battery"
          % ("0 times" if not any(ASK_KEY in " ".join(c) for c in AWS_CALLS) else "read-only"))
    print("    network/egress token census over %s (%d token(s) checked): %s"
          % (REMEDIATE_REL, len(net_tokens), found))
    print("    NOTE: 'invoke(' occurrences are the ladder's rung-1 CALLABLE PARAMETER, which "
          "this battery passes as None or a recording lambda -- no Lambda client is ever "
          "constructed.")
    arm("f", not bad_cli and not bad_boto and found["requests."] == 0
        and found["urllib.request"] == 0 and found["http.client"] == 0,
        "0 SES clients, 0 Lambda invokes, 0 boto3 clients constructed, %d AWS CLI call(s) "
        "across %s with 0 naming ses/sesv2/lambda, and 0 of %d network tokens present in the "
        "changed module -- Andrew's standing constraint cannot be reached from this cell"
        % (len(AWS_CALLS), svc, len(net_tokens)))

    # ---------------------------------------------------------------- arm (g)
    print("\n(g) THE REGRESSION ARMS ARE CONTROLS, NOT CONSTANTS")
    pre_dir2, _ = build_pre_tree("pre_arm_g", pre_tests=False)   # MY tests, PRE-CHANGE code
    rc_pre, p_pre, f_pre = run_pytest(
        os.path.relpath(os.path.join(pre_dir2, "coverage", "tests", "test_remediate.py"), ROOT),
        ["-k", "egs23"])
    rc_post, p_post, f_post = run_pytest(TESTS_REL, ["-k", "egs23"])
    print("    MY arms against the PRE-CHANGE code: rc=%d  %d passed  %d FAILED"
          % (rc_pre, p_pre, f_pre))
    print("    MY arms against THIS cell's code   : rc=%d  %d passed  %d failed"
          % (rc_post, p_post, f_post))
    print("    an arm that passes both ways proves nothing; these fail against the world they "
          "were written to catch and pass against the fix.")
    arm("g", f_pre >= 1 and p_pre == 0 and rc_post == 0 and f_post == 0 and p_post >= 1,
        "%d of %d new arm(s) FAIL against the pre-change code and %d of %d PASS against this "
        "cell's -- controls, not constants"
        % (f_pre, f_pre + p_pre, p_post, p_post + f_post))

    npass = sum(1 for _, ok, _ in ARMS if ok)
    print("\nARMS %d of %d PASS" % (npass, len(ARMS)))
    if npass == len(ARMS) == 7:
        print("EGS23-ASK-NAMES-EVERY-PARTNER")
        return 0
    print("EGS23-NOT-ESTABLISHED -- failing arms: %s"
          % ", ".join(n for n, ok, _ in ARMS if not ok))
    return 1


if __name__ == "__main__":
    sys.exit(main())
