"""ar11_checks.py -- the mechanical checks of IRPT_ANLREQ round 11, workstream Y.

Usage:  python ar11_checks.py <check> --root <workspace root> [--portal <portal root>]

  y111-dev      AR-y-111: the return census's DEV column re-read at a named DEV head, one row per served
                member, and the ticket page's reader named on each trunk                                -> Y111-DEV-OK
  y112-remove   AR-y-112: the Ticket Center's fallback is gone, a one-read test is named, and the folder
                passes (needs --portal)                                                                  -> Y112-REMOVE-OK
  y113-poller   AR-y-113 (RETIRED criterion): irpt-intake-poller builds with NO parity skip and prints its
                recorded digest                                                                          -> Y113-POLLER-OK
  y113-result   AR-y-113 closed as a RESULT: the record states the finding, and neither the map entry
                nor the source folder was changed to pretend the entry builds                            -> Y113-RESULT-OK

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
BASE = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/"
CENSUS = BASE + "r10/RETURN_CENSUS_IRPT_STATUS.json"
REREAD = BASE + "r11/RETURN_CENSUS_DEV_REREAD.json"
POLLER = "irpt-intake-poller"
HELPER = "src/pages/TicketCenter/analysisRequest.ts"
FALLBACK_TEST = "src/pages/TicketCenter/__tests__/package-open-ticket-fallback.test.tsx"
BINDING_TEST = "src/pages/TicketCenter/__tests__/package-open-ticket-binding.test.tsx"
ONE_READ = "a read refused as invalid input is shown after one read"
TOKENS = {"y111-dev": "Y111-DEV", "y112-remove": "Y112-REMOVE", "y113-poller": "Y113-POLLER", "y113-result": "Y113-RESULT"}
RESULT = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r11/INTAKE_POLLER_MAP_ENTRY.json"


def finish(check, problems):
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y111-dev":
        if not (root / REREAD).is_file():
            return finish(check, ["no %s" % REREAD])
        census = json.loads((root / CENSUS).read_text(encoding="utf-8"))
        served = sorted(str(row.get("packaged_as")) for row in census.get("moved_members") or []
                        if row.get("served_effect") == "CHANGES_SERVED_ANSWER")
        doc = json.loads((root / REREAD).read_text(encoding="utf-8"))
        for key in ("dev_ref", "prod_ref"):
            if not re.fullmatch(r"[0-9a-f]{40}", str(doc.get(key, ""))):
                problems.append("%s is not a full commit hash" % key)
        if doc.get("dev_ref") == "9ca634c6ea089796c127a9a1399cfa279323a154":
            problems.append("dev_ref is the head the first census read, not a re-read")
        rows = doc.get("served_members") or []
        if sorted(str(row.get("packaged_as")) for row in rows) != served:
            problems.append("served_members does not hold exactly the %d served members of the census" % len(served))
        for row in rows:
            reader = row.get("portal_reader_dev") or {}
            if reader.get("found") is False:
                if not reader.get("searched"):
                    problems.append("%r: a not-found DEV reader names no search" % row.get("packaged_as"))
            elif not (reader.get("file_function") and isinstance(reader.get("admits_new_shape"), bool) and reader.get("deciding_line")):
                problems.append("%r: the DEV reader is incomplete" % row.get("packaged_as"))
            if row.get("changed_since_first_read") not in (True, False):
                problems.append("%r: changed_since_first_read is not stated" % row.get("packaged_as"))
        ticket = doc.get("ticket_page_reader") or {}
        if not ticket.get("file_function") or not isinstance(ticket.get("on_dev"), bool) or not isinstance(ticket.get("on_prod"), bool) \
                or len(ticket.get("after_reads") or []) < 2:
            problems.append("ticket_page_reader is incomplete (file_function, on_dev, on_prod, two after_reads)")
        print("served members %d, rows %d" % (len(served), len(rows)))
        return finish(check, problems)
    if check == "y112-remove":
        if "--portal" not in argv:
            print(__doc__)
            return 2
        portal = Path(argv[argv.index("--portal") + 1])
        helper = (portal / HELPER).read_text(encoding="utf-8")
        for name in ("readTicketReport", "isInvalidInputRefusal"):
            if name in helper:
                problems.append("%s is still in analysisRequest.ts" % name)
        if (portal / FALLBACK_TEST).is_file():
            problems.append("the fallback test file is still present")
        binding = (portal / BINDING_TEST).read_text(encoding="utf-8") if (portal / BINDING_TEST).is_file() else ""
        if ONE_READ not in binding:
            problems.append("the test named %r is absent from the binding test file" % ONE_READ)
        got = subprocess.run(["bun", "test", "./src/pages/TicketCenter"], cwd=str(portal), capture_output=True, text=True,
                             encoding="utf-8", errors="replace")
        out = re.sub(r"\x1b\[[0-9;]*m", "", (got.stdout or "") + (got.stderr or ""))
        passed, failed = re.search(r"(\d+) pass", out), re.search(r"(\d+) fail", out)
        print("TicketCenter folder: %s pass, %s fail (rc=%d)" % (passed.group(1) if passed else "?", failed.group(1) if failed else "?",
                                                                  got.returncode))
        if got.returncode != 0 or not failed or int(failed.group(1)) != 0 or not passed or int(passed.group(1)) < 49:
            problems.append("the TicketCenter folder does not pass whole")
        return finish(check, problems)
    if check == "y113-result":
        doc = json.loads((root / RESULT).read_text(encoding="utf-8"))
        entry = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"][POLLER]
        live = doc.get("live") or {}
        if live.get("equals_recorded") is not True or live.get("code_sha256") != entry.get("deployed_code_sha256"):
            problems.append("the record does not state a live digest equal to the entry's recorded digest")
        if doc.get("served_member_commit") is not None:
            problems.append("the record names a commit for the served member; the result is that there is none")
        after = str((doc.get("members_equal_live") or {}).get("after", ""))
        found = re.match(r"(\d+) of (\d+)", after)
        if not found or int(found.group(1)) >= int(found.group(2)):
            problems.append("members_equal_live.after does not state fewer members equal to live than the package holds")
        if (doc.get("build") or {}).get("equals_target") is not False:
            problems.append("the record must state that the build does not equal the target")
        if any(str(row.get("packaged_as")) == "firm_registry.json" for row in entry.get("staged_from") or []):
            problems.append("the map entry pins firm_registry.json; the ruling is that the map is not edited")
        if (root / "infra/aws/lambda/investor-reporting/intake/firm_registry.json").exists():
            problems.append("firm_registry.json is present in the source folder")
        got = subprocess.run(["git", "status", "--porcelain", "--", MAP], cwd=str(root), capture_output=True, text=True)
        if got.returncode != 0 or got.stdout.strip():
            problems.append("the source map is modified in this tree")
        print("members equal to live: %s" % after[:60])
        return finish(check, problems)
    entry = json.loads((root / MAP).read_text(encoding="utf-8"))["functions"][POLLER]
    recorded = entry.get("deployed_code_sha256") or entry.get("artifact_sha256")
    env = dict(os.environ, BUILD_ONLY="1", TMPDIR=tempfile.mkdtemp(prefix="ar11-build-"))
    env.pop("BAU_PARITY_SKIP", None)
    got = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", POLLER], cwd=str(root),
                         capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = (got.stdout or "") + (got.stderr or "")
    line = [text for text in out.splitlines() if text.startswith("BUILD_ONLY:")]
    print(line[-1][:200] if line else "\n".join([text for text in out.splitlines() if text.strip()][-3:]))
    print("recorded digest: %s" % recorded)
    if not line or ("sha256=%s" % recorded) not in line[-1]:
        problems.append("a BUILD_ONLY with NO parity skip does not print the entry's recorded digest (rc=%d)" % got.returncode)
    return finish(check, problems)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
