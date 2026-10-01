"""RIV-e-1 AC2 -- the live (daily) mode is scripted and plans its request without calling Bloomberg: with mode "plan" the
stage returns the request it WOULD send for a given security list (field DVD_HIST_ALL, the history window, batches that
cover every security exactly once) and makes NO Bloomberg call; a security list read from a real G1-shaped input keeps every
non-cash security and drops cash/currency lines."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import rivalfunds.enrichment_bloomberg as e

    calls = []
    try:
        import integrations.bloomberg.mcp.blp_client as blp  # noqa: F401
        orig = blp.reference_data
        blp.reference_data = lambda *a, **k: calls.append(a) or {}
    except Exception:
        blp, orig = None, None
    rows = c.capture(c.idvz_captures(1)[0])["rows"]
    hdr = rows[0]
    ids = [r[hdr.index("ID")] for r in rows[1:]]
    secs = sorted(set(ids))
    cash = [s for s in secs if str(s).endswith(" Curncy")]
    try:
        p = e.handler_entry({"mode": "plan", "securities": secs, "batch_id": "chk-plan", "sink": "local:" + c.tmpdir("rv_e1p_"),
                             "date": "2026-09-30"})
    finally:
        if blp is not None:
            blp.reference_data = orig
    print("plan:", str(p)[:400])
    plan = p.get("plan") or {}
    v.check(not calls, f"no Bloomberg call in plan mode ({len(calls)} made)")
    v.check(plan.get("fields") == ["DVD_HIST_ALL"], f"fields {plan.get('fields')}")
    flat = [s for b in plan.get("batches", []) for s in b]
    want = [s for s in secs if s not in cash]
    v.check(sorted(flat) == sorted(want) and len(flat) == len(set(flat)),
            f"batches cover every non-cash security exactly once ({len(flat)} vs {len(want)}; {len(cash)} cash lines dropped)")
    v.check(bool(plan.get("start")) and bool(plan.get("end")), f"history window {plan.get('start')}..{plan.get('end')}")


failures = c.guarded("AC2", run)
if failures == 0:
    print("AC2 RESULT: PASS 0 failures")
else:
    print(f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
