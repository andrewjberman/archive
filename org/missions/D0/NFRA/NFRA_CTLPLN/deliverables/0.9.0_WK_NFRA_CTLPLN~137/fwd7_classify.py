#!/usr/bin/env python3
"""fwd7_classify.py -- NFRA_CTLPLN FWD-7 (TO-CT-ay-1, cell CT-ay-1).

Classifies every cross-box OVERLAP line of the placement read into a shared append-only carrier or a project
path, and reports the project-path overlaps alone. Ruling: CTO round-27 analysis, ruling 4.

    python fwd7_classify.py             run the placement read, classify each line, write FWD7_PROJECT_PATH_OVERLAPS.md
    python fwd7_classify.py --selftest  synthetic lines through classify() (no subprocess, no file written)

READS ONLY. `python .tools/placement-check.py` runs as a subprocess with cwd = the worktree root, bound 200 s.
This script never imports the tool and changes no tool, register, project row or record. Standard library only.

Classes, first match wins:
  CARRIER            both paths lie in the same shared append-only carrier kind (five kinds, printed per line)
  NOT-SAME-FILE      one path is a strict directory-prefix parent of the other and the two differ
  PROJECT-SAME-FILE  the two paths are the same file (the same path after the placement tool's normalisation)
  UNCLASSIFIED       the line cannot be parsed, or no rule places it

Path normalisation and the prefix relation are the placement tool's own (its norm and overlaps): backslashes
become slashes, a trailing slash is dropped, and a glob tail is read as its directory.

Exit: 0 when ok=True; 1 when ok=False; 2 when any line is UNCLASSIFIED.
"""
import fnmatch
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_REL = os.path.join(".tools", "placement-check.py")
REPORT_NAME = "FWD7_PROJECT_PATH_OVERLAPS.md"
CLASSES = ("CARRIER", "NOT-SAME-FILE", "PROJECT-SAME-FILE", "UNCLASSIFIED")
CARRIER_KINDS = ("deploy-ledger-sentinel", "audit-log", "surprise-channel", "open-calls", "crossbox")
DEPLOY_DIR = "org/critical_paths/.open_deploys"
CROSSBOX_DIR = "org/devices/crossbox"
OPEN_CALLS_RE = re.compile(r"^org/devices/state/[^/]+/open_calls\.json$")
OVERLAP_RE = re.compile(r"^\s*OVERLAP (\S+) \(([^()\s]+)\) and (\S+) \(([^()\s]+)\): (\S+) ~ (\S+)\s*$")
FINDINGS_RE = re.compile(r"^FINDINGS: (\d+) unplaced/unreadable, (\d+) cross-box write overlap\(s\)\s*$", re.M)
LIVE_RE = re.compile(r"^placement-check \| live projects: (\d+)", re.M)


def asc(text):
    """ASCII-only text for every printed or written line."""
    return str(text).encode("ascii", "replace").decode("ascii")


def norm(p):
    """The placement tool's norm()."""
    return p.strip().replace("\\", "/").rstrip("/")


def reduce_path(p):
    """The placement tool's overlaps() reduction: a glob tail is read as its directory."""
    return norm(p.split("*")[0])


def in_dir(p, d):
    return p == d or p.startswith(d + "/")


def carrier_kinds(p):
    """The set of the five carrier kinds a reduced path lies in. A project path lies in none."""
    kinds = set()
    base = p.rsplit("/", 1)[-1]
    ancestors = p.split("/")[:-1]
    if in_dir(p, DEPLOY_DIR):
        kinds.add("deploy-ledger-sentinel")
    if fnmatch.fnmatchcase(base, "*audit*.log") or "audit" in ancestors:
        kinds.add("audit-log")
    if "surprise-channel" in ancestors:
        kinds.add("surprise-channel")
    if OPEN_CALLS_RE.match(p):
        kinds.add("open-calls")
    if in_dir(p, CROSSBOX_DIR):
        kinds.add("crossbox")
    return kinds


def classify(line):
    """PURE. One placement OVERLAP line -> a record dict. Never raises."""
    rec = {"raw": line.rstrip("\r\n"), "cls": "UNCLASSIFIED", "kind": None, "rel": None,
           "proj_a": None, "box_a": None, "proj_b": None, "box_b": None,
           "pa": None, "pb": None, "shared": None, "reason": None}
    m = OVERLAP_RE.match(line)
    if not m:
        rec["reason"] = "unparseable: not an OVERLAP line of the placement read"
        return rec
    proj_a, box_a, proj_b, box_b, pa, pb = m.groups()
    rec.update(proj_a=proj_a, box_a=box_a, proj_b=proj_b, box_b=box_b, pa=norm(pa), pb=norm(pb))
    ra, rb = reduce_path(pa), reduce_path(pb)
    if not ra or not rb:
        rec["reason"] = "empty path after normalisation"
        return rec
    common = carrier_kinds(ra) & carrier_kinds(rb)
    if common:
        shared = [k for k in CARRIER_KINDS if k in common]
        rec.update(cls="CARRIER", kind=shared[0], rel="kinds both paths lie in: " + ", ".join(shared))
        return rec
    if ra != rb and (rb.startswith(ra + "/") or ra.startswith(rb + "/")):
        parent, child = (ra, rb) if rb.startswith(ra + "/") else (rb, ra)
        rec.update(cls="NOT-SAME-FILE", rel="directory-prefix: %s is a directory claim over %s" % (parent, child))
        return rec
    if ra == rb:
        rec.update(cls="PROJECT-SAME-FILE", shared=ra, rel="same path")
        return rec
    rec["reason"] = "paths unrelated by every rule (the placement tool does not print such a line)"
    return rec


def summarise(recs, findings, rc):
    """PURE. The four-class count and the ok verdict (the cell's rule, plus rc 0 from the tool)."""
    counts = {c: 0 for c in CLASSES}
    for r in recs:
        counts[r["cls"]] += 1
    total = len(recs)
    classed = sum(counts[c] for c in CLASSES)
    ok = (rc == 0 and findings is not None and total == findings and classed == total
          and counts["UNCLASSIFIED"] == 0)
    return {"total": total, "counts": counts, "findings": findings, "ok": ok}


def find_root():
    d = HERE
    for _ in range(12):
        if os.path.isfile(os.path.join(d, TOOL_REL)):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def read_placement(root):
    """-> (rc, text, error). The tool runs as a subprocess, cwd = the worktree root, bound 200 s."""
    try:
        p = subprocess.run([sys.executable, os.path.join(root, TOOL_REL)], cwd=root,
                           capture_output=True, timeout=200)
    except subprocess.TimeoutExpired:
        return None, "", "TIMEOUT after 200 s"
    except OSError as exc:
        return None, "", "OSError: %s" % exc
    return p.returncode, p.stdout.decode("utf-8", "replace"), None


def write_report(path, recs, summ, live, unplaced, rc):
    counts = summ["counts"]
    proj = [r for r in recs if r["cls"] == "PROJECT-SAME-FILE"]
    nsf = [r for r in recs if r["cls"] == "NOT-SAME-FILE"]
    carr = [r for r in recs if r["cls"] == "CARRIER"]
    unc = [r for r in recs if r["cls"] == "UNCLASSIFIED"]
    out = ["# FWD-7 project-path overlaps (NFRA_CTLPLN.TO-CT-ay-1, cell CT-ay-1)", ""]
    if not proj:
        out.append("Zero project-path overlaps: no two live projects on different boxes name the same file in their "
                   "declared write surfaces (the placement read declares surfaces only; it is blind to what each box "
                   "really writes).")
    else:
        out.append("Project-path overlaps: %d PROJECT-SAME-FILE line(s) name a shared file; they are listed per file "
                   "below, and no fix is proposed (the CTO decides which become a cell)." % len(proj))
    out += ["",
            "Denominator: %d OVERLAP line(s) read from `python .tools/placement-check.py` (rc=%s; live projects %s; "
            "unplaced/unreadable %s). The read's own FINDINGS line counts %s cross-box write overlap(s) (%s)."
            % (summ["total"], rc, live, unplaced, summ["findings"],
               "agrees" if summ["findings"] == summ["total"] else "DISAGREES"),
            "",
            "Classes: CARRIER %d | NOT-SAME-FILE %d | PROJECT-SAME-FILE %d | UNCLASSIFIED %d | sum %d | ok=%s."
            % (counts["CARRIER"], counts["NOT-SAME-FILE"], counts["PROJECT-SAME-FILE"], counts["UNCLASSIFIED"],
               sum(counts.values()), summ["ok"]),
            "",
            "## PROJECT-SAME-FILE (%d)" % len(proj), ""]
    if proj:
        out += ["| # | project A (box) | project B (box) | path A | path B | shared file |",
                "|---|---|---|---|---|---|"]
        for i, r in enumerate(proj, 1):
            out.append("| %d | %s (%s) | %s (%s) | `%s` | `%s` | `%s` |" % (
                i, r["proj_a"], r["box_a"], r["proj_b"], r["box_b"], r["pa"], r["pb"], r["shared"]))
        out += ["", "### Per shared file (which projects touch it; no fix proposed)", ""]
        by_file = {}
        for r in proj:
            by_file.setdefault(r["shared"], set()).update(
                ["%s (%s)" % (r["proj_a"], r["box_a"]), "%s (%s)" % (r["proj_b"], r["box_b"])])
        for f in sorted(by_file):
            out.append("- `%s`: %s" % (f, ", ".join(sorted(by_file[f]))))
    else:
        out.append("(none)")
    out += ["", "## NOT-SAME-FILE (%d)" % len(nsf), ""]
    if nsf:
        out += ["| # | project A (box) | project B (box) | path A | path B | relation |",
                "|---|---|---|---|---|---|"]
        for i, r in enumerate(nsf, 1):
            out.append("| %d | %s (%s) | %s (%s) | `%s` | `%s` | %s |" % (
                i, r["proj_a"], r["box_a"], r["proj_b"], r["box_b"], r["pa"], r["pb"], r["rel"]))
        out += ["", "Each NOT-SAME-FILE line is a directory claim over a path under it; it is classed here by the "
                "prefix rule the earlier table used (R5), which reads the two projects as changing different files. "
                "The relation column shows which path is the directory claim."]
    else:
        out.append("(none)")
    out += ["", "## CARRIER (%d), counts by kind" % len(carr), ""]
    for k in CARRIER_KINDS:
        out.append("- %s: %d" % (k, sum(1 for r in carr if r["kind"] == k)))
    if unc:
        out += ["", "## UNCLASSIFIED (%d)" % len(unc), ""]
        for r in unc:
            out.append("- `%s` -- %s" % (r["raw"].strip(), r["reason"]))
    text = "\n".join(asc(x) for x in out) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def last_line(summ, findings):
    c = summ["counts"]
    return ("FWD7-CLASSES total=%d carrier=%d not_same_file=%d project_same_file=%d unclassified=%d "
            "findings_line=%s ok=%s" % (summ["total"], c["CARRIER"], c["NOT-SAME-FILE"], c["PROJECT-SAME-FILE"],
                                        c["UNCLASSIFIED"], "NONE" if findings is None else findings,
                                        summ["ok"]))


def run():
    root = find_root()
    if root is None:
        print("FWD7-CLASSES total=0 carrier=0 not_same_file=0 project_same_file=0 unclassified=0 "
              "findings_line=NONE ok=False")
        print("ERROR: .tools/placement-check.py not found above %s" % asc(HERE))
        return 1
    rc, text, err = read_placement(root)
    if err:
        print("ERROR: placement read: %s" % err)
    findings = None
    m = FINDINGS_RE.search(text)
    if m:
        findings = int(m.group(2))
    lm = LIVE_RE.search(text)
    live = lm.group(1) if lm else "NONE"
    um = FINDINGS_RE.search(text)
    unplaced = um.group(1) if um else "NONE"
    recs = [classify(ln) for ln in text.splitlines() if "OVERLAP " in ln]
    summ = summarise(recs, findings, rc if rc is not None else -1)
    print(asc("fwd7_classify | tool: %s | rc=%s | live projects %s | unplaced/unreadable %s"
              % (os.path.join(root, TOOL_REL), rc, live, unplaced)))
    for i, r in enumerate(recs, 1):
        if r["cls"] == "CARRIER":
            print(asc("LINE %d CARRIER kind=%s | %s (%s) ~ %s (%s) | %s ~ %s"
                      % (i, r["kind"], r["proj_a"], r["box_a"], r["proj_b"], r["box_b"], r["pa"], r["pb"])))
        elif r["cls"] == "UNCLASSIFIED":
            print(asc("LINE %d UNCLASSIFIED | %s | %s" % (i, r["reason"], r["raw"].strip())))
        else:
            print(asc("LINE %d %s | %s (%s) ~ %s (%s) | %s ~ %s | %s"
                      % (i, r["cls"], r["proj_a"], r["box_a"], r["proj_b"], r["box_b"], r["pa"], r["pb"], r["rel"])))
    write_report(os.path.join(HERE, REPORT_NAME), recs, summ, live, unplaced, rc)
    print("report: " + asc(os.path.join(HERE, REPORT_NAME)))
    print(last_line(summ, findings))
    if summ["counts"]["UNCLASSIFIED"]:
        return 2
    return 0 if summ["ok"] else 1


def selftest():
    arms = [
        ("a sentinel pair is CARRIER",
         "  OVERLAP AMGT_HARVST (dell1) and NFRA_MCPMSP (sitez): org/critical_paths/.open_deploys ~ "
         "org/critical_paths/.open_deploys/nfra-mcpmsp-r1-firm-role.json", "CARRIER", "deploy-ledger-sentinel"),
        ("an open_calls pair is CARRIER",
         "  OVERLAP NFRA_CTLPLN (laptop) and IRPT_BCKEND (dell2): org/devices/state/laptop/open_calls.json ~ "
         "org/devices/state/dell2/open_calls.json", "CARRIER", "open-calls"),
        ("a surprise-channel pair is CARRIER",
         "  OVERLAP NFRA_CTLPLN (laptop) and MDPF_SECCLASS (dell1): org/missions/D0/NFRA/NFRA_CTLPLN/"
         "surprise-channel/investigations/INVESTIGATION_v1.md ~ org/missions/D0/NFRA/NFRA_CTLPLN/"
         "surprise-channel/investigations/INVESTIGATION_v1.md", "CARRIER", "surprise-channel"),
        ("an audit-log pair is CARRIER",
         "  OVERLAP NFRA_OPSWKF (dell2) and NFRA_TRNSPT (dell2): org/safe-deploy-bypass-audit.log ~ "
         "org/safe-deploy-bypass-audit.log", "CARRIER", "audit-log"),
        ("a crossbox pair is CARRIER",
         "  OVERLAP TCKT_VNEXT (dell2) and ETFS_RIVALS (dell1): org/devices/crossbox/XB-20261016T101128Z-0ff7.json ~ "
         "org/devices/crossbox", "CARRIER", "crossbox"),
        ("a directory-prefix parent of a different file is NOT-SAME-FILE",
         "  OVERLAP NFRA_CTLPLN (laptop) and IRPT_BCKEND (dell2): .tools/tests/test_crossbox_call.py ~ .tools/tests",
         "NOT-SAME-FILE", None),
        ("two projects naming the same ordinary source file are PROJECT-SAME-FILE",
         "  OVERLAP NFRA_MCPINDEX (sitez) and ADVI_BDPRCE (dell1): lib/devices.py ~ lib/devices.py",
         "PROJECT-SAME-FILE", None),
        ("a carrier path beside a project file is not CARRIER (no rule places it)",
         "  OVERLAP AMGT_HARVST (dell1) and NFRA_MCPMSP (sitez): org/critical_paths/.open_deploys/x.json ~ "
         "lib/devices.py", "UNCLASSIFIED", None),
        ("a malformed line is UNCLASSIFIED and the run ok is False",
         "  OVERLAP AMGT_HARVST (dell1) and NFRA_MCPMSP sitez lib/devices.py", "UNCLASSIFIED", None),
    ]
    passed = 0
    for name, line, want_cls, want_kind in arms:
        rec = classify(line)
        run_ok = summarise([rec], 1, 0)["ok"]
        good = (rec["cls"] == want_cls and (want_kind is None or rec["kind"] == want_kind)
                and run_ok == (want_cls != "UNCLASSIFIED"))
        passed += 1 if good else 0
        print(asc("%s: %s -> %s kind=%s run_ok=%s" % ("PASS" if good else "FAIL", name, rec["cls"],
                                                       rec["kind"], run_ok)))
    ok = passed == len(arms)
    print("FWD7-SELFTEST arms=%d/%d ok=%s" % (passed, len(arms), ok))
    return 0 if ok else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if argv:
        sys.stderr.write("usage: fwd7_classify.py [--selftest]\n")
        return 2
    return run()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
