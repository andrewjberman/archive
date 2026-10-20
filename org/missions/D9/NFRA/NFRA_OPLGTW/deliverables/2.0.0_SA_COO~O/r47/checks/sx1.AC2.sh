#!/usr/bin/env bash
# OPLGTW OG-sx-1 AC2 (round 47): the YCharts and data-refresh repairs, probed with fakes (no network, no credential).
#  Y1 (Z-S423): _parse_table(rec, calc, symbols) attributes an entry that carries no id key to the requested symbol by position; never the string 'None'.
#  Y2 (Z-S422): ycharts_time_series, ycharts_risk_return_scatter, ycharts_fund_series and ycharts_snapshot_metrics answer an absent_reason that names the
#       upstream status ('upstream_http_403') when the upstream status is 400 or above; a 200 answer carries no absent_reason (None or absent).
#  Z-S424 part: ycharts_fund_series and ycharts_time_series answers fit 51200 bytes as the server indents them (json indent=2): the NEWEST points are kept,
#       'points' stays the total count, 'returned_points' is what is served, 'truncated' is true; a short series is untouched (truncated false or absent).
#  R1 (Z-S423): opal_data_refresh_status of an id the status route answers 404 for is status NOT_FOUND, terminal true (status_note kept); a 500 stays UNKNOWN, terminal false.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 110 python3 -I - <<'EOF'
import sys, json, types
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app.integrations.ycharts import integration as yc
    from app.integrations.opal_portal import integration as op
except Exception as exc:
    print("import failed: %s" % type(exc).__name__); print("NO"); sys.exit(0)

# ---- Y1
rec1 = {"json": {"indicesData": [{"data": [{"calc_name": "ytd_total_return", "calc_raw_value": 12.91}]}]}}
try:
    got = yc._parse_table(rec1, "ytd_total_return", ["^SPX"])
except TypeError:
    got = "TypeError"
say("Y1 one entry without an id key, one symbol", got == {"^SPX": 12.91}, "got %r" % (got,))
rec2 = {"json": {"indicesData": [{"data": [{"calc_name": "price", "calc_raw_value": 1.0}]}, {"data": [{"calc_name": "price", "calc_raw_value": 2.0}]}]}}
try:
    got = yc._parse_table(rec2, "price", ["AAA", "BBB"])
except TypeError:
    got = "TypeError"
say("Y1 two entries without ids, two symbols (by position)", got == {"AAA": 1.0, "BBB": 2.0}, "got %r" % (got,))
rec3 = {"json": {"indicesData": [{"security_id": "ZZZ", "data": [{"calc_name": "price", "calc_raw_value": 3.0}]}]}}
try:
    got = yc._parse_table(rec3, "price", ["ZZZ"])
except TypeError:
    got = "TypeError"
say("Y1 an entry that carries security_id keeps it", got == {"ZZZ": 3.0}, "got %r" % (got,))
rec4 = {"json": {"indicesData": [{"data": [{"calc_name": "price", "calc_raw_value": 1.0}]}, {"data": [{"calc_name": "price", "calc_raw_value": 2.0}]}]}}
try:
    got = yc._parse_table(rec4, "price", ["ONLY"])
except TypeError:
    got = "TypeError"
say("Y1 length mismatch never yields the key 'None'", isinstance(got, dict) and "None" not in got and None not in got, "got %r" % (got,))

# ---- Y2 and the cap, through the registered tools with a fake client
class Mcp:
    def __init__(self): self.fns = {}
    def tool(self, *a, **k):
        def deco(fn):
            self.fns[fn.__name__] = fn
            return fn
        return deco
def collect(client):
    inst = yc.YChartsIntegration()
    inst._client = lambda ck: client
    m = Mcp()
    orig = yc.run_integration_tool
    yc.run_integration_tool = lambda spec, name, args, fn, credential_provider=None: fn("cookie")
    inst.register(m)
    return m.fns, orig
class Client:
    def __init__(self, status=200, points=0):
        self.status, self.points = status, points
    def _series(self):
        return [[1600000000000 + i * 86400000, float(i)] for i in range(self.points)]
    def fund_data(self, symbol, calc):
        return {"http_status": self.status, "json": {"chart_data": [[{"raw_data": self._series()}]]} if self.status == 200 else None}
    def general_data(self, symbol, metric, start, end):
        return {"http_status": self.status, "json": {"chart_data": [{"raw_data": self._series()}]} if self.status == 200 else None}
    def scatter_plot_data(self, symbols, x, y):
        return {"http_status": self.status, "json": {"data": {"series": [{"x": 1, "y": 2}]}} if self.status == 200 else None}
    def indices_table_data(self, symbols, columns):
        return {"http_status": self.status, "json": {"indicesData": [{"data": [{"calc_name": columns[0], "calc_raw_value": 1.0}]}]} if self.status == 200 else None}
try:
    fns, orig = collect(Client(status=403))
    outs = {"ycharts_time_series": fns["ycharts_time_series"]("DIVZ", "price", "2026-10-14", "2026-10-16"),
            "ycharts_risk_return_scatter": fns["ycharts_risk_return_scatter"](["DIVZ", "SPY"], "annualized_volatility", "annualized_total_return"),
            "ycharts_fund_series": fns["ycharts_fund_series"]("DIVZ", "price"),
            "ycharts_snapshot_metrics": fns["ycharts_snapshot_metrics"](["^SPX"], ["ytd_total_return"])}
    for name, o in outs.items():
        reason = o.get("absent_reason") if isinstance(o, dict) else None
        say("Y2 %s on upstream 403" % name, isinstance(reason, str) and "403" in reason and o.get("http_status") == 403, "absent_reason %r" % (reason,))
    fns, _ = collect(Client(status=200, points=10))
    o = fns["ycharts_fund_series"]("DIVZ", "price")
    say("Y2 control: a 200 answer carries no absent_reason", not o.get("absent_reason") and o.get("points") == 10, "absent_reason %r points %r" % (o.get("absent_reason"), o.get("points")))
    say("cap control: a 10-point series is untouched", not o.get("truncated") and len(o.get("series") or []) == 10)
    fns, _ = collect(Client(status=200, points=1255))
    for name, args in (("ycharts_fund_series", ("DIVZ", "price")), ("ycharts_time_series", ("DIVZ", "price", "", ""))):
        o = fns[name](*args)
        size = len(json.dumps(o, indent=2, default=str).encode("utf-8"))
        s = o.get("series") or []
        say("cap %s: 1255 points fit 51200 bytes indented, newest kept, totals honest" % name,
            size <= 51200 and o.get("truncated") is True and o.get("points") == 1255 and o.get("returned_points") == len(s) and 0 < len(s) < 1255 and s[-1] == [1600000000000 + 1254 * 86400000, 1254.0],
            "size %d, points %r, returned %r, truncated %r" % (size, o.get("points"), o.get("returned_points"), o.get("truncated")))
except Exception as exc:
    print("ycharts probe raised %s: %s" % (type(exc).__name__, str(exc)[:120])); ok = False
finally:
    try:
        yc.run_integration_tool = orig
    except Exception:
        pass

# ---- R1
class Resp:
    def __init__(self, code, body=None):
        self.status_code, self._b = code, body or {}
    def json(self): return self._b
    @property
    def text(self): return json.dumps(self._b)
class Session:
    _cred = types.SimpleNamespace(get=lambda: None)
    def token(self, force=False): return "jwt"
def status_for(code):
    inst = op.OpalPortalIntegration()
    inst._session = Session()
    m = Mcp()
    orig_run, orig_get = op.run_integration_tool, op.httpx.get
    op.run_integration_tool = lambda spec, name, args, fn, credential_provider=None: fn("cred")
    def fake_get(url, headers=None, timeout=None, **k):
        if "/data-refresh/status/" in url:
            return Resp(code, {"status": "RUNNING"} if code == 200 else {})
        return Resp(200, {"date": "2026-10-16"})
    op.httpx.get = fake_get
    try:
        inst.register(m)
        return m.fns["opal_data_refresh_status"]("exec-0123456789ab")
    finally:
        op.run_integration_tool, op.httpx.get = orig_run, orig_get
try:
    o404, o500, o200 = status_for(404), status_for(500), status_for(200)
    say("R1 a 404 id is NOT_FOUND and terminal, note kept", o404.get("status") == "NOT_FOUND" and o404.get("terminal") is True and "404" in str(o404.get("status_note")), "status %r terminal %r" % (o404.get("status"), o404.get("terminal")))
    say("R1 a 500 stays UNKNOWN and non-terminal", o500.get("status") == "UNKNOWN" and o500.get("terminal") is False)
    say("R1 a 200 RUNNING stays non-terminal", o200.get("status") == "RUNNING" and o200.get("terminal") is False)
except Exception as exc:
    print("R1 probe raised %s: %s" % (type(exc).__name__, str(exc)[:120])); ok = False
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
