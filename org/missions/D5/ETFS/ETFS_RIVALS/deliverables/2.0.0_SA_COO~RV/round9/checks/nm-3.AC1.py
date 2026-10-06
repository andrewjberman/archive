"""RIV-nm-3 AC1 (CVO C-S36; round-8 analysis item 5): a security the page names by its ticker form gets its real name, asked of
Bloomberg ONCE. Measured on the 10-05 render context: 135 keys carry a ticker-form name ('ATD CN Equity'); 0 of them sit in any
fund's latest holdings (they are past holdings the trade log and rankings still show); 128 were never in any G4 date and 7 sit in
G4 with no name -- the G4 enrichment asks only for current holdings, so these never get a name (the key space, not capacity).

Interface (prescribed): stage `rivalfunds.security_names.handler_entry({"date": <page day>, "sink"}, fetch=None)` reads the newest
holding_contribution object of the page day, takes the security keys whose `security_name` is blank or a ticker form
('<id> XX Equity'), drops the keys the newest `gold/security_names` object already names, asks `fetch(keys) -> {key: name}`
(production: one LONG_COMP_NAME reference request inside the cb-1 budget) for the rest, and writes a new security_names object
holding the prior names plus the new ones. `gold_holding_contribution` takes a key's name from the newest security_names object
when G4 has none, before any G1 name.
Fixture (offline, local sink): hc-1.AC2's page day 2026-10-05 (PFOE holds AAA, PCLG holds BBB); AAA's G4 rows carry 'Aaa Corp';
BBB's G4 rows carry no name and its G1 rows carry 'BBB US Equity'; the fake fetch returns {'BBB_US_Equity': 'Bbb Holdings Inc'}:
  - (a) the names stage asks for exactly ['BBB_US_Equity'];
  - (b) holding_contribution rebuilt after it names BBB 'Bbb Holdings Inc';
  - (c) a second names run asks for nothing;
  - (d) control: AAA keeps 'Aaa Corp' and is never asked.
FAIL at base: (a), (b) and (c) FAIL (no security_names stage); (d) PASSES."""
import importlib
import io
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parents[1] / "round8" / "checks"))
import _common as c  # noqa: E402


def load_hc_ac2():
    p = HERE.parents[1] / "round8" / "checks" / "hc-1.AC2.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("hc1_ac2_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import gold_holding_contribution as hc
    from rivalfunds import homes, sinks

    f = load_hc_ac2()
    orig_g4, orig_g1 = f.g4_rows, f.g1_rows

    def g4_rows(d):
        return [dict(r, security_name=None) if r["security_id"] == "BBB_US_Equity" else r for r in orig_g4(d)]

    def g1_rows(d):
        return [dict(r, security_name="BBB US Equity") if r["security_id"] == "BBB_US_Equity" else r for r in orig_g1(d)]

    spec = f"local:{c.tmpdir('rv_nm3_')}"
    s = sinks.get_sink(spec)
    for d in f.DAYS:
        f.put_parquet(s, homes.canonical_shape(d, f"holdings-{f.REV}.parquet"), g1_rows(d))
        f.put_parquet(s, homes.address("rivalfunds", "etfs", "gold", "security_market", f"date={d}", f"market-{f.G4REV}.parquet"),
                      g4_rows(d))

    def names_of():
        r = hc.handler_entry({"date": f.PAGE, "sink": spec})
        uri = (r.get("outputs") or [None])[0]
        df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas() if uri else None
        sec = df[df["axis"] == "security"] if df is not None else None
        return {} if sec is None else dict(zip(sec["bucket"].astype(str), sec["security_name"].astype(str)))

    before = names_of()
    print("before:", {k: before.get(k) for k in ("AAA_US_Equity", "BBB_US_Equity")})
    asked = []

    def fake(keys):
        asked.append(sorted(keys))
        return {k: "Bbb Holdings Inc" for k in keys if k == "BBB_US_Equity"}

    try:
        sn = importlib.import_module("rivalfunds.security_names")
    except ImportError:
        sn = None
    r1 = sn.handler_entry({"date": f.PAGE, "sink": spec}, fetch=fake) if sn else {"status": "ABSENT"}
    print("names stage 1:", r1.get("status"), "| asked", asked)
    v.check(asked[:1] == [["BBB_US_Equity"]], "(a) the names stage asks Bloomberg for exactly the ticker-named key")
    after = names_of()
    print("after:", {k: after.get(k) for k in ("AAA_US_Equity", "BBB_US_Equity")})
    v.check(after.get("BBB_US_Equity") == "Bbb Holdings Inc", "(b) holding_contribution names BBB from the stored name")
    n0 = len(asked)
    r2 = sn.handler_entry({"date": f.PAGE, "sink": spec}, fetch=fake) if sn else {"status": "ABSENT"}
    print("names stage 2:", r2.get("status"), "| asks since stage 1", asked[n0:])
    v.check(sn is not None and all(not a for a in asked[n0:]), "(c) a second run asks for nothing")
    v.check(after.get("AAA_US_Equity", before.get("AAA_US_Equity")) == "Aaa Corp" and not any("AAA_US_Equity" in a for a in asked),
            "(d) control: AAA keeps its G4 name and is never asked")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
