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
import re
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

# THERE IS NO LAYER LIST IN THIS FILE ANY MORE, AND THAT IS THE FIX RATHER THAN A TIDY-UP.
#
# This file used to keep its own `LAYERED` set beside the packager's. The two diverged the moment
# amendment 3 granted holdings: the packager learned that irpt-holdings attaches irpt-common and
# this verifier did not, so it probed the SERVED holdings artifact with NO /opt/python and reported
# `IMPORT-FAIL: No module named 'keys'` on a sound zip -- a false RED on a function that had just
# been applied, which is the most expensive direction for this instrument to be wrong in. It is the
# THIRD time in this cell that two hand-maintained copies of one fact disagreed (the two in-lane
# test sets, the battery reading the wrong one of them, and now this).
#
# So the attachment is READ FROM THE FUNCTION ITSELF, at the same moment as its handler and its
# CodeSha256 -- one read, of the thing that decides. A list that cannot drift is better than a list
# that is currently correct.

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
    """The LIVE layer's `python/`, extracted once. Downloads the cache itself when absent.

    ROW W1-S17 / S54: a fresh worktree's `.scratch/layer/` cache of the irpt-common layer zip is
    gitignored and therefore absent on every fresh checkout, which made this instrument print
    NOT VERIFIED for the four layered functions while the three-way sha256 chain (declared, S3,
    live CodeSha256) read EQUAL on 7 of 7 in the SAME run -- a false FAIL caused by incidental
    local state, never by the served bytes. Rather than WARN and give up, fetch the PUBLISHED
    layer version's own zip (`get-layer-version` -> `Content.Location`, the same kind of read
    `verify()` already performs on a function's `Code.Location`) into the cache path and proceed.
    A fetch failure still WARNs and returns "" -- this is a repair of the cache-miss path, not a
    new hard dependency on network reachability.
    """
    if _layer_dir:
        return _layer_dir[0]
    if not os.path.isfile(LAYER_ZIP):
        match = re.search(r"([A-Za-z0-9_-]+)-(\d+)\.zip$", os.path.basename(LAYER_ZIP))
        if not match:
            print("WARN: %s absent and no layer name/version could be parsed from its own "
                  "filename -- a layered function cannot be probed in its real layout"
                  % LAYER_ZIP)
            _layer_dir.append("")
            return ""
        layer_name, version = match.group(1), match.group(2)
        print("FETCHING: %s absent -- downloading %s version %s (row W1-S17/S54)"
              % (LAYER_ZIP, layer_name, version))
        try:
            location = aws("lambda", "get-layer-version", "--layer-name", layer_name,
                           "--version-number", version, "--region", "us-east-1",
                           "--output", "text", "--query", "Content.Location")
            os.makedirs(os.path.dirname(LAYER_ZIP), exist_ok=True)
            with urllib.request.urlopen(location, timeout=180) as r, \
                    open(LAYER_ZIP, "wb") as fh:
                fh.write(r.read())
            print("FETCHED: %s (%d bytes)" % (LAYER_ZIP, os.path.getsize(LAYER_ZIP)))
        except Exception as exc:  # noqa: BLE001 -- a fetch failure must WARN, never crash the run
            print("WARN: layer fetch failed (%s: %s) -- a layered function cannot be probed in "
                  "its real layout" % (type(exc).__name__, exc))
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
    # PADDED, BECAUSE AN EMPTY LAST FIELD DISAPPEARS. `--output text` renders the five values
    # tab-separated, and a function with no layers renders the fifth as EMPTY -- so the line ends
    # in a tab, `aws()` strips trailing whitespace, and `split` returns FOUR fields. Unpacking
    # five raised `ValueError: not enough values to unpack`. The count is padded rather than the
    # strip removed, because the strip is what keeps the other four clean.
    _fields = aws(
        "lambda", "get-function-configuration", "--function-name", function,
        "--region", "us-east-1", "--output", "text",
        # NULL-SAFE, AND IT TOOK A FAILURE TO LEARN WHY. `join(',', Layers[].Arn)` raises
        # "invalid type for value: None, expected array-string" on a function with NO layers --
        # which is three of these six -- so the expression that READS the attachment must tolerate
        # its absence. `Layers || `[]`` supplies the empty array before the join sees it. The first
        # version of this query worked on holdings (which HAS a layer) and failed on every
        # layer-less function, so running it over ONE function would have looked clean.
        "--query", "[Handler,CodeSha256,State,LastUpdateStatus,"
                   "join(',', (Layers || `[]`)[].Arn)]").split("\t")
    while len(_fields) < 5:
        _fields.append("")
    handler, live_sha, state, status, layer_arns = _fields[:5]
    layered = bool(layer_arns.strip())
    print("    live: handler=%s state=%s/%s layers=%s"
          % (handler, state, status, layer_arns.strip() or "NONE"))

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
        print("    layout: /var/task + %s"
              % ("/opt/python (the LIVE function attaches a layer)" if layered
                 else "no layer (the LIVE function attaches none)"))
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
