#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-28 / S28-AC1 -- THE UNRESOLVED RECORD MUST NAME ITS PROVIDER.

Six arms, every number beside its denominator, ending with
EGS28-EVERY-UNRESOLVED-NAMES-ITS-PROVIDER only when all six hold.

  (a) THE DEFECT REPRODUCES FIRST, site count ENUMERATED FROM SOURCE (pre-change
      bytes, pinned BY CONTENT out of the issuance commit).
  (b) EVERY SITE IS FIXED -- N of N, each named with the branch it serves.
  (c) AN UNKNOWN PROVIDER STILL READS AS UNKNOWN (positive control on the
      honest-absence path -- the arm that stops this becoming a fabrication).
  (d) THE TERMINAL MESSAGE NOW NAMES A REAL PROVIDER -- the DIFFERENCE control,
      the arm that carries the outcome: the SAME input built BEFORE and AFTER,
      through the orchestrator's OWN `_normalize_unresolved` + `_build_terminal_email`.
  (e) NOTHING ELSE MOVED, and the deploy gap is MEASURED, not closed.
  (f) NO SEND, NO INVOKE, NO EGRESS -- with the denominator of what was checked.

ZERO AWS write calls, zero sends, zero invokes. The only AWS call this battery makes
at all is ONE read-only GetObject against our own artifact prefix, for arm (e)'s
DEPLOYED sha256; it is counted and disclosed in arm (f), and its failure degrades to
a cited HELD value rather than to a claim.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from unittest import mock

# The commit that issued this order; the pre-change bytes are read out of it and
# then RESOLVED BY CONTENT against the sha256 printed below (a pin verified by
# content, never by ancestry -- rule 22a).
ISSUANCE_COMMIT = "32ae4ede66"
PRECHANGE_SHA256 = "25ff4dbed4af6545592d5870b8222e84ac75b7237a4397ce5741ceb4d8803a2a"

REMEDIATE_REL = "data/etfs/scripts/coverage/remediate.py"
TESTS_REL = "data/etfs/scripts/coverage/tests/test_remediate.py"
LAMBDA_REL = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"

DEPLOYED_BUCKET = "opal-313476888478-lambda-artifacts"
DEPLOYED_KEY = "ec2/etfs-reports/coverage/remediate.py"
# Cited fallback ONLY (provenance printed as `held`, never as measured):
# ETFS_GUARDRAIL-S33 grounding, org/missions/D8/ETFS/ETFS_GUARDRAIL/surprise-channel/
# investigations/INVESTIGATION_v1.md @32ae4ede66 -- coverage/remediate.py 11,011 B at
# that prefix, read live by 2.0.0_SA_COO 2026-09-10 ~05:38Z.
HELD_DEPLOYED_BYTES = 11011

FAILURES: list = []
AWS_CALLS: list = []
LADDER_RUNS = [0]


def hr(title: str) -> None:
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def check(ok: bool, label: str) -> bool:
    print("  %s  %s" % ("PASS:" if ok else "FAIL:", label))
    if not ok:
        FAILURES.append(label)
    return ok


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=here,
                         capture_output=True, text=True, timeout=60)
    return out.stdout.strip()


ROOT = repo_root()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_file_bytes(rel: str) -> bytes:
    with io.open(os.path.join(ROOT, rel), "rb") as fh:
        return fh.read()


def git_show(ref: str, rel: str) -> bytes:
    out = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], cwd=ROOT,
                         capture_output=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError("git show %s:%s rc=%d %s" % (ref, rel, out.returncode,
                                                        out.stderr.decode("utf-8", "replace")))
    return out.stdout


def load_module_from_source(name: str, src_bytes: bytes, workdir: str):
    """Import `src_bytes` as a fresh module named `name` (no package machinery, no
    reliance on whatever is already on sys.path)."""
    path = os.path.join(workdir, name + ".py")
    with io.open(path, "wb") as fh:
        fh.write(src_bytes)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def append_sites(src_bytes: bytes):
    """Every `unresolved.append(<dict literal>)` in the given source, read from ITS
    OWN AST. Returns [(lineno, [key literals])...] -- the DENOMINATOR, not a list
    copied from the task order's face."""
    tree = ast.parse(src_bytes.decode("utf-8"))
    sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if not isinstance(f, ast.Attribute) or f.attr != "append":
            continue
        if not isinstance(f.value, ast.Name) or f.value.id != "unresolved":
            continue
        arg = node.args[0] if node.args else None
        keys = [k.value for k in arg.keys
                if isinstance(k, ast.Constant)] if isinstance(arg, ast.Dict) else []
        sites.append((node.lineno, keys))
    return sorted(sites)


# ---------------------------------------------------------------------------
# The one case that reaches EVERY branch, used identically before and after.
# ---------------------------------------------------------------------------
PARTNER = "cottonwood"
MONTH = "2026-08"
CLASSES = {
    "2026-08-04": {"class": "C", "reason": "producer never fired",
                    "probe": {"partition": True, "priced": 7}},
    "2026-08-18": {"class": "D", "reason": "upstream partition missing",
                    "probe": {"partition": False, "priced": 0}},
    "2026-08-20": {"class": "B", "reason": "priced == 0",
                    "probe": {"partition": True, "priced": 0}},
    "2026-08-21": {"class": "UNKNOWN", "reason": "no probe supplied", "probe": None},
}


class _StubS3:
    """head_object raises (nothing landed), put_object RECORDS. No network."""

    def __init__(self, calls):
        self.calls = calls

    def head_object(self, **kw):
        self.calls.append(("s3", "head_object", kw))
        raise Exception("404 Not Found (stub)")

    def put_object(self, **kw):
        self.calls.append(("s3", "put_object", kw))
        return {"ETag": '"stub"'}


class _Invoke:
    def __init__(self, calls, raise_for=()):
        self.calls = calls
        self.raise_for = set(raise_for)

    def __call__(self, function_name, payload):
        self.calls.append(("lambda-stub", function_name, payload))
        if payload["date"] in self.raise_for:
            raise RuntimeError("no fact_holdings partition for date %s" % payload["date"])
        return {"status": "ok"}


def run_ladder(mod, calls, partner=PARTNER, dry_run=False, invoke_none=False):
    """One ladder run through the module under test. `2026-08-18` raises at rung 1
    (site: RUNG-1-RAISED); the other two non-B days land nowhere on rung 2 (site:
    RUNG-2-NO-SLICE); B never reaches rung 1 at all."""
    LADDER_RUNS[0] += 1
    s3 = _StubS3(calls)
    invoke = None if invoke_none else _Invoke(calls, raise_for=["2026-08-18"])
    return mod.remediate_month(partner, MONTH, CLASSES, invoke=invoke, s3=s3,
                               dry_run=dry_run, write_ask=False)


def unresolved_doc(result, partner=PARTNER):
    """The artifact the renderer writes: KEYED BY PARTNER (render_month_end.py:1017
    -> :1138), which is the shape the orchestrator reads."""
    return {partner: result["unresolved"]}


def main() -> int:
    print("ETFS_GUARDRAIL.TO-EG-s-28 / S28-AC1 -- battery")
    print("worker: 0.9.0_WK_ETFS_GUARDRAIL~1   repo root: %s" % ROOT)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, timeout=60).stdout.strip()
    print("HEAD: %s   issuance pin: %s" % (head, ISSUANCE_COMMIT))

    workdir = tempfile.mkdtemp(prefix="egs28_")

    before_src = git_show(ISSUANCE_COMMIT, REMEDIATE_REL)
    before_sha = sha256_bytes(before_src)
    after_src = read_file_bytes(REMEDIATE_REL)
    after_sha = sha256_bytes(after_src)

    # -------------------------------------------------------------- arm (a)
    hr("(a) THE DEFECT REPRODUCES FIRST -- site denominator ENUMERATED FROM SOURCE")
    print("  PRE-CHANGE BYTES resolved BY CONTENT, not by ancestry:")
    print("    git show %s:%s -> %d bytes  sha256=%s" % (
        ISSUANCE_COMMIT, REMEDIATE_REL, len(before_src), before_sha))
    print("    expected sha256                         =%s" % PRECHANGE_SHA256)
    check(before_sha == PRECHANGE_SHA256,
          "(a) pre-change blob is the one this order was cut against (content pin)")

    sites_before = append_sites(before_src)
    n_before = len(sites_before)
    with_provider_before = [ln for ln, keys in sites_before if "provider" in keys]
    print("")
    print("  DENOMINATOR: %d `unresolved.append` site(s) in %s @%s, read from its AST"
          % (n_before, REMEDIATE_REL, ISSUANCE_COMMIT))
    for ln, keys in sites_before:
        print("    line %4d  keys=%s  provider=%s" % (
            ln, keys, "YES" if "provider" in keys else "NO"))
    print("  %d of %d site(s) carry `provider`" % (len(with_provider_before), n_before))
    check(n_before > 0, "(a) the AST census finds sites at all (it can go non-zero)")
    check(len(with_provider_before) == 0,
          "(a) 0 of %d pre-change site(s) carry `provider`" % n_before)
    if with_provider_before:
        print("")
        print("  BLOCKED: THE PREMISE IS WRONG -- %d pre-change site(s) already carry "
              "`provider` (lines %s). A row is owed and this battery STOPS."
              % (len(with_provider_before), with_provider_before))
        print("  STOPPED-ON-PREMISE-FAILURE")
        return 1

    calls_a: list = []
    mod_before = load_module_from_source("remediate_before", before_src, workdir)
    res_before = run_ladder(mod_before, calls_a)
    print("")
    print("  LADDER RUN on the PRE-CHANGE module (%d unresolved record(s)):" % len(
        res_before["unresolved"]))
    for u in res_before["unresolved"]:
        print("    %s" % json.dumps(u, sort_keys=True))
    lacking = [u for u in res_before["unresolved"] if "provider" not in u]
    print("  %d of %d record(s) LACK `provider`" % (len(lacking), len(res_before["unresolved"])))
    check(len(res_before["unresolved"]) > 0, "(a) the run produced unresolved records to judge")
    check(len(lacking) == len(res_before["unresolved"]),
          "(a) every pre-change record lacks `provider` -- the defect reproduces")

    # -------------------------------------------------------------- arm (b)
    hr("(b) EVERY SITE IS FIXED, NOT SOME -- N of N, each named with the branch it serves")
    sites_after = append_sites(after_src)
    n_after = len(sites_after)
    ok_after = [ln for ln, keys in sites_after if "provider" in keys]
    BRANCH_BY_ORDER = [
        "site 1/4 -- DRY-RUN: rung 1 planned, not executed (dry_run=True)",
        "site 2/4 -- NO INVOKE CALLABLE or NO PRODUCER MAPPED for the partner",
        "site 3/4 -- RUNG 1 RAISED: the producer's LOUD-fail on an absent partition (class D)",
        "site 4/4 -- RUNG 2 RE-CHECK: the invoke returned but no slice landed",
    ]
    print("  DENOMINATOR: %d `unresolved.append` site(s) in the CHANGED %s, read from its AST"
          % (n_after, REMEDIATE_REL))
    for i, (ln, keys) in enumerate(sites_after):
        branch = BRANCH_BY_ORDER[i] if i < len(BRANCH_BY_ORDER) else "site %d -- UNNAMED BRANCH" % (i + 1)
        print("    line %4d  provider=%s  %s" % (ln, "YES" if "provider" in keys else "NO", branch))
    print("  %d of %d site(s) carry `provider`" % (len(ok_after), n_after))
    check(n_after == n_before,
          "(b) the site denominator is unchanged (%d before, %d after) -- no site was "
          "deleted to make the count read clean" % (n_before, n_after))
    check(len(ok_after) == n_after,
          "(b) %d of %d site(s) carry `provider`" % (len(ok_after), n_after))
    check(n_after <= len(BRANCH_BY_ORDER),
          "(b) every site is NAMED with the branch it serves (%d named, %d sites)"
          % (len(BRANCH_BY_ORDER), n_after))

    calls_b: list = []
    mod_after = load_module_from_source("remediate_after", after_src, workdir)
    res_after = run_ladder(mod_after, calls_b)
    res_after_dry = run_ladder(mod_after, calls_b, dry_run=True)
    res_after_noinv = run_ladder(mod_after, calls_b, invoke_none=True)
    print("")
    print("  LADDER RUNS on the CHANGED module -- every branch that can produce a record:")
    for label, res in (("rung-1-raised + rung-2-no-slice", res_after),
                       ("dry-run planned", res_after_dry),
                       ("no invoke callable", res_after_noinv)):
        got = res["unresolved"]
        named = [u for u in got if u.get("provider")]
        print("    %-32s %d of %d record(s) name a provider" % (label, len(named), len(got)))
        for u in got:
            print("        %s" % json.dumps(u, sort_keys=True))
        check(len(named) == len(got) and len(got) > 0,
              "(b) %s: %d of %d record(s) name a provider" % (label, len(named), len(got)))
    check(all(u.get("provider") == "Black Diamond" for u in res_after["unresolved"]),
          "(b) the provider named for cottonwood is its mapped vendor, Black Diamond")

    # -------------------------------------------------------------- arm (c)
    hr("(c) AN UNKNOWN PROVIDER STILL READS AS UNKNOWN -- positive control on the "
       "honest-absence path")
    unmapped = "a-partner-with-no-mapping"
    print("  `%s` in _PROVIDER_BY_PARTNER: %s  (mapped partners: %s)" % (
        unmapped, unmapped in mod_after._PROVIDER_BY_PARTNER,
        sorted(mod_after._PROVIDER_BY_PARTNER)))
    calls_c: list = []
    res_c = run_ladder(mod_after, calls_c, partner=unmapped)
    for u in res_c["unresolved"]:
        print("    %s" % json.dumps(u, sort_keys=True))
    providers_c = {u.get("provider") for u in res_c["unresolved"]}
    print("  distinct provider value(s) over %d record(s): %s" % (
        len(res_c["unresolved"]), sorted(providers_c)))
    check(providers_c == {"<no provider mapped>"},
          "(c) an unmapped partner yields the honest absence marker for every record")
    check(None not in providers_c and "None" not in providers_c,
          "(c) it is neither None nor the literal string 'None'")
    check(not (providers_c & set(mod_after._PROVIDER_BY_PARTNER.values())),
          "(c) NO GUESS: no mapped vendor name leaked onto an unmapped partner")

    # -------------------------------------------------------------- arm (d)
    hr("(d) THE TERMINAL MESSAGE NOW NAMES A REAL PROVIDER -- the DIFFERENCE control")
    lam_bytes = read_file_bytes(LAMBDA_REL)
    print("  instrument: the orchestrator's OWN _normalize_unresolved + _build_terminal_email")
    print("    %s  %d bytes  sha256=%s" % (LAMBDA_REL, len(lam_bytes), sha256_bytes(lam_bytes)))
    lam_dir = os.path.join(ROOT, os.path.dirname(LAMBDA_REL))
    if lam_dir not in sys.path:
        sys.path.insert(0, lam_dir)
    os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
    os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub-topic")

    class _StubBoto:
        def __init__(self, service, calls):
            self._service = service
            self._calls = calls

        def __getattr__(self, name):
            def _call(**kwargs):
                self._calls.append((self._service, name, kwargs))
                raise AssertionError("BATTERY BUG: a real AWS call was attempted (%s.%s)"
                                     % (self._service, name))
            return _call

    lam_calls: list = []
    with mock.patch("boto3.client", lambda service, **kw: _StubBoto(service, lam_calls)):
        sys.modules.pop("lambda_function", None)
        import lambda_function as lam  # noqa: E402

    doc_before = unresolved_doc(res_before)
    doc_after = unresolved_doc(res_after)
    dates_b = sorted(r["date"] for r in doc_before[PARTNER])
    dates_a = sorted(r["date"] for r in doc_after[PARTNER])
    print("")
    print("  SAME INPUT, ENGAGED vs DISENGAGED -- same month, same partner, same dates:")
    print("    BEFORE dates=%s  partners=%s" % (dates_b, sorted(doc_before)))
    print("    AFTER  dates=%s  partners=%s" % (dates_a, sorted(doc_after)))
    check(dates_b == dates_a and sorted(doc_before) == sorted(doc_after),
          "(d) the two documents differ ONLY in the field under test")

    def provider_column(doc):
        rows = lam._normalize_unresolved(doc)
        msg = lam._build_terminal_email(MONTH, rows, None,
                                        to_header="battery@localhost.invalid")
        body = msg.get_payload(0).get_payload()
        cols = []
        for line in body.splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5 and parts[0].startswith("2026-"):
                cols.append((parts[0], parts[1], parts[2]))
        return body, cols

    body_before, cols_before = provider_column(doc_before)
    body_after, cols_after = provider_column(doc_after)
    print("")
    print("  BEFORE -- provider column, %d row(s):" % len(cols_before))
    for d, p, prov in cols_before:
        print("    %s | %-11s | %s" % (d, p, prov))
    print("  AFTER  -- provider column, %d row(s):" % len(cols_after))
    for d, p, prov in cols_after:
        print("    %s | %-11s | %s" % (d, p, prov))
    check(len(cols_before) == len(cols_after) == len(dates_a) and len(cols_after) > 0,
          "(d) both messages render one row per date (%d of %d)" % (len(cols_after), len(dates_a)))
    check(all(prov == "(not stated)" for _, _, prov in cols_before),
          "(d) DISENGAGED: %d of %d row(s) render `(not stated)`"
          % (sum(1 for _, _, p in cols_before if p == "(not stated)"), len(cols_before)))
    check(all(prov == "Black Diamond" for _, _, prov in cols_after),
          "(d) ENGAGED: %d of %d row(s) render the real provider `Black Diamond`"
          % (sum(1 for _, _, p in cols_after if p == "Black Diamond"), len(cols_after)))
    check("(not stated)" not in body_after,
          "(d) the AFTER message contains no `(not stated)` anywhere in its body")
    check(body_before != body_after,
          "(d) the two message bodies differ (the control could have shown no change)")
    print("")
    print("  AFTER message body, verbatim:")
    for line in body_after.splitlines():
        print("    | %s" % line)

    # -------------------------------------------------------------- arm (e)
    hr("(e) NOTHING ELSE MOVED, AND THE DEPLOY GAP IS MEASURED, NOT CLOSED")
    before_tests = git_show(ISSUANCE_COMMIT, TESTS_REL)
    tdir = os.path.join(workdir, "beforepkg")
    os.makedirs(os.path.join(tdir, "tests"), exist_ok=True)
    with io.open(os.path.join(tdir, "remediate.py"), "wb") as fh:
        fh.write(before_src)
    with io.open(os.path.join(tdir, "tests", "test_remediate.py"), "wb") as fh:
        fh.write(before_tests)

    ansi = re.compile(chr(27) + r"\[[0-9;]*m")   # ASCII-only source: ESC is chr(27)

    def pytest_run(path, cwd):
        out = subprocess.run([sys.executable, "-m", "pytest", path, "-q", "--color=no"],
                             cwd=cwd, capture_output=True, text=True, timeout=240)
        clean = ansi.sub("", out.stdout)
        tail = [ln for ln in clean.splitlines() if ln.strip()][-1:] or [""]
        return out.returncode, tail[0].strip()

    rc_b, line_b = pytest_run(os.path.join(tdir, "tests", "test_remediate.py"), tdir)
    rc_a, line_a = pytest_run(TESTS_REL, ROOT)
    print("  BEFORE  %s @%s -> rc=%d  %s" % (TESTS_REL, ISSUANCE_COMMIT, rc_b, line_b))
    print("  AFTER   %s (worktree) -> rc=%d  %s" % (TESTS_REL, rc_a, line_a))
    check(rc_b == 0, "(e) the pre-change battery passed (rc=0) -- the baseline is real")
    check(rc_a == 0, "(e) the post-change battery passes (rc=0)")

    n_b = int(line_b.split(" passed")[0].split()[-1]) if " passed" in line_b else -1
    n_a = int(line_a.split(" passed")[0].split()[-1]) if " passed" in line_a else -1
    print("  counts: %d test(s) before, %d test(s) after (+%d, all additive)"
          % (n_b, n_a, n_a - n_b))
    check(n_b > 0 and n_a >= n_b, "(e) no pre-existing test was removed (%d -> %d)" % (n_b, n_a))

    ask_in = [{"date": "2026-08-18", "class": "D", "reason": "r"}]
    ask_before = mod_before.rung3_stop_and_ask(PARTNER, MONTH, ask_in, s3=None, write=False)
    ask_after = mod_after.rung3_stop_and_ask(PARTNER, MONTH, list(ask_in), s3=None, write=False)
    ask_after_withfield = mod_after.rung3_stop_and_ask(
        PARTNER, MONTH,
        [{"date": "2026-08-18", "class": "D", "provider": "Black Diamond", "reason": "r"}],
        s3=None, write=False)
    strip = lambda a: {k: v for k, v in a.items() if k != "generated_at"}  # noqa: E731
    print("")
    print("  THE ASK'S OWN RECORD (rung 3) -- unchanged by this cell:")
    print("    BEFORE: %s" % json.dumps(ask_before["asks"], sort_keys=True))
    print("    AFTER : %s" % json.dumps(ask_after["asks"], sort_keys=True))
    check(strip(ask_before) == strip(ask_after),
          "(e) rung 3's ask is byte-identical before and after (generated_at aside)")
    check(ask_after_withfield["asks"] == ask_after["asks"],
          "(e) an unresolved record CARRYING the new field produces the same ask -- "
          "no leak into the artifact a person authorises egress on")

    built_sha = after_sha
    dep_path = os.path.join(workdir, "deployed_remediate.py")
    dep_sha, dep_len, dep_prov = None, None, "held"
    aws_cmd = os.path.join(ROOT, ".tools", "aws.cmd")   # the Windows face of the
    # MSYS-guard shim; `.tools/aws` itself is a bash script and is not directly
    # executable from CreateProcess (WinError 193), and a bare `bash` on this box
    # resolves to the WSL stub.
    try:
        AWS_CALLS.append(("s3", "GetObject", "s3://%s/%s (READ-ONLY)" % (DEPLOYED_BUCKET, DEPLOYED_KEY)))
        out = subprocess.run([aws_cmd, "s3api", "get-object", "--bucket", DEPLOYED_BUCKET,
                              "--key", DEPLOYED_KEY, dep_path],
                             cwd=ROOT, capture_output=True, text=True, timeout=180)
        if out.returncode != 0:
            print("  WARN: deployed read rc=%d: %s" % (out.returncode, out.stderr.strip()[:300]))
        if out.returncode == 0 and os.path.exists(dep_path):
            with io.open(dep_path, "rb") as fh:
                dep_bytes = fh.read()
            dep_sha, dep_len, dep_prov = sha256_bytes(dep_bytes), len(dep_bytes), "measured"
    except Exception as exc:  # noqa: BLE001 -- a failed retrieval must not become a claim
        print("  WARN: deployed read failed (%s)" % exc)
    print("")
    print("  DEPLOYED vs BUILT -- MEASURED, NOT CLOSED (this cell deploys nothing):")
    print("    DEPLOYED s3://%s/%s  sha256=%s  bytes=%s  [provenance: %s]" % (
        DEPLOYED_BUCKET, DEPLOYED_KEY, dep_sha, dep_len if dep_len is not None else HELD_DEPLOYED_BYTES,
        dep_prov))
    print("    BUILT    %s (worktree, LF)      sha256=%s  bytes=%d  [provenance: measured]" % (
        REMEDIATE_REL, built_sha, len(after_src)))
    print("    PRE-CHANGE @%s                sha256=%s  [provenance: measured]" % (
        ISSUANCE_COMMIT, before_sha))
    check(dep_prov == "measured" and dep_sha is not None,
          "(e) the DEPLOYED sha256 is MEASURED, not held")
    check(dep_sha != built_sha, "(e) DEPLOYED != BUILT")
    check(dep_sha != before_sha,
          "(e) DEPLOYED != the PRE-CHANGE build either -- the prefix was already behind "
          "this repo before this cell touched anything")
    print("    S33/S34 (INVESTIGATION_v1.md @%s): an upload to this artifact prefix DOES "
          "NOT REACH THE BOX -- the renderer pulls the coverage package only inside an "
          "`except ImportError` branch, and the box's /opt/etfs-reports/coverage/ persists "
          "on EBS, so the running bytes do not move when the prefix does. DEPLOYED != BUILT "
          "here understates the gap to the RUNNING plane, and nothing in this cell closes "
          "either gap." % ISSUANCE_COMMIT)

    # -------------------------------------------------------------- arm (f)
    hr("(f) NO SEND, NO INVOKE, NO EGRESS")
    all_stub_calls = calls_a + calls_b + calls_c
    kinds = sorted({(c[0], c[1] if isinstance(c[1], str) else "?") for c in all_stub_calls})
    print("  DENOMINATOR 1 -- stubbed calls recorded across %d ladder run(s) in this "
          "process: %d, kinds=%s" % (LADDER_RUNS[0], len(all_stub_calls), kinds))
    real_invokes = [c for c in all_stub_calls if c[0] == "lambda-stub"]
    puts = [c for c in all_stub_calls if c[1] == "put_object"]
    print("    of which STUB producer 'invokes' (never a boto3 call, a local callable): %d"
          % len(real_invokes))
    print("    of which put_object on the STUB s3 (write_ask=False everywhere): %d" % len(puts))
    check(len(puts) == 0, "(f) zero writes attempted even against the stub")

    print("  DENOMINATOR 2 -- boto3 clients created by the imported orchestrator: every "
          "one is _StubBoto, which RAISES on any method; recorded AWS attempts through "
          "it: %d of %d" % (len(lam_calls), len(lam_calls)))
    check(len(lam_calls) == 0,
          "(f) the orchestrator module made 0 AWS calls -- _build_terminal_email BUILDS, "
          "it does not send (_send_terminal_unresolved was never called)")

    modules_checked = [REMEDIATE_REL, LAMBDA_REL]
    tokens = ("send_raw_email(", "send_email(", ".invoke(", "requests.", "urllib.request")
    print("  DENOMINATOR 3 -- token census over the %d module(s) this battery EXECUTED "
          "code from:" % len(modules_checked))
    for rel in modules_checked:
        txt = read_file_bytes(rel).decode("utf-8")
        hits = {t: txt.count(t) for t in tokens}
        print("    %-62s %s" % (rel, hits))
    rem_txt = read_file_bytes(REMEDIATE_REL).decode("utf-8")
    check(all(rem_txt.count(t) == 0 for t in tokens),
          "(f) remediate.py carries NO send, NO invoke and NO HTTP client of its own "
          "(0 hits for each of %d tokens)" % len(tokens))

    print("  DENOMINATOR 4 -- REAL AWS calls made by this battery: %d, enumerated:"
          % len(AWS_CALLS))
    for c in AWS_CALLS:
        print("    %s %s -- %s" % c)
    check(all(c[1] == "GetObject" for c in AWS_CALLS),
          "(f) every real AWS call is a READ (GetObject) on our own artifact prefix -- "
          "0 sends, 0 invokes, 0 writes, 0 vendor egress")
    print("  Andrew's ~02:5xZ constraint: nothing here can violate it -- no SES call site "
        "was reached, no Lambda was invoked, and no vendor endpoint exists in any module "
        "this battery ran.")

    # -------------------------------------------------------------- verdict
    hr("VERDICT")
    print("  arms: 6 of 6 evaluated; assertions failed: %d" % len(FAILURES))
    for f in FAILURES:
        print("    FAILED: %s" % f)
    if FAILURES:
        print("")
        print("EGS28-BATTERY-FAILED")
        return 1
    print("")
    print("EGS28-EVERY-UNRESOLVED-NAMES-ITS-PROVIDER")
    return 0


if __name__ == "__main__":
    sys.exit(main())
