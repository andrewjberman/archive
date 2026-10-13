"""AMGT_RESAPP round-104 PREP -- `AMGT-bk-2`: the driven first overlay request's SPLIT of the two phases round 103 left unexplained.

  PYTHONPATH=<repo root> python r104_split_table.py --id-file <request file> [--handler-max-ms 3000]     (live: the request's own log stream)
  python r104_split_table.py --lines-file <log lines> [--handler-max-ms 3000]                            (offline control)

Runs `r102_phase_table.py` unchanged (its fourteen phases, T1 to T5, the REPORT line, the optional TARGET lines) and, after it, prints every `AMGT_SUBPHASE` line of the same request with its
share of its phase and two more rows:
    T6 the thirteen sub-phases (feed.imports, feed.snapshot, feed.items, feed.names; peers.read, peers.foreign, peers.subject_name, peers.subject_cap, peers.member_names,
       peers.reason_classes, peers.listed_identity, peers.numeric_tickers, peers.price_currency) once each;
    T7 the feed sub-phases sum within 10 percent or 25 ms of the `feed` phase, and the peers sub-phases within the `peers` phase.
Verdict: `R104 SPLIT TABLE: YES|NO`. The TARGET lines the wrapped instrument prints are INFORMATION for this cell: the cell is graded on the split being present and reconciling; FWD-40 (b)
is graded by the CVO on the handler time itself.
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location("pt", os.path.join(HERE, "..", "..", "round102_prep", "checks", "r102_phase_table.py"))
pt = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pt)
ORIG = pt.report
SUB = ["feed.imports", "feed.snapshot", "feed.items", "feed.names", "peers.read", "peers.foreign", "peers.subject_name", "peers.subject_cap", "peers.member_names",
       "peers.reason_classes", "peers.listed_identity", "peers.numeric_tickers", "peers.price_currency"]
LINE = re.compile(r"AMGT_SUBPHASE route=overlay phase=(\S+) ms=(\d+)")
PHASE = re.compile(r"AMGT_PHASE route=overlay phase=(\S+) ms=(\d+)")


def within(part, whole):
    return abs(part - whole) <= max(25, 0.10 * whole)


def report(messages, rid):
    rc = ORIG(messages, rid)
    sub = [(mm.group(1), int(mm.group(2))) for m in messages for mm in [LINE.search(m)] if mm]
    ph = {mm.group(1): int(mm.group(2)) for m in messages for mm in [PHASE.search(m)] if mm}
    seen = dict(sub)
    for name in SUB:
        if name in seen:
            outer = ph.get(name.split(".")[0])
            print("SUBPHASE %-24s %6d ms  %s of %s" % (name, seen[name], ("%.1f%%" % (100.0 * seen[name] / outer)) if outer else "?", name.split(".")[0]))
    t6 = sorted(n for n, _ in sub) == sorted(SUB)
    feed_sum = sum(v for n, v in sub if n.startswith("feed."))
    peers_sum = sum(v for n, v in sub if n.startswith("peers."))
    t7 = t6 and within(feed_sum, ph.get("feed", 0)) and within(peers_sum, ph.get("peers", 0))
    print("   feed sub-phases %d ms against feed %s ms; peers sub-phases %d ms against peers %s ms" % (feed_sum, ph.get("feed"), peers_sum, ph.get("peers")))
    print("   %s T6 thirteen sub-phases once each" % ("PASS" if t6 else "FAIL"))
    print("   %s T7 the sub-phases sum to their phases" % ("PASS" if t7 else "FAIL"))
    print("R104 SPLIT TABLE: %s" % ("YES" if t6 and t7 else "NO"))
    return rc if (t6 and t7) else 1


pt.report = report

if __name__ == "__main__":
    sys.exit(pt.main(sys.argv[1:]))
