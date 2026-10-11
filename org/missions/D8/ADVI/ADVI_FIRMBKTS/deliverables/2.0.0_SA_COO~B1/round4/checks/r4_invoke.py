"""ADVI_FIRMBKTS round 4 check for cell FB-g-29 (the invocation census for act 4's widened sample: one real post-flip
invocation per admitted principal that exercises the ownership read; the CTO's act 3b CTO half and act 4 ADDENDUM 2),
issuer 2.0.0_SA_COO~B1.

--arms census --file <path> [--root <tree>]  (4 arms)
  V1 the JSON file exists and holds exactly NINE entries: the eight IRPT consumers (irpt-49f-reporting-read-lambda,
     irpt-directory-search, irpt-export-render, irpt-holdings, irpt-narrative, irpt-performance-adapter, irpt-status,
     irpt-ycharts-generate) and the validator (auth-validator-edge), each once, each with the keys: function, kind,
     handler, event, reads_ownership, call_chain, side_effects, source_of_event, before_flip, after_flip.
  V2 each entry's `call_chain` is a list of "path:line" strings, every path exists in the tree and its line holds a token of
     the chain (`lambda_handler` for the first; `load_ownership` or the validator's ownership read for the last).
  V3 each `event` is a JSON object (never empty); `source_of_event` is a "path[:line]" whose file exists in the tree.
  V4 each entry's `side_effects` is one of "none" or a sentence naming the write; an entry whose side effects are not "none"
     carries `invoke_recommended` false. At least 7 of 9 entries are "none".
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys

NAMES = ["irpt-49f-reporting-read-lambda", "irpt-directory-search", "irpt-export-render", "irpt-holdings",
         "irpt-narrative", "irpt-performance-adapter", "irpt-status", "irpt-ycharts-generate", "auth-validator-edge"]
KEYS = ["function", "kind", "handler", "event", "reads_ownership", "call_chain", "side_effects", "source_of_event",
        "before_flip", "after_flip"]


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _line(root, ref):
    m = re.match(r"^(.*?):(\d+)$", ref)
    path, ln = (m.group(1), int(m.group(2))) if m else (ref, None)
    p = os.path.join(root, *path.split("/"))
    if not os.path.isfile(p):
        return False, None
    if ln is None:
        return True, None
    try:
        lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return False, None
    return (0 < ln <= len(lines)), (lines[ln - 1] if 0 < ln <= len(lines) else None)


def census(root, file):
    res = []
    data = None
    try:
        data = json.load(open(file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("  file unreadable: %s" % type(e).__name__)
    ents = data.get("entries") if isinstance(data, dict) else data
    ents = ents if isinstance(ents, list) else []
    got = sorted(e.get("function") for e in ents if isinstance(e, dict))
    ok1 = got == sorted(NAMES) and all(isinstance(e, dict) and all(k in e for k in KEYS) for e in ents)
    print("  V1 entries=%d functions=%s" % (len(ents), got))
    res.append(("V1 nine entries, the eight consumers and the validator, every key present", ok1))

    ok2 = bool(ents)
    for e in ents:
        chain = e.get("call_chain") or []
        if not chain or not isinstance(chain, list):
            ok2 = False
            continue
        for i, ref in enumerate(chain):
            exists, txt = _line(root, ref)
            if not exists or txt is None:
                ok2 = False
                continue
            if i == 0 and "lambda_handler" not in txt and "handler" not in txt:
                ok2 = False
            if i == len(chain) - 1 and not re.search(r"load_ownership|ownership", txt):
                ok2 = False
    print("  V2 call chains verified against the tree: %s" % ok2)
    res.append(("V2 every call-chain line exists in the tree and carries its chain token", ok2))

    ok3 = bool(ents)
    for e in ents:
        ev = e.get("event")
        src = str(e.get("source_of_event", ""))
        if not isinstance(ev, dict) or not ev:
            ok3 = False
        exists, _ = _line(root, src)
        if not exists:
            ok3 = False
    print("  V3 events are objects with an existing source: %s" % ok3)
    res.append(("V3 every event is a non-empty object whose source file exists", ok3))

    none = [e for e in ents if str(e.get("side_effects", "")).strip().lower() == "none"]
    ok4 = bool(ents) and len(none) >= 7 and all(
        e.get("invoke_recommended") is False for e in ents if str(e.get("side_effects", "")).strip().lower() != "none")
    print("  V4 side_effects none=%d of %d" % (len(none), len(ents)))
    res.append(("V4 at least seven entries have no side effect; a side-effecting one is not recommended", ok4))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", choices=("census",), required=True)
    ap.add_argument("--file", required=True)
    ap.add_argument("--root")
    a = ap.parse_args()
    root = _root(a.root)
    try:
        res = census(root, a.file if os.path.isabs(a.file) else os.path.join(root, a.file))
    except Exception as e:  # noqa: BLE001
        print("ABSENT or unreadable: (%s: %s)" % (type(e).__name__, str(e)[:160]))
        res = [("the census readable", False)]
    for name, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    n = sum(1 for _, ok in res if ok)
    print("ROUND 4 INVOKE CENSUS: %d of 4 arms" % n)
    sys.exit(0 if n == 4 else 1)


if __name__ == "__main__":
    main()
