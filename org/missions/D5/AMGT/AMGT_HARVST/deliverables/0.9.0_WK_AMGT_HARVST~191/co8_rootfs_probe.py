"""co8_rootfs_probe.py -- AMGT_HARVST HVST-co-8: the minimal-root probe of the gold-refresh image recipe.

Run from the repo root of the worktree:  python -I <this file>
Writes co8_probe.out in this folder (LF endings) and echoes it.

The root is a temporary directory laid out exactly as the Dockerfile's COPY lines lay the image out (destinations under
${LAMBDA_TASK_ROOT} or /var/task). Every child runs under `python -I` with the repository root NOT on sys.path; the
temporary root is the only project path inserted, as the image's working directory is for `python -m`.
Two S3-touching steps are read-only (the roster build lists and gets; the skip path must make no S3 call). The
S3 operation count is taken from botocore's API call hook, so it counts every S3 operation, not one client handle.

The NEGATIVE CONTROL runs first: a second copy of the root without one data file the roster step reads by path
(the legal-names file named by lib/opal_data_harvest/config.json); the roster step there must fail.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.getcwd()
DOCKERFILE = os.path.join(REPO, "infra", "aws", "harvest", "gold-refresh", "Dockerfile")
OUT = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                   "0.9.0_WK_AMGT_HARVST~191", "co8_probe.out")
SCRATCH = os.path.join(REPO, ".scratch")
TASK_ROOTS = ("${LAMBDA_TASK_ROOT}/", "/var/task/")
COPY_RE = re.compile(r"^COPY\s+(\S+)\s+(\S+)\s*$")
LEGAL_NAMES_REL = ("org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~120/"
                   "rank_universe_identity_20261008.json")
PY = sys.executable
TIMEOUT = 900

CHILD_PATH = r'''
import os, sys
root, repo = sys.argv[1], sys.argv[2]
sys.path.insert(0, root)
def same(a, b):
    return os.path.normcase(os.path.abspath(a or os.curdir)) == os.path.normcase(os.path.abspath(b))
on = any(same(p, repo) for p in sys.path)
print("PROBE root=%s repo_on_path=%s" % (root, "yes" if on else "no"))
'''

CHILD_HELP = r'''
import runpy, sys
root = sys.argv[1]
sys.path.insert(0, root)
sys.argv = ["gold_refresh", "--help"]
runpy.run_module("lib.research.harvest.gold_refresh", run_name="__main__")
'''

CHILD_SKIP = r'''
import contextlib, datetime as dt, io, sys
root = sys.argv[1]
sys.path.insert(0, root)
import botocore.client as bc
ops = {"n": 0}
_orig = bc.BaseClient._make_api_call
def _counting(self, operation_name, api_params):
    if self.meta.service_model.service_name == "s3":
        ops["n"] += 1
    return _orig(self, operation_name, api_params)
bc.BaseClient._make_api_call = _counting
from lib.research.harvest import gold_refresh
buf = io.StringIO()
now = dt.datetime(2026, 10, 24, 14, 0, tzinfo=dt.timezone.utc)
with contextlib.redirect_stdout(buf):
    rc = gold_refresh.main(["--require-trading-day"], now=now)
line = buf.getvalue().strip()
print("PROBE skip now=2026-10-24T14:00:00Z line=%s rc=%d s3_gets=%d" % (line, rc, ops["n"]))
'''

CHILD_ROSTER = r'''
import sys
root = sys.argv[1]
sys.path.insert(0, root)
from lib.research.harvest import universe_securities
roster, summary = universe_securities.build()
universe = summary.get("universe") or {}
print("NOTE roster universe_source=%s fallback_reason=%s" % (ascii(universe.get("source")), ascii(universe.get("fallback_reason"))))
print("PROBE roster names=%d" % len(roster))
'''

lines = []


def emit(text):
    lines.append(text)


def copy_pairs(text):
    pairs = []
    for raw in text.split("\n"):
        m = COPY_RE.match(raw.strip())
        if m:
            pairs.append((m.group(1), m.group(2)))
    return pairs


def image_rel(dst):
    for root in TASK_ROOTS:
        if dst.startswith(root):
            return dst[len(root):]
    return None


def build_root(tmp, pairs):
    for src, dst in pairs:
        rel = image_rel(dst)
        if rel is None:
            continue
        src_path = os.path.join(REPO, *src.rstrip("/").split("/"))
        if not os.path.exists(src_path):
            raise SystemExit("COPY source is missing in the repository: %s" % src)
        target = os.path.join(tmp, *rel.rstrip("/").split("/"))
        if os.path.isdir(src_path):
            shutil.copytree(src_path, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.copyfile(src_path, target)


def run_child(code, args, cwd):
    return subprocess.run([PY, "-I", "-c", code] + args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=TIMEOUT)


def keep(stdout):
    return [ln for ln in stdout.splitlines() if ln.startswith("PROBE ") or ln.startswith("NOTE ")]


def main():
    with open(DOCKERFILE, "r", encoding="utf-8") as fh:
        pairs = copy_pairs(fh.read())
    failures = 0
    tmp_root = tempfile.mkdtemp(prefix="co8_root_", dir=SCRATCH)
    tmp_ctrl = tempfile.mkdtemp(prefix="co8_ctrl_", dir=SCRATCH)
    try:
        build_root(tmp_root, pairs)

        # NEGATIVE CONTROL first: the second copy lacks the legal-names file the roster step reads by path.
        build_root(tmp_ctrl, pairs)
        victim = os.path.join(tmp_ctrl, *LEGAL_NAMES_REL.split("/"))
        if not os.path.isfile(victim):
            raise SystemExit("control victim not in the control root: %s" % LEGAL_NAMES_REL)
        os.remove(victim)
        ctrl = run_child(CHILD_ROSTER, [tmp_ctrl], tmp_ctrl)
        detected = ctrl.returncode != 0 and "legal-name join" in (ctrl.stdout + ctrl.stderr)
        emit("PROBE-CONTROL missing_file_detected=%s" % ("yes" if detected else "no"))
        if not detected:
            failures += 1

        # The real minimal root.
        path = run_child(CHILD_PATH, [tmp_root, REPO], tmp_root)
        emit_lines = keep(path.stdout)
        if path.returncode != 0 or not emit_lines:
            failures += 1
            emit("PROBE root=FAILED rc=%d" % path.returncode)
        for ln in emit_lines:
            emit(ln)
            if "repo_on_path=yes" in ln:
                failures += 1

        help_run = run_child(CHILD_HELP, [tmp_root], tmp_root)
        emit("PROBE help rc=%d" % help_run.returncode)
        if help_run.returncode != 0:
            failures += 1

        skip = run_child(CHILD_SKIP, [tmp_root], tmp_root)
        skip_lines = keep(skip.stdout)
        if skip.returncode != 0 or not skip_lines:
            failures += 1
            emit("PROBE skip FAILED rc=%d" % skip.returncode)
        for ln in skip_lines:
            emit(ln)
            if "line=GOLD-SKIPPED not_a_trading_day" not in ln or "s3_gets=0" not in ln or " rc=0 " not in ln:
                failures += 1

        roster = run_child(CHILD_ROSTER, [tmp_root], tmp_root)
        roster_lines = keep(roster.stdout)
        if roster.returncode != 0:
            failures += 1
            emit("PROBE roster FAILED rc=%d" % roster.returncode)
            tail = (roster.stdout + roster.stderr).strip().splitlines()[-4:]
            for ln in tail:
                emit("NOTE roster-tail %s" % ascii(ln)[:300])
        for ln in roster_lines:
            emit(ln)
            m = re.match(r"^PROBE roster names=(\d+)$", ln)
            if m is not None and int(m.group(1)) < 1:
                failures += 1
        if roster.returncode == 0 and not any(re.match(r"^PROBE roster names=[1-9]\d*$", ln) for ln in roster_lines):
            failures += 1
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
        shutil.rmtree(tmp_ctrl, ignore_errors=True)

    emit("ROOTFS-CHECK failures=%d" % failures)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="ascii", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    for ln in lines:
        os.write(1, (ln + "\n").encode("ascii", "replace"))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
