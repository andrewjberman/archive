#!/usr/bin/env python3
"""check_canon_r1.py -- the mechanical criteria of LGIC_CANON round 1 (decomposition v3), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-1 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line `VERDICT: PASS-<X>` or
`VERDICT: FAIL-<X>`, and exits 0. A missing input is a FAIL verdict, never a traceback. No PASS string is a substring
of another subcommand's PASS or FAIL string, because proof-of-spec-check greps <expect> unanchored.
`--list` prints the subcommands; `selftest-negative` runs every one and counts the PASS verdicts.

The fixed inputs beside this file: CN_TREE_MDPF.md (the judged tree), CN_JUDGE_CASES.json and CN_JUDGE_NAMING_KEY.json
(the judges' naming cases and their key), CN_NAMING_JOB.json and CN_NAMING_KEY.json (the naming job and its key).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "org/missions/D14/LGIC/LGIC_CANON"
DEL = BASE + "/deliverables"
EX = DEL + "/exercises"
FIX = DEL + "/2.0.0_SA_COO~G/fixed_inputs/r1"
CANON = "infra/logic/02_DOCTRINE.md"
RENDER = "infra/logic/render_naming_section.py"
LEDGER = "infra/logic/06_CONFORMANCE_LEDGER.md"
CHECKLIST = "infra/logic/10_ONBOARDING_CHECKLIST.md"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
SCOPES = "infra/logic/registry/scopes.json"
ENFORCE_PRD = "org/missions/D14/LGIC/LGIC_ENFORCE/prd/LGIC_ENFORCE_PRD.md"
BCKEND_PRD = "org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md"
TICKLIST = "infra/logic/04_SCOPE_TICKLIST.md"
FWD2 = DEL + "/FWD2_FROM_RECORD.md"
FWD3 = DEL + "/FWD3_FROM_RECORD.md"
REVIEW = DEL + "/CHECKLIST_REVIEW.md"
RECOUNT = DEL + "/0.9.0_WK_LGIC_CANON~2/ledger_recount.py"
JUDGE = {"a": EX + "/judge-a.tsv", "b": EX + "/judge-b.tsv"}
NAMING = {"a": EX + "/naming-a.tsv", "b": EX + "/naming-b.tsv"}
NAMING_COMPARE = EX + "/naming-compare.md"
BEGIN = "<!-- BEGIN GENERATED NAMING SECTION -->"
END = "<!-- END GENERATED NAMING SECTION -->"
AXES = ("A1", "A2", "A3", "A4", "A5")
VOCAB_AXIS = ("CONFORMS", "VIOLATES", "DECLARED-EXCEPTION", "DEPARTS-RECOMMENDED", "UNDETERMINED")
VOCAB_NAME = ("CONFORMANT", "ALIAS", "OUT-OF-PATTERN", "RAISE")
CITE_RE = re.compile(r"`?([\w./~-]+\.\w+)@([0-9a-f]{7,40})`?")


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


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, text=True)


def commit_ok(sha):
    return bool(sha) and re.match(r"^[0-9a-f]{7,40}$", sha or "") is not None and git("cat-file", "-e", sha + "^{commit}").returncode == 0


def at_commit(sha, path):
    """The file's text at a commit, or None."""
    if not commit_ok(sha):
        return None
    r = git("show", "%s:%s" % (sha, path))
    return r.stdout if r.returncode == 0 else None


def has_path(sha, path):
    return commit_ok(sha) and git("cat-file", "-e", "%s:%s" % (sha, path)).returncode == 0


def author_of(path):
    r = git("log", "-1", "--format=%an", "--", path)
    return r.stdout.strip() if r.returncode == 0 else ""


def tsv(path):
    """(meta, rows): a '# base <sha>' header line, then tab-separated rows; (None, None) when absent."""
    t = read(path)
    if t is None:
        return None, None
    meta, rows = {}, []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"#\s*(base)\s+(\S+)", s)
        if m:
            meta[m.group(1)] = m.group(2)
            continue
        if s.startswith("#"):
            continue
        rows.append([c.strip() for c in ln.split("\t")])
    return meta, rows


# ---------------------------------------------------------------- the canon (CN-k-1)
def canon_rules(text):
    """[(rule id 'R<n>', block text)] -- a rule opens at a line starting '**R<n>' and closes at the next rule, a ##/###
    heading or a '---' rule."""
    rules, cur, buf = [], None, []
    for ln in text.splitlines():
        m = re.match(r"^\*\*R(\d+)\b", ln)
        if m:
            if cur:
                rules.append((cur, "\n".join(buf)))
            cur, buf = "R" + m.group(1), [ln]
            continue
        if cur and (re.match(r"^#{2,3} ", ln) or re.match(r"^---\s*$", ln)):
            rules.append((cur, "\n".join(buf)))
            cur, buf = None, []
            continue
        if cur:
            buf.append(ln)
    if cur:
        rules.append((cur, "\n".join(buf)))
    return rules


def rule_ids():
    return set(r for r, _ in canon_rules(read(CANON) or ""))


def split_section(text):
    """(outside_lines, section_text) around the generated naming section; (None, None) if the markers are absent."""
    if text is None or BEGIN not in text or END not in text or text.index(BEGIN) > text.index(END):
        return None, None
    i, j = text.index(BEGIN), text.index(END)
    return (text[:i] + text[j + len(END):]).splitlines(), text[i:j + len(END)]


def k1_census():
    t = read(CANON)
    if t is None:
        return say("FAIL-K1-NO-CANON", "%s absent" % CANON)
    rules = canon_rules(t)
    full = [r for r, b in rules if all(k in b.lower() for k in ("authority:", "census:", "non-application:"))]
    for r, b in rules:
        if r not in full:
            print("MISSING A PART: %s" % r)
    m = re.search(r"^RULES CARRYING ALL THREE PARTS: (\d+) of (\d+)\s*$", t, re.M)
    print("RECOUNT BY THIS CHECKER: %d of %d rules carry authority, census and non-application" % (len(full), len(rules)))
    if not m:
        return say("FAIL-K1-NO-CENSUS-LINE", "the canon carries no line 'RULES CARRYING ALL THREE PARTS: <n> of <d>'")
    n, d = int(m.group(1)), int(m.group(2))
    ok = bool(rules) and len(full) == len(rules) and n == len(full) and d == len(rules)
    say("PASS-K1-CENSUS-OK" if ok else "FAIL-K1-CENSUS-DIFFERS", "PRINTED: %d of %d  RECOUNTED: %d of %d" % (n, d, len(full), len(rules)))


def run_render(*extra):
    r = subprocess.run([sys.executable, RENDER, "--check"] + list(extra), capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def k1_render():
    if not os.path.isfile(RENDER):
        return say("FAIL-K1-NO-RENDERER", "%s absent" % RENDER)
    outside, sec = split_section(read(CANON))
    if sec is None:
        return say("FAIL-K1-NO-SECTION", "the canon carries no '%s' ... '%s' pair" % (BEGIN, END))
    stamps = re.findall(r"^stamp: (\S+) (\S+) sha256:([0-9a-f]{64})\s*$", sec, re.M)
    rc, out = run_render()
    print("render --check rc=%d" % rc)
    print(out[-600:])
    ok = rc == 0 and bool(stamps)
    say("PASS-K1-RENDER-FRESH" if ok else "FAIL-K1-RENDER-STALE", "STAMP LINES IN THE SECTION: %d  --check rc: %d" % (len(stamps), rc))


def k1_stale():
    if not os.path.isfile(RENDER):
        return say("FAIL-K1-STALE-NO-RENDERER", "%s absent" % RENDER)
    t = read(CANON)
    outside, sec = split_section(t)
    if sec is None:
        return say("FAIL-K1-STALE-NO-SECTION", "no generated section to doctor")
    m = re.search(r"sha256:([0-9a-f]{64})", sec)
    if not m:
        return say("FAIL-K1-STALE-NO-STAMP", "no sha256 stamp in the section")
    h = m.group(1)
    bad = ("0" if h[0] != "0" else "1") + h[1:]
    tmpd = tempfile.mkdtemp(prefix="cn_k1_")
    try:
        clean, doct = os.path.join(tmpd, "clean.md"), os.path.join(tmpd, "doctored.md")
        with open(clean, "w", encoding="utf-8", newline="") as fh:
            fh.write(t)
        with open(doct, "w", encoding="utf-8", newline="") as fh:
            fh.write(t.replace("sha256:" + h, "sha256:" + bad, 1))
        rc_clean, _ = run_render("--canon", clean)
        rc_doct, out = run_render("--canon", doct)
    finally:
        shutil.rmtree(tmpd, ignore_errors=True)
    print("clean copy --check rc=%d  doctored copy --check rc=%d" % (rc_clean, rc_doct))
    print(out[-400:])
    ok = rc_clean == 0 and rc_doct != 0
    say("PASS-K1-STALE-REFUSED" if ok else "FAIL-K1-STALE-ACCEPTED", "A DOCTORED STAMP IS REFUSED: %s (and the clean copy passes: %s)" % (rc_doct != 0, rc_clean == 0))


def enum_sets():
    s = load_json(SCHEMA) or {}
    reg = load_json(SCOPES) or {}
    rows = reg.get("scopes", []) if isinstance(reg, dict) else []
    firm = set()
    for r in rows:
        if r.get("class") == "FIRM":
            firm.update(x for x in (r.get("long"), r.get("short"), r.get("key")) if x)
    for f in s.get("firm_forms") or []:
        firm.update(x for x in (f.get("key"), f.get("short")) if x)
    return {
        "firm forms": (firm, 2),
        "refused tokens": (set(s.get("refused_tokens") or {}), 2),
        "kinds": (set((s.get("kind") or {}).get("values") or []), 3),
        "tiers": (set((s.get("key") or {}).get("tier") or []), 2),
        "cadences": (set((s.get("cadence") or {}).get("values") or []), 2),
    }


TEMPLATE_RE = re.compile(r"\{system\}-\{scope\}-\{function\}|\{source\}/\{scope\}/\{tier\}")


def backtick_runs(line):
    """Runs of adjacent backticked tokens (separated by at most a few characters of space / , . or 'or')."""
    runs, cur, last_end = [], [], None
    for m in re.finditer(r"`([^`\s]+)`", line):
        gap = line[last_end:m.start()] if last_end is not None else None
        if cur and gap is not None and len(gap) <= 6 and re.match(r"^[\s/,|.]*(or|and)?[\s/,|.]*$", gap):
            cur.append(m.group(1))
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [m.group(1)]
        last_end = m.end()
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def k1_noenum():
    outside, sec = split_section(read(CANON))
    if outside is None:
        return say("FAIL-K1-NOENUM-NO-SECTION", "no generated section: every enumeration is outside one")
    sets = enum_sets()
    hits = []
    for i, ln in enumerate(outside, 1):
        if TEMPLATE_RE.search(ln):
            hits.append((i, "a naming grammar template", ln.strip()[:120]))
        for run in backtick_runs(ln):
            toks = set(t.strip("/.,") for t in run)
            for label, (members, need) in sets.items():
                got = toks & members
                if len(got) >= need:
                    hits.append((i, "%s %s" % (label, sorted(got)), ln.strip()[:120]))
    for h in hits:
        print("OUTSIDE LINE %d: %s  |  %s" % h)
    say("PASS-K1-NO-ENUM-OUTSIDE" if not hits else "FAIL-K1-ENUM-OUTSIDE",
        "LINES OUTSIDE THE GENERATED SECTION: %d  ENUMERATIONS FOUND THERE: %d" % (len(outside), len(hits)))


def section_by_heading(text, needle):
    """The text of the level-2 section whose heading contains `needle`, up to the next level-2 heading."""
    lines = (text or "").splitlines()
    out, on = [], False
    for ln in lines:
        if re.match(r"^## ", ln):
            if on:
                break
            on = needle.lower() in ln.lower()
            continue
        if on:
            out.append(ln)
    return "\n".join(out) if on or out else None


def bullets(sec):
    items, cur = [], None
    for ln in sec.splitlines():
        if re.match(r"^- ", ln):
            if cur is not None:
                items.append(cur)
            cur = ln
        elif cur is not None and ln.startswith("  "):
            cur += "\n" + ln
        elif cur is not None and not ln.strip():
            items.append(cur)
            cur = None
    if cur is not None:
        items.append(cur)
    return items


def k1_s6():
    sec = section_by_heading(read(CANON), "DOES NOT RULE")
    if sec is None:
        return say("FAIL-K1-S6-NO-SECTION", "the canon carries no section whose heading reads 'WHAT THIS DOCUMENT DOES NOT RULE'")
    items = bullets(sec)
    open_ = [b for b in items if not (b.startswith("- ~~") or "RULED" in b or "CLOSED" in b or "decider:" in b)]
    for b in open_:
        print("OPEN, NO DECIDER: %s" % b.splitlines()[0][:140])
    ok = bool(items) and not open_
    say("PASS-K1-S6-CLOSED" if ok else "FAIL-K1-S6-OPEN-ITEM", "ITEMS: %d  CLOSED OR NAMING A DECIDER: %d" % (len(items), len(items) - len(open_)))


def k1_d10():
    t = read(CANON)
    if t is None:
        return say("FAIL-K1-D10-NO-CANON", "%s absent" % CANON)
    axes = [a for a in AXES if re.search(r"\*\*%s\b" % a, t)]
    schema_line = "PERMANENT | CONDITIONAL" in t
    cites = [ln for ln in t.splitlines() if "D10_GLOBAL_PIPELINE_STRUCTURE_PRD.md" in ln and re.search(r"(§|s\.)\s*[26]\b", ln)]
    bad = [ln for ln in cites if "absorbed" not in ln.lower()]
    for ln in bad:
        print("POINTER, NOT ABSORBED: %s" % ln.strip()[:140])
    ok = len(axes) == 5 and schema_line and bool(cites) and not bad
    say("PASS-K1-D10-ABSORBED" if ok else "FAIL-K1-D10-POINTER",
        "AXES DEFINED: %d of 5  REGISTER SCHEMA LINE: %s  D10 s.2/s.6 CITATIONS: %d  NOT MARKED ABSORBED: %d" % (len(axes), schema_line, len(cites), len(bad)))


def k1_r1code():
    rules = dict(canon_rules(read(CANON) or ""))
    b = rules.get("R1")
    if b is None:
        return say("FAIL-K1-R1-ABSENT", "the canon carries no rule R1")
    i = b.lower().find("non-application:")
    if i < 0:
        return say("FAIL-K1-R1-NO-NONAPP", "R1 carries no non-application")
    na = b[i:].splitlines()
    hits = [ln for ln in na if "code/" in ln]
    unq = [ln for ln in hits if "legacy" not in ln.lower()]
    for ln in unq:
        print("code/ WITHOUT 'legacy': %s" % ln.strip()[:140])
    ok = bool(hits) and not unq
    say("PASS-K1-R1-LEGACY-CODE" if ok else "FAIL-K1-R1-CODE-UNQUALIFIED", "R1 NON-APPLICATION LINES NAMING code/: %d  WITHOUT 'legacy': %d" % (len(hits), len(unq)))


# ---------------------------------------------------------------- the blind judging (CN-j-1 .. CN-j-3)
def judge_rows(cell):
    meta, rows = tsv(JUDGE[cell])
    if rows is None:
        return None, None
    out = {}
    for r in rows:
        if len(r) >= 3:
            out[r[0]] = (r[1], set(re.findall(r"R\d+", r[2])), r[2])
    return meta, out


def cases():
    d = load_json(FIX + "/CN_JUDGE_CASES.json") or {}
    return [c["id"] for c in d.get("cases", [])]


def j_axes(cell):
    meta, rows = judge_rows(cell)
    if rows is None:
        return say("FAIL-J%s-AXES-ABSENT" % cell.upper(), "%s absent" % JUDGE[cell])
    ids = rule_ids()
    bad = []
    for a in AXES:
        v = rows.get(a)
        if not v or v[0] not in VOCAB_AXIS or not v[1] or not v[1] <= ids:
            bad.append((a, v[0] if v else None, sorted(v[1]) if v else None))
    for b in bad:
        print("AXIS NOT JUDGED: %s  verdict=%s  rules=%s" % b)
    say("PASS-J%s-AXES-JUDGED" % cell.upper() if not bad else "FAIL-J%s-AXES-UNJUDGED" % cell.upper(),
        "AXES: %d  JUDGED WITH A CANON RULE: %d  (rule ids in the canon: %d)" % (len(AXES), len(AXES) - len(bad), len(ids)))


def j_naming(cell):
    meta, rows = judge_rows(cell)
    cs = cases()
    if rows is None or not cs:
        return say("FAIL-J%s-CASES-ABSENT" % cell.upper(), "answer file or case list absent")
    ids = rule_ids()
    bad = []
    for c in cs:
        v = rows.get(c)
        cited = v and (re.search(r"R\d+|§\s*\d+", v[2]) is not None) and (not v[1] or v[1] <= ids)
        if not v or v[0] not in VOCAB_NAME or not cited:
            bad.append((c, v[0] if v else None, v[2] if v else None))
    for b in bad:
        print("CASE NOT GRADED: %s  verdict=%s  cited=%s" % b)
    say("PASS-J%s-CASES-GRADED" % cell.upper() if not bad else "FAIL-J%s-CASES-UNGRADED" % cell.upper(),
        "NAMING CASES: %d  GRADED WITH A CANON CITATION: %d" % (len(cs), len(cs) - len(bad)))


def j_base(cell):
    meta, _ = tsv(JUDGE[cell])
    base = (meta or {}).get("base")
    ok = commit_ok(base)
    say("PASS-J%s-BASE-STATED" % cell.upper() if ok else "FAIL-J%s-BASE-MISSING" % cell.upper(), "BASE: %s  resolves to a commit: %s" % (base, ok))


def j3_verdicts():
    _, a = judge_rows("a")
    _, b = judge_rows("b")
    if a is None or b is None:
        return say("FAIL-J3-VERDICTS-ABSENT", "judge-a: %s  judge-b: %s" % (a is not None, b is not None))
    diff = [(x, (a.get(x) or ("",))[0], (b.get(x) or ("",))[0]) for x in AXES if (a.get(x) or ("",))[0] != (b.get(x) or ("",))[0]]
    for d in diff:
        print("VERDICTS DIFFER: %s  A=%s  B=%s" % d)
    say("PASS-J3-SAME-VERDICTS" if not diff else "FAIL-J3-VERDICTS-DIFFER", "AXES: %d  SAME VERDICT: %d" % (len(AXES), len(AXES) - len(diff)))


def j3_citations():
    _, a = judge_rows("a")
    _, b = judge_rows("b")
    if a is None or b is None:
        return say("FAIL-J3-CITATIONS-ABSENT", "an answer file is absent")
    diff = [(x, sorted((a.get(x) or ("", set()))[1]), sorted((b.get(x) or ("", set()))[1])) for x in AXES
            if (a.get(x) or ("", set()))[1] != (b.get(x) or ("", set()))[1] or not (a.get(x) or ("", set()))[1]]
    for d in diff:
        print("CITATIONS DIFFER: %s  A=%s  B=%s" % d)
    say("PASS-J3-SAME-CITATIONS" if not diff else "FAIL-J3-CITATIONS-DIFFER", "AXES: %d  SAME RULE SET: %d" % (len(AXES), len(AXES) - len(diff)))


def j3_naming_key():
    _, a = judge_rows("a")
    _, b = judge_rows("b")
    key = (load_json(FIX + "/CN_JUDGE_NAMING_KEY.json") or {}).get("key") or {}
    if a is None or b is None or not key:
        return say("FAIL-J3-KEY-ABSENT", "an answer file or the key is absent")
    wrong = [(c, (a.get(c) or ("",))[0], (b.get(c) or ("",))[0], k) for c, k in sorted(key.items())
             if (a.get(c) or ("",))[0] != k or (b.get(c) or ("",))[0] != k]
    for w in wrong:
        print("CASE OFF THE KEY: %s  A=%s  B=%s  key=%s" % w)
    say("PASS-J3-CASES-MATCH-KEY" if not wrong else "FAIL-J3-CASES-OFF-KEY", "CASES: %d  BOTH JUDGES ON THE KEY: %d" % (len(key), len(key) - len(wrong)))


def blind_pair(files, label):
    ma, _ = tsv(files["a"])
    mb, _ = tsv(files["b"])
    ba, bb = (ma or {}).get("base"), (mb or {}).get("base")
    if not (commit_ok(ba) and commit_ok(bb)):
        return say("FAIL-%s-BLIND-NO-BASES" % label, "BASE A: %s  BASE B: %s" % (ba, bb))
    leak = [n for n, sha, p in (("A's base holds B's file", ba, files["b"]), ("B's base holds A's file", bb, files["a"])) if has_path(sha, p)]
    for n in leak:
        print("NOT BLIND: %s" % n)
    say("PASS-%s-MUTUALLY-BLIND" % label if not leak else "FAIL-%s-NOT-BLIND" % label, "BASE A: %s  BASE B: %s  LEAKS: %d of 2" % (ba, bb, len(leak)))


# ---------------------------------------------------------------- graded from the record (CN-r-1, CN-r-2)
def cites_ok(text):
    return [(p, c) for p, c in CITE_RE.findall(text or "") if has_path(c, p)]


def r1_clauses():
    t = read(FWD2)
    if t is None:
        return say("FAIL-R1-RECORD-ABSENT", "%s absent" % FWD2)
    parts = re.split(r"^(?=CLAUSE [123]:)", t, flags=re.M)
    got = {}
    for p in parts:
        m = re.match(r"^CLAUSE ([123]):", p)
        if m:
            got[m.group(1)] = cites_ok(p)
    miss = [n for n in "123" if not got.get(n)]
    for n in miss:
        print("CLAUSE %s: no path@commit citation that resolves" % n)
    say("PASS-R1-CLAUSES-EVIDENCED" if not miss else "FAIL-R1-CLAUSE-UNEVIDENCED", "CLAUSES: 3  EACH BESIDE RESOLVABLE EVIDENCE: %d" % (3 - len(miss)))


def r1_ticked():
    t = read(FWD2)
    if t is None:
        return say("FAIL-R1-TICKED-ABSENT", "%s absent" % FWD2)
    phrase = "Nothing on this table is open"
    quoted = phrase in t
    good = [c for p, c in CITE_RE.findall(t) if p == TICKLIST and phrase in (at_commit(c, p) or "") and "v0.2" in (at_commit(c, p) or "")]
    say("PASS-R1-TICKED-QUOTED" if quoted and good else "FAIL-R1-TICKED-UNQUOTED",
        "QUOTES '%s': %s  CITES %s@<commit> WHERE THAT TEXT AND v0.2 STAND: %d" % (phrase, quoted, TICKLIST, len(good)))


def r2_branches():
    t = read(FWD3)
    if t is None:
        return say("FAIL-R2-RECORD-ABSENT", "%s absent" % FWD3)
    rows = re.findall(r"^PROJECT (IRPT_FNTEND|IRPT_BCKEND): branch (nothing-conflicts|list-of-changes|derived)\b(.*)$", t, re.M)
    got = {p: (b, cites_ok(rest)) for p, b, rest in rows}
    miss = [p for p in ("IRPT_FNTEND", "IRPT_BCKEND") if p not in got or not got[p][1]]
    for p in miss:
        print("PROJECT %s: no branch line with a resolvable path@commit" % p)
    say("PASS-R2-BRANCHES-CITED" if not miss else "FAIL-R2-BRANCH-UNCITED", "PROJECTS: 2  BRANCH CITED: %d" % (2 - len(miss)))


def r2_bckend():
    t = read(FWD3)
    prd = read(BCKEND_PRD)
    if t is None or prd is None:
        return say("FAIL-R2-BCKEND-ABSENT", "record: %s  PRD: %s" % (t is not None, prd is not None))
    m = re.search(r'"prd_version":\s*"([^"]+)"', prd)
    live = m.group(1) if m else None
    r = re.search(r"^IRPT_BCKEND PRD AT HEAD: (\S+) \(MEASURED\)\s*$", t, re.M)
    a = re.search(r"^CONTRADICTS ABSORBED: ([0-3]) of 3 \(MEASURED\)\s*$", t, re.M)
    ok = bool(live) and bool(r) and r.group(1) == live and bool(a)
    say("PASS-R2-BCKEND-MEASURED" if ok else "FAIL-R2-BCKEND-UNMEASURED",
        "PRD version at HEAD: %s  RECORD STATES: %s  ABSORPTION LINE: %s" % (live, r.group(1) if r else None, a.group(0) if a else None))


# ---------------------------------------------------------------- the checklist (CN-o-1, CN-o-2)
def steps():
    t = read(CHECKLIST)
    if t is None:
        return None
    out, cur, buf = [], None, []
    for ln in t.splitlines():
        m = re.match(r"^### STEP (\d+)\b", ln)
        if m:
            if cur is not None:
                out.append((cur, "\n".join(buf)))
            cur, buf = int(m.group(1)), [ln]
            continue
        if cur is not None and re.match(r"^#{2,3} ", ln):
            out.append((cur, "\n".join(buf)))
            cur, buf = None, []
            continue
        if cur is not None:
            buf.append(ln)
    if cur is not None:
        out.append((cur, "\n".join(buf)))
    return out


def o1_order():
    st = steps()
    if not st:
        return say("FAIL-O1-NO-STEPS", "%s absent or carries no '### STEP <n>'" % CHECKLIST)
    nums = [n for n, _ in st]
    ok = nums == list(range(1, len(nums) + 1)) and len(nums) >= 3 and "identity row" in st[0][1].lower() and "dashboard" in st[-1][1].lower()
    say("PASS-O1-ORDERED" if ok else "FAIL-O1-UNORDERED",
        "STEPS: %d numbered %s  FIRST NAMES THE IDENTITY ROW: %s  LAST NAMES THE DASHBOARD: %s"
        % (len(nums), nums, "identity row" in st[0][1].lower(), "dashboard" in st[-1][1].lower()))


def o1_rules():
    st = steps()
    if not st:
        return say("FAIL-O1-RULES-NO-STEPS", "no steps")
    ids = rule_ids()
    bad = []
    for n, b in st:
        m = re.search(r"^rule: (.+)$", b, re.M)
        got = set(re.findall(r"R\d+", m.group(1))) if m else set()
        if not got or not got <= ids:
            bad.append((n, sorted(got)))
    for b in bad:
        print("STEP %d: no canon rule named (%s)" % b)
    say("PASS-O1-RULES-NAMED" if not bad else "FAIL-O1-RULE-UNNAMED", "STEPS: %d  NAMING A CANON RULE: %d" % (len(st), len(st) - len(bad)))


def contract_names():
    t = read(ENFORCE_PRD) or ""
    i = t.find("## CONTRACTS")
    j = t.find("\n## ", i + 5)
    names = []
    for ln in t[i:j].splitlines() if i >= 0 else []:
        if ln.startswith("|") and not ln.startswith("|---"):
            c = ln.split("|")[1].strip()
            if c and c.lower() != "contract":
                names.append(re.sub(r"\s+", " ", c.replace("`", "")).lower())
    return names


def o1_builders():
    st = steps()
    names = contract_names()
    if not st or not names:
        return say("FAIL-O1-BUILDERS-ABSENT", "steps: %s  LGIC_ENFORCE CONTRACTS names: %d" % (bool(st), len(names)))
    bad = []
    for n, b in st:
        m = re.search(r"^builder: (.+)$", b, re.M)
        v = re.sub(r"\s+", " ", m.group(1).replace("`", "")).lower().strip() if m else ""
        if not v or not any(v.startswith(x) for x in names):
            bad.append((n, v[:60]))
    for b in bad:
        print("STEP %d: builder not a LGIC_ENFORCE CONTRACTS name: %r" % b)
    say("PASS-O1-BUILDERS-NAMED" if not bad else "FAIL-O1-BUILDER-UNNAMED", "STEPS: %d  NAMING A CONTRACT: %d  (contract names: %d)" % (len(st), len(st) - len(bad), len(names)))


def o1_unbuilt():
    st = steps()
    if not st:
        return say("FAIL-O1-BUILT-NO-STEPS", "no steps")
    bad = []
    for n, b in st:
        m = re.search(r"^built: (yes|no) (\S+)", b, re.M)
        if not m:
            bad.append((n, "no 'built:' line"))
        elif m.group(1) == "yes" and not os.path.exists(m.group(2).strip("`")):
            bad.append((n, "built: yes but %s does not exist" % m.group(2)))
        elif m.group(1) == "no" and not re.match(r"^`?[A-Z]{2}-[a-z]-\d+(-r\d+)?`?$", m.group(2)):
            bad.append((n, "built: no names no cell id (%s)" % m.group(2)))
    for b in bad:
        print("STEP %d: %s" % b)
    say("PASS-O1-BUILT-STATED" if not bad else "FAIL-O1-BUILT-UNSTATED", "STEPS: %d  BUILT STATE PROVED OR ITS CELL NAMED: %d" % (len(st), len(st) - len(bad)))


def review_marks():
    t = read(REVIEW)
    if t is None:
        return None
    return {int(n): (mark, why) for n, mark, why in re.findall(r"^STEP (\d+): (MECHANICAL|JUDGEMENT) -- (.{8,})$", t, re.M)}


def o2_marks():
    st = steps()
    marks = review_marks()
    if not st or marks is None:
        return say("FAIL-O2-MARKS-ABSENT", "checklist: %s  review: %s" % (bool(st), marks is not None))
    miss = [n for n, _ in st if n not in marks]
    a_rev, a_chk = author_of(REVIEW), author_of(CHECKLIST)
    other = bool(a_rev) and bool(a_chk) and a_rev != a_chk
    for n in miss:
        print("STEP %d: not marked" % n)
    ok = not miss and other
    say("PASS-O2-ALL-MARKED" if ok else "FAIL-O2-MARKS-INCOMPLETE",
        "STEPS: %d  MARKED WITH A REASON: %d  REVIEWER %r IS NOT THE AUTHOR %r: %s" % (len(st), len(st) - len(miss), a_rev, a_chk, other))


def o2_zero():
    st = steps()
    marks = review_marks()
    if not st or not marks:
        return say("FAIL-O2-ZERO-ABSENT", "checklist or review absent")
    judged = [n for n, (mk, _) in marks.items() if mk == "JUDGEMENT"]
    covered = all(n in marks for n, _ in st)
    say("PASS-O2-NO-JUDGEMENT" if covered and not judged else "FAIL-O2-JUDGEMENT-STEP", "STEPS MARKED: %d  MARKED JUDGEMENT: %d %s" % (len(marks), len(judged), judged))


# ---------------------------------------------------------------- the naming exercise (CN-n-1 .. CN-n-3)
def job_ids():
    d = load_json(FIX + "/CN_NAMING_JOB.json") or {}
    return [i["id"] for i in d.get("items", [])]


def naming_rows(cell):
    meta, rows = tsv(NAMING[cell])
    if rows is None:
        return None, None
    return meta, {r[0]: r for r in rows if len(r) >= 2}


def registry_keys(path):
    d = load_json(path) or {}
    keys = set()
    for v in d.values() if isinstance(d, dict) else []:
        if isinstance(v, list):
            keys.update(x.get("key") for x in v if isinstance(x, dict) and x.get("key"))
    return keys


def n_named(cell):
    _, rows = naming_rows(cell)
    ids = job_ids()
    if rows is None or not ids:
        return say("FAIL-N%s-NAMES-ABSENT" % cell.upper(), "answer file or job absent")
    bad = []
    for i in ids:
        r = rows.get(i)
        m = re.match(r"^registry: (infra/logic/registry/\w+\.json)#(\S+)$", r[2]) if r and len(r) >= 3 else None
        if not r or not r[1] or not m or m.group(2) not in registry_keys(m.group(1)):
            bad.append(i)
    for i in bad:
        print("ITEM %s: no name, or no registry row cited that exists" % i)
    say("PASS-N%s-NAMES-CITED" % cell.upper() if not bad else "FAIL-N%s-NAMES-UNCITED" % cell.upper(), "ITEMS: %d  NAMED FROM A CITED REGISTRY ROW: %d" % (len(ids), len(ids) - len(bad)))


def n_base(cell):
    meta, _ = tsv(NAMING[cell])
    base = (meta or {}).get("base")
    ok = commit_ok(base)
    say("PASS-N%s-BASE-STATED" % cell.upper() if ok else "FAIL-N%s-BASE-MISSING" % cell.upper(), "BASE: %s  resolves to a commit: %s" % (base, ok))


def naming_key():
    return (load_json(FIX + "/CN_NAMING_KEY.json") or {}).get("items") or {}


def n3_equal():
    _, a = naming_rows("a")
    _, b = naming_rows("b")
    key = naming_key()
    if a is None or b is None or not key:
        return say("FAIL-N3-EQUAL-ABSENT", "an answer file or the key is absent")
    off = [(i, (a.get(i) or ["", ""])[1], (b.get(i) or ["", ""])[1], k["canonical"]) for i, k in sorted(key.items())
           if (a.get(i) or ["", ""])[1] != k["canonical"] or (b.get(i) or ["", ""])[1] != k["canonical"]]
    for o in off:
        print("OFF THE CANONICAL VALUE: %s  A=%s  B=%s  key=%s" % o)
    say("PASS-N3-BOTH-CANONICAL" if not off else "FAIL-N3-OFF-CANONICAL", "ITEMS: %d  BOTH WORKERS ON THE CANONICAL VALUE: %d" % (len(key), len(key) - len(off)))


def n3_trap():
    _, a = naming_rows("a")
    _, b = naming_rows("b")
    key = naming_key()
    refused = set((load_json(SCHEMA) or {}).get("refused_tokens") or {})
    traps = {i: k for i, k in key.items() if k.get("trap")}
    if a is None or b is None or not traps:
        return say("FAIL-N3-TRAP-ABSENT", "an answer file or the trap item is absent")
    bad = []
    for i, k in traps.items():
        for w, rows in (("A", a), ("B", b)):
            ans = (rows.get(i) or ["", ""])[1]
            toks = set(re.split(r"[-/:.=]", ans))
            if ans != k["canonical"] or toks & refused:
                bad.append((i, w, ans))
    for x in bad:
        print("TRAP NOT CAUGHT: %s by %s: %s" % x)
    say("PASS-N3-TRAP-CAUGHT" if not bad else "FAIL-N3-TRAP-MISSED", "TRAP ITEMS: %d  CAUGHT BY BOTH: %d" % (len(traps), len(traps) - len(set(x[0] for x in bad))))


def n3_sanctioned():
    _, a = naming_rows("a")
    _, b = naming_rows("b")
    key = naming_key()
    t = read(NAMING_COMPARE)
    if a is None or b is None or not key or t is None:
        return say("FAIL-N3-SANCTIONED-ABSENT", "an answer file, the key or %s is absent" % NAMING_COMPARE)
    marks = dict(re.findall(r"^ITEM (\S+): (PASS|FAIL)\b", t, re.M))
    bad = []
    for i, k in key.items():
        both = (a.get(i) or ["", ""])[1] == k["canonical"] and (b.get(i) or ["", ""])[1] == k["canonical"]
        if i not in marks or (both and marks[i] != "PASS"):
            bad.append((i, marks.get(i), both))
    for x in bad:
        print("ITEM %s: marked %s although both answers are the sanctioned form: %s" % x)
    say("PASS-N3-SANCTIONED-KEPT" if not bad else "FAIL-N3-SANCTIONED-COUNTED", "ITEMS: %d  MARKED CORRECTLY: %d" % (len(key), len(key) - len(bad)))


# ---------------------------------------------------------------- the ledger (CN-l-1)
def table_rows(sec):
    """[(header cells, [row cells])] for each markdown table in a section."""
    out, hdr, rows = [], None, []
    for ln in (sec or "").splitlines():
        if ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if hdr is None:
                hdr = [c.strip("* ").lower() for c in cells]
            elif set(ln.replace("|", "").strip()) <= set("-: "):
                continue
            else:
                rows.append(cells)
        elif hdr is not None:
            out.append((hdr, rows))
            hdr, rows = None, []
    if hdr is not None:
        out.append((hdr, rows))
    return out


def recount_output():
    if not os.path.isfile(RECOUNT):
        return None, None
    r = subprocess.run([sys.executable, RECOUNT], capture_output=True, text=True)
    return r.returncode, r.stdout


def l1_recount():
    rc, out = recount_output()
    t = read(LEDGER)
    if rc is None or t is None:
        return say("FAIL-L1-RECOUNT-ABSENT", "%s: %s  ledger: %s" % (RECOUNT, rc is not None, t is not None))
    totals = {k.strip().lower(): int(v) for k, v in re.findall(r"^TOTAL (.+?): (\d+)\s*$", out or "", re.M)}
    sections = re.findall(r"^SECTION .+: \d+ rows \(instrument: .+\)\s*$", out or "", re.M)
    sec = section_by_heading(t, "THE COUNTS")
    compared, diff = 0, []
    for hdr, rows in table_rows(sec):
        for r in rows:
            label = r[0].replace("*", "").strip().lower()
            m = re.match(r"^\**\s*(\d+)\b", r[1]) if len(r) > 1 else None
            if m:
                compared += 1
                if totals.get(label) != int(m.group(1)):
                    diff.append((label, int(m.group(1)), totals.get(label)))
    for d in diff:
        print("COUNT DIFFERS: %s  ledger=%s  script=%s" % d)
    by_hand = "re-derived by hand" in t
    ok = rc == 0 and bool(sections) and compared > 0 and not diff and not by_hand
    say("PASS-L1-RECOUNT-AGREES" if ok else "FAIL-L1-RECOUNT-DISAGREES",
        "script rc: %s  SECTION LINES: %d  COUNT ROWS COMPARED: %d  DIFFERING: %d  'RE-DERIVED BY HAND' STILL PRINTED: %s" % (rc, len(sections), compared, len(diff), by_hand))


def register_rows():
    sec = section_by_heading(read(LEDGER), "EXCEPTION REGISTER")
    for hdr, rows in table_rows(sec):
        if "acknowledged" in hdr:
            return hdr, rows
    return None, None


def l1_deciders():
    hdr, rows = register_rows()
    if hdr is None:
        return say("FAIL-L1-DECIDERS-NO-REGISTER", "the ledger carries no register table with an 'acknowledged' column")
    ai = hdr.index("acknowledged")
    want = {"X2", "X3", "X5"}
    seen, bad = set(), []
    for r in rows:
        xid = r[0].replace("*", "").strip()
        if xid in want:
            seen.add(xid)
            ack = r[ai].replace("*", "").strip() if ai < len(r) else ""
            if ack in ("", "-", "--", "—", "pending") and "decider:" not in "|".join(r):
                bad.append(xid)
    miss = sorted(want - seen)
    for x in bad + miss:
        print("REGISTER ENTRY %s: no decider named" % x)
    ok = not bad and not miss
    say("PASS-L1-DECIDERS-NAMED" if ok else "FAIL-L1-DECIDER-UNNAMED", "ENTRIES X2, X3, X5: %d found  NAMING A DECIDER: %d" % (len(seen), len(seen) - len(bad)))


def l1_conditional():
    hdr, rows = register_rows()
    if hdr is None:
        return say("FAIL-L1-CONDITIONAL-NO-REGISTER", "no register table")
    cond = [r for r in rows if "CONDITIONAL" in "|".join(r)]
    bad = [r[0] for r in cond if not ("condition:" in "|".join(r) and "owner:" in "|".join(r))]
    for x in bad:
        print("CONDITIONAL ENTRY %s: no 'condition:' and 'owner:'" % x)
    ok = bool(cond) and not bad
    say("PASS-L1-CONDITIONS-OWNED" if ok else "FAIL-L1-CONDITION-UNOWNED", "CONDITIONAL ENTRIES: %d  WITH CONDITION AND OWNER: %d" % (len(cond), len(cond) - len(bad)))


def l1_column():
    t = read(LEDGER)
    rc, out = recount_output()
    if t is None or rc is None:
        return say("FAIL-L1-COLUMN-ABSENT", "ledger: %s  recount script: %s" % (t is not None, rc is not None))
    decided = waiting = tables = bad_tables = 0
    bad_cells = []
    for hdr, rows in table_rows(t):
        if "disposition" not in hdr:
            continue
        tables += 1
        if "decided" not in hdr:
            bad_tables += 1
            continue
        di = hdr.index("decided")
        for r in rows:
            v = r[di].replace("*", "").strip() if di < len(r) else ""
            if v == "DECIDED":
                decided += 1
            elif re.match(r"^WAITING \(.+\)$", v):
                waiting += 1
            else:
                bad_cells.append((r[0][:50], v[:30]))
    sd = re.search(r"^DECIDED: (\d+)\s*$", out or "", re.M)
    sw = re.search(r"^WAITING: (\d+)\s*$", out or "", re.M)
    for c in bad_cells[:10]:
        print("DECIDED CELL NOT DECIDED/WAITING (<decider>): %s -> %r" % c)
    ok = (tables > 0 and bad_tables == 0 and not bad_cells and sd is not None and sw is not None
          and int(sd.group(1)) == decided and int(sw.group(1)) == waiting)
    say("PASS-L1-COLUMN-REDERIVED" if ok else "FAIL-L1-COLUMN-MISSING",
        "PLANE TABLES: %d  WITHOUT A 'decided' COLUMN: %d  BAD CELLS: %d  LEDGER DECIDED/WAITING: %d/%d  SCRIPT: %s/%s"
        % (tables, bad_tables, len(bad_cells), decided, waiting, sd.group(1) if sd else None, sw.group(1) if sw else None))


CHECKS = {
    "k1-census": k1_census, "k1-render": k1_render, "k1-stale": k1_stale, "k1-noenum": k1_noenum,
    "k1-s6": k1_s6, "k1-d10": k1_d10, "k1-r1code": k1_r1code,
    "j1-axes": lambda: j_axes("a"), "j1-naming": lambda: j_naming("a"), "j1-base": lambda: j_base("a"),
    "j2-axes": lambda: j_axes("b"), "j2-naming": lambda: j_naming("b"), "j2-base": lambda: j_base("b"),
    "j3-verdicts": j3_verdicts, "j3-citations": j3_citations, "j3-naming-key": j3_naming_key,
    "j3-blind": lambda: blind_pair(JUDGE, "J3"),
    "r1-clauses": r1_clauses, "r1-ticked": r1_ticked, "r2-branches": r2_branches, "r2-bckend": r2_bckend,
    "o1-order": o1_order, "o1-rules": o1_rules, "o1-builders": o1_builders, "o1-unbuilt": o1_unbuilt,
    "o2-marks": o2_marks, "o2-zero": o2_zero,
    "n1-named": lambda: n_named("a"), "n1-base": lambda: n_base("a"),
    "n2-named": lambda: n_named("b"), "n2-base": lambda: n_base("b"),
    "n3-equal": n3_equal, "n3-trap": n3_trap, "n3-sanctioned": n3_sanctioned, "n3-blind": lambda: blind_pair(NAMING, "N3"),
    "l1-recount": l1_recount, "l1-deciders": l1_deciders, "l1-conditional": l1_conditional, "l1-column": l1_column,
}


def selftest_negative():
    passed = []
    for name in sorted(CHECKS):
        out = subprocess.run([sys.executable, __file__, name], capture_output=True, text=True).stdout
        v = [ln for ln in out.splitlines() if ln.startswith("VERDICT: ")]
        verdict = v[-1][9:] if v else "NO-VERDICT"
        print("%-15s %s" % (name, verdict))
        if verdict.startswith("PASS"):
            passed.append(name)
    print("SELFTEST-NEGATIVE: %d of %d subcommands PASS on this tree %s" % (len(passed), len(CHECKS), passed))


def main(argv):
    if len(argv) == 2 and argv[1] == "--list":
        print("\n".join(sorted(CHECKS)))
        return 0
    if not os.path.isdir("org") or not os.path.isdir(".tools"):
        print("run from the worktree root (org/ and .tools/ not found in %s)" % os.getcwd())
        print("VERDICT: FAIL-WRONG-ROOT")
        return 0
    if len(argv) == 2 and argv[1] == "selftest-negative":
        selftest_negative()
        return 0
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: check_canon_r1.py <%s>" % "|".join(sorted(CHECKS)))
        print("VERDICT: FAIL-USAGE")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
