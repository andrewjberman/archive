"""AR-y-492 offline check: the swap pass takes the proposals port and the classification extras.

Stdlib only; no network, no model, no AWS, nothing written. It loads swap_pass.py BY PATH from the worktree that holds
this file and runs eight in-process cases with fakes. `--selftest` rewrites the module text in memory three ways (the
literal empty proposals put back; classify not forwarded to choose_replacement; low_confidence fixed to False) and
prints CONTROL-FIRES only when every rewrite fails at least one case.
"""
import importlib.util
import json
import os
import sys
import types

sys.dont_write_bytecode = True
NAME = "swap_pass_under_check"
SOURCE_REL = os.path.join("infra", "aws", "lambda", "investor-reporting", "ycharts", "research", "swap_pass.py")
EQ = {"asset_class": "equity", "sub_asset_class": "USLargeCap"}
FI = {"asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"}
POOL_ROWS = [
    {"ticker": "AAA", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "BBB", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "CCC", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "DDD", "asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"},
    {"ticker": "EEE", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
]
HIST = {"AAA": 300, "BBB": 900, "CCC": 900, "DDD": 50, "EEE": 100, "NEWCO": 2000, "NEWFI": 3000}
MODEL_SOURCE = "kimi-k3 classification"
GOLDEN = {
    "rows": [{"ticker": "BBB", "amount": "40.25", "client_ticker": "Q"}, {"ticker": "AAA", "amount": "10"}],
    "swaps": [{
        "proxy_for": "Q", "proxy": "BBB", "status": "REPLACED", "method": "CLASS_LONGEST_YAHOO_HISTORY",
        "confidence": "CLASS_MATCH_PRICED", "low_confidence": False, "sources": ["etf-classifications pool snapshot"],
        "pool_as_of": "2026-09-01", "pool_claim": "held", "pool_stale": False, "candidates_priced": 4,
        "dropped_reasons": {}, "merged": False,
        "named": "Q is replaced by BBB (same asset class and sub asset class; longest Yahoo history, 900 days).",
        "history_days": 900,
    }],
}
# (label, exact text in swap_pass.py that must occur once, its replacement)
MUTATIONS = [
    ("literal-empty-proposals", "pool_rows, offered, history_days", "pool_rows, [], history_days"),
    ("classify-not-forwarded", "history_days, classify=port)", "history_days)"),
    ("low-confidence-literal", '"low_confidence": low,', '"low_confidence": False,'),
]


class Hist:
    """A history_days fake over a dict; a missing key answers None."""

    def __init__(self, table):
        self.table = table

    def __call__(self, ticker):
        return self.table.get(ticker)


class Classes:
    """A classify fake over a dict; a value that is an exception instance raises; every ask is kept."""

    def __init__(self, table):
        self.table = table
        self.asked = []

    def __call__(self, symbol):
        self.asked.append(symbol)
        answer = self.table.get(symbol)
        if isinstance(answer, Exception):
            raise answer
        return answer


def pool_of():
    return {"rows": [dict(row) for row in POOL_ROWS], "pool_as_of": "2026-09-01", "pool_claim": "held",
            "stale": False, "stale_days": 10}


def client(extra=None):
    table = {"Q": dict(EQ), "NEWCO": dict(EQ), "NEWFI": dict(FI), "DDD": dict(FI)}
    table.update(extra or {})
    return Classes(table)


def unresolved():
    return {"ticker": "Q", "amount": "40.25", "resolution": "UNRESOLVED"}


def case_proposal_wins(sp):
    out = sp.swap_holdings([unresolved()], pool_of(), classify=client(), history_days=Hist(HIST),
                           proposals=lambda symbol, classification: ["NEWCO"])
    base = sp.swap_holdings([unresolved()], pool_of(), classify=client(), history_days=Hist(HIST))
    record = out["swaps"][0]
    ok = (record["proxy"] == "NEWCO" and record["confidence"] == "CLASS_MATCH_PRICED_MODEL_PROPOSED"
          and out["rows"] == [{"ticker": "NEWCO", "amount": "40.25", "client_ticker": "Q"}]
          and base["swaps"][0]["proxy"] == "BBB")
    return ok, "proxy=%s base=%s" % (record["proxy"], base["swaps"][0]["proxy"])


def case_wrong_class_dropped(sp):
    out = sp.swap_holdings([unresolved()], pool_of(), classify=client(), history_days=Hist(HIST),
                           proposals=lambda symbol, classification: ["DDD"])
    record = out["swaps"][0]
    return (record["proxy"] == "BBB" and record["dropped_reasons"] == {"CLASS_MISMATCH": 1}), str(record["dropped_reasons"])


def case_outside_pool_class_checked(sp):
    classify = client({"BOOM": RuntimeError("down")})
    out = sp.swap_holdings([unresolved()], pool_of(), classify=classify, history_days=Hist(HIST),
                           proposals=lambda symbol, classification: ["NEWFI", "NEWCO", "BOOM"])
    record = out["swaps"][0]
    asked_ok = {"NEWFI", "NEWCO", "BOOM"} <= set(classify.asked)
    ok = (asked_ok and record["proxy"] == "NEWCO"
          and record["dropped_reasons"] == {"CLASS_MISMATCH": 1, "NOT_CLASSIFIED": 1})
    return ok, "proxy=%s dropped=%s" % (record["proxy"], record["dropped_reasons"])


def case_hostile_proposals(sp):
    def raising(symbol, classification):
        raise RuntimeError("proposals down")

    answers = [raising,
               lambda symbol, classification: "NEWCO",
               lambda symbol, classification: [5],
               lambda symbol, classification: ("NEWCO",),
               lambda symbol, classification: ["   ", None]]
    for answer in answers:
        out = sp.swap_holdings([unresolved()], pool_of(), classify=client(), history_days=Hist(HIST), proposals=answer)
        record = out["swaps"][0]
        if record["proxy"] != "BBB" or record["dropped_reasons"] != {}:
            return False, "proxy=%s dropped=%s" % (record["proxy"], record["dropped_reasons"])
    return True, "answers=%d" % len(answers)


def case_baseline_equal(sp):
    rows = [unresolved(), {"ticker": "AAA", "amount": "10"}]
    res = sp.swap_holdings(rows, pool_of(), classify=client(), history_days=Hist(HIST), proposals=None)
    return json.dumps(res, sort_keys=True) == json.dumps(GOLDEN, sort_keys=True), "golden=%d" % len(GOLDEN["swaps"])


def case_low_confidence_carried(sp):
    flagged = {"asset_class": "equity", "sub_asset_class": "USLargeCap", "confidence": 0.55,
               "low_confidence": True, "classified_by": "MODEL"}
    sure = dict(flagged, confidence=0.91, low_confidence=False)
    low = sp.swap_holdings([unresolved()], pool_of(), classify=Classes({"Q": flagged}), history_days=Hist(HIST))["swaps"][0]
    high = sp.swap_holdings([unresolved()], pool_of(), classify=Classes({"Q": sure}), history_days=Hist(HIST))["swaps"][0]
    ok = (low["low_confidence"] is True and low["classified_by"] == "MODEL"
          and low["sources"] == ["etf-classifications pool snapshot", MODEL_SOURCE]
          and high["low_confidence"] is False and high["classified_by"] == "MODEL")
    return ok, "low=%s high=%s" % (low["low_confidence"], high["low_confidence"])


def case_amount_kept(sp):
    out = sp.swap_holdings([unresolved()], pool_of(), classify=client(), history_days=Hist(HIST),
                           proposals=lambda symbol, classification: ["NEWCO"])
    return out["rows"] == [{"ticker": "NEWCO", "amount": "40.25", "client_ticker": "Q"}], "rows=%d" % len(out["rows"])


def case_deterministic(sp):
    def run():
        return sp.swap_holdings([unresolved()], pool_of(), classify=client({"Y": dict(FI)}), history_days=Hist(HIST),
                                proposals=lambda symbol, classification: ["NEWCO", "NEWFI", "DDD"])

    return json.dumps(run(), sort_keys=True) == json.dumps(run(), sort_keys=True), "twice"


CASES = [
    ("proposal_wins", case_proposal_wins),
    ("wrong_class_dropped", case_wrong_class_dropped),
    ("outside_pool_class_checked", case_outside_pool_class_checked),
    ("hostile_proposals", case_hostile_proposals),
    ("baseline_equal", case_baseline_equal),
    ("low_confidence_carried", case_low_confidence_carried),
    ("amount_kept", case_amount_kept),
    ("deterministic", case_deterministic),
]


def run_cases(sp):
    results = []
    for name, func in CASES:
        try:
            ok, detail = func(sp)
        except Exception as exc:
            ok, detail = False, "raised %s" % type(exc).__name__
        results.append((name, bool(ok), detail))
    return results


def find_root(start):
    """The nearest directory above `start` that holds both .tools and infra: the worktree root."""
    here = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(here, ".tools")) and os.path.isdir(os.path.join(here, "infra")):
            return here
        parent = os.path.dirname(here)
        if parent == here:
            return None
        here = parent


def read_source(path):
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def make_module(text, path):
    module = types.ModuleType(NAME)
    module.__file__ = path
    exec(compile(text, path, "exec"), module.__dict__)
    return module


def load_by_path(path):
    spec = importlib.util.spec_from_file_location(NAME, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def yes(results, names):
    passed = {name: ok for name, ok, _ in results}
    return "yes" if all(passed.get(name) for name in names) else "no"


def main(argv):
    root = find_root(os.path.dirname(os.path.abspath(__file__)))
    if root is None:
        print("SWAP-PASS-PORTS-BAD no worktree root above the check")
        return 1
    path = os.path.join(root, SOURCE_REL)
    verbose = "--verbose" in argv
    if "--selftest" in argv:
        text = read_source(path)
        fired = []
        for label, old, new in MUTATIONS:
            count = text.count(old)
            if count != 1:
                if verbose:
                    sys.stderr.write("MUTATION %s not applied (anchor count %d)\n" % (label, count))
                print("CONTROL-DID-NOT-FIRE")
                return 1
            results = run_cases(make_module(text.replace(old, new), path))
            bad = [name for name, ok, _ in results if not ok]
            if verbose:
                sys.stderr.write("MUTATION %s failed %s\n" % (label, ",".join(bad) or "none"))
            fired.append(bool(bad))
        if all(fired):
            print("CONTROL-FIRES")
            return 0
        print("CONTROL-DID-NOT-FIRE")
        return 1
    results = run_cases(load_by_path(path))
    failed = [name for name, ok, _ in results if not ok]
    if verbose:
        for name, ok, detail in results:
            sys.stderr.write("CASE %s %s %s\n" % (name, "pass" if ok else "FAIL", detail))
    if failed:
        print("SWAP-PASS-PORTS-BAD " + ",".join(failed))
        return 1
    print("SWAP-PASS-PORTS-OK cases=%d proposals_forwarded=%s classify_forwarded=%s low_conf_carried=%s baseline_equal=%s"
          % (len(results), yes(results, ["proposal_wins", "wrong_class_dropped"]),
             yes(results, ["outside_pool_class_checked"]), yes(results, ["low_confidence_carried"]),
             yes(results, ["baseline_equal"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
