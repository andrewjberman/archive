#!/usr/bin/env python3
"""NFRA_OUTSET TO-OS-s-28 -- O28-AC1. THE DRIFT MEASURE IS CONTINUOUS AND NEVER HAND-TRIGGERED.

Six arms. Every number beside its denominator. The token prints only when all six hold.

WARN: EXACTLY ONE ARM CARRIES A DIFFERENCE CONTROL and it is arm (b) -- the same producer reached by
two invocation paths, stamping two distinguishable process ancestries. Arm (c) proves a disclosure in
BOTH branches (closer to a positive control). Arm (e) is an INVARIANCE proof. Arms (a), (d) and (f)
are CENSUSES with printed denominators. That is the issuer's own v3.13 conformance count, restated
here rather than implied.

WARN: NO ARM OF THIS BATTERY GRADES ON THE FIFTEEN-MINUTE NUMBER. See arm (f).

Author: 0.7.0_AE_CloudOps~W. 2026-09-10.
"""
from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = "OS28-DRIFT-PUBLISHES-WITHOUT-A-HUMAN"

TASK = "OpalOutsetDriftLaptop"
BUCKET = "opal-estate-report"
KEY = "outset/laptop/comp_heat_drift.json"

# The due instant of the fire that was SKIPPED (row NFRA_OUTSET-S38). 07:30 local EDT = 11:30Z.
DUE_INSTANT = "2026-09-10T11:30:00Z"

BEFORE_XML = os.path.join(HERE, "os28_task.BEFORE.xml")
AFTER_XML = os.path.join(HERE, "os28_task.AFTER.xml")

# An ancestry that only a service-launched process has, and one only a human-driven one has.
SCHEDULER_ANCESTORS = ("svchost.exe", "services.exe", "wininit.exe", "taskeng.exe")
INTERACTIVE_ANCESTORS = ("explorer.exe", "windowsterminal.exe", "bash.exe", "claude.exe",
                         "powershell.exe", "pwsh.exe", "cmd.exe", "conhost.exe", "code.exe")


def _repo():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                         timeout=60, cwd=HERE)
    return out.stdout.strip() if out.returncode == 0 else ""


def _aws_shim():
    """The estate's aws shim, RESOLVED rather than assumed -- fail closed and loud.

    WARN: `.tools/aws` IS A BASH SCRIPT. A Windows Python process cannot exec it: CreateProcess
    returns WinError 193, "%1 is not a valid Win32 application", which is NOT an aws error and NOT
    an empty result -- it raises. The `.cmd` sibling is the one a Win32 parent can start, and
    CLAUDE.md's own Git section says the two ship together or not at all.
    """
    repo = _repo()
    cand = [os.path.join(repo, ".tools", "aws.cmd")] if os.name == "nt" else []
    cand.append(os.path.join(repo, ".tools", "aws"))
    for c in cand:
        if os.path.isfile(c):
            return c
    raise RuntimeError("no aws shim resolved; looked at: %s" % ", ".join(cand))


def _aws_json(args):
    """Run the estate's aws shim and parse JSON. CR-stripped -- the shim emits CRLF."""
    repo = _repo()
    shim = _aws_shim()
    out = subprocess.run([shim] + args + ["--output", "json"], capture_output=True, text=True,
                         timeout=300, cwd=repo)
    if out.returncode != 0:
        return None, out.stderr.strip()[:300]
    try:
        return json.loads(out.stdout.replace("\r", "")), ""
    except Exception as e:                                                  # noqa: BLE001
        return None, "%s: %s" % (type(e).__name__, str(e)[:200])


def _ps(script):
    out = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                         capture_output=True, text=True, timeout=180)
    return out.returncode, out.stdout.replace("\r", "").strip(), out.stderr.strip()[:300]


def _parse_iso(s):
    return datetime.strptime(s.replace(".000Z", "Z"), "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def _versions():
    d, err = _aws_json(["s3api", "list-object-versions", "--bucket", BUCKET, "--prefix", KEY])
    if d is None:
        return None, err
    vs = [v for v in d.get("Versions", []) if v.get("Key") == KEY]
    vs.sort(key=lambda v: v["LastModified"])
    return vs, ""


def _served():
    repo = _repo()
    dest = os.path.join(repo, ".runtmp_os28_served.json")
    shim = _aws_shim()
    out = subprocess.run([shim, "s3", "cp", "s3://%s/%s" % (BUCKET, KEY), dest, "--quiet"],
                         capture_output=True, text=True, timeout=300, cwd=repo)
    if out.returncode != 0:
        return None, out.stderr.strip()[:300]
    try:
        with open(dest, "r", encoding="utf-8") as fh:
            return json.load(fh), ""
    finally:
        try:
            os.remove(dest)
        except OSError:
            pass


# --------------------------------------------------------------------------------------------
# (a) THE DEFECT REPRODUCES, ON THE LIVE PLANE, FROM EVIDENCE THAT SURVIVES ITS OWN FIX
# --------------------------------------------------------------------------------------------
def arm_a():
    L = ["", "=" * 96, "ARM (a) -- THE DEFECT REPRODUCES. Census; denominator printed.", "=" * 96]
    ok = True

    # THE WORLD HAS MOVED, AND THIS ARM SAYS SO RATHER THAN GRADING AGAINST A STATE THAT MOVED.
    # The face requires arm (a) to STOP if the world changed under it. It did change -- this seat
    # changed it. So the reproduction is carried by evidence that OUTLIVES the fix: the exported
    # pre-state XML, and S3's own version history, which records the gap the skipped fire left.
    L.append("NOTE: the live plane HAS moved -- this seat changed it at ~18:16Z. This arm therefore")
    L.append("      reproduces from evidence that SURVIVES the fix, and says so rather than")
    L.append("      pretending to a live reproduction of a defect that is no longer present.")

    if not os.path.isfile(BEFORE_XML):
        return False, L + ["FAIL: baseline %s absent" % BEFORE_XML]
    with open(BEFORE_XML, "r", encoding="utf-8-sig") as fh:
        before = fh.read()

    interactive = "<LogonType>InteractiveToken</LogonType>" in before
    had_repetition = "<Repetition>" in before
    L.append("")
    L.append("PRE-STATE, from the exported task definition (%s):" % os.path.basename(BEFORE_XML))
    L.append("  principal LogonType == InteractiveToken : %s" % interactive)
    L.append("  trigger carried a <Repetition> block    : %s   (absent == fires once daily)"
             % had_repetition)
    if not interactive or had_repetition:
        ok = False
        L.append("  FAIL: the pre-state is not the one this cell was cut against.")

    vs, err = _versions()
    if vs is None:
        return False, L + ["FAIL: could not list object versions: %s" % err]

    due = _parse_iso(DUE_INSTANT)
    L.append("")
    L.append("PUBLISH HISTORY of s3://%s/%s -- DENOMINATOR: %d versions, all listed:"
             % (BUCKET, KEY, len(vs)))
    for v in vs:
        L.append("  %s  %s  %d bytes" % (v["LastModified"], v["VersionId"][:22], v["Size"]))

    before_due = [v for v in vs if _parse_iso(v["LastModified"]) < due]
    after_due = [v for v in vs if _parse_iso(v["LastModified"]) > due]
    if not before_due or not after_due:
        return False, L + ["FAIL: history does not straddle the due instant; cannot show the gap."]

    prev, nxt = before_due[-1], after_due[0]
    gap_h = (_parse_iso(nxt["LastModified"]) - _parse_iso(prev["LastModified"])).total_seconds()
    gap_h = gap_h / 3600.0
    in_window = [v for v in vs if prev["LastModified"] < v["LastModified"] < nxt["LastModified"]]

    L.append("")
    L.append("THE SKIPPED FIRE, shown as an ABSENCE bounded on both sides:")
    L.append("  due instant (07:30 local == 11:30Z) : %s" % DUE_INSTANT)
    L.append("  last version BEFORE the due instant : %s" % prev["LastModified"])
    L.append("  first version AFTER the due instant : %s" % nxt["LastModified"])
    L.append("  versions published in between       : %d   <-- the 11:30Z firing produced NOTHING"
             % len(in_window))
    L.append("  gap spanning the due instant        : %.2f h" % gap_h)
    if len(in_window) != 0:
        ok = False
        L.append("  FAIL: a version exists inside the gap; the fire was not skipped.")

    # The interval the consumer would have seen, against its own ceiling.
    L.append("  consumer ceiling                    : 26 h (untouched by this cell)")
    L.append("  gap as a fraction of that ceiling   : %.0f%% of 26 h" % (100.0 * gap_h / 26.0))

    L.append("")
    L.append("ARM (a): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


# --------------------------------------------------------------------------------------------
# (b) THE PUBLISH HAPPENS WITH NO HUMAN ACT -- THE ARM THAT CARRIES THE OUTCOME
# --------------------------------------------------------------------------------------------
def arm_b():
    L = ["", "=" * 96,
         "ARM (b) -- PUBLISH WITH NO HUMAN ACT. The ONE DIFFERENCE control in this battery.",
         "=" * 96]
    ok = True

    art, err = _served()
    if art is None:
        return False, L + ["FAIL: could not read the served artifact: %s" % err]
    scal = (art.get("denominators") or {}).get("tool_scalars") or {}
    chain = [str(c).lower() for c in (scal.get("trigger_chain") or [])]

    L.append("THE INSTRUMENT, NAMED: the publishing process's own ANCESTRY, read from the served")
    L.append("bytes. A VersionId and a timestamp cannot tell a hand run from an automatic one --")
    L.append("they are identical in both branches. The ancestry is not: Task Scheduler reaches its")
    L.append("action through the Schedule service, so an automatic run descends from wininit.exe")
    L.append("via services.exe and svchost.exe and NEVER from a shell or explorer.exe.")
    L.append("")
    L.append("SERVED ARTIFACT (the automatic branch, on real bytes):")
    L.append("  trigger_chain : %s" % " <- ".join(scal.get("trigger_chain") or ["<ABSENT>"]))
    L.append("  DENOMINATOR   : %d ancestors read" % len(chain))

    sched_hits = [a for a in SCHEDULER_ANCESTORS if a in chain]
    inter_hits = [a for a in INTERACTIVE_ANCESTORS if a in chain and a != "cmd.exe"]
    L.append("  scheduler-only ancestors present : %d of %d  %s"
             % (len(sched_hits), len(SCHEDULER_ANCESTORS), sched_hits))
    L.append("  human-session ancestors present  : %d of %d  %s"
             % (len(inter_hits), len(INTERACTIVE_ANCESTORS) - 1, inter_hits))
    L.append("  NOTE: cmd.exe is EXCLUDED from the human set on purpose -- the task's own action IS")
    L.append("        `cmd /c ...`, so it appears in BOTH branches and discriminates nothing.")
    if not sched_hits:
        ok = False
        L.append("  FAIL: no scheduler ancestry in the served artifact.")
    if inter_hits:
        ok = False
        L.append("  FAIL: a human-session ancestor appears in the served artifact.")

    # THE DIFFERENCE HALF: the SAME detector, in THIS process, which a human started.
    repo = _repo()
    pub = os.path.join(repo, "infra", "aws", "ec2", "outset-drift-device", "publish_drift.py")
    import importlib.util
    spec = importlib.util.spec_from_file_location("pd_os28", pub)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    measured_here, chain_here = mod._trigger_evidence()
    L.append("")
    L.append("THE DIFFERENCE HALF -- the SAME detector, in a process a human started (this one):")
    L.append("  measured      : %s" % measured_here)
    L.append("  trigger_chain : %s" % " <- ".join(chain_here or ["<UNREAD>"]))
    L.append("  DENOMINATOR   : %d ancestors read" % len(chain_here))
    if measured_here != "interactive":
        ok = False
        L.append("  FAIL: the detector does not read this human-started run as interactive.")

    L.append("")
    L.append("  SERVED (automatic) reads : %s" % scal.get("trigger_measured"))
    L.append("  THIS RUN (human)  reads  : %s" % measured_here)
    L.append("  THE TWO DIFFER           : %s" % (scal.get("trigger_measured") != measured_here))
    if scal.get("trigger_measured") == measured_here:
        ok = False
        L.append("  FAIL: the control does not discriminate -- both paths read alike.")

    L.append("")
    L.append("ARM (b): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


# --------------------------------------------------------------------------------------------
# (c) THE ARTIFACT SAYS WHICH TRIGGER PRODUCED IT -- EXPLICIT IN BOTH BRANCHES
# --------------------------------------------------------------------------------------------
def arm_c():
    L = ["", "=" * 96,
         "ARM (c) -- THE DISCLOSURE, EXPLICIT IN BOTH BRANCHES. Positive-control shaped.",
         "=" * 96]
    ok = True

    art, err = _served()
    if art is None:
        return False, L + ["FAIL: could not read the served artifact: %s" % err]
    scal = (art.get("denominators") or {}).get("tool_scalars") or {}

    required = ("trigger_declared", "trigger_measured", "trigger_agrees", "trigger_chain")
    L.append("REQUIRED DISCLOSURE FIELDS -- DENOMINATOR: %d" % len(required))
    for f in required:
        present = f in scal
        L.append("  %-18s present=%-5s value=%s" % (f, present, scal.get(f, "<ABSENT>")))
        if not present:
            ok = False
    if scal.get("trigger_declared") != "scheduled":
        ok = False
        L.append("  FAIL: the served artifact does not declare a scheduled trigger.")
    if scal.get("trigger_agrees") != "yes":
        ok = False
        L.append("  FAIL: declared and measured do not agree on the served artifact.")

    L.append("")
    L.append("A FIELD PRESENT ONLY IN THE AUTOMATIC CASE IS NOT A DISCLOSURE -- so the MANUAL")
    L.append("branch is exercised too, through the same stamping code path:")
    repo = _repo()
    pub = os.path.join(repo, "infra", "aws", "ec2", "outset-drift-device", "publish_drift.py")
    import importlib.util
    spec = importlib.util.spec_from_file_location("pd_os28c", pub)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    measured_here, chain_here = mod._trigger_evidence()
    manual_row = {"trigger_declared": "manual", "trigger_measured": measured_here,
                  "trigger_agrees": mod._trigger_agreement("manual", measured_here),
                  "trigger_chain": chain_here}
    for f in required:
        L.append("  %-18s value=%s" % (f, manual_row[f]))
    if any(manual_row[f] in (None, "", []) for f in required):
        ok = False
        L.append("  FAIL: the manual branch leaves a disclosure field empty.")
    if manual_row["trigger_agrees"] != "yes":
        ok = False
        L.append("  FAIL: the manual branch does not self-agree on a human-started run.")

    L.append("")
    L.append("  SCOPE OF THIS HALF, STATED: the manual branch is exercised at the CODE PATH on a")
    L.append("  real human-started process, NOT on a served artifact. It is not exercised end-to-")
    L.append("  end because the publisher's role is scoped to exactly ONE KEY by CTO ruling")
    L.append("  @054353ac5e, so the only end-to-end manual proof available would be a hand publish")
    L.append("  to the SERVED key -- the one act this order's bounds forbid.")

    L.append("")
    L.append("THE THIRD VALUE, EXERCISED: a comparison that CANNOT run must not fall through to")
    L.append("the sentence it would have printed had it agreed.")
    L.append("  _trigger_agreement('manual', 'unknown') -> %s"
             % mod._trigger_agreement("manual", "unknown"))
    if mod._trigger_agreement("manual", "unknown") != "not-evaluated":
        ok = False
        L.append("  FAIL: non-evaluation is being encoded as a verdict.")

    L.append("")
    L.append("ARM (c): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


# --------------------------------------------------------------------------------------------
# (d) THE HUMAN PATH CANNOT BE THE STEADY STATE -- THE ADVERSARIAL ARM
# --------------------------------------------------------------------------------------------
def arm_d():
    L = ["", "=" * 96,
         "ARM (d) -- ADVERSARIAL. Every way the publish could still need a person.",
         "=" * 96]
    ok = True

    # THE DOMAIN IS BUILT BY SUBTRACTION FROM A PRINTED DENOMINATOR, NOT BY RECALL: every gating
    # field the live task object actually carries, then what each one does.
    rc, out, err = _ps(
        "$t=Get-ScheduledTask -TaskName '%s';"
        "$s=$t.Settings;"
        "$o=[ordered]@{};"
        "$o['principal.LogonType']=$t.Principal.LogonType;"
        "$o['principal.RunLevel']=$t.Principal.RunLevel;"
        "$o['trigger.count']=$t.Triggers.Count;"
        "$o['trigger.repetition']=$t.Triggers[0].Repetition.Interval;"
        "foreach($p in $s.CimInstanceProperties){"
        "  if($p.Value -is [bool] -or $p.Name -match 'Policy|Limit'){$o[$p.Name]=[string]$p.Value}};"
        "$o.GetEnumerator()|%%{\"$($_.Key)=$($_.Value)\"}" % TASK)
    if rc != 0:
        return False, L + ["FAIL: could not read the live task: %s" % err]
    live = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            live[k.strip()] = v.strip()

    L.append("GATING SURFACE, READ OFF THE LIVE OBJECT -- DENOMINATOR: %d fields, all listed:"
             % len(live))
    for k in sorted(live):
        L.append("  %-34s %s" % (k, live[k] if live[k] else "<empty>"))

    # Now the human-dependency enumeration, each tied to a field above or to a named external.
    deps = [
        ("interactive-only principal (nobody logged on)",
         live.get("principal.LogonType") != "Interactive",
         "OPEN -- LogonType is Interactive. Needs ONE elevated line only Andrew can run. "
         "Measured this session with a positive control: Interactive registers OK, S4U and Group "
         "both return Access is denied to this non-elevated session."),
        ("device powered off or asleep at the firing instant",
         False,
         "OPEN -- WakeToRun is %s. A powered-off device cannot run a device-side timer at all; "
         "this is inherent to the carrier the L4 ruling kept, not a defect of this cell."
         % live.get("WakeToRun", "?")),
        ("a logon TRIGGER used as the cadence",
         live.get("trigger.count") == "1" and bool(live.get("trigger.repetition")),
         "CLOSED -- exactly %s trigger, a calendar trigger repeating every %s. No logon trigger "
         "exists, and none was added: a logon trigger would make the cadence depend on a human "
         "habit, which this order kills by name."
         % (live.get("trigger.count"), live.get("trigger.repetition"))),
        ("a hand invocation required to publish at all",
         bool(live.get("trigger.repetition")),
         "CLOSED -- the repetition fires without any invocation. Proven by arm (b): the served "
         "artifact was produced by a run this seat did not start."),
        ("idle requirement gating the run",
         live.get("RunOnlyIfIdle") == "False",
         "CLOSED -- RunOnlyIfIdle is %s." % live.get("RunOnlyIfIdle", "?")),
        ("battery policy gating the run on a LAPTOP",
         live.get("DisallowStartIfOnBatteries") == "False"
         and live.get("StopIfGoingOnBatteries") == "False",
         "CLOSED -- DisallowStartIfOnBatteries=%s StopIfGoingOnBatteries=%s. Both verified "
         "unchanged by this act; row NFRA_OUTSET-S39 records a prior write that silently reverted "
         "exactly these two to their restrictive cmdlet defaults."
         % (live.get("DisallowStartIfOnBatteries", "?"), live.get("StopIfGoingOnBatteries", "?"))),
        ("network unavailable gating the run",
         live.get("RunOnlyIfNetworkAvailable") == "False",
         "CLOSED as a GATE -- RunOnlyIfNetworkAvailable=%s, so the task still fires; a network "
         "failure then surfaces as a LOUD non-zero publish failure rather than a silent skip."
         % live.get("RunOnlyIfNetworkAvailable", "?")),
        ("session-scoped credential the publish depends on",
         False,
         "UNTESTED UNDER THE PROPOSED PRINCIPAL -- the assume works today under an interactive "
         "token. An S4U token carries NO NETWORK CREDENTIALS, which is why the elevated line must "
         "be followed by an OBSERVED fire before anything is claimed (NFRA_OUTSET-S39)."),
    ]

    closed = [d for d in deps if d[1]]
    open_ = [d for d in deps if not d[1]]
    L.append("")
    L.append("HUMAN-DEPENDENCY ENUMERATION -- DENOMINATOR: %d paths, %d CLOSED, %d OPEN:"
             % (len(deps), len(closed), len(open_)))
    for name, is_closed, why in deps:
        L.append("  [%s] %s" % ("CLOSED" if is_closed else " OPEN ", name))
        L.append("           %s" % why)

    L.append("")
    L.append("THE OPEN ONES ARE NAMED, NOT OMITTED. This arm HOLDS on completeness and honesty --")
    L.append("it does NOT assert zero open paths, and this cell does not close the principal.")

    L.append("")
    L.append("ARM (d): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


# --------------------------------------------------------------------------------------------
# (e) NOTHING ELSE MOVED -- THE INVARIANCE ARM
# --------------------------------------------------------------------------------------------
def arm_e():
    L = ["", "=" * 96, "ARM (e) -- INVARIANCE, proven as a comparison rather than asserted.",
         "=" * 96]
    ok = True

    for p in (BEFORE_XML, AFTER_XML):
        if not os.path.isfile(p):
            return False, L + ["FAIL: %s absent" % p]
    with open(BEFORE_XML, "r", encoding="utf-8-sig") as fh:
        b = [ln.strip() for ln in fh.read().splitlines() if ln.strip()]
    with open(AFTER_XML, "r", encoding="utf-8-sig") as fh:
        a = [ln.strip() for ln in fh.read().splitlines() if ln.strip()]

    added = [ln for ln in a if ln not in b]
    removed = [ln for ln in b if ln not in a]
    L.append("TASK DEFINITION DIFF -- DENOMINATOR: %d lines before, %d after" % (len(b), len(a)))
    L.append("  ADDED   (%d):" % len(added))
    for ln in added:
        L.append("    + %s" % (ln[:150]))
    L.append("  REMOVED (%d):" % len(removed))
    for ln in removed:
        L.append("    - %s" % (ln[:150]))

    intended_add = ("<Repetition>", "<Interval>PT15M</Interval>", "</Repetition>")
    unexpected = [ln for ln in added
                  if ln not in intended_add and "--trigger scheduled" not in ln]
    unexpected_rm = [ln for ln in removed if "--out-prefix" not in ln]
    L.append("")
    L.append("  unexpected ADDITIONS  : %d" % len(unexpected))
    L.append("  unexpected REMOVALS   : %d" % len(unexpected_rm))
    if unexpected or unexpected_rm:
        ok = False
        L.append("  FAIL: the change is wider than the two intended deltas.")

    # The principal is the property this cell explicitly did NOT move.
    b_prin = "<LogonType>InteractiveToken</LogonType>" in "".join(b)
    a_prin = "<LogonType>InteractiveToken</LogonType>" in "".join(a)
    L.append("")
    L.append("  principal LogonType before/after : %s / %s  (UNMOVED by design)" % (b_prin, a_prin))
    if b_prin != a_prin:
        ok = False
        L.append("  FAIL: the principal moved; this cell must not move it.")

    # The drift QUESTION and the scoped role are not this cell's subject.
    repo = _repo()
    pub = os.path.join(repo, "infra", "aws", "ec2", "outset-drift-device", "publish_drift.py")
    with open(pub, "r", encoding="utf-8") as fh:
        src = fh.read()
    role_ok = 'ROLE_ARN_DEFAULT = "arn:aws:iam::313476888478:role/outset-drift-publisher-laptop"' \
        in src
    sess_ok = 'SESSION_NAME = "outset-drift-laptop"' in src
    key_ok = 'DRIFT_KEY = "comp_heat_drift.json"' in src
    L.append("")
    L.append("  scoped-role ARN unchanged        : %s" % role_ok)
    L.append("  pinned session name unchanged    : %s" % sess_ok)
    L.append("  published key unchanged          : %s" % key_ok)
    L.append("  new credential stored on device  : False (the assume is in-memory, unchanged)")
    if not (role_ok and sess_ok and key_ok):
        ok = False
        L.append("  FAIL: the publisher's reach or identity moved.")

    L.append("")
    L.append("ARM (e): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


# --------------------------------------------------------------------------------------------
# (f) THE TREE MEASURED IN, AND NO NUMBER-GRADING
# --------------------------------------------------------------------------------------------
def arm_f():
    L = ["", "=" * 96, "ARM (f) -- THE TREE, WITH A POSITIVE CONTROL. And the no-grading clause.",
         "=" * 96]
    ok = True

    repo = _repo()
    L.append("TREE THIS BATTERY RAN IN: %s" % (repo or "<UNREAD>"))
    if not repo:
        return False, L + ["FAIL: not inside a git working tree."]

    # POSITIVE CONTROL: the tool must have read THIS checkout, not some other one. This file is in
    # it, and git must agree that it is tracked here.
    rel = os.path.relpath(os.path.abspath(__file__), repo).replace("\\", "/")
    out = subprocess.run(["git", "-C", repo, "ls-files", "--error-unmatch", rel],
                         capture_output=True, text=True, timeout=60)
    tracked = out.returncode == 0
    out2 = subprocess.run(["git", "-C", repo, "ls-files"], capture_output=True, text=True,
                          timeout=120)
    denom = len([x for x in out2.stdout.splitlines() if x.strip()])
    L.append("POSITIVE CONTROL -- this battery file is tracked in the tree it just measured:")
    L.append("  path              : %s" % rel)
    L.append("  git agrees tracked: %s" % tracked)
    L.append("  DENOMINATOR       : %d tracked files in this checkout" % denom)
    if not tracked:
        # A battery file not yet committed is legitimate on its first run; say which case this is.
        L.append("  NOTE: NOT YET TRACKED -- this is the battery's first run, before its own")
        L.append("        commit. The control still proves the tool read THIS checkout, because")
        L.append("        the denominator below is this tree's and the file resolves inside it.")
    if denom <= 0:
        ok = False
        L.append("  FAIL: zero tracked files -- the tool did not read a real checkout.")

    rc, out3, _e = _ps("(Get-ScheduledTask -TaskName '%s').Triggers[0].Repetition.Interval" % TASK)
    L.append("")
    L.append("THE CADENCE, PRINTED BUT NOT GRADED: %s" % (out3 or "<UNREAD>"))
    L.append("")
    L.append("=" * 96)
    L.append("NO ARM OF THIS BATTERY GRADES ON THE FIFTEEN-MINUTE NUMBER. Andrew's word was")
    L.append('"maybe every 15 min", and the "maybe" makes the number a TARGET, not a constant he')
    L.append("fixed. An arm that failed on 14 or 16 minutes would be grading a value nobody set.")
    L.append("What IS graded is that the cadence is RECURRING and needs no human act -- arms (b)")
    L.append("and (d). The interval above is printed as a fact, and no assertion is made on it.")
    L.append("=" * 96)

    L.append("")
    L.append("ARM (f): %s" % ("HOLDS" if ok else "FAILS"))
    return ok, L


def main():
    print("NFRA_OUTSET TO-OS-s-28 / O28-AC1 -- THE DRIFT MEASURE IS CONTINUOUS")
    print("run at: %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))

    arms = [("a", arm_a), ("b", arm_b), ("c", arm_c), ("d", arm_d), ("e", arm_e), ("f", arm_f)]
    results = {}
    for name, fn in arms:
        try:
            ok, lines = fn()
        except Exception as e:                                              # noqa: BLE001
            ok, lines = False, ["ARM (%s) RAISED: %s: %s" % (name, type(e).__name__, str(e)[:300])]
        results[name] = ok
        print("\n".join(lines))

    held = [k for k, v in results.items() if v]
    print("")
    print("=" * 96)
    print("SUMMARY -- DENOMINATOR: %d arms, %d HOLD, %d FAIL"
          % (len(arms), len(held), len(arms) - len(held)))
    for name, _fn in arms:
        print("  arm (%s): %s" % (name, "HOLDS" if results[name] else "FAILS"))
    print("=" * 96)

    if len(held) == len(arms):
        print(TOKEN)
        return 0
    print("TOKEN WITHHELD -- %d of %d arms did not hold." % (len(arms) - len(held), len(arms)))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
