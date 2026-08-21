#!/usr/bin/env python3
"""COT_SUPERVISED G4 -- amend the persisted daily holdings template (BD 226355).

CTO pin 63339 (B): the daily holdings DataMining template gains
{Holding Supervised, Account Supervised}. Portfolio Group EXCLUDED (63344,
fan-out measured twice).

THE UPDATE MECHANISM, EXERCISED 2026-08-20 (the doc's form is FALSE):
  POST /v1/template/ with a real templateId  -> MINTS A NEW TEMPLATE (270653,
      a same-named clone; deleted same window via DELETE /v1/template/{id}).
      endpoints/README.md:59 ("a real int reuses/updates") is a doc defect,
      routed to its owners -- do not trust it.
  PUT  /v1/template/{id}                     -> HTTP 405.
  PUT  /v1/template/  (id in the BODY)       -> 200, updates IN PLACE (response
      carries no templateId; the only sound verify is a fresh GET diff).

226355 is the Andrew-built 'Assets_Dim' qt1 snapshot template -- the amendment
flips EXACTLY two isSelected bits and touches nothing else. The pre-amendment
enriched body is saved beside this script BEFORE any POST (same-window rollback:
re-POST the saved body). Verification is a fresh GET re-read diffed against the
pre-image (only the two flips), then an ad-hoc QA export read (run-and-read,
NOTHING landed -- tonight's scheduled run is the real acceptance, per the
ad-hoc-runs law).

Usage:
  python g4_amend_holdings_template.py --inspect   # read-only: catalog + current selection
  python g4_amend_holdings_template.py --execute   # save pre-image, amend, verify by re-read
  python g4_amend_holdings_template.py --qa-run    # ad-hoc export read of the amended template
  python g4_amend_holdings_template.py --rollback  # re-POST the saved pre-image
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

WS_ROOT = Path(__file__).resolve().parents[5]  # device-agnostic: derived, never baked
BRONZE_DIR = WS_ROOT / "data" / "cot" / "scripts" / "bronze"
sys.path.insert(0, str(BRONZE_DIR))

import cot_bronze_ingest as cbi  # noqa: E402  (proven flow; DS-owned, imported not edited)

TEMPLATE_ID = 226355
ADD_DIMS = ("Holding Supervised", "Account Supervised")
PRE_IMAGE = Path(__file__).with_name("g4_226355_pre_amendment.json")
POST_IMAGE = Path(__file__).with_name("g4_226355_post_amendment.json")

# The create/update body's exact field set (endpoints/README.md POST v1/template/):
POST_FIELDS = (
    "endDate", "startDate", "name", "templateId", "comment", "dateRangeType",
    "queryTypeId", "levels", "facts", "parentDimensionLevels", "childDimensionLevels",
    "parentQueryAllocationLevelId", "childQueryAllocationLevelId",
    "allocationMarketValueFactId", "allocationCashInclusionId", "sharingStatus",
    "includeAll", "category",
)
NULLABLE = ("category", "parentQueryAllocationLevelId", "allocationCashInclusionId",
            "childQueryAllocationLevelId", "allocationMarketValueFactId")


def fetch_enriched(token: str) -> dict:
    out = cbi._request("GET", "/datamining/request/v1/template/%s" % TEMPLATE_ID, token=token)
    return out.get("template", out)


def selection(body: dict) -> list:
    return sorted((lv.get("queryLevelId"), d["name"])
                  for lv in body.get("levels", [])
                  for d in lv.get("dimensions", []) if d.get("isSelected"))


def find_targets(body: dict) -> dict:
    hits: dict = {}
    for lv in body.get("levels", []):
        for d in lv.get("dimensions", []):
            if d["name"] in ADD_DIMS:
                hits.setdefault(d["name"], []).append(
                    (lv.get("queryLevelId"), lv.get("name"), d.get("isSelected")))
    return hits


def build_post_body(body: dict) -> dict:
    post = {k: body.get(k) for k in POST_FIELDS if k in body or k in NULLABLE}
    for k in NULLABLE:
        post.setdefault(k, None)
    post["templateId"] = TEMPLATE_ID  # real int == in-place update (endpoints/README.md:59)
    # BD echoes ISO datetimes; re-stamp MM/DD/YYYY (the run-body lesson applied to the update body).
    for k in ("startDate", "endDate"):
        v = str(post.get(k) or "")
        if "T" in v:
            post[k] = cbi._mmddyyyy(v.split("T")[0])
    return post


def main() -> int:
    ap = argparse.ArgumentParser(description="COT_SUPERVISED G4 template amendment (226355)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--inspect", action="store_true")
    g.add_argument("--execute", action="store_true")
    g.add_argument("--qa-run", action="store_true")
    g.add_argument("--rollback", action="store_true")
    args = ap.parse_args()

    cookie = cbi.load_bd_session()
    token = cbi.get_datamining_token(cookie)
    print("auth OK (firm=%s)" % cbi.BD_FIRM_ID, flush=True)

    if args.qa_run:
        asof = "2026-08-19"
        start, end = cbi._window_for_asof("holdings", asof)
        tpl = cbi.load_template("holdings", start, end)  # the REAL production envelope from S3
        run_id, guid = cbi.run_query(token, tpl)
        print("QA run=%s guid=%s -- polling" % (run_id, guid), flush=True)
        cbi.poll_status(token, run_id)
        xlsx = cbi.download_export(cookie, guid)
        import warnings
        warnings.filterwarnings("ignore")
        from io import BytesIO
        import openpyxl
        wb = openpyxl.load_workbook(BytesIO(xlsx), read_only=True, data_only=True)
        rows = wb.active.iter_rows(values_only=True)
        header = [str(c) if c is not None else "" for c in next(rows)]
        n = sum(1 for _ in rows)
        wb.close()
        print("QA EXPORT (%d bytes, NOT landed): %d cols, %d data rows" % (len(xlsx), len(header), n), flush=True)
        print("HEADER: %s" % json.dumps(header), flush=True)
        missing = [c for c in ADD_DIMS if c not in header]
        print("VERDICT: %s" % ("PASS -- both new columns present"
                               if not missing else "FAIL -- absent: %s" % missing), flush=True)
        return 0 if not missing else 1

    body = fetch_enriched(token)
    sel = selection(body)
    hits = find_targets(body)
    print("current selection (%d dims): %s" % (len(sel), json.dumps(sel)), flush=True)
    print("target dims in qt1 catalog: %s" % json.dumps(hits), flush=True)

    if args.inspect:
        return 0

    if args.rollback:
        if not PRE_IMAGE.exists():
            raise SystemExit("ABORT: no pre-image saved; nothing to roll back to")
        pre = json.loads(PRE_IMAGE.read_text())
        cbi._request("PUT", "/datamining/request/v1/template/", token=token,
                     body=build_post_body(pre))
        print("ROLLBACK PUT issued (in-place; PUT returns no id -- verifying by GET)", flush=True)
        after = fetch_enriched(token)
        print("post-rollback selection == pre-image selection: %s"
              % (selection(after) == selection(pre)), flush=True)
        return 0

    # --execute. The enriched body carries ONLY the selected dims per level (measured:
    # 15 dims, no catalog), so adding a column is an INSERT of the catalog's dim entry,
    # not a flip. Source of the entries: POST Query/DimensionsFacts {queryTypeId: 1}
    # (the documented catalog endpoint), entries taken VERBATIM with isSelected=True.
    if all(any(d["name"] == name for lv in body.get("levels", [])
               for d in lv.get("dimensions", [])) for name in ADD_DIMS):
        print("NO-OP: both dims already present in the persisted selection", flush=True)
        return 0
    cat = cbi._request("POST", "/datamining/request/Query/DimensionsFacts", token=token,
                       body={"queryTypeId": int(body.get("queryTypeId") or 1)})
    cat_entry: dict = {}
    for lv in cat.get("levels", []):
        for d in lv.get("dimensions", []):
            if d["name"] in ADD_DIMS:
                cat_entry[d["name"]] = (lv["queryLevelId"], d)
    missing = [d for d in ADD_DIMS if d not in cat_entry]
    if missing:
        raise SystemExit("ABORT: target dim(s) absent from the qt1 CATALOG: %s -- STOP AND SURFACE"
                         % missing)
    PRE_IMAGE.write_text(json.dumps(body, indent=1))
    print("pre-image saved: %s" % PRE_IMAGE.name, flush=True)

    expected = set(sel)
    for name, (level_id, entry) in cat_entry.items():
        target_level = next((lv for lv in body.get("levels", [])
                             if lv.get("queryLevelId") == level_id), None)
        if target_level is None:
            raise SystemExit("ABORT: enriched body has no level %s for %r -- STOP AND SURFACE"
                             % (level_id, name))
        add = json.loads(json.dumps(entry))
        add["isSelected"] = True
        ords = [d.get("ordinal", 0) for d in target_level["dimensions"]]
        add["ordinal"] = (max(ords) + 1) if ords else 0  # append, never perturb existing order
        target_level["dimensions"].append(add)
        expected.add((level_id, name))
    cbi._request("PUT", "/datamining/request/v1/template/", token=token,
                 body=build_post_body(body))
    print("update PUT issued (in-place; PUT returns no id -- the GET diff below is the verify)",
          flush=True)

    after = fetch_enriched(token)
    POST_IMAGE.write_text(json.dumps(after, indent=1))
    got = set(selection(after))
    print("post-amendment selection (%d dims): %s" % (len(got), json.dumps(sorted(got))), flush=True)
    delta_added = got - set(sel)
    delta_lost = set(sel) - got
    print("delta: added=%s lost=%s" % (sorted(delta_added), sorted(delta_lost)), flush=True)
    ok = (got == expected) and not delta_lost
    print("VERDICT: %s" % ("PASS -- exactly the two flips, nothing lost"
                           if ok else "FAIL -- unexpected delta; pre-image available for --rollback"),
          flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
