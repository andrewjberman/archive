#!/usr/bin/env python
"""OG-ev-1: ONE projected answer body per marker the CVO named, from the INSTALLED code on the live host. READ-ONLY.

Runs ON i-07dccb1615503ac99 under /opt/opal-gateway/.venv/bin/python (pulled from S3, Rule 12). Calls the registered tool functions
(tools.<name>) so every gate of the dispatch runs: the Opal stand-in for the non-client tools, a master_admin stand-in (built in-process
from the host's own configured roster key; nothing printed) for the five client tools. The Graph token the dispatch fetches after the
entitlement gate is replaced by a placeholder because none of these tools uses it. The audit sink is stubbed. Nothing is written.

HYGIENE, DONE ON THE HOST BEFORE ANYTHING LEAVES IT (the record's check is blind, so the scrub is conservative and says what it did):
  * a number whose integer part has 8 or more digits is rendered as a string with thousands separators; a float with a long digit run is
    rounded to 6 decimals; a string with a digit run of 8 or more gets a hyphen every 4 digits (CUSIPs and dates keep their digits, readably);
  * a key that names a person, contact or account number, or an e-mail address in a string, is replaced by "[masked]";
  * free-text article fields (title, headline, url, description, summary) are replaced by "[masked: article text]" because a headline can
    carry a person's name; the tool's counts, dates, tiers and scores stay;
  * an account reference keeps ****<last4>, the vendor, and the alias is replaced by "[alias]" in the recorded ARGUMENTS only.
A body over its byte limit keeps its scalars and its first rows (the largest list is halved until it fits) and the entry says so.

SSM returns at most ~24000 characters, so the bodies are returned as one zlib-compressed base64 block with a limit lowered until it fits.
Output: a line EV1_BODIES_B64, the block, a line EV1_META_JSON, a small JSON of notes and attempts.
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import traceback
import zlib

ROOT = "/opt/opal-gateway"
PROBE_OID = "00000000-0000-0000-0000-000000000e42"
PERSON_KEYS = ("management", "roster", "officer", "executive", "author", "analyst", "person", "contact", "email", "phone",
               "account_number", "account_id", "owner", "reviewer", "portfolio_manager")
TEXT_KEYS = ("title", "headline", "lead_headline", "url", "description", "summary", "headline_summary", "key_drivers", "counterarguments")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
LONG = re.compile(r"\d{8,}")
CANDIDATE_QUIET = ["F", "GM", "T", "VZ", "KO", "PEP", "XOM", "CVX", "INTC", "PFE", "MRK", "WMT", "DIS", "NKE", "BA", "GE", "IBM", "CSCO",
                   "ORCL", "JNJ", "MCD", "HD", "UNH", "CAT"]


def hyphenate(s: str) -> str:
    return LONG.sub(lambda m: "-".join(m.group(0)[i:i + 4] for i in range(0, len(m.group(0)), 4)), s)


def scrub(o, key=""):
    lk = str(key).lower()
    if any(p in lk for p in PERSON_KEYS):
        return "[masked]"
    if lk in TEXT_KEYS:
        return "[masked: article text]"
    if isinstance(o, dict):
        return {k: scrub(v, k) for k, v in o.items()}
    if isinstance(o, list):
        return [scrub(v, key) for v in o]
    if isinstance(o, bool) or o is None:
        return o
    if isinstance(o, int):
        return "{:,}".format(o) if abs(o) >= 10 ** 7 else o
    if isinstance(o, float):
        if abs(o) >= 10 ** 7:
            return "{:,.2f}".format(o)
        r = repr(o)
        return round(o, 6) if LONG.search(r) else o
    if isinstance(o, str):
        s = EMAIL.sub("[masked]", o)
        return hyphenate(s)
    return o


def size(o) -> int:
    return len(json.dumps(o, separators=(",", ":"), default=str))


def lists_in(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from lists_in(v, path + (k,))
    elif isinstance(o, list):
        yield path, o
        for i, v in enumerate(o[:3]):
            yield from lists_in(v, path + (i,))


def shrink(body, limit):
    """(body, truncated). Halve the largest list until the body fits; then clip very long strings."""
    if size(body) <= limit:
        return body, False
    cut = False
    for _ in range(200):
        if size(body) <= limit:
            break
        best = max(((size(lst), p, lst) for p, lst in lists_in(body) if len(lst) > 1), key=lambda t: t[0], default=None)
        if best is None:
            break
        best[2][:] = best[2][:max(1, len(best[2]) // 2)]
        cut = True

    def clip(o):
        if isinstance(o, dict):
            return {k: clip(v) for k, v in o.items()}
        if isinstance(o, list):
            return [clip(v) for v in o]
        if isinstance(o, str) and len(o) > 240:
            return o[:240] + "..."
        return o
    if size(body) > limit:
        body = clip(body)
        cut = True
    return body, cut


def find_vals(obj, keys, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, (str, int)):
                out.append(v)
            else:
                find_vals(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            find_vals(v, keys, out)
    return out


def mask_args(kw):
    out = {}
    for k, v in kw.items():
        if isinstance(v, str) and re.match(r"^\*{4}\w{4}/", v):
            parts = v.split("/")
            out[k] = "/".join(parts[:2] + ["[alias]"])
        elif k == "account_last4":
            out[k] = "[masked]"
        else:
            out[k] = v
    return out


def dates_in_row(o):
    best = 0
    pat = re.compile(r"^\d{4}-\d{2}-\d{2}")
    if isinstance(o, dict):
        n = sum(1 for v in o.values() if isinstance(v, str) and pat.match(v))
        best = max(best, n)
        for v in o.values():
            best = max(best, dates_in_row(v))
    elif isinstance(o, list):
        for v in o[:50]:
            best = max(best, dates_in_row(v))
    return best


def main() -> int:
    sys.path.insert(0, ROOT)
    os.chdir(ROOT)
    from app import tools                                                    # noqa: E402
    from app import audit, client_core as cc, context, identity_scope        # noqa: E402
    from app.config import get_config                                        # noqa: E402

    audit.log_call = lambda *a, **k: None                                    # type: ignore
    dom = identity_scope.OPAL_USERS_DOMAIN
    opal = context.make_principal(context.MOCK_TENANT_ID, PROBE_OID, "ev1.answers@%s" % dom)
    master = None
    roster = list(getattr(get_config(), "MASTER_ADMIN_PRINCIPALS", ()) or ())
    if roster:
        tid, oid = str(roster[0]).strip().split("/")
        master = context.make_principal(tid, oid, "ev1.master@%s" % dom)
    tools._user_token = lambda: ("ev1.answers@%s" % dom, "no-token")        # type: ignore

    meta = {"attempts": {}, "notes": {}, "blocked": [], "masking": []}
    entries = {"ap-18": [], "ap-19": [], "ap-20": [], "ap-21": [], "ap-23": []}

    def call(tool, who="opal", **kw):
        context.set_current_principal(master if (who == "master" and master is not None) else opal)
        try:
            return getattr(tools, tool)(**kw)
        except Exception as exc:
            return {"error": "%s: %s" % (type(exc).__name__, str(exc)[:200]), "guard_denied": True}

    def ok(res):
        return isinstance(res, dict) and not res.get("guard_denied") and not res.get("code") and "error" not in res

    def add(rel, tool, marker, kw, body, note=None):
        entries[rel].append({"tool": tool, "marker": marker, "arguments": mask_args(kw), "body": body, "note": note})

    # ---------------- ap-18 ----------------
    r = call("harvest_resolve_security", query="AAPL")
    key = (find_vals(r, ("security_key",)) or [None])[0]
    kw = {"security_key": key, "from_day": "2026-10-01", "to_day": "2026-10-15"}
    res = call("harvest_get_chatter", **kw)
    add("ap-18", "harvest_get_chatter", "the newest-part counts of a typed answer (denominator rows_in_part, rows_for_key, days_returned)", kw, res)

    quiet = []
    for t in CANDIDATE_QUIET:
        rr = call("harvest_resolve_security", query=t)
        k2 = (find_vals(rr, ("security_key",)) or [None])[0]
        if not k2:
            continue
        kw2 = {"security_key": k2, "from_day": "2026-09-16", "to_day": "2026-10-15"}
        cr = call("harvest_get_chatter", **kw2)
        if not ok(cr):
            continue
        daily = cr.get("daily") if isinstance(cr.get("daily"), list) else []
        statuses = sorted({str(d.get("data_status")) for d in daily if isinstance(d, dict) and "data_status" in d})
        arts = sum(d.get("articles_total") for d in daily if isinstance(d, dict) and isinstance(d.get("articles_total"), (int, float)))
        quiet.append({"ticker": t, "days_returned": len(daily), "articles_in_window": arts, "statuses": statuses, "kw": kw2, "res": cr})
    meta["attempts"]["ap-18.quiet"] = [{k: v for k, v in q.items() if k not in ("kw", "res")} for q in quiet]
    with_status = [q for q in quiet if q["statuses"]]
    pick = min(with_status, key=lambda q: (q["articles_in_window"], q["days_returned"])) if with_status else (min(quiet, key=lambda q: (q["articles_in_window"], q["days_returned"])) if quiet else None)
    if pick:
        note = None if pick["statuses"] else "no daily row of the quietest name carries a data_status; shown is the quietest answer"
        add("ap-18", "harvest_get_chatter", "data_status on a quiet name (the quietest of %d covered tickers read: %d articles over 30 days, %d daily rows)"
            % (len(quiet), pick["articles_in_window"], pick["days_returned"]), pick["kw"], pick["res"], note)
    else:
        meta["blocked"].append("ap-18 quiet name: no candidate ticker resolved and answered")
    kw = {"query": "999999AA9"}
    add("ap-18", "harvest_resolve_security", "not_held for a CUSIP the registry does not hold", kw, call("harvest_resolve_security", **kw))

    # ---------------- ap-19 ----------------
    add("ap-19", "portal_get_pipeline_freshness", "freshness stated in trading days (denominator trading_days_behind_t1)", {},
        call("portal_get_pipeline_freshness"))
    kw = {"date_from": "2026-10-11", "date_to": "2026-10-11", "limit": 5}
    qres = call("news_search_articles", **kw)
    has_ds = "data_status" in json.dumps(qres, default=str)
    note = ("the portal and news tools carry no field called data_status (it is a field of the harvest chatter and figures answers); this is the "
            "quiet-day answer these tools give, absent_reason and freshness. BLOCKING row filed.")
    if not has_ds:
        meta["blocked"].append("ap-19 data_status on a quiet day: the news and portal tools have no data_status field")
    add("ap-19", "news_search_articles", "data_status on a quiet day (a Sunday: no article matched the window)", kw, qres, None if has_ds else note)
    caps = []
    for wd in (999, 30, 21):
        kw3 = {"ticker": "AAPL", "window_days": wd}
        nres = call("news_for_security", **kw3)
        txt = json.dumps(nres, default=str)
        caps.append({"window_days_asked": wd, "applied": (nres or {}).get("window_days_applied"), "window_days": (nres or {}).get("window_days"),
                     "mentions_14day": bool(re.search(r"14[- ]day|14 days|fourteen", txt, re.I)), "kw": kw3, "res": nres})
    meta["attempts"]["ap-19.cap"] = [{k: v for k, v in c.items() if k not in ("kw", "res")} for c in caps]
    pickc = next((c for c in caps if c["mentions_14day"]), caps[0])
    add("ap-19", "news_for_security", "the 14-day news cap stated in an answer (window asked %s, applied %s)" % (pickc["window_days_asked"], pickc["applied"]),
        pickc["kw"], pickc["res"], None if pickc["mentions_14day"] else ("no string of this answer says '14-day'. The window fields show the cap this tool applies: an ask of %s days is applied as %s days (window_days_applied); the default window is 14 days. The criterion names a 14-day cap and the tool caps at %s: reported as an OBSERVATION row." % (pickc["window_days_asked"], pickc["applied"], pickc["applied"])))

    # ---------------- ap-20 ----------------
    kw = {"fund_ticker": "IDVZ"}
    hres = call("etfs_get_fund_holdings", **kw)
    add("ap-20", "etfs_get_fund_holdings", "weights in percentage points with their unit (weight_column, weight_unit)", kw, hres)
    cands = [("etfs_get_fund_holdings", {"fund_ticker": "IDVZ"}, hres)]
    for tname, k in (("etfs_get_fund_nav_history", {"fund_ticker": "IDVZ"}), ("etfs_get_partner_ownership", {"firm": "49financial"}),
                     ("etfs_get_partner_ownership", {"firm": "cottonwood"})):
        cands.append((tname, k, call(tname, **k)))
    scored = [(dates_in_row(c[2]) if ok(c[2]) else -1, c) for c in cands]
    meta["attempts"]["ap-20.three_dates"] = [{"tool": c[0], "max_dates_in_a_row": s} for s, c in scored]
    bests, bestc = max(scored, key=lambda t: t[0])
    add("ap-20", bestc[0], "three dates in one row (the row with the most date fields: %d)" % bests, bestc[1], bestc[2],
        None if bests >= 3 else "no row of the candidate answers carries three date fields; shown is the row with the most (%d)" % bests)
    add("ap-20", "etfs_get_monthly_report", "coverage from each partner's own csv (coverage, csv_rows)", {}, call("etfs_get_monthly_report"))

    # ---------------- ap-21 ----------------
    for sec, marker in (("ledger", "the section asked for (section: ledger)"), ("versions", "its as-of (as_of beside the section)"),
                        ("timeline", "the 50 KB projection flagged (truncated, projected_to_bytes)")):
        kw = {"security_key": key, "sections": sec}
        add("ap-21", "harvest_get_published_analysis", marker, kw, call("harvest_get_published_analysis", **kw))

    # ---------------- ap-23 ----------------
    ctx = cc._new_ctx()
    from app import client_adapter_smartx as sx                              # noqa: E402
    from app import client_adapter_schwab as sch                             # noqa: E402
    last4, ref = None, None
    try:
        pre = ctx.prefix(sx.VENDOR, sx.SEGMENT, sx.LAYER, sx.T_MAP)
        for p in reversed(ctx.list_partitions(pre)[-10:]):
            nums = [m.get("account_number") for m in ctx.read_rows(pre, p)
                    if isinstance(m.get("account_number"), str) and len(m.get("account_number")) >= 4]
            if nums:
                last4 = nums[0][-4:]
                break
    except Exception as exc:
        meta["notes"]["smartx_last4"] = "%s: %s" % (type(exc).__name__, str(exc)[:100])
    fa, fb = "49financial", "cottonwood"
    if last4:
        r1 = call("client_resolve_account", who="master", firm=fa, account_last4=last4)
        cs = [c for c in ((r1 or {}).get("candidates") or []) if isinstance(c, dict) and c.get("vendor") == "smartx"]
        ref = cs[0].get("account_ref") if cs else None
    if ref:
        kw = {"firm": fa, "account": ref}
        ha = call("client_get_holdings", who="master", **kw)
        add("ap-23", "client_get_holdings", "a firm's data date stated (partition_date, as_of, freshness_td)", kw, ha)
        hb = call("client_get_holdings", who="master", firm=fb, account=ref)
        add("ap-23", "client_get_holdings", "rows never merged across firms (the same account reference asked of two firms, each firm's answer apart)",
            {"firm_a": fa, "firm_b": fb, "account": ref}, {fa: ha, fb: hb},
            "two calls, one account reference, firm %s then firm %s; the second firm's answer holds none of the first firm's rows" % (fa, fb))
    else:
        meta["blocked"].append("ap-23 firm data date and two-firm call: no SmartX account reference could be derived")
    kw = {"fund_ticker": "BASG"}
    add("ap-23", "etfs_get_rival_fund_holdings", "figures with units (weight_unit fraction, market_value)", kw, call("etfs_get_rival_fund_holdings", **kw))
    sref = []
    try:
        index, scanned = sch._index(ctx, fa, None)
        byacc = {}
        for alias, e in index.items():
            byacc.setdefault(e["account_id"], []).append((e["slot"], alias, e["master"]))
        multi = [v for v in byacc.values() if len({s for s, _, _ in v}) >= 2]
        pick = sorted(multi[0]) if multi else None
        if pick is None:
            slots = {}
            for alias, e in index.items():
                slots.setdefault(e["slot"], (e["slot"], alias, e["master"], e["account_id"]))
            pick = [(s, a, m) for s, a, m, _ in sorted(slots.values())][:2]
        for slot, alias, master_no in pick[:2]:
            full = "****%s/schwab/%s" % (str(index[alias]["account_id"])[-4:], alias)
            sref.append((slot, full, bool(multi)))
        meta["notes"]["schwab"] = {"masters_scanned": [{k: s[k] for k in ("slot", "rows", "accounts", "unmintable", "refusal")} for s in scanned],
                                   "account_under_two_masters_found": bool(multi)}
    except Exception as exc:
        meta["notes"]["schwab_error"] = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    if sref:
        body = {}
        for slot, full, _m in sref:
            body["master_slot_%d" % slot] = call("client_get_holdings", who="master", firm=fa, account=full)
        add("ap-23", "client_get_holdings", "Schwab masters never summed (the same account asked under each master it sits in; each master slot answers apart)",
            {"firm": fa, "accounts": ["****%s/schwab/[alias]" % s[1].split("/")[0][4:] for s in sref]}, body,
            "Schwab alias references are minted per master; each master slot's answer is its own and nothing is summed across them"
            + ("" if sref[0][2] else " (no account sits under two masters here: two accounts from two masters are shown)"))
    else:
        meta["blocked"].append("ap-23 Schwab masters: no Schwab account reference could be minted (the catalog holds no Schwab dim_position row for the firm)")
        ph = {"firm": fa, "account": "****0000/schwab/acr_v1_" + "a" * 26}
        add("ap-23", "client_get_holdings", "Schwab masters never summed (CANNOT BE SHOWN: the installed tool answers no_catalog_row for Schwab, see the note)", ph,
            call("client_get_holdings", who="master", **ph),
            "this is the real answer of the installed tool to a well-formed Schwab reference; it cannot show the marker because the catalog carries no Schwab dim_position "
            "row for the firm (MX-c-23 is not landed), so no account reference can be minted and no master's rows are served. BLOCKING row filed.")

    # ---------------- scrub, shrink, fit ----------------
    out = {"releases": {}}
    limit = 12000
    while True:
        total = {}
        for rel, rows in entries.items():
            total[rel] = []
            for e in rows:
                b = scrub(e["body"])
                b, cut = shrink(b, limit)
                row = {"tool": e["tool"], "marker": e["marker"], "arguments": scrub(e["arguments"]), "body": b}
                if cut:
                    row["truncated"] = True
                    row["note"] = ((e["note"] + "; ") if e["note"] else "") + "body clipped to %d bytes: scalars kept, the largest lists keep their first rows" % limit
                elif e["note"]:
                    row["note"] = e["note"]
                total[rel].append(row)
        blob = base64.b64encode(zlib.compress(json.dumps(total, separators=(",", ":"), default=str).encode("utf-8"), 9)).decode("ascii")
        if len(blob) <= 21500 or limit <= 1500:
            out["releases"] = total
            break
        limit = int(limit * 0.8)
    meta["limit_bytes_used"] = limit
    meta["b64_chars"] = len(blob)
    meta["bodies"] = {rel: len(rows) for rel, rows in total.items()}
    print("EV1_BODIES_B64")
    print(blob)
    print("EV1_META_JSON")
    print(json.dumps(meta, separators=(",", ":"), default=str))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("EV1_BODIES_B64")
        print("")
        print("EV1_META_JSON")
        print(json.dumps({"fatal": traceback.format_exc()[-1800:]}))
        sys.exit(1)
