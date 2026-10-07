"""RIV-co-1 AC2 (PRD v0.18 FWD-22, ADDENDUM F.5 items 1 and 4; ROUND15_CELLS_DRAFT.md rev 1.5): the chart object's size line --
over the cap it is thinned and says so; still over, it is not written and the stage says so; the day's page publishes either way.

Measured at the base: `publish_page` has no `CHART_MAX_BYTES`, writes nothing under `charts/` and prints no chart line; the only
size rules are the page's (`MAX_PAGE_BYTES`) and the audit page's (`render.AUDIT_SOFT_CAP`).

Interface (prescribed, verbatim from the cell): `CHART_MAX_BYTES = 1_900_000` per object: over it, the 365-day points are thinned
to weekly (and the object says `"thinned": true`); still over -> the object is not written and the stage prints `FAIL: chart
object over cap for <FUND>`. The manifest gains `charts: {<FUND>: {"uri", "bytes", "securities", "markers", "thinned"}}`. The
day's page publishes whether or not a chart object fails.
The constant is read as `publish_page.CHART_MAX_BYTES` (the cell's file) and is set there by this check, as round 14's as-1 AC1
sets `render.AUDIT_SOFT_CAP`: the publisher must read it at call time.

Fixture: co-1 AC1's (test_p2's books on a `local:` sink, BASG without S02, page day 2026-09-30), built fresh for each of three
publishes: P1 at the default cap; P2 with CHART_MAX_BYTES = (P1's TXUE object bytes - 1); P3 with CHART_MAX_BYTES = 1.
  - (a) P1: `publish_page.CHART_MAX_BYTES` is 1_900_000; TXUE's object is written unthinned (no `thinned`, or false; the manifest
    reads thinned false) and stdout carries no chart FAIL line;
  - (b) P2: TXUE's object is written at no more than the cap, says `"thinned": true`, covers the same securities with fewer
    points in total than P1's, the manifest's charts entry reads thinned true with the stored bytes, and stdout carries no
    `FAIL: chart object over cap for TXUE` line;
  - (c) P3: neither fund's object is written, stdout carries a line starting `FAIL: chart object over cap for TXUE` and one for
    BASG, and the page still publishes (status not FAILED; index.html and manifest.json written);
  - (d) control: P1 publishes the page (status OK or PARTIAL, index.html and manifest.json written) and prints no line starting
    `FAIL: chart object over cap`.
FAIL at base: (a), (b), (c) FAIL (no CHART_MAX_BYTES, no chart object, no FAIL line); (d) PASSES."""
import contextlib
import io
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

DAY = "2026-09-30"
FAIL_LINE = "FAIL: chart object over cap for"
FUNDS = ("TXUE", "BASG")


def fixture():
    """co-1 AC1's fixture: c.page_fixture() with BASG holding no S02. Returns (spec, sink)."""
    import os

    from rivalfunds import gold_trade_schedule, guardrails, sinks
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    os.environ[guardrails.OVERRIDE_ENV] = json.dumps({"min_resolved_fraction": 0.0})
    spec = f"local:{c.tmpdir('rv_co1b_')}"
    s = sinks.get_sink(spec)
    for step, d in enumerate(("2026-09-25", "2026-09-28", tp2.DAY)):
        book = tp2._book(step)
        tp2._put(s, d, {"TXUE": (book, "bloomberg", 0.1 * step),
                        "BASG": ({k: q for k, q in book.items() if k != "S02"}, "issuer", 0.1 * step)})
    r = gold_trade_schedule.handler_entry({"date": tp2.DAY, "mode": "replay", "batch_id": "g", "sink": spec})
    assert r["status"] == "OK", r
    return spec, s


_UNSET = object()


def publish(cap=_UNSET):
    """One publish on a fresh fixture, with publish_page.CHART_MAX_BYTES forced to `cap` for the call (restored after).
    Returns (result, stdout, sink)."""
    from rivalfunds import publish_page
    from rivalfunds.tests import test_p2_page_grouped_by_fund as tp2

    spec, s = fixture()
    had, old = hasattr(publish_page, "CHART_MAX_BYTES"), getattr(publish_page, "CHART_MAX_BYTES", None)
    if cap is not _UNSET:
        publish_page.CHART_MAX_BYTES = cap
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            r = publish_page.handler_entry(tp2._ev(spec, day=DAY))
    finally:
        if cap is not _UNSET:
            if had:
                publish_page.CHART_MAX_BYTES = old
            else:
                del publish_page.CHART_MAX_BYTES
    return r, buf.getvalue(), s


def read(s, fund):
    """(stored bytes | None, parsed object | {}, manifest charts entry | {}) of one fund's chart object."""
    from rivalfunds import homes

    uri = homes.page(DAY, f"charts/{fund}.json")
    raw = s.get(uri) if s.exists(uri) else None
    try:
        obj = json.loads(raw.decode("utf-8")) if raw is not None else {}
    except Exception as e:  # noqa: BLE001 -- an unreadable object is a failed arm, not a crash
        print("unreadable", uri, type(e).__name__, e)
        obj = {}
    man_uri = homes.page(DAY, "manifest.json")
    man = json.loads(s.get(man_uri).decode("utf-8")) if s.exists(man_uri) else {}
    entry = (man.get("charts") or {}).get(fund) if isinstance(man.get("charts"), dict) else None
    return (None if raw is None else len(raw)), (obj if isinstance(obj, dict) else {}), (entry if isinstance(entry, dict) else {})


def n_points(obj) -> int:
    secs = obj.get("securities") if isinstance(obj.get("securities"), dict) else {}
    return sum(len(x.get("points") or []) for x in secs.values() if isinstance(x, dict))


def fail_lines(out: str) -> list:
    return [ln for ln in out.splitlines() if ln.startswith(FAIL_LINE)]


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import homes, publish_page

    idx_uri, man_uri = homes.page(DAY, "index.html"), homes.page(DAY, "manifest.json")
    default = getattr(publish_page, "CHART_MAX_BYTES", None)

    r1, out1, s1 = publish()
    b1, o1, e1 = read(s1, "TXUE")
    print("P1 (default cap", default, "):", r1.get("status"), "| TXUE object", b1, "B | thinned in object:", o1.get("thinned"),
          "| manifest thinned:", e1.get("thinned"), "| points", n_points(o1), "| chart FAIL lines:", fail_lines(out1))
    v.check(default == 1_900_000 and b1 is not None and o1.get("thinned") in (None, False) and e1.get("thinned") is False
            and n_points(o1) > 0 and not fail_lines(out1),
            "(a) CHART_MAX_BYTES is 1_900_000; under it TXUE's object is written unthinned and no chart FAIL line prints")

    cap2 = (b1 - 1) if b1 else 1_000_000
    r2, out2, s2 = publish(cap2)
    b2, o2, e2 = read(s2, "TXUE")
    same = sorted(o2.get("securities") or {}) == sorted(o1.get("securities") or {})
    print("P2 (cap", cap2, "):", r2.get("status"), "| TXUE object", b2, "B | thinned in object:", o2.get("thinned"),
          "| manifest:", {k: e2.get(k) for k in ("bytes", "thinned")}, "| points", n_points(o2), "of", n_points(o1),
          "| same securities:", same, "| chart FAIL lines:", fail_lines(out2))
    v.check(b1 is not None and b2 is not None and b2 <= cap2 and o2.get("thinned") is True and e2.get("thinned") is True
            and e2.get("bytes") == b2 and same and 0 < n_points(o2) < n_points(o1)
            and not any(ln.startswith(f"{FAIL_LINE} TXUE") for ln in fail_lines(out2)) and r2.get("status") != "FAILED",
            "(b) one byte over the cap, TXUE's object is thinned (fewer points, the same securities), says thinned true in the "
            "object and the manifest, fits the cap, and no FAIL line prints for it")

    r3, out3, s3 = publish(1)
    got3 = {f: read(s3, f)[0] for f in FUNDS}
    lines3 = fail_lines(out3)
    print("P3 (cap 1):", r3.get("status"), "| chart objects written:", got3, "| chart FAIL lines:", lines3,
          "| index", s3.exists(idx_uri), "manifest", s3.exists(man_uri))
    v.check(all(b is None for b in got3.values()) and all(any(ln.startswith(f"{FAIL_LINE} {f}") for ln in lines3) for f in FUNDS)
            and r3.get("status") in ("OK", "PARTIAL") and s3.exists(idx_uri) and s3.exists(man_uri),
            "(c) still over the cap after thinning, no chart object is written, the stage prints the FAIL line for each fund, "
            "and the page still publishes")

    print("control: P1 status", r1.get("status"), "| index", s1.exists(idx_uri), "manifest", s1.exists(man_uri),
          "| chart FAIL lines:", fail_lines(out1))
    v.check(r1.get("status") in ("OK", "PARTIAL") and s1.exists(idx_uri) and s1.exists(man_uri) and not fail_lines(out1),
            "(d) control: the page publishes on the fixture and prints no chart FAIL line")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
