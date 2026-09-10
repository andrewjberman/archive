"""CE-e-1 / E1-AC1 -- THE BATTERY: the vendored POTION model asset renders the SAME BYTES in every tree.

TOKEN: CEE1-MODEL-ASSET-RENDERS-LF -- printed ONLY when EVERY arm holds. rc 0 with the token, rc 1
without it. Every path printed absolute; every list carries its denominator.

THE ARMS, as the task order cuts them:
  (a) THE BASELINE WITH ITS ENVIRONMENT (ruling R-8) -- the manifest's declared hash per model file,
      the MAIN tree's sha256 of the same file, `git check-attr -a`, `git ls-files --eol`, and
      `git config core.autocrlf`, all printed; the manifest's hash equal to the MAIN tree's bytes.
  (b) THE FRESH TREE -- every tracked file under org/modules/graph/potion/model/ sha256-EQUAL to the
      MAIN tree's and to the manifest, denominator printed. FAILS BEFORE the fix, PASSES AFTER; both
      runs printed, from two linked worktrees this script cuts itself.
  (c) THE RANKER IN THAT TREE -- comp-which run BY EXPLICIT PATH from the fresh worktree prints NO
      potion ALARM line and ranks SEMANTICALLY, named by a printed discriminator: the FULL ranked
      candidate ordering beside the LEXICAL ordering of the SAME candidates, and they differ.
  (d) THE NEGATIVE CONTROL -- a second worktree WITHOUT the fix reproduces the ALARM and the lexical
      ranking. A detector that cannot return non-zero on the positive case is a constant.
  (e) THE ROUND-7 READING RE-TAKEN -- P4-AC1's three byte-equality arms (c, f, e:real-byte-equal;
      the four C-S46 regression phrasings + the real-subject question) recomputed at the MAIN tree AND
      in the fresh worktree, denominators printed.
  (f) BOTH WORKTREES REMOVED -- `git worktree list` printed as the proof, branches deleted.

THE TWO REFS THIS SCRIPT CUTS, and why neither is the literal string CLOUD (row
NFRA_COMPEFFICACY-W2-S1): at the time this cell was worked the fix lived on the WORKER BRANCH and
CLOUD was the PRE-FIX ref -- the issuer drains worker branches, so a literal CLOUD cut measures the
tree the fix has not reached. AFTER-ref defaults to the invoking worktree's own branch (which IS
CLOUD once the drain has landed and the CVO re-runs this from the main tree). BEFORE-ref is derived
as the PARENT of the commit that introduced the .gitattributes entry, which is pre-fix BY
CONSTRUCTION and stays pre-fix after the drain -- a negative control pinned to CLOUD would stop
being a negative control the moment the fix reached CLOUD. Both refs, their shas, and whether each
carries the entry are printed.

  python test_cee1_model_asset_rendering.py
  python test_cee1_model_asset_rendering.py --after-ref CLOUD --before-ref <sha>
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
# deliverables/<serial>/ -> deliverables -> NFRA_COMPEFFICACY -> NFRA -> D11 -> missions -> org -> ROOT
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))

MODEL_DIR_REL = "org/modules/graph/potion/model"
MANIFEST_REL = "org/modules/graph/potion/MANIFEST.json"
ATTR_PATTERN = "org/modules/graph/potion/model/**"
TOKEN = "CEE1-MODEL-ASSET-RENDERS-LF"
ALARM_NEEDLE = "ALARM: POTION semantic embedder unavailable"

# The P-4 round-7 deliverable this arm (e) re-takes its reading from. READ, never written.
P4_DELIV_REL = "org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1"

# One real routing question for the ranker arms. Not a gold-id question: the subject gate is a
# different cell's subject (CE-p-4) and must not confound the ranker reading here.
RANK_Q = "what produces canonical_prices.parquet?"

RESULTS = []


def check(name, ok, msg):
    RESULTS.append((name, bool(ok), msg))
    print("  [%s] %-24s %s" % ("PASS" if ok else "FAIL", name, msg))
    return bool(ok)


def hdr(t):
    print("")
    print("-" * 100)
    print(t)
    print("-" * 100)


def run(argv, cwd, timeout=600, env=None):
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)
    return r.returncode, (r.stdout or ""), (r.stderr or "")


def git(args, cwd=None, timeout=600):
    return run(["git"] + list(args), cwd or WS, timeout)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main_worktree():
    """The MAIN tree, DERIVED and never hardcoded: `git worktree list --porcelain` names it first."""
    rc, out, _ = git(["worktree", "list", "--porcelain"])
    if rc != 0:
        return ""
    for ln in out.splitlines():
        if ln.startswith("worktree "):
            return ln.split(" ", 1)[1].strip().replace("\\", "/")
    return ""


def worktree_paths():
    rc, out, _ = git(["worktree", "list", "--porcelain"])
    if rc != 0:
        return []
    return [ln.split(" ", 1)[1].strip().replace("\\", "/")
            for ln in out.splitlines() if ln.startswith("worktree ")]


def tracked_model_files(tree):
    rc, out, err = git(["ls-files", "-z", "--", MODEL_DIR_REL], cwd=tree)
    if rc != 0:
        return []
    return sorted(p for p in out.split("\0") if p.strip())


def manifest_of(tree):
    p = os.path.join(tree, *MANIFEST_REL.split("/"))
    if not os.path.isfile(p):
        return {}, {}, p.replace("\\", "/")
    m = json.load(open(p, encoding="utf-8"))
    return (m.get("model_files_sha256") or {}), (m.get("model_files_bytes") or {}), p.replace("\\", "/")


def hash_model_dir(tree):
    """{basename: (sha256, bytes)} for every TRACKED file under the model dir of `tree`."""
    out = {}
    for rel in tracked_model_files(tree):
        p = os.path.join(tree, *rel.split("/"))
        base = rel.rsplit("/", 1)[-1]
        if os.path.isfile(p):
            out[base] = (sha256_of(p), os.path.getsize(p))
        else:
            out[base] = ("", -1)
    return out


# --------------------------------------------------------------------------------------------
# comp-which, run BY EXPLICIT PATH from the tree we mean (never the ~/bin shim: it is baked to the
# MAIN tree and would run the file we did not change -- row NFRA_COMPEFFICACY-W1-S2, cell CE-e-2).
# --------------------------------------------------------------------------------------------
def comp_which(tree, q):
    cli = os.path.join(tree, ".tools", "comp-which")
    spill_dir = os.path.join(tree, ".comp-graph", "which")
    before = {}
    if os.path.isdir(spill_dir):
        for n in os.listdir(spill_dir):
            try:
                before[n] = os.path.getmtime(os.path.join(spill_dir, n))
            except OSError:
                pass
    rc, out, err = run([sys.executable, cli, q], cwd=tree, timeout=600)
    spill = ""
    want = "question: '" + q.replace("'", "''") + "'"
    best_m = -1.0
    if os.path.isdir(spill_dir):
        for n in os.listdir(spill_dir):
            p = os.path.join(spill_dir, n)
            try:
                m = os.path.getmtime(p)
            except OSError:
                continue
            if n in before and m <= before[n]:
                continue
            try:
                body = open(p, "r", encoding="utf-8").read()
            except OSError:
                continue
            if want in body and m > best_m:
                spill, best_m = body, m
    return {"cli": cli.replace("\\", "/"), "rc": rc, "out": out, "err": err, "spill": spill}


def spill_order(spill_text):
    return re.findall(r"(?m)^\s*tool:\s*'(.*)'\s*$", spill_text or "")


# --------------------------------------------------------------------------------------------
# Arm (e): P4-AC1's three byte-equality arms, recomputed in a named tree against the stored BEFORE.
# cep4_lib is imported FROM THE TREE UNDER TEST, so its own WS (and therefore the comp-which it
# runs and the spill dir it reads) resolve to that tree and not to this one.
# --------------------------------------------------------------------------------------------
def load_cep4_lib(tree, tag):
    p = os.path.join(tree, *P4_DELIV_REL.split("/"), "cep4_lib.py")
    if not os.path.isfile(p):
        return None
    spec = importlib.util.spec_from_file_location("cep4_lib_%s" % tag, p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


def p4_byte_equality(tree, tag, before):
    """Return (arm_c_ok, arm_f_ok, arm_e_ok, per_question_rows) for the tree, printing as it goes."""
    L = load_cep4_lib(tree, tag)
    if L is None:
        print("  BLOCKED: no cep4_lib.py under %s/%s" % (tree, P4_DELIV_REL))
        return None
    print("  cep4_lib WS  : %s" % L.WS.replace("\\", "/"))
    print("  comp-which   : %s" % L.COMP_WHICH.replace("\\", "/"))
    rows = []
    all_equal = True
    for i, q in enumerate(L.PHRASINGS, 1):
        rc_c, out_c, spill_c = L.comp_which(q)
        rows_now = L.ranked_rows(spill_c)
        term_now = L.terminal_routes(out_c)
        b = before["questions"][q]
        d_rows = list(difflib.unified_diff(b["ranked_rows"].splitlines(True),
                                           rows_now.splitlines(True), "BEFORE.rank", "NOW.rank", n=0))
        d_term = list(difflib.unified_diff(b["terminal"].splitlines(True),
                                           term_now.splitlines(True), "BEFORE.term", "NOW.term", n=0))
        eq = (not d_rows) and (not d_term)
        all_equal = all_equal and eq
        print("   [%d of 4] rc=%d (BEFORE %d)  rows %d (BEFORE %d)  ranked-diff %d line(s)  "
              "terminal-diff %d line(s)  ALARM=%s  %s"
              % (i, rc_c, b["rc"], L.rank_row_count(spill_c), b["rank_row_count"],
                 len(d_rows), len(d_term), ALARM_NEEDLE in out_c, q[:46]))
        rows.append((q, rows_now))
    carriers = [q for q in L.PHRASINGS if L.GOLD_ID.search(q)]
    rc_r, out_r, spill_r = L.comp_which(L.REAL_Q)
    b_real = before["questions"][L.REAL_Q]
    rows_real = L.ranked_rows(spill_r)
    d_real = list(difflib.unified_diff(b_real["ranked_rows"].splitlines(True),
                                       rows_real.splitlines(True), "BEFORE.rank", "NOW.rank", n=0))
    print("   [real  ] rc=%d (BEFORE %d)  rows %d (BEFORE %d)  ranked-diff %d line(s)  ALARM=%s  %s"
          % (rc_r, b_real["rc"], L.rank_row_count(spill_r), b_real["rank_row_count"],
             len(d_real), ALARM_NEEDLE in out_r, L.REAL_Q))
    rows.append((L.REAL_Q, rows_real))
    print("   arm c            : %s  (4 of 4 phrasings byte-equal on ranked list AND terminal block)"
          % ("PASS" if all_equal else "FAIL"))
    print("   arm f            : %s  (%d of 4 phrasings carry a gold id; byte-equality %s)"
          % ("PASS" if (not carriers and all_equal) else "FAIL", len(carriers),
             "holds" if all_equal else "does not hold"))
    print("   arm e:real-byte-equal: %s  (1 of 1)" % ("PASS" if not d_real else "FAIL"))
    return (all_equal, (not carriers and all_equal), (not d_real), dict(rows))


def main(argv):
    t_start = time.time()
    args = list(argv)

    def opt(name, default=""):
        return args[args.index(name) + 1] if name in args else default

    print("=" * 100)
    print("CE-e-1 / E1-AC1 -- THE VENDORED POTION MODEL ASSET RENDERS THE SAME IN EVERY TREE")
    print("=" * 100)
    print("  battery      : %s" % os.path.abspath(__file__).replace("\\", "/"))
    print("  invoked in   : %s" % WS.replace("\\", "/"))
    MAIN = main_worktree()
    print("  MAIN tree    : %s   (DERIVED from `git worktree list --porcelain`, never hardcoded)" % MAIN)

    after_ref = opt("--after-ref")
    if not after_ref:
        rc, out, _ = git(["rev-parse", "--abbrev-ref", "HEAD"])
        after_ref = out.strip()
        if rc != 0 or not after_ref or after_ref == "HEAD":
            _, out, _ = git(["rev-parse", "HEAD"])
            after_ref = out.strip()
    _, out, _ = git(["rev-parse", after_ref + "^{commit}"])
    after_sha = out.strip()

    before_ref = opt("--before-ref")
    if not before_ref:
        # the commit that INTRODUCED the entry, then its parent -- pre-fix by construction.
        # `git log -S<string>` -- the PICKAXE. NOT `git rev-list -S`, which this git (2.55.0.windows.2)
        # rejects with rc 129 and a usage block: an unbounded rc there resolved BEFORE to HEAD, i.e.
        # to the FIX commit, and the negative control silently became a second copy of the positive
        # one (measured on this battery's own first run, 2026-09-09). --full-history because a
        # path-simplified log can drop the very commit that introduced a change.
        rc, out, err = git(["log", "-1", "--full-history", "--format=%H", "-S" + ATTR_PATTERN,
                            after_sha, "--", ".gitattributes"])
        if rc != 0:
            print("BLOCKED: the pickaxe that finds the fix commit failed rc=%d: %s"
                  % (rc, err.strip()[:200]))
            return 1
        intro = out.strip()
        before_ref = (intro + "^") if intro else ""
    _, out, _ = git(["rev-parse", (before_ref or "HEAD") + "^{commit}"])
    before_sha = out.strip()

    def carries(sha):
        rc, o, _ = git(["show", "%s:.gitattributes" % sha])
        return rc == 0 and ATTR_PATTERN in o

    print("  AFTER  ref   : %-32s sha %s  carries `%s`: %s"
          % (after_ref, after_sha, ATTR_PATTERN, "YES" if carries(after_sha) else "NO"))
    print("  BEFORE ref   : %-32s sha %s  carries `%s`: %s"
          % (before_ref, before_sha, ATTR_PATTERN, "YES" if carries(before_sha) else "NO"))

    if not after_sha or not before_sha:
        print("BLOCKED: could not resolve both refs.")
        return 1
    # A NEGATIVE CONTROL THAT CARRIES THE FIX IS NOT A NEGATIVE CONTROL, and it reads exactly like a
    # passing arm (b) -- refuse instead of measuring the fix against itself.
    if carries(before_sha) or before_sha == after_sha:
        print("BLOCKED: the BEFORE ref %s (%s) CARRIES `%s` (or equals the AFTER ref). The arm-(b)/(d)"
              " control would be a copy of the positive case." % (before_ref, before_sha, ATTR_PATTERN))
        return 1
    if not carries(after_sha):
        print("BLOCKED: the AFTER ref %s (%s) does NOT carry `%s` -- nothing to accept."
              % (after_ref, after_sha, ATTR_PATTERN))
        return 1

    slot_a = "C:/tmp/cee1-after-%d" % os.getpid()
    slot_b = "C:/tmp/cee1-before-%d" % os.getpid()
    br_a = "cee1-after-%d" % os.getpid()
    br_b = "cee1-before-%d" % os.getpid()
    made = []

    try:
        # ---------------------------------------------------------------- (a) BASELINE + ENVIRONMENT
        hdr("(a) THE BASELINE WITH ITS ENVIRONMENT (ruling R-8) -- read at the MAIN tree")
        _, autocrlf, _ = git(["config", "core.autocrlf"])
        print("  core.autocrlf                     : %s" % (autocrlf.strip() or "(unset)"))
        _, ver, _ = git(["--version"])
        print("  git                               : %s" % ver.strip())
        print("  python                            : %s" % sys.version.split()[0])
        tracked_main = tracked_model_files(MAIN)
        disk_main = sorted(n for n in os.listdir(os.path.join(MAIN, *MODEL_DIR_REL.split("/")))
                           if os.path.isfile(os.path.join(MAIN, *MODEL_DIR_REL.split("/"), n)))
        print("  tracked under %s/ at the MAIN tree : %d of %d present on disk"
              % (MODEL_DIR_REL, len(tracked_main), len(disk_main)))
        rc, eol_main, _ = git(["ls-files", "--eol", "--", MODEL_DIR_REL], cwd=MAIN)
        for ln in eol_main.splitlines():
            print("  ls-files --eol (MAIN)             : %s" % ln.strip())
        rc, attr_main, _ = git(["check-attr", "-a", "--"] + [f for f in tracked_main], cwd=MAIN)
        if attr_main.strip():
            for ln in attr_main.splitlines():
                print("  check-attr -a  (MAIN)             : %s" % ln.strip())
        else:
            print("  check-attr -a  (MAIN)             : (no attributes set -- the pre-fix state; the "
                  "MAIN tree's .gitattributes does not carry the entry until the drain lands)")
        man_sha, man_bytes, man_path = manifest_of(MAIN)
        print("  manifest                          : %s" % man_path)
        main_hashes = hash_model_dir(MAIN)
        print("")
        print("  %-20s %-6s %-64s %s" % ("member", "source", "sha256", "bytes"))
        a_ok = True
        pinned = 0
        for base in sorted(main_hashes):
            got, nb = main_hashes[base]
            want, want_b = man_sha.get(base), man_bytes.get(base)
            print("  %-20s %-6s %-64s %d" % (base, "MAIN", got, nb))
            print("  %-20s %-6s %-64s %s" % ("", "MANIF", want, want_b))
            if want is None:
                print("  %-20s %-6s the manifest pins no hash for this tracked member" % ("", "!!"))
                a_ok = False
                continue
            pinned += 1
            if got != want or (want_b is not None and nb != want_b):
                a_ok = False
        check("a", a_ok and pinned == len(tracked_main) and pinned > 0,
              "the manifest's declared hash equals the MAIN tree's bytes for %d of %d tracked "
              "member(s), and every tracked member is pinned" % (pinned, len(tracked_main)))

        # ------------------------------------------------------------------------ cut both worktrees
        hdr("CUTTING TWO LINKED WORKTREES (both removed in arm (f))")
        for slot, br, sha, label in ((slot_b, br_b, before_sha, "BEFORE (pre-fix)"),
                                     (slot_a, br_a, after_sha, "AFTER  (fix present)")):
            t0 = time.time()
            rc, o, e = git(["worktree", "add", "-b", br, slot, sha], timeout=900)
            print("  %s  git worktree add -b %s %s %s -> rc=%d  %.1fs"
                  % (label, br, slot, sha[:10], rc, time.time() - t0))
            if rc != 0:
                print("  BLOCKED: %s" % e.strip()[-400:])
                return 1
            made.append((slot, br))

        # ------------------------------------------------------------------------------ (b) THE FRESH TREE
        hdr("(b) THE FRESH TREE -- every tracked model file EQUAL to the MAIN tree's and to the manifest")
        b_run = {}
        for slot, label in ((slot_b, "BEFORE"), (slot_a, "AFTER")):
            tr = tracked_model_files(slot)
            dsk = sorted(n for n in os.listdir(os.path.join(slot, *MODEL_DIR_REL.split("/")))
                         if os.path.isfile(os.path.join(slot, *MODEL_DIR_REL.split("/"), n)))
            hh = hash_model_dir(slot)
            m_sha, m_b, m_p = manifest_of(slot)
            rc, eol, _ = git(["ls-files", "--eol", "--", MODEL_DIR_REL], cwd=slot)
            print("")
            print("  %s  %s" % (label, slot))
            print("    census: %d tracked of %d present on disk under %s/" % (len(tr), len(dsk), MODEL_DIR_REL))
            for ln in eol.splitlines():
                print("    ls-files --eol: %s" % ln.strip())
            eq_main = eq_man = 0
            for base in sorted(hh):
                got, nb = hh[base]
                mm, mb = main_hashes.get(base, ("", -1))
                want, want_b = m_sha.get(base), m_b.get(base)
                v_main = (got == mm and nb == mb)
                v_man = (want is not None and got == want and (want_b is None or nb == want_b))
                eq_main += 1 if v_main else 0
                eq_man += 1 if v_man else 0
                print("    %-20s sha256 %s %8d B   == MAIN: %-5s   == MANIFEST: %-5s"
                      % (base, got, nb, v_main, v_man))
            print("    RESULT: %d of %d equal to the MAIN tree; %d of %d equal to the manifest"
                  % (eq_main, len(tr), eq_man, len(tr)))
            b_run[label] = (eq_main, eq_man, len(tr))
        eb, mb_, nb_ = b_run["BEFORE"]
        ea, ma_, na_ = b_run["AFTER"]
        check("b:before-fails", not (eb == nb_ and mb_ == nb_),
              "BEFORE the fix the arm FAILS as it must: %d of %d equal to MAIN, %d of %d equal to the "
              "manifest -- a detector that cannot go non-zero on the positive case is a constant"
              % (eb, nb_, mb_, nb_))
        check("b:after-passes", ea == na_ and ma_ == na_ and na_ > 0,
              "AFTER the fix: %d of %d tracked member(s) equal to the MAIN tree AND %d of %d equal to "
              "the manifest" % (ea, na_, ma_, na_))

        # ------------------------------------------------------- (c) + (d) THE RANKER, AND ITS CONTROL
        hdr("(c) THE RANKER IN THE FRESH TREE, and (d) THE NEGATIVE CONTROL -- comp-which BY EXPLICIT PATH")
        print("  question: %s" % RANK_Q)
        r_after = comp_which(slot_a, RANK_Q)
        r_before = comp_which(slot_b, RANK_Q)
        for lbl, r in (("AFTER ", r_after), ("BEFORE", r_before)):
            print("")
            print("  %s  CLI RUN: %s %s" % (lbl, sys.executable.replace("\\", "/"), r["cli"]))
            print("          cwd=%s  rc=%d  stderr=%d B" % (
                (slot_a if lbl.strip() == "AFTER" else slot_b), r["rc"], len(r["err"])))
            print("          potion ALARM on stderr: %s" % (ALARM_NEEDLE in r["err"]))
            for ln in r["err"].splitlines():
                print("          stderr| %s" % ln)
            for ln in r["out"].splitlines():
                if ln.strip().startswith(("1.", "2.", "3.")) or "MATCHES (top" in ln:
                    print("          stdout| %s" % ln.rstrip())
        ord_a, ord_b = spill_order(r_after["spill"]), spill_order(r_before["spill"])
        same_set = set(ord_a) == set(ord_b)
        npos = min(len(ord_a), len(ord_b))
        ndiff = sum(1 for i in range(npos) if ord_a[i] != ord_b[i])
        print("")
        print("  THE DISCRIMINATOR (printed, not asserted) -- the FULL ranked candidate pool from each")
        print("  tree's own spilled rank file, same question, same candidates:")
        print("    AFTER  (semantic) : %d candidates ranked; top 10 %s" % (len(ord_a), ord_a[:10]))
        print("    BEFORE (lexical)  : %d candidates ranked; top 10 %s" % (len(ord_b), ord_b[:10]))
        print("    candidate SET identical: %s (%d of %d)" % (same_set, len(set(ord_a) & set(ord_b)),
                                                              max(len(set(ord_a)), len(set(ord_b)))))
        print("    ORDER differs at %d of %d positions" % (ndiff, npos))
        check("c:no-alarm", ALARM_NEEDLE not in r_after["err"] and r_after["err"].strip() == "",
              "the fresh fixed tree emits NO potion ALARM (stderr %d B)" % len(r_after["err"]))
        check("c:ranks-semantically", same_set and npos > 0 and ndiff > 0,
              "the same %d candidates are ordered DIFFERENTLY from the lexical fallback at %d of %d "
              "positions -- the ranker is not the fallback" % (npos, ndiff, npos))
        check("d:alarm-reproduced", ALARM_NEEDLE in r_before["err"],
              "the negative control (no fix) reproduces the ALARM line verbatim on stderr")
        check("d:lexical-reproduced", ndiff > 0 and len(ord_b) > 0,
              "the negative control's ranking is the LEXICAL one, %d candidates, differing from the "
              "fixed tree's at %d positions" % (len(ord_b), ndiff))

        # --------------------------------------------------------------- (e) THE ROUND-7 READING RE-TAKEN
        hdr("(e) THE ROUND-7 READING RE-TAKEN -- P4-AC1's three byte-equality arms, MAIN and FRESH")
        bpath = os.path.join(MAIN, *P4_DELIV_REL.split("/"), "cep4_before.json")
        print("  stored baseline: %s" % bpath.replace("\\", "/"))
        if not os.path.isfile(bpath):
            print("  BLOCKED: the stored BEFORE baseline is absent.")
            check("e", False, "the stored baseline P4-AC1 compares against is absent")
        else:
            before_json = json.load(open(bpath, encoding="utf-8"))
            alarms = sum(1 for q, v in before_json["questions"].items()
                         if ALARM_NEEDLE in (v.get("terminal") or ""))
            nq = len(before_json["questions"])
            print("  THE BASELINE'S OWN ENVIRONMENT (R-8), read off the baseline: %d of %d captured "
                  "questions carry the potion ALARM in their `terminal` block" % (alarms, nq))
            print("  -> the stored baseline was captured under the LEXICAL FALLBACK. It names no")
            print("     environment field; the ALARM in its own payload is the only tell.")
            print("")
            print("  MAIN TREE  %s" % MAIN)
            res_main = p4_byte_equality(MAIN, "main", before_json)
            print("")
            print("  FRESH TREE %s" % slot_a)
            res_fresh = p4_byte_equality(slot_a, "fresh", before_json)
            if res_main is None or res_fresh is None:
                check("e", False, "cep4_lib.py unreadable in one of the two trees")
            else:
                cm, fm, em, rows_main = res_main
                cf, ff, ef, rows_fresh = res_fresh
                same = sum(1 for q in rows_main if rows_main[q] == rows_fresh.get(q))
                print("")
                print("  CROSS-TREE: the MAIN tree's ranked lists vs the FRESH tree's, same questions: "
                      "%d of %d BYTE-EQUAL" % (same, len(rows_main)))
                check("e:main", cm and fm and em,
                      "P4-AC1's three byte-equality arms (c, f, e:real-byte-equal) PASS at the MAIN "
                      "tree: c=%s f=%s e=%s (denominator 3 of 3 arms, 5 of 5 questions)"
                      % (cm, fm, em))
                check("e:fresh", cf and ff and ef,
                      "P4-AC1's three byte-equality arms PASS in the FRESH worktree: c=%s f=%s e=%s "
                      "(denominator 3 of 3 arms, 5 of 5 questions)" % (cf, ff, ef))
                check("e:main-equals-fresh", same == len(rows_main) and len(rows_main) > 0,
                      "the FRESH worktree now reads IDENTICALLY to the MAIN tree, %d of %d questions "
                      "-- the checkout-property RED is gone" % (same, len(rows_main)))

    finally:
        # ------------------------------------------------------------------------------ (f) CLEANUP
        hdr("(f) BOTH WORKTREES REMOVED")
        leaked = []
        for slot, br in made:
            rc, _, e = git(["worktree", "remove", "--force", slot])
            print("  git worktree remove --force %s -> rc=%d %s" % (slot, rc, e.strip()[:160]))
            rc2, _, e2 = git(["branch", "-D", br])
            print("  git branch -D %s -> rc=%d %s" % (br, rc2, e2.strip()[:160]))
        git(["worktree", "prune"])
        paths = worktree_paths()
        print("")
        print("  git worktree list --porcelain -- %d worktree(s) now:" % len(paths))
        for p in paths:
            print("    %s" % p)
        for slot, _br in made:
            if any(p.lower() == slot.lower() for p in paths) or os.path.exists(slot):
                leaked.append(slot)
        _, brs, _ = git(["branch", "--list", "cee1-*"])
        print("  git branch --list 'cee1-*' -> %s" % (brs.strip() or "(none)"))
        check("f", not leaked and not brs.strip(),
              "%d of %d worktrees this run cut are removed and their branches deleted; %d leak(s)"
              % (len(made) - len(leaked), len(made), len(leaked)))

    hdr("SUMMARY")
    npass = sum(1 for _n, ok, _m in RESULTS if ok)
    for n, ok, m in RESULTS:
        print("  [%s] %-24s %s" % ("PASS" if ok else "FAIL", n, m))
    print("")
    print("  %d of %d arm(s) PASS   elapsed %.1fs" % (npass, len(RESULTS), time.time() - t_start))
    failed = [n for n, ok, _m in RESULTS if not ok]
    if failed:
        print("  arms failed: %s" % ", ".join(failed))
        print("NOT ENFORCED -- %d arm(s) failed. NO TOKEN." % len(failed))
        return 1
    print(TOKEN)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
