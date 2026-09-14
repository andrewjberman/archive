#!/usr/bin/env python3
"""check_ln.py -- the mechanical criteria of LGIC_NAMING round 1 (decomposition v3), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the L6 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line
`VERDICT: PASS-<X>` or `VERDICT: FAIL-<X>`, and exits 0. A missing input file is a FAIL verdict, never a traceback.
A PASS string is never a substring of its FAIL string, because proof-of-spec-check greps <expect> unanchored.
"""
import fnmatch
import json
import math
import os
import re
import subprocess
import sys

BASE = "org/missions/D14/LGIC/LGIC_NAMING"
DEL = BASE + "/deliverables"
EX = DEL + "/exercises"
FIX = DEL + "/2.0.0_SA_COO~G/fixed_inputs"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
TF = "infra/aws/terraform/shared-infra/s3-49financial.tf"
VERDICTS = ("CONFORMANT", "ALIAS", "OUT-OF-PATTERN", "RAISE", "NOT-GRADED")
RESIDUE = ("camel-iam", "purpose-first-policy", "library-first-layer", "default-sg", "workstream-schedule")
FORMS = ("entity-partition", "legacy-served", "code-tier", "legacy-root-code")
FIRMS = ("49financial", "inflection", "cottonwood", "demo")
ALIAS_TOKENS = ("bd", "49f", "49financial", "inf", "inflection", "cot", "cottonwood", "demo")


def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)


def read(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def load_json(path):
    t = read(path)
    if t is None:
        return None
    try:
        return json.loads(t)
    except ValueError:
        return None


def fenced_json(path):
    """The first ```json fenced block of a markdown file, parsed; None when absent or unparseable."""
    t = read(path)
    if t is None:
        return None
    m = re.search(r"```json\s*\n(.*?)\n```", t, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def tsv(path):
    """(base_sha, rows) of a TSV answer file: '# base <sha>' header, then tab-separated rows; None when absent."""
    t = read(path)
    if t is None:
        return None, None
    base, rows = None, []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):
            m = re.match(r"#\s*base\s+([0-9a-f]{7,40})", s)
            if m:
                base = m.group(1)
            continue
        rows.append([c.strip() for c in ln.split("\t")])
    return base, rows


def graded_types():
    d = load_json(SCHEMA) or {}
    kind = list((d.get("kind") or {}).get("by_type", {}).keys())
    other = [k for k, v in (d.get("types_not_graded_by_kind") or {}).items() if not str(v).startswith("NOT GRADED")]
    return sorted(set(kind + other))


def cases():
    d = fenced_json(DEL + "/GRADING_RULE.md")
    if not isinstance(d, dict):
        return None
    wc = d.get("worked_cases")
    return wc if isinstance(wc, list) else None


def sample():
    d = load_json(FIX + "/N6_SAMPLE.json") or {}
    return d.get("discriminating", []), d.get("overlap", [])


def git_has(sha, path):
    if not sha:
        return None
    r = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (sha, path)], capture_output=True)
    return r.returncode == 0


def sha_ok(sha):
    if not sha:
        return False
    r = subprocess.run(["git", "cat-file", "-e", sha + "^{commit}"], capture_output=True)
    return r.returncode == 0


def list_regexes():
    d = load_json(DEL + "/LEGACY_SERVED_PATHS.json") or {}
    out = []
    for p in d.get("paths") or []:
        s = p if isinstance(p, str) else (p.get("path") if isinstance(p, dict) else None)
        if s:
            out.append((s, re.compile("^" + re.sub(r"\\\{[^/]*?\\\}", "[^/]+", re.escape(s)) + "$")))
    return out


def on_list(name, regs):
    return any(r.match(name) for _, r in regs)


# ---------------------------------------------------------------- LN-g-1
def g1_wellformed():
    wc = cases()
    if wc is None:
        return say("FAIL-NO-WORKED-CASES", "GRADING_RULE.md carries no parseable ```json block with worked_cases")
    bad = [c for c in wc if not isinstance(c, dict) or not c.get("name") or not c.get("type")
           or c.get("verdict") not in VERDICTS
           or (c.get("verdict") in ("ALIAS", "OUT-OF-PATTERN") and not c.get("canonical_form"))]
    say("PASS-WELL-FORMED" if wc and not bad else "FAIL-MALFORMED",
        "WORKED-CASES: %d  MALFORMED: %d" % (len(wc), len(bad)))


def g1_types():
    wc = cases() or []
    need = graded_types()
    have = set(c.get("type") for c in wc if isinstance(c, dict))
    miss = [t for t in need if t not in have]
    say("PASS-ALL-25-TYPES" if len(need) == 25 and not miss else "FAIL-TYPES-MISSING",
        "GRADED TYPES (from %s): %d  COVERED: %d  MISSING: %s" % (SCHEMA, len(need), len(need) - len(miss), miss))


def g1_verdicts():
    have = set(c.get("verdict") for c in (cases() or []) if isinstance(c, dict))
    miss = [v for v in VERDICTS[:3] if v not in have]
    say("PASS-ALL-3-VERDICTS" if not miss else "FAIL-VERDICTS-MISSING", "MISSING: %s" % miss)


def g1_residue():
    have = set(c.get("residue_class") for c in (cases() or []) if isinstance(c, dict))
    miss = [r for r in RESIDUE if r not in have]
    say("PASS-ALL-5-RESIDUE" if not miss else "FAIL-RESIDUE-MISSING", "RESIDUE CLASSES 5  MISSING: %s" % miss)


def g1_live():
    live = (load_json(FIX + "/LIVE_NAMES.json") or {}).get("by_type", {})
    wc = [c for c in (cases() or []) if isinstance(c, dict) and not c.get("specimen")]
    off = [(c.get("type"), c.get("name")) for c in wc if c.get("name") not in set(live.get(c.get("type"), []))]
    spec = [c for c in (cases() or []) if isinstance(c, dict) and c.get("specimen")]
    say("PASS-ALL-LIVE" if wc and not off else "FAIL-NOT-LIVE",
        "NON-SPECIMEN CASES: %d  NOT IN LIVE_NAMES: %d %s  SPECIMENS: %d" % (len(wc), len(off), off[:5], len(spec)))


def g1_disjoint():
    disc, _ = sample()
    dn = set(x["name"] for x in disc)
    hit = [c.get("name") for c in (cases() or []) if isinstance(c, dict) and c.get("name") in dn]
    say("PASS-DISJOINT" if cases() and not hit else "FAIL-OVERLAPS-SAMPLE",
        "DISCRIMINATING SAMPLE: %d  WORKED CASES IN IT: %d %s" % (len(dn), len(hit), hit[:5]))


def g1_forms():
    have = set(c.get("form") for c in (cases() or []) if isinstance(c, dict))
    miss = [f for f in FORMS if f not in have]
    say("PASS-ALL-4-FORMS" if not miss else "FAIL-FORMS-MISSING", "V1.3 KEY FORMS 4  MISSING: %s" % miss)


def g1_legacyroot():
    lr = [c for c in (cases() or []) if isinstance(c, dict) and c.get("form") == "legacy-root-code"]
    bad = [c for c in lr if c.get("verdict") != "OUT-OF-PATTERN" or "/code/" not in str(c.get("canonical_form", ""))]
    say("PASS-RULED-VERDICT" if lr and not bad else "FAIL-UNRULED-VERDICT",
        "LEGACY-ROOT-CODE CASES: %d  NOT OUT-OF-PATTERN WITH A /code/ CANONICAL: %d" % (len(lr), len(bad)))


def g1_list():
    d = load_json(DEL + "/LEGACY_SERVED_PATHS.json")
    if not isinstance(d, dict):
        return say("FAIL-NO-LIST", "LEGACY_SERVED_PATHS.json absent or not a JSON object")
    paths = d.get("paths") or []
    den = d.get("denominator")
    ok = bool(d.get("portal_vintage")) and paths and den == len(paths)
    say("PASS-LISTED" if ok else "FAIL-UNLISTED",
        "PORTAL VINTAGE: %s  PATHS: %d  DENOMINATOR: %s" % (d.get("portal_vintage"), len(paths), den))


def g1_pair():
    regs = list_regexes()
    wc = [c for c in (cases() or []) if isinstance(c, dict)]
    on = [c for c in wc if c.get("pair") == "on-list"]
    off = [c for c in wc if c.get("pair") == "off-list"]
    on_ok = [c for c in on if c.get("verdict") == "CONFORMANT" and on_list(c.get("name", ""), regs)]
    off_ok = [c for c in off if c.get("verdict") == "OUT-OF-PATTERN" and not on_list(c.get("name", ""), regs)]
    say("PASS-DISCRIMINATES" if regs and on and off and len(on_ok) == len(on) and len(off_ok) == len(off)
        else "FAIL-NO-DISCRIMINATION",
        "LIST ENTRIES: %d  ON-LIST CASES: %d (CONFORMANT and listed: %d)  OFF-LIST CASES: %d (OUT-OF-PATTERN and unlisted: %d)"
        % (len(regs), len(on), len(on_ok), len(off), len(off_ok)))


def g1_cites():
    t = read(DEL + "/GRADING_RULE.md") or ""
    entries = [s for s, _ in list_regexes()]
    copied = [s for s in entries if s in t]
    ok = "LEGACY_SERVED_PATHS.json" in t and len(copied) <= 3
    say("PASS-CITES-NO-COPY" if ok else "FAIL-COPIES-OR-UNCITED",
        "CITES THE FILE: %s  LIST ENTRIES REPEATED IN THE RULE: %d of %d (at most 3 allowed, for the pair)"
        % ("LEGACY_SERVED_PATHS.json" in t, len(copied), len(entries)))


# ---------------------------------------------------------------- LN-e-1 .. LN-e-5
def items():
    d = load_json(FIX + "/N3_ITEMS.json") or {}
    k = load_json(FIX + "/N3_KEY.json") or {}
    return d.get("items", []), k.get("key", {})


def namer_named(which):
    its, _ = items()
    _, rows = tsv(EX + "/n3-namer-%s.tsv" % which)
    got = {r[0]: r[1] for r in (rows or []) if len(r) >= 2 and r[1]}
    miss = [i["id"] for i in its if i["id"] not in got]
    say("PASS-ALL-NAMED" if its and rows is not None and not miss else "FAIL-UNNAMED",
        "ITEMS: %d  NAMED: %d  MISSING: %s" % (len(its), len(its) - len(miss), miss))


def namer_base(which):
    base, rows = tsv(EX + "/n3-namer-%s.tsv" % which)
    say("PASS-BASE-RECORDED" if rows is not None and sha_ok(base) else "FAIL-NO-BASE", "BASE: %s" % base)


def e3_identical():
    its, _ = items()
    _, a = tsv(EX + "/n3-namer-a.tsv")
    _, b = tsv(EX + "/n3-namer-b.tsv")
    if a is None or b is None:
        return say("FAIL-ANSWERS-ABSENT", "namer A file: %s  namer B file: %s" % (a is not None, b is not None))
    ma = {r[0]: r[1] for r in a if len(r) >= 2}
    mb = {r[0]: r[1] for r in b if len(r) >= 2}
    diff = [(i["id"], ma.get(i["id"]), mb.get(i["id"])) for i in its if ma.get(i["id"]) != mb.get(i["id"])]
    for d in diff:
        print("DIFFERS: %s  A=%s  B=%s" % d)
    say("PASS-IDENTICAL" if its and not diff else "FAIL-DIFFERENT",
        "ITEMS: %d  IDENTICAL: %d  DIFFERENT: %d" % (len(its), len(its) - len(diff), len(diff)))


def blind(fa, fb):
    ba, _ = tsv(fa)
    bb, _ = tsv(fb)
    a_saw_b = git_has(ba, fb)
    b_saw_a = git_has(bb, fa)
    ok = sha_ok(ba) and sha_ok(bb) and a_saw_b is False and b_saw_a is False
    say("PASS-BLIND" if ok else "FAIL-NOT-BLIND",
        "BASE A: %s (holds B's file: %s)  BASE B: %s (holds A's file: %s)" % (ba, a_saw_b, bb, b_saw_a))


def e4_marked():
    _, a = tsv(EX + "/n3-namer-a.tsv")
    _, r = tsv(EX + "/n3-reader.tsv")
    names = [x[1] for x in (a or []) if len(x) >= 2]
    marks = {x[0]: x[1] for x in (r or []) if len(x) >= 2 and x[1]}
    miss = [n for n in names if n not in marks]
    say("PASS-ALL-MARKED" if names and r is not None and not miss else "FAIL-UNMARKED",
        "NAMES: %d  MARKED: %d  MISSING: %d" % (len(names), len(names) - len(miss), len(miss)))


def e5_correct():
    its, key = items()
    _, a = tsv(EX + "/n3-namer-a.tsv")
    _, r = tsv(EX + "/n3-reader.tsv")
    name_of = {x[0]: x[1] for x in (a or []) if len(x) >= 2}
    mark = {x[0]: x[1] for x in (r or []) if len(x) >= 2}
    wrong = []
    for i in its:
        n = name_of.get(i["id"])
        exp = key.get(i["id"])
        if mark.get(n) != exp:
            wrong.append((i["id"], n, mark.get(n), exp))
    for w in wrong:
        print("WRONG: %s  name=%s  marked=%s  expected=%s" % w)
    say("PASS-ALL-CORRECT" if its and a and r and not wrong else "FAIL-MISREAD",
        "ITEMS: %d  CORRECT: %d  WRONG: %d" % (len(its), len(its) - len(wrong), len(wrong)))


def e5_consistent():
    _, r = tsv(EX + "/n3-reader.tsv")
    rows = [x for x in (r or []) if len(x) >= 2]
    marked = set(x[1] for x in rows if x[1] != "none")
    clash = []
    for name, m in ((x[0], x[1]) for x in rows):
        toks = set(re.split(r"[-/=.]", name))
        for t in marked:
            if t in toks and m != t:
                clash.append((name, t, m))
    say("PASS-CONSISTENT" if rows and not clash else "FAIL-TWO-REFERENTS",
        "NAMES: %d  TOKENS MARKED AS A FIRM OR PRODUCT: %d  A MARKED TOKEN READ OTHERWISE ELSEWHERE: %d %s"
        % (len(rows), len(marked), len(clash), clash[:5]))


# ---------------------------------------------------------------- LN-f-1
def f1_data():
    return fenced_json(EX + "/n4-firm-patterns.md")


def f1_one():
    d = f1_data()
    pats = (d or {}).get("patterns") if isinstance(d, dict) else None
    ok = isinstance(pats, dict) and sorted(pats) == sorted(FIRMS) and all(isinstance(v, str) and v for v in pats.values())
    say("PASS-ONE-EACH" if ok else "FAIL-NOT-ONE-EACH", "PATTERNS: %s" % (pats,))


def f1_attributed():
    d = f1_data() or {}
    return d.get("patterns") or {}, d.get("attributed") or {}, d.get("excluded") or []


def f1_catch():
    pats, att, _ = f1_attributed()
    total, missed = 0, []
    for f in FIRMS:
        for a in att.get(f, []):
            total += 1
            if not fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, "")):
                missed.append((f, a.get("canonical")))
    say("PASS-CATCHES-ALL" if pats and total and not missed else "FAIL-MISSES",
        "ATTRIBUTED CANONICAL FORMS: %d  CAUGHT BY OWN FIRM'S PATTERN: %d  MISSED: %s" % (total, total - len(missed), missed[:5]))


def f1_cross():
    pats, att, _ = f1_attributed()
    cross = []
    for f in FIRMS:
        for g in FIRMS:
            if g == f:
                continue
            for a in att.get(g, []):
                if fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, "")):
                    cross.append((f, g, a.get("canonical")))
    say("PASS-NO-CROSS" if pats and att and not cross else "FAIL-CROSSES",
        "CROSS-FIRM CATCHES: %d %s" % (len(cross), cross[:5]))


def f1_covered():
    _, att, exc = f1_attributed()
    live = (load_json(FIX + "/LIVE_NAMES.json") or {}).get("by_type", {}).get("IAM_ROLE", [])
    want = [n for n in live if set(re.split(r"[-_]", n.lower())) & set(ALIAS_TOKENS)]
    seen = set(a.get("name") for f in FIRMS for a in att.get(f, []))
    seen |= set(e.get("name") for e in exc if e.get("reason"))
    miss = [n for n in want if n not in seen]
    say("PASS-COVERED" if want and not miss else "FAIL-UNCOVERED",
        "LIVE IAM_ROLE NAMES CARRYING A FIRM ALIAS TOKEN: %d of %d roles  ATTRIBUTED OR EXCLUDED WITH A REASON: %d  MISSING: %s"
        % (len(want), len(live), len(want) - len(miss), miss[:5]))


# ---------------------------------------------------------------- LN-l-1 .. LN-l-3
def l1_notice():
    t = read(TF) or ""
    head = "\n".join(t.splitlines()[:40])
    ok = "replaced" in head.lower() and "LGIC_NAMING_PRD" in head
    say("PASS-NOTICE" if ok else "FAIL-NO-NOTICE", "FIRST 40 LINES CARRY 'replaced': %s  CITE LGIC_NAMING_PRD: %s"
        % ("replaced" in head.lower(), "LGIC_NAMING_PRD" in head))


def l1_comment():
    mb = subprocess.run(["git", "merge-base", "HEAD", "CLOUD"], capture_output=True, text=True).stdout.strip()
    d = subprocess.run(["git", "diff", "-U0", mb, "HEAD", "--", TF], capture_output=True, text=True).stdout
    changed = [ln for ln in d.splitlines() if ln[:1] in "+-" and not ln.startswith(("+++", "---"))]
    code = [ln for ln in changed if not ln[1:].lstrip().startswith("#") and ln[1:].strip()]
    say("PASS-COMMENT-ONLY" if changed and not code else "FAIL-NOT-COMMENT-ONLY",
        "BASE: %s  CHANGED LINES: %d  NON-COMMENT CHANGED LINES: %d %s" % (mb[:10], len(changed), len(code), code[:3]))


def addresses():
    d = load_json(FIX + "/N5_ADDRESSES.json") or {}
    return d.get("addresses", [])


def l2_labeled():
    ads = addresses()
    _, r = tsv(EX + "/n5-reader.tsv")
    got = {x[0]: x[1] for x in (r or []) if len(x) >= 2 and x[1]}
    miss = [a["id"] for a in ads if a["id"] not in got]
    say("PASS-ALL-LABELED" if ads and r is not None and not miss else "FAIL-UNLABELED",
        "ADDRESSES: %d  LABELED: %d  MISSING: %s" % (len(ads), len(ads) - len(miss), miss))


def l3_key():
    return (load_json(FIX + "/N5_KEY.json") or {}).get("key", {})


def l3_correct():
    key = l3_key()
    _, r = tsv(EX + "/n5-reader.tsv")
    got = {x[0]: x[1].replace(" ", "") for x in (r or []) if len(x) >= 2}
    wrong = [(k, got.get(k), v) for k, v in key.items() if v != "DOES-NOT-FIT" and got.get(k) != v]
    for w in wrong:
        print("WRONG: %s  labeled=%s  expected=%s" % w)
    n = len([v for v in key.values() if v != "DOES-NOT-FIT"])
    say("PASS-ALL-CORRECT" if key and r is not None and not wrong else "FAIL-MISREAD",
        "CONFORMING ADDRESSES: %d  CORRECT: %d  WRONG: %d" % (n, n - len(wrong), len(wrong)))


def l3_control():
    key = l3_key()
    _, r = tsv(EX + "/n5-reader.tsv")
    got = {x[0]: x[1].strip() for x in (r or []) if len(x) >= 2}
    ctl = [k for k, v in key.items() if v == "DOES-NOT-FIT"]
    ok = ctl and all(got.get(k) == "DOES-NOT-FIT" for k in ctl)
    say("PASS-CONTROL-FLAGGED" if ok else "FAIL-CONTROL-MISSED",
        "NEGATIVE CONTROLS: %d  MARKED DOES-NOT-FIT: %d" % (len(ctl), sum(1 for k in ctl if got.get(k) == "DOES-NOT-FIT")))


# ---------------------------------------------------------------- LN-h-1 .. LN-h-3
def grader_graded(which):
    disc, ov = sample()
    _, rows = tsv(EX + "/n6-grader-%s.tsv" % which)
    got = {(x[0], x[1]): x[2] for x in (rows or []) if len(x) >= 3}
    want = [(s["type"], s["name"]) for s in disc + ov]
    miss = [w for w in want if got.get(w) not in VERDICTS]
    say("PASS-ALL-GRADED" if want and rows is not None and not miss else "FAIL-UNGRADED",
        "SAMPLE: %d (%d discriminating + %d overlap)  GRADED WITH A VERDICT: %d  MISSING: %s"
        % (len(want), len(disc), len(ov), len(want) - len(miss), miss[:5]))


def grader_base(which):
    base, rows = tsv(EX + "/n6-grader-%s.tsv" % which)
    say("PASS-BASE-RECORDED" if rows is not None and sha_ok(base) else "FAIL-NO-BASE", "BASE: %s" % base)


def h3_agree():
    disc, _ = sample()
    _, a = tsv(EX + "/n6-grader-a.tsv")
    _, b = tsv(EX + "/n6-grader-b.tsv")
    if a is None or b is None:
        return say("FAIL-GRADINGS-ABSENT", "grader A file: %s  grader B file: %s" % (a is not None, b is not None))
    ga = {(x[0], x[1]): (x[2], x[3] if len(x) > 3 else "") for x in a if len(x) >= 3}
    gb = {(x[0], x[1]): (x[2], x[3] if len(x) > 3 else "") for x in b if len(x) >= 3}
    dis = [(s["type"], s["name"], ga.get((s["type"], s["name"])), gb.get((s["type"], s["name"]))) for s in disc
           if ga.get((s["type"], s["name"])) != gb.get((s["type"], s["name"]))]
    for d in dis:
        print("DISAGREE: %s %s  A=%s  B=%s" % d)
    say("PASS-AGREE" if disc and not dis else "FAIL-DISAGREE",
        "DISCRIMINATING NAMES: %d  AGREE ON VERDICT AND CANONICAL FORM: %d  DISAGREE: %d" % (len(disc), len(disc) - len(dis), len(dis)))


def h3_disjoint():
    return g1_disjoint()


# ---------------------------------------------------------------- LN-t-1
def t1_ten():
    d = fenced_json(DEL + "/TENSION_RANKING.md")
    rows = (d or {}).get("rows") if isinstance(d, dict) else None
    ranks = [r.get("rank") for r in (rows or []) if isinstance(r, dict)]
    empty = [r.get("rank") for r in (rows or []) if isinstance(r, dict) and (not r.get("surface") or not r.get("cost"))]
    ok = ranks == list(range(1, 11)) and not empty
    say("PASS-TEN-COSTED" if ok else "FAIL-NOT-TEN-COSTED", "ROWS: %d  RANKS: %s  WITHOUT SURFACE OR COST: %s" % (len(ranks), ranks, empty))


CHECKS = {
    "g1-wellformed": g1_wellformed, "g1-types": g1_types, "g1-verdicts": g1_verdicts, "g1-residue": g1_residue,
    "g1-live": g1_live, "g1-disjoint": g1_disjoint, "g1-forms": g1_forms, "g1-legacyroot": g1_legacyroot,
    "g1-list": g1_list, "g1-pair": g1_pair, "g1-cites": g1_cites,
    "e1-named": lambda: namer_named("a"), "e1-base": lambda: namer_base("a"),
    "e2-named": lambda: namer_named("b"), "e2-base": lambda: namer_base("b"),
    "e3-identical": e3_identical, "e3-blind": lambda: blind(EX + "/n3-namer-a.tsv", EX + "/n3-namer-b.tsv"),
    "e4-marked": e4_marked, "e5-correct": e5_correct, "e5-consistent": e5_consistent,
    "f1-one": f1_one, "f1-catch": f1_catch, "f1-cross": f1_cross, "f1-covered": f1_covered,
    "l1-notice": l1_notice, "l1-comment": l1_comment,
    "l2-labeled": l2_labeled, "l3-correct": l3_correct, "l3-control": l3_control,
    "h1-graded": lambda: grader_graded("a"), "h1-base": lambda: grader_base("a"),
    "h2-graded": lambda: grader_graded("b"), "h2-base": lambda: grader_base("b"),
    "h3-agree": h3_agree, "h3-disjoint": h3_disjoint,
    "h3-blind": lambda: blind(EX + "/n6-grader-a.tsv", EX + "/n6-grader-b.tsv"),
    "t1-ten": t1_ten,
}


def main(argv):
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: check_ln.py <%s>" % "|".join(sorted(CHECKS)))
        print("VERDICT: FAIL-USAGE")
        return 0
    if not os.path.isdir("org") or not os.path.isdir(".tools"):
        print("run from the worktree root (org/ and .tools/ not found in %s)" % os.getcwd())
        print("VERDICT: FAIL-WRONG-ROOT")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    math.ceil(0)
    sys.exit(main(sys.argv))
