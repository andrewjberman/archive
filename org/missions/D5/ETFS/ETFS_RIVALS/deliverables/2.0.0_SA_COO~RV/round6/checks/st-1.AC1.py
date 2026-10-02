"""RIV-st-1 AC1 (RFW-D01): a G1 object that lands AFTER the A1 tables were built forces the next publish to rebuild
them. Today `publish_page.produce_a1` skips a table when the day already holds an object of it ('1 object(s) already
at date=...'), so a later G1 or G4 object never reaches holding_contribution, buying_trend or input_census.

Interface (prescribed): `publish_page.a1_stale(s, day, table) -> bool` is True when the newest G1 canonical_shape
object or G4 security_market object within the table's input window carries a revision time (the `YYYYMMDDTHHMMSSZ`
in its object name) later than the table's newest object's. `produce_a1` rebuilds a stale table WITHOUT
`refresh_a1`, and the manifest's `a1_produced[<table>]` records `stale_rebuilt: true` and
`stale_input: <the newer input's object uri>`.

Fixture (`_d1_page`, offline, local sink): the round-5 page fixture, published once for page day 2026-09-30 (the
three A1 tables built); then a canonical_shape object for 2026-09-29 is planted one second LATER than every A1
table, carrying different valuations; the next publish runs with no `refresh_a1`.
  - control: the first publish builds one object of each produced table;
  - the second publish writes a NEW holding_contribution object, and that object read the planted G1 (its
    input_manifest `g1` list names it);
  - the second publish's manifest: a1_produced.holding_contribution is status OK (not SKIPPED), stale_rebuilt
    true, and its stale_input names the planted object."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _d1_page as p  # noqa: E402


def run(v):
    c.setup_path()
    import io

    import pyarrow.parquet as pq

    from rivalfunds import revision

    spec, s, r1 = p.start()
    before = {t: p.objects(s, t) for t in p.PRODUCED}
    print("publish 1:", r1["status"], "| objects:", {t: len(u) for t, u in before.items()})
    v.check(r1["status"] in ("OK", "PARTIAL") and all(len(u) == 1 for u in before.values()),
            "control: the first publish builds one object of each produced A1 table")

    planted = p.plant_g1(s)
    r2 = p.publish(spec, "d1b")
    after = p.objects(s, "holding_contribution")
    new = sorted(set(after) - set(before["holding_contribution"]))
    print("planted:", planted.rsplit("/", 1)[-1], "| publish 2:", r2["status"], "| new holding_contribution objects:",
          [u.rsplit("/", 1)[-1] for u in new])
    newest = revision.newest(after)
    frame = pq.read_table(io.BytesIO(s.get(newest))).to_pandas()
    read = json.loads(frame["input_manifest"].iloc[0]).get("g1", [])
    v.check(len(new) == 1 and newest == new[0] and planted in read,
            "the second publish (no refresh_a1) writes a new holding_contribution object, built from the planted G1")

    man = p.manifest(s)
    hc = (man.get("a1_produced") or {}).get("holding_contribution") or {}
    print("manifest batch:", man.get("batch_id"), "| a1_produced.holding_contribution:",
          {k: hc.get(k) for k in ("status", "stale_rebuilt", "stale_input")})
    v.check(man.get("batch_id") == "d1b" and hc.get("status") == "OK" and hc.get("stale_rebuilt") is True
            and planted.rsplit("/", 1)[-1] in str(hc.get("stale_input") or ""),
            "manifest a1_produced.holding_contribution: status OK, stale_rebuilt true, stale_input names the "
            "planted G1")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
