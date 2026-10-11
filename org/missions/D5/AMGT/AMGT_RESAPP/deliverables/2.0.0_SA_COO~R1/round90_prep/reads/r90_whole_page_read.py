"""AMGT_RESAPP round 90, AMGT-oo-1 -- the whole-page read for FWD-8 and FWD-38 (issuer act, read-only).

  PYTHONPATH=<repo root> python r90_whole_page_read.py <out.md> <SECURITY_KEY> [<SECURITY_KEY> ...]

Reads the LIVE function `opal-amgt-scoped-api` (Lambda invoke, GET only, nothing written) for each name's /thesis and /peers
route, which together carry every figure the Security Analysis page prints for the company and its comparison block.
  FWD-8  every peer row's identity agrees with the header company's comparison basis;
  FWD-38 every dated figure carries a vintage within one trading day of the header's.
Every denominator is printed beside its count. The trading-day distance is lib/trading_calendar.trading_days_behind.
"""
import collections
import json
import re
import sys

import boto3

from lib import trading_calendar as tc
from lib.research.api import scoped_amgt
from lib.research.identity import crosswalk
from lib.research.peers import numeric_tickers

FN = "opal-amgt-scoped-api"
PREFIX = "/api/scoped/amgt"
_LAM = boto3.client("lambda", region_name="us-east-1")

# date-bearing keys that are the VINTAGE of a figure (the number beside it)
FIGURE_KEYS = {"vintage", "cap_vintage", "market_cap_vintage"}
# date-bearing keys that are the AS-OF of a whole stored object (posture, scores, management, the peers object)
OBJECT_KEYS = {"as_of", "object_as_of", "universe_vintage"}
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def call(path):
    event = {"rawPath": PREFIX + path, "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(_LAM.invoke(FunctionName=FN, Payload=json.dumps(event).encode())["Payload"].read())
    return r.get("statusCode"), json.loads(r.get("body") or "{}")


def dated(obj, route, out, path=""):
    """Append (route, generic path, key, date) for every figure- or object-vintage string."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            sub = path + "/" + key
            if isinstance(value, str) and key in (FIGURE_KEYS | OBJECT_KEYS):
                m = DATE_RE.match(value)
                if m:
                    out.append((route, path or "/", key, m.group(1)))
            else:
                dated(value, route, out, sub)
    elif isinstance(obj, list):
        for item in obj:
            dated(item, route, out, path + "[]")


def is_us_alpha(member):
    t = member.get("ticker")
    return (member.get("country") == "United States" and isinstance(t, str) and t.isascii() and t.isalpha())


def main(out_path, keys):
    lines = ["# AMGT_RESAPP round 90 -- AMGT-oo-1, the whole-page read (FWD-8, FWD-38)", ""]
    lines.append("Live function `%s`, GET only, read 2026-10-11 by `2.0.0_SA_COO~R1`; trading-day distance from "
                 "`lib/trading_calendar.trading_days_behind` (NYSE)." % FN)
    lines.append("")
    summary = []
    for key in keys:
        c_t, thesis = call("/security/%s/thesis" % key)
        c_p, peers = call("/security/%s/peers" % key)
        figs = [f for f in (thesis.get("header_figures") or []) if isinstance(f, dict)]
        header_dates = collections.Counter((f.get("vintage") or "")[:10] for f in figs)
        header_date = header_dates.most_common(1)[0][0] if header_dates else None
        lines.append("## %s" % key)
        lines.append("")
        lines.append("route status: thesis %s, peers %s | header figures %d, header vintage date(s): %s" % (
            c_t, c_p, len(figs), dict(header_dates)))
        lines.append("")
        # ---- FWD-8: identity
        ti, pi = thesis.get("identity") or {}, peers.get("identity") or {}
        same_subject = ti.get("security_key") == pi.get("security_key") == key
        same_cw = ti.get("crosswalk_vintage") == pi.get("crosswalk_vintage")
        members = [m for m in (peers.get("members") or []) if isinstance(m, dict)]
        us = [m for m in members if is_us_alpha(m)]
        resolvable = {}
        for m in us:
            hit = crosswalk.resolve(m["ticker"] + " US")
            if hit.get("resolution") == crosswalk.RESOLUTION_MEASURED and hit.get("security_key"):
                resolvable[m["ticker"]] = hit["security_key"]
        # the second independent expectation: an all-digit ticker resolves by its Japan code form or a unique held company
        # name, by the route's own rule (AMGT-av-5), recomputed here from the same public functions
        for m in members:
            if numeric_tickers.is_numeric_ticker(m):
                got = numeric_tickers.numeric_fields(
                    {"ticker": m["ticker"], "name": m.get("name")}, scoped_amgt._resolve_held_form,
                    scoped_amgt._held_name_index(), scoped_amgt._clean_display_name)
                if got.get("security_key"):
                    resolvable[m["ticker"]] = got["security_key"]
        served = {m.get("ticker"): (m.get("identity") or {}) for m in members}
        measured = {t: i.get("security_key") for t, i in served.items() if i.get("resolution") == "MEASURED"}
        leaked = [t for t in measured if t not in resolvable]
        wrong = [t for t, k in resolvable.items() if measured.get(t) not in (None, k)]
        missing = [t for t in resolvable if t not in measured]
        no_reason = [m.get("ticker") for m in members
                     if not (m.get("identity") or {}).get("resolution")]
        id_ok = same_subject and same_cw and not leaked and not wrong and not missing and not no_reason
        lines.append("**FWD-8 peer identity** -- subject key equal on thesis and peers: %s; crosswalk vintage equal: %s (%s)" % (
            same_subject, same_cw, ti.get("crosswalk_vintage")))
        lines.append("- members %d | United States alphabetic %d | resolvable (`<T> US`, or an all-digit ticker by its Japan code "
                     "or a unique held name) %d | served MEASURED %d" % (len(members), len(us), len(resolvable), len(measured)))
        lines.append("- served a key the pool does not hold under that form (leaked): %d %s | resolvable but not served (missing): %d %s"
                     " | served a different key (wrong): %d %s | rows with no identity.resolution: %d" % (
                         len(leaked), leaked, len(missing), missing, len(wrong), wrong, len(no_reason)))
        lines.append("- **agrees: %s**" % ("YES" if id_ok else "NO"))
        lines.append("")
        # ---- FWD-38: vintages
        rows = []
        dated(thesis, "thesis", rows)
        dated(peers, "peers", rows)
        grp = collections.OrderedDict()
        for route, path, k, date in rows:
            gap = tc.trading_days_behind(date, header_date) if header_date else None
            grp.setdefault((route, path, k, date), [0, gap])[0] += 1
        fig_in = fig_all = obj_in = obj_all = 0
        table = []
        for (route, path, k, date), (n, gap) in sorted(grp.items()):
            kind = "figure" if k in FIGURE_KEYS else "object"
            ok = gap is not None and gap <= 1
            if kind == "figure":
                fig_all += n
                fig_in += n if ok else 0
            else:
                obj_all += n
                obj_in += n if ok else 0
            table.append("| %s | `%s` `%s` | %s | %s | %d | %s | %s |" % (
                kind, route, path + "/" + k, date, header_date, n, gap, "yes" if ok else "NO"))
        lines.append("**FWD-38 vintages** -- figure vintages within one trading day of the header's: %d of %d; "
                     "object as-of dates within one trading day: %d of %d" % (fig_in, fig_all, obj_in, obj_all))
        lines.append("")
        lines.append("| kind | route and path | date | header date | n | trading days behind | within 1 |")
        lines.append("|---|---|---|---|---|---|---|")
        lines.extend(table)
        caveat = (peers.get("subject") or {}).get("cross_vintage_caveat")
        lines.append("")
        lines.append("page states the cross-vintage itself (`peers.subject.cross_vintage_caveat`): %s" % (
            "yes -- " + str(caveat)[:260] if caveat else "no"))
        lines.append("")
        summary.append((key, id_ok, fig_in, fig_all, obj_in, obj_all))
    lines.append("## Verdicts")
    lines.append("")
    lines.append("| name | FWD-8 identity agrees | figure vintages within 1 trading day | object as-of within 1 trading day |")
    lines.append("|---|---|---|---|")
    for key, id_ok, fi, fa, oi, oa in summary:
        lines.append("| %s | %s | %d of %d | %d of %d |" % (key, "YES" if id_ok else "NO", fi, fa, oi, oa))
    lines.append("")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[-(len(summary) + 6):]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
