"""AR-y-497 check: the swap record carries the class pair and the model confidence for MODEL rows only, and a
low-confidence model replacement's named text ends with the one plain sentence. Stdlib only; offline; fakes only.

It imports swap_pass BY PATH from the worktree this file sits in and runs seven in-process cases. --selftest rewrites the
module text in memory four ways; CONTROL-FIRES prints only when all four read BAD.
Run: python -I org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~369/check_swap_record_class.py [--selftest]
"""
import importlib.util
from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[7]
SWAP_PASS = ROOT / "infra" / "aws" / "lambda" / "investor-reporting" / "ycharts" / "research" / "swap_pass.py"
FLAGS = ("model_rows_carry_class", "model_confidence_float", "other_rows_unchanged", "low_conf_sentence")
PLAIN = "Q is replaced by BBB (same asset class and sub asset class; longest Yahoo history, 900 days)."
LOW = "Q was replaced by BBB on a low-confidence match; review before relying on it."
STALE = " The replacement pool was built on 2026-09-01, 44 days before this run, which is older than 30 days."
NOT_ANALYSED = "Q is not analysed; Opal Staff will manage the replacement."
NEW_KEYS = ("asset_class", "sub_asset_class", "model_confidence")
OLD_KEYS = {"proxy_for", "proxy", "status", "method", "confidence", "low_confidence", "sources", "pool_as_of",
            "pool_claim", "pool_stale", "candidates_priced", "dropped_reasons", "merged", "named", "history_days"}
UNRES = {"ticker": "Q", "amount": "40.25", "resolution": "UNRESOLVED"}
POOL_ROWS = [
    {"ticker": "AAA", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "BBB", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "CCC", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "EEE", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
]
HIST = {"AAA": 300, "BBB": 900, "CCC": 900, "EEE": 100}
MUTANTS = (
    ("model_confidence_copy_removed", 'record["model_confidence"] = confidence', "pass"),
    ("three_keys_on_every_record",
     '    if model:\n        record["classified_by"] = MODEL',
     '    record["asset_class"] = (classification or {}).get("asset_class")\n'
     '    record["sub_asset_class"] = (classification or {}).get("sub_asset_class")\n'
     '    record["model_confidence"] = (classification or {}).get("confidence")\n'
     '    if model:\n        record["classified_by"] = MODEL'),
    ("sub_asset_class_dropped", 'record["sub_asset_class"] = classification["sub_asset_class"]', "pass"),
    ("low_confidence_sentence_removed",
     'named = named + " " + LOW_CONFIDENCE_SENTENCE % (symbol, answer["replacement"])', "pass"),
)


def pool(stale):
    """A pool dict shaped as load_pool returns it; stale=True dates it 44 days before the run."""
    return {"rows": POOL_ROWS, "pool_as_of": "2026-09-01", "pool_claim": "held", "rows_count": len(POOL_ROWS),
            "stale_days": 44 if stale else 10, "stale": stale}


def history(ticker):
    return HIST.get(ticker)


def model(confidence, low):
    return {"asset_class": "equity", "sub_asset_class": "USLargeCap", "classified_by": "MODEL",
            "confidence": confidence, "low_confidence": low}


def one(mod, fresh, answer):
    """The one record of a swap pass over the client's UNRES row, its classify answering `answer` for any symbol."""
    out = mod.swap_holdings([dict(UNRES)], fresh, classify=lambda symbol: answer, history_days=history)
    return out["swaps"][0]


def is_model_class(record):
    return (record.get("asset_class") == "equity" and record.get("sub_asset_class") == "USLargeCap"
            and record.get("classified_by") == "MODEL")


def run_cases(mod):
    """The seven cases. Returns the list of failed flags with a label; an empty list means every flag holds."""
    failures = []

    def check(flag, ok, label):
        if not ok:
            failures.append("%s:%s" % (flag, label))

    fresh = pool(False)
    rec1 = one(mod, fresh, model(0.91, False))
    check("model_rows_carry_class", is_model_class(rec1), "C1")
    check("model_confidence_float", type(rec1.get("model_confidence")) is float and rec1["model_confidence"] == 0.91, "C1")
    check("low_conf_sentence", rec1.get("named") == PLAIN, "C1")

    rec2 = one(mod, fresh, model(0.8, True))
    check("model_rows_carry_class", is_model_class(rec2), "C2")
    check("model_confidence_float", type(rec2.get("model_confidence")) is float and rec2["model_confidence"] == 0.8, "C2")
    check("low_conf_sentence", rec2.get("named") == PLAIN + " " + LOW, "C2")

    rec3 = one(mod, fresh, model(True, False))
    check("model_rows_carry_class", is_model_class(rec3), "C3")
    check("model_confidence_float", "model_confidence" not in rec3, "C3")

    rec4 = one(mod, fresh, model(1.2, False))
    check("model_rows_carry_class", is_model_class(rec4), "C4")
    check("model_confidence_float", "model_confidence" not in rec4, "C4")
    check("low_conf_sentence", rec4.get("named") == PLAIN, "C4")

    rec5 = one(mod, fresh, {"asset_class": "equity", "sub_asset_class": "USLargeCap"})
    check("other_rows_unchanged", set(rec5) == OLD_KEYS and rec5.get("named") == PLAIN, "C5")

    rec6 = one(mod, fresh, None)
    check("other_rows_unchanged", rec6.get("status") != "REPLACED" and rec6.get("named") == NOT_ANALYSED
          and not (set(rec6) & set(NEW_KEYS)) and "classified_by" not in rec6, "C6")

    rec7 = one(mod, pool(True), model(0.8, True))
    check("model_rows_carry_class", is_model_class(rec7), "C7")
    check("low_conf_sentence", rec7.get("named") == PLAIN + STALE + " " + LOW, "C7")
    return failures


def load_real():
    spec = importlib.util.spec_from_file_location("swap_pass_under_check", str(SWAP_PASS))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_text(text):
    mod = types.ModuleType("swap_pass_mutant")
    mod.__file__ = str(SWAP_PASS)
    exec(compile(text, str(SWAP_PASS), "exec"), mod.__dict__)
    return mod


def main(argv):
    if "--selftest" in argv:
        source = SWAP_PASS.read_text(encoding="utf-8")
        read_bad = []
        for name, anchor, replacement in MUTANTS:
            if source.count(anchor) != 1:
                sys.stderr.write("SELFTEST %s anchor-count=%d (not applied)\n" % (name, source.count(anchor)))
                continue
            try:
                failures = run_cases(load_text(source.replace(anchor, replacement, 1)))
            except Exception as exc:  # a mutant that breaks the module reads BAD too
                failures = ["raised:%s" % type(exc).__name__]
            sys.stderr.write("SELFTEST %s read=%s %s\n" % (name, "BAD" if failures else "OK", failures[:3]))
            if failures:
                read_bad.append(name)
        if len(read_bad) == len(MUTANTS):
            print("CONTROL-FIRES")
            return 0
        sys.stderr.write("CONTROL-DOES-NOT-FIRE read_bad=%s\n" % ",".join(read_bad))
        return 1
    try:
        failures = run_cases(load_real())
    except Exception as exc:
        print("SWAP-RECORD-CLASS-BAD import_or_run:%s" % type(exc).__name__)
        return 1
    if failures:
        print("SWAP-RECORD-CLASS-BAD " + "; ".join(failures))
        return 1
    print("SWAP-RECORD-CLASS-OK cases=7 model_rows_carry_class=yes model_confidence_float=yes "
          "other_rows_unchanged=yes low_conf_sentence=yes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
