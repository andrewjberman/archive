#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-h-1 -- the ISSUER'S acceptance read of the first SCHEDULED fire that carries the frontier-count change
(the frontier account counts read the newest A4 account-distribution keyed AT OR BEFORE the axis date, fail closed, never the staged
runner object gold/mdpf_revamp/{scope}/account_distribution.json). S5 disarms on this read-back (CTO round-5 ADDENDUM 5, msg 4782).

Read-only against the SERVED objects (list/get/head, one lambda code read). Run it on the first fire that mints a new as-of date after the
CN-h-1 deploy (2026-10-15 13:30Z at the earliest). Prints dates, counts and differences; never an account id, never a client dollar level.

  python r7_frontier_readback.py read [--date YYYY-MM-DD] [--prior YYYY-MM-DD]
        D = the new global aggregate-aua-timeseries dated key (default: newest); --prior defaults to the previous dated global key.
        The three scopes are global, 49financial, inflection (cottonwood never calls the loader and is not read).
  python r7_frontier_readback.py refused --date YYYY-MM-DD [--expect-version <VersionId>]
        the fail-closed branch, read only if a refused day occurs: whether the scope's objects exist for D, the newest existing key and
        its VersionId (the prior object must be untouched), the run manifest's errors (dates and counts only) and the loader's WARN
        token in the lambda's log (read-only; a denied log read is reported, not a pass).
  python r7_frontier_readback.py selftest
        builds a synthetic "after" object OFFLINE from the real newest served objects by applying the real A4 maps at the as-of (the
        cell's arithmetic), runs F1-F4 and F6 on it (must PASS), then plants three defects and requires each to turn the named arm RED.

Arms (a line `  <ARM> PASS|FAIL <detail>` each, then `ROUND 7 READBACK: k of n arms`; exit 0 only when every arm passes):
  F1 per scope, every overridden key's served account_count[-1] equals the newest A4 map keyed on or before the axis date, and none
     equals the STALE staged value where the two differ (the failure signature: served == staged != A4)
  F2 per scope, account_count_total[-1] equals the composition the build defines (the sum of the last-date counts of every by_model
     line that is not an additive overlay line: the build sums its own leg-composed lines BEFORE the tax and sleeve overlays are
     written); the move against the prior object, and the A4-vs-staged delta, are PRINTED (the roster also moves day to day)
  F3 every date other than the last is byte-equal to the prior object (by_model counts and values, account_count_total) on the common
     dates, excluding the prior object's own last date (the next fire restates it); the override touches only the last date
  F4 meta.frontier_count.staleness names the A4's own period (never the 2026-08-17 staged period) and reads FRESH on equal dates
  F5 on a fire the loader was reached: the deployed loader's body names no staged key (the fail-closed rule is in the bytes that ran);
     the refused-day read is the `refused` subcommand
  F6 the headline arrays other than counts (opal_aggregate_aua, model_aua, non_model_aua, tax_additive_aua, sma_additive_aua) equal the
     prior object on the common dates, excluding the prior object's last date
  F7 the staged runner objects are untouched (LastModified before 2026-08-19: the cell must not write them, and nothing else does)
"""
from __future__ import annotations

import ast
import copy
import io
import json
import sys
import urllib.request
import zipfile

BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
TYPE_TS = "aggregate-aua-timeseries"
TYPE_A4 = "account-distribution"
SCOPES = ("global", "49financial", "inflection")
FOLD_KEY = "other_models"
HEADLINE = ("opal_aggregate_aua", "model_aua", "non_model_aua", "tax_additive_aua", "sma_additive_aua")
STAGED_FMT = "gold/mdpf_revamp/%s/account_distribution.json"
STAGED_PERIOD = "2026-08-17"
STAGED_FROZEN_BEFORE = "2026-08-19"
LAMBDA = "mdpf-gold-lambda"
LOADER = "load_account_dist_frontier_counts"
LOG_GROUP = "/aws/lambda/mdpf-gold-lambda"
LOG_TOKEN = "frontier-count: no A4"


# ------------------------------------------------------------------------------------------------ S3 reads
def _client(kind: str):
    import boto3
    from botocore.config import Config
    return boto3.client(kind, region_name="us-east-1",
                        config=Config(read_timeout=30, connect_timeout=10, retries={"max_attempts": 2}))


def _keys(s3, scope: str, typ: str) -> list:
    out, tok = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": "%s/%s/%s/" % (PREFIX, scope, typ)}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".json")]
        if not r.get("IsTruncated"):
            return sorted(out)
        tok = r.get("NextContinuationToken")


def _json(s3, key: str) -> dict:
    return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())


def _date_of(key: str) -> str:
    return key.rsplit("/", 1)[-1][:-5]


def _opt(argv: list, name: str):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None


# ------------------------------------------------------------------------------------------------ small helpers
def _additive(e) -> bool:
    return (e or {}).get("source_basis") == "additive"


def _last(arr):
    return arr[-1] if arr else None


def _cnt(e):
    return _last((e or {}).get("account_count") or [])


def _didx(ts: dict) -> dict:
    return {d: i for i, d in enumerate(ts.get("dates") or [])}


def _a4_map(a4) -> dict:
    return dict(((a4 or {}).get("meta") or {}).get("account_count_by_model_key") or {})


def _staged_map(obj) -> dict:
    return dict(((obj or {}).get("meta") or {}).get("account_count_by_model_key") or {})


def pick_a4(keys: list, axis: str):
    """The newest A4 key whose file date is <= the axis date (the cell's rule)."""
    best = None
    for k in keys:
        nm = k.rsplit("/", 1)[-1]
        if len(nm) == 15 and nm.endswith(".json") and nm[:-5] <= axis:
            if best is None or nm[:-5] > best[0]:
                best = (nm[:-5], k)
    return best


# ------------------------------------------------------------------------------------------------ arms (pure over dicts)
def f1(new: dict, a4s: dict, staged: dict) -> tuple:
    bad, tot_cmp, tot_eq, tot_fz, parts = [], 0, 0, 0, []
    for sc in SCOPES:
        ts = new.get(sc)
        key, a4 = a4s.get(sc, (None, None))
        if ts is None or a4 is None:
            return False, "%s: %s" % (sc, "no new object" if ts is None else "no A4 at or before the axis date")
        m, sm, bm = _a4_map(a4), _staged_map(staged.get(sc)), ts.get("by_model") or {}
        cmp_ = eq = fz = 0
        for k, v in m.items():
            e = bm.get(k)
            if e is None or k == FOLD_KEY or _additive(e):
                continue                       # a folded line, the fold line and an overlay line are not overridden
            c = _cnt(e)
            cmp_ += 1
            if c == v:
                eq += 1
            else:
                bad.append((sc, k, c, v))
                if k in sm and c == sm[k]:
                    fz += 1
        tot_cmp, tot_eq, tot_fz = tot_cmp + cmp_, tot_eq + eq, tot_fz + fz
        parts.append("%s: A4 %s (period %s) map %d keys, compared %d, equal %d, equal-to-staged-not-A4 %d"
                     % (sc, (key or "?").rsplit("/", 1)[-1], (a4 or {}).get("period"), len(m), cmp_, eq, fz))
        if cmp_ == 0:
            bad.append((sc, "<no key compared>", None, None))
    ok = tot_cmp > 0 and not bad
    tail = "" if ok else " | FIRST %s | frozen signature (served == staged != A4): %d" % (bad[:4], tot_fz)
    return ok, "; ".join(parts) + tail


def f2(new: dict, prior: dict, a4s: dict, staged: dict) -> tuple:
    ok, parts = True, []
    for sc in SCOPES:
        ts = new[sc]
        bm = ts.get("by_model") or {}
        tot = _last(ts.get("account_count_total") or [])
        basis = _last(ts.get("count_basis") or [])
        comp = sum(c for e in bm.values() if not _additive(e) for c in [_cnt(e)] if c is not None)
        p_tot = _last((prior.get(sc) or {}).get("account_count_total") or [])
        m, sm = _a4_map(a4s[sc][1]), _staged_map(staged.get(sc))
        delta = sum(v - sm[k] for k, v in m.items() if k in sm and k in bm and not _additive(bm[k]) and k != FOLD_KEY)
        this = tot is not None and basis != "held" and int(comp) == int(tot)
        ok = ok and this
        parts.append("%s: total[-1] %s, composition %s%s, prior total[-1] %s, move %s, A4-vs-staged delta on the compared keys %+d"
                     % (sc, tot, comp, " HELD" if basis == "held" else "", p_tot,
                        None if (tot is None or p_tot is None) else "%+d" % (tot - p_tot), delta))
    return ok, "; ".join(parts)


def f3(new: dict, prior: dict) -> tuple:
    bad, n = [], 0
    for sc in SCOPES:
        a, b = new[sc], prior.get(sc) or {}
        ia, ib = _didx(a), _didx(b)
        skip = {(b.get("dates") or [None])[-1], (a.get("dates") or [None])[-1]}
        common = [d for d in ib if d in ia and d not in skip]
        for k, e in (a.get("by_model") or {}).items():
            pe = (b.get("by_model") or {}).get(k)
            if pe is None or k == FOLD_KEY or _additive(e):
                continue
            for fld in ("account_count", "model_value"):
                ra, rb = e.get(fld) or [], pe.get(fld) or []
                for d in common:
                    n += 1
                    va = ra[ia[d]] if ia[d] < len(ra) else None
                    vb = rb[ib[d]] if ib[d] < len(rb) else None
                    if va != vb:
                        bad.append((sc, k, fld, d))
        ra, rb = a.get("account_count_total") or [], b.get("account_count_total") or []
        for d in common:
            n += 1
            if (ra[ia[d]] if ia[d] < len(ra) else None) != (rb[ib[d]] if ib[d] < len(rb) else None):
                bad.append((sc, "account_count_total", "-", d))
    return (not bad and n > 0), "cells compared %d across the three scopes, unequal %d%s" % (
        n, len(bad), "" if not bad else " first=%s" % bad[:4])


def f4(new: dict, a4s: dict) -> tuple:
    ok, parts = True, []
    seen = 0
    for sc in SCOPES:
        fc = ((new[sc].get("meta") or {}).get("frontier_count"))
        a4 = a4s[sc][1]
        if not isinstance(fc, dict) or not isinstance(fc.get("staleness"), dict):
            parts.append("%s: no frontier_count stamp (as before)" % sc)
            continue
        seen += 1
        st = fc["staleness"]
        frontier = (new[sc].get("dates") or [None])[-1]
        this = (st.get("as_of") == (a4 or {}).get("period") and st.get("as_of") != STAGED_PERIOD
                and ((st.get("verdict") == "FRESH") == (st.get("as_of") == frontier)))
        ok = ok and this
        parts.append("%s: stamp as_of %s (A4 period %s), frontier %s, verdict %s" % (
            sc, st.get("as_of"), (a4 or {}).get("period"), frontier, st.get("verdict")))
    return (ok and seen > 0), "; ".join(parts) + ("" if seen else " | no scope carries a stamp")


def f6(new: dict, prior: dict) -> tuple:
    bad, n = [], 0
    for sc in SCOPES:
        a, b = new[sc], prior.get(sc) or {}
        ia, ib = _didx(a), _didx(b)
        skip = {(b.get("dates") or [None])[-1]}
        common = [d for d in ib if d in ia and d not in skip]
        for fld in HEADLINE:
            ra, rb = a.get(fld), b.get(fld)
            if ra is None or rb is None:
                continue
            for d in common:
                n += 1
                if ra[ia[d]] != rb[ib[d]]:
                    bad.append((sc, fld, d))
    return (not bad and n > 0), "cells compared %d, unequal %d%s" % (n, len(bad), "" if not bad else " first=%s" % bad[:4])


# ------------------------------------------------------------------------------------------------ live-only arms
def f5_live(lam) -> tuple:
    try:
        loc = lam.get_function(FunctionName=LAMBDA)["Code"]["Location"]
        z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(loc, timeout=60).read()))
        names = [n for n in z.namelist() if n.endswith("dim_mdpf_aggregate_aua_timeseries.py")]
        if not names:
            return False, "dim_mdpf_aggregate_aua_timeseries.py not in the deployed package"
        src = z.read(names[0]).decode("utf-8", "replace")
        fdef = next((n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == LOADER), None)
        if fdef is None:
            return False, "%s not found in the deployed module" % LOADER
        body = ast.get_source_segment(src, fdef) or ""
        # the docstring may NAME the retired object; the rule is that no executable statement carries the staged key
        code = [s for s in fdef.body if not (isinstance(s, ast.Expr) and isinstance(getattr(s, "value", None), ast.Constant)
                                           and isinstance(s.value.value, str))]
        lit = [c.value for s in code for c in ast.walk(s) if isinstance(c, ast.Constant) and isinstance(c.value, str)
               and ("gold/mdpf_revamp" in c.value or "account_distribution.json" in c.value)]
        takes = "axis_date" in [a.arg for a in fdef.args.args]
        return (not lit and takes), ("deployed %s: takes axis_date=%s, %d executable string literal(s) name a staged key, "
                                     "A4 prefix literal present=%s" % (LOADER, takes, len(lit), "account-distribution" in body))
    except Exception as exc:                                  # noqa: BLE001
        return False, "deployed package read failed (%s: %s) -- not a pass" % (type(exc).__name__, str(exc)[:100])


def f7_live(s3) -> tuple:
    parts, ok = [], True
    for sc in SCOPES:
        try:
            lm = s3.head_object(Bucket=BUCKET, Key=STAGED_FMT % sc)["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception as exc:                              # noqa: BLE001
            parts.append("%s: head failed (%s)" % (sc, type(exc).__name__))
            ok = False
            continue
        this = lm < STAGED_FROZEN_BEFORE
        ok = ok and this
        parts.append("%s staged LastModified %s%s" % (sc, lm, "" if this else " (MOVED)"))
    return ok, "; ".join(parts)


# ------------------------------------------------------------------------------------------------ commands
def _report(arms: list) -> int:
    k = sum(1 for a in arms if a)
    print("ROUND 7 READBACK: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) else 1


def _load_world(s3, date, prior):
    gdates = [_date_of(k) for k in _keys(s3, "global", TYPE_TS)]
    if date is None:
        date = gdates[-1]
    if prior is None:
        earlier = [d for d in gdates if d < date]
        prior = earlier[-1] if earlier else None
    new, old, a4s, staged = {}, {}, {}, {}
    for sc in SCOPES:
        keys = {_date_of(k): k for k in _keys(s3, sc, TYPE_TS)}
        if date not in keys:
            raise SystemExit("no %s object for %s on %s" % (TYPE_TS, sc, date))
        new[sc] = _json(s3, keys[date])
        pd = prior if prior in keys else max([d for d in keys if d < date] or [None] or [None])
        old[sc] = _json(s3, keys[pd]) if pd else {}
        axis = (new[sc].get("dates") or [None])[-1]
        pick = pick_a4(_keys(s3, sc, TYPE_A4), axis)
        a4s[sc] = (pick[1], _json(s3, pick[1])) if pick else (None, None)
        try:
            staged[sc] = _json(s3, STAGED_FMT % sc)
        except Exception:                                      # noqa: BLE001
            staged[sc] = None
    return date, prior, new, old, a4s, staged


def cmd_read(argv: list) -> int:
    s3, lam = _client("s3"), _client("lambda")
    date, prior, new, old, a4s, staged = _load_world(s3, _opt(argv, "--date"), _opt(argv, "--prior"))
    print("  object %s against prior %s; axis dates %s" % (date, prior, {sc: (new[sc].get("dates") or [None])[-1] for sc in SCOPES}))
    arms = []
    for name, (ok, detail) in (("F1", f1(new, a4s, staged)), ("F2", f2(new, old, a4s, staged)), ("F3", f3(new, old)),
                               ("F4", f4(new, a4s)), ("F5", f5_live(lam)), ("F6", f6(new, old)), ("F7", f7_live(s3))):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(ok)
    return _report(arms)


def cmd_refused(argv: list) -> int:
    date, expect = _opt(argv, "--date"), _opt(argv, "--expect-version")
    if not date:
        print("refused needs --date")
        return 2
    s3 = _client("s3")
    arms = []
    for sc in SCOPES:
        keys = {_date_of(k): k for k in _keys(s3, sc, TYPE_TS)}
        have = date in keys
        newest = max([d for d in keys if d <= date] or [None]) if keys else None
        ver = None
        if newest:
            ver = s3.head_object(Bucket=BUCKET, Key=keys[newest]).get("VersionId")
        print("  %s: object for %s exists=%s; newest at or before = %s (VersionId %s)" % (sc, date, have, newest, ver))
        if sc == "global" and expect:
            same = ver == expect
            arms.append(same)
            print("  G1 %s: the prior global object's VersionId %s the expected one" % (
                "PASS" if same else "FAIL", "equals" if same else "DIFFERS from"))
    try:
        r = s3.list_objects_v2(Bucket=BUCKET, Prefix="%s/_manifests/%s/" % (PREFIX, date))
        mk = sorted(o["Key"] for o in r.get("Contents", []))
        if mk:
            m = _json(s3, mk[-1])
            errs = m.get("errors") or {}
            print("  manifest %s errors keys %s; global: %s" % (mk[-1].rsplit("/", 1)[-1], sorted(errs),
                                                              str(errs.get("global"))[:300] if errs.get("global") else "none"))
        else:
            print("  no manifest under _manifests/%s/" % date)
    except Exception as exc:                                  # noqa: BLE001
        print("  manifest read failed: %s" % type(exc).__name__)
    try:
        logs = _client("logs")
        import time
        now = int(time.time() * 1000)
        r = logs.filter_log_events(logGroupName=LOG_GROUP, startTime=now - 48 * 3600 * 1000, endTime=now,
                                   filterPattern='"%s"' % LOG_TOKEN, limit=10)
        ev = r.get("events") or []
        print("  loader WARN token '%s' in the last 48 h: %d event(s)%s" % (
            LOG_TOKEN, len(ev), "" if not ev else "; first: " + ev[0]["message"].strip()[:200]))
    except Exception as exc:                                  # noqa: BLE001
        print("  lambda log read not available (%s) -- the token is UNREAD, not absent" % type(exc).__name__)
    return _report(arms) if arms else 0


def _synth_after(real: dict, a4s: dict) -> dict:
    """The cell's arithmetic applied offline: override the last-date count of every compared key from the A4 map, recompute the
    total from the build's composition, restamp the staleness where a scope carries one."""
    out = {}
    for sc in SCOPES:
        ts = copy.deepcopy(real[sc])
        bm = ts.get("by_model") or {}
        _, a4 = a4s[sc]
        for k, v in _a4_map(a4).items():
            e = bm.get(k)
            if e is None or k == FOLD_KEY or _additive(e) or not e.get("account_count"):
                continue
            e["account_count"][-1] = v
        if ts.get("account_count_total") and ts["account_count_total"][-1] is not None:
            ts["account_count_total"][-1] = int(sum(c for e in bm.values() if not _additive(e)
                                                    for c in [_cnt(e)] if c is not None))
        fc = (ts.get("meta") or {}).get("frontier_count")
        if isinstance(fc, dict):
            period, fd = (a4 or {}).get("period"), (ts.get("dates") or [None])[-1]
            fc["staleness"] = {"as_of": period, "frontier_date": fd, "stale_trading_days": 0 if period == fd else None,
                               "verdict": "FRESH" if period == fd else "STALE"}
        out[sc] = ts
    return out


def cmd_selftest(argv: list) -> int:
    s3 = _client("s3")
    date, prior, real, _old, a4s, staged = _load_world(s3, None, None)
    # the "prior" of the selftest is the real current object itself: the synthetic after differs from it only at the last date
    after = _synth_after(real, a4s)
    print("  selftest world: real objects %s; A4 keys %s" % (date, {sc: (a4s[sc][0] or "?").rsplit("/", 1)[-1] for sc in SCOPES}))

    def grade(a):
        return {"F1": f1(a, a4s, staged), "F2": f2(a, real, a4s, staged), "F3": f3(a, real), "F4": f4(a, a4s), "F6": f6(a, real)}

    good = grade(after)
    allok = True
    for name in ("F1", "F2", "F3", "F4", "F6"):
        ok, detail = good[name]
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        allok = allok and ok
    plants = []
    d1 = copy.deepcopy(after)                                  # a count taken from the staged object
    picked = None
    for sc in SCOPES:
        sm, m = _staged_map(staged.get(sc)), _a4_map(a4s[sc][1])
        for k in m:
            e = d1[sc]["by_model"].get(k)
            if e and not _additive(e) and k in sm and sm[k] != m[k] and e.get("account_count"):
                e["account_count"][-1] = sm[k]
                picked = (sc, k)
                break
        if picked:
            break
    if picked is None:                                         # no frozen key left: any one-off count is still a wrong count
        for sc in SCOPES:
            for k, v in _a4_map(a4s[sc][1]).items():
                e = d1[sc]["by_model"].get(k)
                if e and not _additive(e) and e.get("account_count") and k != FOLD_KEY:
                    e["account_count"][-1] = (v or 0) + 1
                    picked = (sc, k)
                    break
            if picked:
                break
    plants.append(("D1 a count taken from the staged object (%s)" % (picked,), d1, "F1"))
    d2 = copy.deepcopy(after)                                  # a non-last date changed
    for k, e in d2["global"]["by_model"].items():
        if not _additive(e) and k != FOLD_KEY and e.get("account_count") and len(e["account_count"]) > 5 \
                and e["account_count"][-3] is not None:
            e["account_count"][-3] += 1
            break
    plants.append(("D2 a non-last date's count changed by 1", d2, "F3"))
    d3 = copy.deepcopy(after)                                  # a headline array changed by 0.01
    arr = d3["global"]["opal_aggregate_aua"]
    for i in range(len(arr) - 5, -1, -1):
        if arr[i] is not None:
            arr[i] = round(arr[i] + 0.01, 2)
            break
    plants.append(("D3 opal_aggregate_aua changed by 0.01", d3, "F6"))
    for label, g, want in plants:
        res = grade(g)
        red = not res[want][0]
        print("  PLANT %s -> %s %s" % (label, want, "RED (expected)" if red else "NOT RED (BAD)"))
        allok = allok and red
    print("ROUND 7 READBACK SELFTEST: %s" % ("OK" if allok else "FAILED"))
    return 0 if allok else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("read", "refused", "selftest"):
        print(__doc__)
        return 2
    return {"read": cmd_read, "refused": cmd_refused, "selftest": cmd_selftest}[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
