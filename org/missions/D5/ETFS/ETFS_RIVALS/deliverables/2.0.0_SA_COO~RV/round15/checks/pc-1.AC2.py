"""RIV-pc-1 AC2 (PRD v0.18 FWD-22; row ETFS_RIVALS-Z-S55; 1.0.0_SA_CTO~Z ruling msg 30787 terms 2 and 3): the chart object
carries each security's quote currency, the page's one script reads it, and the round's earlier chart checks still pass.

Fixture: co-1.AC1's own (`fixture()` and `publish()` of round15/checks/co-1.AC1.py, loaded without its verdict): day
2026-09-30, funds TXUE and BASG. That fixture holds no G4 currency at the base; the cell plants G4 rows carrying `currency`
`USD` for its securities (the one edit the cell may make to it), so its securities are dollar listings.
  - (a) every security of TXUE's and of BASG's chart object carries the key "currency", and its value is "USD";
  - (b) `render.CHART_SCRIPT` reads the object's currency (the text `.currency` is in the script) and names what it says
    when none is stored (the words "currency not on file");
  - (c) the earlier checks still end `PASS 0 failures`: ps-1.AC1, co-1.AC1, co-1.AC2, md-1.AC1, md-1.AC2 (each run as its
    own process from the worktree root);
  - (d) control: the page publishes on the fixture (status OK or PARTIAL) and both chart objects are written and parse.
FAIL at base 370ae7a279: (a), (b) FAIL (no "currency" in the object, none in the script); (c), (d) PASS."""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

EARLIER = ("ps-1.AC1", "co-1.AC1", "co-1.AC2", "md-1.AC1", "md-1.AC2")
FUNDS = ("TXUE", "BASG")


def load_co1():
    """co-1.AC1's module with its fixture and publish only (its own verdict never runs)."""
    p = HERE / "co-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("co1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import homes, render

    co1 = load_co1()
    spec, s = co1.fixture()
    r, _out = co1.publish(spec)
    objs = {}
    for f in FUNDS:
        uri = homes.page(co1.DAY, f"charts/{f}.json")
        try:
            objs[f] = json.loads(s.get(uri).decode("utf-8")) if s.exists(uri) else None
        except Exception as e:  # noqa: BLE001 -- an unreadable object is a failed arm, not a crash
            print("unreadable", uri, type(e).__name__, e)
            objs[f] = None
    ccys = {f: {k: (sec.get("currency", "<absent>") if isinstance(sec, dict) else "<not a dict>")
                for k, sec in ((objs[f] or {}).get("securities") or {}).items()} for f in FUNDS}
    for f in FUNDS:
        print(f"{f}: securities {len(ccys[f])} | currency values {sorted(set(map(str, ccys[f].values())))}")
    v.check(all(ccys[f] and all(val == "USD" for val in ccys[f].values()) for f in FUNDS),
            '(a) every security of each fund\'s chart object carries "currency": "USD" on the dollar fixture')

    script = getattr(render, "CHART_SCRIPT", "") or ""
    print("CHART_SCRIPT chars:", len(script), "| reads .currency:", ".currency" in script,
          "| says 'currency not on file':", "currency not on file" in script)
    v.check(".currency" in script and "currency not on file" in script,
            "(b) the page's one script reads the object's currency and names the case where none is stored")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=600)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(c) ps-1.AC1, co-1.AC1, co-1.AC2, md-1.AC1 and md-1.AC2 still end PASS 0 failures")

    print("publish:", r.get("status"), "| objects parsed:", {f: isinstance(objs[f], dict) for f in FUNDS})
    v.check(r.get("status") in ("OK", "PARTIAL") and all(isinstance(objs[f], dict) and objs[f].get("securities") for f in FUNDS),
            "(d) control: the page publishes on the fixture and both chart objects are written and parse")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
