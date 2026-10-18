#!/usr/bin/env python3
"""HVST-cm-2 row check -- read-only. Run: python -u <this file> (from anywhere; the repo root is derived from this file).

Writes its lines to stdout AND to cm2_row_check.out beside this file (opened with newline="\\n").
Reads: the function-map row (lib.opal_lambda_map.load_entry), the source file at HEAD (git show),
the live CodeSha256 (lambda get-function-configuration through the .tools/aws shim, via the Git Bash
resolver), and the two read-only comp-lambdamap tools (check, sha). Writes nothing to AWS or the repo.
"""
import copy
import hashlib
import os
import re
import subprocess
import sys

FN = "opal-research-pull-enqueue"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cm2_row_check.out")


def _git_root():
    r = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.stderr.write("ERROR: cannot derive repo root from %s\n" % HERE)
        sys.exit(2)
    return r.stdout.strip()


ROOT = _git_root()
sys.path.insert(0, ROOT)

from lib.opal_lambda_map import load_entry  # noqa: E402

# git_bash_resolver is loaded BY PATH: putting .tools on sys.path would let its regular package .tools/lib
# shadow the repo's lib/ (a namespace package), so the lib import above would fail.
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location("git_bash_resolver", os.path.join(ROOT, ".tools", "git_bash_resolver.py"))
_resolver = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_resolver)
git_bash = _resolver.git_bash

_OUT = open(OUT_PATH, "w", encoding="ascii", newline="\n")


def emit(line):
    print(line)
    _OUT.write(line + "\n")
    _OUT.flush()


def fail(msg, rc=2):
    emit("ERROR: " + msg)
    _OUT.close()
    sys.exit(rc)


def compare(a, b):
    """The comparator under test: equal iff the two CodeSha256 strings are identical."""
    return "yes" if a == b else "no"


def run_bash(cmd_args, label):
    bash = git_bash()
    if not bash:
        fail("%s: no Git Bash resolved (refusing to fall back to bare bash)" % label)
    r = subprocess.run([bash] + cmd_args, cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, text=True)
    return r.returncode, r.stdout


def live_code_sha256():
    rc, out = run_bash([".tools/aws", "lambda", "get-function-configuration",
                        "--function-name", FN, "--query", "CodeSha256", "--output", "text"],
                       "live read")
    val = out.strip()
    if rc != 0 or not val or "\n" in val:
        fail("live read rc=%d output=%r" % (rc, out[:300]))
    return val


def matching_lines(text):
    pat = re.compile(r"(?<![A-Za-z0-9_-])" + re.escape(FN) + r"(?![A-Za-z0-9_-])")
    return [ln.rstrip() for ln in text.splitlines() if pat.search(ln)]


def main():
    emit("CM2-CHECK repo=%s function=%s" % (ROOT, FN))

    # (1) the row, through the one reader
    row = load_entry(FN)
    src_dir = row["source_dir"]
    src_rel = src_dir + "/" + row["files"][0]
    emit("ROW-LOADED file=infra/aws/lambda/ci/function-map/%s.json source_dir=%s pipeline=%s "
         "last_deployed_commit=%s" % (FN, src_dir, row.get("pipeline"), row.get("last_deployed_commit")))

    # (2) the source file at HEAD: md5 and sha256 of the bytes git holds at HEAD
    r = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    head = r.stdout.strip()
    r = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + src_rel],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0 or not r.stdout:
        fail("git show HEAD:%s rc=%d %r" % (src_rel, r.returncode, r.stderr[:200]))
    src_bytes = r.stdout
    src_md5 = hashlib.md5(src_bytes).hexdigest()
    src_sha256 = hashlib.sha256(src_bytes).hexdigest()
    emit("SOURCE-HEAD path=%s commit=%s bytes=%d md5=%s sha256_hex=%s"
         % (src_rel, head, len(src_bytes), src_md5, src_sha256))

    # (3) the live CodeSha256, read-only
    live = live_code_sha256()
    emit("LIVE-READ function=%s CodeSha256=%s" % (FN, live))

    # (4) the grade line: the row's value against the live value
    row_val = row["deployed_code_sha256"]
    emit("ROW-MAPS function=%s deployed_code_sha256=%s source_md5=%s live_code_sha256=%s equal=%s"
         % (FN, row_val, src_md5, live, compare(row_val, live)))

    # (5) the negative control: the same comparison on an in-memory copy with one character changed
    planted_row = copy.deepcopy(row)
    s = planted_row["deployed_code_sha256"]
    planted_row["deployed_code_sha256"] = ("B" if s[0] != "B" else "A") + s[1:]
    planted_val = planted_row["deployed_code_sha256"]
    emit("CONTROL-PLANTED planted_value=%s differs_from_row=%s"
         % (planted_val, "yes" if planted_val != row_val else "no"))
    emit("CONTROL-NEGATIVE planted_wrong_sha equal=%s" % compare(planted_val, live))

    # (6) the repository's own drift tools, read-only (check and sha; census and reconcile write, not run)
    lm_check_rc, lm_check_out = run_bash(["-c", "comp-lambdamap check"], "comp-lambdamap check")
    lm_sha_rc, lm_sha_out = run_bash(["-c", "comp-lambdamap sha"], "comp-lambdamap sha")
    for label, rc, text in (("CHECK", lm_check_rc, lm_check_out), ("SHA", lm_sha_rc, lm_sha_out)):
        if rc not in (0, 1):
            emit("LAMBDAMAP-%s tool-error rc=%d (tool could not complete; see its own output)" % (label, rc))
            continue
        hits = matching_lines(text)
        if hits:
            for h in hits:
                emit("LAMBDAMAP-%s %s" % (label, h.strip()))
        else:
            emit("LAMBDAMAP-%s none (rc=%d; the tool names no line for %s)" % (label, rc, FN))
    drift_parts = []
    for text in (lm_check_out, lm_sha_out):
        drift_parts.extend(matching_lines(text))
    drift = "none" if not drift_parts else "; ".join(p.strip() for p in drift_parts)
    emit("LAMBDAMAP-DRIFT function=%s drift=%s" % (FN, drift))

    _OUT.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
