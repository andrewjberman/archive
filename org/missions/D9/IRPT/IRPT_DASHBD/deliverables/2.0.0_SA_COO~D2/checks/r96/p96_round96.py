"""IRPT_DASHBD round 96 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msgs 7258 and 7349.

  DB-b-180 (~146)  render the REAL 49 Financial sample (round 94, ~141) through the tab and export components into a local HTML and a local PDF in the PRIVATE folder
                   C:/dev/_irpt_private_evidence_20261009/fwd21_sample/ -- never in the repo.                                    DB96-1-AC1
  DB-b-181 (~147)  FDRXX -> CASH, cell A (LOCAL): money-market funds classify as cash in the gold ETF classifier, keyed on the canonical row's sub_asset_class,
                   with a COUNT of the canonical rows and of the served holdings that move; no deploy, no write.                  DB96-2-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
PRIV_OUT = os.environ.get("IRPT_P96_PRIV_OUT", "C:/dev/_irpt_private_evidence_20261009/fwd21_sample/")  # the env seam is for the dry-run only
SAMPLE = os.environ.get("IRPT_P96_SAMPLE", "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~141/HOUSEHOLD_SAMPLE.json")
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
CLASSIFIER = "data/black_diamond/scripts/gold/lib/etf_classifier.py"
RUN = re.compile(r"\d{8,}")
HEX64 = re.compile(r"[0-9a-f]{64}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("commit", "portal_commit", "path"):  # a private-folder path carries a date token (DB-b-180 row W146-S3)
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


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pinned_sha(root):
    """sha256 of the classifier at the round-96 pin (a later round may change the working file; the record binds the pin)."""
    r = subprocess.run(["git", "-C", str(root), "show", "e340e07f4e:" + CLASSIFIER], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 and r.stdout else ""


def check_render(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~146"
    r = load(root, folder + "/SAMPLE_RENDER.json")
    need(Path(SAMPLE).is_file(), "the private sample %s is missing" % SAMPLE)
    need(r.get("sample_sha256") == sha(SAMPLE), "the record is not bound to the private sample's bytes")
    c = json.loads((root / CONTRACT).read_bytes().decode("utf-8"))
    member_ids = [m["id"] for m in c["members"]]
    outs = r.get("outputs") or {}
    root_abs = str(root.resolve()).replace("\\", "/").rstrip("/") + "/"
    for key, ext in (("tab_html", ".html"), ("export_pdf", ".pdf"), ("export_html", ".html")):
        o = outs.get(key) or {}
        p = str(o.get("path") or "").replace("\\", "/")
        need(p.startswith(PRIV_OUT) and p.endswith(ext), "outputs.%s.path must be a %s file under %s" % (key, ext, PRIV_OUT))
        need(not p.startswith(root_abs), "outputs.%s is inside the repo: client data never goes there" % key)
        need(Path(p).is_file() and Path(p).stat().st_size > 5000, "outputs.%s does not exist or is too small" % key)
        need(o.get("sha256") == sha(p) and o.get("bytes") == Path(p).stat().st_size, "outputs.%s sha256 or bytes differ from the file" % key)
    tab = Path(outs["tab_html"]["path"]).read_text(encoding="utf-8")
    exp = Path(outs["export_html"]["path"]).read_text(encoding="utf-8")
    for name, text in (("tab_html", tab), ("export_html", exp)):
        ids = set(re.findall(r'data-member="([^"]+)"', text))
        need(ids == set(member_ids), "%s holds %d member ids, the contract has %d: missing %s" % (name, len(ids), len(member_ids), sorted(set(member_ids) - ids)[:3]))
        need(len(re.findall("Not available yet", text)) >= 40, "%s must print 'Not available yet' words for its absent figures" % name)
        need(re.search(r"before advisory fees", text, re.I) is not None, "%s must carry the fee-basis label" % name)
    pdf = Path(outs["export_pdf"]["path"]).read_bytes()
    need(pdf[:5] == b"%PDF-", "export_pdf is not a PDF")
    pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf))
    need(pages >= 8 and r.get("export_pdf_pages") == pages, "export_pdf pages %d (record %r): at least 8 sections' worth are required and the record must state the count" % (pages, r.get("export_pdf_pages")))
    sm = json.loads(Path(SAMPLE).read_text(encoding="utf-8"))
    n_abs = sum(1 for v in (sm.get("values") or {}).values() if isinstance(v, dict) and "absent" in v)
    need(r.get("absent_members_in_sample") == n_abs and n_abs > 0, "absent_members_in_sample %r must equal the sample's %d" % (r.get("absent_members_in_sample"), n_abs))
    for k in ("no_zero_for_absent", "fee_basis_label_present", "synthetic_data_used"):
        need(isinstance(r.get(k), bool), "%s must be a bool" % k)
    need(r["no_zero_for_absent"] is True and r["fee_basis_label_present"] is True and r["synthetic_data_used"] is False, "no_zero_for_absent and fee_basis_label_present true, synthetic_data_used false")
    code = r.get("code") or {}
    f = str(code.get("file") or "")
    need(f.startswith(PROJ) and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")) and (root / f).is_file() and sha(root / f) == code["sha256"], "code %r" % code)
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("secret_reads") == 0 and r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False, "reads/pushed/files_in_repo %r" % rd)
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: the real sample rendered to a %d-page PDF and two HTML files in the private folder (%d member ids, %d absent figures said in words); record holds paths and hashes only"
          % (pages, len(member_ids), n_abs))


def check_fdrxx(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~147"
    r = load(root, folder + "/FDRXX_CASH_CHANGE.json")
    ru = r.get("rule") or {}
    need(ru.get("keyed_on") == "sub_asset_class" and str(ru.get("cash_asset_class_value") or "").strip() != "" and ru.get("ticker_list_used") is False, "rule %r: keyed on the row's sub_asset_class, a stated cash class value, no ticker list" % ru)
    voc = r.get("vocabulary") or {}
    need(isinstance(voc.get("asset_class_values_in_table"), dict) and voc["asset_class_values_in_table"] and ru["cash_asset_class_value"] in voc["asset_class_values_in_table"], "the cash class value %r must be one the canonical table already uses (vocabulary %r)" % (ru["cash_asset_class_value"], list((voc.get("asset_class_values_in_table") or {}).keys())[:6]))
    cnt = r.get("canonical_rows") or {}
    need(is_int(cnt.get("total")) and cnt["total"] > 10000 and is_int(cnt.get("sub_asset_class_cash")) and is_int(cnt.get("cash_rows_already_cash_class")) and is_int(cnt.get("would_move")),
         "canonical_rows %r needs total, sub_asset_class_cash, cash_rows_already_cash_class, would_move" % cnt)
    need(cnt["would_move"] == cnt["sub_asset_class_cash"] - cnt["cash_rows_already_cash_class"] and cnt["would_move"] >= 1, "would_move must equal the Cash-typed rows not already in the cash class, and FDRXX makes it at least 1")
    need(r.get("fdrxx_in_would_move") is True, "fdrxx_in_would_move must be true")
    ho = r.get("served_holdings") or {}
    need(isinstance(ho.get("stores_read"), list) and ho["stores_read"] and is_int(ho.get("positions_scanned")) and ho["positions_scanned"] > 0 and is_int(ho.get("positions_that_move")) and ho["positions_that_move"] <= ho["positions_scanned"]
         and is_int(ho.get("accounts_with_a_moving_position")) and isinstance(ho.get("per_firm"), dict) and ho["per_firm"] and sum(ho["per_firm"].values()) == ho["positions_that_move"],
         "served_holdings %r needs stores_read, positions_scanned, positions_that_move, per_firm summing to it, and accounts_with_a_moving_position" % ho)
    cons = r.get("consumers")
    need(isinstance(cons, list) and cons and all(isinstance(x, str) and x.strip() for x in cons), "consumers must name the readers of the classifier's class (at least one)")
    code = r.get("code") or {}
    f = str(code.get("file") or "")
    need(f == CLASSIFIER and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")) and (root / f).is_file() and code["sha256"] in (sha(root / f), pinned_sha(root)), "code %r must be the classifier, tracked, with its committed sha256 (the working file or the round-96 pin e340e07f4e)" % code)
    need("sub_asset_class" in (root / CLASSIFIER).read_text(encoding="utf-8") and "cash" in (root / CLASSIFIER).read_text(encoding="utf-8").lower(), "the classifier does not carry the rule")
    t = r.get("test") or {}
    need(str(t.get("file") or "").strip() and t.get("mutant_failed") is True and is_int(t.get("passed")) and t["passed"] >= 3 and t.get("failed") == 0, "test %r: a file, a mutant that failed, 3 or more passing, none failing" % t)
    need(r.get("unchanged_rows_still_verbatim") is True and r.get("cash_usd_special_case") in ("unchanged", "changed_with_reason"), "unchanged_rows_still_verbatim true and cash_usd_special_case stated")
    rd = r.get("reads") or {}
    need(rd.get("dynamodb_writes") == 0 and rd.get("s3_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0 and r.get("deployed") is False and r.get("pushed") is False and r.get("served_values_changed") is False,
         "reads/deployed/pushed/served_values_changed %r" % rd)
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: FDRXX rule keyed on sub_asset_class: %d canonical rows move (of %d), %d served positions in %d accounts move; test with a mutant" % (cnt["would_move"], cnt["total"], ho["positions_that_move"], ho["accounts_with_a_moving_position"]))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    fns = {"DB96-1-AC1": check_render, "DB96-2-AC1": check_fdrxx}
    try:
        need(cid in fns, "unknown criterion %r" % cid)
        fns[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB96"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
