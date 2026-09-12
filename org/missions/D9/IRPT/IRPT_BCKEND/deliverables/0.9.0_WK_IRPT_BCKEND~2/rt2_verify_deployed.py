#!/usr/bin/env python3
"""VERIFY A DEPLOYED FUNCTION BY ITS SERVED BYTES -- not by the zip this box happens to hold.

Usage:  python rt2_verify_deployed.py <function-name> [<function-name> ...]

FOUR READS, IN THIS ORDER, AND THE LAST ONE IS THE ONLY ONE THAT CAN SEE A MISSING MODULE:

  1. `get-function-configuration` -> Handler, CodeSha256, State, LastUpdateStatus.
  2. The SERVED artifact, downloaded from the function's own `Code.Location`, and its sha256
     compared with the live CodeSha256. This is the artifact AWS will actually run, fetched from
     AWS -- never the local build, which is a producer reading back its own output.
  3. The declared `artifact_sha256` in lambda-source-map.json, so the RECORD and the WORLD are
     compared rather than each being checked against itself.
  4. EXTRACT-AND-IMPORT in the flat /var/task layout: a FRESH isolated interpreter, the repo
     ASSERTED absent from sys.path, and -- only for the functions whose Terraform attaches it --
     the live irpt-common `python/` mounted as /opt/python. `CodeSha256` equality cannot see a
     missing module by construction: a hash certifies bytes and nothing in the deploy path ever
     imports them.

AND THE NEGATIVE CONTROL RUNS EVERY TIME: the same extracted tree with `served.py` deleted must
FAIL to import. Without it, an IMPORT-OK proves only that the probe can print IMPORT-OK.

NO WRITE OF ANY KIND. Reads AWS, reads the repo, writes only under the system temp directory.
ASCII only. Exit 0 always: the printed verdict is the result.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([os.pardir] * 7)))
# THE .cmd SIBLING, DELIBERATELY: .tools/aws is a BASH shim and CreateProcess refuses it with
# WinError 193 ("not a valid Win32 application"). Both shims exist or neither does; this one is
# the entry point a Windows process can spawn.
AWS = os.path.join(REPO, ".tools", "aws.cmd")
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
LAYER_ZIP = os.path.join(REPO, ".scratch", "layer", "irpt-common-5.zip")

# MEASURED FROM TERRAFORM (`layers = []` vs an arn), never from the layer map.
LAYERED = {"irpt-performance-adapter", "irpt-narrative", "irpt-export-render"}

PROBE = (
    "import sys, os\n"
    "TASK = os.path.dirname(os.path.abspath(__file__))\n"
    "LAYER = os.environ.get('RT2_LAYER_PYTHON') or ''\n"
    "sys.path.insert(0, TASK)\n"
    "if LAYER:\n"
    "    sys.path.insert(1, LAYER)\n"
    "marks = [p for p in sys.path if 'investor-reporting' in p or 'wk-irpt' in p]\n"
    "assert not marks, 'the repository is on sys.path: %r' % marks\n"
    "import entry\n"
    "print('IMPORT-OK lambda_handler=%s' % (getattr(entry, 'lambda_handler', None) is not None))\n"
)

_layer_dir = []


def layer_python():
    if _layer_dir:
        return _layer_dir[0]
    if not os.path.isfile(LAYER_ZIP):
        print("WARN: %s absent -- a layered function cannot be probed in its real layout"
              % LAYER_ZIP)
        _layer_dir.append("")
        return ""
    d = tempfile.mkdtemp(prefix="rt2-verify-layer-")
    with zipfile.ZipFile(LAYER_ZIP) as zf:
        zf.extractall(d)
    _layer_dir.append(os.path.join(d, "python"))
    return _layer_dir[0]


def aws(*args):
    proc = subprocess.run([AWS] + list(args), capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError("aws %s -> rc=%d %s" % (" ".join(args), proc.returncode,
                                                   (proc.stderr or "")[:300]))
    return (proc.stdout or "").strip()


def probe(task_dir, layered, label):
    path = os.path.join(task_dir, "_probe.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(PROBE)
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    env.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")
    env["RT2_LAYER_PYTHON"] = layer_python() if layered else ""
    proc = subprocess.run([sys.executable, "-I", "_probe.py"], cwd=task_dir, env=env,
                          capture_output=True, text=True, timeout=180)
    out = ((proc.stdout or "") + (proc.stderr or "")).strip().splitlines()
    last = out[-1] if out else "(no output)"
    ok = proc.returncode == 0 and "IMPORT-OK" in (proc.stdout or "")
    print("    %-14s %s  %s" % (label, "IMPORT-OK " if ok else "IMPORT-FAIL", last[:140]))
    return ok


def verify(function):
    print("%s" % function)
    handler, live_sha, state, status = aws(
        "lambda", "get-function-configuration", "--function-name", function,
        "--region", "us-east-1", "--output", "text",
        "--query", "[Handler,CodeSha256,State,LastUpdateStatus]").split("\t")
    print("    live: handler=%s state=%s/%s" % (handler, state, status))

    location = aws("lambda", "get-function", "--function-name", function,
                   "--region", "us-east-1", "--output", "text", "--query", "Code.Location")
    tmp = tempfile.mkdtemp(prefix="rt2-verify-")
    try:
        blob = os.path.join(tmp, "served.zip")
        with urllib.request.urlopen(location, timeout=180) as r, open(blob, "wb") as fh:
            fh.write(r.read())
        with open(blob, "rb") as fh:
            served_sha = base64.b64encode(hashlib.sha256(fh.read()).digest()).decode("ascii")

        with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
            declared = (json.load(fh)["functions"][function].get("artifact_sha256") or "")

        chain = (served_sha == live_sha) and (declared == live_sha)
        print("    declared artifact_sha256 = %s" % declared)
        print("    S3/served sha256         = %s" % served_sha)
        print("    live CodeSha256          = %s" % live_sha)
        print("    THREE-WAY CHAIN: %s" % ("EQUAL" if chain else "MISMATCH"))

        task = os.path.join(tmp, "task")
        os.makedirs(task)
        with zipfile.ZipFile(blob) as zf:
            zf.extractall(task)
        layered = function in LAYERED
        print("    layout: /var/task + %s" % ("/opt/python (layer attached)" if layered
                                              else "no layer (layers = [])"))
        ok = probe(task, layered, "SERVED")

        # THE NEGATIVE CONTROL, on the SERVED tree: delete served.py and re-import.
        control = os.path.join(tmp, "control")
        shutil.copytree(task, control)
        victim = os.path.join(control, "served.py")
        had_victim = os.path.isfile(victim)
        if had_victim:
            os.remove(victim)
        neg = probe(control, layered, "NEGATIVE-CTL")
        fires = had_victim and not neg
        if not had_victim:
            print("    WARN: the served artifact carries NO served.py, so the control could not "
                  "be armed -- and that absence is itself the defect this arm looks for")
        verdict = ok and chain and fires
        print("    VERDICT: %s" % ("VERIFIED" if verdict else "NOT VERIFIED"))
        return verdict
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main(argv):
    names = argv[1:]
    if not names:
        print(__doc__)
        return 0
    results = [(n, verify(n)) for n in names]
    print("")
    print("%d of %d function(s) VERIFIED on their served bytes"
          % (sum(1 for _n, v in results if v), len(results)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
