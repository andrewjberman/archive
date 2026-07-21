"""MDPF_REVAMP parity harness (DT lane) -- compare a PUBLISHED portal/ artifact to
its SERVED legacy counterpart. Grounds on LIVE S3, never a self-report. Parity bar
= impl package s6 + the pre-swap baseline + CTO's D1=serve-real bar (2026-07-20).

D1 = SERVE REAL/COMPLETE DATA (Andrew, 2026-07-20): the revamp CORRECTS 3 legacy
artifacts, each a NAMED delta -- (1) real history vs interpolated backfill (converging
by 2026-04-09), (2) full-envelope custody +$20.3M, (3) complete 49F model +$4.1M
(enumeration gap). A value delta is EXPECTED iff it matches the DS-supplied NAMED-DELTA
LEDGER; anything else is UNEXPLAINED.

DATE-JOIN (CTO 135429Z MUST-FIX, 2026-07-21): the served (legacy rederived-business-day)
axis and the published (serve-real real-NYSE-trading-day) axis are DIFFERENT date SETS
(49F: 408 common / 21 served-only synthetic holiday-fills / 20 published-only real trading
days = 19 legacy gaps + 1 fresh frontier tail; the axis GROWS one entry per trading day --
DYNAMIC, never frozen). The comparison therefore JOINS BY DATE KEY, never by positional
index: date-parallel arrays (len == len(axis)) are keyed `path@YYYY-MM-DD` so the served
and published leaf sets intersect on the COMMON dates only. EVERY non-common date is
SURFACED as an explicit structural delta (NAMED via the ledger `_date_axis` entry, else
UNEXPLAINED) -- NEVER silent-skipped (the set-intersection would otherwise drop it, the
same hide path closed for null-mismatch at 5b097cbf3, one axis up). The LATEST cross-section
tie is evaluated at the LAST COMMON date, never positional [-1] (comparing served[-1] to
published[-1] would compare e.g. 07-18-fill vs 07-20-frontier -- the same wrong-axis error).

THE (a)-(d) BAR (CTO): (a) shape parity incl. history arrays + the full date-axis symmetric
diff explained; (b) each value delta MATCHES a ledger entry (magnitude+sign+date-window) and
each non-common date MATCHES the _date_axis entry; (c) NO OTHER unexplained delta; (d) clean
cross-sections tie at last-common + date-drift converges same-cycle. Tight 0.1% tol so any
UNEXPECTED delta surfaces. Verdict: SHAPE_FAIL > UNEXPLAINED_DELTA > NAMED_DELTA_PASS > PASS.
NO ledger -> every value delta AND every non-common date UNEXPLAINED (fail-safe).

LEDGER FORMAT (DS, keyed "<artifact>/<firm>" -> {entry_name: spec}); each spec:
  field_paths: [pattern, ...]     (glob '*'; a "(latest)" suffix or scope:"latest_cross_section"
                                   restricts the entry to the latest cross-section element)
  pct_range: [lo, hi]             SIGNED % band (handles two-sided converging corrections), OR
  abs: N, tol_pct: T              absolute delta +/- tol
  sign: "+"/"-"/"any"             (checked for abs entries; pct_range band is already signed)
  date_before / date_after        ISO date; BOTH => a window [date_after, date_before)
  null_ok: true                   a None-vs-populated mismatch on this field is NAMED (placeholder)
Entries whose name starts with "_" (e.g. _meta/_note) are ignored by the value classifier.
A special ledger entry NAMES the expected date-axis symmetric diff (structural, not a value):
  "_date_axis": {served_only: [ISO...], published_only: [ISO...], note: "..."}
    served_only    dates on the served/legacy axis only (e.g. synthetic holiday-fills) -> EXPECTED
    published_only dates on the published/serve-real axis only (real trading-day gaps + fresh
                   frontier tail) -> EXPECTED
  Any actual non-common date NOT listed is UNEXPLAINED. n_dates and other axis-length-derived
  scalars differ by construction when the axes differ -- name them as expected value deltas.

NOTES: account_distribution keys by_model on DISPLAY NAME; aggregate on MODEL_KEY --
each compared to its OWN served, never cross-normalized. Spec extras (basis/meta) allowed.
account_distribution is a SNAPSHOT (no date axis) -> positional compare, latest everywhere.
aggregate_aua_timeseries axis = 'dates'; aum_timeseries axis = 'periods'.
"""
from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import re
import sys
from collections import Counter

import boto3
from botocore.exceptions import ClientError

SERVED_BUCKET = "opal-data-portal-v2"
PUBLISHED_BUCKET = "opal-data-assets"
REL_TOL = 0.001
ALLOWED_EXTRAS = {"basis", "meta", "source_vintage_last"}
_DATE_RE = re.compile(r"@\d{4}-\d{2}-\d{2}")

ARTIFACTS = {
    ("aggregate_aua_timeseries", "global"): {
        "served": "json/mdpf/global/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/global/aggregate_aua_timeseries.json"},
    ("aggregate_aua_timeseries", "49financial"): {
        "served": "json/mdpf/49financial/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/49financial/aggregate_aua_timeseries.json"},
    ("aggregate_aua_timeseries", "inflection"): {
        "served": "json/mdpf/inflection/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/inflection/aggregate_aua_timeseries.json"},
    ("account_distribution", "49financial"): {
        "served": "json/mdpf/49financial/account-distribution.json",
        "published": "portal/model-portfolios/49financial/account_distribution.json"},
    ("account_distribution", "inflection"): {
        "served": "json/mdpf/inflection/account-distribution.json",
        "published": "portal/model-portfolios/inflection/account_distribution.json"},
    ("non_model_assets", "global"): {
        "served": "json/portfolios/non_model_assets.json",
        "published": "portal/portfolios/global/non_model_assets.json"},
    ("aum_metrics", "global"): {
        "served": "json/portfolios/aum-metrics.json",
        "published": "portal/portfolios/global/aum_metrics.json"},
    ("aum_timeseries", "global"): {
        "served": "json/portfolios/aum-timeseries.json",
        "published": "portal/portfolios/global/aum_timeseries.json"},
    ("account_distribution", "global"): {
        "served": "json/portfolios/account-distribution.json",
        "published": "portal/portfolios/global/account_distribution.json"},
}


def _s3():
    return boto3.client("s3", region_name="us-east-1")


def _get(bucket, key):
    try:
        return json.loads(_s3().get_object(Bucket=bucket, Key=key)["Body"].read())
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "404", "NoSuchBucket"):
            return None
        raise


def _shape(obj, path=""):
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            out.add(p)
            out |= _shape(v, p)
    elif isinstance(obj, list) and obj:
        out |= _shape(obj[0], f"{path}[]")
    return out


def _shape_diff(served, published):
    s, p = _shape(served), _shape(published)
    missing = sorted(s - p)
    extra = sorted(k for k in p - s if k.split(".")[-1].split("[")[0] not in ALLOWED_EXTRAS)
    return missing, extra


def _axis(obj):
    """The timeseries date axis (a list of date strings) the arrays align to, or None
    for a SNAPSHOT. Prefers 'dates' (mdpf aggregate family), falls back to 'periods'
    (portfolios aum-timeseries). Detecting the axis is what lets date-parallel arrays
    JOIN BY DATE instead of by positional index."""
    if not isinstance(obj, dict):
        return None
    for key in ("dates", "periods"):
        v = obj.get(key)
        if isinstance(v, list) and v and all(isinstance(x, str) for x in v):
            return v
    return None


def _leaves(obj, path="", date=None, axis=None):
    """All numeric AND None leaves -> {path: (value|None, date|None)}. An array whose
    length == len(axis) is DATE-PARALLEL: its elements are keyed by the AXIS DATE
    (path@YYYY-MM-DD) and carry that date, so the served/published leaf sets JOIN BY
    DATE KEY -- never by positional index. All other arrays stay positional (path[i])
    and carry no date. None is recorded (not skipped) so a None-vs-populated NULL
    MISMATCH is DETECTED, never silently dropped."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_leaves(v, f"{path}.{k}" if path else k, date, axis))
    elif isinstance(obj, list) and obj:
        date_parallel = axis is not None and len(obj) == len(axis)
        for i, el in enumerate(obj):
            if date_parallel:
                out.update(_leaves(el, f"{path}@{axis[i]}", axis[i], axis))
            else:
                out.update(_leaves(el, f"{path}[{i}]", date, axis))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out[path] = (float(obj), date)
    elif obj is None:
        out[path] = (None, date)
    return out


def _fieldbase(leafpath):
    """Strip positional [i] AND the date suffix @YYYY-MM-DD so a ledger field_path
    matches the clean field name regardless of index/date keying."""
    return _DATE_RE.sub("", re.sub(r"\[\d+\]", "", leafpath))


def _all_specs(entries):
    """Yield (name, spec) over the ledger; a value may be a single spec dict OR a
    LIST of specs (e.g. history_windows[]). Skips _meta/_note/_date_axis markers."""
    for name, val in entries.items():
        if name.startswith("_"):
            continue
        for spec in (val if isinstance(val, list) else [val]):
            if isinstance(spec, dict):
                yield name, spec


def _spec_is_latest(spec):
    return spec.get("scope") == "latest_cross_section" or any(
        "(latest)" in fp for fp in spec.get("field_paths", []))


def _spec_field_hit(spec, base):
    for fp in spec.get("field_paths", []):
        fp_clean = fp.replace("(latest)", "").strip()
        if fp_clean == base or fp_clean in base or fnmatch.fnmatch(base, fp_clean):
            return True
    return False


def _spec_date_ok(spec, idx_date):
    db, da = spec.get("date_before"), spec.get("date_after")
    if db and idx_date and idx_date >= db:
        return False
    if da and idx_date and idx_date < da:
        return False
    return True


def _spec_band(spec, sign, pct_signed, delta, sv):
    if "pct_range" in spec:                          # SIGNED band (two-sided-safe)
        lo, hi = spec["pct_range"]
        return lo <= pct_signed <= hi
    if "abs" in spec:
        if spec.get("sign", "any") not in ("any", sign):
            return False
        tol = spec.get("tol_pct", 10) / 100.0 * abs(spec["abs"])
        return abs(abs(delta) - abs(spec["abs"])) <= tol
    return False


def _ledger_match(leafpath, idx_date, is_latest, sv, pv, entries):
    """Returns the matching note, or None (UNEXPLAINED). A latest-scoped entry is
    AUTHORITATIVE for a latest leaf: if a latest leaf matches its field but falls
    OUTSIDE its (tight) band, it is UNEXPLAINED -- it does NOT fall through to a
    broader all-date entry (else post_convergence [-1.43,2.08] masks a small latest
    bug the tight model_latest_tie [-0.5,0.5] is meant to catch)."""
    delta = pv - sv
    sign = "+" if delta >= 0 else "-"
    base = _fieldbase(leafpath)
    pct_signed = delta / max(abs(sv), 1.0) * 100.0
    if is_latest:
        latest_field_matched = False
        for name, spec in _all_specs(entries):
            if not _spec_is_latest(spec) or not _spec_field_hit(spec, base):
                continue
            latest_field_matched = True
            if _spec_band(spec, sign, pct_signed, delta, sv):
                return spec.get("note", name)
        if latest_field_matched:
            return None                              # authoritative: out of the tight latest band
    for name, spec in _all_specs(entries):           # general (non-latest-scoped) entries
        if _spec_is_latest(spec):
            continue
        if not _spec_field_hit(spec, base) or not _spec_date_ok(spec, idx_date):
            continue
        if _spec_band(spec, sign, pct_signed, delta, sv):
            return spec.get("note", name)
    return None


def _ledger_null_match(leafpath, idx_date, is_latest, entries):
    """A NULL MISMATCH (exactly one side None) is NAMED only by a ledger entry marking
    the field null_ok (a co-sign-gated placeholder that wires + ties at cutover); else
    it is UNEXPLAINED -- never silently skipped."""
    base = _fieldbase(leafpath)
    for name, spec in _all_specs(entries):
        if not spec.get("null_ok") or not _spec_field_hit(spec, base):
            continue
        if _spec_is_latest(spec) and not is_latest:
            continue
        if not _spec_date_ok(spec, idx_date):
            continue
        return spec.get("note", name)
    return None


def _axis_deltas(saxis, paxis, date_axis_spec):
    """Symmetric diff of the two date axes -> named vs unexplained STRUCTURAL deltas.
    A served-only / published-only date is EXPECTED iff listed in the ledger's
    _date_axis {served_only:[], published_only:[]} entry; otherwise UNEXPLAINED
    (fail-safe -- NEVER silently dropped). Also flags duplicate axis dates (a real
    anomaly a positional/date overwrite would otherwise hide)."""
    named_so = set(date_axis_spec.get("served_only", []))
    named_po = set(date_axis_spec.get("published_only", []))
    sset, pset = set(saxis), set(paxis)
    served_only = sorted(sset - pset)
    published_only = sorted(pset - sset)
    sc, pc = Counter(saxis), Counter(paxis)
    dupes = sorted({d for d, c in sc.items() if c > 1} | {d for d, c in pc.items() if c > 1})
    return {
        "common": sorted(sset & pset),
        "served_only_named": [d for d in served_only if d in named_so],
        "served_only_unexplained": [d for d in served_only if d not in named_so],
        "published_only_named": [d for d in published_only if d in named_po],
        "published_only_unexplained": [d for d in published_only if d not in named_po],
        "dupes": dupes,
    }


def compare(served, published, entries=None):
    entries = entries or {}
    missing, extra = _shape_diff(served, published)
    saxis, paxis = _axis(served), _axis(published)
    ls = _leaves(served, axis=saxis)
    lp = _leaves(published, axis=paxis)
    expected, unexplained = [], []
    axis = None

    # --- DATE AXIS: surface EVERY non-common date (NEVER silent-skip) ---
    if bool(saxis) != bool(paxis):
        # one side is a timeseries and the other is not -- a gross structural mismatch, LOUD.
        unexplained.append(("_axis_presence_mismatch",
                            "timeseries" if saxis else "snapshot",
                            "timeseries" if paxis else "snapshot", None))
        ls, lp = _leaves(served), _leaves(published)   # fall back to positional so we still compare
    elif saxis and paxis:
        ax = _axis_deltas(saxis, paxis, entries.get("_date_axis", {}))
        axis = {"common": len(ax["common"]),
                "last_common": ax["common"][-1] if ax["common"] else None,
                "served_only_named": ax["served_only_named"],
                "served_only_unexplained": ax["served_only_unexplained"],
                "published_only_named": ax["published_only_named"],
                "published_only_unexplained": ax["published_only_unexplained"],
                "dupes": ax["dupes"]}
        for d in ax["served_only_named"]:
            expected.append((f"axis@{d}", "served-only", "absent", "named served-only (_date_axis)"))
        for d in ax["published_only_named"]:
            expected.append((f"axis@{d}", "absent", "published-only", "named published-only (_date_axis)"))
        for d in ax["served_only_unexplained"]:
            unexplained.append((f"axis@{d}", "served-only", "absent", None))
        for d in ax["published_only_unexplained"]:
            unexplained.append((f"axis@{d}", "absent", "published-only", None))
        for d in ax["dupes"]:
            unexplained.append((f"axis@{d} DUPLICATE", "dup", "dup", None))

    last_common = axis["last_common"] if axis else None

    # --- VALUE comparison over the common (date-aligned) leaves ---
    for k in sorted(set(ls) & set(lp)):
        sv, sdt = ls[k]
        pv, _ = lp[k]
        idx_date = sdt
        is_latest = (idx_date is None) or (idx_date == last_common)
        if sv is None and pv is None:
            continue
        if isinstance(sv, float) and isinstance(pv, float):
            if abs(sv - pv) / max(abs(sv), 1.0) <= REL_TOL:
                continue
            note = _ledger_match(k, idx_date, is_latest, sv, pv, entries)
        else:                                        # NULL MISMATCH (exactly one side None)
            note = _ledger_null_match(k, idx_date, is_latest, entries)
        (expected if note else unexplained).append((k, sv, pv, note))
    return {"missing": missing, "extra": extra, "expected": expected, "unexplained": unexplained,
            "shape_ok": not (missing or extra), "axis": axis}


def check_pair(name, firm, spec, ledger):
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        return {"name": name, "firm": firm, "verdict": "SERVED_ABSENT", "note": spec["served"]}
    published = _get(PUBLISHED_BUCKET, spec["published"])
    if published is None:
        return {"name": name, "firm": firm, "verdict": "PUBLISHED_ABSENT",
                "note": f"{spec['published']} absent (awaiting publisher); served shape {len(_shape(served))} paths"}
    entries = (ledger or {}).get(f"{name}/{firm}", {})
    r = compare(served, published, entries)
    if not r["shape_ok"]:
        r["verdict"] = "SHAPE_FAIL"
    elif r["unexplained"]:
        r["verdict"] = "UNEXPLAINED_DELTA"
    elif r["expected"]:
        r["verdict"] = "NAMED_DELTA_PASS"
    else:
        r["verdict"] = "PASS"
    r["name"], r["firm"], r["ledger_n"] = name, firm, len([k for k in entries if not k.startswith("_")])
    return r


def self_test():
    spec = ARTIFACTS[("account_distribution", "49financial")]
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        print("SELF-TEST: cannot fetch served TO-3 -- SKIP")
        return None
    ok = True
    ident = compare(served, served)
    ok &= ident["shape_ok"] and not ident["expected"] and not ident["unexplained"]
    mut = copy.deepcopy(served)
    mut["total"]["account_count"] += 100
    ok &= bool(compare(served, mut)["unexplained"])
    # DS-format ledger over a synthetic timeseries (len 2 == dates -> DATE-PARALLEL, keyed @date)
    ts_s = {"dates": ["2025-06-01", "2026-06-01"], "model_aua": [100.0, 200.0], "x": [50.0, 60.0]}
    ts_p = {"dates": ["2025-06-01", "2026-06-01"], "model_aua": [120.0, 204.1], "x": [50.0, 90.0]}  # [@25]:+20% hist; [@26]:+4.1 latest
    led = {
        "history_windows": [  # DS's LIST format -- per-quarter windows
            {"field_paths": ["model_aua"], "sign": "+", "pct_range": [10, 40], "date_after": "2025-01-01", "date_before": "2026-01-01", "note": "Q window"},
        ],
        "latest_abs": {"field_paths": ["model_aua(latest)"], "sign": "+", "abs": 4.1, "tol_pct": 5, "note": "latest abs"},
    }
    r = compare(ts_s, ts_p, led)
    exp_win = any(k == "model_aua@2025-06-01" for k, *_ in r["expected"])     # +20% in-window (LIST) -> EXPECTED
    exp_latest = any(k == "model_aua@2026-06-01" for k, *_ in r["expected"])  # +4.1 latest -> latest-scoped abs entry
    unexp = any(k == "x@2026-06-01" for k, *_ in r["unexplained"])            # +50% unrelated -> UNEXPLAINED
    # authoritative-latest: a latest delta OUT of the tight latest band must NOT be masked by a broader all-date band
    tsa_s = {"dates": ["2026-05-01", "2026-06-01"], "model_aua": [100.0, 100.0]}
    tsa_p = {"dates": ["2026-05-01", "2026-06-01"], "model_aua": [100.0, 101.5]}  # latest +1.5%
    leda = {"latest_tie": {"field_paths": ["model_aua(latest)"], "scope": "latest_cross_section", "pct_range": [-0.5, 0.5], "note": "tie"},
            "post_conv": {"field_paths": ["model_aua"], "pct_range": [-1.43, 2.08], "date_after": "2026-04-09", "note": "postconv"}}
    auth = any(k == "model_aua@2026-06-01" for k, *_ in compare(tsa_s, tsa_p, leda)["unexplained"])
    # null-placeholder: a None-vs-populated mismatch is DETECTED; NAMED iff a null_ok entry names it, else UNEXPLAINED
    tsn_s = {"dates": ["2025-06-01"], "by_model": {"UST": {"account_count": [180.0], "model_value": [100.0]}}}
    tsn_p = {"dates": ["2025-06-01"], "by_model": {"UST": {"account_count": [None], "model_value": [100.0]}}}
    lednull = {"count_ph": {"field_paths": ["by_model.*.account_count"], "null_ok": True, "note": "placeholder"}}
    null_named = any(k.endswith("account_count@2025-06-01") for k, *_ in compare(tsn_s, tsn_p, lednull)["expected"])
    null_unexp = any(k.endswith("account_count@2025-06-01") for k, *_ in compare(tsn_s, tsn_p, {})["unexplained"])

    # ================= DATE-JOIN proof (CTO 135429Z MUST-FIX) =================
    # served has B (2025-02-01) published lacks; published has T (2026-07-20) served lacks.
    # An INDEX-join would compare served model_aua[1]=20 (2025-02-01) vs published [1]=30 (2026-06-02)
    # -> a spurious value "mismatch", AND silently drop served[2]=30. Date-join must instead TIE the
    # two COMMON dates and SURFACE the two frontier dates.
    dj_s = {"dates": ["2025-01-02", "2025-02-01", "2026-06-02"], "model_aua": [10.0, 20.0, 30.0]}
    dj_p = {"dates": ["2025-01-02", "2026-06-02", "2026-07-20"], "model_aua": [10.0, 30.0, 44.0]}
    dj_led = {"_date_axis": {"served_only": ["2025-02-01"], "published_only": ["2026-07-20"]}}
    dj = compare(dj_s, dj_p, dj_led)
    dj_no_spurious = not any(str(k).startswith("model_aua@") for k, *_ in dj["unexplained"])   # (a) common ties, no wrong-date mismatch
    dj_axis_named = (dj["axis"]["served_only_named"] == ["2025-02-01"]
                     and dj["axis"]["published_only_named"] == ["2026-07-20"])                  # (b) non-common SURFACED as NAMED
    dj_last_common = dj["axis"]["last_common"] == "2026-06-02"                                  # (c) last-common != published [-1]=2026-07-20
    # fail-safe: WITHOUT the _date_axis ledger the same non-common dates are UNEXPLAINED (reported, NOT dropped)
    dj_bare = compare(dj_s, dj_p, {})
    dj_reports_unnamed = (any(k == "axis@2025-02-01" for k, *_ in dj_bare["unexplained"])
                          and any(k == "axis@2026-07-20" for k, *_ in dj_bare["unexplained"]))
    # a REAL delta at a COMMON date is CAUGHT at the RIGHT date (99 vs 30 at 2026-06-02)
    dj_p2 = {"dates": ["2025-01-02", "2026-06-02", "2026-07-20"], "model_aua": [10.0, 99.0, 44.0]}
    dj2 = compare(dj_s, dj_p2, dj_led)
    dj_common_delta_caught = any(k == "model_aua@2026-06-02" for k, *_ in dj2["unexplained"])

    ok &= (exp_win and exp_latest and unexp and auth and null_named and null_unexp
           and dj_no_spurious and dj_axis_named and dj_last_common
           and dj_reports_unnamed and dj_common_delta_caught)
    print(f"SELF-TEST snapshot identity+mutant: {ident['shape_ok'] and not ident['unexplained']} / {bool(compare(served, mut)['unexplained'])}")
    print(f"SELF-TEST DS-ledger: history_windows-LIST(model_aua@2025)={exp_win}; latest-scope(model_aua@2026)={exp_latest}; UNEXPLAINED(x@2026)={unexp}")
    print(f"SELF-TEST authoritative-latest: +1.5% latest out-of-tie NOT masked by post_conv -> UNEXPLAINED={auth}")
    print(f"SELF-TEST null-placeholder: null_ok->NAMED={null_named}; no-entry->UNEXPLAINED(NOT silently skipped)={null_unexp}")
    print(f"SELF-TEST DATE-JOIN: common-ties/no-spurious-index-mismatch={dj_no_spurious}; non-common NAMED-surfaced={dj_axis_named}; last_common@2026-06-02(not [-1])={dj_last_common}")
    print(f"SELF-TEST DATE-JOIN fail-safe: unnamed non-common -> UNEXPLAINED(reported,not dropped)={dj_reports_unnamed}; real common-date delta CAUGHT at right date={dj_common_delta_caught}")
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'} -- date-joins by date key, surfaces every non-common date, ties at last-common")
    return ok


def _fmt(v):
    return f"{v:,.2f}" if isinstance(v, float) else str(v)   # None-safe


def _report(r):
    v = r["verdict"]
    head = f"[{v}] {r['name']}/{r['firm']}" + (f" (ledger:{r.get('ledger_n',0)})" if "ledger_n" in r else "")
    if v in ("SERVED_ABSENT", "PUBLISHED_ABSENT"):
        print(f"{head} -- {r['note']}")
        return
    print(head)
    ax = r.get("axis")
    if ax:
        print(f"    (axis) {ax['common']} common | last_common={ax['last_common']} | "
              f"served-only {len(ax['served_only_named'])} named"
              + (f" + {len(ax['served_only_unexplained'])} UNEXPLAINED" if ax['served_only_unexplained'] else "")
              + f" | published-only {len(ax['published_only_named'])} named"
              + (f" + {len(ax['published_only_unexplained'])} UNEXPLAINED" if ax['published_only_unexplained'] else "")
              + (f" | DUPLICATES {ax['dupes']}" if ax['dupes'] else ""))
        if ax["served_only_unexplained"]:
            print(f"        served-only UNEXPLAINED: {ax['served_only_unexplained'][:8]}")
        if ax["published_only_unexplained"]:
            print(f"        published-only UNEXPLAINED: {ax['published_only_unexplained'][:8]}")
    if r["missing"]:
        print(f"    (a) SHAPE MISSING: {r['missing'][:6]}{' ...+%d' % (len(r['missing'])-6) if len(r['missing'])>6 else ''}")
    if r["extra"]:
        print(f"    (a) SHAPE EXTRA: {r['extra'][:6]}{' ...+%d' % (len(r['extra'])-6) if len(r['extra'])>6 else ''}")
    for k, sv, pv, note in r["expected"][:10]:
        print(f"    (b) NAMED {k}: {_fmt(sv)}->{_fmt(pv)} [{note}]")
    if len(r["expected"]) > 10:
        print(f"    (b) ...+{len(r['expected'])-10} more named")
    for k, sv, pv, _ in r["unexplained"][:12]:
        print(f"    (c) UNEXPLAINED {k}: {_fmt(sv)}->{_fmt(pv)}")
    if len(r["unexplained"]) > 12:
        print(f"    (c) ...+{len(r['unexplained'])-12} more UNEXPLAINED")
    if v == "PASS":
        print("    shape identical + all values tie")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact")
    ap.add_argument("--firm")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ledger")
    args = ap.parse_args()
    if args.self_test:
        return 0 if self_test() else 1
    ledger = None
    if args.ledger:
        with open(args.ledger, encoding="utf-8") as fh:
            ledger = json.load(fh)
    if args.all:
        for (name, firm), spec in ARTIFACTS.items():
            _report(check_pair(name, firm, spec, ledger))
        return 0
    if args.artifact and args.firm:
        spec = ARTIFACTS.get((args.artifact, args.firm))
        if not spec:
            print(f"no in-scope artifact ({args.artifact}, {args.firm})")
            return 1
        _report(check_pair(args.artifact, args.firm, spec, ledger))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
