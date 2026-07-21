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
non_model_assets is ROW-oriented (time_series[] of dicts + latest{}, NO top-level dates[]) -> axis is
DERIVED from time_series[].period (it is the portal's parity contract; must not be restructured).
SHAPE: the meta/source_vintage_last PROVENANCE subtrees are EXEMPT from the missing/extra
shape-diff (their keys legitimately differ served-vs-revamp; the DATA-array shape is checked).
VALUE: leaves UNDER those provenance ROOTS are ALSO exempt from the value compare -- their values
(age_hours_at_generation/lag/threshold/generated_at) are run-time, so served-vs-revamp differs by
construction. ROOT-only (_provenance_value_exempt), NOT the leaf-NAME clause -- a numeric data leaf
named after a provenance token (e.g. 'basis') is STILL value-checked (a false PASS is the danger).
FIELD MATCH is EXACT-or-glob (never substring) -- a 'model_aua' entry must not intercept a
'non_model_aua' leaf. --published-prefix points the compare at a staged pre-publish location.
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
ALLOWED_EXTRAS = {"basis", "meta", "source_vintage_last"}   # leaf-name spec extras (published-side, any depth)
SHAPE_EXEMPT_ROOTS = {"meta", "source_vintage_last"}        # provenance subtrees: keys legitimately differ served-vs-revamp
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
    ("aum_metrics", "global"): {   # A1: DS builds a revamp producer -> parity artifact coming (CTO 203613Z)
        "served": "json/portfolios/aum-metrics.json",
        "published": "portal/portfolios/global/aum_metrics.json"},
    # aum_timeseries (A2) REMOVED (CTO 203613Z scope ruling): FE-DERIVE now, stale legacy dropped from the FE
    # -> the revamp produces NO aum-timeseries artifact, so there is nothing to parity-check (it left the
    # picture entirely). Do NOT re-add a target that will only ever read PUBLISHED_ABSENT. Coverage = 8 keys.
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


def _shape_exempt(p):
    """A shape path exempt from the missing/extra diff: any leaf named in ALLOWED_EXTRAS, OR
    any path under a provenance subtree (meta / source_vintage_last) whose keys legitimately
    differ between served and the revamp (DS harness_requirement, 2026-07-21). The DATA-array
    shape is still fully checked -- only provenance metadata is exempt."""
    return (p.split(".")[0].split("[")[0] in SHAPE_EXEMPT_ROOTS
            or p.split(".")[-1].split("[")[0] in ALLOWED_EXTRAS)


def _provenance_value_exempt(p):
    """VALUE-loop exemption (BUG-1 value-side completion, DS harness_requirement 2026-07-21). A numeric leaf
    UNDER a provenance root (meta / source_vintage_last) carries a RUN-TIME-dependent value --
    age_hours_at_generation (= generated_at - source overall), lag, threshold, generated_at -- that
    legitimately differs served-vs-revamp. Provenance is not data; it must not be a parity leaf.
    DELIBERATELY NARROWER than _shape_exempt: ROOT-only, it does NOT include the ALLOWED_EXTRAS leaf-NAME
    clause -- because _leaves records NUMERIC leaves, a numeric DATA figure that happens to share an extras
    name (e.g. a 'basis' value present on both sides) must STILL be value-checked. Exempting a provenance
    SUBTREE must never silently exempt a data leaf BY NAME (a false PASS is the dangerous error here)."""
    return p.split(".")[0].split("[")[0] in SHAPE_EXEMPT_ROOTS


def _shape_diff(served, published):
    s, p = _shape(served), _shape(published)
    missing = sorted(k for k in (s - p) if not _shape_exempt(k))   # was unfiltered -> false SHAPE_FAIL on meta.*
    extra = sorted(k for k in (p - s) if not _shape_exempt(k))
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
    # non_model_assets class (DS~A 2026-07-21): a ROW-oriented timeseries -- top-level time_series[] of
    # dicts each carrying its own 'period' (latest{} holds the cross-section), NO top-level dates[]/periods[].
    # Derive the axis from the row periods so time_series[i] date-JOINS by period. The portal reads this
    # time_series[] shape (portal-proxy.ts NonModelAssetsResponse{latest,time_series[]}) -- it IS the parity
    # contract; restructuring A4 to dates[]+arrays would break the page (Path 1 rejected, source-confirmed).
    ts = obj.get("time_series")
    if isinstance(ts, list) and ts and all(isinstance(r, dict) and isinstance(r.get("period"), str) for r in ts):
        return [r["period"] for r in ts]
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
    """Exact-or-glob field match. NOT substring: `fp_clean in base` wrongly matched 'model_aua'
    inside 'non_model_aua' -> model_latest_tie's tight band intercepted non_model (DS flag,
    2026-07-21). '*' globs (by_model.*.model_value) still match via fnmatch."""
    for fp in spec.get("field_paths", []):
        fp_clean = fp.replace("(latest)", "").strip()
        if base == fp_clean or fnmatch.fnmatch(base, fp_clean):
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
        if _provenance_value_exempt(k):    # provenance values (age_hours_at_generation/lag/threshold/generated_at) are run-time -> never a parity leaf
            continue
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


def check_pair(name, firm, spec, ledger, published_prefix=None):
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        return {"name": name, "firm": firm, "verdict": "SERVED_ABSENT", "note": spec["served"]}
    # --published-prefix points at a staged pre-publish location -> {prefix}/{firm}/{artifact}.json
    pub_key = f"{published_prefix}/{firm}/{name}.json" if published_prefix else spec["published"]
    published = _get(PUBLISHED_BUCKET, pub_key)
    if published is None:
        return {"name": name, "firm": firm, "verdict": "PUBLISHED_ABSENT",
                "note": f"{pub_key} absent (awaiting publisher); served shape {len(_shape(served))} paths"}
    entries = (ledger or {}).get(f"{name}/{firm}", {})
    r = compare(served, published, entries)
    r["published_key"] = pub_key
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


def _coherence_mismatches(agg, ad):
    """Pure frontier-coherence comparator (S3-free, unit-testable). CTO 190518Z (a): the revamp aggregate's
    FRONTIER per-model account_count must equal account_dist's OWN funded count. Returns
    [(model_key, aggregate_frontier, account_dist_count)] for every funded model that does NOT cohere.
    Keyed by STABLE model_key from account_dist.meta.account_count_by_model_key (kills the 49F/global
    display-key trap); SMAs carry no funded count -> absent from the meta-map -> auto-skipped. FRONTIER-ONLY
    (only [-1]); middle published-only gaps are honest-None BY DESIGN and NOT checked. A None meta count is
    skipped; a None frontier vs a real count is a (frozen-None) mismatch -- account_dist HAS the count today."""
    acbmk = (ad.get("meta") or {}).get("account_count_by_model_key") or {}
    by_model = agg.get("by_model") or {}
    out = []
    for mkey, count_ad in acbmk.items():
        if count_ad is None:
            continue
        series = (by_model.get(mkey) or {}).get("account_count")
        frontier = series[-1] if isinstance(series, list) and series else None
        if frontier != count_ad:
            out.append((mkey, frontier, count_ad))
    return out


def check_frontier_coherence(firm, published_prefix=None):
    """INDEPENDENT verification (verification-side, separate from DS's producer ASSERTs) that the frontier
    account_count coherence-by-construction held: loads the STAGED aggregate + account_dist and asserts each
    funded model's aggregate.account_count[-1] == account_dist.meta.account_count_by_model_key[model_key]."""
    def _staged(name):
        key = f"{published_prefix}/{firm}/{name}.json" if published_prefix else ARTIFACTS[(name, firm)]["published"]
        return _get(PUBLISHED_BUCKET, key), key
    agg, agg_key = _staged("aggregate_aua_timeseries")
    ad, ad_key = _staged("account_distribution")
    if agg is None or ad is None:
        return {"firm": firm, "verdict": "COHERENCE_ABSENT",
                "note": f"aggregate={'ok' if agg else 'MISSING'} / account_dist={'ok' if ad else 'MISSING'}"}
    if not (ad.get("meta") or {}).get("account_count_by_model_key"):
        return {"firm": firm, "verdict": "COHERENCE_NO_MAP",
                "note": f"{ad_key} has no meta.account_count_by_model_key (pre-coherence stage -> re-stage account_dist)"}
    mism = _coherence_mismatches(agg, ad)
    checked = len([1 for v in (ad["meta"]["account_count_by_model_key"]).values() if v is not None])
    return {"firm": firm, "verdict": "COHERENCE_PASS" if not mism else "COHERENCE_FAIL",
            "checked": checked, "mismatches": mism, "agg_key": agg_key, "ad_key": ad_key}


def _coherence_firms():
    aggs = {f for (n, f) in ARTIFACTS if n == "aggregate_aua_timeseries"}
    ads = {f for (n, f) in ARTIFACTS if n == "account_distribution"}
    return sorted(aggs & ads)


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

    # ===== REGRESSION: two bugs DS hit on the real staged run (2026-07-21) =====
    # BUG-1: a diff confined to the meta/source_vintage_last provenance subtrees must NOT SHAPE_FAIL
    m_s = {"dates": ["2026-06-01"], "model_aua": [10.0],
           "meta": {"backfill_methods": ["a"]}, "source_vintage_last": {"vintage_bearing_feeders": ["x", "y"]}}
    m_p = {"dates": ["2026-06-01"], "model_aua": [10.0],
           "meta": {"provenance": "revamp", "extra": 1}, "source_vintage_last": {"vintage_bearing_feeders": ["x"], "new": 2}}
    meta_shape_ok = compare(m_s, m_p)["shape_ok"]                       # provenance-only diff -> shape OK
    m_p_realdiff = {"dates": ["2026-06-01"], "model_aua": [10.0], "rogue_data_field": [1.0], "meta": {}}
    real_shape_still_fails = not compare(m_s, m_p_realdiff)["shape_ok"]  # a real DATA-shape diff still FAILS
    # BUG-1 VALUE SIDE (DS 2026-07-21): a numeric leaf UNDER a provenance root (meta/source_vintage_last)
    # present on BOTH sides with a run-time-different value must NOT be UNEXPLAINED (age_hours 15.0 vs 42.2);
    # AND a numeric DATA leaf NAMED 'basis' (a provenance token, but at a DATA root) must STILL be caught --
    # proves the value-exemption is ROOT-only, not the leaf-NAME clause (a false PASS is the dangerous error).
    pv_s = {"dates": ["2026-06-01"], "model_aua": [10.0],
            "meta": {"source_vintage_last": {"age_hours_at_generation": 15.0, "basis": "schwab-rps"}}, "basis": 200.0}
    pv_p = {"dates": ["2026-06-01"], "model_aua": [10.0],
            "meta": {"source_vintage_last": {"age_hours_at_generation": 42.2, "basis": "schwab-rps"}}, "basis": 999.0}
    pv_r = compare(pv_s, pv_p)
    prov_value_exempt = not any(str(k).startswith("meta") for k, *_ in pv_r["unexplained"])   # age_hours 15->42.2 NOT flagged
    basis_data_still_caught = any(k == "basis" for k, *_ in pv_r["unexplained"])              # numeric 'basis' at data root STILL flagged
    # A4 non_model_assets CLASS (DS~A 2026-07-21): a ROW-oriented time_series[]+latest{} artifact (no
    # top-level dates[]) -- _axis must DERIVE the axis from time_series[].period so leaves date-JOIN by
    # period (not read positional/latest-only). Pre-cutover row ties; a post-cutover delta lands at its date.
    a4_s = {"latest": {"date": "2026-06-02", "enterprise_total": 200.0},
            "time_series": [{"period": "2025-06-02", "enterprise_total": 10.0},
                            {"period": "2026-06-02", "enterprise_total": 200.0}]}
    a4_axis_derived = (_axis(a4_s) == ["2025-06-02", "2026-06-02"])           # axis DERIVED from time_series[].period
    a4_p = {"latest": {"date": "2026-06-02", "enterprise_total": 260.0},
            "time_series": [{"period": "2025-06-02", "enterprise_total": 10.0},
                            {"period": "2026-06-02", "enterprise_total": 260.0}]}
    a4_r = compare(a4_s, a4_p, {"w": {"field_paths": ["*.enterprise_total"], "date_after": "2026-01-01",
                                      "pct_range": [20, 40], "note": "post-cutover enterprise"}})
    a4_precut_ties = not any("@2025-06-02" in str(k) for k, *_ in a4_r["unexplained"])         # pre-cutover row ties (10==10)
    a4_post_datejoined = any("@2026-06-02" in str(k) for k, *_ in a4_r["expected"])            # +30% delta DATE-JOINED @2026-06-02, glob-named (not positional/UNEXPLAINED)
    # ITEM-2 FRONTIER COHERENCE (CTO 190518Z (a)): _coherence_mismatches -- aggregate.by_model[mkey].
    # account_count[-1] == account_dist.meta.account_count_by_model_key[mkey]; frontier-only; SMAs (absent
    # from the meta-map) auto-skipped; a value mismatch OR a frozen-None frontier is a mismatch.
    coh_agg = {"by_model": {"ModelA": {"account_count": [None, 100, 246]},
                            "ModelB": {"account_count": [None, None, 50]},
                            "SMA_x":  {"account_count": [None, None, None]}}}
    coh_map = {"meta": {"account_count_by_model_key": {"ModelA": 246, "ModelB": 50}}}          # SMA_x absent -> skipped
    coh_clean = _coherence_mismatches(coh_agg, coh_map) == []                                  # coherent -> no mismatch
    coh_sma_skipped = not any(m[0] == "SMA_x" for m in _coherence_mismatches(coh_agg, coh_map))  # SMA never checked
    coh_val_caught = ("ModelA", 246, 999) in _coherence_mismatches(
        coh_agg, {"meta": {"account_count_by_model_key": {"ModelA": 999, "ModelB": 50}}})      # value mismatch caught
    coh_frozen_caught = any(m[0] == "ModelA" and m[1] is None for m in _coherence_mismatches(
        {"by_model": {"ModelA": {"account_count": [None, None, None]}}},
        {"meta": {"account_count_by_model_key": {"ModelA": 246}}}))                            # frozen-None frontier caught
    # BUG-2: a 'model_aua'-scoped entry must NOT intercept a 'non_model_aua' leaf (exact match, not substring)
    nm_s = {"dates": ["2026-06-01"], "non_model_aua": [100.0]}
    nm_p = {"dates": ["2026-06-01"], "non_model_aua": [150.0]}          # +50% non_model delta
    nm_led = {"model_only": {"field_paths": ["model_aua(latest)"], "scope": "latest_cross_section",
                             "pct_range": [-0.5, 0.5], "note": "model tie"}}
    nm_not_masked = any(k == "non_model_aua@2026-06-01" for k, *_ in compare(nm_s, nm_p, nm_led)["unexplained"])

    ok &= (exp_win and exp_latest and unexp and auth and null_named and null_unexp
           and dj_no_spurious and dj_axis_named and dj_last_common
           and dj_reports_unnamed and dj_common_delta_caught
           and meta_shape_ok and real_shape_still_fails
           and prov_value_exempt and basis_data_still_caught
           and a4_axis_derived and a4_precut_ties and a4_post_datejoined
           and coh_clean and coh_sma_skipped and coh_val_caught and coh_frozen_caught and nm_not_masked)
    print(f"SELF-TEST snapshot identity+mutant: {ident['shape_ok'] and not ident['unexplained']} / {bool(compare(served, mut)['unexplained'])}")
    print(f"SELF-TEST DS-ledger: history_windows-LIST(model_aua@2025)={exp_win}; latest-scope(model_aua@2026)={exp_latest}; UNEXPLAINED(x@2026)={unexp}")
    print(f"SELF-TEST authoritative-latest: +1.5% latest out-of-tie NOT masked by post_conv -> UNEXPLAINED={auth}")
    print(f"SELF-TEST null-placeholder: null_ok->NAMED={null_named}; no-entry->UNEXPLAINED(NOT silently skipped)={null_unexp}")
    print(f"SELF-TEST DATE-JOIN: common-ties/no-spurious-index-mismatch={dj_no_spurious}; non-common NAMED-surfaced={dj_axis_named}; last_common@2026-06-02(not [-1])={dj_last_common}")
    print(f"SELF-TEST DATE-JOIN fail-safe: unnamed non-common -> UNEXPLAINED(reported,not dropped)={dj_reports_unnamed}; real common-date delta CAUGHT at right date={dj_common_delta_caught}")
    print(f"SELF-TEST regression BUG-1 (meta/svl subtree exempt from shape): provenance-diff shape-OK={meta_shape_ok}; real data-shape diff still FAILS={real_shape_still_fails}")
    print(f"SELF-TEST regression BUG-1 VALUE (root-only exemption): provenance value diff (age_hours 15->42.2) NOT unexplained={prov_value_exempt}; numeric data leaf named 'basis' STILL caught={basis_data_still_caught}")
    print(f"SELF-TEST A4 non_model_assets CLASS (time_series[].period axis): axis-derived={a4_axis_derived}; pre-cutover ties={a4_precut_ties}; post-cutover delta date-joined+named={a4_post_datejoined}")
    print(f"SELF-TEST Item-2 frontier coherence: coherent-clean={coh_clean}; SMA auto-skipped={coh_sma_skipped}; value-mismatch caught={coh_val_caught}; frozen-None frontier caught={coh_frozen_caught}")
    print(f"SELF-TEST regression BUG-2 (exact field match, no substring): 'model_aua' entry does NOT mask 'non_model_aua'={nm_not_masked}")
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


def _report_coherence(r):
    v = r["verdict"]
    if v in ("COHERENCE_ABSENT", "COHERENCE_NO_MAP"):
        print(f"[{v}] frontier_coherence/{r['firm']} -- {r['note']}")
        return
    print(f"[{v}] frontier_coherence/{r['firm']} (funded models:{r['checked']})")
    for mkey, frontier, count_ad in r.get("mismatches", [])[:12]:
        fstr = _fmt(float(frontier)) if frontier is not None else "None(frozen)"
        print(f"    (coh) MISMATCH {mkey}: aggregate.frontier={fstr} != account_dist={_fmt(float(count_ad))}")
    if v == "COHERENCE_PASS":
        print("    aggregate frontier account_count == account_dist funded count, every funded model")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact")
    ap.add_argument("--firm")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ledger")
    ap.add_argument("--published-prefix",
                    help="override published key -> {prefix}/{firm}/{artifact}.json "
                         "(e.g. gold/mdpf_revamp for a staged pre-publish parity run)")
    args = ap.parse_args()
    if args.self_test:
        return 0 if self_test() else 1
    ledger = None
    if args.ledger:
        with open(args.ledger, encoding="utf-8") as fh:
            ledger = json.load(fh)
    if args.all:
        for (name, firm), spec in ARTIFACTS.items():
            _report(check_pair(name, firm, spec, ledger, args.published_prefix))
        for firm in _coherence_firms():                          # CTO Item-2: frontier account_count coherence
            _report_coherence(check_frontier_coherence(firm, args.published_prefix))
        return 0
    if args.artifact and args.firm:
        spec = ARTIFACTS.get((args.artifact, args.firm))
        if not spec:
            print(f"no in-scope artifact ({args.artifact}, {args.firm})")
            return 1
        _report(check_pair(args.artifact, args.firm, spec, ledger, args.published_prefix))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
