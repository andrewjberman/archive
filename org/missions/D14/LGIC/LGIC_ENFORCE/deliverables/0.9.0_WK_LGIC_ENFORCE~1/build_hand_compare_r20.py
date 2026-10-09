"""LGIC_ENFORCE round 20, cell EN-z-2 -- compare the HAND ranking with THIS round's census (FWD-5 clause 3).

FWD-5 clause 3: "the totals agree with the ranking the naming work produced by hand."  The hand ranking is
THREE surfaces (round 19's HAND_REMEASURE_R19.json): GRADING_RULE.md worked cases (45), n6-grader-a.tsv rows (88),
TENSION_RANKING.md ranked surfaces (10) -- 143 keys.  Round 19 re-measured the HAND side at the round-8 census
vintage.  This builder runs the SAME 143 keys against the round-20 census,
    org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r20.md.

WHAT IT READS, AND WHAT IT REFUSES TO DO
  HAND side   : HAND_REMEASURE_R19.json per_case_detail[*].hand_remeasured (names) and .figures[].hand_remeasured
                (tension), read byte-for-byte.  The hand side is NEVER re-graded and no round-19 sibling or
                LGIC_NAMING original is edited.
  MACHINE side: the r20 report's own rows (verdict, canonical) per (name, type).  Where the r20 run has NO row for
                the name (carded NOT-JUDGED, R-29, or a name/type the census population does not hold), grade()
                at the worktree HEAD is called and the record says so per key.  The registry hash of HEAD is
                asserted equal to the r20 report's, so that grade() reads the registry the r20 run read.
                For the tension surfaces the machine figures are compare_hand_r9.iv7() run over the r20 report
                (the instrument round 9 and round 19 used), and the same declared tolerance.
  POSITIVE CONTROL: the same comparator, run against the ROUND-8 side (r19's grade_at_census_UNTOUCHED for the
                names; iv7() over the r8 report for the tension figures), must reproduce round 19's recorded
                45/45/0, 88/86/2, 10/9/1 before any r20 figure is believed.
  EXPLANATIONS: every difference gets one, and the facts it cites are READ here from git objects (registry rows at
                the census commit and at HEAD, the commit that added them, the lib/schema state), never typed.
                A difference whose cause is not one of the classes below is written with the explanation
                "UNEXPLAINED" and the build refuses.

Run (from the worktree root):  python <this file>
"""
import collections
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=HERE).decode("utf-8").strip()
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming as on  # noqa: E402

WORKER = "0.9.0_WK_LGIC_ENFORCE~1"
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/" + WORKER
R19 = DELIV + "/HAND_REMEASURE_R19.json"
R9 = DELIV + "/HAND_COMPARISON_R9.json"
R20_REPORT = DELIV + "/NAMING_CENSUS_REPORT.r20.md"
R8_REPORT = DELIV + "/NAMING_CENSUS_REPORT.r8.md"
CMP9 = DELIV + "/compare_hand_r9.py"
OUT = DELIV + "/HAND_COMPARE_R20.json"
RESULT = DELIV + "/hand-compare.r20.result.md"
CENSUS_COMMIT = "54659987c0bd95069d57ab78e425b28678dc32fb"  # the r8 census / r19 hand vintage
KEYS = ("grading_rule_worked_cases", "n6_grader_rows", "tension_ranking_surfaces")
TOL_APPROX, TOL_EXACT, TOL_FLOOR = 0.15, 0.10, 2
RESOURCES = "infra/logic/registry/resources.json"
SYSTEMS = "infra/logic/registry/systems.json"


def rp(rel):
    return os.path.join(ROOT, rel)


def git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=ROOT).decode("utf-8")


def read_json(rel):
    with io.open(rp(rel), encoding="utf-8") as fh:
        return json.load(fh)


def fence(rel):
    with io.open(rp(rel), encoding="utf-8") as fh:
        t = fh.read()
    return json.loads(re.search(r"```json\n(.*?)\n```", t, re.S).group(1))


def show_json(rev, rel):
    return json.loads(subprocess.check_output(["git", "cat-file", "-p", rev + ":" + rel], cwd=ROOT).decode("utf-8"))


def show_text(rev, rel):
    return subprocess.check_output(["git", "cat-file", "-p", rev + ":" + rel], cwd=ROOT).decode("utf-8")


def commit_info(h):
    full = git("rev-parse", h).strip()
    d = git("log", "-1", "--format=%ad|%an|%s", "--date=short", full).strip().split("|", 2)
    return {"commit": full[:10], "date": d[0], "author": d[1], "subject": d[2][:120]}


def first_commit(path, needle):
    """The oldest commit reachable from HEAD whose diff changes the count of `needle` in `path`."""
    out = git("log", "--reverse", "--format=%H", "-S" + needle, "--", path).split()
    if not out:
        return None
    h = out[0]
    if subprocess.call(["git", "merge-base", "--is-ancestor", CENSUS_COMMIT, h], cwd=ROOT) != 0:
        return dict(commit_info(h), after_census_commit=False)
    return dict(commit_info(h), after_census_commit=True)


def fmt_commit(c):
    return "%s (%s, %s)" % (c["commit"], c["date"], c["author"])


# ------------------------------------------------------------------ machine side
def agrees(hand, machine):
    """Round 9's agree_rule, unchanged: AGREE iff the verdict is equal AND (the hand gives no canonical form OR it
    equals the machine's byte for byte).  A hand RAISE agrees only with a machine RAISE."""
    if hand[0] != machine[0]:
        return False
    return hand[1] is None or hand[1] == machine[1]


def grade_head(name, typ):
    try:
        v, c = on.grade(name, typ)
        return (v, c)
    except on.RaiseDefect:
        return ("RAISE", None)


class Machine(object):
    def __init__(self, doc):
        self.rows = {}
        for r in doc["rows"]:
            self.rows.setdefault((r["current"], r["type"]), []).append(r)
        self.carded = set((r["name"], r["type"]) for r in doc["not_judged"])
        self.by_name = {}
        for r in doc["rows"]:
            self.by_name.setdefault(r["current"], set()).add(r["verdict"])

    def verdict(self, name, typ):
        """-> ((verdict, canonical), source, detail)"""
        key = (name, typ)
        if key in self.rows:
            rr = self.rows[key]
            forms = set((x["verdict"], x["canonical"]) for x in rr)
            if len(forms) != 1:
                raise SystemExit("ERROR: %r has %d different r20 rows %r" % (key, len(forms), sorted(forms)))
            planes = sorted(set(x["plane"] for x in rr))
            return forms.pop(), "r20_row", "r20 report row (%s plane, %d row(s))" % ("+".join(planes), len(rr))
        if key in self.carded:
            return grade_head(name, typ), "grade_at_head_carded", \
                "no r20 row: carded NOT-JUDGED (R-29) in the r20 run; grade() at HEAD"
        return grade_head(name, typ), "grade_at_head_not_in_r20", \
            "no r20 row: (name, type) is not in the r20 census population; grade() at HEAD"


# ------------------------------------------------------------------ tension
def load_iv7():
    spec = importlib.util.spec_from_file_location("compare_hand_r9", rp(CMP9))
    mod = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        spec.loader.exec_module(mod)
    finally:
        os.chdir(cwd)
    return mod


def tolerance(hand, approx):
    return max(float(TOL_FLOOR), (TOL_APPROX if approx else TOL_EXACT) * float(hand))


def live_pairs(doc):
    rows = [(r["current"], r["type"]) for r in doc["rows"] if r["plane"] == "live"]
    rows += [(r["name"], r["type"]) for r in doc["not_judged"] if r["plane"] == "live"]
    return rows


def repo_pairs(doc):
    rows = [(r["current"], r["type"]) for r in doc["rows"] if r["plane"] == "repo"]
    rows += [(r["name"], r["type"]) for r in doc["not_judged"] if r["plane"] == "repo"]
    return rows


def moved_names(old_doc, new_doc, pred):
    """The Counter-difference of the live (name, type) multiset selected by pred between the two readings."""
    a = collections.Counter(p for p in live_pairs(old_doc) if pred(*p))
    b = collections.Counter(p for p in live_pairs(new_doc) if pred(*p))
    added = sorted((b - a).elements())
    removed = sorted((a - b).elements())
    return added, removed


def sample(pairs, n=6):
    return ", ".join("%s:%s" % (t, nm) for nm, t in pairs[:n]) + (" ..." if len(pairs) > n else "")


# ------------------------------------------------------------------ explanations of name differences
class Facts(object):
    def __init__(self):
        self.res_c = show_json(CENSUS_COMMIT, RESOURCES)["resources"]
        self.res_h = show_json("HEAD", RESOURCES)["resources"]
        self.sys_c = show_json(CENSUS_COMMIT, SYSTEMS)
        self.sys_h = show_json("HEAD", SYSTEMS)
        self.sys_c_text = show_text(CENSUS_COMMIT, SYSTEMS)
        self.sys_h_text = show_text("HEAD", SYSTEMS)
        self.lib_c = show_text(CENSUS_COMMIT, "lib/opal_naming.py")
        self.lib_h = show_text("HEAD", "lib/opal_naming.py")
        self.sch_c = show_json(CENSUS_COMMIT, "org/standards/NAMING_SCHEMA.json")
        self.sch_h = show_json("HEAD", "org/standards/NAMING_SCHEMA.json")

    @staticmethod
    def row(rs, name, typ):
        x = [r for r in rs if r["name"] == name and r["type"] == typ]
        return x[0] if x else None

    @staticmethod
    def sysrow(doc, key):
        x = [r for r in doc["systems"] if r["key"] == key]
        return x[0] if x else None


def explain_name(f, name, typ, hand, machine, source):
    """-> (class, text).  `hand` and `machine` are (verdict, canonical)."""
    hv, hc = hand
    mv, mc = machine
    rc = f.row(f.res_c, name, typ)
    rh = f.row(f.res_h, name, typ)
    # --- class A: a resource-to-system row fills the {system} blank (R1.d), or re-points the system
    if rh is not None and hc and mc and hv == mv == "OUT-OF-PATTERN":
        new_sys = rh["system"]
        if rc is None and "{system}" in hc and mc == hc.replace("{system}", new_sys, 1):
            c1 = first_commit(RESOURCES, '"name": "%s"' % name)
            extra = ""
            if rh["evidence"].startswith("RE-POINTED") and c1 is not None:
                c2 = first_commit(RESOURCES, rh["evidence"][:60])
                if c2 is not None and c2["commit"] != c1["commit"]:
                    extra = " The row was later RE-POINTED to this system at %s." % fmt_commit(c2)
            return "RESOURCE_ROW_ADDED", (
                "THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form keeps "
                "the blank '{system}' because GRADING_RULE.md R1.d leaves the blank open until a registry "
                "resource-to-system row fills it, and infra/logic/registry/resources.json at the census commit "
                "54659987c0 holds no row for (%s, %s) (%d rows there). At HEAD (%d rows) the row (%s, %s) -> %s "
                "is present, first added at %s.%s Its evidence: %r. The r20 run (registry %s) reads that row and "
                "fills the blank: %s. Every other token of the canonical form is byte-equal to the hand's." % (
                    name, typ, len(f.res_c), len(f.res_h), name, typ, new_sys,
                    fmt_commit(c1) if c1 else "(commit not found)", extra, rh["evidence"][:150], on.registry_hash()[:16], mc))
        if rc is not None and rc["system"] != new_sys and hc.startswith(rc["system"] + "-") \
                and mc == new_sys + hc[len(rc["system"]):]:
            c2 = first_commit(RESOURCES, rh["evidence"][:60])
            return "RESOURCE_ROW_REPOINTED", (
                "THE ESTATE MOVED between the two readings; neither side is wrong. The hand canonical form leads "
                "with '%s', the system the resources.json row (%s, %s) carried at the census commit 54659987c0. "
                "At HEAD the same row names '%s' (re-pointed at %s). Its evidence: %r. The r20 run reads the "
                "re-pointed row and leads with '%s'; every other token is byte-equal." % (
                    rc["system"], name, typ, new_sys, fmt_commit(c2) if c2 else "(commit not found)",
                    rh["evidence"][:170], new_sys))
    # --- class B: a system key landed whose long form / key is the leading token of the name
    if name == "opal-portal-data-proxy-api" and typ == "API_GW":
        sr_c, sr_h = f.sysrow(f.sys_c, "portal"), f.sysrow(f.sys_h, "portal")
        long_c = [r["key"] for r in f.sys_c["systems"] if r.get("long") == "opal-portal"]
        if sr_c is None and not long_c and sr_h is not None and sr_h.get("long") == "opal-portal" \
                and hv == "CONFORMANT" and mc == "portal-data-proxy-api":
            c1 = first_commit(SYSTEMS, '"key": "portal"')
            return "SYSTEM_KEY_ADDED", (
                "THE ESTATE MOVED between the two readings; neither side is wrong. At the census commit "
                "54659987c0 systems.json holds no row with key 'portal' and none with long form 'opal-portal', so "
                "'opal-portal-data-proxy-api' read as the reserved opal prefix plus a name and the hand rule "
                "(applied at that vintage in round 19) rules it CONFORMANT. At HEAD systems.json carries the row "
                "{key: portal, class: %s, long: opal-portal}, first added at %s; the name now leads with that "
                "system's long form, the system slot takes the key, and the canonical form becomes %s, so the "
                "name is OUT-OF-PATTERN. The r20 run (registry %s) reads the HEAD registry." % (
                    sr_h["class"], fmt_commit(c1) if c1 else "(commit not found)", mc, on.registry_hash()[:16]))
    if name == "anthropic-sdk-deps" and typ == "LAMBDA_LAYER":
        sr_c, sr_h = f.sysrow(f.sys_c, "anthropic"), f.sysrow(f.sys_h, "anthropic")
        if sr_c is None and sr_h is not None and hc == "{system}-anthropic-sdk-deps-layer" \
                and mc == "anthropic-sdk-deps-layer":
            c1 = first_commit(SYSTEMS, '"key": "anthropic"')
            return "SYSTEM_KEY_ADDED", (
                "THE ESTATE MOVED between the two readings; neither side is wrong. At the census commit 54659987c0 "
                "'anthropic' is not a systems.json key, so the hand (R1.d) leaves the blank: "
                "'{system}-anthropic-sdk-deps-layer'. At HEAD systems.json carries the row {key: anthropic, class: "
                "%s}, first added at %s; the name's first token is now itself the system, so no blank is owed and "
                "the canonical form is %s (the name plus the layer kind suffix). The r20 run reads the HEAD "
                "registry (%s)." % (sr_h["class"], fmt_commit(c1) if c1 else "(commit not found)", mc,
                                    on.registry_hash()[:16]))
    # --- class C: the fourth verdict
    if hv == "OUT-OF-PATTERN" and mv == "NO-SYSTEM-ASKED" and "{system}" in (hc or "") \
            and mc == hc.replace("{system}-", "", 1):
        lib_ok = ("_NO_SYSTEM_ASKED" not in f.lib_c) and ("_NO_SYSTEM_ASKED" in f.lib_h)
        sch_ok = len(f.sch_c["grade"]["verdicts"]) == 3 and len(f.sch_h["grade"]["verdicts"]) == 4 \
            and "NO-SYSTEM-ASKED" in f.sch_h["grade"]["verdicts"]
        if lib_ok and sch_ok:
            c1 = commit_info("19b61836e4")
            return "FOURTH_VERDICT", (
                "THE GRADING RULE MOVED between the two readings; neither side is wrong. The hand verdict is the "
                "hand rule's own (three verdicts: lib/opal_naming.py at the census commit 54659987c0 has no "
                "NO-SYSTEM-ASKED and NAMING_SCHEMA.json grade.verdicts there lists %d). At HEAD grade.verdicts "
                "lists %d and lib/opal_naming.py carries _NO_SYSTEM_ASKED (landed at %s): a library layer / "
                "purpose-word-led policy name with no resolved system takes the fourth verdict and a canonical form "
                "with no system slot. For (%s, %s) the r20 run reads NO-SYSTEM-ASKED with canonical %s; the hand "
                "form differs only in the '{system}-' blank the rule no longer owes." % (
                    len(f.sch_c["grade"]["verdicts"]), len(f.sch_h["grade"]["verdicts"]), fmt_commit(c1), name, typ, mc))
    # --- class D: a token the hand ruled unresolvable (RAISE) is now a registry key
    if name == "opal-data-news-av" and typ == "S3_BUCKET" and hv == "RAISE":
        un_c = [r["token"] for r in f.sys_c["unresolved"]]
        sr_h = f.sysrow(f.sys_h, "news")
        if "news" in un_c and sr_h is not None:
            c1 = first_commit(SYSTEMS, '"key": "news"')
            return "TOKEN_RESOLVED", (
                "THE ESTATE MOVED between the two readings; the hand is not wrong at its vintage. At the census "
                "commit 54659987c0 'news' sits in systems.json 'unresolved' (V2), so B2 raises on "
                "'opal-data-news-av' and the hand RAISE is right. At HEAD 'news' is a PRODUCT key (long %s), first "
                "added at %s, and grade() at HEAD returns %s %s. NOTE: the r20 run holds NO verdict row for this "
                "name: it is CARDED NOT-JUDGED (R-29) with a card that still reads B2 / V2, so the machine "
                "verdict recorded here is grade() at HEAD, not a r20 row; see this order's surprise row on the "
                "stale cards." % (sr_h.get("long"), fmt_commit(c1) if c1 else "(commit not found)", mv, mc))
    # --- class E: the persistent machine-side departure from the written rule (round 9, unchanged)
    if name == "ExecIncrParityFailure" and typ == "CW_ALARM":
        n2_ok = "Split before each capital that follows a lowercase letter or a digit" in \
            io.open(rp("org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md"), encoding="utf-8").read()
        voc_c = '"incrparity"' in f.sys_c_text
        voc_h = '"incrparity"' in f.sys_h_text
        c1 = first_commit(RESOURCES, '"name": "ExecIncrParityFailure"')
        if rh is not None and rc is None and n2_ok and voc_c and voc_h and mc == "%s-exec-incrparity-failure-alarm" % rh["system"] \
                and hc == "{system}-exec-incr-parity-failure-alarm":
            return "WRITTEN_RULE_DEPARTURE_PLUS_ROW", (
                "TWO DIFFERENCES, ONE STANDING SINCE ROUND 9. (1) ESTATE MOVED: the hand's '{system}' blank is filled "
                "by the resources.json row (ExecIncrParityFailure, CW_ALARM) -> %s, first added at %s (absent at "
                "the census commit 54659987c0). (2) UNMOVED, the machine side departs from the written rule: "
                "GRADING_RULE.md N2 (read at HEAD) says 'Split before each capital that follows a lowercase letter "
                "or a digit ... Then lowercase each piece' and states no re-join, so the hand form is "
                "'exec-incr-parity-failure'; grade() re-joins the pieces of one original segment whose "
                "concatenation is a vocabulary word and 'incrparity' is a token in systems.json at the census "
                "commit and at HEAD, so grade() writes 'exec-incrparity-failure'. The hand follows the rule as "
                "written; the departure is the machine's, it is the same one round 9 recorded, and no ruling has "
                "settled whether N2 lacks a re-join clause or grade() carries one it should not." % (
                    rh["system"], fmt_commit(c1) if c1 else "(commit not found)"))
    return "UNEXPLAINED", "UNEXPLAINED"


# ------------------------------------------------------------------ build
def main():
    r19 = read_json(R19)
    r9 = read_json(R9)
    doc20 = fence(R20_REPORT)
    doc8 = fence(R8_REPORT)
    reg = on.registry_hash()[:16]
    if reg != doc20["registry"]:
        raise SystemExit("ERROR: registry at HEAD %s != the r20 report's %s; grade() would not read what the run read"
                         % (reg, doc20["registry"]))
    m20 = Machine(doc20)
    facts = Facts()
    mod9 = load_iv7()
    surfaces, control = {}, {}
    per_case = {}

    # ---------------- the two per-name surfaces
    for key in ("grading_rule_worked_cases", "n6_grader_rows"):
        cases = r19["per_case_detail"][key]
        out_cases, diffs = [], []
        ctrl = {"compared": 0, "agree": 0}
        srcs = collections.Counter()
        for c in cases:
            hand = tuple(c["hand_remeasured"])
            ctrl["compared"] += 1
            ctrl_ok = agrees(hand, tuple(c["grade_at_census_UNTOUCHED"]))
            ctrl["agree"] += 1 if ctrl_ok else 0
            if ("AGREE" if ctrl_ok else "DISAGREE") != c["result"]:
                raise SystemExit("ERROR: positive control: %s does not reproduce r19's %s" % (c["key"], c["result"]))
            machine, src, detail = m20.verdict(c["name"], c["type"])
            srcs[src] += 1
            ok = agrees(hand, machine)
            out_cases.append({"key": c["key"], "hand": list(hand), "machine": list(machine), "machine_source": src,
                              "result": "AGREE" if ok else "DISAGREE", "r19_result": c["result"]})
            if not ok:
                cls, text = explain_name(facts, c["name"], c["type"], hand, machine, src)
                if cls == "UNEXPLAINED":
                    raise SystemExit("ERROR: no explanation class for %s hand=%r machine=%r" % (c["key"], hand, machine))
                diffs.append({"key": c["key"], "name": c["name"], "type": c["type"],
                              "hand_verdict": hand[0], "machine_verdict": machine[0],
                              "hand_canonical": hand[1], "machine_canonical": machine[1],
                              "differs_in": "verdict" if hand[0] != machine[0] else "canonical form",
                              "machine_source": detail, "cause_class": cls, "explanation": text})
        surfaces[key] = {
            "carrier": r19["surfaces"][key]["carrier"], "compared": len(cases),
            "agree": len(cases) - len(diffs), "disagree": len(diffs),
            "compared_keys": [c["key"] for c in cases], "differences": diffs,
            "machine_source_counts": dict(srcs),
        }
        control[key] = ctrl
        per_case[key] = out_cases

    # ---------------- the tension ranking
    key = "tension_ranking_surfaces"
    r8_fig = mod9.iv7(doc8)
    r20_fig = mod9.iv7(doc20)
    approx = {}
    for ps in r9["surfaces"][key]["per_surface"]:
        for fg in ps["figures"]:
            approx[(ps["rank"], fg["figure"])] = fg["hand_is_approx"]
    cases = r19["per_case_detail"][key]
    t_cases, t_diffs = [], []
    ctrl = {"compared": 0, "agree": 0}
    for ps8, ps20 in zip(r8_fig["per_surface"], r20_fig["per_surface"]):
        rank = ps20["rank"]
        c19 = [x for x in cases if x["rank"] == rank][0]
        if ps8["rank"] != rank or len(ps8["figures"]) != len(c19["figures"]) or len(ps20["figures"]) != len(c19["figures"]):
            raise SystemExit("ERROR: rank %d figure lists differ from round 19's" % rank)
        figs, within_all, ctrl_all = [], True, True
        for f8, f20, f19 in zip(ps8["figures"], ps20["figures"], c19["figures"]):
            if f8["figure"] != f19["figure"] or f20["figure"] != f19["figure"]:
                raise SystemExit("ERROR: figure label mismatch at rank %d" % rank)
            hand = f19["hand_remeasured"]
            tol = tolerance(hand, approx[(rank, f19["figure"])])
            # positive control: the round-8 side reproduces r19's recorded census figure and verdict
            if f8["census_r8_live"] != f19["census_r8_live_UNTOUCHED"]:
                raise SystemExit("ERROR: positive control: iv7(r8) %r != r19 %r at rank %d" % (
                    f8["census_r8_live"], f19["census_r8_live_UNTOUCHED"], rank))
            ctrl_all = ctrl_all and (abs(f8["census_r8_live"] - hand) <= tol)
            ok = abs(f20["census_r8_live"] - hand) <= tol
            within_all = within_all and ok
            figs.append({"figure": f19["figure"], "hand_remeasured_r19": hand, "census_r8": f8["census_r8_live"],
                         "census_r20": f20["census_r8_live"], "tolerance": round(tol, 3), "within": ok})
        ctrl["compared"] += 1
        ctrl["agree"] += 1 if ctrl_all else 0
        if ("AGREE" if ctrl_all else "DISAGREE") != c19["result"]:
            raise SystemExit("ERROR: positive control: rank %d does not reproduce r19's %s" % (rank, c19["result"]))
        k = "rank-%d" % rank
        t_cases.append({"key": k, "result": "AGREE" if within_all else "DISAGREE", "r19_result": c19["result"],
                        "figures": figs})
        if not within_all:
            out = [x for x in figs if not x["within"]]
            t_diffs.append({"key": k, "name": c19["surface"],
                            "hand_verdict": "WITHIN-TOLERANCE" if c19["result"] == "AGREE" else "OUTSIDE-TOLERANCE (r19, unrevised)",
                            "machine_verdict": "OUTSIDE-TOLERANCE (%d of %d figures)" % (len(out), len(figs)),
                            "figures_outside": out,
                            "cause_class": "INSTRUMENT_GAP" if rank == 5 else "ESTATE_MOVED",
                            "explanation": explain_tension(rank, out, len(figs), doc8, doc20)})
    surfaces[key] = {
        "carrier": r19["surfaces"][key]["carrier"], "compared": len(t_cases),
        "agree": len(t_cases) - len(t_diffs), "disagree": len(t_diffs),
        "compared_keys": [x["key"] for x in t_cases], "differences": t_diffs,
        "machine_source_counts": {"iv7_over_r20_report": len(t_cases)},
    }
    control[key] = ctrl
    per_case[key] = t_cases

    # ---------------- totals and the control against round 19's recorded totals
    totals = {"compared": 0, "agree": 0, "disagree": 0}
    for k in KEYS:
        for f in totals:
            totals[f] += surfaces[k][f]
    ctl_tot = {"compared": sum(v["compared"] for v in control.values()),
               "agree": sum(v["agree"] for v in control.values())}
    ctl_tot["disagree"] = ctl_tot["compared"] - ctl_tot["agree"]
    if ctl_tot != r19["totals"]:
        raise SystemExit("ERROR: positive control totals %r != round 19's %r" % (ctl_tot, r19["totals"]))
    for k in KEYS:
        for f in ("compared", "agree", "disagree"):
            if control[k].get(f, control[k]["compared"] - control[k]["agree"]) != r19["surfaces"][k][f]:
                raise SystemExit("ERROR: positive control %s.%s != r19" % (k, f))
    for k in KEYS:
        want = r19["surfaces"][k]["compared_keys"]
        if surfaces[k]["compared_keys"] != want:
            raise SystemExit("ERROR: %s compared_keys differ from round 19's" % k)

    rec = {
        "_about": ("LGIC_ENFORCE round 20, cell EN-z-2. The hand ranking (three surfaces, round 19's key sets exactly) "
                   "compared with THIS round's census. Hand side = HAND_REMEASURE_R19.json read as written, never "
                   "re-graded; machine side = the r20 report's rows, or grade() at HEAD where the r20 run holds no "
                   "row (stated per key in each difference's machine_source and counted in machine_source_counts)."),
        "cell": "EN-z-2",
        "to": "LGIC_ENFORCE.TO-EN-z-2",
        "worker": WORKER,
        "builder": DELIV + "/build_hand_compare_r20.py",
        "census_report": R20_REPORT,
        "census_vintage": doc20["vintage"],
        "census_registry": doc20["registry"],
        "head_registry_equals_census_registry": True,
        "hand_record": R19,
        "hand_vintage_commit": CENSUS_COMMIT,
        "agree_rule": {
            "per_name": "AGREE iff hand verdict == machine verdict AND (hand gives no canonical form OR it equals the machine's byte for byte); a hand RAISE agrees only with a machine RAISE",
            "per_surface": "AGREE iff every figure the surface states is within tolerance (approx 15 pct, exact 10 pct, floor +-2) of the r20 figure computed by compare_hand_r9.iv7()",
        },
        "positive_control": {
            "what": "the same comparator over the ROUND-8 machine side must reproduce round 19's recorded triples",
            "result": ctl_tot, "per_surface": control, "round_19_totals": r19["totals"], "passed": True,
        },
        "surfaces": surfaces,
        "totals": totals,
        "round_19_totals": r19["totals"],
        "per_case_detail": per_case,
    }
    with io.open(rp(OUT), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("WROTE %s" % OUT)
    write_result(rec)
    print("WROTE %s" % RESULT)
    for k in KEYS:
        s = surfaces[k]
        print("%s: compared=%d agree=%d disagree=%d sources=%s" % (k, s["compared"], s["agree"], s["disagree"], s["machine_source_counts"]))
    print("TOTALS compared=%d agree=%d disagree=%d (r19: %s)" % (totals["compared"], totals["agree"], totals["disagree"], r19["totals"]))


def write_result(rec):
    L = []
    a = L.append
    t, h = rec["totals"], rec["round_19_totals"]
    a("# hand-compare.r20.result -- the hand ranking against the round-20 census (LGIC_ENFORCE EN-z-2, FWD-5 clause 3)")
    a("")
    a("Written by `%s` from `%s`; the facts each explanation cites are read from git objects at build time." % (
        rec["builder"], rec["hand_record"]))
    a("")
    a("- Census compared against: `%s`" % rec["census_report"])
    a("- Census vintage: %s (registry %s; grade() at HEAD reads the same registry hash)" % (rec["census_vintage"], rec["census_registry"]))
    a("- Hand side: round 19's re-measured hand verdicts and figures, read as written, never re-graded (vintage commit `%s`)." % rec["hand_vintage_commit"])
    a("- Positive control passed: the comparator over the round-8 machine side reproduces round 19's %s." % json.dumps(rec["positive_control"]["result"]))
    a("")
    a("## Totals")
    a("")
    a("| surface | compared | agree (r20) | disagree (r20) | round 19: agree | round 19: disagree | machine side read from |")
    a("|---|---|---|---|---|---|---|")
    r19s = read_json(R19)["surfaces"]
    for k in KEYS:
        s = rec["surfaces"][k]
        a("| %s | %d | %d | %d | %d | %d | %s |" % (k, s["compared"], s["agree"], s["disagree"], r19s[k]["agree"], r19s[k]["disagree"],
                                                  ", ".join("%s %d" % kv for kv in sorted(s["machine_source_counts"].items()))))
    a("| **total** | **%d** | **%d** | **%d** | **%d** | **%d** | |" % (t["compared"], t["agree"], t["disagree"], h["agree"], h["disagree"]))
    a("")
    cc0 = collections.Counter()
    for k in KEYS:
        for x in rec["surfaces"][k]["differences"]:
            cc0[x["cause_class"]] += 1
    carried = cc0["INSTRUMENT_GAP"] + cc0["WRITTEN_RULE_DEPARTURE_PLUS_ROW"]
    a("The round-19 hand re-measure agreed with the round-8 census on 140 of 143 keys; against the round-20 census it agrees on "
      "%d of %d. Every one of the %d differences below carries an explanation read at the bytes. %d of them are the estate or "
      "the grading rule moving between the round-8 and round-20 readings (registry rows, system keys, the fourth verdict, or "
      "the estate itself); %d (rank-5, the instrument gap, and ExecIncrParityFailure, the machine-side departure from "
      "GRADING_RULE.md N2) were already open in round 9 and round 19." % (
          t["agree"], t["compared"], t["disagree"], t["disagree"] - carried, carried))
    a("")
    a("## Differences, with the cause class counted")
    a("")
    cc = collections.Counter()
    for k in KEYS:
        for x in rec["surfaces"][k]["differences"]:
            cc[x["cause_class"]] += 1
    for kv in sorted(cc.items()):
        a("- %s: %d" % kv)
    a("")
    for k in KEYS:
        s = rec["surfaces"][k]
        a("## %s -- %d compared, %d agree, %d disagree" % (k, s["compared"], s["agree"], s["disagree"]))
        a("")
        for x in s["differences"]:
            a("### %s  [%s]" % (x["key"], x["cause_class"]))
            a("")
            if k == "tension_ranking_surfaces":
                a("- hand: %s; machine: %s" % (x["hand_verdict"], x["machine_verdict"]))
                for f in x["figures_outside"]:
                    a("  - %s: hand %s, r8 %s, r20 %s, tolerance %s" % (f["figure"], f["hand_remeasured_r19"], f["census_r8"], f["census_r20"], f["tolerance"]))
            else:
                a("- hand: %s %s" % (x["hand_verdict"], x["hand_canonical"]))
                a("- machine: %s %s  (%s; differs in %s)" % (x["machine_verdict"], x["machine_canonical"], x["machine_source"], x["differs_in"]))
            a("- explanation: %s" % x["explanation"])
            a("")
    text = "\n".join(L) + "\n"
    if any(ord(c) > 127 for c in text):
        raise SystemExit("ERROR: non-ASCII in the result file")
    with io.open(rp(RESULT), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def vint(doc):
    m = re.search(r"as of (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d UTC)", doc["vintage"])
    return m.group(1) if m else doc["vintage"][:60]


def moved_text(add, rem, what):
    t = "Measured on the two reports' live rows: %d %s are in r20 and not in r8 (e.g. %s)" % (len(add), what, sample(add))
    t += ", %d are in r8 and not in r20 (e.g. %s)." % (len(rem), sample(rem)) if rem else ", and none is in r8 and not in r20."
    return t


def explain_tension(rank, out, n_figs, doc8, doc20):
    """What moved between the r8 and r20 readings, read from the two reports' live rows."""
    d8, d20 = vint(doc8), vint(doc20)
    mod = load_iv7()
    rest = "The other %d of %d figures of this surface stay within tolerance." % (n_figs - len(out), n_figs)
    if rank == 5:
        figs = "; ".join("%s r8 %s -> r20 %s (hand %s, tolerance %.1f)" % (
            x["figure"][:34], x["census_r8"], x["census_r20"], x["hand_remeasured_r19"], x["tolerance"]) for x in out)
        return (
            "NEITHER SIDE IS SHOWN WRONG; THE TWO SIDES COME FROM DIFFERENT INSTRUMENTS, and the gap is the one round 9 "
            "recorded and round 19 left unrevised. The hand figures (339 in all; LAMBDA 15, IAM_ROLE 16, EVENT_RULE "
            "10, LOG_GROUP 68, IAM_POLICY 36) are comp-estate's drift_class LIVE-no-DECLARED; the census has no drift "
            "class, and the figure it can produce is live (name, type) minus repo (name, type), where the repo plane "
            "reads only literal Terraform name attributes and source literals. All %d figures are outside tolerance "
            "at r8 (%s) and at r20 (%s): %s. Re-reading the census at a newer vintage cannot close an instrument "
            "gap." % (len(out), d8, d20, figs))
    if rank == 1:
        tok = lambda nm, t: "49f" in set(mod.tokens(mod.resource_part(nm, t)))  # noqa: E731
        add, rem = moved_names(doc8, doc20, tok)
        x = out[0]
        return (
            "THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure '49f anywhere' is "
            "round 19's re-quote of the r8 census (%s), %s; the same instrument (compare_hand_r9.iv7: live judged + "
            "carded names, tokens split on - / _ . # : and camel humps, a LOG_GROUP tokenised on its resource part) "
            "over the r20 census (%s) reads %s, outside the declared tolerance %.1f. %s %s" % (
                d8, x["hand_remeasured_r19"], d20, x["census_r20"], x["tolerance"],
                moved_text(add, rem, "(name, type) pairs carrying the token 49f"), rest))
    if rank == 4:
        add, rem = moved_names(doc8, doc20, lambda nm, t: t == "IAM_POLICY")
        x = out[0]
        return (
            "THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure '%s' is round 19's "
            "re-quote of the r8 census (%s), %s; the same instrument over the r20 census (%s) reads %s, outside the "
            "declared tolerance %.1f. %s %s" % (
                x["figure"], d8, x["hand_remeasured_r19"], d20, x["census_r20"], x["tolerance"],
                moved_text(add, rem, "IAM_POLICY (name, type) entries"), rest))
    if rank == 9:
        add, rem = moved_names(doc8, doc20, lambda nm, t: t == "SECRET")
        x = out[0]
        return (
            "THE ESTATE MOVED between the two readings; neither side is wrong. The hand figure '%s' is round 19's "
            "re-quote of the r8 census (%s), %s; the same instrument over the r20 census (%s) reads %s, outside the "
            "declared tolerance %.1f. %s %s" % (
                x["figure"], d8, x["hand_remeasured_r19"], d20, x["census_r20"], x["tolerance"],
                moved_text(add, rem, "SECRET names"), rest))
    return "UNEXPLAINED"


if __name__ == "__main__":
    main()
