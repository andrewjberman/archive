"""co8_build_dry.py -- AMGT_HARVST HVST-co-8: the buildspec type check and the cloud-free dry run of the build script.

Run from the repo root of the worktree:  python -I <this file>
Writes co8_build_dry.out in this folder (LF endings) and echoes it.

1. BUILDSPEC-CONTROL: plants one unquoted mapping item (`- echo "A: b"`) in memory; the type test must flag it.
2. BUILDSPEC-CHECK: loads the real buildspec.yml with yaml.safe_load and tests the TYPE of every item of every
   phases.*.commands list (the cn5 method).
3. STUB-CONTROL: an `aws` stub that records any call and exits 1 is put first on PATH; a deliberate call must be recorded.
4. Runs build-image.sh --dry-run under that PATH and counts the stub's records (zero expected).
"""
import os
import re
import shutil
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML is not importable in this interpreter")

REPO = os.getcwd()
RECIPE = "infra/aws/harvest/gold-refresh"
BUILDSPEC = os.path.join(REPO, *RECIPE.split("/"), "buildspec.yml")
BUILD_SCRIPT = RECIPE + "/build-image.sh"
SCRATCH = os.path.join(REPO, ".scratch", "co8_stub")
STUB_DIR = os.path.join(SCRATCH, "bin")
STUB = os.path.join(STUB_DIR, "aws")
LOG = os.path.join(SCRATCH, "aws_calls.log")
OUT = os.path.join(REPO, "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                   "0.9.0_WK_AMGT_HARVST~191", "co8_build_dry.out")
BASH = shutil.which("bash")
ZIP_RE = re.compile(r"^== zip contents: (\d+) entries")
PLANT = 'phases:\n  build:\n    commands:\n      - echo "A: b"\n'

lines = []


def emit(text):
    lines.append(text)


def count_commands(doc):
    """(n_items, bad): every phases.*.commands item, and each item that is not a str (or a phase lacking a list)."""
    n_items = 0
    bad = []
    phases = doc.get("phases") if isinstance(doc, dict) else None
    if not isinstance(phases, dict):
        return 0, [("phases", "not-a-mapping")]
    for phase_name in sorted(phases):
        phase = phases[phase_name]
        commands = phase.get("commands") if isinstance(phase, dict) else None
        if not isinstance(commands, list):
            bad.append(("phases.%s.commands" % phase_name, "not-a-list"))
            continue
        for idx, item in enumerate(commands):
            n_items += 1
            if not isinstance(item, str):
                bad.append(("phases.%s.commands[%d]" % (phase_name, idx), type(item).__name__))
    return n_items, bad


ok = True

# 1. buildspec control
_, planted_bad = count_commands(yaml.safe_load(PLANT))
detected = len(planted_bad) == 1
emit("BUILDSPEC-CONTROL planted_nonstring_detected=%s" % ("yes" if detected else "no"))
ok = ok and detected

# 2. buildspec type check
with open(BUILDSPEC, "r", encoding="utf-8") as fh:
    real_doc = yaml.safe_load(fh.read())
n_cmds, real_bad = count_commands(real_doc)
for where, type_name in real_bad:
    emit("BUILDSPEC-NONSTRING %s type=%s" % (where, type_name))
emit("BUILDSPEC-CHECK commands=%d non_string=%d" % (n_cmds, len(real_bad)))
ok = ok and not real_bad

# 3. the stub: a bash script named aws that appends its argv to the log and exits 1
os.makedirs(STUB_DIR, exist_ok=True)
if os.path.exists(LOG):
    os.remove(LOG)
stub_log_posix = LOG.replace("\\", "/")
with open(STUB, "w", encoding="ascii", newline="\n") as fh:
    fh.write("#!/usr/bin/env bash\n")
    fh.write("printf 'AWS-STUB-CALL %%s\\n' \"$*\" >> '%s'\n" % stub_log_posix)
    fh.write("exit 1\n")
os.chmod(STUB, 0o755)
env = dict(os.environ)
env["PATH"] = STUB_DIR + os.pathsep + os.environ.get("PATH", "")
control = subprocess.run([BASH, "-c", "aws stub-control-call"], cwd=REPO, env=env, capture_output=True, timeout=120)
recorded = 0
if os.path.isfile(LOG):
    with open(LOG, "r", encoding="ascii", errors="replace") as fh:
        recorded = sum(1 for ln in fh if "stub-control-call" in ln)
emit("STUB-CONTROL recorded=%d rc=%d" % (recorded, control.returncode))
ok = ok and recorded == 1
if os.path.exists(LOG):
    os.remove(LOG)

# 4. the dry run, with the stub first on PATH
dry = subprocess.run([BASH, BUILD_SCRIPT, "--dry-run"], cwd=REPO, env=env, capture_output=True, timeout=600)
dry_text = (dry.stdout + dry.stderr).decode("utf-8", "replace")
files = None
for raw in dry_text.splitlines():
    text = raw.rstrip("\r")
    emit("DRY| " + text.encode("ascii", "replace").decode("ascii"))
    m = ZIP_RE.match(text)
    if m:
        files = int(m.group(1))
cloud_calls = 0
if os.path.isfile(LOG):
    with open(LOG, "r", encoding="ascii", errors="replace") as fh:
        cloud_calls = sum(1 for ln in fh if ln.startswith("AWS-STUB-CALL"))
emit("BUILD-DRY-RUN-RC rc=%d" % dry.returncode)
emit("BUILD-DRY-RUN files=%d cloud_calls=%d" % (files or 0, cloud_calls))
ok = ok and dry.returncode == 0 and files is not None and files >= 1 and cloud_calls == 0

emit("BUILD-DRY-RUN-VERDICT %s" % ("PASS" if ok else "FAIL"))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="ascii", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")
for ln in lines:
    os.write(1, (ln + "\n").encode("ascii", "replace"))
sys.exit(0 if ok else 1)
