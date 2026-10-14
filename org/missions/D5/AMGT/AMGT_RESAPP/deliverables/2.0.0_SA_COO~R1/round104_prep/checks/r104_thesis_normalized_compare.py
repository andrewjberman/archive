"""AMGT_RESAPP round-104 PREP -- `AMGT-bk-2`'s pair: the WHOLE /thesis body of the pin against the live function, with the PE_RATIO rows set aside.

  PYTHONPATH=<the pin's worktree> python r104_thesis_normalized_compare.py <out.json> [--workers 4]

`r98_thesis_fullbody_compare.py` diffs by list INDEX, so a withheld P/E row (one list element fewer) shifts every later index and reads as a quarter of a million changed paths. This reads the same two bodies per
resolved name (the live function; the checkout's own handler on the same pool) and:
    1. removes, in BOTH bodies and at every depth, each list element that is a figure row of mnemonic PE_RATIO (the figures lists, top-level and under `model`), each `fiscal_unresolved` entry of
       mnemonic PE_RATIO, and each `check_face` row whose `figure_id` is `fiscal_year_line_item:PE_RATIO:<year>` (the check face follows the SERVED figure: its value and basis text change with the
       row, and a withheld row's check row goes with it); counts them (served rows before and after, withheld entries added, check rows before and after);
    2. checks `model.fiscal_row_count` equals the length of the post `model.fiscal_year_figures` (the one count the derivation legitimately changes), then drops it from the diff;
    3. diffs what remains path by path, classing `.model.team_sheet` paths, request clocks, float representation (the measuring runtime's), and OTHER.
Prints `thesis names <n> | PE rows live <a> served <b> withheld <c> | remaining changed paths <k> {kinds}` and `R104 THESIS NORMALIZED: YES|NO` (YES: 0 `other` and 0 `team_sheet`, every status 200 and 200,
every name's row count equal). Writes nothing but <out.json>.
"""
import concurrent.futures
import contextlib
import io
import json
import re
import sys

import boto3

sys.path.insert(0, ".")
from lib.research.api import scoped_amgt as m  # noqa: E402
from lib.research.corpus import dossier  # noqa: E402
from lib.research.harvest import store  # noqa: E402

CLOCK = re.compile(r"(read_at|fetched_at|generated_at|served_at|_clock|elapsed|duration|request_id|latency|as_of_read)", re.I)
_LAM = boto3.client("lambda", region_name="us-east-1")


def event(key):
    return {"rawPath": "/api/scoped/amgt/security/%s/thesis" % key, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def live(key):
    r = json.loads(_LAM.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event(key)).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def local(key):
    with contextlib.redirect_stdout(io.StringIO()):
        r = m.handler(event(key))
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def strip(node, counts):
    """Remove PE_RATIO figure rows and PE_RATIO unresolved entries at every depth; count them."""
    if isinstance(node, dict):
        return {k: strip(v, counts) for k, v in node.items()}
    if isinstance(node, list):
        out = []
        for item in node:
            if isinstance(item, dict) and item.get("mnemonic") == "PE_RATIO":
                counts["rows" if "value" in item else "unresolved"] += 1
                continue
            if isinstance(item, dict) and str(item.get("figure_id", "")).startswith("fiscal_year_line_item:PE_RATIO:"):
                counts["check"] += 1
                continue
            out.append(strip(item, counts))
        return out
    return node


def walk(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            yield from walk(a.get(k, "<absent>"), b.get(k, "<absent>"), "%s.%s" % (path, k))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            yield path + ".<length>", len(a), len(b)
        for i, (x, y) in enumerate(zip(a, b)):
            yield from walk(x, y, "%s[%d]" % (path, i))
    elif a != b:
        yield path, a, b


def same_number(a, b):
    try:
        x, y = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return abs(x - y) <= 1e-9 * max(1.0, abs(x), abs(y))


def one(key):
    (sb, b), (sa, a) = live(key), local(key)
    cb, ca = {"rows": 0, "unresolved": 0, "check": 0}, {"rows": 0, "unresolved": 0, "check": 0}
    nb, na = strip(b, cb), strip(a, ca)
    count_ok = (a.get("model") or {}).get("fiscal_row_count") == len((a.get("model") or {}).get("fiscal_year_figures") or [])
    for body in (nb, na):
        if isinstance(body.get("model"), dict):
            body["model"].pop("fiscal_row_count", None)
    out = []
    for p, before, after in walk(nb, na):
        kind = "team_sheet" if p.startswith(".model.team_sheet") else "clock" if CLOCK.search(p) else "float_repr" if same_number(before, after) else "other"
        out.append({"key": key, "path": p, "before": before, "after": after, "kind": kind})
    return {"key": key, "status": (sb, sa), "live_rows": cb["rows"], "post_rows": ca["rows"], "post_unresolved": ca["unresolved"], "live_unresolved": cb["unresolved"], "live_check": cb["check"], "post_check": ca["check"], "count_ok": count_ok, "diffs": out}


def main():
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 4
    real_stdout = sys.stdout
    keys = sorted(dossier._resolved_security_keys(client=store._default_client()))
    res, failed = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(one, k): k for k in keys}
        for fut in concurrent.futures.as_completed(futs):
            try:
                res.append(fut.result())
            except Exception as exc:  # a failed name is counted and named, never dropped
                failed.append("%s: %s %s" % (futs[fut], type(exc).__name__, str(exc)[:80]))
    sys.stdout = real_stdout
    res.sort(key=lambda r: r["key"])
    json.dump({"results": res, "failed": failed}, open(sys.argv[1], "w", encoding="utf-8"), default=str)
    kinds = {}
    for r in res:
        for d in r["diffs"]:
            kinds[d["kind"]] = kinds.get(d["kind"], 0) + 1
    live_rows, post_rows = sum(r["live_rows"] for r in res), sum(r["post_rows"] for r in res)
    withheld = sum(r["post_unresolved"] - r["live_unresolved"] for r in res)
    bad_status = [r["key"] for r in res if r["status"] != (200, 200)]
    bad_count = [r["key"] for r in res if not r["count_ok"]]
    print("thesis names %d | failed %d | PE rows live %d post %d | PE unresolved entries added %d | PE check-face rows live %d post %d | remaining changed paths %d %s" % (
        len(res), len(failed), live_rows, post_rows, withheld, sum(r["live_check"] for r in res), sum(r["post_check"] for r in res), sum(kinds.values()), kinds))
    for r in res:
        for d in r["diffs"]:
            if d["kind"] in ("other", "team_sheet"):
                print("  %-8s %s %s %r -> %r" % (d["kind"], d["key"], d["path"][:70], str(d["before"])[:40], str(d["after"])[:40]))
                break
    print("status not (200, 200): %s | fiscal_row_count not equal to the figures length: %s" % (bad_status[:5], bad_count[:5]))
    ok = not failed and not bad_status and not bad_count and not kinds.get("other") and not kinds.get("team_sheet")
    print("R104 THESIS NORMALIZED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
