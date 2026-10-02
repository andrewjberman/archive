"""RIV-st-1 AC3 (RFW-D02): `publish_page.a1_stale` exists, reads a newer input as stale, and reads every produced A1
table as current right after the rebuild -- so the page's fund headline and its input census read ONE G1 vintage.
Today the census keeps the G1 it was built from while the page reads the newer object ('13 of 13 current' beside
'2 of 13 arrived').

Interface (prescribed): `publish_page.a1_stale(s, day, table) -> bool` -- True when the newest G1 canonical_shape
object or G4 security_market object within the table's input window carries a revision time (the
`YYYYMMDDTHHMMSSZ` in its object name) later than the table's newest object's; tables: holding_contribution,
buying_trend, input_census.
Decided at the cut: a stale rebuild whose content equals an object already written (here buying_trend: the planted
G1 changes valuations only, so `write_unique` finds the same content sha and writes nothing today) must still leave
the table NOT stale -- its newest object then carries a revision time no earlier than the newer input's.

Fixture (`_d1_page`, offline, local sink): the round-5 page fixture published once for page day 2026-09-30; a
canonical_shape object for 2026-09-29 planted one second later than every A1 table; a second publish with no
refresh_a1.
  - right after the first build, a1_stale is False for each of the three tables (the rule's negative arm);
  - after the plant, a1_stale is True for each of the three (all three windows hold 2026-09-29);
  - after the second publish, a1_stale is False for each of the three;
  - one vintage: the newest input_census object's holdings rows name the planted G1 as their location, and the page
    manifest's canonical_shape input for 2026-09-29 is the same object;
  - the G4 arm: a security_market object for 2026-09-29 planted later than holding_contribution reads it stale."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _d1_page as p  # noqa: E402


def run(v):
    c.setup_path()
    import pyarrow.parquet as pq

    from rivalfunds import publish_page, revision

    spec, s, r1 = p.start()
    fn = getattr(publish_page, "a1_stale", None)
    v.check(callable(fn), "publish_page.a1_stale exists")

    def stale():
        return {t: (fn(s, p.DAY, t) if callable(fn) else None) for t in p.PRODUCED}

    s0 = stale()
    print("after the first build:", s0)
    v.check(all(x is False for x in s0.values()),
            "right after the first build, a1_stale is False for every produced table")
    planted = p.plant_g1(s)
    s1 = stale()
    print("after the G1 plant:", s1)
    v.check(all(x is True for x in s1.values()), "after a newer G1 lands, a1_stale is True for every produced table")
    r2 = p.publish(spec, "d1b")
    s2 = stale()
    print("publish 2:", r2["status"], "| after the rebuild:", s2)
    v.check(all(x is False for x in s2.values()), "right after the rebuild, a1_stale is False for every produced table")

    cen = pq.read_table(io.BytesIO(s.get(revision.newest(p.objects(s, "input_census"))))).to_pandas()
    locs = sorted(set(cen[cen["input_kind"] == "holdings"]["location"].astype(str)))
    page_g1 = [i.get("uri") for i in p.manifest(s).get("inputs", [])
               if i.get("kind") == "canonical_shape" and i.get("report_date") == p.AS_OF]
    print("census holdings location:", [x.rsplit("/", 1)[-1] for x in locs], "| page G1 for", p.AS_OF, ":",
          [str(x).rsplit("/", 1)[-1] for x in page_g1])
    v.check(locs == [planted] and page_g1 == [planted],
            "one G1 vintage: the census holdings rows and the page both read the planted 2026-09-29 object")

    p.plant_g4(s)
    g4 = fn(s, p.DAY, "holding_contribution") if callable(fn) else None
    print("after a newer G4:", g4)
    v.check(g4 is True, "a newer G4 security_market object in the window reads holding_contribution stale")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
