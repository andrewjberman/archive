#!/usr/bin/env python3
"""MDPF_CANON round 7, cell CN-m-1 -- the issuer's checks for the READER CENSUS of the staged global aggregate.

Staged key: s3://opal-data-assets/gold/mdpf_revamp/global/aggregate_aua_timeseries.json (row MDPF_CANON-D1-W16-S5).

The worker's whole deliverable is ONE record, CN-m-1_READER_CENSUS.json (and a short .md beside it). This script grades its STRUCTURE and
re-derives its anchors from the live world. Read-only: no AWS write, no repo write.

  python r7_cn_m_1.py record  [--record PATH]   structure of the worker's census record (offline)
  python r7_cn_m_1.py verify  [--record PATH]   five live cross-checks of the record against the repo and AWS (read-only get/describe)
  python r7_cn_m_1.py selftest                  offline: a good record passes, five planted defects each turn a named arm red
  python r7_cn_m_1.py universe                  the repo scan's file list and denominator as JSON (the worker classifies each file)

Pass line: `CN-M-1 <MODE>: k of n arms` ; exit 0 only when k == n. Prints dates, counts and paths; never an account id.
"""
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
DEFAULT_RECORD = os.path.normpath(os.path.join(
    ROOT, "org/missions/D8/MDPF/MDPF_CANON/deliverables/0.9.0_WK_MDPF_CANON~20/CN-m-1_READER_CENSUS.json"))
KEY = "gold/mdpf_revamp/global/aggregate_aua_timeseries.json"
BUCKET = "opal-data-assets"
CLASSES = ("code", "scheduled", "iam_static", "iam_live", "trail")
SURFACES = ("NONE", "INTERNAL", "PARTNER-FACING-CANDIDATE", "PARTNER-FACING")
VERDICTS = ("READERS-FOUND", "ZERO-READERS-PROVEN", "ZERO-STATIC-READERS-RUNTIME-UNOBSERVED")
EXCLUDE_REASONS = ("PRODUCER-WRITE-ONLY", "TEST", "DECLARATIVE-ONLY", "COMMENT-ONLY", "OTHER-KEY", "SELF")
ANCHORS = (  # files the issuer's pre-read found to READ a staged aggregate key; the record must list each as a reader
    "data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py",
    "data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py",
    "data/mdpf/scripts/gold/build_portal_gold_accrual.py",
    "data/mdpf/scripts/gold/verify_mdpf_revamp_conditions.py",
)
SUF = (".py", ".sh", ".js", ".mjs", ".ts", ".tsx", ".yaml", ".yml", ".json", ".tf")
SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".scratch", "dist", "build"}
SCAN_TOPS = ("data", "infra", "lib", ".tools")
TRAILS = ("opal-organization-trail", "opal-served-key-write-trail")
SCHEDULE = "mdpf-accrual-bridge-daily"


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


# ---------------------------------------------------------------- record (structure) arms
def record_arms(rec):
    """Return [(arm_id, ok, detail)] for a loaded record. Pure function: the selftest plants defects into copies."""
    out = []
    cls = rec.get("classes") if isinstance(rec, dict) else None
    cls = cls if isinstance(cls, dict) else {}

    missing = [c for c in CLASSES if c not in cls]
    out.append(("M1 five reader classes present", not missing and rec.get("key") == f"s3://{BUCKET}/{KEY}",
                f"classes={sorted(cls)} missing={missing} key={rec.get('key')}"))

    bad = []
    for c in CLASSES:
        d = (cls.get(c) or {}).get("denominator")
        if not (isinstance(d, dict) and _is_int(d.get("scanned")) and d["scanned"] > 0 and d.get("unit")):
            bad.append(c)
    out.append(("M2 every class prints a denominator (scanned > 0 and a unit), also at count 0", not bad, f"classes without one={bad}"))

    mism = []
    for c in ("code", "scheduled", "iam_static"):
        blk = cls.get(c) or {}
        if not (_is_int(blk.get("count")) and isinstance(blk.get("readers"), list) and blk["count"] == len(blk["readers"])):
            mism.append(c)
    live = cls.get("iam_live") or {}
    st = live.get("states") if isinstance(live.get("states"), dict) else {}
    if not (_is_int(live.get("principals_checked")) and st and sum(v for v in st.values() if _is_int(v)) == live.get("principals_checked")
            and set(st) <= {"ALLOWED", "DENIED", "NOT-DECIDABLE"}):
        mism.append("iam_live")
    out.append(("M3 count equals the length of its list; iam_live states sum to principals_checked", not mism, f"inconsistent={mism}"))

    surf_bad = []
    readers = []
    for c in ("code", "scheduled", "iam_static"):
        for r in (cls.get(c) or {}).get("readers") or []:
            readers.append(r)
            if not (isinstance(r, dict) and r.get("id") and r.get("evidence") and r.get("surface") in SURFACES):
                surf_bad.append(str(r)[:60])
            elif r["surface"].startswith("PARTNER-FACING") and not r.get("output_key"):
                surf_bad.append(f"{r['id']} (surface {r['surface']} names no output_key)")
    out.append(("M4 every reader has id, evidence and a surface; a PARTNER-FACING surface names its output key", not surf_bad, f"bad={surf_bad[:4]}"))

    pf = sorted(r["id"] for r in readers if isinstance(r, dict) and str(r.get("surface", "")).startswith("PARTNER-FACING"))
    declared = sorted(rec.get("partner_facing") or [])
    out.append(("M5 partner_facing equals the ids whose surface starts PARTNER-FACING", pf == declared, f"derived={pf} declared={declared}"))

    trail = cls.get("trail") or {}
    trail_ok = (isinstance(trail.get("covered"), bool) and trail.get("evidence") and isinstance(trail.get("trails"), list)
                and isinstance(trail.get("server_access_logging"), bool))
    total = sum((cls.get(c) or {}).get("count", 0) for c in ("code", "scheduled", "iam_static") if _is_int((cls.get(c) or {}).get("count")))
    verdict = rec.get("verdict")
    v_ok = verdict in VERDICTS and rec.get("total_readers") == len(readers) and rec.get("zero_readers") == (len(readers) == 0)
    if verdict == "READERS-FOUND":
        v_ok = v_ok and len(readers) > 0
    if verdict == "ZERO-READERS-PROVEN":   # a zero is PROVEN only where runtime reads are observable
        v_ok = v_ok and len(readers) == 0 and trail.get("covered") is True
    if verdict == "ZERO-STATIC-READERS-RUNTIME-UNOBSERVED":
        v_ok = v_ok and len(readers) == 0 and trail.get("covered") is False
    out.append(("M6 trail coverage stated; the verdict is one the evidence permits (zero readers is PROVEN only on a covered trail)",
                bool(trail_ok) and v_ok, f"trail_ok={bool(trail_ok)} verdict={verdict} readers={len(readers)} counted={total} covered={trail.get('covered')}"))

    try:
        json.dumps(rec).encode("ascii")
        ascii_ok = True
    except UnicodeEncodeError:
        ascii_ok = False
    out.append(("M7 the record is ASCII", ascii_ok, "ascii" if ascii_ok else "non-ASCII present"))
    return out


# ---------------------------------------------------------------- live helpers (read-only)
def _aws(args, timeout=60):
    p = subprocess.run(["bash", os.path.join(ROOT, ".tools", "aws")] + args, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
    if p.returncode != 0:
        return None, f"rc={p.returncode} {p.stderr.strip()[:140]}"
    try:
        return json.loads(p.stdout), ""
    except ValueError:
        return None, "unparseable output"


def code_universe():
    """Files under SCAN_TOPS naming both gold/mdpf_revamp and aggregate_aua_timeseries; returns (sorted paths, scanned)."""
    hits, scanned = [], 0
    for top in SCAN_TOPS:
        base = os.path.join(ROOT, top)
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in fn:
                if not f.endswith(SUF):
                    continue
                p = os.path.join(dp, f)
                try:
                    if os.path.getsize(p) > 3_000_000:
                        continue
                    with open(p, encoding="utf-8", errors="replace") as fh:
                        t = fh.read()
                except OSError:
                    continue
                scanned += 1
                if "gold/mdpf_revamp" in t and "aggregate_aua_timeseries" in t:
                    hits.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return sorted(hits), scanned


def _selector_covers(sel_doc):
    """True if any data-event selector in a get-event-selectors document covers the bucket's objects."""
    arn = f"arn:aws:s3:::{BUCKET}/"
    for es in sel_doc.get("EventSelectors") or []:
        for dr in es.get("DataResources") or []:
            for v in dr.get("Values") or []:
                if v == "arn:aws:s3" or v == "arn:aws:s3:::" or arn.startswith(v) or v.startswith(arn):
                    return True
    for aes in sel_doc.get("AdvancedEventSelectors") or []:
        for fs in aes.get("FieldSelectors") or []:
            if fs.get("Field") == "resources.ARN":
                for k in ("Equals", "StartsWith"):
                    for v in fs.get(k) or []:
                        if arn.startswith(v) or v.startswith(arn):
                            return True
    return False


def verify_arms(rec):
    out = []
    head, err = _aws(["s3api", "head-object", "--bucket", BUCKET, "--key", KEY, "--output", "json"])
    out.append(("V1 the staged key exists now (the census is of a live object)", bool(head and head.get("ContentLength", 0) > 0),
                f"ContentLength={head.get('ContentLength') if head else None} LastModified={head.get('LastModified') if head else None} {err}"))

    cls = (rec or {}).get("classes") or {}
    listed = {r.get("evidence", "").split(":")[0] for r in (cls.get("code") or {}).get("readers", []) if isinstance(r, dict)}
    listed |= {str(r.get("id", "")) for r in (cls.get("code") or {}).get("readers", []) if isinstance(r, dict)}
    absent = [a for a in ANCHORS if a not in listed]
    out.append(("V2 the code class lists each anchor reader the issuer's pre-read found", not absent and bool(rec),
                f"anchors={len(ANCHORS)} missing from the record={absent}"))

    uni, scanned = code_universe()
    code = cls.get("code") or {}
    covered = {r.get("evidence", "").split(":")[0] for r in code.get("readers", []) if isinstance(r, dict)}
    covered |= {r.get("id") for r in code.get("readers", []) if isinstance(r, dict)}
    excl = {e.get("path"): e.get("reason") for e in code.get("excluded", []) if isinstance(e, dict)}
    bad_reason = sorted(p for p, r in excl.items() if r not in EXCLUDE_REASONS)
    unaccounted = [p for p in uni if p not in covered and p not in excl]
    d = code.get("denominator") or {}
    out.append(("V3 every file the repo scan finds is a listed reader or an excluded file with a reason; the record's scanned count is the scan's",
                bool(rec) and not unaccounted and not bad_reason and d.get("scanned") == scanned,
                f"scan: {len(uni)} file(s) of {scanned} scanned; unaccounted={unaccounted[:5]} bad_reason={bad_reason[:3]} record scanned={d.get('scanned')}"))

    cov = False
    errs = []
    for t in TRAILS:
        doc, e = _aws(["cloudtrail", "get-event-selectors", "--trail-name", t, "--output", "json"])
        if doc is None:
            errs.append(f"{t}: {e}")
            continue
        cov = cov or _selector_covers(doc)
    rec_cov = (cls.get("trail") or {}).get("covered")
    out.append(("V4 the record's trail coverage equals the live event selectors of both trails", bool(rec) and not errs and rec_cov is cov,
                f"live covers {BUCKET}={cov} record={rec_cov} errors={errs}"))

    sch, e = _aws(["scheduler", "get-schedule", "--name", SCHEDULE, "--output", "json"])
    live_state = sch.get("State") if sch else None
    entries = [r for r in (cls.get("scheduled") or {}).get("readers", []) if isinstance(r, dict) and SCHEDULE in str(r.get("id", "")) + str(r.get("evidence", ""))]
    rec_state = entries[0].get("state") if entries else None
    out.append(("V5 the accrual bridge schedule is a listed scheduled reader and its state equals the live state", bool(entries) and rec_state == live_state,
                f"live State={live_state} record state={rec_state} listed={len(entries)} {e}"))
    return out


# ---------------------------------------------------------------- selftest (offline)
def good_record():
    reader = lambda i, s, o=None: {"id": i, "evidence": f"{i}:1", "kind": "reads", "surface": s, "output_key": o}  # noqa: E731
    code_readers = [reader(a, "INTERNAL") for a in ANCHORS[:3]] + [reader(ANCHORS[3], "NONE")]
    code_readers[2] = reader(ANCHORS[2], "PARTNER-FACING-CANDIDATE", "portal/gold/mdpf/global/aggregate-aua-timeseries/<as_of>.json")
    return {
        "key": f"s3://{BUCKET}/{KEY}", "verdict": "READERS-FOUND", "zero_readers": False, "total_readers": 6,
        "partner_facing": [ANCHORS[2]],
        "classes": {
            "code": {"denominator": {"scanned": 8831, "unit": "files"}, "count": 4, "readers": code_readers, "excluded": []},
            "scheduled": {"denominator": {"scanned": 1, "unit": "schedules"}, "count": 1,
                          "readers": [{"id": SCHEDULE, "evidence": SCHEDULE, "state": "ENABLED", "surface": "INTERNAL", "output_key": None}]},
            "iam_static": {"denominator": {"scanned": 3, "unit": "roles"}, "count": 1,
                           "readers": [{"id": "mdpf-gold-lambda-role", "evidence": "iam.tf:883", "surface": "NONE", "output_key": None}]},
            "iam_live": {"denominator": {"scanned": 3, "unit": "roles"}, "principals_checked": 3,
                         "states": {"ALLOWED": 2, "DENIED": 0, "NOT-DECIDABLE": 1}},
            "trail": {"denominator": {"scanned": 2, "unit": "trails"}, "covered": False, "server_access_logging": False,
                      "trails": list(TRAILS), "evidence": ["get-event-selectors: opal-data-assets is in no data selector"]},
        },
    }


def selftest():
    import copy
    arms = []
    g = record_arms(good_record())
    arms.append(("G0 a well-formed record passes every structure arm", all(ok for _, ok, _ in g), f"{sum(ok for _, ok, _ in g)} of {len(g)}"))

    def red(name, mutate, want):
        r = copy.deepcopy(good_record())
        mutate(r)
        failed = [a[:2] for a, ok, _ in record_arms(r) if not ok]
        arms.append((name, want in failed, f"failed arms={failed}"))

    red("D1 a class dropped turns M1 red", lambda r: r["classes"].pop("trail"), "M1")
    red("D2 a zero-reader class with no denominator turns M2 red", lambda r: r["classes"]["scheduled"].update(count=0, readers=[], denominator={}), "M2")
    red("D3 a count that disagrees with its list turns M3 red", lambda r: r["classes"]["code"].update(count=9), "M3")
    red("D4 a partner-facing reader missing from partner_facing turns M5 red", lambda r: r.update(partner_facing=[]), "M5")

    def d5(r):  # zero readers, trail uncovered, verdict claims proven
        for c in ("code", "scheduled", "iam_static"):
            r["classes"][c].update(count=0, readers=[])
        r.update(verdict="ZERO-READERS-PROVEN", zero_readers=True, total_readers=0, partner_facing=[])
    red("D5 ZERO-READERS-PROVEN on an uncovered trail turns M6 red", d5, "M6")
    return arms


# ---------------------------------------------------------------- main
def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    path = DEFAULT_RECORD
    if "--record" in argv:
        path = argv[argv.index("--record") + 1]
    if mode == "universe":   # the repo scan's file list and denominator, for the worker to classify (JSON on stdout)
        files, scanned = code_universe()
        print(json.dumps({"scanned": scanned, "unit": "files", "tops": list(SCAN_TOPS), "files": files}, indent=1))
        return 0
    if mode == "selftest":
        arms = selftest()
    elif mode in ("record", "verify"):
        if not os.path.exists(path):
            print(f"  RECORD NOT FOUND: {path}")
            rec = None
        else:
            rec = _load(path)
        if mode == "record":
            arms = record_arms(rec) if rec is not None else [("M0 the census record exists", False, path)]
        else:
            arms = verify_arms(rec)
    else:
        print(__doc__)
        return 2
    k = 0
    for name, ok, detail in arms:
        print(f"  {name.split(' ')[0]} {'PASS' if ok else 'FAIL'} {name.split(' ', 1)[1] if ' ' in name else ''} -- {detail}")
        k += 1 if ok else 0
    print(f"CN-M-1 {mode.upper()}: {k} of {len(arms)} arms")
    return 0 if k == len(arms) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
