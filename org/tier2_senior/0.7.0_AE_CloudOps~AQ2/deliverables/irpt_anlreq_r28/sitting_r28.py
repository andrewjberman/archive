"""IRPT_ANLREQ TO-EXERCISE-R28 executor (0.7.0_AE_CloudOps~AQ2): the release-28 synthetic sitting.

  --offline   the decision logic against the code with fakes: the real ticket handler (the repo's own test harness and a
              fake table), the real template reader, the real default-price-date function, and the portal's own
              parseIrEnvelope loaded from origin/PROD. NO token, NO key, NO AWS call, NO network request.
  --live --go the sitting. Tokens are minted in this process and never written, printed or logged.

Both modes run the SAME arm checks (ticket_arms) over an environment object, so what the offline run predicts is what
the live run grades. No response body is kept: status codes, refusal codes and sha256 values only.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
REGION = "us-east-1"
BASE = "https://d2n2nzpeqf34ge.cloudfront.net"
USERS, PARTNER, TICKETS = "opal-users-v2", "opal-partner-49financial", "opal-tickets"
TICKET_LOG = "/aws/lambda/opal-ticket-api"
KEY_SECRET = "opal/auth/jwt-private-key"
PK_SUB = "svc-irpt-packager"
LIFE = 1140          # seconds; the order caps a token at 20 minutes after iat
GAP = 16             # seconds between request starts; the order asks for at least 15
TITLE = "SYNTHETIC release-28 sitting, do not action"
DOOR = "/api/scoped/investor-reporting/analysis/inputs?selected_tenant=49financial"
PROJECTION_TOP = {"ticket_id", "title", "status", "created_at", "ticket_type", "answers", "package_state"}
PROJECTION_ANSWERS = {"report_type", "household"}
TICKET_ID = re.compile(r"^TCK-\d{8}-[0-9a-f]{8}$")
SUBMIT_VIEW = {"ticket_id", "status", "ticket_type", "title", "created_at"}
READER_R193_SHA = "a61cd0c622f8dd54864b8f2415cbe9968c0287d28087ce703073c7e392c1fc35"


def iso(t=None):
    t = time.time() if t is None else t
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jdump(x):
    return json.dumps(x, sort_keys=True, default=str, separators=(",", ":"))


def sha(x):
    return hashlib.sha256(jdump(x).encode("utf-8")).hexdigest()


def i7(tag):
    return json.dumps({"artifact_id": "ART-r28-" + tag, "sha256": hashlib.sha256(tag.encode()).hexdigest(),
                       "version_id": "v1"}, sort_keys=True, separators=(",", ":"))


REQ1 = "REQ-" + hashlib.sha256(b"irpt-r28-req-1").hexdigest()[:24]
REQ2 = "REQ-" + hashlib.sha256(b"irpt-r28-req-2").hexdigest()[:24]


class Ids:
    def __init__(self, date):
        self.date = date
        self.fa = "success+irpt-r28-fa-%s@simulator.amazonses.com" % date
        self.cw = "irpt-r28-cw-%s@opal.invalid" % date
        self.advisor_key = "irpt-r28-fa-" + date
        self.name = "IRPT_ANLREQ R28 synthetic sitting"


def submit_body(firm):
    return {"ticket_type": "analysis_request", "title": TITLE,
            "answers": {"advisor": "IRPT_ANLREQ R28 synthetic advisor", "firm": firm,
                        "household": "SYNTHETIC household R28", "report_type": "Overview"},
            "attachment": {"upload_id": "UP-" + hashlib.sha256(b"irpt-r28-synthetic-upload").hexdigest(),
                           "input_id": "portfolio_" + hashlib.sha256(b"irpt-r28-synthetic-input").hexdigest()}}


def package_body(request_id, **extra):
    body = {"report_ref": "synthetic/r28/report.json", "pdf_ref": i7("pdf"), "original_ref": "synthetic/r28/original.csv",
            "commentary_ref": i7("commentary"), "firm": "49financial", "request_id": request_id, "request_revision": 1}
    body.update(extra)
    return body


# The three door files: synthetic, no client data. Real, resolvable tickers so the resident's provider read can answer.
D_FILES = {
    "D1": b"Ticker,Dollars,Accnt\nSPY,100,AB12CD\nAGG,200,XY9981\n",
    "D2": b"Ticker,Dollars,Acct Market Value\nSPY,100,25000000\nAGG,200,31000000\n",
    "D3": b"Ticker,Shares\nSPY,10\nAGG,5\n",
}


def door_body(label, date):
    return {"upload_token": "irpt-r28-%s-%s" % (label.lower(), date), "filename": "r28-%s.csv" % label.lower(),
            "file_base64": base64.b64encode(D_FILES[label]).decode(), "file_type": "csv"}


def parsed(raw):
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------------------------------------ the arms
def ticket_arms(env, opts, out):
    """T4a .. PKG-3 in the order of the table. out[arm] = (ok, line, detail). An admitting refusal arm stops the run."""
    state = {"tid": None, "stop": None}

    def note(arm, ok, line, detail):
        out[arm] = (ok, line, detail)
        env.say("%s %s %s" % (arm, "ok" if ok else "FAIL", detail))

    # a. T4a
    st, b, raw = env.call("FA", "POST", "/api/scoped/tickets/submit", submit_body("49financial"), arm="T4a")
    t = b.get("ticket") if isinstance(b, dict) else None
    ok = (st == 201 and isinstance(t, dict) and set(t) == SUBMIT_VIEW and TICKET_ID.match(str(t.get("ticket_id")))
          and "answers" not in raw and "attachment" not in raw)
    note("T4a", ok, "T4a ADMITTED status=201" if ok else "T4a FAIL status=%s" % st, "status=%s body_sha=%s" % (st, hashlib.sha256(raw.encode()).hexdigest()[:16]))
    if not ok:
        return state
    tid = state["tid"] = t["ticket_id"]
    # b. T4b
    before = env.count()
    st, b, raw = env.call("FA", "POST", "/api/scoped/tickets/submit", submit_body("cottonwood"), arm="T4b")
    after = env.count()
    ok = st == 400 and "answers.firm" in str((b or {}).get("error", "")) and before == after
    note("T4b", ok, "T4b REFUSED status=400" if ok else "T4b FAIL status=%s" % st, "status=%s count %s->%s" % (st, before, after))
    if st in (200, 201):
        state["stop"] = "T4b admitted"
        return state
    # c. LIST-A
    st, b, raw = env.call("FA", "GET", "/api/scoped/tickets", None, arm="LIST-A")
    rows = (b or {}).get("tickets") if isinstance(b, dict) else None
    ok, own, foreign, eight = False, 0, 0, False
    if st == 200 and isinstance(rows, list):
        eight = all(isinstance(r, dict) and set(r) == PROJECTION_TOP and isinstance(r.get("answers"), dict)
                    and set(r["answers"]) == PROJECTION_ANSWERS for r in rows)
        items = {r.get("ticket_id"): env.item(r.get("ticket_id")) for r in rows if isinstance(r, dict)}
        for r in rows:
            it = items.get(r.get("ticket_id")) or {}
            good = (r.get("ticket_type") == "analysis_request" and (it.get("requester") or {}).get("firm") == "49financial")
            own += 1 if good else 0
            foreign += 0 if good else 1
        pointers = [v for it in items.values() for v in ((it or {}).get("package") or {}).values()
                    if isinstance(v, str) and len(v) > 12]
        leaked = [p for p in pointers if p in raw]
        mine = [r for r in rows if r.get("ticket_id") == tid]
        ok = (eight and foreign == 0 and len(mine) == 1 and mine[0].get("package_state") == "NONE" and not leaked
              and (b or {}).get("count") == len(rows))
    ids_a = {r.get("ticket_id") for r in rows} if isinstance(rows, list) else set()
    note("LIST-A", ok, ("LIST-A OK own_rows=%d eight_members=true foreign=0" % own) if ok else "LIST-A FAIL status=%s" % st,
         "status=%s rows=%s eight=%s foreign=%s" % (st, len(rows) if isinstance(rows, list) else None, eight, foreign))
    # d. LIST-B
    st, b, raw = env.call("CW", "GET", "/api/scoped/tickets", None, arm="LIST-B")
    rows_b = (b or {}).get("tickets") if isinstance(b, dict) else None
    ids_b = {r.get("ticket_id") for r in rows_b} if isinstance(rows_b, list) else set()
    foreign_b = len(ids_b & ids_a)
    ok = st == 200 and isinstance(rows_b, list) and foreign_b == 0
    note("LIST-B", ok, "LIST-B OK foreign=0" if ok else "LIST-B FAIL status=%s foreign=%s" % (st, foreign_b),
         "status=%s rows=%s foreign=%s" % (st, len(ids_b), foreign_b))
    if st == 200 and foreign_b:
        state["stop"] = "LIST-B admitted"
        return state
    # e. GET-B
    st, b, raw = env.call("CW", "GET", "/api/scoped/tickets/" + tid, None, arm="GET-B")
    ok = st == 403 and isinstance(b, dict) and "ticket" not in b and tid not in raw and TITLE not in raw
    note("GET-B", ok, "GET-B REFUSED status=403" if ok else "GET-B FAIL status=%s" % st, "status=%s" % st)
    if st == 200:
        state["stop"] = "GET-B admitted"
        return state
    # f. PKG-1
    st, b, raw = env.call("PK", "POST", "/api/scoped/tickets/%s/package" % tid, package_body(REQ1), arm="PKG-1")
    it = env.item(tid) or {}
    ref = it.get("report_ref") or {}
    ok = (st == 200 and set(ref) == {"request_id", "revision", "recorded_by", "recorded_at"} and ref.get("request_id") == REQ1
          and int(ref.get("revision", -1)) == 1 and ref.get("recorded_by") == PK_SUB and isinstance(ref.get("recorded_at"), str))
    note("PKG-1", ok, "PKG-1 OK report_ref_set" if ok else "PKG-1 FAIL status=%s" % st, "status=%s" % st)
    if not ok:
        return state
    sha1 = env.item_hash(tid)
    attached = (it.get("package") or {}).get("attached_at")
    # g. PKG-2 (the same PACKAGE again)
    st, b, raw = env.call("PK", "POST", "/api/scoped/tickets/%s/package" % tid, package_body(REQ1), arm="PKG-2")
    code = (b or {}).get("code") if isinstance(b, dict) else None
    unchanged = env.item_hash(tid) == sha1
    ok = unchanged and st == 409 and code == "PACKAGE_ALREADY_ATTACHED"
    note("PKG-2", ok, "PKG-2 OK unchanged status=409 code=PACKAGE_ALREADY_ATTACHED" if ok else "PKG-2 FAIL status=%s code=%s" % (st, code),
         "status=%s code=%s item_unchanged=%s" % (st, code, unchanged))
    # h. PKG-3 (a different request id)
    extra = {"prior_attached_at": attached} if opts.get("pkg3_prior", True) else {}
    st, b, raw = env.call("PK", "POST", "/api/scoped/tickets/%s/package" % tid, package_body(REQ2, **extra), arm="PKG-3")
    code = (b or {}).get("code") if isinstance(b, dict) else None
    unchanged = env.item_hash(tid) == sha1
    ok = st == 409 and code == "REPORT_REF_ALREADY_RECORDED_OTHER" and unchanged
    note("PKG-3", ok, ("PKG-3 REFUSED status=409 code=REPORT_REF_ALREADY_RECORDED_OTHER") if ok else "PKG-3 FAIL status=%s code=%s" % (st, code),
         "status=%s code=%s item_unchanged=%s prior_sent=%s" % (st, code, unchanged, bool(extra)))
    if st == 200:
        state["stop"] = "PKG-3 admitted"
    return state


def d_codes(data):
    return {f.get("code") for f in (data.get("findings") or []) if isinstance(f, dict)}


def door_arms(env, date, out, expected_prices):
    """D1 .. D4 through the upload door as FA; returns the final raw bodies of D1..D3 for C1."""
    bodies = {}

    def post(label):
        st, b, raw = env.call("FA", "POST", DOOR, door_body(label, date), arm=label)
        return st, (b or {}).get("data") if isinstance(b, dict) else None, b, raw

    def resolve(label):
        for _ in range(8):
            st, data, b, raw = post(label)
            if not (isinstance(data, dict) and data.get("state") == "RESOLVING"):
                return st, data, b, raw
        return st, data, b, raw

    st, data, b, raw = post("D1")
    ok = st == 200 and isinstance(data, dict) and data.get("state") == "NEEDS_CORRECTION" and "ACCOUNT_COLUMN_SEVERAL_VALUES" in d_codes(data)
    out["D1"] = (ok, "D1 NEEDS_CORRECTION ACCOUNT_COLUMN_SEVERAL_VALUES" if ok else "D1 FAIL status=%s" % st,
                 "status=%s state=%s" % (st, (data or {}).get("state") if isinstance(data, dict) else None))
    bodies["D1"] = raw
    st, data, b, raw = resolve("D2")
    ok = st == 200 and isinstance(data, dict) and data.get("state") == "NORMALIZED" and isinstance(data.get("input_id"), str)
    out["D2"] = (ok, "D2 NORMALIZED" if ok else "D2 FAIL status=%s state=%s" % (st, (data or {}).get("state") if isinstance(data, dict) else None),
                 "status=%s" % st)
    bodies["D2"] = raw
    d2_input = data.get("input_id") if isinstance(data, dict) else None
    st, data, b, raw = resolve("D3")
    pdate = (((data or {}).get("portfolio") or {}).get("options") or {}).get("price_date") if isinstance(data, dict) else None
    ok = st == 200 and isinstance(data, dict) and data.get("state") == "NORMALIZED" and pdate in expected_prices()
    out["D3"] = (ok, ("D3 NORMALIZED price_date=%s" % pdate) if ok else "D3 FAIL status=%s state=%s price_date=%s" % (
        st, (data or {}).get("state") if isinstance(data, dict) else None, pdate), "status=%s price_date=%s expected=%s" % (st, pdate, sorted(expected_prices())))
    bodies["D3"] = raw
    st, data, b, raw = post("D2")
    ok = (st == 200 and isinstance(data, dict) and data.get("state") == "NORMALIZED" and d2_input is not None
          and data.get("input_id") == d2_input)
    out["D4"] = (ok, "D4 ACCEPTED" if ok else "D4 FAIL status=%s" % st, "status=%s same_input=%s" % (st, ok))
    return bodies


# ------------------------------------------------------------------------------------------------ C1 (bun)
def find_bun():
    return shutil.which("bun") or next(iter(Path.home().glob("AppData/Local/Microsoft/WinGet/Packages/Oven-sh.Bun*/bun-windows-x64/bun.exe")), None)


C1_TS = """import { parseIrEnvelope } from './contracts/envelope'
import { readFileSync } from 'node:fs'
const file = process.argv[2]
const body = JSON.parse(readFileSync(file, 'utf8'))
try {
  parseIrEnvelope(String(body.operation), body)
  console.log('PARSED')
} catch (e) {
  console.log('THREW ' + (e && e.name ? e.name : 'Error') + ' ' + String(e && e.message ? e.message : '').slice(0, 120))
}
"""


def c1_prepare(scratch):
    """Extract envelope.ts and its transitive relative imports from the portal at origin/PROD into scratch (git show per file).
    Returns (commit, folder holding c1.ts). A package import or an unresolved import is a refusal, not a guess."""
    import posixpath
    portal = ["git", "-C", str(REPO / "portal")]
    commit = subprocess.run(portal + ["rev-parse", "origin/PROD"], capture_output=True, text=True).stdout.strip()
    pattern = re.compile(r"(?:^|\n)\s*(?:import|export)\s+(?:type\s+)?(?:[^'\"]*?\s+from\s+)?['\"]([^'\"]+)['\"]")

    def show(path):
        r = subprocess.run(portal + ["show", "origin/PROD:" + path], capture_output=True)
        return r.stdout if r.returncode == 0 else None
    seen, queue = {}, ["src/pages/InvestorReporting/contracts/envelope.ts"]
    while queue:
        path = queue.pop()
        if path in seen:
            continue
        data = show(path)
        if data is None:
            continue
        seen[path] = data
        for spec in pattern.findall(data.decode("utf-8", "replace")):
            if not spec.startswith("."):
                raise RuntimeError("a package import in the closure: " + spec)
            base = posixpath.normpath(posixpath.join(posixpath.dirname(path), spec))
            for cand in (base + ".ts", base + ".tsx", base + "/index.ts", base + "/index.tsx"):
                if cand in seen or show(cand) is not None:
                    queue.append(cand)
                    break
            else:
                raise RuntimeError("an unresolved import in the closure: %s from %s" % (spec, path))
    for path, data in seen.items():
        dest = Path(scratch) / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    root = Path(scratch) / "src" / "pages" / "InvestorReporting"
    (root / "c1.ts").write_text(C1_TS, encoding="utf-8")
    return commit, root


def c1_parse(bun, root, body_text):
    """Write the body to a file, parse it, delete the file at once. -> 'PARSED' or 'THREW <name>'."""
    fd, name = tempfile.mkstemp(suffix=".json", dir=str(root))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(body_text)
        r = subprocess.run([str(bun), "run", "c1.ts", name], cwd=str(root), capture_output=True, text=True, timeout=120)
        got = r.stdout.strip().splitlines()
        if got:
            return got[-1]
        return "NO-OUTPUT rc=%s %s" % (r.returncode, (r.stderr.strip().splitlines() or [""])[0][:200])
    finally:
        try:
            os.remove(name)
        except OSError:
            pass


def envelope(operation, data):
    return json.dumps({"contract_version": "v1", "operation": operation, "firm_id": "opaque-firm", "data": data,
                       "unprojected_grant": {"count": 0, "denominator": 0, "kinds": {}}})


def synthetic_upload_fixtures():
    up = "UP-" + "a" * 64
    content = "b" * 64
    art = {"artifact_id": "ART-" + "c" * 64, "family": "NORMALIZED_PORTFOLIO", "sha256": content, "immutable": True,
           "content_type": "application/json", "version_id": "v1", "byte_length": 10}
    return {
        "NEEDS_CORRECTION": {"upload_id": up, "input_id": None, "state": "NEEDS_CORRECTION", "reason": "TEMPLATE_FINDINGS", "findings": []},
        "RESOLVING": {"upload_id": up, "input_id": None, "state": "RESOLVING"},
        "NORMALIZED": {"upload_id": up, "input_id": "portfolio_" + content, "state": "NORMALIZED",
                       "input_ref": {"input_id": "portfolio_" + content, "content_sha256": content, "artifact_ref": art},
                       "portfolio": {"source": {"upload_id": up}}},
    }


# ------------------------------------------------------------------------------------------------ offline
def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def expected_price_dates():
    sys.path.insert(0, str(REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "intake"))
    sys.path.insert(0, str(REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "_authz"))
    sys.path.insert(0, str(REPO / "lib"))
    import portfolio
    return portfolio.default_price_date


class OfflineEnv:
    def __init__(self, ids):
        self.ids = ids
        tests = REPO / "infra" / "aws" / "lambda" / "ticket_center" / "tests"
        self.PRI = load_module("pri_harness", tests / "test_package_request_id.py")
        self.H = self.PRI.H
        self.mod = self.PRI.mod
        self.table = self.PRI.fresh()
        self.sends = []
        self.mod.notify_dl_isolated = lambda item: self.sends.append(("DL", item["ticket_id"]))
        self.mod.notify_client_isolated = lambda item, kind: self.sends.append((kind, item["requester"]["email"]))
        self.mod.PACKAGE_ALLOWED_FIRMS = frozenset({"49financial", "cottonwood", "inflection"})
        self.ctx = {
            "FA": {"email": ids.fa, "name": ids.name, "firmId": "49financial", "userType": "test-filer", "allowedFirmIds": "49financial"},
            "CW": {"email": ids.cw, "name": ids.name, "firmId": "cottonwood", "userType": "test-filer", "allowedFirmIds": "cottonwood"},
            "PK": {"email": PK_SUB, "name": PK_SUB, "firmId": "null", "userType": "service", "allowedFirmIds": ""},
        }
        self.lines = []
        self.mark = 0
        # seeds: the live table holds other firms' and other types' tickets; the scope must hide them
        seed = [("49financial", "analysis_request"), ("cottonwood", "analysis_request"), ("49financial", "other")]
        for firm, ttype in seed:
            ctx = {"email": "seed-%s@example.test" % firm, "name": "Seed", "firmId": firm, "userType": "User", "allowedFirmIds": firm}
            body = submit_body(firm) if ttype == "analysis_request" else {"ticket_type": ttype, "title": "seed " + ttype}
            self.H.call("POST", "/api/scoped/tickets/submit", ctx, body)
        self.sends.clear()

    def say(self, msg):
        self.lines.append(msg)

    def call(self, who, method, path, body=None, arm=""):
        self.mark = len(self.sends)
        code, b = self.H.call(method, path.split("?")[0], self.ctx[who], body)
        return code, b, json.dumps(b)

    def item(self, tid):
        it = self.table.items.get(tid)
        return json.loads(json.dumps(it)) if it else None

    def item_hash(self, tid):
        return sha(self.table.items.get(tid))

    def count(self):
        return len(self.table.items)


def offline(ids, args):
    res = []
    out = {}
    for variant in (False, True):
        env2 = OfflineEnv(ids)
        out2 = {}
        sends_by_arm = {}
        orig_call = env2.call

        def tracked(who, method, path, body=None, arm="", _o=orig_call, _e=env2, _s=sends_by_arm):
            n0 = len(_e.sends)
            r = _o(who, method, path, body, arm)
            _s[arm] = list(_e.sends[n0:])
            return r
        env2.call = tracked
        ticket_arms(env2, {"pkg3_prior": variant}, out2)
        label = "PKG-3 sends prior_attached_at" if variant else "PKG-3 literal (no prior_attached_at)"
        res.append("== ticket arms, %s" % label)
        for arm in ("T4a", "T4b", "LIST-A", "LIST-B", "GET-B", "PKG-1", "PKG-2", "PKG-3"):
            if arm in out2:
                ok, line, detail = out2[arm]
                res.append("  %-7s %-4s %s | %s" % (arm, "ok" if ok else "FAIL", line, detail))
            else:
                res.append("  %-7s NOT RUN" % arm)
        res.append("  would-be sends by arm: %s" % json.dumps({k: [(a, "FA-simulator-address" if b == ids.fa else b) for a, b in v] for k, v in sends_by_arm.items() if v}))
        if not variant:
            out.update(out2)
    # PKG-2 as a replace (prior_attached_at sent): shows what the replace path does to the item
    env3 = OfflineEnv(ids)
    t = env3.call("FA", "POST", "/api/scoped/tickets/submit", submit_body("49financial"))[1]["ticket"]["ticket_id"]
    env3.call("PK", "POST", "/api/scoped/tickets/%s/package" % t, package_body(REQ1))
    h1 = env3.item_hash(t)
    att = env3.item(t)["package"]["attached_at"]
    st, b, _ = env3.call("PK", "POST", "/api/scoped/tickets/%s/package" % t, package_body(REQ1, prior_attached_at=att))
    res.append("== PKG-2 as a replace (same body + prior_attached_at): status=%s item_unchanged=%s (the replace path rewrites the package and appends an event)" % (st, env3.item_hash(t) == h1))
    # the door files through the real reader
    sys.path.insert(0, str(REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "intake"))
    reader_path = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "intake" / "template_reader.py"
    reader_sha = hashlib.sha256(reader_path.read_bytes()).hexdigest()
    res.append("== door files through the real template reader (sha256 equals r19.3 %s: %s)" % (READER_R193_SHA[:12], reader_sha == READER_R193_SHA))
    reader = load_module("template_reader_r28", reader_path)
    for label, data in D_FILES.items():
        r = reader.read_template(data, "csv")
        errors = sorted({f["code"] for f in r["findings"] if f.get("severity") == "ERROR"})
        res.append("  %s basis=%s ERROR codes=%s all codes=%s" % (label, r["basis"], errors, sorted({f["code"] for f in r["findings"]})))
    day = expected_price_dates()(None)
    res.append("== default price date now (New York prior trading day, the door's own function): %s" % day)
    # C1 toolchain with fixtures
    bun = find_bun()
    scratch = tempfile.mkdtemp(prefix="r28_c1_")
    try:
        commit, root = c1_prepare(scratch)
        res.append("== C1 toolchain: portal origin/PROD %s, bun %s" % (commit[:10], "found" if bun else "NOT FOUND"))
        if bun:
            fx = synthetic_upload_fixtures()
            for name, data in fx.items():
                res.append("  fixture %-17s -> %s" % (name, c1_parse(bun, root, envelope("analysis-input-upload", data))))
            res.append("  negative control (wrong contract_version) -> %s" % c1_parse(bun, root, json.dumps({"contract_version": "v0", "operation": "analysis-input-upload", "firm_id": "x", "data": {}})))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return res, out


# ------------------------------------------------------------------------------------------------ live
def live(ids, args):
    import boto3
    import jwt as pyjwt
    from boto3.dynamodb.types import TypeDeserializer

    ddb = boto3.client("dynamodb", region_name=REGION)
    logs = boto3.client("logs", region_name=REGION)
    deser = TypeDeserializer()
    outdir = Path(args.out)
    lines, results, starts, tokens, exps = [], {}, [], {}, []
    written = []

    def say(msg):
        line = "%s %s" % (iso(), msg)
        print(line, flush=True)
        lines.append(line)

    def ukey(addr):
        return {"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}}

    def cread(addr):
        return ddb.get_item(TableName=USERS, Key=ukey(addr), ConsistentRead=True).get("Item")

    def gsi(addr):
        return ddb.query(TableName=USERS, IndexName="email-index", KeyConditionExpression="email = :e",
                         ExpressionAttributeValues={":e": {"S": addr}}, Select="COUNT")["Count"]

    class Live:
        last = 0.0

        def say(self, msg):
            say(msg)

        def call(self, who, method, path, body=None, arm=""):
            wait = GAP - (time.time() - Live.last)
            if wait > 0:
                time.sleep(wait)
            data = json.dumps(body).encode("utf-8") if body is not None else None
            req = urllib.request.Request(BASE + path, data=data, method=method)
            req.add_header("Authorization", "Bearer " + tokens[who])
            req.add_header("x-contract-version", "v1")
            if data is not None:
                req.add_header("Content-Type", "application/json")
            start = Live.last = time.time()
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    st, raw = r.status, r.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as e:
                st, raw = e.code, e.read().decode("utf-8", "replace")
            starts.append((arm, start))
            say("request %s %s start=%s status=%s body_sha256=%s" % (arm, who, iso(start), st, hashlib.sha256(raw.encode()).hexdigest()))
            return st, parsed(raw), raw

        def item(self, tid):
            it = ddb.get_item(TableName=TICKETS, Key={"ticket_id": {"S": tid}}, ConsistentRead=True).get("Item")
            return {k: deser.deserialize(v) for k, v in it.items()} if it else None

        def item_hash(self, tid):
            return sha(self.item(tid))

        def count(self):
            total, start = 0, None
            while True:
                kw = {"TableName": TICKETS, "Select": "COUNT", "ConsistentRead": True}
                if start:
                    kw["ExclusiveStartKey"] = start
                r = ddb.scan(**kw)
                total += r["Count"]
                start = r.get("LastEvaluatedKey")
                if not start:
                    return total

    env = Live()
    stop = None
    try:
        lam = boto3.client("lambda", region_name=REGION)
        for fn, want in (("irpt-status", "MIVrDbv+/w8ioVB24xS97gnETVbNRCroDiY+Ne5osbA="), ("opal-ticket-api", "C/Rt/FnSqOj7SnZC1GeoEilj8jbCKdvAUHnxYrnNZNM="),
                         ("irpt-ycharts-generate", "reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc=")):
            got = lam.get_function_configuration(FunctionName=fn)["CodeSha256"]
            say("%s CodeSha256 %s" % (fn, "EQUAL" if got == want else "DIFFERENT"))
            if got != want:
                raise RuntimeError("a leg is not at its expected CodeSha256")
        for addr in (ids.fa, ids.cw):
            if cread(addr) is not None or gsi(addr) != 0:
                raise RuntimeError("an address is not ABSENT before the sitting")
        if ddb.get_item(TableName=PARTNER, Key={"email": {"S": ids.fa}}, ConsistentRead=True).get("Item"):
            raise RuntimeError("FA partner row is not ABSENT before the sitting")
        say("pre-state: FA and CW keys ABSENT by ConsistentRead, email index returns 0, FA partner row ABSENT")
        now = iso()
        for who, addr, firm in (("FA", ids.fa, "49financial"), ("CW", ids.cw, "cottonwood")):
            item = {"PK": {"S": "USER#" + addr}, "SK": {"S": "PROFILE"}, "email": {"S": addr}, "firmId": {"S": firm}, "status": {"S": "active"},
                    "name": {"S": ids.name}, "role": {"S": "user"}, "tier": {"S": "advisor"}, "userType": {"S": "test-filer"},
                    "allowedFirmIds": {"L": [{"S": firm}]}, "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}}
            ddb.put_item(TableName=USERS, Item=item, ConditionExpression="attribute_not_exists(PK)")
            written.append(("users", addr))
            back = cread(addr)
            if back is None or back["status"]["S"] != "active" or [x["S"] for x in back["allowedFirmIds"]["L"]] != [firm]:
                raise RuntimeError("%s users row not PRESENT as designed" % who)
            say("%s users row written (attribute_not_exists) and read back PRESENT as designed" % who)
        ddb.put_item(TableName=PARTNER, Item={"email": {"S": ids.fa}, "firmId": {"S": "49financial"}, "advisorKey": {"S": ids.advisor_key},
                                              "advisorName": {"S": ids.name}, "advisorRole": {"S": "advisor"}, "firmRole": {"S": "user"},
                                              "createdAt": {"S": now}, "createdBy": {"S": "0.7.0_AE_CloudOps~AQ2"}, "updatedAt": {"S": now}},
                     ConditionExpression="attribute_not_exists(email)")
        written.append(("partner", ids.fa))
        say("FA partner row written (attribute_not_exists), advisorKey the synthetic key")
        pem = boto3.client("secretsmanager", region_name=REGION).get_secret_value(SecretId=KEY_SECRET)["SecretString"]
        if "BEGIN" not in pem[:40]:
            raise RuntimeError("signing secret is not a PEM string")
        say("signing key read (value never printed or written)")
        iat = int(time.time())
        base = {"iss": "opal-portal-auth", "aud": "opal-portal-api", "iat": iat, "exp": iat + LIFE}
        claims = {
            "FA": dict(base, sub=ids.fa, name=ids.name, firmId="49financial", tier="advisor", role="user", userType="test-filer", advisorId=ids.advisor_key),
            "CW": dict(base, sub=ids.cw, name=ids.name, firmId="cottonwood", tier="advisor", role="user", userType="test-filer"),
            "PK": dict(base, sub=PK_SUB, name=PK_SUB, userType="service", tier="service"),
        }
        for who, c in claims.items():
            tokens[who] = pyjwt.encode(c, pem, algorithm="RS256")
            exps.append(c["exp"])
            say("token for %s minted (held in memory only) iat=%s exp=%s" % (who, iso(c["iat"]), iso(c["exp"])))
        del pem
        out = {}
        state = ticket_arms(env, {"pkg3_prior": args.pkg3_prior}, out)
        bodies = {}
        if state["stop"]:
            stop = state["stop"]
        elif args.doors:
            default_price_date = expected_price_dates()
            before = default_price_date(None)
            bodies = door_arms(env, ids.date, out, lambda: {before, default_price_date(None)})
            say("expected price date (New York prior trading day) before=%s after=%s" % (before, default_price_date(None)))
        # C1
        c1 = "C1 NOT RUN door arms not run"
        if bodies:
            bun = find_bun()
            scratch = tempfile.mkdtemp(prefix="r28_c1_")
            try:
                commit, root = c1_prepare(scratch)
                got = [c1_parse(bun, root, bodies[k]) for k in ("D1", "D2", "D3")]
                say("C1 parseIrEnvelope from portal origin/PROD %s: %s" % (commit[:10], got))
                c1 = "C1 PARSED 3 of 3" if got == ["PARSED"] * 3 else "C1 FAIL %s" % got
            finally:
                shutil.rmtree(scratch, ignore_errors=True)
        out["C1"] = (c1 == "C1 PARSED 3 of 3", c1, c1)
        results.update(out)
        # counts per request sub-window (the ticket service's own log group)
        if starts:
            time.sleep(max(0, (starts[-1][1] + 300 + 60) - time.time()))
        counts = []
        if starts:
            lo_all, hi_all = starts[0][1] - 5, starts[-1][1] + 300
            events = []
            pg = logs.get_paginator("filter_log_events")
            for page in pg.paginate(logGroupName=TICKET_LOG, startTime=int(lo_all * 1000), endTime=int(hi_all * 1000)):
                events.extend(page.get("events", []))
            streams = len({e["logStreamName"] for e in events})
            tok = ("WE_CLIENT_SENT", "WE_DL_UNCONFIGURED", "WE_CLIENT_SEND_FAILED", "WE_DL_SENT", "WE_CLIENT_NOT_SINGULAR")
            for i, (arm, s) in enumerate(starts):
                e_ = starts[i + 1][1] if i + 1 < len(starts) else s + 300
                win = [e for e in events if s * 1000 <= e["timestamp"] < e_ * 1000]
                inv = sum(1 for e in win if e["message"].startswith("START RequestId"))
                tcount = {t: sum(1 for e in win if t in e["message"]) for t in tok}
                counts.append("%-7s [%s, %s) invocations=%d streams_in_window=%d tokens=%s authorize_decision_lines=0 (the service writes none)" % (
                    arm, iso(s), iso(e_), inv, len({e["logStreamName"] for e in win}), {k: v for k, v in tcount.items() if v}))
            counts.append("streams searched in the sitting window: %d (events %d)%s" % (streams, len(events), "  VOID" if streams == 0 else ""))
        (outdir / "SITTING_COUNTS.txt").write_text("\n".join(counts) + "\n", encoding="utf-8")
    except Exception as e:  # noqa: BLE001 -- anything is a STOP; the rows are still removed after exp
        stop = stop or "STOP (%s): %s" % (type(e).__name__, str(e)[:300])
        say(stop)
    finally:
        for k in list(tokens):
            tokens[k] = None
        if written and exps:
            wait = max(exps) + 5 - time.time()
            if wait > 0:
                say("waiting %ds for the later exp %s to pass before removal" % (int(wait), iso(max(exps))))
                time.sleep(wait)
        for kind, addr in written:
            try:
                if kind == "users":
                    ddb.delete_item(TableName=USERS, Key=ukey(addr), ConditionExpression="attribute_exists(PK)")
                else:
                    ddb.delete_item(TableName=PARTNER, Key={"email": {"S": addr}}, ConditionExpression="attribute_exists(email)")
                say("%s row deleted (attribute_exists)" % kind)
            except Exception as e:  # noqa: BLE001
                say("DELETE of %s row failed: %s" % (kind, str(e)[:160]))
        rem = []
        deadline = time.time() + 300
        for addr in (ids.fa, ids.cw):
            g = c = False
            while time.time() < deadline:
                c = cread(addr) is None
                g = gsi(addr) == 0
                say("removal read %s: GSI ABSENT=%s ConsistentRead ABSENT=%s" % (addr.split("@")[0][-24:], g, c))
                if g and c:
                    break
                time.sleep(10)
            if g:
                rem.append("ABSENT GSI %s" % addr)
            if c:
                rem.append("ABSENT CONSISTENT %s" % addr)
        p_abs = ddb.get_item(TableName=PARTNER, Key={"email": {"S": ids.fa}}, ConsistentRead=True).get("Item") is None
        rem.append("ABSENT PARTNER %s" % ids.fa if p_abs else "PRESENT PARTNER %s" % ids.fa)
        (outdir / "SITTING_REMOVAL.txt").write_text("\n".join(rem) + "\n", encoding="utf-8")
        arms = ("T4a", "T4b", "LIST-A", "LIST-B", "GET-B", "PKG-1", "PKG-2", "PKG-3", "D1", "D2", "D3", "D4", "C1")
        res_lines = []
        for arm in arms:
            if arm in results:
                res_lines.append(results[arm][1])
            else:
                res_lines.append("%s NOT RUN %s" % (arm, stop or "an earlier arm did not pass or the arm was not selected"))
        (outdir / "SITTING_RESULT.txt").write_text("\n".join(res_lines) + "\n", encoding="utf-8")
        (outdir / "SITTING_TRACE.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (outdir / "SITTING_DETAIL.txt").write_text("\n".join("%-7s %s | %s" % (a, "ok" if v[0] else "FAIL", v[2]) for a, v in results.items()) + "\n", encoding="utf-8")
    return 0 if not stop else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--go", action="store_true")
    ap.add_argument("--doors", action="store_true", help="run D1 to D4 and C1 (only after the YCharts hold is lifted)")
    ap.add_argument("--pkg3-literal", dest="pkg3_prior", action="store_false", help="PKG-3 without prior_attached_at (AMENDMENT 2 sends it by default)")
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d"))
    ap.add_argument("--out", default=str(HERE))
    args = ap.parse_args(argv)
    ids = Ids(args.date)
    if args.offline:
        res, _ = offline(ids, args)
        text = "\n".join(res) + "\n"
        print(text)
        Path(args.out, "SITTING_OFFLINE.txt").write_text(text, encoding="utf-8")
        return 0
    if args.live and args.go:
        return live(ids, args)
    ap.error("choose --offline, or --live --go")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
