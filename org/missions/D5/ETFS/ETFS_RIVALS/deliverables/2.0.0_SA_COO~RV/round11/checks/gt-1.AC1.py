"""RIV-gt-1 AC1 (rows Z-W3-S23 / Z-S42; round-9 addendum 2 @36310d88f1; round-10 analysis item 1 @134485f75b): a same-input G5 pass
at a NEW code version writes a new revision; at the SAME code version it still writes nothing. Measured 2026-10-05 by RIV-rp-2's
worker: `gold_trade_schedule._g5_target` returns the newest existing object whenever it records the same held funds, so a
`rebuild_funds` replay at a date whose live G5 already sits at the newest G1 revision reads OK and writes nothing (written_new 0).

Interface (prescribed): `gold_trade_schedule.GOLD_VERSION` (a module string, e.g. "gold_trade_schedule/2"). Every G5 object the
stage writes carries it in its parquet schema metadata under the key `producer_version`. `_g5_target` reuses the newest existing
object only when it records the same held funds AND the same `producer_version` as the running code. An object without the key
(every G5 written before this cell) reads as a different version. Otherwise the next `-v<NN>` object is written, never an
overwrite.
Fixture (offline, local sink, round 9's nf-1 fixture): canonical D1 and D2 for SCHY and TXUE at one revision; the stage builds
D2 (batch b1), then re-runs D2 on the SAME canonical revision with rebuild_funds ['TXUE'] under fresh batch ids:
  - (a) control, same code version (b2): written_new 0 and the newest G5 is still b1's object;
  - (b) a new code version (GOLD_VERSION patched, b3): written_new 1; the newest G5 is a new `-v<NN>` object whose metadata
    `producer_version` equals the patched value, and SCHY's rows in it equal b1's (carried, not re-inferred);
  - (c) a legacy object (b1's object rewritten without `producer_version`, current code, b4): written_new 1.
FAIL at base: (b) and (c) FAIL (nothing is written); (a) PASSES."""
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

REV = "20260930T000000Z-aaaaaaaaaaaa"


def run(v):
    c.setup_path()
    c.offline_guards()
    import pyarrow.parquet as pq

    from rivalfunds import gold_trade_schedule as g
    from rivalfunds import homes, markers, revision, sinks
    from rivalfunds.tests.test_g52_trade_schedule_v2 import BOOK, D1, D2, _canon, _doubled, _put_canonical

    spec = f"local:{c.tmpdir('rv_gt1_')}"
    s = sinks.get_sink(spec)
    for d in (D1, D2):
        schy = _doubled(BOOK, "S1 US Equity") if d == D2 else BOOK
        _put_canonical(s, d, _canon(d, schy, fund="SCHY") + _canon(d, BOOK, fund="TXUE"), rev=REV)
    g5_pre = homes.address("rivalfunds", "etfs", "gold", "trade_schedule", f"date={D2}") + "/"

    def objs():
        return sorted(u for u in s.list(g5_pre) if u.endswith(".parquet"))

    def stage(batch, rebuild=None):
        markers.write_marker(g.CANONICAL_STAGE, D2, batch, s,
                             {"status": "OK", "outputs": [homes.canonical_shape(D2, f"holdings-{REV}.parquet")]})
        ev = {"date": D2, "mode": "daily", "batch_id": batch, "sink": spec}
        if rebuild:
            ev["rebuild_funds"] = rebuild
        r = g.handler_entry(ev)
        return r, int((r.get("detail") or {}).get("written_new", -1))

    def schy(uri):
        df = pq.read_table(io.BytesIO(s.get(uri))).to_pandas()
        df = df[df["fund_id"].astype(str) == "SCHY"]
        keep = [k for k in df.columns if k not in ("revision", "produced_at", "batch_id", "producer_version")]
        return df[keep].astype(str).sort_values(keep).reset_index(drop=True)

    r1, w1 = stage("b1")
    first = revision.newest(objs())
    print("b1:", r1.get("status"), "written_new", w1, "| objects", [u.rsplit("/", 1)[-1] for u in objs()])

    r2, w2 = stage("b2", ["TXUE"])
    print("b2 (same version):", r2.get("status"), "written_new", w2, "| newest", revision.newest(objs()).rsplit("/", 1)[-1])
    v.check(w2 == 0 and revision.newest(objs()) == first, "(a) control: a same-input pass at the same code version writes nothing")

    cur = getattr(g, "GOLD_VERSION", None)
    g.GOLD_VERSION = (cur or "gold_trade_schedule/x") + "+check"
    try:
        n_before = len(objs())
        r3, w3 = stage("b3", ["TXUE"])
    finally:
        if cur is None:
            del g.GOLD_VERSION
        else:
            g.GOLD_VERSION = cur
    newest3 = revision.newest(objs())
    meta = (pq.read_schema(io.BytesIO(s.get(newest3))).metadata or {}).get(b"producer_version", b"").decode("utf-8", "replace")
    print("b3 (new version):", r3.get("status"), "written_new", w3, "| newest", newest3.rsplit("/", 1)[-1], "| producer_version", meta)
    v.check(w3 == 1 and len(objs()) == n_before + 1 and newest3 != first and "-v" in newest3.rsplit("/", 1)[-1]
            and meta.endswith("+check") and schy(newest3).equals(schy(first)),
            "(b) a same-input pass at a NEW code version writes a new -v<NN> revision stamped with that version; SCHY carried")

    for u in objs():
        t = pq.read_table(io.BytesIO(s.get(u)))
        md = {k: val for k, val in (t.schema.metadata or {}).items() if k != b"producer_version"}
        buf = io.BytesIO()
        pq.write_table(t.replace_schema_metadata(md or None), buf)
        s.put(u, buf.getvalue())
    n_before = len(objs())
    r4, w4 = stage("b4", ["TXUE"])
    print("b4 (legacy objects, current code):", r4.get("status"), "written_new", w4, "| objects", len(objs()))
    v.check(w4 == 1 and len(objs()) == n_before + 1, "(c) an object without producer_version reads as a different version: a new revision")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
