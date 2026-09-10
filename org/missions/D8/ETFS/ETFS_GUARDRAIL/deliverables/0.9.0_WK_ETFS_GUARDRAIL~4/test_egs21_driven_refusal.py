#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-21 -- S21-AC1 battery, FOURTH seating (EG-s-27 + EG-s-29 terminal).

IT DOES NOT INVOKE THE ORCHESTRATOR AND FIRES NO SEND. Every AWS call is a READ:
lambda:GetFunction(+Configuration), an HTTPS GET of the presigned code location,
s3:GetObject / HeadObject / ListObjectsV2, and ONE read-only producer PROBE invoke
(cot-etf-ownership-daily {"date": d, "probe": true} -- infra/aws/lambda/cot-pipeline/
cot-etf-ownership-daily/lambda_function.py:285-294 `_probe`, "Never reaches
put_object"), whose write-freeness is CONTROLLED here by an ETag read before and
after. The served renderer is executed in-process with `s3` replaced by a
capture-only stub, so `coverage_gate`'s put_object calls are RECORDED, never sent.

WHAT CHANGED SINCE THE THIRD SEATING, AND IT IS REAL:
  * EG-s-27 threaded `--no-ladder` beside the forcing, so the forcing now REACHES
    THE VERDICT instead of dying at the ladder's re-classify.  ARM (b) measures it
    on the SERVED orchestrator.
  * EG-s-29 made the ladder-skipped branch write a RUNG-3-EQUIVALENT egress ask.
    ARM (d) measures it on the SERVED renderer.
  * R-EG-8 re-cut S21-AC1 arm (d) to name the PROPERTY (an egress ask RECORDED for
    the run) instead of one writer of it.

AND THE ORDER IS STILL NOT EXECUTABLE, ON NEW GROUND ONE GRAIN ABOVE THE CRITERION.
S21-AC1 arm (d) and PRD v0.5 FWD-9's ACCEPT both require, of the driven run's month,
that "the publish keys for that month STAY ABSENT (a 404 beside the refused 200)".
ARM (e) is a CENSUS BY SUBTRACTION over the month space:

    candidate months = {months for which ANY partner daily slice exists}
                       (the fixture can only remove a slice that EXISTS, so a month
                        with no slice cannot carry a FORCED class C at all)
    = exactly {2026-05 .. 2026-09}, measured, 0 slices outside that range
    and 5 of those 5 months ALREADY SERVE platinum/reports/<month>/etf_ownership.pdf
    AND .html -- so 0 of 5 can produce the 404 the accept names.

There is therefore NO month in which a driven run can satisfy arm (d), and the
single permitted run is NOT spent on one that cannot. That is a BLOCKING row
(ETFS_GUARDRAIL-W4-S8), not a licence to re-read the arm more kindly.

Prints EGS21-BLOCKED-NO-MONTH-CAN-SATISFY-FWD9-404. It cannot print the success token.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import importlib.util
import io
import json
import os
import sys
import types
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
FUNCTION = "etfs-reports-orchestrator"
REGION = "us-east-1"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "ec2/etfs-reports/render_month_end.py"
ETFS_BUCKET = "opal-data-etfs"
REPORTS_PREFIX = "platinum/reports"
PARTNERS = ("cottonwood", "49financial", "inflection")

# The month/partner/date this order WOULD have driven, chosen in the result document
# and re-derived by ARM (e) here: the only month whose unforced verdict is PUBLISH,
# whose forced partner has a slice to remove, and which serves NO coverage artifact
# that the run would overwrite.
CAND_MONTH, CAND_PARTNER, CAND_DATE = "2026-07", "cottonwood", "2026-07-15"
COT_PRODUCER = "cot-etf-ownership-daily"

BLOCKERS: list = []
ARMS: dict = {}


def head(t):
    print("")
    print("=" * 78)
    print(t)
    print("=" * 78)


def line(tag, msg):
    print("  [%s] %s" % (tag, msg))


def arm(name, ok, msg):
    ARMS[name] = ok
    line("HOLD" if ok else "BLOCKED", "%s -- %s" % (name, msg))
    if not ok:
        BLOCKERS.append("%s: %s" % (name, msg))


_lam = boto3.client("lambda", region_name=REGION)
_s3 = boto3.client("s3", region_name=REGION)
STARTED = datetime.datetime.now(datetime.timezone.utc).isoformat()
print("battery started (UTC): %s" % STARTED)
print("worktree HEAD is the branch's; every claim below is measured at this run's time.")

# =====================================================================================
head("(a) THE PRECONDITION, re-taken at THIS run's time on the CURRENT deployed bytes")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zb = urllib.request.urlopen(fn["Code"]["Location"]).read()
ORCH = zipfile.ZipFile(io.BytesIO(zb)).read("lambda_function.py")
ORCH_SHA = hashlib.sha256(ORCH).hexdigest()
print("served CodeSha256   : %s" % CONF["CodeSha256"])
print("served LastModified : %s" % CONF["LastModified"])
print("zip member          : %d B sha256 %s" % (len(ORCH), ORCH_SHA))
print("zip sha256 (b64)    : %s" % base64.b64encode(hashlib.sha256(zb).digest()).decode())
print("live EMAIL_RECIPIENT: %s" % CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"])
print("EG-s-20 terminal    : <status>complete -- 2026-09-10 ~04:0xZ by "
      "0.9.0_WK_ETFS_GUARDRAIL~4</status>, drained 5d292ff11f "
      "(org/missions/D8/ETFS/ETFS_GUARDRAIL/task-orders/"
      "ETFS_GUARDRAIL.TO-EG-s-20.the-send-path-correct-and-test-safe.md)")


class _Stub:
    """Every AWS client the orchestrator module builds at import. Any call RAISES --
    a battery that silently invoked would be worse than one that crashes."""

    def __init__(self, svc):
        self._svc = svc

    def __getattr__(self, n):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: %s.%s -- this battery invokes nothing"
                                 % (self._svc, n))
        return _c


op = os.path.join(REPO, ".scratch", "egs21d_orch.py")
os.makedirs(os.path.dirname(op), exist_ok=True)
io.open(op, "wb").write(ORCH)
_real = boto3.client
boto3.client = lambda service, **kw: _Stub(service)
os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")
os.environ["EMAIL_RECIPIENT"] = CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"]
_sp = importlib.util.spec_from_file_location("egs21d_orch", op)
ORCHM = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(ORCHM)
boto3.client = _real

EVENTS = [
    {"mode": "run", "month": CAND_MONTH, "test_run": True},
    {"mode": "run", "month": CAND_MONTH, "test_run": True,
     "force_fixture_remove": "%s:%s" % (CAND_PARTNER, CAND_DATE)},
    {"mode": "run", "test_run": True, "test_recipients": ["aj@opalinvest.com"]},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com,andrew@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": ["AJ@OpalInvest.COM"]},
    {"mode": "run", "test_run": True, "test_recipients": ["  aj@opalinvest.com  "]},
    {"mode": "run", "test_run": True, "test_recipients": []},
    {"mode": "run", "test_run": True, "test_recipients": None},
    {"mode": "run", "test_run": 1, "month": CAND_MONTH},
]
leak, n = 0, 0
for ev in EVENTS:
    for base in (ORCHM.EMAIL_RECIPIENT, ORCHM.TERMINAL_RECIPIENT):
        h, env = ORCHM._resolve_recipients(ev, base)
        n += 1
        if any(a.lower() == "aj@opalinvest.com" for a in env) or "aj@" in h.lower():
            leak += 1
_, sched_env = ORCHM._resolve_recipients({"mode": "run"}, ORCHM.EMAIL_RECIPIENT)
_, term_env = ORCHM._resolve_recipients(
    {"mode": "run", "month": CAND_MONTH, "test_run": True,
     "force_fixture_remove": "%s:%s" % (CAND_PARTNER, CAND_DATE)},
    ORCHM.TERMINAL_RECIPIENT)
print("scheduled envelope (must stay BOTH): %s" % sched_env)
print("the driven run's TERMINAL envelope  : %s" % term_env)
arm("(a) PRECONDITION", leak == 0
    and sched_env == ["aj@opalinvest.com", "andrew@opalinvest.com"]
    and term_env == ["andrew@opalinvest.com"],
    "aj@opalinvest.com in %d of %d resolved test-invocation recipient lists on the bytes "
    "deployed at %s; the scheduled path is unchanged; the driven run's terminal envelope "
    "resolves to %s" % (leak, n, CONF["LastModified"], term_env))

# =====================================================================================
head("(b) THE TWO UNBLOCKING CELLS ARE ON THE SERVED BYTES -- EG-s-27 and EG-s-29")
# =====================================================================================
REND_HEAD = _s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
REND = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)["Body"].read()
REND_SHA = hashlib.sha256(REND).hexdigest()
RTEXT = REND.decode("utf-8")
RL = RTEXT.split("\n")
print("SERVED renderer : %d B sha256 %s" % (len(REND), REND_SHA))
print("                  VersionId %s LastModified %s"
      % (REND_HEAD.get("VersionId"), REND_HEAD["LastModified"].astimezone(
          datetime.timezone.utc).isoformat()))
repo_rend = io.open(os.path.join(REPO, "data", "etfs", "scripts", "presentation",
                                 "render_month_end.py"), "rb").read()
print("REPO  renderer  : %d B sha256 %s  -- CONTENT-RESOLVED MATCH: %s"
      % (len(repo_rend), hashlib.sha256(repo_rend).hexdigest(),
         hashlib.sha256(repo_rend).hexdigest() == REND_SHA))

forced_cmd = ORCHM._render_command(CAND_MONTH, "%s:%s" % (CAND_PARTNER, CAND_DATE))[0]
plain_cmd = ORCHM._render_command(CAND_MONTH, "")[0]
tail = forced_cmd[forced_cmd.index("render_month_end.py --month"):]
print("the command a FORCED test invoke would send:")
print("    %s" % tail)
ask_sites = [i for i, x in enumerate(RL, 1) if "_skipped_branch_egress_ask(" in x]
basename_ok = "coverage_egress_ask_ladder_skipped.json" in RTEXT
arm("(b) DEPENDENCIES SERVED",
    "--fixture-remove" in forced_cmd and "--no-ladder" in forced_cmd
    and "--no-ladder" not in plain_cmd and len(ask_sites) >= 2 and basename_ok,
    "EG-s-27: --no-ladder present in the FORCED command and absent from the marker-free "
    "one; EG-s-29: _skipped_branch_egress_ask at %s (denominator %d) and the "
    "ladder-skipped basename present on the served renderer"
    % (ask_sites, len(ask_sites)))

# =====================================================================================
head("(c) THE FORCING NOW REACHES THE VERDICT -- difference control on SERVED bytes")
# =====================================================================================
sys.path.insert(0, os.path.join(REPO, "data", "etfs", "scripts"))
sys.path.insert(0, os.path.join(REPO, "data", "inf", "scripts", "silver"))
import _orion_vendor_asof  # noqa: F401,E402
from coverage import classifier as CLS  # noqa: E402

# The classifier's own C-vs-D boundary, read at file:line so the class below is read
# against the RULE and not against my paraphrase of it.
cls_path = os.path.join(REPO, "data", "etfs", "scripts", "coverage", "classifier.py")
cls_lines = io.open(cls_path, encoding="utf-8").read().split("\n")
print("classifier.py @8471f83a18 -- the C-vs-D boundary, verbatim:")
for i in (177, 178, 179, 192, 193, 194):
    print("  :%-4d %s" % (i, cls_lines[i - 1].strip()))

# real series, read from S3 (presence only, exactly what classify_month reads)
pag = _s3.get_paginator("list_objects_v2")
series_all: dict = {}
for p in PARTNERS:
    ss = {}
    for pg in pag.paginate(Bucket=ETFS_BUCKET, Prefix="daily/%s/" % p):
        for o in pg.get("Contents", []):
            b = o["Key"].rsplit("/", 1)[-1]
            if b.endswith(".json") and len(b) == 15:
                ss[b[:-5]] = True
    series_all[p] = ss
print("daily slice census (denominator = objects listed): %s"
      % {p: len(series_all[p]) for p in PARTNERS})

# THE ONE REAL INVOKE IN THIS BATTERY, AND IT IS A READ. Controlled on both sides.
slice_key = "daily/%s/%s.json" % (CAND_PARTNER, CAND_DATE)
h_before = _s3.head_object(Bucket=ETFS_BUCKET, Key=slice_key)
_pr = _lam.invoke(FunctionName=COT_PRODUCER,
                  Payload=json.dumps({"date": CAND_DATE, "probe": True}).encode("utf-8"))
PROBE_ANSWER = json.loads(_pr["Payload"].read())
h_after = _s3.head_object(Bucket=ETFS_BUCKET, Key=slice_key)
print("REAL PROBE (read-only) %s <- {\"date\": %r, \"probe\": true}: %s"
      % (COT_PRODUCER, CAND_DATE, json.dumps(PROBE_ANSWER)))
print("  write-free control on %s: ETag %s -> %s  UNCHANGED=%s"
      % (slice_key, h_before["ETag"], h_after["ETag"],
         h_before["ETag"] == h_after["ETag"]))

_captured: list = []


class _CaptureS3:
    """Read-through list/get; put_object CAPTURED, never sent."""

    def get_paginator(self, name):
        return _s3.get_paginator(name)

    def get_object(self, **kw):
        return _s3.get_object(**kw)

    def head_object(self, **kw):
        return _s3.head_object(**kw)

    def list_objects_v2(self, **kw):
        return _s3.list_objects_v2(**kw)

    def put_object(self, **kw):
        _captured.append({k: v for k, v in kw.items() if k != "Body"}
                         | {"BodyLen": len(kw.get("Body") or b""),
                            "Body": kw.get("Body")})
        return {}


rp = os.path.join(REPO, ".scratch", "egs21d_rend.py")
io.open(rp, "wb").write(REND)
_capture = _CaptureS3()
_real2 = boto3.client
boto3.client = lambda service, **kw: _capture if service == "s3" else _Stub(service)
RM = types.ModuleType("egs21d_rend")
RM.__file__ = rp
sys.modules["egs21d_rend"] = RM
exec(compile(REND, rp, "exec"), RM.__dict__)
boto3.client = _real2
RM.s3 = _capture


def _probe_stub(partner, date_str):
    """The MEASURED answer above for the candidate date; None elsewhere (no partner
    other than cottonwood has an uncovered trading day in this month, so no other
    date reaches a probe -- see the coverage table printed by ARM (e))."""
    if partner == CAND_PARTNER and date_str == CAND_DATE:
        return {"partition": bool(PROBE_ANSWER.get("partition")),
                "priced": int(PROBE_ANSWER.get("priced", 0) or 0)}
    return None


RESULTS = {}
for engaged in (False, True):
    daily = {p: dict(series_all[p]) for p in PARTNERS}
    fixture = {CAND_PARTNER: [CAND_DATE]} if engaged else {}
    spec = "%s:%s" % (CAND_PARTNER, CAND_DATE) if engaged else ""
    RM._apply_fixture_remove(daily, fixture)
    _captured.clear()
    v = RM.coverage_gate(CAND_MONTH, list(PARTNERS), daily, ["DIVZ"], ladder=False,
                         probe=_probe_stub, fixture_remove=fixture,
                         fixture_remove_spec=spec,
                         run_id="EGS21-BATTERY-HERMETIC", run_id_source="battery")
    cs = {p: v["per_partner"][p]["summary"]["C"] for p in PARTNERS}
    RESULTS[engaged] = (v, list(_captured))
    print("  forcing %-10s ladder=False -> VERDICT=%-8s holes=%d C per partner=%s"
          % ("ENGAGED" if engaged else "DISENGAGED", v["verdict"], v["holes"], cs))

V_ON, CAP_ON = RESULTS[True]
V_OFF, CAP_OFF = RESULTS[False]
c_partners = [p for p in PARTNERS if V_ON["per_partner"][p]["summary"]["C"] > 0]
print("  forced per-partner class table (the object arm (c) would read):")
for p in PARTNERS:
    s = V_ON["per_partner"][p]["summary"]
    print("    %-12s %s | holes=%s" % (p, json.dumps(s), V_ON["per_partner"][p]["holes"]))
print("  forcing record on the forced verdict: %s" % json.dumps(V_ON["forcing"]))
arm("(c) FORCING REACHES THE VERDICT",
    V_ON["verdict"] == "REFUSE" and V_OFF["verdict"] == "PUBLISH" and len(c_partners) >= 1,
    "same served renderer, same month, same real series, same measured probe -- only the "
    "forcing differs: ENGAGED=%s (class C on %s) vs DISENGAGED=%s. This is the arm-(f) "
    "undo pair as well: removing the forcing returns the classifier to PUBLISH."
    % (V_ON["verdict"], c_partners, V_OFF["verdict"]))

# =====================================================================================
head("(d) THE EGRESS ASK WOULD BE RECORDED FOR THE RUN -- EG-s-29's rung-3-equivalent")
# =====================================================================================
ask_puts = [c for c in CAP_ON if "egress_ask" in c["Key"]]
print("  put_object calls CAPTURED (never sent) on the forced run: %d" % len(CAP_ON))
for c in CAP_ON:
    print("    %s  %d B" % (c["Key"], c["BodyLen"]))
ask_ok = False
if ask_puts:
    rec = json.loads(ask_puts[-1]["Body"])
    print("  the ask's provenance, verbatim from the bytes the run would write:")
    print("    written_by : %s" % rec.get("written_by"))
    print("    rung3_ran  : %s" % rec.get("rung3_ran"))
    print("    equivalent_of: %s" % rec.get("equivalent_of"))
    print("    asks       : %s" % json.dumps(rec.get("asks")))
    ask_ok = (rec.get("rung3_ran") is False
              and "RUNG-3-EQUIVALENT" in (rec.get("written_by") or "")
              and ask_puts[-1]["Key"].endswith("coverage_egress_ask_ladder_skipped.json"))
unres_providers = [r.get("provider") for rs in V_ON["unresolved"].values() for r in rs]
print("  unresolved rows' provider field (FWD-10 accept (ii)): %s of %s stated"
      % (len([p for p in unres_providers if p]), len(unres_providers)))
arm("(d) ASK LIMB", ask_ok and all(unres_providers),
    "an egress ask IS recorded for the run, at the ladder-skipped key, and its record "
    "says WHICH wrote it (rung3_ran=false); every unresolved row names its provider")

# =====================================================================================
head("(e) THE BLOCKER -- NO MONTH CAN SATISFY arm (d)'s 404 / FWD-9's 'STAY ABSENT'")
# =====================================================================================
print("FWD-9 ACCEPT, verbatim (org/missions/D8/ETFS/ETFS_GUARDRAIL/prd/"
      "ETFS_GUARDRAIL_PRD.md:566-567, restated at :187, @1d62717c65):")
print("  \"the verdict object reads REFUSE with the classifier's own class table quoted")
print("   at file:line, THE PUBLISH KEYS FOR THAT MONTH STAY ABSENT (a 404 beside the")
print("   refused 200), the refusal reaches a person, and the FORCING is disclosed\"")
print("")
print("THE CANDIDATE SET IS WRITTEN AS A SUBTRACTION FROM A PRINTED DENOMINATOR, never")
print("as a forward list (CLAUDE.md rule 24): a forced class C requires a slice the")
print("fixture can REMOVE, so the candidates are exactly the months in which some")
print("partner HAS a daily slice -- minus nothing.")
months = sorted({d[:7] for p in PARTNERS for d in series_all[p]})
total_slices = sum(len(series_all[p]) for p in PARTNERS)
print("  daily slices scanned: %d across %d partners -> months carrying a slice: %s"
      % (total_slices, len(PARTNERS), months))
print("  slices OUTSIDE that month range: %d"
      % len([d for p in PARTNERS for d in series_all[p] if d[:7] not in months]))

# auto-paginate, then count client-side: a single list_objects_v2 returns a PAGE and
# its length is a page count, not a denominator (CLAUDE.md, put the control on the
# retrieval). Written with the paginator rather than a hand-rolled continuation loop
# because .tools/ds-precommit-check.py false-BLOCKS the latter -- row W4-S12.
listed = []
for _page in _s3.get_paginator("list_objects_v2").paginate(
        Bucket=ETFS_BUCKET, Prefix=REPORTS_PREFIX + "/"):
    listed += _page.get("Contents", [])
print("  served keys under s3://%s/%s/ : %d (denominator)"
      % (ETFS_BUCKET, REPORTS_PREFIX, len(listed)))
keyset = {o["Key"]: o for o in listed}

print("")
print("  month   | pdf 200 | html 200 | 404-able | slice to force | unforced verdict")
print("  --------+---------+----------+----------+----------------+-----------------")
n_404 = 0
for m in months:
    pdf = "%s/%s/etf_ownership.pdf" % (REPORTS_PREFIX, m)
    htm = "%s/%s/etf_ownership.html" % (REPORTS_PREFIX, m)
    has_pdf, has_htm = pdf in keyset, htm in keyset
    can404 = (not has_pdf) and (not has_htm)
    n_404 += 1 if can404 else 0
    td = [d for d in CLS._month_dates(m) if CLS.tcal.is_trading_day(d)]
    forcible = [p for p in PARTNERS
                if any(d.isoformat() in series_all[p] for d in td)]
    gaps = {p: len([d for d in td if d.isoformat() not in series_all[p]])
            for p in PARTNERS}
    unforced = "PUBLISH (0 gaps)" if all(v == 0 for v in gaps.values()) \
        else "NOT PROVEN (gaps %s)" % gaps
    print("  %s | %-7s | %-8s | %-8s | %-14s | %s"
          % (m, has_pdf, has_htm, can404, ",".join(forcible)[:14], unforced))
arm("(e) A MONTH EXISTS THAT CAN SATISFY THE ACCEPT", n_404 > 0,
    "%d of %d months that can carry a FORCED class C serve NO publish key -- so the "
    "404 the accept names is unreachable in every one of them. The single permitted "
    "driven run is NOT spent on a run measured in advance to fail arm (d)."
    % (n_404, len(months)))

print("")
print("  WHAT THE RUN WOULD HAVE WRITTEN on %s, enumerated from the CAPTURED puts plus"
      % CAND_MONTH)
print("  render_month_end.main()'s REFUSE branch (:1305-1332 of the served file):")
for c in CAP_ON:
    print("    NEW  s3://%s/%s  (%d B, coverage_gate)"
          % (ETFS_BUCKET, c["Key"], c["BodyLen"]))
for k in ("%s/%s/coverage_verdict.json" % (REPORTS_PREFIX, CAND_MONTH),
          "%s/%s/coverage_unresolved.json" % (REPORTS_PREFIX, CAND_MONTH),
          "%s/%s/refused/etf_ownership.html" % (REPORTS_PREFIX, CAND_MONTH)):
    print("    %-4s s3://%s/%s" % ("NEW" if k not in keyset else "OVERWRITE",
                                   ETFS_BUCKET, k))
for p in ("49financial", "cottonwood", "inflection"):
    k = "%s/%s/refused/opaletfs_%s_%s.csv" % (REPORTS_PREFIX, CAND_MONTH, p,
                                              CAND_MONTH.replace("-", ""))
    print("    %-4s s3://%s/%s" % ("NEW" if k not in keyset else "OVERWRITE",
                                   ETFS_BUCKET, k))
print("    -- and the PUBLISH keys %s/%s/etf_ownership.{pdf,html} + the three "
      "opaletfs_*.csv ALREADY EXIST (LastModified 2026-09-01T17:38:05Z), which is "
      "exactly why the 404 cannot be produced." % (REPORTS_PREFIX, CAND_MONTH))

# =====================================================================================
head("(f) NOTHING WAS INVOKED, SENT, WRITTEN OR DELETED")
# =====================================================================================
print("  orchestrator invokes         : 0")
print("  SES sends                    : 0")
print("  SSM send_command             : 0")
print("  EC2 start/stop               : 0")
print("  S3 put_object / delete_object: 0 real (%d CAPTURED by the stub, never sent)"
      % (len(CAP_ON) + len(CAP_OFF)))
print("  producer invokes             : 1, read-only PROBE, ETag-controlled UNCHANGED=%s"
      % (h_before["ETag"] == h_after["ETag"]))
arm("(f) NO SIDE EFFECT", h_before["ETag"] == h_after["ETag"],
    "the only mutating capability exercised was the read-only probe, and its control "
    "shows the slice byte-identical before and after")

# =====================================================================================
head("VERDICT")
# =====================================================================================
held = [k for k, v in ARMS.items() if v]
print("arms: %d of %d HOLD" % (len(held), len(ARMS)))
for k, v in ARMS.items():
    print("  %-38s %s" % (k, "HOLD" if v else "BLOCKED"))
print("")
for b in BLOCKERS:
    print("BLOCKING: %s" % b)
print("")
print("NOTHING WAS INVOKED. NO SEND. NO S3 WRITE OR DELETE. EG-s-21's ONE RUN IS UNSPENT.")
print("battery ended (UTC): %s" % datetime.datetime.now(datetime.timezone.utc).isoformat())
print("")
if ARMS.get("(a) PRECONDITION") and ARMS.get("(b) DEPENDENCIES SERVED") \
        and ARMS.get("(c) FORCING REACHES THE VERDICT") and ARMS.get("(d) ASK LIMB") \
        and ARMS.get("(f) NO SIDE EFFECT") \
        and not ARMS.get("(e) A MONTH EXISTS THAT CAN SATISFY THE ACCEPT"):
    print("EGS21-BLOCKED-NO-MONTH-CAN-SATISFY-FWD9-404")
    sys.exit(2)
print("EGS21-INDETERMINATE -- the expected blocking shape did not hold; re-read the output")
sys.exit(1)
