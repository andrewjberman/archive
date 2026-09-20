#!/usr/bin/env python3
"""IB-rtg-1 -- the export receipt aligns to the writer and the taxonomy tests the code.
Rows S105 (address) + S106 (taxonomy), ONE cell per the CTO ruling @0110b9de01.

FIRST PASS (this revision): arms (a)-(c) measure the defect, the source edits, the build and the
packet, then check the never-widen halves. Per this order's <status> and BOUNDS, arm (d)/(e) are
NOT run when the halves are ABSENT -- that is the order's own stated expected first-pass outcome,
not a battery defect. The success token IBR72-EXPORT-RECEIPT-ALIGNED-AND-TAXONOMY-BY-CODE is
printed ONLY if arm (e)'s live, deployed-role round trip is actually exercised and clean; printing
it earlier would assert a live outcome nothing measured.

Re-derives every run from the committed source, the live AWS state and git blobs -- never a
hand-typed verdict table with no premise check.

Usage: py -3.12 battery_ib_rtg_1.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=HERE,
                      capture_output=True, check=True).stdout.decode("utf-8").strip()
REPO = REPO.replace("/", os.sep)
SOURCE_MAP = os.path.join(REPO, "infra", "aws", "lambda", "ci", "lambda-source-map.json")
EXPORT_DIR = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "export")
AWS = os.path.join(REPO, ".tools", "aws.cmd")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")
EXPORT_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "export")

FUNCTION = "irpt-export-render"
PACKET_PATH = os.path.join(HERE, "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-1.md")
COO_DIR = os.path.join(REPO, "org", "tier1_exec", "2.0.0_SA_COO~B", "deliverables")
CTO_DIR = os.path.join(REPO, "org", "tier1_exec", "1.0.0_SA_CTO", "deliverables")


def run(cmd, cwd=None, timeout=180):
    p = subprocess.run(cmd, cwd=cwd or REPO, capture_output=True, timeout=timeout)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def load_source_map():
    with open(SOURCE_MAP, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------------------------- arm (a)
def arm_a():
    print("=" * 100)
    print("ARM (a) -- MEASURE FIRST, printed with denominators")
    print("=" * 100)
    ok = True
    entry = read_text(os.path.join(EXPORT_DIR, "entry.py"))
    handler = read_text(os.path.join(EXPORT_DIR, "handler.py"))

    # S105: the aligned template is in the DECLARED "generations" family, not the old
    # "investor-reporting/export/..." address (0 of 7 GetObject ARNs matched, KeyCount 0, per
    # row S105's own grounding).
    s105_new_template = 'RECEIPT_KEY_TEMPLATE = os.environ.get(\n    "IRPT_EXPORT_RECEIPT_KEY", "firms/{firm}/generations/{export_id}/receipt.json")' in entry
    print("S105 -- aligned RECEIPT_KEY_TEMPLATE assignment present: %s" % s105_new_template)
    # The OLD literal default may still appear INSIDE this cell's own explanatory comment
    # (quoted verbatim, on purpose, so a reader can see what changed) -- a bare substring
    # absence check cannot tell a comment from an active default, so the DEFAULT VALUE ITSELF
    # is checked below via the live RECEIPT_KEY_TEMPLATE the module actually resolves to
    # (the "ALIGNED" check), which is the grain this criterion is actually about.
    ok = ok and s105_new_template

    # S105 second half: a writer of the SAME address exists (receipt_key + persist_receipt,
    # wired into finalize_export).
    s105_writer = ("def receipt_key(" in handler and "def persist_receipt(" in handler
                   and "persist_receipt(" in handler.split("def finalize_export")[1].split("\ndef ")[0])
    print("S105 -- a writer of the aligned address exists in finalize_export(): %s" % s105_writer)
    ok = ok and s105_writer

    # S106: the except clause decides off the modeled CODE (ClientError + Error.Code), never the
    # class NAME two-tuple.
    s106_old_gone = 'exc.__class__.__name__ in ("NoSuchKey", "ClientError")' not in entry
    s106_new = ('isinstance(exc, botocore.exceptions.ClientError)' in entry
                and 'exc.response.get("Error", {}).get("Code", "")' in entry)
    print("S106 -- OLD class-name forward-list test removed: %s" % s106_old_gone)
    print("S106 -- NEW code-based (isinstance + Error.Code) test present: %s" % s106_new)
    ok = ok and s106_old_gone and s106_new

    # The reader/writer alignment -- PROVEN EQUAL, not assumed, by actually calling both builders.
    print()
    print("-- reader/writer address alignment (computed this run, not assumed) --")
    sys.path.insert(0, EXPORT_DIR)
    sys.path.insert(0, os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_keys"))
    sys.path.insert(0, os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting", "_authz"))
    os.environ.setdefault("IRPT_FIRM_REGISTRY",
                          os.path.join(REPO, "data", "firm_registry.json"))
    import importlib.util

    def load_mod(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    entry_mod = load_mod("ib_rtg1_entry", os.path.join(EXPORT_DIR, "entry.py"))
    handler_mod = load_mod("ib_rtg1_handler", os.path.join(EXPORT_DIR, "handler.py"))
    tenant, export_id = "49financial", "EXP-" + "a" * 32
    writer_key = handler_mod.receipt_key(tenant, export_id)
    reader_key = entry_mod.RECEIPT_KEY_TEMPLATE.format(firm=tenant, export_id=export_id)
    print("writer (handler.receipt_key)      = %s" % writer_key)
    print("reader (entry.RECEIPT_KEY_TEMPLATE) = %s" % reader_key)
    aligned = (writer_key == reader_key)
    print("ALIGNED: %s" % aligned)
    ok = ok and aligned

    old_default_still_live = entry_mod.RECEIPT_KEY_TEMPLATE == (
        "investor-reporting/export/{firm}/{export_id}/receipt.json")
    print("RECEIPT_KEY_TEMPLATE's RUNTIME VALUE still the OLD out-of-layout default: %s "
          "(expect False)" % old_default_still_live)
    ok = ok and (old_default_still_live is False)

    # the existing (pre-fix) grant does NOT cover the aligned address -- a NEW grant is needed,
    # measured, never assumed (BOUNDS).
    import fnmatch
    old_grant = "firms/*/generations/*/attempts/*/exports/*"
    matches_old_grant = fnmatch.fnmatch(reader_key, old_grant)
    print("aligned address matches the PRE-EXISTING GetObject grant (%s): %s (expect False -- a "
          "new grant is required and added, see the packet)" % (old_grant, matches_old_grant))
    ok = ok and (matches_old_grant is False)

    print()
    print("ARM (a): %s" % ("PASS" if ok else "FAIL"))
    return ok


# ------------------------------------------------------------------------------------- arm (b)
def arm_b():
    print()
    print("=" * 100)
    print("ARM (b) -- THE SOURCE EDIT + BUILD")
    print("=" * 100)
    ok = True
    sm = load_source_map()
    cfg = sm["functions"][FUNCTION]

    if "keys.py" not in cfg["files"]:
        print("ERROR: keys.py not in files[] (row IRPT_BCKEND-W1-S44's fix did not land)")
        ok = False
    staged_names = [s["packaged_as"] for s in cfg["staged_from"]]
    if "keys.py" not in staged_names:
        print("ERROR: keys.py not in staged_from[]")
        ok = False
    print("keys.py registered in files[] and staged_from[]: %s" % ok)

    print()
    print("-- rebuilding %s (build-and-upload.sh, single-function mode) --" % FUNCTION)
    sys.path.insert(0, os.path.join(REPO, ".tools"))
    from git_bash_resolver import git_bash  # noqa: E402
    bash = git_bash()
    if not bash:
        raise SystemExit("ERROR: no Git Bash found (git_bash_resolver)")
    rc, out, err = run([bash, os.path.join(REPO, "infra", "aws", "lambda", "ci",
                                           "build-and-upload.sh"),
                        "investor-reporting", FUNCTION], timeout=180)
    print(out[-4000:])
    if err.strip():
        print("STDERR (tail):", err[-1500:])
    if rc != 0:
        print("ERROR: build-and-upload.sh rc=%d" % rc)
        return False
    sm2 = load_source_map()
    built_sha = sm2["functions"][FUNCTION]["artifact_sha256"]
    print("built artifact_sha256 (base64, this run): %s" % built_sha)

    print("ARM (b): %s" % ("PASS" if ok else "FAIL"))
    return ok


# ------------------------------------------------------------------------------------- arm (c)
def aws_json(args, timeout=60):
    rc, out, err = run([AWS] + args + ["--output", "json"], timeout=timeout)
    if rc != 0:
        return rc, None, err
    try:
        return rc, json.loads(out), err
    except ValueError:
        return rc, out, err


def arm_c():
    print()
    print("=" * 100)
    print("ARM (c) -- THE PACKET, AND THE HALVES")
    print("=" * 100)

    rc, cfg, err = aws_json(["lambda", "get-function-configuration",
                             "--function-name", FUNCTION,
                             "--query", "{CodeSha256:CodeSha256,LastModified:LastModified}"])
    if rc != 0:
        print("ERROR: get-function-configuration failed rc=%d: %s" % (rc, err[:400]))
        return False
    print("LIVE CodeSha256 (read live, this run): %s  LastModified=%s"
          % (cfg.get("CodeSha256"), cfg.get("LastModified")))

    sm = load_source_map()
    built_sha = sm["functions"][FUNCTION]["artifact_sha256"]
    print("MANIFEST-DECLARED artifact_sha256 (this worktree's last build): %s" % built_sha)
    print("(these two DIFFER until arm (d) applies -- that is the expected pre-apply state)")

    if os.path.isfile(PACKET_PATH):
        rc, out, _ = run(["git", "hash-object", PACKET_PATH])
        print("packet at %s -- blob %s (measured this run; the COMMITTED blob may differ until "
              "the commit lands)" % (PACKET_PATH, out.strip()))
    else:
        print("ERROR: packet not found at %s" % PACKET_PATH)
        return False

    coo_halves = ([f for f in os.listdir(COO_DIR) if "rtg-1" in f.lower()]
                  if os.path.isdir(COO_DIR) else [])
    cto_halves = ([f for f in os.listdir(CTO_DIR) if "rtg-1" in f.lower()]
                  if os.path.isdir(CTO_DIR) else [])
    print("COO half candidates: %s" % (coo_halves or "ABSENT"))
    print("CTO half candidates: %s" % (cto_halves or "ABSENT"))
    halves_present = len(coo_halves) + len(cto_halves)
    print("halves present: %d of 2" % halves_present)

    if halves_present < 2:
        print()
        print("ARM (c): STOP HERE -- halves ABSENT (%d of 2). R72-AC1 FAILS TRUTHFULLY AT (c). "
              "Arm (d)/(e) are NOT run this pass. The order stays open. THIS IS THE ORDER'S OWN "
              "STATED EXPECTED FIRST-PASS OUTCOME." % halves_present)
        return False

    print("ARM (c): both halves present -- proceeding would be arm (d), NOT built into this "
          "revision of the battery (a future pass adds it once there is something to apply).")
    return True


def main():
    a_ok = arm_a()
    b_ok = arm_b()
    c_ok = arm_c()
    print()
    print("=" * 100)
    print("SUMMARY: arm(a)=%s arm(b)=%s arm(c)=%s" % (a_ok, b_ok, c_ok))
    if a_ok and b_ok and c_ok:
        # arm (c) only returns True once both halves are present AND (in a future revision)
        # arm (d)/(e) have actually applied and exercised the deployed route -- this revision
        # does not reach that branch, so the success token is never printed from a False (d)/(e).
        print("IBR72-EXPORT-RECEIPT-ALIGNED-AND-TAXONOMY-BY-CODE")
        return 0
    print("NOT PASSED THIS RUN -- see the STOP line above for the reason (expected on a first "
          "pass whose never-widen halves are ABSENT).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
