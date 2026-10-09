"""LGIC_ENFORCE round 20 -- the issuer's fixed checks, one subcommand per criterion (2.0.0_SA_COO~B1).

Run from the root of the worktree under test:  python <this file> <arm> [--deliverables DIR]

Arms (each prints exactly one PASS-* or FAIL-* verdict line last, and exits 0 only on PASS):
  live      EN-ae-1  the live-plane census r20 report + LIVE_CENSUS_R20.json
  compare   EN-ae-2  HAND_COMPARE_R20.json against the r20 report and the r19 hand re-measure
  stop      EN-ae-3  LOUD_STOP_R20.json: the planted unreadable name STOPS the run; the readable control completes
  s9        EN-ae-4  a name built by name() at a call site is graded by the gate, or the gate prints that it was not
  s12       EN-ae-5  PATTERN_COMMIT_R20.json: one planted PATTERN-name commit on a QA branch, read for its grade
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.getcwd()
PROJ = "org/missions/D14/LGIC/LGIC_ENFORCE"
DELIV = PROJ + "/deliverables"
W1 = "0.9.0_WK_LGIC_ENFORCE~1"
W2 = "0.9.0_WK_LGIC_ENFORCE~2"
W3 = "0.9.0_WK_LGIC_ENFORCE~3"
R13_REPORT = DELIV + "/" + W1 + "/NAMING_CENSUS_REPORT.r13.md"
R19_RECORD = DELIV + "/" + W1 + "/HAND_REMEASURE_R19.json"
R19_KEYS = ("grading_rule_worked_cases", "n6_grader_rows", "tension_ranking_surfaces")

sys.path.insert(0, os.path.join(ROOT, "lib"))


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def load_json(path):
    need(os.path.isfile(path), "absent: %s" % path)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def fence(path):
    need(os.path.isfile(path), "absent: %s" % path)
    with open(path, encoding="utf-8") as fh:
        m = re.search(r"```json\n(.*?)\n```", fh.read(), re.S)
    need(m is not None, "no json fence in %s" % path)
    return json.loads(m.group(1))


def run(args, timeout=600):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout)
    out = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, out.replace("\r\n", "\n")


# ---------------------------------------------------------------- live (EN-ae-1)
def arm_live(d):
    rep_path = os.path.join(d, W1, "NAMING_CENSUS_REPORT.r20.md")
    rec = load_json(os.path.join(d, W1, "LIVE_CENSUS_R20.json"))
    doc = fence(rep_path)
    r13 = fence(R13_REPORT)
    den = doc["denominators"]
    need(doc.get("stopped") is None, "the r20 run STOPPED: %r" % (doc.get("stopped"),))
    need(den["live"] > 0, "live denominator is 0: the live plane was not read")
    need(doc.get("vintage") and doc["vintage"] != r13.get("vintage"), "vintage absent or equal to round 13's (not a fresh pull)")
    need(den["judged_live"] + den["carded_live"] == den["live_nameable"],
         "live plane not closed: judged %d + carded %d != nameable %d" % (den["judged_live"], den["carded_live"], den["live_nameable"]))
    need(den["judged_repo"] + den["carded_repo"] == den["repo"],
         "repo plane not closed: judged %d + carded %d != repo %d" % (den["judged_repo"], den["carded_repo"], den["repo"]))
    need(rec.get("report") == DELIV + "/" + W1 + "/NAMING_CENSUS_REPORT.r20.md", "record.report does not name the r20 report")
    need(rec.get("live_nodes_scanned") == den["live"], "record.live_nodes_scanned != report denominators.live")
    ar = rec.get("all_roots_line") or ""
    need(ar.startswith("ALL-ROOTS ok=True ") and "unmapped=0" in ar, "record.all_roots_line is not an ALL-ROOTS ok=True line with unmapped=0")
    # every card the r20 run carries that round 13 did not carry is a NEW card; each must name its owner, and its name must
    # really RAISE (a card on a readable name hides a verdict, so it is refused)
    old = set((e.get("plane"), e.get("name")) for e in r13["not_judged"])
    new = [e for e in doc["not_judged"] if (e.get("plane"), e.get("name")) not in old]
    rec_new = {(e.get("plane"), e.get("name")): e for e in rec.get("new_cards", [])}
    need(set(rec_new) == set((e.get("plane"), e.get("name")) for e in new),
         "record.new_cards != the report's not_judged minus round 13's (%d vs %d)" % (len(rec_new), len(new)))
    import opal_naming as on
    readable = []
    for key, e in rec_new.items():
        need(str(e.get("owner") or "").strip(), "new card %r names no owner" % (key,))
        need(e.get("type"), "new card %r carries no type" % (key,))
        try:
            on.grade(e["name"], e["type"])
            readable.append(e["name"])
        except on.RaiseDefect:
            pass
    need(not readable, "%d new card(s) on names grade() READS (a card may only hold a RAISE): %s" % (len(readable), readable[:5]))
    print("live=%d nameable=%d judged_live=%d carded_live=%d repo=%d judged_repo=%d carded_repo=%d new_cards=%d" % (
        den["live"], den["live_nameable"], den["judged_live"], den["carded_live"], den["repo"], den["judged_repo"],
        den["carded_repo"], len(new)))
    return "PASS-R20-LIVE"


# ---------------------------------------------------------------- compare (EN-ae-2)
def arm_compare(d):
    rec = load_json(os.path.join(d, W1, "HAND_COMPARE_R20.json"))
    r19 = load_json(R19_RECORD)
    doc = fence(os.path.join(d, W1, "NAMING_CENSUS_REPORT.r20.md"))
    need(rec.get("census_report") == DELIV + "/" + W1 + "/NAMING_CENSUS_REPORT.r20.md", "census_report does not name the r20 report")
    need(sorted(rec.get("surfaces", {})) == sorted(R19_KEYS), "surfaces != the three hand surfaces %s" % (R19_KEYS,))
    by_name = {}
    for r in doc["rows"]:
        by_name.setdefault(r["current"], set()).add(r["verdict"])
    tot = {"compared": 0, "agree": 0, "disagree": 0}
    for k in R19_KEYS:
        s = rec["surfaces"][k]
        want = set(r19["surfaces"][k]["compared_keys"])
        got = set(s.get("compared_keys", []))
        need(got == want, "%s: compared_keys != round 19's set (missing %d, extra %d)" % (k, len(want - got), len(got - want)))
        need(s["compared"] == len(got) and s["agree"] + s["disagree"] == s["compared"], "%s: counts do not add up" % k)
        diffs = s.get("differences", [])
        need(len(diffs) == s["disagree"], "%s: %d differences listed for disagree=%d" % (k, len(diffs), s["disagree"]))
        for x in diffs:
            need(x.get("key") in got, "%s: difference key %r not compared" % (k, x.get("key")))
            need(len(str(x.get("explanation") or "").strip()) >= 20, "%s: difference %r has no explanation" % (k, x.get("key")))
            nm = x.get("name")
            if nm in by_name:
                need(x.get("machine_verdict") in by_name[nm],
                     "%s: %r machine_verdict %r is not the r20 run's %s" % (k, nm, x.get("machine_verdict"), sorted(by_name[nm])))
        for f in tot:
            tot[f] += s[f]
    need(rec.get("totals") == tot, "totals %r != the surfaces' sum %r" % (rec.get("totals"), tot))
    print("compared=%d agree=%d disagree=%d" % (tot["compared"], tot["agree"], tot["disagree"]))
    return "PASS-R20-COMPARE"


# ---------------------------------------------------------------- stop (EN-ae-3)
def _names_lines(path):
    with open(path, encoding="utf-8") as fh:
        return [ln for ln in fh.read().splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def arm_stop(d):
    base = os.path.join(d, W3)
    rec = load_json(os.path.join(base, "LOUD_STOP_R20.json"))
    planted = DELIV + "/" + W3 + "/" + "stop_planted_r20.tsv"
    readable = DELIV + "/" + W3 + "/" + "stop_readable_r20.tsv"
    need(rec.get("planted_file") == planted and rec.get("readable_file") == readable, "record names other files")
    pl, rd = _names_lines(os.path.join(ROOT, planted)), _names_lines(os.path.join(ROOT, readable))
    need(len(pl) == 1 and len(rd) == 1, "each names file holds exactly one name (planted %d, readable %d)" % (len(pl), len(rd)))
    pname = rec.get("planted_name") or ""
    need(pname and pname in [c.strip() for c in pl[0].split("\t")], "record.planted_name is not the planted file's name")
    rc_p, out_p = run([sys.executable, "lib/opal_naming.py", "census", "--names", planted])
    rc_r, out_r = run([sys.executable, "lib/opal_naming.py", "census", "--names", readable])
    need(rc_p == 3, "the planted name did not stop the run: rc=%d (want 3)" % rc_p)
    need(re.search(r"^CENSUS: STOPPED on the first RAISE .*%s" % re.escape(repr(pname)), out_p, re.M),
         "no STOPPED line naming the planted name %r" % pname)
    need(not re.search(r"^CENSUS (OUT-OF-PATTERN|ALIAS|CONFORMANT) .*%s" % re.escape(pname), out_p, re.M),
         "the planted name was filed with a verdict instead of stopping the run")
    need(rc_r == 0 and re.search(r"^CENSUS: COMPLETE 1 judged", out_r, re.M), "the readable control did not complete: rc=%d" % rc_r)
    need(rec.get("planted_rc") == rc_p and rec.get("readable_rc") == rc_r, "recorded rc values differ from the re-run")
    print("planted=%r rc=%d readable rc=%d" % (pname, rc_p, rc_r))
    return "PASS-R20-STOP"


# ---------------------------------------------------------------- s9 (EN-ae-4)
TF_FIXTURE = """diff --git a/infra/aws/terraform/zz-r20-s9-probe/main.tf b/infra/aws/terraform/zz-r20-s9-probe/main.tf
new file mode 100644
--- /dev/null
+++ b/infra/aws/terraform/zz-r20-s9-probe/main.tf
@@ -0,0 +1,8 @@
+module "probe_scheduler_role_name" {
+  source    = "../modules/opal_name"
+  system    = "irpt"
+  scope     = "cottonwood"
+  function  = "reporting-gold"
+  kind      = "role"
+  qualifier = "scheduler"
+}
"""
PY_FIXTURE = """diff --git a/infra/aws/lambda/zz-r20-s9-probe/handler.py b/infra/aws/lambda/zz-r20-s9-probe/handler.py
new file mode 100644
--- /dev/null
+++ b/infra/aws/lambda/zz-r20-s9-probe/handler.py
@@ -0,0 +1,3 @@
+from opal_naming import name
+
+ROLE = name("irpt", "cottonwood", "reporting-gold", "role", "scheduler")
"""
CONTROL_FIXTURE = """diff --git a/infra/aws/terraform/zz-r20-s9-control/main.tf b/infra/aws/terraform/zz-r20-s9-control/main.tf
new file mode 100644
--- /dev/null
+++ b/infra/aws/terraform/zz-r20-s9-control/main.tf
@@ -0,0 +1,3 @@
+resource "aws_iam_role" "probe" {
+  name = "zz-probe-scheduler-role-typed"
+}
"""
BUILT = "irpt-cot-reporting-gold-scheduler-role"


def _gate(fixture):
    with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False, encoding="utf-8", newline="\n") as fh:
        fh.write(fixture)
    try:
        return run([sys.executable, ".tools/naming-gate.py", "--diff", fh.name], timeout=300)
    finally:
        os.unlink(fh.name)


def arm_s9(d):
    for label, fx, path in (("tf-module", TF_FIXTURE, "zz-r20-s9-probe/main.tf"), ("py-call", PY_FIXTURE, "zz-r20-s9-probe/handler.py")):
        rc, out = _gate(fx)
        summ = re.search(r"^NAMING-GATE: (PASS|WARN|REFUSE) (\d+) graded", out, re.M)
        need(summ is not None, "%s: no NAMING-GATE summary line (rc=%d)" % (label, rc))
        graded = re.search(r"^NAMING \S+ \S*%s:\d+ %s\b" % (re.escape(path), re.escape(BUILT)), out, re.M)
        told = re.search(r"^NAMING BUILT-NOT-GRADED \S*%s:\d+" % re.escape(path), out, re.M)
        need(graded or told, "%s: the gate neither graded the built name %s nor printed BUILT-NOT-GRADED (summary: %s)"
             % (label, BUILT, summ.group(0)))
        print("%s: %s" % (label, (graded or told).group(0)))
    # the difference control: a hand-typed literal is still graded, so the arm cannot pass by grading nothing anywhere
    rc, out = _gate(CONTROL_FIXTURE)
    need(re.search(r"^NAMING \S+ \S*zz-r20-s9-control/main.tf:\d+ zz-probe-scheduler-role-typed\b", out, re.M),
         "control: the hand-typed literal was not graded")
    return "PASS-R20-S9"


# ---------------------------------------------------------------- s12 (EN-ae-5)
def arm_s12(d):
    base = os.path.join(d, W2)
    rec = load_json(os.path.join(base, "PATTERN_COMMIT_R20.json"))
    br = rec.get("qa_branch") or ""
    need(br.startswith("qa/lgic-enforce-r20-"), "qa_branch must start qa/lgic-enforce-r20- (got %r)" % br)
    pname = rec.get("planted_name") or ""
    need(rec.get("place_kind") == "PATTERN", "place_kind is not PATTERN")
    import opal_naming_rootcheck as rc_mod
    res = rc_mod.place(pname, rec["planted_type"], rec["planted_root"])
    need(res["kind"] == "PATTERN", "place(%r, %r, %r) is %s, not PATTERN" % (pname, rec["planted_type"], rec["planted_root"], res["kind"]))
    sha = rec.get("commit_sha")
    if sha:
        r, _ = run(["git", "cat-file", "-e", sha + "^{commit}"])
        need(r == 0, "commit %s does not exist" % sha)
        r, out = run(["git", "branch", "--list", br, "--contains", sha])
        need(br in out, "commit %s is not on %s" % (sha, br))
        r, _ = run(["git", "merge-base", "--is-ancestor", sha, "HEAD"])
        need(r == 1, "the planted commit is reachable from HEAD: it must stay on the QA branch only")
        r, diff = run(["git", "show", "--format=", sha])
        need(pname in diff, "the planted commit does not add %r" % pname)
    else:
        need(rec.get("refused") is True and rec.get("commit_rc") not in (None, 0), "no commit_sha and no recorded refusal")
    line = rec.get("grade_line") or ""
    need(line == "NONE" or pname in line, "grade_line neither names the planted name nor is NONE")
    if line == "NONE":
        # AMENDMENT 1 (EN-z-5, row LGIC_ENFORCE-D1-W2-S153): a worker's row id carries W<n> (LGIC_ENFORCE-D1-W2-S152)
        need(re.match(r"LGIC_ENFORCE-(?:[A-Z0-9]+-)+S\d+$", rec.get("row_id") or ""), "grade_line NONE needs a surprise row_id")
        rows = open(os.path.join(ROOT, PROJ, "surprise-channel/investigations/INVESTIGATION_v1.md"), encoding="utf-8").read()
        need(('"id": "%s"' % rec["row_id"]) in rows, "row_id %s is not a row in the channel" % rec["row_id"])
    need(rec.get("gate_summary", "").startswith("NAMING-GATE: "), "gate_summary is not the gate's summary line")
    print("qa_branch=%s commit=%s grade_line=%s summary=%s" % (br, sha, line, rec["gate_summary"]))
    return "PASS-R20-S12"


ARMS = {"live": arm_live, "compare": arm_compare, "stop": arm_stop, "s9": arm_s9, "s12": arm_s12}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arm", choices=sorted(ARMS))
    ap.add_argument("--deliverables", default=DELIV)
    a = ap.parse_args()
    try:
        verdict = ARMS[a.arm](a.deliverables)
    except Fail as exc:
        print("FAIL-R20-%s: %s" % (a.arm.upper(), exc))
        return 1
    print(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())
