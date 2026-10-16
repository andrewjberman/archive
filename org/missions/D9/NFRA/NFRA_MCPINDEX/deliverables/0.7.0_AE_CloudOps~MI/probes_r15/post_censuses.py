"""post_censuses.py <probes dir>: the four censuses AFTER the apply, host vs the cut and host vs before. Read-only."""

import json
import re
import sys

p = sys.argv[1]


def section(txt, start, end):
    return txt.split(start, 1)[1].split(end, 1)[0].split()


served = open(p + "/served_names_host_r15.txt", encoding="utf-8").read()
host_names = set(served.split("---SERVED\n", 1)[1].split("\n---", 1)[0].split())
cut = json.load(open(p + "/tools_cut_r15.json"))
live = json.load(open(p + "/tools_live_r15.json"))
print("(1) TOOLS: host served %d; cut %d; live-before %d" % (len(host_names), cut["total"], live["total"]))
print("    host == cut names: %s; host == live-before names: %s" % (host_names == set(cut["all"]), host_names == set(live["all"])))
neg = sorted(host_names)[0]
print("    NEGATIVE CONTROL (drop %r from the host set): equal to cut reads %s" % (neg, (host_names - {neg}) == set(cut["all"])))

pre = open(p + "/host_read_r15_PREAPPLY.txt", encoding="utf-8").read()
post = open(p + "/host_read_r15_POST.txt", encoding="utf-8").read()
kb = section(pre, "---ENVKEYS\n", "---ENVLINES")
ka = section(post, "---ENVKEYS\n", "---ENVLINES")
print("(2) .env KEYS: before %d, after %d; dropped %s; added %s" % (len(kb), len(ka), sorted(set(kb) - set(ka)), sorted(set(ka) - set(kb))))
eb = re.search(r"---ENABLED (.*)", pre).group(1)
ea = re.search(r"---ENABLED (.*)", post).group(1)
print("(3) ENABLED_INTEGRATIONS before == after: %s (%s)" % (eb == ea, eb))

host_lc = {}
for ln in open(p + "/link_counts_REAL_host_POST.txt", encoding="utf-8"):
    m = re.match(r"REAL TOOL (\S+) (\d+)", ln)
    if m:
        host_lc[m.group(1)] = int(m.group(2))
cut_lc = {}
for ln in open(p + "/link_counts_A1.txt", encoding="utf-8"):
    m = re.match(r"CUT TOOL (\S+) (\d+)", ln)
    if m:
        cut_lc[m.group(1)] = int(m.group(2))
print("(4) LINK COUNTS: host %d tools / %d links; cut %d tools / %d links; per-tool equal: %s"
      % (len(host_lc), sum(host_lc.values()), len(cut_lc), sum(cut_lc.values()), host_lc == cut_lc))
bumped = dict(host_lc)
bumped[sorted(bumped)[0]] += 1
print("    NEGATIVE CONTROL (bump one host count): equal reads %s" % (bumped == cut_lc))
ok = (
    host_names == set(cut["all"]) and set(kb) == set(ka) and eb == ea and host_lc == cut_lc
    and (len(host_lc), sum(host_lc.values())) == (65, 192) and len(host_names) == 127 and len(ka) == 64
)
print("EXPECTED (127 tools equal, 64 keys equal, 7 ids equal, 65 tools / 192 links): %s" % ("MATCH" if ok else "MISMATCH"))
sys.exit(0 if ok else 1)
