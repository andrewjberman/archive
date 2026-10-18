"""ck2_sites.py -- AMGT_HARVST HVST-ck-2 step a (round 96). READ-ONLY: lists the path-component sites this change reads.

Run from the worktree root. Writes ck2_sites.out beside itself: one CHANGED line per prefix site (file:line, the prefix
template, the tool, the shape dir or object) and one NOT-CHANGED line per prefix derived from a COMPONENT of the key. The
line numbers are found by reading the post-change modules; the KEYED table is read from harvest_identity.py itself.
"""

import os
import re

ROOT = os.getcwd()
APP = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway", "app")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "ck2_sites.out")

SITES = (
    ("harvest_research.py", "_union_json(P_MANAGEMENT", "management/v1/%s/", "dir", "harvest_get_research"),
    ("harvest_research.py", "union_rows(path_component_reads(P_FILINGS", "filings/v1/%s/", "dir",
     "harvest_get_filing_analysis"),
    ("harvest_research.py", "object_pick(P_DRAFTING", "drafting/v1/%s.json", "object", "harvest_get_filing_analysis"),
    ("harvest_research.py", "_union_json(P_PEERS", "peers/v1/%s/", "dir", "harvest_get_peers_and_scores"),
    ("harvest_research.py", "object_pick(P_SCORES", "scores/v1/%s.json", "object", "harvest_get_peers_and_scores"),
    ("harvest_research.py", "_union_json(P_POSTURE", "posture/v1/%s/", "dir", "harvest_get_peers_and_scores"),
    ("harvest_figures.py", "picks = _json_under_paths(MODEL_PREFIX + \"%s/\", spelled)", "derived/model_block/%s/", "dir",
     "harvest_get_fundamentals"),
    ("harvest_figures.py", "_json_under_paths(FYE_PREFIX + \"%s/\", spelled)", "derived/model_block_fye/%s/", "dir",
     "harvest_get_fundamentals"),
    ("harvest_figures.py", "picks = _json_under_paths(MODEL_PREFIX + \"%s/\", spelled)      # HVST-ck-2: canonical and legacy raw",
     "derived/model_block/%s/", "dir", "harvest_query_columns"),
    ("harvest_identity.py", "path_component_reads(\"packs/%s/input_ledger.json\"", "packs/%s/input_ledger.json", "object",
     "harvest_security_coverage"),
)

# the KEYED table templates, as harvest_identity.py names them
TEMPLATE_SHAPE = {"_DIR": "dir", "_FILE": "object", "_ROOT": "root", "_CC": "cc", "_HIVE": "partition"}


def lines_of(fname):
    with open(os.path.join(APP, fname), "r", encoding="utf-8") as fh:
        return fh.read().split("\n")


def find(fname, needle):
    """The line numbers whose text holds the needle. The fundamentals and query sites share one call text; the query line is
    the one that carries its own comment, so the fundamentals site is the line WITHOUT the HVST-ck-2 comment."""
    hits = [i + 1 for i, text in enumerate(lines_of(fname)) if needle in text]
    if needle.startswith("picks = _json_under_paths(MODEL_PREFIX") and "HVST-ck-2: canonical" not in needle:
        hits = [h for h in hits if "# HVST-ck-2" not in lines_of(fname)[h - 1]]
    return hits


def keyed_entries():
    """(line, prefix, template constant) of every KEYED row of harvest_identity.py, read from the file."""
    out = []
    for i, text in enumerate(lines_of("harvest_identity.py")):
        m = re.match(r'^\s+\("([^"]+)", (_[A-Z]+), "[a-z]+"\),\s*$', text)
        if m:
            out.append((i + 1, m.group(1), m.group(2)))
    return out


def main():
    rows = []
    out_handle = open(OUT_PATH, "w", encoding="utf-8", newline="\n")

    def out(text):
        print(text, flush=True)
        out_handle.write(text + "\n")

    out("CK2-SITES HVST-ck-2 path-component sites read by the change (round 96); the modules as they stand after the change")
    for fname, needle, prefix, shape, tool in SITES:
        hits = find(fname, needle)
        assert hits, (fname, needle)
        for line in hits:
            rows.append("CHANGED %s:%d prefix=%s tool=%s shape=%s" % (fname, line, prefix, tool, shape))
    for line, prefix, const in keyed_entries():
        shape = TEMPLATE_SHAPE.get(const, "?")
        if const == "_HIVE":
            continue
        if const in ("_DIR", "_FILE"):
            display = prefix + ("%s/" if const == "_DIR" else "%s")
            rows.append("CHANGED harvest_identity.py:%d prefix=%s tool=harvest_security_coverage shape=%s"
                        % (line, display, "dir" if const == "_DIR" else "object"))
        elif const == "_ROOT":
            rows.append("NOT-CHANGED %s<root of key>/ reason=root component of the key (the ticker root, BP/ or BP-SLASH-/ "
                        "as typed), 0 objects under both spellings in ck1_census.out (MATRIX publication-links 0/0/0/0) "
                        "[harvest_identity.py:%d]" % (prefix, line))
        elif const == "_CC":
            rows.append("NOT-CHANGED %s<cc of key>/ reason=country-code component of the key (BP/_LN/ or BP-SLASH-_LN/ as "
                        "typed), 0 objects under both spellings in ck1_census.out (MATRIX raw/seekingalpha 0/0/0/0) "
                        "[harvest_identity.py:%d]" % (prefix, line))
    changed = [r for r in rows if r.startswith("CHANGED")]
    not_changed = [r for r in rows if r.startswith("NOT-CHANGED")]
    for r in changed + not_changed:
        out(r)
    # the coverage FILE stems (drafting/v1/%s, scores/v1/%s) and the object forms (%s.json) are one template to the census
    distinct = sorted(set(r.split(" prefix=")[1].split(" ")[0].replace(".json", "") for r in changed))
    out("CK2-SITES-COUNT changed_sites=%d changed_prefixes=%d not_changed_prefixes=%d tools=%d"
        % (len(changed), len(distinct), len(not_changed),
           len(set(r.split(" tool=")[1].split(" ")[0] for r in changed))))
    out_handle.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
