"""AMGT_RESAPP round-93 PREP -- D1-S21: a candidate row that IS the subject's own company, by held identity, is excluded at the ranker.

  PYTHONPATH=<repo root> python r93_self_peer.py            (no network, no AWS: fixture rows)

The ranker (`engine.peers`) already excludes a row by the subject's ticker, by an EXACT normalised name, and by a share-class sibling. It does
not see a row the held list names as the subject's own company under a different name string: the model block calls Roche 'ROCHE HOLDING
AG-GENUSSCHEIN' and the scanner 'Roche Holding Ltd'; ten subjects list themselves as peers (7 live before pp-1, 10 after). The rule is by
IDENTITY: a row whose cleaned name token (`numeric_tickers.name_token`) names, in the held-name index the serve path already builds, EXACTLY ONE
company and that company is the subject's key, is the subject itself. `peers(..., held_name_index=<{token: [keys]}>, clean_name=<callable>)`;
no index (the default) leaves every result byte-equal.

    E1 the row is excluded: not a member, and `denominators["self_excluded_by_identity"]` names it, `self_excluded` counts it.
    E2 control: without an index the same row IS a member (the arm is not vacuous).
    E3 control: a token that names two held companies (the subject and another) excludes nothing.
    E4 control: a token that names ANOTHER held company excludes nothing.
    E5 backfill: with 13 deeper-rung candidates and the self row ranked first, the set is still 12 members, the self row absent, the next
       ranked present.
    E6 control: an EMPTY index leaves the result byte-equal to the no-index call (ignoring the `vintage` timestamp).
    E7 wiring (source level): `engine.run_batch` and `engine.main` take the index and pass it to `peers` (`held_name_index` is in their
       source). The peers package never imports the api package (a guard test enforces it), so the index comes from a caller above it.
    E8 the caller above: `lib.research.api.peers_rebuild.main(argv)` builds the index ONCE from `scoped_amgt._held_name_index` and the cleaner
       `scoped_amgt._clean_display_name` and hands both to `engine.main`; when the index build raises, it REFUSES (ValueError) and calls nothing.
       The member-by-member control of the rebuild is its own pair.
Verdict: R93 SELF PEER: YES|NO (exit 0|1). At the base (2026-10-11) only E2 PASSes: the keyword does not exist, so E1, E3, E4, E5, E6 raise TypeError and read FAIL, E7 FAILs and E8 FAILs (no such module).
"""
import copy
import inspect
import json
import sys

from lib.research.peers import engine

SUBJ = "SUBJ_US_Equity"
SELF_TOKEN = "subject"          # name_token('Subject Co PLC') == name_token('Subject Co') == 'subject'


def _row(ticker, name, cap, industry="Software and Consulting", country="United States", security_key=None):
    return {"ticker": ticker, "name": name, "sector": "Technology", "industryGroup": industry, "country": country, "mktVal": cap,
            "price": 10.0, "universe_weights": {"sp500": 0.1}, "sources": ["scanner"], "security_key": security_key}


def universe(extra_peers=0):
    rows = [_row("SUBJ", "Subject Co", 1000.0),
            _row("710891", "Subject Co PLC", 1000.0),           # the subject's own company, another name string, ranked first
            _row("T1", "Peer One", 1000.0), _row("T2", "Peer Two", 900.0), _row("T3", "Peer Three", 1100.0)]
    for i in range(extra_peers):
        rows.append(_row("P%02d" % i, "Peer Extra %02d" % i, 800.0 - i))
    return rows


def run(rows, **kw):
    return engine.peers(SUBJ, candidate_universe=copy.deepcopy(rows), resolve_identities=False, **kw)


def say(ok, label, detail=""):
    print("%s %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    return ok


def tickers(result):
    return [m["ticker"] for m in result.get("members") or []]


def e8():
    label = "E8 the caller above builds the index once, hands it to engine.main, and REFUSES when the build raises"
    try:
        from lib.research.api import peers_rebuild, scoped_amgt
    except ImportError as exc:
        return say(False, label, "no lib.research.api.peers_rebuild: %s" % exc)
    seen = {}
    saved = (engine.main, scoped_amgt._held_name_index)
    try:
        engine.main = lambda argv=None, **kw: seen.update(kw, argv=argv) or 0
        calls = []
        scoped_amgt._held_name_index = lambda: calls.append(1) or {"tok": ["K_US_Equity"]}
        rc = peers_rebuild.main(["--as-of", "2026-10-11"])
        built_once = len(calls) == 1 and seen.get("held_name_index") == {"tok": ["K_US_Equity"]} and callable(seen.get("clean_name"))
        seen.clear()

        def boom():
            raise RuntimeError("no names")
        scoped_amgt._held_name_index = boom
        refused = False
        try:
            peers_rebuild.main(["--as-of", "2026-10-11"])
        except ValueError as exc:
            refused = "REFUSED" in str(exc) and not seen
        return say(rc == 0 and built_once and refused, label, "built once and handed on %s, refused %s" % (built_once, refused))
    finally:
        engine.main, scoped_amgt._held_name_index = saved


def main():
    results = []
    rows = universe()
    plain = run(rows)
    results.append(say("710891" in tickers(plain), "E2 control: without an index the self row is a member", str(tickers(plain))))
    idx = {SELF_TOKEN: [SUBJ]}
    try:
        got = run(rows, held_name_index=idx)
        den = got.get("denominators") or {}
        named = any(isinstance(e, dict) and e.get("ticker") == "710891" for e in (den.get("self_excluded_by_identity") or []))
        counted = den.get("self_excluded") == (plain["denominators"]["self_excluded"] + 1)
        results.append(say("710891" not in tickers(got) and named and counted,
                           "E1 the self row is excluded, named and counted", "members %s, named %s, counted %s" % (tickers(got), named, counted)))
        amb = run(rows, held_name_index={SELF_TOKEN: [SUBJ, "OTHER_US_Equity"]})
        results.append(say("710891" in tickers(amb), "E3 control: a token naming two held companies excludes nothing"))
        oth = run(rows, held_name_index={SELF_TOKEN: ["OTHER_US_Equity"]})
        results.append(say("710891" in tickers(oth), "E4 control: a token naming another held company excludes nothing"))
        big = universe(extra_peers=13)
        withx = run(big, held_name_index=idx)
        results.append(say(len(withx["members"]) == 12 and "710891" not in tickers(withx) and "P00" in tickers(withx),
                           "E5 backfill: the set stays at 12 and the next ranked name takes the place",
                           "%d members, self present %s" % (len(withx["members"]), "710891" in tickers(withx))))
        empty = run(rows, held_name_index={})
        a, b = json.loads(json.dumps(plain, sort_keys=True)), json.loads(json.dumps(empty, sort_keys=True))
        a.pop("vintage", None)
        b.pop("vintage", None)
        results.append(say(a == b, "E6 control: an empty index leaves the result byte-equal"))
    except TypeError as exc:
        for label in ("E1 the self row is excluded, named and counted", "E3 control: a token naming two held companies excludes nothing",
                      "E4 control: a token naming another held company excludes nothing",
                      "E5 backfill: the set stays at 12 and the next ranked name takes the place",
                      "E6 control: an empty index leaves the result byte-equal"):
            results.append(say(False, label, "peers() takes no held_name_index: %s" % exc))
    results.append(say("held_name_index" in inspect.getsource(engine.run_batch) and "held_name_index" in inspect.getsource(engine.main),
                       "E7 wiring: run_batch and main take the held-name index and pass it (source level)"))
    results.append(e8())
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R93 SELF PEER: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
