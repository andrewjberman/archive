#!/usr/bin/env python
# NFRA_CLDGRPH.TO-CG-D-9 limb (i) arm (b) -- the CAUSAL classifier for night.sh.
# Author: 0.9.0_WK_NFRA_CLDGRPH~1. Reads CloudTrail RunTask events (JSON lines) on stdin and
# the projection vintage list in env VLIST_ALL. Pure read; writes nothing.
import collections
import datetime
import json
import os
import re
import sys

def iso(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(s)

vints = [v.strip() for v in os.environ.get("VLIST_ALL", "").split("\n") if v.strip()]
vpairs = sorted((iso(v), v) for v in vints)

# A family is REBUILD-CONSTITUTING if it writes a graph artifact: the derive runner (the full
# rebuild), the projection worker (writes projection/<vintage>/ and the pointer), and the
# producers (stamp the marker, which causes a projection rebuild). This is a classification of
# WHAT THE TASK DOES, not of who started it -- and it is UNIONED below with a purely empirical
# test (a projection vintage within 900 s of the task) so that a task OUTSIDE the declared set
# that did in fact produce a vintage is still counted. A scoped set cannot hide a member here.
FAMILY_RE = re.compile(r"(derive-runner|projection-worker|producer)")

rows = []
lines_in = 0
unparsed = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    lines_in += 1
    try:
        e = json.loads(line)
    except Exception:
        # LOUD, never silent. A dropped event understates the denominator this criterion prints,
        # and a bare 'continue' here would make the arm read cleaner the more it failed to read.
        unparsed += 1
        continue
    rp = e.get("requestParameters") or {}
    ui = e.get("userIdentity") or {}
    td = str(rp.get("taskDefinition") or "-")
    fam = td.split("/")[-1].split(":")[0]
    started = str(rp.get("startedBy") or "-")
    invoked = str(ui.get("invokedBy") or "-")
    ityp = str(ui.get("type") or "-")
    arn = str(ui.get("arn") or "-")
    srcip = str(e.get("sourceIPAddress") or "-")
    ua = str(e.get("userAgent") or "-")
    cluster = str(rp.get("cluster") or "-").split("/")[-1]
    t = iso(e["eventTime"])

    # PROVENANCE BY FORM -- what the starter IS, never a list of role names.
    if started.startswith("events-rule/"):
        prov = "RULE"
    elif started.startswith("chronos-schedule/") or started.startswith("schedule/"):
        prov = "SCHEDULE"
    elif started == "Started by Eventbridge Pipes" or started.startswith("pipe/"):
        prov = "PIPE"
    elif started.startswith("ecs-svc/"):
        prov = "SERVICE"
    elif started.startswith("deploy/") or started.startswith("codedeploy"):
        prov = "SERVICE"
    else:
        prov = "HUMAN-OR-SEAT"

    # CORROBORATION on a SECOND, unspoofable field: startedBy is caller-supplied and could be
    # forged; userIdentity.invokedBy is written by CloudTrail when an AWS service made the call.
    # TWO corroborating forms, in order. (i) invokedBy: written by CloudTrail when an AWS
    # service made the call. (ii) userAgent: the SDK banner an AWS-managed runtime emits --
    # an "Amazon*"/"aws-*" agent carrying exec-env/AWS_*. Both are read as FORMS, never as a
    # list of names. The EventBridge Scheduler path sets no invokedBy (it assumes a role and
    # calls as itself), which is exactly why a second form is needed: without it the one
    # scheduled producer in this window reads as uncorroborated.
    ua0 = ua.split()[0] if ua.strip() and ua != "-" else ""
    if invoked.endswith(".amazonaws.com"):
        corrob = "SERVICE-PRINCIPAL:" + invoked
    elif (ua0.startswith("Amazon") or ua0.startswith("AWS") or ua0.startswith("aws-")) and "exec-env/AWS_" in ua:
        corrob = "SERVICE-AGENT:" + ua0
    else:
        corrob = "NONE"
    conflict = (prov == "HUMAN-OR-SEAT" and corrob != "NONE")

    # nearest projection vintage, signed seconds
    if vpairs:
        best = min(vpairs, key=lambda p: abs((p[0] - t).total_seconds()))
        delta = (best[0] - t).total_seconds()
        vname = best[1]
    else:
        delta, vname = None, "-"
    near = abs(delta) <= 900 if delta is not None else False
    constituting = bool(FAMILY_RE.search(fam)) or near
    rows.append(dict(t=e["eventTime"], fam=fam, cluster=cluster, prov=prov, started=started,
                     corrob=corrob, ityp=ityp, arn=arn, srcip=srcip, ua=ua, conflict=conflict,
                     constituting=constituting, delta=delta, vname=vname))

rows.sort(key=lambda r: r["t"], reverse=True)
print("  EVENT LINES IN=%d ; PARSED=%d ; UNPARSED=%d  (an unparsed event is NOT silently"
      " dropped: it is counted here and it would understate every number below)"
      % (lines_in, len(rows), unparsed))
if unparsed:
    print("  WARN: %d CloudTrail event line(s) did not parse -- the denominator below is a FLOOR, not a count" % unparsed)
print("  PER-ROW LABELS (the control: these labels must add up to the totals below)")
print("  %-9s %-20s %-28s %-16s %-8s %s" % ("PROV", "eventTime", "family", "nearest vintage", "rebuild", "startedBy / corroboration"))
for r in rows:
    d = "n/a" if r["delta"] is None else ("%+.0fs" % r["delta"])
    print("  %-9s %-20s %-28s %-16s %-8s %s | %s" % (
        r["prov"], r["t"], r["fam"], d, "YES" if r["constituting"] else "no",
        r["started"], r["corrob"]))
    if r["prov"] == "HUMAN-OR-SEAT":
        print("      ^ identity=%s arn=%s sourceIP=%s nearest_vintage=%s" % (r["ityp"], r["arn"], r["srcip"], r["vname"]))
        print("      ^ userAgent=%s" % r["ua"])
    if r["conflict"]:
        print("      ^ PROV_CONFLICT: labelled HUMAN-OR-SEAT by startedBy but invokedBy names a service")

tot = len(rows)
tally = collections.Counter(r["prov"] for r in rows)
print()
print("  LABEL TALLY (must sum to the denominator):")
for k, v in sorted(tally.items()):
    print("    %-14s %d" % (k, v))
print("    %-14s %d" % ("SUM", sum(tally.values())))
print("  LABELS_AGREE_WITH_DENOMINATOR=%s (%d == %d)" % (str(sum(tally.values()) == tot).lower(), sum(tally.values()), tot))

constit = [r for r in rows if r["constituting"]]
nonconstit = [r for r in rows if not r["constituting"]]
seat_caused = [r for r in constit if r["prov"] == "HUMAN-OR-SEAT"]
uncorrob = [r for r in constit if r["prov"] != "HUMAN-OR-SEAT" and r["corrob"] == "NONE"]

print()
print("  REBUILD-CONSTITUTING tasks: %d ; NOT rebuild-constituting: %d ; total RunTask: %d"
      % (len(constit), len(nonconstit), tot))
print("  UNSCOPED CONTROL -- every HUMAN-OR-SEAT row in the WHOLE window, whether or not its")
print("  family is in the declared rebuild set, with the nearest projection vintage:")
hs = [r for r in rows if r["prov"] == "HUMAN-OR-SEAT"]
if not hs:
    print("    (none)")
for r in hs:
    d = "n/a" if r["delta"] is None else ("%+.0fs" % r["delta"])
    print("    %s  family=%s  nearest_vintage=%s (%s)  -> caused a rebuild: %s"
          % (r["t"], r["fam"], r["vname"], d, "YES" if r["constituting"] else "no"))
print("  CORROBORATION GAP -- automated rows with no service-principal in invokedBy: %d" % len(uncorrob))
for r in uncorrob:
    print("    %s  %s  prov=%s startedBy=%s sourceIP=%s role=%s" % (r["t"], r["fam"], r["prov"], r["started"], r["srcip"], r["arn"]))
    print("      userAgent=%s" % r["ua"])
print()
print("SEAT_CAUSED_REBUILDS=%d of %d" % (len(seat_caused), len(constit)))
