"""ar9_checks.py -- the mechanical checks of IRPT_ANLREQ round 9, workstream Y (cell AR-y-91: the READY gate's grant and census).

Usage:  python ar9_checks.py <check> --root <workspace root>

  y91-grant    the composition read's role policy names the jobs table in its GetItem statement and in its kms
               table-name condition, and names the requests table in both still                    -> Y91-GRANT-OK
  y91-census   the release census exists with the live package's members, the live blob of the gated file
               identified (or stated NOT FOUND with what was searched), and two equal build digests -> Y91-CENSUS-OK

--root is REQUIRED. Each check prints its token last, or the token with -FAIL after one FAIL line per problem. Writes nothing.
The grant check reads Terraform TEXT: it shows the statements are written, never that they are applied.
"""
import json
import re
import sys
from pathlib import Path

TF = "infra/aws/terraform/investor-reporting/export/commentary_composition.tf"
CENSUS = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/r9/COMPOSITION_READ_RELEASE_CENSUS.json"
TOKENS = {"y91-grant": "Y91-GRANT", "y91-census": "Y91-CENSUS"}


def statement(text, sid_prefix):
    found = re.search(r"\{\s*Sid\s*=\s*\"%s[^\"]*\".*?(?=\n\s*\{\s*Sid\s*=|\n\s*\]\s*\n)" % sid_prefix, text, flags=re.S)
    return found.group(0) if found else ""


def main(argv):
    if len(argv) < 2 or argv[1] not in TOKENS or "--root" not in argv:
        print(__doc__)
        return 2
    check = argv[1]
    root = Path(argv[argv.index("--root") + 1])
    problems = []
    if check == "y91-grant":
        text = (root / TF).read_text(encoding="utf-8")
        s1, s2 = statement(text, "S1"), statement(text, "S2")
        if not s1 or not s2:
            problems.append("statement S1 or S2 not found in %s" % TF)
        for name, body in (("S1", s1), ("S2", s2)):
            if "tables.requests" not in body:
                problems.append("%s no longer names the requests table" % name)
            if "tables.jobs" not in body:
                problems.append("%s does not name the jobs table" % name)
        if s1 and "dynamodb:GetItem" not in s1:
            problems.append("S1 is not the GetItem statement")
        actions = re.search(r"Action\s*=\s*\[(.*?)\]", s1, flags=re.S)
        if s1 and (not actions or re.findall(r"\"([^\"]+)\"", actions.group(1)) != ["dynamodb:GetItem"]):
            problems.append("S1's Action list is not exactly dynamodb:GetItem")
        if s1 and "LeadingKeys" not in s1:
            problems.append("S1 lost its LeadingKeys condition")
        if s2 and "kms:ViaService" not in s2:
            problems.append("S2 lost its ViaService condition")
        print("S1 names jobs: %s; S2 names jobs: %s" % ("tables.jobs" in s1, "tables.jobs" in s2))
    else:
        path = root / CENSUS
        if not path.is_file():
            problems.append("no %s" % CENSUS)
        else:
            doc = json.loads(path.read_text(encoding="utf-8"))
            live = doc.get("live") or {}
            if not (isinstance(live.get("code_sha256"), str) and live.get("members") and isinstance(live.get("member_count"), int)):
                problems.append("live: code_sha256, member_count and members are required")
            blob = doc.get("gated_file_live_blob") or {}
            if blob.get("found") not in (True, False) or not blob.get("searched"):
                problems.append("gated_file_live_blob needs found (true/false) and searched")
            if blob.get("found") is True and not (blob.get("commit") and blob.get("sha256")):
                problems.append("gated_file_live_blob found without its commit and sha256")
            build = doc.get("build") or {}
            if not build.get("sha256_first") or build.get("sha256_first") != build.get("sha256_second"):
                problems.append("build: two equal digests are required")
            if not isinstance(build.get("changed_members_vs_live"), list):
                problems.append("build.changed_members_vs_live is required")
            for row in doc.get("moved_members") or []:
                if row.get("served_effect") not in ("CHANGES_ANSWER", "INERT") or row.get("claim") not in ("measured", "inferred") \
                        or not row.get("why") or not row.get("owning_commits"):
                    problems.append("moved member incomplete: %r" % row.get("packaged_as"))
            if len(doc.get("moved_members") or []) != len(build.get("changed_members_vs_live") or [None]):
                problems.append("moved_members does not cover every changed member")
            print("live members %s; changed vs live %s" % (live.get("member_count"), len(build.get("changed_members_vs_live") or [])))
    for problem in problems:
        print("FAIL: %s" % problem)
    print("%s-%s" % (TOKENS[check], "FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
