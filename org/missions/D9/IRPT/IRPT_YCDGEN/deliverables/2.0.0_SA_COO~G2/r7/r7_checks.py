"""IRPT_YCDGEN round 7 checks (issuer 2.0.0_SA_COO~G2): one research role per allowed firm (row D2-S19, CTO ruling @f29d0d8ca1).

    python r7_checks.py firms      the research policy row names exactly cottonwood, 49financial, inflection
    python r7_checks.py fence      each firm's research prefixes (derived as resident.tf derives them) name only its own bucket and scope
    python r7_checks.py regress    the ycharts generate + research suites: no file newly red against the base

Run from the worktree root. Prints one RESULT line, R7-<MODE>-OK or R7-<MODE>-FAIL <reason>; rc 0 only on OK.
"""
import json
import re
import subprocess
import sys

REG = "infra/logic/registry/"
WANT = {"cottonwood", "49financial", "inflection"}
Y = "infra/aws/lambda/investor-reporting/ycharts"
BASE_RED = {Y + "/generate/tests/test_custody_retained.py", Y + "/generate/tests/test_custody_entry.py"}
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def policy():
    rows = json.load(open(REG + "reporting_policies.json", encoding="utf-8"))["policies"]
    return [p for p in rows if p["policy_revision"] == "irpt-ycdgen-research-v1"][0]


def scopes():
    out = {}
    for s in json.load(open(REG + "scopes.json", encoding="utf-8"))["scopes"]:
        if s.get("class") == "FIRM" and (s.get("tenant") or {}).get("kind") == "client" and (s.get("tenant") or {}).get("enabled"):
            out[s["key"]] = s
    return out


def main(mode):
    if mode == "firms":
        firms = set(policy()["firms"])
        if firms != WANT:
            print("R7-FIRMS-FAIL firms=%s want=%s" % (sorted(firms), sorted(WANT)))
            return 1
        print("R7-FIRMS-OK firms=%s" % sorted(firms))
        return 0
    if mode == "fence":
        p, sc = policy(), scopes()
        fams = [f for f in ("YCHARTS_RESPONSE", "YCHARTS_RUN")]
        prefixes = {}
        for firm in p["firms"]:
            if firm not in sc:
                print("R7-FENCE-FAIL %s has no enabled client FIRM scope" % firm)
                return 1
            s = sc[firm]
            prefixes[firm] = ["arn:aws:s3:::%s/%s/%s/%s/%s/*" % (s["bucket"], p["source"], s["long"], p["families"][f]["tier"],
                                                               p["families"][f]["table"]) for f in fams]
        for firm, arns in prefixes.items():
            others = [sc[o] for o in prefixes if o != firm]
            for arn in arns:
                hits = [o["key"] for o in others if o["bucket"] in arn or "/%s/" % o["long"] in arn]
                if hits or sc[firm]["bucket"] not in arn:
                    print("R7-FENCE-FAIL %s prefix %s names %s" % (firm, arn, hits or "not its own bucket"))
                    return 1
        print("R7-FENCE-OK firms=%d prefixes=%d, each names only its own bucket and scope" % (
            len(prefixes), sum(len(v) for v in prefixes.values())))
        return 0
    if mode == "regress":
        red = set()
        for suite in ("generate", "research"):
            out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rfE", Y + "/" + suite + "/tests"],
                                 capture_output=True, text=True, encoding="utf-8", errors="replace")
            text = ANSI.sub("", out.stdout + out.stderr)
            lines = [ln for ln in text.splitlines() if re.search(r"\d+ (passed|failed|error)", ln)]
            print(suite + ": " + (lines[-1].strip() if lines else "(no summary)"))
            red |= {i.split("::")[0] for i in re.findall(r"^(?:FAILED|ERROR) (\S+)", text, re.M)}
        new = sorted(red - BASE_RED)
        if new:
            print("R7-REGRESS-FAIL newly red: " + ", ".join(new))
            return 1
        print("R7-REGRESS-OK red files %d, all in the base set of %d" % (len(red), len(BASE_RED)))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
