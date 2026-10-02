"""Round 28 IB-pr-281 builder (worker 0.9.0_WK_IRPT_BCKEND~101): build ONE real READY Analysis report into an ExportBundle and
a print query through the NEW retained-export path, locally. READS ONLY: DynamoDB get/query (irpt-requests, irpt-jobs) and S3
get_object on the retained report. Nothing is persisted, dispatched, minted, submitted or uploaded.

Usage (repo root): python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P/checks/r28/build_analysis_export_r28.py
Writes deliverables/0.9.0_WK_IRPT_BCKEND~101/{analysis_export_bundle_R28.json,ANALYSIS_EXPORT_R28.json}.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path(os.getcwd()).resolve()
PK = ROOT / "infra/aws/lambda/investor-reporting"
for sub in ("lib", "infra/aws/lambda/investor-reporting/export", "infra/aws/lambda/investor-reporting/reports",
            "infra/aws/lambda/investor-reporting/_render_identity", "infra/aws/lambda/investor-reporting/_keys"):
    sys.path.insert(0, str(ROOT / sub))
os.environ.setdefault("IRPT_DIRECTORY_BUCKET_MAP", "{}")
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")

import boto3  # noqa: E402
import bundle as bundle_mod  # noqa: E402
import handler as handler_mod  # noqa: E402
import package as package_mod  # noqa: E402
import retained_export as rx  # noqa: E402
from composition import build_retained_repositories  # noqa: E402
from opal_naming import reporting_destination, reporting_policy  # noqa: E402

TENANT = "cottonwood"
OUT = ROOT / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~101"
PRINCIPAL = {"firm_id": TENANT, "principal_id": "local-lister@opal.agent", "principal_class": "OPAL_GLOBAL",
             "advisor_id": None, "home_firm_id": TENANT}


def repos(table, s3, authorize):
    return build_retained_repositories(table, s3, authorize, lambda k, r: True, reporting_policy=reporting_policy,
                                       reporting_destination=reporting_destination).reports


def main():
    table = boto3.resource("dynamodb").Table("irpt-requests")
    s3 = boto3.client("s3")
    jobs = boto3.client("dynamodb")
    # 1. LIST the retained ANALYSIS reports through the repository (current-firm authorizer, read only).
    lister = repos(table, s3, lambda p, o: o.get("firm_id") == TENANT)
    refs, cursor = [], None
    while True:
        page = lister.list(PRINCIPAL, "ANALYSIS", cursor=cursor, limit=100, data_firm=TENANT)
        refs += page["items"]
        cursor = page["next_cursor"]
        if not cursor:
            break
    print("retained ANALYSIS reports listed: %d" % len(refs))
    # 2. Pick the first whose request is READY on the job row and whose receipt names exactly this report.
    chosen = None
    for ref in sorted(refs, key=lambda r: r["report_id"]):
        got = lister.get(PRINCIPAL, ref["report_id"], ref["revision"], data_firm=TENANT)
        request_id = got["report"]["request_ref"]["request_id"]
        row = jobs.get_item(TableName="irpt-jobs", Key={"tenant": {"S": TENANT}, "job": {"S": request_id}},
                            ConsistentRead=True).get("Item")
        state = row["state"]["S"] if row else None
        detail = json.loads(row["job_detail"]["S"]) if row and "job_detail" in row else {}
        print("  %s request %s state %s receipt-matches %s" % (
            ref["report_id"][:12], request_id[:12], state,
            detail.get("report_id") == ref["report_id"] and detail.get("revision") == ref["revision"]))
        if chosen is None and state == "READY" and detail.get("report_id") == ref["report_id"] \
                and detail.get("revision") == ref["revision"]:
            chosen = (ref, got, request_id)
    if chosen is None:
        sys.exit("no retained READY Analysis report with a matching receipt")
    ref, got, request_id = chosen
    item = lister.index.get(TENANT, "REPORT#%s#%s" % (ref["report_id"], ref["revision"]))
    # The reader is the report's own owner: every retained Analysis report here is prospect-owned (no accounts), and the
    # export authorizer admits a prospect-owned report only to the identity that owns it.
    owner = item["owner"]
    reader = {"firm_id": TENANT, **{f: owner.get(f) for f in ("principal_id", "principal_class", "advisor_id",
                                                              "home_firm_id")}}
    authorize = rx.authorizer(reader, [str(a) for a in owner["account_ids"]])
    reports = repos(table, s3, authorize)
    body = {"authorized_report_revisions": [{"report_id": ref["report_id"], "revision": ref["revision"]}]}
    resolved = rx.resolve(body, reports=reports, principal=reader, tenant=TENANT, authorize=authorize)
    assert resolved["kind"] == "ANALYSIS" and resolved["request_id"] == request_id
    report = resolved["report"]
    export_revision = "exr_" + "0" * 24
    # 4. The bundle, frozen locally (persist=False, dispatch_render=False): package facts from the portal checkout.
    pkg = package_mod.load(str(ROOT / "portal"))
    sections, seen = [], set()
    for s in report["sections"]:
        if s["section_id"] not in seen:
            seen.add(s["section_id"])
            sections.append(s["section_id"])
    # The narrative packet is not built for an Analysis report (narrative_submit.cutoff_for needs a Performance window);
    # a deterministic local reference over the report's own identity stands in. Recorded as a surprise row.
    nsha = bundle_mod.digest({"analysis_export": "no narrative packet built", "report_id": ref["report_id"],
                              "revision": ref["revision"]})
    narrative_ref = {"packet_id": "NP-" + nsha[:32], "revision": export_revision, "sha256": nsha}
    submitted = handler_mod.submit_export(
        tenant=TENANT, generation_id=export_revision, export_revision=export_revision,
        report_revisions=[resolved["row"]], selected_sections=sections, narrative_packet_ref=narrative_ref,
        versions={"template_version": "analysis-portrait-letter", "renderer_version": pkg["package_version"],
                  "disclosure_version": package_mod.contract_version_of(pkg)},
        render_options={"orientation": "PORTRAIT", "page_size": "LETTER", "brand_revision": "opal-fallback"},
        package=pkg, report_kind="analysis", persist=False, dispatch_render=False)
    bundle = submitted["bundle"]
    bundle_mod.validate(bundle)
    try:
        stamped = rx.render_grant(resolved, principal=reader, tenant=TENANT, bundle_id=submitted["bundle_sha256"],
                                  export_revision=export_revision)
        print("render grant built")
    except rx.ExportSubmitRefused as exc:
        # A prospect-owned report holds no accounts and grant.build requires some (surprise row W101-S1): the print query
        # is built over the SAME pins the grant would carry, from a grant-shaped record. Nothing is written.
        print("render grant refused: %s" % exc)
        stamped = {"bundle_id": submitted["bundle_sha256"], "firm_id": TENANT, "revision": export_revision,
                   "pinned_ids": rx.analysis_pins(resolved)}
    query = rx.print_query(stamped, report)
    assert query["kind"] == "analysis" and query["report"] == ref["report_id"]
    OUT.mkdir(parents=True, exist_ok=True)
    bundle_path = OUT / "analysis_export_bundle_R28.json"
    bundle_path.write_text(json.dumps(bundle, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    blob = item["blob"]
    rec = {"report_ref": {"bucket": blob["bucket"], "key": blob["key"], "report_id": ref["report_id"],
                          "revision": ref["revision"]},
           "request_status": "READY",
           "bundle_file": bundle_path.relative_to(ROOT).as_posix(),
           "print_query": query}
    (OUT / "ANALYSIS_EXPORT_R28.json").write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("OK: report %s rev %s; %d sections selected of %d; kind %s" % (
        ref["report_id"], ref["revision"][:12], len(sections), len(report["sections"]), query["kind"]))


if __name__ == "__main__":
    main()
