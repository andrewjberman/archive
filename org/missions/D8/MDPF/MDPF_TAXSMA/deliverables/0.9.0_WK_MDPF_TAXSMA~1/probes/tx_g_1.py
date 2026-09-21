#!/usr/bin/env python3
"""MDPF_TAXSMA TX-g-1 probe: one acceptance criterion per invocation (TXG1-AC1 .. TXG1-AC23).

    cd <WS> && timeout 120 py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/0.9.0_WK_MDPF_TAXSMA~1/probes/tx_g_1.py AC<n>

Each run prints its measurement with its vintage (HEAD, UTC time, the dirty state of the files under test) and
denominator, then exactly one line: `VERDICT: PASS-TXG1-AC<n>` or `VERDICT: FAIL-TXG1-AC<n> <reason>`.

  AC1 .. AC19  run the one test that carries the criterion, tests/test_taxsma_workbook.py::test_txg1_acNN, in a
               fresh process and forward its measurement lines. PASS = rc 0, '1 passed', the criterion's own
               measurement line present, and 'EGRESS-ATTEMPTS: 0'.
  AC20, AC21   run the WHOLE module with TXG1_CORPUS set, so every call of every test case lands in a corpus file
               (request shape, status, body, the audit records the call wrote, the synthetic fixture values), and
               scan that corpus HERE -- an instrument separate from the tests' own assertions.
  AC22         read the BEFORE record (probes/ac22_before.json, measured at the cut base with the Gateway tree
               untouched) and run the AFTER arm live: every Gateway test module in its own process (one process for
               the whole suite hangs, row NFRA_OPLGTW-W3-S12), test_schwab_engine.py beside the rest.
  AC23         read the two new files' imports against the Gateway's own import set at the cut base and its
               requirements.txt, find the broker and Graph stubs, and re-run the module with moto and msal refused.

  AC22 --record-before   writes probes/ac22_before.json; refused unless the Gateway tree equals HEAD.

A failed or empty read is a FAIL, never a zero.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve()
CUT_BASE = "fd2f1e4b31"
GW_REL = "infra/aws/ec2/opal-gateway"
TEST_REL = "tests/test_taxsma_workbook.py"
MODULE_REL = "app/taxsma_workbook.py"
CONTRACT_REL = "org/standards/MDPF_TAXSMA_DATA_CONTRACT.json"
BEFORE_RECORD = HERE.parent / "ac22_before.json"
UNDER_TEST = ["app/taxsma_workbook.py", "app/server.py", "app/config.py", "tests/test_taxsma_workbook.py",
              "tests/test_principal_cutover.py"]
PER_TEST_TIMEOUT = 100
MODULE_TIMEOUT = 105
HEAVY_MODULE = "test_schwab_engine.py"


def _utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git(repo: Path, *args: str) -> tuple:
    r = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


def _repo() -> Path:
    rc, out, err = _git(HERE.parent, "rev-parse", "--show-toplevel")
    if rc != 0 or not out.strip():
        raise RuntimeError("git rev-parse --show-toplevel failed: rc=%s %s" % (rc, err.strip()))
    return Path(out.strip())


def _env(**extra) -> dict:
    """The environment of every pytest this probe starts. AUDIT_PATH points at a scratch file: the Gateway's
    default is ./audit.jsonl, a TRACKED file, and a test that does not patch AUDIT_PATH appends to it when run
    from the Gateway directory (row MDPF_TAXSMA-W1-S2). Config reads AUDIT_PATH once at import, so the redirect
    changes where an unpatched record lands and nothing else."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    scratch = Path(__file__).resolve().parents[8] / ".scratch"
    scratch.mkdir(exist_ok=True)
    env["AUDIT_PATH"] = str(scratch / "txg1_unpatched_audit.jsonl")
    env.pop("TXG1_CORPUS", None)
    env.update(extra)
    return env


def _vintage(repo: Path) -> str:
    rc, head, _ = _git(repo, "rev-parse", "--short=10", "HEAD")
    paths = ["%s/%s" % (GW_REL, p) for p in UNDER_TEST]
    rc2, st, _ = _git(repo, "status", "--porcelain", "--", *paths)
    dirty = [ln.strip() for ln in st.splitlines() if ln.strip()]
    return "vintage: HEAD %s, %s UTC, files under test %d, dirty vs HEAD %d%s" % (
        head.strip() if rc == 0 else "UNREAD", _utc(), len(paths), len(dirty),
        (" (" + "; ".join(dirty) + ")") if dirty else "")


def _verdict(n: int, ok: bool, reason: str = "") -> int:
    if ok:
        print("VERDICT: PASS-TXG1-AC%d" % n, flush=True)
        return 0
    print("VERDICT: FAIL-TXG1-AC%d %s" % (n, reason or "unspecified"), flush=True)
    return 1


def _contract(repo: Path) -> dict:
    return json.loads((repo / CONTRACT_REL).read_text(encoding="utf-8"))


# --- AC1 .. AC19: one test each ---------------------------------------------------------------------------
def _single_test(repo: Path, n: int) -> int:
    gw = repo / GW_REL
    node = "%s::test_txg1_ac%02d" % (TEST_REL, n)
    cmd = [sys.executable, "-m", "pytest", node, "-q", "-p", "no:cacheprovider", "--color=no"]
    print("invocation: (cwd %s) %s" % (GW_REL, " ".join(cmd[1:])))
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=str(gw), capture_output=True, text=True, timeout=PER_TEST_TIMEOUT, env=_env())
    except subprocess.TimeoutExpired:
        print("TIMEOUT after %ds" % PER_TEST_TIMEOUT)
        return _verdict(n, False, "the test timed out (%ds)" % PER_TEST_TIMEOUT)
    out = (r.stdout or "") + (r.stderr or "")
    mine = re.compile(r"^TXG1-AC%d(?![0-9])" % n)
    measured = [ln for ln in out.splitlines() if mine.match(ln)]
    egress = [ln for ln in out.splitlines() if ln.startswith("EGRESS-ATTEMPTS:")]
    summary = [ln for ln in out.splitlines() if re.match(r"^\d+ (passed|failed|error)", ln) or " passed" in ln
               or " failed" in ln or " error" in ln]
    for ln in measured + egress:
        print(ln)
    print("pytest: %s | rc=%d | %.1fs" % (summary[-1].strip() if summary else "NO SUMMARY LINE", r.returncode,
                                          time.perf_counter() - t0))
    passed_one = re.search(r"(?m)^1 passed(?![^\n]*(failed|error))", out) is not None
    if r.returncode != 0 or not passed_one:
        tail = [ln for ln in out.splitlines() if ln.startswith(("E ", "FAILED", "ERROR"))][:12]
        for ln in tail:
            print("  " + ln)
        return _verdict(n, False, "test_txg1_ac%02d did not pass (rc=%d)" % (n, r.returncode))
    if not measured:
        return _verdict(n, False, "no TXG1-AC%d measurement line in the test output" % n)
    if egress != ["EGRESS-ATTEMPTS: 0"]:
        return _verdict(n, False, "egress line %r (expected exactly 'EGRESS-ATTEMPTS: 0')" % (egress,))
    return _verdict(n, True)


# --- AC20 / AC21: the whole-module corpus ------------------------------------------------------------------
def _corpus_run(repo: Path) -> tuple:
    gw = repo / GW_REL
    scratch = repo / ".scratch"
    scratch.mkdir(exist_ok=True)
    corpus = scratch / ("txg1_corpus_%d.jsonl" % os.getpid())
    if corpus.exists():
        corpus.unlink()
    cmd = [sys.executable, "-m", "pytest", TEST_REL, "-q", "-p", "no:cacheprovider", "--color=no"]
    print("invocation: (cwd %s) TXG1_CORPUS=<.scratch/%s> %s" % (GW_REL, corpus.name, " ".join(cmd[1:])))
    r = subprocess.run(cmd, cwd=str(gw), capture_output=True, text=True, timeout=PER_TEST_TIMEOUT,
                       env=_env(TXG1_CORPUS=str(corpus)))
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(?m)^(\d+) passed(.*)$", out)
    summary = m.group(0) if m else "NO SUMMARY LINE"
    entries = []
    if corpus.exists():
        for ln in corpus.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                entries.append(json.loads(ln))
        corpus.unlink()
    ok_run = r.returncode == 0 and m is not None and "failed" not in m.group(2) and "error" not in m.group(2)
    egress = [ln for ln in out.splitlines() if ln.startswith("EGRESS-ATTEMPTS:")]
    return ok_run, summary, r.returncode, entries, egress


def _walk(obj, keys: list, strings: list, numbers: list) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.append(str(k))
            _walk(v, keys, strings, numbers)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, keys, strings, numbers)
    elif isinstance(obj, bool) or obj is None:
        return
    elif isinstance(obj, (int, float)):
        numbers.append(obj)
    elif isinstance(obj, str):
        strings.append(obj)


def _fixture_values(entries: list) -> tuple:
    by_header: dict = {}
    tokens: set = set()
    for e in entries:
        if e.get("kind") != "fixture":
            continue
        for h, vals in (e.get("values_by_header") or {}).items():
            by_header.setdefault(h, set()).update(json.dumps(v) for v in vals)
        tokens.update(e.get("secrets") or [])
    return {h: {json.loads(v) for v in vs} for h, vs in by_header.items()}, tokens


def _hits(values: set, keys: list, strings: list, numbers: list) -> int:
    n = 0
    for v in values:
        if isinstance(v, bool) or v is None:
            continue
        if isinstance(v, str):
            if len(v.strip()) < 4:
                continue
            n += sum(1 for s in strings if v in s)
        elif isinstance(v, float):
            n += sum(1 for x in numbers if isinstance(x, float) and x == v)
    return n


def _ac20(repo: Path) -> int:
    contract = _contract(repo)
    prohibited = contract["capability"]["prohibited_response_fields"]
    headers = contract["workbook"]["expected_headers_after_outer_whitespace_trim"]
    response_fields = contract["capability"]["response_fields"]
    row_fields = contract["workbook"]["projected_columns"] + contract["workbook"]["row_metadata"]
    ok_run, summary, rc, entries, egress = _corpus_run(repo)
    print("module run: %s | rc=%d | %s" % (summary, rc, "; ".join(sorted(set(egress))) or "no egress line"))
    calls = [e for e in entries if e.get("kind") in ("call", "other_route")]
    route_calls = [e for e in calls if e.get("kind") == "call"]
    tests = sorted({e.get("test", "") for e in calls})
    by_header, secrets = _fixture_values(entries)
    if not ok_run or not calls or not by_header or not secrets:
        return _verdict(20, False, "corpus not usable (run ok=%s, calls=%d, fixture headers=%d, secrets=%d)"
                        % (ok_run, len(calls), len(by_header), len(secrets)))
    bodies = [e.get("body") for e in calls]
    audits = [a for e in calls for a in (e.get("audit") or [])]
    rk, rs, rn = [], [], []
    for b in bodies:
        _walk(b, rk, rs, rn)
    ak, as_, an = [], [], []
    for a in audits:
        _walk(a, ak, as_, an)
    print("corpus: %d test case(s), %d call(s) (%d to /ms/taxsma-workbook, %d to other routes), %d response body(ies), "
          "%d audit record(s); synthetic secrets %d distinct" % (len(tests), len(calls), len(route_calls),
                                                                 len(calls) - len(route_calls), len(bodies),
                                                                 len(audits), len(secrets)))
    bad = 0
    column_fields = [p for p in prohibited if p in headers]
    for f in column_fields:
        vals = by_header.get(f, set())
        scanned = [v for v in vals if (isinstance(v, str) and len(v.strip()) >= 4) or isinstance(v, float)]
        k_resp = sum(1 for k in rk if k == f)
        k_aud = sum(1 for k in ak if k == f)
        v_resp = _hits(vals, rk, rs, rn)
        v_aud = _hits(vals, ak, as_, an)
        bad += k_resp + k_aud + v_resp + v_aud
        print("  %-18s key in responses %d, in audit %d | its %d synthetic value(s) (%d scanned) in responses %d, "
              "in audit %d" % (f, k_resp, k_aud, len(vals), len(scanned), v_resp, v_aud))
    token_fields = [p for p in prohibited if p not in headers and p != "arbitrary Graph fields"]
    for f in token_fields:
        k_resp = sum(1 for k in rk if k.lower() == f.lower())
        k_aud = sum(1 for k in ak if k.lower() == f.lower())
        bad += k_resp + k_aud
        print("  %-18s key in responses %d, in audit %d" % (f, k_resp, k_aud))
    s_resp = sum(1 for t in secrets for s in rs if t in s)
    s_aud = sum(1 for t in secrets for s in as_ if t in s)
    bad += s_resp + s_aud
    print("  %-18s %d synthetic token/bearer/credential value(s): in responses %d, in audit %d"
          % ("any token (value)", len(secrets), s_resp, s_aud))
    auth_aud = sum(1 for s in as_ if "authorization" in s.lower() or "bearer " in s.lower())
    auth_keys = sum(1 for k in ak if k.lower() == "authorization")
    bad += auth_aud + auth_keys
    print("  %-18s 'Authorization'/'Bearer ' in audit values %d, 'authorization' audit keys %d"
          % ("auth header", auth_aud, auth_keys))
    ok_bodies = [e["body"] for e in route_calls if isinstance(e.get("body"), dict) and e.get("status") == 200]
    err_bodies = [e["body"] for e in route_calls if isinstance(e.get("body"), dict) and e.get("status") != 200]
    odd_success = sum(1 for b in ok_bodies if list(b.keys()) != response_fields)
    rows = [r for b in ok_bodies for r in (b.get("rows") or [])]
    odd_rows = sum(1 for r in rows if list(r.keys()) != row_fields)
    envelope = {"error", "complete", "detail", "observed_extent", "limits", "attempts"}
    odd_err = sum(1 for b in err_bodies if not set(b.keys()) <= envelope or b.get("complete") is not False)
    non_json = sum(1 for e in route_calls if not isinstance(e.get("body"), dict) and e.get("method") != "HEAD")
    bad += odd_success + odd_rows + odd_err + non_json
    print("  %-18s 200 bodies whose keys != capability.response_fields %d of %d; rows whose keys != the 7 projected "
          "+ 3 metadata %d of %d; error bodies outside {%s} or without complete=false %d of %d; non-JSON bodies %d"
          % ("arbitrary Graph fields", odd_success, len(ok_bodies), odd_rows, len(rows), ", ".join(sorted(envelope)),
             odd_err, len(err_bodies), non_json))
    print("prohibited-field occurrences in total: %d (fields enumerated %d of %d contract prohibited_response_fields)"
          % (bad, len(column_fields) + len(token_fields) + 1, len(prohibited)))
    return _verdict(20, bad == 0 and ok_run, "prohibited occurrences %d" % bad)


_RFC3339 = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")


def _module_tuple(repo: Path, name: str) -> tuple:
    tree = ast.parse((repo / GW_REL / MODULE_REL).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return tuple(ast.literal_eval(node.value))
    raise RuntimeError("module constant %s not found" % name)


def _ac21(repo: Path) -> int:
    contract = _contract(repo)
    cap = contract["capability"]
    fields = cap["audit_fields"]
    errors = cap["errors"]
    labels = set(_module_tuple(repo, "CALLER_LABELS"))
    operations = set(_module_tuple(repo, "OPERATIONS"))
    ok_run, summary, rc, entries, egress = _corpus_run(repo)
    print("module run: %s | rc=%d | %s" % (summary, rc, "; ".join(sorted(set(egress))) or "no egress line"))
    calls = [e for e in entries if e.get("kind") == "call"]
    by_header, secrets = _fixture_values(entries)
    if not ok_run or not calls:
        return _verdict(21, False, "corpus not usable (run ok=%s, calls=%d)" % (ok_run, len(calls)))

    def own(lines):
        # The capability's records; another writer's line in the same audit stream carries 'tool' (audit.log_call,
        # e.g. revocation's control alarm) or 'event' (audit.log_credential) and is reported, not counted.
        return [a for a in (lines or []) if "tool" not in a and "event" not in a]

    one_each = sum(1 for e in calls if len(own(e.get("audit"))) == 1)
    records = [a for e in calls for a in own(e.get("audit"))]
    foreign = [a for e in calls for a in (e.get("audit") or []) if "tool" in a or "event" in a]
    print("other writers' lines in the audit stream during those calls: %d (%s)"
          % (len(foreign), ", ".join(sorted({str(a.get("tool") or a.get("event")) for a in foreign})) or "none"))
    exact = sum(1 for a in records if list(a.keys()) == fields)
    domain_bad = []
    for a in records:
        probs = []
        if not (isinstance(a.get("request_id"), str) and re.fullmatch(r"[0-9a-f]{32}", a["request_id"])):
            probs.append("request_id")
        if a.get("caller_capability_label") not in labels:
            probs.append("caller_capability_label")
        ref = a.get("delegated_identity_ref")
        if ref is not None and not (isinstance(ref, dict) and set(ref) == {"principal", "display_email"}
                                    and re.fullmatch(r"[0-9a-f-]{36}/[0-9a-f-]{36}", str(ref.get("principal")))
                                    and (ref.get("display_email") is None or "@" in str(ref.get("display_email")))):
            probs.append("delegated_identity_ref")
        if a.get("operation") not in operations:
            probs.append("operation")
        if a.get("item_id") != contract["workbook"]["item_id"] or a.get("sheet") != contract["workbook"]["sheet"]:
            probs.append("item_id/sheet")
        if a.get("snapshot_id") is not None and not re.fullmatch(r"[0-9a-f]{64}", str(a.get("snapshot_id"))):
            probs.append("snapshot_id")
        if a.get("etag") is not None and not isinstance(a.get("etag"), str):
            probs.append("etag")
        if not (isinstance(a.get("observed_at"), str) and _RFC3339.match(a["observed_at"])):
            probs.append("observed_at")
        if a.get("result") not in set(errors) | {"OK"}:
            probs.append("result")
        if not (isinstance(a.get("latency_ms"), int) and not isinstance(a.get("latency_ms"), bool)
                and a["latency_ms"] >= 0):
            probs.append("latency_ms")
        if probs:
            domain_bad.append(probs)
    ak, as_, an = [], [], []
    for a in records:
        _walk(a, ak, as_, an)
    acct = _hits(by_header.get("Account Number", set()), ak, as_, an)
    acct_n = sum(1 for v in by_header.get("Account Number", set()) if isinstance(v, int) and not isinstance(v, bool)
                 and any(x == v for x in an))
    names = _hits(by_header.get("Name", set()), ak, as_, an)
    row_vals = set().union(*by_header.values()) if by_header else set()
    rows_hit = _hits(row_vals, ak, as_, an)
    row_scanned = sum(1 for v in row_vals if (isinstance(v, str) and len(v.strip()) >= 4) or isinstance(v, float))
    toks = sum(1 for t in secrets for s in as_ if t in s)
    auth = sum(1 for s in as_ if "authorization" in s.lower() or "bearer " in s.lower()) + \
        sum(1 for k in ak if k.lower() == "authorization")
    results = {}
    for a in records:
        results[a.get("result")] = results.get(a.get("result"), 0) + 1
    ops = {}
    for a in records:
        ops[a.get("operation")] = ops.get(a.get("operation"), 0) + 1
    unexercised = [c for c in list(errors) + ["OK"] if c not in results]
    print("calls to /ms/taxsma-workbook across every test case: %d; exactly one audit record %d of %d; records %d"
          % (len(calls), one_each, len(calls), len(records)))
    print("records carrying exactly capability.audit_fields (%d, in order) %d of %d; every field in its declared "
          "domain %d of %d" % (len(fields), exact, len(records), len(records) - len(domain_bad), len(records)))
    print("audit_exclusions: account numbers %d (+%d numeric), account names %d, row values %d (%d of %d distinct "
          "synthetic values long enough to scan; the rest are held by the domain check), tokens %d (%d synthetic), "
          "authorization headers %d" % (acct, acct_n, names, rows_hit, row_scanned, len(row_vals), toks,
                                        len(secrets), auth))
    print("results seen: %s; operations seen: %s; contract outcome classes not exercised: %s"
          % (", ".join("%s %d" % kv for kv in sorted(results.items())),
             ", ".join("%s %d" % kv for kv in sorted(ops.items())), unexercised or "none"))
    ok = (one_each == len(calls) and exact == len(records) and not domain_bad and acct + acct_n + names + rows_hit
          + toks + auth == 0 and not unexercised)
    return _verdict(21, ok, "one-each %d/%d, exact %d/%d, domain faults %d, exclusion hits %d, unexercised %s"
                    % (one_each, len(calls), exact, len(records), len(domain_bad),
                       acct + acct_n + names + rows_hit + toks + auth, unexercised))


# --- AC22: per-module regression ---------------------------------------------------------------------------
def _run_module(gw: Path, name: str, xml_dir: Path) -> dict:
    xml = xml_dir / (name + ".xml")
    if xml.exists():
        xml.unlink()
    cmd = [sys.executable, "-m", "pytest", "tests/" + name, "-q", "-p", "no:cacheprovider", "--color=no",
           "--junitxml=" + str(xml)]
    t0 = time.perf_counter()
    try:
        r = subprocess.run(cmd, cwd=str(gw), capture_output=True, text=True, timeout=MODULE_TIMEOUT, env=_env())
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": MODULE_TIMEOUT, "collection_error": None, "tests": {}, "rc": None,
                "summary": "TIMEOUT"}
    # pytest colours its collection-error tracebacks even under --color=no; strip ANSI before parsing.
    out = _ANSI.sub("", (r.stdout or "") + (r.stderr or ""))
    coll = None
    if "ERROR collecting" in out:
        reasons = re.findall(r"(?m)^E\s+((?:ModuleNotFoundError|ImportError)[^\r\n]*)$", out)
        coll = reasons[0].strip() if reasons else "collection error (reason unparsed)"
    tests, messages = {}, {}
    if xml.exists() and coll is None:
        for tc in ET.parse(str(xml)).iter("testcase"):
            nid = "%s::%s" % (tc.get("classname", ""), tc.get("name", ""))
            bad = tc.find("failure") if tc.find("failure") is not None else tc.find("error")
            if tc.find("failure") is not None:
                tests[nid] = "failed"
            elif tc.find("error") is not None:
                tests[nid] = "error"
            elif tc.find("skipped") is not None:
                tests[nid] = "skipped"
            else:
                tests[nid] = "passed"
            if bad is not None:
                messages[nid] = re.sub(r"\s+", " ", _ANSI.sub("", bad.get("message", "")))[:160]
    lines = [ln for ln in out.splitlines() if ln.strip()]
    return {"status": "RAN", "seconds": round(time.perf_counter() - t0, 1), "collection_error": coll,
            "tests": tests, "messages": messages, "rc": r.returncode, "summary": lines[-1].strip() if lines else ""}


_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def _run_all(repo: Path) -> dict:
    """test_schwab_engine.py runs ALONE first -- its lag bar is load-sensitive (row NFRA_OPLGTW-W3-S12), and run
    beside the other modules it failed one test in this probe's first record -- then the rest three at a time."""
    gw = repo / GW_REL
    xml_dir = repo / ".scratch" / "txg1_ac22_junit"
    xml_dir.mkdir(parents=True, exist_ok=True)
    names = sorted(p.name for p in (gw / "tests").glob("test_*.py"))
    out = {}
    if HEAVY_MODULE in names:
        out[HEAVY_MODULE] = _run_module(gw, HEAVY_MODULE, xml_dir)
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {n: ex.submit(_run_module, gw, n, xml_dir) for n in names if n != HEAVY_MODULE}
        for n, f in futures.items():
            out[n] = f.result()
    return dict(sorted(out.items()))


def _counts(m: dict) -> str:
    if m.get("status") == "TIMEOUT":
        return "TIMEOUT"
    if m.get("collection_error"):
        return "NOT COLLECTED (%s)" % m["collection_error"]
    c = {}
    for o in m["tests"].values():
        c[o] = c.get(o, 0) + 1
    return ", ".join("%s %d" % (k, c[k]) for k in ("passed", "failed", "error", "skipped") if k in c) or "0 tests"


def _record_before(repo: Path) -> int:
    # CONTENT equality, not porcelain status: on this autocrlf box a file rewritten with its HEAD blob's bytes keeps a
    # stale stat entry and reads ' M' while `git diff` is empty (row MDPF_TAXSMA-W1-S2).
    rc, _, _ = _git(repo, "diff", "--quiet", "HEAD", "--", GW_REL)
    rcu, untracked, _ = _git(repo, "ls-files", "--others", "--exclude-standard", "--", GW_REL)
    if rc != 0 or rcu != 0 or untracked.strip():
        print("REFUSED: the Gateway tree is not equal to HEAD (git diff --quiet HEAD rc=%d; untracked %r)"
              % (rc, untracked.strip()))
        return 2
    _, head, _ = _git(repo, "rev-parse", "HEAD")
    t0 = time.perf_counter()
    mods = _run_all(repo)
    rec = {"recorded_at": _utc(), "head": head.strip(), "gateway_tree_equal_to_head": True,
           "python": sys.version.split()[0], "wall_seconds": round(time.perf_counter() - t0, 1), "modules": mods}
    BEFORE_RECORD.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for name, m in mods.items():
        print("  %-28s %s (%ss)" % (name, _counts(m), m.get("seconds")))
    print("recorded %s at HEAD %s, %d module(s), wall %.1fs" % (BEFORE_RECORD.name, head.strip()[:10], len(mods),
                                                               rec["wall_seconds"]))
    return 0


def _route_class_disclosure(repo: Path) -> str:
    code = r'''
import ast, json, sys, types
sys.path.insert(0, ".")
if "msal" not in sys.modules:
    m = types.ModuleType("msal")
    class _R:
        def __init__(self, *a, **k):
            raise RuntimeError("msal stub")
    m.SerializableTokenCache = _R
    m.ConfidentialClientApplication = _R
    sys.modules["msal"] = m
from app.config import get_config
cfg = get_config()
cfg.MOCK_GRAPH = True
import app.server as s
served = sorted(r.path for r in s.app.routes)
tree = ast.parse(open("tests/test_principal_cutover.py", encoding="utf-8").read())
rc = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ROUTE_CLASS" for t in node.targets):
        rc = ast.literal_eval(node.value)
print(json.dumps({"served": served, "route_class": rc}))
'''
    r = subprocess.run([sys.executable, "-c", code], cwd=str(repo / GW_REL), capture_output=True, text=True,
                       timeout=60, env=_env())
    try:
        data = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        return "DISCLOSURE (not graded by AC22): ROUTE_CLASS census UNREAD (rc=%d)" % r.returncode
    served, rcl = set(data["served"]), data["route_class"] or {}
    return ("DISCLOSURE (not graded by AC22): tests/test_principal_cutover.py ROUTE_CLASS names %d of %d routes "
            "app.server serves; missing %s; extra %s; '/ms/taxsma-workbook' -> %r"
            % (len(served & set(rcl)), len(served), sorted(served - set(rcl)) or "none",
               sorted(set(rcl) - served) or "none", rcl.get("/ms/taxsma-workbook")))


def _ac22(repo: Path) -> int:
    if not BEFORE_RECORD.exists():
        return _verdict(22, False, "no BEFORE record at %s" % BEFORE_RECORD.name)
    before = json.loads(BEFORE_RECORD.read_text(encoding="utf-8"))
    print("BEFORE: %s, recorded %s at HEAD %s (Gateway tree equal to HEAD: %s), %d module(s)"
          % (BEFORE_RECORD.name, before["recorded_at"], before["head"][:10], before["gateway_tree_equal_to_head"],
             len(before["modules"])))
    t0 = time.perf_counter()
    after = _run_all(repo)
    print("AFTER: live, %d module(s), wall %.1fs" % (len(after), time.perf_counter() - t0))
    regress, lost, new_bad = [], [], []
    b_pass = a_pass = 0
    for name, b in before["modules"].items():
        a = after.get(name)
        print("  %-28s before: %-40s after: %s" % (name, _counts(b), _counts(a) if a else "ABSENT"))
        if b.get("collection_error") or b.get("status") == "TIMEOUT":
            continue
        if a is None or a.get("collection_error") or a.get("status") == "TIMEOUT":
            lost.append(name)
            continue
        for nid, o in b["tests"].items():
            if o == "passed":
                b_pass += 1
                if a["tests"].get(nid) == "passed":
                    a_pass += 1
                else:
                    regress.append("%s -> %s" % (nid, a["tests"].get(nid, "ABSENT")))
        for nid, o in a["tests"].items():
            if o in ("failed", "error") and b["tests"].get(nid) not in ("failed", "error"):
                new_bad.append("%s %s" % (nid, o))
    added = [n for n in after if n not in before["modules"]]
    for n in added:
        print("  %-28s before: %-40s after: %s" % (n, "(new module)", _counts(after[n])))
    not_eval = sorted(n for n, b in before["modules"].items() if b.get("collection_error"))
    pre_bad = []
    for name, b in before["modules"].items():
        for nid, o in b.get("tests", {}).items():
            if o in ("failed", "error"):
                a_o = ((after.get(name) or {}).get("tests") or {}).get(nid, "ABSENT")
                pre_bad.append("%s %s before (%s), %s after" % (nid.split("::")[-1], o,
                                                                b.get("messages", {}).get(nid, ""), a_o))
    pre_bad.sort()
    collected_b = [n for n, b in before["modules"].items() if not b.get("collection_error")]
    print("modules that collected before: %d of %d; still collect after: %d of %d"
          % (len(collected_b), len(before["modules"]), len(collected_b) - len(lost), len(collected_b)))
    print("tests that passed before: %d; still pass after: %d of %d; newly failing or erroring after: %d"
          % (b_pass, a_pass, b_pass, len(new_bad)))
    print("NOT-EVALUATED on this box (collection error before, moto absent): %d -- %s" % (len(not_eval),
                                                                                       ", ".join(not_eval)))
    print("failing or erroring BEFORE the edit (not graded, after shown above): %s" % ("; ".join(pre_bad) or "none"))
    print(_route_class_disclosure(repo))
    ok = (not regress and not lost and not new_bad and before["head"].startswith(CUT_BASE)
          and before["gateway_tree_equal_to_head"])
    return _verdict(22, ok, "regressed %d, lost %d, new failures %d%s" % (
        len(regress), len(lost), len(new_bad), (" (" + "; ".join((regress + lost + new_bad)[:5]) + ")")
        if (regress or lost or new_bad) else ""))


# --- AC23: no new dependency ---------------------------------------------------------------------------------
def _imports(src: str) -> set:
    names = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.add(node.module.split(".")[0])
    return names


def _ac23(repo: Path) -> int:
    gw = repo / GW_REL
    test_src = (gw / TEST_REL).read_text(encoding="utf-8")
    mod_src = (gw / MODULE_REL).read_text(encoding="utf-8")
    mine = _imports(test_src) | _imports(mod_src)
    stdlib = set(sys.stdlib_module_names)
    third = sorted(m for m in mine if m not in stdlib and m != "app")
    rc, ls, _ = _git(repo, "ls-tree", "-r", "--name-only", CUT_BASE, "--", GW_REL + "/app", GW_REL + "/tests")
    base_py = [p for p in ls.splitlines() if p.endswith(".py")]
    base_imports, empty_blobs = set(), 0
    for p in base_py:
        rc2, src, err = _git(repo, "show", "%s:%s" % (CUT_BASE, p))
        if rc2 != 0:   # a FAILED read is a FAIL; an EMPTY blob is a real read (app/__init__.py is 0 bytes at the base)
            return _verdict(23, False, "git show %s:%s failed (rc=%d %s)" % (CUT_BASE, p, rc2, err.strip()))
        empty_blobs += 0 if src.strip() else 1
        try:
            base_imports |= _imports(src)
        except SyntaxError:
            continue
    if not base_py or empty_blobs == len(base_py) or "starlette" not in base_imports:
        return _verdict(23, False, "the base import census read nothing usable (%d files, %d empty; positive "
                        "control 'starlette' present: %s)" % (len(base_py), empty_blobs, "starlette" in base_imports))
    print("base import census: %d .py files read at %s, %d empty blob(s); positive control: 'starlette' imported by "
          "the base Gateway (app/server.py)" % (len(base_py), CUT_BASE, empty_blobs))
    rc3, reqs, _ = _git(repo, "show", "%s:%s/requirements.txt" % (CUT_BASE, GW_REL))
    req_names = sorted({re.split(r"[=<>\[;#\s]", ln.strip(), maxsplit=1)[0].lower() for ln in reqs.splitlines()
                        if ln.strip() and not ln.strip().startswith("#")})
    new = [m for m in third if m not in base_imports]
    rcd, _, _ = _git(repo, "diff", "--quiet", CUT_BASE, "--", GW_REL + "/requirements.txt")
    _, st, _ = _git(repo, "status", "--porcelain", "--", GW_REL + "/requirements.txt")
    forbidden = sorted(m for m in mine if m in ("moto", "msal"))
    stubs = {"token_broker.get_token": 0, "graph.call": 0}
    for node in ast.walk(ast.parse(test_src)):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "setattr"
                and len(node.args) >= 2 and isinstance(node.args[0], ast.Name)
                and isinstance(node.args[1], ast.Constant)):
            key = "%s.%s" % (node.args[0].id, node.args[1].value)
            if key in stubs:
                stubs[key] += 1
    print("imports: test module %d, capability module %d (top-level names); third-party %s; the Gateway's own import "
          "set at %s: %d names over %d .py files; requirements.txt at %s names %d: %s"
          % (len(_imports(test_src)), len(_imports(mod_src)), third or "none", CUT_BASE, len(base_imports),
             len(base_py), CUT_BASE, len(req_names), ", ".join(req_names)))
    print("third-party names new to the Gateway: %s; moto/msal imported by the new files: %s; requirements.txt "
          "unchanged vs %s: %s (diff rc=%d, worktree status %r)"
          % (new or "none", forbidden or "none", CUT_BASE, rcd == 0 and not st.strip(), rcd, st.strip()))
    print("stubs in the test module: monkeypatch.setattr(token_broker, 'get_token', ...) x%d, "
          "monkeypatch.setattr(graph, 'call', ...) x%d" % (stubs["token_broker.get_token"], stubs["graph.call"]))
    code = r'''
import importlib.abc, sys
class _Block(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in ("moto", "msal"):
            raise ModuleNotFoundError("refused by the TX-g-1 probe: %s" % name, name=name)
        return None
sys.meta_path.insert(0, _Block())
import pytest
sys.exit(pytest.main(["tests/test_taxsma_workbook.py", "-q", "-p", "no:cacheprovider", "--color=no"]))
'''
    r = subprocess.run([sys.executable, "-c", code], cwd=str(gw), capture_output=True, text=True,
                       timeout=PER_TEST_TIMEOUT, env=_env())
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(?m)^(\d+) passed(.*)$", out)
    blocked_ok = r.returncode == 0 and m is not None and "failed" not in m.group(2) and "error" not in m.group(2)
    print("module re-run with 'moto' and 'msal' imports refused by a meta-path finder: %s | rc=%d"
          % (m.group(0) if m else "NO SUMMARY LINE", r.returncode))
    ok = (not new and not forbidden and rcd == 0 and not st.strip() and all(v >= 1 for v in stubs.values())
          and blocked_ok)
    return _verdict(23, ok, "new=%s forbidden=%s reqs_changed=%s stubs=%s blocked_run_ok=%s"
                    % (new, forbidden, not (rcd == 0 and not st.strip()), stubs, blocked_ok))


def main(argv: list) -> int:
    if not argv or not re.fullmatch(r"AC([1-9]|1[0-9]|2[0-3])", argv[0]):
        print("usage: tx_g_1.py AC<1..23> [--record-before (AC22 only)]", file=sys.stderr)
        return 2
    n = int(argv[0][2:])
    try:
        repo = _repo()
        if n == 22 and "--record-before" in argv[1:]:
            return _record_before(repo)
        print("TXG1-AC%d probe; %s" % (n, _vintage(repo)))
        if n <= 19:
            return _single_test(repo, n)
        return {20: _ac20, 21: _ac21, 22: _ac22, 23: _ac23}[n](repo)
    except Exception as exc:  # noqa: BLE001 -- an instrument failure is a FAIL, never a zero
        return _verdict(n, False, "probe error %s: %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
