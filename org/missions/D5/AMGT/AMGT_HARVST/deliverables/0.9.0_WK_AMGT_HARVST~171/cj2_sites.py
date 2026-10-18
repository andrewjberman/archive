"""cj2_sites.py -- AMGT_HARVST HVST-cj-2 step 1a (read only). Prints the harvest tools of app/harvest_research.py, the
line and enclosing function of every site that builds a prefix from the security key or compares a security_key value,
and whether the deployed artifact can import lib.research.identity.crosswalk. Reads files only; writes cj2_sites.out.

Usage, from the worktree root:  python -u <this file>
"""

import os
import re
import sys

ROOT = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "cj2_sites.out")
GW = os.path.join(ROOT, "infra", "aws", "ec2", "opal-gateway")
RESEARCH = os.path.join(GW, "app", "harvest_research.py")
DEPLOY = os.path.join(GW, "deploy-to-ec2.sh")

SITE = re.compile(r"%\s*(key|security_key)\b|security_key\"\)\s*==|== key\b|sk == key|P_[A-Z_]+ % ")


def read_lines(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def main():
    lines = []

    def out(text):
        safe = text.encode("ascii", "backslashreplace").decode("ascii")
        print(safe, flush=True)
        lines.append(safe)

    src = read_lines(RESEARCH)
    out("CJ2-SITES file=infra/aws/ec2/opal-gateway/app/harvest_research.py lines=%d" % len(src))
    current = "module"
    tools = []
    for number, text in enumerate(src, start=1):
        m = re.match(r"def (\w+)\(", text)
        if m:
            current = m.group(1)
        if re.match(r"(TOOL_|P_)[A-Z_]+ = ", text):
            out("CONST line=%d %s" % (number, text.strip()))
        if text.startswith("def harvest_get_"):
            tools.append((number, current))
    for number, name in tools:
        out("TOOL line=%d %s" % (number, name))
    sites = 0
    for number, text in enumerate(src, start=1):
        m = re.match(r"def (\w+)\(", text)
        if m:
            current = m.group(1)
        if SITE.search(text) and not re.match(r"(TOOL_|P_)[A-Z_]+ = ", text):
            sites += 1
            out("SITE line=%d fn=%s %s" % (number, current, text.strip()))
    out("DENOMINATOR sites=%d tools=%d" % (sites, len(tools)))

    deploy = read_lines(DEPLOY)
    lib_lines = [t.strip() for t in deploy if re.search(r'bundle/lib"|lib/(trading_calendar|opal_naming)\.py', t)]
    for t in lib_lines:
        out("DEPLOY-LIB %s" % t[:160])
    shipped = [t for t in lib_lines if "crosswalk" in t or "lib/research" in t]
    out("DEPLOY-CROSSWALK-SHIPPED %s (the artifact lib/ carries trading_calendar.py and opal_naming.py only; "
        "tar -C bundle lib, no lib/research)" % ("yes" if shipped else "no"))
    out("DEPLOY-CROSSWALK-IMPORTABLE-ON-HOST %s -- %s" % (
        "no" if not shipped else "yes",
        "the normalizer is a copy in the app (order step b)" if not shipped else "the app may import the module"))

    with open(OUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        for line in lines:
            fh.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
