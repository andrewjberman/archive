"""ADVI_FIRMBKTS round 4 check for cell FB-g-36 (the side-effect-free invocation events of the partners API Lambda, one per
served class its code reads through the seam; act 4c's object-level read), issuer 2.0.0_SA_COO~B1.

--arms census --file <path> [--root <tree>]  (4 arms)
  Q1 the JSON file exists and holds `entries`: a non-empty list; each entry has `class` (a registered LEGACY prefix of
     `platinum_destinations.json`), `event` (a non-empty JSON object), `handler`, `call_chain` (a list of "path:line"),
     `side_effects`, `invoke_recommended`, `source_of_event` ("path[:line]").
  Q2 every entry's `class` is one of the 11 registered legacy prefixes, no class appears twice, and the file's
     `classes_read_by_code` equals the set of entries' classes plus `classes_not_read` (a list, possibly empty): together
     the 11 registered prefixes, no overlap.
  Q3 every `call_chain` path exists in the tree under the Lambda's source directory and its last line holds the token
     `source(` or `list_target(` (a read through the seam); the first holds `lambda_handler`.
  Q4 every entry's `side_effects` is "none" with `invoke_recommended` true, or names the write with `invoke_recommended`
     false; at least one entry is invokable.
Plain ASCII output; the last line carries the arm count. READ-ONLY. Never edit this file.
"""
import argparse
import json
import os
import re
import subprocess
import sys

LAMBDA_DIR = "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data"
REG = "infra/logic/registry/platinum_destinations.json"


def _root(arg):
    if arg:
        return arg
    return subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def _line(root, ref):
    m = re.match(r"^(.*?):(\d+)$", str(ref))
    path, ln = (m.group(1), int(m.group(2))) if m else (str(ref), None)
    p = os.path.join(root, *path.split("/"))
    if not os.path.isfile(p):
        return None, None, path
    if ln is None:
        return True, None, path
    lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
    return True, (lines[ln - 1] if 0 < ln <= len(lines) else None), path


def census(root, file):
    res = []
    legacy = sorted({c["legacy_prefix"] for c in json.load(open(os.path.join(root, *REG.split("/")),
                                                                 encoding="utf-8"))["platinum_destinations"]})
    d = None
    try:
        d = json.load(open(file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("  file unreadable: %s" % type(e).__name__)
    ents = d.get("entries") if isinstance(d, dict) else None
    keys = ("class", "event", "handler", "call_chain", "side_effects", "invoke_recommended", "source_of_event")
    ok1 = isinstance(ents, list) and bool(ents) and all(
        isinstance(e, dict) and all(k in e for k in keys) and isinstance(e.get("event"), dict) and e["event"]
        and isinstance(e.get("call_chain"), list) and e["call_chain"] for e in ents)
    print("  Q1 entries=%d" % (len(ents) if isinstance(ents, list) else 0))
    res.append(("Q1 a non-empty entries list with every key", ok1))

    classes = [e.get("class") for e in (ents or []) if isinstance(e, dict)]
    nread = (d or {}).get("classes_not_read") if isinstance(d, dict) else None
    ok2 = (ok1 and len(set(classes)) == len(classes) and set(classes) <= set(legacy) and isinstance(nread, list)
           and set(nread) <= set(legacy) and not (set(nread) & set(classes)) and set(classes) | set(nread) == set(legacy))
    print("  Q2 classes covered=%d of %d registered; not read=%s" % (len(set(classes)), len(legacy),
                                                                     sorted(nread or [])[:11]))
    res.append(("Q2 the entries and the not-read list partition the 11 registered legacy prefixes", ok2))

    ok3 = ok1
    for e in ents or []:
        chain = e.get("call_chain") or []
        for i, ref in enumerate(chain):
            ex, txt, path = _line(root, ref)
            if not ex or txt is None or not path.startswith(LAMBDA_DIR):
                ok3 = False
                continue
            if i == 0 and "lambda_handler" not in txt:
                ok3 = False
            if i == len(chain) - 1 and not re.search(r"source\(|list_target\(", txt):
                ok3 = False
    print("  Q3 call chains verified: %s" % ok3)
    res.append(("Q3 each call chain is in the Lambda's directory and ends in a read through the seam", ok3))

    ok4 = ok1 and any(e.get("invoke_recommended") is True for e in ents) and all(
        (str(e.get("side_effects")).strip().lower() == "none") == (e.get("invoke_recommended") is True) for e in ents)
    res.append(("Q4 side effects and invoke_recommended agree; at least one entry is invokable", ok4))
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
    for n, ok in res:
        print("%s %s" % ("PASS" if ok else "FAIL", n))
    k = sum(1 for _, ok in res if ok)
    print("ROUND 4 PARTNERS EVENTS: %d of 4 arms" % k)
    sys.exit(0 if k == 4 else 1)


if __name__ == "__main__":
    main()
