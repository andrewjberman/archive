#!/usr/bin/env python3
"""IB-s-4 acceptance battery -- criterion S4-AC1, arms (a)-(e), (f), (g), (h), (i), (amend).

Prints `IBS4-FRESHNESS-DRIVEN` on the LAST line if and only if every arm passes, with ONE
declared exception the face itself writes: arm (h) may read `BLOCKED-BY-W1-S8` -- the runner's
first-mint has no declared bundle, measured at IB-s-12 -- and "per the criterion's own rule the
token is not withheld when every other arm holds".

Every count carries its DENOMINATOR and every absence carries a control that can go non-zero.

Usage:  python battery_ib_s_4.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, *([os.pardir] * 7)))
_PKG = os.path.join(_REPO, "infra", "aws", "lambda", "investor-reporting")
_DIR = os.path.join(_PKG, "directory")
_GOLD = os.path.join(_REPO, "data", "assets", "scripts", "gold", "investor_reporting")

for p in (_HERE, _DIR, os.path.join(_PKG, "_authz"), os.path.join(_PKG, "_scope"),
          os.path.join(_PKG, "_keys"), os.path.join(_REPO, "lib"), _GOLD):
    if p not in sys.path:
        sys.path.insert(0, p)

import expiry                     # noqa: E402
import ib_s_4_controlled_clock as harness   # noqa: E402
import refresh                    # noqa: E402

RESULTS = []
SCHEDULE_NAME = "irpt-directory-refresh"
FUNCTION_NAME = "irpt-directory-refresh"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-directory-refresh.zip"
LEDGER_SLUG = "irpt-bckend-s4"
SENTINEL = os.path.join(_REPO, "org", "critical_paths", ".open_deploys", LEDGER_SLUG + ".json")
LEDGER_DIR = os.path.join(_REPO, "org", "critical_paths", "change_management")
SHARED_CODE_BUCKET = "opal-data-mdpf"
SHARED_CODE_PREFIX = "code/scripts/assets_gold/investor_reporting/"


def record(arm, verdict, line):
    RESULTS.append((arm, verdict, line))
    print("ARM {} {}: {}".format(arm, verdict, line))


def section(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def _aws(args, timeout=120):
    """The estate's aws shim, invoked the way a PYTHON parent must invoke it.

    `.tools/aws` is a bash script, not a PE binary; `.tools/aws.cmd` is the Windows-plane
    forwarder that exists for this call site. Never a bare `aws` -- that bypasses the
    MSYS path-mangling guard the shim IS. The shim emits CRLF, so the CR is stripped here.
    """
    shim = os.path.join(_REPO, ".tools", "aws.cmd" if os.name == "nt" else "aws")
    if not os.path.isfile(shim):
        return 127, "BLOCKED: aws shim absent at " + shim
    p = subprocess.run([shim] + args, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).replace(chr(13), "").strip()


# ============================================================================ arms (a)-(e)
def arms_a_to_e():
    section("ARMS (a)-(e) -- FIVE ARMS, FIVE READINGS, ON A CONTROLLED CLOCK")
    rows, elapsed, cal_source = harness.run_arms()
    print("  calendar: %s (REAL frontier, not an approximation)" % cal_source)
    codes, pairs = [], []
    for r in rows:
        print("  ARM (%s) %-20s -> %-42s state=%-9s business_date=%s"
              % (r["arm"], r["name"], r["reason_code"], r["state"], r["business_date"]))
        print("        %s" % r["observable"])
        codes.append(r["reason_code"])
        pairs.append((r["state"], r["reason_code"]))
    print("  the five status values: %s" % codes)
    print("  PAIRWISE DISTINCT: %d of %d reason codes; %d of %d (state, code) pairs"
          % (len(set(codes)), len(codes), len(set(pairs)), len(pairs)))
    distinct = len(set(codes)) == len(codes) == 5

    # Per-arm verdicts, because "five arms pass" cannot tell a reader WHICH one stopped reading
    # differently.
    expect = {"a": "REFRESH_COMPLETED_WITH_ADDITIONS",
              "b": "REFRESH_COMPLETED_WITH_ELIGIBILITY_CHANGE",
              "c": "REFRESH_TRIGGER_MISSED",
              "d": "REFRESH_FAILED",
              "e": "DIRECTORY_OVER_AGE"}
    by_arm = {r["arm"]: r for r in rows}
    for arm in ("a", "b", "c", "d", "e"):
        r = by_arm.get(arm)
        ok = bool(r) and r["reason_code"] == expect[arm] and distinct
        if arm == "b" and r:
            ok = ok and r["delta"].get("disappeared") == 0   # stays VISIBLE, never deleted
        record(arm, "PASS" if ok else "FAIL",
               "%s -> %s (state %s); distinct 5 of 5" % (r["name"], r["reason_code"], r["state"])
               if r else "arm did not run")
    return elapsed


# ============================================================================ arm (f)
def arm_f(elapsed):
    section("ARM (f) -- NO WAIT")
    ok = True
    print("  harness wall clock: %.3f s (ceiling 60 s)" % elapsed)
    if elapsed >= 60:
        ok = False

    # SOURCE CENSUS: no sleep longer than one second anywhere in this cell's own code.
    files = [os.path.join(_HERE, "ib_s_4_controlled_clock.py"),
             os.path.join(_HERE, "battery_ib_s_4.py"),
             os.path.join(_DIR, "refresh.py"), os.path.join(_DIR, "expiry.py")]
    pat = re.compile(r"(?:time\.)?sleep\(\s*([0-9.]+)")
    hits = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            for i, line in enumerate(fh.read().splitlines(), 1):
                for m in pat.finditer(line):
                    hits.append((os.path.basename(f), i, float(m.group(1))))
    print("  DENOMINATOR: %d source file(s) censused for a sleep call" % len(files))
    over = [h for h in hits if h[2] > 1.0]
    print("  sleep call(s) found: %d, of which longer than 1 s: %d" % (len(hits), len(over)))
    for h in over:
        print("    OVER: %s:%d sleep(%s)" % h)
    if over:
        ok = False
    # POSITIVE CONTROL: the matcher must be able to find one.
    probe = len(pat.findall("time.sleep(5)  # a synthetic offender"))
    print("  POSITIVE CONTROL on the matcher: a synthetic `time.sleep(5)` line matches %d -- "
          "the census can go non-zero" % probe)
    if probe != 1:
        ok = False
    record("f", "PASS" if ok else "FAIL",
           "harness %.3f s < 60 s; %d of %d sleep call(s) over 1 s across %d source file(s)"
           % (elapsed, len(over), len(hits), len(files)))


# ============================================================================ arm (g)
def arm_g():
    section("ARM (g) -- THE SCHEDULE IS APPLIED AND ENABLED")
    ok = True
    lines = []
    rc, out = _aws(["scheduler", "get-schedule", "--name", SCHEDULE_NAME, "--output", "json"])
    print("  get-schedule --name %s rc=%d" % (SCHEDULE_NAME, rc))
    state = expr = tz = target = None
    if rc == 0:
        try:
            doc = json.loads(out)
            state = doc.get("State")
            expr = doc.get("ScheduleExpression")
            tz = doc.get("ScheduleExpressionTimezone")
            target = (doc.get("Target") or {}).get("Arn")
        except ValueError:
            pass
    print("    State: %s" % state)
    print("    ScheduleExpression: %s  (timezone %s)" % (expr, tz))
    print("    Target: %s" % target)
    if state != "ENABLED" or expr != expiry.SCHEDULE_EXPRESSION:
        ok = False
        lines.append("state/expression: %s / %s" % (state, expr))
    else:
        lines.append("State ENABLED with the declared expression %s (%s)" % (expr, tz))

    # WHICH ARTIFACT DOES THE SCHEDULE ACTUALLY INVOKE? The amendment's own question. The target
    # is a LAMBDA, so the code that runs is the zip Terraform ships -- verified by CodeSha256
    # against the artifact's own content-sha256, two different objects.
    rc2, out2 = _aws(["lambda", "get-function-configuration", "--function-name", FUNCTION_NAME,
                      "--output", "json"])
    served = None
    if rc2 == 0:
        try:
            served = json.loads(out2).get("CodeSha256")
        except ValueError:
            pass
    rc3, out3 = _aws(["s3api", "head-object", "--bucket", ARTIFACT_BUCKET, "--key",
                      ARTIFACT_KEY, "--output", "json"])
    built = None
    size = None
    if rc3 == 0:
        try:
            doc = json.loads(out3)
            size = doc.get("ContentLength")
            built = (doc.get("Metadata") or {}).get("content-sha256")
        except ValueError:
            pass
    print("  THE SCHEDULE INVOKES A LAMBDA, so the code that runs is the ZIP TERRAFORM SHIPS:")
    print("    artifact s3://%s/%s ContentLength=%s content-sha256=%s"
          % (ARTIFACT_BUCKET, ARTIFACT_KEY, size, built))
    print("    served   get-function-configuration %s CodeSha256=%s" % (FUNCTION_NAME, served))
    print("    equal: %s" % (served is not None and served == built))
    print("    NEGATIVE CONTROL: served == a bogus sha? %s (must be False)"
          % (served == "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="))
    print("    NOT the shared-home gold script: that artifact is 404 (arm (h)), and nothing in "
          "this schedule's path reads it")
    if served is None or built is None or served != built:
        ok = False
        lines.append("CodeSha256 %s vs built %s" % (served, built))
    else:
        lines.append("CodeSha256 == the artifact's own content-sha256 (%s)" % built)

    # The ledger, graded on the ENTRY (deploy_ledger.py close DELETES the sentinel as the act of
    # closing, so a sentinel present at grading time can only mean the entry is still OPEN).
    entries = [f for f in sorted(os.listdir(LEDGER_DIR)) if LEDGER_SLUG in f]
    print("  ledger entries matching %s: %d of %d files in change_management/"
          % (LEDGER_SLUG, len(entries), len(os.listdir(LEDGER_DIR))))
    status_line, legs_closed, commit = "", 0, ""
    if entries:
        with open(os.path.join(LEDGER_DIR, entries[-1]), "r", encoding="utf-8") as fh:
            text = fh.read()
        for line in text.splitlines():
            if line.startswith("**Status:**"):
                status_line = line
        legs_closed = text.count("| CLOSED ")
        print("  %s" % status_line)
        print("  legs CLOSED: %d" % legs_closed)
        cp = subprocess.run(["git", "log", "-1", "--format=%H", "--",
                             os.path.join("org", "critical_paths", "change_management",
                                          entries[-1])],
                            cwd=_REPO, capture_output=True, text=True, timeout=60)
        commit = cp.stdout.strip()
        print("  ledger entry committed at %s" % (commit or "NOT COMMITTED"))
    print("  sentinel %s: %s -- the OPEN sentinel was committed before the apply and REMOVED by "
          "the close" % (os.path.basename(SENTINEL),
                         "present" if os.path.isfile(SENTINEL) else "absent"))
    sp = subprocess.run(["git", "log", "--oneline", "--all", "--",
                         os.path.join("org", "critical_paths", ".open_deploys",
                                      LEDGER_SLUG + ".json")],
                        cwd=_REPO, capture_output=True, text=True, timeout=60)
    sentinel_commits = [ln for ln in sp.stdout.strip().splitlines() if ln]
    print("  sentinel commit(s) in history: %d -- %s"
          % (len(sentinel_commits), sentinel_commits[0] if sentinel_commits else "NONE"))
    if "CLOSED" not in status_line or not commit or os.path.isfile(SENTINEL) \
            or not sentinel_commits:
        ok = False
        lines.append("ledger: %s / legs %d / commit %s / sentinel present %s / sentinel commits %d"
                     % (status_line.strip(), legs_closed, commit[:10],
                        os.path.isfile(SENTINEL), len(sentinel_commits)))
    else:
        lines.append("ledger CLOSED with %d legs, committed %s, sentinel committed (%s) then "
                     "removed by the close" % (legs_closed, commit[:10],
                                               sentinel_commits[0].split()[0]))
    record("g", "PASS" if ok else "FAIL", "; ".join(lines))


# ============================================================================ arm (h)
def arm_h():
    section("ARM (h) -- THE RUNNER'S FIRST-MINT: THE ARTIFACT, NOT THE EXIT CODE")
    lines = []
    # The guard's own explicit first-mint mechanism, run ONCE for the record.
    sd = os.path.join(_REPO, ".tools", "safe-deploy.sh")
    p = subprocess.run(["bash", sd, "--mint-bundle", "investor_reporting"], cwd=_REPO,
                       capture_output=True, text=True, timeout=180)
    out = (p.stdout + p.stderr).replace(chr(13), "").strip()
    print("  safe-deploy.sh --mint-bundle investor_reporting rc=%d" % p.returncode)
    for line in out.splitlines():
        print("    | %s" % line)
    # The ARTIFACT, which is the thing the arm actually grades.
    key = SHARED_CODE_PREFIX + "directory_runner.py"
    rc, head = _aws(["s3api", "head-object", "--bucket", SHARED_CODE_BUCKET, "--key", key,
                     "--output", "json"])
    print("  head-object s3://%s/%s rc=%d" % (SHARED_CODE_BUCKET, key, rc))
    for line in head.splitlines()[:4]:
        print("    | %s" % line)
    local = os.path.join(_GOLD, "directory_runner.py")
    with open(local, "rb") as fh:
        blob = fh.read()
    print("  the BUILT file beside it: %s size=%d sha256=%s"
          % (os.path.basename(local), len(blob), hashlib.sha256(blob).hexdigest()))
    landed = (rc == 0)
    if landed:
        record("h", "PASS", "the runner's first-mint LANDED: head-object rc=0 on %s" % key)
        return
    lines.append("the guard's explicit mint was run ONCE and refused; head-object on the served "
                 "code prefix reads 404 for directory_runner.py -- both printed verbatim above")
    lines.append("the exit code is NOT the delivery: the artifact is absent, which is what this "
                 "arm grades")
    record("h", "BLOCKED-BY-W1-S8", "; ".join(lines))


# ============================================================================ arm (i)
def arm_i():
    section("ARM (i) -- THE ID SPACE, TRACED (issuer amendment, row W1-S7)")
    ok = True
    commit = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], cwd=_REPO,
                            capture_output=True, text=True, timeout=60).stdout.strip()
    runner = os.path.join(_GOLD, "directory_runner.py")
    with open(runner, "r", encoding="utf-8") as fh:
        src = fh.read().splitlines()

    def line_of(needle, start=0):
        for i in range(start, len(src)):
            if needle in src[i]:
                return i + 1, src[i].strip()
        return None, None

    common_ln, common_txt = line_of('opaque_id("account", firm_id, a["account_number"])')
    print("  ALL FIRMS share one call site:")
    print("    data/assets/scripts/gold/investor_reporting/directory_runner.py:%s @ %s"
          % (common_ln, commit))
    print("      %s" % common_txt)
    print("    so the RAW KEY is whatever each firm's row builder puts in `account_number`:")
    traced = {}
    for firm, needle, note in (
            ("49financial", 'return {"account_number": aid, "account_type": _s(r.get("acct_type"))',
             'aid is the index of `acc` -- dim_account.account_id (set_index at the line below)'),
            ("inflection", 'return {"account_number": _s(r.get("account_number")),',
             'accounts_v2.account_number -- NOT accounts_v2.account_id'),
            ("cottonwood", 'return {"account_number": _s(r.get("Account Number"))',
             'fact_allocations "Account Number" (or "Original Account Number") -- NOT '
             'fact_model_assignment.external_id')):
        ln, txt = line_of(needle)
        traced[firm] = (ln, txt, note)
        print("      %-12s :%-4s  %s" % (firm, ln, txt))
        print("      %-12s          RAW KEY: %s" % ("", note))
        if ln is None:
            ok = False
    ix_ln, ix_txt = line_of('acc_ix = acc.set_index(')
    print("      %-12s :%-4s  %s" % ("49financial", ix_ln, ix_txt))
    print("  %d of 3 firms traced to a file:line @ %s" % (len(traced), commit))

    # THE REFRESHED DIRECTORY, built now, against the LATEST holdings snapshot per firm.
    import importlib.util
    spec = importlib.util.spec_from_file_location("directory_runner", runner)
    dr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dr)
    buckets = dr.firm_bucket_map()
    print("  resolving each firm's LATEST holdings snapshot and the REFRESHED directory:")
    totals = []
    for firm in dr.client_firms():
        fid = firm["firm_id"]
        bucket = buckets.get(fid)
        t0 = time.time()
        res = dr.run_firm(firm, buckets, qa=True, upload=False, local_out=None, explicit=None)
        dir_ids = set()
        for e in res["entries"]:
            dir_ids.update((e.get("ids") or {}).get("account_ids") or [])
        rc, out = _aws(["s3api", "get-object", "--bucket", bucket, "--key",
                        "investor-reporting/qa/holdings/latest.json",
                        os.path.join(_REPO, ".scratch", "hold_%s.json" % fid), "--output",
                        "json"])
        hold_ids, hold_key = set(), None
        if rc == 0:
            with open(os.path.join(_REPO, ".scratch", "hold_%s.json" % fid), "r",
                      encoding="utf-8") as fh:
                ptr = json.load(fh)
            hold_key = ptr.get("key")
            rc2, _ = _aws(["s3api", "get-object", "--bucket", bucket, "--key", hold_key,
                           os.path.join(_REPO, ".scratch", "holdsnap_%s.json" % fid),
                           "--output", "json"])
            if rc2 == 0:
                with open(os.path.join(_REPO, ".scratch", "holdsnap_%s.json" % fid), "r",
                          encoding="utf-8") as fh:
                    snap = json.load(fh)
                hold_ids = _account_ids_of(snap)
        resolved = len(hold_ids & dir_ids)
        totals.append((fid, resolved, len(hold_ids)))
        print("    %-12s directory accounts=%-6d holdings accounts=%-6d RESOLVED %d of %d "
              "(%.1fs, snapshot %s)"
              % (fid, len(dir_ids), len(hold_ids), resolved, len(hold_ids),
                 time.time() - t0, hold_key))
    print("  NO JOIN WAS EDITED: this arm READS the raw-key selection and COUNTS the overlap; "
          "whether one id space is owed is the CTO's L10 read (row W1-S7).")
    # POSITIVE CONTROL: the resolver must be able to report a non-zero, or a 0 means nothing.
    nonzero = [t for t in totals if t[1] > 0]
    print("  POSITIVE CONTROL: %d of %d firms resolve NON-ZERO, so a zero elsewhere is a real "
          "id-space gap and not a broken comparison" % (len(nonzero), len(totals)))
    if not nonzero:
        ok = False
    record("i", "PASS" if ok else "FAIL",
           "3 of 3 firms traced to file:line @ %s; holdings ids resolved against the refreshed "
           "directory: %s" % (commit, "; ".join("%s %d of %d" % t for t in totals)))


def _account_ids_of(node, out=None):
    """Every account id anywhere in a holdings snapshot, by shape rather than by a fixed path."""
    if out is None:
        out = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("account_ids", "opaque_account_ids") and isinstance(v, list):
                out.update(str(x) for x in v)
            elif k in ("opaque_account_id", "account_id_opaque") and isinstance(v, str):
                out.add(v)
            else:
                _account_ids_of(v, out)
    elif isinstance(node, list):
        for v in node:
            _account_ids_of(v, out)
    return out


# ============================================================================ arm (amend)
def arm_amend():
    section("ARM (amend) -- GUARDED, BOUND, AND SILENT ON THE REFUSED VALUE")
    ok = True
    import enforce as ez
    import fixtures as afx        # the _authz fixtures (shapes, not identities)

    # 1. GUARDED. This cell ships ONE handler (the scheduled refresh entry) and registers it in
    #    the route table below; the census reads that table.
    e_deps = afx.Deps()
    binding = ez.FirmBinding(afx.TENANT, afx.OPAQUE_FIRM)
    enforcer = ez.Enforcer(binding, e_deps.load_directory, e_deps.load_ownership,
                           e_deps.load_policy, artifacts=dict(afx.ARTIFACTS))

    @enforcer.guard("directory_refresh_read", "account")
    def refresh_read_handler(request, scope):
        return {"ok": True, "accounts": list(scope["permitted_account_set"])}

    routes = {"SCHEDULE irpt-directory-refresh -> refresh.lambda_handler": refresh_read_handler}
    census = ez.unguarded_routes(routes)
    print("  routes this cell registers: %d" % census["routes"])
    print("  unguarded_routes(): %s" % json.dumps(census, sort_keys=True))
    print("  reads %d of %d unguarded" % (len(census["unguarded"]), census["routes"]))
    if census["unguarded"]:
        ok = False
    dirty = ez.unguarded_routes(dict(routes, **{"GET /leak": lambda r, s=None: None}))
    print("  POSITIVE CONTROL: the same census over a table carrying one unwrapped handler "
          "reads %d of %d unguarded -- it can go non-zero"
          % (len(dirty["unguarded"]), dirty["routes"]))
    if not dirty["unguarded"]:
        ok = False

    # 2. BOUND. A non-reconciling FirmBinding is a REFUSAL, never an empty served set.
    cal = expiry.resolve_calendar()
    good = {"as_of_business_date": str(cal.expected_last_trading_day(dt.date.today())),
            "firm_id_opaque": afx.OPAQUE_FIRM, "directory_revision": "rev-amend"}
    bad = dict(good, firm_id_opaque="fir_SOMETHING_ELSE")
    out_bad, extra_bad = refresh.serve_read(bad, dt.date.today(), "amend-1", cal,
                                            binding=binding)
    out_good, _extra = refresh.serve_read(good, dt.date.today(), "amend-2", cal,
                                          binding=binding)
    print("  non-reconciling binding -> ok=%s code=%s (never an empty served set)"
          % (out_bad.get("ok"), out_bad.get("code")))
    print("  reconciling binding     -> state=%s (the CONTROL: the refusal is not a constant)"
          % out_good.get("state"))
    if out_bad.get("code") != "FIRM_BINDING" or extra_bad is not None:
        ok = False
    if out_good.get("state") != "READY":
        ok = False

    # 3. SILENT ON THE REFUSED VALUE. A fixture that keys by a client display name.
    secret = "Whitfield Family"
    res = enforcer.serve(ez.Request(afx.headers(), "directory_refresh_read", "account", afx.A1,
                                    params={"client": secret}), lambda scope: {"x": 1})
    envelope = res.as_envelope() if not res.ok else {"served": True}
    blob = json.dumps({"envelope": envelope, "audit": enforcer.audit}, sort_keys=True)
    hits = blob.count(secret)
    print("  a fixture keying by a client display name -> %s"
          % (("REFUSED " + res.code) if not res.ok else "KEYED -- FAIL"))
    print("  WHOLE-ENVELOPE census (body + reason + audit trail): %d occurrence(s) of the "
          "refused value across %d bytes" % (hits, len(blob)))
    print("  the reason names the COMPONENT instead: %r" % (res.reason[:90] if not res.ok
                                                            else "-"))
    if res.ok or hits:
        ok = False
    control = json.dumps({"leaky": "the refused value was %s" % secret}).count(secret)
    print("  POSITIVE CONTROL on the census: a synthetic leaky envelope trips it at %d -- the "
          "census can go non-zero" % control)
    if control != 1:
        ok = False
    record("amend", "PASS" if ok else "FAIL",
           "%d of %d routes unguarded; a non-reconciling FirmBinding REFUSES with FIRM_BINDING "
           "while a reconciling one serves; %d occurrence(s) of a refused client name across the "
           "whole envelope and audit trail" % (len(census["unguarded"]), census["routes"], hits))


# ============================================================================ main
def main():
    print("IB-s-4 BATTERY -- %s"
          % dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("repo: %s" % _REPO)
    elapsed = arms_a_to_e()
    arm_f(elapsed)
    arm_g()
    arm_h()
    arm_i()
    arm_amend()

    section("SUMMARY")
    for arm, verdict, line in RESULTS:
        print("  ARM (%s) %s: %s" % (arm, verdict, line))
    expected = 10
    passed = sum(1 for _, v, _ in RESULTS if v == "PASS")
    blocked = [a for a, v, _ in RESULTS if v.startswith("BLOCKED")]
    print("  %d of %d arms PASS; %d BLOCKED by a named row: %s"
          % (passed, expected, len(blocked), blocked))
    # The face's OWN rule: arm (h) may read BLOCKED-BY-W1-S8 and the token is NOT withheld when
    # every other arm holds. No other arm may be blocked and no arm may FAIL.
    others_hold = (passed + len(blocked)) == expected and len(RESULTS) == expected
    only_h_blocked = blocked in ([], ["h"])
    if others_hold and only_h_blocked:
        if blocked:
            print("  arm (h) reads BLOCKED-BY-W1-S8 (the runner's first-mint has no declared "
                  "bundle -- measured at IB-s-12, carried to L10 by the issuer). The face: "
                  "'the token is not withheld when every other arm holds'.")
        print("IBS4-FRESHNESS-DRIVEN")
        return 0
    print("TOKEN WITHHELD -- %d of %d arms PASS, blocked: %s" % (passed, expected, blocked))
    return 1


if __name__ == "__main__":
    sys.exit(main())
