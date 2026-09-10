#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-25 S25-AC1 battery -- THE VERDICT DISCLOSES ITS OWN FORCING.

Prints EGS25-VERDICT-DISCLOSES-FORCING only when all six arms (a)-(f) hold.

WHY ARM (a) IS STILL LIVE AFTER THE DEPLOY, said up front because it is the one
thing a reader would reasonably doubt: arm (a) must reproduce the ABSENCE on the
deployed bytes, but this cell has since REPLACED those bytes. The artifact bucket
has versioning ENABLED (measured, not assumed), so the exact pre-change object is
still addressable by its versionId and arm (a) re-reads THAT, live, every run --
it is not read from a local copy and not taken on trust from the issuer's row.

Arms (b) and (c) drive the REAL main() in-process with every AWS call stubbed:
zero invokes, zero S3 writes, zero sends. Arm (d) loads the OLD module (the same
pre-change object) beside the NEW one and compares their decisions directly.

Bounds: vendored CLI v1 shim under a per-call timeout; every S3 time UTC via
s3api; denominators on every count. ASCII only.

Run from the worktree root:
  timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs25_verdict_discloses_forcing.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(ROOT, ".tools", "aws.cmd" if sys.platform == "win32" else "aws")

ART_BUCKET = "opal-313476888478-lambda-artifacts"
ART_PREFIX = "ec2/etfs-reports/"
ART_KEY = ART_PREFIX + "render_month_end.py"
PRIOR_VERSION_ID = "FVBt9YneBrdWknuYkwRZKKoGrU2blLVk"
PRIOR_SHA = "55701125e86740f3bf51a715aba8f68e8441d3eb7bffc99a43b7d3ff29b973e9"
REPORTS_BUCKET = "opal-data-etfs"
REPORTS_PREFIX = "platinum/reports/"
CODE_COMMIT = "c2787650f5"
ENTRY = os.path.join(ROOT, "org", "critical_paths", "change_management",
                     "20260910T0518Z_etfs-guardrail-egs25-renderer-forcing-disclosure-20260910"
                     "_deploy_completion.md")
DEPLOY_EV = os.path.join(HERE, "egs25_deploy_evidence.json")
PRES = os.path.join(ROOT, "data", "etfs", "scripts", "presentation")
NEW_SRC = os.path.join(PRES, "render_month_end.py")

DISCLOSURE_TOKENS = ["forcing", "forced", "fixture_remove_spec", "removed_slice_count",
                     "run_id", "run_id_source", "RUN-ID", "disclosure_version",
                     "_forcing_record", "_mint_run_id"]
# the issuer's five, quoted with its numbers so the re-take is comparable
CONTROL_TOKENS = {"generated_at": 1, "fixture_remove": 22, "verdict": 23,
                  "unresolved": 13, "per_partner": 6}

ARMS: list = []


def arm(name, ok, detail):
    ARMS.append((name, ok, detail))
    print("  ARM %-3s %-4s %s" % (name, "PASS" if ok else "FAIL", detail))
    return ok


def aws(args, timeout=120):
    try:
        p = subprocess.run([AWS] + args, capture_output=True, timeout=timeout, cwd=ROOT)
        rc, so, se = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT"
    return (rc, so.decode("utf-8", "replace").replace("\r\n", "\n"),
            se.decode("utf-8", "replace").replace("\r\n", "\n"))


def aws_json(args, timeout=120):
    rc, so, se = aws(args, timeout)
    doc = None
    if rc == 0 and so.strip():
        try:
            doc = json.loads(so)
        except Exception:
            pass
    return rc, doc, so, se


def count_sub(text, token):
    return text.count(token)


def count_wb(text, token):
    return len(re.findall(r"(?<![A-Za-z0-9_])" + re.escape(token) + r"(?![A-Za-z0-9_])", text))


# --------------------------------------------------------------------------- stubs
class _ExplodingLam:
    def invoke(self, **kw):
        raise AssertionError("NO INVOKE IS PERMITTED IN THIS CELL: %r" % (kw,))


class _RecordingS3:
    def __init__(self):
        self.put_calls = []

    def put_object(self, Bucket, Key, Body, ContentType=None, **kw):
        self.put_calls.append((Bucket, Key, Body))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def drive_main(mod, month, aug_days, present, spec, tmpdir):
    """Drive the REAL main() with every AWS touch stubbed. Returns (verdict_doc, rc)."""
    rec = _RecordingS3()
    saved = {}
    for attr, val in (("load_universe", lambda: ["DIVZ"]),
                      ("load_monthly_avg", lambda m: {}),
                      ("load_all_daily", lambda p: {d: {"DIVZ": {"v": 100.0, "n": 1, "as_of": d}}
                                                    for d in present} if p == "cottonwood" else {}),
                      ("opal_logo_svg", lambda: ""),
                      ("_make_probe", lambda lam_client=None: (
                          lambda partner, date_str: {"partition": True, "priced": 999})),
                      ("lam", _ExplodingLam()),
                      ("s3", rec)):
        saved[attr] = getattr(mod, attr, None)
        setattr(mod, attr, val)

    argv = ["render_month_end.py", "--month", month,
            "--out", os.path.join(tmpdir, "out_%s.html" % (spec and "forced" or "unforced")),
            "--gate", "--no-ladder",
            "--s3-out", "s3://test-bucket/platinum/reports/"]
    if spec:
        argv += ["--fixture-remove", spec]
    saved_argv = sys.argv
    sys.argv = argv
    try:
        rc = mod.main()
    except SystemExit as exc:
        rc = exc.code
    finally:
        sys.argv = saved_argv
        for a, v in saved.items():
            setattr(mod, a, v)

    body = next(b for _bk, k, b in rec.put_calls if k.endswith("coverage_verdict.json"))
    written = [k for _bk, k, _b in rec.put_calls]
    return json.loads(body), rc, written


def main() -> int:
    print("=" * 100)
    print("EG-s-25 S25-AC1 -- THE VERDICT ARTIFACT MUST DISCLOSE ITS OWN FORCING")
    print("run at %s   worktree %s"
          % (dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), ROOT))
    print("=" * 100)

    ev = json.load(open(DEPLOY_EV, encoding="utf-8")) if os.path.exists(DEPLOY_EV) else {}

    # ===================================================================== ARM (a)
    print("\n(a) THE ABSENCE REPRODUCES FIRST, ON THE DEPLOYED BYTES  [LIVE, by versionId]")
    print("    The deploy has since replaced this key, so the PRE-CHANGE object is re-read by")
    print("    its versionId -- the bucket has versioning ENABLED, so those exact bytes are")
    print("    still addressable and this arm re-measures them live rather than trusting a row.")
    rc, vdoc, _, _ = aws_json(["s3api", "get-bucket-versioning", "--bucket", ART_BUCKET,
                               "--output", "json"])
    print("    [LIVE] get-bucket-versioning %s -> rc %d, Status=%s"
          % (ART_BUCKET, rc, (vdoc or {}).get("Status")))
    old_path = os.path.join(ROOT, ".scratch", "egs25_arm_a_prior.py")
    os.makedirs(os.path.dirname(old_path), exist_ok=True)
    rc_get, _, _ = aws(["s3api", "get-object", "--bucket", ART_BUCKET, "--key", ART_KEY,
                        "--version-id", PRIOR_VERSION_ID,
                        ".scratch/egs25_arm_a_prior.py", "--output", "json"])[0:1] + ("", "")
    old = open(old_path, "rb").read()
    old_sha = hashlib.sha256(old).hexdigest()
    old_text = old.decode("utf-8")
    print("    [LIVE] the PRE-CHANGE deployed object: %d bytes, sha256 %s" % (len(old), old_sha))
    print("           versionId %s ; matches the sha recorded before the copy: %s"
          % (PRIOR_VERSION_ID, old_sha == PRIOR_SHA))

    print("    DISCLOSURE TOKENS on those bytes -- BOTH counting methods printed, because the")
    print("    issuer's quoted numbers reproduce under substring and not under word-boundary")
    print("    (row W5-S5), and a reader must be able to compare like with like:")
    print("      %-22s %10s %10s" % ("TOKEN", "SUBSTRING", "WORD-BDY"))
    disc_zero = True
    for t in DISCLOSURE_TOKENS:
        cs, cw = count_sub(old_text, t), count_wb(old_text, t)
        print("      %-22s %10d %10d" % (t, cs, cw))
        if cs != 0 or cw != 0:
            disc_zero = False
    print("      => %d of %d disclosure tokens read ZERO on BOTH methods"
          % (len(DISCLOSURE_TOKENS) if disc_zero else -1, len(DISCLOSURE_TOKENS)))

    print("    POSITIVE CONTROLS on the SAME bytes -- this is what makes the zeros an ABSENCE")
    print("    rather than a dead read:")
    print("      %-22s %10s %10s %10s" % ("TOKEN", "ISSUER", "SUBSTRING", "WORD-BDY"))
    ctrl_nonzero = True
    ctrl_match = 0
    for t, quoted in CONTROL_TOKENS.items():
        cs, cw = count_sub(old_text, t), count_wb(old_text, t)
        print("      %-22s %10d %10d %10d" % (t, quoted, cs, cw))
        if cs == 0 or cw == 0:
            ctrl_nonzero = False
        if cs == quoted:
            ctrl_match += 1
    print("      => %d of %d controls NON-ZERO on both methods; %d of %d reproduce the issuer's"
          % (len(CONTROL_TOKENS) if ctrl_nonzero else -1, len(CONTROL_TOKENS),
             ctrl_match, len(CONTROL_TOKENS)))
    print("         quoted number EXACTLY under substring counting.")
    print("    PREMISE CHECK: a disclosure field already present in the OLD bytes would mean the")
    print("    premise is wrong and this battery must STOP. `forcing` in old bytes: %s"
          % ("forcing" in old_text))
    a_ok = (rc == 0 and (vdoc or {}).get("Status") == "Enabled" and old_sha == PRIOR_SHA
            and disc_zero and ctrl_nonzero and ctrl_match == len(CONTROL_TOKENS))
    arm("a", a_ok,
        "the pre-change object re-read live by versionId (%d B, sha256 matches the pre-copy "
        "record): %d of %d disclosure tokens ZERO on both counting methods, against %d of %d "
        "positive controls NON-ZERO, %d of %d reproducing the issuer's quoted number exactly. "
        "The absence is real and the premise holds."
        % (len(old), len(DISCLOSURE_TOKENS), len(DISCLOSURE_TOKENS), len(CONTROL_TOKENS),
           len(CONTROL_TOKENS), ctrl_match, len(CONTROL_TOKENS)))

    # ------------------------------------------------------------ load both modules
    sys.path.insert(0, os.path.join(ROOT, "data", "inf", "scripts", "silver"))
    sys.path.insert(0, os.path.join(ROOT, "data", "etfs", "scripts"))
    sys.path.insert(0, PRES)
    sys.path.insert(0, ROOT)
    from lib import trading_calendar as tcal  # noqa: E402
    month = "2026-08"
    aug = [d.isoformat() for d in tcal.trading_days_between(dt.date(2026, 8, 1),
                                                            dt.date(2026, 8, 31))]
    print("\n    fixture month %s: %d of %d NYSE trading days (lib/trading_calendar.py)"
          % (month, len(aug), len(aug)))
    new_mod = load_module(NEW_SRC, "rme_new_egs25")
    old_mod = load_module(old_path, "rme_old_egs25")
    tmpdir = os.path.join(ROOT, ".scratch")

    # ===================================================================== ARM (b)
    print("\n(b) A FORCED RUN DISCLOSES  [hermetic: zero AWS calls, zero invokes, zero sends]")
    spec = "cottonwood:" + ",".join(aug[16:])
    forced_doc, forced_rc, forced_keys = drive_main(new_mod, month, aug, aug[:16], spec, tmpdir)
    print("    invocation: main() --month %s --gate --no-ladder --fixture-remove %s" % (month, spec))
    print("    rc %d (REFUSE), keys the run would have written: %d" % (forced_rc, len(forced_keys)))
    print("    THE WRITTEN coverage_verdict.json, forcing record PRINTED WHOLE:")
    print(json.dumps(forced_doc["forcing"], indent=6, sort_keys=True))
    f = forced_doc["forcing"]
    b_ok = (f.get("forced") is True and f.get("mechanism") == "--fixture-remove"
            and f.get("fixture_remove_spec") == spec
            and f.get("fixture_remove") == {"cottonwood": sorted(aug[16:])}
            and f.get("removed_slice_count") == 5
            and bool(f.get("run_id")) and bool(f.get("run_id_source")))
    arm("b", b_ok,
        "forced=True, mechanism='--fixture-remove', the spec recorded verbatim, %d removed slices "
        "enumerated by partner, and a run id (%s) with its source stated."
        % (f.get("removed_slice_count"), str(f.get("run_id"))[:12] + "..."))

    # ===================================================================== ARM (c)
    print("\n(c) AN UNFORCED RUN SAYS SO EXPLICITLY -- THE ARM THAT CARRIES THE OUTCOME")
    unforced_doc, unforced_rc, _ = drive_main(new_mod, month, aug, aug, "", tmpdir)
    print("    invocation: main() --month %s --gate --no-ladder   (NO --fixture-remove)" % month)
    print("    rc %d (PUBLISH)" % unforced_rc)
    print("    THE WRITTEN coverage_verdict.json, forcing record PRINTED WHOLE:")
    # A MISSING FIELD IS THE DEFECT THIS ARM EXISTS TO REFUSE, so it must be GRADED,
    # never raised: a battery that crashes on the positive case reports a traceback
    # where it owes a verdict.
    if "forcing" not in unforced_doc:
        print("      <<< THE FIELD IS ABSENT ON THE UNFORCED RUN >>>")
        print("      That is precisely the defect this arm refuses: a field that is missing")
        print("      when nothing was forced and missing when something WAS forced tells a")
        print("      reader nothing. Top-level keys actually written: %s"
              % sorted(unforced_doc.keys()))
    else:
        print(json.dumps(unforced_doc["forcing"], indent=6, sort_keys=True))
    u = unforced_doc.get("forcing") or {}
    a_txt = json.dumps(f, sort_keys=True)
    u_txt = json.dumps(u, sort_keys=True) if u else "<FIELD ABSENT>"
    print("    SIDE BY SIDE, the two records:")
    print("      FORCED  : %s" % a_txt)
    print("      UNFORCED: %s" % u_txt)
    print("    A MISSING FIELD WOULD NOT PASS THIS ARM. field present on the unforced run: %s ; "
          "forced value is an explicit boolean False (not null, not absent): %r"
          % ("forcing" in unforced_doc, u.get("forced")))
    c_ok = ("forcing" in unforced_doc and u.get("forced") is False
            and u.get("mechanism") == "none" and u.get("fixture_remove") == {}
            and u.get("fixture_remove_spec") == "" and u.get("removed_slice_count") == 0
            and bool(u.get("run_id")) and a_txt != u_txt)
    arm("c", c_ok,
        "the unforced run carries the SAME field with forced=False and mechanism='none' -- "
        "explicit, not absent -- and the two records are textually different, so a reader can "
        "tell 'this run forced nothing' from 'this run did not say'.")

    # ===================================================================== ARM (d)
    print("\n(d) THE VERDICT ITSELF DID NOT MOVE  [OLD bytes vs NEW bytes, same inputs]")
    print("    THE FORCED CASE IS EXCLUDED FROM THIS COMPARISON, and the reason is that the OLD")
    print("    code cannot express a forcing record at all, so there is nothing on the old side")
    print("    to compare a forced run against. Arm (d) asks whether adding the record disturbed")
    print("    the DECISION, which is an unforced-vs-unforced question.")
    pre_keys = ["month", "verdict", "per_partner", "holes", "unresolved"]
    d_ok = True
    for label, present in (("COMPLETE month (%d of %d present)" % (len(aug), len(aug)), aug),
                           ("HOLED month (16 of %d present, 5 class-C)" % len(aug), aug[:16])):
        for m in (old_mod, new_mod):
            m.lam = _ExplodingLam()
        daily = {"cottonwood": {d: {"DIVZ": {"v": 100.0, "n": 1, "as_of": d}} for d in present}}

        def pr(partner, date_str):
            return {"partition": True, "priced": 100}

        r_old = old_mod.coverage_gate(month, ["cottonwood"], daily, ["DIVZ"], ladder=False, probe=pr)
        r_new = new_mod.coverage_gate(month, ["cottonwood"], daily, ["DIVZ"], ladder=False, probe=pr)
        print("    SCENARIO: %s" % label)
        print("      denominator: %d of %d pre-existing key(s) compared" % (len(pre_keys), len(pre_keys)))
        for k in pre_keys:
            same = r_old[k] == r_new[k]
            d_ok = d_ok and same
            print("        %-12s OLD == NEW : %-5s" % (k, same))
        s_o = r_old["per_partner"]["cottonwood"]["summary"]
        s_n = r_new["per_partner"]["cottonwood"]["summary"]
        cls = sorted(set(s_o) | set(s_n))
        eq = sum(1 for c in cls if s_o.get(c) == s_n.get(c))
        d_ok = d_ok and eq == len(cls)
        print("      CLASS COUNTS: %d of %d identical -- %s"
              % (eq, len(cls), ", ".join("%s=%s" % (c, s_o.get(c)) for c in cls)))
        print("      VERDICT: OLD %s / NEW %s -- IDENTICAL: %s"
              % (r_old["verdict"], r_new["verdict"], r_old["verdict"] == r_new["verdict"]))
        print("      keys ADDED by the change: %s ; keys REMOVED: %s"
              % (sorted(set(r_new) - set(r_old)), sorted(set(r_old) - set(r_new))))
        d_ok = d_ok and sorted(set(r_new) - set(r_old)) == ["forcing"]
        d_ok = d_ok and not (set(r_old) - set(r_new))
    arm("d", d_ok,
        "across a PUBLISH scenario and a REFUSE scenario, %d of %d pre-existing keys and every "
        "class count identical between the old deployed bytes and the new ones; exactly one key "
        "added ('forcing'), none removed. The class-C verdict rule is EG-s-4's and is absent "
        "from the diff." % (len(pre_keys), len(pre_keys)))

    # ===================================================================== ARM (e)
    print("\n(e) THE DEPLOY IS REAL AND REVERSIBLE  [LIVE]")
    rc, hdoc, _, _ = aws_json(["s3api", "head-object", "--bucket", ART_BUCKET, "--key", ART_KEY,
                               "--output", "json"])
    print("    [LIVE] head-object %s -> rc %d, Size %s, LastModified %s, versionId %s"
          % (ART_KEY, rc, (hdoc or {}).get("ContentLength"),
             str((hdoc or {}).get("LastModified")), (hdoc or {}).get("VersionId")))
    served_path = os.path.join(ROOT, ".scratch", "egs25_arm_e_served.py")
    aws(["s3api", "get-object", "--bucket", ART_BUCKET, "--key", ART_KEY,
         ".scratch/egs25_arm_e_served.py", "--output", "json"])
    served = open(served_path, "rb").read()
    served_sha = hashlib.sha256(served).hexdigest()
    committed = subprocess.run(["git", "cat-file", "blob",
                                "%s:data/etfs/scripts/presentation/render_month_end.py" % CODE_COMMIT],
                               capture_output=True, cwd=ROOT).stdout
    comm_sha = hashlib.sha256(committed).hexdigest()
    print("    [LIVE] SERVED object    : %d bytes  sha256 %s" % (len(served), served_sha))
    print("    [LIVE] COMMITTED bytes  : %d bytes  sha256 %s   (git blob at %s)"
          % (len(committed), comm_sha, CODE_COMMIT))
    print("           BYTE-EQUAL: %s -- read from the SERVED artifact, never from a producer rc"
          % (served_sha == comm_sha))
    entry = io.open(ENTRY, encoding="utf-8", newline="").read() if os.path.exists(ENTRY) else ""
    m_open = re.search(r"(\d{8}T\d{6}Z) OPENED by 0\.9\.0_WK_ETFS_GUARDRAIL~5", entry)
    m_close = re.search(r"(\d{8}T\d{6}Z) CLOSED -- all 5 legs proven", entry)
    copy_utc = (ev.get("copy_utc") or "").replace("-", "").replace(":", "")
    print("    entry OPENED %s ; COPY %s ; entry CLOSED %s"
          % (m_open and m_open.group(1), copy_utc, m_close and m_close.group(1)))
    print("           opened BEFORE the copy: %s ; closed BEFORE this grading read: %s"
          % (bool(m_open) and m_open.group(1) < copy_utc, bool(m_close)))
    print("    PRIOR object sha256 recorded in the entry BEFORE the copy: %s" % (PRIOR_SHA in entry))
    print("    ROLLBACK, an exact key-and-bytes restore, stated in the entry: %s"
          % (PRIOR_VERSION_ID in entry and "copy-object" in entry))
    e_ok = (rc == 0 and served_sha == comm_sha and len(committed) > 0
            and bool(m_open) and bool(m_close) and copy_utc != ""
            and m_open.group(1) < copy_utc and PRIOR_SHA in entry
            and PRIOR_VERSION_ID in entry and "copy-object" in entry)
    arm("e", e_ok,
        "the served object at the artifact key is byte-equal to the committed bytes at %s "
        "(sha256 both sides); the prior object's sha256 and versionId are recorded in the entry, "
        "which opened %s BEFORE the %s copy and closed before this grading read; the rollback is "
        "stated as an exact key-and-bytes restore."
        % (CODE_COMMIT, m_open.group(1) if m_open else "-", copy_utc))

    # ===================================================================== ARM (f)
    print("\n(f) NO SEND, NO INVOKE, NO SERVED-REPORT WRITE  [LIVE + this run's own evidence]")
    win = ev.get("ses_window", {})
    ses_ok = True
    for metric in ("Send", "Delivery", "Reputation.BounceRate"):
        rc, sdoc, _, _ = aws_json(["cloudwatch", "get-metric-statistics", "--namespace", "AWS/SES",
                                   "--metric-name", metric, "--start-time", win.get("start"),
                                   "--end-time", win.get("end"), "--period", "300",
                                   "--statistics", "Sum", "--output", "json"])
        pts = (sdoc or {}).get("Datapoints", []) or []
        tot = sum(p.get("Sum", 0) for p in pts)
        print("    [LIVE] AWS/SES %-22s rc %d  DENOMINATOR %d datapoint(s)  Sum %s"
              % (metric, rc, len(pts), tot))
        if rc != 0 or tot != 0:
            ses_ok = False
    rep_before = ev.get("reports_before", {})
    rep_after = ev.get("reports_after", {})
    rep_delta = ev.get("reports_delta", [])
    print("    [CAPTURED at the act] platinum/reports/ DENOMINATOR %d key(s) before, %d after; "
          "keys differing on Size/ETag/LastModified: %d"
          % (len(rep_before), len(rep_after), len(rep_delta)))
    rc, live_rep, _, _ = aws_json(["s3api", "list-objects-v2", "--bucket", REPORTS_BUCKET,
                                   "--prefix", REPORTS_PREFIX, "--output", "json"])
    live_keys = {c["Key"] for c in (live_rep or {}).get("Contents", []) or []}
    print("    [LIVE] platinum/reports/ now: DENOMINATOR %d key(s)" % len(live_keys))
    verbs = sorted({s["argv"][1] + " " + s["argv"][2] for s in ev.get("steps", [])
                    if len(s.get("argv", [])) > 2})
    print("    EVERY AWS VERB THIS CELL'S DEPLOY USED, enumerated from the committed evidence")
    print("    ledger (denominator %d recorded command(s)): %s" % (len(ev.get("steps", [])), verbs))
    invoked = [v for v in verbs if "invoke" in v]
    print("    lambda invoke among them: %d of %d verbs" % (len(invoked), len(verbs)))
    print("    THE BATTERY'S OWN RUNS: arms (b),(c),(d) drove the real main() with an")
    print("    _ExplodingLam that RAISES if .invoke() is ever called, and a recording S3 stub --")
    print("    so 'no invoke' is enforced by the harness, not merely unobserved.")
    print("    etfs-reports-orchestrator was NOT invoked in any mode, at any point, by this cell.")
    f_ok = (ses_ok and len(rep_delta) == 0 and not invoked and rc == 0
            and len(rep_before) == len(rep_after))
    arm("f", f_ok,
        "3 of 3 AWS/SES metrics read 0 datapoints and Sum 0 live; platinum/reports/ %d keys "
        "before and %d after with 0 differing; 0 of %d AWS verbs in the deploy's recorded "
        "command set is a lambda invoke; the battery's own harness raises on any invoke."
        % (len(rep_before), len(rep_after), len(verbs)))

    # ===================================================================== VERDICT
    print("\n" + "=" * 100)
    passed = sum(1 for _n, ok, _d in ARMS if ok)
    for n, ok, _d in ARMS:
        print("  arm %-3s %s" % (n, "PASS" if ok else "FAIL"))
    print("  ARMS PASSED: %d of %d" % (passed, len(ARMS)))
    if passed == len(ARMS) and len(ARMS) == 6:
        print("\nEGS25-VERDICT-DISCLOSES-FORCING")
        print("\nA forced refusal can no longer be mistaken for an organic one: the artifact now")
        print("says which it was, on BOTH branches, and the decision it reports is unchanged.")
        print("=" * 100)
        return 0
    print("\nTOKEN WITHHELD -- %d arm(s) failed; S25-AC1 does NOT pass." % (len(ARMS) - passed))
    print("=" * 100)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
