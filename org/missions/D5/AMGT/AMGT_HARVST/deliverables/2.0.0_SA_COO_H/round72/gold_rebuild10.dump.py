"""HARVST served gold rebuild #10 -- THE DIAGNOSTIC DUMP (issuer, NO WRITE to S3): the same build as the signing dry run,
through the same capturing client (PUTS SENT 0), with the served and the built rows of both tables kept on local disk under
`.runtime/harvest-backfill/r72_dump/` so the figures `1.0.0_SA_CTO~Z` msg 31812 asks about are read from rows, not counts.
"""
import importlib.util
import datetime
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("r10_signing", os.path.join(HERE, "gold_rebuild10.signing.py"))
s = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(s)

OUT = os.path.join(s.c.ROOT, ".runtime", "harvest-backfill", "r72_dump")


def keep(name, rows):
    with io.open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(rows, handle, default=str)
    print("KEPT %s: %d rows" % (name, len(rows)))
    sys.stdout.flush()


def main():
    os.makedirs(OUT, exist_ok=True)
    proposed = json.load(open(s.R64, encoding="utf-8"))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = s.store._default_client()
    print("READ STARTED %s as_of %s" % (datetime.datetime.now(datetime.timezone.utc).isoformat(), as_of))
    keep("served_mention", s.pg._latest_gold_snapshot_rows(s.pg.GOLD_TABLE))
    keep("served_daily", s.pg._latest_gold_snapshot_rows(s.pg.GOLD_DAILY_TABLE))
    cm = s.sg.CapturingClient(real)
    s.pg.build_mention(proposed, as_of, client=cm)
    (_mkey, mbody), = cm.puts.items()
    mention = s.pq.read_table(io.BytesIO(mbody)).to_pylist()
    keep("built_mention", mention)
    orig = s.pg._latest_gold_snapshot_rows
    s.pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == s.pg.GOLD_TABLE else orig(table, client=client)
    cd = s.sg.CapturingClient(real)
    s.pg.build_daily(proposed, as_of, client=cd)
    (_dkey, dbody), = cd.puts.items()
    keep("built_daily", s.pq.read_table(io.BytesIO(dbody)).to_pylist())
    s.pg._latest_gold_snapshot_rows = orig
    print("PUTS SENT: %d" % (cm.sent + cd.sent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
