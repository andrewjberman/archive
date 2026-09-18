"""EN-s-41 (LGIC_ENFORCE round 9) -- percent-style substitution census and negative arm.

Measures, at the run's own time, four things the scope decision on row LGIC_ENFORCE-W3-S17 rests on:

  A. POPULATION IN THE GRADED CORPUS. Every row's raw, pre-grade `current` in the two corpora the
     brace instrument reads: NAMING_CENSUS_REPORT.r8.md's `rows` fence (the census, 3254 rows at the
     round-9 cut) and PLACEHOLDER_CAMPAIGN_R6.json (resolved + carded + deferred, the corpus EN-m-39's
     negative arm drew from). A row is %-STYLE when its `current` carries a python printf conversion
     field (PCT_RE below), `%%` excluded.

  B. THE UNSCOPED READ. The same predicate over string literals in every TRACKED .py file
     (`git ls-files`), restricted to KEY-SHAPED literals (no whitespace, carries a '/'). This is a
     different instrument from comp-find and a different population from the census: it answers what
     the census's own extractor did NOT admit.

  C. THE BRACE RULE'S VERDICT on each construct: key.template_detection's test as NAMING_SCHEMA.json
     states it -- every {[^{}]+} token of the raw `current`, minus the four grade.placeholder
     sanctions; a non-empty remainder => KEY TEMPLATE, empty => ORDINARY.

  D. THE WIDENED RULE (decision WIDEN), its predicate READ FROM NAMING_SCHEMA.json
     key.template_detection.percent_field_regex -- so this instrument is bound by the stated rule and
     carries no regex of its own for it. NEGATIVE ARM: every ordinary census row plus one exemplar of
     each look-alike and each unnamed syntax that percent_field_excludes names -- each must read
     ORDINARY. POSITIVE CONTROL: LABEL_TRUTH_R7.json's 15 key_template_rows, the census %-rows and one
     exemplar per admitted form -- each must read TEMPLATE, so the negative arm cannot pass on a
     constant. PCT_RE above is the BROAD population predicate (any printf/strftime field); the
     widened rule is deliberately narrower than it.

Read-only. Writes nothing; prints one JSON document. Run from the worktree root:
    python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/percent_style_census_r9.py
"""

import io
import json
import os
import re
import subprocess
import sys

D1 = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/"
CENSUS = D1 + "NAMING_CENSUS_REPORT.r8.md"
CAMPAIGN = D1 + "PLACEHOLDER_CAMPAIGN_R6.json"
LABEL_TRUTH = D1 + "LABEL_TRUTH_R7.json"
SCHEMA = "org/standards/NAMING_SCHEMA.json"

# python printf conversion field: %[(name)][flags][width][.precision][length]type ; '%%' is a literal.
PCT_RE = re.compile(r"%(?:\([A-Za-z_][A-Za-z0-9_]*\))?[-#0 +]*(?:\*|\d+)?(?:\.(?:\*|\d+))?[hlL]?[diouxXeEfFgGcrsa]")
# strftime directives the same '%' introduces (a %-syntax runtime substitution of a different grammar)
STRF_RE = re.compile(r"%[YmdHMSjbBaAyIpfzZ]")
BRACE_RE = re.compile(r"\{[^{}]+\}")
SANCTIONED = {"{system}", "{source}", "{scope}", "{cadence}"}
LIT_RE = re.compile(r"(['\"])([^'\"\s]*?)\1")
# a URL-ENCODED literal, defined INDEPENDENTLY of any substitution predicate: every '%' in it is
# followed by two hex digits. MEASURED AMBIGUOUS on its own: '%05d' passes it (hex '05' then 'd')
# and is a real zero-padded printf field. So a GENUINE URL-encoded look-alike additionally
# requires every %XX to decode to a PRINTABLE byte (0x20-0x7E, or a UTF-8 lead/continuation
# byte >= 0x80) -- a control byte (%00-%1F) is never a real URL byte in a key or path -- and
# carries no brace token (a braced row is selected by (a), not (b), and is not a look-alike).
URLENC_RE = re.compile(r"%(?![0-9A-Fa-f]{2})")
PAIR_RE = re.compile(r"%([0-9A-Fa-f]{2})")


def genuine_urlenc(lit):
    if "%" not in lit or URLENC_RE.search(lit) or BRACE_RE.search(lit):
        return False
    return all(int(h, 16) >= 0x20 and int(h, 16) != 0x7F for h in PAIR_RE.findall(lit))


def pct_fields(s):
    s = str(s).replace("%%", "")
    return PCT_RE.findall(s) + [m for m in STRF_RE.findall(s) if m not in PCT_RE.findall(s)]


def template_verdict(current):
    rem = sorted(set(BRACE_RE.findall(str(current))) - SANCTIONED)
    return ("TEMPLATE" if rem else "ORDINARY"), rem


def fence_rows(path):
    t = io.open(path, encoding="utf-8").read()
    fences = re.findall(r"```json\n(.*?)\n```", t, re.S)
    rows = []
    for f in fences:
        v = json.loads(f)
        if isinstance(v, dict) and isinstance(v.get("rows"), list):
            rows.extend(v["rows"])
    return rows, len(fences)


def scan_corpus(name, rows):
    hits = []
    for i, r in enumerate(rows):
        cur = r.get("current", "")
        f = pct_fields(cur)
        if f:
            v, rem = template_verdict(cur)
            hits.append({"corpus": name, "index": i, "current": cur, "type": r.get("type"),
                         "plane": r.get("plane"), "fields": f, "brace_rule_verdict": v})
    return hits


def repo_scan():
    out = subprocess.run(["git", "ls-files", "-z", "--", "*.py"], capture_output=True, check=True)
    files = [p for p in out.stdout.decode("utf-8", "replace").split("\0") if p]
    scanned, unreadable, hits, urlenc = 0, 0, [], []
    for p in files:
        try:
            with io.open(p, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError):
            unreadable += 1
            continue
        scanned += 1
        for ln, line in enumerate(lines, 1):
            if "%" not in line or "/" not in line:
                continue
            for m in LIT_RE.finditer(line):
                lit = m.group(2)
                if "/" not in lit:
                    continue
                if "%" in lit and not URLENC_RE.search(lit):
                    urlenc.append({"file": p, "line": ln, "literal": lit})
                if lit.startswith(("http:", "https:")):
                    continue
                f = pct_fields(lit)
                if f:
                    hits.append({"file": p, "line": ln, "literal": lit, "fields": f,
                                 "brace_rule_verdict": template_verdict(lit)[0]})
    return {"tracked_py_files": len(files), "scanned": scanned, "unreadable": unreadable, "hits": hits,
            "urlenc": urlenc}


def main():
    census, nfence = fence_rows(CENSUS)
    c6 = json.load(io.open(CAMPAIGN, encoding="utf-8"))
    campaign = c6["resolved"] + c6["carded"] + c6["deferred"]
    lt = json.load(io.open(LABEL_TRUTH, encoding="utf-8"))["key_template_rows"]

    census_hits = scan_corpus("NAMING_CENSUS_REPORT.r8.md", census)
    campaign_hits = scan_corpus("PLACEHOLDER_CAMPAIGN_R6.json", campaign)
    repo = repo_scan()

    tier = ("bronze/", "silver/", "gold/", "platinum/", "state/", "code/")
    repo_tier = [h for h in repo["hits"] if h["literal"].startswith(tier)]
    census_currents = {h["current"] for h in census_hits}
    repo_files = sorted({h["file"] for h in repo["hits"]})
    repo_tier_files = sorted({h["file"] for h in repo_tier})
    repo_outside = [h for h in repo_tier if h["literal"] not in census_currents]

    # WIDEN predicate, read FROM THE SCHEMA so the instrument is bound by the stated rule, not by
    # a regex of its own: brace remainder (as before) OR a percent field per percent_field_regex,
    # searched after every '%%' pair is removed.
    td = json.load(io.open(SCHEMA, encoding="utf-8"))["key"]["template_detection"]
    widened_re = re.compile(td["percent_field_regex"])

    def widened_verdict(cur):
        s = str(cur)
        if template_verdict(s)[0] == "TEMPLATE":
            return "TEMPLATE"
        return "TEMPLATE" if widened_re.search(s.replace("%%", "")) else "ORDINARY"

    # NEGATIVE ARM: every construct the widened scope must NOT sweep in. (1) every ordinary census
    # row -- the 3254 less the 15 brace templates and the 2 %-rows; (2) look-alikes of a %-field
    # the schema's percent_field_excludes names (literal percent, URL-encoded byte, other printf
    # forms, strftime other than %d); (3) runtime-substitution syntaxes the bound does NOT name.
    known = {r["current"] for r in lt} | census_currents
    ordinary = [r["current"] for r in census if r.get("current") not in known]
    lookalikes = [
        ("literal percent pair", "silver/100%%/"),
        ("trailing literal percent", "gold/growth_100%"),
        ("URL-encoded slash", "bronze/a%2Fb/data.parquet"),
        ("URL-encoded space", "platinum/reports/Q1%20final/"),
        ("URL-encoded colon", "silver/ts%3A00/"),
        ("URL-encoded byte 0xDC (the %d collision)", "bronze/m%dcller/"),
        ("URL-encoded multibyte em dash", "gold/a%E2%80%94b/"),
        ("printf width form", "silver/%5s/"),
        ("printf float", "gold/rate_%f.json"),
        ("printf hex", "state/id_%x/"),
        ("printf repr", "silver/%r/"),
        ("printf %i", "gold/run_%i/"),
        ("strftime year/month", "bronze/snapshots/%Y/%m/"),
        ("strftime clock", "state/at_%H%M%S.json"),
        ("empty-brace str.format positional", "silver/{}/"),
        ("unbraced shell reference", "silver/$TABLE/"),
    ]
    real_urlenc = [("%s:%d" % (h["file"], h["line"]), h["literal"]) for h in repo["urlenc"]
                   if genuine_urlenc(h["literal"])]
    urlenc_shape_not_genuine = [dict(h, widened_verdict=widened_verdict(h["literal"]))
                                for h in repo["urlenc"] if not genuine_urlenc(h["literal"])]
    neg = [("census ordinary row", c) for c in ordinary] + lookalikes + real_urlenc
    neg_res = [{"case": c, "construct": s, "verdict": widened_verdict(s)} for c, s in neg]
    # POSITIVE CONTROL: the 15 brace templates, the 2 census %-rows, and the admitted forms
    pos = ([("LABEL_TRUTH_R7 key_template_row", r["current"]) for r in lt]
           + [("census %-row", h["current"]) for h in census_hits]
           + [("admitted form %d before '/'", "gold/run_%d/"),
              ("admitted form %(name)s", "silver/%(table)s/date=%(d)s/"),
              ("admitted form %02d", "silver/x/2026-07-%02d/"),
              ("strftime carrying %d", "bronze/snapshots/%Y/%m/%d/")])
    pos_res = [{"case": c, "current": s, "verdict": widened_verdict(s)} for c, s in pos]
    repo_sel = sum(1 for h in repo_tier if widened_verdict(h["literal"]) == "TEMPLATE")
    # a braced ${name} IS in scope through (a) -- recorded so the bound's edge is measured
    braced_env = widened_verdict("silver/${table}/")
    brace_only_on_pct_rows = [template_verdict(h["current"])[0] for h in census_hits]

    schema = json.load(io.open(SCHEMA, encoding="utf-8"))
    tng = schema["types_not_graded_by_kind"]
    not_graded = sorted(k for k, v in tng.items() if str(v).startswith("NOT GRADED"))
    routed = sorted(k for k, v in tng.items() if not str(v).startswith("NOT GRADED"))

    doc = {
        "census": {"file": CENSUS, "fences": nfence, "rows": len(census),
                   "percent_style_rows": len(census_hits), "hits": census_hits},
        "campaign": {"file": CAMPAIGN, "rows": len(campaign),
                     "percent_style_rows": len(campaign_hits), "hits": campaign_hits},
        "repo_unscoped": {"instrument": "git ls-files -z -- *.py ; key-shaped string literals (no whitespace, carries '/', not http) carrying a printf/strftime field",
                          "tracked_py_files": repo["tracked_py_files"], "scanned": repo["scanned"],
                          "unreadable": repo["unreadable"],
                          "key_shaped_hits": len(repo["hits"]), "key_shaped_files": len(repo_files),
                          "tier_prefixed_hits": len(repo_tier), "tier_prefixed_files": repo_tier_files,
                          "tier_prefixed_not_in_census": len(repo_outside),
                          "tier_prefixed": repo_tier},
        "widened_regex_read_from_schema": td["percent_field_regex"],
        "brace_only_verdict_on_census_pct_rows": brace_only_on_pct_rows,
        "negative_arm": {"tested": len(neg_res),
                         "rejected": sum(1 for r in neg_res if r["verdict"] == "ORDINARY"),
                         "census_ordinary_rows": len(ordinary), "lookalikes": len(lookalikes),
                         "real_url_encoded_repo_literals": len(real_urlenc),
                         "url_encoded_shape_total": len(repo["urlenc"]),
                         "url_encoded_shape_but_not_genuine": urlenc_shape_not_genuine,
                         "swept_in": [r for r in neg_res if r["verdict"] != "ORDINARY"],
                         "lookalike_cases": neg_res[len(ordinary):]},
        "positive_control": {"tested": len(pos_res),
                             "selected": sum(1 for r in pos_res if r["verdict"] == "TEMPLATE"),
                             "cases": pos_res},
        "repo_tier_prefixed_selected_by_widened_rule": repo_sel,
        "broad_predicate_hits_the_bound_leaves_ordinary": [
            h for h in repo["hits"] if widened_verdict(h["literal"]) == "ORDINARY"],
        "braced_env_reference_verdict": braced_env,
        "exclusion_table_measured": {"genuinely_not_graded": not_graded, "still_routed": routed},
    }
    json.dump(doc, sys.stdout, indent=1, ensure_ascii=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    os.chdir(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                            check=True).stdout.decode().strip())
    sys.exit(main())
