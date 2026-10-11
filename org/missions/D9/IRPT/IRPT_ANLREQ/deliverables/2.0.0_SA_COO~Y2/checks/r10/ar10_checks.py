"""ar10_checks.py -- the mechanical checks of IRPT_ANLREQ round 10, workstream Y.

Usage:  python ar10_checks.py <check> --root <workspace root> [--portal <portal root>]

  y101-fallback  AR-y-101: the portal test file holds the four named tests and passes (needs --portal)   -> Y101-FALLBACK-OK
  y101-keep      AR-y-101: the whole TicketCenter test folder passes (needs --portal)                    -> Y101-KEEP-OK
  y102-build     AR-y-102: the composition-read function builds with NO parity skip, prints the LIVE
                 digest, and none of its packaged members is unpinned                                    -> Y102-BUILD-OK
  y103-census    AR-y-103: the PROPOSED irpt-status entry (a deliverable; the map itself untouched) has every
                 member at ONE pin, and the return's census is complete (two equal digests with no parity
                 skip, every member that differs from live filled, with its portal reader where it serves) -> Y103-CENSUS-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing
(the build check builds into a temp folder outside the tree with BUILD_ONLY=1; it never uploads).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAP = "infra/aws/lambda/ci/lambda-source-map.json"
CCR = "irpt-commentary-composition-read-lambda"
CCR_LIVE = "DbvBUxTGlCsdG4htVOhbI4NBxBMNbmjD6BLpMGu2Yo4="
PORTAL_TEST = "src/pages/TicketCenter/__tests__/package-open-ticket-fallback.test.tsx"
PORTAL_NAMES = (
    "the first read sends the ticket's id",
    "an unexpected-query refusal repeats the read once without the ticket's id",
    "any other refusal is shown and the read is not repeated",
    "a binding refusal is still shown as a binding refusal",
)
CENSUS = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r10/RETURN_CENSUS_IRPT_STATUS.json"
ENTRY = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/r10/IRPT_STATUS_ENTRY_ONE_PIN.json"
STATUS_LIVE = "6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc="
TOKENS = {"y101-fallback": "Y101-FALLBACK", "y101-keep": "Y101-KEEP", "y102-build": "Y102-BUILD", "y103-census": "Y103-CENSUS"}


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def bun(portal, target):
    got = subprocess.run(["bun", "test", target], cwd=str(portal), capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
    passed, failed = re.search(r"(\d+) pass", out), re.search(r"(\d+) fail", out)
    return got.returncode, int(passed.group(1)) if passed else -1, int(failed.group(1)) if failed else -1


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check in ("y101-fallback", "y101-keep"):
        if "--portal" not in argv:
            print(__doc__)
            return 2
        portal = Path(argv[argv.index("--portal") + 1])
        if check == "y101-fallback":
            path = portal / PORTAL_TEST
            if not path.is_file():
                return finish(check, ["no %s" % PORTAL_TEST])
            text = path.read_text(encoding="utf-8")
            for name in PORTAL_NAMES:
                if name not in text:
                    problems.append("the test named %r is absent" % name)
            helper = (portal / "src/pages/TicketCenter/analysisRequest.ts").read_text(encoding="utf-8")
            for label, body in (("the test file", text), ("analysisRequest.ts", helper)):
                if "'INVALID_INPUT'" not in body:
                    problems.append("%s does not name the served reason 'INVALID_INPUT'" % label)
                if "'UNEXPECTED_OWNED_READ_QUERY'" in body:
                    problems.append("%s still compares the exception message UNEXPECTED_OWNED_READ_QUERY, which is never served" % label)
            rc, passed, failed = bun(portal, "./" + PORTAL_TEST)
            print("new file: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed != 0 or passed < len(PORTAL_NAMES):
                problems.append("the new test file does not pass with at least %d tests" % len(PORTAL_NAMES))
        else:
            rc, passed, failed = bun(portal, "./src/pages/TicketCenter")
            print("TicketCenter folder: %d pass, %d fail (rc=%d)" % (passed, failed, rc))
            if rc != 0 or failed != 0 or passed < 49:
                problems.append("the TicketCenter folder does not pass whole (49 passed at the base)")
        return finish(check, problems)
    if check == "y102-build":
        entry = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"][CCR]
        pinned = {str(row.get("packaged_as")) for row in entry.get("staged_from") or []}
        unpinned = [name for name in entry.get("files") or [] if name not in pinned]
        print("members %d, unpinned %d %s" % (len(entry.get("files") or []), len(unpinned), unpinned))
        if unpinned:
            problems.append("%d packaged member(s) are not pinned" % len(unpinned))
        if entry.get("artifact_sha256") != CCR_LIVE:
            problems.append("the entry's artifact_sha256 is not the live digest")
        env = dict(os.environ, BUILD_ONLY="1", TMPDIR=tempfile.mkdtemp(prefix="ar10-build-"))
        env.pop("BAU_PARITY_SKIP", None)
        got = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", CCR], cwd=str(root),
                             capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
        out = (got.stdout or "") + (got.stderr or "")
        line = [text for text in out.splitlines() if text.startswith("BUILD_ONLY:")]
        print(line[-1] if line else "\n".join([text for text in out.splitlines() if text.strip()][-3:]))
        if not line or ("sha256=%s" % CCR_LIVE) not in line[-1]:
            problems.append("a BUILD_ONLY with NO parity skip does not print the live digest (rc=%d)" % got.returncode)
        return finish(check, problems)
    got = subprocess.run(["git", "status", "--porcelain", "--", MAP], cwd=str(root), capture_output=True, text=True)
    if got.returncode != 0 or got.stdout.strip():
        problems.append("the source map is modified in this tree (the proposed entry is a deliverable, never a map edit)")
    live_entry = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"]["irpt-status"]
    if live_entry.get("artifact_sha256") != STATUS_LIVE:
        problems.append("the map's irpt-status entry no longer records the live digest")
    for name in (ENTRY, CENSUS):
        if not (root / name).is_file():
            return finish(check, problems + ["no %s" % name])
    entry = json.loads((root / ENTRY).read_text(encoding="utf-8"))
    rows = entry.get("staged_from") or []
    pins = sorted(set(str(row.get("pin")) for row in rows))
    pinned = {str(row.get("packaged_as")) for row in rows}
    unpinned = [name for name in entry.get("files") or [] if name not in pinned]
    print("proposed entry: members %d, distinct pins %d, unpinned %d" % (len(entry.get("files") or []), len(pins), len(unpinned)))
    if len(pins) != 1 or unpinned:
        problems.append("the proposed entry is not every member at one pin")
    doc = json.loads((root / CENSUS).read_text(encoding="utf-8"))
    build = doc.get("build") or {}
    if not build.get("sha256_first") or build.get("sha256_first") != build.get("sha256_second"):
        problems.append("the census does not record two equal build digests")
    if build.get("parity_skip") is not False:
        problems.append("the census must record parity_skip: false")
    if doc.get("pin") != (pins[0] if len(pins) == 1 else None):
        problems.append("the census's pin is not the proposed entry's one pin")
    if (doc.get("live") or {}).get("code_sha256") != STATUS_LIVE:
        problems.append("the census's live digest is not the live irpt-status digest this order names")
    changed = build.get("changed_members_vs_live")
    moved = doc.get("moved_members") or []
    if not isinstance(changed, list) or sorted(changed) != sorted(str(row.get("packaged_as")) for row in moved):
        problems.append("moved_members does not cover exactly the members that differ from live")
    for row in moved:
        if row.get("served_effect") not in ("CHANGES_SERVED_ANSWER", "INERT") or row.get("claim") not in ("measured", "inferred")                 or not row.get("why") or not row.get("owning_commits"):
            problems.append("moved member incomplete: %r" % row.get("packaged_as"))
        if row.get("served_effect") == "CHANGES_SERVED_ANSWER" and not (row.get("after_read") and row.get("portal_reader")):
            problems.append("%r changes a served answer and names no after_read or no portal_reader" % row.get("packaged_as"))
    print("changed vs live: %s" % (len(changed) if isinstance(changed, list) else "?"))
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
