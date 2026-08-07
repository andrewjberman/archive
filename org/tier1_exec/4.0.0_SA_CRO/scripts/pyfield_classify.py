#!/usr/bin/env python3
"""pyfield_classify.py -- the STATED DECISION PROCEDURE over pyfield_column_probe.py evidence.

TO: NFRA_PYFIELD.TO-0.  Author: 4.0.0_SA_CRO.

THREE STATES, and the third is not a formality (TO-0 acceptance criterion 2):
    column                    the base is a DataFrame/Series, so the subscript names a COLUMN
    not-column                the base is a dict / record / API response / mapping
    undecidable-at-this-site  the evidence AT THE CALL SITE does not disambiguate

>> CONFLICT RESOLVES TO UNDECIDABLE, NEVER TO A VERDICT. <<
If a column-rule and a not-column-rule both fire, the site is undecidable. Forcing it would be
the exact defect TO-0 names: the ambiguity gets absorbed where nobody can see it and the
denominator silently inherits the forcing. The same applies to a base with no evidence at all --
absence of evidence is undecidable, never "not a column."

WHY A PROCEDURE AND NOT A HAND-READ OF EVERY SITE: 4,406 name-based sites is beyond an honest
hand pass, and a hand-picked subset measures the author (criterion 4). So the procedure is
applied MECHANICALLY to the full population, and its own error rate is then measured by
hand-auditing a SYSTEMATIC sample (first-per-file alphabetical). The audit is what converts the
procedure's output from an assertion into a measurement with an error bar.

RETURN-TYPE FACTS BELOW WERE READ FROM SOURCE, NOT ASSUMED, AND THE DENOMINATOR WAS ENUMERATED:
  _read_s3          21 definitions, ALL return pd.read_parquet(...) on the success path
  _read_s3_parquet  12 definitions, ALL return pd.read_parquet(...) on the success path
                    (the `None` / `pd.DataFrame()` returns are missing-key branches -- never a dict)
  floored_distribution_stats  -> dict   (annotated)
  build_nna_atomic  -> tuple[pd.DataFrame, dict]  -- SAME evidence shape, DIFFERENT truth by
                    tuple position, which this evidence level cannot see -> undecidable by design.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys

# ---- verified-by-reading return maps (see module docstring for the enumeration) --------------
DF_RETURNING_HELPERS = {"_read_s3", "_read_s3_parquet"}
DICT_RETURNING_HELPERS = {"floored_distribution_stats"}
TUPLE_MIXED_HELPERS = {"build_nna_atomic"}          # DataFrame AND dict, position-dependent

MINIMAL = {"value_counts", "nunique", "fillna"}     # impossible on dict/list/str/tuple/set/object

DICT_RHS_TOKENS = (
    "dict-literal", "dict-comprehension", "call:dict", "call:defaultdict",
    "call:OrderedDict", "call:Counter", "call:json.loads", "call:json.load",
)
RESPONSE_RHS_TOKENS = ("get_object", "list_objects", "head_object", "get_item", "describe_")
PD_CTOR_TOKENS = ("call:pd.", "call:pandas.")


def tail(shape: str) -> str:
    """'call:a.b.c' -> 'c'."""
    return shape.split(":", 1)[-1].split(".")[-1] if ":" in shape else shape


def classify(rec):
    """Return (verdict, reason). Pure function of the site's evidence record."""
    ev = rec.get("evidence") or {}
    assigned = ev.get("assigned_from") or []
    loop = ev.get("loop_over")
    col_reasons, not_reasons = [], []

    # ---------------- COLUMN evidence ----------------
    if rec.get("usage_attr") in MINIMAL:
        col_reasons.append(f"usage .{rec['usage_attr']}() cannot exist on a dict/list/str")
    if rec.get("binding_hit"):
        col_reasons.append("base resolves flow-locally to a pandas constructor")
    if loop and loop.startswith("call:") and loop.endswith(".iterrows"):
        col_reasons.append("loop var over .iterrows() is a Series -> subscript is a column")
    for a in assigned:
        if a.startswith(PD_CTOR_TOKENS):
            col_reasons.append(f"assigned from {a[5:]}")
        elif a.startswith("call:") and tail(a) in DF_RETURNING_HELPERS:
            col_reasons.append(f"assigned from {tail(a)}() -- verified DataFrame-returning")

    # ---------------- NOT-COLUMN evidence ----------------
    for a in assigned:
        if any(t in a for t in DICT_RHS_TOKENS):
            not_reasons.append(f"assigned from {a} (a mapping)")
        elif any(t in a for t in RESPONSE_RHS_TOKENS):
            not_reasons.append(f"assigned from {a} (an API response dict)")
        elif a.startswith("call:") and tail(a) in DICT_RETURNING_HELPERS:
            not_reasons.append(f"assigned from {tail(a)}() -- annotated -> dict")
    if loop:
        if loop.startswith("call:") and tail(loop) == "get":
            not_reasons.append("loop var over a paginator/response .get(...) list of dicts")
        elif loop.startswith("call:") and tail(loop) == "items":
            not_reasons.append("loop var over .items() of a mapping")
        elif loop.startswith(("dict-literal", "list-literal")):
            not_reasons.append(f"loop var over a {loop}")

    # ---------------- resolution ----------------
    if col_reasons and not_reasons:
        return ("undecidable-at-this-site",
                "CONFLICT: " + col_reasons[0] + " || " + not_reasons[0])
    if col_reasons:
        return ("column", col_reasons[0])
    if not_reasons:
        return ("not-column", not_reasons[0])

    # ---------------- explicit undecidable causes (named, not lumped) ----------------
    for a in assigned:
        if a.startswith("call:") and tail(a) in TUPLE_MIXED_HELPERS:
            return ("undecidable-at-this-site",
                    f"{tail(a)}() returns tuple[DataFrame, dict]; tuple position not tracked")
    if any(a == "const:NoneType" for a in assigned) and len(set(assigned)) == 1:
        return ("undecidable-at-this-site", "base only ever assigned None here; real bind is elsewhere")
    if any(a == "ifexp" for a in assigned):
        return ("undecidable-at-this-site", "base assigned from a conditional expression (two shapes)")
    if assigned:
        return ("undecidable-at-this-site", f"unresolved RHS shape: {assigned[0]}")
    if loop:
        return ("undecidable-at-this-site", f"loop var over unresolved iterable: {loop}")
    if ev.get("is_param"):
        return ("undecidable-at-this-site", "base is a function parameter; caller not resolved (flow-local limit)")
    if ev.get("with_from"):
        return ("undecidable-at-this-site", f"base from with-context: {ev['with_from']}")
    return ("undecidable-at-this-site", "no binding evidence for this base in any enclosing scope")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("sites_jsonl")
    ap.add_argument("--out", required=True, help="per-site verdict records (criterion 2 / req 2)")
    ap.add_argument("--audit-out", default=None, help="systematic audit sample for hand-checking")
    ap.add_argument("--audit-every", type=int, default=0,
                    help="also take every Nth site of each stratum into the audit sample")
    args = ap.parse_args(argv)

    # errors="replace" per the strict-utf8 gate. Safe for this payload rather than merely
    # compliant: json.dumps writes ASCII by default, and a replaced byte would still fail LOUD
    # at json.loads (invalid JSON) rather than silently corrupting a record.
    lines = open(args.sites_jsonl, encoding="utf-8", errors="replace").read().splitlines()
    header = json.loads(lines[0])["_header"]
    recs = [json.loads(ln) for ln in lines[1:]]
    name = [r for r in recs if r["base_kind"] == "name"]

    for r in recs:
        v, why = classify(r)
        r["verdict"], r["reason"] = v, why
        r["locus"] = f"{r['file']}:{r['line']}:{r['col']}"

    # ---- strata (re-derivable definitions; see the deliverable for the PRD mapping) ----
    def stratum(r):
        if r["base_kind"] != "name":
            return "S-D expr-base"
        if r["usage_WIDE"] and not r["binding_hit"]:
            return "S-A usage-only"
        if r["usage_WIDE"]:
            return "S-B usage+binding"
        if r["binding_hit"]:
            return "S-B2 binding-only"
        return "S-C neither-axis"

    for r in recs:
        r["stratum"] = stratum(r)
        r["marker_band"] = bool(r["base_kind"] == "name" and r["usage_WIDE"] and not r["usage_MINIMAL"])

    print(f"probe vintage: {header['vintage']}   corpus: {header['corpus']}")
    print(f"denominator_grain: {header['denominator_grain']}")
    print(f"sites: {len(recs)}  name-based: {len(name)}  expr-based: {len(recs)-len(name)}\n")

    def table(rows, label, denom=None):
        c = collections.Counter(r["verdict"] for r in rows)
        n = len(rows) if denom is None else denom
        print(f"-- {label} (n={len(rows)}) --")
        for v in ("column", "not-column", "undecidable-at-this-site"):
            pct = 100.0 * c[v] / n if n else 0.0
            print(f"     {v:<26} {c[v]:>5}  ({pct:5.1f}%)")
        return c

    table(name, "ALL name-based")
    for s in ("S-A usage-only", "S-B usage+binding", "S-B2 binding-only", "S-C neither-axis"):
        table([r for r in name if r["stratum"] == s], s)
    table([r for r in name if r["marker_band"]], "MARKER BAND (WIDE minus MINIMAL)")
    table([r for r in recs if r["base_kind"] != "name"], "S-D expr-base")

    print("\n-- top undecidable REASONS (the residue, named not lumped) --")
    ud = [r for r in name if r["verdict"] == "undecidable-at-this-site"]
    for why, n in collections.Counter(r["reason"].split(";")[0].split(":")[0] for r in ud).most_common(10):
        print(f"     {n:>5}  {why}")

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"_header": {**header, "classifier": "pyfield_classify.py"}}) + "\n")
        for r in recs:
            fh.write(json.dumps({k: r[k] for k in
                                 ("locus", "file", "line", "col", "scope", "base", "base_kind",
                                  "key", "src", "stratum", "marker_band", "usage_attr",
                                  "binding_hit", "verdict", "reason")}) + "\n")
    print(f"\nwrote {len(recs)} per-site verdict records -> {args.out}")

    # ---- systematic audit sample: FIRST-PER-FILE alphabetical, per stratum ----
    if args.audit_out:
        by = collections.defaultdict(list)
        for r in sorted(name, key=lambda r: (r["stratum"], r["file"], r["line"], r["col"])):
            by[(r["stratum"], r["file"])].append(r)
        sample = [v[0] for k, v in sorted(by.items())]          # first-per-file, per stratum
        if args.audit_every > 1:
            for s in sorted(set(r["stratum"] for r in name)):
                rows = sorted([r for r in name if r["stratum"] == s],
                              key=lambda r: (r["file"], r["line"], r["col"]))
                sample.extend(rows[::args.audit_every])
        seen, uniq = set(), []
        for r in sample:
            if r["locus"] not in seen:
                seen.add(r["locus"])
                uniq.append(r)
        uniq.sort(key=lambda r: (r["stratum"], r["file"], r["line"]))
        with open(args.audit_out, "w", encoding="utf-8") as fh:
            for r in uniq:
                fh.write(json.dumps(r) + "\n")
        print(f"audit sample (first-per-file alphabetical per stratum"
              f"{', + every %dth' % args.audit_every if args.audit_every > 1 else ''}): "
              f"{len(uniq)} sites -> {args.audit_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
