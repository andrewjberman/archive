#!/usr/bin/env python3
"""check_en_r3 -- LGIC_ENFORCE round 3's checker. The ISSUER's fixed input; workers never edit it.

Round 3's cells call these subcommands as their criteria's invocations. Each prints ONE verdict
token on its last line so a criterion's <expect> is an anchored, unambiguous match.

CELL 4 (the placement, R-12 / R-2 / A-9, ruled a WORKER cell by R-23 @2a2d10acd8) is graded
against PLACEMENT_MAP.json -- a FIXED INPUT written by the issuer at the cut. That separation is
the point: the cell is graded on a map it cannot edit, so "every file went to its first minting
author's folder" is checked against the authorship measured BEFORE the move, not against whatever
the tree looks like afterwards. After a git mv, `git log --diff-filter=A` on the NEW path can
resolve differently, so recomputing the map at grade time would grade the cell's own act.

USAGE: check_en_r3.py <subcommand> | --list | selftest-arms
Exit 0 on PASS, 1 on FAIL, 2 on usage/read error.
"""
import json
import os
import re
import shutil as _shutil
import subprocess
import sys
import tempfile as _tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# r3 -> fixed_inputs -> 2.0.0_SA_COO~G -> deliverables -> LGIC_ENFORCE -> LGIC -> D14 -> missions -> org -> repo
# NINE steps, not eight. The self-test cannot catch this: every arm passes an explicit cwd
# fixture and never reads REPO, so a wrong REPO is invisible to a green selftest. Exercised
# below by running a subcommand with NO cwd against the real tree.
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
DELIV = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables"
MAP = os.path.join(HERE, "PLACEMENT_MAP.json")

# A REAL CSI sequence. The chr(27) is written as a CALL, not a literal ESC byte, so this line
# survives being read through a terminal -- a raw ESC renders invisibly and the one character
# that decides the pattern is the one a reader cannot see (measured 2026-09-16 on S55).
_CSI = re.compile(chr(27) + r"\[[0-9;]*[A-Za-z]")


def say(*parts):
    print(" ".join(str(p) for p in parts))


def git(args, cwd=None):
    r = subprocess.run(["git"] + args, capture_output=True, text=True, cwd=cwd or REPO)
    return r.returncode, r.stdout


def load_map(path=None):
    with open(path or MAP, encoding="utf-8") as fh:
        return json.load(fh)


def tree_blobs(cwd=None):
    """The files sitting DIRECTLY under deliverables/ with no serial subfolder, BY OBJECT TYPE.

    `git ls-tree --name-only` does not mark trees, so a name-only read counts the nine serial
    FOLDERS as files (an early count of this population read 26 for exactly that reason). Read the
    type column instead.
    """
    rc, out = git(["ls-tree", "HEAD", DELIV + "/"], cwd=cwd)
    if rc != 0:
        return None
    blobs = []
    for line in out.splitlines():
        if not line.strip():
            continue
        head, _, name = line.partition("\t")
        cols = head.split()
        if len(cols) >= 2 and cols[1] == "blob":
            blobs.append(name.strip())
    return blobs


# ---------------------------------------------------------------- cell 4 arms

def p4_population(cwd=None, mapdoc=None):
    """The ownerless population is EMPTY, against the denominator the cut printed."""
    m = mapdoc or load_map()
    expected = m["denominator_blobs"]
    blobs = tree_blobs(cwd)
    if blobs is None:
        say("FAIL-P4-POPULATION-UNREADABLE (git ls-tree failed)")
        return 1
    say("DENOMINATOR: %d ownerless blob(s) at the cut; %d remain now; trees excluded by type, not by name"
        % (expected, len(blobs)))
    if blobs:
        for b in sorted(blobs)[:20]:
            say("   STILL OWNERLESS:", b.split("/")[-1])
        say("FAIL-P4-POPULATION-NONEMPTY")
        return 1
    say("PASS-P4-POPULATION-EMPTY")
    return 0


def p4_destinations(cwd=None, mapdoc=None):
    """Every mapped file exists at its first-minting author's folder, and nowhere else."""
    m = mapdoc or load_map()
    root = cwd or REPO
    missing, found = [], 0
    for row in m["rows"]:
        dest = row["destination"]
        if os.path.exists(os.path.join(root, dest.replace("/", os.sep))):
            found += 1
        else:
            missing.append((row["basename"], row["first_minting_author"]))
    say("DENOMINATOR: %d mapped file(s); %d present at their mapped destination; %d missing"
        % (len(m["rows"]), found, len(missing)))
    for b, a in missing[:20]:
        say("   MISSING:", b, "-> expected under", a)
    if missing:
        say("FAIL-P4-DESTINATION-MISSING")
        return 1
    say("PASS-P4-DESTINATIONS-ALL-PLACED")
    return 0


def p4_citations(cwd=None, mapdoc=None):
    """No TRACKED file still cites a moved file at its OLD flat path.

    Walks the tracked set rather than shelling to a recursive search, so the denominator is the
    tracked file count and the read cannot be a silent rail no-op.
    """
    m = mapdoc or load_map()
    root = cwd or REPO
    rc, out = git(["ls-files"], cwd=root)
    if rc != 0:
        say("FAIL-P4-CITATIONS-UNREADABLE")
        return 1
    files = [f for f in out.splitlines() if f.strip()]
    olds = {row["source"]: row["basename"] for row in m["rows"]}
    # the map file itself and this checker RECORD the old paths by design
    exempt = {
        DELIV + "/2.0.0_SA_COO~G/fixed_inputs/r3/PLACEMENT_MAP.json",
        DELIV + "/2.0.0_SA_COO~G/fixed_inputs/r3/check_en_r3.py",
    }
    hits = []
    for f in files:
        if f in exempt:
            continue
        p = os.path.join(root, f.replace("/", os.sep))
        try:
            with open(p, encoding="utf-8", errors="replace") as fh:
                t = fh.read()
        except (OSError, IOError):
            continue
        for old in olds:
            if old in t:
                hits.append((f, olds[old]))
    say("DENOMINATOR: %d tracked file(s) scanned, %d old path(s) searched, %d exempt (the map and this checker)"
        % (len(files), len(olds), len(exempt)))
    for f, b in hits[:20]:
        say("   DANGLING:", f, "cites", b, "at its old flat path")
    if hits:
        say("FAIL-P4-CITATION-DANGLING")
        return 1
    say("PASS-P4-CITATIONS-REPOINTED")
    return 0


# ---------------------------------------------------------------- cell 2 arms
#
# The gate's DOMAIN (R-11/R-13, R-15, A-6, A-7, A-8, S42, S45). These arms name the CONTRACT the
# cell must build, and every one of them reads RED against .tools/naming-gate.py at the cut --
# the gate prints no denominator, no declaration-tree record and no coverage line today. That is
# the state a criterion must be in before its cell runs (W2-S11): a criterion that already passes
# is not evidence the cell did anything.
#
# The contract is deliberately about PRINTED, CHECKABLE FACTS rather than an implementation. The
# denominator and the coverage line exist because Rule 22 requires a claim to carry the set it
# ranged over: a gate that grades "the files it could see" without printing what it could NOT see
# is unfalsifiable at a glance, which is exactly S42's finding.

GATE = ".tools/naming-gate.py"


def _gate(args, cwd=None):
    """Run the naming gate and return its combined output, ANSI-stripped."""
    r = subprocess.run([sys.executable, GATE] + list(args),
                       capture_output=True, text=True, cwd=cwd or REPO)
    return _CSI.sub("", (r.stdout or "") + (r.stderr or ""))


def _diff_fixture(tmp, body):
    p = os.path.join(tmp, "fixture.diff")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    return p


_SAMPLE_DIFF = (
    "diff --git a/infra/logic/x.tf b/infra/logic/x.tf\n"
    "--- a/infra/logic/x.tf\n"
    "+++ b/infra/logic/x.tf\n"
    "@@ -0,0 +1,1 @@\n"
    '+resource "aws_s3_bucket" "b" { bucket = "opal-data-assets" }\n'
)


def n2_denominator(cwd=None):
    """Every run prints the DENOMINATOR of paths it graded."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    has = "DENOMINATOR" in out
    say("gate output lines: %d; DENOMINATOR line present: %s" % (len(out.splitlines()), has))
    if not has:
        say("FAIL-N2-NO-DENOMINATOR")
        return 1
    say("PASS-N2-DENOMINATOR-PRINTED")
    return 0


def n2_coverage(cwd=None):
    """Every run prints what it could NOT see -- the coverage half of the same claim (S42)."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2c_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    has = "COVERAGE" in out
    say("COVERAGE line (paths the gate cannot see) present: %s" % has)
    if not has:
        say("FAIL-N2-NO-COVERAGE")
        return 1
    say("PASS-N2-COVERAGE-PRINTED")
    return 0


def n2_declaration_subtraction(cwd=None):
    """The declaration-tree set is printed as a SUBTRACTION from the denominator, never a list.

    Rule 24(i): a forward list of trees omits silently; the same set written as denominator MINUS
    exclusions cannot lose a member without the count disagreeing. `org/**` and `docs/**` are the
    declared exclusions, so both must appear as EXCLUDED rather than merely be absent.
    """
    import tempfile
    tmp = tempfile.mkdtemp(prefix="en_r3_n2d_")
    try:
        out = _gate(["--diff", _diff_fixture(tmp, _SAMPLE_DIFF)], cwd)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    named = "EXCLUDED" in out and "org/" in out and "docs/" in out
    say("declaration-tree subtraction printed with org/ and docs/ named EXCLUDED: %s" % named)
    if not named:
        say("FAIL-N2-NO-SUBTRACTION")
        return 1
    say("PASS-N2-SUBTRACTION-PRINTED")
    return 0


# ---------------------------------------------------------------- cell 3a arm
#
# LGIC_NAMING-S21: proof-of-spec-check.py's surprises limb resolves a cited row by globbing
# WORKSPACE = Path(__file__).resolve().parent.parent -- the checkout holding the SCRIPT -- not the
# checkout holding the INSTANCE being graded. So the main checkout's script, pointed at an instance
# on a side branch or in a linked worktree whose channel carries the row, reads "resolves to NO row"
# although the row is committed in the graded tree. The CVO's L9 and the L10 gate run that script.
#
# The arm builds a throwaway git repo shaped like the tree: a channel carrying a planted row id that
# the script's own checkout does NOT carry, and an instance citing it. It runs the script under test
# against that instance and PASSes only when the limb resolves the planted row. Reproduced RED at
# HEAD before this arm was written: "0 resolve to a channel row ... names row id LGIC_ENFORCE-S9990
# which resolves to NO row".


POS_CHECK = ".tools/proof-of-spec-check.py"
_PLANTED_RID = "LGIC_ENFORCE-S9990"


def _s21_fixture(root):
    """A git repo at `root` whose channel carries _PLANTED_RID and whose instance cites it."""
    subprocess.run(["git", "init", "-q"], cwd=root, capture_output=True)
    ch = os.path.join(root, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "surprise-channel", "investigations")
    os.makedirs(ch, exist_ok=True)
    with open(os.path.join(ch, "INVESTIGATION_v1.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# fixture\n\n```json\n" + json.dumps([{"id": _PLANTED_RID, "project": "LGIC_ENFORCE"}], indent=1)
                 + "\n```\n")
    dl = os.path.join(root, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "deliverables", "0.9.0_WK_LGIC_ENFORCE~9")
    os.makedirs(dl, exist_ok=True)
    inst = os.path.join(dl, "LGIC_ENFORCE.TO-EN-q-9.fixture.proof_of_spec.json")
    with open(inst, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"schema_version": "1.0", "to_id": "LGIC_ENFORCE.TO-EN-q-9",
                   "surprises": [_PLANTED_RID + ": planted row present ONLY in the graded checkout"]}, fh)
    subprocess.run(["git", "add", "-A"], cwd=root, capture_output=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "f"],
                   cwd=root, capture_output=True)
    return inst


def _limb_resolves(script, inst):
    """(resolved, evidence line). Reads the limb's OWN frame and announce lines."""
    r = subprocess.run([sys.executable, script, inst], capture_output=True, text=True)
    out = _CSI.sub("", (r.stdout or "") + (r.stderr or ""))
    miss = "names row id %s which resolves to NO row" % _PLANTED_RID
    frame = [ln for ln in out.splitlines() if ln.strip().startswith("surprises-frame:")]
    ev = frame[0].strip() if frame else "(no surprises-frame line -- the limb did not run)"
    if not frame:
        return None, ev
    return (miss not in out and " 1 resolve to a channel row" in ev), ev


def i3_channel_root(script=None):
    """The script under test resolves a cited row from the INSTANCE's checkout."""
    token = _i3_verdict(script)
    say(token)
    return 0 if token.startswith("PASS-") else 1


def _i3_verdict(script=None):
    """The verdict TOKEN, printed evidence above it. A self-test compares tokens so a control can never
    pass for the wrong reason (a RED that is really LIMB-DID-NOT-RUN is not a RED)."""
    script = script or os.path.join(REPO, POS_CHECK)
    base = _tempfile.mkdtemp(prefix="en_r3_i3_")
    try:
        inst = _s21_fixture(base)
        # CONTROL on the premise: the planted id must be ABSENT from the script's own checkout, or a
        # PASS would prove nothing about rooting.
        own = os.path.abspath(os.path.join(os.path.dirname(script), os.pardir))
        own_ch = os.path.join(own, "org", "missions", "D14", "LGIC", "LGIC_ENFORCE", "surprise-channel",
                              "investigations", "INVESTIGATION_v1.md")
        try:
            with open(own_ch, encoding="utf-8", errors="replace") as fh:
                premise_broken = _PLANTED_RID in fh.read()
        except (OSError, IOError):
            premise_broken = False
        if premise_broken:
            say("PREMISE: %s already exists in the script's own checkout -- the arm cannot discriminate" % _PLANTED_RID)
            return "FAIL-I3-PREMISE-BROKEN"
        resolved, ev = _limb_resolves(script, inst)
        say("script under test: %s" % script)
        say("planted row %s: present in the GRADED checkout, absent from the script's own" % _PLANTED_RID)
        say("limb frame: %s" % ev[:220])
        if resolved is None:
            return "FAIL-I3-LIMB-DID-NOT-RUN"
        if not resolved:
            return "FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT"
        return "PASS-I3-ROOTED-AT-INSTANCE-CHECKOUT"
    finally:
        _shutil.rmtree(base, ignore_errors=True)


def _install_script(root):
    """A copy of the live script under `root`, WITH the schema it reads relative to its own root
    (org/standards/PROOF_OF_SPEC.schema.json) -- without it the copy exits rc=2 before any limb runs,
    which is how a first version of this self-test reported a RED for the wrong reason."""
    os.makedirs(os.path.join(root, ".tools"), exist_ok=True)
    os.makedirs(os.path.join(root, "org", "standards"), exist_ok=True)
    dst = os.path.join(root, ".tools", "proof-of-spec-check.py")
    _shutil.copy(os.path.join(REPO, POS_CHECK), dst)
    _shutil.copy(os.path.join(REPO, "org", "standards", "PROOF_OF_SPEC.schema.json"),
                 os.path.join(root, "org", "standards", "PROOF_OF_SPEC.schema.json"))
    return dst


def _selftest_i3():
    """Both controls use COPIES of the script, so the self-test does not depend on whether the live
    script has been fixed yet. RED: a copy rooted in a checkout WITHOUT the row must return EXACTLY
    FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT. GREEN: a copy rooted INSIDE the graded checkout -- what a correct
    fix is equivalent to -- must resolve the row."""
    out = []
    elsewhere = _tempfile.mkdtemp(prefix="en_r3_i3_other_")
    try:
        mis = _install_script(elsewhere)
        tok = _i3_verdict(mis)
        out.append(("i3 RED   mis-rooted copy -> ROOTED-AT-SCRIPT (%s)" % tok[:28],
                    tok == "FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT"))
    finally:
        _shutil.rmtree(elsewhere, ignore_errors=True)

    base = _tempfile.mkdtemp(prefix="en_r3_i3_in_")
    try:
        inst = _s21_fixture(base)
        rooted = _install_script(base)
        resolved, _ev = _limb_resolves(rooted, inst)
        out.append(("i3 GREEN copy rooted INSIDE the graded checkout", resolved is True))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


# ---------------------------------------------------------------- cell 5 arms
#
# RULING R-6 on the six tokens EN-r-2 left `unresolved` in systems.json. Refused keys live INSIDE
# infra/logic/registry/systems.json as the `refused_keys` dict -- there is NO refused_keys.json file.
# Two carriers name one: this seat's own row LGIC_ENFORCE-S57 (the origin, a path typed into an act-census
# script and never checked for existence) and RULING R-23, which copied it. LGIC_ENFORCE-S58. Measured at the cut: refused_keys
# carries workstream_code / generic_noun / purpose_word and no `retired` class, and all six tokens --
# find, harvest, imo, astn, trade, news -- still sit in `unresolved`. So every arm below reads RED
# before the cell runs.
#
# NOT an arm here, on purpose: S19's stale scopes.json _about.row_fields sentence. It was introduced at
# a925c8a642 (EN-r-1) and REMOVED at 22e86e55f5 (EN-r-3-r2, round 2); the schema's firm_forms key is
# gone too. A criterion on it would PASS before the cell runs, which W2-S11 forbids.

SYSTEMS = "infra/logic/registry/systems.json"

# The `why` text each token carried at the cut. A token the cell leaves unresolved must carry a NEW,
# measured why -- re-reading the old sentence is not a measurement (R-6 s.3).
PRE_CELL_WHY = {
    "find": "infra/logic/05_IDENTITY_SPINE.md s.3 marks harvest/find UNRESOLVED (tick-list row 18)",
    "harvest": "infra/logic/05_IDENTITY_SPINE.md s.3 marks harvest/find UNRESOLVED (tick-list row 18)",
    "imo": "infra/logic/05_IDENTITY_SPINE.md s.3: whether imo is a product, a vendor or retired is a word (tick-list row 18)",
}
PRE_CELL_WHY_PREFIX = "GRADING_RULE.md V1 lists it as a PRODUCT, but no DIRECTIVES.yaml line"
PRODUCT_TOKENS = ["harvest", "astn", "news", "trade"]


def _systems(root=None):
    with open(os.path.join(root or REPO, SYSTEMS.replace("/", os.sep)), encoding="utf-8") as fh:
        return json.load(fh)


def _unresolved(sy):
    return {u.get("token"): u.get("why", "") for u in (sy.get("unresolved") or []) if isinstance(u, dict)}


def r5_imo_retired(root=None):
    """`imo` is a member of a refused_keys `retired` class carrying its basis, and is no longer unresolved."""
    sy = _systems(root)
    rk = sy.get("refused_keys") or {}
    retired = rk.get("retired")
    members = retired if isinstance(retired, list) else (retired or {}).get("members", []) if isinstance(retired, dict) else []
    in_class = "imo" in members
    still_open = "imo" in _unresolved(sy)
    say("refused_keys classes: %s" % sorted(k for k in rk if k != "basis"))
    say("retired class present: %s; imo a member: %s; imo still unresolved: %s"
        % (retired is not None, in_class, still_open))
    if not in_class or still_open:
        say("FAIL-R5-IMO-NOT-RETIRED")
        return 1
    say("PASS-R5-IMO-RETIRED")
    return 0


def r5_find_refused(root=None):
    """`find` is a refused workstream code (V3: a project code is never a system), no longer unresolved."""
    sy = _systems(root)
    wc = (sy.get("refused_keys") or {}).get("workstream_code") or []
    in_class = "find" in wc
    still_open = "find" in _unresolved(sy)
    say("workstream_code members: %d; find a member: %s; find still unresolved: %s"
        % (len(wc), in_class, still_open))
    if not in_class or still_open:
        say("FAIL-R5-FIND-NOT-REFUSED")
        return 1
    say("PASS-R5-FIND-REFUSED")
    return 0


def r5_product_owners(root=None):
    """Each of harvest/astn/news/trade is EITHER a PRODUCT row whose owner_claim is `inferred` or
    `measured` with a non-empty owner_basis citation, OR still unresolved with a NEW measured why.
    Never the pre-cell sentence unchanged: that is the guess R-6 refuses."""
    sy = _systems(root)
    rows = {r.get("key"): r for r in (sy.get("systems") or []) if isinstance(r, dict)}
    unres = _unresolved(sy)
    bad = []
    for tok in PRODUCT_TOKENS:
        row = rows.get(tok)
        if row is not None:
            claim = row.get("owner_claim")
            basis = (row.get("owner_basis") or "").strip()
            ok = row.get("class") == "PRODUCT" and claim in ("measured", "inferred") and len(basis) >= 12
            say("  %-8s ROW   class=%s owner_claim=%s basis_len=%d -> %s"
                % (tok, row.get("class"), claim, len(basis), "ok" if ok else "DEFECT"))
            if not ok:
                bad.append(tok)
        elif tok in unres:
            why = unres[tok]
            unchanged = why == PRE_CELL_WHY.get(tok) or why.startswith(PRE_CELL_WHY_PREFIX)
            say("  %-8s OPEN  why changed from the cut: %s" % (tok, not unchanged))
            if unchanged:
                bad.append(tok)
        else:
            say("  %-8s GONE  neither a row nor unresolved -- a token cannot vanish" % tok)
            bad.append(tok)
    say("DENOMINATOR: %d product token(s) ruled by R-6; %d defective" % (len(PRODUCT_TOKENS), len(bad)))
    if bad:
        say("FAIL-R5-OWNERS-UNMEASURED")
        return 1
    say("PASS-R5-OWNERS-MEASURED")
    return 0


def _selftest_r5():
    """Each arm RED on a copy of the registry as it stood at the cut, GREEN on a copy with the ruling
    applied -- both built in a temp root, so the self-test never reads the live file."""
    import copy
    live = _systems()
    out = []
    for label, apply, fn in [
        ("r5-imo-retired", lambda d: (d["refused_keys"].__setitem__("retired", ["imo"]),
                                      d.__setitem__("unresolved", [u for u in d["unresolved"] if u["token"] != "imo"])),
         r5_imo_retired),
        ("r5-find-refused", lambda d: (d["refused_keys"]["workstream_code"].append("find"),
                                       d.__setitem__("unresolved", [u for u in d["unresolved"] if u["token"] != "find"])),
         r5_find_refused),
        ("r5-product-owners", lambda d: [
            (d["systems"].append({"key": t, "class": "PRODUCT", "long": t, "owner_directive": "D9",
                                  "owner_claim": "inferred", "owner_basis": "lambda-source-map.json source_dir data/%s" % t}),
             d.__setitem__("unresolved", [u for u in d["unresolved"] if u["token"] != t]))
            for t in PRODUCT_TOKENS],
         r5_product_owners),
    ]:
        for state in ("RED", "GREEN"):
            doc = copy.deepcopy(live)
            if state == "GREEN":
                apply(doc)
            base = _tempfile.mkdtemp(prefix="en_r3_r5_")
            try:
                d = os.path.join(base, *SYSTEMS.split("/")[:-1])
                os.makedirs(d)
                with open(os.path.join(base, *SYSTEMS.split("/")), "w", encoding="utf-8") as fh:
                    json.dump(doc, fh)
                rc = fn(base)
            finally:
                _shutil.rmtree(base, ignore_errors=True)
            out.append(("%s %-5s" % (label, state), rc == (1 if state == "RED" else 0)))
    # the SAME-SENTENCE trap: a token left unresolved with its cut-time why must stay RED
    doc = copy.deepcopy(live)
    base = _tempfile.mkdtemp(prefix="en_r3_r5s_")
    try:
        os.makedirs(os.path.join(base, *SYSTEMS.split("/")[:-1]))
        with open(os.path.join(base, *SYSTEMS.split("/")), "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        out.append(("r5-product-owners unchanged-why stays RED", r5_product_owners(base) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


# ---------------------------------------------------------------- cell 6 arms
#
# The census, to the end (A-4, RULING ROWS, W2-S10). Round 2's run STOPPED on the first RAISE: its
# report's own fenced json reads judged_live 3 of live_nameable 1821, judged_repo 0 of repo 1878, a
# non-null `stopped`, and one row whose canonical carries the `{system}` placeholder. Each arm reads the
# REPORT'S OWN FENCED JSON, never its prose, so a number is graded exactly as the tool wrote it.
#
# Every arm takes an optional path. A criterion names the round-3 file the cell writes; with no path the
# arm looks for exactly ONE deliverables/*/NAMING_CENSUS_REPORT.r3.md (resp. COMPARISON), and zero or
# several is a FAIL naming the count, never a silent pick.
#
# NOT MECHANICAL, and so NOT AN ARM: whether each hand row the comparison leaves uncompared has a stated
# reason. No field decides that; it is a JUDGMENT criterion graded by 3.0.0_SA_CVO at L9.

_FENCE = re.compile(r"```json\s*(.*?)```", re.S)
HAND_POPULATIONS = {"N2": 45, "N6": 88}
NL = "\n"

# Round 2's measured numbers, EMBEDDED rather than read from round 2's files. Those files are ownerless
# blobs that cell 4 MOVES; a self-test reading them at their flat path would, after cell 4 drains, fail on
# "file missing" and still count as a RED -- a control passing for the wrong reason.
ROUND2_REPORT = {
    "vintage": "Built from the estate as of 2026-09-16 05:57:28 UTC.",
    "denominators": {"repo": 1878, "live": 2176, "live_nameable": 1821, "judged_live": 3, "judged_repo": 0},
    "stopped": {"plane": "live", "type": "API_GW", "current": "sentiment-query-api"},
    "rows": [
        {"current": "inf-otp-relay-api", "canonical": "{system}-inf-otp-relay-api", "verdict": "OUT-OF-PATTERN"},
        {"current": "opal-portal-data-proxy-api", "canonical": "opal-portal-data-proxy-api", "verdict": "CONFORMANT"},
        {"current": "opal-session-analytics-api", "canonical": "opal-session-analytics-api", "verdict": "CONFORMANT"},
    ],
}
ROUND2_COMPARISON = {
    "census": {"judged_live": 3, "live_nameable": 1821, "judged_repo": 0, "repo": 1878,
               "stopped": {"plane": "live"}},
    "against": {"N2": {"hand_population": 45, "compared": ["opal-portal-data-proxy-api"], "uncompared_hand_rows": 44},
                "N6": {"hand_population": 88, "compared": ["inf-otp-relay-api", "opal-session-analytics-api"],
                       "uncompared_hand_rows": 86}},
}


def _fenced(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        blocks = _FENCE.findall(fh.read())
    if not blocks:
        return None
    try:
        return json.loads(blocks[-1])
    except ValueError:
        return None


def _one(pattern_name, path, root=None):
    """(path or None, message). Exactly one match or a stated failure."""
    if path:
        return (path, "") if os.path.exists(path) else (None, "named file does not exist: %s" % path)
    import glob as _glob
    hits = sorted(_glob.glob(os.path.join(root or REPO, *DELIV.split("/"), "*", pattern_name)))
    if len(hits) != 1:
        return None, "%d file(s) match deliverables/*/%s (exactly one required)" % (len(hits), pattern_name)
    return hits[0], ""


def _report(path=None, root=None):
    p, why = _one("NAMING_CENSUS_REPORT.r3.md", path, root)
    if p is None:
        say(why)
        return None, None
    d = _fenced(p)
    if d is None:
        say("no parseable fenced json in %s" % p)
    return p, d


def s6_live_complete(path=None, root=None):
    """judged_live == live_nameable > 0, a built: vintage, and no stop."""
    p, d = _report(path, root)
    if d is None:
        say("FAIL-S6-REPORT-UNREADABLE")
        return 1
    den = d.get("denominators") or {}
    jl, ln = den.get("judged_live"), den.get("live_nameable")
    vint = str(d.get("vintage") or "")
    say("report: %s" % p)
    say("DENOMINATOR: judged_live %s of live_nameable %s; live pulled %s; stopped=%s; vintage built-line: %s"
        % (jl, ln, den.get("live"), d.get("stopped") is not None, "Built from the estate" in vint))
    if d.get("stopped") is not None:
        say("FAIL-S6-LIVE-STOPPED-ON-RAISE")
        return 1
    if not isinstance(ln, int) or ln <= 0 or jl != ln:
        say("FAIL-S6-LIVE-INCOMPLETE")
        return 1
    if "Built from the estate" not in vint:
        say("FAIL-S6-LIVE-NO-VINTAGE")
        return 1
    say("PASS-S6-LIVE-COMPLETE")
    return 0


def s6_repo_complete(path=None, root=None):
    """judged_repo == repo > 0 and no stop."""
    p, d = _report(path, root)
    if d is None:
        say("FAIL-S6-REPORT-UNREADABLE")
        return 1
    den = d.get("denominators") or {}
    jr, rn = den.get("judged_repo"), den.get("repo")
    say("DENOMINATOR: judged_repo %s of repo %s; stopped=%s" % (jr, rn, d.get("stopped") is not None))
    if d.get("stopped") is not None:
        say("FAIL-S6-REPO-STOPPED-ON-RAISE")
        return 1
    if not isinstance(rn, int) or rn <= 0 or jr != rn:
        say("FAIL-S6-REPO-INCOMPLETE")
        return 1
    say("PASS-S6-REPO-COMPLETE")
    return 0


def s6_no_placeholder(path=None, root=None):
    """No report row's canonical carries a `{...}` placeholder (W2-S10), against a non-empty row set."""
    p, d = _report(path, root)
    if d is None:
        say("FAIL-S6-REPORT-UNREADABLE")
        return 1
    rows = d.get("rows") or []
    leaked = [r for r in rows if "{" in str(r.get("canonical", ""))]
    say("DENOMINATOR: %d report row(s); %d carry a placeholder in canonical" % (len(rows), len(leaked)))
    for r in leaked[:10]:
        say("   PLACEHOLDER:", r.get("current"), "->", r.get("canonical"))
    if not rows:
        say("FAIL-S6-NO-ROWS (an empty row set cannot be checked for placeholders)")
        return 1
    if leaked:
        say("FAIL-S6-PLACEHOLDER-IN-REPORT")
        return 1
    say("PASS-S6-NO-PLACEHOLDER")
    return 0


def _complete(census, judged, total):
    n = census.get(total)
    return isinstance(n, int) and n > 0 and census.get(judged) == n


def s6_comparison_arithmetic(path=None, root=None):
    """The comparison runs over the REAL hand populations (N2 45, N6 88), each set's compared + uncompared
    closes to its population, and the census embedded in it is COMPLETE on both planes.

    CLOSING ARITHMETIC IS NOT ENOUGH, measured on round 2's own comparison: it closes on BOTH sets (N2 1+44=45,
    N6 2+86=88) and is RED only because its census block is `stopped`. A comparison run against an unstopped
    but INCOMPLETE census would close too, so the census it read must itself be complete."""
    p, why = _one("NAMING_CENSUS_COMPARISON.r3.md", path, root)
    if p is None:
        say(why)
        say("FAIL-S6-COMPARISON-UNREADABLE")
        return 1
    d = _fenced(p) or {}
    against = d.get("against") or {}
    bad = []
    for name, pop in HAND_POPULATIONS.items():
        a = against.get(name) or {}
        hp = a.get("hand_population")
        comp = len(a.get("compared") or [])
        unc = a.get("uncompared_hand_rows")
        closes = isinstance(unc, int) and comp + unc == hp
        say("  %s: hand_population %s (ruled %d); compared %d + uncompared %s -> %s"
            % (name, hp, pop, comp, unc, "closes" if closes and hp == pop else "DEFECT"))
        if hp != pop or not closes:
            bad.append(name)
    census = d.get("census") if isinstance(d.get("census"), dict) else {}
    stopped = census.get("stopped") is not None
    live_done = _complete(census, "judged_live", "live_nameable")
    repo_done = _complete(census, "judged_repo", "repo")
    say("embedded census: stopped=%s; judged_live %s of %s; judged_repo %s of %s"
        % (stopped, census.get("judged_live"), census.get("live_nameable"),
           census.get("judged_repo"), census.get("repo")))
    if bad or stopped or not live_done or not repo_done:
        say("FAIL-S6-COMPARISON-NOT-OVER-REAL-POPULATION")
        return 1
    say("PASS-S6-COMPARISON-ARITHMETIC")
    return 0


def _write_fenced(path, doc):
    with open(path, "w", encoding="utf-8", newline=NL) as fh:
        fh.write("# fixture" + NL + NL + "```json" + NL + json.dumps(doc) + NL + "```" + NL)
    return path


def _selftest_s6():
    """RED on round 2's EMBEDDED numbers; GREEN on synthesized complete documents; plus the trap arm for a
    comparison that closes over an unstopped but incomplete census."""
    out = []
    base = _tempfile.mkdtemp(prefix="en_r3_s6_")
    try:
        r2r = _write_fenced(os.path.join(base, "r2_report.md"), ROUND2_REPORT)
        r2c = _write_fenced(os.path.join(base, "r2_comparison.md"), ROUND2_COMPARISON)
        good = {"vintage": "Built from the estate as of 2026-09-16 12:17:46 UTC.",
                "denominators": {"live": 2176, "live_nameable": 2, "judged_live": 2, "repo": 1, "judged_repo": 1},
                "stopped": None,
                "rows": [{"current": "a", "canonical": "opal-a", "verdict": "CONFORMANT"},
                         {"current": "b", "canonical": "opal-b", "verdict": "OUT-OF-PATTERN"}]}
        gr = _write_fenced(os.path.join(base, "good_report.md"), good)
        gcd = {"census": {"stopped": None, "judged_live": 2, "live_nameable": 2, "judged_repo": 1, "repo": 1},
               "against": {"N2": {"hand_population": 45, "compared": ["x"] * 40, "uncompared_hand_rows": 5},
                           "N6": {"hand_population": 88, "compared": ["y"] * 80, "uncompared_hand_rows": 8}}}
        gc = _write_fenced(os.path.join(base, "good_comparison.md"), gcd)
        opened = json.loads(json.dumps(gcd))
        opened["against"]["N6"]["uncompared_hand_rows"] = 3
        oc = _write_fenced(os.path.join(base, "open_comparison.md"), opened)
        incomplete = json.loads(json.dumps(gcd))
        incomplete["census"].update({"judged_live": 3, "live_nameable": 1821})
        ic = _write_fenced(os.path.join(base, "incomplete_census_comparison.md"), incomplete)

        out.append(("s6-live-complete RED  (round 2 numbers)", s6_live_complete(r2r) == 1))
        out.append(("s6-live-complete GREEN", s6_live_complete(gr) == 0))
        out.append(("s6-repo-complete RED  (round 2 numbers)", s6_repo_complete(r2r) == 1))
        out.append(("s6-repo-complete GREEN", s6_repo_complete(gr) == 0))
        out.append(("s6-no-placeholder RED (round 2 numbers)", s6_no_placeholder(r2r) == 1))
        out.append(("s6-no-placeholder GREEN", s6_no_placeholder(gr) == 0))
        out.append(("s6-comparison RED    (round 2 numbers)", s6_comparison_arithmetic(r2c) == 1))
        out.append(("s6-comparison GREEN", s6_comparison_arithmetic(gc) == 0))
        out.append(("s6-comparison RED    (arithmetic open)", s6_comparison_arithmetic(oc) == 1))
        out.append(("s6-comparison RED    (closes, census incomplete)", s6_comparison_arithmetic(ic) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


# ---------------------------------------------------------------- cell 7 arm (DEC-4 ii)
#
# RULING R-20: four live IAM roles carry a firm key but are LEGACY-NAMED, so the generated fence catches
# none of them (0 of 4). DEC-4(ii): before a firm bucket's Deny lands on a principal the rule does not name,
# that principal is RENAMED under name() by its OWNER (D9's IRPT projects; the ADVI family), or NAMED in
# exemptions.json with its reason. R-20: an exemption is the interim THIS cell may write; a rename is not.
# A role that genuinely never touches the bucket is recorded NOT_A_PRINCIPAL with its evidence.
#
# MEASURED BEFORE BUILDING, and it is why this arm is the only cell-7 limb cut now:
#   - the generated fence is ALREADY APPLIED on opal-data-49financial (round 1, EN-f-2; ledger
#     20260915T0334Z_lgic-enforce-fence-49financial_deploy_completion.md CLOSED 4 of 4 legs);
#   - the three probe roles were removed at that entry's close (NoSuchEntity x3, re-plan 0-diff) and the live
#     plane reads 0 'fenceprobe' nodes of 2,558 -- so "probes removed" would PASS before the cell runs and is
#     NOT a criterion;
#   - FWD-2's EXERCISED limb is an open call at 1.0.0_SA_CTO and is cut when ruled.
#
# THE RENAMED BRANCH RE-MEASURES the live plane rather than trusting the worker's field. Predicate measured
# with controls before use: `^name$` returns 0 for roles that ARE live (the aws corpus matches name+arn+props
# concatenated, so line anchors never hold) -- a broken predicate reading as an absence. `role/<name>` with a
# negative lookahead returns exactly 1 for a live role and 0 for an invented one, and the returned node name
# must equal the role exactly.

LEGACY_WRITERS = [
    {"role": "irpt-core-firm-49financial", "bucket": "opal-data-49financial"},
    {"role": "irpt-core-firm-inflection", "bucket": "opal-data-inf"},
    {"role": "irpt-core-firm-cottonwood", "bucket": "opal-data-cot"},
    {"role": "demo-transform-runner-ec2-role", "bucket": "opal-data-demo"},
]
EXEMPTIONS = "infra/logic/registry/exemptions.json"
DISPOSITIONS = ("EXEMPTED", "RENAMED", "NOT_A_PRINCIPAL")


def _live_role(name):
    """(present or None, vintage). None means the instrument did not answer -- never an absence."""
    argv = [sys.executable, os.path.join(REPO, ".tools", "comp-find"), "--corpus", "aws",
            r"role/%s(?![A-Za-z0-9_-])" % re.escape(name), "IAM_ROLE", "--limit", "10"]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=180,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=REPO)
    except subprocess.TimeoutExpired:
        return None, None
    out = (r.stdout or "") + (r.stderr or "")
    den = re.search(r"DENOMINATOR: (\d+) hit\(s\) across (\d+) aws node", out)
    vin = re.search(r"VINTAGE: Built from the estate as of ([0-9-]+ [0-9:]+ UTC)", out)
    if not den or int(den.group(2)) == 0:
        return None, None
    names = re.findall(r"^    (\S+)\s+drift=", out, re.M)
    return (name in names), (vin.group(1) if vin else None)


def w7_writers_dispositioned(path=None, root=None, live_role=None):
    """Each of R-20's four legacy writers carries a disposition that the ARTIFACT, not the worker, confirms."""
    live_role = live_role or _live_role
    p, why = _one("FENCE_WRITER_DISPOSITION.r3.json", path, root)
    if p is None:
        say(why)
        say("FAIL-W7-DISPOSITION-UNREADABLE")
        return 1
    try:
        with open(p, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        say("unreadable disposition file: %s" % exc)
        say("FAIL-W7-DISPOSITION-UNREADABLE")
        return 1
    rows = {r.get("role"): r for r in (doc.get("rows") or []) if isinstance(r, dict)}
    with open(os.path.join(root or REPO, *EXEMPTIONS.split("/")), encoding="utf-8") as fh:
        ex = json.load(fh).get("exemptions") or {}
    bad = []
    for w in LEGACY_WRITERS:
        role, bucket = w["role"], w["bucket"]
        row = rows.get(role)
        if row is None:
            say("  %-32s MISSING from the disposition file" % role)
            bad.append(role)
            continue
        disp = row.get("disposition")
        evidence = str(row.get("evidence") or "").strip()
        if disp not in DISPOSITIONS:
            say("  %-32s disposition %r is not one of %s" % (role, disp, DISPOSITIONS))
            bad.append(role)
        elif disp == "EXEMPTED":
            named = [e for e in (ex.get(bucket) or []) if isinstance(e, dict) and e.get("principal") == role]
            ok = bool(named) and len(str(named[0].get("reason") or "").strip()) >= 12
            say("  %-32s EXEMPTED under %s: present with a reason in exemptions.json -> %s" % (role, bucket, ok))
            if not ok:
                bad.append(role)
        elif disp == "RENAMED":
            present, vintage = live_role(role)
            say("  %-32s RENAMED: legacy name live at vintage %s -> %s" % (role, vintage, present))
            if present is not False:
                bad.append(role)
        else:
            ok = len(evidence) >= 40
            say("  %-32s NOT_A_PRINCIPAL of %s: evidence %d chars -> %s" % (role, bucket, len(evidence), ok))
            if not ok:
                bad.append(role)
    say("DENOMINATOR: %d legacy writer(s) ruled by R-20; %d without a confirmed disposition" % (len(LEGACY_WRITERS), len(bad)))
    if bad:
        say("FAIL-W7-WRITERS-UNDISPOSITIONED")
        return 1
    say("PASS-W7-WRITERS-DISPOSITIONED")
    return 0


def _selftest_w7():
    """Every branch, both ways, against a temp root and an INJECTED live-plane reader -- the self-test never
    reads the live plane, so its verdict cannot drift with the estate."""
    out = []
    base = _tempfile.mkdtemp(prefix="en_r3_w7_")
    try:
        os.makedirs(os.path.join(base, "infra", "logic", "registry"))
        dl = os.path.join(base, *DELIV.split("/"), "0.9.0_WK_LGIC_ENFORCE~9")
        os.makedirs(dl)

        def write(exempt_rows, rows):
            with open(os.path.join(base, *EXEMPTIONS.split("/")), "w", encoding="utf-8") as fh:
                json.dump({"exemptions": exempt_rows}, fh)
            fp = os.path.join(dl, "FENCE_WRITER_DISPOSITION.r3.json")
            with open(fp, "w", encoding="utf-8") as fh:
                json.dump({"rows": rows}, fh)
            return fp

        def gone(_n):
            return False, "2026-09-16 12:17:46 UTC"

        def still(_n):
            return True, "2026-09-16 12:17:46 UTC"

        def silent(_n):
            return None, None

        empty = {w["bucket"]: [] for w in LEGACY_WRITERS}
        exempted = {w["bucket"]: [{"principal": w["role"], "reason": "reads its firm's bucket, measured in E1's census"}]
                    for w in LEGACY_WRITERS}
        all_exempted = [{"role": w["role"], "disposition": "EXEMPTED"} for w in LEGACY_WRITERS]

        fp = write(empty, all_exempted)
        out.append(("w7 RED   claimed EXEMPTED, absent from exemptions.json", w7_writers_dispositioned(fp, base, gone) == 1))
        fp = write(exempted, all_exempted)
        out.append(("w7 GREEN EXEMPTED and present with a reason", w7_writers_dispositioned(fp, base, gone) == 0))
        renamed = [{"role": w["role"], "disposition": "RENAMED"} for w in LEGACY_WRITERS]
        fp = write(empty, renamed)
        out.append(("w7 RED   claimed RENAMED, legacy name still live", w7_writers_dispositioned(fp, base, still) == 1))
        out.append(("w7 RED   claimed RENAMED, live plane did not answer", w7_writers_dispositioned(fp, base, silent) == 1))
        out.append(("w7 GREEN RENAMED and gone from the live plane", w7_writers_dispositioned(fp, base, gone) == 0))
        thin = [{"role": w["role"], "disposition": "NOT_A_PRINCIPAL", "evidence": "n/a"} for w in LEGACY_WRITERS]
        fp = write(empty, thin)
        out.append(("w7 RED   NOT_A_PRINCIPAL with no evidence", w7_writers_dispositioned(fp, base, gone) == 1))
        fp = write(exempted, all_exempted[:3])
        out.append(("w7 RED   one of the four missing", w7_writers_dispositioned(fp, base, gone) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


# ---------------------------------------------------------------- cell 7 regression arm (R-25)
#
# RULING R-25 @96ebbde746: FWD-2's EXERCISED bar was met in round 1 -- mdpf-49f-fenceprobe-role, a real role
# named by name(), was ALLOWED by the live generated fence in a real get-object while the cot and unscoped
# probes were DENIED (FENCE_PROBES.md; ledger 20260915T0334Z_..._deploy_completion.md). Cell 7 carries the
# REGRESSION READ: the Deny APPLIED on the real bucket still equals what the builder produces from the registry.
#
# This is a REGRESSION guard, not a progress criterion, and is named `regress-` so W2-S11 is not misread: it
# PASSES before the cell runs because the fence is already live, and it must still PASS after the cell edits
# exemptions.json -- which is exactly the point, since a new exemption row the cell writes must reach the
# applied policy through the generator, never by hand.
#
# THE LIVE READ is `aws s3api get-bucket-policy`, which DEC-4 names as the APPLIED read. No comp-tool prints a
# bucket-policy DOCUMENT (comp-find --corpus aws exposes the node and its drift class, not the statement). The
# read fails CLOSED: empty output, unparseable JSON (the shim can truncate at rc=0) or a missing statement is a
# FAIL naming the cause, never a pass. Measured at the cut: 17 of 17 equal (1 pattern + 16 exemption ARNs).

FENCE_BUCKET = "opal-data-49financial"
FENCE_FIRM = "49financial"
FENCE_SID = "DenyForeignFirmPrincipals"


def _live_policy(bucket):
    """(policy dict or None, cause)."""
    # the shim is a bash script with a .cmd twin (CLAUDE.md: both or neither); Windows Python can run only the .cmd
    shim = os.path.join(REPO, ".tools", "aws.cmd" if os.name == "nt" else "aws")
    argv = [shim, "s3api", "get-bucket-policy", "--bucket", bucket,
            "--query", "Policy", "--output", "text"]
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=90, cwd=REPO)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, "live read did not run: %s" % exc
    raw = (r.stdout or "").strip()
    if r.returncode != 0 or not raw:
        return None, "live read rc=%d, %d bytes: %s" % (r.returncode, len(raw), (r.stderr or "")[:160])
    try:
        return json.loads(raw), ""
    except ValueError as exc:
        return None, "live policy unparseable (%d bytes): %s" % (len(raw), exc)


def _builder_expected(root=None):
    sys.path.insert(0, os.path.join(root or REPO, "lib"))
    import opal_naming  # noqa: E402 -- the builder under test lives in the repo, not on the default path
    with open(os.path.join(root or REPO, *EXEMPTIONS.split("/")), encoding="utf-8") as fh:
        ex = (json.load(fh).get("exemptions") or {}).get(FENCE_BUCKET) or []
    return list(opal_naming.fence_patterns(FENCE_FIRM)) + [e["arn"] for e in ex if isinstance(e, dict) and e.get("arn")]


def regress_w7_applied_deny(path=None, root=None, live_reader=None, expected=None):
    """The applied Deny on the real bucket equals fence_patterns() + fence_exemption_arns(), as sets."""
    policy, cause = (live_reader or _live_policy)(FENCE_BUCKET)
    if policy is None:
        say(cause)
        say("FAIL-W7R-LIVE-UNREADABLE")
        return 1
    stmts = [s for s in (policy.get("Statement") or []) if isinstance(s, dict) and s.get("Sid") == FENCE_SID]
    if len(stmts) != 1 or stmts[0].get("Effect") != "Deny":
        say("statements named %s: %d (exactly one Deny required)" % (FENCE_SID, len(stmts)))
        say("FAIL-W7R-NO-FENCE-STATEMENT")
        return 1
    live = ((stmts[0].get("Condition") or {}).get("ArnNotLike") or {}).get("aws:PrincipalArn") or []
    live = [live] if isinstance(live, str) else list(live)
    exp = expected if expected is not None else _builder_expected(root)
    only_live = sorted(set(live) - set(exp))
    only_builder = sorted(set(exp) - set(live))
    say("DENOMINATOR: live ArnNotLike %d entr%s; builder %d (fence_patterns + exemptions.json[%s])"
        % (len(live), "y" if len(live) == 1 else "ies", len(exp), FENCE_BUCKET))
    for a in only_live[:10]:
        say("   ON THE BUCKET, NOT FROM THE BUILDER:", a)
    for a in only_builder[:10]:
        say("   FROM THE BUILDER, NOT ON THE BUCKET:", a)
    if not live or not exp:
        say("FAIL-W7R-EMPTY-SET (an empty side cannot evidence equality)")
        return 1
    if only_live or only_builder:
        say("FAIL-W7R-APPLIED-DENY-DRIFTED-FROM-BUILDER")
        return 1
    say("PASS-W7R-APPLIED-DENY-EQUALS-BUILDER")
    return 0


def _selftest_w7r():
    """Injected live reader and expected set, so the verdict never drifts with the estate."""
    pat = "arn:aws:iam::313476888478:role/*-49f-*"
    exa = "arn:aws:iam::313476888478:role/aws-service-role/support.amazonaws.com/AWSServiceRoleForSupport"
    exp = [pat, exa]

    def policy(arns, sid=FENCE_SID, effect="Deny"):
        return lambda _b: ({"Statement": [{"Sid": sid, "Effect": effect,
                                           "Condition": {"ArnNotLike": {"aws:PrincipalArn": arns}}}]}, "")

    typed = "arn:aws:iam::313476888478:role/cot-*"
    return [
        ("w7r GREEN live equals builder", regress_w7_applied_deny(live_reader=policy([exa, pat]), expected=exp) == 0),
        ("w7r RED   an exemption missing on the bucket", regress_w7_applied_deny(live_reader=policy([pat]), expected=exp) == 1),
        ("w7r RED   a hand-typed principal added", regress_w7_applied_deny(live_reader=policy([pat, exa, typed]), expected=exp) == 1),
        ("w7r RED   statement is an Allow", regress_w7_applied_deny(live_reader=policy(exp, effect="Allow"), expected=exp) == 1),
        ("w7r RED   live read failed closed", regress_w7_applied_deny(live_reader=lambda _b: (None, "rc=255"), expected=exp) == 1),
        ("w7r RED   both sides empty", regress_w7_applied_deny(live_reader=policy([]), expected=[]) == 1),
    ]


# ---------------------------------------------------------------- cell 8 arms
#
# The roots census, evaluated (A-12, T3R-J1, T3R-AC2). Round 2's LIMB_ROOTS_CENSUS carries 72 roots (68
# planned, 4 NOT planned, each with a recorded plan rc=1 cause) and, per row, `plan_sha256` = the SHA-256 of the
# FULL `terraform show -json` document the committed extract was reduced from. The full documents are not
# committed.
#
# THE ANALYSIS TABLE'S WORDING IS UNSATISFIABLE, measured before this arm was written (LGIC_ENFORCE-S59): it says
# the re-plan's "plan_sha256 equal to the extract's". Every full plan document carries its own creation
# `timestamp` (measured on four committed full plans in this project: 03:47:57Z, 10:05:33Z, 11:19:12Z,
# 11:23:25Z), so a re-plan's full document can NEVER byte-equal round 2's and its SHA-256 can never match -- a
# PERFECT reproduction would FAIL. Round 2's own census states the achievable bar: "a spot re-plan of any planned
# root reproduces its EXTRACT". So the arm compares the reduced extract (resource_changes, which carries no
# timestamp) canonically, and requires the re-plan to be NEW (its own timestamp after the census vintage) so a
# copied round-2 document cannot stand in for a run.

ROOTS_CENSUS_R2 = "LIMB_ROOTS_CENSUS.md"


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _census_rows(path):
    d = _fenced(path)
    return (d or {}).get("roots"), (d or {}).get("vintage")


def t8_replan_reproduces_extract(path=None, root=None):
    """A re-plan of ONE planned root, run with -lockfile=readonly and newer than the census, reduces to exactly the
    committed round-2 extract for that root."""
    p, why = _one("ROOTS_REPRODUCTION.r3.json", path, root)
    if p is None:
        say(why)
        say("FAIL-T8-REPRODUCTION-UNREADABLE")
        return 1
    base = root or REPO
    try:
        with open(p, encoding="utf-8") as fh:
            rep = json.load(fh)
    except (OSError, ValueError) as exc:
        say("unreadable reproduction record: %s" % exc)
        say("FAIL-T8-REPRODUCTION-UNREADABLE")
        return 1
    census = os.path.join(base, *DELIV.split("/"), ROOTS_CENSUS_R2)
    rows, vintage = _census_rows(census) if os.path.exists(census) else (None, None)
    if rows is None:
        # cell 4 relocates the round-2 census; the record may name where it now lives
        alt = rep.get("census_path")
        if alt and os.path.exists(os.path.join(base, *alt.split("/"))):
            rows, vintage = _census_rows(os.path.join(base, *alt.split("/")))
    if rows is None:
        say("round-2 roots census not found at %s or the record's census_path" % ROOTS_CENSUS_R2)
        say("FAIL-T8-CENSUS-UNREADABLE")
        return 1
    target = rep.get("root")
    row = next((r for r in rows if r.get("root") == target), None)
    say("root under reproduction: %s; in census: %s; planned there: %s"
        % (target, row is not None, bool(row and row.get("planned"))))
    if row is None or not row.get("planned") or not row.get("extract"):
        say("FAIL-T8-ROOT-NOT-A-PLANNED-CENSUS-ROW")
        return 1
    cmd = str(rep.get("command") or "")
    if "-lockfile=readonly" not in cmd:
        say("command lacks -lockfile=readonly: %s" % cmd[:160])
        say("FAIL-T8-LOCKFILE-NOT-READONLY")
        return 1
    try:
        with open(os.path.join(base, *str(rep.get("full_plan") or "").split("/")), encoding="utf-8") as fh:
            full = json.load(fh)
        with open(os.path.join(base, *row["extract"].split("/")), encoding="utf-8") as fh:
            committed = json.load(fh)
    except (OSError, ValueError) as exc:
        say("plan or extract unreadable: %s" % exc)
        say("FAIL-T8-PLAN-UNREADABLE")
        return 1
    stamp = str(full.get("timestamp") or "")
    fresh = bool(stamp) and bool(vintage) and stamp > str(vintage)
    say("re-plan timestamp %s vs census vintage %s -> a new run: %s" % (stamp or "(none)", vintage, fresh))
    if not fresh:
        say("FAIL-T8-REPLAN-NOT-NEW")
        return 1
    ours, theirs = full.get("resource_changes"), committed.get("resource_changes")
    same = ours is not None and theirs is not None and _canon(ours) == _canon(theirs)
    say("DENOMINATOR: re-plan resource_changes %s; committed extract %s; canonical equal: %s"
        % (len(ours) if isinstance(ours, list) else "?", len(theirs) if isinstance(theirs, list) else "?", same))
    if not same:
        say("FAIL-T8-EXTRACT-NOT-REPRODUCED")
        return 1
    say("PASS-T8-EXTRACT-REPRODUCED")
    return 0


def t8_init_flags(path=None, root=None):
    """Every root row of the round-3 census prints the init flags it ran with (A-12)."""
    p, why = _one("LIMB_ROOTS_CENSUS.r3.md", path, root)
    if p is None:
        say(why)
        say("FAIL-T8-CENSUS-UNREADABLE")
        return 1
    rows, _v = _census_rows(p)
    if not rows:
        say("FAIL-T8-CENSUS-UNREADABLE")
        return 1
    missing = [r.get("root") for r in rows if not str(r.get("init_flags") or "").strip()]
    say("DENOMINATOR: %d root row(s); %d without init_flags" % (len(rows), len(missing)))
    for m in missing[:8]:
        say("   NO INIT FLAGS:", m)
    if missing:
        say("FAIL-T8-INIT-FLAGS-MISSING")
        return 1
    say("PASS-T8-INIT-FLAGS-PRINTED")
    return 0


def regress_t8_unplanned_have_cause(path=None, root=None):
    """REGRESSION (T3R-AC2 as A-12 re-reads it): a root recorded NOT planned is admitted only with its cause."""
    p = path or os.path.join(root or REPO, *DELIV.split("/"), ROOTS_CENSUS_R2)
    if not os.path.exists(p):
        p, why = _one("LIMB_ROOTS_CENSUS.r3.md", None, root)
        if p is None:
            say(why)
            say("FAIL-T8R-CENSUS-UNREADABLE")
            return 1
    rows, _v = _census_rows(p)
    if not rows:
        say("FAIL-T8R-CENSUS-UNREADABLE")
        return 1
    unplanned = [r for r in rows if not r.get("planned")]
    silent = [r.get("root") for r in unplanned if not str(r.get("reason") or "").strip()]
    say("DENOMINATOR: %d root(s); %d NOT planned; %d of those with no recorded cause"
        % (len(rows), len(unplanned), len(silent)))
    if silent:
        say("FAIL-T8R-UNPLANNED-WITHOUT-CAUSE")
        return 1
    say("PASS-T8R-UNPLANNED-ROOTS-CARRY-CAUSE")
    return 0


def _selftest_t8():
    """Temp-root fixtures only; the timestamp trap and the copied-document trap each held RED."""
    out = []
    base = _tempfile.mkdtemp(prefix="en_r3_t8_")
    try:
        dl = os.path.join(base, *DELIV.split("/"))
        wk = os.path.join(dl, "0.9.0_WK_LGIC_ENFORCE~9")
        os.makedirs(wk)
        changes = [{"address": "aws_s3_bucket.b", "change": {"actions": ["no-op"]}}]
        with open(os.path.join(wk, "extract.json"), "w", encoding="utf-8") as fh:
            json.dump({"format_version": "1.2", "resource_changes": changes}, fh)
        census = {"vintage": "2026-09-16T10:15:18Z", "roots": [
            {"root": "infra/r1", "planned": True, "extract": DELIV + "/0.9.0_WK_LGIC_ENFORCE~9/extract.json",
             "plan_sha256": "x", "reason": None, "init_flags": "-backend=true -lockfile=readonly"},
            {"root": "infra/r2", "planned": False, "extract": None, "plan_sha256": None,
             "reason": "terraform plan rc=1: No value for required variable", "init_flags": "-backend=true"}]}
        _write_fenced(os.path.join(dl, ROOTS_CENSUS_R2), census)

        def rec(full, cmd="terraform plan -lockfile=readonly -out=p", name="ROOTS_REPRODUCTION.r3.json"):
            with open(os.path.join(wk, "full.json"), "w", encoding="utf-8") as fh:
                json.dump(full, fh)
            rp = os.path.join(wk, name)
            with open(rp, "w", encoding="utf-8") as fh:
                json.dump({"root": "infra/r1", "command": cmd,
                           "full_plan": DELIV + "/0.9.0_WK_LGIC_ENFORCE~9/full.json"}, fh)
            return rp

        new = {"timestamp": "2026-09-16T19:00:00Z", "resource_changes": changes}
        out.append(("t8 GREEN new re-plan reproduces the extract", t8_replan_reproduces_extract(rec(new), base) == 0))
        drift = {"timestamp": "2026-09-16T19:00:00Z", "resource_changes": [{"address": "aws_s3_bucket.b",
                                                                             "change": {"actions": ["update"]}}]}
        out.append(("t8 RED   re-plan's changes differ", t8_replan_reproduces_extract(rec(drift), base) == 1))
        old = {"timestamp": "2026-09-16T09:00:00Z", "resource_changes": changes}
        out.append(("t8 RED   document older than the census (a copy)", t8_replan_reproduces_extract(rec(old), base) == 1))
        out.append(("t8 RED   no -lockfile=readonly", t8_replan_reproduces_extract(rec(new, cmd="terraform plan"), base) == 1))

        r3 = os.path.join(wk, "LIMB_ROOTS_CENSUS.r3.md")
        _write_fenced(r3, census)
        out.append(("t8 GREEN every row has init_flags", t8_init_flags(r3, base) == 0))
        bare = json.loads(json.dumps(census))
        del bare["roots"][1]["init_flags"]
        out.append(("t8 RED   one row without init_flags", t8_init_flags(_write_fenced(r3, bare), base) == 1))

        out.append(("t8r GREEN unplanned root carries its cause", regress_t8_unplanned_have_cause(None, base) == 0))
        silent = json.loads(json.dumps(census))
        silent["roots"][1]["reason"] = ""
        sp = _write_fenced(os.path.join(base, "silent.md"), silent)
        out.append(("t8r RED  unplanned root with no cause", regress_t8_unplanned_have_cause(sp, base) == 1))
    finally:
        _shutil.rmtree(base, ignore_errors=True)
    return out


# ---------------------------------------------------------------- self-test

def _fixture(tmp, blobs, placed):
    """A throwaway git repo shaped like the real one: `blobs` left flat, `placed` under authors."""
    os.makedirs(tmp, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp, capture_output=True)
    d = os.path.join(tmp, DELIV.replace("/", os.sep))
    os.makedirs(d, exist_ok=True)
    for b in blobs:
        with open(os.path.join(d, b), "w", encoding="utf-8") as fh:
            fh.write("x\n")
    for author, name in placed:
        sub = os.path.join(d, author)
        os.makedirs(sub, exist_ok=True)
        with open(os.path.join(sub, name), "w", encoding="utf-8") as fh:
            fh.write("x\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp, capture_output=True)
    subprocess.run(["git", "commit", "-q", "-m", "f"], cwd=tmp, capture_output=True)


def selftest_arms():
    """Every arm RED-FIRST: each must FAIL on the un-done tree and PASS on the done one."""
    import shutil
    import tempfile
    base = tempfile.mkdtemp(prefix="en_r3_selftest_")
    results = []
    try:
        names = ["A.md", "B.md"]
        mapdoc = {
            "denominator_blobs": 2,
            "rows": [
                {"basename": "A.md", "source": DELIV + "/A.md", "first_minting_author": "0.9.0_WK_LGIC_ENFORCE~1",
                 "destination": DELIV + "/0.9.0_WK_LGIC_ENFORCE~1/A.md"},
                {"basename": "B.md", "source": DELIV + "/B.md", "first_minting_author": "0.9.0_WK_LGIC_ENFORCE~2",
                 "destination": DELIV + "/0.9.0_WK_LGIC_ENFORCE~2/B.md"},
            ],
        }
        before = os.path.join(base, "before")
        _fixture(before, names, [])
        after = os.path.join(base, "after")
        _fixture(after, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])

        results.append(("p4-population  RED  (files still flat)", p4_population(before, mapdoc) == 1))
        results.append(("p4-population  GREEN (none flat)", p4_population(after, mapdoc) == 0))
        results.append(("p4-destinations RED  (nothing placed)", p4_destinations(before, mapdoc) == 1))
        results.append(("p4-destinations GREEN (all placed)", p4_destinations(after, mapdoc) == 0))

        # a citation fixture: one tracked file naming a moved file's OLD path
        cite = os.path.join(base, "cite")
        _fixture(cite, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])
        with open(os.path.join(cite, "notes.md"), "w", encoding="utf-8") as fh:
            fh.write("see " + DELIV + "/A.md\n")
        subprocess.run(["git", "add", "-A"], cwd=cite, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", "c"], cwd=cite, capture_output=True)
        results.append(("p4-citations   RED  (a dangling old path)", p4_citations(cite, mapdoc) == 1))
        results.append(("p4-citations   GREEN (none dangling)", p4_citations(after, mapdoc) == 0))

        # DISCRIMINATION: the type-column read must not count serial TREES as files
        trees = os.path.join(base, "trees")
        _fixture(trees, [], [("0.9.0_WK_LGIC_ENFORCE~1", "A.md"), ("0.9.0_WK_LGIC_ENFORCE~2", "B.md")])
        blobs = tree_blobs(trees)
        results.append(("tree-vs-blob   (2 serial folders counted as 0 files)", blobs == []))
    finally:
        shutil.rmtree(base, ignore_errors=True)

    results.extend(_selftest_i3())
    results.extend(_selftest_r5())
    results.extend(_selftest_s6())
    results.extend(_selftest_w7())
    results.extend(_selftest_w7r())
    results.extend(_selftest_t8())

    say("")
    for label, ok in results:
        say("  %-46s %s" % (label, "OK" if ok else "BROKEN"))
    good = sum(1 for _, ok in results if ok)
    say("SELFTEST-ARMS: %d of %d" % (good, len(results)))
    return 0 if good == len(results) else 1


CMDS = {
    "t8-replan-reproduces-extract": t8_replan_reproduces_extract,
    "t8-init-flags": t8_init_flags,
    "regress-t8-unplanned-have-cause": regress_t8_unplanned_have_cause,
    "regress-w7-applied-deny": regress_w7_applied_deny,
    "w7-writers-dispositioned": w7_writers_dispositioned,
    "s6-live-complete": s6_live_complete,
    "s6-repo-complete": s6_repo_complete,
    "s6-no-placeholder": s6_no_placeholder,
    "s6-comparison-arithmetic": s6_comparison_arithmetic,
    "r5-imo-retired": r5_imo_retired,
    "r5-find-refused": r5_find_refused,
    "r5-product-owners": r5_product_owners,
    "i3-channel-root": i3_channel_root,
    "n2-denominator": n2_denominator,
    "n2-coverage": n2_coverage,
    "n2-declaration-subtraction": n2_declaration_subtraction,
    "p4-population": p4_population,
    "p4-destinations": p4_destinations,
    "p4-citations": p4_citations,
    "selftest-arms": selftest_arms,
}


def main():
    if len(sys.argv) not in (2, 3):
        say("usage: check_en_r3.py <subcommand> [path] | --list | selftest-arms")
        return 2
    cmd = sys.argv[1]
    if cmd == "--list":
        for k in sorted(CMDS):
            say(k)
        return 0
    fn = CMDS.get(cmd)
    if fn is None:
        say("unknown subcommand:", cmd)
        return 2
    if len(sys.argv) == 3:
        return fn(sys.argv[2])
    return fn()


if __name__ == "__main__":
    sys.exit(main())
