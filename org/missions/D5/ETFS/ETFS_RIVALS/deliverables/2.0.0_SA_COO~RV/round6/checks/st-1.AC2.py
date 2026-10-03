"""RIV-st-1 AC2 (RFW-D01, CONTROL): with NO newer input, a second publish rebuilds nothing -- every produced A1 table
is SKIPPED and no new A1 object is written, as today. The staleness test must not turn every publish into a rebuild.

Interface: `publish_page.produce_a1(s, sink_spec, day, refresh=False) -> {table: {"status", ...}}` (signature
unchanged).

Fixture (`_d1_page`, offline, local sink): the round-5 page fixture, published once for page day 2026-09-30; every
G1 object in it (revision 20260930T000000Z) is older than the A1 tables just built.
  - a second publish (new batch, no refresh_a1) leaves the object count of each produced table unchanged;
  - `produce_a1` called again on the same sink reports SKIPPED for each of the three tables."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _d1_page as p  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import publish_page

    spec, s, r1 = p.start()
    before = {t: p.objects(s, t) for t in p.PRODUCED}
    r2 = p.publish(spec, "d1c")
    after = {t: p.objects(s, t) for t in p.PRODUCED}
    print("publish 1:", r1["status"], "| publish 2:", r2["status"],
          "| objects before:", {t: len(u) for t, u in before.items()}, "after:", {t: len(u) for t, u in after.items()})
    v.check(all(len(u) == 1 for u in before.values()) and after == before,
            "a second publish with no newer input writes no new A1 object")
    res = publish_page.produce_a1(s, spec, p.DAY)
    print("produce_a1 again:", {t: (res.get(t) or {}).get("status") for t in p.PRODUCED})
    v.check(all((res.get(t) or {}).get("status") == "SKIPPED" for t in p.PRODUCED),
            "produce_a1 with no newer input reports SKIPPED for holding_contribution, buying_trend and input_census")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
