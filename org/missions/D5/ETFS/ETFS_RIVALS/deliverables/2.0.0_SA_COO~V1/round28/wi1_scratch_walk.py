"""RIV-wi-1 J1: the scratch-sink FULL run_dag walk the CVO accepts as the real run for the lookup clauses (ADDENDUM 12, row D1-C-S13).

    python -I wi1_scratch_walk.py <day YYYY-MM-DD> <scratch dir> [--withhold <security_id> ...] [--cap N]

What is REAL: the stored G4 closes and corporate actions (copied READ-ONLY from the S3 sink into the scratch dir), `sweep.run_dag`
itself (the real function, so `run_one` -> `lookup_before_publish` -> `dramatic_move.run_for_day` is the real call chain),
`detect`, `lookup`, the parse, `write_rows` (to the scratch sink) and the Bright Data search (a WORLD act: --cap bounds it).
What is STUBBED: the stage runners (silver, canonical-shape, trade-schedule, publish-page) record that they ran and write nothing;
the markers are in memory. Nothing is written to S3 and no page is published.
--withhold drops that security's stored corporate-action rows from the SCRATCH COPY only, to re-create the condition "a dramatic
move with no split on file" for a name the stored data now explains (a constructed condition, labelled as such in the output).
"""
import datetime as dt
import io
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[8]
sys.path.insert(0, str(ROOT / "data" / "etfs" / "scripts"))

import pyarrow.parquet as pq  # noqa: E402

from rivalfunds import dramatic_move as dm  # noqa: E402
from rivalfunds import homes, sinks, sweep  # noqa: E402


class _Markers:
    def __init__(self):
        self.m = {}

    def has_marker(self, stage, date, sink):
        return bool(self.m.get((stage, date)))

    def read_markers(self, stage, date, sink):
        return list(self.m.get((stage, date), []))


def _runners(mk, order, stages):
    def mk_runner(stage):
        def run(ev):
            order.append(stage)
            mk.m.setdefault((stage, ev["date"]), []).append({"batch_id": ev["batch_id"]})
            return {"status": "OK", "outputs": []}
        return run
    return {s: mk_runner(s) for s in stages}


def _norm(k):
    return str(k).replace(" ", "_").strip().lower()


def main(argv):
    day, scratch = argv[0], argv[1]
    withhold, cap = [], dm.MAX_LOOKUPS_PER_RUN
    i = 2
    while i < len(argv):
        if argv[i] == "--withhold":
            withhold.append(argv[i + 1])
            i += 2
        elif argv[i] == "--cap":
            cap = int(argv[i + 1])
            i += 2
        else:
            raise SystemExit("unknown argument %r" % argv[i])
    src = sinks.get_sink("s3")
    dst = sinks.LocalSink(scratch)
    hi = dt.date.fromisoformat(day)
    lo = hi - dt.timedelta(days=dm.LOOKBACK_DAYS)
    copied = {"security_market": 0, "corporate_actions": 0}
    dropped_rows = 0
    d = lo
    while d <= hi:
        for kind in ("security_market", "corporate_actions"):
            prefix = homes.address("rivalfunds", "etfs", "gold", kind, "date=%s" % d.isoformat()) + "/"
            for uri in src.list(prefix):
                if not uri.endswith(".parquet"):
                    continue
                data = src.get(uri)
                if kind == "corporate_actions" and withhold:
                    t = pq.read_table(io.BytesIO(data))
                    keep = [i for i, sid in enumerate(t.column("security_id").to_pylist())
                            if _norm(sid) not in {_norm(w) for w in withhold}]
                    dropped_rows += t.num_rows - len(keep)
                    if len(keep) != t.num_rows:
                        buf = io.BytesIO()
                        pq.write_table(t.take(keep), buf)
                        data = buf.getvalue()
                dst.put(uri, data, "application/octet-stream")
                copied[kind] += 1
        d += dt.timedelta(days=1)
    print("SCRATCH sink %s: copied objects %s; withheld %s (%d stored action row(s) dropped from the COPY only)"
          % (scratch, copied, withhold or "none", dropped_rows))

    order, mk = [], _Markers()
    real_run = dm.run_for_day
    dm.run_for_day = lambda dday, sink, **k: real_run(dday, sink, cap=cap, **k)   # the real function; only the cap is bounded
    out = sweep.run_dag(day, dst, _runners(mk, order, sweep.DAG_RUNNERS), markers=mk, gate=lambda *a, **k: (True, "ok", {}))
    print("run_dag ran stages: %s" % order)
    print("run_dag dramatic_move: %s" % json.dumps(out.get("dramatic_move"), default=str))
    uri = ((out.get("dramatic_move") or {}).get("report") or {}).get("uri")
    if uri:
        t = pq.read_table(io.BytesIO(dst.get(uri))).to_pandas()
        print("WROTE %s (scratch): %d row(s)" % (uri, len(t)))
        for _, r in t.iterrows():
            print("  ", {k: (str(r[k]) if k != "ratio" else float(r[k])) for k in
                         ("security_id", "event_type", "ratio", "ex_date", "claim", "source", "source_url") if k in t.columns})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
