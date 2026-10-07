"""RIV-nc-1 AC1 (PRD v0.18 FWD-22; 1.0.0_SA_CTO~Z ruling msg 30817 term 2): a holding with no stored currency draws no
curve and says why.

Interface (prescribed, from the cell): `price_series.NO_HISTORY = "No price history is stored for this holding yet."`; for a
key with no stored currency `series` returns `source_words` equal to NO_HISTORY exactly (points all None, currency None). The
page's one script, for a security whose `currency` is null, draws no chart and shows the object's `source_words`, with the
same sentence in the script as its fallback.

Fixture: pc-1.AC1's frames (loaded without its verdict), window 2026-09-01 .. 2026-09-04: NNN_US_Equity has no G4 row (no
stored currency) and a fund report on every day; JJJ_JP_Equity is stored JPY; AAA_US_Equity is stored USD.
  - (a) `price_series.NO_HISTORY` is the prescribed sentence, and NNN's `source_words` equals it exactly;
  - (b) NNN keeps currency None and four None points; JJJ (a stored non-dollar currency) and AAA (USD) do NOT carry the
    sentence in their `source_words`;
  - (c) `render.CHART_SCRIPT` holds the sentence exactly once as text, and still holds "currency not on file" (the axis
    words of round 16);
  - (d) pc-1.AC1, pc-1.AC2 and md-1.AC2 still end `PASS 0 failures` (each run as its own process from the worktree root);
  - (e) control: the fixture holds no G4 row for NNN, a JPY row for JJJ and a USD row for AAA.
FAIL at base 0f7e460190: (a), (c) FAIL (no NO_HISTORY; the sentence is not in the script); (b), (d), (e) PASS."""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

SENTENCE = "No price history is stored for this holding yet."
EARLIER = ("pc-1.AC1", "pc-1.AC2", "md-1.AC2")
NNN, JJJ, AAA = "NNN_US_Equity", "JJJ_JP_Equity", "AAA_US_Equity"


def load_pc1():
    """pc-1.AC1's module with its fixture only (its own verdict never runs)."""
    p = HERE / "pc-1.AC1.py"
    src = p.read_text(encoding="utf-8")
    src = src[: src.index("failures = c.guarded(")]
    mod = type(sys)("pc1_ac1_fixture")
    mod.__file__ = str(p)
    exec(compile(src, str(p), "exec"), mod.__dict__)
    return mod


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import price_series, render

    pc1 = load_pc1()
    g4, g1, _g4_cols, _g1_cols = pc1.frames()
    out, err = {}, None
    try:
        out = price_series.series(g4, g1, [NNN, JJJ, AAA], pc1.START, pc1.END) or {}
    except Exception as e:  # noqa: BLE001 -- a raising build is a failed arm, and the control arm below still runs
        err = f"{type(e).__name__}: {e}"
    res = {k: (out.get(k) if isinstance(out.get(k), dict) else {}) for k in (NNN, JJJ, AAA)}
    const = getattr(price_series, "NO_HISTORY", None)
    print("series() error:", err, "| price_series.NO_HISTORY:", repr(const))
    for k in (NNN, JJJ, AAA):
        print(f"  {k}: currency {res[k].get('currency', '<absent>')!r} | priced points "
              f"{sum(1 for p in res[k].get('points') or [] if p[1] is not None)} of {len(res[k].get('points') or [])} | "
              f"source_words {res[k].get('source_words')!r}")

    v.check(const == SENTENCE and res[NNN].get("source_words") == SENTENCE,
            "(a) price_series.NO_HISTORY is the prescribed sentence and a key with no stored currency carries it as source_words")
    nnn_pts = res[NNN].get("points") or []
    v.check("currency" in res[NNN] and res[NNN]["currency"] is None and len(nnn_pts) == 4 and all(p[1] is None for p in nnn_pts)
            and all(isinstance(res[k].get("source_words"), str) and res[k]["source_words"].strip()
                    and SENTENCE not in res[k]["source_words"] for k in (JJJ, AAA)),
            "(b) that key keeps currency None and four None points; a stored JPY listing and a USD listing do not carry the sentence")

    script = getattr(render, "CHART_SCRIPT", "") or ""
    print("CHART_SCRIPT chars:", len(script), "| sentence count:", script.count(SENTENCE),
          "| 'currency not on file':", "currency not on file" in script)
    v.check(script.count(SENTENCE) == 1 and "currency not on file" in script,
            "(c) the page's one script holds the sentence exactly once and still holds the round-16 axis words")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(d) pc-1.AC1, pc-1.AC2 and md-1.AC2 still end PASS 0 failures")

    ccy = {k: sorted({str(x) for x in g4[g4.security_id == k].currency.dropna()}) for k in (NNN, JJJ, AAA)}
    print("fixture G4 currencies:", ccy, "| G1 rows for NNN:", int((g1.security_id == NNN).sum()))
    v.check(ccy == {NNN: [], JJJ: ["JPY"], AAA: ["USD"]} and int((g1.security_id == NNN).sum()) == 4,
            "(e) control: the fixture holds no G4 row for NNN, a JPY row for JJJ, a USD row for AAA, and four fund reports of NNN")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
