"""IV-e-119: for the cards that share one title, does section_id through the census give distinct names?

Reads ONLY repo files: the census and the producer's extract.py (to verify the lines it cites). No AWS, no request.
Rule as read in infra/aws/lambda/investor-reporting/ycharts/extract/extract.py:
  :113      NON_SCALAR_UNITS = ("list", "table")
  :211-234  classify_sections: no fields -> CHART_ONLY; no "field" row or disclosure grain -> DISCLOSURE; else TYPED
  :556-606  _row_values(max_columns=6): a field row yields up to 6 values, numbered c0..c5 left to right
            (same line, else below); "column" is that ORDINAL and nothing else
  :650      a NON_SCALAR unit never becomes a section
  :655-679  for a field the FIRST label hit that has candidates is used; one row of one page
  :685      a cell that is MISSING ('--', blank) is carried in `unlocated`, never as a section
  :704-707  section_id = "<S-code>.<slug of field>.c<column>"; section_type = "<S-code>"
  :927      _slug(name) = lower, runs of non [a-z0-9] -> "_", stripped
Usage: python -I shared_title_count.py <repo_root> <out.json>
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

CENSUS = "docs/briefs/sources/YCHARTS_COMPARISON_REPORT_FIELD_SCRAPE_20260909.json"
EXTRACT = "infra/aws/lambda/investor-reporting/ycharts/extract/extract.py"
NON_SCALAR_UNITS = ("list", "table")
DISCLOSURE_GRAINS = ("disclosure", "glossary", "methodology")
# Served counts by section_type, from the second walk (WALK_2_RESULT_READ_20261012.md section 2 / answer 3 and the issuer's spawn facts)
SERVED = {"S01": 2, "S03": 6, "S10": 4, "S14": 5, "S15": 35, "S16": 5, "S18": 46}
# Columns per located field under the producer's rule, by what the census says the section's columns are:
#  entity sections (no axes, or axes.entity_labels): one column per compared entity (census: 2)
#  window/lookback sections: the first label hit is ONE row, whose values are the periods (census axes list length)
ENTITY_COLUMNS = 2


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")


def has_value(f):
    """True when the census holds at least one non-null value for the field (a null is '--' on the page: unlocated)."""
    vals = f.get("values") or {}
    for k, v in vals.items():
        if k in ("categories", "hierarchy"):
            continue
        if isinstance(v, list):
            if any(x is not None for x in v):
                return True
        elif v is not None:
            return True
    return False


def column_model(section):
    axes = section.get("axes") or {}
    for key in ("window", "lookback"):
        if isinstance(axes.get(key), list):
            return key, len(axes[key])
    if section["id"] == "S10":
        return "category", None
    return "entity", ENTITY_COLUMNS


def min_still_shared(n, k):
    """Fewest cards that can share a name when n cards carry k distinct possible names, each name at least once."""
    if n <= k:
        return 0
    singles = min(k - 1, n - 2)
    return n - singles


def main():
    root = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2])
    census = json.loads((root / CENSUS).read_bytes().decode("utf-8"))
    extract_lines = (root / EXTRACT).read_bytes().decode("utf-8").splitlines()
    cited = {113: "NON_SCALAR_UNITS", 556: "def _row_values", 650: "NON_SCALAR_UNITS", 704: "sections.append",
             705: "section_id", 927: "def _slug"}
    cite_check = {str(n): (needle in extract_lines[n - 1]) for n, needle in cited.items()}
    max_columns_ok = "max_columns=6" in extract_lines[555]

    secs = {s["id"]: s for s in census["sections"]}
    groups = {}
    for sid in SERVED:
        s = secs[sid]
        typed = [f for f in s.get("fields", []) if "field" in f]
        scalar = [f for f in typed if f.get("unit") not in NON_SCALAR_UNITS]
        located = [f for f in scalar if has_value(f)]
        slugs = Counter(slug(f["field"]) for f in typed)
        by_slug = {slug(f["field"]): f["field"] for f in typed}
        kind, ncols = column_model(s)
        derived = None
        ids = []
        if ncols is not None:
            for f in located:
                for c in range(ncols):
                    ids.append("%s.%s.c%d" % (sid, slug(f["field"]), c))
            derived = len(ids)
        resolved = [by_slug.get(i.split(".")[1]) for i in ids]
        named = sum(1 for r in resolved if r)
        cnt = Counter(r for r in resolved if r)
        shared_cards = sum(n for n in cnt.values() if n > 1) + (len(resolved) - named)
        groups[sid] = {
            "section_type": sid, "section_title": s["title"], "census_fields": len(typed),
            "scalar_fields": len(scalar), "fields_with_a_census_value": len(located),
            "slug_collisions_in_section": sum(1 for v in slugs.values() if v > 1),
            "column_means": kind, "columns_per_field_under_rule": ncols,
            "served_cards": SERVED[sid], "derived_cards": derived,
            "derived_matches_served": (derived == SERVED[sid]) if derived is not None else None,
            "derived_named": named if derived is not None else None,
            "derived_unnamed": (len(resolved) - named) if derived is not None else None,
            "derived_distinct_names": len(cnt) if derived is not None else None,
            "derived_still_shared": shared_cards if derived is not None else None,
            "derived_group_sizes": dict(Counter(cnt.values())) if derived is not None else None,
            "served_still_shared_min": min_still_shared(SERVED[sid], len(located)),
            "sample_section_ids": ids[:4],
        }
    g = groups["S18"]
    s18_ids = []
    for f in [f for f in secs["S18"]["fields"] if "field" in f and f.get("unit") not in NON_SCALAR_UNITS and has_value(f)]:
        for c in range(ENTITY_COLUMNS):
            s18_ids.append("S18.%s.c%d" % (slug(f["field"]), c))
    other = [{"section_type": k, "cards": v["served_cards"], "still_shared": v["served_still_shared_min"],
              "still_shared_basis": "LOWER BOUND on the served count: %d cards over at most %d locatable fields" % (
                  v["served_cards"], v["fields_with_a_census_value"]),
              "derived_cards": v["derived_cards"], "derived_still_shared": v["derived_still_shared"],
              "column_means": v["column_means"]}
             for k, v in groups.items() if k != "S18"]
    record = {
        "to_id": "DSGN_IRPTV1.TO-IV-e-119", "worker": "0.9.0_WK_DSGN_IRPTV1~67", "product_change": False,
        "cards": len(s18_ids), "served_count": SERVED["S18"], "served_count_reproduced": len(s18_ids) == SERVED["S18"],
        "named": g["derived_named"], "unnamed": g["derived_unnamed"], "distinct_names": g["derived_distinct_names"],
        "still_shared": g["derived_still_shared"], "groups": [{"size": k, "count": v} for k, v in g["derived_group_sizes"].items()],
        "served_46_still_shared_min": g["served_still_shared_min"],
        "verdict": "SOME_SHARED" if g["derived_still_shared"] > 0 else "ALL_SEPARATE",
        "source": "PRODUCER_RULE_ON_CENSUS",
        "source_basis": ("No retained producer answer sits in the repo: ycharts/extract/fixtures/synthetic_pdf holds three synthetic PDFs "
                         "(overview, comparison, multicomp) and a MANIFEST, no answer JSON with section_id values; the portal fixtures "
                         "were not found to carry S18 ids (Grep for S18. under portal/src/pages/InvestorReporting: 0 files). So the ids "
                         "are produced by applying extract.py :704-707 to the S18 fields of the census, two entity columns."),
        "method": ("1) read extract.py: section_id = S-code + slug(field) + c<column>, column = ordinal of the value on the located row "
                   "(:556-606, max 6), a null census cell is unlocated (:685) and a list/table unit is skipped (:650); 2) take the census "
                   "S18 fields, drop non-scalar units and fields whose every census value is null, emit one id per field per entity "
                   "column (2 entities in the census); 3) resolve each id's slug back to the census field of its section; 4) a card is "
                   "'still shared' when another card resolves to the same field, because the column's meaning is not on the wire so "
                   "it cannot enter the name; 5) for the served count 46 (not reproduced) a pigeonhole lower bound on still_shared "
                   "is given: cards minus the most singletons the locatable fields allow."),
        "other_groups": other,
        "column_meaning": ("The column is the ORDINAL of a value on the located row (extract.py :604-606, 'column': i), not a name. Which "
                           "thing it stands for depends on the section: in entity sections (S01, S03, S18 in the census: no axes) c0 is "
                           "the first compared security and c1 the second; in S14/S15/S16 the first label hit is one entity row and the "
                           "columns are its periods (census axes window/lookback: 5 entries). Nothing on the wire says which: a section "
                           "carries the eight keys only; the answer's data holds request_ref ids, vendor_artifact, effective_inputs "
                           "(read_back, holdings_fingerprint, an open settings map), extraction_validation, extraction_coverage; no "
                           "entity name or period label (contracts/wire/AnalysisReport.ts :12-100; schema section_id is a plain string)."),
        "page_can_print_column": False,
        "remainder_needs": ("A wire member that names what each column of a section is: per section_type (or per section row) an ordered "
                            "list of column labels, entity names or period labels (e.g. section_columns: [{section_type, columns: "
                            "[{index, kind: ENTITY|PERIOD, label}]}]), or one label per section row (column_label). The producer holds "
                            "the compared security names (request composition) and the period headers it read; the page does not."),
        "limits": ("Derived 36, served 46: the walked report's column counts per field are not on any retained file, so the 10-card gap "
                   "is unexplained (candidates: a third entity column on some rows, more than two numeric tokens on a row up to the "
                   "6 cap, a different report shape). No answer file of the walk is in the repo. S10, S03, S16 served counts also "
                   "differ from the model. The census is one scraped report; the walked report may differ."),
    }
    result = {
        "census_sha_note": "read from " + CENSUS,
        "extract_line_cites_verified": cite_check, "max_columns_6_at_line_556": max_columns_ok,
        "s18": g, "s18_derived_section_ids": s18_ids,
        "other_groups": other, "groups_all": groups,
        "served_total_typed": sum(SERVED.values()),
    }
    record["calc"] = result
    out_path.write_bytes((json.dumps(record, indent=2) + "\n").encode("ascii"))
    print(json.dumps({"s18": {k: g[k] for k in ("served_cards", "derived_cards", "derived_named", "derived_distinct_names",
                                                "derived_still_shared", "derived_group_sizes", "served_still_shared_min")},
                      "cites": cite_check, "other": other}, indent=1))


main()
