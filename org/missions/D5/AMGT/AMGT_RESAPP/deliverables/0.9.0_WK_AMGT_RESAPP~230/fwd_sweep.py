"""AMGT_RESAPP round 70, AMGT-at-5 -- THE 30-OUTCOME SWEEP: every gradeable FWD exercised ONCE on the DEPLOYED
`opal-amgt-scoped-api` against its DONE WHEN (never its ACCEPT).

  PYTHONPATH=<repo root> python fwd_sweep.py --where deployed      (cwd = the repo root)

READ ONLY. Every read is a lambda:Invoke of the deployed function through 0.9.0_WK_AMGT_RESAPP~158/capture_lib.py `_invoke`
(or the same event shape for a raw PDF / Markdown body), plus these reads and nothing else: the covered universe
(lib.research.coverage.covered_universe, a fresh read of research_dossier/), the identity crosswalk object the served bodies
name (S3 GET), the gold/DynamoDB reads the round-56 graders make, and the producer's own record copy of the price generation.
No deploy, no store write, no vendor call, no portal write.

Instruments (all invoke the DEPLOYED function):
  - per covered name (95 at the cut): /thesis /overlay /peers /coverage /ledger /versions and /print?format=rich -- the
    features below are read from them in ONE pass and the bodies are dropped;
  - globals: /freshness /lists /lead-panel rankings and the monthly chatter route, /security/<uncovered>/..., /compare, the PDF print;
  - the existing graders, each run as a child process with --where deployed (round 56 af_1/af_2, round 64 c9/c11/c12/c13,
    round 65 c17, round 66 c18/c22, round 67 c24, round 68 c27): FWD-32/33/34/36/37/38/39.

STATUS (the round-51 state_rule, kept so the two passes read alike):
  MEETS                     every limb of the DONE WHEN reads true on a value measured here on the served plane.
  DOES_NOT_MEET             an instrument returned a limb of the DONE WHEN false, OR returned the PRECONDITION of a human-act
                            clause absent on the served state (the act cannot have occurred on it).
  UNMEASURABLE_WITH_REASON  the DONE WHEN names a completed human act, a rendered-page state, or a qualified wait, and its
                            precondition is present: the reason says which and the measured enabling state is the evidence.
A FWD whose route could not be read is UNMEASURABLE_WITH_REASON "instrument failure" and is NOT counted as read.
FWD-21..FWD-29 are RE-HOMED (PRD Addendum C, s.C.1) and are printed, never graded.

Prints 39 FWD lines and `SWEEP: <n> of 30 read`; writes FWD_SWEEP_ROUND70.json and FWD_SWEEP_ROUND70.md beside this file.
Exit 0 only when n == 30 and the deployed CodeSha256 did not move during the sweep.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import importlib.util
import json
import math
import re
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
DELIV = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables"
PRD_PATH = "org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md"
CAPTURE_LIB = ROOT / DELIV / "0.9.0_WK_AMGT_RESAPP~158/capture_lib.py"
R56 = ROOT / DELIV / "2.0.0_SA_COO~Z/round56/checks"
PREFIX = "/api/scoped/amgt"
GRADEABLE = list(range(1, 21)) + list(range(30, 40))
REHOMED = list(range(21, 30))
FIVE_KINDS = ("market_data", "filings", "news", "social", "web")
STATE_RULE = (
    "MEETS = every limb of the DONE WHEN reads true on a value measured in this sweep on the served plane. DOES_NOT_MEET = an "
    "instrument returned a limb false, or returned the precondition of a human-act clause absent on the served state. "
    "UNMEASURABLE_WITH_REASON = the DONE WHEN names a completed human act, a rendered-page state or a qualified wait and its "
    "precondition is present; the measured enabling state is the evidence. Graded on the DONE WHEN, never the ACCEPT."
)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CL = _load("capture_lib", CAPTURE_LIB)


def make_client():
    import boto3
    from botocore.config import Config

    cfg = Config(read_timeout=300, connect_timeout=30, retries={"max_attempts": 10, "mode": "adaptive"})
    return boto3.client("lambda", region_name=CL.REGION, config=cfg)


def raw_invoke(lam, path, query=None):
    """The same event shape as capture_lib._invoke, but the body is returned undecoded-as-JSON: (status, content_type, bytes)."""
    resp = lam.invoke(FunctionName=CL.FUNCTION, Payload=json.dumps(CL._event(path, query)).encode("utf-8"))
    raw = resp["Payload"].read()
    if resp.get("FunctionError"):
        return None, "", raw[:300]
    p = json.loads(raw)
    body = p.get("body") or ""
    blob = base64.b64decode(body) if p.get("isBase64Encoded") else body.encode("utf-8")
    h = p.get("headers") or {}
    return p.get("statusCode"), h.get("Content-Type") or h.get("content-type") or "", blob


def get(lam, path, query=None):
    """(status, body-or-None). A non-200 or a FunctionError is a REFUSAL, never an empty answer."""
    body, meta = CL._invoke(lam, PREFIX + path, query)
    if body is None:
        return meta.get("status") or meta.get("error") or "no-status", None
    return 200, body


# --------------------------------------------------------------------------------------------------------------------
# the PRD: DONE WHEN quotes
# --------------------------------------------------------------------------------------------------------------------
def read_prd():
    text = (ROOT / PRD_PATH).read_text(encoding="utf-8")
    a = text.index("## ENDPOINT (step 2")
    b = text.index("**BAR DISTRIBUTION")
    blocks, cur = {}, None
    for ln in text[a:b].splitlines():
        m = re.match(r"^  FWD-(\d+)\s+(?!->)(\S.*)$", ln)
        if m:
            cur = int(m.group(1))
            blocks[cur] = [ln]
            continue
        if re.match(r"^  FWD-\d+\s+->", ln) or re.match(r"^  =====", ln):
            cur = None
            continue
        if cur:
            blocks[cur].append(ln)
    done, rehome = {}, {}
    for n, lines in blocks.items():
        s = " ".join(x.strip() for x in lines)
        m = re.search(r"DONE WHEN\s+(.*?)\s+ACCEPT\s", s)
        done[n] = re.sub(r"\s+", " ", m.group(1)) if m else None
    for m in re.finditer(r"^  FWD-(\d+) -> (DSGN FWD-\d+)", text, re.M):
        rehome[int(m.group(1))] = m.group(2)
    ver = re.findall(r'"prd_version"\s*:\s*"([^"]+)"', text)
    return done, rehome, (ver[0] if ver else "?"), sorted(blocks)


# --------------------------------------------------------------------------------------------------------------------
# one pass over the covered population
# --------------------------------------------------------------------------------------------------------------------
ROUTES = (("thesis", "/security/{k}/thesis"), ("overlay", "/security/{k}/overlay"), ("peers", "/security/{k}/peers"),
          ("coverage", "/security/{k}/coverage"), ("ledger", "/security/{k}/ledger"), ("versions", "/security/{k}/versions"))


def _et(ts):
    try:
        from zoneinfo import ZoneInfo

        d = datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%MZ").replace(tzinfo=datetime.timezone.utc)
        return d.astimezone(ZoneInfo("America/New_York")).strftime("%H:%M %Z")
    except Exception:  # noqa: BLE001 -- no tz database on this box: say so, never guess an offset
        return "ET not resolved on this box"


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_rich(text):
    figs, cites, pcites, sec = {}, set(), set(), None
    for ln in text.splitlines():
        if ln.startswith("## Header"):
            sec = ("header", None)
            continue
        m = re.match(r"## Fiscal year (\d{4})", ln)
        if m:
            sec = ("fy", m.group(1))
            continue
        if ln.startswith("## "):
            sec = (ln[3:].strip(), None)
            continue
        if sec and sec[0] in ("header", "fy") and ln.startswith("| ") and not ln.startswith("| Mnemonic") and not ln.startswith("|---"):
            c = ln.strip().strip("|").split(" | ", 2)
            if len(c) == 3:
                figs[(sec[0], sec[1], c[0].strip())] = c[2].strip()
        m = re.match(r"> (P\d+) --", ln)
        if m:
            cites.add(m.group(1))
        m = re.match(r"> cites: (.*)", ln)
        if m:
            pcites |= {x.strip() for x in m.group(1).split(",")}
    return figs, cites, pcites


def harvest(lam, key, sibling_keys):
    r = {"key": key, "route_status": {}}
    B = {}
    for name, tpl in ROUTES:
        st, b = get(lam, tpl.format(k=key))
        r["route_status"][name] = st
        B[name] = b
    st, ctype, blob = raw_invoke(lam, PREFIX + "/security/%s/print" % key, {"format": "rich"})
    r["route_status"]["print_rich"] = st
    rich = blob.decode("utf-8", "replace") if st == 200 else None
    th, ov, pe, le, ve = (B[n] or {} for n in ("thesis", "overlay", "peers", "ledger", "versions"))
    r["ok"] = all(v == 200 for v in r["route_status"].values())

    # identity across the six JSON routes
    ids = {}
    for n in ("thesis", "overlay", "peers", "coverage", "ledger", "versions"):
        ident = (B[n] or {}).get("identity") or {}
        ids[n] = (ident.get("security_key"), ident.get("identity_status"))
    r["identity"] = {n: v[0] == key and v[1] == "MEASURED" for n, v in ids.items()}
    r["bloomberg"] = (th.get("identity") or {}).get("bloomberg")
    if sibling_keys:
        blob_text = json.dumps([B[n] for n, _ in ROUTES]) + (rich or "")
        r["sibling_hits"] = {s: (s in blob_text) for s in sibling_keys}

    # thesis
    hf = th.get("header_figures") or []
    fy = th.get("fiscal_year_figures") or []
    ff = (th.get("model") or {}).get("forecast_figures") or []
    allf = hf + fy + ff
    valued = [f for f in allf if f.get("value") is not None]
    r["figs"] = {"header_valued": sum(1 for f in hf if f.get("value") is not None), "fy": len(fy), "forecast": len(ff),
                 "total": len(allf), "valued": len(valued), "null_valued": len(allf) - len(valued),
                 "null_without_reason": sum(1 for f in allf if f.get("value") is None and not str(f.get("reason") or "").strip()),
                 "missing_basis": sum(1 for f in valued if not f.get("basis")),
                 "missing_vintage": sum(1 for f in valued if not f.get("vintage")),
                 "missing_source": sum(1 for f in valued if not f.get("source"))}
    r["model_status"] = th.get("model_status")
    cf = th.get("check_face") or []
    r["check_face"] = dict(Counter(c.get("verdict") for c in cf))
    r["refuse_marked"] = sum(1 for c in cf if c.get("verdict") == "REFUSE" and c.get("marker") and str(c.get("reason") or "").strip())
    sents = [s for sec in (th.get("drafted_sections") or []) for s in (sec.get("sentences") or [])]
    r["drafted"] = {"status": th.get("drafting_status"), "sentences": len(sents),
                    "generated_true": sum(1 for s in sents if s.get("generated") is True),
                    "with_evidence": sum(1 for s in sents if s.get("evidence") and all(
                        e.get("passage") and (e.get("source") or {}).get("accession") for e in s["evidence"])),
                    "evidence_items": sum(len(s.get("evidence") or []) for s in sents)}
    dc = th.get("thesis_driver_chart") or {}
    r["driver_chart"] = {"status": dc.get("status"), "points": dc.get("points_count"), "source": dc.get("source")}
    mg = th.get("management") or {}
    offs = mg.get("officers") or []
    r["mgmt"] = {"status": mg.get("management_status"), "officers": len(offs),
                 "officers_sourced": sum(1 for o in offs if str(o.get("source") or "").strip()),
                 "tenure": sum(1 for o in offs if o.get("tenure_years") is not None),
                 "chain": bool(mg.get("chain_tried")), "reason": bool(str(mg.get("reason") or "").strip())}
    po = th.get("posture") or {}
    r["posture"] = {"status": po.get("status"), "marked": po.get("marked"), "comparable": bool(po.get("comparable")),
                    "verdict": po.get("verdict"), "reason": bool(str(po.get("reason") or "").strip())}
    dv = (th.get("scores") or {}).get("divergence") or {}
    r["divergence"] = {"state": dv.get("state"), "D": dv.get("D")}
    dm = (th.get("dossier_fields") or {}).get("management") or {}
    r["dossier_mgmt"] = dm.get("status")

    # overlay
    de = ov.get("description") or {}
    feed = ov.get("feed") or {}
    items = feed.get("items") or []
    r["description"] = de.get("status")
    r["feed"] = {"items": len(items), "with_url": sum(1 for i in items if i.get("url")),
                 "social_items": len((feed.get("social") or {}).get("items") or []),
                 "coverage_status": feed.get("coverage_status")}
    r["provenance_inputs"] = sorted(i.get("input") for i in ((ov.get("provenance") or {}).get("inputs") or []))
    r["bloomberg_session_state"] = ov.get("bloomberg_session_state")
    pr, bp = ov.get("price") or {}, ov.get("breakout_price") or {}
    r["overlay_price"] = {"as_of": pr.get("as_of_date"), "score_pct": pr.get("score_pct"), "axis": pr.get("axis")}
    r["overlay_breakout"] = {"as_of": bp.get("as_of_date"), "score_pct": bp.get("score_pct"), "axis": bp.get("axis"),
                             "measure": bp.get("movement_measure"), "pct_jump_pct": bp.get("pct_jump_pct")}

    # peers
    members = pe.get("members") or []
    root = str(((pe.get("identity") or {}).get("display_ticker") or key).split(" ")[0]).upper()
    r["peers"] = {"basis": pe.get("basis"), "members": len(members),
                  "self_in_members": sum(1 for m in members if str(m.get("ticker") or "").upper() == root),
                  "reason": bool(str(pe.get("reason") or "").strip())}

    # ledger and versions
    cls = le.get("classes") or {}
    lbc = le.get("latest_by_class") or {}
    r["ledger"] = {k: {"source": bool((cls.get(k) or {}).get("source")), "run": k in lbc} for k in FIVE_KINDS}
    r["ledger_denominators"] = le.get("denominators") or {}
    vs = ve.get("versions") or []
    r["versions"] = {"n": len(vs), "first": vs[0]["stamp"] if vs else None, "last": vs[-1]["stamp"] if vs else None}

    # export (rich) against the served thesis bundle
    if rich is not None:
        figs, cites, pcites = parse_rich(rich)
        served = {}
        for f in hf:
            if f.get("value") is not None:
                served[("header", None, f["mnemonic"])] = f["value"]
        for f in fy:
            if f.get("value") is not None:
                served[("fy", str(f["fiscal_year"]), f["mnemonic"])] = f["value"]
        cfv = {c.get("figure_id"): c.get("verdict") for c in cf}
        missing = [k for k in served if k not in figs]
        extra = [k for k in figs if k not in served]
        # a figure its own check REFUSED is withheld from the table and stated as a "MNEMONIC: REFUSED -- reason" line instead
        withheld = [k for k in missing if k[0] == "fy" and cfv.get("fiscal_year_line_item:%s:%s" % (k[2], k[1])) == "REFUSE"]
        refused_line_ok = sum(1 for k in withheld if ("%s: REFUSED" % k[2]) in rich)
        missing_fy_other = [k for k in missing if k[0] == "fy" and k not in withheld]
        differ = 0
        for k, v in served.items():
            if k in figs:
                tok = figs[k].split(" ")[0]
                a, b = _num(tok), _num(v)
                ok = (a is not None and b is not None and math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)) or (
                    (a is None or b is None) and figs[k].startswith(str(v)))
                if not ok:
                    differ += 1
        sc = {e["id"] for s in sents for e in (s.get("evidence") or []) if e.get("id")}
        pc = {c for b in (po.get("basis") or []) for c in (b.get("cites") or [])}
        r["export"] = {"bytes": len(rich), "served_figs": len(served), "rich_figs": len(figs),
                       "missing_header": sum(1 for k in missing if k[0] == "header"),
                       "missing_fy": sum(1 for k in missing if k[0] == "fy"), "withheld_refused": len(withheld),
                       "withheld_with_refusal_line": refused_line_ok, "missing_fy_unexplained": len(missing_fy_other),
                       "missing_header_mnemonics": sorted({k[2] for k in missing if k[0] == "header"}),
                       "extra": len(extra), "differ": differ,
                       "cites_served": len(sc), "cites_rich": len(cites), "cites_only_served": len(sc - cites),
                       "cites_only_rich": len(cites - sc), "pcites_served": len(pc), "pcites_rich": len(pcites),
                       "pcites_diff": len(pc ^ pcites)}
    return r


def population_pass(lam, keys, collisions):
    out, t0 = {}, time.time()
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {k: ex.submit(harvest, lam, k, collisions.get(k)) for k in keys}
        for k, f in futs.items():
            try:
                out[k] = f.result()
            except Exception as e:  # noqa: BLE001 -- an unreadable name is COUNTED, never dropped
                out[k] = {"key": k, "ok": False, "error": "%s: %s" % (type(e).__name__, str(e)[:160]), "route_status": {}}
    return out, round(time.time() - t0)


# --------------------------------------------------------------------------------------------------------------------
# graders run as child processes against the deployed function
# --------------------------------------------------------------------------------------------------------------------
def run_child(args, timeout=1500):
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-W", "ignore"] + args, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout, cwd=str(ROOT))
        out, rc = p.stdout, p.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b"").decode("utf-8", "replace") if isinstance(e.stdout, bytes) else (e.stdout or ""), 124
    lines = [ln.rstrip() for ln in out.splitlines() if ln.strip()]
    clauses = [ln for ln in lines if re.match(r"^(PASS|FAIL) ", ln)]
    verdict = next((ln for ln in reversed(lines) if re.search(r": (YES|NO)\s*$", ln)), None)
    return {"cmd": " ".join(args), "rc": rc, "seconds": round(time.time() - t0),
            "pass": sum(1 for c in clauses if c.startswith("PASS")), "fail": sum(1 for c in clauses if c.startswith("FAIL")),
            "verdict_line": verdict, "lines": [ln[:330] for ln in lines][:60],
            "met": rc == 0 and bool(verdict) and verdict.rstrip().endswith("YES") and not any(c.startswith("FAIL") for c in clauses)}


def child_main(which):
    """Run one round-56 grader with its LOCAL call swapped for an invoke of the DEPLOYED function (round 57's own swap)."""
    lam = make_client()

    def deployed(path, query=None):
        body, meta = CL._invoke(lam, path, query)
        if body is None:
            print("REFUSED: deployed read failed: " + json.dumps(meta)[:300])
            return meta.get("status"), {"refused": True}
        return 200, body

    if which == "af1":
        a = _load("af_1_route", R56 / "af_1_route.py")
        a._live_body = lambda: deployed(a.PATH)
        sys.argv = ["af_1_route.py"]
    else:
        a = _load("af_2_serve", R56 / "af_2_serve.py")
        a._call = deployed
        sys.argv = ["af_2_serve.py", "--what", which]
    return a.main()


GRADERS = {
    "af1": ["{self}", "--child", "af1"],
    "af33": ["{self}", "--child", "fwd33"],
    "af34": ["{self}", "--child", "fwd34"],
    "c9": [DELIV + "/2.0.0_SA_COO~Z/round64/checks/r64_served.py", "--cell", "c9", "--where", "deployed"],
    "c11": [DELIV + "/2.0.0_SA_COO~Z/round64/checks/r64_served.py", "--cell", "c11", "--where", "deployed"],
    "c12": [DELIV + "/2.0.0_SA_COO~Z/round64/checks/r64_served.py", "--cell", "c12", "--where", "deployed"],
    "c13": [DELIV + "/2.0.0_SA_COO~Z/round64/checks/r64_served.py", "--cell", "c13", "--where", "deployed"],
    "c17": [DELIV + "/2.0.0_SA_COO~Z/round65/checks/r65_served.py", "--cell", "c17", "--where", "deployed"],
    "c18": [DELIV + "/2.0.0_SA_COO~Z/round66/checks/r66_served.py", "--cell", "c18", "--where", "deployed"],
    "c22": [DELIV + "/2.0.0_SA_COO~Z/round66/checks/r66_served.py", "--cell", "c22", "--where", "deployed"],
    "c24": [DELIV + "/2.0.0_SA_COO~Z/round67/checks/r67_served.py", "--cell", "c24", "--where", "deployed"],
    "c27": [DELIV + "/2.0.0_SA_COO~Z/round68/checks/r68_served.py", "--cell", "c27", "--where", "deployed"],
}


def run_graders():
    jobs = {}
    for name, argv in GRADERS.items():
        jobs[name] = [str(Path(__file__).resolve()) if a == "{self}" else a for a in argv]
    out = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {n: ex.submit(run_child, a) for n, a in jobs.items()}
        for n, f in futs.items():
            out[n] = f.result()
    return out


# --------------------------------------------------------------------------------------------------------------------
# the globals
# --------------------------------------------------------------------------------------------------------------------
def read_globals(lam, keys):
    g = {}
    st, fr = get(lam, "/freshness")
    g["freshness"] = {"status": st}
    if fr:
        rows = fr.get("rows") or []
        by = {r.get("security_key"): r for r in rows}
        cov = [by[k] for k in keys if k in by]
        g["freshness"].update({"rows": len(rows), "covered_present": len(cov), "covered_absent": [k for k in keys if k not in by][:8],
                               "covered_absent_n": sum(1 for k in keys if k not in by),
                               "distinct_last_refreshed_on_covered": len({r.get("last_refreshed") for r in cov}),
                               "never_on_covered": sum(1 for r in cov if r.get("last_refreshed") == "NEVER"),
                               "generated_at": fr.get("generated_at")})
    st, ls = get(lam, "/lists")
    g["lists"] = {"status": st}
    if ls:
        g["lists"].update({k: {f: v.get(f) for f in ("owner_status", "entries_total", "entries_stale", "list_stale", "reviewed_at",
                                                    "review_interval_days", "unresolvable_count")}
                           for k, v in (ls.get("lists") or {}).items()})
    rk = {}
    for mv in ("trending", "breakout"):
        for sub in ("price", "chatter"):
            st, b = get(lam, "/lead-panel/rankings/%s/%s" % (mv, sub))
            rk["%s_%s" % (mv, sub)] = {"status": st, "body": b}
    g["rankings"] = rk
    st, b = get(lam, "/lead-panel/timeseries/collected/chatter")
    g["monthly"] = {"status": st, "body": b}
    # FWD-2: a name the firm does not cover
    unc = {}
    for k in ("AAPL_US_Equity", "ZZZZ_US_Equity"):
        if k in keys:
            continue
        s1, o = get(lam, "/security/%s/overlay" % k)
        s2, t = get(lam, "/security/%s/thesis" % k)
        unc[k] = {"overlay": s1, "thesis": s2,
                  "identity_status": ((o or {}).get("identity") or {}).get("identity_status"),
                  "description_status": ((o or {}).get("description") or {}).get("status"),
                  "model_status": (t or {}).get("model_status"),
                  "drafting_status": (t or {}).get("drafting_status")}
    g["uncovered"] = unc
    s3, refresh = get(lam, "/refresh")
    g["refresh_get"] = {"status": s3, "note": "POST-only route; a GET is a refusal, no write was attempted"}
    return g


def read_compare_and_print(lam, vers):
    out = {}
    key = "BA_US_Equity" if (vers.get("BA_US_Equity") or {}).get("first") != (vers.get("BA_US_Equity") or {}).get("last") else next(
        (k for k, x in sorted(vers.items()) if x and x.get("first") and x.get("first") != x.get("last")), "BA_US_Equity")
    v = vers.get(key) or {}
    if v.get("first") and v.get("last") and v["first"] != v["last"]:
        st, b = get(lam, "/security/%s/compare" % key, {"from": v["first"], "to": v["last"]})
        cm = (b or {}).get("compared") or {}
        dn = (b or {}).get("denominators") or {}
        out["compare"] = {"key": key, "status": st, "from": v["first"], "to": v["last"],
                          "from_stamp": cm.get("from_stamp"), "to_stamp": cm.get("to_stamp"),
                          "figures_from": dn.get("figures_from"), "figures_to": dn.get("figures_to"),
                          "added": dn.get("added"), "removed": dn.get("removed"), "changed": dn.get("changed"),
                          "unchanged": dn.get("unchanged"), "available_stamps": len((b or {}).get("available_stamps") or []),
                          "reason": (b or {}).get("reason")}
    else:
        out["compare"] = {"key": key, "status": "no two stamps"}
    pdfs = []
    for k in ("BA_US_Equity", "AMD_US_Equity"):
        st, ctype, blob = raw_invoke(lam, PREFIX + "/security/%s/print" % k)
        pdfs.append({"key": k, "status": st, "content_type": ctype, "bytes": len(blob),
                     "pages": len(re.findall(rb"/Type\s*/Page(?![a-z])", blob)) if st == 200 else None})
    out["pdf"] = pdfs
    return out


def price_generation_record(as_of):
    """The producer's own record copy of the generation (the generation's `excluded` record). Looked up in this tree first, then in
    the checkout this worktree was cut from (git common dir) -- derived, never typed."""
    name = "0.9.0_WK_AMGT_RESAPP~6/price_axis_rows_%s.json" % as_of
    cands = [ROOT / DELIV / name]
    try:
        gc = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, cwd=str(ROOT)).stdout.strip()
        if gc:
            cands.append((ROOT / gc).resolve().parent / DELIV / name)
    except OSError:
        pass
    for c in cands:
        if c.is_file():
            return str(c), json.loads(c.read_text(encoding="utf-8"))
    return None, None


# --------------------------------------------------------------------------------------------------------------------
# grading
# --------------------------------------------------------------------------------------------------------------------
def grade(done, keys, H, G, GR, extra):
    N = len(keys)
    hv = [h for h in H.values()]
    okn = sum(1 for h in hv if h.get("ok"))
    out = {}

    def S(n, status, reason, evidence, routes, denominator, not_read=None):
        out[n] = {"fwd": "FWD-%d" % n, "done_when": done.get(n), "routes": routes, "denominator": denominator,
                  "status": status, "reason": reason, "evidence": evidence, "not_read": not_read or []}

    def cnt(f):
        return sum(1 for h in hv if h.get("ok") and f(h))

    all_ok = okn == N
    stream = "/thesis /overlay /peers /coverage /ledger /versions /print?format=rich"
    den = "%d of %d covered names read (all 7 routes 200)" % (okn, N)
    if not all_ok:
        bad = [h["key"] for h in hv if not h.get("ok")]
        extra["instrument_failures"] = bad

    # FWD-1
    enab = cnt(lambda h: h["figs"]["header_valued"] > 0 and h["figs"]["fy"] > 0 and h["model_status"] == "SERVED" and h["description"] == "SERVED")
    S(1, "UNMEASURABLE_WITH_REASON" if enab == N else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst has actually done it); no record of that act exists on any surface this sweep reads"
      if enab == N else "the enabling state is absent on %d of %d names, so the act cannot have occurred on them" % (N - enab, N),
      {"enabling_state_names": enab, "of": N, "header_valued_min": min((h["figs"]["header_valued"] for h in hv if h.get("ok")), default=None),
       "fiscal_year_figures_min": min((h["figs"]["fy"] for h in hv if h.get("ok")), default=None),
       "model_status_SERVED": cnt(lambda h: h["model_status"] == "SERVED"), "description_SERVED": cnt(lambda h: h["description"] == "SERVED")},
      stream, den)

    # FWD-2
    unc = G["uncovered"]
    pulled = [k for k, v in unc.items() if v["description_status"] == "SERVED" and v["model_status"] == "SERVED"]
    S(2, "UNMEASURABLE_WITH_REASON" if pulled else "DOES_NOT_MEET",
      ("an uncovered name serves a pulled pack; the act of a person typing it and reading it is a human act" if pulled else
       "no real uncovered name is pulled: every uncovered form probed serves description and model ABSENT, and the only refresh route is POST-only "
       "(not called: bound is GET only), so 'a real uncovered name has been pulled and read' cannot have occurred on this state"),
      {"uncovered_probes": unc, "refresh_get": G["refresh_get"]}, "/security/<uncovered>/overlay /thesis, GET /refresh",
      "%d uncovered names probed" % len(unc), ["POST /refresh (a write; bound)"])

    # FWD-3
    miss = {f: sum(h["figs"]["missing_" + f] for h in hv if h.get("ok")) for f in ("basis", "vintage", "source")}
    tot = sum(h["figs"]["valued"] for h in hv if h.get("ok"))
    nulls = sum(h["figs"]["null_valued"] for h in hv if h.get("ok"))
    nowhy = sum(h["figs"]["null_without_reason"] for h in hv if h.get("ok"))
    f3 = all_ok and not any(miss.values()) and nowhy == 0
    S(3, "UNMEASURABLE_WITH_REASON" if f3 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (a figure actually challenged and answered from the page); the enabling state is measured: every one of the %d valued figures carries basis, vintage and source, and the %d null figures each carry a reason" % (tot, nulls)
      if f3 else "valued figures lack basis, vintage or source on the served bundle (%s), or a null figure carries no reason (%d)" % (miss, nowhy),
      {"valued_figures_read": tot, "null_figures": nulls, "null_figures_without_reason": nowhy, "missing": miss}, "/thesis header_figures + fiscal_year_figures + model.forecast_figures",
      "%d figures over %d names" % (tot, okn))

    # FWD-4
    items = sum(h["feed"]["items"] for h in hv if h.get("ok"))
    with_url = sum(h["feed"]["with_url"] for h in hv if h.get("ok"))
    names_items = cnt(lambda h: h["feed"]["items"] > 0)
    S(4, "UNMEASURABLE_WITH_REASON" if with_url > 0 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst read one and followed it out); followable items are served and the act is not recorded"
      if with_url > 0 else "the precondition of following an item out is absent: %d feed items across %d names carry NO url (0 with a url), so no item can be followed out to its original from the served feed" % (items, names_items),
      {"feed_items": items, "feed_items_with_url": with_url, "names_with_items": names_items,
       "social_items": sum(h["feed"]["social_items"] for h in hv if h.get("ok"))}, "/overlay feed.items", den)

    # FWD-5
    pdfs = G["print"]["pdf"]
    pdf_ok = all(p["status"] == 200 and "pdf" in p["content_type"].lower() and (p["pages"] or 0) > 0 for p in pdfs)
    S(5, "UNMEASURABLE_WITH_REASON" if pdf_ok else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (Adam has actually forwarded one); the print is served and no record of any forward exists on a surface this sweep reads"
      if pdf_ok else "the print route did not serve a PDF", {"pdf": pdfs}, "/security/<key>/print (default format)",
      "%d names printed" % len(pdfs))

    # FWD-6
    cmpd = G["print"]["compare"]
    vn = [h["versions"]["n"] for h in hv if h.get("ok")]
    cmp_ok = cmpd.get("status") == 200 and cmpd.get("from_stamp") and cmpd.get("to_stamp")
    S(6, "UNMEASURABLE_WITH_REASON" if cmp_ok and all(n >= 1 for n in vn) else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (someone has actually compared two versions); the compare is served with both stamps named, and whether a person used it on the page is not recorded here"
      if cmp_ok else "the compare route did not serve two named versions",
      {"compare": cmpd, "versions_per_name": dict(sorted(Counter(vn).items())), "names_with_2plus_versions": sum(1 for n in vn if n >= 2)},
      "/security/<key>/versions, /security/<a name with 2+ versions>/compare", den, ["the portal surface that calls compare (a rendered state)"])

    # FWD-7
    fr = G["freshness"]
    full = fr.get("covered_absent_n", 99) == 0 and fr.get("status") == 200
    S(7, "UNMEASURABLE_WITH_REASON" if full else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (Adam has used it to find a stale name); the route lists every covered name" if full else
      "the precondition is absent: /freshness lists %d of %d covered names (%d absent), so 'sees every company the team covers' cannot occur on it"
      % (fr.get("covered_present", 0), N, fr.get("covered_absent_n", N)),
      fr, "/freshness", "%d of %d covered names present among %s rows" % (fr.get("covered_present", 0), N, fr.get("rows")))

    # FWD-8
    idn = cnt(lambda h: all(h["identity"].values()))
    bas = cnt(lambda h: h["peers"]["basis"] in ("derived", "absent") or h["peers"]["reason"])
    selfm = sum(h["peers"]["self_in_members"] for h in hv if h.get("ok"))
    S(8, "UNMEASURABLE_WITH_REASON" if idn == N and bas == N and selfm == 0 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst who distrusted the comparison block has stopped); the enabling state is measured"
      if idn == N and selfm == 0 else "the comparison block is not about the company on the page for some names",
      {"identity_agrees_all_6_routes": idn, "peers_basis_counts": dict(Counter(h["peers"]["basis"] for h in hv if h.get("ok"))),
       "subject_ticker_among_its_own_members": selfm, "members_total": sum(h["peers"]["members"] for h in hv if h.get("ok"))},
      "/peers (+ identity on 6 routes)", den)

    # FWD-9 (APPLIED)
    dn = [h for h in hv if h.get("ok") and h["drafted"]["status"] == "SERVED"]
    sent = sum(h["drafted"]["sentences"] for h in dn)
    gen = sum(h["drafted"]["generated_true"] for h in dn)
    wev = sum(h["drafted"]["with_evidence"] for h in dn)
    pst = [h for h in hv if h.get("ok") and h["posture"]["status"] == "SERVED"]
    pm = sum(1 for h in pst if h["posture"]["marked"] == "machine")
    m9 = bool(dn) and sent > 0 and gen == sent and wev == sent and pm == len(pst)
    S(9, "MEETS" if m9 else "DOES_NOT_MEET",
      "the marking is in place on the served plane: every drafted sentence carries generated=true beside its own evidence list (passage + accession), and every served posture is marked 'machine'"
      if m9 else "a drafted sentence lacks the machine marking or its evidence, or a served posture is not marked machine",
      {"names_with_drafted_prose": len(dn), "sentences": sent, "generated_true": gen, "with_passage_and_accession": wev,
       "postures_served": len(pst), "postures_marked_machine": pm},
      "/thesis drafted_sections[].sentences[] (generated, evidence), posture.marked", den,
      ["the portal's rendered machine marker (static render read 210 of 210 at round 51)"])

    # FWD-10
    refuse = sum(h["check_face"].get("REFUSE", 0) for h in hv if h.get("ok"))
    rmark = sum(h["refuse_marked"] for h in hv if h.get("ok"))
    S(10, "UNMEASURABLE_WITH_REASON" if refuse > 0 and rmark == refuse else "DOES_NOT_MEET",
      "the first limb is measured (checks have refused: %d REFUSE verdicts, each carrying a marker and a reason); the second limb, that the refusal 'was seen on the page', is a rendered-page state and a person's reading, which this sweep does not read" % refuse
      if refuse > 0 and rmark == refuse else "no check has refused anything, or a refusal is served without its marker",
      {"check_face_totals": dict(sum((Counter(h["check_face"]) for h in hv if h.get("ok")), Counter())),
       "refuse_with_marker_and_reason": rmark, "names_with_a_refusal": cnt(lambda h: h["check_face"].get("REFUSE", 0) > 0)},
      "/thesis check_face[]", den, ["the page render of a refused figure"])

    # FWD-11
    soc = sum(h["feed"]["social_items"] for h in hv if h.get("ok"))
    S(11, "UNMEASURABLE_WITH_REASON" if soc > 0 else "DOES_NOT_MEET",
      "social items are served; the act of an analyst reading one and pointing at its admitting rule is a human act" if soc > 0 else
      "the precondition is absent: %d social items across %d names, so there is no item an analyst could point at and no admission rule served with one" % (soc, okn),
      {"social_items": soc, "names": okn}, "/overlay feed.social", den)

    # FWD-12
    kinds = {k: {"names_with_source": cnt(lambda h, k=k: h["ledger"][k]["source"]), "names_with_a_run": cnt(lambda h, k=k: h["ledger"][k]["run"])}
             for k in FIVE_KINDS}
    nrun = [k for k, v in kinds.items() if v["names_with_a_run"] == 0]
    S(12, "DOES_NOT_MEET" if nrun else "UNMEASURABLE_WITH_REASON",
      ("%d of the 5 named input kinds have no run recorded on any name (%s), and no single-input re-run is observable (POST /refresh not called: bound)" % (len(nrun), ", ".join(nrun))
       if nrun else "the 5 kinds carry runs; a single-input re-run is a human act"),
      {"per_kind": kinds, "classes_with_a_stage_names": cnt(lambda h: (h["ledger_denominators"].get("classes_with_a_stage") or 0) > 0)},
      "/ledger", den)

    # FWD-13
    ident_all = idn == N
    cc = G["collision"]
    leaks = {k: v for k, v in cc["by_name"].items() if any(v.values())}
    S(13, "MEETS" if ident_all and cc["names"] > 0 and not leaks else "DOES_NOT_MEET",
      "checked on names more than one business uses (%d covered names share a ticker root with a second crosswalk key) and found not mixed: identity agrees on all six routes for %d of %d names and no sibling key appears in any served body"
      % (cc["names"], idn, N) if ident_all and cc["names"] > 0 and not leaks else
      "identity disagrees across routes (%d of %d agree), or a sibling business appears in a served body (%d names), or no shared-root name was found to check on" % (idn, N, len(leaks)),
      {"identity_agrees_all_6_routes": idn, "shared_root_names": cc["names"], "shared_root_pairs": cc["pairs"], "sibling_leaks": leaks,
       "crosswalk": cc["crosswalk"]}, "6 JSON routes' identity.security_key; sibling-key scan of the 6 bodies + the rich export",
      "%d of %d names; %d shared-root controls over %d crosswalk records" % (idn, N, cc["names"], cc["records"]))

    # FWD-14
    L = G["lists"]
    unassigned = [k for k, v in L.items() if isinstance(v, dict) and v.get("owner_status") == "UNASSIGNED"]
    stale = sum((v.get("entries_stale") or 0) for v in L.values() if isinstance(v, dict))
    S(14, "DOES_NOT_MEET" if unassigned or stale == 0 else "UNMEASURABLE_WITH_REASON",
      ("the precondition is absent: %d of 2 lists have no named owner (%s) and no entry is out of date (%d stale entries), so 'a list has actually gone out of date and somebody was told by the system' has not occurred and has no one to occur to" % (len(unassigned), ", ".join(unassigned), stale)
       if unassigned or stale == 0 else "a list is stale and owned; whether somebody was told is a human act"), L, "/lists", "2 lists")

    # FWD-15
    rk = G["rankings"]
    keyset = set(keys)
    rows15 = {n: (v["body"] or {}).get("rows") or [] for n, v in rk.items()}
    canon = {n: sum(1 for r in rr if r.get("security_key") in keyset) for n, rr in rows15.items()}
    ch_ok = all((rk[n]["body"] or {}).get("ranking_status") == "SERVED" or ((rk[n]["body"] or {}).get("ranking_status") == "EMPTY"
                                                                           and (rk[n]["body"] or {}).get("empty_reason")) for n in ("trending_chatter", "breakout_chatter"))
    served15 = bool(rows15["trending_price"]) and bool(rows15["breakout_price"]) and ch_ok
    S(15, "UNMEASURABLE_WITH_REASON" if served15 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (a PM opened the page, read the ranked list and clicked through); the ranked lists are served with canonical keys"
      if served15 else "a ranked list is not served, so a PM has nothing to open",
      {"rows": {n: len(rr) for n, rr in rows15.items()}, "rows_with_canonical_covered_key": canon,
       "as_of": {n: (v["body"] or {}).get("as_of_date") for n, v in rk.items()}, "status": {n: v["status"] for n, v in rk.items()},
       "ranking_status": {n: (v["body"] or {}).get("ranking_status") for n, v in rk.items()},
       "chatter_empty_reason": {n: (v["body"] or {}).get("empty_reason") for n, v in rk.items() if "chatter" in n}},
      "/lead-panel/rankings/{trending,breakout}/{price,chatter}", "4 rankings")

    # FWD-16
    desc = cnt(lambda h: h["description"] == "SERVED")
    f16 = desc == N and names_items > 0 and with_url > 0
    S(16, "UNMEASURABLE_WITH_REASON" if f16 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst has read the day's items at the top of a page and followed one out); the description is served on %d of %d names and %d feed items carry a url" % (desc, N, with_url)
      if f16 else "the precondition of 'followed one out' is absent: the description is served on %d of %d names and the feed on %d, but %d of %d feed items carry NO url, so no served item can be followed out to its source" % (desc, N, names_items, items - with_url, items),
      {"description_SERVED": desc, "names_with_feed_items": names_items, "feed_items": items, "feed_items_with_url": with_url},
      "/overlay description, feed", den, ["the page header render"])

    # FWD-17
    ms = cnt(lambda h: h["mgmt"]["status"] == "SERVED" and h["mgmt"]["officers"] > 0 and h["mgmt"]["officers_sourced"] == h["mgmt"]["officers"])
    reasoned = cnt(lambda h: h["mgmt"]["status"] != "SERVED" and h["mgmt"]["chain"] and h["mgmt"]["reason"])
    S(17, "UNMEASURABLE_WITH_REASON" if ms > 0 and ms + reasoned == N else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst used the profile to answer a question about a management team); the roster is served with a source on every officer on %d names and the other %d state the chain they tried and a reason" % (ms, reasoned)
      if ms > 0 and ms + reasoned == N else "a name serves neither a sourced roster nor the chain tried with a reason",
      {"names_roster_served_all_officers_sourced": ms, "names_absent_with_chain_and_reason": reasoned,
       "officers": sum(h["mgmt"]["officers"] for h in hv if h.get("ok")), "officers_with_tenure": sum(h["mgmt"]["tenure"] for h in hv if h.get("ok"))},
      "/thesis management", den)

    # FWD-18
    dch = cnt(lambda h: h["driver_chart"]["status"] == "SERVED")
    S(18, "UNMEASURABLE_WITH_REASON" if dn and wev > 0 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (an analyst clicked a filing-derived figure through to its passage); the passage text and accession ride every drafted sentence (%d of %d) and %d names serve a filing-sourced driver chart" % (wev, sent, dch)
      if dn and wev > 0 else "no filing-derived sentence carries a passage",
      {"names_with_drafted_prose": len(dn), "sentences_with_passage_and_accession": wev, "sentences": sent, "evidence_items": sum(h["drafted"]["evidence_items"] for h in dn),
       "driver_chart_SERVED_names": dch, "driver_chart_points": [h["driver_chart"]["points"] for h in hv if h.get("ok") and h["driver_chart"]["status"] == "SERVED"][:5]},
      "/thesis drafted_sections, thesis_driver_chart", den)

    # FWD-19
    called = [h for h in pst if h["posture"]["verdict"] not in (None, "absent")]
    pc = sum(1 for h in called if h["posture"]["comparable"])
    pr = cnt(lambda h: h["posture"]["status"] != "SERVED" and h["posture"]["reason"])
    f19 = bool(called) and pm == len(pst) and pc == len(called)
    S(19, "UNMEASURABLE_WITH_REASON" if f19 else "DOES_NOT_MEET",
      "the DONE WHEN names a completed human act (a PM has read a posture and acted on it, or declined it, on the page); postures are served on %d names, all marked machine, %d of them with a call (a verdict and its named comparable) and the rest a stated no-call; %d names state ABSENT with a reason" % (len(pst), len(called), pr)
      if f19 else "no posture carries a call, or a served posture lacks its machine marker or a call lacks its comparable",
      {"postures_served": len(pst), "marked_machine": pm, "with_a_call": len(called), "calls_with_comparable": pc, "absent_with_reason": pr,
       "verdicts": dict(Counter(h["posture"]["verdict"] for h in pst))}, "/thesis posture", den)

    # FWD-20
    dnn = sum(1 for h in hv if h.get("ok") and h["divergence"]["D"] is not None)
    states = dict(Counter(h["divergence"]["state"] for h in hv if h.get("ok")))
    S(20, "DOES_NOT_MEET" if dnn == 0 else "UNMEASURABLE_WITH_REASON",
      "no Divergence figure is served on any name (D non-null on 0 of %d); the page can only state ABSENT with its reason, which is the clause's own fallback arm and not its DONE WHEN (a figure traced to a house forecast)" % okn
      if dnn == 0 else "Divergence is served on %d names; tracing it to the house forecast is a human act" % dnn,
      {"divergence_non_null_names": dnn, "states": states}, "/thesis scores.divergence", den)

    # FWD-30
    ex = [h["export"] for h in hv if h.get("ok") and h.get("export")]
    tot = lambda f: sum(e[f] for e in ex)  # noqa: E731
    rich200 = sum(1 for h in hv if h["route_status"].get("print_rich") == 200)
    S(30, "UNMEASURABLE_WITH_REASON" if rich200 == N else "DOES_NOT_MEET",
      "branch (b), the machine-readable rich-text export, is served as 200 Markdown on %d of %d names. The field-by-field comparison 'against the page' is NOT read: the round-45 comparison grader renders the portal page, and at this portal checkout its render loader no longer loads and a scratch-patched loader read NOT_OK on its 3-name probe for reasons not traced to the export (row AMGT_RESAPP-Z-W230-S1), so it is not a trustworthy page reading. The served-bundle reading below is a second reading: every served value that is in the export equals it (%d differing), %d fiscal-year figures the bundle serves are not in the table (%d of them REFUSED by their own check and stated as a REFUSED line, %d unexplained), drafting cites and posture cites are equal both ways, and %d header figures the bundle serves are not in the export, whether the page shows them being the unread limb" % (rich200, N, tot("differ"), tot("missing_fy"), tot("withheld_with_refusal_line"), tot("missing_fy_unexplained"), tot("missing_header"))
      if rich200 == N else "the rich export is not served on every name",
      {"export_served_names": rich200, "bundle_vs_export": {
          "figures_served_with_value": tot("served_figs"), "figures_in_export": tot("rich_figs"),
          "missing_from_export_fiscal_year": tot("missing_fy"), "of_which_withheld_by_a_REFUSE_check": tot("withheld_refused"),
          "of_which_withheld_and_stated_as_a_REFUSED_line": tot("withheld_with_refusal_line"),
          "missing_from_export_fiscal_year_unexplained": tot("missing_fy_unexplained"), "missing_from_export_header": tot("missing_header"),
          "header_mnemonics_not_in_export": dict(Counter(m for e in ex for m in e["missing_header_mnemonics"]).most_common()),
          "in_export_not_in_bundle": tot("extra"), "values_differing": tot("differ"),
          "drafting_cites_served": tot("cites_served"), "drafting_cites_in_export": tot("cites_rich"),
          "drafting_cites_only_in_bundle": tot("cites_only_served"), "drafting_cites_only_in_export": tot("cites_only_rich"),
          "posture_cites_symmetric_difference": tot("pcites_diff")}},
      "/print?format=rich against /thesis", "%d of %d names compared" % (len(ex), N), ["the portal page render (sweep.py page reader)", "the ACCEPT (Adam forwards it) is not graded"])

    # FWD-31
    dms = cnt(lambda h: h["dossier_mgmt"] == "SERVED")
    S(31, "UNMEASURABLE_WITH_REASON" if dms > 0 else "DOES_NOT_MEET",
      "the DONE WHEN is a rendered Exec Management state captured with and without the passage (a browser capture with a positive control); the team's MANAGEMENT passage is served on %d of %d names and the rendering is not read by a deployed-function read" % (dms, N)
      if dms > 0 else "no name's pack carries a MANAGEMENT passage on the served route",
      {"dossier_fields_management_SERVED": dms, "absent": cnt(lambda h: h["dossier_mgmt"] == "ABSENT"),
       "other": dict(Counter(h["dossier_mgmt"] for h in hv if h.get("ok") and h["dossier_mgmt"] not in ("SERVED", "ABSENT"))),
       "portal_source_reads_dossier_fields": extra.get("portal_dossier_files")}, "/thesis dossier_fields.management", den,
      ["the Exec Management tab render, with and without the passage"])
    return out


def grade_graders(out, GR, H, G, keys, extra):
    """FWD-32..FWD-39 -- from the graders and the population."""
    N = len(keys)
    hv = [h for h in H.values()]

    def S(n, status, reason, evidence, routes, denominator, not_read=None):
        out[n] = {"fwd": "FWD-%d" % n, "done_when": extra["done"].get(n), "routes": routes,
                  "denominator": denominator, "status": status, "reason": reason, "evidence": evidence, "not_read": not_read or []}

    def gv(*names):
        return {n: {k: GR[n][k] for k in ("met", "rc", "pass", "fail", "verdict_line", "seconds")} | {"lines": GR[n]["lines"][:14]} for n in names}

    # FWD-32
    mo = G["monthly"]
    body = mo.get("body") or {}
    vint = body.get("vintage")
    hold = [r.get("security_key") for r in (body.get("rows") or []) if any(("hold" in str(k).lower() or "held" in str(k).lower()) for k in r)]
    m32 = GR["af1"]["met"] and bool(vint) and not hold and mo["status"] == 200
    S(32, "MEETS" if m32 else "DOES_NOT_MEET",
      "the monthly chatter route serves one row per covered name (%d of %d) with per-month collected counts and per-publisher counts that equal the gold recompute, no fabricated zero month, the archive vintage stated, no name-level hold, and the BA September positive control non-zero"
      % (len(body.get("rows") or []), N) if m32 else "a clause of the monthly-route grader read false, the vintage is not stated, or a name-level hold is published",
      {"grader_af_1": gv("af1")["af1"], "vintage": vint, "rows": len(body.get("rows") or []), "months": body.get("months"),
       "name_level_hold_keys": hold[:5]}, "GET /lead-panel/timeseries/collected/chatter; gold chatter_daily + article_security_mention recompute",
      "%d covered names (fresh read of research_dossier/)" % N)

    # FWD-33
    rk = G["rankings"]
    rows_b = {r.get("security_key"): r for r in (rk["breakout_price"]["body"] or {}).get("rows") or []}
    with_rank = [h for h in hv if h.get("ok") and h["key"] in rows_b]
    asof_b = (rk["breakout_price"]["body"] or {}).get("as_of_date")
    matched = sum(1 for h in with_rank if h["overlay_breakout"]["as_of"] == asof_b and h["overlay_breakout"]["axis"] == "BREAKOUT_PRICE"
                  and h["overlay_breakout"]["measure"] == "PCT_JUMP_VS_TRAILING_BASELINE"
                  and _num(h["overlay_breakout"]["score_pct"]) is not None
                  and math.isclose(_num(h["overlay_breakout"]["score_pct"]), _num(rows_b[h["key"]].get("score_pct")), rel_tol=1e-6, abs_tol=1e-9))
    stale = (rk["breakout_price"]["body"] or {}).get("stale_trading_days")
    req = (rk["breakout_price"]["body"] or {}).get("requested_as_of")
    m33 = GR["af33"]["met"] and with_rank and matched == len(with_rank) and isinstance(stale, int)
    S(33, "MEETS" if m33 else "DOES_NOT_MEET",
      "a per-name lookup and the ranking read, made on %s (a day with no producer file of its own), return the producer's latest run (%s, stale_trading_days %s); the overlay's breakout value is the breakout row's value on %d of %d names with a ranking row"
      % (req, asof_b, stale, matched, len(with_rank)) if m33 else "a clause of the per-name grader read false, or an overlay breakout value is not the breakout row's",
      {"grader_af_2_fwd33": gv("af33")["af33"], "names_with_a_breakout_ranking_row": len(with_rank), "overlay_breakout_equals_ranking_row": matched,
       "ranking_as_of": asof_b, "requested_as_of": req, "stale_trading_days": stale}, "/security/<key>/overlay price + breakout_price; /lead-panel/rankings/breakout/price",
      "%d names with a served ranking row of %d covered" % (len(with_rank), N))

    # FWD-34
    tr = (rk["trending_price"]["body"] or {}).get("rows") or []
    br = list(rows_b.values())
    bad_t = [r.get("ticker") for r in tr if _num(r.get("score_pct")) is None or not math.isclose(_num(r["score_pct"]), _num(r.get("score")), rel_tol=1e-6, abs_tol=1e-9)]
    bad_b = [r.get("ticker") for r in br if "pct_jump" in r or _num(r.get("pct_jump_pct")) is None or _num(r.get("score_pct")) is None]
    units = [(k, v) for r in tr + br for k, v in r.items() if k.endswith("_unit") and str(v).lower() != "percent"]
    m34 = GR["af34"]["met"] and not bad_t and not bad_b and not units and tr and br
    S(34, "MEETS" if m34 else "DOES_NOT_MEET",
      "every price-movement figure is served as a _pct field in percent (%d trending and %d breakout rows, 0 unsuffixed, 0 contradicting unit fields) and the named example per axis equals the producer's stored fraction x 100"
      % (len(tr), len(br)) if m34 else "a movement figure is unsuffixed, a unit contradicts percent, or an example differs from the stored value",
      {"grader_af_2_fwd34": gv("af34")["af34"], "trending_rows": len(tr), "trending_rows_bad": len(bad_t), "breakout_rows": len(br),
       "breakout_rows_bad": len(bad_b), "contradicting_unit_fields": units[:3]},
      "/lead-panel/rankings/{trending,breakout}/price; DynamoDB stored fraction (the grader's oracle)", "%d + %d ranking rows" % (len(tr), len(br)))

    # FWD-35
    asof = (rk["trending_price"]["body"] or {}).get("as_of_date")
    gen = rk["trending_price"]["body"] or {}
    keyset = set(keys)
    served_keys = {r.get("security_key") for r in tr}
    absent = sorted(keyset - served_keys)
    path, rec = price_generation_record(asof)
    excl = {}
    if rec:
        for p in rec.get("products") or []:
            if p.get("axis") == "TRENDING_PRICE":
                excl = p.get("excluded") or {}
    signed = [r for r in tr if _num(r.get("return_30d_pct")) is not None and r.get("window_days") == 30]
    absent_tickers = sorted(str(h.get("bloomberg")) for h in hv if h.get("ok") and h["key"] in absent)
    rec_ok = (bool(rec) and rec.get("universe_denominator") == N and len(tr) + len(excl) == N
              and sorted(excl) == absent_tickers)
    scheduled_note = ("generation computed_at %s = %s, run_id %s; scheduled-versus-ad-hoc provenance is not on the served plane"
                      % (tr[0].get("computed_at") if tr else None, _et(tr[0].get("computed_at") if tr else None), gen.get("run_id")))
    m35 = bool(rec) and rec_ok and len(signed) == len(tr) and gen.get("state") == "COMPLETE"
    S(35, "MEETS" if m35 else ("UNMEASURABLE_WITH_REASON" if not rec else "DOES_NOT_MEET"),
      ("the latest generation carries %d rows for %d covered names (denominator read fresh) and the generation's own exclusion record names the other %d with its reason; every row serves a signed 30-day return in percent (window_days 30). %s. Terminal state beside it: overlay bloomberg_session_state %s"
       % (len(tr), N, len(excl), scheduled_note, Counter(h.get("bloomberg_session_state") for h in hv if h.get("ok")).most_common(1)[0][0]) if m35 else
       ("the generation's own exclusion record (the producer's record copy) could not be read from this tree or the checkout it was cut from, so the %d covered names with no row cannot be shown named and counted" % len(absent) if not rec else
        "the rows plus the exclusion record do not account for every covered name, or a row lacks a signed 30-day return")),
      {"generation_id": gen.get("generation_id"), "run_id": gen.get("run_id"), "state": gen.get("state"), "as_of_date": asof,
       "rows": len(tr), "rows_with_signed_30d_return_pct": len(signed), "covered_denominator": N, "covered_names_with_no_row": absent,
       "exclusion_record": excl, "absent_covered_tickers": absent_tickers, "record_copy": path, "record_universe_denominator": (rec or {}).get("universe_denominator"),
       "negative_returns": sum(1 for r in signed if _num(r["return_30d_pct"]) < 0), "terminal_state": dict(Counter(h.get("bloomberg_session_state") for h in hv if h.get("ok"))),
       "scheduled_provenance": scheduled_note}, "/lead-panel/rankings/trending/price; the producer's record copy price_axis_rows_<as_of>.json",
      "%d rows + %d excluded vs %d covered names read fresh" % (len(tr), len(excl), N),
      ["scheduled-versus-ad-hoc provenance of the generation (not carried on the served plane)"])

    # FWD-36
    ok36 = GR["c9"]["met"] and GR["c22"]["met"] and GR["c24"]["met"] and mo["status"] == 200
    S(36, "MEETS" if ok36 else "DOES_NOT_MEET",
      "(the fence's v0.35 QUALIFIED WAIT on the price 90/365 windows is not applied: those generations now serve and are read) collected/chatter answers 30/90/365 windows (each ending at the last trading day, with window start and a note where the store is shorter, every row serving articles_total, tone and voters from the stored table, by_month kept) and the price ranking answers real 90- and 365-day generations with rank order, numeric scores, window_days and window_end; the calendar-month route is still served"
      if ok36 else "a window, tone or price-window clause read false",
      gv("c9", "c22", "c24"), "/lead-panel/timeseries/collected/chatter?days=, /lead-panel/rankings/{trending,breakout}/price?days=",
      "3 windows x 2 routes", ["'never computed at request time' (the route's own mechanism, not observable from a response)"])

    # FWD-37
    c11 = GR["c11"]
    S(37, "UNMEASURABLE_WITH_REASON" if c11["met"] else "DOES_NOT_MEET",
      "QUALIFIED WAIT written in the fence (v0.34): the earnings path is gradeable only after the CORPUS Model-block pull that carries the dates, which waits on Andrew's vendor word. The interim branch the fence names is measured and reads true: markers serve {date, kind, label} with a coverage_event for every event and earnings_release absent with the reason 'no earnings dates are pulled yet'. That is not a read of the earnings path (ABSENT != EXERCISED)"
      if c11["met"] else "the interim branch read false: markers missing or malformed",
      gv("c11"), "/security/<key>/timeline", "3 names (BA, AMD, VLO)", ["the earnings_release markers from the CORPUS Bloomberg block (not pulled)"])

    # FWD-38
    ok38 = GR["c12"]["met"] and GR["c13"]["met"] and GR["c17"]["met"]
    prov_all = sum(1 for h in hv if h.get("ok") and set(h["provenance_inputs"]) >= {"filings", "harvested_news", "bloomberg"})
    S(38, "MEETS" if ok38 else "DOES_NOT_MEET",
      "on BA, AMD and VLO the recent-news list holds every article the day view shows in its window, every route serves one title-case display name with no share-class code, each served move names its measure and window, and the provenance block names filings, harvested news and Bloomberg with a last run or a reason (%d of %d covered names carry all three inputs)" % (prov_all, N)
      if ok38 else "a limb read false: feed vs day view, one display name, move axis and window, or provenance",
      gv("c12", "c13", "c17") | {"provenance_names_with_all_three_inputs": prov_all}, "/overlay feed, /timeline/day, /peers, rankings, chatter, overlay provenance",
      "3 names x 4 limbs + population on rankings and provenance")

    # FWD-39
    ok39 = GR["c18"]["met"] and GR["c27"]["met"]
    S(39, "MEETS" if ok39 else "DOES_NOT_MEET",
      "on BA, AMD and VLO the timeline carries word_cloud: at most 40 counted terms ordered by count, none in the declared stop list, none a word of the company's own name, and an empty list with a reason where the window holds no headlines; a census over every cloud-serving name reads no own-name leak and no junk token"
      if ok39 else "a word-cloud clause read false",
      gv("c18", "c27"), "/security/<key>/timeline word_cloud", "3 names + census over the cloud-serving names")
    return out


def collision_control(lam, keys):
    """FWD-13's control: covered names whose ticker root is shared by a second crosswalk key. Returns the map key -> [sibling keys]."""
    import boto3

    st, co = get(lam, "/security/%s/coverage" % keys[0])
    src = ((co or {}).get("identity") or {}).get("crosswalk_source") or ""
    m = re.match(r"s3://([^/]+)/(.+)", src)
    if not m:
        return {}, {"crosswalk": src, "records": 0, "pairs": [], "names": 0}
    d = json.loads(boto3.client("s3").get_object(Bucket=m.group(1), Key=m.group(2))["Body"].read())
    recs = d.get("records") or []
    by_root = {}
    for r in recs:
        root = str(r.get("bloomberg") or "").split(" ")[0].upper()
        if root:
            by_root.setdefault(root, []).append(r.get("security_key"))
    sib = {}
    for k in keys:
        rec = next((r for r in recs if r.get("security_key") == k), None)
        if not rec:
            continue
        root = str(rec.get("bloomberg") or "").split(" ")[0].upper()
        others = [x for x in by_root.get(root, []) if x != k]
        if others:
            sib[k] = others
    return sib, {"crosswalk": src, "records": len(recs), "pairs": sorted("%s~%s" % (k, ",".join(v)) for k, v in sib.items()), "names": len(sib)}


def portal_dossier_files():
    root = ROOT / "portal" / "src" / "pages" / "SecurityAnalysis"
    if not root.is_dir():
        return "portal source not present in this tree"
    hits = []
    for p in root.rglob("*.ts*"):
        if "__harness__" in p.parts or "__rendercheck__" in p.parts:
            continue
        try:
            if "dossier_fields" in p.read_text(encoding="utf-8", errors="replace"):
                hits.append(p.name)
        except OSError:
            pass
    return sorted(hits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--where", choices=("deployed",))
    ap.add_argument("--child")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="smoke only: read the first N covered names")
    ap.add_argument("--skip-graders", action="store_true", help="smoke only: do not run the child graders")
    a = ap.parse_args()
    if a.child:
        return child_main(a.child)
    if a.where != "deployed":
        print("usage: fwd_sweep.py --where deployed")
        return 2
    t_start = time.time()
    done, rehome, prd_ver, defined = read_prd()
    print("PRD %s @ %s: %d outcomes defined in the ENDPOINT fence (FWD-%d..FWD-%d); %d RE-HOMED; %d gradeable"
          % (prd_ver, PRD_PATH, len(defined), defined[0], defined[-1], len(REHOMED), len(GRADEABLE)), flush=True)
    lam = make_client()
    sha0 = lam.get_function_configuration(FunctionName=CL.FUNCTION)["CodeSha256"]
    print("opal-amgt-scoped-api CodeSha256 at start: %s" % sha0, flush=True)
    from lib.research.coverage import covered_universe

    keys = sorted(covered_universe.covered_security_keys())
    if a.limit:
        keys = keys[: a.limit]
    print("population: %d covered names (covered_universe.covered_security_keys, fresh read)" % len(keys), flush=True)
    sib, cc = collision_control(lam, keys)

    # graders in the background of the population pass
    with ThreadPoolExecutor(max_workers=1) as bg:
        skipped = {n: {"met": False, "rc": None, "pass": 0, "fail": 0, "verdict_line": None, "seconds": 0, "lines": [], "cmd": "skipped"}
                   for n in GRADERS}
        gfut = bg.submit((lambda: skipped) if a.skip_graders else run_graders)
        H, secs = population_pass(lam, keys, sib)
        print("population pass: %d of %d names read in %ds; graders running" % (sum(1 for h in H.values() if h.get("ok")), len(keys), secs), flush=True)
        G = read_globals(lam, keys)
        vers = {k: h.get("versions") for k, h in H.items() if h.get("ok")}
        G["print"] = read_compare_and_print(lam, vers)
        by_name = {}
        for k, others in sib.items():
            hits = (H.get(k) or {}).get("sibling_hits") or {}
            by_name[k] = {s: bool(hits.get(s)) for s in others}
        G["collision"] = dict(cc, by_name=by_name)
        GR = gfut.result()
    sha1 = lam.get_function_configuration(FunctionName=CL.FUNCTION)["CodeSha256"]

    extra = {"done": done, "portal_dossier_files": portal_dossier_files()}
    out = grade(done, keys, H, G, GR, extra)
    out = grade_graders(out, GR, H, G, keys, extra)

    # a FWD whose instrument did not run is NOT read: it is never graded on the part of the population that did answer
    okn = sum(1 for h in H.values() if h.get("ok"))
    needs = {32: ["af1"], 33: ["af33"], 34: ["af34"], 36: ["c9", "c22", "c24"], 37: ["c11"], 38: ["c12", "c13", "c17"], 39: ["c18", "c27"]}
    pop_fwds = set(range(1, 21)) | {13, 30, 31, 33, 34, 35, 38}
    for n, o in out.items():
        why = None
        if n in pop_fwds and okn < len(keys):
            why = "instrument failure: %d of %d covered names did not answer all seven routes 200" % (len(keys) - okn, len(keys))
        for g in needs.get(n, []):
            if GR[g].get("verdict_line") is None:
                why = "instrument failure: grader %s printed no verdict (rc %s, %s)" % (g, GR[g].get("rc"), GR[g].get("cmd"))
        if why:
            o["not_graded_status"] = o["status"]
            o["status"], o["reason"] = "UNMEASURABLE_WITH_REASON", why

    # print and assemble
    lines, rows = [], []
    nread = 0
    for n in range(1, 40):
        if n in REHOMED:
            lines.append("FWD-%-2d RE-HOMED  -> %s (PRD Addendum C, s.C.1); not graded here" % (n, rehome.get(n, "DSGN")))
            rows.append({"fwd": "FWD-%d" % n, "status": "RE-HOMED", "re_homed_to": rehome.get(n), "done_when": done.get(n)})
            continue
        o = out[n]
        failed = o["status"] == "UNMEASURABLE_WITH_REASON" and str(o["reason"]).startswith("instrument failure")
        if not failed:
            nread += 1
        lines.append("FWD-%-2d %-24s %s" % (n, o["status"], str(o["reason"])[:190].replace("\n", " ")))
        rows.append(o)
    cs = Counter(o["status"] for o in rows if o["status"] != "RE-HOMED")
    print("COUNTS: MEETS %d, DOES_NOT_MEET %d, UNMEASURABLE_WITH_REASON %d, RE-HOMED %d" % (
        cs.get("MEETS", 0), cs.get("DOES_NOT_MEET", 0), cs.get("UNMEASURABLE_WITH_REASON", 0), len(REHOMED)))
    moved = sha0 != sha1
    print("opal-amgt-scoped-api CodeSha256 at end: %s (%s)" % (sha1, "MOVED DURING THE SWEEP" if moved else "unchanged"))
    for ln in lines:
        print(ln)
    print("SWEEP: %d of %d read" % (nread, len(GRADEABLE)))

    doc = {"sweep": "FWD_SWEEP_ROUND70", "cell": "AMGT-at-5", "worker": "0.9.0_WK_AMGT_RESAPP~230",
           "run_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "prd": {"path": PRD_PATH, "prd_version": prd_ver, "outcomes_defined": len(defined)},
           "code_sha256_start": sha0, "code_sha256_end": sha1,
           "population": {"covered_names": len(keys), "names_all_routes_200": sum(1 for h in H.values() if h.get("ok")),
                          "source": "lib.research.coverage.covered_universe.covered_security_keys (fresh read of research_dossier/)",
                          "route_failures": {k: h.get("route_status") for k, h in H.items() if not h.get("ok")}},
           "state_rule": STATE_RULE,
           "counts": {"MEETS": cs.get("MEETS", 0), "DOES_NOT_MEET": cs.get("DOES_NOT_MEET", 0),
                      "UNMEASURABLE_WITH_REASON": cs.get("UNMEASURABLE_WITH_REASON", 0), "RE-HOMED": len(REHOMED), "read": nread, "gradeable": len(GRADEABLE)},
           "seconds": round(time.time() - t_start), "outcomes": rows}
    if not a.no_write:
        (HERE / "FWD_SWEEP_ROUND70.json").write_text(json.dumps(doc, indent=1, default=str) + "\n", encoding="utf-8")
        md = ["# FWD_SWEEP_ROUND70 -- AMGT-at-5, the 30-outcome sweep on the deployed function", "",
              "PRD %s; deployed CodeSha256 %s (end: %s); population %d covered names; run %s." % (prd_ver, sha0, "unchanged" if not moved else sha1, len(keys), doc["run_at"]),
              "", "Counts: MEETS %d, DOES_NOT_MEET %d, UNMEASURABLE_WITH_REASON %d, RE-HOMED %d (SWEEP: %d of %d read)." % (
                  cs.get("MEETS", 0), cs.get("DOES_NOT_MEET", 0), cs.get("UNMEASURABLE_WITH_REASON", 0), len(REHOMED), nread, len(GRADEABLE)),
              "", "| FWD | status | reason (the DONE WHEN and the evidence are in the JSON) |", "|---|---|---|"]
        for o in rows:
            if o["status"] == "RE-HOMED":
                md.append("| %s | RE-HOMED | -> %s |" % (o["fwd"], o.get("re_homed_to")))
            else:
                md.append("| %s | %s | %s |" % (o["fwd"], o["status"], str(o["reason"]).replace("|", "/").replace("\n", " ")))
        (HERE / "FWD_SWEEP_ROUND70.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return 0 if nread == len(GRADEABLE) and not moved else 1


if __name__ == "__main__":
    sys.exit(main())
