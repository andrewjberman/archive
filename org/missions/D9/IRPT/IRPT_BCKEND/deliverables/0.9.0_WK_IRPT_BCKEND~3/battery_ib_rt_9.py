"""IB-rt-9 battery -- RT9-AC1. PARTIAL: arm (a) only, under the managed wind-down.

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

WHAT DOES NOT RUN -- arms (b) FENCING, (c) ROTATION, (d) EVICTION, (e)
ABSORBED/STOPPED/CONVERGED, (f) NOTHING LEFT THE MACHINE. Arm (e) is a
ledger + `state mv` + apply, forbidden for the rest of this session by the
managed wind-down (0.0.0_AB_MSTR, relayed 2026-09-11 17:30Z). Arms (b)-(d)
and (f) are fixture work that is permitted but unbuilt when this session
ended; they are described in WIP_IB-rt-9_winddown.md beside this file.

BOUND 1 HOLDS: nothing here makes a YCharts call, a login or a capture. The
only network calls are two AWS control-plane reads (describe-rule), and the
predicate is exercised on RECORDED statuses and bodies through the probe's
injected `fetch` seam.
"""
from __future__ import annotations

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


def main():
    print("=" * 78)
    print("IB-rt-9 / RT9-AC1 -- ARM (a) ONLY, under the managed wind-down")
    print("=" * 78)
    code_hits = arm_a1()
    arm_a2(code_hits)
    arm_a3()
    arm_a4()
    print()
    print("-" * 78)
    for arm, why in (
            ("(b) FENCING", "two capture attempts on the fixture -- not built"),
            ("(c) ROTATION", "publish a new version, old refused -- not built"),
            ("(d) EVICTION", "401 mid-job, ONE refresh, resume at checkpoint -- not built"),
            ("(e) ABSORBED", "ledger + state mv + apply -- BLOCKED, row IRPT_BCKEND-W3-S26: "
                             "the ycharts root's plan carries an unapplied handler flip to "
                             "entry.lambda_handler and entry.py is in no zip, so the apply "
                             "this arm REQUIRES takes irpt-ycharts-generate down"),
            ("(f) NO EGRESS", "guard log across the whole battery -- not built")):
        print("  NOT RUN  %-14s %s" % (arm, why))
    print("-" * 78)
    print("ARM (a) checks failed: %d" % len(FAILURES))
    for f in FAILURES:
        print("  FAILED: %s" % f)
    print("FINAL: ARM-A-ONLY, INCOMPLETE -- RT9-AC1 is NOT met by this run and its "
          "acceptance token is deliberately absent from this output in EVERY form, "
          "including negated: the expect is graded as a REGEX and a negated line would "
          "match. Arm (e) is BLOCKED by row IRPT_BCKEND-W3-S26.")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
