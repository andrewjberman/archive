"""Issuance contention check: does a cell RUN or READ what another OPEN cell WRITES?

WHY THIS EXISTS. The write-surface census run at every issuance intersects each cell's
<paths> with every other cell's <paths>. That answers "will two cells overwrite each
other". It does NOT answer "can two cells run at the same time", because it never reads
what a cell INVOKES or READS. Three contentions in LGIC_ENFORCE round 2 had EMPTY
<paths> intersections and were still real:

    LGIC_ENFORCE-S23   instrument-vs-output   EN-s-1 RUNS lib/opal_naming.py, EN-r-6 WRITES it
    LGIC_ENFORCE-S24   input-vs-output        EN-d-1 WRITES the registry EN-s-1 READS
    LGIC_ENFORCE-S26   capacity-vs-capacity   disk; NOT covered by this tool, see LIMITS

All three were caught by hand. A rule applied by remembering is not a check, so this is
the check. S23's disarm names exactly this widening as its durable half.

WHAT IT DOES. For the candidate cell, collect every repo path its <invocation> elements
and its "**Read:**" line name. For every OPEN sibling, collect its <paths> grant. Report
each candidate target an open sibling would write, using the ESTATE'S OWN grant semantics
(imported from .tools/owned-paths-validate.py) so a glob or directory prefix is read here
exactly as the resolver reads it.

TERMINALITY is the gate's, imported from .tools/surprise-row-gate.py: an order is OPEN
only when its status word is non-terminal AND it is not terminal by its proof. An order
that FAILED a criterion on a VALID proof is TERMINAL and cannot contend with anything.

MEASURED AGAINST THE THREE CASES IT WAS BUILT FROM: it catches 2 of 3.

    S23  EN-s-1 RUNS lib/opal_naming.py, EN-r-6 WRITES it          CAUGHT (rooted path)
    S24  EN-s-2 READS NAMING_CENSUS_REPORT.md, EN-s-1 WRITES it    CAUGHT (by basename)
    S24  EN-s-1 reads the REGISTRY, EN-d-1 WRITES it               MISSED

The miss is the honest shape of limit 1 and is not fixable cheaply: EN-s-1's order never
NAMES the registry. It says "run python lib/opal_naming.py census", and the census reads
the registry inside itself. Catching that needs the transitive closure of what an invoked
program reads, which is a different tool. 2 of 3 is what this is worth -- use it to narrow
the hand check, never to replace it.

LIMITS, stated because a check that hides them is worse than none:
  1. It reads PATHS NAMED IN TEXT, rooted or by a sibling's granted basename. A cell that
     reaches a file THROUGH THE PROGRAM IT INVOKES, an env var or a computed path is
     invisible here (the measured miss above). This narrows the blind spot; it does not
     close it.
  2. It does not model DISK, MEMORY or any shared capacity (LGIC_ENFORCE-S26). Two cells
     can pass this check and still be unable to run together.
  3. It is ADVISORY. It refuses nothing and gates nothing; the issuer decides.
  4. A hit is not automatically a defect: a cell may legitimately read a file a sibling
     rewrites if the ORDER between them is fixed by a dependency. The check prints the
     pair; the issuer reads the dependency.

USAGE
    python <this> --project LGIC_ENFORCE
    python <this> --project LGIC_ENFORCE --candidate EN-d-1
    python <this> --selftest
"""

import argparse
import glob
import importlib.util
import io
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))


def _load(mod_name, rel):
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(REPO, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_OPV = _load("opv", os.path.join(".tools", "owned-paths-validate.py"))
_SRG = _load("srg", os.path.join(".tools", "surprise-row-gate.py"))

# A repo-root-relative path as it appears in prose or an invocation. Deliberately narrow:
# it must carry a directory separator and a plausible extension or a trailing slash, so
# bare words and sentence fragments are not mistaken for paths.
_PATH_RE = re.compile(
    r"(?<![\w/.-])((?:org|lib|infra|data|\.tools|docs|deck_generation|integrations)"
    r"/[\w./*?\[\]{}~-]+)"
)


def _orders(project):
    pat = os.path.join(REPO, "org", "missions", "D*", "*", project, "task-orders", "*.md")
    return sorted(p.replace("\\", "/") for p in glob.glob(pat))


def _is_open(path):
    """True when the gate reads this order as NOT terminal -- by word and by proof."""
    text = io.open(path, encoding="utf-8", errors="replace").read()
    m = _SRG.TO_STATUS_RE.search(text)
    word = (m.group(1).lower() if m else "")
    if word in _SRG.TERMINAL_TO_WORDS:
        return False, text
    rel = os.path.relpath(path, REPO).replace("\\", "/")
    try:
        terminal = _SRG._proof_terminal(REPO, rel, text)[0]
    except Exception:
        terminal = False
    return (not terminal), text


def _blob(text):
    """The text a cell's RUN/READ targets live in: every <invocation> plus the '**Read:**' run."""
    blob = " ".join(re.findall(r"<invocation>(.*?)</invocation>", text, re.S))
    read = re.search(r"\*\*Read:\*\*(.*?)(?:\n\n|\n###|\n##)", text, re.S)
    if read:
        blob += " " + read.group(1)
    return blob


def _targets(text):
    """Rooted paths the cell RUNS or READS."""
    out = set()
    for hit in _PATH_RE.findall(_blob(text)):
        out.add(hit.rstrip(".,;`)").replace("\\", "/"))
    return out


def _bare_hits(text, grants):
    """Grant entries a cell names by BASENAME ONLY.

    THE REASON THIS EXISTS IS A FALSE CLEAR THIS TOOL PRODUCED ON ITS FIRST REAL RUN.
    A cell's Read line often names a file with no directory -- EN-s-2's reads
    `NAMING_CENSUS_REPORT.md`, which is EN-s-1's whole write surface. The rooted-path
    regex cannot see that, so the pair read CLEAR while a real input-vs-output
    contention sat between them. A check that cannot go non-zero on the case it was
    built for is a constant wearing a measurement's clothes.

    Matching is deliberately narrow to stay honest: only against the BASENAMES A
    SIBLING ACTUALLY GRANTS, whole-word, and never for a directory-shaped entry (a
    trailing slash or a glob has no single basename to name).
    """
    blob = _blob(text)
    out = []
    for e in grants:
        if e.endswith("/") or any(ch in e for ch in "*?["):
            continue
        base = e.rsplit("/", 1)[-1]
        if not base or "." not in base:
            continue
        if re.search(r"(?<![\w/.-])%s(?![\w-])" % re.escape(base), blob):
            out.append(e)
    return out


def _cell_of(path):
    base = os.path.basename(path)
    m = re.search(r"\.((?:TO-)?[A-Za-z]+-[a-z]-\d+)", base)
    return (m.group(1).replace("TO-", "") if m else base)


def run(project, candidate=None):
    orders = _orders(project)
    if not orders:
        print("no task orders found for %s under %s" % (project, REPO))
        return 2

    state = {}
    for p in orders:
        is_open, text = _is_open(p)
        state[p] = (is_open, text)

    open_orders = [p for p in orders if state[p][0]]
    print("project %s: %d task order(s), %d OPEN" % (project, len(orders), len(open_orders)))
    print("OPEN: %s" % ", ".join(sorted(_cell_of(p) for p in open_orders)) or "(none)")
    print("")

    pool = [p for p in open_orders
            if candidate is None or _cell_of(p).lower() == candidate.lower()]
    if candidate and not pool:
        print("candidate %s is not an OPEN order of %s (already terminal, or misspelled)"
              % (candidate, project))
        return 2

    hits = 0
    for p in pool:
        cell = _cell_of(p)
        targets = _targets(state[p][1])
        found = []
        for q in open_orders:
            if q == p:
                continue
            grants = _OPV._paths_block_entries(state[q][1])
            for t in sorted(targets):
                if _OPV._order_grants(t, grants):
                    found.append((_cell_of(q), t, "rooted"))
            for e in _bare_hits(state[p][1], grants):
                if not any(f[0] == _cell_of(q) and f[1] == e for f in found):
                    found.append((_cell_of(q), e, "by basename"))
        print("%-12s runs/reads %d rooted path(s)" % (cell, len(targets)))
        if found:
            hits += len(found)
            for other, t, how in found:
                print("   CONTENDS  %-12s WRITES  %-58s [%s]" % (other, t, how))
        else:
            print("   clear against %d other open cell(s)" % (len(open_orders) - 1))
    print("")
    print("RESULT: %d contention(s) over %d candidate(s); %d open cell(s) in the pool"
          % (hits, len(pool), len(open_orders)))
    print("ADVISORY -- this refuses nothing. It does not model disk or any shared "
          "capacity (LGIC_ENFORCE-S26), and it sees only paths NAMED IN TEXT.")
    return 0


def selftest():
    """Both arms. A check that cannot go non-zero on the positive case is a constant."""
    ok = True

    writer = "<paths>\nlib/opal_naming.py\ndata/firm_registry.json\n</paths>"
    reader = ("<invocation>cd X && python lib/opal_naming.py census</invocation>"
              "\n**Read:** `lib/opal_naming.py`\n\n")
    grants = _OPV._paths_block_entries(writer)
    tgts = _targets(reader)

    arm1 = any(_OPV._order_grants(t, grants) for t in tgts)
    print("POSITIVE  reader runs what writer writes -> contention detected: %s" % arm1)
    ok = ok and arm1

    other = _OPV._paths_block_entries("<paths>\ndocs/architecture/X.md\n</paths>")
    arm2 = not any(_OPV._order_grants(t, other) for t in tgts)
    print("NEGATIVE  disjoint surfaces -> no contention: %s" % (arm2))
    ok = ok and arm2

    pre = _OPV._paths_block_entries("<paths>\ninfra/aws/terraform/modules/opal_name/\n</paths>")
    arm3 = _OPV._order_grants("infra/aws/terraform/modules/opal_name/main.tf", pre)
    print("PREFIX    a directory grant covers a file under it: %s" % arm3)
    ok = ok and arm3

    arm4 = not _OPV._order_grants("lib/opal_naming_extra.py", grants)
    print("NOT-A-PREFIX  'lib/opal_naming.py' does not grant a longer name: %s" % arm4)
    ok = ok and arm4

    empty = _targets("no invocations and no read line here")
    arm5 = (empty == set())
    print("EMPTY     a cell naming no path yields no targets: %s" % arm5)
    ok = ok and arm5

    print("SELFTEST: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project")
    ap.add_argument("--candidate", help="one cell id, e.g. EN-d-1")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.project:
        ap.error("--project is required unless --selftest")
    return run(a.project, a.candidate)


if __name__ == "__main__":
    sys.exit(main())
