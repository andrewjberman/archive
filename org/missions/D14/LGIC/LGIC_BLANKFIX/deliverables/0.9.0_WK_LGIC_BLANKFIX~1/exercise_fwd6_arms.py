#!/usr/bin/env python3
"""exercise_fwd6_arms -- arms A to G of the FWD-6 design, run on the real gate script (.tools/naming-gate.py).

    python org/missions/D14/LGIC/LGIC_BLANKFIX/deliverables/0.9.0_WK_LGIC_BLANKFIX~1/exercise_fwd6_arms.py

Each arm builds a unified diff by hand from HEAD's text of one Terraform file (difflib), writes it in a temporary folder and
runs the gate's own main() on it with --diff. The gate script is loaded from .tools/naming-gate.py; only its three file
constants are pointed at the temporary folder: the older switch (naming-gate.enforce) at a path that does not exist, so
the older gate is in WARN mode and every refusal below is the placement step's; the placement switch (naming-place.enforce)
at a temporary file for the arms that need it PRESENT and at a path that does not exist for the arm that needs it ABSENT; the
verdict log at a temporary file. The repository's own switch file is never created, touched or read as present, and nothing
is written in the repository. Root maps for arms C are copies in the temporary folder. The arms run in child processes of this
script (the placement step reads files through a process-wide overlay), a few at a time.

The seven arms (design: FWD6_DESIGN_round6.md, "The exercise that would prove it"):
  A  refuse FIX             a NEW schedule irpt-directory-newjob, no cadence word      -> rc=1, the name to use, no blank
  B  let through (negative) the same schedule named irpt-directory-newjob-daily         -> rc=0, PASS
  C  refuse HOLE            a NEW Lambda daily-pull; root unmapped (C) and one-firm entry (C2); control on the real map
  D  ratchet grows          irpt-directory-refresh given cron(0/7 ...): HOLE count 0 -> 1; D-neg: a cron edit on a name that
                            already carries its word: count equal, rc=0
  E  organic (negative)     an existing wrong name touched, not renamed               -> rc=0, WARN
  F  ratchet shrinks (neg)  a diff that removes a HOLE (investor-reporting/intake)   -> rc=0, HOLE count 1 -> 0
                            The HOLE is PLANTED in the overlay the arm hands the gate (a schedule block, minute field 0/7,
                            added to the pre-image), never read from a live registry row's absence (row S12, BF-x-2).
                            Difference control inside the arm: the same planted HOLE ADDED by the diff is refused (rc=1)
                            with the placement switch present, and passes (rc=0, the skip notice printed) with it absent.
  G  switch absent          arm A with the placement switch absent                   -> the same text, rc=0
Arm G runs with NAMING_PLACE_PREVIEW=1 in its child's environment (ruling W1-S22): while the switch is absent the commit
gate skips the placement step unless that variable is 1, and arm G is the arm that runs the step with the switch absent. The
other arms run without it (arm F's control reads the skip on purpose).
One line per arm: expected and got. Last line, printed once: FWD6-ARMS ok=<bool> arms=7 held=<n>
Python 3.9; ASCII only; standard library only.
"""
import concurrent.futures
import contextlib
import difflib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root(start):
    d = start
    for _ in range(40):
        if os.path.isdir(os.path.join(d, ".tools")) and os.path.isdir(os.path.join(d, "org")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("FWD6-ARMS ok=False (no repository root above %s)" % start)


ROOT = repo_root(HERE)
GATE = os.path.join(ROOT, ".tools", "naming-gate.py")
APPLY_GATE = os.path.join(ROOT, ".tools", "naming-apply-gate.py")
REPO_SWITCH = os.path.join(ROOT, "org", "mcp", "naming-place.enforce")
REAL_MAP = os.path.join(ROOT, "infra", "logic", "registry", "root_map.json")
DIR_TF = "infra/aws/terraform/investor-reporting/directory/schedule.tf"
INTAKE_TF = "infra/aws/terraform/investor-reporting/intake/main.tf"
DIR_MAP_KEY = "investor-reporting/directory"
CRO = "4.0.0_SA_CRO"

SCHEDULE_BLOCK = '''
resource "aws_scheduler_schedule" "irpt_directory_newjob" {
  name                         = "%s"
  group_name                   = "default"
  state                        = "ENABLED"
  schedule_expression          = "cron(50 9 ? * MON-FRI *)"
  schedule_expression_timezone = "America/New_York"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = module.irpt_directory_refresh.function_arn
    role_arn = aws_iam_role.irpt_directory_refresh_scheduler.arn
  }
}
'''
LAMBDA_BLOCK = '''
resource "aws_lambda_function" "irpt_directory_daily_pull" {
  function_name = "daily-pull"
  role          = aws_iam_role.irpt_directory_refresh_scheduler.arn
  handler       = "handler.main"
  runtime       = "python3.12"
}
'''


def head_text(path):
    p = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + path], capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("git show HEAD:%s failed rc=%d" % (path, p.returncode))
    return p.stdout.decode("utf-8").replace("\r\n", "\n")


def make_diff(path, pre, post):
    body = "".join(difflib.unified_diff(pre.splitlines(True), post.splitlines(True), "a/" + path, "b/" + path))
    return "diff --git a/%s b/%s\n%s" % (path, path, body)


def load_gate(tmp, place_on, old_enforce=False):
    spec = importlib.util.spec_from_file_location("naming_gate_real", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ENFORCE_FILE = os.path.join(tmp, "older-switch-absent.enforce")
    mod.VERDICT_LOG = os.path.join(tmp, "verdicts.log")
    mod.PLACE_FILE = os.path.join(tmp, "place-switch.enforce")
    if place_on:
        with open(mod.PLACE_FILE, "w") as fh:
            fh.write("temporary switch for the exercise\n")
    elif os.path.exists(mod.PLACE_FILE):  # a run in the same folder that had it present
        os.remove(mod.PLACE_FILE)
    return mod


def run_gate(mod, tmp, path, pre, post):
    df = os.path.join(tmp, "arm.diff")
    with open(df, "w", newline="\n") as fh:
        fh.write(make_diff(path, pre, post))
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.main(["--diff", df])
    out = buf.getvalue()
    return rc, out, [ln for ln in out.splitlines() if ln.strip()]


def run_apply(tmp, name, place_on):
    """The apply gate's plan mode on a hand-built plan that ADDS a schedule called `name` (a name the tree on disk holds, which
    is how a plan of this tree would name it). Same temporary constants as the commit gate."""
    spec = importlib.util.spec_from_file_location("naming_apply_gate_real", APPLY_GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ENFORCE_FILE = os.path.join(tmp, "older-switch-absent.enforce")
    mod.VERDICT_LOG = os.path.join(tmp, "apply-verdicts.log")
    mod.PLACE_FILE = os.path.join(tmp, "apply-place-switch.enforce")
    if place_on:
        with open(mod.PLACE_FILE, "w") as fh:
            fh.write("temporary switch for the exercise" + chr(10))
    plan = {"format_version": "1.2", "resource_changes": [{
        "address": "aws_scheduler_schedule.added", "mode": "managed", "type": "aws_scheduler_schedule", "name": "added",
        "change": {"actions": ["create"], "before": None, "after": {"name": name}}}]}
    pf = os.path.join(tmp, "plan.json")
    with open(pf, "w", newline=chr(10)) as fh:
        json.dump(plan, fh)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.main(["--plan-json", pf])
    lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
    arrow, why = row_of(lines, name)
    return {"rc": rc, "arrow": arrow, "why": why, "last": last_line(lines)}


def row_of(lines, name):
    """(arrow line, why line) of the NAMING row for `name`."""
    for i, ln in enumerate(lines):
        if ln.startswith("NAMING ") and (" %s -> " % name) in ln:
            return ln, (lines[i + 1] if i + 1 < len(lines) else "")
    return "", ""


def last_line(lines):
    return lines[-1] if lines else ""


def map_copy(tmp, tag, mutate):
    with open(REAL_MAP, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    mutate(doc)
    p = os.path.join(tmp, "root_map.%s.json" % tag)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)
    return p


def post_with(pre, block, name):
    return pre + block % name if "%s" in block else pre + block


def edit_line(text, needle, new):
    assert text.count(needle) == 1, "edit target not unique: %r" % needle
    return text.replace(needle, new)


# ----------------------------------------------------------------------------------------------------- the arms (children)
def arm_A(tmp, place_on=True, control=True):
    pre = head_text(DIR_TF)
    post = pre + SCHEDULE_BLOCK % "irpt-directory-newjob"
    mod = load_gate(tmp, place_on)
    rc, out, lines = run_gate(mod, tmp, DIR_TF, pre, post)
    arrow, why = row_of(lines, "irpt-directory-newjob")
    res = {"rc": rc, "arrow": arrow, "why": why, "last": last_line(lines), "out": out}
    res["apply"] = run_apply(tmp, "irpt-directory-refresh", place_on)
    if control:  # difference control: the same gate with the placement step taken out prints the blank
        mod2 = load_gate(tmp, place_on)
        mod2.place_step = lambda rows, meta: rows
        _rc2, out2, lines2 = run_gate(mod2, tmp, DIR_TF, pre, post)
        a2, _w2 = row_of(lines2, "irpt-directory-newjob")
        res["control_arrow"] = a2
    return res


def judge_A(r):
    ap = r["apply"]
    good = (r["rc"] == 1 and r["arrow"].endswith("-> irpt-directory-newjob-daily") and "Owed: use irpt-directory-newjob-daily" in r["why"]
            and "{" not in r["arrow"] and r["control_arrow"].endswith("-> irpt-directory-newjob-{cadence}")
            and ap["rc"] == 1 and ap["arrow"].endswith("-> irpt-directory-refresh-daily") and "Owed: use" in ap["why"])
    got = "rc=%d form=%s blank_in_form=%s owed_text=%s control_without_step=%s; apply gate plan mode on an added irpt-directory-refresh: rc=%d form=%s" % (
        r["rc"], r["arrow"].rsplit("-> ", 1)[-1], "{" in r["arrow"], "Owed: use" in r["why"],
        r["control_arrow"].rsplit("-> ", 1)[-1], ap["rc"], ap["arrow"].rsplit("-> ", 1)[-1])
    return good, got


def arm_B(tmp):
    pre = head_text(DIR_TF)
    post = pre + SCHEDULE_BLOCK % "irpt-directory-newjob-daily"
    mod = load_gate(tmp, True)
    rc, out, lines = run_gate(mod, tmp, DIR_TF, pre, post)
    arrow, _why = row_of(lines, "irpt-directory-newjob-daily")
    return {"rc": rc, "arrow": arrow, "last": last_line(lines), "apply": run_apply(tmp, "irpt-directory-refresh-retry-daily", True)}


def judge_B(r):
    ap = r["apply"]
    good = (r["rc"] == 0 and r["arrow"].startswith("NAMING CONFORMANT") and r["last"] == "NAMING-GATE: PASS 1 graded"
            and ap["rc"] == 0 and ap["last"] == "NAMING-PLAN: PASS 1 graded")
    return good, "rc=%d row=%s last=%s; apply gate plan mode on an added irpt-directory-refresh-retry-daily: rc=%d last=%s" % (
        r["rc"], r["arrow"].split(" ")[1] if r["arrow"] else "none", r["last"], ap["rc"], ap["last"])


def arm_C(tmp, which):
    pre = head_text(DIR_TF)
    post = pre + LAMBDA_BLOCK
    mod = load_gate(tmp, True)
    if which == "c":
        mod.PLACE_MAP = map_copy(tmp, "c", lambda d: d["roots"].pop(DIR_MAP_KEY))
    elif which == "c2":
        def mut(d):
            d["roots"][DIR_MAP_KEY]["fills"] = ["scope"]
        mod.PLACE_MAP = map_copy(tmp, "c2", mut)
    rc, out, lines = run_gate(mod, tmp, DIR_TF, pre, post)
    arrow, why = row_of(lines, "daily-pull")
    return {"rc": rc, "arrow": arrow, "why": why, "which": which}


def judge_C(r):
    w = r["which"]
    if w == "control":
        good = r["rc"] == 1 and r["arrow"].endswith("-> irpt-daily-pull-lambda") and "Owed: use irpt-daily-pull-lambda" in r["why"]
        return good, "control(real map) rc=%d form=%s" % (r["rc"], r["arrow"].rsplit("-> ", 1)[-1])
    if w == "c":
        need = "could not fill {system}: no map entry for this root"
    else:
        need = "could not fill {system}: this root serves more than one firm; its map entry does not give the system"
    good = r["rc"] == 1 and "HOLE" in r["why"] and need in r["why"] and CRO in r["why"]
    return good, "%s rc=%d hole_clause=%s owner_%s=%s" % (w, r["rc"], need.split("could not fill ")[1][:44], CRO, CRO in r["why"])


def counts_of(root, pre_by, post_by):
    sys.path.insert(0, os.path.join(ROOT, "lib"))
    import opal_naming_rootcheck as rcm
    rr = rcm.place_root(root, rcm.DEFAULT_MAP, [], post_by, pre_by, ratchet=True)
    return rr["head_holes"], rr["post_holes"]


def arm_D(tmp, neg):
    pre = head_text(DIR_TF)
    if not neg:
        post = edit_line(pre, 'schedule_expression          = "cron(30 9 ? * MON-FRI *)"',
                         'schedule_expression          = "cron(0/7 9 ? * MON-FRI *)"')
    else:
        post = edit_line(pre, 'schedule_expression          = "cron(40 9 ? * MON-FRI *)"',
                         'schedule_expression          = "cron(40 9 ? * MON *)"')
    mod = load_gate(tmp, True)
    rc, out, lines = run_gate(mod, tmp, DIR_TF, pre, post)
    head_n, post_n = counts_of("infra/aws/terraform/investor-reporting/directory", {DIR_TF: pre}, {DIR_TF: post})
    ratchet = [ln for ln in lines if " <hole-count-ratchet> " in ln]
    why = lines[lines.index(ratchet[0]) + 1] if ratchet else ""
    return {"rc": rc, "ratchet": bool(ratchet), "why": why, "head": head_n, "post": post_n, "neg": neg, "last": last_line(lines)}


def judge_D(r):
    if r["neg"]:
        good = r["rc"] == 0 and not r["ratchet"] and r["head"] == r["post"]
        return good, "D-neg rc=%d holes head=%d post=%d ratchet_row=%s" % (r["rc"], r["head"], r["post"], r["ratchet"])
    good = (r["rc"] == 1 and r["ratchet"] and r["head"] == 0 and r["post"] == 1 and "HOLE SCHEDULE irpt-directory-refresh" in r["why"]
            and "could not fill {cadence}" in r["why"])
    return good, "D rc=%d holes head=%d post=%d ratchet_row=%s new_line=HOLE SCHEDULE irpt-directory-refresh" % (
        r["rc"], r["head"], r["post"], r["ratchet"])


def arm_E(tmp):
    pre = head_text(DIR_TF)
    post = edit_line(pre, 'name                         = "irpt-directory-refresh"\n',
                     'name                         = "irpt-directory-refresh" # touched, not renamed\n')
    mod = load_gate(tmp, True)
    rc, out, lines = run_gate(mod, tmp, DIR_TF, pre, post)
    arrow, why = row_of(lines, "irpt-directory-refresh")
    head_n, post_n = counts_of("infra/aws/terraform/investor-reporting/directory", {DIR_TF: pre}, {DIR_TF: post})
    return {"rc": rc, "arrow": arrow, "why": why, "last": last_line(lines), "head": head_n, "post": post_n,
            "ratchet": any(" <hole-count-ratchet> " in ln for ln in lines)}


def judge_E(r):
    good = (r["rc"] == 0 and "EXISTING" in r["why"] and "WARN" in r["why"] and r["last"] == "NAMING-GATE: WARN 1 graded"
            and not r["ratchet"] and r["head"] == r["post"])
    return good, "rc=%d row=%s last=%s holes head=%d post=%d" % (r["rc"], r["arrow"].split(" ")[1] if r["arrow"] else "none",
                                                                r["last"], r["head"], r["post"])


HOLE_BLOCK = '''
resource "aws_scheduler_schedule" "x_hole" {
  name                = "irpt-intake-zhole"
  schedule_expression = "cron(0/7 9 ? * MON-FRI *)"
}
'''


def arm_F(tmp):
    base = head_text(INTAKE_TF)
    pre = base + HOLE_BLOCK  # the HOLE planted in the overlay: the pre-image the gate is handed carries it
    mod = load_gate(tmp, True)
    rc, out, lines = run_gate(mod, tmp, INTAKE_TF, pre, base)
    head_n, post_n = counts_of("infra/aws/terraform/investor-reporting/intake", {INTAKE_TF: pre}, {INTAKE_TF: base})
    # difference control: the planted HOLE added by the diff, switch present then absent
    modp = load_gate(tmp, True)
    rc_on, _o, lines_on = run_gate(modp, tmp, INTAKE_TF, base, pre)
    moda = load_gate(tmp, False)
    rc_off, out_off, lines_off = run_gate(moda, tmp, INTAKE_TF, base, pre)
    return {"rc": rc, "head": head_n, "post": post_n, "ratchet": any(" <hole-count-ratchet> " in ln for ln in lines),
            "last": last_line(lines), "ctl_on_rc": rc_on, "ctl_on_ratchet": any(" <hole-count-ratchet> " in ln for ln in lines_on),
            "ctl_off_rc": rc_off, "ctl_off_notice": any("PLACE-NOTICE" in ln for ln in lines_off)}


def judge_F(r):
    good = (r["rc"] == 0 and not r["ratchet"] and r["head"] == 1 and r["post"] == 0
            and r["ctl_on_rc"] == 1 and r["ctl_on_ratchet"] and r["ctl_off_rc"] == 0 and r["ctl_off_notice"])
    return good, "rc=%d holes head=%d post=%d ratchet_row=%s last=%s | control: planted HOLE added, switch present rc=%d ratchet_row=%s; switch absent rc=%d skip_notice=%s" % (
        r["rc"], r["head"], r["post"], r["ratchet"], r["last"], r["ctl_on_rc"], r["ctl_on_ratchet"], r["ctl_off_rc"], r["ctl_off_notice"])


def child(arm):
    with tempfile.TemporaryDirectory(prefix="fwd6_arm_") as tmp:
        if arm == "A":
            r = arm_A(tmp)
        elif arm == "B":
            r = arm_B(tmp)
        elif arm in ("C0", "C1", "C2"):
            r = arm_C(tmp, {"C0": "control", "C1": "c", "C2": "c2"}[arm])
        elif arm in ("D", "Dneg"):
            r = arm_D(tmp, arm == "Dneg")
        elif arm == "E":
            r = arm_E(tmp)
        elif arm == "F":
            r = arm_F(tmp)
        elif arm == "G":
            r = arm_A(tmp, place_on=False, control=False)
        else:
            raise SystemExit("unknown arm %s" % arm)
    r.pop("out", None)
    print("CHILD " + json.dumps(r))
    return 0


# ---------------------------------------------------------------------------------------------------------------- the parent
def snapshot():
    p = subprocess.run(["git", "-C", ROOT, "status", "--porcelain"], capture_output=True)
    log = os.path.join(ROOT, "org", "mcp", "naming-gate-verdicts.log")
    return (p.stdout, os.path.exists(REPO_SWITCH), os.path.getsize(log) if os.path.exists(log) else None)


def spawn(arm):
    env = dict(os.environ)
    env.pop("NAMING_PLACE_PREVIEW", None)
    if arm == "G":
        env["NAMING_PLACE_PREVIEW"] = "1"  # ruling W1-S22: the step runs with the switch absent only under this variable
    p = subprocess.run([sys.executable, os.path.abspath(__file__), "--child", arm], capture_output=True, cwd=ROOT, env=env)
    out = p.stdout.decode("utf-8", "replace")
    for ln in out.splitlines():
        if ln.startswith("CHILD "):
            return json.loads(ln[6:])
    raise RuntimeError("arm %s: no result (rc=%d): %s" % (arm, p.returncode, (out + p.stderr.decode("utf-8", "replace"))[-600:]))


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--child":
        return child(sys.argv[2])
    before = snapshot()
    if before[1]:
        print("FWD6-ARMS ok=False (org/mcp/naming-place.enforce is PRESENT in the repository before the run)")
        return 1
    names = ["A", "B", "C0", "C1", "C2", "D", "Dneg", "E", "F", "G"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        got = dict(zip(names, pool.map(spawn, names)))
    A_good, A_got = judge_A(got["A"])
    B_good, B_got = judge_B(got["B"])
    cs = [judge_C(got[k]) for k in ("C0", "C1", "C2")]
    ds = [judge_D(got["D"]), judge_D(got["Dneg"])]
    E_good, E_got = judge_E(got["E"])
    F_good, F_got = judge_F(got["F"])
    a, g = got["A"], got["G"]
    same_text = bool(g["arrow"]) and g["arrow"] == a["arrow"] and g["why"] == a["why"]
    ga, aa = g["apply"], a["apply"]
    same_apply = bool(ga["arrow"]) and ga["arrow"] == aa["arrow"] and ga["why"] == aa["why"]
    G_good = (g["rc"] == 0 and same_text and g["last"] == "NAMING-GATE: WARN 1 graded"
              and ga["rc"] == 0 and same_apply)
    G_got = "rc=%d same_row_text_as_A=%s last=%s; apply gate plan mode: rc=%d same_row_text_as_A=%s" % (
        g["rc"], same_text, g["last"], ga["rc"], same_apply)
    arms = [
        ("A refuse FIX", "rc=1; form irpt-directory-newjob-daily; owed text; no blank; control prints the blank", A_good, A_got),
        ("B let through", "rc=0; CONFORMANT; NAMING-GATE: PASS 1 graded", B_good, B_got),
        ("C refuse HOLE", "rc=1 x3; control FIX irpt-daily-pull-lambda; unmapped HOLE no map entry and one-firm HOLE, owner %s" % CRO,
         all(c[0] for c in cs), " | ".join(c[1] for c in cs)),
        ("D ratchet grows", "rc=1; holes 0 -> 1; new HOLE line; D-neg: rc=0, holes equal", all(d[0] for d in ds),
         " | ".join(d[1] for d in ds)),
        ("E organic", "rc=0; EXISTING name WARN; holes equal; no ratchet row", E_good, E_got),
        ("F ratchet shrinks", "rc=0; HOLE planted in overlay, holes 1 -> 0; no ratchet row; control: refused rc=1 switch present, rc=0 switch absent", F_good, F_got),
        ("G switch absent", "arm A text unchanged; rc=0; NAMING-GATE: WARN 1 graded", G_good, G_got),
    ]
    held = 0
    for label, expected, good, gotten in arms:
        held += 1 if good else 0
        print("ARM %s | %s | expected: %s | got: %s" % (label, "HELD" if good else "NOT HELD", expected, gotten))
    after = snapshot()
    clean = before == after and not after[1]
    print("REPOSITORY left as found: %s (placement switch present in repo: %s; git status and verdict-log size unchanged: %s)" % (
        clean, after[1], before[0] == after[0] and before[2] == after[2]))
    ok = held == 7 and clean
    print("FWD6-ARMS ok=%s arms=7 held=%d" % (ok, held))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
