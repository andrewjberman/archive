"""IRPT_DASHBD round 103 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-102 ANALYSIS (msg for @9f4d4ea591; numbered 103 because round 102 already
carries the one issuance of DB-b-192, and the gate admits one issuance per round).

  DB-b-193 (~158)  the render fix: percents at their stored scale, no build language on a client-facing line, every omission said in words, the holdings table in the baseline's
                   orientation (CVO judgment), the header's firm title from the registry; 49F re-rendered, every PDF page read as an image.                              DB103-1-AC1
  DB-b-194 (~159)  the model benchmark windows compounded from the served dated series: the 32 benchmark members and the 12-month chart; nothing else moves.            DB103-2-AC1
  DB-b-195 (~160)  a READ: why Cottonwood's account_return_daily stops at 2026-06-22, its producer, its schedule (DESIRED vs APPLIED), what a resume needs.             DB103-3-AC1
  DB-b-196 (~161)  Cottonwood's account_dim and household key adapter from its silver (own prefix only): contract, adapter, tests, a read-only dry run; nothing written.  DB103-4-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import datetime as dt
import html as htmllib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PRIV = "C:/dev/_irpt_private_evidence_20261009/"
SAMPLE154 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~154/HOUSEHOLD_SAMPLE.json"
SAMPLE154_SHA = "c8075558c155ebc5034127dc4abf03c8391b31d63fbdac0b32737b533535bd71"
NEW_SAMPLE159 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~159/HOUSEHOLD_SAMPLE.json"
OUT_A = PRIV + "fwd21_sample_r103/"
SERIES_FILE = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~159/MODEL_SERIES_DAILY.json"
STEMS = ("benchmark_ultra_short_term", "benchmark_short_term", "benchmark_intermediate_term", "benchmark_long_term")
WINDOWS = ("qtd", "ytd", "last_12_months", "since_inception")
FIRM_TITLE = "49 Financial"
V030_SHA = "ca633614a32e85f4caa4ee07fdc08923d8398fd287adfc31c7f532efae89b574"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
CHART = "overview.chart.portfolio_performance_last_12_months"
BANNED = [re.compile(x, re.I) for x in (r"\b(contract|contracts|sibling|siblings|gold|parquet|schema|ruling|issuer|builder|adapter|pipeline|silver|bronze|baseline)\b",)] + \
         [re.compile(r"\b[a-z]+_[a-z_]+\b"), re.compile(r"\bC-[A-Z]+\b"), re.compile(r"\b[A-Z]{3,}_[A-Z_]+\b")]
TOL = 0.06


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def p101():
    spec = importlib.util.spec_from_file_location("p101", str(Path(__file__).resolve().parents[1] / "r101" / "p101_round101.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P = p101()
is_int, nes, sha, load, contract, is_absent, member_absent = P.is_int, P.nes, P.sha, P.load, P.contract, P.is_absent, P.member_absent


def hashlib_sha(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


def visible_text(html_text):
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html_text)
    t = re.sub(r"(?s)<[^>]*>", " ", t)
    return re.sub(r"\s+", " ", htmllib.unescape(t))


def check_render(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~158/RENDER_FIX_R103.json")
    c = contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    need(r.get("sample_sha256") == SAMPLE154_SHA and P.sha(SAMPLE154) == SAMPLE154_SHA, "the record must be bound to the round-101 filled sample (sha256 %s...)" % SAMPLE154_SHA[:12])
    sm = P.sample_json(SAMPLE154)
    outs = r.get("outputs") or {}
    paths = {k: P.private_file(root, outs.get(k), OUT_A, ext, k) for k, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
    tab = Path(paths["tab_html"]).read_text(encoding="utf-8")
    exp = Path(paths["export_html"]).read_text(encoding="utf-8")
    for name, text in (("tab_html", tab), ("export_html", exp)):
        got = set(re.findall(r'data-member="([^"]+)"', text))
        need(got == set(ids), "%s holds %d member ids, the contract has %d" % (name, len(got), len(ids)))
    # 1. percents at their stored scale
    want, scaled = set(), set()
    for k, v in sm["values"].items():
        if unit[k] != "percent":
            continue
        vals = [v] if isinstance(v, (int, float)) and not isinstance(v, bool) else ([x for x in v["by_row"].values() if isinstance(x, (int, float)) and not isinstance(x, bool)] if isinstance(v, dict) and "by_row" in v else [])
        for x in vals:
            want.add("%.1f%%" % x)
            scaled.add("%.1f%%" % (x * 100))
    scaled -= want
    need(want, "the sample holds no percent figure to check")
    for name, text in (("tab_html", tab), ("export_html", exp)):
        vt = visible_text(text)
        miss = sorted(x for x in want if x not in vt)
        need(not miss, "%s does not print %d stored percent figure(s) at their stored scale (for example %s)" % (name, len(miss), miss[0] if miss else ""))
        bad = sorted(x for x in scaled if x in vt)
        need(not bad, "%s prints a percent at 100 times its stored scale (%s)" % (name, bad[0] if bad else ""))
    need(r.get("percent_check", {}).get("stored_figures_found") == len(want) and r.get("percent_check", {}).get("scaled_figures_found") == 0, "percent_check must state stored_figures_found %d and scaled_figures_found 0" % len(want))
    # 2. no build language
    for name, text in (("tab_html", tab), ("export_html", exp)):
        vt = visible_text(text)
        for rx in BANNED:
            m = rx.search(vt)
            need(not m, "%s carries build language on a client-facing line: %r" % (name, m.group(0) if m else ""))
    need(r.get("banned_words_found") == 0, "banned_words_found must be 0")
    # 3. omissions said in words
    om = r.get("omissions")
    need(isinstance(om, list) and om and all(isinstance(x, dict) and nes(x.get("element")) and nes(x.get("words")) for x in om), "omissions must list {element, words}: every baseline chart or row the contract has no member for")
    vt = visible_text(exp)
    for x in om:
        need(x["words"] in vt, "omission %r: its words %r are not in the export text" % (x["element"], x["words"][:60]))
    # 4. the header's firm title comes from the registry, never a placeholder or a hard-coded name
    for name, text in (("tab_html", tab), ("export_html", exp)):
        vt = visible_text(text)
        need("Sample Firm" not in vt and FIRM_TITLE in vt, "%s must print the registry's firm title %r and never 'Sample Firm'" % (name, FIRM_TITLE))
    ft = r.get("firm_title") or {}
    need(ft.get("source") == "firm_registry" and ft.get("text") == FIRM_TITLE and ft.get("hard_coded") is False, "firm_title %r: source firm_registry, the text %r, hard_coded false" % (ft, FIRM_TITLE))
    # 5. footers and the PDF read as images
    P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    # 6. the portal change
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-158-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-158-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(root / "portal"), "cat-file", "-t", pt["commit"]], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip() == "commit", "portal commit %s is not in the portal repository" % pt["commit"])
    need(isinstance(pt.get("files_changed"), list) and pt["files_changed"] and all(str(f).startswith("src/pages/InvestorReporting/") for f in pt["files_changed"]), "portal.files_changed under src/pages/InvestorReporting/")
    t = r.get("tests") or {}
    need(nes(t.get("new_file")) and t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and isinstance((t.get("suite_after") or {}).get("new_failing_ids"), list) and t["suite_after"]["new_failing_ids"] == [],
         "tests %r: a new file, a failing mutant, lint 0, typecheck 0, no new failing test" % t)
    need(nes(t.get("percent_pin_test")), "tests.percent_pin_test must name the test that pins a stored 1.5 to read 1.5%")
    P.zero_effects(r)
    print("OK: %d stored percent figures print at their stored scale, no build language, %d omission(s) said in words, the header reads %s, %d PDF pages read, none clipped" % (len(want), len(om), FIRM_TITLE, pages))


def cum(returns, lo, hi):
    out = 1.0
    n = 0
    for d, x in returns:
        if lo <= d <= hi:
            out *= 1 + x
            n += 1
    return (out - 1) * 100, n


def check_bench(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~159/BENCHMARK_FILL.json")
    c = contract(root)
    members = [m["id"] for m in c["members"] if "benchmark" in m["id"]]
    need(len(members) == 32, "the contract has 32 benchmark members")
    # the contract states the new source: version above 0.3.0, the 0.3.0 bytes in its lineage, the 32 benchmark members sourced from the model series, nothing else changed
    need(tuple(int(x) for x in str(c["contract_version"]).split(".")) > (0, 3, 0) and any(x.get("sha256") == V030_SHA for x in (c.get("lineage") or [])), "the contract must be above 0.3.0 with the 0.3.0 bytes (sha256 %s...) in its lineage" % V030_SHA[:12])
    need(all(isinstance(m["source"], dict) and nes(m["source"].get("input")) and "timeseries" in str(m["source"]["input"]).lower() and nes(m["source"].get("fold")) for m in c["members"] if ("benchmark" in m["id"] or m["id"] == CHART)),
         "every benchmark member's source, and the 12-month chart's, must be an object naming the model series input (containing 'timeseries') and its fold")
    h = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "-n", "60", "--", CONTRACT_REL], capture_output=True, text=True)
    prior = None
    for cm in h.stdout.split():
        b0 = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (cm, CONTRACT_REL)], capture_output=True)
        if b0.returncode == 0 and hashlib_sha(b0.stdout) == V030_SHA:
            prior = json.loads(b0.stdout.decode("utf-8"))
            break
    need(prior is not None, "the 0.3.0 contract bytes were not found in the file's git history")
    pm = {m["id"]: m for m in prior["members"]}
    need(sorted(pm) == sorted(m["id"] for m in c["members"]) and all(pm[m["id"]] == m for m in c["members"] if "benchmark" not in m["id"] and m["id"] != CHART), "a member other than the 32 benchmark members and the 12-month chart changed in the contract")
    old = P.sample_json(SAMPLE154)
    need(P.sha(SAMPLE154) == SAMPLE154_SHA and r.get("prior_sample_sha256") == SAMPLE154_SHA, "the prior sample must be the unchanged round-101 sample")
    need(Path(NEW_SAMPLE159).is_file() and r.get("sample_sha256") == P.sha(NEW_SAMPLE159), "the new sample must be at %s and the record bound to its bytes" % NEW_SAMPLE159)
    new = P.sample_json(NEW_SAMPLE159)
    try:
        P.p97(root).check_sample_shape(new, c)
    except Exception as e:  # the round-97 shape check has its own Fail class
        raise Fail("the new sample does not conform to the filled-report shape: %s" % e)
    chart = "overview.chart.portfolio_performance_last_12_months"
    for k, v in old["values"].items():
        if k not in members and k != chart:
            need(new["values"][k] == v, "member %s changed: only the benchmark members and the 12-month chart may move" % k)
    need(new["household"] == old["household"], "the household block must be unchanged")
    # the daily model series, in the worker's normalised file
    need(Path(SERIES_FILE).is_file() and r.get("series_sha256") == P.sha(SERIES_FILE), "the daily model series file must be at %s and hashed in series_sha256" % SERIES_FILE)
    series = json.loads(Path(SERIES_FILE).read_text(encoding="utf-8"))
    st = series.get("stems") or {}
    need(sorted(st) == sorted(STEMS), "the series file must hold the four stems %s" % (STEMS,))
    ser = {k: [(dt.date.fromisoformat(d), float(x)) for d, x in v] for k, v in st.items()}
    need(all(len(v) > 400 for v in ser.values()), "each stem's daily series must hold more than 400 days")
    src = r.get("source") or {}
    need(nes(src.get("served_object")) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(src.get("data_as_of") or "")) and nes(src.get("return_basis")), "source %r: served_object, data_as_of (ISO) and return_basis in words (the claim the figures carry)" % src)
    R = dt.date.fromisoformat(old["household"]["as_of"])
    ws = r.get("window_starts") or {}
    q0 = dt.date(R.year, 3 * ((R.month - 1) // 3) + 1, 1)
    try:
        y12 = dt.date(R.year - 1, R.month, R.day) + dt.timedelta(days=1)
    except ValueError:
        y12 = dt.date(R.year - 1, R.month, 28) + dt.timedelta(days=1)
    need(ws.get("qtd") == q0.isoformat() and ws.get("ytd") == dt.date(R.year, 1, 1).isoformat() and ws.get("last_12_months") == y12.isoformat() and ws.get("since_inception") == old["household"]["first_data_date"],
         "window_starts %r must be qtd %s, ytd %s, last_12_months %s, since_inception the household's first data date (the returns count days strictly after it)" % (ws, q0, dt.date(R.year, 1, 1), y12))
    start = {"qtd": q0, "ytd": dt.date(R.year, 1, 1), "last_12_months": y12}
    first = {a["account_id"]: dt.date.fromisoformat(a["first_data_date"]) for a in old["household"]["accounts"]}
    hh_first = dt.date.fromisoformat(old["household"]["first_data_date"])
    filled = 0
    n_checked = 0
    for mid in members:
        v = new["values"][mid]
        stem = next(s for s in STEMS if mid.endswith(s))
        win = next(w for w in WINDOWS if (".%s." % w) in mid)
        rows = v["by_row"].items() if isinstance(v, dict) and "by_row" in v else [(None, v)]
        any_fig = False
        for key, x in rows:
            if is_absent(x):
                continue
            need(isinstance(x, (int, float)) and not isinstance(x, bool), "member %s holds a value that is not a figure" % mid)
            any_fig = True
            if win == "since_inception":
                fd = first.get(key, hh_first)
                exp, n = cum(ser[stem], fd + dt.timedelta(days=1), R)
            else:
                exp, n = cum(ser[stem], start[win], R)
            need(n > 0 and abs(round(exp, 1) - x) <= TOL, "member %s: stored %s but compounding the daily series gives %.2f" % (mid, x, exp))
            n_checked += 1
        filled += 1 if any_fig else 0
        need(any_fig or member_absent(v), "member %s is neither filled nor absent" % mid)
    need(r.get("filled_of_32") == filled and filled >= 1, "filled_of_32 must equal the sample's %d (and be above 0)" % filled)
    bm = r.get("benchmark_members")
    need(isinstance(bm, dict) and sorted(bm) == sorted(members) and all(x in ("filled", "absent") for x in bm.values()) and sum(1 for x in bm.values() if x == "filled") == filled, "benchmark_members must state filled or absent for each of the 32")
    # the 12-month chart draws from the series
    ch = new["values"][chart]
    need(isinstance(ch, list) and sum(1 for s in ch if isinstance(s, dict) and any(n.split()[0].lower() in str(s.get("name", "")).lower() for n in ("ultra-short", "short", "intermediate", "long"))) >= 4, "the 12-month chart must carry the four model benchmark series")
    bs = [s for s in ch if isinstance(s, dict) and len(s.get("points") or []) >= 100]
    need(len(bs) >= 4, "four chart series must hold 100 or more points each")
    for s in bs[:4]:
        need(set(s.keys()) == {"name", "points"} and all(isinstance(p, dict) and set(p) == {"date", "value"} for p in s["points"]), "a chart series is {name, points: [{date, value}]}")
    P.zero_effects(r)
    bf = root / D / "0.9.0_WK_IRPT_DASHBD~159" / "build_sample.py"
    need(bf.is_file() and r.get("builder_sha256") == P.sha(bf), "the builder must be in the worker's folder and hashed")
    need(r.get("firm_branches_outside_adapter") == 0, "firm_branches_outside_adapter must be 0")
    print("OK: %d of the 32 benchmark members filled (%d figures re-computed from the daily series), the 12-month chart carries the four series, nothing else moved" % (filled, n_checked))


def check_stale(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~160/COTTONWOOD_RETURN_STALE.json")
    pr = r.get("producer") or {}
    need(nes(pr.get("name")) and nes(pr.get("entry_file")) and (root / pr["entry_file"]).is_file(), "producer %r: a name and an existing entry_file" % pr)
    sc = r.get("schedule") or {}
    need(sc.get("trigger_kind") in ("EVENTBRIDGE", "S3_EVENT", "MANUAL", "NONE", "OTHER") and nes(sc.get("desired")) and nes(sc.get("applied")) and nes(sc.get("evidence")), "schedule %r: trigger_kind, desired, applied (DESIRED vs APPLIED) and evidence in words" % sc)
    need(r.get("newest_partition") == "2026-06-22" and r.get("address") and nes(r["address"]), "newest_partition must read 2026-06-22 (the issuer's own list) with the address")
    ro = str(r.get("read_on") or "")
    need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", ro) and ro >= "2026-10-14", "read_on must be an ISO date on or after 2026-10-14")
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc  # the one frontier
    n = len(tc.trading_days_between("2026-06-22", ro)) - 1
    need(r.get("trading_days_since_newest") == n, "trading_days_since_newest must equal %d (lib/trading_calendar.py, counted after the newest partition up to %s)" % (n, ro))
    need(nes(r.get("why_it_stops")) and nes(r.get("resume_needs")) and isinstance(r.get("resume_writes_gold"), bool), "why_it_stops, resume_needs (words) and resume_writes_gold (bool: a resume that writes is a later round under a pair)")
    need(nes(r.get("recommendation")), "recommendation must be stated")
    P.zero_effects(r)
    print("OK: Cottonwood account_return_daily stops at 2026-06-22, %d trading days before %s; producer %s, trigger %s" % (n, ro, pr["name"], sc["trigger_kind"]))


def check_dim(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~161/COTTONWOOD_ACCOUNT_DIM.json")
    cf = "org/standards/IRPT_DASHBD_ACCOUNT_DIM_CONTRACT.json"
    need((root / cf).is_file(), "no %s" % cf)
    c = json.loads((root / cf).read_bytes().decode("utf-8"))
    need(c.get("table") == "account_dim" and P.HEX64.fullmatch(str(c.get("schema_hash") or "")) and isinstance(c.get("columns"), (list, dict)) and c["columns"] and nes(c.get("schema_hash_basis")),
         "the contract needs table account_dim, columns, schema_hash and schema_hash_basis")
    cols = [x if isinstance(x, str) else x.get("name") for x in (c["columns"] if isinstance(c["columns"], list) else list(c["columns"]))]
    need(all(k in cols for k in ("firm", "account_id", "method_version", "coverage")), "every C-SHAPE table carries firm, account_id, method_version and coverage")
    ad = r.get("adapter") or {}
    f = str(ad.get("file") or "")
    need(f.startswith("data/assets/scripts/gold/irpt_reporting/") and f.endswith(".py") and (root / f).is_file() and ad.get("sha256") == sha(root / f) and ad.get("tracked") is True, "adapter %r: a tracked .py under data/assets/scripts/gold/irpt_reporting/ hashed as recorded" % ad)
    need("cottonwood" in (root / f).read_text(encoding="utf-8").lower() and r.get("firm_branches_outside_adapter") == 0, "the adapter is the one place firm knowledge lives (Black Diamond column names appear only in it)")
    # the schema hash is recomputed from the adapter's own ARROW_SCHEMA
    code = ("import sys, hashlib, importlib.util\nspec = importlib.util.spec_from_file_location('m', %r)\nm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
            "lines = sorted('%%s:%%s' %% (f.name, f.type) for f in m.ARROW_SCHEMA)\nprint(hashlib.sha256('\\n'.join(lines).encode()).hexdigest())\n") % str((root / f).resolve())
    o = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, cwd=str(root))
    need(o.returncode == 0 and o.stdout.strip() == c["schema_hash"], "the schema hash recomputed from the adapter's ARROW_SCHEMA must equal the contract's (%s)" % (o.stderr.strip()[-160:] or o.stdout.strip()[:16]))
    t = r.get("tests") or {}
    need(nes(t.get("file")) and (root / t["file"]).is_file() and is_int(t.get("passed")) and t["passed"] >= 3 and t.get("failed") == 0 and t.get("mutant_failed") is True, "tests %r: a file, 3 or more passing, none failing, a mutant that failed" % t)
    q = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", str((root / t["file"]).resolve())], capture_output=True, text=True, cwd=str(root))
    need(q.returncode == 0, "the adapter's test file does not pass when the checker runs it: %s" % q.stdout.strip()[-200:])
    dr = r.get("dry_run") or {}
    pre = dr.get("prefixes_read")
    need(isinstance(pre, list) and pre and all(isinstance(x, dict) and x.get("bucket") == "opal-data-assets" and str(x.get("prefix") or "").startswith("blackdiamond/cottonwood/") for x in pre),
         "dry_run.prefixes_read must be {bucket opal-data-assets, prefix under blackdiamond/cottonwood/} only: never another firm's prefix")
    need(is_int(dr.get("accounts")) and dr["accounts"] > 0 and is_int(dr.get("relationship_ids")) and dr["relationship_ids"] > 0 and isinstance(dr.get("null_counts"), dict) and nes(dr.get("target_address")),
         "dry_run needs accounts, relationship_ids (the household key), null_counts per column and the target_address from lib/opal_naming.py address() (computed, not written)")
    need("cottonwood" in dr["target_address"] and "account_dim" in dr["target_address"] and dr["target_address"].startswith("s3://opal-data-cottonwood/irpt/cottonwood/gold/"), "target_address must be the address() gold home s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/...")
    P.zero_effects(r)
    print("OK: account_dim contract (%d columns, hash recomputed equal), adapter and %d tests pass, dry run read %d prefix(es) of Cottonwood only: %d accounts, %d relationship ids" % (len(cols), t["passed"], len(pre), dr["accounts"], dr["relationship_ids"]))


FNS = {"DB103-1-AC1": check_render, "DB103-2-AC1": check_bench, "DB103-3-AC1": check_stale, "DB103-4-AC1": check_dim}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FNS[cid](root)
    except (Fail, P.Fail) as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB103"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
