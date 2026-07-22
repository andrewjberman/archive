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
SHAPE: the meta/source_vintage_last/cohort_provenance PROVENANCE subtrees are EXEMPT from the
missing/extra shape-diff (their keys legitimately differ served-vs-revamp; the DATA-array shape is
checked). cohort_provenance is revamp-only (49f+inflection; global omits) -- a NAMED intended delta.
VALUE: leaves UNDER those provenance ROOTS are ALSO exempt from the value compare -- their values
(age_hours_at_generation/lag/threshold/generated_at) are run-time, so served-vs-revamp differs by
construction. ROOT-only (_provenance_value_exempt), NOT the leaf-NAME clause -- a numeric data leaf
named after a provenance token (e.g. 'basis') is STILL value-checked (a false PASS is the danger).
FIELD MATCH is EXACT-or-glob (never substring) -- a 'model_aua' entry must not intercept a
'non_model_aua' leaf. --published-prefix points the compare at a staged pre-publish location.

=================== INTERNAL-CONSISTENCY GATE (--consistency), 2026-07-22 ===================
PARITY IS NOT CONSISTENCY. Everything above compares SERVED to PUBLISHED. A defect present on
BOTH sides ties perfectly and passes -- so a clean 3/3 parity gate says nothing about whether
either side is internally correct. That is not a hypothetical: my date-joined leg was honestly
CLEAN (CTO confirmed 3/3, 2026-07-22 000840Z) while live Global was internally wrong.

  INVARIANT   total == model_aua + non_model_aua, PER FIRM, PER DATE.
  TOTAL FIELD resolved by PRESENCE, measured not assumed -- global carries `opal_aggregate_aua`;
              49financial/inflection carry `partner_custody_total`. A gate hard-coded to the
              global field would silently no-op on 2 of 3 firms while reporting a clean sweep.
  NULLS       absent is NOT zero (zero-filling makes the exact live hole tie perfectly). All
              three None -> honest-None row, skipped + counted. SOME None -> PARTIAL_NULL FAIL.
  TOLERANCE   $1.00 absolute floor. USD sums at ~1e9 in float64 carry ~1e-6 genuine FP noise, so
              the floor sits ~6 orders above it. The mutant test MEASURES and PRINTS the achieved
              floor ($1.01) -- a gate whose sensitivity is unstated cannot be relied on.
  CROSS-FIRM  companion check (BEYOND the routed per-firm ask, flagged so it can be accepted or
              rejected independently): global component == sum(partner components), date-joined.
              Catches a firm dropping out of the roll-up -- the LD-0292 class.
  EXERCISED   every clause is mutant-gated (Rule 22a): seeded defects must turn it RED, and a
              coherent control must still turn it GREEN. A gate that has never failed a seeded
              defect has never been tested; an instrument that cannot pass is equally broken.
  RC          --consistency returns 1 on ANY violation, INCLUDING uncheckable states (absent
              artifact / absent total field). UNCHECKABLE IS NOT A PASS. --all now also reflects
              this in its rc (it previously always returned 0); the parity verdicts still do not.
  --served    runs the same invariant against the LEGACY LIVE artifacts, so "is what we serve
              today correct?" is answerable by the same instrument, not an ad-hoc script.

KNOWN RESIDUALS -- what this gate CANNOT see (CVO adversarial pass, ACCEPTED-CVO 2026-07-22).
An instrument whose limits are unstated invites over-trust, so they are named here, not omitted:
  (1) A COMPENSATING ERROR at one firm (model +$50M / non_model -$50M, total unchanged) passes the
      per-firm identity BY DESIGN -- the identity constrains the sum, not the split. The cross-firm
      per-field check catches it when the shift is firm-vs-rollup, which is why cross-firm is KEPT
      (CVO Q3: it is the LOCALIZER, not scope creep -- CROSSFIRM_PASS on both sides is exactly what
      pinned the 2026-07-22 P0 to opal_aggregate_aua's COMPOSITION rather than the roll-up).
  (2) THE FRONTIER: a compensating error present IDENTICALLY at firm AND global level evades BOTH
      checks. Only a deeper-source (cohort / account-level) re-derive catches that -- CVO's Layer-3.
      Per-firm + cross-firm both green == a component re-derive TRANSITIVELY, not independently.
  (3) This gate answers "is the artifact internally coherent?", NEVER "is it the RIGHT number?".
      Coherence is not correctness -- a self-consistent artifact built from a wrong feed passes.
"""
from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import math
import re
import sys
from collections import Counter

import boto3
from botocore.exceptions import ClientError

SERVED_BUCKET = "opal-data-portal-v2"
PUBLISHED_BUCKET = "opal-data-assets"
REL_TOL = 0.001
# --- INTERNAL-CONSISTENCY gate (COO-routed 2026-07-22 after the Global P0) ---
# Tolerance is chosen by MEASURED sensitivity, not by taste: these are USD sums at ~1e9 magnitude carried
# in float64 (~15-16 sig digits), so genuine FP noise on a few-hundred-term sum is ~1e-6 USD. A $1.00 floor
# is therefore ~6 orders of magnitude above the noise and still catches any defect worth a dollar. The
# mutant test MEASURES and PRINTS the floor it actually achieves -- an unstated sensitivity is an
# unrelyable gate.
CONSISTENCY_ABS_TOL_USD = 1.00
CONSISTENCY_REL_TOL = 1e-9
# MEASURED 2026-07-22 (live S3, not assumed): only `global` carries opal_aggregate_aua; 49financial and
# inflection carry `partner_custody_total`. Resolution is by PRESENCE, so the gate covers all three firms.
TOTAL_FIELD_CANDIDATES = ("opal_aggregate_aua", "partner_custody_total")
CROSSFIRM_FIELDS = ("model_aua", "non_model_aua")
GLOBAL_FIRM = "global"
# Andrew-direct ruling 2026-07-22 ("EXCLUDE consistently", relayed by DS 044655Z): the global total keeps
# its value and global.non_model_aua is REBASED to 49F-only; Inflection non-model moves to a separate
# NON-TOTAL audit field. It must NEVER be summed into the total -- the per-firm identity enforces that
# automatically (summing it back in would break total == model + non_model).
EXCLUDED_PARTNER = "inflection"
EXCLUDED_PARTNER_FIELD = "inflection_non_model_aua"
ALLOWED_EXTRAS = {"basis", "meta", "source_vintage_last"}   # leaf-name spec extras (published-side, any depth)
SHAPE_EXEMPT_ROOTS = {"meta", "source_vintage_last", "cohort_provenance"}  # provenance subtrees: keys legitimately differ served-vs-revamp. cohort_provenance wired @7e0320cc0 (49f+inflection only; global omits) -- ledger harness_requirement + CTO 235117Z: EXEMPT from shape/value-diff (source-path-derived, FE-unconsumed 0-refs, CVO lineage-verifies the map)
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
    # A1 aum-metrics + A2 aum-timeseries (coherent-9 exact-9, CTO 233555Z + manifest 235117Z): deliberately
    # NOT in the date-join value registry. Both stage at gold/mdpf_revamp/portfolios/aum-{metrics,timeseries}.json
    # -- a portfolios/{hyphen} path that does NOT fit the {prefix}/{firm}/{name} convention -- AND carry NO ledger
    # window. A1 is QUARTERLY (q0-q3) FIELD-IDENTITY (not a daily date-join); A2 is a revamp-native series whose
    # +3.07% D-1 + freshness recovery (07-20 fresh vs 05-29 legacy clobber) is CVO-reconciled NAMED, not a value
    # delta this leg owns. Value-comparing either HERE would manufacture a spurious UNEXPLAINED_DELTA (no ledger)
    # or PUBLISHED_ABSENT (wrong path). They are confirmed by a separate FIELD-IDENTITY read (key-set/shape +
    # freshness), citing CTO+CVO -- see the session log. The date-join GATE = 3 aggregates + A4 non_model.
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


def _named_shape_hit(path, patterns):
    """EXACT-or-glob, never substring -- same discipline as _spec_field_hit (BUG-2). A declared
    'model_aua' must not silently name a 'non_model_aua' extra."""
    return any(path == pat or fnmatch.fnmatch(path, pat) for pat in patterns)


def _shape_diff(served, published, entries=None):
    """Shape diff, with a LEDGER-DECLARED named-extra channel.

    A revamp-only DATA field (e.g. `inflection_non_model_aua`, the Andrew EXCLUDE/B audit carrier,
    2026-07-22) is an INTENDED published-only key. The cohort_provenance precedent solved that class by
    adding a harness EXEMPTION -- correct there, because cohort_provenance is provenance: FE-unconsumed,
    run-time, not data. It is the WRONG tool for a numeric DATA field: an exemption is invisible in the
    record, applies forever, and cannot distinguish the intended field from a future accidental one.

    So a data extra is NAMED, not exempted -- declared by DS in the ledger:
        "_shape_extras": {"published_only": ["inflection_non_model_aua"], "note": "..."}
    A declared extra is reported as an EXPECTED structural delta; anything undeclared still SHAPE_FAILs.
    The declaration lives in the ledger (reviewed, diffable, per-artifact) rather than in my source, so
    it cannot silently widen and it expires with the ledger entry. Same fail-safe as _date_axis: NO
    ledger -> every extra is unexplained."""
    entries = entries or {}
    spec = entries.get("_shape_extras") or {}
    named_pats = spec.get("published_only") or []
    missing_pats = spec.get("served_only") or []
    s, p = _shape(served), _shape(published)
    missing_all = sorted(k for k in (s - p) if not _shape_exempt(k))  # was unfiltered -> false SHAPE_FAIL on meta.*
    extra_all = sorted(k for k in (p - s) if not _shape_exempt(k))
    named_extra = [k for k in extra_all if _named_shape_hit(k, named_pats)]
    named_missing = [k for k in missing_all if _named_shape_hit(k, missing_pats)]
    missing = [k for k in missing_all if k not in named_missing]
    extra = [k for k in extra_all if k not in named_extra]
    return missing, extra, named_missing, named_extra


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
    missing, extra, named_missing, named_extra = _shape_diff(served, published, entries)
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
    for k in named_extra:
        expected.append((f"shape:{k}", "absent", "published-only", "named published-only (_shape_extras)"))
    for k in named_missing:
        expected.append((f"shape:{k}", "served-only", "absent", "named served-only (_shape_extras)"))
    return {"missing": missing, "extra": extra, "expected": expected, "unexplained": unexplained,
            "shape_ok": not (missing or extra), "axis": axis,
            "named_missing": named_missing, "named_extra": named_extra}


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


def _resolve_total_field(obj):
    """Which field carries this firm's TOTAL. MEASURED, not assumed (2026-07-22): `opal_aggregate_aua`
    exists ONLY on global; 49financial/inflection carry `partner_custody_total` instead. A gate hard-coded
    to opal_aggregate_aua would therefore silently no-op on both partner firms -- covering 1 of 3 firms
    while reporting a clean sweep. Returns the field name, or None (-> TOTAL_FIELD_ABSENT, a FAIL)."""
    for f in TOTAL_FIELD_CANDIDATES:
        if isinstance(obj.get(f), list):
            return f
    return None


def _is_finite_num(x):
    """A value the identity can actually be evaluated on. CVO-found false-PASS (2026-07-22, ITEM 1):
    a NaN anywhere in (total, model, non_model) makes diff NaN, and `abs(nan) > tol` is **False** in
    Python -- so the gate returned CLEAN and still counted the date as checked. `json.loads` parses a
    bare NaN by default, so a producer emitting NaN slipped the gate silently: a false PASS on the exact
    axis this gate exists for, and a direct violation of its own UNCHECKABLE-IS-NOT-A-PASS rule.
    inf was already caught (abs(inf) > tol is True) but reported as a SUM_MISMATCH with an infinite
    hole, which is a misleading verdict; both are now NON_FINITE. bool is excluded deliberately --
    True/False is not a dollar amount, and `True + 1` would otherwise evaluate happily."""
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _marker(obj):
    """The producer's honest-None declaration (DS @943d0a2bb, CVO-ruled architecture B 045700Z).
    `meta.honest_none` = {basis, model_feed_prefix, custody_feed_prefix, by_date (date -> REASON),
    model_absent_dates, custody_absent_dates, verify, ...}."""
    return ((obj.get("meta") or {}).get("honest_none")) or {}


def _marker_reason(marker, date):
    """The declared reason TOKEN for a date (the text before ' --'), or None if undeclared."""
    raw = (marker.get("by_date") or {}).get(date)
    return raw.split(" --")[0].strip() if isinstance(raw, str) and raw.strip() else None


def _marker_admits(marker, date, reason, total_field, t, m, n):
    """MECHANISM-BOUND admission (CTO 051606Z + CVO architecture B). Returns (admit, why_refused).

    A marker is a producer SELF-REPORT, and a self-report is never trusted alone. CVO owns the
    lineage-verify (declaration vs LIVE partition presence) -- deliberately NOT done here, because
    reaching into bronze/silver from the parity harness over-couples it (CVO ruled out architecture A).
    What IS done here, and what makes this more than a blanket skip: **the reason string makes a
    PREDICTION about the null pattern, and the prediction is checked against the artifact's own data.**
    A marker that contradicts the data it is supposed to explain is REFUSED, so the exemption cannot
    launder a real producer drop:

      model_partition_absent -> model_aua MUST be None. A populated model IS a measurement, so the
          partition demonstrably was not absent -> REFUSE (this is CTO's seeded mutant).
          Self-coherence: date in model_absent_dates and NOT in custody_absent_dates.
          For a CUSTODY-derived total (partner_custody_total) the custody partition is present by
          construction here, so the total MUST be populated; a None total means all_feeds_absent was
          the real reason -> REFUSE. A DERIVED total (opal_aggregate_aua) legitimately propagates to
          None when a contributing leg is absent, so it is not constrained.
      all_feeds_absent      -> ALL THREE MUST be None; ANY populated value -> REFUSE.
          Self-coherence: date in BOTH model_absent_dates and custody_absent_dates.

    An unrecognised reason is REFUSED -- a marker cannot buy amnesty with a string nobody parses.
    THE RESIDUAL, stated plainly: a marker that lies about a date whose data is null-shaped exactly as
    the reason predicts is NOT catchable from the artifact alone. That is precisely CVO's leg, which is
    why his verify is load-bearing rather than belt-and-braces."""
    model_absent = set(marker.get("model_absent_dates") or [])
    custody_absent = set(marker.get("custody_absent_dates") or [])
    if reason == "model_partition_absent":
        if date not in model_absent:
            return False, "reason=model_partition_absent but date not in model_absent_dates (marker self-incoherent)"
        if date in custody_absent:
            return False, "reason=model_partition_absent but date IS in custody_absent_dates (that is all_feeds_absent)"
        if m is not None:
            return False, f"reason=model_partition_absent but model_aua is POPULATED ({m!r}) -- a measurement exists"
        if total_field == "partner_custody_total" and t is None:
            return False, "reason=model_partition_absent (custody present) but the custody total is None"
        return True, ""
    if reason == "all_feeds_absent":
        if not (date in model_absent and date in custody_absent):
            return False, "reason=all_feeds_absent but the date is not in BOTH absent lists (marker self-incoherent)"
        populated = [f for f, v in (("total", t), ("model", m), ("non_model", n)) if v is not None]
        if populated:
            return False, f"reason=all_feeds_absent but {'+'.join(populated)} POPULATED -- a measurement exists"
        return True, ""
    return False, f"unrecognised honest-None reason {reason!r} -- a marker cannot exempt with an unparsed string"


def _consistency_violations(obj):
    """Pure INTERNAL-CONSISTENCY comparator (S3-free, unit-testable): total == model_aua + non_model_aua,
    PER DATE, on ONE firm's aggregate. This is the invariant the 3-pass structurally lacked -- a
    served-vs-published PARITY check cannot see it, because a defect present on BOTH sides ties clean.
    (Live proof 2026-07-22: global's total omits Inflection non-model on 421/427 staged dates, hole
    $64.5M-$203.2M, and my 3/3 parity leg was honestly CLEAN throughout. PARITY IS NOT CONSISTENCY.)

    NULL DISCIPLINE -- absent is NOT zero. Coercing a missing non_model to 0.0 would make the exact
    Inflection hole tie perfectly. A null is admissible ONLY when the producer DECLARES it via
    `meta.honest_none` AND the declaration survives _marker_admits (see there):
      any null at a date, marker ADMITS   -> HONEST_NONE, exempt + counted separately.
      any null at a date, marker REFUSES  -> MARKER_CONTRADICTED (the marker disagrees with its own data).
      any null at a date, NO marker       -> PARTIAL_NULL / UNDECLARED_NULL_ROW. Never silently skipped.

    >> A WHOLLY-NULL ROW IS NOT SELF-JUSTIFYING. This function previously skipped an all-None row as
    "honest" with no declaration required, which made "null the whole row" a way to leave the gate --
    the same shape of hole DS found in their own gate (an identity that only runs where every term is
    present never examines the rows someone emptied). A null row must now be DECLARED, exactly like a
    partial one. Verified no-op on the 2026-07-22 staged set: every all-None row on all three firms is
    already marked. <<

    Returns (violations, stats); violations = [(date, kind, total, model, non_model, diff)] where
    diff = (model + non_model) - total, or a reason string for marker refusals."""
    tfield = _resolve_total_field(obj)
    if tfield is None:
        return None, {"total_field": None}
    dates = obj.get("dates") or []
    tot, mod, non = obj.get(tfield) or [], obj.get("model_aua") or [], obj.get("non_model_aua") or []
    marker = _marker(obj)
    viol, n_checked, n_honest, n_undeclared = [], 0, 0, 0
    for i, d in enumerate(dates):
        t = tot[i] if i < len(tot) else None
        m = mod[i] if i < len(mod) else None
        n = non[i] if i < len(non) else None
        nulls = [x is None for x in (t, m, n)]
        if any(nulls):
            reason = _marker_reason(marker, d)
            if reason is None:
                n_undeclared += 1
                viol.append((d, "UNDECLARED_NULL_ROW" if all(nulls) else "PARTIAL_NULL", t, m, n, None))
                continue
            admit, why = _marker_admits(marker, d, reason, tfield, t, m, n)
            if not admit:
                viol.append((d, "MARKER_CONTRADICTED", t, m, n, why))
                continue
            n_honest += 1
            continue
        if not all(_is_finite_num(x) for x in (t, m, n)):
            viol.append((d, "NON_FINITE", t, m, n, None))
            continue
        n_checked += 1
        diff = (m + n) - t
        if abs(diff) > max(CONSISTENCY_ABS_TOL_USD, abs(t) * CONSISTENCY_REL_TOL):
            viol.append((d, "SUM_MISMATCH", t, m, n, diff))
    return viol, {"total_field": tfield, "checked": n_checked, "all_null": n_honest,
                  "honest_none": n_honest, "undeclared": n_undeclared, "dates": len(dates),
                  "marker": bool(marker)}


def _agg_source(firm, published_prefix=None, served=False):
    """Resolve (bucket, key) for a firm's aggregate. served=True targets the LEGACY LIVE artifact -- the
    bytes the portal serves TODAY -- so the same invariant can be run against what is actually in front of
    users, not only against what is staged to replace it."""
    if served:
        return SERVED_BUCKET, ARTIFACTS[("aggregate_aua_timeseries", firm)]["served"]
    key = (f"{published_prefix}/{firm}/aggregate_aua_timeseries.json" if published_prefix
           else ARTIFACTS[("aggregate_aua_timeseries", firm)]["published"])
    return PUBLISHED_BUCKET, key


def check_internal_consistency(firm, published_prefix=None, served=False):
    """STANDING pre-serve gate (COO-routed 2026-07-22 after the Global P0): each firm's own total must
    equal its own model + non_model, per date. Reads the STAGED/PUBLISHED artifact (the bytes about to be
    served), never a producer self-report. served=True points it at the legacy live artifact instead."""
    bucket, key = _agg_source(firm, published_prefix, served)
    obj = _get(bucket, key)
    if obj is None:
        return {"firm": firm, "verdict": "CONSISTENCY_ABSENT", "note": f"{key} absent", "key": key}
    viol, stats = _consistency_violations(obj)
    if viol is None:
        return {"firm": firm, "verdict": "TOTAL_FIELD_ABSENT", "key": key,
                "note": f"no total field ({'/'.join(TOTAL_FIELD_CANDIDATES)}) -- UNCHECKABLE, not clean"}
    return {"firm": firm, "verdict": "CONSISTENCY_PASS" if not viol else "CONSISTENCY_FAIL",
            "violations": viol, "key": key, **stats}


def _crossfirm_violations(glob_obj, partner_objs, field):
    """Pure cross-firm ROLL-UP comparator: global[field] == sum(partner[field]) at the SAME date
    (date-joined, never positional). Catches a firm silently dropping out of the global roll-up -- the
    LD-0292 class (49financial vanished from mdpf held_by_partner, ~$528mm -> public float).
    A date where global is populated but any partner is missing/None is a violation, not a skip:
    dropping the partner is exactly the defect being hunted."""
    out = []
    gdates = glob_obj.get("dates") or []
    gvals = glob_obj.get(field) or []
    idx = [({d: j for j, d in enumerate(o.get("dates") or [])}, o.get(field) or []) for o in partner_objs]
    for i, d in enumerate(gdates):
        g = gvals[i] if i < len(gvals) else None
        if g is None:
            continue
        parts, missing = [], False
        for dmap, vals in idx:
            j = dmap.get(d)
            v = vals[j] if (j is not None and j < len(vals)) else None
            if v is None:
                missing = True
                break
            parts.append(v)
        if missing:
            out.append((d, "PARTNER_MISSING", g, None, None))
            continue
        # same NaN false-PASS as the per-firm identity: sum() with a NaN gives NaN, and abs(nan) > tol
        # is False -> silently clean. Guarded on BOTH sides of the roll-up, not just the per-firm gate.
        if not (_is_finite_num(g) and all(_is_finite_num(v) for v in parts)):
            out.append((d, "NON_FINITE", g, None, None))
            continue
        s = sum(parts)
        diff = s - g
        if abs(diff) > max(CONSISTENCY_ABS_TOL_USD, abs(g) * CONSISTENCY_REL_TOL):
            out.append((d, "ROLLUP_MISMATCH", g, s, diff))
    return out


def check_crossfirm_rollup(published_prefix=None, served=False):
    """Companion gate (BEYOND COO's literal per-firm ask -- flagged as such, accept/reject independently):
    global's component fields must equal the sum of the partner firms', per date. Measured clean 421/421
    on the 2026-07-22 staged set for BOTH components -- which is what localises the P0 to the total-field
    COMPOSITION, not to the firm-sum."""
    def _load(firm):
        bucket, key = _agg_source(firm, published_prefix, served)
        return _get(bucket, key), key
    firms = [f for (n, f) in ARTIFACTS if n == "aggregate_aua_timeseries"]
    partners = sorted(f for f in firms if f != GLOBAL_FIRM)
    if GLOBAL_FIRM not in firms or not partners:
        return {"verdict": "CROSSFIRM_ABSENT", "note": f"need {GLOBAL_FIRM} + >=1 partner; have {sorted(firms)}"}
    gobj, gkey = _load(GLOBAL_FIRM)
    pobjs = []
    for f in partners:
        o, _ = _load(f)
        if o is None:
            return {"verdict": "CROSSFIRM_ABSENT", "note": f"partner {f} artifact absent"}
        pobjs.append(o)
    if gobj is None:
        return {"verdict": "CROSSFIRM_ABSENT", "note": f"{gkey} absent"}
    return {**_crossfirm_regime_probe(gobj, partners, pobjs),
            "dates": len(gobj.get("dates") or []), "key": gkey}


def _crossfirm_regime_probe(gobj, partners, pobjs):
    """Pure cross-firm roll-up evaluator (S3-free, unit-testable -- same split as _coherence_mismatches).

    REGIME DETECTION (Andrew ruling EXCLUDE/B, 2026-07-22, via DS 044655Z) -- by PRESENCE, the same
    pattern as the total field, so the gate is correct on BOTH sides of the cutover with no flag day."""
    #   REGIME A (pre-fix):  global.non_model_aua == 49f + inflection   (all partners summed)
    #   REGIME B (post-fix): global.non_model_aua == 49f ONLY, and Inflection non-model is carried in a
    #                        SEPARATE audit field global.inflection_non_model_aua == inflection.non_model_aua
    # Under B the old all-partner sum would FALSE-RED a correct artifact -- DS flagged this and is right.
    # model_aua is unaffected in both regimes (it remains the sum over all partners).
    regime_b = isinstance(gobj.get(EXCLUDED_PARTNER_FIELD), list)
    res, notes = {}, []
    for f in CROSSFIRM_FIELDS:
        if f == "non_model_aua" and regime_b:
            # (i) global's rebased non_model must equal the INCLUDED partners only
            incl = [o for f2, o in zip(partners, pobjs) if f2 != EXCLUDED_PARTNER]
            res[f] = _crossfirm_violations(gobj, incl, f)
            notes.append(f"non_model_aua rebased to {'+'.join(x for x in partners if x != EXCLUDED_PARTNER)} (EXCLUDE/B)")
            # (ii) the audit carrier must equal the EXCLUDED partner's own non_model -- so the excluded
            # money is still CHECKED, not merely moved out of the total and forgotten.
            exc = [o for f2, o in zip(partners, pobjs) if f2 == EXCLUDED_PARTNER]
            if exc:
                res[EXCLUDED_PARTNER_FIELD] = _crossfirm_violations(
                    {"dates": gobj.get("dates"), EXCLUDED_PARTNER_FIELD: gobj.get(EXCLUDED_PARTNER_FIELD)},
                    [{"dates": exc[0].get("dates"), EXCLUDED_PARTNER_FIELD: exc[0].get("non_model_aua")}],
                    EXCLUDED_PARTNER_FIELD)
                notes.append(f"{EXCLUDED_PARTNER_FIELD} == {EXCLUDED_PARTNER}.non_model_aua (audit carrier)")
        else:
            res[f] = _crossfirm_violations(gobj, pobjs, f)
    bad = {f: v for f, v in res.items() if v}
    return {"verdict": "CROSSFIRM_PASS" if not bad else "CROSSFIRM_FAIL", "partners": partners,
            "by_field": res,
            "regime": "B (EXCLUDE)" if regime_b else "A (all-partner sum)", "notes": notes}


def _consistency_self_test():
    """MUTANT-GATED acceptance (COO 034839Z, Rule 22a EXERCISED-not-asserted): a gate that has never
    failed a seeded defect has never been tested. Every clause below seeds a KNOWN defect and asserts
    the gate goes RED -- plus a clean control asserting it can still go GREEN (an instrument that cannot
    pass is as broken as one that cannot fail). Returns (ok, measured_floor_usd)."""
    base = {"dates": ["2026-07-16", "2026-07-17", "2026-07-20"],
            "opal_aggregate_aua": [300.0, 400.0, 500.0],
            "model_aua": [200.0, 250.0, 300.0],
            "non_model_aua": [100.0, 150.0, 200.0]}
    # CONTROL: a coherent artifact PASSES (the gate is not stuck-red / undiscriminating)
    clean_v, clean_s = _consistency_violations(base)
    c_clean = (clean_v == [] and clean_s["checked"] == 3 and clean_s["total_field"] == "opal_aggregate_aua")
    # MUTANT 1 -- THE LIVE BUG'S EXACT SHAPE: total omits one component chunk (Inflection non-model).
    m1 = copy.deepcopy(base)
    m1["opal_aggregate_aua"] = [t - 153_000_000.0 for t in m1["opal_aggregate_aua"]]
    v1, _ = _consistency_violations(m1)
    c_m1 = (len(v1) == 3 and all(k == "SUM_MISMATCH" for _, k, *_ in v1)
            and abs(v1[0][5] - 153_000_000.0) < 1.0)
    # MUTANT 2 -- SENSITIVITY FLOOR: descending seeded holes; find the smallest one it still catches.
    floor, caught = None, []
    for hole in (1_000_000.0, 1_000.0, 10.0, 2.0, 1.01, 0.50, 0.01):
        mm = copy.deepcopy(base)
        mm["opal_aggregate_aua"] = [t - hole for t in mm["opal_aggregate_aua"]]
        vv, _ = _consistency_violations(mm)
        if vv:
            caught.append(hole)
            floor = hole
    c_m2 = (1_000_000.0 in caught and 1_000.0 in caught and 10.0 in caught
            and 0.01 not in caught)          # catches real money; ignores sub-cent FP noise
    # MUTANT 3 -- MISSING-IS-NOT-ZERO: non_model absent at one date must FAIL, never zero-fill.
    m3 = copy.deepcopy(base)
    m3["non_model_aua"][2] = None
    v3, _ = _consistency_violations(m3)
    c_m3 = any(d == "2026-07-20" and k == "PARTIAL_NULL" for d, k, *_ in v3)
    # MUTANT 3b -- the same hole via a SHORT array (truncated series, not an explicit None)
    m3b = copy.deepcopy(base)
    m3b["non_model_aua"] = m3b["non_model_aua"][:2]
    v3b, _ = _consistency_violations(m3b)
    c_m3b = any(d == "2026-07-20" and k == "PARTIAL_NULL" for d, k, *_ in v3b)
    # MUTANT 3c -- NON-FINITE (CVO ITEM 1, 2026-07-22): the false PASS CVO constructed. A NaN made
    # diff NaN, and `abs(nan) > tol` is False -> the gate returned CLEAN **and counted the date as
    # checked**. json.loads parses a bare NaN by default, so a producer emitting one slipped the gate
    # silently. Every non-finite shape must now be UNCHECKABLE, and must NOT inflate n_checked.
    nf_ok = True
    for bad in (float("nan"), float("inf"), float("-inf"), True, "1234.5"):
        for field in ("opal_aggregate_aua", "model_aua", "non_model_aua"):
            mnf = copy.deepcopy(base)
            mnf[field] = list(mnf[field])
            mnf[field][2] = bad
            vnf, snf = _consistency_violations(mnf)
            nf_ok &= any(d == "2026-07-20" and k == "NON_FINITE" for d, k, *_ in vnf)
            nf_ok &= (snf["checked"] == 2)          # the poisoned date is NOT counted as checked-clean
    # and the cross-firm roll-up carries the SAME guard (sum() with a NaN is NaN -> silently clean)
    g_nf = {"dates": ["2026-07-20"], "model_aua": [float("nan")], "non_model_aua": [40.0]}
    pA_nf = {"dates": ["2026-07-20"], "model_aua": [250.0], "non_model_aua": [25.0]}
    pB_nf = {"dates": ["2026-07-20"], "model_aua": [150.0], "non_model_aua": [15.0]}
    nf_xf_global = any(k == "NON_FINITE" for _, k, *_ in _crossfirm_violations(g_nf, [pA_nf, pB_nf], "model_aua"))
    g_ok = {"dates": ["2026-07-20"], "model_aua": [400.0], "non_model_aua": [40.0]}
    pA_bad = {"dates": ["2026-07-20"], "model_aua": [float("nan")], "non_model_aua": [25.0]}
    nf_xf_partner = any(k == "NON_FINITE" for _, k, *_ in _crossfirm_violations(g_ok, [pA_bad, pB_nf], "model_aua"))
    # MUTANT 4 -- TOTAL FIELD ABSENT is UNCHECKABLE, never a silent clean sweep.
    m4 = {k: v for k, v in base.items() if k != "opal_aggregate_aua"}
    v4, s4 = _consistency_violations(m4)
    c_m4 = (v4 is None and s4["total_field"] is None)
    # PARTNER SHAPE: partner_custody_total resolves as the total field (global-only hard-code would no-op)
    part = {"dates": ["2026-07-20"], "partner_custody_total": [500.0],
            "model_aua": [300.0], "non_model_aua": [200.0]}
    pv, ps = _consistency_violations(part)
    c_part = (pv == [] and ps["total_field"] == "partner_custody_total")
    part_bad = copy.deepcopy(part)
    part_bad["partner_custody_total"] = [400.0]
    c_part_bad = bool(_consistency_violations(part_bad)[0])          # partner defect CAUGHT too
    # HONEST-NONE: all three None at a date -> exempt + counted, NOT a violation -- but ONLY WHEN
    # DECLARED. This clause used to assert that an all-None row was self-justifying; the marker work
    # (2026-07-22) deliberately removed that, so the row now needs a marker. Kept as a PAIR: declared
    # -> exempt, undeclared -> RED, so the tightening itself is regression-locked in both directions.
    hn = copy.deepcopy(base)
    for f in ("opal_aggregate_aua", "model_aua", "non_model_aua"):
        hn[f][1] = None
    hn["meta"] = {"honest_none": {"by_date": {"2026-07-17": "all_feeds_absent -- both partitions missing"},
                                  "model_absent_dates": ["2026-07-17"],
                                  "custody_absent_dates": ["2026-07-17"]}}
    vhn, shn = _consistency_violations(hn)
    c_hn = (vhn == [] and shn["honest_none"] == 1 and shn["checked"] == 2)
    hn_undeclared = copy.deepcopy(base)
    for f in ("opal_aggregate_aua", "model_aua", "non_model_aua"):
        hn_undeclared[f][1] = None
    c_hn_undeclared = any(k == "UNDECLARED_NULL_ROW" for _, k, *_ in _consistency_violations(hn_undeclared)[0])
    c_hn = c_hn and c_hn_undeclared
    # CROSS-FIRM: clean roll-up passes; a partner dropping out of global is CAUGHT (LD-0292 class)
    g = {"dates": ["2026-07-17", "2026-07-20"], "model_aua": [300.0, 400.0], "non_model_aua": [30.0, 40.0]}
    pA = {"dates": ["2026-07-17", "2026-07-20"], "model_aua": [200.0, 250.0], "non_model_aua": [20.0, 25.0]}
    pB = {"dates": ["2026-07-17", "2026-07-20"], "model_aua": [100.0, 150.0], "non_model_aua": [10.0, 15.0]}
    c_xf_clean = (_crossfirm_violations(g, [pA, pB], "model_aua") == []
                  and _crossfirm_violations(g, [pA, pB], "non_model_aua") == [])
    c_xf_drop = bool(_crossfirm_violations(g, [pA], "model_aua"))            # firm B dropped -> CAUGHT
    pB_gap = {"dates": ["2026-07-17"], "model_aua": [100.0], "non_model_aua": [10.0]}
    c_xf_missing = any(k == "PARTNER_MISSING" for _, k, *_ in
                       _crossfirm_violations(g, [pA, pB_gap], "model_aua"))  # partner absent AT a date -> CAUGHT
    # date-join proof: a partner whose dates are ORDERED DIFFERENTLY still ties (never positional)
    pB_rev = {"dates": ["2026-07-20", "2026-07-17"], "model_aua": [150.0, 100.0], "non_model_aua": [15.0, 10.0]}
    c_xf_datejoin = (_crossfirm_violations(g, [pA, pB_rev], "model_aua") == [])

    # ===== REGIME B (Andrew EXCLUDE ruling 2026-07-22): rebased non_model + audit carrier =====
    # The gate must be correct on BOTH sides of the cutover, and regime B must still CATCH defects --
    # a regime switch that makes everything pass is a gate that was retired, not adapted.
    # NOTE: REALISTIC MAGNITUDES ON PURPOSE. These fixtures were first written at unit scale, where a
    # seeded $1.00 drift sat exactly ON the $1.00 tolerance boundary -- so `b_catch_rebased` went FALSE
    # and the self-test failed. The GATE was right (a $1.00 diff is within tolerance); the TEST was
    # wrong. Kept as a note because it is the mutant doing its job on the test author: a mutant whose
    # magnitude is inside the tolerance proves nothing about the gate.
    gB = {"dates": ["2026-07-20"], "model_aua": [400_000_000.0],
          "non_model_aua": [25_000_000.0],                 # 49f ONLY (rebased)
          "inflection_non_model_aua": [15_000_000.0]}      # inflection's own, carried separately
    p49 = {"dates": ["2026-07-20"], "model_aua": [250_000_000.0], "non_model_aua": [25_000_000.0]}
    pinf = {"dates": ["2026-07-20"], "model_aua": [150_000_000.0], "non_model_aua": [15_000_000.0]}
    rB = _crossfirm_regime_probe(gB, ["49financial", "inflection"], [p49, pinf])
    b_clean = (rB["regime"].startswith("B") and rB["verdict"] == "CROSSFIRM_PASS")
    # regime B still CATCHES: global's rebased non_model wrong (26 != 49f's 25)
    gB_bad = copy.deepcopy(gB)
    gB_bad["non_model_aua"] = [26_000_000.0]
    b_catch_rebased = _crossfirm_regime_probe(gB_bad, ["49financial", "inflection"], [p49, pinf])["verdict"] == "CROSSFIRM_FAIL"
    # regime B still CATCHES: the AUDIT CARRIER drifting from inflection's own non_model (the excluded
    # money must stay CHECKED -- "moved out of the total" must not mean "no longer verified")
    gB_bad2 = copy.deepcopy(gB)
    gB_bad2["inflection_non_model_aua"] = [99_000_000.0]
    b_catch_audit = _crossfirm_regime_probe(gB_bad2, ["49financial", "inflection"], [p49, pinf])["verdict"] == "CROSSFIRM_FAIL"
    # regime A (no audit field) still behaves as before: global.non_model == sum of ALL partners
    gA = {"dates": ["2026-07-20"], "model_aua": [400_000_000.0], "non_model_aua": [40_000_000.0]}
    rA = _crossfirm_regime_probe(gA, ["49financial", "inflection"], [p49, pinf])
    a_clean = (rA["regime"].startswith("A") and rA["verdict"] == "CROSSFIRM_PASS")
    # and the per-firm identity under B: total == model + non_model(rebased); the audit field is NOT summed
    gB_ident = {"dates": ["2026-07-20"], "opal_aggregate_aua": [425_000_000.0], "model_aua": [400_000_000.0],
                "non_model_aua": [25_000_000.0], "inflection_non_model_aua": [15_000_000.0]}
    b_identity = (_consistency_violations(gB_ident)[0] == [])
    gB_summed = copy.deepcopy(gB_ident)
    gB_summed["opal_aggregate_aua"] = [440_000_000.0]   # audit field wrongly summed in
    b_catch_summed = bool(_consistency_violations(gB_summed)[0])
    # ===== HONEST-NONE MARKER CONSUMER (CTO 051606Z leg; CVO architecture B 045700Z) =====
    # The exemption must be MECHANISM-BOUND: a marker that contradicts its own data buys nothing.
    R_MODEL = "model_partition_absent -- custody partition PRESENT, honest custody-only day"
    R_ALL = "all_feeds_absent -- BOTH partitions missing"
    def _mk(by_date, model_abs, cust_abs):
        return {"by_date": by_date, "model_absent_dates": model_abs, "custody_absent_dates": cust_abs}
    # (a) PARTNER, model_partition_absent: custody present, model+non_model None -> ADMITTED
    pm = {"dates": ["2026-05-21"], "partner_custody_total": [202_041_468.86],
          "model_aua": [None], "non_model_aua": [None],
          "meta": {"honest_none": _mk({"2026-05-21": R_MODEL}, ["2026-05-21"], [])}}
    v_pm, s_pm = _consistency_violations(pm)
    mk_partner_ok = (v_pm == [] and s_pm["honest_none"] == 1)
    # (b) CTO'S SEEDED MUTANT: same marker on a date whose MODEL IS POPULATED -> a measurement exists,
    #     so the partition demonstrably was not absent. MUST still go RED.
    pm_bad = copy.deepcopy(pm)
    pm_bad["model_aua"] = [100_000_000.0]        # populated + non_model still None -> partial, marked
    v_pmb, _ = _consistency_violations(pm_bad)
    mk_populated_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in v_pmb)
    # (c) marker self-incoherence: reason says model-absent but the date is NOT in model_absent_dates
    pm_inc = copy.deepcopy(pm)
    pm_inc["meta"]["honest_none"] = _mk({"2026-05-21": R_MODEL}, [], [])
    mk_incoherent_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in _consistency_violations(pm_inc)[0])
    # (d) reason mismatch: claims model-only but the date is ALSO in custody_absent_dates
    pm_mis = copy.deepcopy(pm)
    pm_mis["meta"]["honest_none"] = _mk({"2026-05-21": R_MODEL}, ["2026-05-21"], ["2026-05-21"])
    mk_reason_mismatch_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in _consistency_violations(pm_mis)[0])
    # (e) model_partition_absent on a CUSTODY-derived total with a None total -> really all_feeds_absent
    pm_not = copy.deepcopy(pm)
    pm_not["partner_custody_total"] = [None]
    mk_custody_none_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in _consistency_violations(pm_not)[0])
    # (f) all_feeds_absent, everything None -> ADMITTED; but ANY populated value -> RED
    af = {"dates": ["2026-07-13"], "partner_custody_total": [None], "model_aua": [None],
          "non_model_aua": [None],
          "meta": {"honest_none": _mk({"2026-07-13": R_ALL}, ["2026-07-13"], ["2026-07-13"])}}
    mk_all_ok = (_consistency_violations(af)[0] == [])
    af_bad = copy.deepcopy(af)
    af_bad["partner_custody_total"] = [202_000_000.0]
    mk_all_populated_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in _consistency_violations(af_bad)[0])
    # (g) unrecognised reason cannot buy amnesty with an unparsed string
    af_junk = copy.deepcopy(af)
    af_junk["meta"]["honest_none"] = _mk({"2026-07-13": "because I said so"}, ["2026-07-13"], ["2026-07-13"])
    mk_junk_red = any(k == "MARKER_CONTRADICTED" for _, k, *_ in _consistency_violations(af_junk)[0])
    # (h) GLOBAL (derived total) propagates to None under model_partition_absent -> ADMITTED, and the
    #     custody-total constraint must NOT be applied to a derived total.
    gm = {"dates": ["2026-05-21"], "opal_aggregate_aua": [None], "model_aua": [None],
          "non_model_aua": [None],
          "meta": {"honest_none": _mk({"2026-05-21": R_MODEL}, ["2026-05-21"], [])}}
    mk_global_prop_ok = (_consistency_violations(gm)[0] == [])
    # (i) THE HOLE THIS CLOSES: an UNDECLARED wholly-null row is no longer self-justifying
    und = {"dates": ["2026-05-21"], "partner_custody_total": [None], "model_aua": [None],
           "non_model_aua": [None]}
    v_und, s_und = _consistency_violations(und)
    mk_undeclared_red = (any(k == "UNDECLARED_NULL_ROW" for _, k, *_ in v_und) and s_und["undeclared"] == 1)
    # (j) a marker must not exempt a FULLY-POPULATED row's real SUM_MISMATCH (marker != amnesty)
    sm = {"dates": ["2026-05-21"], "partner_custody_total": [100_000_000.0],
          "model_aua": [90_000_000.0], "non_model_aua": [20_000_000.0],
          "meta": {"honest_none": _mk({"2026-05-21": R_MODEL}, ["2026-05-21"], [])}}
    mk_sum_still_red = any(k == "SUM_MISMATCH" for _, k, *_ in _consistency_violations(sm)[0])

    # ===== LEDGER-NAMED SHAPE EXTRA (vs a harness exemption) =====
    se_s = {"dates": ["2026-07-20"], "model_aua": [10.0], "non_model_aua": [5.0]}
    se_p = {"dates": ["2026-07-20"], "model_aua": [10.0], "non_model_aua": [5.0],
            "inflection_non_model_aua": [3.0]}
    se_led = {"_shape_extras": {"published_only": ["inflection_non_model_aua"], "note": "EXCLUDE/B carrier"}}
    se_named = compare(se_s, se_p, se_led)["shape_ok"]                       # declared -> shape OK
    se_undeclared = not compare(se_s, se_p, {})["shape_ok"]                  # NO ledger -> still SHAPE_FAIL
    se_other = not compare(se_s, {**se_p, "rogue_field": [1.0]}, se_led)["shape_ok"]  # a DIFFERENT extra still FAILS
    # EXACT-not-substring: declaring 'model_aua' must NOT name a 'non_model_aua' extra (BUG-2 discipline)
    se_sub_s = {"dates": ["2026-07-20"], "model_aua": [10.0]}
    se_sub_p = {"dates": ["2026-07-20"], "model_aua": [10.0], "non_model_aua": [5.0]}
    se_no_substring = not compare(se_sub_s, se_sub_p, {"_shape_extras": {"published_only": ["model_aua"]}})["shape_ok"]

    ok = (c_clean and c_m1 and c_m2 and c_m3 and c_m3b and c_m4 and c_part and c_part_bad
          and c_hn and c_xf_clean and c_xf_drop and c_xf_missing and c_xf_datejoin
          and nf_ok and nf_xf_global and nf_xf_partner
          and b_clean and b_catch_rebased and b_catch_audit and a_clean
          and b_identity and b_catch_summed
          and se_named and se_undeclared and se_other and se_no_substring
          and mk_partner_ok and mk_populated_red and mk_incoherent_red and mk_reason_mismatch_red
          and mk_custody_none_red and mk_all_ok and mk_all_populated_red and mk_junk_red
          and mk_global_prop_ok and mk_undeclared_red and mk_sum_still_red)
    print(f"SELF-TEST consistency CONTROL (coherent artifact PASSES, gate not stuck-red)={c_clean}")
    print(f"SELF-TEST consistency MUTANT-1 (live bug shape: total omits $153M component) -> RED={c_m1}")
    print(f"SELF-TEST consistency MUTANT-2 sensitivity: caught holes {caught} -> measured floor ${floor:,.2f}; sub-cent ignored={c_m2}")
    print(f"SELF-TEST consistency MUTANT-3 missing-is-NOT-zero: explicit None -> PARTIAL_NULL={c_m3}; truncated array -> PARTIAL_NULL={c_m3b}")
    print(f"SELF-TEST consistency MUTANT-3c NON_FINITE (CVO ITEM 1 false-PASS): NaN/inf/-inf/bool/str in any of 3 fields -> UNCHECKABLE + not counted checked={nf_ok}; crossfirm global-side={nf_xf_global}, partner-side={nf_xf_partner}")
    print(f"SELF-TEST consistency MUTANT-4 total field absent -> UNCHECKABLE (not a clean sweep)={c_m4}")
    print(f"SELF-TEST REGIME-B (Andrew EXCLUDE 2026-07-22): B detected+clean={b_clean}; A still clean={a_clean}; "
          f"B CATCHES rebased-non_model drift={b_catch_rebased}; B CATCHES audit-carrier drift={b_catch_audit}")
    print(f"SELF-TEST REGIME-B identity: total==model+non_model(rebased) clean={b_identity}; "
          f"audit field wrongly SUMMED into total -> CAUGHT={b_catch_summed}")
    print(f"SELF-TEST honest-None MARKER consumer: partner model-absent ADMITTED={mk_partner_ok}; global derived-total propagation ADMITTED={mk_global_prop_ok}; all_feeds_absent ADMITTED={mk_all_ok}")
    print(f"SELF-TEST marker REFUSALS (mechanism-bound, marker != amnesty): populated-model->RED={mk_populated_red}; self-incoherent->RED={mk_incoherent_red}; reason-mismatch->RED={mk_reason_mismatch_red}; custody-None-under-model-reason->RED={mk_custody_none_red}; all_feeds+populated->RED={mk_all_populated_red}; unparsed-reason->RED={mk_junk_red}; real SUM_MISMATCH still RED={mk_sum_still_red}")
    print(f"SELF-TEST UNDECLARED wholly-null row -> RED (a null row is not self-justifying)={mk_undeclared_red}")
    print(f"SELF-TEST ledger-NAMED shape extra (_shape_extras, not a harness exemption): declared->shape OK={se_named}; "
          f"undeclared->SHAPE_FAIL={se_undeclared}; a DIFFERENT extra still FAILS={se_other}; exact-not-substring={se_no_substring}")
    print(f"SELF-TEST consistency PARTNER shape (partner_custody_total resolves)={c_part}; partner defect caught={c_part_bad}")
    print(f"SELF-TEST consistency honest-None row (all 3 None) skipped+counted, not a violation={c_hn}")
    print(f"SELF-TEST crossfirm: clean rollup PASS={c_xf_clean}; dropped firm CAUGHT={c_xf_drop}; partner-missing-at-date CAUGHT={c_xf_missing}; date-joined (reordered partner ties)={c_xf_datejoin}")
    return ok, floor


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
    # REGRESSION cohort_provenance (DS wired @7e0320cc0; ledger harness_requirement + CTO 235117Z): the
    # revamp-only cohort_provenance.* subtree (source-path-derived provenance, FE-unconsumed) must NOT
    # SHAPE_FAIL as a published-only EXTRA -- EXEMPT like meta/source_vintage_last. A real published-only
    # DATA extra OUTSIDE the exempt roots STILL fails (a false PASS is the danger). Caught on the real
    # coherent-9 run 2026-07-21: 49f+inflection aggregates SHAPE_FAIL'd on cohort_provenance[].{model,custody}
    # because SHAPE_EXEMPT_ROOTS lacked cohort_provenance -- the ledger required it, my harness didn't do it.
    cp_s = {"dates": ["2026-06-01"], "model_aua": [10.0]}
    cp_p = {"dates": ["2026-06-01"], "model_aua": [10.0],
            "cohort_provenance": [{"model": "SmartX", "custody": "Schwab"}]}
    cp_shape_ok = compare(cp_s, cp_p)["shape_ok"]                                 # cohort_provenance-only extra -> shape OK
    cp_realextra = {"dates": ["2026-06-01"], "model_aua": [10.0], "rogue_field": [1.0]}
    cp_real_still_fails = not compare(cp_s, cp_realextra)["shape_ok"]             # a real DATA extra STILL fails
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

    cons_ok, cons_floor = _consistency_self_test()
    ok &= cons_ok
    ok &= (exp_win and exp_latest and unexp and auth and null_named and null_unexp
           and dj_no_spurious and dj_axis_named and dj_last_common
           and dj_reports_unnamed and dj_common_delta_caught
           and meta_shape_ok and real_shape_still_fails
           and prov_value_exempt and basis_data_still_caught
           and cp_shape_ok and cp_real_still_fails
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
    print(f"SELF-TEST regression cohort_provenance (revamp-only extra EXEMPT): cohort_provenance-only extra shape-OK={cp_shape_ok}; real DATA extra STILL fails={cp_real_still_fails}")
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


def _report_consistency(r):
    v = r["verdict"]
    if v in ("CONSISTENCY_ABSENT", "TOTAL_FIELD_ABSENT"):
        print(f"[{v}] internal_consistency/{r['firm']} -- {r['note']}")
        return
    print(f"[{v}] internal_consistency/{r['firm']} "
          f"(total_field={r['total_field']}; checked {r['checked']}/{r['dates']} dates, "
          f"{r['all_null']} honest-None)")
    viol = r.get("violations") or []
    sums = [x for x in viol if x[1] == "SUM_MISMATCH"]
    if sums:
        diffs = [x[5] for x in sums]
        print(f"    (ic) SUM_MISMATCH on {len(sums)} date(s); hole (model+non_model)-total "
              f"min={_fmt(min(diffs))} max={_fmt(max(diffs))}")
    for d, kind, t, m, n, diff in viol[:8]:
        if kind == "PARTIAL_NULL":
            print(f"    (ic) PARTIAL_NULL {d}: total={_fmt(t)} model={_fmt(m)} non_model={_fmt(n)} "
                  f"-- absent is NOT zero, UNCHECKABLE at this date")
        elif kind == "NON_FINITE":
            print(f"    (ic) NON_FINITE {d}: total={t!r} model={m!r} non_model={n!r} "
                  f"-- not evaluable, UNCHECKABLE at this date (NaN would read CLEAN unguarded)")
        else:
            print(f"    (ic) {d}: total={_fmt(t)} != model {_fmt(m)} + non_model {_fmt(n)} "
                  f"= {_fmt(m + n)}  HOLE={_fmt(diff)}")
    if len(viol) > 8:
        print(f"    (ic) ...+{len(viol)-8} more")
    if v == "CONSISTENCY_PASS":
        print("    total == model_aua + non_model_aua at every checked date")


def _report_crossfirm(r):
    v = r["verdict"]
    if v == "CROSSFIRM_ABSENT":
        print(f"[{v}] crossfirm_rollup -- {r['note']}")
        return
    print(f"[{v}] crossfirm_rollup (global == {' + '.join(r['partners'])}; {r['dates']} dates; "
          f"regime {r.get('regime', '?')})")
    for n in r.get("notes") or []:
        print(f"    (xf) regime note: {n}")
    for field, viol in (r.get("by_field") or {}).items():
        if not viol:
            print(f"    (xf) {field}: ties at every date")
            continue
        print(f"    (xf) {field}: {len(viol)} violation(s)")
        for d, kind, g, s, diff in viol[:5]:
            if kind == "PARTNER_MISSING":
                print(f"        {d}: global={_fmt(g)} but a partner is missing/None at this date")
            elif kind == "NON_FINITE":
                print(f"        {d}: non-finite value on the global or a partner side -- UNCHECKABLE")
            else:
                print(f"        {d}: global={_fmt(g)} != sum(partners) {_fmt(s)}  DIFF={_fmt(diff)}")


def _consistency_firms():
    return sorted({f for (n, f) in ARTIFACTS if n == "aggregate_aua_timeseries"})


def _run_consistency(published_prefix=None, served=False):
    """Run the standing gate over every firm + the cross-firm roll-up. Returns True if ANY violation
    (including UNCHECKABLE states -- an absent artifact or an absent total field is NOT a pass)."""
    bad = False
    print(f"--- internal-consistency gate: {'SERVED (legacy live)' if served else 'STAGED/PUBLISHED'} ---")
    for firm in _consistency_firms():
        r = check_internal_consistency(firm, published_prefix, served)
        _report_consistency(r)
        bad |= r["verdict"] != "CONSISTENCY_PASS"
    xf = check_crossfirm_rollup(published_prefix, served)
    _report_crossfirm(xf)
    bad |= xf["verdict"] != "CROSSFIRM_PASS"
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact")
    ap.add_argument("--firm")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--consistency", action="store_true",
                    help="run ONLY the internal-consistency + cross-firm roll-up gate "
                         "(rc=1 on any violation -- the scriptable pre-serve gate)")
    ap.add_argument("--served", action="store_true",
                    help="point the consistency gate at the LEGACY LIVE artifacts (what the portal serves "
                         "today) instead of the staged/published set")
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
    if args.consistency or args.all:
        bad = _run_consistency(args.published_prefix, args.served)
        if args.consistency:
            return 1 if bad else 0
    if args.all:
        for (name, firm), spec in ARTIFACTS.items():
            _report(check_pair(name, firm, spec, ledger, args.published_prefix))
        for firm in _coherence_firms():                          # CTO Item-2: frontier account_count coherence
            _report_coherence(check_frontier_coherence(firm, args.published_prefix))
        # rc REFLECTS the consistency gate (deliberate change 2026-07-22): --all previously always
        # returned 0, so a caller could not machine-check it. The parity verdicts still do not affect
        # rc (read the output, as before); only a CONSISTENCY/CROSSFIRM violation does.
        return 1 if bad else 0
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
