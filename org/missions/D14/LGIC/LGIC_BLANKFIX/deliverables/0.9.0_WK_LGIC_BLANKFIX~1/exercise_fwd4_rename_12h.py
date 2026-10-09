"""exercise_fwd4_rename_12h -- FWD-4 R1 (LGIC_BLANKFIX BF-ac-1): ONE twice-a-day schedule renamed -12h from its list line alone.

Takes one schedule's list line (argument 1; when none is given, the line the real root check prints for
keyword-intelligence-generator-daily in the news-pipeline root is fetched and used as that one line: its expression is
cron(0 8,20 * * ? *), two fires 12 hours apart, and the current name says daily) and nothing else. From that line only -- current
name, new name, file:line -- it writes the rename into a TEMPORARY COPY of the .tf file (the repository is never written), builds
the unified diff of the copy against the repository's file, and runs the real .tools/naming-gate.py --diff --enforce on that diff.
Before the gate it asserts the line's new name ends in -12h and that opal_naming_cadence reads that schedule's own expression as
12h. The renamed name must grade CONFORMANT and no placement refusal may print. No apply, no AWS, no network.

Last line: FWD4-RENAME-12H ok=True name=<new> grade=CONFORMANT   (ok=False otherwise).
"""
import difflib
import os
import re
import shutil
import subprocess
import sys
import tempfile


def _repo_root():
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(d, "lib", "opal_naming.py")):
            return d
        up = os.path.dirname(d)
        if up == d:
            raise SystemExit("FWD4-RENAME-12H ok=False reason=repository root not found above %s" % __file__)
        d = up


ROOT = _repo_root()
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import opal_naming_cadence as cad  # noqa: E402
import opal_naming_rootcheck as rc  # noqa: E402

MAP = "infra/logic/registry/root_map.json"
# keyword-intelligence-generator-daily: an EventBridge rule, cron(0 8,20 * * ? *), twice a day 12 hours apart, no firm token in
# its new name (the 49f schedules are refused for a hand-kept firm token: row LGIC_BLANKFIX-D1-W1-S7, the work of BF-ac-2).
DEFAULT_ROOT = "infra/aws/terraform/news-pipeline"
DEFAULT_CURRENT = "keyword-intelligence-generator-daily"
DEFAULT_TYPE = "EVENT_RULE"


def fetch_line():
    lines = []
    rc.check_root(DEFAULT_ROOT, MAP, out=lines.append, report_only=True)
    hit = [ln for ln in lines if ln.startswith("FIX %s %s -> " % (DEFAULT_TYPE, DEFAULT_CURRENT))]
    if len(hit) != 1:
        raise SystemExit("FWD4-RENAME-12H ok=False reason=%d list lines for %s, not 1" % (len(hit), DEFAULT_CURRENT))
    return hit[0]


def fail(why):
    print("FWD4-RENAME-12H ok=False reason=%s" % why)
    return 1


def main(argv):
    line = argv[0] if argv else fetch_line()
    print("LIST LINE: " + line)
    parts = rc._split_line(line)
    if parts is None:
        return fail("not a list line")
    kind, typ, cur, new, where = parts
    if kind != "FIX" or typ not in ("EVENT_RULE", "SCHEDULE"):
        return fail("the line is %s %s, not a FIX schedule line" % (kind, typ))
    if not new.endswith("-12h"):
        return fail("the list line's new name %s does not end in -12h" % new)
    rows = [r for r in cad.cadences(os.path.dirname(where.rpartition(":")[0])) if r["current"] == cur and r["where"] == where]
    if len(rows) != 1 or rows[0]["word"] != "12h":
        return fail("the reader does not read %s at %s as 12h from its own expression: %r" % (cur, where, rows))
    print("EXPRESSION: %s -> %s (%s)" % (rows[0]["expression"], rows[0]["word"], rows[0]["basis"]))
    path, _, lineno = where.rpartition(":")
    if not path.endswith(".tf") or not lineno.isdigit():
        return fail("the line points at %s, not a .tf file:line" % where)
    with open(path, "r", encoding="utf-8", newline="") as fh:
        before = fh.read()
    tmpdir = tempfile.mkdtemp(prefix="fwd4_rename_")
    try:
        copy = os.path.join(tmpdir, os.path.basename(path))
        shutil.copyfile(path, copy)
        with open(copy, "r", encoding="utf-8", newline="") as fh:
            text = fh.read()
        eol = "\r\n" if "\r\n" in text else "\n"
        rows = text.split(eol)
        # the resource block the list line points at: from file:line down to its first closing brace at column 0
        start = int(lineno) - 1
        end = start
        while end < len(rows) and rows[end] != "}":
            end += 1
        pat = re.compile(r'^(\s*name\s*=\s*)"%s"(\s*)$' % re.escape(cur))
        hits = [i for i in range(start, min(end, len(rows))) if pat.match(rows[i])]
        if len(hits) != 1:
            return fail("%d name attributes '%s' in the block at %s, not 1" % (len(hits), cur, where))
        rows[hits[0]] = pat.sub(lambda m: '%s"%s"%s' % (m.group(1), new, m.group(2)), rows[hits[0]])
        with open(copy, "w", encoding="utf-8", newline="") as fh:
            fh.write(eol.join(rows))
        with open(copy, "r", encoding="utf-8", newline="") as fh:
            after = fh.read()
        if after == before:
            return fail("the copy did not change")
        diff = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                            fromfile="a/" + path, tofile="b/" + path, n=3))
        print("DIFF (temporary copy against the repository file; the repository is not written):")
        print(diff.rstrip("\n"))
        dpath = os.path.join(tmpdir, "rename.diff")
        with open(dpath, "w", encoding="utf-8", newline="") as fh:
            fh.write(diff)
        proc = subprocess.run([sys.executable, ".tools/naming-gate.py", "--diff", dpath, "--enforce"],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=240)
        out = proc.stdout
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    print("GATE OUTPUT (rc=%d):" % proc.returncode)
    print(out.rstrip("\n"))
    verdicts = [ln for ln in out.splitlines() if ln.startswith("NAMING ") and (' %s ' % new) in ln + " "]
    grade = None
    for ln in verdicts:
        m = re.match(r"^NAMING (\S+) %s:\d+ %s -> " % (re.escape(path), re.escape(new)), ln)
        if m:
            grade = m.group(1)
    refused = [ln for ln in out.splitlines()
               if ln.startswith("NAMING-PLACE: REFUSE") or ln.startswith("NAMING PLACE") or ln.startswith("NAMING REFUSE")
               or ln.startswith("NAMING PLACE-REFUSE") or ln.startswith("NAMING ERROR")]
    ok = proc.returncode == 0 and grade == "CONFORMANT" and not refused
    print("FWD4-RENAME-12H ok=%s name=%s grade=%s" % (ok, new, grade))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
