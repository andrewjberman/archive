#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-29 -- S29-AC1: THE LADDER-SKIPPED BRANCH CARRIES THE PROPERTY.

Seven arms, each one clause, every number beside its denominator. The token
EGS29-SKIPPED-BRANCH-CARRIES-THE-PROPERTY prints ONLY when all seven hold.

  (a) the defect reproduces first, and the writer population is enumerated FROM SOURCE
      (AST census over BOTH files, not from the task order's list)
  (b) every record on the skipped branch names its provider  [DIFFERENCE control]
  (c) an unmapped partner still reads as unknown             [POSITIVE control]
  (d) the egress ask is recorded for the run                 [DIFFERENCE control, carries
      the outcome: the equivalent beside a real rung-3 ask over the same input]
  (e) the ladder branch did not move                         [INVARIANCE]
  (f) the deploy is real and reversible, and nothing else fired  [CENSUS]
  (g) the tree this battery measured in                      [CENSUS + positive control]

HERMETIC BY CONSTRUCTION: boto3.client and subprocess.run are POISONED before either
renderer module is imported, so any AWS call or any box-bootstrap `aws s3 cp` raises
instead of reaching the world. Arm (f) reads a separately-recorded deploy evidence file
(the only AWS the cell touches) rather than making calls of its own.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
from datetime import date

TOKEN = "EGS29-SKIPPED-BRANCH-CARRIES-THE-PROPERTY"

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
RENDERER = os.path.join(REPO, "data", "etfs", "scripts", "presentation", "render_month_end.py")
REMEDIATE = os.path.join(REPO, "data", "etfs", "scripts", "coverage", "remediate.py")
EVIDENCE = os.path.join(HERE, "egs29_deploy_evidence.json")

# The BEFORE side, pinned by COMMIT and resolved by CONTENT (a negative control asserts
# the blob does NOT carry the fix), never by filename or by "the previous version".
BEFORE_REF = "2a672685b99ebe46dfe1d4b08053e2d48283879e"

MONTH = "2026-08"
FAILS: list = []


def head(n, title):
    print("")
    print("=" * 100)
    print("ARM (%s) -- %s" % (n, title))
    print("=" * 100)


def check(arm, ok, label):
    print("  [%s] %s :: %s" % ("PASS" if ok else "FAIL", arm, label))
    if not ok:
        FAILS.append("%s: %s" % (arm, label))
    return ok


def git(*args) -> str:
    out = subprocess._REAL_RUN(["git"] + list(args), cwd=REPO, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if out.returncode != 0:
        raise RuntimeError("git %s rc=%d %s" % (args, out.returncode, out.stderr[:300]))
    return out.stdout.decode("utf-8", "replace")


def git_bytes(*args) -> bytes:
    out = subprocess._REAL_RUN(["git"] + list(args), cwd=REPO, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if out.returncode != 0:
        raise RuntimeError("git %s rc=%d %s" % (args, out.returncode, out.stderr[:300]))
    return out.stdout


# ---------------------------------------------------------------------------
# HERMETICITY -- poison the world before anything imports the renderer
# ---------------------------------------------------------------------------
subprocess._REAL_RUN = subprocess.run
AWS_CALLS: list = []
SUBPROCESS_CALLS: list = []


class _NoAWS:
    """Any attribute access is a call attempt; every call raises. Nothing reaches AWS."""

    def __init__(self, service):
        self._service = service

    def __getattr__(self, name):
        def _boom(*a, **k):
            AWS_CALLS.append((self._service, name))
            raise AssertionError("HERMETICITY BREACH: boto3 %s.%s(...) attempted"
                                 % (self._service, name))
        return _boom


def _no_subprocess(*a, **k):
    SUBPROCESS_CALLS.append(a[0] if a else k.get("args"))
    raise AssertionError("HERMETICITY BREACH: subprocess.run attempted: %r" % (a[:1],))


import boto3  # noqa: E402

boto3.client = lambda service, *a, **k: _NoAWS(service)
subprocess.run = _no_subprocess

for p in (REPO,
          os.path.join(REPO, "data", "etfs", "scripts"),
          os.path.join(REPO, "data", "inf", "scripts", "silver")):
    if p not in sys.path:
        sys.path.insert(0, p)

from coverage import remediate as REM  # noqa: E402


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Stubs: a recording S3 with a real in-memory store (so the ask MERGE is exercised)
# ---------------------------------------------------------------------------
class StubS3:
    def __init__(self, existing=None):
        self.existing = {k: set(v) for k, v in (existing or {}).items()}
        self.store: dict = {}
        self.puts: list = []
        self.gets: list = []

    def get_paginator(self, name):
        assert name == "list_objects_v2"
        return self

    def paginate(self, Bucket, Prefix):
        partner = Prefix.split("/")[1]
        yield {"Contents": [{"Key": "daily/%s/%s.json" % (partner, d)}
                            for d in sorted(self.existing.get(partner, set()))]}

    def head_object(self, Bucket, Key):
        partner = Key.split("/")[1]
        d = Key.rsplit("/", 1)[-1][: -len(".json")]
        if d in self.existing.get(partner, set()):
            return {}
        raise Exception("404 Not Found")

    def get_object(self, Bucket, Key, **kw):
        self.gets.append(Key)
        if Key not in self.store:
            raise Exception("404 Not Found")
        return {"Body": io.BytesIO(self.store[Key])}

    def put_object(self, Bucket, Key, Body, ContentType=None, **kw):
        self.store[Key] = Body if isinstance(Body, bytes) else Body.encode("utf-8")
        self.puts.append((Bucket, Key, len(self.store[Key])))
        return {}


class ExplodingLam:
    def invoke(self, **kw):
        raise AssertionError("lam.invoke must never be called on a --no-ladder arm")


def slice_row(v, as_of):
    return {"DIVZ": {"v": v, "n": 1, "as_of": as_of}}


sys.path.insert(0, os.path.join(REPO, "lib"))
from lib import trading_calendar as tcal  # noqa: E402

AUG = [d.isoformat() for d in tcal.trading_days_between(date(2026, 8, 1), date(2026, 8, 31))]
assert len(AUG) == 21, len(AUG)

# THE CASE that reaches every record-producing path on the skipped branch: COVERED days,
# one A day (a weekend -- supplied by the calendar, not by this fixture), one B day
# (priced 0), one C day (priced > 0), one D day (no partition) and one UNKNOWN day (the
# probe declines to answer). C, D and UNKNOWN are the three classes the branch records.
COVERED = AUG[:16]
D_C, D_D, D_UNK, D_B = AUG[16], AUG[17], AUG[18], AUG[19]
LAST = AUG[20]
PROBE_ANSWERS = {
    D_C: {"partition": True, "priced": 4242},
    D_D: {"partition": False, "priced": 0},
    D_UNK: None,
    D_B: {"partition": True, "priced": 0},
    LAST: {"partition": True, "priced": 7},
}


def probe(partner, date_str):
    return PROBE_ANSWERS.get(date_str, {"partition": True, "priced": 1})


DAILY = {"cottonwood": {d: slice_row(100.0, d) for d in COVERED}}


# ===========================================================================
# (a) THE DEFECT REPRODUCES, AND THE WRITER POPULATION IS ENUMERATED FROM SOURCE
# ===========================================================================
def census_record_sites(src: str, label: str) -> list:
    """Every per-day record CONSTRUCTOR in `src`, found by reading the source.

    POPULATION RULE, stated so the denominator is a subtraction and not a recall list:
    every `ast.Dict` LITERAL in the file whose key set contains BOTH "date" and "class".
    That is what a per-day record is. Each hit is then BANDED by where its value flows:
      UNRESOLVED  -- appended to a list whose name starts with "unresolved", or the
                     element of a comprehension bound to a dict key "unresolved" or to a
                     variable whose name starts with "unresolved"
      ASK-ENTRY   -- anything else (rung 3 builds ask entries of the same shape)

    THE BAND RULE IS ITSELF A HAZARD and is stated rather than trusted: it reads NAMES.
    A record that reached `unresolved` through a differently-named variable would band as
    ASK-ENTRY, so the ASK-ENTRY band is PRINTED IN FULL beside the other, and the reader
    checks it -- the point of a denominator is that nothing leaves the population silently.
    """
    tree = ast.parse(src)
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    def ancestors(node):
        cur = parents.get(node)
        while cur is not None:
            yield cur
            cur = parents.get(cur)

    def enclosing_def(node):
        for a in ancestors(node):
            if isinstance(a, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return a.name
        return "<module>"

    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [k.value for k in node.keys
                if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        if not ("date" in keys and "class" in keys):
            continue
        band = "ASK-ENTRY"
        for a in ancestors(node):
            if (isinstance(a, ast.Call) and isinstance(a.func, ast.Attribute)
                    and a.func.attr == "append" and isinstance(a.func.value, ast.Name)
                    and a.func.value.id.startswith("unresolved")):
                band = "UNRESOLVED"
                break
            if isinstance(a, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id.startswith("unresolved")
                    for t in a.targets):
                band = "UNRESOLVED"
                break
            if isinstance(a, (ast.ListComp, ast.GeneratorExp)):
                p = parents.get(a)
                if isinstance(p, ast.Dict):
                    for k, v in zip(p.keys, p.values):
                        if v is a and isinstance(k, ast.Constant) and k.value == "unresolved":
                            band = "UNRESOLVED"
                            break
                if band == "UNRESOLVED":
                    break
        hits.append({"file": label, "line": node.lineno, "func": enclosing_def(node),
                     "band": band, "has_provider": "provider" in keys, "keys": keys})
    return sorted(hits, key=lambda h: h["line"])


def arm_a():
    head("a", "THE DEFECT REPRODUCES FIRST, AND THE WRITER POPULATION IS ENUMERATED "
              "FROM SOURCE")
    before_blob = git_bytes("show", "%s:data/etfs/scripts/presentation/render_month_end.py"
                            % BEFORE_REF).decode("utf-8")
    print("BEFORE side pinned by COMMIT and resolved by CONTENT:")
    print("  ref            %s" % BEFORE_REF)
    print("  subject        %s" % git("log", "-1", "--format=%s", BEFORE_REF).strip()[:120])
    print("  blob bytes     %d   sha256 %s"
          % (len(before_blob.encode("utf-8")),
             hashlib.sha256(before_blob.encode("utf-8")).hexdigest()))
    neg = "_skipped_branch_egress_ask" not in before_blob
    check("a", neg, "NEGATIVE CONTROL: the BEFORE blob does NOT carry this cell's fix "
                    "(marker `_skipped_branch_egress_ask` absent) -- so it is genuinely "
                    "the before side and not the same file twice")

    after_src = io.open(RENDERER, encoding="utf-8").read()
    rem_src = io.open(REMEDIATE, encoding="utf-8").read()
    rem_head = git("log", "-1", "--format=%h %s", "--", REMEDIATE).strip()
    print("")
    print("CENSUS -- every per-day record CONSTRUCTOR across BOTH files, by AST, read")
    print("from the source and not from the task order's list (that list is the issuer's,")
    print("and a list is exactly how the fifth writer went uncounted).")
    print("  rule: an ast.Dict literal whose keys contain BOTH \"date\" and \"class\"")
    print("  remediate.py at   %s" % rem_head)

    for label, src in (("BEFORE render_month_end.py @%s" % BEFORE_REF[:10], before_blob),
                       ("AFTER  render_month_end.py (worktree)", after_src),
                       ("remediate.py (worktree, EG-s-28 terminal)", rem_src)):
        hits = census_record_sites(src, label)
        unres = [h for h in hits if h["band"] == "UNRESOLVED"]
        with_p = [h for h in unres if h["has_provider"]]
        print("")
        print("  %s" % label)
        print("    DENOMINATOR: %d per-day record site(s); %d UNRESOLVED-record site(s), "
              "%d ASK-ENTRY site(s)" % (len(hits), len(unres), len(hits) - len(unres)))
        for h in hits:
            print("      line %-5d %-28s %-11s provider=%-5s keys=%s"
                  % (h["line"], h["func"], h["band"], h["has_provider"], ",".join(h["keys"])))
        print("    UNRESOLVED sites carrying `provider`: %d of %d" % (len(with_p), len(unres)))
        if label.startswith("BEFORE"):
            check("a", len(unres) == 1 and len(with_p) == 0,
                  "the BEFORE renderer has 1 UNRESOLVED site and 0 of 1 carries `provider`")
        elif label.startswith("AFTER"):
            check("a", len(unres) == 1 and len(with_p) == 1,
                  "the AFTER renderer has 1 UNRESOLVED site and 1 of 1 carries `provider`")
        else:
            check("a", len(unres) == 4 and len(with_p) == 4,
                  "remediate.py has 4 UNRESOLVED sites and 4 of 4 carry `provider` "
                  "(EG-s-28, unmoved by this cell)")

    n_renderer = len([h for h in census_record_sites(after_src, "x")
                      if h["band"] == "UNRESOLVED"])
    n_remediate = len([h for h in census_record_sites(rem_src, "y")
                       if h["band"] == "UNRESOLVED"])
    total_unres = n_renderer + n_remediate
    print("")
    print("  POPULATION ACROSS BOTH FILES: %d UNRESOLVED-record site(s) -- %d in "
          "remediate.py + %d in render_month_end.py. The task order says the same; it was "
          "MEASURED here rather than adopted, which is the whole point: EG-s-28 asked "
          "whether four was the POPULATION or merely the list it was handed, and it was "
          "not." % (total_unres, n_remediate, n_renderer))
    check("a", total_unres == 5, "the writer population is 5 of 5, measured from source")

    print("")
    print("THE DEFECT ITSELF, on the BEFORE bytes (hermetic; boto3 poisoned):")
    path_before = os.path.join(REPO, ".scratch", "egs29_before_render_month_end.py")
    os.makedirs(os.path.dirname(path_before), exist_ok=True)
    io.open(path_before, "w", encoding="utf-8", newline="").write(before_blob)
    before = load_module(path_before, "egs29_before_renderer")
    before.s3 = StubS3()
    before.lam = ExplodingLam()
    res = before.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=False,
                               probe=probe)
    recs = res["unresolved"]["cottonwood"]
    lacking = [r for r in recs if "provider" not in r]
    print("  --no-ladder verdict=%s holes=%d   unresolved records: %d"
          % (res["verdict"], res["holes"], len(recs)))
    for r in recs:
        print("    %s | cottonwood | %s | %s | %s"
              % (r["date"], r.get("provider", "(not stated)"), r["class"], r["reason"]))
    print("  records LACKING `provider`: %d of %d" % (len(lacking), len(recs)))
    print("  S3 puts made by the BEFORE branch: %d (rung 3 unreachable, no ask of any kind)"
          % len(before.s3.puts))
    check("a", len(recs) > 0 and len(lacking) == len(recs),
          "the premise HOLDS: 0 of %d records on the BEFORE skipped branch carry "
          "`provider`" % len(recs))
    check("a", len(before.s3.puts) == 0,
          "the BEFORE skipped branch records NO egress ask (0 put_object) -- the second "
          "half of the defect")
    return before, res


# ===========================================================================
# (b) EVERY RECORD ON THE SKIPPED BRANCH NAMES ITS PROVIDER
# ===========================================================================
def arm_b(before_res):
    head("b", "EVERY RECORD ON THE SKIPPED BRANCH NAMES ITS PROVIDER  [DIFFERENCE control]")
    after = load_module(RENDERER, "egs29_after_renderer")
    stub = StubS3()
    after.s3 = stub
    after.lam = ExplodingLam()
    res = after.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=False,
                              probe=probe)
    recs = res["unresolved"]["cottonwood"]
    classes = sorted({r["class"] for r in recs})
    print("THE CASE reaches every record-producing path on this branch: classes present "
          "in the records = %s (the branch records exactly C, D and UNKNOWN; A/B/COVERED "
          "are excluded by the branch's own filter and are present in the month)" % classes)
    summary = res["per_partner"]["cottonwood"]["summary"]
    print("  month class census (denominator = %d calendar-mapped day(s) of the month): %s"
          % (sum(v for k, v in summary.items() if k in ("A", "COVERED", "B", "C", "D",
                                                        "UNKNOWN")),
             {k: summary[k] for k in ("A", "COVERED", "B", "C", "D", "UNKNOWN")}))
    with_p = [r for r in recs if r.get("provider")]
    print("")
    for r in recs:
        print("    %s | cottonwood | %s | %s | %s"
              % (r["date"], r.get("provider", "(not stated)"), r["class"], r["reason"]))
    print("  carrying `provider`: %d of %d" % (len(with_p), len(recs)))
    check("b", len(recs) > 0 and len(with_p) == len(recs),
          "%d of %d records on the AFTER skipped branch carry `provider`"
          % (len(with_p), len(recs)))

    print("")
    print("THE VALUE IS COMPARED AGAINST remediate.py, not asserted: the same partner's")
    print("record built by remediate.remediate_month (the module EG-s-28 fixed) is asked")
    print("for its provider, and the two are compared byte for byte.")
    lad = REM.remediate_month(
        "cottonwood", MONTH,
        {r["date"]: {"class": r["class"], "probe": None} for r in recs},
        invoke=None, s3=None, write_ask=False)
    lad_vals = {r.get("provider") for r in lad["unresolved"]}
    skip_vals = {r.get("provider") for r in recs}  # .get: a MUTANT that drops the field must FAIL the clause, not crash the battery
    print("  remediate.remediate_month -> %r  (%d record(s))" % (lad_vals, len(lad["unresolved"])))
    print("  skipped branch            -> %r  (%d record(s))" % (skip_vals, len(recs)))
    check("b", lad_vals == skip_vals and lad_vals == {"Black Diamond"},
          "the skipped branch's provider EQUALS remediate.py's for the same partner")

    print("")
    print("DIFFERENCE CONTROL -- the SAME run, engaged and disengaged (BEFORE bytes vs")
    print("AFTER bytes, same month, same series, same probe):")
    b_recs = before_res["unresolved"]["cottonwood"]
    print("  BEFORE: %d record(s), %d carry `provider`"
          % (len(b_recs), len([r for r in b_recs if "provider" in r])))
    print("  AFTER : %d record(s), %d carry `provider`" % (len(recs), len(with_p)))
    same_shape = ([(r["date"], r["class"], r["reason"]) for r in b_recs]
                  == [(r["date"], r["class"], r["reason"]) for r in recs])
    check("b", same_shape,
          "date/class/reason IDENTICAL either side -- the ONLY difference is the new "
          "field, so the control discriminates the change and nothing else")
    return after, res, stub


# ===========================================================================
# (c) AN UNMAPPED PARTNER STILL READS AS UNKNOWN  [POSITIVE control]
# ===========================================================================
def arm_c(after):
    head("c", "AN UNMAPPED PARTNER STILL READS AS UNKNOWN  [POSITIVE control: the "
              "honest-absence path can still fire]")
    partner = "acmecapital"
    print("PARTNER %r is absent from remediate._PROVIDER_BY_PARTNER (mapped partners: %s)"
          % (partner, sorted(REM._PROVIDER_BY_PARTNER)))
    stub = StubS3()
    after.s3 = stub
    after.lam = ExplodingLam()
    res = after.coverage_gate(MONTH, [partner], {partner: {d: slice_row(1.0, d)
                                                           for d in COVERED}},
                              ["DIVZ"], ladder=False, probe=probe)
    skipped = res["unresolved"][partner]
    vals = {r.get("provider") for r in skipped}
    print("  SKIPPED branch : %d record(s), provider value(s) %r" % (len(skipped), vals))

    lad = REM.remediate_month(partner, MONTH,
                              {r["date"]: {"class": r["class"], "probe": None}
                               for r in skipped},
                              invoke=None, s3=None, write_ask=False)
    lvals = {r.get("provider") for r in lad["unresolved"]}
    print("  LADDER  branch : %d record(s), provider value(s) %r" % (len(lad["unresolved"]),
                                                                    lvals))
    check("c", vals == {"<no provider mapped>"},
          "the skipped branch renders the honest absence marker '<no provider mapped>' "
          "-- never a guess, never None")
    check("c", vals == lvals,
          "BYTE-IDENTICAL to what the ladder branch renders for the same partner")
    check("c", all(r.get("provider") is not None for r in skipped),
          "no record carries a null provider")
    return res


# ===========================================================================
# (d) THE EGRESS ASK IS RECORDED FOR THE RUN  [DIFFERENCE control -- carries the outcome]
# ===========================================================================
def arm_d(after):
    head("d", "THE EGRESS ASK IS RECORDED FOR THE RUN  [DIFFERENCE control; this is the "
              "arm that unblocks EG-s-21]")
    skip_stub = StubS3()
    after.s3 = skip_stub
    after.lam = ExplodingLam()
    after.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=False, probe=probe)
    print("PUT CENSUS, --no-ladder run: %d object(s)" % len(skip_stub.puts))
    for b, k, n in skip_stub.puts:
        print("    s3://%s/%s  (%d B)" % (b, k, n))
    equiv_key = "platinum/reports/%s/coverage_egress_ask_ladder_skipped.json" % MONTH
    rung3_key = "platinum/reports/%s/coverage_egress_ask.json" % MONTH
    keys = [k for _b, k, _n in skip_stub.puts]
    check("d", equiv_key in keys, "the run RECORDED an egress ask at %s" % equiv_key)
    check("d", rung3_key not in keys,
          "and did NOT write rung 3's own artifact %s -- so EG-s-26's disclosure "
          "(`ABSENT BY CONSTRUCTION`) stays TRUE, and a rehearsal run can never merge "
          "into the document a person authorises real egress on" % rung3_key)
    if equiv_key not in skip_stub.store:
        # FAIL-SOFT, and deliberately: the MUTANT control breaks exactly this, and a
        # battery that CRASHES instead of recording a FAIL cannot be used as its own
        # mutant oracle -- the crash and a real defect would look different only in the
        # traceback.
        check("d", False, "no ask record was written, so nothing can be compared against "
                          "a real rung-3 ask -- the rest of this arm is UNEVALUATED")
        return None, None, None
    equiv = json.loads(skip_stub.store[equiv_key])
    print("")
    print("THE RECORD, WHOLE:")
    print(json.dumps(equiv, indent=2))

    # --- the real rung-3 ask, from an UNFORCED LADDER run over the SAME input ---
    lad_stub = StubS3()
    after.s3 = lad_stub
    after.lam = ExplodingLam()
    after._make_invoke = lambda lam_client=None: (lambda fn, payload: {"status": "ok"})
    after.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=True, probe=probe)
    print("")
    print("PUT CENSUS, LADDER run over the SAME input: %d object(s)" % len(lad_stub.puts))
    for b, k, n in lad_stub.puts:
        print("    s3://%s/%s  (%d B)" % (b, k, n))
    check("d", rung3_key in lad_stub.store,
          "the ladder run wrote a REAL rung-3 ask at %s -- so the comparison below is "
          "against a real one, not a reconstruction" % rung3_key)
    real = json.loads(lad_stub.store[rung3_key])
    print("")
    print("THE REAL RUNG-3 ASK, WHOLE:")
    print(json.dumps(real, indent=2))

    print("")
    print("EVERY FIELD THAT DIFFERS (denominator = the union of both key sets):")
    allk = sorted(set(equiv) | set(real))
    diffs = []
    for k in allk:
        a, b = equiv.get(k, "<ABSENT>"), real.get(k, "<ABSENT>")
        same = (a == b)
        if not same:
            diffs.append(k)
        print("  %-22s %s" % (k, "IDENTICAL" if same else "DIFFERS"))
        if not same:
            print("      equivalent : %s" % json.dumps(a)[:400])
            print("      rung 3     : %s" % json.dumps(b)[:400])
    print("  %d of %d field(s) differ: %s" % (len(diffs), len(allk), diffs))

    check("d", equiv.get("rung3_ran") is False and "RUNG 3 DID NOT RUN" in equiv["written_by"],
          "the record SAYS it was written by the skipped branch and not by rung 3 -- a "
          "reader cannot mistake the equivalent for the original")
    check("d", equiv.get("authorization") == real.get("authorization")
          and str(equiv.get("authorization", "")).startswith("PER-USE"),
          "the PER-USE authorization semantics are rung 3's OWN string, byte-identical")
    ask_rows = equiv.get("asks", [])
    ok_rows = [a for a in ask_rows if a.get("partner") and a.get("provider") and a.get("date")]
    print("  ask rows carrying date+partner+provider: %d of %d" % (len(ok_rows), len(ask_rows)))
    check("d", ask_rows and len(ok_rows) == len(ask_rows),
          "every ask row carries its date, its partner AND its provider")
    check("d", equiv.get("ask_scope") == real.get("ask_scope"),
          "`ask_scope` is rung 3's own merge verdict (%r), not a restatement"
          % equiv.get("ask_scope"))
    check("d", equiv.get("partners_covered") == real.get("partners_covered"),
          "`partners_covered` identical -- the month-completeness EG-s-23 added is "
          "inherited, not re-implemented")
    return equiv, real, diffs


# ===========================================================================
# (e) THE LADDER BRANCH DID NOT MOVE  [INVARIANCE]
# ===========================================================================
def volatile_strip(v: dict) -> dict:
    out = json.loads(json.dumps(v))
    out.pop("generated_at", None)
    f = out.get("forcing", {})
    f.pop("run_id", None)
    f.pop("run_id_source", None)
    return out


def arm_e(before, after):
    head("e", "THE LADDER BRANCH DID NOT MOVE  [INVARIANCE]")
    scenarios = {
        "COMPLETE (no holes)": ({"cottonwood": {d: slice_row(100.0, d) for d in AUG}},
                                set(AUG)),
        "5 HOLES (C/D/UNKNOWN/B mix)": (DAILY, set(COVERED)),
    }
    quantities = ("verdict", "holes", "A", "COVERED", "B", "C", "D", "UNKNOWN")
    compared = 0
    identical = 0
    verdicts = set()
    for label, (daily, existing) in scenarios.items():
        for mod, side in ((before, "BEFORE"), (after, "AFTER")):
            mod.lam = ExplodingLam()
            mod._make_invoke = lambda lam_client=None: (lambda fn, payload: {"status": "ok"})
        pre_stub = StubS3({"cottonwood": existing})
        post_stub = StubS3({"cottonwood": existing})
        before.s3, after.s3 = pre_stub, post_stub
        rb = before.coverage_gate(MONTH, ["cottonwood"], daily, ["DIVZ"], ladder=True,
                                  probe=probe)
        ra = after.coverage_gate(MONTH, ["cottonwood"], daily, ["DIVZ"], ladder=True,
                                 probe=probe)
        sb, sa = rb["per_partner"]["cottonwood"]["summary"], ra["per_partner"]["cottonwood"]["summary"]
        verdicts.add(rb["verdict"])
        print("")
        print("  scenario %r (ladder=True)" % label)
        for q in quantities:
            vb = rb[q] if q in ("verdict", "holes") else sb[q]
            va = ra[q] if q in ("verdict", "holes") else sa[q]
            compared += 1
            identical += int(vb == va)
            print("    %-9s BEFORE=%-8s AFTER=%-8s %s"
                  % (q, vb, va, "SAME" if vb == va else "*** MOVED ***"))
        ub = json.dumps(rb["unresolved"], sort_keys=True)
        ua = json.dumps(ra["unresolved"], sort_keys=True)
        compared += 1
        identical += int(ub == ua)
        print("    unresolved records BYTE-IDENTICAL: %s (%d B either side)"
              % (ub == ua, len(ub)))
        fb = json.dumps(volatile_strip(rb)["forcing"], sort_keys=True)
        fa = json.dumps(volatile_strip(ra)["forcing"], sort_keys=True)
        compared += 1
        identical += int(fb == fa)
        print("    forcing record (EG-s-25) + skip record (EG-s-26) BYTE-IDENTICAL on the "
              "LADDER branch: %s" % (fb == fa))
        compared += 1
        identical += int(json.dumps(volatile_strip(rb), sort_keys=True)
                         == json.dumps(volatile_strip(ra), sort_keys=True))
        print("    WHOLE verdict object byte-identical (volatile generated_at/run_id "
              "stripped): %s" % (json.dumps(volatile_strip(rb), sort_keys=True)
                                 == json.dumps(volatile_strip(ra), sort_keys=True)))
        print("    rung-3 asks written: BEFORE %d, AFTER %d; ladder-skipped key written: "
              "BEFORE %d, AFTER %d"
              % (len([k for _b, k, _n in pre_stub.puts if k.endswith("coverage_egress_ask.json")]),
                 len([k for _b, k, _n in post_stub.puts if k.endswith("coverage_egress_ask.json")]),
                 len([k for _b, k, _n in pre_stub.puts if "ladder_skipped" in k]),
                 len([k for _b, k, _n in post_stub.puts if "ladder_skipped" in k])))
        compared += 1
        identical += int([k for _b, k, _n in pre_stub.puts] == [k for _b, k, _n in post_stub.puts])

    print("")
    print("  DENOMINATOR: %d compared quantit(ies) across %d scenario(s) on ladder=True; "
          "%d IDENTICAL" % (compared, len(scenarios), identical))
    check("e", compared == identical,
          "the ladder branch did not move: %d of %d" % (identical, compared))
    check("e", verdicts == {"PUBLISH", "REFUSE"},
          "NEGATIVE CONTROL on the comparator: the two scenarios DISAGREE with each "
          "other (%s), so 'identical' is a measurement and not a constant" % sorted(verdicts))

    # the two records, present and unchanged, on BOTH branches
    print("")
    print("  EG-s-25's forcing record and EG-s-26's skip record, on BOTH branches:")
    fields = ("forced", "mechanism", "fixture_remove_spec", "fixture_remove",
              "removed_slice_count", "ladder_ran", "ladder_skip_mechanism",
              "rung3_stop_and_ask_reachable", "coverage_egress_ask_possible",
              "skip_note", "run_shape", "disclosure_version")
    ok_all = True
    for ladder in (True, False):
        before.s3 = StubS3({"cottonwood": set(COVERED)})
        after.s3 = StubS3({"cottonwood": set(COVERED)})
        rb = before.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=ladder,
                                  probe=probe)
        ra = after.coverage_gate(MONTH, ["cottonwood"], DAILY, ["DIVZ"], ladder=ladder,
                                 probe=probe)
        fb, fa = rb["forcing"], ra["forcing"]
        missing = [k for k in fields if k not in fa]
        moved = [k for k in fields if k in fa and fa[k] != fb.get(k)]
        print("    ladder=%-5s present %d of %d field(s); moved %d of %d: %s"
              % (ladder, len(fields) - len(missing), len(fields), len(moved), len(fields),
                 moved or "none"))
        ok_all = ok_all and not missing and not moved
    check("e", ok_all,
          "both records are PRESENT and UNCHANGED on their respective branches -- "
          "including `coverage_egress_ask_possible: false` and the skip_note naming "
          "coverage_egress_ask.json as absent by construction, which this cell keeps TRUE "
          "by writing its equivalent to a different key")


# ===========================================================================
# (f) THE DEPLOY IS REAL AND REVERSIBLE, AND NOTHING ELSE FIRED  [CENSUS]
# ===========================================================================
def arm_f():
    head("f", "THE DEPLOY IS REAL AND REVERSIBLE, AND NOTHING ELSE FIRED  [CENSUS]")
    if not os.path.exists(EVIDENCE):
        check("f", False, "deploy evidence %s ABSENT -- the deploy has not run" % EVIDENCE)
        return
    ev = json.load(io.open(EVIDENCE, encoding="utf-8"))
    print("EVIDENCE FILE: %s" % EVIDENCE)
    print("  bucket/key            s3://%s/%s" % (ev["bucket"], ev["key"]))
    print("  disposition           %s" % ev["disposition"])
    print("  prior VersionId       %s" % ev["prior_version_id"])
    print("  prior sha256          %s  (%s B)" % (ev["prior_sha256"], ev["prior_bytes"]))
    print("  committed sha256      %s  (%s B)" % (ev["committed_sha256"], ev["committed_bytes"]))
    print("  served  VersionId     %s" % ev["served_version_id"])
    print("  served  sha256        %s  (%s B)  RE-DOWNLOADED by VersionId: %s"
          % (ev["served_sha256"], ev["served_bytes"], ev["served_read_by_version_id"]))
    print("  served == committed   %s" % ev["served_equals_committed"])
    print("  NEGATIVE CONTROL prior != served: %s" % (ev["prior_sha256"] != ev["served_sha256"]))
    print("  rollback              %s" % ev["rollback_command"])
    print("  version history       %d version(s) on the key; %s"
          % (ev.get("version_history_count", 0), ev.get("latest_placement_note", "")))
    print("  ledger entry          %s" % ev["ledger_entry"])
    check("f", ev["served_equals_committed"] is True,
          "the SERVED object is byte-equal to the committed bytes, both sha256 printed, "
          "the served copy RE-DOWNLOADED by its VersionId rather than trusted from the PUT")
    check("f", ev["served_read_by_version_id"] is True,
          "the served read was by VersionId (not a bare GET that could race another writer)")
    check("f", ev["prior_sha256"] != ev["served_sha256"],
          "NEGATIVE CONTROL: prior sha256 DIFFERS from served, so the equality above "
          "discriminates and the rollback is a real restore, not a no-op")
    check("f", ev["prior_recorded_before_copy"] is True,
          "the prior sha256 + VersionId were recorded BEFORE the copy")

    art = ev["artifact_prefix_census"]
    print("")
    print("  ARTIFACT PREFIX %s : %d key(s) before, %d after; changed %d, added %d, "
          "removed %d" % (ev["prefix"], art["before_count"], art["after_count"],
                          len(art["changed"]), len(art["added"]), len(art["removed"])))
    for k in art["changed"]:
        print("      CHANGED %s" % k)
    check("f", art["before_count"] > 0 and art["after_count"] > 0,
          "ZERO GUARD: both listings NON-EMPTY before any delta is graded (an empty "
          "listing and an untouched population are the same value)")
    check("f", len(art["changed"]) <= 1 and not art["added"] and not art["removed"],
          "at most ONE key of %d changed between the listing pair, none added, none removed"
          % art["after_count"])
    moved = art.get("moved_since_entry_opened", [])
    print("    MOVED SINCE THE ENTRY OPENED (LastModified >= opened_at -- the measurement "
          "that survives a re-run, since a before/after listing pair on a second "
          "invocation reports zero and reads exactly like 'never touched'):")
    for k, lm in moved:
        print("      %s  %s" % (k, lm))
    print("      %d of %d key(s)" % (len(moved), art["after_count"]))
    check("f", len(moved) == 1 and moved[0][0] == ev["key"],
          "EXACTLY ONE key of %d moved during the act, and it is the ordered key"
          % art["after_count"])

    rep = ev["reports_prefix_census"]
    print("")
    print("  SERVED REPORTS %s : %d key(s) before, %d after; delta %d"
          % (rep["prefix"], rep["before_count"], rep["after_count"], len(rep["changed"])))
    for k in rep["changed"]:
        print("      CHANGED %s" % k)
    check("f", rep["before_count"] > 0,
          "ZERO GUARD on the reports listing: non-empty (%d key(s))" % rep["before_count"])
    rmoved = rep.get("moved_since_entry_opened", [])
    print("    MOVED SINCE THE ENTRY OPENED: %d of %d key(s) %s"
          % (len(rmoved), rep["after_count"], rmoved))
    print("    DISCLOSURE ON THIS DENOMINATOR: %s" % rep.get("disclosure", ""))
    check("f", not rep["changed"] and rep["before_count"] == rep["after_count"]
          and not rmoved,
          "NO WRITE under platinum/reports/ during this cell's deploy: 0 of %d key(s) "
          "moved, by BOTH instruments (listing pair and LastModified)"
          % rep["after_count"])

    print("")
    print("  SES: %s" % ev["ses_note"])
    print("    datapoints overlapping the act window: %d of %d for the UTC day"
          % (ev["ses_overlapping_datapoints"], ev["ses_day_datapoints"]))
    check("f", ev["ses_overlapping_datapoints"] == 0,
          "NO SES SEND: 0 datapoint(s) overlap the act window (the claim is TIME OVERLAP, "
          "not a whole-day zero -- other seats send legitimate mail)")
    print("  LAMBDA: %d function(s) checked of %d in the account (denominator BY "
          "SUBTRACTION: %d total MINUS %d whose name carries neither 'etf' nor 'report'); "
          "invocations summed = %d"
          % (ev["lambda_checked"], ev["lambda_total"], ev["lambda_total"],
             ev["lambda_total"] - ev["lambda_checked"], ev["lambda_invocations"]))
    check("f", ev["lambda_invocations"] == 0,
          "NO LAMBDA INVOKE across the checked functions in the act window")
    print("  ARGV CENSUS, second instrument on a different axis (what was ISSUED, not "
        "what FIRED): %d of %d recorded step(s) touch anything but s3api/s3/cloudwatch/"
        "lambda-list: %s" % (ev["argv_offaxis_steps"], ev["argv_total_steps"],
                             ev["argv_services"]))
    check("f", ev["argv_offaxis_steps"] == 0,
          "0 of %d recorded steps issued an SES call, a lambda invoke or an SSM command"
          % ev["argv_total_steps"])

    print("")
    print("  HERMETICITY OF THIS BATTERY ITSELF: boto3.client and subprocess.run were "
          "poisoned before any renderer import.")
    print("    boto3 call attempts: %d      subprocess.run attempts: %d"
          % (len(AWS_CALLS), len(SUBPROCESS_CALLS)))
    check("f", not AWS_CALLS and not SUBPROCESS_CALLS,
          "this battery made 0 AWS calls and 0 subprocess.run calls of its own")


# ===========================================================================
# (g) THE TREE THIS BATTERY MEASURED IN  [CENSUS + positive control]
# ===========================================================================
def arm_g():
    head("g", "THE TREE THIS BATTERY MEASURED IN  [CENSUS + positive control on the tool]")
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    hsh = git("rev-parse", "HEAD").strip()
    print("  worktree      %s" % REPO)
    print("  branch        %s" % branch)
    print("  HEAD          %s" % hsh)
    print("  git dir       %s" % git("rev-parse", "--git-dir").strip())
    print("  renderer      %s (%d B, sha256 %s)"
          % (RENDERER, os.path.getsize(RENDERER),
             hashlib.sha256(io.open(RENDERER, "rb").read()).hexdigest()))

    comprail = os.path.join(REPO, ".tools", "_comprail.py")
    src = io.open(comprail, encoding="utf-8").read()
    n = src.count("def corpus_root")
    print("")
    print("  ROW S35 -- the comp-rail resolved its corpus from the tool's INSTALL "
          "LOCATION until 838b963638, so a worktree-run census silently scanned the MAIN "
          "tree and returned a well-formed zero with a real denominator. PROVEN PRESENT "
          "HERE, not assumed:")
    print("    .tools/_comprail.py `def corpus_root` occurrences: %d" % n)
    anc = subprocess._REAL_RUN(["git", "merge-base", "--is-ancestor", "838b963638", "HEAD"],
                               cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("    838b963638 is an ancestor of HEAD: rc=%d (0 = yes)" % anc.returncode)
    check("g", n >= 1 and anc.returncode == 0,
          "the comp-rail corpus fix is IN THIS TREE (marker present AND the commit is in "
          "ancestry) -- proven, not assumed")

    print("")
    print("  POSITIVE CONTROL that a repo-wide census reads THIS worktree: a file that "
          "exists ONLY on this branch must appear in the hits.")
    only_here = "org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs29_skipped_branch_carries_the_property.py"
    tracked = git("ls-files", "--", only_here).strip()
    untracked = git("status", "--porcelain", "--", only_here).strip()
    print("    probe file            %s" % only_here)
    print("    tracked at HEAD       %r" % tracked)
    print("    working-tree status   %r" % untracked)
    present_on_disk = os.path.exists(os.path.join(REPO, only_here))
    print("    present on disk       %s" % present_on_disk)
    on_cloud = subprocess._REAL_RUN(["git", "cat-file", "-e", "CLOUD:%s" % only_here],
                                    cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("    present on CLOUD      %s (git cat-file rc=%d; 0 = present)"
          % (on_cloud.returncode == 0, on_cloud.returncode))
    check("g", present_on_disk and on_cloud.returncode != 0,
          "the probe file exists in THIS worktree and NOT on CLOUD -- so any census that "
          "finds it read this tree, and one that misses it read another")

    marker = "_skipped_branch_egress_ask"
    hits = [(p, i) for p in (RENDERER,)
            for i, line in enumerate(io.open(p, encoding="utf-8").read().splitlines(), 1)
            if marker in line]
    print("")
    print("    census of %r over the ordered path (denominator = 1 file, %d line(s)): "
          "%d hit(s) at line(s) %s"
          % (marker, len(io.open(RENDERER, encoding="utf-8").read().splitlines()),
             len(hits), [i for _p, i in hits]))
    check("g", len(hits) >= 2, "the cell's own marker is present in the file it names")


def main() -> int:
    print("=" * 100)
    print("ETFS_GUARDRAIL.TO-EG-s-29 -- S29-AC1 BATTERY")
    print("0.9.0_WK_ETFS_GUARDRAIL~5   %s" % os.environ.get("OPAL_AGENT_SERIAL", "<unset>"))
    print("=" * 100)
    before, before_res = arm_a()
    after, _after_res, _stub = arm_b(before_res)
    arm_c(after)
    arm_d(after)
    arm_e(before, after)
    arm_f()
    arm_g()

    print("")
    print("=" * 100)
    if FAILS:
        print("RESULT: %d FAILING clause(s)" % len(FAILS))
        for f in FAILS:
            print("   FAIL %s" % f)
        print("TOKEN WITHHELD")
        return 1
    print("RESULT: every clause of every arm holds (a,b,c,d,e,f,g -- 7 of 7)")
    print(TOKEN)
    return 0


if __name__ == "__main__":
    sys.exit(main())
