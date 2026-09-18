"""EN-c-40 (LGIC_ENFORCE round 9) -- the hand-grading comparison instrument.

Compares LGIC_NAMING's three hand products against grade() at the COMPLETED census's vintage:

  N2  GRADING_RULE.md section 9 worked cases  -- per name: hand verdict (+ canonical form) vs grade()
  N6  exercises/n6-grader-a.tsv grader rows  -- per name: hand verdict (+ canonical form) vs grade()
  IV7 TENSION_RANKING.md ranked surfaces      -- per surface: the hand's figures vs the census rows' figures

grade() is imported from a tree materialised by `git archive <census commit>` of every path lib/opal_naming.py
reads for a grade, so the verdicts are those the r8 census's own code, schema and registry produce -- not HEAD's.
It is also run at the worktree's HEAD, and any case where the two vintages differ is printed.

AGREE on N2/N6 means the VERDICT is equal AND, where the hand gives a canonical form, the canonical form is equal
byte for byte. A RAISE hand verdict agrees only with grade() raising RaiseDefect.

AGREE on IV7 means EVERY figure the surface states is within the tolerance declared in IV7_TOLERANCE below,
fixed before the census figures were computed and never changed; the raw numbers are all recorded beside the
verdict so a reader can re-judge with any other bar. DISCLOSED: the GRAIN of rank 1's per-spelling figures, rank
1's first-token figure, rank 4's alarm figure, and every LOG_GROUP's tokenisation were revised AFTER a first run, to the grain the hand's
own source (infra/logic/09_NAMING_CENSUS.md s.1-s.3) states for each figure; the first run's figures are kept in
HAND_COMPARISON_R9.json under iv7_first_run so the revision can be judged against its effect.

Usage (from the worktree root):  python <this file> [--write <json path>]
Read-only on every input. Writes only the --write path (and a temp dir it removes).
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
NAMING = "org/missions/D14/LGIC/LGIC_NAMING/deliverables"
GRADING_RULE = NAMING + "/GRADING_RULE.md"
N6_TSV = NAMING + "/exercises/n6-grader-a.tsv"
TENSION = NAMING + "/TENSION_RANKING.md"
CENSUS = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r8.md"
GRADE_INPUTS = ["lib", "org/standards/NAMING_SCHEMA.json", "infra/logic/registry",
                "org/missions/DIRECTIVES.yaml", NAMING + "/LEGACY_SERVED_PATHS.json"]
# Declared before any census figure was computed: an approximate hand figure ("~N") agrees within 15%, an exact
# hand figure within 10%, and never tighter than +-2. The two censuses are five days and two instruments apart
# (hand: infra/logic/09_NAMING_CENSUS.md, 2026-09-13, 1,912 names over 19 types; census r8: 2026-09-18 live plane).
IV7_TOLERANCE = {"approx": 0.15, "exact": 0.10, "floor": 2}


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, check=True).stdout


def census_commit():
    return git("log", "-1", "--format=%H", "--", CENSUS).decode().strip()


def load_grade(commit):
    tmp = tempfile.mkdtemp(prefix="c40_grade_")
    tar = git("archive", "--format=tar", commit, *GRADE_INPUTS)
    import tarfile
    with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
        tf.extractall(tmp)  # trusted input: this repo's own git archive
    import importlib.util
    spec = importlib.util.spec_from_file_location("opal_naming_" + commit[:10], os.path.join(tmp, "lib", "opal_naming.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, tmp


def run_grade(mod, name, typ):
    try:
        v, c = mod.grade(name, typ)
        return v, c, None
    except mod.RaiseDefect as e:
        return "RAISE", None, str(e)


def worked_cases():
    t = io.open(GRADING_RULE, encoding="utf-8").read()
    sec = t[t.index("## 9. WORKED CASES"):t.index("## 10.")]
    fences = re.findall(r"```json\n(.*?)\n```", sec, re.S)
    assert len(fences) == 1, len(fences)
    return json.loads(fences[0])


def n6_rows():
    rows = []
    with io.open(N6_TSV, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    header = lines[0]
    for ln in lines[1:]:
        if not ln.strip():
            continue
        p = ln.split("\t")
        rows.append({"type": p[0], "name": p[1], "verdict": p[2], "canonical_form": (p[3] if len(p) > 3 and p[3] else None)})
    return header, len([x for x in lines if x.strip()]), rows


def census():
    t = io.open(CENSUS, encoding="utf-8").read()
    fences = re.findall(r"```json\n(.*?)\n```", t, re.S)
    return json.loads(fences[-1])


def compare_names(cases, mod_c, mod_h, cen):
    by_key = {}
    for r in cen["rows"]:
        by_key.setdefault((r["current"], r["type"]), []).append(("judged", r["plane"], r["verdict"], r["canonical"]))
    for r in cen["not_judged"]:
        by_key.setdefault((r["name"], r["type"]), []).append(("carded", r["plane"], "RAISE", None))
    out = {"compared": 0, "agree": 0, "disagree": 0, "disagreements": [], "per_case": [], "vintage_diffs": []}
    for c in cases:
        name, typ, hv, hc = c["name"], c["type"], c["verdict"], c.get("canonical_form")
        gv, gc, gerr = run_grade(mod_c, name, typ)
        hv2, hc2, _ = run_grade(mod_h, name, typ)
        if (gv, gc) != (hv2, hc2):
            out["vintage_diffs"].append({"name": name, "type": typ, "census_vintage": [gv, gc], "head": [hv2, hc2]})
        v_ok = hv == gv
        c_ok = hc is None or hc == gc
        ok = v_ok and c_ok
        seen = by_key.get((name, typ), [])
        rec = {"name": name, "type": typ, "hand": [hv, hc], "grade_at_census": [gv, gc],
               "raise_step": gerr, "in_census_r8": seen, "result": "AGREE" if ok else "DISAGREE"}
        out["per_case"].append(rec)
        out["compared"] += 1
        if ok:
            out["agree"] += 1
        else:
            out["disagree"] += 1
            out["disagreements"].append(rec)
    return out


# ------------------------------------------------------------------ IV7

def tokens(name):
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1-\2", s)
    return [t for t in re.split(r"[-/_.#:\s]+", s.lower()) if t]


def resource_part(name, typ):
    """The hand census derives a LOG_GROUP's tokens from the resource name it logs (09_NAMING_CENSUS.md s.2,
    'derived from the resource name'), so /aws/{service}/ and /aws/vendedlogs/{service}/ are stripped."""
    if typ == "LOG_GROUP":
        m = re.match(r"^/aws/(?:vendedlogs/)?[^/]+/(.*)$", name)
        if m:
            return m.group(1)
    return name


def live_names(cen):
    rows = [(r["current"], r["type"]) for r in cen["rows"] if r["plane"] == "live"]
    rows += [(r["name"], r["type"]) for r in cen["not_judged"] if r["plane"] == "live"]
    return rows


def within(hand, got, approx):
    tol = max(IV7_TOLERANCE["floor"], hand * (IV7_TOLERANCE["approx"] if approx else IV7_TOLERANCE["exact"]))
    return abs(got - hand) <= tol, tol


def iv7(cen):
    live = live_names(cen)
    repo = [(r["current"], r["type"]) for r in cen["rows"] if r["plane"] == "repo"] + \
           [(r["name"], r["type"]) for r in cen["not_judged"] if r["plane"] == "repo"]
    first = [(tokens(resource_part(n, t))[0] if tokens(resource_part(n, t)) else "", n, t) for n, t in live]
    anyt = [(set(tokens(resource_part(n, t))), n, t) for n, t in live]

    def n_first(tok):
        return sum(1 for f, _, _ in first if f == tok)

    def n_any(tok):
        return sum(1 for s, _, _ in anyt if tok in s)

    surfaces = []

    def surface(rank, title, figs, note):
        # figs: list of (label, hand, approx, got)
        rows, ok = [], True
        for label, hand, approx, got in figs:
            good, tol = within(hand, got, approx)
            ok = ok and good
            rows.append({"figure": label, "hand": hand, "hand_is_approx": approx, "census_r8_live": got,
                         "tolerance": round(tol, 2), "within": good})
        surfaces.append({"rank": rank, "surface": title, "figures": rows, "note": note,
                         "result": "AGREE" if ok else "DISAGREE"})

    firm_first = sum(n_first(t) for t in ("bd", "49f", "49financial", "inf", "inflection", "cot", "cottonwood"))
    firm_first4 = sum(1 for f, _, t in first if t in ("LAMBDA", "IAM_ROLE", "EVENT_RULE", "LOG_GROUP")
                      and f in ("bd", "49f", "49financial", "inf", "inflection", "cot", "cottonwood"))
    firm_any = sum(1 for s, _, _ in anyt if s & {"bd", "49f", "inf", "cot"})
    surface(1, "Firm spelled bd/49f/inf/cot in ~330 resource names, firm-as-system in ~210", [
        ("names carrying bd/49f/inf/cot as a token", 330, True, firm_any),
        ("firm as FIRST token over LAMBDA/IAM_ROLE/EVENT_RULE/LOG_GROUP (hand's grain: census s.1(c) pos0 "
         "47+55+45+57=204)", 210, True, firm_first4),
        ("firm as FIRST token over every type (no hand figure at this grain; census s.3 first-token "
         "inf 136 + bd 119 + cot 30 = 285)", 285, False, firm_first),
        ("bd as FIRST token (hand's grain: census s.3 first-token 119)", 120, True, n_first("bd")),
        ("49f anywhere (hand's grain undeclared; census s.2 per-type sums are any-position)", 45, True, n_any("49f")),
        ("49financial anywhere (census s.1: 1 role, 1 policy, 1 table, 1 bucket)", 4, False, n_any("49financial")),
        ("inf as FIRST token (hand's grain: census s.3 first-token 136)", 140, True, n_first("inf")),
        ("inflection anywhere (census s.1: 1 role, 3 alarms)", 4, False, n_any("inflection")),
        ("cot as FIRST token (hand's grain: census s.3 first-token 30)", 30, True, n_first("cot")),
        ("cottonwood anywhere", 2, False, n_any("cottonwood"))],
        "census r8 live plane, judged + carded names; tokens split on - / _ . # : and camel humps; a LOG_GROUP "
        "tokenised on the resource part after /aws/{service}/ as the hand census did; each per-spelling figure "
        "read at the grain the hand census used for it")
    surface(2, "bd = vendor AND firm", [("names whose FIRST token is bd", 119, False, n_first("bd"))],
            "hand cites census s.3 exactly (119); brief ~120")
    # 3: the hand gives no count; the checkable claim is that BOTH grammars are present and grade() rules
    # source-first. Measured over the census's S3Key rows (repo plane: the live plane carries no S3Key rows).
    tiers = {"bronze", "silver", "gold", "platinum"}
    s3k = [r for r in cen["rows"] if r["type"] == "S3Key"]
    tier_first = [r for r in s3k if r["current"].split("/")[0] in tiers]
    tier_first_oop = [r for r in tier_first if r["verdict"] == "OUT-OF-PATTERN"]
    surface(3, "Key grammar split: source-first vs tier-first", [
        ("tier-first keys present in the census (hand: split exists, >=1)", 1, False, min(1, len(tier_first))),
        ("tier-first keys grade() rules OUT-OF-PATTERN, as a share of tier-first (hand: ruling is source-first => all)",
         len(tier_first), False, len(tier_first_oop))],
        "hand gives no key count; S3Key judged rows %d, tier-first %d, of which OUT-OF-PATTERN %d" %
        (len(s3k), len(tier_first), len(tier_first_oop)))
    pol = [n for n, t in live if t == "IAM_POLICY"]
    def camel(n):
        return bool(re.search(r"[A-Z]", n)) and "-" not in n and "/" not in n
    surface(4, "96 camel IAM policies incl. 6x CloudWatchLogs; 6 camel roles; 6 camel alarms", [
        ("camel IAM policies", 96, False, sum(1 for n in pol if camel(n))),
        ("customer-managed IAM policies", 502, False, len(pol)),
        ("CloudWatchLogs policies", 6, False, sum(1 for n in pol if n == "CloudWatchLogs")),
        ("camel IAM roles", 6, False, sum(1 for n, t in live if t == "IAM_ROLE" and camel(n))),
        ("CW alarms carrying capitals (hand's grain: census s.2 '6 Camel/Pascal-kebab', hyphens allowed)", 6, False,
         sum(1 for n, t in live if t == "CW_ALARM" and re.search(r"[A-Z]", n)))],
        "live plane; census r8 excludes 10 aws_fixed IAM_POLICY names and dedupes nothing (a repeated name counts each node)")
    repo_set = set(repo)
    lnd = [(n, t) for n, t in live if (n, t) not in repo_set]
    def by(typ):
        return sum(1 for n, t in lnd if t == typ)
    surface(5, "339 LIVE-no-DECLARED nodes (Lambda 15, role 16, rule 10, log 68, policy 36)", [
        ("live names with no same (name,type) on the census repo plane", 339, False, len(lnd)),
        ("LAMBDA", 15, False, by("LAMBDA")), ("IAM_ROLE", 16, False, by("IAM_ROLE")),
        ("EVENT_RULE", 10, False, by("EVENT_RULE")), ("LOG_GROUP", 68, False, by("LOG_GROUP")),
        ("IAM_POLICY", 36, False, by("IAM_POLICY"))],
        "DIFFERENT INSTRUMENT: the hand figure is comp-estate's drift_class; the census has no drift class, so this "
        "is live (name,type) minus repo (name,type), where the repo plane reads only literal Terraform name "
        "attributes and source literals")
    surface(6, "Project/workstream codes as systems (gldinc 7, quartz 5, cmtque 4, wsb 6, wsd 6)", [
        ("gldinc", 7, False, n_first("gldinc")), ("quartz", 5, False, n_first("quartz")),
        ("cmtque", 4, False, n_first("cmtque")), ("wsb", 6, False, n_first("wsb")), ("wsd", 6, False, n_first("wsd")),
        ("total", 28, False, sum(n_first(x) for x in ("gldinc", "quartz", "cmtque", "wsb", "wsd")))],
        "first token, live plane")
    opal = [(n, t) for f, n, t in first if f == "opal"]
    surface(7, "opal- as a null prefix (445 names, 18 types)", [
        ("names whose first token is opal", 445, False, len(opal)),
        ("types among them", 18, False, len(set(t for _, t in opal)))], "live plane")
    def pf(tok):
        return sum(1 for n in pol if tokens(n) and tokens(n)[0] == tok)
    surface(8, "Purpose-first IAM policy names (cross 39, s3 29, cloudwatch 23)", [
        ("cross-*", 39, False, pf("cross")), ("s3-*", 29, False, pf("s3")), ("cloudwatch-*", 23, False, pf("cloudwatch")),
        ("total", 91, False, pf("cross") + pf("s3") + pf("cloudwatch"))],
        "first token of live IAM_POLICY names; the 42% system-first share is not re-derived (no system reading here)")
    sec = [n for n, t in live if t == "SECRET"]
    surface(9, "Secrets: 10 of 96 off the slash-path grammar", [
        ("secrets", 96, False, len(sec)), ("secrets with no slash", 10, False, sum(1 for n in sec if "/" not in n))],
        "live plane")
    surfaces.append({"rank": 10, "surface": "Terraform LABELS and tags -- UNMEASURED", "figures": [],
                     "note": "The hand states this plane is unmeasured. The census r8 repo plane reads each "
                             "resource's literal NAME attribute (and records 132 expression names as not judged); "
                             "it reads no Terraform resource LABEL, module name or tag. So the census measures "
                             "this plane no more than the hand did: the claim compared is the unmeasured status, "
                             "and nothing in the census contradicts it.",
                     "result": "AGREE"})
    out = {"compared": len(surfaces), "agree": sum(1 for s in surfaces if s["result"] == "AGREE")}
    out["disagree"] = out["compared"] - out["agree"]
    out["per_surface"] = surfaces
    out["live_population"] = len(live)
    out["repo_population"] = len(repo)
    return out


def main(argv):
    wc = worked_cases()
    header, n6_lines, n6 = n6_rows()
    cen = census()
    cc = census_commit()
    head = git("rev-parse", "HEAD").decode().strip()
    mod_c, tmp_c = load_grade(cc)
    mod_h, tmp_h = load_grade(head)
    try:
        n2 = compare_names(wc["worked_cases"], mod_c, mod_h, cen)
        nn6 = compare_names(n6, mod_c, mod_h, cen)
        t = iv7(cen)
    finally:
        shutil.rmtree(tmp_c, ignore_errors=True)
        shutil.rmtree(tmp_h, ignore_errors=True)
    from collections import Counter
    res = {"census_commit": cc, "head": head, "census_vintage": cen["vintage"], "census_registry": cen["registry"],
           "worked_cases_count": len(wc["worked_cases"]),
           "worked_cases_by_verdict": dict(Counter(c["verdict"] for c in wc["worked_cases"])),
           "worked_cases_types": len(set(c["type"] for c in wc["worked_cases"])),
           "n6_lines": n6_lines, "n6_header": header, "n6_rows": len(n6),
           "iv7_json_rows": len(re.findall(r'\{"rank": \d+', io.open(TENSION, encoding="utf-8").read())),
           "N2": n2, "N6": nn6, "IV7": t}
    print("WORKED CASES: %d %s over %d types" % (res["worked_cases_count"], res["worked_cases_by_verdict"], res["worked_cases_types"]))
    print("N6 LINES %d  DATA ROWS %d" % (n6_lines, len(n6)))
    for k in ("N2", "N6", "IV7"):
        b = res[k]
        print("%s: compared %d agree %d disagree %d" % (k, b["compared"], b["agree"], b["disagree"]))
    print("VINTAGE DIFFS census-vs-HEAD: N2 %d  N6 %d" % (len(n2["vintage_diffs"]), len(nn6["vintage_diffs"])))
    if "--write" in argv:
        p = argv[argv.index("--write") + 1]
        with io.open(p, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(res, fh, indent=1, ensure_ascii=True)
            fh.write("\n")
        print("WROTE", p)


if __name__ == "__main__":
    main(sys.argv[1:])
