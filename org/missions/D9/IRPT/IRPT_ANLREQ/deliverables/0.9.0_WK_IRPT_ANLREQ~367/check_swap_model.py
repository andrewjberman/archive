"""IRPT_ANLREQ AR-y-493 check: the swap model adapter run in-process, offline, over eight cases with a fake send.

Usage: python -I check_swap_model.py            prints one SWAP-MODEL-OK or SWAP-MODEL-BAD line (rc 0 or 1)
       python -I check_swap_model.py --selftest prints CONTROL-FIRES only when all three mutants of the module text read BAD

No network, no secret, no model call: every send is a fake that records its payloads. Stdlib only.
"""
import json
import os
import sys
import types

MODULE_REL = os.path.join("infra", "aws", "lambda", "investor-reporting", "ycharts", "research", "swap_model.py")
SHARED_REL = os.path.join("infra", "aws", "lambda", "v2_portal", "_shared")

POOL = [
    {"ticker": "SPY", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
    {"ticker": "SGOV", "asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"},
    {"ticker": "HDGE", "asset_class": "alternatives", "sub_asset_class": "HedgeFund"},
    {"ticker": "CNIN", "asset_class": "crypto", "sub_asset_class": "Coin"},
]

# (anchor, replacement) in the module text: each must occur exactly once or the control cannot be applied.
MUTANTS = [
    ("vocabulary check removed", "if pair_key not in pool_pairs:", "if False:"),
    ("threshold compare flipped to <=", '"low_confidence": confidence < threshold,',
     '"low_confidence": confidence <= threshold,'),
    ("proposals cap removed", "return out[:max_proposals]", "return out"),
]


def _repo_root():
    cur = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(cur, MODULE_REL)):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def _load_classifier(root):
    sys.path.insert(0, os.path.join(root, SHARED_REL))
    import etf_classification_model
    return etf_classification_model


def _load_module_text(path, text):
    mod = types.ModuleType("swap_model_under_test")
    mod.__file__ = path
    exec(compile(text, path, "exec"), mod.__dict__)
    return mod


def _recorder(*replies):
    payloads = []

    def send(payload, timeout_seconds):
        payloads.append(payload)
        item = replies[min(len(payloads), len(replies)) - 1]
        if isinstance(item, BaseException):
            raise item
        return item
    return send, payloads


def _chat(content, finish="stop"):
    return {"choices": [{"finish_reason": finish, "message": {"content": content}}]}


def _answer(asset, sub, conf):
    return _chat(json.dumps({"asset_class": asset, "sub_asset_class": sub, "confidence": conf, "reason": "etf"}))


def _split(prompt):
    instruction, data_text = prompt.rsplit("\n", 1)
    return instruction, json.loads(data_text)


def run_battery(make_swap_model, ecm):
    """The eight cases. Returns ({case_number: bool}, first failure reason or None)."""
    results = {}
    reasons = []

    def build(send):
        return make_swap_model(POOL, send, model_module=ecm, api_key="k")

    def case(number, check):
        try:
            ok, why = check()
        except Exception as exc:  # noqa: BLE001 - a raising path is a failed case, reported with its type
            ok, why = False, "raised %s" % type(exc).__name__
        results[number] = bool(ok)
        if not ok:
            reasons.append("case%d %s" % (number, why))

    def c1():
        send, _sent = _recorder(_answer("equity", "uslargecap", 0.93))
        got = build(send).classify("ZQXV")
        want = {"asset_class": "equity", "sub_asset_class": "USLargeCap", "confidence": 0.93,
                "low_confidence": False, "classified_by": "MODEL"}
        return got == want, "mapping %r" % (got,)

    def c2():
        send, _sent = _recorder(_answer("equity", "Crypto", 0.95))
        got = build(send).classify("ZQXV")
        return got is None, "out-of-vocabulary sub-class answered %r" % (got,)

    def c3():
        send, _sent = _recorder(_answer("crypto", "Coin", 0.95))
        got = build(send).classify("ZQXV")
        return got is None, "class outside the six answered %r" % (got,)

    def c4():
        send, _sent = _recorder(_answer("fixed_income", "UltraShortDuration", 0.79))
        got = build(send).classify("ZQXV")
        return isinstance(got, dict) and got["low_confidence"] is True, "0.79 gave %r" % (got,)

    def c5():
        send, _sent = _recorder(_answer("fixed_income", "UltraShortDuration", 0.80))
        got = build(send).classify("ZQXV")
        return isinstance(got, dict) and got["low_confidence"] is False, "0.80 gave %r" % (got,)

    def c6():
        listed = ["toolongticker1", "a b", "  ", 7, "IVV", "spy", "ZQXV", "zqxv", "BRK.B", "QQQ", "VTI", "VOO", "SCHD",
                  "ivv"]
        send, _sent = _recorder(_chat(json.dumps({"tickers": listed})))
        got = build(send).propose("ZQXV", {"asset_class": "equity", "sub_asset_class": "USLargeCap"})
        want = ["IVV", "SPY", "BRK.B", "QQQ", "VTI"]
        return got == want, "filtered list %r" % (got,)

    def c7():
        cls = {"asset_class": "equity", "sub_asset_class": "USLargeCap"}
        failures = [
            _recorder(RuntimeError("boom"))[0],
            _recorder(_chat("not json"))[0],
            _recorder(_chat(json.dumps({"tickers": "IVV"})))[0],
            _recorder(_chat(json.dumps({"tickers": ["IVV"]}), finish="length"))[0],
        ]
        got = [build(send).propose("ZQXV", cls) for send in failures]
        return all(item == [] for item in got), "failure answers %r" % (got,)

    def c8():
        send, sent = _recorder(_answer("equity", "USLargeCap", 0.9))
        model = build(send)
        first = model.classify("zqxv")
        second = model.classify("ZQXV")
        blank = model.classify("   ")
        model.propose("ZQXV", {"asset_class": "equity", "sub_asset_class": "USLargeCap"})
        if first is None or second != first or blank is not None or len(sent) != 2:
            return False, "calls=%d first=%r" % (len(sent), first)
        for payload in sent:
            if set(payload) != {"model", "temperature", "max_tokens", "messages"} or payload["model"] != ecm.MODEL:
                return False, "payload shape"
        classify_instruction, classify_data = _split(sent[0]["messages"][0]["content"])
        propose_instruction, propose_data = _split(sent[1]["messages"][0]["content"])
        if classify_data != {"name": None, "ticker": "ZQXV"} or "ZQXV" in classify_instruction:
            return False, "classify payload carries more than the symbol"
        if propose_data.get("security") != "ZQXV" or "ZQXV" in propose_instruction:
            return False, "propose payload places the symbol outside the data object"
        for word in ("firm", "amount", "account", "client", "holding"):
            if word in json.dumps(propose_data) or word in json.dumps(classify_data):
                return False, "client-shaped word in a data object"
        return True, "ok"

    for number, fn in enumerate([c1, c2, c3, c4, c5, c6, c7, c8], start=1):
        case(number, fn)
    return results, (reasons[0] if reasons else None)


def _flags(results):
    return {
        "vocab_bound": results.get(2, False),
        "never_coerced": results.get(2, False) and results.get(3, False),
        "flag_at_0.80": results.get(4, False) and results.get(5, False),
        "proposals_filtered": results.get(6, False) and results.get(7, False),
        "symbol_only": results.get(8, False),
    }


def main():
    root = _repo_root()
    if root is None:
        print("SWAP-MODEL-BAD repo root not found")
        return 1
    ecm = _load_classifier(root)
    path = os.path.join(root, MODULE_REL)
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    module = _load_module_text(path, text)
    results, why = run_battery(module.make_swap_model, ecm)
    if why is not None or len(results) != 8:
        print("SWAP-MODEL-BAD %s" % (why or "cases=%d" % len(results)))
        return 1
    flags = _flags(results)
    if not all(flags.values()):
        print("SWAP-MODEL-BAD flags %s" % ",".join(sorted(k for k, v in flags.items() if not v)))
        return 1
    print("SWAP-MODEL-OK cases=8 vocab_bound=yes never_coerced=yes flag_at_0.80=yes proposals_filtered=yes "
          "symbol_only=yes")
    return 0


def selftest():
    root = _repo_root()
    if root is None:
        print("CONTROL-MISSED repo root not found")
        return 1
    ecm = _load_classifier(root)
    path = os.path.join(root, MODULE_REL)
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    baseline, why = run_battery(_load_module_text(path, text).make_swap_model, ecm)
    if why is not None:
        print("CONTROL-MISSED baseline %s" % why)
        return 1
    readings = []
    for name, anchor, replacement in MUTANTS:
        if text.count(anchor) != 1:
            print("CONTROL-MISSED anchor count %d for %s" % (text.count(anchor), name))
            return 1
        mutated = text.replace(anchor, replacement)
        results, _why = run_battery(_load_module_text(path, mutated).make_swap_model, ecm)
        readings.append((name, not all(results.get(number, False) for number in range(1, 9))))
    if all(bad for _name, bad in readings):
        print("CONTROL-FIRES")
        return 0
    for name, bad in readings:
        if not bad:
            sys.stderr.write("control read as passing: %s\n" % name)
    print("CONTROL-MISSED")
    return 1


if __name__ == "__main__":
    ARGS = sys.argv[1:]
    if ARGS == []:
        sys.exit(main())
    if ARGS == ["--selftest"]:
        sys.exit(selftest())
    print("SWAP-MODEL-BAD usage: [--selftest]")
    sys.exit(1)
