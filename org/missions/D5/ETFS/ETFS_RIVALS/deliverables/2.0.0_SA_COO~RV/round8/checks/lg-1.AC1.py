"""RIV-lg-1 AC1 (row Z-S20): the Bloomberg leg carries an index-control-sized holdings list, and an overflow is a per-name
partial, never a leg crash. Source (measured 2026-10-03, one scripted query for 2026-10-01): IDVZ 45 / PFOE 24 / ACWI 2,198 /
IWM 1,979 rows. `excel_fetch` runs ONE query per date over every fund with max_rows=2000 and raises RuntimeError on overflow
(collector_bloomberg.py ~:411), which `_handler_entry` does not catch: the whole daily leg crashes.

Interface (prescribed at the cut):
  - a fund whose role is `index_control` (`universe.role`) is queried ON ITS OWN per date (its BQL names no other fund), under
    a row cap of at least 2,500 and below 50,000; the range read never truncates silently;
  - an overflow is a PER-NAME partial: the other funds' captures land, the batch reads PARTIAL with the overflowing fund named
    in `detail`, and no capture for it lands as OK;
  - the call shape stays `_handler_entry(event, fetch=None)` running `excel_fetch` (the terminal machine's Excel BQL path).

Offline: pywin32 is replaced by a fake Excel whose sheet returns, for the funds its BQL names, a planted holdings list
(header ID / ORIG_IDS / REPORT_DATE / DATES / name()). Local sink. Event: daily, date 2026-10-02 (-> report 2026-10-01).
RIVALFUNDS_LEG_ENABLE=1 so the v0.8 controls are in the universe.
  - (a) TXUE 40 + BIDD 40 + ACWI 2,300: no exception; the landed sidecars carry TXUE 40, BIDD 40 and ACWI 2,300 rows;
  - (b) the BQL that names ACWI names no other fund, and no other BQL names ACWI;
  - (c) TXUE 40 + BIDD 40 + IWM 50,000: no exception; status PARTIAL; TXUE and BIDD land 40 each; IWM is named in detail
        and no OK sidecar carries IWM;
  - (d) control: TXUE 40 + BIDD 40 alone lands both in OK captures, status OK;
  - (e) AMENDED 2026-10-05 (rows Z-S21/Z-S22, measured on the real Terminal: Range.Value overflowed on one IWM cell for
        2026-01-16 while Range.Value2 read every row and returned dates as Excel serials): with a sheet whose `Value` raises
        com_error and whose `Value2` returns the date columns as Excel serials, TXUE 40 + BIDD 40 still land whole, in OK
        captures (their DATES / REPORT_DATE read back as ISO dates), with no exception.
  - (f) AMENDED 2026-10-05 (row Z-S23, measured on the real Terminal: for 2026-01-16 Bloomberg returned IWM's columns in a
        different order from ACWI's -- `id().DATE` at column 1, not 7 -- and the merge kept only the first part's header, so
        every IWM row read as off the requested date): with ACWI's sheet in the usual column order and IWM's in a permuted
        order, both controls land whole in an OK capture, status OK.
FAIL at base: (a), (b), (c), (e) FAIL; (d) and (f) PASS (one query, one header). At the amend-2 build 5bb37fb4e0: (f) FAILS
(two queries, two headers, and the merge keeps the first)."""
import datetime as dt
import json
import os
import pathlib
import re
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY, REPORT = "2026-10-02", "2026-10-01"
HDR = ["ID", "ORIG_IDS", "REPORT_DATE", "DATES", "name()"]
FORMULAS: list[str] = []
BAD_VALUE: set = set()  # funds whose sheet makes Range.Value raise (a cell the COM conversion overflows on)
PERMUTE: set = set()  # funds whose sheet comes back with its columns in another order (DATES moved to column 1)


def rows_for(fund: str, n: int) -> list[list]:
    return [[f"SEC{fund}{i:05d} Equity", f"{fund} US Equity", REPORT, REPORT, f"Security {fund} {i}"] for i in range(n)]


def install_fake_com(plant: dict[str, int]) -> None:
    """pythoncom / pywintypes / win32com.client stand-ins: each sheet answers the BQL in its A1 formula from `plant`."""
    class ComError(Exception):
        hresult = 0

    class _Rows:
        def __init__(self, sh):
            self.sh = sh

        @property
        def Count(self):
            return len(self.sh.data)

    class _Used:
        def __init__(self, sh):
            self.sh = sh
            self.Rows = _Rows(sh)

        @property
        def Value(self):
            return tuple(tuple(r) for r in self.sh.data) or None

    class _Range:
        def __init__(self, sh, addr):
            self.sh, self.addr = sh, addr

        @property
        def Text(self):
            return self.sh.data[0][0] if self.sh.data else ""

        def _get_formula(self):
            return self.sh.formula

        def _set_formula(self, f):
            self.sh.set_formula(f)

        Formula = property(_get_formula, _set_formula)

        def _rows(self):
            m = re.match(r"^A1:[A-Z]+(\d+)$", self.addr)
            n = int(m.group(1)) if m else 1
            got = [tuple(r) for r in self.sh.data[:n]]
            width = len(HDR)
            return got + [(None,) * width] * (n - len(got))

        @property
        def Value(self):
            if BAD_VALUE and any(str(r[1]).split()[0] in BAD_VALUE for r in self.sh.data[1:]):
                err = ComError("Exception occurred.")
                err.hresult = -2147352567
                raise err
            return tuple(self._rows())

        @property
        def Value2(self):
            def serial(v):
                try:
                    return float((dt.date.fromisoformat(str(v)[:10]) - dt.date(1899, 12, 30)).days)
                except ValueError:
                    return v
            rows = self._rows()
            hdr = rows[0] if rows else ()
            dcols = {i for i, h in enumerate(hdr) if h in ("REPORT_DATE", "DATES")}
            return tuple(tuple(serial(v) if i in dcols and r[0] != "ID" and v is not None else v
                               for i, v in enumerate(r)) for r in rows)

    class _Cells:
        def __init__(self, sh):
            self.sh = sh

        def ClearContents(self):
            self.sh.formula, self.sh.data = "", []

    class _Sheet:
        def __init__(self):
            self.Name, self.formula, self.data = "", "", []
            self.Cells = _Cells(self)
            self.UsedRange = _Used(self)

        def Range(self, addr):
            return _Range(self, addr)

        def set_formula(self, f):
            self.formula = f
            FORMULAS.append(f)
            funds = re.findall(r"'([A-Z0-9]+) US Equity'", f.replace("''", "'"))
            data = [list(HDR)]
            for fd in funds:
                data += rows_for(fd, plant.get(fd, 0))
            if any(fd in PERMUTE for fd in funds):  # Bloomberg's column order differs per query: DATES moves to column 1
                order = [0, 3, 1, 2, 4]
                data = [[r[i] for i in order] for r in data]
            self.data = data

    class _Sheets:
        def __init__(self):
            self.all = []

        def Add(self):
            sh = _Sheet()
            self.all.append(sh)
            return sh

    class _Book:
        def __init__(self):
            self.Worksheets = _Sheets()

        def Close(self, SaveChanges=False):
            pass

    class _Books:
        def Open(self, p):
            return None

        def Add(self):
            return _Book()

    class _Excel:
        Visible = False
        DisplayAlerts = False

        def __init__(self):
            self.Workbooks = _Books()

        def RegisterXLL(self, p):
            return True

        def Calculate(self):
            pass

        def Quit(self):
            pass

    pc = types.ModuleType("pythoncom")
    pc.PumpWaitingMessages = lambda: None
    pw = types.ModuleType("pywintypes")
    pw.com_error = ComError
    w32 = types.ModuleType("win32com")
    cl = types.ModuleType("win32com.client")
    cl.DispatchEx = lambda name: _Excel()
    cl.Dispatch = cl.DispatchEx
    w32.client = cl
    sys.modules.update({"pythoncom": pc, "pywintypes": pw, "win32com": w32, "win32com.client": cl})


def sidecars(s, cb) -> list[dict]:
    return [json.loads(s.get(u).decode("utf-8")) for u in s.list(cb.bronze_prefix("")) if u.endswith(".sidecar.json")]


def landed(scs) -> dict[str, int]:
    out: dict[str, int] = {}
    for sc in scs:
        for f, n in (sc.get("row_count") or {}).items():
            out[f] = out.get(f, 0) + int(n)
    return out


def fire(plant, funds, tag):
    from rivalfunds import collector_bloomberg as cb
    from rivalfunds import sinks
    install_fake_com(plant)
    FORMULAS.clear()
    spec = f"local:{c.tmpdir('rv_lg1_' + tag + '_')}"
    ev = {"mode": "daily", "date": DAY, "funds": funds, "sink": spec, "batch_id": f"batch-lg1-{tag}"}
    try:
        res, err = cb._handler_entry(ev), None
    except Exception as e:  # the base behaviour: the overflow escapes the leg
        res, err = None, f"{type(e).__name__}: {e}"
    s = sinks.get_sink(spec)
    scs = sidecars(s, cb)
    print(f"[{tag}] error={err} status={res and res.get('status')} landed={landed(scs)} formulas={len(FORMULAS)}")
    return res, err, scs, list(FORMULAS)


def run(v):
    c.setup_path()
    c.offline_guards()
    os.environ["RIVALFUNDS_LEG_ENABLE"] = "1"

    res, err, scs, forms = fire({"TXUE": 40, "BIDD": 40, "ACWI": 2300}, ["TXUE", "BIDD", "ACWI"], "a")
    got = landed(scs)
    v.check(err is None and got.get("TXUE") == 40 and got.get("BIDD") == 40 and got.get("ACWI") == 2300,
            "(a) a 2,300-row control beside two rivals: no exception; TXUE 40, BIDD 40, ACWI 2,300 rows land")
    with_acwi = [f for f in forms if "'ACWI US Equity'" in f.replace("''", "'")]
    alone = bool(with_acwi) and all(not re.search(r"'(?!ACWI )[A-Z0-9]+ US Equity'", f.replace("''", "'")) for f in with_acwi)
    v.check(alone, f"(b) the control is queried on its own ({len(with_acwi)} BQL naming ACWI; none names another fund)")

    res, err, scs, _ = fire({"TXUE": 40, "BIDD": 40, "IWM": 50000}, ["TXUE", "BIDD", "IWM"], "c")
    got = landed([sc for sc in scs if sc.get("status") == "OK"])
    named = res is not None and "IWM" in json.dumps(res.get("detail"), default=str)
    v.check(err is None and res.get("status") == "PARTIAL" and got.get("TXUE") == 40 and got.get("BIDD") == 40
            and "IWM" not in got and named,
            "(c) a 50,000-row overflow is a per-name partial: PARTIAL, TXUE/BIDD land 40 each, IWM named, no OK IWM capture")

    res, err, scs, _ = fire({"TXUE": 40, "BIDD": 40}, ["TXUE", "BIDD"], "d")
    got = landed([sc for sc in scs if sc.get("status") == "OK"])
    v.check(err is None and res.get("status") == "OK" and got == {"TXUE": 40, "BIDD": 40},
            "(d) control: two rivals alone land OK, 40 rows each")

    BAD_VALUE.add("BIDD")
    res, err, scs, _ = fire({"TXUE": 40, "BIDD": 40}, ["TXUE", "BIDD"], "e")
    BAD_VALUE.clear()
    got = landed([sc for sc in scs if sc.get("status") == "OK"])
    v.check(err is None and res is not None and res.get("status") == "OK" and got == {"TXUE": 40, "BIDD": 40},
            "(e) a sheet whose Range.Value overflows still lands whole through Value2, dates read back as ISO (OK captures)")

    PERMUTE.add("IWM")
    res, err, scs, _ = fire({"ACWI": 300, "IWM": 200}, ["ACWI", "IWM"], "f")
    PERMUTE.clear()
    got = landed([sc for sc in scs if sc.get("status") == "OK"])
    print("[f] statuses:", [sc.get("status") for sc in scs])
    v.check(err is None and res is not None and res.get("status") == "OK" and got == {"ACWI": 300, "IWM": 200},
            "(f) two controls whose sheets come back in different column orders both land whole in an OK capture")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
