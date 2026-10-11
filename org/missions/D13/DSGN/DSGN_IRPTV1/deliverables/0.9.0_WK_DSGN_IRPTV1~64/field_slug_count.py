"""Count how many census field rows the producer's section_id rule gives a slug for, and how many map back to ONE census field.

Rule as read (infra/aws/lambda/investor-reporting/ycharts/extract/extract.py):
  :704-707  section_id = "%s.%s.c%d" % (row["section_id"], _slug(row["field"]), cand["column"]); section_type = row["section_id"]
  :927-928  _slug(name) = re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")
  :211-228  classify_sections: no fields -> CHART_ONLY; no "field" row, or grain starts with disclosure/glossary/methodology -> DISCLOSURE;
            else TYPED
  :237-255  census_field_rows: only TYPED sections, only rows holding a "field" key
  :650      a row whose unit is in NON_SCALAR_UNITS ("list", "table") (:113) never becomes a section
Usage: python -I field_slug_count.py <census.json> <out.json>
"""
import json
import re
import sys
from collections import Counter

NON_SCALAR_UNITS = ("list", "table")
DISCLOSURE_GRAINS = ("disclosure", "glossary", "methodology")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")


def main():
    census = json.loads(open(sys.argv[1], "rb").read().decode("utf-8"))
    sections = census["sections"]
    census_fields = 0
    derivable = 0
    exact = 0
    collisions = []
    not_derivable = Counter()
    per_class = Counter()
    chart_slugs = 0
    for s in sections:
        fields = s.get("fields", [])
        grain = str(s.get("grain", ""))
        typed = [f for f in fields if "field" in f]
        census_fields += len(typed)
        if not fields:
            cls = "CHART_ONLY"
        elif not typed or any(grain.startswith(g) for g in DISCLOSURE_GRAINS):
            cls = "DISCLOSURE"
        else:
            cls = "TYPED"
        per_class[cls] += 1
        if cls == "CHART_ONLY":
            chart_slugs += 1
        slugs = Counter(slug(f["field"]) for f in typed)
        for f in typed:
            if cls != "TYPED":
                not_derivable["section class " + cls] += 1
                continue
            if f.get("unit") in NON_SCALAR_UNITS:
                not_derivable["non-scalar unit " + str(f.get("unit"))] += 1
                continue
            derivable += 1
            sl = slug(f["field"])
            if sl and slugs[sl] == 1:
                exact += 1
        for sl, n in slugs.items():
            if n > 1:
                collisions.append({"section": s["id"], "slug": sl, "fields": n})
    out = {
        "sections": len(sections),
        "section_classes": dict(per_class),
        "census_fields": census_fields,
        "slugs_derivable": derivable,
        "exact_matches": exact,
        "slug_collisions_in_a_section": len(collisions),
        "collision_detail": collisions,
        "not_derivable_by_reason": dict(not_derivable),
        "chart_only_sections_slug_of_title_not_field": chart_slugs,
    }
    open(sys.argv[2], "wb").write((json.dumps(out, indent=2) + "\n").encode("ascii"))
    print(json.dumps(out, indent=2))


main()
