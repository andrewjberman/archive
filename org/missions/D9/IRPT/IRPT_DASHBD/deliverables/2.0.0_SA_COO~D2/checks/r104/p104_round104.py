"""IRPT_DASHBD round 104 (issuer 2.0.0_SA_COO~D2) -- the issuance for 1.0.0_SA_CTO~DELL2's ROUND-104 ANALYSIS (@267f2b547a; the CVO graded DB103-1-J1 FAIL on its wording clause).

  DB-b-197 (~162)  the render cell, J1's remedy: an unheld class prints the baseline's dash, every kind note names its figure, a chart title says what it draws, the before-fee line
                   only when its member is present; 49F re-rendered, every PDF page read as an image.                                                             DB104-1-AC1
  DB-b-198 (~163)  contract 0.4.1 (the percent-points unit sentence and a unit_scale field on every percent member) and the absent_kind PROPOSAL (vocabulary, four-postulate
                   record, word-boundary token census); no code reads absent_kind.                                                                                 DB104-2-AC1
  DB-b-199 (~164)  the model daily series into the report's gold: contract, producer, tests and the never-widen PACKET (keys written, rollback, no other key moves); writes nothing. DB104-3-AC1
  DB-b-200 (~165)  Cottonwood account_dim into its address() gold: the never-widen PACKET (the exact keys, the rollback, no other key moves); writes nothing.      DB104-4-AC1
  DB-b-201 (~166)  who rewrote Cottonwood's manifests on 2026-10-11 (read) and the return-gold RESUME PACKET onto a schedule; writes nothing.                       DB104-5-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P3 = load_mod("p103", "r103/p103_round103.py")
P = P3.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D = P.D
PRIV = P.PRIV
SAMPLE159 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~159/HOUSEHOLD_SAMPLE.json"
SAMPLE159_SHA = "25446cfc9b987a97aa54cb91ecfb5212983ace90fbb823173cde6a3eadea1301"
OUT_R = PRIV + "fwd21_sample_r104/"
V040_SHA = "45c6c2005663ae5cf356ae890133f90cc1579093be0b0fb27e85c0f3d9710523"
CONTRACT_REL = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
DASH = "–"
BARE = ("This figure needs more history than is available yet.", "This figure is not available yet.", "This figure does not apply.")
PACKET_HEADS = (r"1\.\s+The act", r"2\.\s+What moves", r"3\.\s+When and where", r"4b\.\s+Writers", r"5\.\s+Both branches", r"6\.\s+Rollback", r"7\.\s+Conditions", r"8\.\s+Not established")
KINDS = ("NOT_HELD", "NOT_APPLICABLE", "NO_SOURCE_YET", "INSUFFICIENT_HISTORY")
Fail = P.Fail


def packet_doc(root, rel, rec_sha):
    p = root / str(rel or "")
    need(nes(rel) and p.is_file() and p.suffix == ".md", "the packet file %r must exist (a .md)" % rel)
    need(rec_sha == sha(p), "packet_sha256 must equal the packet file's bytes")
    t = p.read_text(encoding="utf-8")
    for h in PACKET_HEADS:
        need(re.search(r"(?m)^##\s+" + h, t), "the packet lacks the section '## %s'" % h.replace("\\.", "."))
    need("never-widen" in t.lower() or "never widen" in t.lower(), "the packet must say it is a never-widen packet")
    return t


def check_render(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~162/RENDER_FIX_R104.json")
    c = P.contract(root)
    ids = [m["id"] for m in c["members"]]
    unit = {m["id"]: m["unit"] for m in c["members"]}
    need(r.get("sample_sha256") == SAMPLE159_SHA and P.sha(SAMPLE159) == SAMPLE159_SHA, "the record must be bound to the round-103 benchmark sample (sha256 %s...)" % SAMPLE159_SHA[:12])
    sm = P.sample_json(SAMPLE159)
    outs = r.get("outputs") or {}
    paths = {k: P.private_file(root, outs.get(k), OUT_R, ext, k) for k, ext in (("tab_html", ".html"), ("export_html", ".html"), ("export_pdf", ".pdf"))}
    tab = Path(paths["tab_html"]).read_text(encoding="utf-8")
    exp = Path(paths["export_html"]).read_text(encoding="utf-8")
    texts = (("tab_html", tab), ("export_html", exp))
    for name, text in texts:
        need(set(re.findall(r'data-member="([^"]+)"', text)) == set(ids), "%s must hold all %d member ids" % (name, len(ids)))
    # percents at their stored scale (the round-103 rule stands)
    want, scaled = set(), set()
    for k, v in sm["values"].items():
        if unit[k] != "percent":
            continue
        vals = [v] if isinstance(v, (int, float)) and not isinstance(v, bool) else ([x for x in v["by_row"].values() if isinstance(x, (int, float)) and not isinstance(x, bool)] if isinstance(v, dict) and "by_row" in v else [])
        for x in vals:
            want.add("%.1f%%" % x)
            scaled.add("%.1f%%" % (x * 100))
    scaled -= want
    for name, text in texts:
        vt = P3.visible_text(text)
        need(all(x in vt for x in want) and not any(x in vt for x in scaled), "%s: a stored percent prints off its stored scale" % name)
        for rx in P3.BANNED:
            m = rx.search(vt)
            need(not m, "%s carries build language: %r" % (name, m.group(0) if m else ""))
        need("Sample Firm" not in vt and P3.FIRM_TITLE in vt, "%s must print the registry's firm title" % name)
        # 1. an unheld class prints the baseline's dash, never 'Not available yet'
        need("no holding" not in vt.lower(), "%s prints the unheld-class reason text" % name)
        # 2. a kind note names its figure: the bare sentences of round 103 are gone
        for b in BARE:
            need(b not in vt, "%s still prints a kind note with no referent: %r" % (name, b))
    unheld = sum(1 for v in sm["values"].values() if isinstance(v, dict) and "by_row" in v for x in v["by_row"].values() if P.is_absent(x) and x["absent"].startswith("no holding in this asset class"))
    need(unheld >= 1, "the sample holds no unheld-class entry to check")
    for name, text in texts:
        need(P3.visible_text(text).count(DASH) >= unheld, "%s must print the baseline's dash (an en dash) in at least %d unheld-class cells" % (name, unheld))
    need(r.get("unheld_cells") == unheld and nes(r.get("dash_source_form")) and all(ord(ch) < 128 for ch in r["dash_source_form"]), "unheld_cells must equal %d and dash_source_form must name the ASCII-safe source form (an entity or escape) the components use" % unheld)
    kn = r.get("kind_notes")
    need(isinstance(kn, list) and kn and all(isinstance(x, dict) and nes(x.get("kind")) and nes(x.get("example")) and x.get("names_figure") is True for x in kn), "kind_notes must list {kind, example, names_figure true}")
    vt = P3.visible_text(exp)
    need(all(x["example"] in vt for x in kn), "every kind note's example sentence must appear in the export text")
    # 3. a chart title says what the chart draws
    chart = "overview.chart.portfolio_performance_last_12_months"
    names = [str(s.get("name", "")) for s in (sm["values"][chart] if isinstance(sm["values"][chart], list) else []) if isinstance(s, dict)]
    at = exp.find('data-member="%s"' % chart)
    nxt = exp.find('data-member="', at + 10)
    seg = P3.visible_text(exp[at: nxt if nxt > 0 else at + 4000])
    if not any("household" in n.lower() for n in names):
        need("household" not in seg.lower(), "the 12-month chart is titled for a household line the sample does not carry (its series are %s)" % names)
    ct = r.get("chart_titles") or {}
    need(nes(ct.get(chart)) and ct[chart] in vt and (("household" in ct[chart].lower()) == any("household" in n.lower() for n in names)), "chart_titles[%s] must be the printed title, naming a household line only if one is drawn" % chart)
    # 4. the before-fee line prints only when its member is present
    fee = "convention.fee_basis_label"
    fee_absent = P.member_absent(sm["values"][fee])
    need(not fee_absent or "before advisory fees" not in vt.lower(), "the before-fee line prints while its member is absent")
    need(r.get("fee_line_follows_member") is True, "fee_line_follows_member must be true")
    P3.P.footer_ok(exp, sm["household"]["as_of"])
    pages = P.pdf_pages(paths["export_pdf"])
    need(pages >= 8, "the PDF holds %d pages" % pages)
    P.check_pdf_read(r, pages)
    need(sum(1 for x in r["pdf_clipping"] if x["clipped"]) == 0, "a page is recorded clipped: fix it and re-render")
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-162-portal" and P.HEXC.fullmatch(str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-162-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(root / "portal"), "cat-file", "-t", pt["commit"]], capture_output=True, text=True)
    need(g.returncode == 0 and g.stdout.strip() == "commit" and isinstance(pt.get("files_changed"), list) and pt["files_changed"] and all(str(f).startswith("src/pages/InvestorReporting/") for f in pt["files_changed"]), "portal commit and files under src/pages/InvestorReporting/")
    t = r.get("tests") or {}
    need(nes(t.get("new_file")) and t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and (t.get("suite_after") or {}).get("new_failing_ids") == [], "tests: a new file, a failing mutant, lint 0, typecheck 0, no new failing test")
    P.zero_effects(r)
    print("OK: %d unheld cells print the dash, no bare kind note, the chart title says what it draws, the before-fee line follows its member, %d PDF pages read, none clipped" % (unheld, pages))


def check_contract(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~163/CONTRACT_041_AND_PROPOSAL.json")
    c = P.contract(root)
    need(c["contract_version"] == "0.4.1" and any(x.get("sha256") == V040_SHA for x in c.get("lineage") or []), "the contract must be 0.4.1 with the 0.4.0 bytes (sha256 %s...) in its lineage" % V040_SHA[:12])
    need(all(m.get("unit_scale") == "percent_points" for m in c["members"] if m["unit"] == "percent") and not any("unit_scale" in m for m in c["members"] if m["unit"] != "percent"), "every percent member carries unit_scale percent_points and no other member does")
    sent = json.dumps(c["document"]).lower()
    need("percent points" in sent and "1.5" in sent, "document.shape must say percent values are percent points (a stored 1.5 means 1.5 percent)")
    h = subprocess.run(["git", "-C", str(root), "log", "--format=%H", "-n", "60", "--", CONTRACT_REL], capture_output=True, text=True)
    prior = None
    for cm in h.stdout.split():
        b0 = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (cm, CONTRACT_REL)], capture_output=True)
        if b0.returncode == 0 and P3.hashlib_sha(b0.stdout) == V040_SHA:
            prior = json.loads(b0.stdout.decode("utf-8"))
            break
    need(prior is not None, "the 0.4.0 contract bytes were not found in the file's git history")
    pm = {m["id"]: m for m in prior["members"]}
    need(sorted(pm) == sorted(m["id"] for m in c["members"]), "the member set changed")
    for m in c["members"]:
        a = dict(m)
        a.pop("unit_scale", None)
        need(a == pm[m["id"]], "member %s changed beyond unit_scale" % m["id"])
    # the proposal
    pf = str(r.get("proposal_file") or "")
    pp = root / pf
    need(pf.endswith(".md") and pp.is_file() and r.get("proposal_sha256") == sha(pp), "proposal_file must be an existing .md hashed in proposal_sha256")
    t = pp.read_text(encoding="utf-8")
    for h2 in ("Vocabulary", "Four-postulate record", "Token census"):
        need(re.search(r"(?m)^##\s+" + h2, t), "the proposal lacks the section '## %s'" % h2)
    for p4 in ("MECE", "SAME GRAIN", "INTENT COHERENCE", "STATE COHERENCE"):
        need(p4 in t, "the four-postulate record lacks %s" % p4)
    for k in KINDS:
        need(k in t, "the proposal must carry the vocabulary member %s" % k)
    cs = r.get("census")
    need(isinstance(cs, dict) and cs.get("method") and is_int(cs.get("files_scanned")) and cs["files_scanned"] > 0 and isinstance(cs.get("tokens"), dict) and sorted(cs["tokens"]) == sorted(KINDS) and all(is_int(v) for v in cs["tokens"].values()),
         "census needs method, files_scanned and a count for each of the four tokens (word-boundary)")
    d = r.get("domain") or {}
    need(is_int(d.get("absent_members_at_member_grain")) and d["absent_members_at_member_grain"] == len(P.absent_ids(P.sample_json(SAMPLE159))) and is_int(d.get("by_row_absent_entries")), "domain.absent_members_at_member_grain must equal the sample's absent member count (the denominator the subtraction runs over)")
    need(r.get("code_reads_absent_kind") is False, "no code may read absent_kind before the proposal is accepted")
    P.zero_effects(r)
    print("OK: contract 0.4.1 (%d percent members carry unit_scale), the absent_kind proposal carries its four-postulate record and a census of %d files" % (sum(1 for m in c["members"] if m["unit"] == "percent"), cs["files_scanned"]))


def check_series_gold(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~164/MODEL_SERIES_GOLD_PACKET.json")
    cf = nes(r.get("contract_file")) and r["contract_file"].startswith("org/standards/IRPT_DASHBD_") and r["contract_file"].endswith("_CONTRACT.json")
    need(cf and (root / r["contract_file"]).is_file(), "contract_file must be an existing org/standards/IRPT_DASHBD_*_CONTRACT.json")
    c = json.loads((root / r["contract_file"]).read_bytes().decode("utf-8"))
    need(P.HEX64.fullmatch(str(c.get("schema_hash") or "")) and nes(c.get("schema_hash_basis")) and c.get("table") == r.get("table") and nes(r.get("table")), "the contract needs table, schema_hash and schema_hash_basis and the record the same table")
    ad = r.get("producer") or {}
    f = str(ad.get("file") or "")
    need(f.startswith("data/assets/scripts/gold/irpt_reporting/") and f.endswith(".py") and (root / f).is_file() and ad.get("sha256") == sha(root / f) and ad.get("tracked") is True, "producer: a tracked .py under data/assets/scripts/gold/irpt_reporting/ hashed as recorded")
    code = ("import hashlib, importlib.util\nspec = importlib.util.spec_from_file_location('m', %r)\nm = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
            "print(hashlib.sha256('\\n'.join(sorted('%%s:%%s' %% (x.name, x.type) for x in m.ARROW_SCHEMA)).encode()).hexdigest())\n") % str((root / f).resolve())
    o = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, cwd=str(root))
    need(o.returncode == 0 and o.stdout.strip() == c["schema_hash"], "the schema hash recomputed from the producer's ARROW_SCHEMA must equal the contract's")
    t = r.get("tests") or {}
    need(nes(t.get("file")) and (root / t["file"]).is_file() and is_int(t.get("passed")) and t["passed"] >= 3 and t.get("failed") == 0 and t.get("mutant_failed") is True, "tests: a file, 3 or more passing, none failing, a failing mutant")
    q = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", str((root / t["file"]).resolve())], capture_output=True, text=True, cwd=str(root))
    need(q.returncode == 0, "the test file does not pass when the checker runs it")
    aa = r.get("address_args")
    need(isinstance(aa, list) and len(aa) == 5 and all(nes(x) for x in aa), "address_args must be the five address() arguments")
    sys.path.insert(0, str(root / "lib"))
    import opal_naming
    target = opal_naming.address(*aa)
    kw = r.get("keys_written")
    need(isinstance(kw, list) and kw and all(isinstance(x, dict) and nes(x.get("bucket")) and nes(x.get("prefix")) and is_int(x.get("objects_per_partition")) for x in kw), "keys_written: {bucket, prefix, objects_per_partition}")
    need(all(("s3://%s/%s" % (x["bucket"], x["prefix"])).rstrip("/").startswith(target.rsplit("/date=", 1)[0].rstrip("/")) for x in kw), "every key written must be under the address() home %s" % target)
    need(nes(r.get("rollback")) and r.get("no_other_key_moves") is True and r.get("writes_in_this_cell") is False and nes(r.get("source_claim")) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(r.get("data_as_of") or "")), "rollback, no_other_key_moves true, writes_in_this_cell false, source_claim and data_as_of (ISO)")
    packet_doc(root, r.get("packet_file"), r.get("packet_sha256"))
    P.zero_effects(r)
    print("OK: %s gold home %s: contract hash recomputed equal, %d tests pass, packet with %d key pattern(s), nothing written" % (r["table"], target.rsplit("/date=", 1)[0], t["passed"], len(kw)))


def check_dim_packet(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~165/ACCOUNT_DIM_GOLD_PACKET.json")
    sys.path.insert(0, str(root / "lib"))
    import opal_naming
    target = opal_naming.address("irpt", "cottonwood", "gold", "account_dim", "date=2026-10-12")
    need(r.get("address_args") == ["irpt", "cottonwood", "gold", "account_dim", "date=2026-10-12"], "address_args must be the five address() arguments of the account_dim partition")
    kw = r.get("keys_written")
    need(isinstance(kw, list) and kw and all(isinstance(x, dict) and x.get("bucket") == "opal-data-cottonwood" and str(x.get("prefix") or "").startswith("irpt/cottonwood/gold/account_dim/") and is_int(x.get("objects_per_partition")) for x in kw), "keys_written must be {bucket opal-data-cottonwood, prefix under irpt/cottonwood/gold/account_dim/, objects_per_partition}")
    need(target.startswith("s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/"), "the address() target is the Cottonwood gold home")
    need(nes(r.get("rollback")) and r.get("no_other_key_moves") is True and r.get("writes_in_this_cell") is False, "rollback in words, no_other_key_moves true, writes_in_this_cell false")
    cn = r.get("counts") or {}
    need(is_int(cn.get("accounts")) and cn["accounts"] > 0 and is_int(cn.get("relationship_ids")) and cn["relationship_ids"] > 0 and is_int(cn.get("partitions_written_by_the_apply")) and cn["partitions_written_by_the_apply"] >= 1, "counts: accounts, relationship_ids and partitions_written_by_the_apply (a first apply is ONE partition)")
    need(nes(r.get("adapter_file")) and (root / r["adapter_file"]).is_file() and r.get("adapter_sha256") == sha(root / r["adapter_file"]) and nes(r.get("applier")) and nes(r.get("run_command_shape")), "adapter_file hashed as recorded, the applier named, and the run command's shape (the exact invocation, no live run)")
    need(isinstance(r.get("writers_of_the_property"), list) and r["writers_of_the_property"] and nes(r.get("both_branches")), "writers_of_the_property counted (a list) and both_branches stated")
    packet_doc(root, r.get("packet_file"), r.get("packet_sha256"))
    P.zero_effects(r)
    print("OK: account_dim packet for %s: %d key pattern(s), %d accounts, rollback stated, nothing written" % (target.rsplit("/date=", 1)[0], len(kw), cn["accounts"]))


def check_resume(root):
    r = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~166/COTTONWOOD_RESUME_PACKET.json")
    mw = r.get("manifest_rewrite_2026_10_11") or {}
    need(isinstance(mw.get("established"), bool) and nes(mw.get("evidence")) and is_int(mw.get("versions_read")) and (mw["established"] is False or nes(mw.get("writer"))) and (mw["established"] is True or mw.get("writer") == "NOT_ESTABLISHED"),
         "manifest_rewrite_2026_10_11 %r: established, evidence in words, versions_read, and the writer (or NOT_ESTABLISHED)" % mw)
    rp = r.get("resume_packet") or {}
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc
    need(rp.get("backfill_from") == "2026-06-23" and re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(rp.get("backfill_to") or "")) and rp["backfill_to"] >= "2026-10-12", "backfill_from must be 2026-06-23 and backfill_to an ISO date on or after 2026-10-12")
    n = len(tc.trading_days_between(rp["backfill_from"], rp["backfill_to"]))
    need(rp.get("trading_days_count") == n, "trading_days_count must equal %d (lib/trading_calendar.py, inclusive)" % n)
    need(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(rp.get("input_available_through") or "")) and isinstance(rp.get("input_covers_backfill"), bool) and rp["input_covers_backfill"] == (rp["input_available_through"] >= rp["backfill_to"]), "input_available_through (ISO) and input_covers_backfill must agree with backfill_to")
    if not rp["input_covers_backfill"]:
        need(nes(rp.get("gap_in_words")) and nes(rp.get("resume_blocked_on")), "when the input does not cover the backfill the packet names the gap and what the resume is blocked on")
    sc = rp.get("schedule") or {}
    need(sc.get("kind") == "EVENTBRIDGE" and nes(sc.get("rule_name")) and nes(sc.get("owner")) and nes(sc.get("cron")) and nes(sc.get("name_source")), "schedule: kind EVENTBRIDGE, the rule name (from name(), say how in name_source), its owner serial and cron")
    kw = rp.get("keys_written")
    need(isinstance(kw, list) and kw and all(isinstance(x, dict) and x.get("bucket") == "opal-data-cottonwood" and str(x.get("prefix") or "").startswith("irpt/cottonwood/gold/account_return_daily/") and is_int(x.get("objects_per_partition")) for x in kw), "keys_written under irpt/cottonwood/gold/account_return_daily/ in opal-data-cottonwood")
    need(nes(rp.get("rollback")) and rp.get("no_other_key_moves") is True and r.get("writes_in_this_cell") is False, "rollback, no_other_key_moves true, writes_in_this_cell false")
    packet_doc(root, r.get("packet_file"), r.get("packet_sha256"))
    P.zero_effects(r)
    print("OK: manifest rewrite writer %s; resume packet %s to %s (%d trading days), input covers it: %s, schedule %s" % (mw.get("writer", "")[:40] or "NOT_ESTABLISHED", rp["backfill_from"], rp["backfill_to"], n, str(rp["input_covers_backfill"]).lower(), sc["rule_name"]))


FNS = {"DB104-1-AC1": check_render, "DB104-2-AC1": check_contract, "DB104-3-AC1": check_series_gold, "DB104-4-AC1": check_dim_packet, "DB104-5-AC1": check_resume}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid in FNS, "unknown criterion %r" % cid)
        FNS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB104"))
        sys.exit(1)
    except (KeyError, TypeError, ValueError, AttributeError, IndexError, ImportError) as e:
        print("FAIL: malformed record: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
