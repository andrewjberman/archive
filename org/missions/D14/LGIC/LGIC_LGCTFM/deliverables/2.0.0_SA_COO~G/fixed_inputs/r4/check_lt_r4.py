"""LGIC_LGCTFM ROUND 4 -- the fixed input. Three cells, ten arms.

Round 3 built the discovery, the render and the rename, and its own drain test (S30) read the engine
NON-CONFORMANT against R-81 on both halves. Round 4 repairs those two, adds the canonical manifest entry
R-81 asks for, and THEN runs the subject for real.

FOUR CONSTRUCTION RULES, each from something this project measured rather than from principle:

1. THE COVERAGE CORES ARE IMPORTED FROM ROUND 3, NEVER RE-IMPLEMENTED. A second copy of a grading rule is
   a second thing to drift. `check_lt_r3.py` is imported by path and its cores are called here.
2. A RE-POINT MAY ADD AND MUST NOT SILENTLY REMOVE. `e6-no-loss` compares per-node_type `involved` against
   round 3's measured figures and requires every DROP to be named with the leg that used to reach it.
3. THE ROUTING LESSON IS BUILT IN (S23/S29): a contract written into a deliverables folder is named
   `*.lgctfm-contract.json` so the estate's router routes it. The arm that broke round 3 cannot recur.
4. THE STALE-PROOF BAR (S32) IS AN ARM, watching BOTH r4's and r3's fixed inputs -- because this checker
   runs r3's cores, an r3 edit moves a round-4 arm's meaning exactly as an r4 edit would.
"""

import glob
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 9)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
BASEFILE = os.path.join(HERE, "R4_BASE.json")
R3 = os.path.join(REPO, ROOT, "deliverables", "2.0.0_SA_COO~G", "fixed_inputs", "r3", "check_lt_r3.py")
MANIFEST = "org/modules/graph/graph-call-manifest.yaml"
ORDER_SHAPE = re.compile(r"RECORD SHAPE[^\n]*\n+```json\n(.*?)\n```", re.S)
REFUSED = ("comp-iam role", "comp-iam roles", "comp-iam gaps", "comp-iam services", "comp-iam stats",
           "comp-estate", "comp-routes", "comp-aws")
ALLOWED_AUTH = ("comp-iam live", "comp-iam reconcile", "comp-iam simulate")


def _scrub(t):
    return str(t).replace("VERDICT", "VERD1CT").replace("PASS-", "PASS_").replace("FAIL-", "FAIL_")


def say(tag, *lines):
    for ln in lines:
        print(ln)
    print("VERDICT: " + tag)
    return 0


def verdict(ok, p, f, lines):
    return say(p if ok else f, *lines)


def base():
    with open(BASEFILE, encoding="utf-8") as fh:
        return json.load(fh)


def load_json(p):
    try:
        with open(os.path.join(REPO, p) if not os.path.isabs(p) else p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def r3mod():
    """Round 3's checker, imported by path: its cores are the grading rule and are NOT copied here."""
    spec = importlib.util.spec_from_file_location("check_lt_r3", R3)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def manifest():
    import yaml
    with open(os.path.join(REPO, MANIFEST), encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def entries_digest(entries):
    pairs = sorted((e.get("id"), hashlib.sha1((e.get("canonical_call") or "").encode("utf-8")).hexdigest()[:12])
                   for e in entries)
    return hashlib.sha1(json.dumps(pairs, sort_keys=True).encode("utf-8")).hexdigest()


def text_of(*paths):
    out = []
    for p in paths:
        try:
            with open(os.path.join(REPO, p), encoding="utf-8") as fh:
                out.append(fh.read())
        except OSError:
            pass
    return "\n".join(out)


# ------------------------------------------------------------------ cores
# The manifest's OWN vocabulary, from its own header (`graph-call-manifest.yaml:28`,
# "status: canonical | deprecated | planned | retired"). This arm first demanded
# `active|current|live` -- THREE VALUES THE FILE HAS NEVER ADMITTED. Measured when the defect
# surfaced (LGIC_LGCTFM-W2-S35, 0.9.0_WK_LGIC_LGCTFM~2): 127 entries carry a status, 125
# `canonical` and 2 `retired`, so the accepted set's INTERSECTION WITH THE LIVE POPULATION WAS
# ZERO and no conforming entry could ever pass. A checker that invents a vocabulary grades its
# author's memory, not the estate; the values come from the file, and `retired` is a RECORD and
# never a route (CG-s-17), so it is refused HERE rather than by omission.
MANIFEST_STATUSES = ("canonical", "deprecated", "planned", "retired")
LIVE_STATUSES = ("canonical",)


def _status_is_live(v):
    return str(v or "").strip().lower() in LIVE_STATUSES


def core_entry(d, want_keys, assigned_tool):
    inv = [e for e in (d.get("entries") or []) if str(e.get("id", "")).startswith("cloud.inventory.")]
    bad = []
    if len(inv) != 1:
        return False, ["cloud.inventory.* entries: %d (exactly one canonical entry is the bar)" % len(inv)]
    e = inv[0]
    miss = [k for k in want_keys if k not in e]
    if miss:
        bad.append("entry lacks required key(s): %s" % _scrub(miss))
    if assigned_tool not in str(e.get("canonical_call", "")):
        bad.append("canonical_call does not carry the R-81-assigned instrument %r" % assigned_tool)
    if not _status_is_live(e.get("status")):
        bad.append("status %r is not a LIVE status in the manifest's OWN vocabulary %s"
                   % (_scrub(e.get("status")), _scrub(sorted(MANIFEST_STATUSES))))
    if e.get("tool") not in (d.get("tools_index") or {}):
        bad.append("tool %r is not in tools_index" % _scrub(e.get("tool")))
    return (not bad), ["entry %s | tool %s | call %s" % (_scrub(e.get("id")), _scrub(e.get("tool")),
                                                         _scrub(str(e.get("canonical_call"))[:70]))] + bad


def core_untouched(d, want_digest, want_count):
    got = entries_digest([e for e in d.get("entries") or [] if not str(e.get("id", "")).startswith("cloud.inventory.")])
    n = len(d.get("entries") or [])
    ok = got == want_digest and n == want_count + 1
    return ok, "pre-existing entries digest %s (want %s); entry count %d (want %d)" % (
        got[:12], want_digest[:12], n, want_count + 1)


def design_text(t):
    """The DESIGN half of the method note -- everything before the COMP-TOOL LEDGER.

    The ledger is an Andrew-direct artifact (msg 98038, @c9e54d5c0f) whose PURPOSE is to name
    every comp tool and say whether it was used; the three R-81-refused sources appear there and
    ONLY there, each row reading NOT USED. A whole-file substring search cannot tell "the design
    USES comp-estate" from "the ledger RECORDS that comp-estate is refused" -- so this arm made
    Andrew's ledger and its own AC1 mutually unsatisfiable, and the only passing move was to
    DELETE A TRUTHFUL RECORD. Measured when it surfaced (LGIC_LGCTFM-W1-S35,
    0.9.0_WK_LGIC_LGCTFM~1): 3 of 3 residual hits inside the ledger, 0 of 3 in any design section.
    """
    m = re.search(r"^#{2,4}\s*COMP-TOOL LEDGER", t, re.M | re.I)
    return t[:m.start()] if m else t


def core_sources(text, refused, allowed):
    text = design_text(text)
    hit = [r for r in refused if r in text]
    auth = [a for a in allowed if a in text]
    lines = ["R-81-refused discovery sources named in the design: %d %s" % (len(hit), _scrub(hit)),
             "R-81-allowed authorization instrument(s) named: %d %s" % (len(auth), _scrub(auth))]
    return (not hit and bool(auth)), lines


def core_handsurface(rec):
    hs = ((rec or {}).get("repoint") or {}).get("hand_surfaces") or []
    if not hs:
        return False, ["no hand_surfaces entry -- lambda-source-map.json is read by the source_text leg"]
    bad = []
    for h in hs:
        t = str(h.get("treatment", "")).upper()
        if t not in ("GUARDED", "DECLARED"):
            bad.append("%s: treatment %r is neither GUARDED nor DECLARED" % (_scrub(h.get("file")), _scrub(t)))
            continue
        g = h.get("guard_or_declaration")
        if t == "DECLARED":
            miss = [k for k in ("date", "owner", "un_defers_when") if not str((g or {}).get(k) or "").strip()]
            if miss:
                bad.append("%s: DECLARED without %s" % (_scrub(h.get("file")), _scrub(miss)))
        elif not str(g or "").strip():
            bad.append("%s: GUARDED with no evidence" % _scrub(h.get("file")))
    return (not bad), ["hand surfaces treated: %d" % len(hs)] + bad


def core_no_loss(new_inv, old_inv, named_drops):
    bad, lines = [], []
    for nt, old in sorted(old_inv.items()):
        new = int(new_inv.get(nt, 0))
        lines.append("  %-24s round3 %4d -> round4 %4d" % (nt, old, new))
        if new < old:
            named = len((named_drops.get(nt) or {}).get("dropped") or [])
            if named < (old - new):
                bad.append("%s DROPPED %d and the record names %d" % (nt, old - new, named))
    return (not bad), lines + bad


def core_stale(commits, rec, prior):
    """The bar is SET EQUALITY against the proofs that COULD be stale, never `> 0`.

    REPAIRED mid-round by the issuer on LGIC_ENFORCE-W1-S88, which measured the same arm one
    project over: the window opens at the ANALYSIS pin, and the commit that MINTS the fixed
    input lands after it -- so the arm counts its own creation, and the old `> 0` rule then
    demanded a re-run list where the honest list is EMPTY (nothing was pinned before the input
    existed). `> 0` made the only passing move an INVENTED proof name. `prior` is the set of
    proof instances that existed at the parent of the earliest counted commit: it is empty at a
    mint, so a mint passes with `[]`, and a real mid-round edit still refuses both an
    under-enumeration and a name that was never there to go stale.
    """
    n = len(commits)
    if n == 0:
        return True, ["fixed-input commits since the cut: 0 -- no proof can be stale against them"]
    sp = ((rec or {}).get("stale_proofs") or {})
    named = set(sp.get("proofs_re_run") or [])
    prior = set(prior or ())
    # THE COUNT IS INFORMATIONAL, NEVER THE BAR. It is CHECKOUT-DEPENDENT -- a worker measures it
    # in its own worktree and the merged tree computes a different number the moment any fixed-input
    # commit lands, including the issuer's own repairs -- so grading equality on it makes the arm
    # unsatisfiable by a record that was honest when written (LGIC_LGCTFM-W1-S38, measured: record 1,
    # merged tree 3). What must match is the SET OF PROOFS AT RISK, which is a fact about the world
    # rather than about which checkout asked.
    ok = named == prior
    lines = ["fixed-input commits since the cut: %d (informational, checkout-dependent) %s" % (n, _scrub(commits[:3])),
             "record states: %s" % _scrub(sp.get("fixed_input_commits_since_cut")),
             "proofs pinned BEFORE the earliest of them: %d -- %s" % (len(prior), _scrub(sorted(prior)) or "none"),
             "record enumerates %d re-run proof(s): %s" % (len(named), _scrub(sorted(named)) or "none")]
    if named - prior:
        lines.append("NAMED BUT NEVER AT RISK: %s" % _scrub(sorted(named - prior)))
    if prior - named:
        lines.append("AT RISK AND NOT RE-RUN: %s" % _scrub(sorted(prior - named)))
    return ok, lines


def _is_this_round(path, tag):
    """THIS round's proofs only. An earlier round's proof was graded against ITS OWN fixed input
    and is FROZEN HISTORY (R-43) -- an r4 edit cannot make an r1 proof stale, and sweeping the
    whole project makes the bar unsatisfiable in the other direction."""
    b = os.path.basename(path)
    return b.endswith("proof_of_spec.json") and ".TO-" in b and ("-%s." % tag) in b


def proofs_at_risk(commits):
    """This round's proof instances that existed at the parent of the EARLIEST counted commit."""
    if not commits:
        return set()
    oldest = commits[-1].split()[0]
    tag = os.path.basename(HERE)
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", "%s^" % oldest, "--", ROOT],
                       cwd=REPO, capture_output=True, timeout=120)
    if r.returncode != 0:
        return set()
    return set(ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines()
               if _is_this_round(ln, tag))


# ------------------------------------------------------------------ arms
def m1_entry():
    b = base()
    try:
        d = manifest()
    except Exception as exc:
        return say("FAIL-M1-ENTRY", "manifest unreadable: %s" % _scrub(exc))
    ok, lines = core_entry(d, b["manifest_baseline"]["required_entry_keys"], b["r81_assignment"]["inventory"])
    return verdict(ok, "PASS-M1-ENTRY", "FAIL-M1-ENTRY", lines)


def m1_untouched():
    b = base()
    try:
        d = manifest()
    except Exception as exc:
        return say("FAIL-M1-UNTOUCHED", "manifest unreadable: %s" % _scrub(exc))
    ok, line = core_untouched(d, b["manifest_baseline"]["entries_digest_sha1_of_id_plus_call"],
                              b["manifest_baseline"]["entries"])
    return verdict(ok, "PASS-M1-UNTOUCHED", "FAIL-M1-UNTOUCHED", [line])


def e6_sources():
    b = base()
    txt = text_of("infra/logic/10_LEGACY_TRANSFORM.md")
    c = load_json(b["the_routing_lesson"]["e6_walk_output"])
    txt += "\n" + json.dumps((c or {}).get("coverage") or {})
    ok, lines = core_sources(txt, REFUSED, ALLOWED_AUTH)
    return verdict(ok, "PASS-E6-SOURCES", "FAIL-E6-SOURCES",
                   ["read: the method note plus the new contract's coverage block"] + lines)


def e6_handsurface():
    b = base()
    ok, lines = core_handsurface(load_json(b["record_shape"]["paths"]["LT-e-6"]))
    return verdict(ok, "PASS-E6-HANDSURFACE", "FAIL-E6-HANDSURFACE", lines)


def e6_coverage():
    """Round 3's own cores, run against the round-4 walk output."""
    b = base()
    m = r3mod()
    c = load_json(b["the_routing_lesson"]["e6_walk_output"])
    if c is None:
        return say("FAIL-E6-COVERAGE", "no contract at %s" % b["the_routing_lesson"]["e6_walk_output"])
    names, _meta, note = m.floor_now(m.base())
    if names is None:
        return say("FAIL-E6-COVERAGE", note)
    ok1, l1 = m.core_cov_shape(c, list(names))
    ok2, l2 = m.core_cov_floor(c, names)
    ok3, l3 = m.core_cov_named(c, names, m.base()["named_classes"]["classes"])
    return verdict(ok1 and ok2 and ok3, "PASS-E6-COVERAGE", "FAIL-E6-COVERAGE",
                   [note, "(cores imported from check_lt_r3.py, never re-implemented)"] + l1 + l2 + l3)


def e6_no_loss():
    b = base()
    c = load_json(b["the_routing_lesson"]["e6_walk_output"])
    rec = load_json(b["record_shape"]["paths"]["LT-e-6"]) or {}
    if c is None:
        return say("FAIL-E6-NO-LOSS", "no contract at the walk output")
    new = {k: (v or {}).get("involved", 0) for k, v in ((c.get("coverage") or {}).get("by_node_type") or {}).items()}
    ok, lines = core_no_loss(new, b["round3_coverage_to_beat"]["involved_by_node_type"],
                             (rec.get("coverage_delta") or {}).get("by_node_type") or {})
    return verdict(ok, "PASS-E6-NO-LOSS", "FAIL-E6-NO-LOSS", lines)


def _newest_run(b):
    subj = b["subject"]["run_home_subject"]
    cut = b["cut_at"].replace("-", "").replace(":", "").replace("Z", "")[:13]
    runs = []
    for d in glob.glob(os.path.join(REPO, "workflows", "legacy_transform", subj, "*")):
        mm = re.match(r"^(\d{8}T\d{6})Z-[0-9a-f]+$", os.path.basename(d))
        if mm and mm.group(1) > cut + "00" and os.path.isfile(os.path.join(d, "HASHES.json")):
            runs.append((mm.group(1), d))
    runs.sort()
    return (runs[-1][1] if runs else None), len(runs)


def x4_run():
    b = base()
    m = r3mod()
    d, n = _newest_run(b)
    if not d:
        return say("FAIL-X4-RUN", "no post-cut run with HASHES.json under the run home (%d found)" % n)
    ok_r, l1 = m.receiving_accept(os.path.join(d, "contract.json"))
    c = load_json(os.path.join(d, "contract.json"))
    ok_s, lines = m.core_cov_shape(c or {}, list(m.base()["floor"]["by_node_type"]))
    return verdict(ok_r and ok_s, "PASS-X4-RUN", "FAIL-X4-RUN",
                   ["run: %s (%d post-cut)" % (os.path.relpath(d, REPO), n), l1] + lines)


def x4_floor():
    b = base()
    m = r3mod()
    d, _n = _newest_run(b)
    c = load_json(os.path.join(d, "contract.json")) if d else None
    if c is None:
        return say("FAIL-X4-FLOOR", "no post-cut run contract")
    names, _meta, note = m.floor_now(m.base())
    if names is None:
        return say("FAIL-X4-FLOOR", note)
    ok1, l1 = m.core_cov_floor(c, names)
    ok2, l2 = m.core_cov_named(c, names, m.base()["named_classes"]["classes"])
    return verdict(ok1 and ok2, "PASS-X4-FLOOR", "FAIL-X4-FLOOR", [note] + l1 + ["named classes:"] + l2)


def x4_no_registry_move():
    b = base()
    paths = ["infra/logic/registry/", "org/missions/D14/LGIC/LGIC_NAMING/deliverables/LEGACY_SERVED_PATHS.json"]
    r = subprocess.run(["git", "diff", "--name-only", b["cut_pin"], "HEAD", "--"] + paths,
                       cwd=REPO, capture_output=True, timeout=120)
    changed = [ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines() if ln.strip()]
    r2 = subprocess.run(["git", "cat-file", "-e", b["cut_pin"] + "^{commit}"], cwd=REPO, capture_output=True, timeout=60)
    return verdict(r.returncode == 0 and r2.returncode == 0 and not changed,
                   "PASS-X4-NO-REGISTRY-MOVE", "FAIL-X4-NO-REGISTRY-MOVE",
                   ["registries + LEGACY_SERVED_PATHS since %s: %d path(s) changed (pin resolvable=%s)"
                    % (b["cut_pin"][:10], len(changed), r2.returncode == 0)] + changed)


def r4_stale_proofs():
    b = base()
    out = []
    for p in b["stale_proof_bar"]["watched_paths"]:
        r = subprocess.run(["git", "log", "--format=%h %s", "%s..HEAD" % b["cut_pin"], "--", p],
                           cwd=REPO, capture_output=True, timeout=120)
        out += [ln for ln in (r.stdout or b"").decode("utf-8", "replace").splitlines() if ln.strip()]
    rec = None
    for p in b["record_shape"]["paths"].values():
        rec = rec or load_json(p)
    ok, lines = core_stale(out, rec, proofs_at_risk(out))
    return verdict(ok, "PASS-R4-STALE-PROOFS", "FAIL-R4-STALE-PROOFS", lines)


# ------------------------------------------------------------------ selftest
def selftest_arms():
    b = base()
    res = []

    def arm(n, ok, why=""):
        res.append((n, bool(ok), why))

    keys = b["manifest_baseline"]["required_entry_keys"]
    tool = b["r81_assignment"]["inventory"]
    good = {"tools_index": {"comp-find": {}}, "entries": [dict({k: "x" for k in keys}, **{
        "id": "cloud.inventory.subject_composition", "tool": "comp-find", "status": "canonical",
        "canonical_call": "comp-find --corpus aws '\\b<token>\\b' --all"})]}
    arm("POSITIVE-entry", core_entry(good, keys, tool)[0], "one canonical entry, assigned instrument")
    two = {"tools_index": {"comp-find": {}}, "entries": good["entries"] + [dict(good["entries"][0], id="cloud.inventory.other")]}
    arm("MUTANT-entry-two", not core_entry(two, keys, tool)[0], "two canonical entries -> FAIL")
    wrongtool = {"tools_index": {"comp-find": {}}, "entries": [dict(good["entries"][0], canonical_call="comp-estate --layers")]}
    arm("MUTANT-entry-wrong-instrument", not core_entry(wrongtool, keys, tool)[0])
    arm("MUTANT-entry-missing-key", not core_entry(
        {"tools_index": {"comp-find": {}}, "entries": [{k: "x" for k in keys if k != "freshness"}]}, keys, tool)[0])

    src = [{"id": "a", "canonical_call": "x"}, {"id": "b", "canonical_call": "y"}]
    dig = entries_digest(src)
    arm("POSITIVE-untouched", core_untouched({"entries": src + [{"id": "cloud.inventory.z", "canonical_call": "n"}]},
                                             dig, len(src))[0])
    arm("MUTANT-untouched-edited", not core_untouched(
        {"entries": [{"id": "a", "canonical_call": "CHANGED"}, src[1], {"id": "cloud.inventory.z", "canonical_call": "n"}]},
        dig, len(src))[0], "an existing call edited -> FAIL")

    arm("POSITIVE-sources", core_sources("the leg reads comp-iam live", REFUSED, ALLOWED_AUTH)[0])
    arm("MUTANT-sources-refused", not core_sources("comp-iam live and comp-iam role", REFUSED, ALLOWED_AUTH)[0])
    arm("MUTANT-sources-no-auth", not core_sources("comp-kuzu only", REFUSED, ALLOWED_AUTH)[0])

    decl = {"repoint": {"hand_surfaces": [{"file": "lambda-source-map.json", "treatment": "DECLARED",
                                           "guard_or_declaration": {"date": "2026-09-19", "owner": "x",
                                                                    "un_defers_when": "y"}}]}}
    arm("POSITIVE-handsurface-declared", core_handsurface(decl)[0])
    arm("POSITIVE-handsurface-guarded", core_handsurface(
        {"repoint": {"hand_surfaces": [{"file": "f", "treatment": "GUARDED", "guard_or_declaration": "comp-lambdamap run"}]}})[0])
    arm("MUTANT-handsurface-partial", not core_handsurface(
        {"repoint": {"hand_surfaces": [{"file": "f", "treatment": "DECLARED",
                                        "guard_or_declaration": {"date": "d", "owner": "o"}}]}})[0], "no un_defers_when")
    arm("MUTANT-handsurface-absent", not core_handsurface({"repoint": {}})[0])

    old = {"LAMBDA": 67, "SCHEDULE": 9}
    arm("POSITIVE-no-loss-grew", core_no_loss({"LAMBDA": 70, "SCHEDULE": 9}, old, {})[0])
    arm("MUTANT-no-loss-silent-drop", not core_no_loss({"LAMBDA": 60, "SCHEDULE": 9}, old, {})[0])
    arm("POSITIVE-no-loss-named", core_no_loss({"LAMBDA": 66, "SCHEDULE": 9}, old,
                                               {"LAMBDA": {"dropped": [{"name": "x", "old_leg": "iam_grant"}]}})[0],
        "a drop NAMED with its old leg is admissible")

    arm("POSITIVE-status-canonical", _status_is_live("canonical"),
        "125 of the manifest's 127 statuses; the value its own schema and NFRA_GRAPHS AC1 require")
    arm("MUTANT-status-retired", not _status_is_live("retired"),
        "a retired entry is a RECORD, not a route (CG-s-17)")
    arm("MUTANT-status-invented", not (_status_is_live("active") or _status_is_live("live")),
        "the values this arm used to demand: never in the file's vocabulary, intersection 0 with 127 live entries (W2-S35)")

    _led = ("## Walk order\nuse comp-kuzu and comp-iam reconcile\n\n"
            "### COMP-TOOL LEDGER\n| 3 | comp-estate | NOT USED -- refused |\n")
    arm("POSITIVE-sources-ledger-names-refused", core_sources(_led, REFUSED, ALLOWED_AUTH)[0],
        "the ledger MUST name every refused tool (Andrew-direct msg 98038); naming one there is not using it")
    arm("MUTANT-sources-in-design", not core_sources(
        "## Plan\nread the roles with comp-estate\n\n### COMP-TOOL LEDGER\n| 1 | comp-kuzu | used |\n",
        REFUSED, ALLOWED_AUTH)[0], "a refused source in a DESIGN section still fails")

    arm("POSITIVE-stale-none", core_stale([], None, set())[0])
    arm("POSITIVE-stale-count-moves", core_stale(
        ["a x", "b y", "c z"], {"stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": []}},
        set())[0], "an honest record whose checkout counted 1 while this one counts 3 still PASSES: the SET is the bar (W1-S38)")
    _one = {"stale_proofs": {"fixed_input_commits_since_cut": 1, "proofs_re_run": []}}
    arm("POSITIVE-stale-mint", core_stale(["abc mint"], _one, set())[0],
        "the commit that MINTS the fixed input puts NO proof at risk -- [] is the honest answer (W1-S88)")
    arm("MUTANT-stale-unenumerated", not core_stale(["abc x"], _one, {"a/p.proof_of_spec.json"})[0])
    arm("MUTANT-stale-invented", not core_stale(
        ["abc x"], {"stale_proofs": {"fixed_input_commits_since_cut": 1,
                                     "proofs_re_run": ["never/existed.proof_of_spec.json"]}}, set())[0],
        "a name that was never at risk cannot buy a PASS -- the repair's own back door")
    arm("POSITIVE-stale-this-round", _is_this_round("d/LGIC_LGCTFM.TO-LT-m-1-r4.x.proof_of_spec.json", "r4"))
    arm("MUTANT-stale-frozen-round", not _is_this_round(
        "d/LGIC_LGCTFM.TO-LT-e-1-r1.walk.proof_of_spec.json", "r4"),
        "an r1 proof is frozen history (R-43): an r4 edit cannot make it stale")
    arm("MUTANT-scrub", "VERDICT: PASS-" not in _scrub("VERDICT: PASS-M1-ENTRY"))

    try:
        m = r3mod()
        arm("R3-CORES-IMPORTABLE", all(hasattr(m, n) for n in
                                       ("core_cov_shape", "core_cov_floor", "core_cov_named", "floor_now",
                                        "receiving_accept", "base")),
            "round 3's cores are the grading rule and are imported, not copied")
    except Exception as exc:
        arm("R3-CORES-IMPORTABLE", False, _scrub(exc))

    want = b["record_shape"]["shape"]
    orders = sorted(glob.glob(os.path.join(REPO, ROOT, "task-orders", "LGIC_LGCTFM.TO-LT-*-r4.*.md")))
    quoting = 0
    for op in orders:
        with open(op, encoding="utf-8") as fh:
            mm = ORDER_SHAPE.search(fh.read())
        if mm:
            quoting += 1
            try:
                got = json.loads(mm.group(1))
            except ValueError:
                got = None
            arm("S85-order-quotes-carrier:" + os.path.basename(op)[len("LGIC_LGCTFM.TO-"):][:16], got == want)
    arm("S85-every-order-quotes", quoting == len(orders), "%d of %d round-4 order(s)" % (quoting, len(orders)))

    for n, ok, why in res:
        print("  %-42s %s  %s" % (n, "PASS" if ok else "FAIL", _scrub(why)))
    pos = sum(1 for n, _o, _w in res if n.startswith("POSITIVE-"))
    print("arms driven: %d (%d POSITIVE-SATISFIABILITY, %d mutant/other)" % (len(res), pos, len(res) - pos))
    print("NOT driven here, stated: floor_now(), receiving_accept() and the git/yaml reads -- live calls with no "
          "fixture, exercised by the real arms, which print their own denominators.")
    print("VERDICT: " + ("PASS-ARMS-DISCRIMINATE" if all(o for _n, o, _w in res) else "FAIL-ARMS-DO-NOT-DISCRIMINATE"))
    return 0


CMDS = {"m1-entry": m1_entry, "m1-untouched": m1_untouched, "e6-sources": e6_sources,
        "e6-handsurface": e6_handsurface, "e6-coverage": e6_coverage, "e6-no-loss": e6_no_loss,
        "x4-run": x4_run, "x4-floor": x4_floor, "x4-no-registry-move": x4_no_registry_move,
        "r4-stale-proofs": r4_stale_proofs, "selftest-arms": selftest_arms}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("known: %s" % ", ".join(sorted(CMDS)))
        print("VERDICT: FAIL-NO-SUCH-SUBCOMMAND")
        return 0
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
