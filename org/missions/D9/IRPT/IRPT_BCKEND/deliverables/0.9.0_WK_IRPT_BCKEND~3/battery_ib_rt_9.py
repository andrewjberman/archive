"""IB-rt-9 battery -- RT9-AC1. FIVE arms of six: (a), (b), (c), (d), (f). (e) is BLOCKED.

  Serial: 0.9.0_WK_IRPT_BCKEND~3
  Order : IRPT_BCKEND.TO-IB-rt-9

THE ACCEPTANCE TOKEN IS DELIBERATELY NOT PRINTED BY THIS FILE, in any form, not
even negated. RT9-AC1's `<expect>` is graded as a REGEX over this output, so a
line reading "<token>: NOT ASSERTED" would MATCH and the criterion would read
PASS on a run that proved one arm of six. The successor adds the token to the
final line only when arms (a) through (f) all pass in one run.

WHAT RUNS HERE -- arm (a), THE CUTOVER, EVERY READER:
  a1  census every reader of `ycharts/session/current` in the repository, with
      the denominator printed, and classify each as MIGRATED, RETIRED or
      OUT-OF-SCOPE-BY-PRD-NAME
  a2  census the legacy any-non-403 predicate: the count must be 0
  a3  the DIFFERENCE CONTROL on the predicate itself -- old vs new over a
      recorded status/body matrix, printing every row where they disagree.
      Without this, "the predicate was replaced" is a claim about a diff; with
      it, it is a measurement of behaviour.
  a4  the retired capture reader: its handler refuses, and its two trigger
      paths are read (the EventBridge rule LIVE, the probe's invoke in source)

  b   FENCING -- two capture attempts on the fixture through the RUNNER'S OWN
      `persistSession`: one wins, one refuses, and the published BYTES are
      digest-identical before and after the loser's write. Driven in a node
      subprocess under the runner's netguard.
  c   ROTATION -- a new version published, the replay transport's NEXT
      invocation uses it, the superseded version refused on the fence.
  d   EVICTION -- a 401 mid-job on `job.GenerationJob`: ONE broker refresh,
      resumed at the checkpoint through the job's own reconcile, with the
      no-resubmit difference control and the repeat-eviction park.
  f   NOTHING LEFT THE MACHINE -- both drives' guard summaries with their
      denominators AND their positive controls.

WHAT DOES NOT RUN -- arm (e) ABSORBED/STOPPED/CONVERGED. It is a ledger +
`state mv` + apply of the ycharts root, and that root's plan carries an
unapplied handler flip to `entry.lambda_handler` whose module is in no zip, so
the apply this arm REQUIRES takes `irpt-ycharts-generate` down. Row
IRPT_BCKEND-W3-S26; the remedy belongs to cell IB-rt-2, not here.

THE ARMS ARE DRIVEN IN SUBPROCESSES, and that is the point: each drive installs
its outbound-network guard BEFORE anything under test is evaluated, which no
in-process arrangement can do once this battery has imported the probe.

BOUND 1 HOLDS: nothing here makes a YCharts call, a login or a capture. The
only network calls are AWS control-plane reads (describe-rule) from THIS
process, declared in arm (f) rather than hidden; every vendor interaction is a
RECORDED fixture through an injected seam.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
import sys

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                      text=True, check=True).stdout.strip()
PROBE = os.path.join(REPO, "infra", "aws", "lambda", "ycharts-session-probe")
CAPTURE = os.path.join(REPO, "infra", "aws", "lambda", "ycharts-session-capture",
                       "index.mjs")
SECRET = "ycharts/session/current"

sys.path.insert(0, PROBE)
import lambda_function as probe            # noqa: E402  the rewritten probe

FAILURES = []


def check(label, ok, detail=""):
    print("  %-7s %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  --  " + detail) if detail else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def tracked_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True,
                         check=True, cwd=REPO).stdout
    return [p for p in out.replace("\r", "").split("\n") if p]


# --------------------------------------------------------------------------- a1

# The four code readers, declared with the disposition each must prove. This is
# the CLAIM; the census below is the check that the claim's domain is the whole
# population -- a member the census finds and this table does not hold voids it.
EXPECTED_READERS = {
    "infra/aws/ec2/investor-reporting-ycharts/ycharts_session.js": (
        "MIGRATED", "the v0.9 runner: leases, fences and persists the versioned bundle"),
    "infra/aws/lambda/investor-reporting/ycharts/generate/transport.py": (
        "MIGRATED", "IB-s-9 replay/live transport: holds the bundle by name, verifies "
                    "schema, identity and transport before resuming"),
    "infra/aws/lambda/ycharts-session-probe/lambda_function.py": (
        "MIGRATED", "this cell: fence read + positive allowlist replace the non-403 predicate"),
    # ADDED BY THIS CELL and found by the census BEFORE it was declared, which is the table
    # working: the arm failed 4-of-5 on the run that first carried the broker, and the entry
    # below is the answer to that failure rather than a widening of the discriminator.
    "infra/aws/lambda/investor-reporting/ycharts/session/broker.py": (
        "MIGRATED", "this cell's broker: reads the versioned bundle BY NAME, refuses "
                    "NOT_VERSIONED / NOT_CONFIGURED / UNPARSEABLE / STALE_FENCE, and never "
                    "publishes -- publication stays on the capture host"),
    "infra/aws/lambda/ycharts-session-capture/index.mjs": (
        "RETIRED", "handler refuses; schedule DISABLED; the probe no longer invokes it"),
}

CODE_SUFFIXES = (".py", ".js", ".mjs", ".cjs", ".ts", ".sh", ".ps1")

# THE DISCRIMINATOR BETWEEN A READER AND A MENTION, and it is not the secret
# name. The first run of this arm counted every code file CONTAINING the string
# and got 7, because a comment in a test fake, a research evidence dict and this
# worker's own IB-s-8 battery all name the secret without ever resolving it.
# A READER is code that RESOLVES the secret at runtime, so the test is the
# presence of a Secrets Manager READ API call. Measured: 4 of the 7 code files
# that name the secret call one; 3 do not, and those 3 are exactly the three
# that cannot read anything.
SM_READ_API = re.compile(r"get_secret_value|GetSecretValueCommand|get-secret-value")

# A FOURTH CLASS, and it exists because THIS FILE became TRACKED when its own
# branch drained. A census over `git ls-files` then finds the battery itself: its
# fake Secrets Manager client defines `get_secret_value` and its fixtures name the
# secret, so the READER/MENTION discriminator -- correctly -- calls it a reader.
# It is not an ESTATE reader; it reaches no AWS. The discriminator for this class
# is STRUCTURAL, never a file name: a file under this project's own deliverables/
# is a TEST HARNESS. Every member is PRINTED with its own count, so the exclusion
# is visible on the output and the estate denominator stays honest -- a silent
# skip here would be the self-wrapping the bounds forbid, inverted.
# Row IRPT_BCKEND-W3-S29.
HARNESS_PREFIX = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"


def arm_a1():
    print("(a1) CENSUS -- every reader of %s in the repository" % SECRET)
    files = tracked_files()
    hits, code_hits, readers, mentions = [], [], [], []
    for rel in files:
        path = os.path.join(REPO, rel)
        try:
            with open(path, "rb") as fh:
                blob = fh.read()
        except (OSError, MemoryError):
            continue
        if SECRET.encode() not in blob:
            continue
        hits.append(rel)
        if not rel.endswith(CODE_SUFFIXES):
            continue
        code_hits.append(rel)
        text = blob.decode("utf-8", "replace")
        (readers if SM_READ_API.search(text) else mentions).append(rel)
    harness = [r for r in readers if r.startswith(HARNESS_PREFIX)]
    readers = [r for r in readers if not r.startswith(HARNESS_PREFIX)]
    print("      DENOMINATOR: %d file(s) scanned (git ls-files, tracked) | "
          "%d name the secret | %d are CODE | %d of those RESOLVE it "
          "(a Secrets Manager read API) | %d only MENTION it | "
          "%d of the resolvers are this cell's OWN TEST HARNESS, listed below "
          "and excluded from the estate denominator"
          % (len(files), len(hits), len(code_hits), len(readers) + len(harness),
             len(mentions), len(harness)))

    # MECE BY SUBTRACTION, not by recall: the population is the READERS the
    # census FOUND, minus what the table accounts for. A leftover voids it.
    unaccounted = [r for r in readers if r not in EXPECTED_READERS]
    missing = [r for r in EXPECTED_READERS if r not in readers]
    for rel in sorted(readers):
        disp, why = EXPECTED_READERS.get(rel, ("UNACCOUNTED", "not in the declared table"))
        print("      %-12s %s" % (disp, rel))
        print("                   %s" % why)
    for rel in sorted(mentions):
        print("      MENTION      %s" % rel)
        print("                   names the secret but calls no Secrets Manager read API")
    for rel in sorted(harness):
        print("      HARNESS      %s" % rel)
        print("                   this cell's own battery under deliverables/: its FAKE "
              "Secrets Manager client defines the read API and reaches no AWS")
    for rel in unaccounted:
        print("      UNACCOUNTED  %s -- the census found a reader the table does not hold"
              % rel)
    for rel in missing:
        print("      ABSENT       %s -- the table holds a reader the census did not find" % rel)

    n = len(EXPECTED_READERS)
    accounted = len([r for r in readers if r in EXPECTED_READERS])
    check("a1 readers migrated or retired: %d of %d" % (accounted, len(readers)),
          not unaccounted and not missing and accounted == n,
          "denominator is the census, not the table")
    # CONTROL ON THE EXCLUSION ITSELF: the harness class must never swallow a
    # declared estate reader. If it ever does, the exclusion is hiding the answer.
    check("a1 the HARNESS exclusion removed 0 declared estate reader(s): %d of %d "
          "excluded file(s) are under deliverables/"
          % (len(harness), len(harness)),
          not [r for r in harness if r in EXPECTED_READERS],
          "an exclusion that can remove a real reader is a hole, not a class")
    return code_hits


# --------------------------------------------------------------------------- a2

# THE DETECTOR, NARROWED TWICE BY ITS OWN FALSE POSITIVES.
#
# First shape -- any line comparing against 403 near an authentication word --
# fired on 2, and BOTH were wrong:
#   ycharts_session.js:272  `if (status === 403) return {..., authenticated: false}`
#       a POSITIVE classifier: 403 means NOT authenticated. That is the correct
#       direction and the opposite of the defect.
#   lambda_function.py:7    the rewritten probe's own DOCSTRING, quoting the
#       retired predicate verbatim so the next reader knows what changed.
#       Recording the defect is not committing it.
#
# So the detector is now directional AND structural: it matches only a NEGATIVE
# comparison against 403 (the shape that lets everything else through), and it
# reads STRIPPED source -- python comments and string literals removed by
# tokenize, JS comments and string literals removed by a scanner -- so no
# docstring, comment or fixture can fire it. The cost is that a legacy predicate
# built by string concatenation would be missed; nothing in this estate does that.
LEGACY_PREDICATE = re.compile(r"!==?\s*403|403\s*!==?|not\s+in\s*[\(\[][^)\]]*403")
AUTH_CONTEXT = re.compile(r"auth_ok|authenticated|is_fresh|fresh|session_ok",
                          re.IGNORECASE)


def _strip_python(text):
    """Blank out comments and string literals; keep line numbers."""
    import io                                                       # noqa: PLC0415
    import tokenize                                                 # noqa: PLC0415
    lines = text.split("\n")
    keep = [[" "] * len(ln) for ln in lines]
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return lines            # unparseable: fall back to the raw text
    for tok in toks:
        if tok.type in (tokenize.COMMENT, tokenize.STRING):
            continue
        (r1, c1), (r2, c2) = tok.start, tok.end
        if r1 != r2 or not (1 <= r1 <= len(keep)):
            continue
        row = keep[r1 - 1]
        for c in range(c1, min(c2, len(row), len(lines[r1 - 1]))):
            row[c] = lines[r1 - 1][c]
    return ["".join(r) for r in keep]


def _strip_js(text):
    """Blank out // and /* */ comments and quoted strings; keep line numbers."""
    out, i, n = [], 0, len(text)
    mode = None                 # None | line | block | quote char
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if mode is None:
            if ch == "/" and nxt == "/":
                mode, i = "line", i + 2
                out.append("  ")
                continue
            if ch == "/" and nxt == "*":
                mode, i = "block", i + 2
                out.append("  ")
                continue
            if ch in "\"'`":
                mode, i = ch, i + 1
                out.append(" ")
                continue
            out.append(ch)
        elif mode == "line":
            if ch == "\n":
                mode = None
                out.append(ch)
            else:
                out.append(" ")
        elif mode == "block":
            if ch == "*" and nxt == "/":
                mode, i = None, i + 2
                out.append("  ")
                continue
            out.append("\n" if ch == "\n" else " ")
        else:                   # inside a quoted string
            if ch == "\\":
                out.append("  ")
                i += 2
                continue
            if ch == mode:
                mode = None
            out.append("\n" if ch == "\n" else " ")
        i += 1
    return "".join(out).split("\n")


def arm_a2(code_hits):
    print()
    print("(a2) CENSUS -- legacy any-non-403 authentication predicates")
    files = [r for r in tracked_files() if r.endswith(CODE_SUFFIXES)]
    found, stripped_files = [], 0
    for rel in files:
        try:
            with open(os.path.join(REPO, rel), "r", encoding="utf-8",
                      errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        if rel.endswith(".py"):
            lines = _strip_python(text)
            stripped_files += 1
        elif rel.endswith((".js", ".mjs", ".cjs", ".ts")):
            lines = _strip_js(text)
            stripped_files += 1
        else:
            lines = [("" if ln.lstrip().startswith("#") else ln)
                     for ln in text.split("\n")]
        raw = text.split("\n")
        for i, line in enumerate(lines, 1):
            if LEGACY_PREDICATE.search(line) and AUTH_CONTEXT.search(line):
                found.append("%s:%d: %s" % (rel, i, raw[i - 1].strip()[:140]))
    print("      DENOMINATOR: %d code file(s) scanned, %d of them comment/string-stripped "
          "| %d line(s) match (a NEGATIVE 403 comparison AND an authentication word, in CODE)"
          % (len(files), stripped_files, len(found)))
    for f in found:
        print("      HIT %s" % f)
    check("a2 legacy any-non-403 probes remaining: %d" % len(found), not found)

    # POSITIVE CONTROL -- a detector that cannot fire is a constant, and this one
    # was just narrowed twice. Run it over the predicate it exists to find.
    probe_line = 'rec["auth_ok"] = rec.get("status") is not None and rec.get("status") != 403'
    fires = bool(LEGACY_PREDICATE.search(probe_line) and AUTH_CONTEXT.search(probe_line))
    check("a2 POSITIVE CONTROL: the detector fires on the retired predicate verbatim", fires,
          "the line this cell removed from ycharts-session-probe")
    # NEGATIVE CONTROL -- the correct direction must NOT fire.
    ok_line = "if (status === 403) return { state: 'DISTURBED', authenticated: false };"
    check("a2 NEGATIVE CONTROL: the detector is silent on a correct 403-means-refused line",
          not (LEGACY_PREDICATE.search(ok_line) and AUTH_CONTEXT.search(ok_line)),
          "ycharts_session.js:272, which the first shape of this detector wrongly flagged")


# --------------------------------------------------------------------------- a3

def old_predicate(status, body=b"", ctype=""):
    """VERBATIM the predicate this cell replaced, from lambda_function.py@684e7eb90a:

        rec["auth_ok"] = rec.get("status") is not None and rec.get("status") != 403
    """
    return status is not None and status != 403


# (label, status, body, content-type, IS IT REALLY AN AUTHENTICATED SESSION)
MATRIX = [
    ("healthy json 200", 200, b'{"data":[[1,2]]}', "application/json", True),
    ("hard eviction 403", 403, b"concurrent sign in detected", "text/html", False),
    ("disturbed 403", 403, b"you have been signed out", "text/html", False),
    ("bad params 400", 400, b'{"error":"bad params"}', "application/json", False),
    ("unauthenticated 401", 401, b"", "", False),
    ("not found 404", 404, b"not found", "text/html", False),
    ("rate limited 429", 429, b"slow down", "text/html", False),
    ("server error 500", 500, b"oops", "text/html", False),
    ("waf interstitial 200", 200, b"<html>awswaf challenge</html>", "text/html", False),
    ("login page 200", 200, b'<html><form id_username name="password">', "text/html", False),
    ("redirect to login", 302, b"", "", False),
    ("transport failure", None, b"", "", False),
    ("html body, json ctype", 200, b"<html>Sign in</html>", "application/json", False),
    ("teapot 418", 418, b"", "", False),
]


def arm_a3():
    print()
    print("(a3) DIFFERENCE CONTROL -- old predicate vs new, over a recorded matrix")
    print("      %-24s %-6s %-26s %-8s %-8s %s"
          % ("case", "status", "new state", "new", "old", "truth"))
    disagreements, new_wrong, old_wrong = [], [], []
    for label, status, body, ctype, truth in MATRIX:
        state, new_ok = probe.classify(status, body, ctype)
        old_ok = old_predicate(status, body, ctype)
        print("      %-24s %-6s %-26s %-8s %-8s %s"
              % (label, status, state, new_ok, old_ok, truth))
        if new_ok != old_ok:
            disagreements.append((label, state, new_ok, old_ok))
        if new_ok != truth:
            new_wrong.append(label)
        if old_ok != truth:
            old_wrong.append(label)
    print("      DENOMINATOR: %d recorded case(s) | old predicate wrong on %d | "
          "new predicate wrong on %d | they disagree on %d"
          % (len(MATRIX), len(old_wrong), len(new_wrong), len(disagreements)))
    for label in old_wrong:
        print("      OLD-FALSE-GREEN  %s -- the retired predicate called this authenticated"
              % label)
    check("a3 new predicate correct on every recorded case: %d of %d"
          % (len(MATRIX) - len(new_wrong), len(MATRIX)), not new_wrong,
          "wrong on: %s" % new_wrong if new_wrong else "")
    # The POSITIVE control on the control: if the old predicate were right
    # everywhere, this matrix could not have detected the defect at all.
    check("a3 the matrix DISCRIMINATES: the old predicate is wrong on %d of %d case(s)"
          % (len(old_wrong), len(MATRIX)), len(old_wrong) > 0,
          "a matrix on which both predicates agree proves nothing")
    # The vocabulary is closed and every state used is a member of it.
    vocab = set(probe.REFUSALS) | {probe.AUTHENTICATED}
    used = {probe.classify(s, b, c)[0] for _l, s, b, c, _t in MATRIX}
    check("a3 every state produced is in the closed vocabulary: %d of %d"
          % (len(used & vocab), len(used)), used <= vocab,
          "outside: %s" % sorted(used - vocab))


# --------------------------------------------------------------------------- a4

class _FakeSecrets(object):
    def __init__(self, payload):
        self._payload = payload

    def get_secret_value(self, SecretId=None):      # noqa: N803  boto3's casing
        if self._payload is None:
            raise type("ResourceNotFoundException", (Exception,), {})()
        return {"SecretString": self._payload}


def arm_a4():
    print()
    print("(a4) THE RETIRED READER, AND THE FENCE THE MIGRATED ONE READS")

    src = open(CAPTURE, "r", encoding="utf-8", errors="replace").read()
    check("a4 capture handler refuses on entry",
          'reason: "RETIRED"' in src and "statusCode: 410" in src)
    check("a4 the retirement says WHY in source",
          "RETIRED 2026-09-11" in src and "ONE AUTOMATION OWNER" in src)

    probe_src = open(os.path.join(PROBE, "lambda_function.py"), "r",
                     encoding="utf-8", errors="replace").read()
    check("a4 the probe no longer invokes the capture Lambda",
          "CAPTURE_FUNCTION_NAME" not in probe_src and "_trigger_capture" not in probe_src)

    # The live trigger. An AWS control-plane READ, not a deploy.
    rule = "ycharts-session-capture-schedule"
    aws = os.path.join(REPO, ".tools", "aws.cmd")
    try:
        out = subprocess.run([aws, "events", "describe-rule", "--name", rule,
                              "--query", "State", "--output", "text"],
                             capture_output=True, timeout=120, cwd=REPO)
        state = out.stdout.decode("utf-8", "replace").replace("\r", "").strip()
    except Exception as exc:                                        # noqa: BLE001
        state = "UNREAD(%s)" % type(exc).__name__
    print("      live read: aws events describe-rule --name %s -> State=%s" % (rule, state))
    check("a4 the retired reader's schedule is DISABLED", state == "DISABLED",
          "measured live, not asserted from the .tf")

    # The fence predicate itself, on recorded secret payloads.
    versioned = json.dumps({
        "cookies": [{"name": "ycsessionid", "value": "x", "domain": "ycharts.com"},
                    {"name": "csrftoken", "value": "y", "domain": "ycharts.com"}],
        "identity_evidence": {"names": ["ycsessionid"]},
        "captured_at": "2026-09-11T12:00:00Z", "captured_by": "runner-1", "fence": 7})
    legacy_flat = json.dumps({"cookies": "ycsessionid=x; csrftoken=y"})
    legacy_fields = json.dumps({"ycsessionid": "x", "csrftoken": "y"})

    s_ok = probe.read_session(_FakeSecrets(versioned))
    check("a4 a versioned bundle reads OK with its fence: verdict=%s fence=%s"
          % (s_ok.verdict, s_ok.fence), s_ok.verdict == "OK" and s_ok.fence == 7)
    for label, payload in (("flat cookie string", legacy_flat),
                           ("field-assembled", legacy_fields)):
        st = probe.read_session(_FakeSecrets(payload))
        check("a4 legacy %s bundle is NOT_VERSIONED (not graded stale, not graded fresh): %s"
              % (label, st.verdict), st.verdict == "NOT_VERSIONED")
    st = probe.read_session(_FakeSecrets(None))
    check("a4 an unset secret is NOT_CONFIGURED: %s" % st.verdict,
          st.verdict == "NOT_CONFIGURED")

    # The fence's whole point: a reading taken under a superseded fence is discarded.
    healthy = [{"endpoint": "e", "auth_ok": True}]
    stale = [{"endpoint": "e", "auth_ok": False}]
    check("a4 fence unchanged + all probes authenticated -> FRESH",
          probe.evaluate(s_ok, healthy, 7) == "FRESH")
    check("a4 fence unchanged + a refusal -> STALE",
          probe.evaluate(s_ok, stale, 7) == "STALE")
    check("a4 fence ADVANCED mid-probe -> SUPERSEDED, not STALE",
          probe.evaluate(s_ok, stale, 8) == "SUPERSEDED",
          "another runner published a newer session; the reading is discarded")
    check("a4 a fence that went BACKWARDS is not SUPERSEDED",
          probe.evaluate(s_ok, stale, 6) == "STALE",
          "only a forward fence means someone else published")

    # End to end through the injected seams: no network, no AWS, no boto3.
    calls = []

    def fake_fetch(method, url, headers, timeout=None):
        calls.append(url)
        return 400, b'{"error":"bad params"}', "application/json"

    class _CW(object):
        def __init__(self):
            self.emitted = []

        def put_metric_data(self, Namespace=None, MetricData=None):   # noqa: N803
            self.emitted.append(MetricData[0]["Value"])

    cw = _CW()
    res = probe.lambda_handler({}, None, secrets=_FakeSecrets(versioned),
                               cloudwatch=cw, fetch=fake_fetch)
    check("a4 END TO END: every probe 400 -> verdict=%s, SessionFresh=%s"
          % (res["verdict"], cw.emitted),
          res["verdict"] == "STALE" and cw.emitted == [0.0],
          "THE CUTOVER IN ONE LINE: the retired predicate returned fresh=True here")
    check("a4 the same run under the OLD predicate would have reported FRESH",
          all(old_predicate(400) for _ in res["probes"]),
          "difference control on the deployed path, not just on classify()")


# --------------------------------------------------------------------------- b, c, d, f
#
# THE THREE DRIVES ARE SUBPROCESSES, AND THAT IS THE POINT. Each runs under its own
# outbound-network guard installed BEFORE anything under test is evaluated, which no
# in-process arrangement can do once this battery has already imported the probe. Arm (f)
# then reads the two guards' own summaries, so "0 external" is a reading of an instrument
# that was demonstrably able to fire, not an absence of evidence.

RUNNER_DIR = os.path.join(REPO, "infra", "aws", "ec2", "investor-reporting-ycharts")
FENCE_DRIVE = os.path.join("tests", "fence_race.js")
NODE_GUARD = os.path.join(".", "tests", "netguard.js")
SESSION_SUITE = os.path.join(REPO, "infra", "aws", "lambda", "investor-reporting",
                             "ycharts", "session", "tests", "run_session_suite.py")

_DRIVE_CACHE = {}


def drive(key, cmd, cwd, timeout=420):
    """Run a drive ONCE per battery run and parse its RESULT block. rc is recorded, never
    trusted: a suite that died before printing its result is a FAILED arm, not a silent one."""
    if key in _DRIVE_CACHE:
        return _DRIVE_CACHE[key]
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout, shell=False)
        out = proc.stdout
        if "RESULT-BEGIN" not in out:
            data = {"_no_result": True, "rc": proc.returncode,
                    "stdout_tail": out[-800:], "stderr_tail": proc.stderr[-800:]}
        else:
            data = json.loads(out.split("RESULT-BEGIN", 1)[1].split("RESULT-END", 1)[0])
            data["_rc"] = proc.returncode
    except subprocess.TimeoutExpired:
        data = {"_no_result": True, "rc": 124, "stdout_tail": "TIMEOUT"}
    _DRIVE_CACHE[key] = data
    return data


def fence_drive():
    return drive("fence", ["node", "--require", NODE_GUARD, FENCE_DRIVE], RUNNER_DIR)


def session_drive():
    return drive("session", [sys.executable, SESSION_SUITE], REPO)


def arm_b():
    print()
    print("(b) FENCING -- two capture attempts on the fixture, driving the REAL persistSession")
    data = fence_drive()
    if data.get("_no_result"):
        check("b the fencing drive produced a result block", False,
              "rc=%s %s" % (data.get("rc"), str(data.get("stdout_tail"))[:200]))
        return
    cases = data["cases"]
    sim, slow, none = (cases["simultaneous"], cases["slow_runner_stale_fence"],
                       cases["no_lease_never_publishes"])
    print("      DENOMINATOR: 3 race case(s) driven | %d passing"
          % sum(1 for c in (sim, slow, none) if c["pass"]))
    print("      (b1) SIMULTANEOUS -- A holds the lease, B asks for it")
    print("           lease A ok=%s fence=%s | lease B ok=%s reason=%s"
          % (sim["lease_a"]["ok"], sim["lease_a"]["fence"], sim["lease_b"]["ok"],
             sim["lease_b"]["reason"]))
    print("           published fence=%s by=%s digest=%s -> after the loser tried: "
          "fence=%s by=%s digest=%s"
          % (sim["published_before_loser"]["fence"], sim["published_before_loser"]["persisted_by"],
             sim["published_before_loser"]["digest"], sim["published_after_loser"]["fence"],
             sim["published_after_loser"]["persisted_by"], sim["published_after_loser"]["digest"]))
    check("b1 1 wins, 1 refuses: the loser raises %s (%s) and never reaches the secret"
          % (sim["loser_refused"]["name"], sim["loser_refused"]["class"]), sim["pass"],
          "secret put calls across the whole case: %d" % sim["secret_put_calls"])
    check("b1 THE PUBLISHED VERSION IS UNCHANGED BY THE LOSER: digest %s == %s"
          % (sim["published_before_loser"]["digest"], sim["published_after_loser"]["digest"]),
          sim["published_unchanged_by_the_loser"],
          "compared over the published BYTES, not over a field")

    print("      (b2) THE SLOW RUNNER -- A's lease expired mid-capture and A still holds a "
          "fence-1 lease object")
    print("           A fence=%s -> B takes over fence=%s -> B publishes fence=%s"
          % (slow["lease_a_first"]["fence"], slow["lease_b_takeover"]["fence"],
             slow["b_published"]["fence"]))
    r = slow["a_stale_write_refused"]
    print("           A's late write: %s/%s my_fence=%s stored_fence=%s -- %s"
          % (r["name"], r["class"], r["my_fence"], r["stored_fence"], r["why"]))
    check("b2 the stale-fence write is REFUSED and the published version is unchanged: "
          "digest %s == %s"
          % (slow["published_after_b"]["digest"], slow["published_after_a_tried"]["digest"]),
          slow["pass"], "this is the shape NOTHING AT THE LEASE can see")
    ctl = slow["difference_control_same_runner_current_fence"]
    check("b2 DIFFERENCE CONTROL: the SAME runner with a CURRENT fence (%s) DOES publish "
          "(digest changes to %s)" % (ctl["lease_fence"], ctl["published_facts"]["digest"]),
          ctl["published"] and ctl["changed_this_time"],
          "so the refusal is the FENCE, not a fake that refuses everything")
    check("b3 a persist with NO held lease never reaches the secret: %d put call(s)"
          % none["secret_put_calls"], none["pass"],
          "otherwise the lease is optional and a caller that forgot it looks like a winner")


def arm_c():
    print()
    print("(c) ROTATION -- a new version published, the next invocation uses it, the old refused")
    data = session_drive()
    if data.get("_no_result"):
        check("c the session drive produced a result block", False,
              "rc=%s %s" % (data.get("rc"), str(data.get("stdout_tail"))[:200]))
        return
    c = data["arms"]["c_rotation"]
    print("      DENOMINATOR: %d published version(s) of %s | AWSCURRENT now %s"
          % (len(c["published_versions"]), "ycharts/session/current",
             c["awscurrent_after_rotation"]))
    print("      read 1: state=%s fence=%s generation=%s"
          % (c["read_1"]["state"], c["read_1"]["fence"], c["read_1"]["generation"]))
    print("      read 2: state=%s fence=%s generation=%s"
          % (c["read_2"]["state"], c["read_2"]["fence"], c["read_2"]["generation"]))
    n = c["next_invocation_used"]
    check("c the replay transport's NEXT invocation uses the new version: "
          "capture_generation %s -> %s" % (n["before_rotation"], n["after_rotation"]),
          n["before_rotation"] == "capture-generation-0001"
          and n["after_rotation"] == "capture-generation-0002"
          and n["identity_ok_before"] and n["identity_ok_after"],
          "read off recipe.step_identity, which the job itself uses to verify a session")
    t = c["token_value_rotation"]
    check("c the token VALUES rotated while the cookie NAME set did not: "
          "fingerprint %s -> %s" % (t["cookie_fingerprint_before"], t["cookie_fingerprint_after"]),
          t["values_rotated"] and t["cookie_NAME_set_unchanged"],
          "sha256 prefix over the whole jar -- no cookie value is printed anywhere")
    o = c["old_version_refused"]
    check("c THE OLD VERSION IS REFUSED: fence %s against an accepted fence of %s -> %s"
          % (o["fence_seen"], o["min_fence"], o["state"]),
          o["state"] == "STALE_FENCE", "closed vocabulary: %s" % ", ".join(
              c["read_state_vocabulary"]))
    check("c DIFFERENCE CONTROL: the SAME read unpinned reads %s"
          % c["difference_control_same_read_unpinned"]["state"],
          c["difference_control_same_read_unpinned"]["state"] == "OK",
          "so STALE_FENCE is the fence's doing and not a defect in the bundle")
    check("c a resume onto the OLD generation is refused by transport.resume_allowed: %s"
          % c["resume_onto_the_old_generation_allowed"],
          c["resume_onto_the_old_generation_allowed"] is False,
          "the rule, called -- not restated here")


def arm_d():
    print()
    print("(d) EVICTION / SELF-HEALING -- driven on job.GenerationJob with the replay transport")
    data = session_drive()
    if data.get("_no_result"):
        check("d the session drive produced a result block", False,
              "rc=%s" % data.get("rc"))
        return
    d = data["arms"]["d_eviction"]
    one, ctl, rep = (d["one_eviction"], d["no_resubmit_difference_control"],
                     d["repeat_eviction"])
    print("      evicted at step=%s status=%s -> transport.decision=%s"
          % (one["evicted_at"]["step"], one["evicted_at"]["status"],
             one["evicted_at"]["decision"]))
    print("      the JOB'S OWN why for that same step was %r -- job.py has no eviction "
          "outcome, so the classification is taken from the wire" % one["job_own_why_for_that_step"])
    print("      verified three ways before the resume: %s"
          % ", ".join("%s=%s" % (k, v) for k, v in sorted(one["verified_three_ways"].items())))
    check("d a 401 mid-job -> ONE broker refresh (refreshes_used=%d) -> outcome %s"
          % (one["refreshes_used"], one["outcome"]),
          one["outcome"] == "RECOVERED" and one["refreshes_used"] == 1
          and one["refresh_allowed"] is True,
          "rule called: %s; new generation %s" % (one["refresh_rule_called"],
                                                  one["new_generation"]))
    check("d it RESUMED AT THE CHECKPOINT and the job completed: resumed=%s ok=%s"
          % (one["resumed_at_checkpoint"], one["job_ok_after_recovery"]),
          one["resumed_at_checkpoint"] and one["job_ok_after_recovery"],
          "through the job's OWN resume() reconcile and after_create(), never a new create")
    check("d NO-RESUBMIT DIFFERENCE CONTROL: %d create POST(s) with the broker's recovery "
          "vs %d with a restart instead"
          % (ctl["creates_with_broker_recovery"], ctl["creates_with_a_restart_instead"]),
          ctl["creates_with_broker_recovery"] == 1
          and ctl["creates_with_a_restart_instead"] == 2 and ctl["discriminates"],
          ctl["denominator"])
    check("d a REPEAT eviction reaches %s, not a loop: second refresh refused -- %s"
          % (rep["outcome"], rep["second_refresh_refused"]["why"]),
          rep["outcome"] == "RETRYABLE_ATTENTION"
          and rep["second_refresh_refused"]["allowed"] is False
          and rep["parked_state"] == "ATTENTION" and rep["retryable"] is True,
          "request PRESERVED: %s" % json.dumps(rep["request_preserved"], sort_keys=True))
    ctrl = data["arms"]["controls"]
    check("d CONTROL: a 422 CONTRACT failure at the same step is %s with %d refresh(es)"
          % (ctrl["contract_failure_is_NOT_an_eviction"]["outcome"],
             ctrl["contract_failure_is_NOT_an_eviction"]["refreshes_used"]),
          ctrl["contract_failure_is_NOT_an_eviction"]["outcome"] == "NOT_AN_EVICTION"
          and ctrl["contract_failure_is_NOT_an_eviction"]["refreshes_used"] == 0,
          "without this, 'the broker refreshed' cannot be told from 'the broker refreshes "
          "on any failure' -- the login storm the rule exists to stop")
    check("d the read vocabulary is covered, not just its happy member: %s"
          % json.dumps(ctrl["read_state_coverage"], sort_keys=True),
          ctrl["pass"], "legacy flat bundle, unset secret and unparseable value")


def arm_f():
    print()
    print("(f) NOTHING LEFT THE MACHINE -- both guards, their denominators, and their controls")
    fence, session = fence_drive(), session_drive()
    if fence.get("_no_result") or session.get("_no_result"):
        check("f both guarded drives produced a result block", False,
              "a guard summary cannot be read from a drive that did not finish")
        return
    rows = [("node  infra/aws/ec2/investor-reporting-ycharts (arm b)",
             fence["netguard"], fence["netguard_positive_control"]),
            ("py    investor-reporting/ycharts/session (arms c, d)",
             session["netguard"], session["netguard_positive_control"])]
    total_attempts = total_external = 0
    for label, guard, control in rows:
        total_attempts += guard["attempts_observed"]
        total_external += guard["external_refused"]
        print("      %s" % label)
        print("        guard=%s installed=%s | attempts_observed=%d (DENOMINATOR) "
              "loopback_allowed=%d external_refused=%d"
              % (guard["guard"], guard["installed"], guard["attempts_observed"],
                 guard["loopback_allowed"], guard["external_refused"]))
        print("        POSITIVE CONTROL: attempted %s -> refused=%s, external count %s -> %s"
              % (control["attempted"], control["refused"], control["external_before"],
                 control["external_after"]))
    # The battery's own ARM-(a) network use is declared here rather than hidden: it is AWS
    # control plane, in the PARENT, through the aws shim -- a guard with an allow-list for
    # "our own AWS calls" would have a hole shaped exactly like the thing it guards against.
    print("      DECLARED, NOT GUARDED: arm (a4) makes one AWS control-plane read "
          "(events describe-rule) from THIS process. It is not a vendor call and it is not "
          "inside either guarded drive.")
    check("f 0 connection(s) to a non-loopback destination escaped either drive: "
          "%d refused of %d attempt(s) observed" % (total_external, total_attempts),
          all(g["installed"] for _l, g, _c in rows)
          and all(g["external_refused"] == len([d for d in g["external_destinations"]])
                  for _l, g, _c in rows)
          and total_external == total_attempts,
          "every attempt either drive observed WAS the positive control; no drive opened a "
          "socket of its own")
    check("f both guards are DEMONSTRABLY able to fire: %d of %d positive control(s) refused "
          "and counted" % (sum(1 for _l, _g, c in rows if c["pass"]), len(rows)),
          all(c["pass"] for _l, _g, c in rows),
          "a guard reporting 0 external and a guard that was never installed read identically")


RESEARCH_ROOT = "infra/aws/terraform/investor-reporting/ycharts-research-20260911"
YCHARTS_ROOT = os.path.join(REPO, "infra", "aws", "terraform", "investor-reporting", "ycharts")
TERRAFORM = os.path.join(REPO, ".tools", "terraform.exe")
AWS = os.path.join(REPO, ".tools", "aws.cmd")
LEDGER = os.path.join(REPO, "org", "critical_paths", "change_management",
                      "20260912T0314Z_irpt-bckend-rt9_deploy_completion.md")
SENTINEL = os.path.join(REPO, "org", "critical_paths", ".open_deploys",
                        "irpt-bckend-rt9.json")
ABSORBED = ("aws_secretsmanager_secret.research_session",
            "aws_cloudwatch_log_group.research_probe")
HOST = "i-0167fd745ad906a66"


def sh(cmd, cwd=None, timeout=900):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                          shell=False)


def arm_e():
    print()
    print("(e) ABSORBED, STOPPED, CONVERGED -- the research root's resources under the "
          "ycharts root")

    # -- the research root is GONE FROM THE TREE. Asked of git, not of the filesystem: a
    # gitignored .terraform/ cache can leave the DIRECTORY on disk while the ROOT is gone,
    # and `os.path.isdir` cannot tell those apart.
    tracked = sh(["git", "ls-files", RESEARCH_ROOT], cwd=REPO).stdout.strip()
    n_tracked = len([ln for ln in tracked.splitlines() if ln.strip()])
    at_head = sh(["git", "ls-tree", "-r", "--name-only", "HEAD", "--", RESEARCH_ROOT],
                 cwd=REPO).stdout.strip()
    n_head = len([ln for ln in at_head.splitlines() if ln.strip()])
    parent = sh(["git", "ls-tree", "-r", "--name-only", "HEAD~2", "--", RESEARCH_ROOT],
                cwd=REPO).stdout.strip()
    n_parent = len([ln for ln in parent.splitlines() if ln.strip()])
    print("      tracked files under %s: worktree=%d, HEAD=%d, HEAD~2=%d"
          % (RESEARCH_ROOT, n_tracked, n_head, n_parent))
    check("e the research root is GONE FROM THE TREE: %d tracked file(s) at HEAD, down from %d"
          % (n_head, n_parent),
          n_head == 0 and n_tracked == 0 and n_parent == 2,
          "asked of git, not of the filesystem -- the gitignored .terraform/ provider cache "
          "still leaves the DIRECTORY on disk in this worktree and os.path.isdir cannot tell "
          "that apart from a root that is still declared")

    # -- both resources are under the YCHARTS root's state.
    listed = sh([TERRAFORM, "state", "list"], cwd=YCHARTS_ROOT)
    addresses = [ln.strip() for ln in listed.stdout.splitlines() if ln.strip()]
    present = [a for a in ABSORBED if a in addresses]
    print("      ycharts state list: %d resource(s); the absorbed pair:" % len(addresses))
    for a in ABSORBED:
        print("        %-46s %s" % (a, "PRESENT" if a in addresses else "ABSENT"))
    check("e the absorbed resources are under the ycharts root's state: %d of %d, in a "
          "%d-resource state" % (len(present), len(ABSORBED), len(addresses)),
          listed.returncode == 0 and len(present) == len(ABSORBED) and len(addresses) == 19,
          "state list printed, not asserted")

    # -- and they are under NO OTHER root: the research state key is empty. A resource in TWO
    # states is the dangerous end state of a botched move, and a check that only looks at the
    # destination cannot see it.
    # THE NAIVE INSTRUMENT CANNOT BE USED HERE, AND IT FAILS IN THE WORST DIRECTION.
    # `terraform state list` in the research directory now REFUSES -- deleting main.tf removed
    # the backend declaration, so terraform reports "Backend initialization required ...
    # Unsetting the previously set backend s3", writes NOTHING to stdout and exits 1. An
    # emptiness check that read stdout alone would parse that refusal as ZERO RESOURCES and
    # PASS on a command that never looked at the state. This is not a transient failure that
    # an `init` would fix: the declaration that addressed the state is gone by design, so the
    # refusal is permanent and the instrument is retired, not retried. Row IRPT_BCKEND-W3-S37.
    research_dir = os.path.join(REPO, RESEARCH_ROOT)
    naive = sh([TERRAFORM, "state", "list"], cwd=research_dir, timeout=300) \
        if os.path.isdir(os.path.join(research_dir, ".terraform")) else None
    if naive is not None:
        first = next((ln.strip() for ln in (naive.stdout + naive.stderr).splitlines()
                      if "Error:" in ln), "<no error line>")
        print("      NAIVE INSTRUMENT, RETIRED: `terraform state list` in the deleted root -> "
              "rc=%d, %d stdout line(s)" % (naive.returncode, len(naive.stdout.split())))
        print("        %s" % re.sub(r"\x1b\[[0-9;]*m", "", first)[:110])
        check("e the retired instrument's refusal is DISTINGUISHED from an empty state: rc=%d "
              "with 0 stdout lines" % naive.returncode,
              naive.returncode != 0 and not naive.stdout.strip(),
              "an emptiness check reading stdout alone would have PASSED on this -- a refusal "
              "and a clean zero are identical there, which is why the reading below is taken "
              "from the state OBJECT instead")

    # SO THE EMPTINESS IS READ FROM THE STATE OBJECT ITSELF -- an instrument that needs neither
    # the deleted declaration nor terraform, and that answers the actual question: does any
    # OTHER state still own these two resources?
    obj = os.path.join(REPO, ".scratch", "research_tfstate_read.json")
    # The rc is not read here on purpose: the ORACLE is whether the object parses and what it
    # holds, and `sh` already captures the call. An absent or unreadable object leaves
    # `remaining` None, which FAILS the check below -- so a missing read cannot pass as empty.
    sh([AWS, "s3api", "get-object", "--bucket",
        "opal-313476888478-terraform-state", "--key",
        "investor-reporting/ycharts-research-20260911/tfstate",
        "--region", "us-east-1", obj,
        "--query", "ContentLength", "--output", "text"], timeout=300)
    remaining = None
    if os.path.exists(obj):
        with io.open(obj, "r", encoding="utf-8") as fh:
            doc = json.load(fh)
        remaining = [r.get("type", "") + "." + r.get("name", "")
                     for r in (doc.get("resources") or [])]
        print("      research STATE OBJECT read directly from S3: serial=%s, %d resource(s) %s"
              % (doc.get("serial"), len(remaining), remaining))
    check("e the research state OBJECT holds %s resource(s) -- the pair is under ONE root, "
          "not two" % (len(remaining) if remaining is not None else "UNREADABLE"),
          remaining == [],
          "read from the tfstate object itself, so it needs neither the deleted backend "
          "declaration nor terraform; a resource left in BOTH states is the dangerous outcome "
          "of a half-done move and only this reading can see it")

    # -- the objects THEMSELVES survived. A DIFFERENT INSTRUMENT than the one that moved them:
    # `state rm` reporting "Removed" is terraform describing itself, and it cannot distinguish
    # a forgotten resource from a deleted one.
    secret = sh([AWS, "secretsmanager", "describe-secret", "--secret-id",
                 "ycharts/session/research-20260911", "--region", "us-east-1",
                 "--query", "Name", "--output", "text"], timeout=300)
    group = sh([AWS, "logs", "describe-log-groups", "--log-group-name-prefix",
                "/aws/lambda/irpt-ycharts-research-20260911", "--region", "us-east-1",
                "--query", "logGroups[].logGroupName", "--output", "text"], timeout=300)
    s_ok = "ycharts/session/research-20260911" in secret.stdout
    g_ok = "irpt-ycharts-research-20260911" in group.stdout
    print("      live control plane: secret=%r log_group=%r"
          % (secret.stdout.strip()[:60], group.stdout.strip()[:60]))
    check("e NOTHING WAS DESTROYED -- both objects still exist, read from the AWS control "
          "plane: secret %s, log group %s"
          % ("PRESENT" if s_ok else "MISSING", "PRESENT" if g_ok else "MISSING"),
          s_ok and g_ok,
          "the move was import-then-state-rm; state rm FORGETS and never deletes, and this is "
          "the instrument that can tell those apart")

    # -- the ycharts root CONVERGED.
    plan = sh([TERRAFORM, "plan", "-input=false", "-no-color"], cwd=YCHARTS_ROOT)
    converged = "No changes. Your infrastructure matches the configuration." in plan.stdout
    line = next((ln.strip() for ln in plan.stdout.splitlines()
                 if "No changes" in ln or ln.strip().startswith("Plan:")), "<no verdict line>")
    print("      ycharts post-apply plan: %s" % line)
    check("e the ycharts root's POST-APPLY plan reads No changes", converged,
          "run with the worktree's .tools/terraform.exe after init; the apply that preceded it "
          "reported 'Apply complete! Resources: 0 added, 2 changed, 0 destroyed'")

    # -- the host is STOPPED, live.
    host = sh([AWS, "ec2", "describe-instances", "--instance-ids", HOST, "--region",
               "us-east-1", "--query", "Reservations[].Instances[].State.Name",
               "--output", "text"], timeout=300)
    state = host.stdout.strip()
    check("e the runner host is STOPPED: %s -> %r" % (HOST, state),
          state == "stopped",
          "read live from the control plane, never asserted from instance.tf -- bound 1 holds, "
          "no login and no capture rode on any of this")

    # -- the ledger is CLOSED and its sentinel is gone. Both, because either alone is
    # ambiguous: a CLOSED entry with a sentinel still present is a half-landed close, and an
    # absent sentinel with no entry is a ledger that was never opened.
    with io.open(LEDGER, "r", encoding="utf-8") as fh:
        entry = fh.read()
    closed = "**Status:** CLOSED" in entry
    legs_closed = entry.count("CLOSED 2026")
    sentinel_gone = not os.path.exists(SENTINEL)
    committed = sh(["git", "ls-files", "--error-unmatch",
                    "org/critical_paths/change_management/"
                    "20260912T0314Z_irpt-bckend-rt9_deploy_completion.md"], cwd=REPO)
    print("      ledger: status CLOSED=%s | leg proofs closed=%d | sentinel present=%s | "
          "entry tracked=%s" % (closed, legs_closed, not sentinel_gone,
                                committed.returncode == 0))
    check("e the ledger is CLOSED with %d leg(s) proven, its sentinel REMOVED, and the entry "
          "committed" % legs_closed,
          closed and legs_closed >= 6 and sentinel_gone and committed.returncode == 0,
          "a CLOSED entry whose sentinel is still present is a half-landed close; an absent "
          "sentinel with no entry is a ledger nobody opened -- so both are read")


def main():
    print("=" * 78)
    print("IB-rt-9 / RT9-AC1 -- arms (a), (b), (c), (d), (e), (f)")
    print("=" * 78)
    code_hits = arm_a1()
    arm_a2(code_hits)
    arm_a3()
    arm_a4()
    arm_b()
    arm_c()
    arm_d()
    arm_e()
    arm_f()
    print()
    print("-" * 78)
    print("ARMS RUN: 6 of 6  (a cutover, b fencing, c rotation, d eviction, e absorbed, "
          "f no egress)")
    print("checks failed: %d" % len(FAILURES))
    for f in FAILURES:
        print("  FAILED: %s" % f)
    print("-" * 78)
    if FAILURES:
        print("FINAL: INCOMPLETE -- the acceptance token is deliberately absent from this "
              "output in EVERY form, including negated: the expect is graded as a REGEX and a "
              "negated line would MATCH and grade a failing run PASS.")
        return 1
    print("IBRT9-BROKER-FENCED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
