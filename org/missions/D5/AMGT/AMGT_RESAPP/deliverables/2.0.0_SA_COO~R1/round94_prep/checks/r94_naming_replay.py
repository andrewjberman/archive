"""AMGT_RESAPP round-94 PREP -- the builder replay for the ff-4 redeploy: `lib/opal_naming.py` changed since the live pin (another project's change: LGIC /
FIRMBKTS, +188 -11) and the function reaches it at request time (`corpus.dossier` -> `harvest.store` -> `naming.address` / `naming.key`).

  PYTHONPATH=<repo root> python r94_naming_replay.py [--pin 6a6c5c49d0]

RECORD: the checkout's own `lib.opal_naming` `address`, `key` and `name` are wrapped, and the handler serves overlay, thesis and peers for a fixed set of subjects plus
the four ranked lists and a rank timeseries; every builder call's arguments and result are logged. REPLAY: the pin's `lib/opal_naming.py` and `infra/logic/registry`
(extracted by `git show` into a temp root, so its registry is the pin's own) is loaded under another module name and called with the SAME arguments. Verdict:
    P1 the function's reads exercised the builder at least once, and the distinct calls are counted and printed;
    P2 every replayed call returns the SAME string at the pin as at the checkout (the count of differing calls is 0).
A call the pin's builder refuses (raises) is a DIFFERENCE, printed. Read-only: S3 GETs and DynamoDB reads by the handler, as the table scripts do.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

SUBJECTS = ("SAN_FP_Equity", "CSL_AU_Equity", "ASML_NA_Equity", "SAP_GY_Equity", "BA_US_Equity", "ROG_SW_Equity", "TSM_US_Equity", "IMB_LN_Equity",
            "BABA_US_Equity", "AZN_LN_Equity")


def git_show(ref, path):
    out = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True, check=False)
    if out.returncode != 0:
        raise RuntimeError("git show %s:%s failed" % (ref, path))
    return out.stdout


def load_pin(pin):
    root = tempfile.mkdtemp(prefix="r94_pin_naming_")
    files = subprocess.run(["git", "ls-tree", "-r", "--name-only", pin, "--", "infra/logic/registry"], capture_output=True, text=True).stdout.split()
    for path in ["lib/opal_naming.py", "org/standards/NAMING_SCHEMA.json", "org/missions/DIRECTIVES.yaml"] + files:
        dest = os.path.join(root, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            data = git_show(pin, path)
        except RuntimeError:
            continue  # a file the pin did not carry is simply absent in the temp root, as it was in the package
        with open(dest, "wb") as fh:
            fh.write(data)
    spec = importlib.util.spec_from_file_location("pin_opal_naming", os.path.join(root, "lib", "opal_naming.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, root, len(files)


def main():
    pin = sys.argv[sys.argv.index("--pin") + 1] if "--pin" in sys.argv else "6a6c5c49d0"
    import lib.opal_naming as naming
    from lib.research.api import scoped_amgt

    calls = []
    originals = {}
    for fn in ("address", "key", "name"):
        originals[fn] = getattr(naming, fn)

        def wrap(*a, _fn=fn, **kw):
            try:
                res = originals[_fn](*a, **kw)
            except Exception as exc:  # noqa: BLE001 -- recorded, then re-raised to the caller
                calls.append((_fn, a, kw, "RAISED %s" % type(exc).__name__))
                raise
            calls.append((_fn, a, kw, res))
            return res
        setattr(naming, fn, wrap)
    try:
        def serve(path, query=None):
            ev = {"rawPath": "/api/scoped/amgt" + path, "queryStringParameters": query, "requestContext": {"http": {"method": "GET"}},
                  "headers": {"x-firm-id": "opal"}}
            return scoped_amgt.handler(ev).get("statusCode")
        statuses = []
        for key in SUBJECTS:
            for leaf in ("overlay", "thesis", "peers"):
                statuses.append(serve("/security/%s/%s" % (key, leaf)))
        for movement in scoped_amgt.MOVEMENTS:
            for subject in scoped_amgt.SUBJECTS:
                statuses.append(serve("/lead-panel/rankings/%s/%s" % (movement, subject)))
        statuses.append(serve("/lead-panel/timeseries/TRENDING/PRICE", {"tickers": "SAN FP,BA US"}))
    finally:
        for fn, orig in originals.items():
            setattr(naming, fn, orig)
    distinct = {}
    for fn, a, kw, res in calls:
        distinct[(fn, repr(a), repr(sorted(kw.items())))] = (fn, a, kw, res)
    pin_mod, root, nreg = load_pin(pin)
    differing = []
    for _k, (fn, a, kw, res) in distinct.items():
        try:
            at_pin = getattr(pin_mod, fn)(*a, **kw)
        except Exception as exc:  # noqa: BLE001 -- a refusal at the pin is a difference
            at_pin = "RAISED %s" % type(exc).__name__
        if at_pin != res:
            differing.append((fn, a, kw, res, at_pin))
    print("   served %d requests (statuses %s) | builder calls %d, distinct %d | pin %s registry files %d (temp root %s)" % (
        len(statuses), json.dumps(sorted(set(str(s) for s in statuses))), len(calls), len(distinct), pin, nreg, root))
    by_fn = {}
    for fn, _a, _kw, _r in distinct.values():
        by_fn[fn] = by_fn.get(fn, 0) + 1
    print("   distinct calls by builder: %s" % json.dumps(by_fn, sort_keys=True))
    for fn, a, kw, res, at_pin in differing[:20]:
        print("   DIFFERENT %s%r %r: checkout=%r pin=%r" % (fn, a, kw, res, at_pin))
    p1 = len(distinct) > 0
    p2 = p1 and not differing
    print("%s P1 the function's reads exercised the builder (%d distinct calls)" % ("PASS" if p1 else "FAIL", len(distinct)))
    print("%s P2 every replayed call returns the same string at the pin (%d differ)" % ("PASS" if p2 else "FAIL", len(differing)))
    print("R94 NAMING REPLAY: %s" % ("YES" if p2 else "NO"))
    return 0 if p2 else 1


if __name__ == "__main__":
    sys.exit(main())
