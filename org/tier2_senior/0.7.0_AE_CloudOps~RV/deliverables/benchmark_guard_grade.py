"""AC3 grader for OPAL_BBGTML.TO-GUARD-1 -- the stale-benchmark guard's served output.

Grades the SERVED artifact against the never-widen pair's cell-level expectation:
  COO half @1253afc83c, CTO half @78a9e8a39e section 3.

  comprehensive: 273 null and 27 numbers byte-equal to the base, of 300 benchmark cells
  model:         100 of 100 cells equal to the base
  legacy:        the number->null / unchanged / changed-number partition, with its denominator

HOW A CELL IS CLASSIFIED -- measured, never hardcoded. The AFTER artifact declares each
series' frontier in `benchmark_last_date`, so staleness is read off the artifact and then
applied to the base cells. The 9-stale/1-current split is therefore an OUTPUT of this
script, not an assumption baked into it. If the guard is absent the field is absent and
the script refuses rather than grading against a default.

BOTH BRANCHES OF CTO SECTION 4 CONDITION 3 are handled. If a re-pull has landed and the
served data_as_of is NEWER than the base's, a stale series may legitimately carry numbers
with benchmark_last_date == data_as_of; that is track 3's proof, not a failure here. The
script says which branch it took and grades that branch's expectation.

Run:  python org/tier2_senior/0.7.0_AE_CloudOps~RV/deliverables/benchmark_guard_grade.py
Exit: 0 on PASS, 1 on FAIL (a FAIL triggers CTO section 4 condition 4's rollback).
"""
import json
import sys

import boto3

BUCKET = 'opal-data-portal-v2'
KEY_COMPREHENSIVE = 'json/benchmarks/model_portfolio_benchmarks.json'
KEY_LEGACY = 'json/benchmarks/benchmark_returns.json'
KEY_TIMESERIES = 'json/benchmarks/model_portfolio_timeseries.json'

# The base, pinned by VersionId in BOTH never-widen halves and re-read live by the CTO
# at signing. An immutable pin: this script cannot drift off the signed base.
BASE_VERSIONS = {
    KEY_COMPREHENSIVE: '9NuMvtEAPll77jLbwgGKki5y7oVS9U8M',
    KEY_LEGACY: 'JJStBVZG4cRu0XHd5axb_EVvVvnHHx.S',
    KEY_TIMESERIES: 'QeBEvgycTlhaOGyt3x1QfhlcvhlRcrek',
}
BASE_DATA_AS_OF = '2026-10-05'

MODEL_CODES = ['UST', 'ST', 'INT', 'LT', 'ULT']
PERIODS = ['1D', 'WTD', 'MTD', '1M', 'QTD', '1Q', 'YTD', '1Y', 'Since Inception', 'TTW']

# The 6 benchmark-derived fields per period, by the series each is sourced from.
# index_spread and etf_spread are benchmark-sourced: each is None whenever its
# benchmark leg is None, so the guard reaches them through the benchmark.
FIELDS_BY_SOURCE = {
    'index': ['index_benchmark', 'index_spread', 'index_benchmark_volatility'],
    'etf': ['etf_benchmark', 'etf_spread', 'etf_benchmark_volatility'],
}
MODEL_FIELDS = ['model', 'model_volatility']
LEGACY_BENCHMARK_FIELDS = ['benchmark', 'spread', 'benchmark_volatility']

s3 = boto3.client('s3', region_name='us-east-1')


def _get(key, version_id=None):
    kwargs = {'Bucket': BUCKET, 'Key': key}
    if version_id:
        kwargs['VersionId'] = version_id
    resp = s3.get_object(**kwargs)
    raw = resp['Body'].read()
    return json.loads(raw), len(raw), resp.get('VersionId'), resp['LastModified']


def _models(payload):
    return {m['code']: m for m in payload.get('models', [])}


def _is_null(v):
    return v is None


def _same(a, b):
    """Byte-equality of two JSON scalars: identical type and identical serialization."""
    return type(a) is type(b) and json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def main():
    failures = []
    notes = []

    print("=" * 78)
    print("AC3 -- served-output grade, OPAL_BBGTML.TO-GUARD-1 (stale-benchmark guard)")
    print("=" * 78)

    base, base_bytes, base_ver, _ = _get(KEY_COMPREHENSIVE, BASE_VERSIONS[KEY_COMPREHENSIVE])
    after, after_bytes, after_ver, after_mtime = _get(KEY_COMPREHENSIVE)

    print("\n-- the two objects --")
    print("  BASE   %s  %d B  VersionId %s  data_as_of %s"
          % (KEY_COMPREHENSIVE, base_bytes, base_ver, base.get('data_as_of')))
    print("  SERVED %s  %d B  VersionId %s  data_as_of %s  LastModified %s"
          % (KEY_COMPREHENSIVE, after_bytes, after_ver, after.get('data_as_of'),
             after_mtime.strftime('%Y-%m-%dT%H:%M:%SZ')))

    if base.get('data_as_of') != BASE_DATA_AS_OF:
        failures.append("the pinned BASE version's data_as_of is %r, not the signed %r"
                        % (base.get('data_as_of'), BASE_DATA_AS_OF))

    served_as_of = after.get('data_as_of')
    repull_landed = served_as_of != BASE_DATA_AS_OF
    print("\n-- CTO section 4 condition 3: which branch --")
    if repull_landed:
        print("  BRANCH B: served data_as_of %s differs from the base's %s -- a re-pull has"
              % (served_as_of, BASE_DATA_AS_OF))
        print("            landed. A stale bucket may legitimately carry NUMBERS whose")
        print("            benchmark_last_date equals data_as_of; that is track 3's proof.")
        notes.append("BRANCH B: graded against a re-pulled vintage (%s), not the signed base "
                     "vintage (%s)." % (served_as_of, BASE_DATA_AS_OF))
    else:
        print("  BRANCH A: served data_as_of %s equals the base's -- grade section 3 as written."
              % served_as_of)

    after_models = _models(after)
    base_models = _models(base)
    missing = [c for c in MODEL_CODES if c not in after_models]
    if missing:
        print("\nBLOCKED: served artifact is missing model(s) %r -- cannot grade." % missing)
        return 1

    # ---- the frontier each series declares (the classifier, measured) ----
    print("\n-- benchmark_last_date, read off the SERVED artifact (the classifier) --")
    frontier = {}
    for code in MODEL_CODES:
        bld = after_models[code].get('benchmark_last_date')
        if not isinstance(bld, dict):
            print("BLOCKED: model %s carries no benchmark_last_date -- the guard is not "
                  "deployed, or the deployed bytes are not the code leg's. Refusing to "
                  "grade against a default." % code)
            return 1
        frontier[code] = bld
        for source in ('index', 'etf'):
            last = bld.get(source)
            stale = (last is not None and served_as_of is not None and last < served_as_of)
            print("  %-4s %-5s last bar %-12s vs data_as_of %s  -> %s"
                  % (code, source, last, served_as_of, 'STALE' if stale else 'current'))

    def is_stale(code, source):
        last = frontier[code][source]
        return last is not None and served_as_of is not None and last < served_as_of

    # ---- the 300 benchmark cells ----
    print("\n-- the 300 benchmark-derived cells (5 models x 10 periods x 6 fields) --")
    buckets = {
        'stale_number_to_null': [],
        'stale_null_to_null': [],
        'current_number_equal': [],
        'current_null_unchanged': [],
    }
    bad = []
    total = 0
    for code in MODEL_CODES:
        for period in PERIODS:
            a_cell = after_models[code]['returns'][period]
            b_cell = base_models[code]['returns'][period]
            for source, fields in FIELDS_BY_SOURCE.items():
                stale = is_stale(code, source)
                for field in fields:
                    total += 1
                    av, bv = a_cell.get(field), b_cell.get(field)
                    where = "%s/%s/%s" % (code, period, field)
                    if stale:
                        if not _is_null(av):
                            if repull_landed:
                                buckets.setdefault('branch_b_number', []).append(where)
                            else:
                                bad.append("%s: stale series still serves %r" % (where, av))
                        elif _is_null(bv):
                            buckets['stale_null_to_null'].append(where)
                        else:
                            buckets['stale_number_to_null'].append(where)
                    else:
                        if _is_null(bv):
                            if _is_null(av):
                                buckets['current_null_unchanged'].append(where)
                            else:
                                bad.append("%s: current-sourced null became %r" % (where, av))
                        elif _same(av, bv):
                            buckets['current_number_equal'].append(where)
                        else:
                            bad.append("%s: CURRENT series moved, base %r -> served %r"
                                       % (where, bv, av))

    print("  stale-sourced, number -> null (the silent half, now refused) : %3d"
          % len(buckets['stale_number_to_null']))
    print("  stale-sourced, null -> null (the already-visible N/A)        : %3d"
          % len(buckets['stale_null_to_null']))
    print("  current-sourced, number byte-equal to the base               : %3d"
          % len(buckets['current_number_equal']))
    print("  current-sourced, null unchanged (min_points=5)               : %3d"
          % len(buckets['current_null_unchanged']))
    if buckets.get('branch_b_number'):
        print("  BRANCH B, re-pulled series serving a number                  : %3d"
              % len(buckets['branch_b_number']))
    print("  " + "-" * 62)
    print("  DENOMINATOR                                                  : %3d" % total)

    nulls = (len(buckets['stale_number_to_null']) + len(buckets['stale_null_to_null'])
             + len(buckets['current_null_unchanged']))
    numbers = len(buckets['current_number_equal']) + len(buckets.get('branch_b_number', []))
    print("  => %d null, %d numbers, of %d" % (nulls, numbers, total))

    if total != 300:
        failures.append("benchmark-cell denominator is %d, not 300" % total)
    for b in bad:
        failures.append(b)

    if not repull_landed:
        if nulls != 273:
            failures.append("expected 273 null benchmark cells, got %d" % nulls)
        if numbers != 27:
            failures.append("expected 27 number benchmark cells, got %d" % numbers)
        if len(buckets['stale_number_to_null']) != 171:
            failures.append("expected 171 number->null cells (the blast radius "
                            "@162e733fff), got %d" % len(buckets['stale_number_to_null']))

    # ---- the 100 model cells ----
    print("\n-- the 100 model cells (model + model_volatility) --")
    model_equal, model_moved = 0, []
    for code in MODEL_CODES:
        for period in PERIODS:
            a_cell = after_models[code]['returns'][period]
            b_cell = base_models[code]['returns'][period]
            for field in MODEL_FIELDS:
                if _same(a_cell.get(field), b_cell.get(field)):
                    model_equal += 1
                else:
                    model_moved.append("%s/%s/%s: base %r -> served %r"
                                       % (code, period, field,
                                          b_cell.get(field), a_cell.get(field)))
    print("  equal to the base: %d of %d (DENOMINATOR %d)"
          % (model_equal, model_equal + len(model_moved), model_equal + len(model_moved)))
    for m in model_moved:
        failures.append("MODEL CELL MOVED -- " + m)
    if model_equal != 100:
        failures.append("expected 100 model cells equal, got %d" % model_equal)

    # ---- the legacy key ----
    print("\n-- the legacy key %s --" % KEY_LEGACY)
    lbase, lbase_bytes, _, _ = _get(KEY_LEGACY, BASE_VERSIONS[KEY_LEGACY])
    lafter, lafter_bytes, lafter_ver, _ = _get(KEY_LEGACY)
    print("  BASE %d B  |  SERVED %d B  VersionId %s  data_as_of %s"
          % (lbase_bytes, lafter_bytes, lafter_ver, lafter.get('data_as_of')))
    lb, la = _models(lbase), _models(lafter)

    lp = {'number_to_null': 0, 'null_unchanged': 0, 'number_unchanged': 0, 'number_changed': []}
    ltotal = 0
    for code in MODEL_CODES:
        if code not in la:
            failures.append("legacy key is missing model %s" % code)
            continue
        for period in PERIODS:
            a_cell = la[code]['returns'][period]
            b_cell = lb[code]['returns'][period]
            for field in LEGACY_BENCHMARK_FIELDS:
                ltotal += 1
                av, bv = a_cell.get(field), b_cell.get(field)
                if _is_null(av) and not _is_null(bv):
                    lp['number_to_null'] += 1
                elif _is_null(av) and _is_null(bv):
                    lp['null_unchanged'] += 1
                elif _same(av, bv):
                    lp['number_unchanged'] += 1
                else:
                    lp['number_changed'].append("%s/%s/%s: %r -> %r"
                                                % (code, period, field, bv, av))
    lmodel_equal, lmodel_moved = 0, []
    for code in MODEL_CODES:
        if code not in la:
            continue
        for period in PERIODS:
            for field in MODEL_FIELDS:
                if _same(la[code]['returns'][period].get(field),
                         lb[code]['returns'][period].get(field)):
                    lmodel_equal += 1
                else:
                    lmodel_moved.append("%s/%s/%s" % (code, period, field))

    print("  benchmark cells: number -> null %d | null unchanged %d | number unchanged %d "
          "| number CHANGED %d   (DENOMINATOR %d)"
          % (lp['number_to_null'], lp['null_unchanged'], lp['number_unchanged'],
             len(lp['number_changed']), ltotal))
    print("  model cells: %d equal of %d (DENOMINATOR %d)"
          % (lmodel_equal, lmodel_equal + len(lmodel_moved), lmodel_equal + len(lmodel_moved)))
    print("  NOTE the legacy format carries ONE benchmark field, sourced from the INDEX")
    print("       series only. It has no ETF-sourced value, so the CTO half's \"INT's")
    print("       ETF-sourced values are byte-equal\" clause is VACUOUS here -- named, not")
    print("       silently passed.")
    print("  benchmark_last_date present on every legacy model: %s"
          % all('benchmark_last_date' in la[c] for c in MODEL_CODES if c in la))

    for c in lp['number_changed']:
        failures.append("LEGACY NUMBER CHANGED (rollback trigger) -- " + c)
    for m in lmodel_moved:
        failures.append("LEGACY MODEL CELL MOVED -- " + m)

    # ---- the timeseries ----
    print("\n-- the timeseries key --")
    tbase, tbase_bytes, _, _ = _get(KEY_TIMESERIES, BASE_VERSIONS[KEY_TIMESERIES])
    tafter, tafter_bytes, tafter_ver, _ = _get(KEY_TIMESERIES)
    tb, ta = tbase.get('timeseries', []), tafter.get('timeseries', [])
    rows_equal = (tb == ta)
    print("  BASE %d B / %d rows  |  SERVED %d B / %d rows  VersionId %s"
          % (tbase_bytes, len(tb), tafter_bytes, len(ta), tafter_ver))
    print("  rows byte-identical: %s  (generated_at differs by construction: %s -> %s)"
          % (rows_equal, tbase.get('generated_at'), tafter.get('generated_at')))
    if not rows_equal and not repull_landed:
        failures.append("timeseries rows moved -- the guard must not touch build_timeseries")

    # ---- verdict ----
    print("\n" + "=" * 78)
    for n in notes:
        print("NOTE: " + n)
    if failures:
        print("GRADE: FAIL -- %d failed row(s). CTO section 4 condition 4 rollback applies:"
              % len(failures))
        print("       the prior artifact through the module with one safe-apply, then")
        print("       copy-object of each key's base VersionId. Never a delete.")
        for f in failures[:40]:
            print("  FAIL: " + f)
        if len(failures) > 40:
            print("  ... and %d more" % (len(failures) - 40))
        print("=" * 78)
        return 1

    print("GRADE: PASS -- comprehensive %d null / %d byte-equal of %d; model %d/100 equal; "
          "legacy partition printed with denominator" % (nulls, numbers, total, model_equal))
    print("=" * 78)
    return 0


if __name__ == '__main__':
    sys.exit(main())
