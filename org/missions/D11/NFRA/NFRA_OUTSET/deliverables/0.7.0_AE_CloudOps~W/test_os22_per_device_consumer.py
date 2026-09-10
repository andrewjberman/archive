"""O22-AC1 -- THE PER-DEVICE CONSUMER, read on a SERVED DAY.

Prints OS22-PER-DEVICE-CONSUMER only when every arm holds.

⛔ ONE ARM CANNOT PASS BEFORE 2026-09-11 13:00Z AND THE BATTERY SAYS SO RATHER THAN SKIPPING IT.
The DISCLOSURE arm (the CTO's ruling on S36, clause (v)) must read a per-device state out of the
SERVED bytes. That state lives in the stratum's DENOMINATOR, which reached no served artifact at
all until TO-OS-s-27 serialized it -- measured on four artifacts with a positive control (rows
S40, corrected by S41). OS-s-27 is TERMINAL and DEPLOYED, but its bound is explicit: no served
report is rewritten and nothing is backfilled, so the first artifact carrying the field is
tomorrow's scheduled fire. The arm is WRITTEN and RUN; it reports NOT-YET-SERVED against today's
artifact and FAILS the battery, because a criterion that cannot be read yet must not print a
token that says it passed.

NO AD-HOC RUN IS FIRED TO MANUFACTURE ONE. After 13:00Z today the runner's own schedule-mark rule
dates a report 2026-09-10, so a manual run now would REWRITE today's served keys -- which is the
act that produced the S34 rollback, and which TO-OS-s-27's own bound forbids. The wait is
qualified by that, not by convenience.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-22). 2026-09-10.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from datetime import datetime, timezone

BUCKET = "opal-estate-report"
CODE_KEY = "code/estate_report_runner.py"
SEAM_PREFIX = "s3://opal-estate-report/outset"

# The served day this grades: the first SCHEDULED fire carrying the per-device consumer.
REPORT_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
REPORT_VERSION = "kIo74Zug6entwLkwzLOw5TYMktp7RJ1R"

REAL_DEVICE = "laptop"
PROBE_DEVICE = "_os22_probe_device"
SILENT_DEVICE = "site-z"
CEILING_H = 26.0

# The single-key read this cell RETIRED, and the tokens that prove it, each with a control.
RETIRED_TOKEN = 'prefix.rstrip("/") + "/comp_heat_drift.json"'
PRESENT_TOKENS = ("OUTSET_DEVICES", "_outset_device_fields", "OUTSET_DRIFT_KEY", "OUT-OF-CORPUS")

DISCLOSURE_MARK = "NOT-PUBLISHED-OR-UNREADABLE"

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def note(msg):
    print("  .. %s" % msg)


def counts(den: str) -> dict:
    """The per-device state COUNTS out of the composition's headline, as numbers.

    ⛔ TWO WAYS THIS WENT WRONG BEFORE, BOTH RECORDED BECAUSE BOTH LOOKED FINE.
    (1) A `"QUIET" in denominator` test fired on the runner's OUT-OF-CORPUS explanation, which
        itself ends "(never read as QUIET)" -- a check that greps a producer's prose reads the
        PRODUCER, not the world.
    (2) A "first parenthesised group" regex latched onto `device(s)` in "N of M rostered
        device(s) reporting", and silently dropped the `quiet` count while returning the other
        three -- a PARTIAL parse that reads exactly like a complete one.

    So this matches the DECLARED STATE NAMES directly. The name list is the runner's own
    five-state enumeration; a state it emits that is missing here returns absent rather than zero,
    which the caller must not read as "none of those".
    """
    import re as _re
    states = ("quiet", "silent", "out-of-corpus", "NOT-PUBLISHED-OR-UNREADABLE")
    out = {}
    for s in states:
        m = _re.search(r"(\d+)\s+" + _re.escape(s), den)
        if m:
            out[s.lower()] = int(m.group(1))
    return out


def load_served_runner(s3, dest):
    r = s3.get_object(Bucket=BUCKET, Key=CODE_KEY)
    raw = r["Body"].read()
    with open(dest, "wb") as fh:
        fh.write(raw)
    os.environ.setdefault("ESTATE_REPORT_BUCKET", BUCKET)
    for k in ("ESTATE_GITHUB_SECRET_ID", "ESTATE_KIMI_SECRET_ID", "ESTATE_KIMI_MODEL"):
        os.environ.setdefault(k, "battery-placeholder")
    os.environ.setdefault("ESTATE_KIMI_URL", "http://placeholder.invalid")
    os.environ.setdefault("ESTATE_REPO_URL", "http://placeholder.invalid")
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    spec = importlib.util.spec_from_file_location("os22_served", dest)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, raw, r["VersionId"]


def served_report(s3):
    body = s3.get_object(Bucket=BUCKET, Key=REPORT_KEY, VersionId=REPORT_VERSION)["Body"].read()
    return json.loads(body.decode("utf-8")), body.decode("utf-8", errors="replace")


def device_citation(doc):
    for p in ((doc.get("ai") or {}).get("proposals") or []):
        c = p.get("tool_row_cited")
        if isinstance(c, str) and "A_propagation@" in c:
            return c
    return ""


# --------------------------------------------------------------------------- (a)
def arm_a(doc):
    print("\n(a) EACH REPORTING DEVICE BY NAME, WITH ITS OWN VINTAGE, ON THE SERVED BYTES")
    cit = device_citation(doc)
    if not cit:
        fail("a", "no served citation names A_propagation@, so no per-device composition is "
                  "visible in the artifact")
        return None
    print("      %s" % cit[:300])
    parts = [p.strip() for p in cit.split("|")]
    print("      DENOMINATOR: %d device segment(s) in the composition" % len(parts))
    named = {}
    for seg in parts:
        for dev in (REAL_DEVICE, SILENT_DEVICE, PROBE_DEVICE):
            if seg.startswith("A_propagation@%s" % dev) or seg.startswith("%s:" % dev):
                named[dev] = seg
    for dev in (REAL_DEVICE, SILENT_DEVICE, PROBE_DEVICE):
        print("        %-22s %s" % (dev, named.get(dev, "*** NOT NAMED ***")))
    missing = [d for d in (REAL_DEVICE, SILENT_DEVICE, PROBE_DEVICE) if d not in named]
    if missing:
        fail("a", "%d rostered device(s) are not named in the served composition: %s"
             % (len(missing), missing))
        return None
    if "produced" not in named[REAL_DEVICE]:
        fail("a", "the reporting device carries no vintage in the served composition")
        return None
    ok("all 3 rostered devices are named BY NAME in the served bytes, and the reporting one "
       "carries its own vintage")
    return named


# --------------------------------------------------------------------------- (b)
def arm_b(named):
    print("\n(b) A DEVICE PAST ITS CEILING READS FAILED WHILE THE OTHERS RENDER")
    if not named:
        fail("b", "no composition from arm (a)")
        return
    silent = named[SILENT_DEVICE]
    real = named[REAL_DEVICE]
    print("      silent device : %s" % silent[:160])
    print("      reporting one : %s" % real[:160])
    if "UNREAD" not in silent.upper() and "SILENT" not in silent.upper():
        fail("b", "the non-reporting device does not read UNREAD/SILENT: %r" % silent[:120])
        return
    if "produced" not in real:
        fail("b", "the reporting device did not render beside the silent one")
        return
    ok("one device reads UNREAD/SILENT while another renders its own vintage in the same "
       "composition -- silence is PER DEVICE and does not blank the group")


# --------------------------------------------------------------------------- (c)
def arm_c(mod, named):
    print("\n(c) THE PLANTED SECOND DEVICE IS A SECOND ROW AND NEVER MERGES INTO THE FIRST'S n")
    if not named:
        fail("c", "no composition from arm (a)")
        return
    if PROBE_DEVICE not in named or "produced" not in named[PROBE_DEVICE]:
        fail("c", "the probe fixture does not render as its own row in the served bytes")
        return
    ok("the probe fixture renders as a SECOND row with its own vintage: %s"
       % named[PROBE_DEVICE][:120])

    # THE ARITHMETIC CLAIM, exercised on the SERVED function rather than argued: two devices with
    # known counts must produce TWO per-device figures and never one summed figure.
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    def doc_for(dev, n, tracked):
        # `answer_state` is NOT optional. _outset_read maps it through the seam's DECLARED
        # DOMAIN, and a fixture omitting it reads SILENT -- so the arm would never reach the
        # per-device arithmetic it exists to test and would fail for the wrong reason. A fixture
        # that cannot represent the case cannot score it.
        return json.dumps({"seam": mod.SEAM_TAG, "answer_state": "OK",
                           "vintage": {"answer_produced_utc": stamp},
                           "device": dev, "n": n, "n_modified": n, "n_untracked": 0,
                           "tracked_total": tracked, "git_head": "deadbeef", "rows": []})

    def loader(src):
        if "/alpha/" in src:
            return doc_for("alpha", 7, 100)
        if "/beta/" in src:
            return doc_for("beta", 11, 200)
        raise FileNotFoundError(src)

    st = mod._stratum_propagation("PIN", prefix=SEAM_PREFIX, loader=loader, now=now,
                                  devices=("alpha", "beta"))
    den = st["denominator"]
    print("      two planted devices, n=7 over 100 and n=11 over 200")
    print("      denominator: %s" % den[:320])
    has_7 = "n=7" in den
    has_11 = "n=11" in den
    summed = "n=18" in den
    print("      n=7 present: %s   n=11 present: %s   n=18 (SUMMED) present: %s  <- must be False"
          % (has_7, has_11, summed))
    if summed:
        fail("c", "the composition SUMMED two devices into one n -- the quantity no tree has")
        return
    if not (has_7 and has_11):
        fail("c", "the two devices' counts do not both appear per-device (7=%s, 11=%s)"
             % (has_7, has_11))
        return
    ok("both device counts appear SEPARATELY and their sum appears nowhere -- per device, never "
       "summed")


# --------------------------------------------------------------------------- (d)
def arm_d(served_bytes, s3):
    print("\n(d) THE SINGLE-KEY READ IS RETIRED, PROVEN IN THE SERVED RUNNER, TOKEN BY TOKEN")
    now = s3.get_object(Bucket=BUCKET, Key=CODE_KEY)["Body"].read().decode("utf-8",
                                                                          errors="replace")
    vs = sorted([v for v in s3.list_object_versions(Bucket=BUCKET,
                                                    Prefix=CODE_KEY).get("Versions", [])
                 if v["Key"] == CODE_KEY], key=lambda x: x["LastModified"])
    # THE CONTROL VERSION is the runner as it stood BEFORE this cell's deploy, so every token has
    # a PRIOR count that proves the detector can fire. W1-S27: a census of N tokens is N detectors,
    # and a token reading 0 on both sides discriminates nothing.
    pre = None
    for v in vs:
        if v["LastModified"].astimezone(timezone.utc) < datetime(2026, 9, 9, 15, 58,
                                                                 tzinfo=timezone.utc):
            pre = v
    if pre is None:
        fail("d", "no pre-deploy version of the runner to use as the token control")
        return
    old = s3.get_object(Bucket=BUCKET, Key=CODE_KEY,
                        VersionId=pre["VersionId"])["Body"].read().decode("utf-8",
                                                                          errors="replace")
    print("      control version %s (%s), %d B" % (pre["VersionId"][:16] + "..",
                                                   pre["LastModified"].astimezone(timezone.utc)
                                                   .strftime("%Y-%m-%dT%H:%M:%SZ"), len(old)))
    print("      DENOMINATOR: %d token(s), each with a prior count" % (1 + len(PRESENT_TOKENS)))
    a, b = old.count(RETIRED_TOKEN), now.count(RETIRED_TOKEN)
    print("        %-46s prior=%d now=%d  %s" % (RETIRED_TOKEN[:44], a, b,
                                                 "RETIRED" if a > 0 and b == 0 else "***"))
    if a == 0:
        fail("d", "the retired token read 0 BEFORE as well, so its detector never fired and the "
                  "retirement is not measured (W1-S27)")
        return
    if b != 0:
        fail("d", "the single-key read is STILL present in the served runner (%d occurrence(s))" % b)
        return
    for t in PRESENT_TOKENS:
        pa, pb = old.count(t), now.count(t)
        print("        %-46s prior=%d now=%d  %s" % (t, pa, pb, "ADDED" if pa == 0 and pb else ""))
        if pb == 0:
            fail("d", "%r is absent from the served runner, so the per-device composition it "
                      "belongs to is not there" % t)
            return
    ok("the single-key read is RETIRED in the served bytes (prior=%d -> now=0, so the detector "
       "was able to fire) and %d per-device tokens are present" % (a, len(PRESENT_TOKENS)))


# --------------------------------------------------------------------------- (e)
def arm_e(doc, served_text):
    print("\n(e) THE DISCLOSURE ARM (the CTO's ruling on S36, clause (v))")
    groups = (doc.get("ai") or {}).get("groups") or {}
    a = groups.get("A") or {}
    has_field = "stratum_denominator" in a
    print("      ai.groups.A keys on THIS served artifact: %s" % sorted(a.keys()))
    print("      carries stratum_denominator: %s" % has_field)
    if not has_field:
        fail("e", "NOT-YET-SERVED. The disclosure state lives in the stratum DENOMINATOR, which "
                  "reached no served artifact until TO-OS-s-27 serialized it (rows S40/S41). "
                  "OS-s-27 is TERMINAL and DEPLOYED, but its own bound forbids rewriting a served "
                  "report, so the FIRST artifact carrying this field is the 2026-09-11 13:00Z "
                  "fire. This arm is written and cannot be read today; no ad-hoc run is fired to "
                  "manufacture one, because after 13:00Z a manual run rewrites TODAY's served "
                  "keys -- the act that produced the S34 rollback.")
        note("what CAN be said today, and it is not the accept: the served bytes contain "
             "'AccessDenied' %d time(s), against 3 on the manual served day -- so the FALSEHOOD is "
             "gone even though the DISCLOSURE is not yet readable."
             % served_text.count("AccessDenied"))
        return
    den = a.get("stratum_denominator") or ""
    seg = [s for s in den.split(";") if SILENT_DEVICE in s]
    print("      site-z segment, verbatim: %s" % (seg[0].strip()[:400] if seg else "(none)"))
    if not seg:
        fail("e", "the serialized denominator names no %s segment" % SILENT_DEVICE)
        return
    if DISCLOSURE_MARK not in seg[0]:
        fail("e", "the site-z state does not carry %r" % DISCLOSURE_MARK)
        return
    real_seg = [s for s in den.split(";") if REAL_DEVICE in s and SILENT_DEVICE not in s]
    if any(DISCLOSURE_MARK in s for s in real_seg):
        fail("e", "the disclosure wording ALSO appears for a device that published -- it decorates "
                  "every row instead of discriminating")
        return
    ok("the disclosure state is read out of the SERVED bytes for %s and does NOT appear for %s, "
       "so it discriminates" % (SILENT_DEVICE, REAL_DEVICE))


# --------------------------------------------------------------------------- (f)
def arm_f(mod, served_bytes):
    print("\n(f) THE NEGATIVE ARMS")
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    def make(dev, n, tracked, drop_device=False):
        d = {"seam": mod.SEAM_TAG, "answer_state": "OK",
             "vintage": {"answer_produced_utc": stamp},
             "n": n, "n_modified": n, "n_untracked": 0, "tracked_total": tracked,
             "git_head": "deadbeef", "rows": []}
        if not drop_device:
            d["device"] = dev
        return json.dumps(d)

    # (f1) tracked_total 0 -> OUT-OF-CORPUS, never QUIET.
    st = mod._stratum_propagation("PIN", prefix=SEAM_PREFIX,
                                  loader=lambda s: make("alpha", 0, 0), now=now,
                                  devices=("alpha",))
    d1 = st["denominator"]
    # ⛔ READ THE HEADLINE COUNTS, NOT THE PROSE. A `"QUIET" in denominator` test looked right and
    # was wrong: the runner's OUT-OF-CORPUS explanation itself ends "(never read as QUIET)", so the
    # check fired on the very sentence that says the device is NOT quiet. A check that greps a
    # producer's prose reads the PRODUCER, not the world. The headline carries the counts as
    # numbers and that is what the arm asserts.
    n1 = counts(d1)
    print("      tracked_total=0 -> counts %s" % n1)
    if n1.get("out-of-corpus") != 1 or n1.get("quiet") != 0:
        fail("f", "an artifact with tracked_total 0 did not render OUT-OF-CORPUS (or rendered "
                  "QUIET): counts %s" % n1)
        return
    # (f2) no `device` field -> OUT-OF-CORPUS.
    st = mod._stratum_propagation("PIN", prefix=SEAM_PREFIX,
                                  loader=lambda s: make("alpha", 3, 50, drop_device=True),
                                  now=now, devices=("alpha",))
    d2 = st["denominator"]
    n2 = counts(d2)
    print("      no `device` field -> counts %s" % n2)
    if n2.get("out-of-corpus") != 1:
        fail("f", "an artifact with no `device` field did not render OUT-OF-CORPUS: counts %s" % n2)
        return
    # THE POSITIVE CONTROL of the same two arms: a WELL-FORMED artifact must NOT read
    # OUT-OF-CORPUS, or the state is a constant.
    st = mod._stratum_propagation("PIN", prefix=SEAM_PREFIX,
                                  loader=lambda s: make("alpha", 3, 50), now=now,
                                  devices=("alpha",))
    d3 = st["denominator"]
    n3 = counts(d3)
    print("      well-formed artifact -> counts %s  (the positive control)" % n3)
    if n3.get("out-of-corpus", 0) != 0:
        fail("f", "a WELL-FORMED artifact ALSO reads OUT-OF-CORPUS -- the state is a constant and "
                  "neither negative arm above is a measurement: counts %s" % n3)
        return
    ok("tracked_total 0 and a missing `device` field both read OUT-OF-CORPUS and never QUIET, "
       "while a well-formed artifact does not -- so the state discriminates")

    # (f3) THE PLANTED MUTANT, in a COPY of the runner, ANCHOR UNIQUENESS ASSERTED FIRST.
    src = served_bytes.decode("utf-8", errors="replace")
    anchor = '(quiet if f["n"] == 0 else reporting).append(dev)'
    count = src.count(anchor)
    print("      mutant anchor occurrences in the served runner: %d  <- must be exactly 1" % count)
    if count != 1:
        fail("f", "the mutant anchor is not unique (%d occurrences), so a planted mutant would "
                  "land somewhere unintended" % count)
        return
    mutated = src.replace(
        anchor,
        anchor + '\n        f["n"] = f["n"] + sum(1 for _ in range(0))  # planted: identity\n'
                 '        _os22_planted_total = locals().get("_os22_planted_total", 0) + f["n"]\n'
                 '        f["n"] = _os22_planted_total  # planted MUTANT: sums devices into one n',
        1)
    here = os.path.dirname(os.path.abspath(__file__))
    mpath = os.path.join(here, ".os22_mutant_runner.py")
    with open(mpath, "w", encoding="utf-8") as fh:
        fh.write(mutated)
    try:
        spec = importlib.util.spec_from_file_location("os22_mutant", mpath)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)

        def loader2(src_):
            if "/alpha/" in src_:
                return make("alpha", 7, 100)
            if "/beta/" in src_:
                return make("beta", 11, 200)
            raise FileNotFoundError(src_)
        stm = mm._stratum_propagation("PIN", prefix=SEAM_PREFIX, loader=loader2, now=now,
                                      devices=("alpha", "beta"))
        dm = stm["denominator"]
        summed = "n=18" in dm
        print("      MUTANT composition: n=18 (summed) present: %s  <- must be True for the "
              "detector to be proven" % summed)
        if not summed:
            fail("f", "the planted summing mutant did NOT produce a summed n, so arm (c)'s check "
                      "is not proven able to catch one")
            return
        ok("the planted mutant DOES sum two devices into one n, and arm (c)'s assertion is exactly "
           "what refuses it -- the detector is proven able to fire")
    finally:
        try:
            os.remove(mpath)
        except OSError:
            pass


def main():
    print("=" * 78)
    print("O22-AC1 -- THE PER-DEVICE CONSUMER, ON A SERVED DAY")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s)." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(here, ".served_runner_os22.py")
    try:
        mod, raw, vid = load_served_runner(s3, dest)
    except Exception as exc:                                                # noqa: BLE001
        print("BLOCKED: could not load the SERVED runner (%s: %s)" % (type(exc).__name__, exc))
        return 1
    print("served runner %s @%s (%d B)" % (CODE_KEY, vid[:12], len(raw)))
    doc, text = served_report(s3)
    print("served report %s @%s.. (%d B)" % (REPORT_KEY, REPORT_VERSION[:12], len(text)))

    named = arm_a(doc)
    arm_b(named)
    arm_c(mod, named)
    arm_d(raw, s3)
    arm_e(doc, text)
    arm_f(mod, raw)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS22-PER-DEVICE-CONSUMER")
    return 0


if __name__ == "__main__":
    sys.exit(main())
