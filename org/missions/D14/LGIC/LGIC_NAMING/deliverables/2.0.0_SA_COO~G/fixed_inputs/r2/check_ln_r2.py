#!/usr/bin/env python3
"""check_ln_r2.py -- the mechanical criteria of LGIC_NAMING round 2 (decomposition v4), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-2 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line `VERDICT: PASS-<X>` or
`VERDICT: FAIL-<X>`, and exits 0. A missing input is a FAIL verdict, never a traceback. No PASS string is a substring
of another subcommand's PASS or FAIL string, because proof-of-spec-check greps <expect> unanchored.
`--list` prints the subcommands; `selftest-negative` runs every one and counts the PASS verdicts.

The four blind cells (e1, e2, e4, l2) are answered by a clean-context seat (blind_seat.py beside this file). Their
criteria read the seat's VERBATIM reply (seats/<cell>.answer.txt, hashed in the seat record) and re-derive the prompt
with blind_seat.build(), so neither the prompt nor an answer can be shaped by the worker who ran the seat.
"""
import fnmatch
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = "org/missions/D14/LGIC/LGIC_NAMING"
EX = BASE + "/deliverables/exercises"
EXR2 = EX + "/r2"
SEATS = EXR2 + "/seats"
FIX = BASE + "/deliverables/2.0.0_SA_COO~G/fixed_inputs"
R2 = FIX + "/r2"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
FIRMS = ("49financial", "inflection", "cottonwood", "demo")
ALIAS_TOKENS = ("bd", "49f", "49financial", "inf", "inflection", "cot", "cottonwood", "demo")
LEAKS = ("3.6.7", "7801")
STEP_RE = re.compile(r"^[A-Z][A-Z0-9]*(\.[A-Za-z0-9]+)*$")


def say(verdict, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + verdict)


def read(path, exact=False):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace", newline="" if exact else None) as fh:
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
    """(meta, rows): '# base <sha>' and '# seat <id>' header lines, then tab-separated rows; (None, None) when absent."""
    t = read(path)
    if t is None:
        return None, None
    meta, rows = {}, []
    for ln in t.splitlines():
        s = ln.strip()
        if not s:
            continue
        m = re.match(r"#\s*(base|seat)\s+(\S+)", s)
        if m:
            meta[m.group(1)] = m.group(2)
            continue
        if s.startswith("#"):
            continue
        rows.append([c.strip() for c in ln.split("\t")])
    return meta, rows


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def seat_module():
    spec = importlib.util.spec_from_file_location("blind_seat", R2 + "/blind_seat.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ANSWER_FILE = {"e1": EXR2 + "/n3-namer-a.tsv", "e2": EXR2 + "/n3-namer-b.tsv",
               "e4": EXR2 + "/n3-reader.tsv", "l2": EXR2 + "/n5-reader.tsv"}


def seat_parts(cell):
    return (load_json(SEATS + "/%s.seat.json" % cell), read(SEATS + "/%s.prompt.txt" % cell, exact=True),
            read(SEATS + "/%s.answer.txt" % cell, exact=True), load_json(SEATS + "/%s.raw.json" % cell))


# ---------------------------------------------------------------- the clean seat (e1, e2, e4, l2)
def seat_clean(cell):
    rec, prompt, answer, raw = seat_parts(cell)
    if not isinstance(rec, dict):
        return say("FAIL-NO-SEAT-RECORD", "SEAT RECORD %s/%s.seat.json: absent or unparseable" % (SEATS, cell))
    argv = rec.get("argv") or []
    try:
        want = seat_module().build(cell, rec.get("base"))
    except (SystemExit, Exception) as exc:  # noqa: BLE001
        want, why = None, str(exc)
    else:
        why = ""
    meta, rows = tsv(ANSWER_FILE[cell])
    parsed = seat_module().parse(answer)[1] if isinstance(answer, str) else None
    checks = [
        ("the seat folder is outside the workspace", rec.get("seat_dir_inside_workspace") is False),
        ("the seat folder is in no git repository", rec.get("seat_dir_in_a_git_repo") is False),
        ("the seat folder held no file at launch", rec.get("files_in_seat_dir_before") == 0),
        ("no CLAUDE.md up the folder's parent chain", rec.get("claude_md_in_parent_chain") == []),
        ("the seat ran with no tools", "--tools" in argv and argv.index("--tools") + 1 < len(argv) and argv[argv.index("--tools") + 1] == ""),
        ("the seat exited 0 without error", rec.get("rc") == 0 and rec.get("is_error") is False),
        ("the prompt is the builder's, at the recorded base", prompt is not None and want is not None and prompt == want
         and sha(prompt) == rec.get("prompt_sha256")),
        ("the reply file is the session's reply, verbatim", isinstance(raw, dict) and isinstance(answer, str)
         and raw.get("result") == answer and sha(answer) == rec.get("result_sha256")),
        ("the answer file is the reply, parsed", rows is not None and parsed is not None and rows == parsed),
        ("the answer file carries the seat's base and session", meta is not None and meta.get("base") == rec.get("base")
         and meta.get("seat") == str(rec.get("session_id"))),
    ]
    for label, ok in checks:
        print("%s  %s" % ("OK  " if ok else "NOT ", label))
    if why:
        print("BUILDER: %s" % why)
    bad = [label for label, ok in checks if not ok]
    say("PASS-CLEAN-SEAT" if not bad else "FAIL-SEAT-NOT-PROVED",
        "SEAT CONDITIONS: %d  HELD: %d  NOT HELD: %s" % (len(checks), len(checks) - len(bad), bad))


def canary(cell):
    rec, _, answer, _ = seat_parts(cell)
    if not isinstance(answer, str) or not isinstance(rec, dict) or sha(answer) != rec.get("result_sha256"):
        return say("FAIL-NO-CANARY", "REPLY %s/%s.answer.txt: absent, or not the reply the seat record hashes" % (SEATS, cell))
    q = seat_module().parse(answer)[0]
    leaked = [m for m in LEAKS if m in answer]
    print("Q1: %r  Q2: %r" % (q.get("Q1"), q.get("Q2")))
    if leaked:
        return say("FAIL-CANARY-LEAK", "FACTS STATED ONLY IN THE WORKSPACE CONTEXT FOUND IN THE REPLY: %s of %d" % (leaked, len(LEAKS)))
    ok = "Q1" in q and "Q2" in q
    say("PASS-CANARY-BLIND" if ok else "FAIL-NO-CANARY",
        "CANARY ANSWERS: %d of 2  WORKSPACE-ONLY FACTS IN THE REPLY: 0 of %d" % (len(q), len(LEAKS)))


# ---------------------------------------------------------------- LN-e-1 .. LN-e-5
def items():
    d = load_json(FIX + "/N3_ITEMS.json") or {}
    k = load_json(R2 + "/N3_KEY_R2.json") or {}
    return d.get("items", []), k.get("key", {})


def namer_named(cell):
    its, _ = items()
    _, rows = tsv(ANSWER_FILE[cell])
    got = {r[0]: r[1] for r in (rows or []) if len(r) >= 2 and r[1]}
    miss = [i["id"] for i in its if i["id"] not in got]
    say("PASS-ALL-NAMED" if its and rows is not None and not miss else "FAIL-UNNAMED",
        "ITEMS: %d  NAMED (a RAISE is an answer): %d  MISSING: %s" % (len(its), len(its) - len(miss), miss))


def briefed_v16(cell):
    meta, _ = tsv(ANSWER_FILE[cell])
    base = (meta or {}).get("base")
    ver = None
    if base:
        r = subprocess.run(["git", "show", "%s:%s" % (base, SCHEMA)], capture_output=True)
        if r.returncode == 0:
            try:
                ver = json.loads(r.stdout.decode("utf-8")).get("version")
            except ValueError:
                ver = None
    say("PASS-BRIEFED-ON-V16" if ver == "v1.6" else "FAIL-NOT-BRIEFED-ON-V16", "BASE: %s  NAMING_SCHEMA.json version there: %s" % (base, ver))


def e3_identical():
    its, _ = items()
    _, a = tsv(ANSWER_FILE["e1"])
    _, b = tsv(ANSWER_FILE["e2"])
    if a is None or b is None:
        return say("FAIL-ANSWERS-ABSENT", "namer A file: %s  namer B file: %s" % (a is not None, b is not None))
    ma = {r[0]: r[1] for r in a if len(r) >= 2}
    mb = {r[0]: r[1] for r in b if len(r) >= 2}
    diff = [(i["id"], ma.get(i["id"]), mb.get(i["id"])) for i in its if ma.get(i["id"]) != mb.get(i["id"])]
    for d in diff:
        print("DIFFERS: %s  A=%s  B=%s" % d)
    say("PASS-IDENTICAL" if its and not diff else "FAIL-DIFFERENT",
        "ITEMS: %d  IDENTICAL: %d  DIFFERENT: %d" % (len(its), len(its) - len(diff), len(diff)))


def e3_blind():
    ra, pa, _, _ = seat_parts("e1")
    rb, pb, _, _ = seat_parts("e2")
    ok = (isinstance(ra, dict) and isinstance(rb, dict) and pa is not None and pb is not None
          and sha(pa) == ra.get("prompt_sha256") and sha(pb) == rb.get("prompt_sha256")
          and ra.get("prompt_sha256") == rb.get("prompt_sha256")
          and ra.get("session_id") and rb.get("session_id") and ra.get("session_id") != rb.get("session_id")
          and ra.get("seat_dir") != rb.get("seat_dir"))
    say("PASS-NAMERS-UNCONFERRED" if ok else "FAIL-NAMERS-NOT-SEPARATED",
        "PROMPT A sha: %s  PROMPT B sha: %s  (identical input: neither seat was given anything but the briefing)"
        % ((ra or {}).get("prompt_sha256"), (rb or {}).get("prompt_sha256")),
        "SESSION A: %s  SESSION B: %s" % ((ra or {}).get("session_id"), (rb or {}).get("session_id")))


def reader_names():
    _, a = tsv(ANSWER_FILE["e1"])
    return sorted(set(x[1] for x in (a or []) if len(x) >= 2 and x[1] and x[1] != "RAISE"))


def e4_marked():
    names = reader_names()
    _, r = tsv(ANSWER_FILE["e4"])
    marks = {x[0]: x[1] for x in (r or []) if len(x) >= 2 and x[1]}
    miss = [n for n in names if n not in marks]
    say("PASS-ALL-MARKED" if names and r is not None and not miss else "FAIL-UNMARKED",
        "NAMES: %d  MARKED: %d  MISSING: %d %s" % (len(names), len(names) - len(miss), len(miss), miss[:5]))


def e5_correct():
    its, key = items()
    _, a = tsv(ANSWER_FILE["e1"])
    _, r = tsv(ANSWER_FILE["e4"])
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
    say("PASS-ALL-CORRECT" if its and key and a and r and not wrong else "FAIL-MISREAD",
        "ITEMS: %d  CORRECT: %d  WRONG: %d (key: N3_KEY_R2.json, firm or none)" % (len(its), len(its) - len(wrong), len(wrong)))


def e5_consistent():
    """RULING R: a clash is ONE token read as two referents -- marked as the firm in one name, and read as something
    else (none, or another token) in another name that carries it as a whole segment."""
    _, r = tsv(ANSWER_FILE["e4"])
    rows = [x for x in (r or []) if len(x) >= 2]
    marked = set(x[1] for x in rows if x[1] != "none")
    clash = []
    for name, m in ((x[0], x[1]) for x in rows):
        toks = set(re.split(r"[-/=.]", name))
        for t in marked:
            if t in toks and m != t:
                clash.append((name, t, m))
    say("PASS-ONE-REFERENT-EACH" if rows and not clash else "FAIL-TWO-REFERENTS",
        "NAMES: %d  TOKENS MARKED AS A FIRM: %d  A MARKED TOKEN READ AS ANOTHER REFERENT ELSEWHERE: %d %s"
        % (len(rows), len(marked), len(clash), clash[:5]))


# ---------------------------------------------------------------- LN-f-1 (round 2: the RAISE disposition)
def f1_data():
    d = fenced_json(EXR2 + "/n4-firm-patterns.md")
    return d if isinstance(d, dict) else {}


def f1_one():
    pats = f1_data().get("patterns")
    ok = isinstance(pats, dict) and sorted(pats) == sorted(FIRMS) and all(isinstance(v, str) and v for v in pats.values())
    say("PASS-ONE-EACH" if ok else "FAIL-NOT-ONE-EACH", "PATTERNS: %s" % (pats,))


def f1_catch():
    d = f1_data()
    pats, att = d.get("patterns") or {}, d.get("attributed") or {}
    total, missed = 0, []
    for f in FIRMS:
        for a in att.get(f, []):
            total += 1
            if not fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, "")):
                missed.append((f, a.get("canonical")))
    say("PASS-CATCHES-ALL" if pats and total and not missed else "FAIL-MISSES",
        "ATTRIBUTED CANONICAL FORMS: %d  CAUGHT BY OWN FIRM'S PATTERN: %d  MISSED: %s" % (total, total - len(missed), missed[:5]))


def f1_cross():
    d = f1_data()
    pats, att = d.get("patterns") or {}, d.get("attributed") or {}
    cross = []
    for f in FIRMS:
        for g in FIRMS:
            if g == f:
                continue
            for a in att.get(g, []):
                if fnmatch.fnmatchcase(a.get("canonical", ""), pats.get(f, "")):
                    cross.append((f, g, a.get("canonical")))
    say("PASS-NO-CROSS" if pats and att and not cross else "FAIL-CROSSES", "CROSS-FIRM CATCHES: %d %s" % (len(cross), cross[:5]))


def f1_covered():
    d = f1_data()
    att, exc, rai = d.get("attributed") or {}, d.get("excluded") or [], d.get("raise") or []
    live = (load_json(FIX + "/LIVE_NAMES.json") or {}).get("by_type", {}).get("IAM_ROLE", [])
    want = [n for n in live if set(re.split(r"[-_]", n.lower())) & set(ALIAS_TOKENS)]
    seen = set(a.get("name") for f in FIRMS for a in att.get(f, []))
    seen |= set(e.get("name") for e in exc if isinstance(e, dict) and e.get("reason"))
    seen |= set(x.get("name") for x in rai if isinstance(x, dict) and x.get("step"))
    miss = [n for n in want if n not in seen]
    say("PASS-COVERED" if want and d and not miss else "FAIL-UNCOVERED",
        "LIVE IAM_ROLE NAMES CARRYING A FIRM ALIAS TOKEN: %d of %d roles  ATTRIBUTED, EXCLUDED WITH A REASON, OR RAISED "
        "WITH A STEP: %d  MISSING: %s" % (len(want), len(live), len(want) - len(miss), miss[:5]))


def f1_raise():
    """Row LGIC_NAMING-W1-S5, option (b): the shape gains a RAISE disposition beside attributed and excluded."""
    d = f1_data()
    rai, exc = d.get("raise"), d.get("excluded") or []
    if not isinstance(rai, list):
        return say("FAIL-NO-RAISE-DISPOSITION", "the json block carries no 'raise' list (present: %s)" % sorted(d))
    bad = [x for x in rai if not (isinstance(x, dict) and x.get("name") and isinstance(x.get("step"), str)
                                  and STEP_RE.match(x.get("step")) and x.get("why"))]
    misfiled = [e.get("name") for e in exc if isinstance(e, dict) and "raise" in str(e.get("reason", "")).lower()]
    ok = not bad and not misfiled
    say("PASS-RAISE-DISPOSED" if ok else "FAIL-RAISE-MISFILED",
        "RAISE ENTRIES: %d  WITHOUT NAME, STEP (for example R1.f) OR WHY: %d %s" % (len(rai), len(bad), bad[:3]),
        "EXCLUDED ENTRIES WHOSE REASON IS A RAISE: %d %s" % (len(misfiled), misfiled[:3]))


# ---------------------------------------------------------------- LN-l-2 .. LN-l-3
def addresses():
    return (load_json(FIX + "/N5_ADDRESSES.json") or {}).get("addresses", [])


def l2_labeled():
    ads = addresses()
    _, r = tsv(ANSWER_FILE["l2"])
    got = {x[0]: x[1] for x in (r or []) if len(x) >= 2 and x[1]}
    miss = [a["id"] for a in ads if a["id"] not in got]
    say("PASS-ALL-LABELED" if ads and r is not None and not miss else "FAIL-UNLABELED",
        "ADDRESSES: %d  LABELED: %d  MISSING: %s" % (len(ads), len(ads) - len(miss), miss))


def l3_key():
    return (load_json(FIX + "/N5_KEY.json") or {}).get("key", {})


def l3_correct():
    key = l3_key()
    _, r = tsv(ANSWER_FILE["l2"])
    got = {x[0]: x[1].replace(" ", "") for x in (r or []) if len(x) >= 2}
    wrong = [(k, got.get(k), v) for k, v in key.items() if v != "DOES-NOT-FIT" and got.get(k) != v]
    for w in wrong:
        print("WRONG: %s  labeled=%s  expected=%s" % w)
    n = len([v for v in key.values() if v != "DOES-NOT-FIT"])
    say("PASS-ALL-READ-RIGHT" if key and r is not None and not wrong else "FAIL-MISREAD-LAYOUT",
        "CONFORMING ADDRESSES: %d  CORRECT: %d  WRONG: %d" % (n, n - len(wrong), len(wrong)))


def l3_control():
    key = l3_key()
    _, r = tsv(ANSWER_FILE["l2"])
    got = {x[0]: x[1].strip() for x in (r or []) if len(x) >= 2}
    ctl = [k for k, v in key.items() if v == "DOES-NOT-FIT"]
    ok = ctl and r is not None and all(got.get(k) == "DOES-NOT-FIT" for k in ctl)
    say("PASS-CONTROL-FLAGGED" if ok else "FAIL-CONTROL-MISSED",
        "NEGATIVE CONTROLS: %d  MARKED DOES-NOT-FIT: %d" % (len(ctl), sum(1 for k in ctl if got.get(k) == "DOES-NOT-FIT")))


CHECKS = {
    "e1-seat": lambda: seat_clean("e1"), "e1-canary": lambda: canary("e1"),
    "e1-named": lambda: namer_named("e1"), "e1-v16": lambda: briefed_v16("e1"),
    "e2-seat": lambda: seat_clean("e2"), "e2-canary": lambda: canary("e2"),
    "e2-named": lambda: namer_named("e2"), "e2-v16": lambda: briefed_v16("e2"),
    "e3-identical": e3_identical, "e3-blind": e3_blind,
    "e4-seat": lambda: seat_clean("e4"), "e4-canary": lambda: canary("e4"), "e4-marked": e4_marked,
    "e5-correct": e5_correct, "e5-consistent": e5_consistent,
    "f1-one": f1_one, "f1-catch": f1_catch, "f1-cross": f1_cross, "f1-covered": f1_covered, "f1-raise": f1_raise,
    "l2-seat": lambda: seat_clean("l2"), "l2-canary": lambda: canary("l2"), "l2-labeled": l2_labeled,
    "l3-correct": l3_correct, "l3-control": l3_control,
}


def selftest_negative():
    passed = []
    for name in sorted(CHECKS):
        out = subprocess.run([sys.executable, __file__, name], capture_output=True, text=True).stdout
        v = [ln for ln in out.splitlines() if ln.startswith("VERDICT: ")]
        verdict = v[-1][9:] if v else "NO-VERDICT"
        print("%-14s %s" % (name, verdict))
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
        print("usage: check_ln_r2.py <%s>" % "|".join(sorted(CHECKS)))
        print("VERDICT: FAIL-USAGE")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
