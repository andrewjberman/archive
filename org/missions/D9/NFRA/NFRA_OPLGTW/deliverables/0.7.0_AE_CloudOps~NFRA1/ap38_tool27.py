#!/usr/bin/env python
"""OG-ap-38 Phase A step 3(e) (amendment A3, the CTO's CT1): THE 27-TOOL READ, LIVE CODE AGAINST CANDIDATE. Each of the 27 tools of ap23_served_harness's set runs in its OWN fresh process under a named hard guard,
once on the LIVE code and once on the CANDIDATE, one process at a time, with the SAME fixed arguments (derived once, on the live code, and written to the scratch stage; for the tools that take a security,
fund, scope or part the same values on both; no client value is printed or recorded: the record holds hashes, outcome words and counts). READ ONLY; nothing is deployed.
  python ap38_tool27.py <out.json> <release_sha>        -> RUNNER (repository root): uploads this file, ap38_measure.py, the guard and the candidate's files; runs the driver once over SSM
  python ap38_tool27.py --driver <expected_md5_json>    -> HOST DRIVER (runs no gateway code; spawns the guarded children)
  python ap38_tool27.py --args <stage>                  -> HOST CHILD: derive the fixed arguments on <stage> into <stage>/args.json (mode 600)
  python ap38_tool27.py --tool <name> <stage>           -> HOST CHILD: one tool, one process: outcome class, refusal code, absent_reason, row count, the sha256 of its canonical answer and of each top-level key
Guards: oom_score_adj_1000_cgroup_memmax_1400mb (systemd-run --scope MemoryMax=1400M ...) for the 26 tools that read Parquet (pyarrow cannot start its pools under RLIMIT_AS), and
oom_score_adj_1000_rlimit_as_1400mb for etfs_compare_peers (its live run is the runaway; the address-space cap makes it a MemoryError, never a host event)."""
from __future__ import annotations

import asyncio
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ap38_measure as m  # noqa: E402

FIRM = m.FIRM
PY, GUARD = m.PY, m.GUARD
GUARD_CG, GUARD_AS = m.CGROUP_GUARD_NAME, m.GUARD_NAME
VOLATILE = {"generated_at", "served_at", "timestamp", "elapsed_s", "seconds", "request_id", "nonce", "retrieved_at", "fetched_at"}
TOOLS = ["etfs_get_peer_group_members", "etfs_get_rival_fund_holdings", "etfs_who_holds", "etfs_get_security_reference", "etfs_get_coverage", "etfs_get_fund_trades", "etfs_get_fund_flows",
         "etfs_compare_peers", "etfs_get_research_notes", "etfs_get_rival_page_status", "client_resolve_account", "client_get_holdings", "client_get_transactions", "client_get_allocation",
         "client_get_fees", "etfs_get_new_securities", "etfs_get_fund_bloomberg_characteristics", "etfs_get_fund_snapshot", "portal_get_correlations", "portal_get_etf_returns",
         "portal_get_factor_tilts", "portal_get_model_portfolio_timeseries", "portal_get_peer_performance", "portal_get_trending", "portal_get_cma_assumptions", "mdpf_get_model_composition",
         "mdpf_get_security_classification"]
ENVELOPE = ("as_of", "source_keys", "denominator", "absent_reason")


def scan(obj, keys, out=None):
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and isinstance(v, str):
                out.append(v)
            else:
                scan(v, keys, out)
    elif isinstance(obj, list):
        for v in obj:
            scan(v, keys, out)
    return out


def enveloped(res):
    return isinstance(res, dict) and all(k in res for k in ENVELOPE)


def refused(res):
    return isinstance(res, dict) and bool(res.get("guard_denied") or res.get("code"))


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items() if k not in VOLATILE}
    if isinstance(o, list):
        return [clean(v) for v in o]
    return o


def dig(o):
    return hashlib.sha256(json.dumps(clean(o), sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def row_count(res):
    n = 0
    if isinstance(res, dict):
        for k in ("rows", "holdings", "members", "candidates", "trades", "positions", "transactions", "fees", "series", "notes", "weights"):
            v = res.get(k)
            if isinstance(v, list):
                n += len(v)
    return n


def modules():
    from app import audit, context, identity_scope
    from app import etfs_funds as ef, etfs_rivals as rv, etfs_rivals_flow as rf, etfs_silver as es
    from app import mdpf_classification as mc, portal_json_served as pj, portal_served as ps
    audit.log_call = lambda *a, **k: None
    opal = context.make_principal(context.MOCK_TENANT_ID, m.PROBE_OID, "%s@%s" % (m.PROBE_LOCAL, identity_scope.OPAL_USERS_DOMAIN))
    return context, opal, ef, rv, rf, es, mc, pj, ps


# ----------------------------------------------------------------------------------------------------- children (INSIDE the guard)
def child_args(stage):
    m.load_env(stage)
    context, opal, ef, rv, rf, es, mc, pj, ps = modules()
    context.set_current_principal(opal)
    homes = ["IDVZ", "PFOE"]
    funds = []
    for t in scan(rv.etfs_get_coverage(), ("fund_ticker", "ticker", "fund")):
        if re.fullmatch(r"[A-Z]{2,6}", t) and t not in funds:
            funds.append(t)
    rivals = [t for t in scan(rv.etfs_get_peer_group_members("IDVZ"), ("fund_ticker", "rival_ticker", "ticker")) if re.fullmatch(r"[A-Z]{2,6}", t) and t not in homes]
    cand_funds = rivals + [f for f in funds if f not in rivals] + homes
    sec, fund_h = None, None
    for f in cand_funds[:6]:
        res = rv.etfs_get_rival_fund_holdings(f)
        vals = scan(res, rv.IDENTIFIER_FIELDS) if enveloped(res) else []
        if vals:
            sec, fund_h = vals[0], f
            break
    fund = fund_h or (cand_funds[0] if cand_funds else None)
    try:
        home_fund = ef.FUND_TICKERS[0]
    except Exception:
        home_fund = None
    scope = None
    try:
        scopes = ps._firm_values(ps._row(ps._loaded()))
        scope = "global" if "global" in scopes else (scopes[0] if scopes else None)
    except Exception:
        pass
    part = None
    try:
        parts = pj.factor_parts()
        part = parts[0] if parts else None
    except Exception:
        pass
    tk = None
    for t in ([sec] if sec else []) + ["AAPL", "SPY", "MSFT"]:
        res = mc.mdpf_get_security_classification(t)
        if enveloped(res) and not refused(res):
            tk = t
            if res.get("absent_reason") is None:
                break
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    l4 = ref.split("/")[0][-4:]
    args = {"fund": fund, "sec": sec, "home_fund": home_fund, "scope": scope, "part": part, "tk": tk, "last4": l4,
            "today": dt.datetime.now(dt.timezone.utc).date().isoformat()}
    fd = os.open(os.path.join(stage, "args.json"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.write(fd, json.dumps(args).encode("utf-8"))
    os.close(fd)
    m.emit({"derived": {k: (v is not None) for k, v in args.items()}})


def call_tool(name, a, ref, mods):
    context, opal, ef, rv, rf, es, mc, pj, ps = mods
    from app import tools
    frm = (dt.date.fromisoformat(a["today"]) - dt.timedelta(days=m.WINDOW_DAYS)).isoformat()
    if name.startswith("client_"):
        context.set_current_principal(m.master_setup())
        fn = {"client_resolve_account": lambda: tools.client_resolve_account(firm=FIRM, account_last4=a["last4"]),
              "client_get_holdings": lambda: tools.client_get_holdings(firm=FIRM, account=ref),
              "client_get_allocation": lambda: tools.client_get_allocation(firm=FIRM, account=ref),
              "client_get_transactions": lambda: tools.client_get_transactions(firm=FIRM, account=ref, from_date=frm, to_date=a["today"]),
              "client_get_fees": lambda: tools.client_get_fees(firm=FIRM, account=ref, from_date=frm, to_date=a["today"])}[name]
    else:
        context.set_current_principal(opal)
        fn = {"etfs_get_peer_group_members": lambda: rv.etfs_get_peer_group_members("IDVZ"),
              "etfs_get_rival_fund_holdings": lambda: rv.etfs_get_rival_fund_holdings(a["fund"]),
              "etfs_who_holds": lambda: rv.etfs_who_holds(a["sec"] or "AAPL"),
              "etfs_get_security_reference": lambda: rv.etfs_get_security_reference(a["sec"] or "AAPL"),
              "etfs_get_coverage": lambda: rv.etfs_get_coverage(),
              "etfs_get_fund_trades": lambda: rf.etfs_get_fund_trades(fund_ticker=a["fund"]),
              "etfs_get_fund_flows": lambda: rf.etfs_get_fund_flows(a["fund"]),
              "etfs_compare_peers": lambda: rf.etfs_compare_peers("IDVZ", "x", "y"),
              "etfs_get_research_notes": lambda: rf.etfs_get_research_notes(a["fund"]),
              "etfs_get_rival_page_status": lambda: rf.etfs_get_rival_page_status(),
              "etfs_get_new_securities": lambda: es.etfs_get_new_securities(),
              "etfs_get_fund_bloomberg_characteristics": lambda: es.etfs_get_fund_bloomberg_characteristics(a["home_fund"] or a["fund"]),
              "etfs_get_fund_snapshot": lambda: es.etfs_get_fund_snapshot(a["home_fund"] or a["fund"]),
              "portal_get_correlations": lambda: pj.portal_get_correlations(),
              "portal_get_etf_returns": lambda: pj.portal_get_etf_returns(),
              "portal_get_factor_tilts": lambda: pj.portal_get_factor_tilts(a["part"] or ""),
              "portal_get_model_portfolio_timeseries": lambda: pj.portal_get_model_portfolio_timeseries(),
              "portal_get_peer_performance": lambda: pj.portal_get_peer_performance(),
              "portal_get_trending": lambda: pj.portal_get_trending(),
              "portal_get_cma_assumptions": lambda: pj.portal_get_cma_assumptions(),
              "mdpf_get_model_composition": lambda: ps.mdpf_get_model_composition(a["scope"] or "global"),
              "mdpf_get_security_classification": lambda: mc.mdpf_get_security_classification(a["tk"] or "AAPL")}[name]
    r = fn()
    if asyncio.iscoroutine(r):
        r = asyncio.run(r)
    return r


def child_tool(name, stage):
    m.load_env(stage)
    a = json.load(open(os.path.join(stage, "args.json"), encoding="utf-8"))
    ref = open(os.path.join(stage, "ref.txt"), encoding="utf-8").read().strip()
    mods = modules()
    out = {"tool": name}
    t0 = time.monotonic()
    try:
        r = call_tool(name, a, ref, mods)
        out["wall_s"] = round(time.monotonic() - t0, 2)
        out["class"] = "refused" if refused(r) else ("answered" if isinstance(r, dict) else type(r).__name__)
        out["code"] = r.get("code") if isinstance(r, dict) and refused(r) else None
        out["absent"] = r.get("absent_reason") if isinstance(r, dict) else None
        out["rows"] = row_count(r)
        out["digest"] = dig(r)
        out["keys"] = {k: dig(v) for k, v in r.items() if k not in VOLATILE} if isinstance(r, dict) else None
        out["enveloped"] = enveloped(r)
    except MemoryError:
        out["wall_s"] = round(time.monotonic() - t0, 2)
        out["class"], out["code"] = "failed", "MemoryError"
    except BaseException as exc:          # a tool that raises is a failure of that code, named
        out["wall_s"] = round(time.monotonic() - t0, 2)
        out["class"], out["code"] = "failed", type(exc).__name__
        out["error_text"] = str(exc)[:120]
    out["vm_hwm_mb"] = round(m.hwm_mb(), 1)
    m.emit(out)


# ----------------------------------------------------------------------------------------------------- driver (runs NO gateway code)
def run_child(args, guard):
    """One fresh guarded process. guard 'cgroup' (systemd-run scope, no address-space cap) or 'as' (the address-space cap)."""
    me = os.path.abspath(__file__)
    if guard == "cgroup":
        cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", "120", me] + args
    else:
        cmd = [PY, GUARD, "120", me] + args
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
    lines = [ln for ln in p.stdout.splitlines() if ln.startswith("AP38_RESULT ")]
    res = json.loads(lines[-1].split(" ", 1)[1]) if lines else {"class": "failed", "code": "no_result", "stderr_tail": p.stderr[-300:], "stdout_tail": p.stdout[-200:]}
    res["exit_code"] = p.returncode
    if p.returncode in (-9, -6, 137):
        res.setdefault("class", "failed")
        res["killed_by_guard"] = True
    return res


def same_answer(x, y):
    return x.get("class") == "answered" and y.get("class") == "answered" and x.get("digest") == y.get("digest")


def driver(md5s_json):
    exp = json.loads(md5s_json)
    base = "/tmp/ap38_t27_%d" % os.getpid()
    cand, live = base + "_cand", base + "_live"
    res = {"scratch_removed": False, "guard": GUARD_CG, "guard_for_etfs_compare_peers": GUARD_AS}
    try:
        for d in (cand, live):
            os.makedirs(d, mode=0o700)
            shutil.copytree(os.path.join(m.SERVICE, "app"), os.path.join(d, "app"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copytree(os.path.join(m.SERVICE, "lib"), os.path.join(d, "lib"), ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel in m.CAND_FILES:
            shutil.copyfile("/tmp/ap38_cand_" + os.path.basename(rel), os.path.join(cand, rel))
        res["staged_md5_equals_release"] = {rel: hashlib.md5(open(os.path.join(cand, rel), "rb").read()).hexdigest() == md5 for rel, md5 in exp.items() if rel in m.CAND_FILES}
        # the resolve child lives in ap38_measure; run it through that script under the cgroup guard
        cmd = ["systemd-run", "--scope", "--quiet", "-p", "MemoryMax=1400M", "-p", "MemoryHigh=1100M", "-p", "MemorySwapMax=0", "--", PY, GUARD, "--cgroup", "120", "/tmp/ap38_measure.py", "--resolve", live]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=200)
        res["ref_resolved"] = "AP38_RESULT {\"ref_resolved\":true}" in p.stdout
        if not res["ref_resolved"]:
            res["fatal"] = "no account ref resolved: " + (p.stdout[-200:] + p.stderr[-200:])
            return res
        for d in (cand,):
            shutil.copyfile(os.path.join(live, "ref.txt"), os.path.join(d, "ref.txt"))
            os.chmod(os.path.join(d, "ref.txt"), 0o600)
        ra = run_child(["--args", live], "cgroup")
        res["args_derived"] = ra.get("derived")
        if not ra.get("derived"):
            res["fatal"] = "arguments not derived: %s" % json.dumps(ra)[:300]
            return res
        shutil.copyfile(os.path.join(live, "args.json"), os.path.join(cand, "args.json"))
        os.chmod(os.path.join(cand, "args.json"), 0o600)
        detail = {}
        for name in TOOLS:
            guard = "as" if name == "etfs_compare_peers" else "cgroup"
            lv = run_child(["--tool", name, live], guard)
            cd = run_child(["--tool", name, cand], guard)
            row = {"guard": GUARD_AS if guard == "as" else GUARD_CG, "live": {k: lv.get(k) for k in ("class", "code", "absent", "rows", "digest", "wall_s", "vm_hwm_mb", "exit_code", "killed_by_guard", "stderr_tail", "error_text")},
                   "candidate": {k: cd.get(k) for k in ("class", "code", "absent", "rows", "digest", "wall_s", "vm_hwm_mb", "exit_code", "killed_by_guard", "stderr_tail", "error_text")}}
            if lv.get("class") == "answered" and cd.get("class") == "answered" and lv.get("digest") != cd.get("digest"):
                lv2 = run_child(["--tool", name, live], guard)         # is the difference time-driven? the live code again
                row["live_repeat"] = {k: lv2.get(k) for k in ("class", "digest")}
                row["live_repeat_equals_first_live"] = lv2.get("digest") == lv.get("digest")
                lk, ck, l2k = lv.get("keys") or {}, cd.get("keys") or {}, lv2.get("keys") or {}
                row["top_level_keys_differing_live_vs_candidate"] = sorted(k for k in set(lk) | set(ck) if lk.get(k) != ck.get(k))
                row["top_level_keys_differing_live_vs_live_repeat"] = sorted(k for k in set(lk) | set(l2k) if lk.get(k) != l2k.get(k))
            detail[name] = row
        equal, both_failed, better, bad_ref, bad_diff = 0, [], [], [], []
        for name, row in detail.items():
            lv, cd = row["live"], row["candidate"]
            if lv.get("class") == "answered" and cd.get("class") == "answered":
                if lv.get("digest") == cd.get("digest"):
                    equal += 1
                elif row.get("live_repeat_equals_first_live") is False and not (set(row.get("top_level_keys_differing_live_vs_candidate") or []) - set(row.get("top_level_keys_differing_live_vs_live_repeat") or [])):
                    equal += 1                              # the live code differs from ITSELF in exactly these keys: time-driven, stated in the detail
                    row["equal_by"] = "the live code differs from itself in exactly the keys that differ from the candidate"
                else:
                    bad_diff.append(name)
            elif lv.get("class") == "answered":
                bad_ref.append(name)
            elif cd.get("class") == "answered":
                better.append(name)
            else:
                both_failed.append(name)
        res["tool27"] = {"tools": len(TOOLS), "equal": equal, "both_failed": both_failed, "candidate_answered_live_failed": better, "live_answered_candidate_refused": bad_ref, "answers_differ": bad_diff,
                         "guard": GUARD_CG, "guard_for_etfs_compare_peers": GUARD_AS}
        res["detail"] = detail
    finally:
        for d in (cand, live):
            shutil.rmtree(d, ignore_errors=True)
        res["scratch_removed"] = not any(os.path.exists(d) for d in (cand, live))
        res["host_pct_after"] = round(m.host_pct(), 1)
    return res


def runner(outp, release_sha):
    import boto3
    g = "infra/aws/ec2/opal-gateway/"
    here = os.path.dirname(os.path.abspath(__file__))
    s3 = boto3.client("s3")
    exp = {}
    for rel in ("app/typed_scope.py", "app/etfs_rivals_flow.py", "deploy/opal-gateway.service"):
        blob = subprocess.run(["git", "show", "%s:%s" % (release_sha, g + rel)], capture_output=True, check=True).stdout
        exp[rel] = hashlib.md5(blob).hexdigest()
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/ap38_cand_" + os.path.basename(rel), Body=blob)
    for n in ("ap38_tool27.py", "ap38_measure.py", "ap38_guard.py"):
        s3.put_object(Bucket=m.BUCKET, Key="ec2/opal-gateway/" + n, Body=io.open(os.path.join(here, n), "rb").read())
    pulls = " && ".join("aws s3 cp s3://%s/ec2/opal-gateway/%s /tmp/%s --region us-east-1 >/dev/null" % (m.BUCKET, n, n)
                        for n in ("ap38_tool27.py", "ap38_measure.py", "ap38_guard.py", "ap38_cand_typed_scope.py", "ap38_cand_etfs_rivals_flow.py", "ap38_cand_opal-gateway.service"))
    cmd = "cd /opt/opal-gateway && rm -f /tmp/ap38_tool27.py /tmp/ap38_measure.py /tmp/ap38_guard.py /tmp/ap38_cand_* && %s && %s /tmp/ap38_tool27.py --driver '%s'" % (pulls, PY, json.dumps(exp))
    ssm = boto3.client("ssm")
    cid = ssm.send_command(InstanceIds=[m.INSTANCE], DocumentName="AWS-RunShellScript", Parameters={"commands": [cmd]}, TimeoutSeconds=2400)["Command"]["CommandId"]
    inv = None
    for _ in range(600):
        time.sleep(4)
        try:
            inv = ssm.get_command_invocation(CommandId=cid, InstanceId=m.INSTANCE)
        except Exception:
            continue
        if inv["Status"] not in ("Pending", "InProgress", "Delayed"):
            break
    so = inv.get("StandardOutputContent", "")
    io.open(outp + ".raw.txt", "w", encoding="utf-8", newline="\n").write("status=%s\n--- STDOUT ---\n%s\n--- STDERR ---\n%s\n" % (inv["Status"], so, inv.get("StandardErrorContent", "")[-600:]))
    if "AP38_T27_JSON" not in so:
        raise SystemExit("no marker; status=%s stderr=%s" % (inv["Status"], inv.get("StandardErrorContent", "")[-300:]))
    doc = json.loads(so.split("AP38_T27_JSON", 1)[1].strip())
    doc["ssm_command_id"] = cid
    io.open(outp, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({k: v for k, v in doc.items() if k != "detail"}, indent=1))


if __name__ == "__main__":
    a = sys.argv
    if "--args" in a:
        child_args(a[a.index("--args") + 1])
    elif "--tool" in a:
        i = a.index("--tool")
        child_tool(a[i + 1], a[i + 2])
    elif "--driver" in a:
        print("AP38_T27_JSON")
        try:
            print(json.dumps(driver(a[a.index("--driver") + 1]), separators=(",", ":"), default=str))
        except Exception:
            import traceback
            print(json.dumps({"fatal": traceback.format_exc()[-900:]}))
            sys.exit(1)
    else:
        runner(a[1], a[2])
