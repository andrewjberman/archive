"""RIV-nm-1 AC1 (RFW-D05): the Bloomberg capture REQUESTS a security name; canonical_shape carries it as
`security_name`.

Offline: no Bloomberg session, no Excel, no S3 (a local sink).
  - the plan: `collector_bloomberg.request_plan(D, None, {"funds": [...]})["queries"][D]` asks for the BQL field
    `name()` in its get() beside `id()`; the holdings universe and dates clause is unchanged;
  - the live request: `collector_bloomberg.excel_fetch` run against a FAKE Excel COM (pythoncom, pywintypes and
    win32com replaced in sys.modules BEFORE the call, every attribute of the fake client is the fake; `time` is a
    fake clock) writes ONE BQL.Query formula whose get() asks for `name()`, and its query equals the plan's for
    the same funds and date (two query builders that drift apart fail here);
  - the response: a capture whose header carries the BQL column `name()` -> collector import -> silver_bloomberg
    (column `name`, the header lower-cased as today) -> `gold_canonical_shape.build_bloomberg_rows` sets
    `security_name` to the captured name VERBATIM (display casing is `rivalfunds.names.display_name`, nm-1 AC2/AC3);
  - control: a row whose name cell is empty keeps `security_name` NULL (never the ticker).
Interface: query "get(id(), name()) for(holdings(['<T> US Equity',...],dates=<D>))" (spacing inside get() free),
the same string from request_plan and excel_fetch; silver column `name`; G1 `security_name` = silver `name`."""
import datetime as dt
import io
import json
import pathlib
import re
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D = "2026-10-01"
FUNDS = ["TXUE", "BIDD"]
SECS = [("8306 JP Equity", "MITSUBISHI UFJ FINANCIAL GROUP"), ("ATD CN Equity", "Alimentation Couche-Tard Inc"),
        ("XYZ US Equity", None)]


def get_clause(q):
    m = re.match(r"\s*get\((.*)\)\s*for\((.*)\)\s*$", q or "")
    return (m.group(1), "for(" + m.group(2) + ")") if m else (None, None)


class _Obj:
    """Any fake COM object: every attribute is another _Obj and every call returns one."""

    def __getattr__(self, k):
        return _Obj()

    def __call__(self, *a, **k):
        return _Obj()


FORMULAS, DISPATCHED = [], []


class _Range(_Obj):
    Text = "ID"
    Value = (("ID", "ORIG_IDS", "REPORT_DATE", "DATES"), ("X1", "TXUE US Equity", D, D))

    def __setattr__(self, k, val):
        if k == "Formula":
            FORMULAS.append(val)
        object.__setattr__(self, k, val)


class _Sheet(_Obj):
    UsedRange = types.SimpleNamespace(Rows=types.SimpleNamespace(Count=2))

    def Range(self, addr):
        return _Range()


def _dispatch(*a, **k):
    DISPATCHED.append(a)
    excel = _Obj()
    book = _Obj()
    object.__setattr__(book, "Worksheets", types.SimpleNamespace(Add=lambda *x, **y: _Sheet()))
    object.__setattr__(excel, "Workbooks", types.SimpleNamespace(Open=lambda *x, **y: None, Add=lambda *x, **y: book))
    return excel


class _Clock:
    def __init__(self, real):
        self.real, self.t = real, 0.0

    def monotonic(self):
        self.t += 0.5
        return self.t

    def sleep(self, s):
        return None

    def __getattr__(self, k):
        return getattr(self.real, k)


def fake_fetch(cb, funds_by_date):
    """excel_fetch under the fake COM; returns (captures or the exception, formulas written)."""
    names = ("pythoncom", "pywintypes", "win32com", "win32com.client")
    saved = {n: sys.modules.get(n) for n in names}
    pc, pt = types.ModuleType("pythoncom"), types.ModuleType("pywintypes")
    pc.PumpWaitingMessages = lambda *a, **k: None
    pt.com_error = type("com_error", (Exception,), {"hresult": 0})
    w, wc = types.ModuleType("win32com"), types.ModuleType("win32com.client")
    wc.DispatchEx = wc.Dispatch = _dispatch
    wc.__getattr__ = lambda name: _dispatch     # any other client entry point is the fake too
    w.client = wc
    real_time = cb.time
    sys.modules.update({"pythoncom": pc, "pywintypes": pt, "win32com": w, "win32com.client": wc})
    cb.time = _Clock(real_time)
    try:
        assert sys.modules["win32com.client"].DispatchEx is _dispatch
        try:
            out = cb.excel_fetch(funds_by_date, max_rows=10)
        except Exception as e:  # the fake answers little; the request written before any read is what is graded
            out = e
    finally:
        cb.time = real_time
        for n, m in saved.items():
            if m is None:
                sys.modules.pop(n, None)
            else:
                sys.modules[n] = m
    return out, list(FORMULAS)


def run(v):
    c.setup_path()
    import pyarrow.parquet as pq
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import gold_canonical_shape as gcs
    from rivalfunds import silver_bloomberg as sb
    from rivalfunds import sinks
    from rivalfunds.tests import test_b1_bloomberg_channel as tb1

    q_plan = cb.request_plan(D, None, {"funds": FUNDS})["queries"][D]
    g, tail = get_clause(q_plan)
    print("plan query:", q_plan)
    v.check(g is not None and "name()" in g.replace(" ", "") and "id()" in g.replace(" ", ""),
            "the plan's get() asks for name() beside id()")
    v.check(tail == f"for(holdings(['TXUE US Equity','BIDD US Equity'],dates={D}))",
            "control: the plan's holdings universe and dates clause is unchanged")

    out, formulas = fake_fetch(cb, {D: FUNDS})
    q_live = out[D].get("query") if isinstance(out, dict) and D in out else None
    print("fake COM: dispatched", len(DISPATCHED), "| formulas", formulas, "| result",
          type(out).__name__ if not isinstance(out, dict) else sorted(out))
    m = re.search(r'BQL\.Query\("(.*?)",', formulas[0]) if len(formulas) == 1 else None
    g_live = get_clause(m.group(1))[0] if m else None
    v.check(len(DISPATCHED) == 1 and g_live is not None and "name()" in g_live.replace(" ", ""),
            "the live fetch (fake COM) writes one BQL.Query formula whose get() asks for name()")
    v.check(q_live is not None and q_live == q_plan,
            "the live fetch's query equals the plan's query for the same funds and date")

    tmp = pathlib.Path(c.tmpdir("rv_nm1_"))
    spec = f"local:{tmp / 'sink'}"
    rows = [tb1._row("TXUE", sec, D) + [name] for sec, name in SECS]
    cap = tb1._cap(D, f"{D}T23:00:00-04:00", rows, funds=("TXUE",), header=tb1.HDR + ["name()"])
    (tmp / "cap.json").write_text(json.dumps(cap), encoding="utf-8")
    r1 = cb.handler_entry({"mode": "import", "captures": [str(tmp / "cap.json")], "batch_id": "nm1", "sink": spec,
                           "date": D})
    r2 = sb.handler_entry({"mode": "replay", "batch_id": "nm1s", "sink": spec, "date": D})
    s = sinks.get_sink(spec)
    uris = [u for u in s.list(sb.silver_prefix(D) + "/") if u.endswith(".parquet")]
    print("import", r1.get("status"), "| silver", r2.get("status"), "|", len(uris), "silver object(s)")
    v.check(r1.get("status") == "OK" and r2.get("status") == "OK" and len(uris) == 1,
            "control: the fixture capture lands in bronze and types into one silver object")
    if len(uris) != 1:
        return
    silver = pq.read_table(io.BytesIO(s.get(uris[0]))).to_pylist()
    print("silver columns:", sorted(silver[0]))
    g1 = gcs.build_bloomberg_rows(silver, "TXUE", dt.date.fromisoformat(D), "rev-nm1", uris[0],
                                  lambda sec, path=None: {"security_key": None, "reason": "fixture"}, None, "fixture")
    names = {r["security_bloomberg"]: r.get("security_name") for r in g1}
    print("G1 security_name:", names)
    v.check(names.get("8306 JP Equity") == "MITSUBISHI UFJ FINANCIAL GROUP"
            and names.get("ATD CN Equity") == "Alimentation Couche-Tard Inc",
            "canonical_shape security_name carries the captured name verbatim (today: NULL on every Bloomberg row)")
    v.check("XYZ US Equity" in names and names["XYZ US Equity"] is None,
            "control: a row with no name keeps security_name NULL, never the ticker")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
