"""MDPF_TAXSMA TX-r-3 -- the ACTIVATION BLAST RADIUS, measured: which of the Gold function's shaped documents
change when Tax turns ON, field by field.

Two full builds in one process, both `dry_run` (ZERO S3 writes; the bodies are collected in memory):
  OFF  the capability unconfigured, exactly as deployed today (Tax DISABLED);
  ON   the capability configured, the Tax prelude run on the live custodian sources with IN-MEMORY stores.

The workbook rows are NOT in the repository (account numbers are private). Pass a local JSON file:
  {"rows": [[index, account_number_or_null, ria_or_null, strategy, aum_mn, traded], ...]}

Usage, from the workspace root:
  py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/4.0.0_SA_CRO/probes/tx_r_3_blast_radius.py \
      --sheet <local sheet json> [--out <local dir for the two body sets>]

Prints one line per document (IDENTICAL or CHANGED with its changed top-level fields and leaf count), then the
headline values before and after. Process-time fields are excluded from the comparison and named in the output."""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime

ROOT = os.getcwd()
for _p in ("data/mdpf/scripts/gold", "data/mdpf/scripts/silver"):
    sys.path.insert(0, os.path.join(ROOT, *_p.split("/")))

import mdpf_gold_consolidator as gc  # noqa: E402
import taxsma_assets as assets  # noqa: E402
import taxsma_membership as membership  # noqa: E402
import taxsma_reconcile as reconcile  # noqa: E402
import taxsma_sources as sources  # noqa: E402
import taxsma_workbook as silver  # noqa: E402

PROCESS_TIME_FIELDS = ("generated_at", "process_time", "last_updated", "source_vintage_age_hours")


def _body(rows, observed_at):
    out = []
    for n, acct, ria, strategy, aum, traded in rows:
        biz = {c: None for c in silver.BUSINESS_COLUMNS}
        biz.update({"Index": n, "Account Number": acct, "RIA": ria, "Traded": traded, "AUM (Mn)": aum,
                    "Strategy": strategy})
        out.append({"row_number": n + 1, "row_kind": "ACCOUNT_SLOT", "other_business_cells_present": True,
                    "business": biz})
    env = {"schema_version": "0.6.0", "snapshot_id": "snap-" + observed_at[:10], "site_id": "s", "item_id": "i",
           "sheet": "Sheet1", "etag": "e", "source_modified_at": observed_at, "observed_at": observed_at,
           "used_rows": len(out) + 1, "account_slot_count": len(out), "header_fingerprint": "hf", "complete": True,
           "rows": out}
    return json.dumps(env, sort_keys=True, separators=(",", ":")).encode("utf-8")


def tax_result(rows, history_days):
    """The prelude on live sources with in-memory stores: one run per history day (knowledge day, session), then
    today's own run on the real clock and calendar. Returns today's result, history merged."""
    stores = {"disposition_stores": {reconcile.FIRM_49F: membership.LocalDispositionStore(),
                                     reconcile.FIRM_COT: membership.LocalDispositionStore()},
              "gold_assets_stores": {reconcile.FIRM_49F: assets.LocalGoldAssetsStore(),
                                     reconcile.FIRM_COT: assets.LocalGoldAssetsStore()}}
    result = None
    for day, session in history_days:
        now = datetime.fromisoformat(day + "T00:00:05+00:00")
        result = gc.run_taxsma_prelude(
            now=lambda now=now: now, gateway_call=lambda timeout_seconds, now=now: _body(rows, now.isoformat()),
            expected_session_fn=lambda dt, session=session: session, sources_loader=sources.load_sources, **stores)
        print("PRELUDE knowledge %s valuation %s: %s %s" % (day, session, result["run_result"],
                                                            result.get("reason_codes")))
    today = gc.run_taxsma_prelude(
        now=gc._now, gateway_call=lambda timeout_seconds: _body(rows, gc._now().isoformat()),
        sources_loader=sources.load_sources, **stores)
    print("PRELUDE today: knowledge %s valuation %s: %s %s%s" % (
        today.get("knowledge_date"), today.get("valuation_date"), today["run_result"], today.get("reason_codes"),
        (" | " + str(today.get("detail"))[:160]) if today.get("detail") else ""))
    return today


def _strip(o):
    if isinstance(o, dict):
        return {k: _strip(v) for k, v in o.items() if k not in PROCESS_TIME_FIELDS}
    if isinstance(o, list):
        return [_strip(v) for v in o]
    return o


def _leaves(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                yield "%s/%s" % (path, k)
            else:
                yield from _leaves(a[k], b[k], "%s/%s" % (path, k))
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from _leaves(x, y, "%s[%d]" % (path, i))
    elif a != b:
        yield path


def build(label, out_dir):
    bodies: dict = {}
    # one trigger label for both builds: the label rides every document's `_provenance`
    manifest = gc.build_all({"kind": "qa-local(blast-radius)"}, dry_run=True,
                            out_dir=os.path.join(out_dir, label), collect_bodies=bodies)
    print("BUILD %s: status=%s errors=%s a4_objects_built=%s tax_prelude=%s" % (
        label, manifest["run"].get("status"), list(manifest.get("errors", {})),
        manifest["run"].get("a4_objects_built"),
        (manifest.get("scopes", {}).get("tax_prelude") or {}).get("run_result")))
    return {k: json.loads(v["body"]) for k, v in bodies.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--history", default="2026-09-29:2026-09-28,2026-09-30:2026-09-29",
                    help="knowledge:session pairs run before today's own run")
    args = ap.parse_args()
    rows = json.load(open(args.sheet, encoding="utf-8"))["rows"]
    out_dir = args.out or tempfile.mkdtemp(prefix="taxsma-blast-")
    history = [tuple(p.split(":")) for p in args.history.split(",") if p]

    off = build("OFF", out_dir)

    result = tax_result(rows, history)
    saved = (gc.taxsma_capability_configured, gc.taxsma_session, gc.taxsma_capability_bearer,
             gc.run_taxsma_prelude, gc.taxsma_snapshot.make_default_gateway_call)
    os.environ.setdefault("TAXSMA_GATEWAY_BASE_URL", "http://unused.invalid")
    import boto3
    gc.taxsma_capability_configured = lambda: True
    gc.taxsma_session = lambda firm=None: boto3.Session()
    gc.taxsma_capability_bearer = lambda session: "unused"
    gc.taxsma_snapshot.make_default_gateway_call = lambda base, bearer: (lambda timeout_seconds: b"")
    gc.run_taxsma_prelude = lambda **kw: result          # the stores build_all hands in are never touched
    try:
        on = build("ON", out_dir)
    finally:
        (gc.taxsma_capability_configured, gc.taxsma_session, gc.taxsma_capability_bearer,
         gc.run_taxsma_prelude, gc.taxsma_snapshot.make_default_gateway_call) = saved

    print("COMPARED %d document(s) OFF vs ON; excluded process-time fields: %s" % (
        len(set(off) | set(on)), ", ".join(PROCESS_TIME_FIELDS)))
    changed = 0
    for key in sorted(set(off) | set(on)):
        if key not in off or key not in on:
            print("  %-70s PRESENT ON ONE SIDE ONLY (off=%s on=%s)" % (key, key in off, key in on))
            changed += 1
            continue
        leaves = list(_leaves(_strip(off[key]), _strip(on[key])))
        if not leaves:
            print("  %-70s IDENTICAL" % key)
            continue
        changed += 1
        tops = sorted({p.split("/")[1].split("[")[0] for p in leaves})
        print("  %-70s CHANGED %d leaf path(s); top-level: %s" % (key, len(leaves), ", ".join(tops)))
    print("RESULT: %d of %d document(s) change when Tax turns ON" % (changed, len(set(off) | set(on))))

    def _last(v):
        return v[-1] if isinstance(v, list) and v else v

    for key in sorted(set(off) & set(on)):
        a, b = off[key], on[key]
        if "aggregate-aua-timeseries" in key:
            print("  HEADLINE %s: opal_aggregate_aua %s -> %s | tax_additive_aua %s | aggregate_basis %s" % (
                key, _last(a.get("opal_aggregate_aua")), _last(b.get("opal_aggregate_aua")),
                _last(b.get("tax_additive_aua")), b.get("aggregate_basis")))
        elif "aum-metrics" in key:
            print("  HEADLINE %s: total.aum %s -> %s | tax_additive_aum %s" % (
                key, (a.get("total") or {}).get("aum"), (b.get("total") or {}).get("aum"),
                (b.get("total") or {}).get("tax_additive_aum")))
        elif "category-views" in key:
            na, nb = a.get("nodes") or {}, b.get("nodes") or {}
            print("  HEADLINE %s: total %s -> %s | SMA %s -> %s | Client %s -> %s" % (
                key, (a.get("sums") or {}).get("total_aua"), (b.get("sums") or {}).get("total_aua"),
                (na.get("SMA") or {}).get("aum"), (nb.get("SMA") or {}).get("aum"),
                (na.get("Client") or {}).get("aum"), (nb.get("Client") or {}).get("aum")))
    print("bodies: %s" % out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
