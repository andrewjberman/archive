#!/usr/bin/env python3
"""check_ln_r3.py -- the mechanical criteria of LGIC_NAMING round 3 (decomposition v5 s.0d), one subcommand per criterion.

Issued by 2.0.0_SA_COO~G with the round-3 issuance. Run from the worktree root: `python <this file> <subcommand>`.
Every subcommand prints its evidence, a denominator where one exists, and exactly one line `VERDICT: PASS-<X>` or
`VERDICT: FAIL-<X>`, and exits 0. A missing input is a FAIL verdict, never a traceback. No PASS string is a substring
of another subcommand's PASS or FAIL string, because proof-of-spec-check greps <expect> unanchored.
`--list` prints the subcommands; `selftest-negative` runs every one and counts the PASS verdicts.

The three blind cells (e1, e2, e4) are answered by a clean-context seat (blind_seat.py beside this file). Their
criteria read the seat's VERBATIM reply (seats/<cell>.answer.txt, hashed in the seat record) and re-derive the prompt
with blind_seat.build(), so neither the prompt nor an answer can be shaped by the worker who ran the seat.
The key is round 2's, unchanged (round-2 analysis s.5 item 2): fixed_inputs/r2/N3_KEY_R2.json.
"""
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

BASE = "org/missions/D14/LGIC/LGIC_NAMING"
EX = BASE + "/deliverables/exercises"
EXR3 = EX + "/r3"
SEATS = EXR3 + "/seats"
FIX = BASE + "/deliverables/2.0.0_SA_COO~G/fixed_inputs"
R2 = FIX + "/r2"
R3 = FIX + "/r3"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
RULE = BASE + "/deliverables/GRADING_RULE.md"
RECORD = EX + "/r2/n4-firm-patterns.md"
LEAKS = ("3.6.7", "7801")
COUNT_RE = re.compile(r"^FORMS CHANGED BY THE v1\.7 STEPS: (\d+) of (\d+)\s*$", re.M)


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
    spec = importlib.util.spec_from_file_location("blind_seat_r3", R3 + "/blind_seat.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ANSWER_FILE = {"e1": EXR3 + "/n3-namer-a.tsv", "e2": EXR3 + "/n3-namer-b.tsv", "e4": EXR3 + "/n3-reader.tsv"}


def seat_parts(cell):
    return (load_json(SEATS + "/%s.seat.json" % cell), read(SEATS + "/%s.prompt.txt" % cell, exact=True),
            read(SEATS + "/%s.answer.txt" % cell, exact=True), load_json(SEATS + "/%s.raw.json" % cell))


# ---------------------------------------------------------------- the clean seat (e1, e2, e4)
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


def briefed_v17(cell):
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
    say("PASS-BRIEFED-ON-V17" if ver == "v1.7" else "FAIL-NOT-BRIEFED-ON-V17", "BASE: %s  NAMING_SCHEMA.json version there: %s" % (base, ver))


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
        "ITEMS: %d  CORRECT: %d  WRONG: %d (key: r2/N3_KEY_R2.json, unchanged, firm or none)" % (len(its), len(its) - len(wrong), len(wrong)))


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


# ---------------------------------------------------------------- LN-g-1 (round 3: the rule re-cut to v1.7)
def v17_changes():
    """Round 2's attributed canonical forms re-graded by the two mechanical v1.7 steps (round-2 analysis s.2):
    FN1b drops a function token already written in the system or scope slot; the own-kind bar drops the resource's OWN
    kind (kind.by_type for its type) from the function. Returns (forms, changed) or (None, reason)."""
    d = fenced_json(RECORD)
    s = load_json(SCHEMA)
    if not isinstance(d, dict) or not isinstance(s, dict):
        return None, "record %s or schema %s unreadable" % (RECORD, SCHEMA)
    scopes = set(f["short"] for f in s.get("firm_forms", [])) | {s.get("global_scope", {}).get("short", "global")}
    own = [k.lower() for k in (s.get("kind", {}).get("by_type", {}).get("IAM_ROLE") or [])]
    forms = [a.get("canonical", "") for v in (d.get("attributed") or {}).values() for a in v]
    changed = []
    for c in forms:
        tk = c.split("-")
        if len(tk) < 3:
            continue
        sc = tk[1] if tk[1] in scopes else None
        fn = tk[(2 if sc else 1):-1]
        dropped = [x for x in fn if x == tk[0] or (sc and x == sc) or x in own]
        if dropped:
            changed.append((c, dropped))
    return forms, changed


def g1_count():
    t = read(RULE)
    forms, changed = v17_changes()
    if forms is None:
        return say("FAIL-NO-RECOUNT", "RECOUNT: %s" % changed)
    for c, dropped in changed:
        print("CHANGES: %s  drops %s" % (c, dropped))
    m = COUNT_RE.search(t or "")
    print("RECOUNT BY THIS CHECKER: %d of %d  (own kind of IAM_ROLE from %s; record %s)" % (len(changed), len(forms), SCHEMA, RECORD))
    if not m:
        return say("FAIL-NO-COUNT-LINE", "GRADING_RULE.md carries no line 'FORMS CHANGED BY THE v1.7 STEPS: <n> of <d>'")
    n, d = int(m.group(1)), int(m.group(2))
    ok = forms and n == len(changed) and d == len(forms)
    say("PASS-COUNT-RECOMPUTED" if ok else "FAIL-COUNT-DIFFERS",
        "PRINTED BY THE RULE: %d of %d  RECOUNTED: %d of %d" % (n, d, len(changed), len(forms)))


def g1_version():
    t = read(RULE) or ""
    head = "\n".join(t.splitlines()[:40])
    ok = "NAMING_SCHEMA.json v1.7" in head
    say("PASS-GRADES-V17" if ok else "FAIL-NOT-GRADING-V17",
        "GRADING_RULE.md's first 40 lines name 'NAMING_SCHEMA.json v1.7': %s" % ok)


CHECKS = {
    "e1-seat": lambda: seat_clean("e1"), "e1-canary": lambda: canary("e1"),
    "e1-named": lambda: namer_named("e1"), "e1-v17": lambda: briefed_v17("e1"),
    "e2-seat": lambda: seat_clean("e2"), "e2-canary": lambda: canary("e2"),
    "e2-named": lambda: namer_named("e2"), "e2-v17": lambda: briefed_v17("e2"),
    "e3-identical": e3_identical, "e3-blind": e3_blind,
    "e4-seat": lambda: seat_clean("e4"), "e4-canary": lambda: canary("e4"), "e4-marked": e4_marked,
    "e5-correct": e5_correct, "e5-consistent": e5_consistent,
    "g1-count": g1_count, "g1-version": g1_version,
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
        print("usage: check_ln_r3.py <%s>" % "|".join(sorted(CHECKS)))
        print("VERDICT: FAIL-USAGE")
        return 0
    CHECKS[argv[1]]()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
