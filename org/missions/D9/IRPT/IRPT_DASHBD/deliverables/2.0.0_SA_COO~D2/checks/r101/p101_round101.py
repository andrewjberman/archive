"""IRPT_DASHBD round 101 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msgs 7451 and 7465 (CTO rounds 99-100 analysis, FWD-21 enrichment).

  DB-b-187 (~152)  the three render defects fixed (absent reason printed once per section, the as-of footer, charts) and the real sample re-rendered, the PDF read as an image   DB101-1-AC1
  DB-b-188 (~153)  the 73 ABSENT members of the real sample classified (a) mappable now, (b) derivable by a ratified rule, (c) truly absent                              DB101-2-AC1
  DB-b-189 (~154)  every (a) member filled by the builder (now firm-parameterised), same household, nothing else moves                                                 DB101-3-AC1
  DB-b-190 (~155)  a READ of what Cottonwood and Inflection hold against the eight C-SHAPE tables (no gold exists for either: s3 irpt/ prefix empty)                  DB101-4-AC1
  DB-b-191 (~156)  the section-by-section check of the re-rendered 49 Financial report, by a seat other than the builders (mechanical record; the grade is the CVO's)   DB101-5-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import hashlib
import html as htmllib
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
PRIV = "C:/dev/_irpt_private_evidence_20261009/"
SAMPLE = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~141/HOUSEHOLD_SAMPLE.json"
OLD_SAMPLE_SHA = "76a48793d6979ba66358d4e1d2cdc3d59d34c9a5217df1b7b421715925ddf16d"
NEW_SAMPLE = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~154/HOUSEHOLD_SAMPLE.json"
OUT_A = PRIV + "fwd21_sample_r101/"
OUT_D = PRIV + "fwd21_sample_r101_final/"
SECTIONS = ("cover", "portfolio_overview", "summary_of_portfolio_accounts", "holdings_overview", "taxable_realized_gain_loss_ytd", "account_overview", "gain_loss_review_by_account", "disclosure")
TABLES = ("account_return_daily", "account_class_daily", "account_activity_daily", "account_transaction", "account_lot_realized", "account_lot_unrealized_daily", "account_dim", "market_topic_daily")
BUILDERS = {141, 146, 148, 152, 154}
MAX_REASON_REPEATS = len(SECTIONS)
RUN = re.compile(r"\d{8,}")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEXC = re.compile(r"[0-9a-f]{7,40}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def nes(v):
    return isinstance(v, str) and v.strip() != ""


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("path", "commit", "portal_commit", "file", "key", "checked_by"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def load(root, rel):
    p = root / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def contract(root):
    return json.loads((root / CONTRACT).read_bytes().decode("utf-8"))


def is_absent(v):
    return isinstance(v, dict) and set(v.keys()) == {"absent"} and isinstance(v["absent"], str) and v["absent"].strip() != ""


def sample_json(path):
    need(Path(path).is_file(), "the private sample %s is missing" % path)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def p97(root):
    spec = importlib.util.spec_from_file_location("p97", str(Path(__file__).resolve().parents[1] / "r97" / "p97_round97.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def zero_effects(r):
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0, "reads %r" % rd)
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])


def private_file(root, o, folder, ext, key):
    p = str((o or {}).get("path") or "").replace("\\", "/")
    root_abs = str(root.resolve()).replace("\\", "/").rstrip("/") + "/"
    need(p.startswith(folder) and p.endswith(ext), "outputs.%s.path must be a %s file under %s" % (key, ext, folder))
    need(not p.startswith(root_abs), "outputs.%s is inside the repo: client data never goes there" % key)
    need(Path(p).is_file() and Path(p).stat().st_size > 5000, "outputs.%s does not exist or is too small" % key)
    need(o.get("sha256") == sha(p) and o.get("bytes") == Path(p).stat().st_size, "outputs.%s sha256 or bytes differ from the file" % key)
    return p


def pdf_pages(path):
    b = Path(path).read_bytes()
    need(b[:5] == b"%PDF-", "%s is not a PDF" % path)
    return len(re.findall(rb"/Type\s*/Page[^s]", b))


def check_pdf_read(r, pages):
    need(r.get("export_pdf_pages") == pages and r.get("pdf_pages_read") == pages, "export_pdf_pages and pdf_pages_read must both equal the PDF's %d pages (record %r, %r)" % (pages, r.get("export_pdf_pages"), r.get("pdf_pages_read")))
    cl = r.get("pdf_clipping")
    need(isinstance(cl, list) and len(cl) == pages and sorted(x.get("page") for x in cl if isinstance(x, dict)) == list(range(1, pages + 1))
         and all(isinstance(x.get("clipped"), bool) and nes(x.get("note")) for x in cl), "pdf_clipping must hold one {page, clipped, note} per page 1..%d" % pages)


def footer_ok(text, as_of):
    t = htmllib.unescape(text)
    foot = re.findall(r"As of\s+([^<\n]{1,80})", t)
    need(foot, "no 'As of' footer found in the export HTML")
    need(not any(f.strip().lower().startswith("not available") for f in foot), "an 'As of' footer still reads 'Not available': %r" % foot[0])
    d = datetime.strptime(as_of, "%Y-%m-%d")
    forms = {as_of, d.strftime("%B %d, %Y"), d.strftime("%B %-d, %Y") if sys.platform != "win32" else d.strftime("%B %#d, %Y"), d.strftime("%b %d, %Y"), d.strftime("%m/%d/%Y"), d.strftime("%-m/%-d/%Y") if sys.platform != "win32" else d.strftime("%#m/%#d/%Y")}
    need(any(any(f in x for f in forms) for x in foot), "no 'As of' footer carries the household's as_of date in an ISO or long date form: %r" % foot[:2])


def check_fix(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~152/RENDER_FIX.json")
    c = contract(root)
    ids = [m["id"] for m in c["members"]]
    need(r.get("sample_sha256") == OLD_SAMPLE_SHA and sha(SAMPLE) == OLD_SAMPLE_SHA, "the record must be bound to the unchanged real sample (sha256 %s...)" % OLD_SAMPLE_SHA[:12])
    outs = r.get("outputs") or {}
    paths = {k: private_file(root, outs.get(k), OUT_A, ext, k) for k, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"), ("fixture_html", ".html"))}
    tab = Path(paths["tab_html"]).read_text(encoding="utf-8")
    exp = Path(paths["export_html"]).read_text(encoding="utf-8")
    for name, text in (("tab_html", tab), ("export_html", exp)):
        got = set(re.findall(r'data-member="([^"]+)"', text))
        need(got == set(ids), "%s holds %d member ids, the contract has %d: missing %s" % (name, len(got), len(ids), sorted(set(ids) - got)[:3]))
        need("Not available yet" in text, "%s must still say 'Not available yet' for what is absent" % name)
    need(re.search(r"before advisory fees", exp, re.I) is not None and r.get("fee_basis_label_present") is True and r.get("no_zero_for_absent") is True, "the fee-basis label and the no-zero-for-absent rule must hold")
    # defect 1: an absent reason prints once per section at most
    sm = sample_json(SAMPLE)
    reasons = sorted({v["absent"] for v in sm["values"].values() if is_absent(v) and len(v["absent"]) >= 40})
    reasons = [x for x in reasons if not any(x != y and x in y for y in reasons)]  # a reason that is part of a longer one is counted inside it
    need(reasons, "the sample holds no long absent reason to count")
    worst = 0
    for name, text in (("tab_html", tab), ("export_html", exp)):
        t = htmllib.unescape(text)
        for reason in reasons:
            n = t.count(reason)
            worst = max(worst, n)
            need(n <= MAX_REASON_REPEATS, "%s prints one absent reason %d times (at most %d, once per section): the reason must print at its section or table head and each cell a short word" % (name, n, MAX_REASON_REPEATS))
    need(is_int(r.get("max_reason_repeats")), "max_reason_repeats must be stated (the checker counts its own: %d)" % worst)
    # defect 2: the footer
    footer_ok(exp, sm["household"]["as_of"])
    # defect 3: the charts
    chart_ids = [i for i in ids if ".chart." in i]
    ch = r.get("charts")
    need(isinstance(ch, list) and sorted(x.get("id") for x in ch if isinstance(x, dict)) == sorted(chart_ids), "charts must hold one entry for each of the %d chart members" % len(chart_ids))
    for x in ch:
        i = x["id"]
        at = exp.find('data-member="%s"' % i)
        nxt = exp.find('data-member="', at + 10)
        seg = exp[at: nxt if nxt > 0 else at + 4000]
        need(isinstance(x.get("drew"), bool) and isinstance(x.get("absent_words"), bool) and (x["drew"] or x["absent_words"]), "chart %s must have drawn or printed its absent words" % i)
        need(("<svg" in seg) == x["drew"] and (("Not available yet" in seg) == x["absent_words"] or x["drew"]), "chart %s: the record disagrees with the export HTML (svg %s, words %s)" % (i, "<svg" in seg, "Not available yet" in seg))
    fx = Path(paths["fixture_html"]).read_text(encoding="utf-8")
    need(fx.count("<svg") >= 1 and r.get("fixture_svg_count") == fx.count("<svg"), "the synthetic-fixture render must draw at least one chart (<svg), proving the draw path, and the record must state the count")
    # the PDF read page by page
    pages = pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    check_pdf_read(r, pages)
    # the portal change
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-152-portal" and HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-152-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(root / "portal"), "cat-file", "-t", pt["commit"]], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip() == "commit", "portal commit %s is not in the portal repository" % pt["commit"])
    need(isinstance(pt.get("files_changed"), list) and pt["files_changed"] and all(str(f).startswith("src/pages/InvestorReporting/") for f in pt["files_changed"]), "portal.files_changed must name the changed component files under src/pages/InvestorReporting/")
    hn = (root / D / "0.9.0_WK_IRPT_DASHBD~152" / "render_sample.ts")
    need(hn.is_file() and r.get("harness_sha256") == sha(hn), "the harness render_sample.ts must be in the worker's folder and hashed in harness_sha256")
    zero_effects(r)
    print("OK: re-rendered; no absent reason prints more than %d times (worst %d); the footer carries the as-of date; %d chart slots drew or said why, the fixture draws %d chart(s); %d PDF pages read, %d clipped"
          % (MAX_REASON_REPEATS, worst, len(chart_ids), fx.count("<svg"), pages, sum(1 for x in r["pdf_clipping"] if x["clipped"])))


def absent_ids(sample):
    return sorted(k for k, v in sample["values"].items() if is_absent(v))


def check_classify(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~153/ABSENT_CLASSIFICATION.json")
    c = contract(root)
    src = {m["id"]: m["source"] for m in c["members"]}
    sm = sample_json(SAMPLE)
    need(sha(SAMPLE) == OLD_SAMPLE_SHA and r.get("sample_sha256") == OLD_SAMPLE_SHA, "bound to the unchanged real sample")
    ab = absent_ids(sm)
    need(r.get("denominator") == len(ab), "denominator must equal the sample's absent members (%d), record says %r" % (len(ab), r.get("denominator")))
    ms = r.get("members")
    need(isinstance(ms, list) and sorted(m.get("id") for m in ms if isinstance(m, dict)) == ab, "members must hold exactly the %d absent member ids of the sample, once each" % len(ab))
    cnt = {"a": 0, "b": 0, "c": 0}
    for m in ms:
        i = m["id"]
        want = "contract_absent" if src[i] == "ABSENT" else "sourced_unfilled"
        need(m.get("state_now") == want, "member %s: state_now %r, the contract says %r" % (i, m.get("state_now"), want))
        k = m.get("class")
        need(k in cnt, "member %s: class must be a, b or c" % i)
        cnt[k] += 1
        e = m.get("evidence") or {}
        if k == "a":
            tc = str(e.get("table_contract") or "")
            need(tc.startswith("org/standards/") and tc.endswith("_CONTRACT.json") and (root / tc).is_file(), "member %s (a): table_contract must be an existing org/standards/*_CONTRACT.json" % i)
            col = str(e.get("column") or "")
            need(col and col in (root / tc).read_text(encoding="utf-8"), "member %s (a): column %r is not in %s" % (i, col, tc))
            need(nes(e.get("fold")), "member %s (a): fold must say in words how the column maps to the member" % i)
        elif k == "b":
            mr = str(e.get("method_ref") or "")
            need(mr and (root / mr).is_file() and nes(e.get("rule")), "member %s (b): method_ref must be an existing file and rule stated in words" % i)
        else:
            need(nes(e.get("holder")) and nes(e.get("reason")), "member %s (c): holder (the gold table that would hold it) and reason in words" % i)
    need(r.get("counts") == cnt and sum(cnt.values()) == len(ab), "counts %r must equal the tally %r and sum to %d" % (r.get("counts"), cnt, len(ab)))
    zero_effects(r)
    print("OK: %d absent members classified: %d (a) mappable now, %d (b) derivable, %d (c) truly absent" % (len(ab), cnt["a"], cnt["b"], cnt["c"]))


def check_fill(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~154/SAMPLE_FILL.json")
    cl = load(root, D + "0.9.0_WK_IRPT_DASHBD~153/ABSENT_CLASSIFICATION.json")
    a_ids = sorted(m["id"] for m in cl["members"] if m["class"] == "a")
    old = sample_json(SAMPLE)
    need(sha(SAMPLE) == OLD_SAMPLE_SHA and r.get("prior_sample_sha256") == OLD_SAMPLE_SHA, "the prior sample must be unchanged (sha256 %s...)" % OLD_SAMPLE_SHA[:12])
    need(Path(NEW_SAMPLE).is_file() and r.get("sample_sha256") == sha(NEW_SAMPLE), "the new sample must be at %s and the record bound to its bytes" % NEW_SAMPLE)
    root_abs = str(root.resolve()).replace("\\", "/").rstrip("/") + "/"
    need(not NEW_SAMPLE.startswith(root_abs), "the new sample is inside the repo")
    new = sample_json(NEW_SAMPLE)
    c = contract(root)
    p97(root).check_sample_shape(new, c)
    need(new["household"]["household_ref"] == old["household"]["household_ref"] and [a["account_id"] for a in new["household"]["accounts"]] == [a["account_id"] for a in old["household"]["accounts"]],
         "the household must be the same (household_ref and the account ids)")
    filled_now = sorted(k for k, v in new["values"].items() if not is_absent(v))
    filled_before = sorted(k for k, v in old["values"].items() if not is_absent(v))
    newly = sorted(set(filled_now) - set(filled_before))
    need(newly == a_ids, "the newly filled members must be exactly the (a) members of the classification: %d filled, %d expected (extra %s, missing %s)" % (len(newly), len(a_ids), sorted(set(newly) - set(a_ids))[:3], sorted(set(a_ids) - set(newly))[:3]))
    need(r.get("newly_filled_ids") == newly and r.get("filled_before") == len(filled_before) and r.get("filled_after") == len(filled_now) == len(filled_before) + len(a_ids), "newly_filled_ids, filled_before and filled_after must equal what the samples hold")
    need(all(new["values"][k] == old["values"][k] for k in filled_before), "a member filled before changed its value: a fill moves nothing else")
    ic = r.get("identity_checks") or {}
    need(is_int(ic.get("counted")) and ic["counted"] > 0 and ic.get("failed") == 0 and is_int(ic.get("passed")) and ic["passed"] + ic.get("not_gradeable", 0) <= ic["counted"] + ic.get("not_gradeable", 0) and r.get("window_residual_checks_failed") == 0,
         "identity_checks %r: counted above 0, failed 0; window_residual_checks_failed 0" % ic)
    bf = root / D / "0.9.0_WK_IRPT_DASHBD~154" / "build_sample.py"
    need(bf.is_file() and r.get("builder_sha256") == sha(bf) and "--firm" in bf.read_text(encoding="utf-8"), "the builder must be in the worker's folder, hashed, and take a --firm argument")
    need(r.get("firm_branches_outside_adapter") == 0, "firm_branches_outside_adapter must be 0 (a needed branch is a finding row, not a branch)")
    zero_effects(r)
    print("OK: %d (a) members filled (%d to %d of %d), the household and every earlier figure unchanged, identity checks %d counted none failing" % (len(a_ids), len(filled_before), len(filled_now), len(c["members"]), ic["counted"]))


def check_readiness(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~155/FIRM_READINESS.json")
    firms = {"cottonwood": "opal-data-cot", "inflection": "opal-data-inf"}
    fs = r.get("firms")
    need(isinstance(fs, list) and sorted(f.get("firm") for f in fs if isinstance(f, dict)) == sorted(firms), "firms must hold exactly cottonwood and inflection")
    for f in fs:
        n = f["firm"]
        need(f.get("bucket") == firms[n] and f.get("irpt_prefix_exists") is False, "%s: bucket %s and irpt_prefix_exists false (the issuer's own read: the prefix lists empty)" % (n, firms[n]))
        tb = f.get("tables")
        need(isinstance(tb, list) and sorted(t.get("table") for t in tb if isinstance(t, dict)) == sorted(TABLES), "%s: tables must hold exactly the eight C-SHAPE tables" % n)
        for t in tb:
            need(isinstance(t.get("source_exists"), bool) and nes(t.get("candidate_source")) and nes(t.get("gap_in_words")) and isinstance(t.get("reuses_existing_gold"), bool), "%s %s: source_exists, candidate_source, gap_in_words and reuses_existing_gold" % (n, t.get("table")))
        need(isinstance(f.get("existing_gold_inputs"), list) and f["existing_gold_inputs"] and all(isinstance(x, dict) and nes(x.get("what")) and nes(x.get("address")) and isinstance(x.get("columns_served"), int) for x in f["existing_gold_inputs"]), "%s: existing_gold_inputs must name the gold IRPT_BCKEND already builds (what, address, columns_served)" % n)
        need(f.get("readiness") in ("READY", "BLOCKED") and nes(f.get("blockers")) and nes(f.get("household_dimension")), "%s: readiness, blockers and household_dimension in words" % n)
        need(f.get("shadow_pull_proposed") is False, "%s: an adapter reuses the existing gold; shadow_pull_proposed must be false" % n)
    need(nes(r.get("recommendation")) and nes(r.get("adapter_order_proposal")), "recommendation and adapter_order_proposal must be stated")
    zero_effects(r)
    print("OK: both firms read against the eight tables: %s" % ", ".join("%s %s" % (f["firm"], f["readiness"]) for f in fs))


def check_section(root):
    r = load(root, D + "0.9.0_WK_IRPT_DASHBD~156/SECTION_CHECK.json")
    c = contract(root)
    m = re.fullmatch(r"0\.9\.0_WK_IRPT_DASHBD~(\d+)", str(r.get("checked_by") or ""))
    need(m and int(m.group(1)) not in BUILDERS, "checked_by must be a worker serial other than the builders %s" % sorted(BUILDERS))
    need(Path(NEW_SAMPLE).is_file() and r.get("sample_sha256") == sha(NEW_SAMPLE), "the check must be bound to the filled sample's bytes (round 101 DB-b-189)")
    new = sample_json(NEW_SAMPLE)
    outs = r.get("outputs") or {}
    paths = {k: private_file(root, outs.get(k), OUT_D, ext, k) for k, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
    pages = pdf_pages(paths["export_pdf"])
    check_pdf_read(r, pages)
    need(r.get("firms_checked") == ["49financial"] and r.get("firms_not_built") == ["cottonwood", "inflection"], "firms_checked ['49financial'] and firms_not_built ['cottonwood', 'inflection']")
    ss = r.get("sections")
    need(isinstance(ss, list) and [s.get("section") for s in ss] == list(SECTIONS), "sections must hold the eight baseline sections in order")
    for s in ss:
        mem = [x["id"] for x in c["members"] if x["section"] == s["section"]]
        filled = sum(1 for i in mem if not is_absent(new["values"][i]))
        need(s.get("members_total") == len(mem) and s.get("members_filled") == filled, "section %s: members_total and members_filled must be %d and %d" % (s["section"], len(mem), filled))
        want = "PRESENT" if filled == len(mem) else ("ABSENT" if filled == 0 else "PARTIAL")
        need(s.get("state") == want and nes(s.get("reason")) and nes(s.get("seen_in_render")), "section %s: state %r must be %s, with a reason and what was seen in the render" % (s["section"], s.get("state"), want))
    need(nes(r.get("baseline_schema_read")) and (root / str(r["baseline_schema_read"])).is_file(), "baseline_schema_read must be the path of the baseline schema this seat read")
    zero_effects(r)
    print("OK: %d sections tabulated against the baseline for the 49 Financial render (%s); %d PDF pages read" % (len(ss), ", ".join("%s %s" % (s["section"].split("_")[0], s["state"]) for s in ss), pages))


FNS = {"DB101-1-AC1": check_fix, "DB101-2-AC1": check_classify, "DB101-3-AC1": check_fill, "DB101-4-AC1": check_readiness, "DB101-5-AC1": check_section}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FNS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB101"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
