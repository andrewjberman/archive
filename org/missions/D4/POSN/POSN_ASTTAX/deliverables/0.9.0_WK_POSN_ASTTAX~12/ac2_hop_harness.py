#!/usr/bin/env python3
"""
POSN_ASTTAX.TO-T3-1  T3-AC2 hop harness -- 0.9.0_WK_POSN_ASTTAX~12

Hop-tests the FIVE-CLASS value 'Commodities' through EVERY enumerated asset_class
hop in the two sibling consumers TO-S7-1 named but never tested.

READ-ONLY: imports / execs consumer source, writes nothing, deploys nothing.

Instruments (deliberately DIFFERENT from comp-read, so AC1 and AC2 do not
corroborate each other by repetition):
  1. substring-occurrence recount  -> independent denominator vs comp-read
  2. sys.settrace line tracing of a REAL call into the real module (file A)
  3. verbatim exec of the REAL source lines pulled by line number (file B)
Positive control: a known-dropping reducer must be reported SILENTLY DROPPED.
"""
import importlib.util
import io
import os
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, "infra", "aws", "lambda", "v2_portal", "yang_pipeline", "positioning")
FILE_A = os.path.join(BASE, "yang-generate-allocation-summary", "lambda_function.py")
FILE_B = os.path.join(BASE, "yang-generate-holdings-attribution", "lambda_function.py")
REL_A = "infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-allocation-summary/lambda_function.py"
REL_B = "infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-holdings-attribution/lambda_function.py"

PROBE = "Commodities"
TOKEN = "asset_class"

# ---------------------------------------------------------------- categories
# AC1 categories: dict-key construction / subscript / comparison branch /
# output field / mention.  MENTION lines are NOT hops (nothing can be dropped
# at a docstring).  Everything else IS a hop and MUST be tested.
MENTION = "mention"
HOPKINDS = ("dict-key-construction", "subscript", "comparison-branch",
            "output-field", "transform-assign", "container-plumbing",
            "default-lookup")


def read_lines(path):
    with io.open(path, "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def occurrences(line):
    """Independent recount: raw substring occurrences, same grain comp-read counts."""
    n, i = 0, 0
    while True:
        j = line.find(TOKEN, i)
        if j < 0:
            return n
        n += 1
        i = j + 1


def classify(line, lineno, in_doc):
    s = line.strip()
    if s.startswith("#"):
        return MENTION, "comment"
    if in_doc or s.startswith('"""') or s.startswith("'''") or s.startswith("- "):
        return MENTION, "docstring"
    if "logger." in s:
        return MENTION, "log-string"
    if s.startswith("def "):
        return MENTION, "def-signature"
    # real hops
    if ".get(" in s and ("'" + TOKEN + "'") in s:
        return "default-lookup", "dict .get with default"
    if s.startswith("if ") or s.startswith("elif ") or s.startswith("else") or " in (" in s or " not in " in s:
        return "comparison-branch", "branch on the value"
    if "': " in s or "':" in s and s.endswith(","):
        return "output-field", "emitted as a JSON field"
    if "[" in s and "]" in s and "=" in s:
        return "subscript", "keyed by the value"
    if "[" in s and "]" in s:
        return "subscript", "keyed by the value"
    if "=" in s and not s.startswith("return"):
        return "transform-assign", "assignment / reassignment"
    return "container-plumbing", "list/dict carried"


def enumerate_file(path, rel):
    lines = read_lines(path)
    hits = 0
    rows = []
    in_doc = False
    for i, line in enumerate(lines, start=1):
        # crude docstring tracking
        trips = line.count('"""') + line.count("'''")
        n = occurrences(line)
        if n:
            hits += n
            kind, why = classify(line, i, in_doc)
            rows.append((i, n, kind, why, line.strip()))
        if trips % 2 == 1:
            in_doc = not in_doc
    distinct = len(rows)
    hoplines = [r for r in rows if r[2] != MENTION]
    mentions = [r for r in rows if r[2] == MENTION]
    return {"rel": rel, "lines": len(lines), "hits": hits, "distinct": distinct,
            "rows": rows, "hops": hoplines, "mentions": mentions}


# ------------------------------------------------------- file A: real call
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def trace_call(fn, args, path):
    """Execute fn under settrace; record which lines of `path` ran and the
    asset_class-ish locals live at each."""
    seen = {}
    target = os.path.abspath(path)

    def tracer(frame, event, arg):
        if os.path.abspath(frame.f_code.co_filename) != target:
            return None
        if event == "line":
            ln = frame.f_lineno
            vals = {}
            for k in ("raw_asset_class", "asset_class", "asset_class_name"):
                if k in frame.f_locals:
                    vals[k] = frame.f_locals[k]
            grp = frame.f_locals.get("asset_class_groups")
            if isinstance(grp, dict):
                vals["_groups"] = sorted(grp.keys())
            acs = frame.f_locals.get("asset_classes")
            if isinstance(acs, list):
                vals["_names"] = [d.get("name") for d in acs if isinstance(d, dict)]
            seen.setdefault(ln, []).append(vals)
        return tracer

    sys.settrace(tracer)
    try:
        out = fn(*args)
        err = None
    except Exception as e:  # RAISES is a legitimate verdict
        out, err = None, "%s: %s" % (type(e).__name__, e)
        traceback.print_exc()
    finally:
        sys.settrace(None)
    return out, err, seen


FIVE_CLASS_HOLDINGS = [
    {"asset_class": "Commodities", "weight": 10.0, "asset_allocation": 0.10, "total_attribution": 0.20},
    {"asset_class": "Equity", "weight": 50.0, "asset_allocation": 0.50, "total_attribution": 0.60},
    {"asset_class": "Fixed Income", "weight": 25.0, "asset_allocation": 0.25, "total_attribution": 0.30},
    {"asset_class": "Real Estate", "weight": 10.0, "asset_allocation": 0.10, "total_attribution": 0.15},
    {"asset_class": "Cash", "weight": 5.0, "asset_allocation": 0.05, "total_attribution": 0.05},
]
TWO_CLASS_HOLDINGS = [
    {"asset_class": "Equity", "weight": 60.0, "asset_allocation": 0.6, "total_attribution": 0.7},
    {"asset_class": "Fixed Income", "weight": 40.0, "asset_allocation": 0.4, "total_attribution": 0.5},
]


def dropping_reducer(holdings, model_code):
    """POSITIVE CONTROL: a reducer that DOES silently drop the five-class value.
    If the harness cannot report this one SILENTLY DROPPED it cannot report any."""
    keep = {"Fixed Income": 0.0, "Equity": 0.0}
    for h in holdings:
        ac = h.get("asset_class")
        if ac in keep:
            keep[ac] += h.get("weight") or 0
    return [{"name": k, "style_weight": v} for k, v in keep.items()]


def verdict_for(names, err):
    if err:
        return "RAISES"
    if names is None:
        return "RAISES"
    return "SURVIVES" if PROBE in names else "SILENTLY DROPPED"


# --------------------------------------------- file B: verbatim line exec
def src(path, a, b=None):
    lines = read_lines(path)
    b = a if b is None else b
    return "\n".join(txt for txt in lines[a - 1:b])


def dedent_block(text):
    body = list(text.split("\n"))
    pads = [len(ln) - len(ln.lstrip()) for ln in body if ln.strip()]
    cut = min(pads) if pads else 0
    return "\n".join(ln[cut:] if len(ln) >= cut else ln for ln in body)


def run_b_hop(label, lineno, endline, seed, watch):
    """exec the REAL source lines verbatim; report what happened to the value."""
    code = dedent_block(src(FILE_B, lineno, endline))
    ns = dict(seed)
    try:
        exec(compile(code, "%s:%d" % (REL_B, lineno), "exec"), ns)
        err = None
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
    got = {k: ns.get(k) for k in watch}
    seed_flat = " ".join(str(x) for x in seed.values())
    probe_in_scope = PROBE in seed_flat or PROBE.lower() in seed_flat
    if err:
        v = "RAISES"
    elif not probe_in_scope:
        # HONESTY GUARD: a hop the probe never entered cannot DROP the probe.
        # Reporting it as a drop would manufacture a finding.
        flat = " ".join(str(x) for x in got.values())
        v = "N/A PROBE-ABSENT (got %r -- hardcoded default, TO-S1-1's defect, not a five-class drop)" % flat
    else:
        flat = " ".join(str(x) for x in got.values())
        v = "SURVIVES" if PROBE in flat or PROBE.lower() in flat else "SILENTLY DROPPED"
    return {"label": label, "loc": "%s:%d" % (REL_B, lineno if endline is None else lineno),
            "span": (lineno, endline), "code": code, "err": err, "got": got, "verdict": v}


def main():
    print("=" * 108)
    print("T3-AC2  HOP HARNESS -- five-class probe value %r through both sibling consumers" % PROBE)
    print("worktree: %s" % ROOT)
    print("=" * 108)

    ea = enumerate_file(FILE_A, REL_A)
    eb = enumerate_file(FILE_B, REL_B)

    print("\n--- DENOMINATORS (independent recount; instrument = substring occurrence, NOT comp-read) ---")
    for e in (ea, eb):
        print("  %-92s" % e["rel"])
        print("    file lines=%d | token hits=%d | distinct lines carrying the token=%d | HOPS=%d | mentions=%d"
              % (e["lines"], e["hits"], e["distinct"], len(e["hops"]), len(e["mentions"])))
    print("  RECONCILE vs T3-AC1 comp-read: allocation-summary expect 93, got %d %s | holdings-attribution expect 49, got %d %s"
          % (ea["hits"], "MATCH" if ea["hits"] == 93 else "MISMATCH",
             eb["hits"], "MATCH" if eb["hits"] == 49 else "MISMATCH"))

    print("\n--- AC1 CLASSIFICATION: every distinct token line, banded (A = allocation-summary) ---")
    for e, tag in ((ea, "A"), (eb, "B")):
        print("  [%s] %s" % (tag, e["rel"]))
        for (ln, n, kind, why, text) in e["rows"]:
            t = text if len(text) <= 96 else text[:93] + "..."
            print("     %s:%-4d x%d  %-22s %s" % (tag, ln, n, kind, t))

    # ---------------- consumer A: REAL call, traced
    print("\n" + "=" * 108)
    print("CONSUMER A -- yang-generate-allocation-summary :: REAL call to aggregate_by_asset_class()")
    print("=" * 108)
    mod = load_module(FILE_A, "alloc_summary_under_test")
    out5, err5, seen5 = trace_call(mod.aggregate_by_asset_class, (FIVE_CLASS_HOLDINGS, "INT"), FILE_A)
    names5 = None if out5 is None else [r["name"] for r in out5]
    out2, err2, seen2 = trace_call(mod.aggregate_by_asset_class, (TWO_CLASS_HOLDINGS, "INT"), FILE_A)
    names2 = None if out2 is None else [r["name"] for r in out2]

    # --- drive the OUTER function for real, with a five-class S3 payload (test
    # double on OUR imported copy only; the repo file is untouched, nothing is
    # read from or written to AWS).
    payload = {"portfolios": {mc: {p: {"holdings": FIVE_CLASS_HOLDINGS}
                                   for p in ("qtd", "ytd", "1y", "si")}
                              for mc in mod.MODEL_CODES}}
    mod.s3_client = _FakeS3(payload)
    outer, err_outer, seen_outer = trace_call(
        mod.generate_allocation_summary, ({}, "2026-09-11", "opal-data-portal-v2", {}), FILE_A)
    outer_names = None
    if outer:
        outer_names = [r["name"] for r in outer["portfolios"]["INT"]["qtd"]["asset_classes"]]
    tot, err_tot, seen_tot = trace_call(mod.calculate_total, (out5 or [],), FILE_A)
    ph, err_ph, seen_ph = trace_call(mod.generate_placeholder_data, ("2026-09-11",), FILE_A)
    ph_names = None
    if ph:
        ph_names = [r["name"] for r in ph["portfolios"]["INT"]["qtd"]["asset_classes"]]
    # five classes INCLUDING hedge/cash reclass targets, weights NOT summing to
    # 100 -> exercises the hedge branch and the renormalisation branch.
    skew = [
        {"asset_class": "Commodities", "weight": 12.0, "asset_allocation": 0.10, "total_attribution": 0.20},
        {"asset_class": "Hedge", "weight": 8.0, "asset_allocation": 0.08, "total_attribution": 0.09},
        {"asset_class": "Equity", "weight": 40.0, "asset_allocation": 0.50, "total_attribution": 0.60},
        {"asset_class": "Fixed Income", "weight": 20.0, "asset_allocation": 0.25, "total_attribution": 0.30},
        {"asset_class": "Real Estate", "weight": 9.0, "asset_allocation": 0.10, "total_attribution": 0.15},
    ]
    out_sk, err_sk, seen_sk = trace_call(mod.aggregate_by_asset_class, (skew, "INT"), FILE_A)
    sk_names = None if out_sk is None else [r["name"] for r in out_sk]
    print("  SKEW run (hedge present, weights sum 89 not 100) OUTPUT: %s  err=%s" % (sk_names, err_sk))
    if out_sk:
        for r in out_sk:
            print("     row name=%-14s style_weight=%-8s policy_weight=%-7s bet=%s"
                  % (r["name"], r["style_weight"], r["policy_weight"], r["bet"]))

    # force the per-model EXCEPT branch (lines 220-223)
    bad = {"portfolios": {mc: {"qtd": "NOT-A-DICT"} for mc in mod.MODEL_CODES}}
    mod.s3_client = _FakeS3(bad)
    out_bad, err_bad, seen_bad = trace_call(
        mod.generate_allocation_summary, ({}, "2026-09-11", "opal-data-portal-v2", {}), FILE_A)
    bad_names = None
    if out_bad:
        bad_names = out_bad["portfolios"]["INT"]["qtd"]["asset_classes"]
    print("  EXCEPT-branch run (malformed portfolio) INT/qtd asset_classes: %s  err=%s"
          % (bad_names, err_bad))

    # five-class reach set vs other-input reach set, kept SEPARATE on purpose
    for extra in (seen_outer, seen_tot, seen_ph, seen_sk):
        for k, v in extra.items():
            seen5.setdefault(k, []).extend(v)
    seen_other = {}
    for extra in (seen2, seen_bad):
        for k, v in extra.items():
            seen_other.setdefault(k, []).extend(v)
    print("  OUTER generate_allocation_summary (five-class S3 payload) INT/qtd rows: %s  err=%s"
          % (outer_names, err_outer))
    print("  calculate_total over the five-class rows: %s  err=%s" % (tot, err_tot))
    print("  generate_placeholder_data rows: %s  err=%s   <-- FIXED-KEY placeholder path" % (ph_names, err_ph))

    print("  five-class input  : %s" % [h["asset_class"] for h in FIVE_CLASS_HOLDINGS])
    print("  five-class OUTPUT : %s   err=%s" % (names5, err5))
    print("  two-class  OUTPUT : %s   err=%s   (negative control: no five-class value present)" % (names2, err2))
    if out5:
        for r in out5:
            print("     row name=%-14s style_weight=%-8s policy_weight=%-7s bet=%-8s asset_allocation=%s"
                  % (r["name"], r["style_weight"], r["policy_weight"], r["bet"], r["asset_allocation"]))
    ctrl = dropping_reducer(FIVE_CLASS_HOLDINGS, "INT")
    ctrl_names = [r["name"] for r in ctrl]
    print("  POSITIVE CONTROL (known-dropping reducer) OUTPUT: %s -> harness verdict %s"
          % (ctrl_names, verdict_for(ctrl_names, None)))

    print("\n  EXECUTED-LINE TRACE (five-class run) -- which enumerated hops actually RAN:")
    ran = sorted(seen5.keys())
    hop_lines_a = [r[0] for r in ea["hops"]]
    print("    lines of file A executed under the five-class call: %d" % len(ran))
    print("    enumerated HOP lines in file A: %d" % len(hop_lines_a))

    rows_a = []
    for (ln, n, kind, why, text) in ea["rows"]:
        if kind == MENTION:
            continue
        obs = seen5.get(ln)
        if obs is None:
            # not reached under ANY five-class input -- say so, never call it a pass
            if ln in seen_other:
                v = "NOT-REACHED under five classes (runs ONLY on the 2-class / error path)"
            else:
                v = "NOT-REACHED by any run"
        else:
            vals = set()
            for d in obs:
                for k, val in d.items():
                    if k in ("_groups", "_names"):
                        vals.update([x for x in val if x])
                    elif isinstance(val, str):
                        vals.add(val)
            if PROBE in vals:
                v = "SURVIVES"
            else:
                v = "RAN, probe not bound at this line"
        rows_a.append((ln, kind, v, text))

    # ---------------- consumer B: verbatim source-line exec
    print("\n" + "=" * 108)
    print("CONSUMER B -- yang-generate-holdings-attribution :: VERBATIM exec of the real source lines")
    print("=" * 108)
    b_tests = [
        ("raw read from Excel cols 1-2 (df row -> asset_class)", 394, 395,
         {"df": _FakeDF(PROBE), "pd": _FakePd(), "row": 0, "str": str}, ["_probe"]),
        ("sub_asset_class carry-forward (417-421)", 417, 421,
         {"holding": {"asset_class": PROBE, "sub_asset_class": ""},
          "holdings": [{"asset_class": PROBE, "sub_asset_class": "Energy"}]}, ["holding"]),
        ("hierarchy/subtotal INITIALISERS (487-491)", 487, 491,
         {}, ["current_asset_class", "current_sub_asset_class", "asset_class_subtotals"]),
        ("Excel sub-hierarchy capture (562)", 562, 562,
         {"col_c": PROBE}, ["current_sub_asset_class"]),
        ("carry-forward fill when blank (411-414)", 411, 415,
         {"holding": {"asset_class": "", "sub_asset_class": ""},
          "holdings": [{"asset_class": PROBE, "sub_asset_class": "Energy"}]}, ["holding"]),
        ("carry-forward when ALREADY the probe (411-414)", 411, 415,
         {"holding": {"asset_class": PROBE, "sub_asset_class": "Energy"},
          "holdings": [{"asset_class": "Equity", "sub_asset_class": "US"}]}, ["holding"]),
        ("subtotal-name normalization else-branch (524-536)", 524, 536,
         {"col_b": PROBE, "policy_return_subtotal": 0.1, "asset_allocation_subtotal": 0.2,
          "style_allocation_subtotal": 0.3, "total_subtotal": 0.4, "asset_class_subtotals": {}},
         ["normalized_name", "asset_class_subtotals"]),
        ("Excel hierarchy capture (558)", 558, 558, {"col_b": PROBE}, ["current_asset_class"]),
        ("registry hit -> asset_class (585-586)", 585, 586,
         {"classification": {"asset_class": PROBE, "sub_asset_class": "Energy"},
          "current_asset_class": "", "current_sub_asset_class": ""},
         ["asset_class", "sub_asset_class"]),
        ("registry MISS -> Excel hierarchy fallback (589-590)", 589, 590,
         {"current_asset_class": PROBE, "current_sub_asset_class": "Energy"},
         ["asset_class", "sub_asset_class"]),
        ("registry MISS and NO hierarchy -> hardcoded default (589-590)", 589, 590,
         {"current_asset_class": "", "current_sub_asset_class": ""},
         ["asset_class", "sub_asset_class"]),
        ("display normalization chain, NO else (594-597)", 594, 597,
         {"asset_class": PROBE}, ["asset_class"]),
        ("output field emit (627-628)", 627, 628,
         {"asset_class": PROBE, "sub_asset_class": "Energy", "holding": {}}, ["_emit"]),
        ("subtotal key derive + lookup, subtotal PRESENT (643-647)", 643, 647,
         {"asset_class": PROBE, "holding": {},
          "asset_class_subtotals": {PROBE.lower(): {"policy_return": 0.9, "asset_allocation": 0.1}}},
         ["normalized_ac", "holding"]),
        ("subtotal key derive + lookup, subtotal ABSENT (643-647)", 643, 647,
         {"asset_class": PROBE, "holding": {},
          "asset_class_subtotals": {"equity": {"policy_return": 0.9}, "fixed_income": {"policy_return": 0.2}}},
         ["normalized_ac", "holding"]),
    ]
    results_b = []
    for label, a, b, seed, watch in b_tests:
        if label.startswith("raw read") or label.startswith("output field"):
            results_b.append(_special_b(label, a, b, seed, watch))
        else:
            results_b.append(run_b_hop(label, a, b, seed, watch))
    for r in results_b:
        print("\n  HOP %s  [%s]" % (r["span"], r["label"]))
        for cl in r["code"].split("\n"):
            print("      | %s" % cl)
        print("      -> %s   err=%s   state=%s" % (r["verdict"], r["err"], r["got"]))

    # ---------------- THE TABLE
    print("\n" + "=" * 108)
    print("T3-AC2 HOP TABLE -- one row per hop per consumer")
    print("=" * 108)
    print("%-2s %-6s %-24s %-46s %s" % ("#", "LINE", "HOP KIND", "FILE:LINE", "VERDICT"))
    print("-" * 108)
    i = 0
    drops = []
    for (ln, kind, v, text) in rows_a:
        i += 1
        print("%-2d %-6d %-24s %-46s %s" % (i, ln, kind, "A " + REL_A.split("/")[-2] + ":%d" % ln, v))
        if "DROP" in v:
            drops.append("A %s:%d" % (REL_A, ln))
    for r in results_b:
        i += 1
        ln = r["span"][0]
        print("%-2d %-6d %-24s %-46s %s" % (i, ln, "exec:" + r["label"][:18], "B " + REL_B.split("/")[-2] + ":%d" % ln, r["verdict"]))
        if "DROP" in r["verdict"]:
            drops.append("B %s:%d" % (REL_B, ln))
    print("-" * 108)

    # ---- MECHANICAL COVERAGE MAP: every enumerated hop line must be covered by
    # an executed span.  Uncovered lines are NAMED, never rounded away.
    b_spans = [r["span"] for r in results_b]
    b_hop_lines = [r[0] for r in eb["hops"]]
    b_cov, b_unc = [], []
    for ln in b_hop_lines:
        if any(a <= ln <= b for (a, b) in b_spans):
            b_cov.append(ln)
        else:
            b_unc.append(ln)
    a_hop_lines = [r[0] for r in ea["hops"]]
    a_cov = [ln for ln in a_hop_lines if ln in seen5]
    a_unc = [ln for ln in a_hop_lines if ln not in seen5]

    print("HOPS ENUMERATED (AC1, non-mention lines): A=%d  B=%d  TOTAL=%d"
          % (len(ea["hops"]), len(eb["hops"]), len(ea["hops"]) + len(eb["hops"])))
    print("HOPS COVERED BY AN EXECUTED SPAN:         A=%d/%d  B=%d/%d  TOTAL=%d/%d"
          % (len(a_cov), len(a_hop_lines), len(b_cov), len(b_hop_lines),
             len(a_cov) + len(b_cov), len(a_hop_lines) + len(b_hop_lines)))
    a_any = [ln for ln in a_hop_lines if ln in seen5 or ln in seen_other]
    a_any_unc = [ln for ln in a_hop_lines if ln not in seen5 and ln not in seen_other]
    print("HOPS COVERED BY *ANY* RUN (incl. 2-class + error path): A=%d/%d  B=%d/%d  TOTAL=%d/%d"
          % (len(a_any), len(a_hop_lines), len(b_cov), len(b_hop_lines),
             len(a_any) + len(b_cov), len(a_hop_lines) + len(b_hop_lines)))
    print("UNCOVERED BY ANY RUN -- A: %s | B: %s"
          % (a_any_unc if a_any_unc else "none", b_unc if b_unc else "none"))
    print("REACHED ONLY OUTSIDE A FIVE-CLASS INPUT -- A: %s"
          % [ln for ln in a_hop_lines if ln not in seen5 and ln in seen_other])
    print("UNCOVERED HOP LINES (five-class runs only) -- A: %s" % (a_unc if a_unc else "none"))
    print("UNCOVERED HOP LINES (five-class runs only) -- B: %s" % (b_unc if b_unc else "none"))
    print("HOP TEST ROWS IN THIS TABLE:            A=%d  B=%d  TOTAL=%d"
          % (len(rows_a), len(results_b), len(rows_a) + len(results_b)))
    print("SILENTLY-DROPPED SITES: %s" % (drops if drops else "NONE -- the probe value is never silently discarded"))
    print("\nFIVE-CLASS END-TO-END (consumer A, the decisive read): input classes=%d -> output rows=%s"
          % (len(FIVE_CLASS_HOLDINGS), names5))
    print("PROBE %r IN CONSUMER A OUTPUT: %s" % (PROBE, verdict_for(names5, err5)))
    print("PROBE %r THROUGH CONSUMER B CHAIN: %s"
          % (PROBE, "SURVIVES" if all(r["verdict"] == "SURVIVES" for r in results_b
                                      if "NO hierarchy" not in r["label"]) else "SEE TABLE"))


class _FakeS3(object):
    """Test double for boto3 s3 client -- returns a five-class payload in the
    exact shape the consumer's json.loads(response['Body'].read()) expects.
    No network, no credentials, no AWS call."""

    def __init__(self, payload):
        self._payload = payload

    def get_object(self, Bucket=None, Key=None):
        import json as _j
        return {"Body": io.BytesIO(_j.dumps(self._payload).encode("utf-8"))}

    def put_object(self, **kw):
        raise AssertionError("READ-ONLY HARNESS: put_object must never be called")


class _FakePd(object):
    @staticmethod
    def notna(x):
        return x is not None


class _FakeDF(object):
    def __init__(self, v):
        self._v = v
        self.shape = (10, 12)

    class _ILoc(object):
        def __init__(self, v):
            self._v = v

        def __getitem__(self, key):
            return self._v

    @property
    def iloc(self):
        return _FakeDF._ILoc(self._v)


def _special_b(label, a, b, seed, watch):
    """Hops whose real line needs a df/dict context -- still the REAL source text."""
    code = dedent_block(src(FILE_B, a, b))
    ns = dict(seed)
    err = None
    try:
        if label.startswith("raw read"):
            wrapped = "holding = {\n" + code.rstrip().rstrip(",") + "\n}"
            exec(compile(wrapped, "%s:%d" % (REL_B, a), "exec"), ns)
            got = {"_probe": ns.get("holding")}
        else:
            wrapped = "holding = {\n" + code.rstrip().rstrip(",") + "\n}"
            exec(compile(wrapped, "%s:%d" % (REL_B, a), "exec"), ns)
            got = {"_emit": ns.get("holding")}
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, e)
        got = {}
    flat = " ".join(str(x) for x in got.values())
    v = "RAISES" if err else ("SURVIVES" if PROBE in flat else "SILENTLY DROPPED")
    return {"label": label, "loc": "%s:%d" % (REL_B, a), "span": (a, b),
            "code": code, "err": err, "got": got, "verdict": v}


if __name__ == "__main__":
    main()
