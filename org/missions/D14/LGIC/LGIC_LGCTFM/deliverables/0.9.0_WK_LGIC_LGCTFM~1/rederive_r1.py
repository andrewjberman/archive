"""LT-a-2's INSTRUMENT: re-derive round 1's fourteen judgment claims from a THIRD POSITION.

This file is the `instrument_path` of RE_DERIVATION_R2.json and it is TRACKED for that reason
(row LGIC_ENFORCE-S69: a record whose second reader is an untracked scratch file has an
unverifiable claim at its centre, and the drain deletes the evidence as routine hygiene).

It grades nothing and it edits nothing. Three subcommands:

  position    what checkout this is -- the THIRD POSITION the record declares (branch, HEAD,
              worktree path, and the round-1 worker branches it is NOT).
  mechanism   THE UNSCOPED CENSUS, and it is deliberately a DIFFERENT INSTRUMENT from the one
              that found the silent pair. Row LGIC_LGCTFM-S18 found x2-flag and x3-filed by
              GREPPING one helper name (`base_ref()`) in check_lt_r1.py. This walks the AST of
              that file, builds the whole call graph, and asks of EVERY arm in its own
              SUBCOMMANDS table -- the printed denominator, never a remembered list -- which
              POSITION-RELATIVE PRIMITIVES it transitively reaches. A grep of one helper cannot
              see an arm that reaches the same class through a different helper; a closure over
              the denominator can, and the classes it reports are then inspected by hand.
  probes      Per round-1 judgment criterion, re-run the invocation THAT CLAIM'S OWN EVIDENCE
              names, from here, and print the deciding line verbatim with its rc. `--only <id>`
              bounds one criterion per call.

ASCII only. LF endings.
"""
from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys

# 7 levels: ~1 / deliverables / LGIC_LGCTFM / LGIC / D14 / missions / org
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 7)))
ROOT = "org/missions/D14/LGIC/LGIC_LGCTFM"
R1CHECK = ROOT + "/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_lt_r1.py"
W1 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~1"
W2 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~2"
W3 = ROOT + "/deliverables/0.9.0_WK_LGIC_LGCTFM~3"
SUBJECT = "workflows/legacy_transform/blackdiamond-49financial"


def ab(path):
    return path if os.path.isabs(path) else os.path.join(REPO, path)


def run(argv, timeout=240):
    try:
        res = subprocess.run(argv, capture_output=True, text=True, cwd=REPO, timeout=timeout)
        return res.returncode, (res.stdout or "") + (res.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT after %ds -- rc 124 IS the recorded output" % timeout
    except Exception as exc:  # noqa: BLE001
        return 1, "%s: %s" % (type(exc).__name__, exc)


def git(*args):
    return run(["git"] + list(args), timeout=120)


def deciding(out, tokens=("VERDICT", "PASS-", "FAIL-")):
    """The one line a reader grades on: the last line carrying a verdict token, else the last line."""
    lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
    hits = [ln for ln in lines if any(t in ln for t in tokens)]
    if hits:
        return hits[-1]
    return lines[-1] if lines else "<no output>"


# ================================================================================ position
def position():
    rc1, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    rc2, head = git("rev-parse", "HEAD")
    rc3, wts = git("worktree", "list")
    rc4, top = git("rev-parse", "--show-toplevel")
    print("branch                : %s (rc=%d)" % (branch.strip(), rc1))
    print("HEAD                  : %s (rc=%d)" % (head.strip(), rc2))
    print("worktree toplevel     : %s (rc=%d)" % (top.strip(), rc4))
    print("REPO as this file sees: %s" % REPO.replace(os.sep, "/"))
    print("linked worktrees (rc=%d):" % rc3)
    for ln in wts.splitlines():
        print("  " + ln.rstrip())
    rc5, branches = git("branch", "--list", "wk-lgic-lgctfm*")
    print("round-1/2 worker branches this checkout is NOT (rc=%d):" % rc5)
    for ln in branches.splitlines():
        print("  " + ln.rstrip())
    return 0


# ================================================================================ mechanism census
# The PRIMITIVE classes. Each is a property of the INVOKING CHECKOUT rather than of the cell a
# criterion is about, so an arm that reaches one grades WHERE IT RAN as well as WHAT IT READ.
AMBIENT_REF = "AMBIENT-REF: a git ref resolved from the invoking checkout (HEAD / CLOUD / merge-base)"
AMBIENT_TREE = "AMBIENT-TREE: the invoking worktree's own uncommitted state (git status)"
DIR_POSITION = "DIR-POSITION: a subject resolved BY POSITION in a directory many runs share"
DIR_LISTING = "DIR-LISTING: a denominator taken from os.listdir of a shared directory"


def _calls(node):
    names = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            fn = sub.func
            if isinstance(fn, ast.Name):
                names.add(fn.id)
            elif isinstance(fn, ast.Attribute):
                names.add(fn.attr)
    return names


def _literals(node):
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.add(sub.value)
    return out


def _direct_primitives(fn):
    """Which primitive classes does THIS function body touch directly?"""
    got = set()
    lits = _literals(fn)
    calls = _calls(fn)
    if "git" in calls and ({"merge-base", "HEAD", "CLOUD"} & lits or
                           any(lit.endswith("..HEAD") or "%s..HEAD" in lit for lit in lits)):
        got.add(AMBIENT_REF)
    if "git" in calls and "status" in lits:
        got.add(AMBIENT_TREE)
    if "listdir" in calls:
        got.add(DIR_LISTING)
    return got


def _subcommand_table(tree):
    """The DENOMINATOR: the arms the checker itself dispatches, read from its own SUBCOMMANDS dict."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "SUBCOMMANDS" and isinstance(node.value, ast.Dict):
                    table = {}
                    for key, val in zip(node.value.keys, node.value.values):
                        if isinstance(key, ast.Constant) and isinstance(val, ast.Name):
                            table[key.value] = val.id
                    return table
    return {}


def mechanism():
    src = open(ab(R1CHECK), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            funcs[node.name] = node
    direct = {name: _direct_primitives(fn) for name, fn in funcs.items()}
    # DIR-POSITION is an INDEXED read of a listing -- the two helpers that do it, found by their
    # own bodies (a subscript over the value a listdir-bearing helper returned), not by name.
    for name, fn in funcs.items():
        if DIR_LISTING not in direct[name] and not any(
                isinstance(s, ast.Subscript) for s in ast.walk(fn)):
            continue
        calls = _calls(fn)
        indexed = any(isinstance(s, ast.Subscript) for s in ast.walk(fn))
        if indexed and (DIR_LISTING in direct[name] or "subject_runs" in calls):
            direct[name].add(DIR_POSITION)
    edges = {name: (_calls(fn) & set(funcs)) for name, fn in funcs.items()}

    def closure(name, seen=None):
        seen = seen or set()
        if name in seen:
            return set()
        seen.add(name)
        got = set(direct.get(name, ()))
        for callee in edges.get(name, ()):
            got |= closure(callee, seen)
        return got

    table = _subcommand_table(tree)
    print("DENOMINATOR, printed and read from the checker's OWN dispatch table:")
    print("  functions parsed          : %d" % len(funcs))
    print("  arms in SUBCOMMANDS       : %d" % len(table))
    reach = {}
    for arm, fname in sorted(table.items()):
        got = closure(fname)
        if got:
            reach[arm] = sorted(got)
    print("  arms reaching NO position-relative primitive: %d" % (len(table) - len(reach)))
    print("  arms reaching AT LEAST ONE                  : %d" % len(reach))
    for cls in (AMBIENT_REF, AMBIENT_TREE, DIR_POSITION, DIR_LISTING):
        arms = sorted(a for a, v in reach.items() if cls in v)
        print("")
        print("%s" % cls)
        print("  arms: %d of %d  %s" % (len(arms), len(table), arms))
    print("")
    print("PER-ARM detail (arms with at least one class):")
    for arm in sorted(reach):
        print("  %-18s %s" % (arm, [c.split(":")[0] for c in reach[arm]]))
    return 0


# ================================================================================ probes
# (criterion, label, kind, args) -- kind in {pin, arm, jsonlen, filegrep, cmd, lines}
PROBES = (
    ("D1R1-AC3", "the removed sort at the cited pin", "pin",
     ("9b628270a1", "lib/opal_lgctfm.py", "distinct = sorted(set(members))")),
    # The claim's prose names `build_row's kind="FORK" dict at :914-921`. The LINE RANGE is right and
    # the FORK dict is there; the ENCLOSING FUNCTION named in the citation is not -- build_row() is at
    # :416 and the dict at :915 is an inline literal inside cmd_forks() (:804). The needle here is the
    # bytes as the file actually spells them, and the first form tried (`kind="FORK"`, the citation's
    # own spelling) read ABSENT -- a wrong-object read, not a missing blob.
    ("D1R1-AC3", "the FORK dict at the cited pin, as spelled", "pin",
     ("9b628270a1", "lib/opal_lgctfm.py", '"kind": "FORK"')),
    ("D1R1-AC3", "the function the citation names, at that pin", "pin",
     ("9b628270a1", "lib/opal_lgctfm.py", "def build_row(")),
    ("D1R1-AC3", "the pinned input's :leaf seeds at the cited pin", "pin",
     ("2deeff1764", "lib/tests/test_opal_lgctfm.py", ":leaf")),
    ("D1R1-AC3", "the cell's own arm", "arm", ("d1-negative-first",)),
    ("D1R1-AC3", "the cell's own arm", "arm", ("d1-pytest",)),

    ("E1R1-AC9", "walk order section in the method doc", "filegrep",
     ("infra/logic/10_LEGACY_TRANSFORM.md", "Walk order")),
    ("E1R1-AC9", "coverage hole section in the method doc", "filegrep",
     ("infra/logic/10_LEGACY_TRANSFORM.md", "Coverage hole")),
    ("E1R1-AC9", "the plant's cited instrument text", "filegrep",
     (W1 + "/walk/PLANT.json", "NOT scanned")),
    ("E1R1-AC9", "the cell's own arms", "arm", ("e1-method",)),
    ("E1R1-AC9", "the cell's own arms", "arm", ("e1-cells",)),
    ("E1R1-AC9", "the cell's own arms", "arm", ("e1-plant",)),
    ("E1R1-AC9", "the cell's own arms", "arm", ("e1-control",)),

    ("E2R1-AC5", "seeds are storage locations", "jsonlen", (W1 + "/forks/SEEDS.json", "seeds")),
    ("E2R1-AC5", "the engine never opens FORK_CONTROLS", "filegrep",
     ("lib/opal_lgctfm.py", "FORK_CONTROLS")),
    ("E2R1-AC5", "the cell's own arms", "arm", ("e2-forks",)),
    ("E2R1-AC5", "the cell's own arms", "arm", ("e2-negative",)),
    ("E2R1-AC5", "the cell's own arms", "arm", ("e2-reproduce",)),

    ("E3R1-AC6", "the population the claim cites", "jsonlen",
     (W1 + "/walk/contract.json", "tensions")),
    ("E3R1-AC6", "the cited sample tension", "filegrep", (W1 + "/walk/contract.json", "T-0271")),
    ("E3R1-AC6", "irreversible read from the canon's words", "filegrep",
     ("infra/logic/02_DOCTRINE.md", "renames authorized")),
    ("E3R1-AC6", "the cell's own arms", "arm", ("e3-factors",)),
    ("E3R1-AC6", "the cell's own arms", "arm", ("e3-order",)),
    ("E3R1-AC6", "the cell's own arms", "arm", ("e3-rule",)),

    ("E4R1-AC9", "the flag's declaration", "filegrep", ("lib/opal_lgctfm.py", "--plant-untypeable")),
    ("E4R1-AC9", "the flag's default", "filegrep", ("lib/opal_lgctfm.py", "plant_untypeable")),
    ("E4R1-AC9", "the cell's own arms", "arm", ("a4-plant-off",)),
    ("E4R1-AC9", "the cell's own arms", "arm", ("a4-flag-on",)),
    ("E4R1-AC9", "the cell's own arms", "arm", ("a4-count-typed",)),

    ("H1R1-AC5", "cmd_manifest at the cited pin", "pin",
     ("c0889dfd7e", "workflows/legacy_transform/run_home.py", "_iter_runs")),
    ("H1R1-AC5", "the README's never-overwrite words at the cited pin", "pin",
     ("c0889dfd7e", "workflows/legacy_transform/README.md", "never overwritten")),
    ("H1R1-AC5", "the README's identity key at the cited pin", "pin",
     ("c0889dfd7e", "workflows/legacy_transform/README.md", "keyed on identity")),
    ("H1R1-AC5", "the cell's own arms", "arm", ("h1-manifest",)),
    ("H1R1-AC5", "the cell's own arms", "arm", ("h1-no-overwrite",)),

    ("P1R1-AC6", "the sampled row in the run's own contract", "filegrep",
     (W2 + "/plan_r1/contract.json", "R-0221")),
    ("P1R1-AC6", "the sampled package", "filegrep", (W2 + "/plan_r1/plan.json", "R-0221-PORT")),
    ("P1R1-AC6", "the cell's own arms", "arm", ("p1-fields",)),
    ("P1R1-AC6", "the cell's own arms", "arm", ("p1-served",)),
    ("P1R1-AC6", "the cell's own arms", "arm", ("p1-r19",)),

    ("R1R1-AC5", "the renderer at the cited pin", "pin",
     ("d795f75122", "lib/lgctfm_render.py", "TRIGGERS")),
    ("R1R1-AC5", "the house-style document the claim is graded against", "lines",
     (".claude/skills/draw/SKILL.md",)),
    ("R1R1-AC5", "DEC-7's cited lines", "filegrep", (ROOT + "/prd/LGIC_LGCTFM_PRD.md", "DEC-7")),
    ("R1R1-AC5", "the cell's own arms", "arm", ("r1-identical",)),
    ("R1R1-AC5", "the cell's own arms", "arm", ("r1-edit",)),

    ("S1R1-AC7", "the record at the cited pin", "pin",
     ("e2daf62f07", W1 + "/CONTRACT_SCHEMA_RULE24.md", "uncovered")),
    ("S1R1-AC7", "the schema at the cited pin", "pin",
     ("e2daf62f07", "org/standards/LGCTFM_CONTRACT.schema.json", "fork_row")),
    ("S1R1-AC7", "the cell's own arms", "arm", ("s1-valid",)),
    ("S1R1-AC7", "the cell's own arms", "arm", ("s1-enums",)),
    ("S1R1-AC7", "the cell's own arms", "arm", ("s1-node-types",)),

    ("S2R1-AC8", "the owning tool at the cited pin", "pin",
     ("4ad93b7166", ".tools/lgctfm-contract-check.py", "vintage")),
    ("S2R1-AC8", "the ROUTES table at the cited pin", "pin",
     ("4ad93b7166", ".tools/receiving-check.py", "ROUTES")),
    ("S2R1-AC8", "the schema at the second cited pin", "pin",
     ("ef8197ed07", "org/standards/LGCTFM_CONTRACT.schema.json", "properties")),
    ("S2R1-AC8", "the cell's own arms", "arm", ("s2-selftest",)),
    ("S2R1-AC8", "the cell's own arms", "arm", ("s2-accept-valid",)),
    ("S2R1-AC8", "the cell's own arms", "arm", ("s2-unchecked",)),

    ("V1R1-AC5", "the sample at the cited pin", "pin",
     ("a5cef2724f", W3 + "/REPRODUCTION.json", "grade")),
    ("V1R1-AC5", "the card at the cited pin", "pin",
     ("a5cef2724f", W3 + "/ANDREW_CARD.md", "RECOMMENDATION")),
    ("V1R1-AC5", "the card as it stands now", "filegrep", (W3 + "/ANDREW_CARD.md", "RECOMMENDATION")),
    ("V1R1-AC5", "the cell's own arms", "arm", ("v1-reproduced",)),
    ("V1R1-AC5", "the cell's own arms", "arm", ("v1-order",)),
    ("V1R1-AC5", "the cell's own arms", "arm", ("v1-card",)),

    ("X1R1-AC6", "the live-plane record of the window", "filegrep",
     (SUBJECT + "/20260918T011619Z-8db9eb1/FWD10.json", "built")),
    ("X1R1-AC6", "the cell's own arms", "arm", ("x1-fwd10",)),
    ("X1R1-AC6", "the cell's own arms", "arm", ("x1-hashes",)),
    ("X1R1-AC6", "the cell's own arms", "arm", ("x1-footprint",)),
    ("X1R1-AC6", "the cell's own arms", "arm", ("x1-r16",)),
    ("X1R1-AC6", "the live plane AS IT READS NOW (the window cannot be re-taken)", "cmd",
     ("comp-find", "opal-data-bd|opal-data-49financial", "--corpus", "aws", "--files")),

    ("X2R1-AC4", "the planted addition itself", "filegrep",
     (W3 + "/PLANTED_REFUSAL/add.diff", "bd_gold_accounts_dimension_e12_strict")),
    ("X2R1-AC4", "the file the addition is a sibling in", "lines",
     ("data/black_diamond/scripts/gold/gold_freshness_config.yaml",)),
    ("X2R1-AC4", "the cell's own arms", "arm", ("x2-adding",)),
    ("X2R1-AC4", "the cell's own arms", "arm", ("x2-removing",)),
    ("X2R1-AC4", "the cell's own arms", "arm", ("x2-flag",)),

    ("X3R1-AC5", "the DIFF.md the claim names, by run id", "filegrep",
     (SUBJECT + "/20260918T002711Z-caf0983/DIFF.md", "R-0185|A3|GRAMMAR|R1")),
    ("X3R1-AC5", "its UNCHANGED count", "filegrep",
     (SUBJECT + "/20260918T002711Z-caf0983/DIFF.md", "UNCHANGED: 179")),
    ("X3R1-AC5", "the cell's own arms", "arm", ("x3-two-runs",)),
    ("X3R1-AC5", "the cell's own arms", "arm", ("x3-diff",)),
    ("X3R1-AC5", "the cell's own arms", "arm", ("x3-nontrivial",)),
    ("X3R1-AC5", "the cell's own arms", "arm", ("x3-filed",)),
)


def _probe_pin(commit, path, needle):
    rc, out = git("cat-file", "-p", "%s:%s" % (commit, path))
    if rc != 0:
        return rc, "BLOB UNREACHABLE at %s:%s -- git rc=%d %s" % (commit, path, rc, out.strip()[:120])
    lines = out.splitlines()
    hits = [(i + 1, ln) for i, ln in enumerate(lines) if needle in ln]
    if not hits:
        return 1, ("blob reachable (%d lines) but the cited bytes %r are ABSENT at that vintage"
                   % (len(lines), needle))
    return 0, ("blob reachable (%d lines); %r occurs %d time(s); first at :%d -- %s"
               % (len(lines), needle, len(hits), hits[0][0], hits[0][1].strip()[:120]))


def _probe_filegrep(path, needle):
    p = ab(path)
    if not os.path.isfile(p):
        return 1, "ABSENT in this checkout: %s" % path
    raw = open(p, "rb").read().decode("utf-8", "replace")
    lines = raw.splitlines()
    hits = [(i + 1, ln) for i, ln in enumerate(lines) if needle in ln]
    if not hits:
        return 1, "%d lines; %r occurs 0 time(s)" % (len(lines), needle)
    return 0, ("%d lines; %r occurs %d time(s); first at :%d -- %s"
               % (len(lines), needle, len(hits), hits[0][0], hits[0][1].strip()[:120]))


def _probe_jsonlen(path, key):
    p = ab(path)
    if not os.path.isfile(p):
        return 1, "ABSENT in this checkout: %s" % path
    try:
        doc = json.load(open(p, encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return 1, "unparseable: %s" % exc
    val = doc.get(key)
    if isinstance(val, list):
        return 0, "%s[%r] carries %d entries" % (os.path.basename(path), key, len(val))
    return 1, "%s[%r] is %s, not a list" % (os.path.basename(path), key, type(val).__name__)


def _probe_lines(path):
    p = ab(path)
    if not os.path.isfile(p):
        rc, out = git("ls-files", "--error-unmatch", path)
        return 1, ("ABSENT in this checkout; git ls-files rc=%d (%s)"
                   % (rc, "tracked" if rc == 0 else "not tracked either"))
    raw = open(p, "rb").read().decode("utf-8", "replace")
    return 0, "present, %d lines, %d bytes" % (len(raw.splitlines()), len(raw))


def _probe_arm(arm):
    rc, out = run([sys.executable, ab(R1CHECK), arm], timeout=300)
    return rc, deciding(out)


def _probe_cmd(*argv):
    rc, out = run(list(argv), timeout=240)
    return rc, deciding(out, tokens=("built:", "hit(s)", "denominator", "scanned"))


def probes(only=None):
    done = 0
    for crit, label, kind, args in PROBES:
        if only and crit != only:
            continue
        if kind == "pin":
            rc, line = _probe_pin(*args)
        elif kind == "filegrep":
            rc, line = _probe_filegrep(*args)
        elif kind == "jsonlen":
            rc, line = _probe_jsonlen(*args)
        elif kind == "lines":
            rc, line = _probe_lines(*args)
        elif kind == "arm":
            rc, line = _probe_arm(*args)
        elif kind == "cmd":
            rc, line = _probe_cmd(*args)
        else:
            rc, line = 1, "unknown probe kind %r" % kind
        done += 1
        print("%-10s | %-6s | %-44s | rc=%-4d| %s" % (crit, kind, label[:44], rc, line))
    print("probes run: %d of %d in the table%s" % (done, len(PROBES),
                                                   (" (filtered to %s)" % only) if only else ""))
    return 0


def denominator():
    """THE CONTROL ON THE POPULATION: read the judgment criteria from the ORDERS, not from R2_BASE.

    R2_BASE.json pins fourteen ids and names its own instrument. This re-reads the task-order
    directory UNSCOPED -- every `*-r1.*.md` order it finds, not a list of fourteen filenames -- and
    prints the per-file count, so a criterion in a round-1 order that R2_BASE omits would show up as
    a file with a judgment criterion and no pinned id.
    """
    todir = os.path.join(REPO, ROOT, "task-orders")
    files = sorted(f for f in os.listdir(todir) if f.endswith(".md"))
    r1 = [f for f in files if "-r1." in f]
    pinned = json.load(open(os.path.join(
        REPO, ROOT, "deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/R2_BASE.json"), encoding="utf-8"))
    pinned_ids = set((pinned.get("round_1_judgment_criteria") or {}).get("by_id", {}))
    found = {}
    for name in files:
        text = open(os.path.join(todir, name), encoding="utf-8").read()
        for match in re.finditer(r'<criterion\s+id="([^"]+)"[^>]*judgment="true"', text):
            found.setdefault(match.group(1), name)
    print("order files in the directory (ALL rounds): %d" % len(files))
    print("of them, round-1 orders (`-r1.` in the filename): %d" % len(r1))
    print("criterion elements carrying judgment=\"true\", any round: %d" % len(found))
    r1_found = {k: v for k, v in found.items() if "-r1." in v}
    print("of those, in a round-1 order: %d" % len(r1_found))
    print("pinned by R2_BASE.json: %d" % len(pinned_ids))
    print("in the ORDERS but NOT pinned (must be empty): %s" % sorted(set(r1_found) - pinned_ids))
    print("pinned but NOT found in a round-1 order (must be empty): %s" % sorted(pinned_ids - set(r1_found)))
    for cid in sorted(r1_found):
        print("  %-10s %s" % (cid, r1_found[cid]))
    return 0


CMDS = {"position": position, "mechanism": mechanism, "probes": probes, "denominator": denominator}


def main(argv):
    if len(argv) < 2 or argv[1] not in CMDS:
        print("usage: rederive_r1.py position|mechanism|probes [--only <criterion-id>]")
        return 2
    if argv[1] == "probes":
        only = argv[3] if len(argv) > 3 and argv[2] == "--only" else None
        return probes(only)
    return CMDS[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
