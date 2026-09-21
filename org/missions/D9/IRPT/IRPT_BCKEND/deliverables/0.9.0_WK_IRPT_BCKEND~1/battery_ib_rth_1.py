#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rth-1 battery -- R76-AC1: inflection's serving route resolves live, 3 of 3
firms, no S3 404 / UNEXPECTED.

FIRST PASS. B1, code-only, a NEVER-WIDEN act (packet
NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md, blob computed at arm (b) below): the fix is committed to
`_authz/loaders.py::load_ownership` (recognise the AccessDenied-masking wire shape as an absent
map, same as NoSuchKey -- see the packet and IB-rth-1_investigation.md). NOTHING IS BUILT OR
DEPLOYED BY THIS ORDER; this battery is written to be RE-RUN UNCHANGED once the two halves are
signed and a build+apply follows -- it gates itself on both and only reaches the live proof when
they hold.

  (a) SOURCE AT REST: the fix committed (blob at HEAD == worktree == the constant below);
      py_compile clean; the full `_authz/tests/` suite passes (no regression).
  (b) THE PACKET: committed, blob at HEAD == worktree == the signed blob.
  (c) THE HALVES at HEAD naming the packet blob, 2 of 2. STOP here if not -- (d) and (e) are
      NOT graded, matching every prior never-widen battery in this project (rtf-10's own arm d).
  (d) DEPLOYED-BYTES CHECK (only if (c) holds): for each of the 7 functions that stage
      `_authz/loaders.py` (measured, `infra/aws/lambda/ci/lambda-source-map.json`), download the
      LIVE zip's `loaders.py` member and hash it; every GRADED function must equal the committed fix's sha256.
      RULING 99069 re-scopes the graded set to 6 of 7: irpt-ycharts-generate is carried to row S102 (its build
      is refused on two sourceless members) -- still read and printed, never counted.
      This is the discriminator for "built and deployed" that does not require knowing a build
      version in advance -- it reads the bytes actually served.
  (e) THE LIVE PROOF (only if (d) holds): reuses the bounded-principal, FIRM_OPERATIONS-class
      mechanism `../0.9.0_WK_IRPT_BCKEND~3/IB-rtg-3_arm_e_live_proof.py` builds and this order's
      face names (rtf-10's mechanism, generalised to one principal per firm) -- invoked as a
      subprocess so the lifecycle (create -> login -> request -> rollback, each verified) is not
      duplicated. Expected: 3 of 3 firms resolve a TenantRoute (SERVED or a policy refusal
      carrying a firm_id), never UNEXPECTED, route/function/role printed per firm.

NEVER PRINTED OR WRITTEN: any secret value. Response bodies are bound by sha256 only.
"""
from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rth-1_R76-AC1_battery_output.txt")
TOKEN = "IBR76-INFLECTION-ROUTE-RESOLVES-LIVE-3-OF-3"
D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1"
SOURCE_REL = "infra/aws/lambda/investor-reporting/_authz/loaders.py"
SOURCE_BLOB_SHA256 = "0c086052e6e65d2cb411f15362862b1656bad0b2320f9756be6a32444b665765"
PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rth-1.md"
PACKET_BLOB = "19389dc50b6e3bfb7436681328cb2721c9c11802"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
LIVE_PROOF_SCRIPT = os.path.join(
    WS, "org", "missions", "D9", "IRPT", "IRPT_BCKEND", "deliverables",
    "0.9.0_WK_IRPT_BCKEND~3", "IB-rtg-3_arm_e_live_proof.py")
ACCT = "313476888478"
# RULING 99069 (2.0.0_SA_COO~B, 2026-09-21T15:19:10Z, on row IRPT_BCKEND-S111, option ii of its disarm menu): arm
# (d)'s denominator is RE-SCOPED to the buildable-and-applied functions. irpt-ycharts-generate is CARRIED to row
# IRPT_BCKEND-S102 -- its files[] declares firm_registry.json and settings.json with no source anywhere in git, so
# build-and-upload.sh refuses it before upload -- and stays at its current live bytes (both signed halves' no-change
# branch; it has no route, schedule or event source). Its live loaders.py is still READ AND PRINTED below: carried,
# never hidden, and never counted as deployed. Applied by 0.7.0_AE_CloudOps~V on the ruling; nothing else changed.
CARRIED_TO_S102 = {"irpt-ycharts-generate"}

LINES: list[str] = []
s3 = boto3.client("s3", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def arm_a() -> bool:
    emit("(a) SOURCE AT REST -- the fix committed, compiles, and the full _authz test suite passes")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + SOURCE_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", SOURCE_REL)
    wt = wt.strip()
    _, headtext = git("show", "HEAD:" + SOURCE_REL) if head else (1, "")
    head_content_sha = sha256_bytes(headtext.encode("utf-8")) if head else "ABSENT"
    committed = bool(head) and head == wt
    emit("  %s: blob at HEAD %s, worktree %s -> %s" % (SOURCE_REL, head or "ABSENT", wt,
                                                        "COMMITTED, UNCHANGED" if committed else "NOT COMMITTED / DIFFERS"))
    content_ok = head_content_sha == SOURCE_BLOB_SHA256
    emit("  content sha256 at HEAD: %s, expected %s -> %s" % (head_content_sha, SOURCE_BLOB_SHA256,
                                                                "EQUAL" if content_ok else "DIFFERS"))
    compile_rc = subprocess.run([sys.executable, "-m", "py_compile", SOURCE_REL], cwd=WS,
                                capture_output=True, text=True, timeout=60).returncode
    emit("  py_compile: rc=%d -> %s" % (compile_rc, "CLEAN" if compile_rc == 0 else "FAILED"))
    test_dir = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting", "_authz", "tests")
    pt = subprocess.run([sys.executable, "-m", "pytest", test_dir, "-q"], cwd=WS,
                        capture_output=True, text=True, timeout=300)
    m = re.search(r"(\d+) passed", pt.stdout)
    n_passed = int(m.group(1)) if m else 0
    tests_ok = pt.returncode == 0 and "failed" not in pt.stdout
    emit("  pytest %s: rc=%d, %d passed -> %s" % (test_dir, pt.returncode, n_passed,
                                                   "PASS, no regression" if tests_ok else "FAIL"))
    return committed and content_ok and compile_rc == 0 and tests_ok


def arm_b() -> tuple[bool, str]:
    emit("(b) THE PACKET -- committed, blob at HEAD == worktree == signed")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head) and head == wt.strip() == PACKET_BLOB
    emit("  packet %s: blob at HEAD %s, worktree %s, signed %s -> %s" % (
        PACKET_REL, head or "ABSENT", wt.strip(), PACKET_BLOB,
        "COMMITTED, UNCHANGED" if ok else "NOT THE SIGNED BLOB"))
    return ok, head


def arm_c(blob: str) -> bool:
    emit("(c) THE HALVES at HEAD naming the packet blob")
    n = 0
    for who, pattern in (
        ("COO", "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rth-1_*.md"),
        ("CTO", "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rth-1_*.md"),
    ):
        _, listing = git("ls-tree", "-r", "--name-only", "HEAD", "--", os.path.dirname(pattern))
        hits = [p for p in listing.splitlines() if re.fullmatch(pattern.replace(".", r"\.").replace("*", ".*"), p)]
        naming = [p for p in hits if blob and blob in git("show", "HEAD:" + p)[1]]
        n += bool(naming)
        emit("  %s half: %d file(s) matching at HEAD, %d naming blob %s -> %s" % (
            who, len(hits), len(naming), blob or "?", "PRESENT" if naming else "ABSENT"))
    emit("  halves: %d of 2" % n)
    return n == 2


def _staged_functions() -> list[str]:
    with open(os.path.join(WS, SOURCE_MAP_REL), encoding="utf-8") as fh:
        sm = json.load(fh)
    out = []
    for name, spec in sm.get("functions", {}).items():
        files = spec.get("files") or []
        if any("loaders.py" in str(f) for f in files):
            out.append(name)
    return sorted(out)


def arm_d() -> bool:
    emit("(d) DEPLOYED-BYTES CHECK -- each function that stages loaders.py, live zip vs the committed fix")
    fns = _staged_functions()
    emit("  functions staging loaders.py (lambda-source-map.json): %d: %s" % (len(fns), fns))
    graded = [f for f in fns if f not in CARRIED_TO_S102]
    carried = [f for f in fns if f in CARRIED_TO_S102]
    emit("  graded denominator per RULING 99069: %d of %d (carried to row S102, read but not graded: %s)" % (
        len(graded), len(fns), carried))
    ok_n = 0
    for fn in fns:
        cfg = lam.get_function(FunctionName=fn)
        code = cfg["Code"]
        loc = code.get("Location")
        # get_function returns a presigned URL for Location when Code is S3-backed; fetch it directly.
        if loc:
            import urllib.request
            with urllib.request.urlopen(loc, timeout=60) as r:
                zbytes = r.read()
        else:
            emit("  %-28s NO CODE LOCATION -> FAIL" % fn)
            continue
        with zipfile.ZipFile(io.BytesIO(zbytes)) as zf:
            names = zf.namelist()
            member = "loaders.py" if "loaders.py" in names else next((n for n in names if n.endswith("/loaders.py")), None)
            if member is None:
                emit("  %-28s loaders.py NOT a zip member (%d members) -> FAIL" % (fn, len(names)))
                continue
            live_bytes = zf.read(member)
        live_sha = sha256_bytes(live_bytes)
        good = live_sha == SOURCE_BLOB_SHA256
        if fn in CARRIED_TO_S102:
            emit("  %-28s live %s sha256 %s -> %s; CARRIED to row S102 per RULING 99069, NOT GRADED" % (
                fn, member, live_sha, "fix present" if good else "pre-fix bytes, as carried"))
            continue
        ok_n += good
        emit("  %-28s live %s sha256 %s, expected %s -> %s" % (
            fn, member, live_sha, SOURCE_BLOB_SHA256, "DEPLOYED" if good else "NOT YET DEPLOYED"))
    emit("  deployed-bytes match: %d of %d graded (%d carried to S102)" % (ok_n, len(graded), len(carried)))
    return len(graded) > 0 and ok_n == len(graded)


def arm_e() -> bool:
    emit("(e) THE LIVE PROOF -- reusing the bounded-principal mechanism, subprocess")
    if not os.path.isfile(LIVE_PROOF_SCRIPT):
        emit("  live-proof script ABSENT at %s -> FAIL" % LIVE_PROOF_SCRIPT)
        return False
    # RULING 99070 ASK1 (2.0.0_SA_COO~B, 2026-09-21T15:39:47Z, row IRPT_BCKEND-S112): 1200 -> 3300. The live proof
    # sleeps ~910 s per firm for the deleted principal's token to expire, 3 firms in sequence (~46 min); the face's
    # invocation bound moves 1800 -> 3600 in the same ruling.
    p = subprocess.run([sys.executable, LIVE_PROOF_SCRIPT], cwd=WS, capture_output=True, text=True, timeout=3300)
    for ln in p.stdout.splitlines():
        emit("  | " + ln)
    if p.stderr:
        emit("  STDERR (last 2000 chars): " + p.stderr[-2000:])
    emit("  live-proof script rc=%d" % p.returncode)
    # The live-proof script's own R74-AC1 token names route resolution in-process; for THIS
    # criterion the discriminator is the printed per-firm class over the subprocess's own output:
    # 3 of 3 firms SERVED or POLICY (never UNEXPECTED).
    classes = re.findall(r"class (\w+)", p.stdout)
    firms_ok = sum(1 for c in classes if c in ("SERVED", "POLICY"))
    unexpected = sum(1 for c in classes if c == "UNEXPECTED")
    emit("  classes observed: %s -> %d resolved (SERVED/POLICY), %d UNEXPECTED" % (classes, firms_ok, unexpected))
    return p.returncode == 0 and unexpected == 0 and firms_ok >= 3


def main() -> int:
    emit("IB-rth-1 R76-AC1 battery (first pass) -- run at %s -- worktree HEAD %s" % (
        now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("")
    a_ok = arm_a()
    emit("")
    b_ok, blob = arm_b()
    emit("")
    c_ok = arm_c(blob)
    emit("")
    arms = {"(a) source": a_ok, "(b) packet": b_ok, "(c) halves": c_ok}
    if not c_ok:
        emit("STOP at (c): a half is ABSENT -- (d) and (e) are NOT graded. This is the expected "
             "state for this cell's first pass: B1 is a never-widen act and this order does not "
             "sign its own halves.")
        arms["(d) deployed-bytes"] = False
        arms["(e) live proof"] = False
    else:
        d_ok = arm_d()
        emit("")
        if not d_ok:
            emit("STOP at (d): the fix is not yet built/deployed to every graded function -- (e) is NOT graded.")
            arms["(d) deployed-bytes"] = d_ok
            arms["(e) live proof"] = False
        else:
            arms["(d) deployed-bytes"] = d_ok
            arms["(e) live proof"] = arm_e()
    emit("")
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
    if all(arms.values()):
        emit("RESULT: R76-AC1 PASS -- %d of %d arms hold" % (len(arms), len(arms)))
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R76-AC1 FAIL (or not yet reachable) -- %d of %d arms hold"
             % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
