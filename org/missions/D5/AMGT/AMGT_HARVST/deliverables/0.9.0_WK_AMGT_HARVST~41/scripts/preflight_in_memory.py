"""HVST-d-2 PREFLIGHT (read-only): the in-memory rebuild set against the pair, before any put."""
import datetime
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _rebuild as R  # noqa: E402

from lib.research.harvest import store  # noqa: E402


def main():
    client = store._default_client()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    print("as_of (today UTC) = %s" % as_of)
    served = {t: R.read_key(R.parts(t, client)[-1][0], client) for t in R.TABLES}
    mem, n_art, _titles = R.memory(R.load_securities(), as_of, client)
    print("silver articles read = %d" % n_art)
    m = R.classify_mention(served[R.TABLES[0]], mem[R.TABLES[0]])
    d = R.classify_daily(served[R.TABLES[1]], mem[R.TABLES[1]], as_of)
    e = R.classify_event(served[R.TABLES[2]], mem[R.TABLES[2]])
    R.print_classification("preflight", m, d, e)
    bad = m["outside"] + d["outside"] + e["outside"]
    print("PREFLIGHT %s (%d outside)" % ("CLEAN" if not bad else "OUTSIDE", len(bad)))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
